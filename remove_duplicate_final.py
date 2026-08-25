#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script definitivo para eliminar duplicados de REAL_GPS_DATA
"""

with open(r'd:\mvp-moviq\dashboard-telemetria-fv.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Buscar todas las líneas que contienen 'const REAL_GPS_DATA'
gps_data_positions = []
for i, line in enumerate(lines):
    if 'const REAL_GPS_DATA' in line:
        gps_data_positions.append(i)

print(f'Encontradas {len(gps_data_positions)} ocurrencias de REAL_GPS_DATA en líneas: {[p+1 for p in gps_data_positions]}')

if len(gps_data_positions) >= 2:
    # Eliminar desde la segunda ocurrencia
    second_start = gps_data_positions[1]

    # Retroceder para incluir el comentario (normalmente 5-6 líneas antes)
    block_start = second_start - 6

    # Buscar el cierre de la template string
    block_end = second_start
    for i in range(second_start, min(second_start + 3300, len(lines))):
        if lines[i].strip() == '`;':
            block_end = i + 1
            break

    print(f'\nEliminando bloque duplicado:')
    print(f'  Desde línea: {block_start+1}')
    print(f'  Hasta línea: {block_end}')
    print(f'  Total líneas: {block_end - block_start}')

    # Crear nueva lista sin el bloque duplicado
    new_lines = lines[:block_start] + lines[block_end:]

    # También necesitamos eliminar los event listeners duplicados
    # Buscar y contar
    listener_count = 0
    listener_positions = []
    for i, line in enumerate(new_lines):
        if 'const loadRealDemoBtn = document.getElementById' in line:
            listener_positions.append(i)
            listener_count += 1

    if len(listener_positions) > 1:
        print(f'\nTambién se encontraron {len(listener_positions)} event listeners duplicados')
        print(f'Eliminando duplicados del listener...')
        # Eliminar el listener adicional (que probablemente está unas 4 líneas después)
        for pos in reversed(listener_positions[1:]):
            # Eliminar desde esa línea hasta el cierre del listener (normalmente 4 líneas)
            del new_lines[pos:pos+5]

    # Guardar
    with open(r'd:\mvp-moviq\dashboard-telemetria-fv.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print('\nArchivo limpiado exitosamente')
    print('dashboard-telemetria-fv.html actualizado')

else:
    print('Solo hay una ocurrencia, no hay duplicados que eliminar')

# Verificar el resultado final
with open(r'd:\mvp-moviq\dashboard-telemetria-fv.html', 'r', encoding='utf-8') as f:
    content = f.read()
    gps_count = content.count('const REAL_GPS_DATA')
    listener_count = content.count('loadRealDemoBtn')
    print(f'\nVerificacion final:')
    print(f'  REAL_GPS_DATA: {gps_count} ocurrencia(s)')
    print(f'  loadRealDemoBtn: {listener_count} ocurrencia(s)')
