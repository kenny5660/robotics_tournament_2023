#include <Arduino.h>
#include <Servo.h>

Servo serv1,serv2;
void setup() {
    serv1.attach(12);
    serv1.write(90);
    serv2.attach(11);
    serv2.write(0);
}

void loop() {
  
}