// Stepper motor output
int STEP_PUL = 12; //define Pulse pin
int STEP_DIR = 11; //define Direction pin
int STEP_ENA = 10; //define Enable Pin

// Jetson nano input
int NANO_SPEED[] = {4, 5, 6, 7}; //2^4 = 16 speed control
/* Pin 2 MSB
 * Pin 5 LSB
 * 0000 - 1111
 * 900 - 100 (us)
 * Each bit is 50us
 */
int NANO_DIR = 8;
int NANO_ENA = 9;

int value;

int udelay = 0; //Delay between pulses

void setup() {
  Serial.begin(9600); 
  
  pinMode (STEP_PUL, OUTPUT);
  pinMode (STEP_DIR, OUTPUT);
  pinMode (STEP_ENA, OUTPUT);

  for (int x = 0; x < 4; x++){
    pinMode(NANO_SPEED[x], INPUT);
  }
  pinMode (NANO_DIR, INPUT);
  pinMode (NANO_ENA, INPUT);

}

void loop() {


  if(digitalRead(NANO_ENA) == HIGH){
    // Get direction
    value = digitalRead(NANO_DIR);
    digitalWrite(STEP_DIR,value);

    // Get speed
    udelay =  750;
    for (int x = 0; x < 4; x++){
      if(digitalRead(NANO_SPEED[x]) == HIGH){
        udelay = udelay - 150;
      }
    }
    
    digitalWrite(STEP_ENA,HIGH);
    digitalWrite(STEP_PUL,HIGH);
    delayMicroseconds(udelay);
    digitalWrite(STEP_PUL,LOW);
    delayMicroseconds(udelay);

    
    //int ena = digitalRead(NANO_ENA);
    //int dir = digitalRead(NANO_DIR);
    //Serial.print("Speed: ");
    //int spd [] = {0, 0, 0, 0};
    //for (int x = 0; x < 4; x++){
    //  spd[x] = digitalRead(NANO_SPEED[x]);
    //  Serial.print(spd[x]);
    //}
  
    //Serial.print(" ENA: ");
    //Serial.print(ena);
    //Serial.print(" DIR: ");
    //Serial.print(dir);
    
    //Serial.print("\n");
    }

}
