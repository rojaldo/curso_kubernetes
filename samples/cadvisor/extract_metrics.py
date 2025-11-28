#!/usr/bin/env python3
"""
Script para extraer y analizar métricas de cAdvisor
"""

import requests
import json
from collections import defaultdict
from datetime import datetime

CADVISOR_URL = "http://localhost:8080/metrics"

def fetch_metrics():
    """Obtiene las métricas de cAdvisor en formato Prometheus"""
    try:
        response = requests.get(CADVISOR_URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metrics: {e}")
        return None

def parse_prometheus_metrics(metrics_text):
    """Parsea métricas en formato Prometheus"""
    metrics = defaultdict(list)
    
    for line in metrics_text.split('\n'):
        line = line.strip()
        
        # Saltar comentarios y líneas vacías
        if not line or line.startswith('#'):
            continue
        
        # Parsear métrica
        try:
            if '{' in line:
                metric_name = line.split('{')[0]
                labels_part = line.split('{')[1].split('}')[0]
                value_part = line.split('} ')[1].split(' ')
                value = float(value_part[0])
                timestamp = int(value_part[1]) if len(value_part) > 1 else None
                
                metrics[metric_name].append({
                    'labels': labels_part,
                    'value': value,
                    'timestamp': timestamp
                })
            else:
                parts = line.split()
                if len(parts) >= 2:
                    metric_name = parts[0]
                    value = float(parts[1])
                    timestamp = int(parts[2]) if len(parts) > 2 else None
                    
                    metrics[metric_name].append({
                        'value': value,
                        'timestamp': timestamp
                    })
        except (ValueError, IndexError):
            pass
    
    return metrics

def extract_key_metrics(metrics):
    """Extrae las métricas más importantes"""
    key_metrics = {}
    
    # Información de versión
    if 'cadvisor_version_info' in metrics:
        key_metrics['version'] = metrics['cadvisor_version_info']
    
    # Métricas de CPU
    cpu_metrics = {
        'cfs_periods': len(metrics.get('container_cpu_cfs_periods_total', [])),
        'throttled_periods': len(metrics.get('container_cpu_cfs_throttled_periods_total', [])),
        'load_average': len(metrics.get('container_cpu_load_average_10s', []))
    }
    key_metrics['cpu'] = cpu_metrics
    
    # Métricas de memoria
    memory_metrics = {
        'usage': len(metrics.get('container_memory_usage_bytes', [])),
        'limit': len(metrics.get('container_memory_limit_bytes', [])),
        'working_set': len(metrics.get('container_memory_working_set_bytes', []))
    }
    key_metrics['memory'] = memory_metrics
    
    # Métricas de red
    network_metrics = {
        'rx_bytes': len(metrics.get('container_network_receive_bytes_total', [])),
        'tx_bytes': len(metrics.get('container_network_transmit_bytes_total', [])),
        'rx_packets': len(metrics.get('container_network_receive_packets_total', [])),
        'tx_packets': len(metrics.get('container_network_transmit_packets_total', []))
    }
    key_metrics['network'] = network_metrics
    
    # Métricas de filesystem
    fs_metrics = {
        'usage': len(metrics.get('container_fs_usage_bytes', [])),
        'limit': len(metrics.get('container_fs_limit_bytes', []))
    }
    key_metrics['filesystem'] = fs_metrics
    
    return key_metrics

def print_summary(metrics):
    """Imprime un resumen de las métricas disponibles"""
    print("\n" + "="*80)
    print("RESUMEN DE MÉTRICAS DE CADVISOR".center(80))
    print("="*80)
    print(f"Timestamp: {datetime.now().isoformat()}\n")
    
    print("MÉTRICAS DISPONIBLES:")
    print("-" * 80)
    
    # Contar total de series de tiempo
    total_series = sum(len(v) for v in metrics.values())
    print(f"Total de series de tiempo: {total_series}\n")
    
    print("Categorías de métricas:")
    print(f"  - CPU: {metrics.get('cpu', {}).get('cfs_periods', 0)} series")
    print(f"  - Memoria: {metrics.get('memory', {}).get('usage', 0)} series")
    print(f"  - Red: {metrics.get('network', {}).get('rx_bytes', 0)} series")
    print(f"  - Filesystem: {metrics.get('filesystem', {}).get('usage', 0)} series")
    
    print("\n" + "="*80)

def save_metrics_json(metrics_text, filepath):
    """Guarda las métricas en un archivo JSON formateado"""
    try:
        # Parsear y contar métricas
        lines = [l.strip() for l in metrics_text.split('\n') if l.strip() and not l.strip().startswith('#')]
        
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_metric_lines': len(lines),
            'cadvisor_url': CADVISOR_URL,
            'metric_types': {
                'cpu': len([l for l in lines if 'cpu' in l.lower()]),
                'memory': len([l for l in lines if 'memory' in l.lower()]),
                'network': len([l for l in lines if 'network' in l.lower()]),
                'filesystem': len([l for l in lines if 'fs' in l.lower()]),
                'disk': len([l for l in lines if 'disk' in l.lower()]),
                'accelerator': len([l for l in lines if 'accelerator' in l.lower()])
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\nResumen guardado en: {filepath}")
        return output
    except Exception as e:
        print(f"Error guardando métricas: {e}")
        return None

def main():
    print("Conectando a cAdvisor...")
    metrics_text = fetch_metrics()
    
    if metrics_text:
        print(f"✓ Métricas obtenidas correctamente ({len(metrics_text)} bytes)")
        
        # Parsear métricas
        metrics = parse_prometheus_metrics(metrics_text)
        print(f"✓ {len(metrics)} tipos de métricas diferentes encontrados")
        
        # Extraer métricas clave
        key_metrics = extract_key_metrics(metrics)
        
        # Imprimir resumen
        print_summary(key_metrics)
        
        # Guardar en JSON
        output = save_metrics_json(metrics_text, 
                                   '/home/rojaldo/cursos/contenedores/repo/samples/cadvisor/cadvisor_metrics_summary.json')
        
        if output:
            print("\nDetalles del resumen:")
            print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("✗ No se pudieron obtener las métricas")

if __name__ == '__main__':
    main()
