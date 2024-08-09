# LUMI
Software and hardware for LUMI

## eyecontrol
In the folder eyecontrol you find the processing.org sketch 'eyecontrol.pde' and necessary data (images and mp3 files) for controlling LUMI eye animation

The gamecontrolplus library is installed (through the library manager) to allow control by a Logitech gamepad. Wheb the application is first started, a custom mapping has to be made between controller buttons and software inputs. This mapping is stored as plain-txt in the file 'gamepad_eyes':

'''Eyes controllernext
XPOS	Pupil X 	3	SLIDER	z	0	1.0	0.15
YPOS	Pupil Y 	3	SLIDER	rz	0	1.0	0.15
EYELID	Eye lid 	1	BUTTON	11	0	0.0	0.0
A	button A	1	BUTTON	1	0	0.0	0.0
B	button B	1	BUTTON	2	0	0.0	0.0
X	button X	1	BUTTON	0	0	0.0	0.0
Y	button Y	1	BUTTON	3	0	0.0	0.0
RT	button RT	1	BUTTON	5	0	0.0	0.0
RS	button RS	1	BUTTON	7	0	0.0	0.0
START	button START	1	BUTTON	9	0	0.0	0.0
BACK	button BACK	1	BUTTON	8	0	0.0	0.0'''

#### todo
Desired functions to add:
- 8 images to be activated by the POV hat switch
- pupil dilation
- for expressiveness: change eyelid shape rather than just colour

