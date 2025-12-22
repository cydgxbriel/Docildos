import httpx
import os
from typing import Dict, Any, List
from datetime import datetime, date, timedelta
from dotenv import load_dotenv

load_dotenv()

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")


class CalendarTool:
    """Tool para operações com agenda de entregas"""
    
    def __init__(self):
        self.base_url = f"{BACKEND_API_URL}/api/agenda"
    
    def listar_agenda(
        self, data_inicio: str = None, data_fim: str = None
    ) -> List[Dict[str, Any]]:
        """Lista agenda de entregas"""
        try:
            params = {}
            if data_inicio:
                params["data_inicio"] = data_inicio
            if data_fim:
                params["data_fim"] = data_fim
            
            response = httpx.get(self.base_url, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return [{"error": f"Erro ao listar agenda: {str(e)}"}]
    
    def obter_agenda_dia(self, dia: date) -> List[Dict[str, Any]]:
        """Obtém agenda de um dia específico"""
        dia_str = str(dia)
        return self.listar_agenda(data_inicio=dia_str, data_fim=dia_str)
    
    def processar_mensagem(self, mensagem: str, contexto: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa mensagem do usuário e executa ação apropriada"""
        mensagem_lower = mensagem.lower()
        
        # Detectar intenção
        if "agenda" in mensagem_lower or "entreg" in mensagem_lower or "entrega" in mensagem_lower:
            # Tentar extrair data
            hoje = date.today()
            dia_alvo = None
            
            if "hoje" in mensagem_lower:
                dia_alvo = hoje
            elif "amanhã" in mensagem_lower or "amanha" in mensagem_lower:
                dia_alvo = hoje + timedelta(days=1)
            elif "sexta" in mensagem_lower:
                # Encontrar próxima sexta
                dias_ate_sexta = (4 - hoje.weekday()) % 7
                if dias_ate_sexta == 0:
                    dias_ate_sexta = 7
                dia_alvo = hoje + timedelta(days=dias_ate_sexta)
            elif "sábado" in mensagem_lower or "sabado" in mensagem_lower:
                # Encontrar próximo sábado
                dias_ate_sabado = (5 - hoje.weekday()) % 7
                if dias_ate_sabado == 0:
                    dias_ate_sabado = 7
                dia_alvo = hoje + timedelta(days=dias_ate_sabado)
            
            if dia_alvo:
                agenda = self.obter_agenda_dia(dia_alvo)
                return {
                    "action": "listar_dia",
                    "data": agenda,
                    "dia": str(dia_alvo),
                }
            else:
                # Listar próximos dias
                fim_semana = hoje + timedelta(days=7)
                agenda = self.listar_agenda(
                    data_inicio=str(hoje), data_fim=str(fim_semana)
                )
                return {
                    "action": "listar",
                    "data": agenda,
                }
        
        else:
            return {
                "action": "consulta",
                "message": "Não entendi o que você quer fazer com agenda. Pode reformular?",
            }

