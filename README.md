# LUMI
Software and hardware for LUMI

## eyecontrol
In the folder eyecontrol you find the processing.org sketch 'eyecontrol.pde' and necessary data (images and mp3 files) for controlling LUMI eye animation. Currently processing version 4.3 is used (run on a Panasonic CF-19 laptop (Intel I5) running Ubuntu 22.04LTS)

The [gamecontrolplus](http://www.lagers.org.uk/gamecontrol/index.html) library is installed (through the library manager) to allow control by a Logitech gamepad. Wheb the application is first started, a custom mapping has to be made between controller buttons and software inputs. This mapping is stored as plain-txt in the file 'gamepad_eyes':

``` 
Eyes controllernext
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
BACK	button BACK	1	BUTTON	8	0	0.0	0.0
```

The HDMI (vga to HDMI to DVI) video output is taken from the second screen (no screen mirroring) - only the top 192 x 80 pixels are sent to the eyes. The eyes are circular (80 pixels diameter) but each one on a rectangular 96 x 80 matrix. Both eyes together are mapped as 192 x 80 pixel screen, by the LED driver taken from the top-left corner. Therefore, the application should run fullScreen (otherwise GUI artifacts will be shown on Lumi's eyes).

#### todo
Desired functions to add:
- 8 images to be activated by the POV hat switch
- pupil dilation
- for expressiveness: change eyelid shape rather than just colour

