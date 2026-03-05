import React from 'react';
import { render, screen } from '@testing-library/react';
import ChatPane from '../ChatPane';
import { Message } from '../../app/page';

describe('ChatPane Component (Worst-Case UI Resilience)', () => {

    // Mock scrollIntoView to prevent jsdom errors
    window.HTMLElement.prototype.scrollIntoView = jest.fn();

    const mockSendMessage = jest.fn();

    it('TC-01: Correctly applies text-wrapping classes for extreme string payloads', () => {
        const extremeWord = "W".repeat(5000);
        const messages: Message[] = [
            { id: '1', role: 'user', content: extremeWord },
            { id: '2', role: 'assistant', content: "This is a normal answer." }
        ];

        render(<ChatPane status="idle" messages={messages} onSendMessage={mockSendMessage} />);

        // Find the user bubble by its continuous text content
        const userBubbleText = screen.getByText(extremeWord);
        const userBubbleContainer = userBubbleText.closest('div.bg-origin-text');

        expect(userBubbleContainer).toBeInTheDocument();
        // Verify that the critical CSS wrapping classes are present!
        expect(userBubbleContainer).toHaveClass('break-words');
        expect(userBubbleContainer).toHaveClass('whitespace-pre-wrap');
        expect(userBubbleContainer).toHaveClass('min-w-0');
    });

    it('TC-02: Preserves and renders full chat history array', () => {
        const messages: Message[] = [
            { id: 'msg-1', role: 'user', content: 'What is tax?' },
            { id: 'msg-2', role: 'assistant', content: 'Tax is a mandatory financial charge.' },
            { id: 'msg-3', role: 'user', content: 'What is a deduction?' },
            { id: 'msg-4', role: 'assistant', content: 'A deduction lowers taxable income.' },
        ];

        render(<ChatPane status="done" messages={messages} onSendMessage={mockSendMessage} />);

        // We verify that all four messages are rendered without being overwritten
        expect(screen.getByText('What is tax?')).toBeInTheDocument();
        expect(screen.getByText('Tax is a mandatory financial charge.')).toBeInTheDocument();
        expect(screen.getByText('What is a deduction?')).toBeInTheDocument();
        expect(screen.getByText('A deduction lowers taxable income.')).toBeInTheDocument();
    });

    it('TC-03: Displays spinner correctly when status is searching or generating', () => {
        const messages: Message[] = [
            { id: '1', role: 'user', content: 'Tell me a joke about taxes.' }
        ];

        const { rerender } = render(<ChatPane status="searching" messages={messages} onSendMessage={mockSendMessage} />);
        expect(screen.getByText('Searching tax code...')).toBeInTheDocument();

        rerender(<ChatPane status="generating" messages={messages} onSendMessage={mockSendMessage} />);
        expect(screen.getByText('Generating answer...')).toBeInTheDocument();
    });
});
