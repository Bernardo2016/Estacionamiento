from datetime import datetime, timedelta
import math

# Diccionario de vehículos activos
# Estructura: { 'PLACA': {'hora_ingreso': 'HH:MM', 'tipo': 'Auto/Moto/Camioneta'} }
estacionamiento = {}

# Historial de cobros realizados (útil para un futuro módulo de corte de caja)
historial_cobros = []

TIPOS_VEHICULO = {"1": "Auto", "2": "Moto", "3": "Camioneta"}

# Tarifas por hora o fracción según el tipo de vehículo
TARIFAS_POR_HORA = {"Moto": 15.00, "Auto": 25.00, "Camioneta": 35.00}


# ==========================================
# MÓDULO 1: REGISTRO DE INGRESO
# ==========================================
def registrar_ingreso():
  print("\n--- MÓDULO 1: REGISTRO DE INGRESO ---")
  placa = input("Ingrese la placa del vehículo: ").strip().upper()

  if not placa:
    print("❌ Error: La placa no puede estar vacía.")
    return

  if placa in estacionamiento:
    print(
        f"⚠️ El vehículo con placa '{placa}' ya está dentro del"
        " estacionamiento."
    )
    return

  print("\nSeleccione el tipo de vehículo:")
  for clave, valor in TIPOS_VEHICULO.items():
    print(f"  {clave}. {valor} (${TARIFAS_POR_HORA[valor]:.2f}/hora)")

  opcion_tipo = input("Opción (1-3): ").strip()
  if opcion_tipo not in TIPOS_VEHICULO:
    print("❌ Error: Tipo de vehículo no válido.")
    return
  tipo_vehiculo = TIPOS_VEHICULO[opcion_tipo]

  print("\nHora de ingreso:")
  print("  1. Usar hora actual del sistema")
  print("  2. Ingresar hora manualmente (formato HH:MM)")
  opcion_hora = input("Opción (1-2): ").strip()

  if opcion_hora == "1":
    hora_ingreso = datetime.now().strftime("%H:%M")
  elif opcion_hora == "2":
    hora_manual = input("Ingrese la hora de entrada (HH:MM, ej. 14:30): ").strip()
    try:
      datetime.strptime(hora_manual, "%H:%M")
      hora_ingreso = hora_manual
    except ValueError:
      print("❌ Error: Formato inválido. Use HH:MM en formato 24h.")
      return
  else:
    print("❌ Error: Opción no válida.")
    return

  estacionamiento[placa] = {"hora_ingreso": hora_ingreso, "tipo": tipo_vehiculo}
  print(
      f"\n✅ Ingreso registrado: Placa {placa} | {tipo_vehiculo} | Entrada:"
      f" {hora_ingreso}"
  )


