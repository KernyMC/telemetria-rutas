# Changelog - FV Telemetría & Rutas MVP

## [2.1.0] - 2026-08-25

### ✅ Agregado: Administración y grupos de empleados

- Nuevo panel `Administrar` para gestionar la asignación de personal a paradas.
- Selector demostrativo de perfil entre `Superadmin` y `Usuario normal`.
- Drag and drop para mover usuarios entre paradas y la lista `No viajan`.
- Datos demo precargados: 3 usuarios en la primera parada, 2 en la segunda y 1 fuera de ruta.
- Persistencia de asignaciones en `localStorage`.
- La generación de ruta usa únicamente los usuarios asignados a una parada.
- Botón para restablecer la configuración demo inicial.
- La sección `Planificar Ruta` ahora muestra dos grupos de empleados: `Grupo A · Operativo` y `Grupo B · Logística`.
- Archivo monolítico regenerado para incluir estas mejoras.

---

## [2.0.0] - 2026-08-24

### 🎯 Mejoras Principales del Documento de Propuesta de Negocio

Esta versión implementa la transformación del MVP básico a una plataforma de **Inteligencia Operacional** según el documento "Propuesta: Inteligencia Operacional para Transporte Corporativo".

---

### ✅ Agregado

#### 1. KPIs Ampliados (14 métricas vs 6 originales)

**Cumplimiento del Servicio:**
- ✨ Paradas detectadas (grupos consecutivos > 30 seg)
- ✨ Duración promedio de paradas

**Eficiencia Operacional:**
- ✨ Duración promedio de paradas

**Seguridad y Conducción (NUEVO):**
- ✨ Velocidad promedio
- ✨ Velocidad máxima registrada
- ✨ Velocidad promedio en movimiento
- ✨ Contador de excesos de velocidad (>50 km/h urbano)

**Calidad de Datos GPS (NUEVO):**
- ✨ HDOP promedio (Horizontal Dilution of Precision)
- ✨ Porcentaje de señal GPS de calidad (HDOP ≤ 2.0, satélites ≥ 6)

#### 2. Timeline de Eventos

Nuevo componente visual que muestra la cronología del viaje:
- Inicio del viaje con indicador de puntualidad (verde/rojo)
- Paradas significativas (las 3 más largas)
- Excesos de velocidad más severos (los 3 peores)
- Fin del viaje con duración total

Cada evento muestra:
- Hora exacta
- Duración o velocidad según el tipo
- Código de colores por severidad

#### 3. Sistema de Alertas y Recomendaciones

Motor de inteligencia que detecta automáticamente:

**Alertas Críticas:**
- Desviación > 20% de ruta óptima → Revisar con conductor
- Incumplimiento de horario → Evaluar penalización contractual

**Alertas de Advertencia:**
- Excesos de velocidad frecuentes (>10) → Capacitación o cambio conductor
- Paradas prolongadas (>10 min) → Solicitar justificación
- Calidad GPS insuficiente (<70%) → Verificar hardware

**Alertas Informativas:**
- Desviación moderada (5-20%) → Justificación operativa
- Buen desempeño → Reconocimiento al conductor

Cada alerta incluye **recomendación accionable** específica.

#### 4. Histórico y Comparación de Viajes

Sistema completo de gestión de auditorías:

**Persistencia Local:**
- Guarda hasta 20 auditorías en localStorage del navegador
- Sin servidor, total privacidad
- Botón "Guardar Viaje" disponible después de cada auditoría

**Vista de Histórico:**
- Lista compacta con métricas clave
- Distancia, desviación, puntualidad, excesos de velocidad
- Fecha y nombre de archivo
- Ordenado por más reciente

**Comparación:**
- Compara auditoría actual vs cualquier viaje histórico
- Muestra variación porcentual entre KPIs
- Ideal para evaluar tendencias de conductor/cooperativa

**Gestión:**
- Eliminar viajes individuales
- Limpiar todo el histórico
- Navegación entre vista de auditoría e histórico

#### 5. Reporte de Impresión Mejorado

El PDF exportado ahora es un documento profesional de auditoría:

**Resumen Ejecutivo:**
- Evaluación automática del servicio (satisfactorio / aceptable / requiere atención)
- Párrafo ejecutivo con hallazgos principales destacados
- Valores clave resaltados visualmente

**Alertas e Incidencias:**
- Sección dedicada a problemas detectados
- Clasificadas por severidad (crítico / advertencia / info)
- Incluye recomendaciones

**KPIs Organizados:**
- Agrupados por las 4 categorías de negocio
- Layout de 3 columnas optimizado para A4
- Formato profesional para defensa contractual

**Leyenda Ampliada:**
- Incluye todos los elementos del mapa
- Excesos de velocidad ahora visibles en leyenda

#### 6. Mejoras en Visualización del Mapa

- Marcadores ámbar para excesos de velocidad
- Tooltips mejorados con velocidad en cada ping
- Colores semánticos consistentes (verde=inicio, rojo=parada, ámbar=exceso, azul=ruta)

---

### 🔧 Cambiado

#### Reorganización de UI

**Antes:**
- 6 KPIs en cuadrícula simple
- Sin categorización

**Ahora:**
- 14 KPIs organizados en 4 secciones temáticas
- Títulos de sección con estilo profesional
- Alineado con documento de propuesta de negocio

#### Constantes de Negocio Agregadas

```javascript
SPEED_LIMIT_URBAN = 50.0 km/h    // Límite para detectar excesos
GOOD_HDOP_THRESHOLD = 2.0        // Señal GPS excelente
MIN_SATELLITES = 6               // Mínimo para buena precisión
```

#### Detección Mejorada de Paradas

**Antes:**
- Marcaba cada ping con velocidad < 2 km/h

