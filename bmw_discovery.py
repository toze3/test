#!/usr/bin/env python3
# BMW i3S 120Ah — MQTT Discovery para Home Assistant
# Uso: python3 bmw_discovery.py <user> <password> <VIN>
# Exemplo: python3 bmw_discovery.py mqtt-ha a_tua_pass WBY8P610807F39507

import json
import sys
import subprocess

# ── Configuração ──────────────────────────────────────────────────────────────
MQTT_HOST = "192.168.0.101"
MQTT_PORT = "1883"
MQTT_USER = sys.argv[1] if len(sys.argv) > 1 else "ha"
MQTT_PASS = sys.argv[2] if len(sys.argv) > 2 else "toze3"
VIN       = sys.argv[3] if len(sys.argv) > 3 else "WBY8P610807F39507"

BASE = f"bmw/vehicles/{VIN}"

DEVICE = {
    "identifiers": ["bmw_i3s_120ah"],
    "name": "BMW i3S 120Ah",
    "manufacturer": "BMW",
    "model": "i3S 120Ah"
}

# ── Sensores normais ──────────────────────────────────────────────────────────
SENSORS = [

    # Bateria
    {
        "unique_id": "bmw_i3s_soc",
        "name": "BMW i3S - Bateria SOC",
        "state_topic": f"{BASE}/vehicle.drivetrain.batteryManagement.header",
        "value_template": "{{ value_json.value }}",
        "unit_of_measurement": "%",
        "device_class": "battery",
        "state_class": "measurement",
        "icon": "mdi:battery-electric-vehicle",
    },
    {
        "unique_id": "bmw_i3s_autonomia",
        "name": "BMW i3S - Autonomia Elétrica",
        "state_topic": f"{BASE}/vehicle.drivetrain.electricEngine.kombiRemainingElectricRange",
        "value_template": "{{ value_json.value }}",
        "unit_of_measurement": "km",
        "device_class": "distance",
        "state_class": "measurement",
        "icon": "mdi:map-marker-distance",
    },
    {
        "unique_id": "bmw_i3s_bateria_max",
        "name": "BMW i3S - Capacidade Bateria",
        "state_topic": f"{BASE}/vehicle.drivetrain.batteryManagement.maxEnergy",
        "value_template": "{{ value_json.value }}",
        "unit_of_measurement": "kWh",
        "state_class": "measurement",
        "icon": "mdi:battery-high",
    },
    {
        "unique_id": "bmw_i3s_energia_carga",
        "name": "BMW i3S - Energia para Carregar",
        "state_topic": f"{BASE}/vehicle.drivetrain.electricEngine.charging.smeEnergyDeltaFullyCharged",
        "value_template": "{{ value_json.value }}",
        "unit_of_measurement": "kWh",
        "device_class": "energy",
        "state_class": "measurement",
        "icon": "mdi:battery-charging",
    },

    # Carregamento
    {
        "unique_id": "bmw_i3s_charging_status",
        "name": "BMW i3S - Estado de Carregamento",
        "state_topic": f"{BASE}/vehicle.drivetrain.electricEngine.charging.status",
        "value_template": "{{ value_json.value }}",
        "icon": "mdi:ev-station",
    },
    {
        "unique_id": "bmw_i3s_charging_method",
        "name": "BMW i3S - Método de Carregamento",
        "state_topic": f"{BASE}/vehicle.drivetrain.electricEngine.charging.method",
        "value_template": "{{ value_json.value }}",
        "icon": "mdi:cable-data",
    },
    {
        "unique_id": "bmw_i3s_charging_ampere",
        "name": "BMW i3S - Corrente de Carga",
        "state_topic": f"{BASE}/vehicle.drivetrain.electricEngine.charging.acAmpere",
        "value_template": "{{ value_json.value }}",
        "unit_of_measurement": "A",
        "device_class": "current",
        "state_class": "measurement",
        "icon": "mdi:current-ac",
    },
    {
        "unique_id": "bmw_i3s_charging_voltage",
        "name": "BMW i3S - Tensão de Carga",
        "state_topic": f"{BASE}/vehicle.drivetrain.electricEngine.charging.acVoltage",
        "value_template": "{{ value_json.value }}",
        "unit_of_measurement": "V",
        "device_class": "voltage",
        "state_class": "measurement",
        "icon": "mdi:lightning-bolt",
    },

    # Localização
    {
        "unique_id": "bmw_i3s_latitude",
        "name": "BMW i3S - Latitude",
        "state_topic": f"{BASE}/vehicle.cabin.infotainment.navigation.currentLocation.latitude",
        "value_template": "{{ value_json.value }}",
        "icon": "mdi:crosshairs-gps",
    },
    {
        "unique_id": "bmw_i3s_longitude",
        "name": "BMW i3S - Longitude",
        "state_topic": f"{BASE}/vehicle.cabin.infotainment.navigation.currentLocation.longitude",
        "value_template": "{{ value_json.value }}",
        "icon": "mdi:crosshairs-gps",
    },
    {
        "unique_id": "bmw_i3s_altitude",
        "name": "BMW i3S - Altitude",
        "state_topic": f"{BASE}/vehicle.cabin.infotainment.navigation.currentLocation.altitude",
        "value_template": "{{ value_json.value }}",
        "unit_of_measurement": "m",
        "state_class": "measurement",
        "icon": "mdi:altimeter",
    },
    {
        "unique_id": "bmw_i3s_heading",
        "name": "BMW i3S - Orientação",
        "state_topic": f"{BASE}/vehicle.cabin.infotainment.navigation.currentLocation.heading",
        "value_template": "{{ value_json.value }}",
        "unit_of_measurement": "°",
        "state_class": "measurement",
        "icon": "mdi:compass",
    },

    # Estado
    {
        "unique_id": "bmw_i3s_quilometragem",
        "name": "BMW i3S - Quilometragem",
        "state_topic": f"{BASE}/vehicle.vehicle.travelledDistance",
        "value_template": "{{ value_json.value }}",
        "unit_of_measurement": "km",
        "device_class": "distance",
        "state_class": "total_increasing",
        "icon": "mdi:counter",
    },
]

