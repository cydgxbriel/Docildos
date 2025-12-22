import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  timestamp?: Date;
  children?: React.ReactNode;
}

export function ChatMessage({ role, content, timestamp, children }: ChatMessageProps) {
  const isAssistant = role === "assistant";

  return (
    <div
      className={cn(
        "flex gap-3 animate-slide-up",
        isAssistant ? "flex-row" : "flex-row-reverse"
      )}
    >
      <div
        className={cn(
          "flex-shrink-0 w-9 h-9 rounded-full flex items-center justify-center",
          isAssistant
            ? "bg-primary text-primary-foreground"
            : "bg-chocolate text-accent-foreground"
        )}
      >
        {isAssistant ? <Bot className="w-5 h-5" /> : <User className="w-5 h-5" />}
      </div>

      <div
        className={cn(
          "flex flex-col gap-2 max-w-[75%]",
          isAssistant ? "items-start" : "items-end"
        )}
      >
        <div
          className={cn(
            "px-4 py-3 rounded-2xl shadow-card",
            isAssistant
              ? "bg-card rounded-tl-md"
              : "bg-primary text-primary-foreground rounded-tr-md"
          )}
        >
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{content}</p>
        </div>

        {children && <div className="w-full">{children}</div>}

        {timestamp && (
          <span className="text-xs text-muted-foreground px-1">
            {timestamp.toLocaleTimeString("pt-BR", {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </span>
        )}
      </div>
    </div>
  );
}
