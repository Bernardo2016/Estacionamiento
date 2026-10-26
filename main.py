from datetime import datetime

# Diccionario principal para almacenar los vehículos activos en el estacionamiento
# Estructura: { 'PLACA': {'hora_ingreso': 'HH:MM', 'tipo': 'Auto/Moto/Camioneta'} }
estacionamiento = {}

# Catálogo de tipos de vehículos permitidos
TIPOS_VEHICULO = {"1": "Auto", "2": "Moto", "3": "Camioneta"}


def registrar_ingreso():
  print("\n--- MÓDULO 1: REGISTRO DE INGRESO ---")

  # 1. Captura y validación de la Placa
  placa = input("Ingrese la placa del vehículo: ").strip().upper()
  if not placa:
    print(" Error: La placa no puede estar vacía.")
    return

  if placa in estacionamiento:
    print(
        f" El vehículo con placa '{placa}' ya se encuentra dentro del"
        " estacionamiento."
    )
    return

  # 2. Selección del Tipo de Vehículo
  print("\nSeleccione el tipo de vehículo:")
  for clave, valor in TIPOS_VEHICULO.items():
    print(f"  {clave}. {valor}")

  opcion_tipo = input("Opción (1-3): ").strip()
  if opcion_tipo not in TIPOS_VEHICULO:
    print(" Error: Tipo de vehículo no válido.")
    return
  tipo_vehiculo = TIPOS_VEHICULO[opcion_tipo]

  # 3. Captura de la Hora de Ingreso
  print("\nHora de ingreso:")
  print("  1. Usar hora actual del sistema")
  print("  2. Ingresar hora manualmente (formato HH:MM)")
  opcion_hora = input("Opción (1-2): ").strip()

  if opcion_hora == "1":
    hora_ingreso = datetime.now().strftime("%H:%M")
  elif opcion_hora == "2":
    hora_manual = input("Ingrese la hora (HH:MM, ej. 14:30): ").strip()
    try:
      # Validamos que el formato ingresado sea realmente una hora válida
      datetime.strptime(hora_manual, "%H:%M")
      hora_ingreso = hora_manual
    except ValueError:
      print(" Error: Formato de hora inválido. Debe ser HH:MM en formato 24h.")
      return
  else:
    print(" Error: Opción de hora no válida.")
    return

  # 4. Guardar el registro
  estacionamiento[placa] = {"hora_ingreso": hora_ingreso, "tipo": tipo_vehiculo}

  print(f"\n Registro exitoso:")
  print(
      f"   Placa: {placa} | Tipo: {tipo_vehiculo} | Hora de entrada:"
      f" {hora_ingreso}"
  )


def mostrar_vehiculos_activos():
  """Función auxiliar para verificar los registros del Módulo 1."""
  print("\n--- VEHÍCULOS EN EL ESTACIONAMIENTO ---")
  if not estacionamiento:
    print("El estacionamiento está vacío.")
    return

  print(f"{'PLACA':<10} | {'TIPO':<12} | {'HORA INGRESO':<12}")
  print("-" * 40)
  for placa, datos in estacionamiento.items():
    print(f"{placa:<10} | {datos['tipo']:<12} | {datos['hora_ingreso']:<12}")


# Menú de prueba para el Módulo 1
def menu_modulo_1():
  while True:
    print("\n=== SISTEMA DE ESTACIONAMIENTO ===")
    print("1. Registrar ingreso de vehículo (Módulo 1)")
    print("2. Ver vehículos estacionados")
    print("3. Salir")

    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
      registrar_ingreso()
    elif opcion == "2":
      mostrar_vehiculos_activos()
    elif opcion == "3":
      print("Saliendo del programa...")
      break
    else:
      print(" Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
  menu_modulo_1()