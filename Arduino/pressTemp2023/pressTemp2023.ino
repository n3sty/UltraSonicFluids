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

MS5837 sensor2;
MS5837 sensor4;
MS5837 sensor6;

float myVals[6] = {0, 0, 0, 0, 0, 0};

extern "C" {
#include "utility/twi.h"  // from Wire library, so we can do bus scanning
}

#define TCAADDR 0x70

void tcaselect(uint8_t i) {
  if (i > 7) return;

  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();
}


void setup()
{
  while (!Serial);
  delay(1000);

  Wire.begin();

  Serial.begin(115200);
  Serial.setTimeout(1000);

  tcaselect(2);
  //Serial.println("TCA Port #2");
  while (!sensor2.init()) {
    Serial.println("Init 2 failed!");
    delay(5000);
  }
  sensor2.setModel(MS5837::MS5837_30BA);
  sensor2.setFluidDensity(997); // kg/m^3 (freshwater, 1029 for seawater)

  tcaselect(4);
  //Serial.println("TCA Port #4");
  while (!sensor4.init()) {
    Serial.println("Init 4 failed!");
    delay(5000);
  }
  sensor4.setModel(MS5837::MS5837_30BA);
  sensor4.setFluidDensity(997); // kg/m^3 (freshwater, 1029 for seawater)

  tcaselect(6);
  //Serial.println("TCA Port #6");
  while (!sensor6.init()) {
    Serial.println("Init 6 failed!");
    delay(5000);
  }
  sensor6.setModel(MS5837::MS5837_30BA);
  sensor6.setFluidDensity(997); // kg/m^3 (freshwater, 1029 for seawater)
  Serial.println("Init succeeded"); 
}


void loop() {
  if (Serial.available() > 0) {
    int A = Serial.read();  // input over Serial
    Serial.read();
    
    if (A == 49) { //Over serial: "1"
      // 1 Update pressure and temperature readings
      tcaselect(2);
      sensor2.read();
      myVals[0] = 1.045 * sensor2.pressure(); // waarom 1.045???
      myVals[1] = sensor2.temperature();
  
      tcaselect(4);
      sensor4.read();
      myVals[2] = sensor4.pressure();
      myVals[3] = sensor4.temperature();
  
      tcaselect(6);
      sensor6.read();
      myVals[4] = sensor6.pressure();
      myVals[5] = sensor6.temperature();
    } else {
      // bad index catch
      for (int i = 0; i < 6; i++) {
        myVals[i] = 0.0;
      }
    }
    
    for (int i = 0; i < 5; i++)
    {
      Serial.print(myVals[i]);
      Serial.print(", ");
    }
    Serial.print(myVals[5]);

    Serial.println("");
  }
  delay(50);
}



// oud stukje code, was al uitgecomment - M
//void loop() {
//  // Update pressure and temperature readings
//  tcaselect(2);
//  sensor2.read();
//  myVals[0] = 1.045*sensor2.pressure();
//  myVals[1] = sensor2.temperature();
//
//  tcaselect(4);
//  sensor4.read();
//  myVals[2] = sensor4.pressure();
//  myVals[3] = sensor4.temperature();
//
//  tcaselect(6);
//  sensor6.read();
//  myVals[4] = sensor6.pressure();
//  myVals[5] = sensor6.temperature();
//
//  for (int i = 0; i < 6; i++)
//  {
//    Serial.print(myVals[i]);
//    Serial.print(", ");
//  }
//
//  Serial.println("");
//  delay(100);
//}
