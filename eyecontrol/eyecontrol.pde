 /**
 Basic demonstration of using a gamepad.
 
 When this sketch runs it will try and find
 a game device that matches the configuration
 file 'gamepad' if it can't match this device
 then it will present you with a list of devices
 you might try and use.
 
 The chosen device requires 3 sliders and 2 button.
 
 for Processing V3
 (c) 2020 Peter Lager
 */

import org.gamecontrolplus.gui.*;
import org.gamecontrolplus.*;
import net.java.games.input.*;

ControlIO control;
Configuration config;
ControlDevice gpad;


import processing.sound.*;

SoundFile track;
SoundFile sample;

int screenWidth = 192;
int screenHeight = 80;
int eyeSize = 3*screenHeight/4;
int upperValue = eyeSize/2;

PImage eyeImg;

float pupilPosX, pupilPosY, pupilSize;
boolean blink;


public void setup() {
  //size(400, 240);
  background(0);
  fullScreen();
  background(0);
eyeImg = loadImage("eye.png");
  surface.setTitle("LUMI eye control");
  // Initialise the ControlIO
  control = ControlIO.getInstance(this);
  // Find a gamepad that matches the configuration file. To match with any 
  // connected device remove the call to filter.
  gpad = control.filter(GCP.GAMEPAD).getMatchedDevice("gamepad_eyes");
  if (gpad == null) {
    println("No suitable device configured");
    System.exit(-1); // End the program NOW!
  }
  track = new SoundFile(this, "track.mp3");
  sample = new SoundFile(this, "samples.mp3");
}
boolean playing;
public void getUserInput() {
  // Either button will dilate pupils
 // boolean dilated = gpad.getButton("PUPILSIZE1").pressed() || gpad.getButton("PUPILSIZE2").pressed();
  //pupilSize = dilated ? irisSize * 0.6f : irisSize * 0.45f; 
  pupilPosX =   map(gpad.getSlider("XPOS").getValue(), -1, 1, 0,screenWidth/2);
  pupilPosY =   map(gpad.getSlider("YPOS").getValue(), -1, 1, 0,screenHeight);
  blink = gpad.getButton("EYELID").pressed();
  if(!track.isPlaying() && gpad.getButton("START").pressed()){println("play");playing = true; track.play();}
  else if (track.isPlaying() && gpad.getButton("STOP").pressed()){println("stop");playing = false; track.stop();}

  if(!sample.isPlaying() && gpad.getButton("SAMPLE").pressed()){println("sample");sample.play();}
  
}
float eyeX, prevEyeX, eyeY, prevEyeY;
public void draw() {
  getUserInput(); // Poll the input device 
  background(127);
  fill(255);
  rect(0, 0, screenWidth, screenHeight);
  eyeX = pupilPosX * 0.10 + prevEyeX * 0.90;
  eyeY = pupilPosY * 0.10 + prevEyeY * 0.90;
  
  prevEyeX = eyeX;
  prevEyeY = eyeY;
  
 drawEyes((int)eyeX,(int)eyeY,blink);

    noCursor();
}


public void drawEyes(int x, int y, boolean blink) {
  int lidMid = screenHeight/2;
  int dLid = 0;
  if (y>screenHeight) y = screenHeight;
  if (y<0) y = 0;
  if (x<eyeSize/2) x = eyeSize/2;
  if (x>(screenWidth/2-eyeSize/2)) x = (screenWidth/2-eyeSize/2);
  fill(0, 255, 100, 200);
  stroke(0);
  image(eyeImg, x-144, y-121);
  image(eyeImg, x+screenWidth/2-144, y-121);
  //ellipse(x, y, eyeSize, eyeSize);
  //ellipse(x+screenWidth/2, y, eyeSize, eyeSize);
  fill(0);
  //ellipse(x, y, eyeSize/4, eyeSize/4);
  //ellipse(x+screenWidth/2, y, eyeSize/4, eyeSize/4);
  if (blink == true) dLid = -eyeSize/10;
  else dLid = eyeSize/10;
  upperValue += dLid;
  if (upperValue>eyeSize/2) upperValue = eyeSize/2;
  if (upperValue<0) upperValue = 0;

  // and now for 4 different eyelids...
  beginShape();
  vertex(0, 0);
  vertex(screenWidth/2, 0);
  vertex(screenWidth/2, lidMid);
  bezierVertex(x+eyeSize/4, y-upperValue, x-eyeSize/4, y-upperValue, 0, lidMid);
  endShape();

  beginShape();
  vertex(0, screenHeight);
  vertex(screenWidth/2, screenHeight);
  vertex(screenWidth/2, lidMid);
  bezierVertex(x+eyeSize/4, y+upperValue, x-eyeSize/4, y+upperValue, 0, lidMid);
  endShape();

  beginShape();
  vertex(screenWidth/2, 0);
  vertex(screenWidth, 0);
  vertex(screenWidth, lidMid);
  bezierVertex(x+screenWidth/2+eyeSize/4, y-upperValue, x+screenWidth/2-eyeSize/4, y-upperValue, screenWidth/2, lidMid);
  endShape();

  beginShape();
  vertex(screenWidth/2, screenHeight);
  vertex(screenWidth, screenHeight);
  vertex(screenWidth, lidMid);
  bezierVertex(x+screenWidth/2+eyeSize/4, y+upperValue, x+screenWidth/2-eyeSize/4, y+upperValue, screenWidth/2, lidMid);
  endShape();
  noStroke();
  // clean up the bottom bit
  fill(127);
  rect(0,screenHeight,screenWidth,2*screenHeight);
   
}
