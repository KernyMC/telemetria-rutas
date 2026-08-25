# FV Telemetría & Rutas - MVP de Inteligencia Operacional

Dashboard de auditoría de telemetría GPS y planificación de rutas para transporte corporativo.

## Estructura del Proyecto

El proyecto está disponible en **dos formatos**:

### 📁 **Opción A: Archivos Separados** (recomendado para desarrollo)

```
mvp-moviq/
├── dashboard.html              # Estructura HTML principal
├── styles.css                  # Estilos completos de la UI
├── app.js                      # Lógica de la aplicación
├── CLAUDE.md                   # Contexto del proyecto para Claude Code
└── README.md                   # Este archivo
```

**Ventajas:**
- Fácil debugging (errores apuntan a líneas específicas de `app.js`)
- Mejor para git (ver qué cambió en cada archivo)
- Colaboración sin conflictos
- Mantenimiento más sencillo

### 📄 **Opción B: Archivo Monolítico** (recomendado para distribución)

```
mvp-moviq/
└── dashboard-telemetria-fv.html # TODO en un solo archivo (290 KB, 5614 líneas)
```

**Ventajas:**
- Un solo archivo para abrir y listo
- Fácil de compartir por email/WhatsApp
- No requiere conocimientos técnicos del usuario final
- Autocontenido (solo depende de CDNs externos)

## Cómo Usar

### Archivos Separados
1. Abre `dashboard.html` en tu navegador (doble clic o usando Live Server de VS Code)

### Archivo Monolítico
1. Abre `dashboard-telemetria-fv.html` directamente en tu navegador

2. **Requiere conexión a internet**: El dashboard carga desde CDN:
   - Tiles de CartoDB Voyager
   - OSRM público para routing
   - Google Fonts

3. **Probar con datos sintéticos**: Usa el botón "Datos sintéticos FV" en la pestaña Auditoría para cargar un recorrido de prueba completo.

4. **Cargar CSV real**: Usa el botón "Cargar CSV" para subir archivos del hardware GPS con formato:
   ```
   timestamp,latitude,longitude,speed_kmh,heading,altitude,hdop,satellites
   ```

## Mejoras Implementadas

### ✅ Nuevos KPIs (14 métricas totales)

Organizados en 4 categorías según propuesta de negocio:

**1. Cumplimiento del Servicio**
- Cumplimiento de horario
- Tiempo total del recorrido
- Paradas detectadas (grupos > 30 seg)
- Tiempo detenido total

**2. Eficiencia Operacional**
- Distancia recorrida
- Desviación vs. ruta ideal
- Km improductivos
- Duración promedio de paradas

**3. Seguridad y Conducción**
- Velocidad promedio
- Velocidad máxima
- Velocidad promedio en movimiento
- Excesos de velocidad (>50 km/h urbano)

**4. Calidad de Datos GPS**
- HDOP promedio (precisión GPS)
- % de señal GPS de calidad

### ✅ Timeline de Eventos

Visualización cronológica de eventos importantes del viaje:
- Inicio del viaje (con indicador de puntualidad)
- Paradas significativas (las 3 más largas)
- Excesos de velocidad (los 3 más severos)
- Fin del viaje

Cada evento muestra hora, duración/velocidad y severidad con código de colores.

### ✅ Sistema de Alertas y Recomendaciones

Motor de inteligencia operacional que detecta automáticamente:

**Alertas Críticas (rojas):**
- Desviación > 20% de la ruta óptima
- Incumplimiento de horario de salida

**Alertas de Advertencia (ámbar):**
- Más de 10 excesos de velocidad
- Paradas prolongadas (> 10 minutos)
- Calidad de señal GPS < 70%

**Alertas Informativas (azules):**
- Desviación moderada justificable (5-20%)
- Buen desempeño general

Cada alerta incluye una **recomendación accionable** específica para el contexto.

### ✅ Mejoras en el Mapa

- Marcadores de excesos de velocidad (ámbar)
- Tooltips detallados en cada punto GPS
- Leyenda expandida con todos los elementos
- Separación visual clara entre ruta ideal (gris punteado) y ruta real (azul sólido)

### ✅ Reporte de Impresión Mejorado

El PDF exportado ahora incluye:

**Resumen Ejecutivo:**
- Evaluación automática del desempeño (satisfactorio / aceptable / requiere atención)
- Síntesis de hallazgos principales
- Destacados con valores clave

**Sección de Alertas e Incidencias:**
- Lista de problemas detectados por severidad
- Recomendaciones específicas

**KPIs Organizados:**
- Agrupados por categoría de negocio
- Formato profesional para auditoría contractual

### ✅ Histórico y Comparación de Viajes

Sistema de gestión de auditorías usando localStorage del navegador:

**Guardar Viajes:**
- Botón "Guardar Viaje" después de cada auditoría
- Almacena hasta 20 auditorías más recientes
- Persiste en el navegador local (sin servidor)

**Ver Histórico:**
- Lista de viajes guardados con métricas resumidas
- Vista compacta con distancia, desviación, puntualidad y excesos
- Organizado por fecha (más reciente primero)

**Comparar Viajes:**
- Comparación directa entre auditoría actual y cualquier viaje histórico
- Muestra variación porcentual entre métricas clave
- Ideal para identificar tendencias y evaluar desempeño del conductor/cooperativa

**Gestión:**
- Eliminar viajes individuales
- Limpiar todo el histórico
- Los datos se mantienen localmente (privacidad total)

## Funcionalidades Futuras (Backlog)

Según documento de propuesta de negocio:

- [ ] Gráficos de velocidad a lo largo del tiempo (sparklines CSS)
- [ ] Detección de zonas de riesgo/anomalías recurrentes
- [ ] Exportar histórico completo a CSV/JSON
- [ ] Modo de comparación visual (tabla lado a lado)
- [ ] Filtros en histórico (por fecha, desempeño, cooperativa)
- [ ] Cálculo de tendencias (mejorando/empeorando)
- [ ] Integración con datos de nómina/asistencia
- [ ] API REST para integrar con sistemas empresariales

## Stack Técnico

- **100% Frontend**: HTML, CSS, JavaScript vanilla
- **Mapas**: Leaflet + CartoDB Voyager tiles
- **Routing**: OSRM público
- **Iconos**: Lucide icons
- **Sin build step**: Se puede abrir directamente en el navegador

## Restricciones Importantes

- **OSRM demo server**: Sin SLA ni API key. Para producción se requiere instancia propia en Docker.
- **Sin backend**: Todos los cálculos son client-side.
- **Datos mock**: Coordenadas de ejemplo en Quito, Ecuador.

## Fórmulas de Negocio

- **Distancia real**: Suma de Haversine entre pings GPS consecutivos
- **Distancia ideal**: OSRM `/route/v1/driving/` entre inicio y fin
- **Desviación %**: `((real - ideal) / ideal) * 100`
- **Km improductivos**: `max(0, real - ideal)`
- **Tiempo detenido**: Suma de intervalos con `speed < 2.0 km/h`
- **Cumplimiento horario**: Primer ping `<= 08:35:00`
- **Excesos velocidad**: Pings con `speed > 50 km/h`

## Contacto de Negocio

Este MVP implementa la **Fase 1: Visibilidad** del documento "Propuesta: Inteligencia Operacional para Transporte Corporativo".

El producto busca convertirse en una plataforma B2B de Transport Intelligence as a Service para empresas que contratan cooperativas de transporte.
# telemetria-rutas
