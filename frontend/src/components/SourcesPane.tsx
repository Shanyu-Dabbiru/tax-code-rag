import React from 'react';
import { BookOpen } from 'lucide-react';

export default function SourcesPane() {
    return (
        <div className="w-96 h-full bg-white border-l border-gray-200 flex flex-col shadow-sm">
            <div className="p-6 border-b border-gray-100 flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-origin-accent" />
                <h2 className="text-lg font-semibold text-origin-text">Retrieved Tax Code</h2>
            </div>
            <div className="flex-1 p-6 overflow-y-auto">
                {/* Placeholder for Source Documents */}
                <div className="text-center text-gray-400 mt-10">
                    <p>Sources will appear here after a search.</p>
                </div>
            </div>
        </div>
    );
}
