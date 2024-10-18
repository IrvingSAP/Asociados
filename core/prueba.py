from datetime import datetime
def invierte_Fecha(c1,valor):
    invertida = "".join(reversed(valor.split(c1)))
    return invertida

print(invierte_Fecha('-','30-12-2024'))

fecha_actual = datetime.now().strftime("%Y%m%d")
print(fecha_actual)  # Salida: 20241012 (si la fecha actual es 12 de octubre de 2024)


