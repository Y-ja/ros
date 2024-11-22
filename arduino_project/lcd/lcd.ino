#include <LiquidCrystal_I2C.h>
#include <Wire.h>

// Create LCD object (20x4 display with I2C address 0x27)
LiquidCrystal_I2C lcd(0x27, 20, 4);

void setup()
{
    lcd.init(); // Initialize the LCD
    lcd.backlight(); // Turn on the backlight
    lcd.setCursor(0, 0);
    lcd.print("Hello, world!");
    lcd.setCursor(0, 1);
    lcd.print("Ywrobot Arduino!");
    lcd.setCursor(0, 2);
    lcd.print("Arduino LCM IIC 2004");
    lcd.setCursor(0, 3);
    lcd.print("Power By Ec-yuan!");
    
    Serial.begin(119200); // Initialize Serial at baud rate 119200
}

void loop()
{
    static String buffer;
    if (Serial.available() > 0)
    {
        buffer = Serial.readStringUntil('\n'); // Read input from Serial until newline
        Serial.print(buffer.substring(0, 4)); // Print the first 4 characters (command)

        // Check the command prefix (lcd0, lcd1, lcd2, lcd3) and update the corresponding row
        if (buffer.substring(0, 4) == "lcd0")
        {
            lcd.setCursor(0, 0); // Set cursor to the first row
            lcd.print("                "); // Clear the row
            lcd.print(buffer.substring(4)); // Print the new text
        }
        else if (buffer.substring(0, 4) == "lcd1")
        {
            lcd.setCursor(0, 1); // Set cursor to the second row
            lcd.print("                "); // Clear the row
            lcd.print(buffer.substring(4)); // Print the new text
        }
        else if (buffer.substring(0, 4) == "lcd2")
        {
            lcd.setCursor(0, 2); // Set cursor to the third row
            lcd.print("                "); // Clear the row
            lcd.print(buffer.substring(4)); // Print the new text
        }
        else if (buffer.substring(0, 4) == "lcd3")
        {
            lcd.setCursor(0, 3); // Set cursor to the fourth row
            lcd.print("                "); // Clear the row
            lcd.print(buffer.substring(4)); // Print the new text
        }

        Serial.flush(); // Ensure all Serial data is transmitted
    }
}
