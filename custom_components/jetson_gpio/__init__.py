"""Support for controlling GPIO pins of a Jetson."""

from homeassistant.const import (
    EVENT_HOMEASSISTANT_STARTED,
    EVENT_HOMEASSISTANT_STOP,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from Jetson.GPIO import GPIO as JetsonGPIO  # pylint: disable=import-error

DOMAIN = "jetson_gpio"
PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.COVER,
    Platform.SWITCH,
]


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Jetson GPIO component."""

    def cleanup_gpio(event):
        """Stuff to do before stopping."""
        JetsonGPIO.cleanup()

    def prepare_gpio(event):
        """Stuff to do when Home Assistant starts."""
        hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, cleanup_gpio)

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STARTED, prepare_gpio)
    JetsonGPIO.setmode(JetsonGPIO.BOARD)
    return True


def setup_output(port):
    """Set up a GPIO as output."""
    JetsonGPIO.setup(port, JetsonGPIO.OUT)


def setup_input(port, pull_mode):
    """Set up a GPIO as input."""
    JetsonGPIO.setup(
        port,
        JetsonGPIO.IN,
        JetsonGPIO.PUD_DOWN if pull_mode == "DOWN" else JetsonGPIO.PUD_UP,
    )


def write_output(port, value):
    """Write a value to a GPIO."""
    JetsonGPIO.output(port, value)


def read_input(port):
    """Read a value from a GPIO."""
    return JetsonGPIO.input(port)


def edge_detect(port, event_callback, bounce):
    """Add detection for RISING and FALLING events."""
    JetsonGPIO.add_event_detect(
        port, JetsonGPIO.BOTH, callback=event_callback, bouncetime=bounce
    )
