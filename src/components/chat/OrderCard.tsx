import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Package, Clock, MapPin, Check, ChefHat } from "lucide-react";
import { cn } from "@/lib/utils";

interface OrderItem {
  name: string;
  quantity: number;
  variant?: string;
}

interface Order {
  id: string;
  cliente: string;
  items: OrderItem[];
  status: "novo" | "producao" | "pronto" | "entregue";
  dataEntrega: Date;
  horario?: string;
  local?: string;
}

const statusConfig = {
  novo: {
    label: "Novo",
    color: "bg-warning/20 text-warning border-warning/30",
    icon: Clock,
  },
  producao: {
    label: "Em Produção",
    color: "bg-primary/20 text-primary border-primary/30",
    icon: ChefHat,
  },
  pronto: {
    label: "Pronto",
    color: "bg-success/20 text-success border-success/30",
    icon: Check,
  },
  entregue: {
    label: "Entregue",
    color: "bg-muted text-muted-foreground border-border",
    icon: Package,
  },
};

interface OrderCardProps {
  order: Order;
  onStatusChange?: (orderId: string, newStatus: Order["status"]) => void;
}

export function OrderCard({ order, onStatusChange }: OrderCardProps) {
  const config = statusConfig[order.status];
  const StatusIcon = config.icon;

  const formatDate = (date: Date) => {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    if (date.toDateString() === today.toDateString()) {
      return "Hoje";
    } else if (date.toDateString() === tomorrow.toDateString()) {
      return "Amanhã";
    }
    return date.toLocaleDateString("pt-BR", {
      weekday: "short",
      day: "numeric",
      month: "short",
    });
  };

  return (
    <div className="bg-card rounded-xl p-4 shadow-card border border-border/50 animate-fade-in">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div>
          <h4 className="font-semibold text-foreground">{order.cliente}</h4>
          <p className="text-xs text-muted-foreground">Pedido #{order.id}</p>
        </div>
        <Badge
          variant="outline"
          className={cn("gap-1 text-xs font-medium border", config.color)}
        >
          <StatusIcon className="w-3 h-3" />
          {config.label}
        </Badge>
      </div>

      <div className="space-y-2 mb-3">
        {order.items.map((item, index) => (
          <div
            key={index}
            className="flex items-center gap-2 text-sm text-foreground"
          >
            <span className="w-6 h-6 rounded-full bg-secondary flex items-center justify-center text-xs font-medium text-secondary-foreground">
              {item.quantity}
            </span>
            <span>
              {item.name}
              {item.variant && (
                <span className="text-muted-foreground"> · {item.variant}</span>
              )}
            </span>
          </div>
        ))}
      </div>

      <div className="flex items-center gap-4 text-xs text-muted-foreground mb-3">
        <div className="flex items-center gap-1">
          <Clock className="w-3.5 h-3.5" />
          <span>
            {formatDate(order.dataEntrega)}
            {order.horario && ` às ${order.horario}`}
          </span>
        </div>
        {order.local && (
          <div className="flex items-center gap-1">
            <MapPin className="w-3.5 h-3.5" />
            <span>{order.local}</span>
          </div>
        )}
      </div>

      {order.status !== "entregue" && (
        <div className="flex gap-2">
          {order.status === "novo" && (
            <Button
              variant="chip"
              size="chip"
              onClick={() => onStatusChange?.(order.id, "producao")}
            >
              Iniciar Produção
            </Button>
          )}
          {order.status === "producao" && (
            <Button
              variant="chip"
              size="chip"
              onClick={() => onStatusChange?.(order.id, "pronto")}
            >
              Marcar Pronto
            </Button>
          )}
          {order.status === "pronto" && (
            <Button
              variant="chip"
              size="chip"
              onClick={() => onStatusChange?.(order.id, "entregue")}
            >
              Confirmar Entrega
            </Button>
          )}
        </div>
      )}
    </div>
  );
}
