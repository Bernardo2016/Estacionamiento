from datetime import datetime, timedelta
import math

# Diccionario de vehículos activos
# Estructura: { 'PLACA': {'hora_ingreso': 'HH:MM', 'tipo': 'Auto/Moto/Camioneta', 'cajon': 'A-1'} }
estacionamiento = {}

# Historial de cobros realizados
historial_cobros = []

TIPOS_VEHICULO = {"1": "Auto", "2": "Moto", "3": "Camioneta"}

TARIFAS_POR_HORA = {"Moto": 15.00, "Auto": 25.00, "Camioneta": 35.00}

# ==========================================
# CONFIGURACIÓN DE CAPACIDAD Y CAJONES (MÓDULO 3)
# ==========================================
CAPACIDAD_MAXIMA = {"Auto": 10, "Moto": 5, "Camioneta": 5}

# Generación dinámica de cajones (None = Libre, 'PLACA' = Ocupado)
# Ejemplo: {'Auto': {'A-1': None, 'A-2': None...}, 'Moto': {'M-1': None...}}
cajones = {
    "Auto": {f"A-{i}": None for i in range(1, CAPACIDAD_MAXIMA["Auto"] + 1)},
    "Moto": {f"M-{i}": None for i in range(1, CAPACIDAD_MAXIMA["Moto"] + 1)},
    "Camioneta": {
        f"C-{i}": None for i in range(1, CAPACIDAD_MAXIMA["Camioneta"] + 1)
    },
}


def obtener_cajon_disponible(tipo_vehiculo):
  """Busca y retorna el primer cajón libre para el tipo de vehículo dado."""
  for codigo_cajon, placa_ocupante in cajones[tipo_vehiculo].items():
    if placa_ocupante is None:
      return codigo_cajon
  return None


def contar_disponibles(tipo_vehiculo):
  """Cuenta cuántos cajones libres quedan de un tipo específico."""
  return sum(
      1 for ocupante in cajones[tipo_vehiculo].values() if ocupante is None
  )


# ==========================================
# MÓDULO 3: MONITOR DE DISPONIBILIDAD EN TIEMPO REAL
# ==========================================
def mostrar_disponibilidad_tiempo_real():
  print("\n" + "=" * 52)
  print("      ESTADO DEL ESTACIONAMIENTO EN TIEMPO REAL")
  print("=" * 52)

  total_capacidad = sum(CAPACIDAD_MAXIMA.values())
  total_ocupados = len(estacionamiento)
  total_libres = total_capacidad - total_ocupados

  print(
      f" Ocupación Global: {total_ocupados}/{total_capacidad} ocupados |"
      f" {total_libres} disponibles\n"
  )

  # 1. Resumen con barra de progreso por tipo
  print(f" {'TIPO':<10} | {'LIBRES':<8} | {'OCUPADOS':<8} | {'ESTADO'}")
  print("-" * 52)
  for tipo, max_cap in CAPACIDAD_MAXIMA.items():
    libres = contar_disponibles(tipo)
    ocupados = max_cap - libres
    # Barra visual: ■ ocupado, □ libre
    barra = "■" * ocupados + "□" * libres
    estado_txt = "LLENO" if libres == 0 else "DISPONIBLE"
    print(
        f" {tipo:<10} | {libres:<8} | {ocupados:<8} | [{barra}] ({estado_txt})"
    )

  # 2. Mapa detallado de cajones
  print("\n--- MAPA DE CAJONES ( [Libre] / [Placa] ) ---")
  for tipo, lista_cajones in cajones.items():
    print(f"\nZona {tipo}s:")
    fila = "  "
    contador = 0
    for codigo, placa in lista_cajones.items():
      estado = f"🟢 {codigo}: Libre" if placa is None else f"🔴 {codigo}: {placa}"
      fila += f"[{estado:<15}]  "
      contador += 1
      # Salto de línea cada 3 cajones para que se vea ordenado en consola
      if contador % 3 == 0:
        print(fila)
        fila = "  "
    if fila.strip():
      print(fila)
  print("=" * 52)


# ==========================================
# MÓDULO 1: REGISTRO DE INGRESO (Con asignación de cajón)
# ==========================================
def registrar_ingreso():
  print("\n--- MÓDULO 1: REGISTRO DE INGRESO ---")

  # Verificar si el estacionamiento entero está lleno antes de pedir datos
  if len(estacionamiento) >= sum(CAPACIDAD_MAXIMA.values()):
    print(
        "⛔ ESTACIONAMIENTO LLENO: No hay lugares disponibles en ninguna"
        " categoría."
    )
    return

  placa = input("Ingrese la placa del vehículo: ").strip().upper()
  if not placa:
    print("❌ Error: La placa no puede estar vacía.")
    return

  if placa in estacionamiento:
    cajon_actual = estacionamiento[placa]["cajon"]
    print(
        f"⚠️ El vehículo con placa '{placa}' ya está adentro (Cajón"
        f" {cajon_actual})."
    )
    return

  print("\nSeleccione el tipo de vehículo:")
  for clave, valor in TIPOS_VEHICULO.items():
    libres = contar_disponibles(valor)
    estado_cupo = f"{libres} disponibles" if libres > 0 else "AGOTADO"
    print(
        f"  {clave}. {valor:<10} (${TARIFAS_POR_HORA[valor]:.2f}/h) ->"
        f" [{estado_cupo}]"
    )

  opcion_tipo = input("Opción (1-3): ").strip()
  if opcion_tipo not in TIPOS_VEHICULO:
    print("❌ Error: Tipo de vehículo no válido.")
    return
  tipo_vehiculo = TIPOS_VEHICULO[opcion_tipo]

  # Validar disponibilidad en tiempo real para esa categoría
  cajon_asignado = obtener_cajon_disponible(tipo_vehiculo)
  if cajon_asignado is None:
    print(
        f"⛔ Cupo lleno: No quedan cajones disponibles para '{tipo_vehiculo}'."
    )
    return

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

  # Ocupar cajón en tiempo real y guardar registro
  cajones[tipo_vehiculo][cajon_asignado] = placa
  estacionamiento[placa] = {
      "hora_ingreso": hora_ingreso,
      "tipo": tipo_vehiculo,
      "cajon": cajon_asignado,
  }

  libres_restantes = contar_disponibles(tipo_vehiculo)
  print(f"\n✅ Ingreso registrado con éxito:")
  print(
      f"   Placa: {placa} | Tipo: {tipo_vehiculo} | Cajón asignado:"
      f" [{cajon_asignado}] | Entrada: {hora_ingreso}"
  )
  print(
      f"   📊 Quedan {libres_restantes} lugar(es) disponible(s) para"
      f" {tipo_vehiculo}."
  )


