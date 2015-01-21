
#include <Arduino.h>
#include <SoftwareSerial.h>
#include "WiFly.h"

#define SSID      "abc"
#define KEY       ""
// WIFLY_AUTH_OPEN / WIFLY_AUTH_WPA1 / WIFLY_AUTH_WPA1_2 / WIFLY_AUTH_WPA2_PSK
#define AUTH      WIFLY_AUTH_OPEN

// #define UDP_HOST_IP        "255.255.255.255"      // broadcast
#define UDP_HOST_IP        "192.168.0.103"      // broadcast
#define UDP_REMOTE_PORT    55555
#define UDP_LOCAL_PORT     55555

// Pins' connection
// Arduino       WiFly
//  2    <---->    TX
//  3    <---->    RX
SoftwareSerial uart(2, 3);
WiFly wifly(uart);

void setupUDP(const char *host_ip, uint16_t remote_port, uint16_t local_port)
{
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

void setup() {

  Serial.begin(9600);
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
  
  setupUDP(UDP_HOST_IP, UDP_REMOTE_PORT, UDP_REMOTE_PORT);
  // displayInfo();
  delay(1000);
  wifly.clear();
  Serial.println("Start Looping");
  // wifly.send("I'm wifly, I'm living\r\n");
  Serial.println("Sending");
  wifly.send("ACK\r\n");
}

void displayInfo(){
  // wifly.sendCommand("get everthing\r");
  char c;
  while (wifly.receive((uint8_t *)&c, 1, 300) > 0) {
    Serial.print((char)c);
  }
}

long unsigned int time_point = 0;
#define MESSAGEBUFFER 128
char message[MESSAGEBUFFER];
int messagePointer = 0;
int msgstar = 0;
int mesgSize = 0;

void loop() {

  int c;
  if (wifly.available())
  {
    // Serial.println("----------------------->");
    while (wifly.available()) {
      c = wifly.read();
      message[messagePointer] = c;

      messagePointer = (messagePointer + 1) % MESSAGEBUFFER;
      // Serial.print(c, HEX);
      // Serial.print(":");
      mesgSize++;

      if (c == 0x64) break;

    } // end while
    // Serial.println("\n<-----------------------");

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
      // find a end point. 
      if (mesgSize > 200) {
        // message is too big, something wrong here. 
      }

      if (char(message[(msgstar + 0) % MESSAGEBUFFER]) == 'C')
      {
        int packetSize = int(message[(msgstar + 1) % MESSAGEBUFFER]);  // base servo
          
        if (mesgSize != packetSize)
        {
          Serial.println("========= Bad Packet ========= ");
        }

        // control model
        if (message[(msgstar + 1) % MESSAGEBUFFER] == 0)
        {
          // turn left
        } else if (message[(msgstar + 1) % MESSAGEBUFFER] == 1)
        {
          // go straight
        }if (message[(msgstar + 1) % MESSAGEBUFFER] == 2)
        {
          // turn right
        }

        int servo0 = int(message[(msgstar + 3) % MESSAGEBUFFER]);  // base servo
        int servo1 = int(message[(msgstar + 4) % MESSAGEBUFFER]);  // left servo
        int servo2 = int(message[(msgstar + 5) % MESSAGEBUFFER]);  // right servo
        int servo3 = int(message[(msgstar + 6) % MESSAGEBUFFER]);  // graber


        // TODO; fix bug here , ring bug. 
        int speed = *((int *) &message[(msgstar + 8) % MESSAGEBUFFER]);
        int packetNumber = *((int *) &message[(msgstar + 12) % MESSAGEBUFFER]);


        // Serial.print("speed: ");
        // Serial.println(speed);
        // Serial.println("Receive C");
        Serial.print("packet number: ");
        Serial.println(packetNumber);
        
        // Serial.print("Packet Size:");
        // Serial.println(packetSize);

        // Serial.print("Message Size:");
        // Serial.println(mesgSize);

        char str[80];
        sprintf(str, "ACK packetSize: %d, packetNumber: %d speed: %d \r\n", packetSize, packetNumber, speed);
        wifly.send(str);

      }

      if ((msgstar + mesgSize)%MESSAGEBUFFER == messagePointer)
        messagePointer = 0;

      msgstar = messagePointer;
      mesgSize = 0;

    } 
  }

  
    // send an UDP packet in every 10 second
  if ((millis() - time_point) > 10000) {
    time_point = millis();
    // Serial.print("Time: ");
    // Serial.println(time_point, DEC);
    // Serial.println(time_point, HEX);
    // Serial.println("Sending");
    Serial.println("Sending: I'm wifly, I'm living");
    wifly.send("I'm wifly, I'm living\r\n");
  }
}