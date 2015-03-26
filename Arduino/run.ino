#include <Wire.h>
#include <SoftwareSerial.h>
#include <Arduino.h>
// #include <EEPROM.h>


// #include "utility/Adafruit_PWMServoDriver.h"
#include "Adafruit_PWMServoDriver.h"
#include "Adafruit_MotorShield.h"
#include "WiFly.h"


#define LEFT 4
#define RIGHT 8
#define BOTTOM 0
#define CLIPPER 12


#define LP 450  // Big to raise
#define RP 111
#define BP 360
#define CP 160 // From 140 - 190

#define SINGLEMOVEDELAY 50 // Normal
// #define SINGLEMOVEDELAY 200 // Testing

#define SSMOVEDELAY 15 //Normal
#define SSMOVEDIFFERNCE 4
// #define SSMOVEDELAY 50 //Testing

#define MOVINGPERIOD 300 // Normal
// #define MOVINGPERIOD 2000

#define NONEWIFIPERIOD 2000


// WhatisPassword
#define SSID      "whatIsPassword"
#define KEY       "12345678909"
#define AUTH      WIFLY_AUTH_WPA2_PSK
#define UDP_HOST_IP        "192.168.0.19"      // broadcast


// #define UDP_HOST_IP        "255.255.255.255"      // broadcast
// WIFLY_AUTH_OPEN / WIFLY_AUTH_WPA1 / WIFLY_AUTH_WPA1_2 / WIFLY_AUTH_WPA2_PSK
// #define SSID      "abc"
// #define AUTH      WIFLY_AUTH_OPEN
// #define KEY       ""
// #define UDP_HOST_IP        "192.168.0.102"      // broadcast


#define UDP_REMOTE_PORT    55555
#define UDP_LOCAL_PORT     55555

#define MESSAGEBUFFER 128

#define SENSORPIN 10


int LeftCurrentPosition = LP;
int RightCurrentPosition = RP;
int BotCurrentPosition = BP;
int ClipperCurrentPosition = CP;

int motorSpeed = 0;
int direction = 1;

int servo0_base = BP;  // base servo
int servo1_left = LP;  // left servo
int servo2_rightServo = RP;  // RIGHT servo
int servo3_grabber = CP;  // graber


long unsigned int time_point = 0;
long unsigned int time_point2 = 0;
long unsigned int time_point3_wifiConnection = 0;
long unsigned int time_point4_badPacketCounter = 0;



char message[MESSAGEBUFFER];
int messagePointer = 0;
int msgstar = 0;
int mesgSize = 0;


int connectionStatus = 0;

//pin for sensor


// Pins' connection
// Arduino       WiFly
//  2    <---->    TX
//  3    <---->    RX
SoftwareSerial uart(2, 3);
WiFly wifly(uart);

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();


// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 
Adafruit_DCMotor *backMotor = AFMS.getMotor(1);
Adafruit_DCMotor *frontMotor = AFMS.getMotor(3);


void displayInfo() {
  // wifly.sendCommand("get everthing\r");
  char c;
  while (wifly.receive((uint8_t *)&c, 1, 300) > 0) {
    Serial.print((char)c);
  }
}


void setupUDP(const char *host_ip, uint16_t remote_port, uint16_t local_port) {
  char cmd[32];
  
  wifly.sendCommand("set w j 1\r", "AOK");   // enable auto join
  wifly.sendCommand("set i p 1\r", "AOK");
  snprintf(cmd, sizeof(cmd), "set i h %s\r", host_ip);
  wifly.sendCommand(cmd, "AOK");
  snprintf(cmd, sizeof(cmd), "set i r %d\r", remote_port);
  wifly.sendCommand(cmd, "AOK");
  snprintf(cmd, sizeof(cmd), "set i l %d\r", local_port);
  wifly.sendCommand(cmd, "AOK");
  wifly.sendCommand("save\r");
  wifly.sendCommand("reboot\r");
}

