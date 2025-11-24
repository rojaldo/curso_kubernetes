# 🚀 Curso Completo de Kubernetes

Este repositorio contiene todo el material teórico, práctico y ejercicios para conocer la orquestación de contenedores con Kubernetes.

## 📋 Descripción

Este curso está diseñado para llevar a los estudiantes desde los conceptos básicos de Kubernetes hasta la implementación de clusters productivos y patrones avanzados. Incluye teoría, ejercicios prácticos y presentaciones interactivas para cada módulo.

## 🎯 Objetivos del Curso

- Comprender la arquitectura y componentes de Kubernetes
- Dominar el despliegue y gestión de aplicaciones en contenedores
- Implementar estrategias de networking, almacenamiento y configuración
- Aplicar prácticas de seguridad y observabilidad
- Gestionar escalado y performance de aplicaciones
- Utilizar Helm para gestión de paquetes
- Implementar CI/CD con Kubernetes
- Trabajar con Service Mesh y operadores
- Preparar clusters para producción

## 📚 Contenido del Curso

### Módulo 1: Introducción a Kubernetes
- ¿Qué es Kubernetes?
- Historia y origen del proyecto
- Arquitectura del cluster
- Componentes del Control Plane y Nodos
- Instalación y configuración de entornos

### Módulo 2: Trabajando con Pods
- Anatomía de un Pod
- Ciclo de vida de Pods
- Contenedores init y sidecar
- Health checks (Liveness, Readiness, Startup)
- Recursos y límites

### Módulo 3: Controllers y Workloads
- Deployments
- ReplicaSets
- StatefulSets
- DaemonSets
- Jobs y CronJobs
- Estrategias de actualización

### Módulo 4: Servicios y Redes
- Tipos de Services (ClusterIP, NodePort, LoadBalancer)
- Ingress Controllers
- Network Policies
- DNS en Kubernetes
- Service Mesh básico

### Módulo 5: Almacenamiento
- Volumes y tipos de volúmenes
- PersistentVolumes (PV)
- PersistentVolumeClaims (PVC)
- StorageClasses
- StatefulSets con almacenamiento

### Módulo 6: Configuración y Secrets
- ConfigMaps
- Secrets
- Gestión de variables de entorno
- Mejores prácticas de seguridad
- Herramientas de gestión de secretos

### Módulo 7: Seguridad
- RBAC (Role-Based Access Control)
- Service Accounts
- Pod Security Policies/Standards
- Network Policies avanzadas
- Seguridad de imágenes

### Módulo 8: Observabilidad
- Logging centralizado
- Métricas con Prometheus
- Visualización con Grafana
- Tracing distribuido
- Alertas y monitorización

### Módulo 9: Escalado y Performance
- Horizontal Pod Autoscaling (HPA)
- Vertical Pod Autoscaling (VPA)
- Cluster Autoscaler
- Optimización de recursos
- Mejores prácticas de performance

### Módulo 10: Helm
- Introducción a Helm
- Creación de Charts
- Gestión de releases
- Repositorios de Helm
- Helm en CI/CD

### Módulo 11: CI/CD
- Integración continua con Kubernetes
- GitOps con ArgoCD/Flux
- Pipelines de despliegue
- Estrategias Blue/Green y Canary
- Rollbacks automáticos

### Módulo 12: Service Mesh
- Conceptos de Service Mesh
- Istio/Linkerd
- Traffic management
- Security y mTLS
- Observabilidad avanzada

### Módulo 13: Operaciones Avanzadas
- Operadores de Kubernetes
- Custom Resources (CRDs)
- Backup y recuperación
- Disaster recovery
- Multi-cluster management

### Módulo 14: Kubernetes en Producción
- Hardening de clusters
- Alta disponibilidad
- Gestión de actualizaciones
- Capacity planning
- Troubleshooting avanzado

### Módulo 15: Casos de Uso y Patrones
- Arquitecturas de microservicios
- Aplicaciones stateful
- Big Data en Kubernetes
- Machine Learning workloads
- Patrones de diseño comunes

## 🗂️ Estructura del Repositorio

