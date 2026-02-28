import React from 'react';
import HeroGreeting from './HeroGreeting';
import ChatInputBox from './ChatInputBox';
import { SearchStatus } from '../app/page';

interface ChatPaneProps {
    status: SearchStatus;
    answer: string | null;
    userQuery: string;
    onSendMessage: (query: string) => void;
}

export default function ChatPane({ status, answer, userQuery, onSendMessage }: ChatPaneProps) {
    return (
        <div className="flex-1 h-full flex flex-col relative bg-origin-bg items-center pt-16 p-8 overflow-y-auto pb-32">
            {status === 'idle' && !answer && (
                <div className="flex-1 flex items-center justify-center -mt-32">
                    <HeroGreeting />
                </div>
            )}

            {status !== 'idle' && (
                <div className="max-w-3xl w-full flex flex-col gap-6">
                    {/* User Query Bubble */}
                    <div className="self-end bg-origin-text text-white px-6 py-4 rounded-2xl rounded-tr-sm max-w-[80%] shadow-sm">
                        <p className="text-lg">{userQuery}</p>
                    </div>

                    {/* Loading State or Answer Bubble */}
                    <div className="self-start w-full">
                        {(status === 'searching' || status === 'generating') && (
                            <div className="flex items-center gap-3 text-origin-text/70 mt-2">
                                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-origin-text"></div>
                                <span>{status === 'searching' ? 'Searching tax code...' : 'Generating answer...'}</span>
                            </div>
                        )}

                        {status === 'error' && (
                            <div className="text-red-500 mt-2">
                                An error occurred while processing your query.
                            </div>
                        )}

                        {answer && (
                            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 text-origin-text leading-relaxed whitespace-pre-wrap mt-2">
                                {answer}
                            </div>
                        )}
                    </div>
                </div>
            )}

            <ChatInputBox onSendMessage={onSendMessage} disabled={status === 'searching' || status === 'generating'} />
        </div>
    );
}
