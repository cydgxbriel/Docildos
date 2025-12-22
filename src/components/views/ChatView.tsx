import { useState, useRef, useEffect } from "react";
import { ChatMessage } from "@/components/chat/ChatMessage";
import { ChatInput } from "@/components/chat/ChatInput";
import { QuickActions } from "@/components/chat/QuickActions";
import { OrderCard } from "@/components/chat/OrderCard";
import { RecipeCard } from "@/components/chat/RecipeCard";
import { StatsCard } from "@/components/dashboard/StatsCard";
import { Package, Truck, Clock, AlertTriangle } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  cards?: Array<{
    type: "order" | "recipe" | "stats";
    data: any;
  }>;
}

// Sample data
const sampleOrder = {
  id: "001",
  cliente: "Nicole Silva",
  items: [
    { name: "Chocotone", quantity: 2, variant: "500g recheado" },
    { name: "Panetone", quantity: 1, variant: "300g tradicional" },
  ],
  status: "novo" as const,
  dataEntrega: new Date(Date.now() + 86400000),
  horario: "15:00",
  local: "Rua das Flores, 123",
};

const sampleRecipe = {
  id: "001",
  name: "Panetone 500g Recheado",
  description: "Panetone artesanal com recheio de chocolate belga",
  prepTime: 180,
  yield: "2 unidades",
  estimatedCost: 28.5,
  ingredients: [
    { name: "Farinha", quantity: "500", unit: "g" },
    { name: "Açúcar", quantity: "150", unit: "g" },
    { name: "Manteiga", quantity: "100", unit: "g" },
    { name: "Ovos", quantity: "4", unit: "un" },
    { name: "Chocolate", quantity: "200", unit: "g" },
    { name: "Leite", quantity: "200", unit: "ml" },
  ],
};

const initialMessages: Message[] = [
  {
    id: "1",
    role: "assistant",
    content:
      "Olá! 👋 Sou sua assistente de confeitaria. Posso ajudar com pedidos, agenda de entregas, receitas, estoque e muito mais. O que você precisa hoje?",
    timestamp: new Date(Date.now() - 60000),
  },
];

export function ChatView() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      let responseContent = "";
      let cards: Message["cards"] = undefined;

      if (content.toLowerCase().includes("pedido")) {
        responseContent =
          "Aqui está o pedido mais recente que encontrei. Você pode atualizar o status usando os botões abaixo:";
        cards = [{ type: "order", data: sampleOrder }];
      } else if (
        content.toLowerCase().includes("receita") ||
        content.toLowerCase().includes("ficha")
      ) {
        responseContent =
          "Encontrei a ficha técnica que você pediu! Veja os detalhes abaixo:";
        cards = [{ type: "recipe", data: sampleRecipe }];
      } else if (content.toLowerCase().includes("hoje")) {
        responseContent =
          "Aqui está o resumo do dia. Você tem pedidos para entregar e alguns precisam de atenção:";
        cards = [{ type: "stats", data: null }];
      } else {
        responseContent =
          "Entendi! Deixa eu processar isso para você. Você pode usar os atalhos abaixo para ações rápidas, ou me dizer mais detalhes sobre o que precisa.";
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: responseContent,
        timestamp: new Date(),
        cards,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1000);
  };

  const handleQuickAction = (actionId: string) => {
    const actionMessages: Record<string, string> = {
      "pedidos-hoje": "Me mostra os pedidos de hoje",
      "entregas-amanha": "O que tem para entregar amanhã?",
      "lista-compras": "Gerar lista de compras para os próximos pedidos",
      cardapio: "Me mostra o cardápio completo",
      estoque: "Qual o status do estoque?",
      sugestoes: "Me dá sugestões de organização para hoje",
    };

    const message = actionMessages[actionId];
    if (message) {
      handleSend(message);
    }
  };

  const handleOrderStatusChange = (orderId: string, newStatus: any) => {
    const statusLabels: Record<string, string> = {
      producao: "em produção",
      pronto: "como pronto",
      entregue: "como entregue",
    };

    const assistantMessage: Message = {
      id: Date.now().toString(),
      role: "assistant",
      content: `Perfeito! ✅ Pedido #${orderId} foi marcado ${statusLabels[newStatus]}. Precisa de mais alguma coisa?`,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, assistantMessage]);
  };

  return (
    <div className="flex flex-col h-full">
      {/* Stats Header */}
      <div className="p-4 border-b border-border bg-card/50">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <StatsCard
            title="Pedidos Hoje"
            value={8}
            subtitle="3 novos"
            icon={Package}
            variant="primary"
          />
          <StatsCard
            title="Entregas"
            value={5}
            subtitle="2 pendentes"
            icon={Truck}
            variant="default"
          />
          <StatsCard
            title="Em Produção"
            value={3}
            icon={Clock}
            variant="warning"
          />
          <StatsCard
            title="Estoque Baixo"
            value={2}
            subtitle="itens críticos"
            icon={AlertTriangle}
            variant="warning"
          />
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id}>
            <ChatMessage
              role={message.role}
              content={message.content}
              timestamp={message.timestamp}
            >
              {message.cards?.map((card, index) => (
                <div key={index} className="mt-2">
                  {card.type === "order" && (
                    <OrderCard
                      order={card.data}
                      onStatusChange={handleOrderStatusChange}
                    />
                  )}
                  {card.type === "recipe" && <RecipeCard recipe={card.data} />}
                  {card.type === "stats" && (
                    <div className="grid grid-cols-2 gap-2">
                      <StatsCard
                        title="Total Pedidos"
                        value="R$ 1.240"
                        icon={Package}
                        variant="success"
                      />
                      <StatsCard
                        title="Itens"
                        value={12}
                        subtitle="para produzir"
                        icon={Clock}
                      />
                    </div>
                  )}
                </div>
              ))}
            </ChatMessage>
          </div>
        ))}

        {isLoading && (
          <ChatMessage role="assistant" content="">
            <div className="flex gap-1.5 px-4 py-3">
              <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce" />
              <div
                className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce"
                style={{ animationDelay: "0.1s" }}
              />
              <div
                className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce"
                style={{ animationDelay: "0.2s" }}
              />
            </div>
          </ChatMessage>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      <div className="px-4 py-2 border-t border-border bg-background/50">
        <QuickActions onAction={handleQuickAction} />
      </div>

      {/* Input */}
      <ChatInput
        onSend={handleSend}
        onVoiceStart={() => setIsRecording(true)}
        onVoiceStop={() => setIsRecording(false)}
        isRecording={isRecording}
        disabled={isLoading}
      />
    </div>
  );
}
