"""Test component setup."""
import pathlib
from custom_components.bosch_homecom.const import (
    DOMAIN,
    MANUFACTURER,
    MODEL,
    CONF_DEVICES,
)
from unittest.mock import Mock, AsyncMock, patch
from homeassistant.helpers import device_registry as dr
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homecom_alt import BHCDeviceRac, BHCDeviceK40
from homeassistant.setup import async_setup_component
from collections.abc import Awaitable, Callable
from pytest_homeassistant_custom_component.common import MockConfigEntry
import pytest
import json
from custom_components.bosch_homecom import PLATFORMS
from pathlib import Path

@pytest.fixture
def bhc():
    """Fixture for HomeComAlt instance."""
    return Mock()

@pytest.fixture
def entry():
    return MockConfigEntry(
        domain=DOMAIN,
        title="test",
        unique_id="test",
        data={
            CONF_USERNAME: "test-user",
            CONF_PASSWORD: "test-pass",
            CONF_DEVICES: {},
        },
    )

@pytest.fixture()
def devices():
    return [{"deviceId":"123","deviceType":"rac"}]

@pytest.fixture()
def devices_k30():
    return [{"deviceId":"123","deviceType":"k30"}]

@pytest.fixture()
def sensor_data():
    """Fixture to load test data from JSON file."""
    file_path = Path(__file__).parent / "fixtures" / "bosch_homecom.json"
    with file_path.open() as f:
        data = json.load(f)
    return data


@pytest.mark.asyncio
async def test_entry_setup_unload(hass, entry, devices, sensor_data):
    """Test config entry setup and unload."""
    entry.data[CONF_DEVICES][
        f"{devices[0]['deviceId']}_{devices[0]['deviceType']}"
    ] = True
    entry.add_to_hass(hass)

    mock_api = AsyncMock()
    mock_api.async_get_devices.return_value = AsyncMock(
        return_value=AsyncMock(return_value=devices)
    )()
    mock_api.async_get_firmware.return_value = {"value": "1.0.0"}
    mock_api.async_update.return_value = BHCDeviceRac(
        device=devices[0]["deviceId"],
        firmware=sensor_data["firmwares"],
        notifications=sensor_data["notifications"],
        stardard_functions=sensor_data["stardard_functions"],
        advanced_functions=sensor_data["advanced_functions"],
        switch_programs=sensor_data["switch_programs"],
        )

    with patch(
        "custom_components.bosch_homecom.config_flow.async_check_credentials",
        return_value=None,
    ), patch(
        "custom_components.bosch_homecom.HomeComAlt.create",
        return_value=mock_api,
    ), patch.object(
        hass.config_entries, "async_forward_entry_setup", return_value=True
    ) as setup:
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    dev_reg = dr.async_get(hass)
    dev_entries = dr.async_entries_for_config_entry(dev_reg, entry.entry_id)

    assert dev_entries
    dev_entry = dev_entries[0]
    assert dev_entry.identifiers == {
        (DOMAIN, devices[0]["deviceId"])
    }
    assert dev_entry.manufacturer == MANUFACTURER
    assert dev_entry.name == "Boschcom_rac_123"
    assert dev_entry.model == "Residential Air Conditioning"

    with patch.object(
        hass.config_entries, "async_forward_entry_unload", return_value=True
    ) as unload:
        assert await hass.config_entries.async_unload(entry.entry_id)
        await hass.async_block_till_done()
        assert unload.call_count == len(PLATFORMS)


@pytest.mark.asyncio
async def test_entry_setup_unload_k30(hass, entry, devices_k30, sensor_data):
    """Test config entry setup for k30 device."""
    entry.data[CONF_DEVICES][
        f"{devices_k30[0]['deviceId']}_{devices_k30[0]['deviceType']}"
    ] = True
    entry.add_to_hass(hass)

    mock_api = AsyncMock()
    mock_api.async_get_devices.return_value = AsyncMock(
        return_value=AsyncMock(return_value=devices_k30)
    )()
    mock_api.async_get_firmware.return_value = {"value": "1.0.0"}
    mock_api.async_update.return_value = BHCDeviceK40(
        device=devices_k30[0]["deviceId"],
        firmware=sensor_data["firmwares"],
        notifications=sensor_data["notifications"],
        holiday_mode=None,
        away_mode=None,
        consumption=None,
        power_limitation=None,
        hs_pump_type=None,
        dhw_circuits=[],
        heating_circuits=[],
    )

    with patch(
        "custom_components.bosch_homecom.config_flow.async_check_credentials",
        return_value=None,
    ), patch(
        "custom_components.bosch_homecom.HomeComAlt.create",
        return_value=mock_api,
    ), patch.object(
        hass.config_entries, "async_forward_entry_setup", return_value=True
    ) as setup:
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    dev_reg = dr.async_get(hass)
    dev_entries = dr.async_entries_for_config_entry(dev_reg, entry.entry_id)

    assert dev_entries
    dev_entry = dev_entries[0]
    assert dev_entry.identifiers == {
        (DOMAIN, devices_k30[0]["deviceId"])
    }
    assert dev_entry.manufacturer == MANUFACTURER
    assert dev_entry.name == "Boschcom_k30_123"
    assert dev_entry.model == "Bosch boiler k30"

    with patch.object(
        hass.config_entries, "async_forward_entry_unload", return_value=True
    ) as unload:
        assert await hass.config_entries.async_unload(entry.entry_id)
        await hass.async_block_till_done()
        assert unload.call_count == len(PLATFORMS)

async def test_async_setup(hass):
    """Test the component gets setup."""
    assert await async_setup_component(hass, DOMAIN, {}) is True
