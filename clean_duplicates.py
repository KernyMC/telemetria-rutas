#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para limpiar las duplicaciones en el HTML
"""

# Leer el HTML con duplicaciones
with open(r'd:\mvp-moviq\dashboard-telemetria-fv.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# PASO 1: Eliminar la segunda constante REAL_GPS_DATA
# Buscar el patrón que se repite y eliminar la segunda ocurrencia

# Encontrar todas las ocurrencias de la constante
import re
pattern = r'/\* ={60,}\s+DATOS GPS SINTETICOS REALES.*?const REAL_GPS_DATA = `.*?`;'
matches = list(re.finditer(pattern, html_content, re.DOTALL))

if len(matches) > 1:
    print(f"Encontradas {len(matches)} ocurrencias de REAL_GPS_DATA. Eliminando duplicados...")
    # Eliminar todas las ocurrencias excepto la primera
    for match in reversed(matches[1:]):
        start, end = match.span()
        html_content = html_content[:start] + html_content[end:]
    print(f"Duplicados de REAL_GPS_DATA eliminados")

# PASO 2: Eliminar el event listener duplicado
listener_pattern = r'const loadRealDemoBtn = document\.getElementById\(\'loadRealDemoBtn\'\);.*?runAudit\(REAL_GPS_DATA, currentFileName\);.*?\}\);'
listener_matches = list(re.finditer(listener_pattern, html_content, re.DOTALL))

if len(listener_matches) > 1:
    print(f"Encontradas {len(listener_matches)} ocurrencias del listener. Eliminando duplicados...")
    # Eliminar todas las ocurrencias excepto la primera
    for match in reversed(listener_matches[1:]):
        start, end = match.span()
        html_content = html_content[:start] + html_content[end:]
    print(f"Duplicados del listener eliminados")

# Guardar el HTML limpio
with open(r'd:\mvp-moviq\dashboard-telemetria-fv.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\nHTML limpiado con exito")
print("Archivo actualizado: dashboard-telemetria-fv.html")
