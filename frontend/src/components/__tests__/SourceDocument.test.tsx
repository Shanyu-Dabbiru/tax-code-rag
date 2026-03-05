import React from 'react';
import { render, screen } from '@testing-library/react';
import SourceDocument, { SourceDocumentData } from '../SourceDocument';

describe('SourceDocument Component - Resilience Tests', () => {
    it('TC-04: Renders correctly with all valid fields', () => {
        const validDoc: SourceDocumentData = {
            id: '123',
            section_number: '26 U.S.C. § 162',
            title: 'Trade or business expenses',
            text: 'There shall be allowed as a deduction all the ordinary and necessary expenses paid or incurred during the taxable year...'
        };

        render(<SourceDocument doc={validDoc} />);

        expect(screen.getByText('26 U.S.C. § 162')).toBeInTheDocument();
        expect(screen.getByText('Trade or business expenses')).toBeInTheDocument();
        expect(screen.getByText(/allowed as a deduction/i)).toBeInTheDocument();
    });

    it('TC-05: Renders correctly when optional title is missing', () => {
        const noTitleDoc: SourceDocumentData = {
            id: '456',
            section_number: 'Sec 101',
            text: 'Random tax code text.'
        };

        render(<SourceDocument doc={noTitleDoc} />);

        expect(screen.getByText('Sec 101')).toBeInTheDocument();
        expect(screen.getByText('Random tax code text.')).toBeInTheDocument();
        // Ensure no empty title div is rendered if there's no title
        const titleElements = screen.queryAllByText(/text-sm font-medium/);
        expect(titleElements.length).toBe(0);
    });

    it('TC-06: Does not crash when extreme HTML/script injection is passed as text (XSS test via text rendering)', () => {
        const maliciousDoc: SourceDocumentData = {
            id: '789',
            section_number: 'Hack',
            title: 'Malicious',
            text: '<script>alert("hacked!")</script><img src=x onerror=alert(1)>'
        };

        render(<SourceDocument doc={maliciousDoc} />);

        // React should escape the tags automatically and render them as raw text
        expect(screen.getByText('<script>alert("hacked!")</script><img src=x onerror=alert(1)>')).toBeInTheDocument();
        // Verify that the actual script tag hasn't been executed or injected into DOM structure
        expect(document.scripts.length).toBe(0);
    });
});
