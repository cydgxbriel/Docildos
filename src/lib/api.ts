const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface ChatMessage {
  message: string;
  session_id?: string;
}

export interface ChatResponse {
  response: string;
  cards?: Array<{
    type: string;
    data: any;
  }>;
  actions?: Array<{
    id: string;
    label: string;
  }>;
  requires_confirmation: boolean;
  confirmation_question?: string;
}

export interface Pedido {
  id: number;
  cliente: string;
  status: string;
  data_entrega: string;
  horario?: string;
  local?: string;
  observacoes?: string;
  preco_total?: number;
  itens: Array<{
    id: number;
    receita_id: number;
    quantidade: number;
    unidade?: string;
    personalizacoes?: string;
    receita_nome?: string;
  }>;
}

export interface Receita {
  id: number;
  nome: string;
  descricao?: string;
  tempo_preparo?: number;
  rendimento?: string;
  ingredientes: Array<{
    id: number;
    ingrediente_id: number;
    quantidade: number;
    unidade: string;
    ingrediente_nome?: string;
  }>;
}

export interface Stats {
  pedidos_hoje: number;
  pedidos_novos: number;
  entregas_pendentes: number;
  em_producao: number;
  estoque_baixo: number;
  total_pedidos_hoje?: number;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: `HTTP ${response.status}: ${response.statusText}`,
      }));
      throw new Error(error.detail || "Erro na requisição");
    }

    return response.json();
  }

  async sendChatMessage(message: ChatMessage): Promise<ChatResponse> {
    return this.request<ChatResponse>("/api/chat", {
      method: "POST",
      body: JSON.stringify(message),
    });
  }

  async getPedidos(params?: {
    data_inicio?: string;
    data_fim?: string;
    status?: string;
    cliente?: string;
  }): Promise<Pedido[]> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value) queryParams.append(key, value);
      });
    }
    const query = queryParams.toString();
    return this.request<Pedido[]>(`/api/pedidos${query ? `?${query}` : ""}`);
  }

  async getPedido(id: number): Promise<Pedido> {
    return this.request<Pedido>(`/api/pedidos/${id}`);
  }

  async createPedido(pedido: any): Promise<Pedido> {
    return this.request<Pedido>("/api/pedidos", {
      method: "POST",
      body: JSON.stringify(pedido),
    });
  }

  async updatePedidoStatus(id: number, status: string): Promise<Pedido> {
    return this.request<Pedido>(`/api/pedidos/${id}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    });
  }

  async getReceitas(nome?: string): Promise<Receita[]> {
    const query = nome ? `?nome=${encodeURIComponent(nome)}` : "";
    return this.request<Receita[]>(`/api/receitas${query}`);
  }

  async getReceita(id: number): Promise<Receita> {
    return this.request<Receita>(`/api/receitas/${id}`);
  }

  async getStats(): Promise<Stats> {
    return this.request<Stats>("/api/stats");
  }

  async getAgenda(params?: {
    data_inicio?: string;
    data_fim?: string;
  }): Promise<any[]> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value) queryParams.append(key, value);
      });
    }
    const query = queryParams.toString();
    return this.request<any[]>(`/api/agenda${query ? `?${query}` : ""}`);
  }
}

export const apiClient = new ApiClient();

