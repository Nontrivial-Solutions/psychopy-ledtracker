"""Marks the package containing the Psychopy Ledstrip plugin hardware wrapper."""

from asyncio import Lock
from enum import Enum
from lib2to3.pytree import Base
from pathlib import Path

from fastrakSerialDriver.fastrakPosition import FastrakPostion
from psychopy import constants, logging
from psychopy.experiment import Experiment
from psychopy.hardware import DeviceManager
from psychopy.hardware.listener import BaseListener
from psychopy_fastrak.hardware import FastrakHardwareDevice

from ..hardware import LedstripHardwareDevice


class LockStatus(Enum):
    IS_LOCKED = 0
    NOT_LOCKED = 1


class LedFastrakListner(BaseListener):
    _lastPos: FastrakPostion | None

    def __init__(self):
        BaseListener.__init__(self)
        self._lastPos = None

    @property
    def position(self) -> FastrakPostion | None:
        """Get the current/last position reported by the configured fastrak device.

        Returns
        -------
        FastrakPostion | None
                When present the last known position of the Fastrak device. Otherwise, `None`.

        """
        return self._lastPos

    def receiveMessage(self, message):
        """
        Method defining what to do when receiving a message. Must be implemented by subclasses.

        Parameters
        ----------
        message
            Message received.
        """
        self._lastPos = message.value


class LedstripWrapper:
    """Wraps a Psychopy Ledstrip hardware device for use in a Psychopy component.

    Attributes
    ----------
    _device : LedstripHardwareDevice
        The Ledstrip device to wrap.
    _outputPath : Path
        The path (relative to the data directory) to store a data file.
        >[!note]
        > Also serves as an "ID" when logging.
    _status : int
        The Base device status. The values are derived from consts in a [SimpleNamespace which is essentially a
        Dict](https://docs.python.org/3/library/types.html#types.SimpleNamespace).
        > [!warning]
        > This is **NOT** an [Enum](https://docs.python.org/3/library/enum.html).
    _hasDeviceLock : bool
        Indicates if this instance of the wrapper believes it holds the lock on its hardware device.
    _counter : int
        The number of times this wrapper has run. 1 indexed.
    """

    _ledDevice: LedstripHardwareDevice
    _fastrakDevice: FastrakHardwareDevice
    _listener: LedFastrakListner
    _status: int
    _deviceLockStatus: LockStatus
    _counter: int

    def __init__(self, ledDevice: str, fastrakDevice: str) -> None:
        """Initialize the wrapper object.

        Parameters
        ----------
        device : str
            The name of the hardware device to wrap.

        """
        if not isinstance(ledDevice, str) or ledDevice not in DeviceManager.devices:
            raise ValueError(
                f"Could not find device named '{ledDevice}', make sure it has been set up in DeviceManager."
            )  # TODO: Add specific exception object

        self._ledDevice = DeviceManager.getDevice(ledDevice)
        self._fastrakDevice = DeviceManager.getDevice(fastrakDevice)
        self._listener = LedFastrakListner()
        self._fastrakDevice.addListener(self._listener)
        self._status = constants.NOT_STARTED
        self._deviceLockStatus = LockStatus.NOT_LOCKED

    @property
    def status(self) -> int:
        """Wrapper Status attribute.

        Returns
        -------
        int
            Indicates the status of the wrapper.
            > [!warning]
            > This is **NOT** an [Enum](https://docs.python.org/3/library/enum.html).

        """
        return self._status

    @status.setter
    def status(self, status: int) -> None:
        """Set the wrapper Status attribute."""
        self._status = status

    @property
    def hasLock(self) -> bool:
        """Wrapper Status attribute.

        Returns
        -------
        int
            Indicates the status of the wrapper.
            > [!warning]
            > This is **NOT** an [Enum](https://docs.python.org/3/library/enum.html).

        """
        if self._deviceLockStatus == LockStatus.IS_LOCKED:
            return True
        return False

    def reset(self) -> None:
        """Reset this object to a state it can collect another stream sample.

        Between repeated trials and routines within an experiment objects are reused. There's no
        good way to handle the behavior as it stands instead we initialize the least number of
        objects and explicitly reset their state when needed.

        Parameters
        ----------
        outputDir : None | str
            The path (relative to the data directory) to store a data file. Alternatively, `None` in
            the case the directory should remain unchanged.
        """
        # If we have the lock that's a problem. Locks need to be released before reset.
        if self._deviceLockStatus != LockStatus.IS_LOCKED:
            raise ValueError(
                f"'{self._ledDevice.name}' does not have the stream lock and can't be reset."
            )  # TODO: Add specific exception object

        # Try to unlock the fastrak
        if not self._ledDevice.unlock():
            raise ValueError(
                f"'{self._ledDevice.name}' is still locked."
            )  # TODO: Add specific exception object

        self._deviceLockStatus = LockStatus.NOT_LOCKED

    def startup(self) -> None:
        """Assert the state of the wrapped device and obtain lock."""
        logging.info(f'Startup the fastrak')

        # If we have the lock that's a problem. We must already be running.
        if self._deviceLockStatus == LockStatus.IS_LOCKED:
            raise ValueError(
                f"'{self._ledDevice.name}' already has the stream lock."
            )  # TODO: Add specific exception object

        # If we can't lock the Fastrak that's a problem. Someone else must be using the Fastrak.
        if not self._ledDevice.lock():
            raise ValueError(
                f"'{self._ledDevice.name}' is locked."
            )  # TODO: Add specific exception object

        self._deviceLockStatus = LockStatus.IS_LOCKED
        self._ledDevice.startup()

    def step(self) -> None:
        """Assert the state of the wrapped device and obtain lock."""
        logging.info(f'Startup the fastrak')

        # If we have the lock that's a problem. We must already be running.
        if self._deviceLockStatus != LockStatus.IS_LOCKED:
            raise ValueError(
                f"'{self._ledDevice.name}' already has the stream lock."
            )  # TODO: Add specific exception object

        if self._listener.position is not None:
            self._ledDevice.setLedState(pos=self._listener.position)
