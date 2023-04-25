// copy paste pins
const pin_t _WKP = WKP;
// const pin_t _DAC = A6;
const pin_t _A5 = A5;
const pin_t _A4 = A4;
const pin_t _A3 = A3;
const pin_t _A2 = A2;
const pin_t _A1 = A1;
const pin_t _A0 = A0;
const pin_t _D7 = D7;
const pin_t _D6 = D6;
const pin_t _D5 = D5;
const pin_t _D4 = D4;
const pin_t _D3 = D3;
const pin_t _D2 = D2;
const pin_t _D1 = D1;
const pin_t _D0 = D0;
int analogvalue;

// allows code to run before the cloud is connected.
SYSTEM_THREAD(ENABLED);

// This function is called when the Particle.function is called
int ledToggle(String command)
{
    if (command.equals("on"))
    {
        digitalWrite(_D7, HIGH);
        return 1;
    }
    else if (command.equals("off"))
    {
        digitalWrite(_D7, LOW);
        return 0;
    }
    else
    {
    // Unknown option
    return -1;
    }
}

int writeBitStream(String bits) {
    //write motor value bit by bit
    digitalWrite(_A5, bits.charAt(0) == '1');
    digitalWrite(_A4, bits.charAt(1) == '1');
    digitalWrite(_A3, bits.charAt(2) == '1');
    digitalWrite(_A2, bits.charAt(3) == '1');
    digitalWrite(_A1, bits.charAt(4) == '1');
    digitalWrite(_A0, bits.charAt(5) == '1');

    digitalWrite(_D5, bits.charAt(6) == '1');
    digitalWrite(_D4, bits.charAt(7) == '1');
    digitalWrite(_D3, bits.charAt(8) == '1');
    digitalWrite(_D2, bits.charAt(9) == '1');
    digitalWrite(_D1, bits.charAt(10) == '1');
    digitalWrite(_D0, bits.charAt(11) == '1');
    return 0;
}

int setMode(String mode) {
    if (mode.equals("color"))
    {
        digitalWrite(_D7, HIGH);
        return 1;
    }
    else if (mode.equals("joystick"))
    {
        digitalWrite(_D6, LOW);
        return 0;
    }
}

// The setup() method is called once when the device boots.
void setup()
{  
    //define pinmodes
    pinMode(_WKP, OUTPUT);
    pinMode(_A5, OUTPUT);
    pinMode(_A4, OUTPUT);
    pinMode(_A3, OUTPUT);
    pinMode(_A2, OUTPUT);
    pinMode(_A1, OUTPUT);
    pinMode(_A0, OUTPUT);

    pinMode(_D7, OUTPUT);
    pinMode(_D6, OUTPUT);
    pinMode(_D5, OUTPUT);
    pinMode(_D4, OUTPUT);
    pinMode(_D3, OUTPUT);
    pinMode(_D2, OUTPUT);
    pinMode(_D1, OUTPUT);
    pinMode(_D0, OUTPUT);

    //define functions
    Particle.function("writeMotor", writeBitStream);
    Particle.function("led", ledToggle);
    Particle.function("mode", setMode);
    Particle.variable("analogvalue", analogvalue);
}

void loop()
{
}
