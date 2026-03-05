import React, { useRef, useEffect } from 'react';
import HeroGreeting from './HeroGreeting';
import ChatInputBox from './ChatInputBox';
import { SearchStatus, Message } from '../app/page';

interface ChatPaneProps {
    status: SearchStatus;
    messages: Message[];
    onSendMessage: (query: string) => void;
}

export default function ChatPane({ status, messages, onSendMessage }: ChatPaneProps) {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages, status]);

    return (
        <div className="flex-1 h-full flex flex-col relative bg-origin-bg items-center pt-16 p-8 overflow-y-auto pb-32">
            {messages.length === 0 && (
                <div className="flex-1 flex items-center justify-center -mt-32">
                    <HeroGreeting />
                </div>
            )}

            {messages.length > 0 && (
                <div className="max-w-3xl w-full flex flex-col gap-6">
                    {messages.map((msg) => (
                        <div key={msg.id} className={`w-full flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                            {msg.role === 'user' ? (
                                <div className="bg-origin-text text-white px-6 py-4 rounded-2xl rounded-tr-sm max-w-[80%] shadow-sm min-w-0 break-words whitespace-pre-wrap">
                                    <p className="text-lg">{msg.content}</p>
                                </div>
                            ) : (
                                <div className="bg-white p-6 rounded-2xl rounded-tl-sm w-full shadow-sm border border-gray-100 text-origin-text leading-relaxed min-w-0 break-words whitespace-pre-wrap mt-2">
                                    <p className="text-lg">{msg.content}</p>
                                </div>
                            )}
                        </div>
                    ))}

                    <div className="self-start w-full">
                        {(status === 'searching' || status === 'generating') && (
                            <div className="flex items-center gap-3 text-origin-text/70 mt-2">
                                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-origin-text"></div>
                                <span>{status === 'searching' ? 'Searching tax code...' : 'Generating answer...'}</span>
                            </div>
                        )}

                        {status === 'error' && (
                            <div className="text-red-500 mt-2">
                                An error occurred while processing your query. Please try again.
                            </div>
                        )}
                    </div>
                    <div ref={messagesEndRef} />
                </div>
            )}

            <ChatInputBox onSendMessage={onSendMessage} disabled={status === 'searching' || status === 'generating'} />
        </div>
    );
}
