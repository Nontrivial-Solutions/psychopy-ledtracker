"""PsychoPy component for calling a Ledstrip in a routine."""

from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape
from psychopy.experiment import Experiment
from psychopy.experiment.components import BaseDeviceComponent, getInitVals
from psychopy.experiment.devices import DeviceBackend
from psychopy.experiment.exports import IndentingBuffer
from psychopy.experiment.params import Param
from psychopy_fastrak.components.fastrakComponent import FastrakDeviceBackend


class LedstripComponent(BaseDeviceComponent):
    """PsychoPy component for collecting streaming data from a Polhemus Ledstrip."""

    plugin = 'psychopy-ledstrip'
    targets = ['PsychoPy']
    categories = ['Stimuli']
    iconFile = Path(__file__).parent / 'icon.png'
    iconSVG = Path(__file__).parent / 'icon.svg'
    tooltip = 'Component for collecting streaming data from a Polhemus Ledstrip.'
    version = '2026.1.3'
    beta = False

    def __init__(
        self,
        exp: Experiment,
        parentName: str,
        name: str = 'ledstrip',
        startType: str = 'time (s)',
        startVal: float = 0.0,
        stopType: str = 'duration (s)',
        stopVal: float | str = '',
        deviceLabel: str = '',
        deviceLabelFT: str = '',
    ):
        """Initialize a new component object for generating Ledstrip experiment/routine code.

        > [!warning]
        > I'm guessing at the type hinting here. There's no documentation from PsychoPy for what
        > the typing is.

        Parameters
        ----------
        exp : Experiment
            The experiment this object is associated with.

        parentName : str
            The name of the parent?

            > [!warning]
            > What this is doing is unclear. It seems to be how the routine that owns this object
            > interacts with the object.

        name : str
            The name of this object.

            > [!warning]
            > This is linked to the actual variable name for the object.

        startType : str
            Indicates the type of start condition for the component.

        startVal : float
            The start "value" for the component.

            > [!warning]
            > In the `BaseComponent` this is type `code`. I don't know what that means beyond the.
            > docstring from the Param class
            > > - code: Some code, will be compiled verbatim or translated to JS (no ")

        stopType : str
            Indicates the type of stop condition for the component.

        stopVal : float
            The stop "value" for the component.

            > [!warning]
            > In the `BaseComponent` this is type `code`. I don't know what that means beyond the.
            > docstring from the Param class
            > > - code: Some code, will be compiled verbatim or translated to JS (no ")

        deviceLabel : str
            A label for the device.

            > [!warning]
            > In the `BaseComponent` this is type `device`. I don't know what that means beyond the.
            > docstring from the Param class which says it's a `str`.
        """
        BaseDeviceComponent.__init__(
            self,
            exp,
            parentName,
            name=name,
            startType=startType,
            startVal=startVal,
            stopType=stopType,
            stopVal=stopVal,
            deviceLabel=deviceLabel,
        )

        self.order += []
        self.type = 'Ledstrip'
        self.url = 'https://psychopy-ledstrip.nontrivialsolutions.org'

        # require hardware
        self.exp.requirePsychopyLibs(['hardware'])

        # --- Device params ---
        self.order += ['deviceLabel']
        # label to refer to device by
        self.params['deviceLabelFT'] = Param(
            deviceLabelFT,
            valType='device',
            inputType='device',
            categ='Device',
            allowedVals=list(self.backends),
            label='Fastrak Device',
            hint='The named device from Device Manager to use for this Component.',
        )

        self._env = Environment(
            loader=PackageLoader('psychopy_ledstrip.components.ledstripComponent'),
            autoescape=select_autoescape(),
        )

        self.exp.requireImport(
            importName='LedstripWrapper',
            importFrom='psychopy_ledstrip.wrapper',
        )

    def _writeJinjaCode(self, buff: IndentingBuffer, params: dict, tmpltSource: str):
        """Write to the experiment python file the Jinja template.

        > [!note]
        > Many of the other components (plugin or otherwise) use old style python string
        > replacements. We use Jinja for easier configuration management.

        Parameters
        ----------
        buff : IndentingBuffer
            The output experiment python file buffer.

        params : dict
            A dictionary with replacement variables.

        tmpltSource : str
            The path to the jinja template to insert.
        """
        template = self._env.get_template(tmpltSource)
        code = template.render(params)
        buff.writeIndentedLines(code)

    def _blockComment(self, buff: IndentingBuffer, content: str) -> None:
        """Insert a block comment into the experiment python file.

        > [!note]
        > This only supports single line comments at the moment. A jinja for loop over the lines of
        > content would support multiline block comments.

        Parameters
        ----------
        buff : IndentingBuffer
            The output experiment python file buffer.

        content : str
            The content of the block comment.

        """
        self._writeJinjaCode(buff, {'content': content}, 'blockComment.jinja')

    def writeStartCode(self, buff):
        """Write code that a component needs at the start of an experiment.

        Reference the [experiment life cycle](/content/notes/explifecycle).

        Parameters
        ----------
        buff : IndentingBuffer
            The output experiment python file buffer.
        """
        inits = getInitVals(self.params)
        self._writeJinjaCode(buff, inits, 'start.jinja')

    def writeInitCode(self, buff: IndentingBuffer):
        """Write code that a component needs at the init of an experiment.

        Reference the [experiment life cycle](/content/notes/explifecycle).

        Parameters
        ----------
        buff : IndentingBuffer
            The output experiment python file buffer.
        """
        inits = getInitVals(self.params)
        self._writeJinjaCode(buff, inits, 'init.jinja')

    def writeRoutineStartCode(self, buff: IndentingBuffer):
        """Write code that a component needs at the start of a routine.

        Reference the [experiment life cycle](/content/notes/explifecycle).

        Parameters
        ----------
        buff : IndentingBuffer
            The output experiment python file buffer.
        """
        self.writeParamUpdates(buff, updateType='set every repeat')
        self._writeJinjaCode(buff, self.params.copy(), 'routineStart.jinja')

    def writeFrameCode(self, buff: IndentingBuffer):
        """Write code that a component needs during a frame of a routine.

        Reference the [experiment life cycle](/content/notes/explifecycle).

        Parameters
        ----------
        buff : IndentingBuffer
            The output experiment python file buffer.
        """
        # update any parameters which need updating
        self.writeParamUpdates(buff, updateType='set every frame')

        self._blockComment(buff, f'{self.params["name"]} start frame')
        indent = self.writeStartTestCode(buff)
        if indent:
            self._writeJinjaCode(buff, self.params.copy(), 'firstFrame.jinja')
            buff.setIndentLevel(-indent, relative=True)

        self._blockComment(buff, f'{self.params["name"]} active frame')
        indent = self.writeActiveTestCode(buff)
        if indent:
            self._writeJinjaCode(buff, self.params.copy(), 'activeFrame.jinja')
            buff.setIndentLevel(-indent, relative=True)

        self._blockComment(buff, f'{self.params["name"]} stop frame')
        indent = self.writeStopTestCode(buff)
        if indent:
            self._writeJinjaCode(buff, self.params.copy(), 'finalFrame.jinja')
            buff.setIndentLevel(-indent, relative=True)

        self._blockComment(buff, f'End {self.params["name"]} frame updates')

    def writeRoutineEndCode(self, buff: IndentingBuffer):
        """Write code that a component needs at the end of a routine.

        Reference the [experiment life cycle](/content/notes/explifecycle).

        Parameters
        ----------
        buff : IndentingBuffer
            The output experiment python file buffer.
        """
        # create a copy of params so that we can safely edit stuff
        self._writeJinjaCode(buff, self.params.copy(), 'routineEnd.jinja')


