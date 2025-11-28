# Métricas de cAdvisor

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
