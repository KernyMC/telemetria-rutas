# CLAUDE.md

Contexto de proyecto para Claude Code. Léelo antes de tocar código en este repo.

## Qué es esto

MVP de **auditoría de telemetría GPS y planificación de rutas** para FV. La empresa
subcontrata una cooperativa de transporte de personal que cobra por kilómetro
recorrido, pero hoy el registro es manual (cuaderno). Este dashboard resuelve dos
problemas de negocio:

1. **Auditoría (post-viaje):** cargar el `.csv` que exporta nuestro hardware GPS
   propio y calcular cuánto se le debe pagar realmente a la cooperativa, detectando
   "kilómetros improductivos" (desvíos, paseos fantasma, vueltas innecesarias) y
   paradas no justificadas.
2. **Planificación (pre-viaje):** dado el personal que confirmó asistencia, generar
   la ruta óptima por calles reales (TSP) desde la Planta FV, para tener una
   referencia de cuántos km/minutos *debería* tomar el viaje.

El dashboard es la fuente de verdad para **auditar la factura de la cooperativa**,
no un mapa decorativo. Cualquier cambio a la lógica de cálculo de KPIs debe
mantenerse defendible frente a un proveedor que va a disputar el número.

## Stack y restricciones duras

- **100% frontend, sin backend, sin build step.** Todo vive en un único archivo
  `.html` que se abre directo en el navegador o se sirve como estático. No
  introducir bundlers, npm scripts, ni un `package.json` a menos que se pida
  explícitamente — romper el "un solo archivo listo para correr" es un cambio de
  alcance, no un detalle técnico.
- **Leaflet** (inyectado nativamente vía CDN, no react-leaflet) para el mapa.
- **OpenStreetMap** (`tile.openstreetmap.org`) como basemap (tiles raster, sin API key; CARTO pasó a exigir key).
- **OSRM público** (`https://router.project-osrm.org`) para routing:
  - `/trip/v1/driving/` → pestaña Planificar Ruta (resuelve TSP con
    `source=first&roundtrip=false`).
  - `/route/v1/driving/` → pestaña Auditoría (ruta ideal entre el primer y
    último punto del CSV, para comparar contra la distancia real).
  - Es el **demo server gratuito** de OSRM, sin SLA. No tiene API key. Si en
    algún momento se necesita confiabilidad real (uso productivo, volumen alto),
    la siguiente iteración es levantar una instancia propia de OSRM en Docker —
    no hackear reintentos infinitos contra el demo público.
- **Lucide** vía CDN (`unpkg.com/lucide`) para iconos estáticos de la UI.
  Los marcadores del mapa (pines, círculos) usan `L.divIcon` con HTML/CSS plano,
  **no** lucide — evita el problema de tener que re-invocar
  `lucide.createIcons()` cada vez que Leaflet inyecta un marcador nuevo en el DOM.
- **Sin frameworks** (no React, no Vue). JS vainilla, un único `<script>` al
  final del `<body>`, envuelto en un IIFE `(function(){ "use strict"; ... })()`.
- **Idioma de la UI: español.** Todos los textos visibles, labels de KPIs,
  tooltips y mensajes de error van en español. Los nombres de variables/funciones
  en el código sí van en inglés (convención normal de JS).

## Estructura del archivo principal

`dashboard-telemetria-fv.html` (nombre puede variar) tiene tres bloques:

1. `<style>` — design tokens en `:root` + CSS del shell (sidebar, tabs, KPIs,
   mapa, `@media print`).
2. `<body>` — markup del sidebar (dos tabs: Auditoría / Planificar Ruta), el
   `<div id="map">`, y un bloque `.print-only` separado que solo se ve al
   imprimir (no confundir con el contenido normal del sidebar, que se **oculta**
   al imprimir).
3. `<script>` — un único IIFE con estas secciones, en este orden:
   - `CONFIG / MOCK DATA` — coordenadas de la Planta FV y lista mock de
     empleados (`EMPLOYEES`).
   - `MAP INIT` — Leaflet + tile layer + dos `L.layerGroup()` separados:
     `planLayer` (pestaña Planificar) y `auditLayer` (pestaña Auditoría). Nunca
     mezclar capas de las dos pestañas en el mismo group; el patrón es
     `layer.clearLayers()` antes de redibujar.
   - `ICONS` — `pinIcon()`, `plantIcon()` (divIcons planos).
   - `HELPERS` — `haversineKm()`, formateadores (`fmtKm`, `fmtDurationMin`,
     `fmtClock`), `fetchJSON()` (wrapper de `fetch` que valida `data.code`).
   - `TABS` / `SIDEBAR TOGGLE` — UI plumbing.
   - `PLANIFICAR RUTA` — render de empleados, toggles, llamada a
     `/trip/v1/driving/`, dibujo de ruta morada.
   - `AUDITORÍA` — carga de CSV (`parseCSV`), generador de datos de prueba
     (`generateTestCSV`), orquestador (`runAudit`), render de mapa
     (`renderAuditMap`), render de KPIs (`renderKPIs`), render del resumen de
     impresión (`renderPrintReport`).

## Contrato de datos: CSV de telemetría

El hardware GPS propio exporta filas con este header exacto (orden importa para
el parseo por índice de columna, aunque `parseCSV` busca por nombre de columna
en el header así que tolera reordenamiento, no falta de columnas):

```
timestamp,latitude,longitude,speed_kmh,heading,altitude,hdop,satellites
```

- `timestamp`: cualquier string parseable por `new Date(...)` (ideal: ISO 8601).
- `speed_kmh`: velocidad instantánea del ping.
- Columnas opcionales para el cálculo de KPIs actuales: `heading`, `altitude`,
  `hdop`, `satellites` (se guardan pero no se usan en los cálculos de negocio
  todavía — quedan disponibles para futuras validaciones de calidad de señal).

