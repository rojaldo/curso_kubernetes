#!/usr/bin/env python3
"""
Script para descargar y exportar métricas de cAdvisor en varios formatos
"""

import requests
import json
import re
from pathlib import Path
from datetime import datetime

CADVISOR_URL = "http://localhost:8080/metrics"
OUTPUT_DIR = "/home/rojaldo/cursos/contenedores/repo/samples/cadvisor/metrics_export"

def create_output_dir():
    """Crea el directorio de salida si no existe"""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def fetch_metrics():
    """Obtiene las métricas de cAdvisor"""
    response = requests.get(CADVISOR_URL)
    response.raise_for_status()
    return response.text

def save_raw_metrics(metrics_text):
    """Guarda las métricas en formato Prometheus raw"""
    filepath = f"{OUTPUT_DIR}/cadvisor_metrics_raw.txt"
    with open(filepath, 'w') as f:
        f.write(metrics_text)
    return filepath

def extract_container_metrics(metrics_text):
    """Extrae métricas específicas de contenedores"""
    container_data = {}
    
    # Regex para parsear líneas Prometheus
    pattern = r'(\w+)\{([^}]+)\}\s+([\d.e+-]+)\s+(\d+)?'
    
    for line in metrics_text.split('\n'):
        if line.startswith('#') or not line.strip():
            continue
        
        match = re.match(pattern, line)
        if match:
            metric_name, labels_str, value, timestamp = match.groups()
            
            # Parsear labels
            labels = {}
            for label_pair in labels_str.split(','):
                if '=' in label_pair:
                    k, v = label_pair.split('=', 1)
                    labels[k.strip()] = v.strip('"')
            
            # Filtrar métricas de contenedores
            container_id = labels.get('id', '')
            if 'kubepods' in container_id or 'container' in container_id:
                if container_id not in container_data:
                    container_data[container_id] = {}
                
                if metric_name not in container_data[container_id]:
                    container_data[container_id][metric_name] = []
                
                container_data[container_id][metric_name].append({
                    'labels': labels,
                    'value': float(value),
                    'timestamp': int(timestamp) if timestamp else None
                })
    
    return container_data

def save_container_metrics(container_data):
    """Guarda métricas de contenedores en JSON"""
    filepath = f"{OUTPUT_DIR}/container_metrics.json"
    
    # Convertir a formato serializable
    output = {
        'timestamp': datetime.now().isoformat(),
        'cadvisor_url': CADVISOR_URL,
        'containers': {}
    }
    
    for container_id, metrics in container_data.items():
        output['containers'][container_id] = {
            'metric_count': len(metrics),
            'metric_types': list(metrics.keys()),
            'metrics_summary': {
                name: {
                    'count': len(values),
                    'sample_value': values[0]['value'] if values else None
                }
                for name, values in metrics.items()
            }
        }
    
    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    return filepath

def extract_specific_metrics(metrics_text):
    """Extrae métricas específicas más útiles"""
    metrics = {}
    
    # Patrones para encontrar métricas específicas
    patterns = {
        'cadvisor_version': r'cadvisor_version_info.*',
        'cpu_usage': r'container_cpu_usage_seconds_total.*',
        'memory_usage': r'container_memory_usage_bytes.*',
        'memory_limit': r'container_memory_limit_bytes.*',
        'network_rx': r'container_network_receive_bytes_total.*',
        'network_tx': r'container_network_transmit_bytes_total.*',
        'fs_usage': r'container_fs_usage_bytes.*'
    }
    
    for key, pattern in patterns.items():
        matches = re.findall(pattern, metrics_text)
        if matches:
            metrics[key] = {
                'count': len(matches),
                'sample': matches[0] if matches else None
            }
    
    return metrics

def create_readme():
    """Crea un README con instrucciones de uso"""
    readme_content = """# Métricas de cAdvisor

## Descripción

Este directorio contiene las métricas exportadas desde cAdvisor, una herramienta que proporciona información detallada 
sobre el uso de recursos de contenedores en Kubernetes.

## Archivos

- **cadvisor_metrics_raw.txt**: Métricas en formato Prometheus raw
- **container_metrics.json**: Métricas estructuradas de contenedores en JSON
- **cadvisor_metrics_summary.json**: Resumen de tipos de métricas disponibles

## Cómo usar las métricas

### 1. Con Prometheus
Puedes integrar estas métricas con Prometheus agregando esta configuración:

```yaml
scrape_configs:
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: '/metrics'
```

### 2. Con Grafana
Usando Prometheus como datasource, puedes crear dashboards con consultas como:

```promql
# CPU
container_cpu_usage_seconds_total

# Memoria
container_memory_usage_bytes

# Red
rate(container_network_receive_bytes_total[5m])
rate(container_network_transmit_bytes_total[5m])

# Filesystem
container_fs_usage_bytes
```

### 3. Con Python (requests)

```python
import requests

url = "http://localhost:8080/metrics"
response = requests.get(url)
metrics = response.text

# Procesar las métricas...
```

## Tipos de Métricas Disponibles

- **CPU**: Períodos CFS, throttling, carga promedio
- **Memoria**: Uso total, límite, working set, caché
- **Red**: Bytes/paquetes enviados y recibidos
- **Filesystem**: Uso y límite de disco
- **Procesos**: Número de procesos en ejecución

## Referencia de Métricas Prometheus

Para más información sobre las métricas específicas, consulta:
https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md

## Port Forward

Para acceder a cAdvisor localmente:
```bash
kubectl port-forward -n monitoring pod/cadvisor 8080:8080
```

Luego accede a:
- Página web: http://localhost:8080
- Métricas: http://localhost:8080/metrics
"""
    
    filepath = f"{OUTPUT_DIR}/README.md"
    with open(filepath, 'w') as f:
        f.write(readme_content)
    
    return filepath

def main():
    print("Exportando métricas de cAdvisor...\n")
    
    create_output_dir()
    print(f"✓ Directorio creado: {OUTPUT_DIR}\n")
    
    # Obtener métricas
    print("Descargando métricas...")
    metrics_text = fetch_metrics()
    print(f"✓ {len(metrics_text)} bytes descargados\n")
    
    # Guardar métricas raw
    print("Exportando en diferentes formatos...")
    filepath1 = save_raw_metrics(metrics_text)
    print(f"  1. Prometheus raw: {filepath1}")
    
    # Extraer y guardar métricas de contenedores
    container_data = extract_container_metrics(metrics_text)
    filepath2 = save_container_metrics(container_data)
    print(f"  2. Contenedores JSON: {filepath2}")
    
    # Extraer métricas específicas
    specific = extract_specific_metrics(metrics_text)
    print(f"  3. Métricas específicas encontradas: {len(specific)}")
    
    # Crear README
    filepath3 = create_readme()
    print(f"  4. Documentación: {filepath3}")
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE EXPORTACIÓN")
    print("="*80)
    print(f"Total de contenedores: {len(container_data)}")
    print(f"Tipos de métrica encontrados: {len(specific)}\n")
    
    print("Métricas detectadas:")
    for metric_type, info in specific.items():
        print(f"  - {metric_type}: {info['count']} series")
    
    print("\n✓ Exportación completada exitosamente")

if __name__ == '__main__':
    main()
