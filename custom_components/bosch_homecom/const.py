"""Constants."""

from __future__ import annotations

from datetime import timedelta
from typing import Final

DOMAIN = "bosch_homecom"
DEFAULT_UPDATE_INTERVAL: Final = timedelta(minutes=4)
MANUFACTURER: Final = "Bosch"

MODEL = {
    "rac": "Residential Air Conditioning",
    "k40": "Bosch boiler",
    "k30": "Bosch boiler k30",
}

ATTR_NOTIFICATIONS = "notifications"
ATTR_FIRMWARE = "fw"
ATTR_MODE = "operationMode"
ATTR_SPEED = "fanSpeed"
ATTR_HORIZONTAL = "airFlowHorizontal"
ATTR_VERTICAL = "airFlowVertical"
ATTR_TEMP = "temperatureSetpoint"
ATTR_ROOM_TEMP = "roomTemperature"
ATTR_AIR_PURIFICATION = "airPurificationMode"
ATTR_FULL_POWER = "fullPowerMode"
ATTR_ECO_MODE = "ecoMode"
ATTR_TIMERS_ON = "timersOn"
ATTR_TIMERS_OFF = "timersOff"

CONF_DEVICES = "devices"
