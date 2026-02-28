import SidebarLeft from "../components/SidebarLeft";
import ChatPane from "../components/ChatPane";
import SourcesPane from "../components/SourcesPane";

export default function Home() {
  return (
    <main className="flex h-screen w-full overflow-hidden bg-origin-bg font-sans">
      <SidebarLeft />
      <ChatPane />
      <SourcesPane />
    </main>
  );
}