```
.
├── README.md                    # Este archivo
├── docs/
│   ├── kubernetes.adoc          # Documentación completa del curso
│   ├── kubernetes_ejercicios.adoc # Ejercicios prácticos
│   ├── html/                    # Documentación en HTML
│   │   ├── kubernetes.html
│   │   └── kubernetes_ejercicios.html
│   └── reveal/                  # Presentaciones por módulo
│       ├── modulo-1-introduccion-kubernetes.html
│       ├── modulo-2-trabajando-con-pods.html
│       ├── modulo-3-controllers-workloads.html
│       ├── modulo-4-servicios-redes.html
│       ├── modulo-5-almacenamiento-completo.html
│       ├── modulo-6-configuracion-secrets.html
│       ├── modulo-7-seguridad.html
│       ├── modulo-8-observabilidad.html
│       ├── modulo-9-escalado-performance.html
│       ├── modulo-10-helm.html
│       ├── modulo-11-cicd.html
│       ├── modulo-12-service-mesh.html
│       ├── modulo-13-operaciones-avanzadas.html
│       ├── modulo-14-kubernetes-produccion.html
│       └── modulo-15-casos-uso-patrones.html
```

## 🚀 Requisitos Previos

### Conocimientos
- Conocimientos básicos de Linux/Unix
- Familiaridad con línea de comandos
- Conceptos básicos de contenedores (Docker recomendado)
- Nociones de redes y arquitectura de aplicaciones

### Software Necesario
- **kubectl**: Cliente de línea de comandos de Kubernetes
- **Docker**: Para construcción de imágenes
- **Minikube** o **Kind**: Para cluster local de desarrollo
- **Git**: Para clonar el repositorio
- Navegador web moderno para las presentaciones

### Instalación de Herramientas

#### kubectl
```bash
# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verificar instalación
kubectl version --client
```

#### Minikube
```bash
# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Iniciar cluster
minikube start
```

## 📖 Cómo Usar Este Curso

### 1. Documentación Completa
Abre los archivos HTML en tu navegador:
```bash
# Teoría completa
firefox docs/html/kubernetes.html

# Ejercicios prácticos
firefox docs/html/kubernetes_ejercicios.html
```

### 2. Presentaciones Interactivas
Cada módulo tiene una presentación Reveal.js:
```bash
# Ejemplo: Módulo 1
firefox docs/reveal/modulo-1-introduccion-kubernetes.html
```

### 3. Práctica con Ejercicios
Sigue los ejercicios en `kubernetes_ejercicios.adoc` para cada módulo. Cada ejercicio incluye:
- **Objetivo de aprendizaje**: Qué aprenderás
- **Descripción**: Contexto del ejercicio
- **Tareas**: Pasos detallados
- **Solución**: Resolución completa
- **Verificación**: Cómo comprobar que funciona
- **Limpieza**: Cómo eliminar recursos

## 🎓 Metodología de Aprendizaje

1. **Lee la teoría** de cada módulo en la documentación
2. **Revisa la presentación** para conceptos visuales
3. **Practica con los ejercicios** en un cluster local
4. **Experimenta y modifica** los ejemplos
5. **Resuelve problemas** por ti mismo antes de ver las soluciones

## 🛠️ Configuración del Entorno

### Cluster Local con Minikube
```bash
# Iniciar Minikube con recursos adecuados
minikube start --cpus=4 --memory=8192 --driver=docker

# Habilitar addons útiles
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard

# Acceder al dashboard
minikube dashboard
```

### Verificar Configuración
```bash
# Verificar cluster
kubectl cluster-info
kubectl get nodes

# Verificar componentes
kubectl get pods -n kube-system
```

## 📚 Recursos Adicionales

### Documentación Oficial
- [Kubernetes Docs](https://kubernetes.io/docs/)
- [Kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
- [API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)

### Comunidad
- [Kubernetes Slack](https://slack.k8s.io/)
- [Stack Overflow - Kubernetes](https://stackoverflow.com/questions/tagged/kubernetes)
- [Reddit - r/kubernetes](https://www.reddit.com/r/kubernetes/)

### Herramientas Útiles
- [k9s](https://k9scli.io/) - Terminal UI para Kubernetes
- [Lens](https://k8slens.dev/) - IDE para Kubernetes
- [kubectx/kubens](https://github.com/ahmetb/kubectx) - Cambiar contextos y namespaces

## 🤝 Contribuir

Si encuentras errores o quieres mejorar el contenido:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -am 'Añadir mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Crea un Pull Request

## 📝 Licencia

Este curso está diseñado con fines educativos. Todo el contenido es material de aprendizaje.

## ✨ Autor

Curso creado por rojaldo para la formación en tecnologías de contenedores y orquestación.

---

**¡Feliz aprendizaje de Kubernetes! 🎉**

Para comenzar, abre la [documentación completa](docs/html/kubernetes.html) o la [primera presentación](docs/reveal/modulo-1-introduccion-kubernetes.html).