# ==========================================
# MÓDULO 2: CÁLCULO DE TARIFA Y COBRO (Con liberación de cajón)
# ==========================================
def calcular_tiempo_y_monto(hora_ingreso_str, hora_salida_str, tipo_vehiculo):
  formato = "%H:%M"
  t_ingreso = datetime.strptime(hora_ingreso_str, formato)
  t_salida = datetime.strptime(hora_salida_str, formato)

  if t_salida < t_ingreso:
    t_salida += timedelta(days=1)

  diferencia = t_salida - t_ingreso
  minutos_totales = int(diferencia.total_seconds() // 60)

  horas_cobrar = 1 if minutos_totales == 0 else math.ceil(minutos_totales / 60)
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
  cajon = datos_vehiculo["cajon"]

  print(
      f"\nVehículo encontrado -> Cajón: [{cajon}] | Tipo: {tipo} | Entrada:"
      f" {hora_ingreso}"
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

  minutos, horas_cobrar, tarifa, total = calcular_tiempo_y_monto(
      hora_ingreso, hora_salida, tipo
  )
  horas_reales = minutos // 60
  minutos_restantes = minutos % 60

  print("\n" + "=" * 38)
  print("         TICKET DE ESTACIONAMIENTO")
  print("=" * 38)
  print(f" Placa:             {placa}")
  print(f" Cajón ocupado:     {cajon}")
  print(f" Tipo de vehículo:  {tipo}")
  print(f" Hora de entrada:   {hora_ingreso}")
  print(f" Hora de salida:    {hora_salida}")
  print(f" Tiempo estancia:   {horas_reales}h {minutos_restantes}min")
  print(f" Horas a cobrar:    {horas_cobrar} hr(s) (Hora o fracción)")
  print(f" Tarifa por hora:   ${tarifa:.2f}")
  print("-" * 38)
  print(f" TOTAL A PAGAR:     ${total:.2f}")
  print("=" * 38)

  while True:
    try:
      pago = float(input(f"\nIngrese el monto recibido ($): "))
      if pago < total:
        print(f"⚠️ Monto insuficiente. Faltan ${total - pago:.2f}")
      else:
        cambio = pago - total
        print(f"✅ Pago registrado. Su cambio es: ${cambio:.2f}")
        break
    except ValueError:
      print("❌ Error: Ingrese una cantidad numérica válida.")

  # Liberar el cajón en tiempo real y eliminar de vehículos activos
  cajones[tipo][cajon] = None
  del estacionamiento[placa]

  historial_cobros.append({
      "placa": placa,
      "cajon": cajon,
      "tipo": tipo,
      "entrada": hora_ingreso,
      "salida": hora_salida,
      "horas_cobradas": horas_cobrar,
      "total": total,
  })

  libres_actuales = contar_disponibles(tipo)
  print(
      f"🚗 Vehículo '{placa}' retirado. El cajón [{cajon}] ahora está LIBRE."
  )
  print(f"📊 Lugares disponibles para {tipo}: {libres_actuales}")


def mostrar_vehiculos_activos():
  print("\n--- LISTA DE VEHÍCULOS ESTACIONADOS ---")
  if not estacionamiento:
    print("El estacionamiento está vacío.")
    return

  print(f"{'CAJÓN':<8} | {'PLACA':<10} | {'TIPO':<12} | {'HORA INGRESO':<12}")
  print("-" * 50)
  for placa, datos in estacionamiento.items():
    print(
        f"{datos['cajon']:<8} | {placa:<10} | {datos['tipo']:<12} |"
        f" {datos['hora_ingreso']:<12}"
    )


# ==========================================
# MENÚ PRINCIPAL CON INDICADOR EN VIVO
# ==========================================
def menu_principal():
  while True:
    total_cap = sum(CAPACIDAD_MAXIMA.values())
    libres_totales = total_cap - len(estacionamiento)

    print("\n" + "=" * 44)
    print(
        "   SISTEMA DE ESTACIONAMIENTO [Lugares Libres:"
        f" {libres_totales}/{total_cap}]"
    )
    print("=" * 44)
    print("1. Registrar ingreso de vehículo (Módulo 1)")
    print("2. Registrar salida y cobro (Módulo 2)")
    print("3. Ver disponibilidad y mapa en tiempo real (Módulo 3)")
    print("4. Ver lista de vehículos estacionados")
    print("5. Salir")

    opcion = input("\nSeleccione una opción: ").strip()

    if opcion == "1":
      registrar_ingreso()
    elif opcion == "2":
      registrar_salida_y_cobro()
    elif opcion == "3":
      mostrar_disponibilidad_tiempo_real()
    elif opcion == "4":
      mostrar_vehiculos_activos()
    elif opcion == "5":
      print("Saliendo del programa...")
      break
    else:
      print("⚠️ Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
  menu_principal()