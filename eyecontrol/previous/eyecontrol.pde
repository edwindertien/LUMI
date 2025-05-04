/** LUMI eyes control software
 
 Lumi uses two LED matrix eyes of 96 x 80 pixels controlled over HDMI.
 the first 192x80 pixels of a screen are transferred to these Matrices.
 
 Libraries used:
 - GameControlPlus for Processing V3 (c) 2020 Peter Lager
 - Sound (processing standard)
 
 */

import org.gamecontrolplus.gui.*;
import org.gamecontrolplus.*;
import net.java.games.input.*;

ControlIO control;
Configuration config;
ControlDevice gpad;


import processing.sound.*;

//SoundFile track;

//SoundFile sndYes, sndNo, sndAngry, sndStartup, sndShutdown, sndBreakdown, sndAlarm, sndCalculate, sndMove;

int screenWidth = 192;
int screenHeight = 80;
int eyeSize = 5*screenHeight/8;
int upperValue = eyeSize/2;

int imageNumber;
float pupilPosX, pupilPosY, pupilSize;
boolean blink;
boolean dilate;

//The image names in the folder that can be activated with the POV hat
String[] imageNames = {
  "lumi-battery.jpg", 
  "lumi-classified.jpg", 
  "lumi-map.jpg", 
  "lumi-route.jpg",
  "lumi-noconnection.jpg", 
  "lumi-ok.jpg",  
  "lumi-weather.jpg", 
  "lumi-steps.jpg",
  "lumi-warning.jpg"
};
int [] link = { 1, 4, 1, 5,1, 5, 1, 4,0,0};

String[] sampleNames = {
  "lumi-alarm.mp3",
  "lumi-yes.mp3",
  "lumi-yes1.mp3",
  "lumi-yes2.mp3",
  "lumi-no.mp3",
  "lumi-no2.mp3",
  "lumi-startup.mp3",
  "lumi-shutdown.mp3"
};

PImage[] images = new PImage[9];
SoundFile [] samples = new SoundFile[8];

public void setup() {
  //size(400, 240);
  fullScreen(2);
  background(0);

  // Map the image names to integers 1-8
  for (int i = 0; i < imageNames.length; i++) {
    images[i] = loadImage(imageNames[i]);
  }
  
    for (int i = 0; i < sampleNames.length; i++) {
    samples[i] = new SoundFile(this, sampleNames[i]);
  }

  surface.setTitle("LUMI eye control");
  // Initialise the ControlIO
  control = ControlIO.getInstance(this);
  // Find a gamepad that matches the configuration file. To match with any
  // connected device remove the call to filter.
  //gpad = control.getMatchedDevice("gamepad_eyes");
  gpad = control.filter(GCP.GAMEPAD).getMatchedDevice("gamepad_eyes");
  if (gpad == null) {
    println("No suitable device configured");
    System.exit(-1); // End the program NOW!
  }

}
int lastSample = 0;
boolean alarm = false; 
public void getUserInput() {
  dilate = gpad.getButton("DILATE").pressed();
  pupilPosX =   map(gpad.getSlider("XPOS").getValue(), -1, 1, 0, screenWidth/2);
  pupilPosY =   map(gpad.getSlider("YPOS").getValue(), -1, 1, 0, screenHeight);
  blink = gpad.getButton("EYELID").pressed();
  alarm = gpad.getButton("ALARM").pressed();
  imageNumber = gpad.getHat("POV").getPos();
  if (imageNumber == 0) lastSample = 0;
  if (!samples[1].isPlaying() && gpad.getButton("A").pressed()) { samples[1].play();}
  if (!samples[4].isPlaying() && gpad.getButton("X").pressed()) { samples[4].play();}
  if (!samples[5].isPlaying() && gpad.getButton("Y").pressed()) { samples[5].play();}
  if (!samples[2].isPlaying() && gpad.getButton("B").pressed()) { samples[2].play();}
  if (gpad.getButton("START").pressed()&& mode == 0) {
    mode = 1;
    if(!samples[6].isPlaying()) samples[6].play();
  }
  if (gpad.getButton("BACK").pressed()&& mode == 1) {
    if(!samples[7].isPlaying()) samples[7].play();
    mode = 0;
  }
  if(alarm) {
    if (!samples[0].isPlaying()) samples[0].play();
  imageNumber = 9;
  }
}
float eyeX, prevEyeX, eyeY, prevEyeY;
int blinkTimer, nextBlinkTime, blinkDuration;
int eyeTimer, nextEyeTime, eyeOffsetX, eyeOffsetY;
int mode = 0;