void singleMove(int servoNumber, int Position) {

  int* servoPos;
  if (servoNumber == RIGHT)
  {
    servoPos =  &RightCurrentPosition;
  } 
  else if (servoNumber == LEFT) {
    servoPos = & LeftCurrentPosition;
  }
  else if (servoNumber == BOTTOM) {
    servoPos = & BotCurrentPosition;
  } 
  else if (servoNumber == CLIPPER) {
    servoPos = & ClipperCurrentPosition;
  }

  // Serial.print("=====In move on: "); Serial.print(servoNumber);
  // Serial.print(" Pos: "); Serial.println(*servoPos);

  int different = 4;

  while ((*servoPos - Position) >= different || (*servoPos - Position) <= -different){

    if (*servoPos > Position){
     (*servoPos) -= different; 
    }else{
     (*servoPos) += different; 
    }
    pwm.setPWM(servoNumber, 0, *servoPos);
    delay(SINGLEMOVEDELAY);

  } 

  // delay(100);

  if (servoNumber != CLIPPER)
  {
    pwm.setPWM(servoNumber, 0, 0);
  }

}

int singleSingleMove(int servoNumber, int Position) {
  int* servoPos;
  if (servoNumber == RIGHT)
    servoPos =  &RightCurrentPosition;
  else if (servoNumber == LEFT) 
    servoPos = & LeftCurrentPosition;
  else if (servoNumber == BOTTOM)
    servoPos = & BotCurrentPosition;
  else if (servoNumber == CLIPPER)
    servoPos = & ClipperCurrentPosition;

  int different = SSMOVEDIFFERNCE;

  if ((*servoPos - Position) >= different || (*servoPos - Position) <= -different)
  {
    if (*servoPos > Position)
     (*servoPos) -= different; 
    else
     (*servoPos) += different; 



    // Serial.print(" (");
    // Serial.print(servoNumber);
    // Serial.print(") ");
    pwm.setPWM(servoNumber, 0, *servoPos);
    delay(SSMOVEDELAY);

      if (servoNumber != CLIPPER)
        pwm.setPWM(servoNumber, 0, 0);
    return 1;
  }
  else {
    // pwm.setPWM(servoNumber, 0, *servoPos);
    // delay(SSMOVEDELAY);

    // if (servoNumber != CLIPPER)
    //     pwm.setPWM(servoNumber, 0, 0);
    return 0;
    
  }

}

void smartMove(int x, int y, int z, int w) {
  int count = 0;
  while(true) {
    count ++;
    int result = singleSingleMove(LEFT, x) + singleSingleMove(RIGHT, y);
    result += singleSingleMove(BOTTOM, z) + singleSingleMove(CLIPPER, w);

    // Serial.print("Current: (");
    // Serial.print(LeftCurrentPosition);
    // Serial.print(", ");
    // Serial.print(RightCurrentPosition);
    // Serial.print(", ");
    // Serial.print(BotCurrentPosition);
    // Serial.print(", ");
    // Serial.print(ClipperCurrentPosition);
    // Serial.println(") ");

     // delay(2000);
    // if (result == 0 || (millis() - time_point2 > MOVINGPERIOD)) {
    if (result == 0) {
      delay(100);
      pwm.setPWM(LEFT, 0, 0);
      pwm.setPWM(RIGHT, 0, 0);
      pwm.setPWM(BOTTOM, 0, 0);
      // pwm.setPWM(CLIPPER, 0, 0);
      // delay(2000);

      break;
    }
  }

  // if (count > 10)
  // {
  //   Serial.print("Count:"); 
  //   Serial.println(count); 
  // }
}

