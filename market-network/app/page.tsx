import NetworkGraph from "@/components/NetworkGraph";

export default function Home() {
  return (
    <main className="min-h-screen p-4">
      <div className="max-w-7xl mx-auto">
        <header className="mb-6">
          <h1 className="text-3xl font-bold mb-2">Polymarket Event Network</h1>
          <p className="text-gray-400 text-sm">
            Events connected by trader overlap (3%+ shared traders)
          </p>
        </header>
        
        <NetworkGraph />
        
        <footer className="mt-6 text-center text-gray-500 text-xs">
          Data: Gamma API + PNL Subgraph | 100 events, 633 connections
        </footer>
      </div>
    </main>
  );
}

