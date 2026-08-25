# Leer todo el CSV
with open(r'd:\mvp-moviq\ruta_FV_gps_sintetico.csv', 'r', encoding='utf-8') as f:
    content = f.read()

# Guardar en una variable JavaScript
with open(r'd:\mvp-moviq\real_gps_data.js', 'w', encoding='utf-8') as f:
    f.write('const REAL_GPS_DATA = `')
    f.write(content)
    f.write('`;')

print('Archivo JS generado: real_gps_data.js')
print(f'Tamaño: {len(content)} caracteres')
