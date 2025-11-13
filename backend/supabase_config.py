"""
Alias pour supabase_client.py
Compatibilité avec les nouveaux endpoints
"""

from supabase_client import supabase, get_supabase_client

__all__ = ['supabase', 'get_supabase_client']