# ==========================================
# MÓDULO 2: CÁLCULO DE TARIFA Y COBRO
# ==========================================
def calcular_tiempo_y_monto(hora_ingreso_str, hora_salida_str, tipo_vehiculo):
  """Calcula los minutos transcurridos, las horas a cobrar (hora o fracción) y el total."""
  formato = "%H:%M"
  t_ingreso = datetime.strptime(hora_ingreso_str, formato)
  t_salida = datetime.strptime(hora_salida_str, formato)

  # Si la hora de salida es menor a la de entrada, asumimos que cruzó la medianoche
  if t_salida < t_ingreso:
    t_salida += timedelta(days=1)

  diferencia = t_salida - t_ingreso
  minutos_totales = int(diferencia.total_seconds() // 60)

  # Cobro por hora o fracción (mínimo 1 hora aunque esté pocos minutos)
  if minutos_totales == 0:
    horas_cobrar = 1
  else:
    horas_cobrar = math.ceil(minutos_totales / 60)

  tarifa_unitaria = TARIFAS_POR_HORA[tipo_vehiculo]
  total_pagar = horas_cobrar * tarifa_unitaria

  return minutos_totales, horas_cobrar, tarifa_unitaria, total_pagar


def registrar_salida_y_cobro():
  print("\n--- MÓDULO 2: SALIDA Y COBRO DE TARIFA ---")
  if not estacionamiento:
    print("ℹ️ No hay vehículos en el estacionamiento actualmente.")
    return

  placa = input("Ingrese la placa del vehículo que sale: ").strip().upper()

  if placa not in estacionamiento:
    print(
        f"❌ Error: No se encontró ningún vehículo activo con la placa"
        f" '{placa}'."
    )
    return

  datos_vehiculo = estacionamiento[placa]
  hora_ingreso = datos_vehiculo["hora_ingreso"]
  tipo = datos_vehiculo["tipo"]

  print(
      f"\nVehículo encontrado -> Tipo: {tipo} | Hora de entrada: {hora_ingreso}"
  )
  print("Hora de salida:")
  print("  1. Usar hora actual del sistema")
  print("  2. Ingresar hora manualmente (formato HH:MM)")
  opcion_hora = input("Opción (1-2): ").strip()

  if opcion_hora == "1":
    hora_salida = datetime.now().strftime("%H:%M")
  elif opcion_hora == "2":
    hora_manual = input("Ingrese la hora de salida (HH:MM, ej. 16:45): ").strip()
    try:
      datetime.strptime(hora_manual, "%H:%M")
      hora_salida = hora_manual
    except ValueError:
      print("❌ Error: Formato inválido. Use HH:MM en formato 24h.")
      return
  else:
    print("❌ Error: Opción no válida.")
    return

  # Realizar cálculo de tarifa
  minutos, horas_cobrar, tarifa, total = calcular_tiempo_y_monto(
      hora_ingreso, hora_salida, tipo
  )
  horas_reales = minutos // 60
  minutos_restantes = minutos % 60

  # Mostrar desglose del ticket
  print("\n" + "=" * 38)
  print("         TICKET DE ESTACIONAMIENTO")
  print("=" * 38)
  print(f" Placa:             {placa}")
  print(f" Tipo de vehículo:  {tipo}")
  print(f" Hora de entrada:   {hora_ingreso}")
  print(f" Hora de salida:    {hora_salida}")
  print(f" Tiempo estancia:   {horas_reales}h {minutos_restantes}min")
  print(f" Horas a cobrar:    {horas_cobrar} hr(s) (Hora o fracción)")
  print(f" Tarifa por hora:   ${tarifa:.2f}")
  print("-" * 38)
  print(f" TOTAL A PAGAR:     ${total:.2f}")
  print("=" * 38)

  # Proceso de pago (caja)
  while True:
    try:
      pago = float(input(f"\nIngrese el monto recibido ($): "))
      if pago < total:
        faltante = total - pago
        print(f"⚠️ Monto insuficiente. Faltan ${faltante:.2f}")
      else:
        cambio = pago - total
        print(f"✅ Pago registrado con éxito. Su cambio es: ${cambio:.2f}")
        break
    except ValueError:
      print("❌ Error: Ingrese una cantidad numérica válida.")

  # Liberar espacio del estacionamiento y guardar en el historial
  del estacionamiento[placa]
  historial_cobros.append({
      "placa": placa,
      "tipo": tipo,
      "entrada": hora_ingreso,
      "salida": hora_salida,
      "horas_cobradas": horas_cobrar,
      "total": total,
  })
  print(f"🚗 El vehículo '{placa}' ha salido del estacionamiento.")


def mostrar_vehiculos_activos():
  print("\n--- VEHÍCULOS EN EL ESTACIONAMIENTO ---")
  if not estacionamiento:
    print("El estacionamiento está vacío.")
    return

  print(f"{'PLACA':<10} | {'TIPO':<12} | {'HORA INGRESO':<12}")
  print("-" * 40)
  for placa, datos in estacionamiento.items():
    print(f"{placa:<10} | {datos['tipo']:<12} | {datos['hora_ingreso']:<12}")


# ==========================================
# MENÚ PRINCIPAL
# ==========================================
def menu_principal():
  while True:
    print("\n=== SISTEMA DE ESTACIONAMIENTO ===")
    print("1. Registrar ingreso de vehículo (Módulo 1)")
    print("2. Registrar salida y cobro (Módulo 2)")
    print("3. Ver vehículos estacionados actualmente")
    print("4. Salir")

    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
      registrar_ingreso()
    elif opcion == "2":
      registrar_salida_y_cobro()
    elif opcion == "3":
      mostrar_vehiculos_activos()
    elif opcion == "4":
      print("Saliendo del programa...")
      break
    else:
      print("⚠️ Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
  menu_principal()