# Nginx Helm Chart

Este es un chart de Helm de ejemplo para desplegar un servidor Nginx en Kubernetes.

## Características

- Deployment con múltiples réplicas
- Service (ClusterIP, NodePort o LoadBalancer)
- ConfigMap para la configuración de Nginx
- Liveness y Readiness probes
- Ingress opcional
- Horizontal Pod Autoscaler opcional
- Límites de recursos configurables

## Requisitos

- Kubernetes 1.20+
- Helm 3+

## Instalación

### 1. Instalación básica

```bash
helm install mi-nginx .
```

### 2. Instalación con valores personalizados

```bash
helm install mi-nginx . \
  --set replicaCount=3 \
  --set image.tag="1.25.0"
```

### 3. Instalación con archivo de valores

```bash
helm install mi-nginx . -f values-production.yaml
```

### 4. Instalación con Ingress habilitado

```bash
helm install mi-nginx . \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host="nginx.example.com" \
  --set ingress.className="nginx"
```

## Parámetros configurables

### Imagen y replicas

| Parámetro | Descripción | Por defecto |
|-----------|-------------|------------|
| `replicaCount` | Número de réplicas | `2` |
| `image.repository` | Repositorio de la imagen | `nginx` |
| `image.tag` | Tag de la imagen | `1.25.0` |
| `image.pullPolicy` | Política de descarga | `IfNotPresent` |

### Servicio

| Parámetro | Descripción | Por defecto |
|-----------|-------------|------------|
| `service.type` | Tipo de servicio | `ClusterIP` |
| `service.port` | Puerto del servicio | `80` |
| `service.targetPort` | Puerto del contenedor | `80` |

### Ingress

| Parámetro | Descripción | Por defecto |
|-----------|-------------|------------|
| `ingress.enabled` | Habilitar ingress | `false` |
| `ingress.className` | Clase de ingress | `nginx` |
| `ingress.hosts` | Hosts del ingress | `nginx.example.local` |

### Recursos

| Parámetro | Descripción | Por defecto |
|-----------|-------------|------------|
| `resources.requests.cpu` | CPU solicitada | `50m` |
| `resources.requests.memory` | Memoria solicitada | `64Mi` |
| `resources.limits.cpu` | CPU límite | `100m` |
| `resources.limits.memory` | Memoria límite | `128Mi` |

### Autoscaling

| Parámetro | Descripción | Por defecto |
|-----------|-------------|------------|
| `autoscaling.enabled` | Habilitar HPA | `false` |
| `autoscaling.minReplicas` | Mínimo de réplicas | `2` |
| `autoscaling.maxReplicas` | Máximo de réplicas | `10` |
| `autoscaling.targetCPUUtilizationPercentage` | CPU target | `80` |

## Ejemplos de uso

### Ejemplo 1: Nginx simple en desarrollo

```bash
helm install nginx-dev . \
  --set replicaCount=1 \
  --set resources.requests.cpu=10m \
  --set resources.requests.memory=32Mi
```

### Ejemplo 2: Nginx en producción con Ingress

```bash
helm install nginx-prod . \
  --set replicaCount=3 \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host="api.example.com" \
  --set ingress.className="nginx" \
  --set autoscaling.enabled=true \
  --set autoscaling.minReplicas=3 \
  --set autoscaling.maxReplicas=10
```

### Ejemplo 3: Usar archivo de valores personalizado

```bash
cat > custom-values.yaml <<EOF
replicaCount: 3
image:
  tag: "1.25.0"
service:
  type: LoadBalancer
  port: 8080
ingress:
  enabled: true
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
EOF

helm install nginx-prod . -f custom-values.yaml
```

## Comandos útiles

### Listar releases instalados

```bash
helm list
```

### Ver valores de un release

```bash
helm get values mi-nginx
```

### Actualizar un release

```bash
helm upgrade mi-nginx . --set replicaCount=5
```

### Desinstalar un release

```bash
helm uninstall mi-nginx
```

### Ver el estado del deployment

```bash
kubectl get deployment
kubectl get pods
kubectl get svc
```

### Ver logs de los pods

```bash
kubectl logs -f deployment/release-name-nginx-example
```

### Ver template renderizado (sin instalar)

```bash
helm template mi-nginx .
```

### Validar el chart

```bash
helm lint .
```

## Configuración de Nginx

La configuración de Nginx se define en `values.yaml` en la sección `nginx.config`. Para cambiar la configuración:

```bash
helm install mi-nginx . --set nginx.config="server { ... }"
```

O usando un archivo:

```yaml
nginx:
  config: |
    server {
      listen 80;
      server_name _;

      location / {
        root /usr/share/nginx/html;
        index index.html;
      }
    }
```

## Notas

- Los probes (liveness y readiness) se configuran automáticamente apuntando al endpoint `/health`
- La configuración de Nginx se monta como un ConfigMap
- Los recursos están limitados por defecto (ver `values.yaml`)
- El chart soporta múltiples ambientes mediante archivos de valores separados

## Troubleshooting

### Ver qué está instalado

```bash
helm get all mi-nginx
```

### Ver eventos del cluster

```bash
kubectl describe deployment mi-nginx-nginx-example
```

### Acceder al pod

```bash
kubectl exec -it <pod-name> -- /bin/bash
```

## Licencia

MIT
