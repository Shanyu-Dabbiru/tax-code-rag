import React from 'react';
import { MessageSquare, LayoutDashboard, Settings } from 'lucide-react';
import { ThemeToggle } from './ThemeToggle';

export default function SidebarLeft() {
    return (
        <div className="w-64 h-full border-r border-origin-border bg-origin-bg flex flex-col">
            <div className="p-6">
                <h1 className="text-xl font-bold text-origin-text">Origin Financial</h1>
            </div>
            <nav className="flex-1 px-4 py-2 space-y-2">
                <a href="#" className="flex items-center gap-3 px-3 py-2 text-origin-text hover:bg-origin-panel rounded-md transition-colors">
                    <LayoutDashboard className="w-5 h-5" />
                    Dashboard
                </a>
                <a href="#" className="flex items-center gap-3 px-3 py-2 text-origin-text bg-origin-panel shadow-sm rounded-md transition-colors">
                    <MessageSquare className="w-5 h-5 text-origin-accent" />
                    Recent Chats
                </a>
                <a href="#" className="flex items-center gap-3 px-3 py-2 text-origin-text hover:bg-origin-panel rounded-md transition-colors">
                    <Settings className="w-5 h-5" />
                    Settings
                </a>
            </nav>
            <div className="p-4 border-t border-origin-border flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-origin-primary text-white flex items-center justify-center font-bold">
                        U
                    </div>
                    <span className="text-sm font-medium text-origin-text">User</span>
                </div>
                <ThemeToggle />
            </div>
        </div>
    );
}