class LedstripDeviceBackend(DeviceBackend):
    """In the GUI configurator this represents an available 'backend' for an object.

    Attributes
    ----------
    backendLabel : str
        The label for the backend that will appear in the configurator.
    component : object
        The associated component for the backend.
    deviceClass : str
        The hardware device this backend represents.
    icon : str
        The icon to appear in the configurator.
    """

    backendLabel: str = 'Ledstrip'
    component: object = LedstripComponent
    deviceClass: str = 'psychopy_ledstrip.hardware.LedstripHardwareDevice'
    icon: str = 'light/icon.png'

    def __init__(self, profile):
        """Initialize a Ledstrip device backend.

        Parameters
        ----------
        profile : object?
            Not sure what this is or does. It doesn't seem to be documented anywhere but it is
            expected.
        """
        DeviceBackend.__init__(self, profile)
        self.order += [
            'name',
        ]

        self.params['baudrate'] = Param(
            9600,
            valType='code',
            inputType='single',
            label='Number of LED',
            hint="""Keys to treat as buttons (in order of what button index you want them to be). 
                Must be the same length as the number of buttons.""",
        )

        self.params['ledCount'] = Param(
            0,
            valType='code',
            inputType='single',
            label='Number of LED',
            hint="""Keys to treat as buttons (in order of what button index you want them to be). 
                Must be the same length as the number of buttons.""",
        )

        self.params['ledCenter'] = Param(
            0,
            valType='code',
            inputType='single',
            label='LED to treat as zero',
            hint="""Keys to treat as buttons (in order of what button index you want them to be). 
                Must be the same length as the number of buttons.""",
        )

        self.params['angle2light'] = Param(
            10,
            valType='code',
            inputType='single',
            label='Angle of LEDs to light',
            hint="""Keys to treat as buttons (in order of what button index you want them to be). 
                Must be the same length as the number of buttons.""",
        )

        self.params['colorR'] = Param(
            0,
            valType='code',
            inputType='single',
            label='Red Value',
            hint="""Keys to treat as buttons (in order of what button index you want them to be). 
                Must be the same length as the number of buttons.""",
        )

        self.params['colorG'] = Param(
            0,
            valType='code',
            inputType='single',
            label='Green Value',
            hint="""Keys to treat as buttons (in order of what button index you want them to be). 
                Must be the same length as the number of buttons.""",
        )

        self.params['colorB'] = Param(
            0,
            valType='code',
            inputType='single',
            label='Blue Value',
            hint="""Keys to treat as buttons (in order of what button index you want them to be). 
                Must be the same length as the number of buttons.""",
        )

    def writeDeviceCode(self, buff: IndentingBuffer):
        """Write code that the hardware device needs to be registered by PsychoPy during an experiment.

        > [!note]
        > This is a `DeviceBackend` interface.

        Parameters
        ----------
        buff : IndentingBuffer
            The output experiment python file buffer.
        """
        self.writeBaseDeviceCode(buff, close=True)


LedstripComponent.registerBackend(LedstripDeviceBackend)
LedstripComponent.registerBackend(FastrakDeviceBackend)
