"use client";

import { useState } from "react";
import SidebarLeft from "../components/SidebarLeft";
import ChatPane from "../components/ChatPane";
import SourcesPane from "../components/SourcesPane";
import { SourceDocumentData } from "../components/SourceDocument";

export type SearchStatus = 'idle' | 'searching' | 'generating' | 'done' | 'error';

export type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceDocumentData[];
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sources, setSources] = useState<SourceDocumentData[]>([]);
  const [status, setStatus] = useState<SearchStatus>('idle');

  const handleSendMessage = async (userQuery: string) => {
    if (!userQuery.trim()) return;

    try {
      const newUserMsg: Message = { id: Math.random().toString(), role: 'user', content: userQuery };
      setMessages((prev) => [...prev, newUserMsg]);
      setStatus('searching');
      setSources([]);

      // Step 1: Retrieval
      const searchRes = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userQuery, top_k: 5 }),
      });

      if (!searchRes.ok) throw new Error("Search failed");
      const searchData = await searchRes.json();

      const retrievedSources = searchData.results.map((r: { chunk_id?: string; section_number: string; title?: string; text: string }) => ({
        id: r.chunk_id || Math.random().toString(),
        section_number: r.section_number,
        title: r.title,
        text: r.text,
      }));

      setSources(retrievedSources);
      setStatus('generating');

      // Step 2: Generation
      const generateRes = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: userQuery,
          contexts: retrievedSources.map((s: SourceDocumentData) => `${s.section_number} - ${s.title}\n${s.text}`),
        }),
      });

      if (!generateRes.ok) throw new Error("Generation failed");
      const generateData = await generateRes.json();

      const newAsstMsg: Message = { id: Math.random().toString(), role: 'assistant', content: generateData.answer, sources: retrievedSources };
      setMessages((prev) => [...prev, newAsstMsg]);
      setStatus('done');

    } catch (error) {
      console.error(error);
      setStatus('error');
    }
  };

  return (
    <main className="flex h-screen w-full overflow-hidden bg-origin-bg font-sans">
      <SidebarLeft />
      <ChatPane status={status} messages={messages} onSendMessage={handleSendMessage} />
      <SourcesPane sources={sources} />
    </main>
  );
}
