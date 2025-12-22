"""Serviços de validação"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional


def validate_date(date_str: str) -> Optional[date]:
    """Valida e converte string para date"""
    try:
        return datetime.fromisoformat(date_str).date()
    except (ValueError, TypeError):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return None


def validate_decimal(value: any) -> Optional[Decimal]:
    """Valida e converte para Decimal"""
    try:
        if isinstance(value, str):
            return Decimal(value.replace(",", "."))
        return Decimal(value)
    except (ValueError, TypeError):
        return None


def validate_positive_decimal(value: any) -> Optional[Decimal]:
    """Valida Decimal positivo"""
    decimal_value = validate_decimal(value)
    if decimal_value is not None and decimal_value >= 0:
        return decimal_value
    return None