void MoveoverallFast(int x,int y,int z,int w){
  pwm.setPWM(RIGHT, 0, x);
  delay(120);
   pwm.setPWM(LEFT, 0, y);
     delay(120);
  pwm.setPWM(BOTTOM, 0, z);
    delay(120);
  pwm.setPWM(CLIPPER, 0, w);
    delay(120);

  RightCurrentPosition = x;
  LeftCurrentPosition = y;
  BotCurrentPosition = z;
  ClipperCurrentPosition = w;
}

void moveoverall(int leftServo, int rightServo, int baseServo, int cliperServo = ClipperCurrentPosition){
  singleMove(LEFT, leftServo);
  singleMove(RIGHT, rightServo);
  singleMove(BOTTOM, baseServo);
  singleMove(CLIPPER, cliperServo);
}

// Direction Control
void turn(int dire){
  // moveFoward(255);
  // SetUp speed and dire
  if (dire == 0)
  {
    turnLeft();// turn left
  } else if (dire == 1)
  {
    turnStraight();
  }if (dire == 2)
  {
    turnRight();// turn right
  } 
}

void turnRight(){
  frontMotor->run(BACKWARD);
  frontMotor->setSpeed(255);
}

void turnLeft(){
  frontMotor->run(FORWARD);
  frontMotor->setSpeed(255);
}

void turnStraight(){
  frontMotor->run(FORWARD);
  frontMotor->setSpeed(0);
}

void stationanryBackMotor(){
  backMotor->run(RELEASE);
}

void stationanryFrontMotor(){
  backMotor->run(RELEASE);
}


void move(int sp) {
  if(sp > 0 ){
    moveFoward(sp);
  }
  else{
    moveBackward(sp);
  }// go straight
}


void moveFoward(int x){
  backMotor->run(FORWARD);
  backMotor->setSpeed(x);
}

void moveBackward(int x){
  backMotor->run(BACKWARD);
  backMotor->setSpeed(abs(x)); 
}





void setup() {

  Serial.begin(9600);
  AFMS.begin();  
  // Serial.println("16 channel Servo test begin!");

  
  // pwd for servo  
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates

  // smartMove(LP, RP, BP, CP);

  delay(100);

  //for wifi purposes
  Serial.println("--------- WIFLY UDP --------");
  uart.begin(9600);     // WiFly UART Baud Rate: 9600
  wifly.reset();
  pinMode(8,OUTPUT);


  while (1) {
    Serial.println("Try to join " SSID );
    if (wifly.join(SSID, KEY, AUTH)) {
      Serial.println("Succeed to join " SSID);
      wifly.clear();
      break;
    } else {
      Serial.println("Failed to join " SSID);
      Serial.println("Wait 1 second and try again...");
      delay(1000);
    }
  }
  setupUDP(UDP_HOST_IP, UDP_REMOTE_PORT, UDP_LOCAL_PORT);
  // displayInfo();
  // delay(1000);
  wifly.clear();
  Serial.println("Start Looping");
  wifly.send("HARM: ACK\r\n");
}

// void printTargetPosition(){
//     Serial.println("\n===============================================");
//     Serial.print("TargetPos: (");
//     Serial.print(servo1_left);
//     Serial.print(", ");
//     Serial.print(servo2_rightServo);
//     Serial.print(", ");
//     Serial.print(servo0_base);
//     Serial.print(", ");
//     Serial.print(servo3_grabber);
//     Serial.println(") ");
// }

long microsecondsToCentimeters(long microseconds)
{
  return microseconds / 29 / 2;
}

long sensorDistance() 
{
  // Serial.print(cm);
  // Serial.println("cm");
  long duration, cm;
  pinMode(SENSORPIN, OUTPUT);
  digitalWrite(SENSORPIN, LOW);
  delayMicroseconds(2);
  digitalWrite(SENSORPIN, HIGH);
  delayMicroseconds(5);
  digitalWrite(SENSORPIN, LOW);

  pinMode(SENSORPIN, INPUT);
  duration = pulseIn(SENSORPIN, HIGH);

  cm = microsecondsToCentimeters(duration);
  return cm;
}

