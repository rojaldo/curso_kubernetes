#!/usr/bin/env python3
"""
Script interactivo para monitorear métricas de cAdvisor en tiempo real
"""

import requests
import time
import os
from datetime import datetime
from collections import defaultdict

CADVISOR_URL = "http://localhost:8080/metrics"

def clear_screen():
    """Limpia la pantalla"""
    os.system('clear' if os.name == 'posix' else 'cls')

def fetch_and_parse_metrics():
    """Obtiene y parsea las métricas"""
    response = requests.get(CADVISOR_URL)
    response.raise_for_status()
    
    metrics = defaultdict(list)
    
    for line in response.text.split('\n'):
        line = line.strip()
        
        if not line or line.startswith('#'):
            continue
        
        try:
            # Parsear métrica Prometheus
            if '{' in line:
                metric_name = line.split('{')[0]
                value_str = line.split('} ')[1].split()[0]
                value = float(value_str)
                
                metrics[metric_name].append(value)
        except (ValueError, IndexError):
            pass
    
    return metrics

def format_bytes(bytes_val):
    """Formatea bytes a unidades legibles"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} TB"

def display_metrics():
    """Muestra las métricas en tiempo real"""
    try:
        clear_screen()
        
        print("┌" + "─" * 78 + "┐")
        print("│" + " MONITOREO EN TIEMPO REAL - cADVISOR ".center(78) + "│")
        print("└" + "─" * 78 + "┘")
        
        metrics = fetch_and_parse_metrics()
        
        print(f"\n⏰ Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Tipos de métricas: {len(metrics)}\n")
        
        # Métricas de CPU
        print("┌─ CPU ─────────────────────────────────────────────────────────────────────────┐")
        cpu_metrics = [k for k in metrics.keys() if 'cpu' in k]
        print(f"│ Métricas CPU encontradas: {len(cpu_metrics)}")
        for metric in sorted(cpu_metrics)[:3]:
            values = metrics[metric]
            print(f"│   • {metric}: {len(values)} series, valor promedio: {sum(values)/len(values):.2f}")
        print("└────────────────────────────────────────────────────────────────────────────────┘\n")
        
        # Métricas de Memoria
        print("┌─ MEMORIA ──────────────────────────────────────────────────────────────────────┐")
        mem_metrics = [k for k in metrics.keys() if 'memory' in k]
        print(f"│ Métricas Memoria encontradas: {len(mem_metrics)}")
        for metric in sorted(mem_metrics)[:3]:
            values = metrics[metric]
            avg_bytes = sum(values) / len(values)
            print(f"│   • {metric}: {len(values)} series")
            print(f"│     Promedio: {format_bytes(avg_bytes)}")
        print("└────────────────────────────────────────────────────────────────────────────────┘\n")
        
        # Métricas de Red
        print("┌─ RED ──────────────────────────────────────────────────────────────────────────┐")
        net_metrics = [k for k in metrics.keys() if 'network' in k]
        print(f"│ Métricas Red encontradas: {len(net_metrics)}")
        for metric in sorted(net_metrics)[:3]:
            values = metrics[metric]
            avg_bytes = sum(values) / len(values)
            print(f"│   • {metric}: {len(values)} series")
            print(f"│     Promedio: {format_bytes(avg_bytes)}")
        print("└────────────────────────────────────────────────────────────────────────────────┘\n")
        
        # Métricas de Filesystem
        print("┌─ FILESYSTEM ───────────────────────────────────────────────────────────────────┐")
        fs_metrics = [k for k in metrics.keys() if 'fs' in k]
        print(f"│ Métricas Filesystem encontradas: {len(fs_metrics)}")
        for metric in sorted(fs_metrics)[:3]:
            values = metrics[metric]
            avg_bytes = sum(values) / len(values)
            print(f"│   • {metric}: {len(values)} series")
            print(f"│     Promedio: {format_bytes(avg_bytes)}")
        print("└────────────────────────────────────────────────────────────────────────────────┘\n")
        
        # Información del sistema
        print("┌─ INFORMACIÓN DEL SISTEMA ─────────────────────────────────────────────────────┐")
        print(f"│ URL: {CADVISOR_URL}")
        version_metrics = [k for k in metrics.keys() if 'version' in k]
        print(f"│ Métricas de versión: {len(version_metrics)}")
        print("│")
        print("│ Presiona Ctrl+C para salir")
        print("└────────────────────────────────────────────────────────────────────────────────┘")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error conectando a cAdvisor: {e}")
        print(f"   Verifica que cAdvisor esté corriendo en {CADVISOR_URL}")

def main():
    """Bucle principal de monitoreo"""
    try:
        while True:
            display_metrics()
            time.sleep(5)
    except KeyboardInterrupt:
        clear_screen()
        print("\n👋 Monitoreo finalizado\n")

if __name__ == '__main__':
    main()
