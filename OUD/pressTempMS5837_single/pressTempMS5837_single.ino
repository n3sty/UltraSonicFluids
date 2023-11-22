/* Blue Robotics MS5837 Library Example
  -----------------------------------------------------

  Title: Blue Robotics MS5837 Library Example

  Description: This example demonstrates the MS5837 Library with a connected
  sensor. The example reads the sensor and prints the resulting values
  to the serial terminal.

  The code is designed for the Arduino Uno board and can be compiled and
  uploaded via the Arduino 1.0+ software.

  -------------------------------
  The MIT License (MIT)

  Copyright (c) 2015 Blue Robotics Inc.

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
  -------------------------------*/

#include <Wire.h>
#include "MS5837.h"

MS5837 sensor;

float myVals[6] = {0, 0, 0, 0, 0, 0};

int sensorPin0 = A0;    // dummy analog value for home testing
int sensorPin1 = A1;    // dummy analog value for home testing

extern "C" {
#include "utility/twi.h"  // from Wire library, so we can do bus scanning
}

#define TCAADDR 0x70




void setup()
{
  while (!Serial);
  delay(1000);

  Wire.begin();

  Serial.begin(115200);
  Serial.setTimeout(1000);

  while (!sensor.init()) {
    Serial.println("Init sensor failed!");
    delay(5000);
  }
  sensor.setModel(MS5837::MS5837_30BA);
  sensor.setFluidDensity(997); // kg/m^3 (freshwater, 1029 for seawater)

  //Serial.println("\ndone");
}


void loop() {
  if (Serial.available() > 0) {
    int A = Serial.read();
    Serial.read();

    if (A == 49){
      // 1 Update pressure and temperature readings
      
      sensor.read();
      myVals[0] = 1.045 * sensor.pressure();
      myVals[1] = sensor.temperature();

      myVals[2] = analogRead(sensorPin0);
      myVals[3] = analogRead(sensorPin1);
  
    } else if (A == 48){
      // 0 Update pressure and temperature readings RAW
      
      sensor.read();
      myVals[0] = sensor.presRAW();
      myVals[1] = sensor.tempRAW(); //temperature();

    } else if (A == 50){
      // 2 read sensor 2 C values
      
      //sensor2.read();
      for (int i = 0; i < 6; i++) {
        myVals[i] = sensor.Cval(i+1);
      }       
    } else{
      // bad index catch
      for (int i = 0; i < 6; i++) {
        myVals[i] = 0.0;
      }
    }
    
    for (int i = 0; i < 6; i++)
    {
      Serial.print(myVals[i]);
      Serial.print("; ");
    }

    Serial.println("");
  }
  delay(100);
}
