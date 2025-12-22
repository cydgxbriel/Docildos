import { Button } from "@/components/ui/button";
import {
  Package,
  Calendar,
  ShoppingCart,
  ChefHat,
  Warehouse,
  Sparkles,
} from "lucide-react";

interface QuickActionsProps {
  onAction: (action: string) => void;
}

const actions = [
  { id: "pedidos-hoje", label: "Pedidos de hoje", icon: Package },
  { id: "entregas-amanha", label: "Entregas amanhã", icon: Calendar },
  { id: "lista-compras", label: "Lista de compras", icon: ShoppingCart },
  { id: "cardapio", label: "Ver cardápio", icon: ChefHat },
  { id: "estoque", label: "Estoque", icon: Warehouse },
  { id: "sugestoes", label: "Sugestões IA", icon: Sparkles },
];

export function QuickActions({ onAction }: QuickActionsProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {actions.map((action) => (
        <Button
          key={action.id}
          variant="chip"
          size="chip"
          onClick={() => onAction(action.id)}
          className="gap-1.5"
        >
          <action.icon className="w-3.5 h-3.5" />
          {action.label}
        </Button>
      ))}
    </div>
  );
}
