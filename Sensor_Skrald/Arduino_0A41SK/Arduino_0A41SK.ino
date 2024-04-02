#define pin 2    
void setup () 
{          
          Serial.begin (115200);
          pinMode(pin, INPUT);
}

void loop () 
{
          uint16_t value = analogRead (pin);
          double distance = get_IR (value);
          Serial.println (value);
           Serial.print (distance);
          Serial.println (" cm");
          Serial.println ();
          delay (500);     
}

double get_IR (uint16_t value) 
{ 
         if (value < 16)  value = 16;
          return 2076.0 / (value - 11.0);
}