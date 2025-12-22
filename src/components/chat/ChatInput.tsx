import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Mic, Send, Square } from "lucide-react";
import { cn } from "@/lib/utils";

interface ChatInputProps {
  onSend: (message: string) => void;
  onVoiceStart?: () => void;
  onVoiceStop?: () => void;
  isRecording?: boolean;
  disabled?: boolean;
}

export function ChatInput({
  onSend,
  onVoiceStart,
  onVoiceStop,
  isRecording = false,
  disabled = false,
}: ChatInputProps) {
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage("");
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    // Auto-resize textarea
    const textarea = e.target;
    textarea.style.height = "auto";
    textarea.style.height = Math.min(textarea.scrollHeight, 150) + "px";
  };

  return (
    <div className="flex items-end gap-3 p-4 bg-card/80 backdrop-blur-lg border-t border-border">
      <div className="flex-1 relative">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder="Digite uma mensagem ou use o microfone..."
          disabled={disabled || isRecording}
          rows={1}
          className={cn(
            "w-full resize-none rounded-xl border border-input bg-background px-4 py-3 text-sm",
            "placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring",
            "disabled:opacity-50 disabled:cursor-not-allowed",
            "transition-all duration-200"
          )}
          style={{ maxHeight: "150px" }}
        />
      </div>

      {message.trim() ? (
        <Button
          variant="coral"
          size="icon"
          onClick={handleSubmit}
          disabled={disabled}
          className="h-12 w-12 rounded-xl"
        >
          <Send className="w-5 h-5" />
        </Button>
      ) : (
        <Button
          variant="voice"
          size="icon-lg"
          onMouseDown={onVoiceStart}
          onMouseUp={onVoiceStop}
          onMouseLeave={onVoiceStop}
          onTouchStart={onVoiceStart}
          onTouchEnd={onVoiceStop}
          disabled={disabled}
          className={cn(
            "transition-all duration-300",
            isRecording && "scale-110 animate-pulse-soft bg-destructive"
          )}
        >
          {isRecording ? (
            <Square className="w-6 h-6" />
          ) : (
            <Mic className="w-6 h-6" />
          )}
        </Button>
      )}
    </div>
  );
}
