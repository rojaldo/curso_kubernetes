#!/bin/bash
# quickstart_cadvisor.sh - Guía rápida de inicio para cAdvisor

echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                  cADVISOR - GUÍA RÁPIDA DE INICIO                    ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"

# Funciones auxiliares
desplegar_cadvisor() {
    echo -e "\n📦 Desplegando cAdvisor..."
    kubectl apply -f cadvisor-simple.yml
    echo "✅ Despliegue completado"
    sleep 2
    kubectl get pods -n monitoring
}

conectar_cadvisor() {
    echo -e "\n🔌 Estableciendo conexión a cAdvisor..."
    echo "   Ejecutando: kubectl port-forward -n monitoring pod/cadvisor 8080:8080"
    kubectl port-forward -n monitoring pod/cadvisor 8080:8080 &
    sleep 2
    echo "✅ Port forward establecido"
}

ver_metricas_basicas() {
    echo -e "\n📊 Primeras métricas de cAdvisor:"
    curl -s http://localhost:8080/metrics | grep -v '^#' | head -10
}

extraer_metricas() {
    echo -e "\n💾 Extrayendo y analizando métricas..."
    python3 extract_metrics.py
}

exportar_metricas() {
    echo -e "\n📁 Exportando métricas en múltiples formatos..."
    python3 export_metrics.py
}

monitoreo_tiempo_real() {
    echo -e "\n📈 Iniciando monitoreo en tiempo real..."
    echo "   (Presiona Ctrl+C para salir)"
    python3 monitor_metrics.py
}

ver_demo() {
    echo -e "\n🎬 Ejecutando demostración completa..."
    python3 demo_metrics.py
}

ver_documentacion() {
    echo -e "\n📚 Abriendo documentación..."
    cat << 'DOC'

OPCIONES DISPONIBLES:
===================

1. Desplegar cAdvisor
   kubectl apply -f cadvisor-simple.yml

2. Conectar a cAdvisor
   kubectl port-forward -n monitoring pod/cadvisor 8080:8080

3. Ver estado del pod
   kubectl get pods -n monitoring

4. Obtener métricas con cURL
   curl http://localhost:8080/metrics

5. Extraer y analizar métricas
   python3 extract_metrics.py

6. Exportar en múltiples formatos
   python3 export_metrics.py

7. Monitoreo en tiempo real
   python3 monitor_metrics.py

8. Demostración interactiva
   python3 demo_metrics.py

9. Ver documentación completa
   cat GUIA_COMPLETA.md

ACCESO RÁPIDO A MÉTRICAS:
========================

# Todas las métricas
curl http://localhost:8080/metrics

# Solo CPU
curl -s http://localhost:8080/metrics | grep container_cpu | head -5

# Solo memoria
curl -s http://localhost:8080/metrics | grep container_memory | head -5

# Contar total de series
curl -s http://localhost:8080/metrics | grep -v '^#' | wc -l

# Guardar todo en archivo
curl -s http://localhost:8080/metrics > all_metrics.txt

CONSULTAS PROMETHEUS:
====================

# CPU por contenedor
rate(container_cpu_usage_seconds_total[5m])

# Memoria usada
container_memory_usage_bytes

# Porcentaje memoria
(container_memory_usage_bytes / container_memory_limit_bytes) * 100

# Red - bytes recibidos
rate(container_network_receive_bytes_total[5m])

# Disco usado
container_fs_usage_bytes

NEXT STEPS:
==========

1. Ver ./GUIA_COMPLETA.md para documentación detallada
2. Ver ./RESUMEN.md para resumen de lo realizado
3. Ejecutar: ./quickstart_cadvisor.sh
4. Revisar: ./metrics_export/ para archivos exportados

DOC
}

mostrar_menu() {
    echo -e "\n╔═══════════════════════════════════════════════════════════════════════╗"
    echo "║                        MENÚ DE OPCIONES                                 ║"
    echo "╚═══════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "  1) Desplegar cAdvisor en el cluster"
    echo "  2) Conectar a cAdvisor (port-forward)"
    echo "  3) Ver métricas básicas (cURL)"
    echo "  4) Extraer y analizar métricas"
    echo "  5) Exportar en múltiples formatos"
    echo "  6) Monitoreo en tiempo real"
    echo "  7) Ver demostración completa"
    echo "  8) Ver documentación"
    echo "  9) Ver estado del pod"
    echo "  0) Salir"
    echo ""
}

# Menu principal
main() {
    while true; do
        mostrar_menu
        read -p "  Selecciona una opción [0-9]: " opcion
        
        case $opcion in
            1) desplegar_cadvisor ;;
            2) conectar_cadvisor ;;
            3) ver_metricas_basicas ;;
            4) extraer_metricas ;;
            5) exportar_metricas ;;
            6) monitoreo_tiempo_real ;;
            7) ver_demo ;;
            8) ver_documentacion ;;
            9) kubectl get pods -n monitoring ;;
            0) echo "👋 Hasta luego" && exit 0 ;;
            *) echo "❌ Opción no válida" ;;
        esac
    done
}

# Ejecutar
if [ "$#" -eq 0 ]; then
    main
else
    case "$1" in
        desplegar) desplegar_cadvisor ;;
        conectar) conectar_cadvisor ;;
        metricas) ver_metricas_basicas ;;
        extraer) extraer_metricas ;;
        exportar) exportar_metricas ;;
        monitor) monitoreo_tiempo_real ;;
        demo) ver_demo ;;
        docs) ver_documentacion ;;
        status) kubectl get pods -n monitoring ;;
        *) ver_documentacion ;;
    esac
fi
