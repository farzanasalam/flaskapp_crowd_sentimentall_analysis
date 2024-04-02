// Define motor pins
const int motorPin1 = 9; // Motor driver input pin 1
const int motorPin2 = 10; // Motor driver input pin 2

void setup() {
  // Initialize motor pins as outputs
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);

  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    
    // Check the received character and control the motor accordingly
    switch(receivedChar) {
      case 'W': // Rotate the motor
        digitalWrite(motorPin1, HIGH);
        digitalWrite(motorPin2, LOW);
        break;
        
      case 'S': // Stop the motor
        digitalWrite(motorPin1, LOW);
        digitalWrite(motorPin2, LOW);
        break;
        
      default: // Stop the motor if unknown command received
        digitalWrite(motorPin1, LOW);
        digitalWrite(motorPin2, LOW);
        break;
    }
  }
}
