import { useState } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { ChatView } from "@/components/views/ChatView";

const Index = () => {
  const [currentView, setCurrentView] = useState("chat");

  return (
    <div className="flex h-screen bg-background">
      <Sidebar currentView={currentView} onViewChange={setCurrentView} />
      
      <main className="flex-1 flex flex-col overflow-hidden md:ml-0">
        {currentView === "chat" && <ChatView />}
        
        {currentView !== "chat" && (
          <div className="flex-1 flex items-center justify-center p-8">
            <div className="text-center">
              <div className="w-20 h-20 mx-auto mb-4 rounded-2xl gradient-warm flex items-center justify-center">
                <span className="text-4xl">🎂</span>
              </div>
              <h2 className="font-display text-2xl font-bold text-foreground mb-2">
                {currentView === "pedidos" && "Pedidos"}
                {currentView === "agenda" && "Agenda de Entregas"}
                {currentView === "receitas" && "Receitas & Cardápio"}
                {currentView === "estoque" && "Controle de Estoque"}
              </h2>
              <p className="text-muted-foreground max-w-sm">
                Use o chat para gerenciar {currentView}. Digite ou fale o que precisa e a IA vai te ajudar!
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Index;
