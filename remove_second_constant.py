#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para eliminar la segunda ocurrencia de la constante REAL_GPS_DATA
"""

with open(r'd:\mvp-moviq\dashboard-telemetria-fv.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Buscar todas las ocurrencias del comentario que precede a REAL_GPS_DATA
marker = 'DATOS GPS SINTETICOS REALES'
found_positions = []

for i, line in enumerate(lines):
    if marker in line:
        found_positions.append(i)

print(f'Encontradas {len(found_positions)} ocurrencias del marcador en líneas: {[p+1 for p in found_positions]}')

if len(found_positions) >= 2:
    # La segunda ocurrencia empieza algunas líneas antes del comentario
    # Buscar hacia atrás desde la segunda ocurrencia hasta encontrar el inicio del bloque de comentario
    second_start = found_positions[1]

    # Retroceder unas líneas para capturar todo el bloque de comentario
    block_start = second_start - 3  # Ajustar según sea necesario

    # Buscar el final de la constante (la línea que termina con `;`)
    block_end = second_start
    for i in range(second_start, len(lines)):
        if 'const REAL_GPS_DATA' in lines[i]:
            # Encontrar el cierre de la template string (`;`)
            for j in range(i, min(i+3300, len(lines))):  # 3300 líneas debería cubrir todos los datos
                if lines[j].strip() == '`;':
                    block_end = j + 1
                    break
            break

    print(f'Eliminando bloque desde línea {block_start+1} hasta {block_end+1}')
    print(f'Total de líneas a eliminar: {block_end - block_start}')

    # Eliminar el bloque
    new_lines = lines[:block_start] + lines[block_end:]

    # Guardar
    with open(r'd:\mvp-moviq\dashboard-telemetria-fv.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print('\nSegunda constante REAL_GPS_DATA eliminada con exito')

else:
    print('Solo se encontro una ocurrencia, no hay nada que eliminar')
