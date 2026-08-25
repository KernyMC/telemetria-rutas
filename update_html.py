#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para agregar los datos GPS sintéticos reales al dashboard HTML
"""

# Leer el HTML original
with open(r'd:\mvp-moviq\dashboard-telemetria-fv.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Leer los datos GPS reales
with open(r'd:\mvp-moviq\ruta_FV_gps_sintetico.csv', 'r', encoding='utf-8') as f:
    gps_data = f.read()

# ===== PASO 1: Agregar la constante REAL_GPS_DATA =====
# Buscar la línea "const STOP_SPEED_THRESHOLD = 2.0; // km/h"
# e insertar la constante justo después

insertion_point_1 = "const STOP_SPEED_THRESHOLD = 2.0; // km/h"
real_gps_constant = f"""
/* ============================================================
   DATOS GPS SINTÉTICOS REALES
   ============================================================ */
// Datos GPS reales generados a partir de la ruta Google My Maps
// Quitumbe -> FV Area Andina, 3241 puntos @ 1Hz
// Fuente: ruta_FV_gps_sintetico.xlsx
const REAL_GPS_DATA = `{gps_data}`;
"""

html_content = html_content.replace(
    insertion_point_1,
    insertion_point_1 + real_gps_constant
)

# ===== PASO 2: Agregar el nuevo botón "Datos sintéticos FV" =====
# Buscar la línea con el botón "Datos de prueba" y agregar uno nuevo después

old_button_html = '''          <div class="btn-row">
            <button class="btn btn-primary" id="loadCsvBtn"><i data-lucide="upload"></i>Cargar CSV</button>
            <button class="btn btn-outline-blue" id="loadDemoBtn"><i data-lucide="flask-conical"></i>Datos de prueba</button>
          </div>'''

new_button_html = '''          <div class="btn-row">
            <button class="btn btn-primary" id="loadCsvBtn"><i data-lucide="upload"></i>Cargar CSV</button>
          </div>
          <div style="height:8px"></div>
          <div class="btn-row">
            <button class="btn btn-outline-blue" id="loadDemoBtn"><i data-lucide="flask-conical"></i>Datos de prueba</button>
            <button class="btn btn-outline-blue" id="loadRealDemoBtn"><i data-lucide="route"></i>Datos sintéticos FV</button>
          </div>'''

html_content = html_content.replace(old_button_html, new_button_html)

# ===== PASO 3: Agregar el event listener para el nuevo botón =====
# Buscar la línea del event listener del botón demo y agregar uno nuevo después

old_listener = """loadDemoBtn.addEventListener('click', ()=>{
  currentFileName = 'telemetria_prueba_demo.csv';
  runAudit(generateTestCSV(), currentFileName);
});"""

new_listener = """loadDemoBtn.addEventListener('click', ()=>{
  currentFileName = 'telemetria_prueba_demo.csv';
  runAudit(generateTestCSV(), currentFileName);
});

const loadRealDemoBtn = document.getElementById('loadRealDemoBtn');
loadRealDemoBtn.addEventListener('click', ()=>{
  currentFileName = 'ruta_FV_gps_sintetico.csv';
  runAudit(REAL_GPS_DATA, currentFileName);
});"""

html_content = html_content.replace(old_listener, new_listener)

# Guardar el HTML modificado
with open(r'd:\mvp-moviq\dashboard-telemetria-fv.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Dashboard actualizado con exito")
print("Se agrego la constante REAL_GPS_DATA (3241 registros GPS)")
print("Se agrego el boton 'Datos sinteticos FV'")
print("Se configuro el event listener para cargar los datos reales")
