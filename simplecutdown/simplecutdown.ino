#include <stdio.h>

// Launch time, in minutes
unsigned long launchDelay = 15;
// Use the onboard LED on pin 13 for debugging
int debugLED = 13;
// Burn circuit triggered on 5v from pin 12
int burnPin = 6;
// A character buffer for cleanly printing output
char output[100];

void setup() {
  // Initialize pins
  pinMode(debugLED, OUTPUT);
  pinMode(burnPin, OUTPUT);
  
  // Ensure pins stay LOW until burn time
  digitalWrite(debugLED, LOW);
  digitalWrite(burnPin, LOW);
  
  // Serial communications used for debugging
  Serial.begin(9600);
  sprintf(output, "Burn timer set for %d minutes.", launchDelay);
  Serial.println(output);

}

void cutdown(){
  // Engages burn circuit for 5 sec, then goes dormant
  Serial.print("Beginning burn.. ");
  // Heat the burn wire
  digitalWrite(burnPin, HIGH);
  digitalWrite(debugLED, HIGH);
  
  delay(5000);
  
  // Turn off burn wire and LED
  digitalWrite(debugLED, LOW);
  digitalWrite(burnPin, LOW);
  
  Serial.println("burn complete.");
  while(true) ; // Does nothing, forever.
}

void loop() {
  // Get time in seconds, since the arduino powered up
  unsigned long curSec = millis()/1000;

  // Compare launch time (min) against time since launch (rounded down to min)
  if(curSec/60 >= launchDelay){
    cutdown();
  }

  // Display some debugging information
  sprintf(output, "Current time: %lu minutes and %lu seconds.", curSec/60, curSec%60);
  Serial.println(output);

  // Blink the LED on/off every other second while waiting to burn
  digitalWrite(debugLED, curSec%2==0?HIGH:LOW);
  
  delay(1000); // Not necessary, but reduces spammy output
}
