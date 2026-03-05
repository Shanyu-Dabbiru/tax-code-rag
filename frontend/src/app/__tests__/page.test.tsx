import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Page from '../page';

// Mock the scrollIntoView on jsdom
window.HTMLElement.prototype.scrollIntoView = jest.fn();

describe('Page - Worst Case Orchestration Scenarios', () => {
    let mockFetch: jest.Mock;

    beforeEach(() => {
        // Reset and mock global fetch
        mockFetch = jest.fn();
        global.fetch = mockFetch;
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    it('handles a 500 Internal Server Error from the /search endpoint cleanly', async () => {
        mockFetch.mockResolvedValueOnce({
            ok: false,
            json: async () => ({ detail: 'Database Timeout Error (Qdrant Unreachable)' }),
        });

        render(<Page />);
        const input = screen.getByPlaceholderText('Ask a tax question...');
        const submitBtn = screen.getByRole('button', { name: /send message/i });

        fireEvent.change(input, { target: { value: 'What are crypto taxes?' } });
        fireEvent.click(submitBtn);

        // Expect the Searching status initially
        expect(screen.getByText('Searching tax code...')).toBeInTheDocument();

        // Wait for the error state
        await waitFor(() => {
            expect(screen.getByText('Database Timeout Error (Qdrant Unreachable)')).toBeInTheDocument();
        });

        // The second endpoint (/generate) should NOT be called
        expect(mockFetch).toHaveBeenCalledTimes(1);
    });

    it('handles a 500 Error from the /generate endpoint after a successful /search', async () => {
        // First call: /search (Success)
        mockFetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ results: [{ chunk_id: '1', section_number: 'Sec 1', title: 'A', text: 'B' }] }),
        });

        // Second call: /generate (Failure)
        mockFetch.mockResolvedValueOnce({
            ok: false,
            json: async () => ({ detail: 'LLM Generation Failed' }),
        });

        render(<Page />);
        const input = screen.getByPlaceholderText('Ask a tax question...');
        fireEvent.change(input, { target: { value: 'Crypto' } });
        fireEvent.click(screen.getByRole('button', { name: /send message/i }));

        // Wait for the error text to appear
        await waitFor(() => {
            expect(screen.getByText('LLM Generation Failed')).toBeInTheDocument();
        });

        // We should also verify that the retrieved source from step 1 is still rendered!
        expect(screen.getByText('Retrieved Tax Code')).toBeInTheDocument();
        // Since it's in the state, it should persist through the failure.
        expect(screen.getByText('Sec 1')).toBeInTheDocument();
        expect(screen.getByText('A')).toBeInTheDocument();

        expect(mockFetch).toHaveBeenCalledTimes(2);
    });

    it('recovers from an error state when a new valid query is submitted', async () => {
        // Fail the first query
        mockFetch.mockResolvedValueOnce({
            ok: false,
            json: async () => ({ detail: 'First try failed' }),
        });

        render(<Page />);
        const input = screen.getByPlaceholderText('Ask a tax question...');
        fireEvent.change(input, { target: { value: 'Fail me' } });
        fireEvent.click(screen.getByRole('button', { name: /send message/i }));

        await waitFor(() => {
            expect(screen.getByText('First try failed')).toBeInTheDocument();
        });

        // Second query: Should succeed
        mockFetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ results: [] }),
        }).mockResolvedValueOnce({
            ok: true,
            json: async () => ({ answer: 'Second try succeeded' }),
        });

        fireEvent.change(input, { target: { value: 'Succeed now' } });
        fireEvent.click(screen.getByRole('button', { name: /send message/i }));

        // Error message should disappear
        await waitFor(() => {
            expect(screen.queryByText('First try failed')).not.toBeInTheDocument();
        });

        // Answer should appear
        await waitFor(() => {
            expect(screen.getByText('Second try succeeded')).toBeInTheDocument();
        });
    });

    it('handles non-JSON garbage response from /search endpoint (HTML 502 Bad Gateway proxy error)', async () => {
        // Simulating Nginx or Load Balancer returning HTML on a 502 Bad Gateway
        mockFetch.mockResolvedValueOnce({
            ok: false,
            json: async () => { throw new Error("Unexpected token < in JSON at position 0"); }
        });

        render(<Page />);
        fireEvent.change(screen.getByPlaceholderText('Ask a tax question...'), { target: { value: 'What if API returns an HTML page?' } });
        fireEvent.click(screen.getByRole('button', { name: /send message/i }));

        await waitFor(() => {
            expect(screen.getByText('Search failed')).toBeInTheDocument(); // The default error in the code fallback
        });
    });

    it('handles an empty results array from /search gracefully without crashing /generate', async () => {
        // It's entirely possible a query yields 0 results from Qdrant
        mockFetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ results: [] }),
        });

        mockFetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ answer: 'I could not find any tax code matching that, but taxes are mandatory.' }),
        });

        render(<Page />);
        fireEvent.change(screen.getByPlaceholderText('Ask a tax question...'), { target: { value: 'A completely unrelated query' } });
        fireEvent.click(screen.getByRole('button', { name: /send message/i }));

        await waitFor(() => {
            expect(screen.getByText('I could not find any tax code matching that, but taxes are mandatory.')).toBeInTheDocument();
        });

        // Verifying that Generate was called with an empty contexts array
        const generateCall = mockFetch.mock.calls[1][1];
        const bodyObj = JSON.parse(generateCall.body);
        expect(bodyObj.contexts).toEqual([]);
    });
});