void loop() {

  // int servo0_base = BP;  // base servo
  // int servo1_left = LP;  // left servo
  // int servo2_rightServo = RP;  // RIGHT servo
  // int servo3_grabber = CP;  // graber
  // int isMessage = 0;  // if there is a message, set to 

  // EEPROM.write(0, 1);
  // EEPROM.write(2, 2);
  // EEPROM.write(4, 3);
  // EEPROM.write(6, 4);
  // byte value;
  // value = EEPROM.read(0);  
  // Serial.println(value, DEC);
  // value = EEPROM.read(2);  
  // Serial.println(value, DEC);
  // value = EEPROM.read(4);  
  // Serial.println(value, DEC);
  // value = EEPROM.read(6);  
  // Serial.println(value, DEC);


  // Serial.print("===================Loop ============================\n");
  // delay(1000);

  // testing
  #if 0
  // backMotor->run(FORWARD);
  // backMotor->setSpeed(100);
  // delay(1000);
  // backMotor->setSpeed(0);


  Serial.print("Prepare\n");
  moveoverall(LP, RP, BP, CP);
  Serial.print("Moving\n");
  delay(2000);
  Serial.print("Moving 1 \n");
  moveoverall(LP + 50, RP + 50, BP + 150, CP);
  delay(1000);

  Serial.print("Moving back \n");
  moveoverall(LP, RP, BP, CP);
  delay(2000);

  Serial.print("Moving 2\n");
  smartMove(LP, RP, BP, CP);
  delay(1000);
  Serial.print("Moving 2 start\n");
  smartMove(LP + 50, RP + 50, BP + 150, CP);


  backMotor->run(BACKWARD);
  backMotor->setSpeed(100);

  delay(3000);

  #endif


  // wifi 
  #if 1
  int c;
  if (wifly.available())
  {
    // Serial.println("\n----------------------->");
    while (wifly.available()) {
      c = wifly.read();
      message[messagePointer] = c;
      messagePointer = (messagePointer + 1) % MESSAGEBUFFER;
      // Serial.print(c, HEX);
      // Serial.print(":");
      mesgSize++;

      if (c == 0x64) break;

    }  //end while
    // Serial.println("\n<-----------------------\n");

    // trying to find end string 'end'
    int e, n, d;
    e = messagePointer -3;
    n = messagePointer -2;
    d = messagePointer -1;
    if (d < 0) d += MESSAGEBUFFER;
    if (n < 0) n += MESSAGEBUFFER;

    if (message[e] == 0x65
      && message[n] == 0x6E
      && message[d] == 0x64)
    {
      time_point3_wifiConnection = millis();

      // find a end point. 
      if (mesgSize > 200) {
        // message is too big, something wrong here. 
      }
      connectionStatus = 1;

      int packetSize = int(message[(msgstar + 1) % MESSAGEBUFFER]);  // base servo
          
      if (mesgSize != packetSize)
      {
        Serial.print("mesageSize: ");
        Serial.print(mesgSize);
        Serial.print("packet Size: ");
        Serial.println(packetSize);
        Serial.println("========= Bad Packet ========= ");
        wifly.send("HARM badPack");
        time_point4_badPacketCounter = millis();

        messagePointer = 0;
        msgstar = 0;
        mesgSize = 0;
      } else {
        // get a good message
        
        if (char(message[(msgstar + 0) % MESSAGEBUFFER]) == 'C')
        {
          time_point4_badPacketCounter = 0;
          // get all information from message
          direction = int(message[(msgstar + 2) % MESSAGEBUFFER]);
          servo1_left = *((int *) &message[(msgstar + 3) % MESSAGEBUFFER]);  // base servo
          servo2_rightServo = *((int *) &message[(msgstar + 7) % MESSAGEBUFFER]);  // left servo
          servo0_base = *((int *) &message[(msgstar + 11) % MESSAGEBUFFER]);  // right servo
          servo3_grabber = *((int *) &message[(msgstar + 15) % MESSAGEBUFFER]);  // graber

          // TODO; fix bug here , ring bug. 
          motorSpeed = *((int *) &message[(msgstar + 19) % MESSAGEBUFFER]);
          int packetNumber = *((int *) &message[(msgstar + 23) % MESSAGEBUFFER]);
          

          #if 1
          // Serial.println("Receive Command update");
        
          Serial.print("direction: ");
          Serial.print(direction);

          Serial.print(", speed: ");
          Serial.println(motorSpeed);

          // Serial.print("servo0_base: ");
          // Serial.println(servo0_base);

          // Serial.print("servo1_left: ");
          // Serial.println(servo1_left);

          // Serial.print("servo2_rightServo: ");
          // Serial.println(servo2_rightServo);


          // Serial.print("servo3_grabber: ");
          // Serial.println(servo3_grabber);
          
          // Serial.print("packet number: ");
          // Serial.println(packetNumber);
          
          // Serial.print("Packet Size:");
          // Serial.println(packetSize);

          // Serial.print("Message Size:");
          // Serial.println(mesgSize);

          #endif
          char str[80];
          // sprintf(str, "HARM: ACK %d \r", packetNumber);
          sprintf(str, "HARM: ACK packetSize: %d, packetNumber: %d speed: %d \r\n", packetSize, packetNumber, motorSpeed);
          wifly.send(str);

        } else if (char(message[(msgstar + 0) % MESSAGEBUFFER]) == 'A')
        {
          int packetNumber = *((int *) &message[(msgstar + 2) % MESSAGEBUFFER]);
          char str[80];
          sprintf(str, "HARM: A packetNumber: %d \r", packetNumber);
          wifly.send(str);
        }

        if ((msgstar + mesgSize)%MESSAGEBUFFER == messagePointer)
          messagePointer = 0;

        msgstar = messagePointer;
        mesgSize = 0;


        // moveoverall(servo1_left, servo2_rightServo, servo0_base, servo3_grabber);

      }

    } 
  } // End wifi
  #endif 

  // send an UDP packet in every 10 second
  // if ((millis() - time_point) > 10000 || connectionStatus == 0) {
  if (connectionStatus == 0) {
    time_point = millis();
    Serial.println("Sending: WifiSignal");
    wifly.send("HARM: CONNECTION\r");
    delay(500);
  }


  long unsigned int t = millis();
  // reset H-ARM when there is no WIFI signal in 5 sec
  if (((t - time_point3_wifiConnection) > NONEWIFIPERIOD && connectionStatus != 0)|| 
      (time_point4_badPacketCounter != 0 && t - time_point4_badPacketCounter > 1000)) {
    // stop, and move arm back
    connectionStatus = 0;
    Serial.println("No Connection, Reset everything");
    turn(1);
    move(0);
    smartMove(LP, RP, BP, CP);
  } 
  else{
    if ((millis() - time_point2) > MOVINGPERIOD) {
      // Moving arm in each x sec. x is define by MOVINGPERIOD
      time_point2 = millis();
      // printTargetPosition();
      smartMove(servo1_left, servo2_rightServo, servo0_base, servo3_grabber);
    }

    long cm = 100;
    cm = sensorDistance();

    // char str[80];
    // sprintf(str, "HARM: distance: %d cm\r", cm);
    // wifly.send(str);

    // small than 10 cm, must stop
    // small than 40 cm, speed must below 100 
    if (cm < 10 && motorSpeed > 0) {
      move(0);
      // wifly.send("HARM: Stop, distance small then 30\r");
    } else if (cm < 100 && motorSpeed > 0) {
      // wifly.send("HARM: Slow down, distance small than 100\r");
      if (motorSpeed > 90) {
        turn(direction);
        move(90);
      }
    } else {
      turn(direction);
      move(motorSpeed);
    }
  } 
  delay(100);
} // end main