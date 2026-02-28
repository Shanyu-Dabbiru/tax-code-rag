import React from 'react';

export interface SourceDocumentData {
    id: string;
    section_number: string;
    title?: string;
    text: string;
}

export default function SourceDocument({ doc }: { doc: SourceDocumentData }) {
    return (
        <div className="flex flex-col gap-2 p-5 mb-4 rounded-lg bg-origin-bg border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-origin-accent text-lg">
                {doc.section_number}
            </h3>
            {doc.title && (
                <div className="text-sm font-medium text-origin-text">
                    {doc.title}
                </div>
            )}
            <div className="text-sm text-origin-text/90 whitespace-pre-wrap leading-relaxed mt-1">
                {doc.text}
            </div>
        </div>
    );
}
