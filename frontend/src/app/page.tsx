"use client";

import { useState } from "react";
import SidebarLeft from "../components/SidebarLeft";
import ChatPane from "../components/ChatPane";
import SourcesPane from "../components/SourcesPane";
import { SourceDocumentData } from "../components/SourceDocument";

export type SearchStatus = 'idle' | 'searching' | 'generating' | 'done' | 'error';

export default function Home() {
  const [query, setQuery] = useState("");
  const [sources, setSources] = useState<SourceDocumentData[]>([]);
  const [answer, setAnswer] = useState<string | null>(null);
  const [status, setStatus] = useState<SearchStatus>('idle');

  const handleSendMessage = async (userQuery: string) => {
    if (!userQuery.trim()) return;

    try {
      setQuery(userQuery);
      setStatus('searching');
      setSources([]);
      setAnswer(null);

      // Step 1: Retrieval
      const searchRes = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userQuery, top_k: 5 }),
      });

      if (!searchRes.ok) throw new Error("Search failed");
      const searchData = await searchRes.json();

      const retrievedSources = searchData.results.map((r: any) => ({
        id: r.chunk_id || Math.random().toString(),
        section_number: r.section_number,
        title: r.title,
        text: r.text,
      }));

      setSources(retrievedSources);
      setStatus('generating');

      // Step 2: Generation
      const generateRes = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: userQuery,
          contexts: retrievedSources.map((s: SourceDocumentData) => `${s.section_number} - ${s.title}\n${s.text}`),
        }),
      });

      if (!generateRes.ok) throw new Error("Generation failed");
      const generateData = await generateRes.json();

      setAnswer(generateData.answer);
      setStatus('done');

    } catch (error) {
      console.error(error);
      setStatus('error');
    }
  };

  return (
    <main className="flex h-screen w-full overflow-hidden bg-origin-bg font-sans">
      <SidebarLeft />
      <ChatPane status={status} answer={answer} onSendMessage={handleSendMessage} userQuery={query} />
      <SourcesPane sources={sources} />
    </main>
  );
}