//pupil constants
float minPupilSize = eyeSize * 0.4f;
float maxPupilSize = eyeSize * 0.7f;
float basePupilSize = eyeSize * 0.55f;
float dilationSpeed = 0.1f;
float contractionSpeed = 0.05f;
int lastEyeMoveTime = 0;
int eyeMoveThreshold = 200; // Time in milliseconds to consider eyes as focused
boolean isFocusing = false;

int sampleDelay=0;
public void draw() {
  
  getUserInput(); // Poll the input device
  background(127);
  fill(255);
  rect(0, 0, screenWidth, screenHeight);
if(sampleDelay>0) sampleDelay--;
  eyeX = (pupilPosX + eyeOffsetX)* 0.10 + prevEyeX * 0.90;
  eyeY = (pupilPosY + eyeOffsetY)* 0.10 + prevEyeY * 0.90;

  // Detect eye movement
  if (abs(eyeX - prevEyeX) > 0.5 || abs(eyeY - prevEyeY) > 0.5) {
    lastEyeMoveTime = millis(); // Update last eye move time
    isFocusing = false; // Not focusing
  } else {
    if (millis() - lastEyeMoveTime > eyeMoveThreshold) {
      isFocusing = true; // Eyes are stationary long enough
    }
  }

  if (millis()>blinkTimer+nextBlinkTime) {
    blinkTimer = millis();
    nextBlinkTime = (int)random(4000, 15000);
    blinkDuration = (int)random(5, 20);
  }
  if (blinkDuration>0) blinkDuration--;
  if (millis()>eyeTimer+nextEyeTime) {
    eyeTimer = millis();
    nextEyeTime = (int)random(1000, 4000);
    eyeOffsetX = (int)random(-15, 15);
    eyeOffsetY = (int)random(-2, 15);
  }

  prevEyeX = eyeX;
  prevEyeY = eyeY;

  if (blinkDuration>0) drawEyes((int)eyeX, (int)eyeY, true);
  else drawEyes((int)eyeX, (int)eyeY, blink);


  // Display an image prompted by the POV Hat (1-8)
  if (imageNumber != 0) {
    println(imageNames[imageNumber - 1]);
    int imgWidth = screenWidth/2;
    image(images[imageNumber-1], 0, 0, imgWidth, screenHeight);
    image(images[imageNumber-1], imgWidth, 0, imgWidth, screenHeight);
    // and play the linked sample from the list
    if(!samples[link[imageNumber-1]].isPlaying() && lastSample != imageNumber && sampleDelay == 0) {sampleDelay = 20; samples[link[imageNumber-1]].play(); lastSample = imageNumber;}
  }

  // Update pupil size based on focus and dilate button
  if (dilate) {
    pupilSize += (maxPupilSize - pupilSize) * dilationSpeed;
  } else if (isFocusing) {
    pupilSize += (minPupilSize - pupilSize) * contractionSpeed; // Enlarge pupils if focusing
  } else {
    pupilSize += (basePupilSize - pupilSize) * contractionSpeed; // Contract pupils if not focusing
  }

  pupilSize = constrain(pupilSize, minPupilSize, maxPupilSize);

  noCursor();
}


public void drawEyes(int x, int y, boolean blink) {
  int lidMid = screenHeight/2;
  int dLid = 0;
  if (y>screenHeight) y = screenHeight;
  if (y<0) y = 0;
  if (x<eyeSize/2) x = eyeSize/2;
  if (x>(screenWidth/2-eyeSize/2)) x = (screenWidth/2-eyeSize/2);
  if (samples[2].isPlaying()) fill(255, 0, 0, 255);
  else if (samples[5].isPlaying()) fill(255, 255, 0, 200);
  else if (samples[4].isPlaying()) fill(0, 0, 255, 200);
  else if (samples[1].isPlaying()) fill(0, 255, 0, 255);
  else fill(0, 255, 100, 200);
  stroke(0);
  if (mode==0) blink = true;
  ellipse(x, y, eyeSize, eyeSize);
  ellipse(x+screenWidth/2, y, eyeSize, eyeSize);
  fill(0);
  ellipse(x, y, pupilSize, pupilSize);
  ellipse(x+screenWidth/2, y, pupilSize, pupilSize);
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
  rect(0, screenHeight, screenWidth, 2*screenHeight);
}
