#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script corregido para agregar los datos GPS sintéticos reales al dashboard HTML
(evita duplicaciones)
"""

# Leer el HTML ORIGINAL (hacer backup primero si es necesario)
with open(r'd:\mvp-moviq\dashboard-telemetria-fv.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Leer los datos GPS reales
with open(r'd:\mvp-moviq\ruta_FV_gps_sintetico.csv', 'r', encoding='utf-8') as f:
    gps_data = f.read()

# Verificar si ya se aplicaron los cambios (para evitar duplicados)
if 'REAL_GPS_DATA' in html_content:
    print("ADVERTENCIA: El archivo ya contiene REAL_GPS_DATA")
    print("Eliminando duplicados y rehaciendo la integración...")

    # Revertir a una versión limpia: eliminar todas las inserciones previas
    # Método: cargar el archivo original de nuevo desde git si existe, o pedirle al usuario
    print("\nPor favor, restaura el archivo original primero.")
    print("Puedes usar: git checkout dashboard-telemetria-fv.html")
    exit(1)

# Si llegamos aquí, el archivo está limpio y podemos proceder
print("Archivo HTML limpio detectado. Aplicando cambios...")

# ===== PASO 1: Agregar la constante REAL_GPS_DATA =====
insertion_point_1 = "const STOP_SPEED_THRESHOLD = 2.0; // km/h"

# Verificar que el punto de inserción existe
if insertion_point_1 not in html_content:
    print(f"ERROR: No se encontró el punto de inserción: {insertion_point_1}")
    exit(1)

real_gps_constant = f"""
/* ============================================================
   DATOS GPS SINTETICOS REALES
   ============================================================ */
// Datos GPS reales generados a partir de la ruta Google My Maps
// Quitumbe -> FV Area Andina, 3241 puntos @ 1Hz
// Fuente: ruta_FV_gps_sintetico.xlsx
const REAL_GPS_DATA = `{gps_data}`;
"""

# Hacer el reemplazo UNA SOLA VEZ
html_content = html_content.replace(
    insertion_point_1,
    insertion_point_1 + real_gps_constant,
    1  # Solo reemplazar la primera ocurrencia
)

# ===== PASO 2: Agregar el nuevo botón =====
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
            <button class="btn btn-outline-blue" id="loadRealDemoBtn"><i data-lucide="route"></i>Datos sinteticos FV</button>
          </div>'''

if old_button_html in html_content:
    html_content = html_content.replace(old_button_html, new_button_html, 1)
else:
    print("ADVERTENCIA: No se pudo encontrar el HTML del botón original")

# ===== PASO 3: Agregar el event listener =====
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

if old_listener in html_content:
    html_content = html_content.replace(old_listener, new_listener, 1)
else:
    print("ADVERTENCIA: No se pudo encontrar el listener original")

# Guardar el HTML modificado
with open(r'd:\mvp-moviq\dashboard-telemetria-fv-updated.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\nDashboard actualizado con exito")
print("Archivo guardado como: dashboard-telemetria-fv-updated.html")
print("Se agrego la constante REAL_GPS_DATA (3241 registros GPS)")
print("Se agrego el boton 'Datos sinteticos FV'")
print("Se configuro el event listener para cargar los datos reales")
print("\nPor favor, revisa el archivo y renombralo a dashboard-telemetria-fv.html si todo está OK")
