import { toast } from "sonner";

export function handleApiError(error: any): string {
  if (error instanceof Error) {
    const message = error.message;
    
    // Erros de rede
    if (message.includes("Failed to fetch") || message.includes("NetworkError")) {
      toast.error("Erro de conexão. Verifique se o backend está rodando.");
      return "Erro de conexão com o servidor.";
    }
    
    // Erros HTTP
    if (message.includes("404")) {
      return "Recurso não encontrado.";
    }
    
    if (message.includes("400")) {
      return "Dados inválidos. Verifique as informações fornecidas.";
    }
    
    if (message.includes("500")) {
      toast.error("Erro interno do servidor. Tente novamente mais tarde.");
      return "Erro interno do servidor.";
    }
    
    return message || "Ocorreu um erro inesperado.";
  }
  
  return "Ocorreu um erro inesperado.";
}

