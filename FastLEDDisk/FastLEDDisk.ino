#include "FastLED.h"

#define NUM_LEDS 255 

#define DATA_PIN SPI_DATA
#define CLOCK_PIN SPI_CLOCK

// Define the array of leds
CRGB leds[NUM_LEDS];

#define ringCount 10 //Total Number of Rings. AdaFruit Disk has 10

//Map rings on disk to indicies.
//This is where all the magic happens. 
//Each represents one of the concentric rings.
uint8_t rings[ringCount][2] = {
    {254,254},    //0 Center Point
    {248,253},    //1
    {236,247},    //2
    {216,235},    //3
    {192,215},    //4
    {164,191},    //5
    {132,163},    //6
    {92,131},    //7
    {48,91},    //8
    {0,47},     //9 Outter Ring
};

//For convenience, last ring index
uint8_t lastRing = ringCount - 1;

//Arrays containing degrees between each pixel for each ring.
//This is to speed up later calculations by doing these ahead of time.
//I've given everything with the option of using 360 degres per cirlce 
//or 256. The latter fits nicer into a single byte and *should* be a bit
//faster since it's only doing single byte math and not having to deal with
//negative angles since uint8_t already rolls around to a positive value.
//In the 256 degree per circle methods, 64 is equivalent to 90, 128 to 180, 
//and 192 to 270
float * ringSteps360;
float * ringSteps256;

//360 Degree Helper function to map angle and ring index to pixel
uint16_t angleToPixel360(int16_t angle, uint8_t ring)
{
  if(ring >= ringCount) return 0;
  angle = angle%360;
  if(angle < 0) angle = 360 + angle;
  return rings[ring][0] + int(angle/ringSteps360[ring]);
}

//256 Degree Helper function to map angle and ring index to pixel
uint16_t angleToPixel256(uint8_t angle, uint8_t ring)
{
  if(ring >= ringCount) return 0;
  return rings[ring][0] + int(angle/ringSteps256[ring]);
}

//Fill in the ringSteps arrays for later use.
inline void setupRings()
{
  ringSteps360 = (float*)malloc(ringCount * sizeof(float));
  uint8_t count = 0;
  for(int r=0; r<ringCount; r++)
  {
    count = (rings[r][1] - rings[r][0] + 1);
    ringSteps360[r] = (360.0/float(count));
  }

  ringSteps256 = (float*)malloc(ringCount * sizeof(float));
  count = 0;
  for(int r=0; r<ringCount; r++)
  {
    count = (rings[r][1] - rings[r][0] + 1);
    ringSteps256[r] = (256.0/float(count));
  }
}

//360 Degree helper to set a pixel, given angle and ring index
void setPixel360(int16_t angle, uint8_t ring, CRGB color)
{
  uint16_t pixel = angleToPixel360(angle, ring);
  leds[pixel] = color;
}

//256 Degree helper to set a pixel, given angle and ring index
void setPixel256(uint8_t angle, uint8_t ring, CRGB color)
{
  uint16_t pixel = angleToPixel256(angle, ring);
  leds[pixel] = color;
}

//360 Degree function to draw a line along a given angle from one ring to another
void drawRadius360(int16_t angle, CRGB color, uint8_t startRing, uint8_t endRing)
{
  if(startRing > lastRing) startRing = 0;
  if(endRing > lastRing) endRing = lastRing;
  for(uint8_t r=startRing; r<=endRing; r++)
  {
    setPixel360(angle, r, color);
  }
}

//256 Degree function to draw a line along a given angle from one ring to another
void drawRadius256(uint8_t angle, CRGB color, uint8_t startRing, uint8_t endRing)
{
  if(startRing > lastRing) startRing = 0;
  if(endRing > lastRing) endRing = lastRing;
  for(uint8_t r=startRing; r<=endRing; r++)
  {
    setPixel256(angle, r, color);
  }
}

