#!/usr/bin/env python3
"""
Script para demostrar diferentes formas de acceder a las métricas de cAdvisor
"""

import requests
import json
from datetime import datetime

CADVISOR_URL = "http://localhost:8080/metrics"

def demo_basic_metrics():
    """Demo 1: Obtener métricas básicas"""
    print("\n" + "="*80)
    print("DEMO 1: OBTENER MÉTRICAS BÁSICAS")
    print("="*80)
    
    try:
        response = requests.get(CADVISOR_URL)
        metrics_text = response.text
        
        # Contar líneas
        lines = [l for l in metrics_text.split('\n') if l.strip() and not l.startswith('#')]
        metric_types = set(l.split('{')[0] for l in lines if '{' in l)
        
        print(f"\n✓ Total de líneas de métrica: {len(lines)}")
        print(f"✓ Tipos de métrica únicos: {len(metric_types)}")
        print(f"\nPrimeros 5 tipos de métrica:")
        for i, metric in enumerate(sorted(metric_types)[:5], 1):
            print(f"  {i}. {metric}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_filter_metrics():
    """Demo 2: Filtrar métricas por tipo"""
    print("\n" + "="*80)
    print("DEMO 2: FILTRAR MÉTRICAS POR TIPO")
    print("="*80)
    
    try:
        response = requests.get(CADVISOR_URL)
        metrics_text = response.text
        
        filters = {
            'CPU': 'container_cpu',
            'Memoria': 'container_memory',
            'Red': 'container_network',
            'Filesystem': 'container_fs'
        }
        
        print("\nMétricas encontradas por categoría:\n")
        
        for category, filter_str in filters.items():
            count = len([l for l in metrics_text.split('\n') 
                        if filter_str in l and not l.startswith('#')])
            print(f"  {category:15} : {count:5} series")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_extract_values():
    """Demo 3: Extraer valores específicos"""
    print("\n" + "="*80)
    print("DEMO 3: EXTRAER VALORES ESPECÍFICOS DE MÉTRICAS")
    print("="*80)
    
    try:
        response = requests.get(CADVISOR_URL)
        metrics_text = response.text
        
        # Buscar cadvisor_version_info
        print("\nInformación de cAdvisor:")
        for line in metrics_text.split('\n'):
            if 'cadvisor_version_info' in line and not line.startswith('#'):
                print(f"\n  {line[:100]}...")
                
                # Extraer labels
                if '{' in line:
                    labels_part = line.split('{')[1].split('}')[0]
                    labels = {}
                    for pair in labels_part.split(','):
                        k, v = pair.split('=')
                        labels[k.strip()] = v.strip('"')
                    
                    print(f"\n  Detalles:")
                    print(f"    - Versión: {labels.get('cadvisorVersion', 'N/A')}")
                    print(f"    - Kernel: {labels.get('kernelVersion', 'N/A')}")
                    print(f"    - OS: {labels.get('osVersion', 'N/A')}")
                
                break
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_parse_numeric_metrics():
    """Demo 4: Parsear y analizar métricas numéricas"""
    print("\n" + "="*80)
    print("DEMO 4: ANALIZAR MÉTRICAS NUMÉRICAS")
    print("="*80)
    
    try:
        response = requests.get(CADVISOR_URL)
        metrics_text = response.text
        
        # Buscar container_memory_usage_bytes
        memory_values = []
        cpu_values = []
        
        for line in metrics_text.split('\n'):
            if not line.startswith('#') and line.strip():
                if 'container_memory_usage_bytes{' in line:
                    try:
                        value = float(line.split('} ')[1].split()[0])
                        memory_values.append(value)
                    except:
                        pass
                
                if 'container_cpu_usage_seconds_total{' in line:
                    try:
                        value = float(line.split('} ')[1].split()[0])
                        cpu_values.append(value)
                    except:
                        pass
        
        print(f"\nMemoria en contenedores:")
        if memory_values:
            print(f"  - Total de series: {len(memory_values)}")
            print(f"  - Promedio: {sum(memory_values)/len(memory_values)/1024/1024:.2f} MB")
            print(f"  - Máximo: {max(memory_values)/1024/1024:.2f} MB")
            print(f"  - Mínimo: {min(memory_values)/1024/1024:.2f} MB")
        
        print(f"\nCPU en contenedores:")
        if cpu_values:
            print(f"  - Total de series: {len(cpu_values)}")
            print(f"  - Promedio: {sum(cpu_values)/len(cpu_values):.4f} segundos")
            print(f"  - Máximo: {max(cpu_values):.4f} segundos")
            print(f"  - Mínimo: {min(cpu_values):.4f} segundos")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_json_export():
    """Demo 5: Exportar a JSON"""
    print("\n" + "="*80)
    print("DEMO 5: EXPORTAR MÉTRICAS A JSON")
    print("="*80)
    
    try:
        response = requests.get(CADVISOR_URL)
        metrics_text = response.text
        
        # Crear estructura JSON
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'source': CADVISOR_URL,
            'summary': {
                'total_metrics': len([l for l in metrics_text.split('\n') 
                                     if l.strip() and not l.startswith('#')]),
                'cpu_metrics': len([l for l in metrics_text.split('\n') 
                                   if 'container_cpu' in l and not l.startswith('#')]),
                'memory_metrics': len([l for l in metrics_text.split('\n') 
                                      if 'container_memory' in l and not l.startswith('#')]),
                'network_metrics': len([l for l in metrics_text.split('\n') 
                                       if 'container_network' in l and not l.startswith('#')]),
                'fs_metrics': len([l for l in metrics_text.split('\n') 
                                  if 'container_fs' in l and not l.startswith('#')]),
            }
        }
        
        output_file = '/home/rojaldo/cursos/contenedores/repo/samples/cadvisor/demo_export.json'
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"\n✓ JSON exportado a: {output_file}")
        print(f"\nContenido:")
        print(json.dumps(export_data, indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_curl_examples():
    """Demo 6: Ejemplos de cURL"""
    print("\n" + "="*80)
    print("DEMO 6: EJEMPLOS DE COMANDOS cURL")
    print("="*80)
    
    examples = [
        ("Obtener todas las métricas", 
         "curl http://localhost:8080/metrics"),
        
        ("Contar líneas de métrica", 
         "curl -s http://localhost:8080/metrics | wc -l"),
        
        ("Obtener solo métricas de CPU", 
         "curl -s http://localhost:8080/metrics | grep container_cpu"),
        
        ("Obtener solo métricas de memoria", 
         "curl -s http://localhost:8080/metrics | grep container_memory"),
        
        ("Guardar métricas en archivo", 
         "curl -s http://localhost:8080/metrics > metrics.txt"),
        
        ("Ver primeras 20 líneas", 
         "curl -s http://localhost:8080/metrics | head -20"),
        
        ("Contar tipos de métrica únicos", 
         "curl -s http://localhost:8080/metrics | grep -v '^#' | cut -d'{' -f1 | sort -u | wc -l"),
    ]
    
    print("\nComandos útiles:\n")
    for i, (desc, cmd) in enumerate(examples, 1):
        print(f"  {i}. {desc}:")
        print(f"     {cmd}\n")

def demo_prometheus_queries():
    """Demo 7: Ejemplos de consultas Prometheus"""
    print("\n" + "="*80)
    print("DEMO 7: EJEMPLOS DE CONSULTAS PROMETHEUS (PromQL)")
    print("="*80)
    
    queries = {
        'CPU': [
            ('Uso de CPU actual', 'container_cpu_usage_seconds_total'),
            ('Tasa de CPU (5 min)', 'rate(container_cpu_usage_seconds_total[5m])'),
            ('CPU throttled', 'rate(container_cpu_cfs_throttled_seconds_total[5m])'),
        ],
        'Memoria': [
            ('Memoria usada', 'container_memory_usage_bytes'),
            ('Porcentaje de memoria', '(container_memory_usage_bytes / container_memory_limit_bytes) * 100'),
            ('Working set', 'container_memory_working_set_bytes'),
        ],
        'Red': [
            ('Bytes recibidos/seg', 'rate(container_network_receive_bytes_total[5m])'),
            ('Bytes enviados/seg', 'rate(container_network_transmit_bytes_total[5m])'),
            ('Paquetes recibidos', 'container_network_receive_packets_total'),
        ],
        'Filesystem': [
            ('Uso de disco', 'container_fs_usage_bytes'),
            ('Porcentaje disco', '(container_fs_usage_bytes / container_fs_limit_bytes) * 100'),
        ],
    }
    
    print("\nConsultas por categoría:\n")
    for category, query_list in queries.items():
        print(f"  {category}:")
        for desc, query in query_list:
            print(f"    • {desc}")
            print(f"      {query}\n")

def main():
    """Ejecutar todas las demos"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " DEMOSTRACIÓN COMPLETA DE EXTRACCIÓN DE MÉTRICAS DE cADVISOR ".center(78) + "║")
    print("╚" + "="*78 + "╝")
    
    demos = [
        demo_basic_metrics,
        demo_filter_metrics,
        demo_extract_values,
        demo_parse_numeric_metrics,
        demo_json_export,
        demo_curl_examples,
        demo_prometheus_queries,
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\n❌ Error en demo: {e}")
    
    print("\n" + "="*80)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
