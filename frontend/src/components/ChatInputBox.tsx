"use client";

import React, { useState } from 'react';
import { ArrowUp } from 'lucide-react';

export default function ChatInputBox() {
    const [query, setQuery] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Future API logic
        console.log("Submitted:", query);
    };

    return (
        <div className="absolute bottom-8 w-full max-w-3xl px-6 left-1/2 -translate-x-1/2">
            <form onSubmit={handleSubmit} className="relative flex items-center w-full">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask a tax question..."
                    className="w-full bg-transparent border border-gray-300 focus:outline-none focus:ring-1 focus:ring-origin-text text-origin-text rounded-none px-4 py-4 pr-14 shadow-sm"
                />
                <button
                    type="submit"
                    className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-lg bg-origin-text text-white hover:opacity-80 transition-opacity flex items-center justify-center"
                    aria-label="Send message"
                >
                    <ArrowUp size={20} />
                </button>
            </form>
        </div>
    );
}
