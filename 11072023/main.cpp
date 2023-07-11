#include <Arduino.h>
#include <map>
#include <ESPmDNS.h>
const int ledPinG = PIN; // Replace with LED PIN
const int ledPinR = PIN; // Replace with LED PIN
const int Switch = PIN;  // Replace with Switch PIN


String text;
std::map<char, std::string> Morse;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(250000);
  Serial.println("Serial connection begun");
  Morse[' '] = " ";
  Morse['A'] = "._";
  Morse['B'] = "_...";
  Morse['C'] = "_._.";
  Morse['D'] = "_..";
  Morse['E'] = ".";
  Morse['F'] = ".._.";
  Morse['G'] = "__.";
  Morse['H'] = "....";
  Morse['I'] = "..";
  Morse['J'] = ".___";
  Morse['K'] = "_._";
  Morse['L'] = "._..";
  Morse['M'] = "__";
  Morse['N'] = "_.";
  Morse['O'] = "___";
  Morse['P'] = ".__.";
  Morse['Q'] = "__._";
  Morse['R'] = "._.";
  Morse['S'] = "...";
  Morse['T'] = "_";
  Morse['U'] = ".._";
  Morse['V'] = ".._";
  Morse['W'] = ".__";
  Morse['X'] = "_.._";
  Morse['Y'] = "_.__";
  Morse['Z'] = "__..";
  Morse['1'] = ".____";
  Morse['2'] = "..___";
  Morse['3'] = "...__";
  Morse['4'] = "...._";
  Morse['5'] = ".....";
  Morse['6'] = "_....";
  Morse['7'] = "__...";
  Morse['8'] = "___..";
  Morse['9'] = "____.";
  Morse['0'] = "_____";
  pinMode(ledPinG,OUTPUT);
  pinMode(ledPinR,OUTPUT);
  pinMode(Switch,INPUT);
}

void loop() {
  int switchState = digitalRead(Switch);
  if (switchState == LOW){
  Serial.println("Type the text below to convert text into Morse Code and hit ENTER.");
  text = Serial.readString();
  Serial.println(text);  
  for (int i = 0; i < text.length(); i++) {
    char character = toupper(text[i]);

    if (Morse.find(character) != Morse.end()) {
      std::string code = Morse[character];

      for (int j = 0; j < code.length(); j++) {
        if (code[j] == '.') {
          Serial.println(code[j]);
          digitalWrite(ledPinG, HIGH);
          delay(500);  // Blink duration for dots (shorter duration)
          digitalWrite(ledPinG, LOW);
          delay(500);  // Delay between dots and dashes
        } else if (code[j] == '_') {
          Serial.println(code[j]);
          digitalWrite(ledPinR, HIGH);
          delay(1500);  // Blink duration for dashes (longer duration)
          digitalWrite(ledPinR, LOW);
          delay(500);  // Delay between dots and dashes
        }
      }
      delay(1500);  // Delay between letters
    }
  }
  Serial.println("Reset by pressing the button again.");
  }
}
