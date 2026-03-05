import React from 'react';
import { render, screen } from '@testing-library/react';
import SourcesPane from '../SourcesPane';
import { SourceDocumentData } from '../SourceDocument';

describe('SourcesPane - Worst Case Scenarios', () => {
    it('handles empty sources array gracefully', () => {
        render(<SourcesPane sources={[]} />);
        expect(screen.getByText('Ask a question to see retrieved tax code snippets here.')).toBeInTheDocument();
    });

    it('renders huge text content without crashing', () => {
        const enormousText = 'Lorem ipsum dolor sit amet '.repeat(10000);
        const hugeSources: SourceDocumentData[] = [
            { id: '2', section_number: 'Sec 1', title: enormousText, text: enormousText },
            { id: undefined as any, section_number: 'Sec 1', title: enormousText, text: enormousText },
        ];

        const { container } = render(<SourcesPane sources={hugeSources} />);

        // Expect no crash, and some text is rendered
        expect(screen.getAllByText(/Lorem ipsum dolor sit amet/)[0]).toBeInTheDocument();
    });

    it('handles malformed data missing standard properties (resilience test)', () => {
        // Simulating bad API response passing through
        const badSources: any[] = [
            { id: null, section_number: null, title: null, text: null },
            { random_field: "Unexpected data" }
        ];

        render(<SourcesPane sources={badSources} />);
        // As long as it doesn't throw and render crashes, it's fairly resilient.
        // It might render empty sections or undefined, but the app stays alive.
        const sections = screen.queryAllByText('Missing Section Number');
        // SourceDocument component uses `doc.section_number`, if it's null it might be empty string or throw depending on how it's coded.
        // Let's verify it survives rendering.
        expect(screen.getByText('Retrieved Tax Code')).toBeInTheDocument();
    });
});
