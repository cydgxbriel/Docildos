import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  MessageCircle,
  Package,
  Calendar,
  ChefHat,
  Warehouse,
  Settings,
  Menu,
  X,
} from "lucide-react";
import { useState } from "react";

interface SidebarProps {
  currentView: string;
  onViewChange: (view: string) => void;
}

const navItems = [
  { id: "chat", label: "Chat", icon: MessageCircle },
  { id: "pedidos", label: "Pedidos", icon: Package },
  { id: "agenda", label: "Agenda", icon: Calendar },
  { id: "receitas", label: "Receitas", icon: ChefHat },
  { id: "estoque", label: "Estoque", icon: Warehouse },
];

export function Sidebar({ currentView, onViewChange }: SidebarProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Mobile Toggle */}
      <Button
        variant="ghost"
        size="icon"
        className="fixed top-4 left-4 z-50 md:hidden"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </Button>

      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-foreground/20 backdrop-blur-sm z-40 md:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 w-64 bg-card border-r border-border transform transition-transform duration-300 ease-in-out md:translate-x-0 md:static",
          isOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="p-6 border-b border-border">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl gradient-warm flex items-center justify-center text-primary-foreground font-display font-bold text-lg">
                B
              </div>
              <div>
                <h1 className="font-display font-bold text-lg text-foreground">
                  Brigadeiros
                </h1>
                <p className="text-xs text-muted-foreground">
                  Gestão Inteligente
                </p>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-1">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  onViewChange(item.id);
                  setIsOpen(false);
                }}
                className={cn(
                  "w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200",
                  currentView === item.id
                    ? "bg-primary text-primary-foreground shadow-warm"
                    : "text-muted-foreground hover:text-foreground hover:bg-secondary"
                )}
              >
                <item.icon className="w-5 h-5" />
                {item.label}
              </button>
            ))}
          </nav>

          {/* Settings */}
          <div className="p-4 border-t border-border">
            <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors">
              <Settings className="w-5 h-5" />
              Configurações
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