# ── Binary sensors (true/false) ───────────────────────────────────────────────
BINARY_SENSORS = [
    {
        "unique_id": "bmw_i3s_ficha",
        "name": "BMW i3S - Ficha de Carga",
        "state_topic": f"{BASE}/vehicle.body.chargingPort.status",
        "value_template": "{{ value_json.value }}",
        "payload_on": "CONNECTED",
        "payload_off": "DISCONNECTED",
        "device_class": "plug",
        "icon": "mdi:ev-plug-type2",
    },
    {
        "unique_id": "bmw_i3s_porta_condutor",
        "name": "BMW i3S - Porta Condutor",
        "state_topic": f"{BASE}/vehicle.cabin.door.row1.driver.isOpen",
        "value_template": "{{ value_json.value }}",
        "payload_on": True,
        "payload_off": False,
        "device_class": "door",
    },
    {
        "unique_id": "bmw_i3s_porta_passageiro",
        "name": "BMW i3S - Porta Passageiro",
        "state_topic": f"{BASE}/vehicle.cabin.door.row1.passenger.isOpen",
        "value_template": "{{ value_json.value }}",
        "payload_on": True,
        "payload_off": False,
        "device_class": "door",
    },
    {
        "unique_id": "bmw_i3s_porta_tras_condutor",
        "name": "BMW i3S - Porta Traseira Condutor",
        "state_topic": f"{BASE}/vehicle.cabin.door.row2.driver.isOpen",
        "value_template": "{{ value_json.value }}",
        "payload_on": True,
        "payload_off": False,
        "device_class": "door",
    },
    {
        "unique_id": "bmw_i3s_porta_tras_passageiro",
        "name": "BMW i3S - Porta Traseira Passageiro",
        "state_topic": f"{BASE}/vehicle.cabin.door.row2.passenger.isOpen",
        "value_template": "{{ value_json.value }}",
        "payload_on": True,
        "payload_off": False,
        "device_class": "door",
    },
    {
        "unique_id": "bmw_i3s_mala",
        "name": "BMW i3S - Mala",
        "state_topic": f"{BASE}/vehicle.body.trunk.door.isOpen",
        "value_template": "{{ value_json.value }}",
        "payload_on": True,
        "payload_off": False,
        "device_class": "door",
        "icon": "mdi:car-back",
    },
    {
        "unique_id": "bmw_i3s_capo",
        "name": "BMW i3S - Capô",
        "state_topic": f"{BASE}/vehicle.body.hood.isOpen",
        "value_template": "{{ value_json.value }}",
        "payload_on": True,
        "payload_off": False,
        "device_class": "door",
    },
]

# ── Publicar ──────────────────────────────────────────────────────────────────
def pub(topic, payload):
    cmd = [
        "mosquitto_pub",
        "-h", MQTT_HOST,
        "-p", MQTT_PORT,
        "-u", MQTT_USER,
        "-P", MQTT_PASS,
        "-r",
        "-t", topic,
        "-m", json.dumps(payload, ensure_ascii=False)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  ✅  {payload['name']}")
    else:
        print(f"  ❌  {payload['name']} → {result.stderr.strip()}")

print(f"\n📡 BMW i3S Discovery — VIN: {VIN}\n")

print("── Sensores ──────────────────────────────────────")
for s in SENSORS:
    s["device"] = DEVICE
    pub(f"homeassistant/sensor/{s['unique_id']}/config", s)

print("\n── Binary Sensors ────────────────────────────────")
for s in BINARY_SENSORS:
    s["device"] = DEVICE
    pub(f"homeassistant/binary_sensor/{s['unique_id']}/config", s)

print(f"\n🎉 Concluído! Verifica no HA → Definições → Dispositivos e Serviços → MQTT\n")
