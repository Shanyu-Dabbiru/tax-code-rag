import React from 'react';
import HeroGreeting from './HeroGreeting';
import ChatInputBox from './ChatInputBox';

export default function ChatPane() {
    return (
        <div className="flex-1 h-full flex flex-col relative bg-origin-bg items-center justify-center">
            <HeroGreeting />
            <ChatInputBox />
        </div>
    );
}