Si cambias el formato del CSV de hardware, actualiza `parseCSV()` y el
`generateTestCSV()` (deben seguir produciendo el mismo shape de `records`).

## Fórmulas de negocio (no cambiar sin entender el porqué)

Todas viven en `runAudit()` / `renderKPIs()`:

- **Distancia recorrida (real):** suma de Haversine entre cada par de puntos
  consecutivos del CSV. Es la distancia que se le paga a la cooperativa si no
  hay auditoría.
- **Distancia ideal:** `distance` que devuelve OSRM `/route/v1/driving/` entre
  el primer y último punto del CSV (la ruta más corta por calles reales).
- **Desviación %:** `((real - ideal) / ideal) * 100`.
- **Km improductivos:** `max(0, real - ideal)` — esta es la cifra que
  potencialmente se descuenta del pago a la cooperativa.
- **Tiempo detenido:** suma de los deltas de tiempo entre pings consecutivos
  donde `speed_kmh < 2.0` (constante `STOP_SPEED_THRESHOLD`).
- **Cumplimiento de horario:** "A tiempo" si el primer timestamp del CSV es
  `<= 08:35:00` del mismo día (constantes `ON_TIME_LIMIT_HOURS` /
  `ON_TIME_LIMIT_MIN`). Este umbral es un dato de negocio real de FV — si
  cambia el horario de salida acordado con la cooperativa, actualízalo aquí,
  no hardcodees el string "08:35" en otro lado.

Si se agregan nuevos KPIs, deben mantener el mismo patrón: un objeto de métrica
con `{ icon, color, value, unit, label, tip }` empujado al array `cards` dentro
de `renderKPIs()`, más su contraparte en `renderPrintReport()` para que también
aparezca en el PDF.

## Sistema de diseño

Tokens en `:root` (no usar valores hex sueltos en el CSS, referenciar las
variables):

- Fondo: `--void` / `--panel` / `--panel-raised` (escala de oscuros, estética
  "consola de operaciones GIS/telemetría", no un dashboard SaaS genérico).
- Acento de **Planificar Ruta** = morado (`--accent-purple`), por requerimiento
  explícito del negocio ("dibujar la ruta sugerida en el mapa color morado").
  No cambiar ese color sin confirmarlo — es una convención visual esperada por
  el usuario.
- Acento de **ruta real (GPS)** en Auditoría = azul (`--accent-blue`); ruta
  ideal OSRM = gris punteado; paradas = rojo (`--accent-red`).
- Tipografía: `Space Grotesk` (headers/marca), `Inter` (UI/cuerpo), `JetBrains
  Mono` (todo lo que sea un número/dato/coordenada — KPIs, coordenadas, chips).
  Mantener esta separación: los valores numéricos siempre en mono, el resto en
  Inter.
- Las tarjetas KPI llevan un tooltip (`.kpi-help` + `.kpi-tooltip`) explicando
  la fórmula — es un requerimiento de producto (usuarios auditando plata
  necesitan poder defender de dónde sale cada número), no decoración.

## Exportación a PDF

`exportPdfBtn` solo llama a `window.print()`. Todo el layout de impresión vive
en el bloque `@media print` + el `<div class="print-only" id="printReport">`
que está fuera de `.app` en el DOM. Reglas:

- El sidebar completo se oculta al imprimir (`.sidebar{ display:none }`).
- El `#map` se mantiene visible y se redimensiona a una altura fija en mm para
  A4 (`height:105mm`).
- `renderPrintReport()` debe llamarse siempre en el mismo punto que
  `renderKPIs()` dentro de `runAudit()` — si agregas un KPI a uno, agrégalo al
  otro o el PDF quedará desincronizado del dashboard en pantalla.
- Conocido: la impresión de tiles de Leaflet depende de que el navegador ya los
  tenga renderizados en el DOM al momento de imprimir; funciona en Chrome. Si
  se reporta un mapa en blanco al exportar, no es un bug de lógica de negocio,
  es un tema de captura de canvas/tiles — la solución futura sería congelar el
  mapa a una imagen estática (p. ej. `leaflet-image` o una captura server-side)
  antes de imprimir.

## Cómo correr / probar

No hay build. Abrir el `.html` directamente en el navegador (doble clic o
`Live Server` de VS Code). Requiere internet: tiles de OpenStreetMap, OSRM público y
Google Fonts se cargan desde CDN — no hay modo offline.

Para probar sin un CSV real, usar el botón "Datos de prueba" (pestaña
Auditoría) — genera un recorrido sintético con un desvío deliberado y una
parada, pensado para que los 6 KPIs muestren valores distintos de cero/100% y
sea fácil verificar visualmente que el cálculo tiene sentido.

## Datos mock

`PLANT` y `EMPLOYEES` (coordenadas en Quito, Ecuador) son datos de ejemplo, no
datos reales de FV. Si el usuario pide "conectar datos reales", la pregunta
correcta es de dónde saldrá esa lista (¿RRHH exporta un CSV/JSON de
empleados?), no asumir un backend — este proyecto sigue siendo 100% client-side
salvo que se indique explícitamente lo contrario.

## Qué NO hacer sin que te lo pidan explícitamente

- No agregar un backend, base de datos, o build step (webpack/vite/etc.).
- No migrar a React/Vue "porque es mejor práctica" — el requerimiento original
  fue explícito: client-side puro, un archivo.
- No cambiar el color morado de Planificar Ruta ni el azul de la ruta real en
  Auditoría — son convenciones de negocio, no elección estética libre.
- No romper el flujo `parseCSV → runAudit → renderAuditMap + renderKPIs +
  renderPrintReport` — los tres renders deben quedar sincronizados siempre que
  se audite un viaje nuevo.
