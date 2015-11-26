
String readString;
char c ;
const int redPin1 = 2;
const int greenPin1 = 4;
const int bluePin1 = 3;
const int redPin2 = 10;
const int greenPin2 = 11;
const int bluePin2 = 12;

int red1 ;
int blue1 ;
int green1 ;
int red2;
int blue2;
int green2;

int Fade ;




void setup() {
 
  Serial.begin(9600);
  
  pinMode(redPin1, OUTPUT);
  pinMode(greenPin1, OUTPUT);
  pinMode(bluePin1, OUTPUT);
  pinMode(redPin2, OUTPUT);
  pinMode(greenPin2, OUTPUT);
  pinMode(bluePin2, OUTPUT);
}

void loop() {
  
  
  while(!Serial.available()) {}
  
  // serial read section
    readString = ""; 
    
  while (Serial.available())
  { 
    //delay(1);
    delayMicroseconds(900);
    
    if (Serial.available()>0)
    {
      c= Serial.read();
      readString += c;
      
    }
    
    if (readString.length()>0)
    { red1=0 ; green1=0 ; blue1=0 ;red2=0; green2=0;blue2=0;
      
      Serial.println(readString);
      if (readString == "R")
      {
        red1=255 ; green1=0 ; blue1=0 ; red2=255; green2=0; blue2=0;
        delay(20);
        readString = "";
      }
      if (readString == "B")
      {
        red1=0 ; green1=0 ; blue1=255 ;red2=0; green2=0;blue2=255;
        delay(20);
        readString = "";
      }
      if (readString == "G")
      {
        red1=0 ; green1=255 ; blue1=0 ;red2=0; green2=255;blue2=0;
        delay(20);
        readString = "";
      }
      
      else
      { 
        
        if (readString.length()  == 3)
       {
        Fade = readString.toInt();
        Fade = Fade ;
        
        if (Fade < 101)
        {
        
        red1=0 ; green1 = Fade*2.55 ; blue1 = 0 ;
        red2 = 0 ; green2 = Fade*2.55 ; blue2 = 0;
        delay(2);
        
        }
        
        if ( Fade > 100 )
        {
          if (Fade < 201)
          {
            red1=0 ; green1 = 255 ; blue1 = 255/100*Fade-255 ;
            red2 = 0 ; green2 = 255 ; blue2 = 255/100*Fade-255;
            delay(2);
            
          }
          if (Fade > 200)
          {
            if (Fade < 256)
            {
              red1= 255*Fade/55 +927; green1 = 255 ; blue1 = 255 ;
              red2 = 255*Fade/55 +927 ; green2 = 255 ; blue2 = 255;
              delay(2);
              
            }
          }
        }
        
        if ( Fade > 255)
        {
          red1=255 ; green1=0 ; blue1=0 ; red2=255; green2=0; blue2=0;
          delay(20);
        }
        
        
        
        Serial.println(Fade);
        readString = "";
        
        
      }
        
      if (readString.length() >= 4) 
      {
       readString = ""; 
      }
      }
    
  }
    
      
      red1 = 255-constrain(red1, 0, 255);
      green1 = 255-constrain(green1, 0,255);
      blue1 = 255-constrain(blue1, 0, 255);

      red2 = 255-constrain(red2, 0, 255);
      green2 = 255-constrain(green2, 0, 255);
      blue2 = 255-constrain(blue2, 0, 255);

      
      analogWrite(redPin1, red1);
      analogWrite(greenPin1, green1);
      analogWrite(bluePin1, blue1);
      analogWrite(redPin2, red2);
      analogWrite(greenPin2, green2);
      analogWrite(bluePin2, blue2);
 
  }
}










