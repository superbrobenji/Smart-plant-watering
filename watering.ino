const int AirValue = 510;        //needs to be callibrated with air
const int WaterValue = 244;      //needs to be callibrated with water
int waterThreasholdPercent = 25; //the percentage that the soil must be under to water plant
int soilMoistureValue = 0;       //reading from sensor
int soilmoisturepercent = 0;     //reading from sensor in precent
int loopDataLog = 2700;
char incomingByte; // for incoming serial data

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Initialising...");
  delay(100); //Allow for serial print to complete

  Serial.println("Initialisation complete.");
  delay(100); //Allow for serial print to complete.
}

void loop()
{

  if (Serial.available() > 0)
  {
    incomingByte = Serial.read();
    int triggerCheck = atoi(&incomingByte);
    if (triggerCheck == 1)
    {
      measureSoilMoisture();
      triggerCheck = 0;
      delay(100);
    }
    else if (triggerCheck == 2)
    {
      waterPlant();
      triggerCheck = 0;
      delay(100);
    }
  }
  delay(300);
}

void waterPlant()
{
  measureSoilMoisture();
  if (soilmoisturepercent < waterThreasholdPercent)
  {
    triggerPump();
  }
  else
  {
  }
  Serial.println("water: 0");
}

void measureSoilMoisture()
{
  soilMoistureValue = analogRead(A0); //put Sensor insert into soil
  soilmoisturepercent = map(soilMoistureValue, AirValue, WaterValue, 0, 100);

  if (soilmoisturepercent >= 100)
  {
    handleData(100);
  }
  else if (soilmoisturepercent <= 0)
  {
    handleData(0);
  }
  else if (soilmoisturepercent > 0 && soilmoisturepercent < 100)
  {
    handleData(soilmoisturepercent);
  }
}

void triggerPump()
{
  //this is where I shall trigger the pump
  Serial.println("water: 1");
}

void handleData(int percent)
{

  //this is where I will send data to pi through serial.
  Serial.print("moisture: ");
  Serial.println(percent);

  Serial.print("sensor reading: ");
  Serial.println(soilMoistureValue);

  Serial.print("0% calibration: ");
  Serial.println(AirValue);

  Serial.print("100% calibration: ");
  Serial.println(WaterValue);

  Serial.print("pump trigger threshold: ");
  Serial.println(waterThreasholdPercent);
}
