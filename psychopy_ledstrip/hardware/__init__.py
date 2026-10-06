"""Marks the package containing the Psychopy Ledstrip plugin hardware objects."""

from fastrakSerialDriver.fastrakPosition import FastrakPostion
from psychopy import logging
from psychopy.hardware.base import BaseDevice
from serial.tools import list_ports
from slasd.commands.support import LedColor
from slasd.fastrakAnimator import FastrakAnimationDevice


class LedstripHardwareDevice(BaseDevice):
    """Psychopy hardware object for a Ledstrip.

    Attributes
    ----------
    _ftd : LedstripDevice
        Ledstrip serial driver object.

    _name : str
        The name of hardware object.

    _is_locked : bool
        Indicates if the object is locked. A hardware object can only be accessed by one experiment
        object at a time.

        - Locked when `True`
        - Unlocked when `False`

    _is_setup : bool
        The setup routine only needs to be called once per hardware device. This flag indicates when
        the setup has already been run.
    """

    _name: str
    _is_locked: bool
    _is_setup: bool
    _ledStrip: FastrakAnimationDevice
    _port: str
    _angleToLight: int
    _ledCount: int
    _ledCenterIdx: int
    _color: LedColor

    def __init__(self, *args, **kwargs):
        """Initialize a Psychopy hardware object for a Ledstrip."""
        super().__init__()

        port = kwargs.get('port')
        if not isinstance(port, str):
            raise Exception(
                'Port input for Fastrak is not a string.'
            )  # TODO: Add specific Exception
        self._port = port

        baudrate = kwargs.get('baudrate')
        if not isinstance(baudrate, int):
            raise Exception(
                'Baudrate for Fastrak is not valid.'
            )  # TODO: Add specific Exception
        self._baud = baudrate

        ledCount = kwargs.get('ledCount')
        if not isinstance(ledCount, int):
            raise Exception(
                'Baudrate for Fastrak is not valid.'
            )  # TODO: Add specific Exception
        self._ledCount = ledCount

        ledCenter = kwargs.get('ledCenter')
        if not isinstance(ledCenter, int):
            raise Exception(
                'Baudrate for Fastrak is not valid.'
            )  # TODO: Add specific Exception
        self._ledCenterIdx = ledCenter

        angle2light = kwargs.get('angle2light')
        if not isinstance(angle2light, int):
            raise Exception(
                'Baudrate for Fastrak is not valid.'
            )  # TODO: Add specific Exception
        self._angleToLight = angle2light

        colorR = kwargs.get('colorR')
        if not isinstance(colorR, int):
            raise Exception(
                'Baudrate for Fastrak is not valid.'
            )  # TODO: Add specific Exception

        colorG = kwargs.get('colorG')
        if not isinstance(colorG, int):
            raise Exception(
                'Baudrate for Fastrak is not valid.'
            )  # TODO: Add specific Exception

        colorB = kwargs.get('colorB')
        if not isinstance(colorB, int):
            raise Exception(
                'Baudrate for Fastrak is not valid.'
            )  # TODO: Add specific Exception
        self._color = LedColor(red=colorR, green=colorG, blue=colorB)

        # Create a driver instance for the device.
        self._name = f'Ledstrip-{port}_{baudrate}KHz'
        self._is_setup = False
        self._is_locked = False
        ledStrip = FastrakAnimationDevice.create_valid_device(
            COMport=port,
            baud=baudrate,
            timeout=1,
            ledCount=self._ledCount,
            setup=False,
            color=self._color,
        )
        if ledStrip is not None:
            self._ledStrip = ledStrip
        else:
            raise Exception(
                'Unable to create a Fastrak driver instance.'
            )  # TODO: Add specific Exception object

    def isSameDevice(self, other: 'LedstripHardwareDevice') -> bool:
        """Determine whether this object represents the same physical device as a given `other` object.

        > [!note]
        > This is a `BaseResponseDevice` interface.

        Parameters
        ----------
        other : LedstripHardwareDevice
            Other device object to compare against.

        Returns
        -------
        bool
            True if the two objects represent the same physical device
        """
        return (
            isinstance(other, LedstripHardwareDevice)
            and other._ledStrip == self._ledStrip
        )

    @staticmethod
    def getAvailableDevices() -> list[dict]:
        """Get all available Ledstrip Hardware Devices.

        > [!note]
        > This is a `BaseResponseDevice` interface.

        -------
        list[dict]
            List of dictionaries containing the parameters needed to initialize each device.
        """
        ports = list_ports.comports()
        ledstripDevices = []
        for device in ports:
            ledstrip = {
                'deviceName': f'Ledstrip@{device.device}',
                'deviceClass': 'psychopy_ledstrip.hardware.LedstripHardwareDevice',
                'port': device.device,
            }
            ledstripDevices.append(ledstrip)
        return ledstripDevices

    @property
    def name(self) -> str:
        """Name attribute of the object.

        Returns
        -------
        str
            The name attribute of the object.


        """
        return self._name

    def setLedState(self, pos: FastrakPostion) -> None:

        self._ledStrip.compNSndState(
            posData=pos, angleToLight=self._angleToLight, zeroLED=self._ledCenterIdx
        )

    def lock(self) -> bool:
        """Acquire the Fastrak device lock.

        Returns
        -------
        bool
            Returns True when lock is acquired, False otherwise.
        """
        if self._is_locked:
            return False
        self._is_locked = True
        return True

    def unlock(self) -> bool:
        """Release the Fastrak device lock.

        Returns
        -------
        bool
            Returns True when lock is released, False otherwise.
        """
        if self._is_locked:
            self._is_locked = False
            return True
        return False

    def startup(self):
        """Set up the Fastrak device for streaming."""
        if not self._is_setup:
            self._ledStrip.connect()
        self._ledStrip.setOff()
        self._is_setup = True