//360 Degree function to fill a ring from one angle to another (draw an arc)
void fillRing360(uint8_t ring, CRGB color, int16_t startAngle, int16_t endAngle)
{
  uint8_t start = angleToPixel360(startAngle, ring);
  uint8_t end = angleToPixel360(endAngle, ring);
  if(start > end)
  {
    for(int i=start; i<=rings[ring][1]; i++)
    {
      leds[i] = color;
    }
    for(int i=rings[ring][0]; i<=end; i++)
    {
      leds[i] = color;
    }
  }
  else
  {
    for(int i=start; i<=end; i++)
    {
      leds[i] = color;
    }
  }
}

//256 Degree function to fill a ring from one angle to another (draw an arc)
void fillRing256(uint8_t ring, CRGB color, uint8_t startAngle, uint8_t endAngle)
{
  uint8_t start = angleToPixel256(startAngle, ring);
  uint8_t end = angleToPixel256(endAngle, ring);
  if(start > end)
  {
    for(int i=start; i<=rings[ring][1]; i++)
    {
      leds[i] = color;
    }
    for(int i=rings[ring][0]; i<=end; i++)
    {
      leds[i] = color;
    }
  }
  else
  {
    for(int i=start; i<=end; i++)
    {
      leds[i] = color;
    }
  }
}

void setup() { 
  setupRings();  

  Serial.begin(115200);
  LEDS.addLeds<APA102,DATA_PIN,CLOCK_PIN,BGR>(leds,NUM_LEDS);
  LEDS.setBrightness(64);
}


uint16_t pixel = 0;
uint8_t angle256 = 0;
void loop() { 

  //Chase a single pixel around the outer ring
  for(int angle360 = 0; angle360 < 360; angle360++)
  {
    FastLED.clear();
    setPixel360(angle360, lastRing, CRGB::Red);
    FastLED.show();
  }

  //Chase a single pixel around the outer ring using 256 degrees per circle.
  //Note that this will appear faster because there are less steps in the circle.
  angle256 = 0;
  while(true)
  {
    FastLED.clear();
    setPixel256(angle256, lastRing, CRGB::Green);
    FastLED.show();
    angle256++;
    if(angle256 == 0) break;
  }

  //Chase radius line using 360 degrees per circle
  for(int angle360 = 0; angle360 < 360; angle360++)
  {
    FastLED.clear();
    drawRadius360(angle360, CRGB::Blue, 0, lastRing);
    FastLED.show();
  }

  //Chase radius line using 256 degrees per circle
  angle256 = 0;
  while(true)
  {
    FastLED.clear();
    drawRadius256(angle256, CRGB::Purple, 0, lastRing);
    FastLED.show();
    angle256++;
    if(angle256 == 0) break;
  }

  //Draw a half circle (180 degree) rainbow using 360 degrees per circle
  for(int angle360 = 0; angle360 < 360; angle360++)
  {
    FastLED.clear();
    fillRing360(9, CRGB::Red, angle360 - 90, angle360 + 90);
    fillRing360(8, CRGB::Orange, angle360 - 90, angle360 + 90);
    fillRing360(7, CRGB::Yellow, angle360 - 90, angle360 + 90);
    fillRing360(6, CRGB::Green, angle360 - 90, angle360 + 90);
    fillRing360(5, CRGB::Blue, angle360 - 90, angle360 + 90);
    fillRing360(4, CRGB::Purple, angle360 - 90, angle360 + 90);
    FastLED.show();
  }

  //Draw a half circle (128 degree) rainbow using 256 degrees per circle
  angle256 = 0;
  while(true)
  {
    FastLED.clear();
    fillRing256(9, CRGB::Purple, angle256 - 64, angle256 + 64);
    fillRing256(8, CRGB::Blue, angle256 - 64, angle256 + 64);
    fillRing256(7, CRGB::Green, angle256 - 64, angle256 + 64);
    fillRing256(6, CRGB::Yellow, angle256 - 64, angle256 + 64);
    fillRing256(5, CRGB::Orange, angle256 - 64, angle256 + 64);
    fillRing256(4, CRGB::Red, angle256 - 64, angle256 + 64);
    FastLED.show();
    angle256++;
    if(angle256 == 0) break;
  }
}


