import React from 'react';
import { BookOpen } from 'lucide-react';
import SourceDocument, { SourceDocumentData } from './SourceDocument';

interface SourcesPaneProps {
    sources: SourceDocumentData[];
}

export default function SourcesPane({ sources }: SourcesPaneProps) {
    return (
        <div className="w-96 h-full bg-origin-panel border-l border-origin-border flex flex-col shadow-sm max-w-[33%] shrink-0">
            <div className="p-6 border-b border-origin-border flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-origin-accent" />
                <h2 className="text-lg font-semibold text-origin-text">Retrieved Tax Code</h2>
            </div>
            <div className="flex-1 p-6 overflow-y-auto">
                {sources.length === 0 ? (
                    <div className="text-origin-text/50 text-center mt-10">
                        Ask a question to see retrieved tax code snippets here.
                    </div>
                ) : (
                    sources.map((doc, index) => (
                        <SourceDocument key={doc.id || index} doc={doc} />
                    ))
                )}
            </div>
        </div>
    );
}