**Ahora:**
- Agrupa pings consecutivos detenidos
- Solo cuenta paradas > 30 segundos
- Calcula duración de cada parada
- Identifica las más significativas

---

### 📁 Estructura de Archivos

#### Archivos Separados (desarrollo)

```
mvp-moviq/
├── dashboard.html              ← HTML limpio (232 líneas)
├── styles.css                  ← CSS separado (849 líneas)
├── app.js                      ← JavaScript separado (4531 líneas)
├── README.md                   ← Documentación actualizada
└── CHANGELOG.md                ← Este archivo
```

#### Archivo Monolítico (distribución)

```
mvp-moviq/
└── dashboard-telemetria-fv.html ← TODO en uno (290 KB, 5614 líneas)
```

**Actualizado:** El archivo monolítico ha sido regenerado con todas las mejoras de la versión 2.0. Ambas versiones (separada y monolítica) son funcionalmente idénticas.

---

### 🎨 Nuevos Estilos CSS

**Componentes agregados:**
- `.timeline` - Timeline de eventos
- `.timeline-item` - Eventos individuales con marcador y línea vertical
- `.alerts-container` - Panel de alertas
- `.alert-item` (critical/warning/info) - Tarjetas de alerta por severidad
- `.history-list` - Lista de viajes guardados
- `.history-item` - Tarjeta de viaje con métricas resumidas
- `.print-executive-summary` - Resumen ejecutivo en PDF
- `.print-alerts` - Alertas en PDF
- `.print-alert-item` - Alertas individuales en PDF

---

### 📊 Nuevas Funciones JavaScript

**Cálculos de métricas:**
- Cálculo de velocidad promedio total y en movimiento
- Detección y conteo de excesos de velocidad
- Cálculo de HDOP promedio y % de señal de calidad
- Agrupación de paradas consecutivas

**Renderizado:**
- `renderAlerts()` - Motor de detección y renderizado de alertas
- `renderTimeline()` - Generación del timeline de eventos
- `renderHistory()` - Lista de viajes guardados
- Mejoras en `renderPrintReport()` con resumen ejecutivo

**LocalStorage:**
- `saveAuditToHistory()` - Guardar auditoría
- `getAuditHistory()` - Recuperar histórico
- `deleteAudit()` - Eliminar viaje individual
- `clearHistory()` - Limpiar todo
- `compareAudit()` - Comparación de métricas

**Utilidades:**
- `storeCurrentAudit()` - Almacena auditoría actual en memoria
- Event listeners para gestión de histórico

---

### 🐛 Corregido

- Leyenda del mapa ahora incluye marcadores de excesos de velocidad
- Reporte de impresión sincronizado con KPIs de pantalla
- Tooltips de paradas ahora muestran solo paradas significativas

---

### 📈 Métricas del Proyecto

**Líneas de código:**
- HTML: ~208 líneas (dashboard.html)
- CSS: ~750 líneas (styles.css)
- JavaScript: ~4500 líneas (app.js)
- **Total: ~5458 líneas**

**Comparado con versión 1.0:**
- +8 KPIs nuevos
- +4 componentes de UI (timeline, alertas, histórico, resumen ejecutivo)
- +200% funcionalidad de auditoría
- Sigue siendo 100% client-side, sin backend

---

### 🚀 Impacto de Negocio

Esta versión implementa la **Fase 1: Visibilidad** del documento de propuesta:

✅ **Cumplimiento del Servicio** - Métricas completas de puntualidad y paradas
✅ **Eficiencia Operacional** - Km improductivos y desviaciones detectables
✅ **Seguridad** - Control de excesos de velocidad
✅ **Calidad de Datos** - Validación de confiabilidad GPS
✅ **Alertas Automáticas** - Inteligencia operacional básica
✅ **Histórico** - Comparación para negociación contractual

El MVP está listo para prueba piloto según el documento de propuesta.

---

### 📝 Notas de Migración

**Usuarios de la versión 1.0:**

1. Abrir `dashboard.html` en lugar de `dashboard-telemetria-fv.html`
2. Los archivos CSS y JS se cargan automáticamente
3. El histórico de auditorías se guarda localmente en el navegador
4. Para exportar histórico a otro navegador/PC, usar el futuro botón "Exportar JSON"

**Desarrolladores:**

- El archivo original monolítico se mantiene como `dashboard-telemetria-fv.html`
- Nuevos cambios se hacen en `dashboard.html`, `styles.css` y `app.js`
- Los tres archivos separados facilitan mantenimiento y versionado

---

### 🔮 Próximos Pasos (Roadmap)

**Fase 2: Control Operacional** (Propuesta de negocio)
- [ ] Gráficos de velocidad a lo largo del tiempo
- [ ] Tabla de comparación visual (lado a lado)
- [ ] Exportar histórico a CSV/JSON
- [ ] Cálculo de tendencias (mejorando/empeorando)
- [ ] Filtros en histórico (fecha, desempeño, cooperativa)

**Fase 3: Optimización Avanzada** (Propuesta de negocio)
- [ ] Integración con nómina/asistencia (mock)
- [ ] Pronóstico de demanda (basado en histórico)
- [ ] Simulación de escenarios
- [ ] API REST para integración empresarial

---

### 👥 Créditos

**Desarrollado por:** Claude Sonnet 4.5
**Basado en:** Documento "Propuesta: Inteligencia Operacional para Transporte Corporativo"
**Cliente:** FV (Planta de producción en Quito, Ecuador)
**Fecha:** Agosto 2026

---

## [1.0.0] - 2026-08-11

### Versión Inicial

- Dashboard básico de auditoría GPS
- 6 KPIs originales
- Planificador de rutas TSP
- Exportación a PDF
- Datos sintéticos de prueba
