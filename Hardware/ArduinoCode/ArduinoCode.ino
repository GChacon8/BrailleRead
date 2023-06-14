#include <MatrizLed.h>

// Declare  a char array with one index for every possible ASCII byte / character
byte myBrailleDots[255];
int  firstOutputPin = 2; // pin corresponding to least significant bit
int buzzerPin  = 8; // Buzzer on pin 8
byte matrixPoints = 0; // byte that will store the point  matrix configuration
                       // for a specific ASCII character
byte  inByte;
byte mask = 1; //our bitmask

MatrizLed lc;

String message[10];

bool ledMap[8][8];
bool buzzerMap[6];

bool characterNeedsPrefix = true;

// Flag for numbers of two or more digits
bool lastCharacterWasNotNumber = true;

// Flag to avoid showing # when numbers prefix is buzzing
bool showableNumberSymbol = true;

// Last character readed ASCII code
byte lastCharacterReaded = 255;

// Constants
byte numericalPrefixByte = 35; // Numerical prefix is 010111
byte uppercasePrefixByte = 200; // Uppercase prefix is 010001
byte prefixByte1 = 201; // Prefix 1 is 000001
byte prefixByte2 = 202; // Prefix 2 is 000100
byte prefixByte3 = 203; // Prefix 3 is 010101
byte prefixByte4 = 204; // Prefix 4 is 010100

void setupAnimation(int stage){
  //Restarts ledMap
  for(int i=0; i<8; i++){
    for(int j=0; j<8; j++){
      ledMap[i][j]=false;
    }
  }

  switch(stage){
    case 1:
      ledMap[3][0] = true; ledMap[3][1] = true; ledMap[4][0] = true; ledMap[4][1] = true;
      displayCharacterOnScreenAux(ledMap);
    break;

    case 2:
      ledMap[3][0] = true; ledMap[3][1] = true; ledMap[4][0] = true; ledMap[4][1] = true; ledMap[3][3] = true; ledMap[3][4] = true; ledMap[4][3] = true; ledMap[4][4] = true;
      displayCharacterOnScreenAux(ledMap);
    break;

    case 3:
      ledMap[3][0] = true; ledMap[3][1] = true; ledMap[4][0] = true; ledMap[4][1] = true; ledMap[3][3] = true; ledMap[3][4] = true; ledMap[4][3] = true; ledMap[4][4] = true;
      ledMap[3][6] = true; ledMap[3][7] = true; ledMap[4][6] = true; ledMap[4][7] = true;
      displayCharacterOnScreenAux(ledMap);
    break;

    case 4:
      //ledMap[1][2] = true; ledMap[1][5] = true; ledMap[1][3] = true; ledMap[1][4] = true; ledMap[2][2] = true; ledMap[2][5] = true; ledMap[5][1] = true; ledMap[5][6] = true;
      //ledMap[6][1] = true; ledMap[6][2] = true; ledMap[6][5] = true; ledMap[6][6] = true;

      ledMap[2][2] = true; ledMap[3][1] = true; ledMap[3][3] = true; ledMap[4][4] = true; ledMap[5][5] = true; ledMap[6][6] = true;
      displayCharacterOnScreenAux(ledMap);
    break;
  }
}

void setup() {
  lc.begin(11,13,10,1);   
  lc.setIntensidad(10);
  lc.clearDisplay(0);

  // Sets the whole ledMap to false
  for(int i=0; i<8; i++){
    for(int j=0; j<8; j++){
      ledMap[i][j]=false;
    }
  }

  // Sets the whole buzzermap to false
  for(int i=0; i<6; i++){
    buzzerMap[i]=false;
  }

  // Temporarily  assign 99 to every possible ASCII byte/character
  // All the characters in the  input string will decode to "99" by default
  for (int i = 0; i < 256; i =  i + 1) {
     myBrailleDots[i] = 99;
  }

  // Now, only for the ASCII  characters with a corresponding Braille character.
  // assign the corresponding  Braille Dot configuration
  myBrailleDots[32] = 0;  // blank is 000000
  myBrailleDots[33]  = 14;  // ! is 001110
  myBrailleDots[34] = 11;  // " is 001011
  myBrailleDots[35] = 23; // # is 010111
  myBrailleDots[36] = 26; // $ is 011010
  myBrailleDots[37] = 7; // % is 000111
  myBrailleDots[38] = 59; // & is 111011
  myBrailleDots[39] = 11; // ' is 001011
  myBrailleDots[40]  = 41;  // ( is 101001
  myBrailleDots[41] = 22;  // ) is 010110
  myBrailleDots[42] = 9; // * is 001001
  myBrailleDots[43] = 14; // + is 001110
  myBrailleDots[44] = 8;  // , is 001000
  myBrailleDots[45] = 3; // - is 000011
  myBrailleDots[46]  = 2;  // . is 000010
  myBrailleDots[47] = 8; // / is 001000
  myBrailleDots[48] = 28; // 0 is 011100
  myBrailleDots[49]  = 32; // 1 is 100000
  myBrailleDots[50] = 40; // 2 is 101000
  myBrailleDots[51]  = 48; // 3 is 110000
  myBrailleDots[52] = 52; // 4 is 110100
  myBrailleDots[53]  = 36; // 5 is 100100
  myBrailleDots[54] = 56; // 6 is 111000
  myBrailleDots[55]  = 60; // 7 is 111100
  myBrailleDots[56] = 44; // 8 is 101100
  myBrailleDots[57]  = 24; // 9 is 011000
  myBrailleDots[58] = 12; // : is 001100
  myBrailleDots[59]  = 10; // ; is 001010
  myBrailleDots[60] = 34; // < is 100010
  myBrailleDots[61] = 15 ;// = is 001111
  myBrailleDots[62] = 8; // > is 001000
  myBrailleDots[63] = 9; // ? is 001001
  myBrailleDots[64] = 4 ;// @ is 000100
  myBrailleDots[65] = 32; // A is 100000
  myBrailleDots[66] = 40; // B is 101000
  myBrailleDots[67] = 48; // C is 110000
  myBrailleDots[68] = 52; // D is 110100
  myBrailleDots[69] = 36; // E is 100100
  myBrailleDots[70] = 56; // F is 111000
  myBrailleDots[71] = 60; // G is 111100
  myBrailleDots[72] = 44; // H is 101100
  myBrailleDots[73] = 24; // I is 011000
  myBrailleDots[74] = 28; // J is 011100
  myBrailleDots[75] = 34; // K is 100010
  myBrailleDots[76] = 42; // L is 101010
  myBrailleDots[77] = 50; // M is 110010
  myBrailleDots[78] = 54; // N is 110110
  myBrailleDots[79] = 38; // O is 100110
  myBrailleDots[80] = 58; // P is 111010
  myBrailleDots[81] = 62; // Q is 111110
  myBrailleDots[82] = 46; // R is 101110
  myBrailleDots[83] = 26; // S is 011010
  myBrailleDots[84] = 30; // T is 011110
  myBrailleDots[85] = 35; // U is 100011
  myBrailleDots[86] = 43; // V is 101011
  myBrailleDots[87] = 29; // W is 011101
  myBrailleDots[88] = 51; // X is 110011
  myBrailleDots[89] = 55; // Y is 110111
  myBrailleDots[90] = 39; // Z is 100111
  myBrailleDots[91] = 47; // [ is 101111
  myBrailleDots[93] = 31; // ] is 011111 
  myBrailleDots[96] = 2;  // ´ is 000010
  myBrailleDots[97] = 32; // a is 100000
  myBrailleDots[98] = 40; // b is 101000
  myBrailleDots[99] = 48; // c is 110000
  myBrailleDots[100] = 52; // d is 110100
  myBrailleDots[101] = 36; // e is 100100
  myBrailleDots[102] = 56; // f is  111000
  myBrailleDots[103] = 60; // g is 111100
  myBrailleDots[104] = 44;  // h is 101100
  myBrailleDots[105] = 24; // i is 011000
  myBrailleDots[106]  = 28; // j is 011100
  myBrailleDots[107] = 34; // k is 100010
  myBrailleDots[108]  = 42; // l is 101010
  myBrailleDots[109] = 50; // m is 110010
  myBrailleDots[110]  = 54; // n is 110110
  myBrailleDots[111] = 38; // o is 100110
  myBrailleDots[112]  = 58; // p is 111010
  myBrailleDots[113] = 62; // q is 111110
  myBrailleDots[114]  = 46; // r is 101110
  myBrailleDots[115] = 26; // s is 011010
  myBrailleDots[116]  = 30; // t is 011110
  myBrailleDots[117] = 35; // u is 100011
  myBrailleDots[118]  = 43; // v is 101011
  myBrailleDots[119] = 29; // w is 011101
  myBrailleDots[120]  = 51; // x is 110011
  myBrailleDots[121] = 55; // y is 110111
  myBrailleDots[122]  = 39; // z is 100111
  myBrailleDots[123] = 42; // { is 101010
  myBrailleDots[125] = 8; // } is 001000
  myBrailleDots[128] = 59; // Catalunya C is 111011
  myBrailleDots[129] = 45; // Dier. u is 101101
  myBrailleDots[130] = 63; // é is 111111
  myBrailleDots[135] = 59; // Catalunya c is 111011
  myBrailleDots[144] = 63; // É is 111111
  myBrailleDots[156] = 27; // Pound is 011011
  myBrailleDots[154] = 45; // Dier. U is 101101
  myBrailleDots[158] = 11; // x is 001011
  myBrailleDots[160] = 47; // á is 101111
  myBrailleDots[161] = 18; // í is 010010
  myBrailleDots[162] = 25; // ó is 011001
  myBrailleDots[163] = 31; // ú is 011111
  myBrailleDots[164] = 61; // ñ is 111101
  myBrailleDots[165] = 61; // Ñ is 111101
  myBrailleDots[181] = 47; // Á is 101111
  myBrailleDots[189] = 48; // cent is 110000
  myBrailleDots[190] = 55; // Yen is 110111
  myBrailleDots[214] = 18; // Í is 010010
  myBrailleDots[224] = 25; // Ó is 011001
  myBrailleDots[233] = 31; // Ú is 011111

  // Special characters
  myBrailleDots[200] = 17; // Uppercase prefix is 010001
  myBrailleDots[201] = 1; // Prefix 1 is 000001
  myBrailleDots[202] = 4; // Prefix 2 is 000100
  myBrailleDots[203] = 21; // Prefix 3 is 010101
  myBrailleDots[204] = 20; // Prefix 4 is 010100

  // Null ASCII Bindings
  myBrailleDots[195] = 0;
  myBrailleDots[194] = 0;

  pinMode(buzzerPin, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6,  OUTPUT);
  pinMode(7, OUTPUT);

  Serial.begin(9600);
  
  // Buzzer test to check integrity of hardware

  // 1. All of them
  setupAnimation(1);

  digitalWrite(2,HIGH);
  digitalWrite(3,HIGH);
  digitalWrite(4,HIGH);
  digitalWrite(5,HIGH);
  digitalWrite(6,HIGH);
  digitalWrite(7,HIGH);

  delay(1000);

  setupAnimation(2);

  digitalWrite(2,LOW);
  digitalWrite(3,LOW);
  digitalWrite(4,LOW);
  digitalWrite(5,LOW);
  digitalWrite(6,LOW);
  digitalWrite(7,LOW);

  delay(250);

  setupAnimation(3);

  delay(250);

  lc.clearDisplay(0);

  // 2. One by one
  for (int i = 7; i>=2; i--){
    digitalWrite(i,HIGH);

    delay(250);

    digitalWrite(i,LOW);

    delay(250);

    if (i == 7 || i ==6){
      setupAnimation(1);
    } else if (i == 5 || i == 4){
      setupAnimation(2);
    } else {
      setupAnimation(3);
    }
  }

  lc.clearDisplay(0);

  delay(250);

  setupAnimation(1);

  // 3. Buzzing rush
  for (int i = 0; i<3; i++){
    digitalWrite(2,HIGH);
    digitalWrite(3,HIGH);
    digitalWrite(4,HIGH);
    digitalWrite(5,HIGH);
    digitalWrite(6,HIGH);
    digitalWrite(7,HIGH);

    delay(250);

    digitalWrite(2,LOW);
    digitalWrite(3,LOW);
    digitalWrite(4,LOW);
    digitalWrite(5,LOW);
    digitalWrite(6,LOW);
    digitalWrite(7,LOW);

    delay(250);

    setupAnimation(i+1);
  }

  delay(250);

  lc.clearDisplay(0);

  setupAnimation(4);

  delay(2000);

  lc.clearDisplay(0);
}

void notTranslatableCharacteranimation(){
  //Restarts ledMap
  for(int i=0; i<8; i++){
    for(int j=0; j<8; j++){
      ledMap[i][j]=false;
    }
  }

  ledMap[1][2] = true; ledMap[1][5] = true; ledMap[2][2] = true; ledMap[2][3] = true; ledMap[2][4] = true; ledMap[2][5] = true; ledMap[5][1] = true; ledMap[5][2] = true; 
  ledMap[5][5] = true; ledMap[5][6] = true; ledMap[6][2] = true; ledMap[6][5] = true;

  displayCharacterOnScreenAux(ledMap);
}

void displayCharacterOnScreenAux(bool ledMap[8][8]){
  for(int i=0; i<8; i++){
    for(int j=0; j<8; j++){
      if(ledMap[i][j]){
        lc.setLed(0, j, i, true);
      }
    }
  }
}

void displayCharacterOnScreen(byte characterByte){
  //Restarts ledMap
  for(int i=0; i<8; i++){
    for(int j=0; j<8; j++){
      ledMap[i][j]=false;
    }
  }

  switch(characterByte){
    case 33: // ! Character
      ledMap[0][3] = true; ledMap[0][4] = true; ledMap[1][3] = true; ledMap[1][4] = true; ledMap[3][3] = true; ledMap[3][4] = true; ledMap[4][3] = true;
      ledMap[4][4] = true; ledMap[5][3] = true; ledMap[5][4] = true; ledMap[6][3] = true; ledMap[6][4] = true; ledMap[7][3] = true; ledMap[7][4] = true; 
      break;

    case 34: // " Character
      ledMap[2][2] = true; ledMap[2][3] = true; ledMap[3][2] = true; ledMap[3][3] = true; ledMap[4][1] = true; ledMap[4][2] = true; ledMap[5][1] = true; ledMap[5][2] = true;
      ledMap[2][5] = true; ledMap[2][6] = true; ledMap[3][5] = true; ledMap[3][6] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[5][4] = true; ledMap[5][5] = true;
      break;

    case 35: // # Character
      ledMap[0][1] = true; ledMap[0][2] = true; ledMap[0][5] = true; ledMap[0][6] = true; ledMap[1][0] = true; ledMap[1][1] = true; ledMap[1][2] = true; ledMap[1][3] = true;
      ledMap[1][4] = true; ledMap[1][5] = true; ledMap[1][6] = true; ledMap[1][7] = true; ledMap[2][0] = true; ledMap[2][1] = true; ledMap[2][2] = true; ledMap[2][3] = true;
      ledMap[2][4] = true; ledMap[2][5] = true; ledMap[2][6] = true; ledMap[2][7] = true; ledMap[3][1] = true; ledMap[3][2] = true; ledMap[3][5] = true; ledMap[3][6] = true;
      ledMap[4][1] = true; ledMap[4][2] = true; ledMap[4][5] = true; ledMap[4][6] = true; ledMap[5][0] = true; ledMap[5][1] = true; ledMap[5][2] = true; ledMap[5][3] = true;
      ledMap[5][4] = true; ledMap[5][5] = true; ledMap[5][6] = true; ledMap[5][7] = true; ledMap[6][0] = true; ledMap[6][1] = true; ledMap[6][2] = true; ledMap[6][3] = true;
      ledMap[6][4] = true; ledMap[6][5] = true; ledMap[6][6] = true; ledMap[6][7] = true; ledMap[7][1] = true; ledMap[7][2] = true; ledMap[7][5] = true; ledMap[7][6] = true;
      break;

    case 36: // $ Character
      ledMap[0][4] = true; ledMap[1][2] = true; ledMap[1][3] = true; ledMap[1][4] = true; ledMap[1][5] = true; ledMap[1][6] = true; ledMap[2][1] = true; ledMap[2][4] = true;
      ledMap[2][6] = true; ledMap[2][7] = true; ledMap[3][4] = true; ledMap[3][6] = true; ledMap[3][7] = true; ledMap[4][1] = true; ledMap[4][2] = true; ledMap[4][3] = true;
      ledMap[4][4] = true; ledMap[4][5] = true; ledMap[4][6] = true; ledMap[5][1] = true; ledMap[5][2] = true; ledMap[5][4] = true; ledMap[5][7] = true; ledMap[6][2] = true;
      ledMap[6][3] = true; ledMap[6][4] = true; ledMap[6][5] = true; ledMap[6][6] = true; ledMap[7][4] = true;
    break;

    case 37: // % Character
      ledMap[1][1] = true; ledMap[1][2] = true; ledMap[1][5] = true; ledMap[1][6] = true; ledMap[2][1] = true; ledMap[2][2] = true; ledMap[2][3] = true; ledMap[2][5] = true;
      ledMap[2][6] = true; ledMap[3][2] = true; ledMap[3][3] = true; ledMap[3][4] = true; ledMap[4][3] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[5][1] = true;
      ledMap[5][2] = true; ledMap[5][4] = true; ledMap[5][5] = true; ledMap[5][6] = true; ledMap[6][1] = true; ledMap[6][2] = true; ledMap[6][5] = true; ledMap[6][6] = true;
    break;

    case 38: // & Character
      ledMap[0][1] = true; ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][6] = true; ledMap[0][7] = true; ledMap[1][0] = true; ledMap[1][1] = true;
      ledMap[1][2] = true; ledMap[1][4] = true; ledMap[1][5] = true; ledMap[2][0] = true; ledMap[2][1] = true; ledMap[2][4] = true; ledMap[2][5] = true; ledMap[2][6] = true;
      ledMap[3][0] = true; ledMap[3][1] = true; ledMap[3][3] = true; ledMap[3][4] = true; ledMap[3][6] = true; ledMap[3][7] = true; ledMap[4][1] = true; ledMap[4][2] = true;
      ledMap[4][3] = true; ledMap[5][1] = true; ledMap[5][2] = true; ledMap[5][4] = true; ledMap[6][1] = true; ledMap[6][2] = true; ledMap[6][4] = true; ledMap[6][5] = true;
      ledMap[7][2] = true; ledMap[7][3] = true; ledMap[7][4] = true;
    break;

    case 39: // ' Character
      ledMap[2][4] = true; ledMap[2][5] = true; ledMap[3][4] = true; ledMap[3][5] = true; ledMap[4][3] = true; ledMap[4][4] = true; ledMap[5][3] = true; ledMap[5][4] = true;
    break;

    case 40: // ( Character
      ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[1][2] = true; ledMap[1][3] = true; ledMap[1][4] = true; ledMap[2][2] = true; ledMap[2][3] = true; 
      ledMap[3][2] = true; ledMap[3][3] = true; ledMap[4][2] = true; ledMap[4][3] = true; ledMap[5][2] = true; ledMap[5][3] = true; ledMap[6][2] = true; ledMap[6][3] = true; 
      ledMap[6][4] = true; ledMap[7][3] = true; ledMap[7][4] = true; ledMap[7][5] = true;
      break;

    case 41: // ) Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[1][3] = true; ledMap[1][4] = true; ledMap[1][5] = true; ledMap[2][4] = true; ledMap[2][5] = true; 
      ledMap[3][4] = true; ledMap[3][5] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[5][4] = true; ledMap[5][5] = true; ledMap[6][3] = true; ledMap[6][4] = true; 
      ledMap[6][5] = true; ledMap[7][2] = true; ledMap[7][3] = true; ledMap[7][4] = true;
      break;

    case 42: // * Character
      ledMap[1][4] = true; ledMap[2][2] = true; ledMap[2][4] = true; ledMap[2][6] = true; ledMap[3][3] = true; ledMap[3][4] = true; ledMap[3][5] = true; ledMap[4][1] = true;
      ledMap[4][2] = true; ledMap[4][3] = true; ledMap[4][5] = true; ledMap[4][6] = true; ledMap[4][7] = true; ledMap[5][3] = true; ledMap[5][4] = true; ledMap[5][5] = true;
      ledMap[6][2] = true; ledMap[6][4] = true; ledMap[6][6] = true; ledMap[7][4] = true;
    break;

    case 43: // + Character
      ledMap[1][3] = true; ledMap[1][4] = true; ledMap[2][3] = true; ledMap[2][4] = true; ledMap[3][1] = true; ledMap[3][2] = true; ledMap[3][3] = true; ledMap[3][4] = true;
      ledMap[3][5] = true; ledMap[3][6] = true; ledMap[4][1] = true; ledMap[4][2] = true; ledMap[4][3] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[4][6] = true;
      ledMap[5][3] = true; ledMap[5][4] = true; ledMap[6][3] = true; ledMap[6][4] = true;
    break;
    
    case 44: // , Character
      ledMap[2][3] = true; ledMap[3][4] = true; ledMap[4][3] = true; ledMap[4][4] = true; ledMap[5][3] = true; ledMap[5][4] = true; 
      break;

    case 45: // - Character
      ledMap[3][2] = true; ledMap[3][3] = true; ledMap[3][4] = true; ledMap[3][5] = true; ledMap[4][2] = true; ledMap[4][3] = true; ledMap[4][4] = true; ledMap[4][5] = true;
    break;

    case 46: // . Character
      ledMap[3][3] = true; ledMap[3][4] = true; ledMap[4][3] = true; ledMap[4][4] = true; 
      break;

    case 47: // / Character
      ledMap[1][1] = true; ledMap[1][2] = true; ledMap[2][1] = true; ledMap[2][2] = true; ledMap[2][3] = true; ledMap[3][2] = true; ledMap[3][3] = true; ledMap[3][4] = true;
      ledMap[4][3] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[5][4] = true; ledMap[5][5] = true; ledMap[5][6] = true; ledMap[6][5] = true; ledMap[6][6] = true;
    break;

    case 58: // : Character
      ledMap[1][3] = true; ledMap[1][4] = true; ledMap[2][3] = true; ledMap[2][4] = true;
      ledMap[5][3] = true; ledMap[5][4] = true; ledMap[6][3] = true; ledMap[6][4] = true;
      break;

    case 59: // ; Character
      ledMap[0][4] = true; ledMap[1][3] = true; ledMap[1][4] = true; ledMap[2][3] = true; ledMap[2][4] = true;
      ledMap[5][3] = true; ledMap[5][4] = true; ledMap[6][3] = true; ledMap[6][4] = true;
      break;

    case 60: // < Character
      ledMap[0][5] = true; ledMap[0][6] = true; ledMap[1][4] = true; ledMap[1][5] = true; ledMap[2][3] = true; ledMap[2][4] = true; ledMap[3][2] = true; ledMap[3][3] = true;
      ledMap[4][2] = true; ledMap[4][3] = true; ledMap[5][3] = true; ledMap[5][4] = true; ledMap[6][4] = true; ledMap[6][5] = true; ledMap[7][5] = true; ledMap[7][6] = true;
    break;

    case 61: // = Character
      ledMap[1][1] = true; ledMap[1][2] = true; ledMap[1][3] = true; ledMap[1][4] = true; ledMap[1][5] = true; ledMap[1][6] = true; ledMap[2][1] = true; ledMap[2][2] = true;
      ledMap[2][3] = true; ledMap[2][4] = true; ledMap[2][5] = true; ledMap[2][6] = true; ledMap[5][1] = true; ledMap[5][2] = true; ledMap[5][3] = true; ledMap[5][4] = true;
      ledMap[5][5] = true; ledMap[5][6] = true; ledMap[6][1] = true; ledMap[6][2] = true; ledMap[6][3] = true; ledMap[6][4] = true; ledMap[6][5] = true; ledMap[6][6] = true;
    break;

    case 62: // > Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[1][3] = true; ledMap[1][4] = true; ledMap[2][4] = true; ledMap[2][5] = true; ledMap[3][5] = true; ledMap[3][6] = true;
      ledMap[4][5] = true; ledMap[4][6] = true; ledMap[5][4] = true; ledMap[5][5] = true; ledMap[6][3] = true; ledMap[6][4] = true; ledMap[7][2] = true; ledMap[7][3] = true;
    break;

    case 63: // ? Character
      ledMap[0][3] = true; ledMap[0][4] = true; ledMap[2][3] = true; ledMap[2][4] = true; ledMap[3][3] = true; ledMap[3][4] = true; ledMap[4][4] = true; ledMap[4][5] = true;
      ledMap[4][6] = true; ledMap[5][1] = true; ledMap[5][2] = true; ledMap[5][5] = true; ledMap[5][6] = true; ledMap[6][1] = true; ledMap[6][2] = true; ledMap[6][3] = true; 
      ledMap[6][4] = true; ledMap[6][5] = true; ledMap[6][6] = true; ledMap[7][2] = true; ledMap[7][3] = true; ledMap[7][4] = true; ledMap[7][5] = true; 
      break;

    case 64: // @ Character
      ledMap[0][0] = true; ledMap[0][1] = true; ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[0][6] = true; ledMap[1][0] = true;
      ledMap[1][7] = true; ledMap[2][0] = true; ledMap[2][2] = true; ledMap[2][3] = true; ledMap[2][4] = true; ledMap[3][0] = true; ledMap[3][2] = true; ledMap[3][5] = true;
      ledMap[3][6] = true; ledMap[3][7] = true; ledMap[4][0] = true; ledMap[4][2] = true; ledMap[4][5] = true; ledMap[4][7] = true; ledMap[5][0] = true; ledMap[5][2] = true;
      ledMap[5][3] = true; ledMap[5][4] = true; ledMap[5][5] = true; ledMap[5][7] = true; ledMap[6][0] = true; ledMap[6][7] = true; ledMap[7][0] = true; ledMap[7][1] = true;
      ledMap[7][2] = true; ledMap[7][3] = true; ledMap[7][4] = true; ledMap[7][5] = true; ledMap[7][6] = true; ledMap[7][7] = true;
    break;

    case 91: // [ Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[1][2] = true; ledMap[1][3] = true; ledMap[2][2] = true; ledMap[2][3] = true;
      ledMap[3][2] = true; ledMap[3][3] = true; ledMap[4][2] = true; ledMap[4][3] = true; ledMap[5][2] = true; ledMap[5][3] = true; ledMap[6][2] = true; ledMap[6][3] = true;
      ledMap[7][2] = true; ledMap[7][3] = true; ledMap[7][4] = true; ledMap[7][5] = true;
    break;

    case 93: // ] Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[1][4] = true; ledMap[1][5] = true; ledMap[2][4] = true; ledMap[2][5] = true;
      ledMap[3][4] = true; ledMap[3][5] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[5][4] = true; ledMap[5][5] = true; ledMap[6][4] = true; ledMap[6][5] = true;
      ledMap[7][2] = true; ledMap[7][3] = true; ledMap[7][4] = true; ledMap[7][5] = true;
    break;

    case 96: // ` Character
      ledMap[3][4] = true; ledMap[4][4] = true; ledMap[5][3] = true;
    break;
    
    case 123: // { Character
      ledMap[1][4] = true; ledMap[1][5] = true; ledMap[2][3] = true; ledMap[2][4] = true; ledMap[3][3] = true; ledMap[4][2] = true; ledMap[4][3] = true; ledMap[5][3] = true;
      ledMap[6][3] = true; ledMap[6][4] = true; ledMap[7][4] = true; ledMap[7][5] = true;
    break;

    case 125: // } Character
      ledMap[1][2] = true; ledMap[1][3] = true; ledMap[2][3] = true; ledMap[2][4] = true; ledMap[3][4] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[5][4] = true;
      ledMap[6][3] = true; ledMap[6][4] = true; ledMap[7][2] = true; ledMap[7][3] = true;
    break;

    case 128: // Catalunya C Character
      ledMap[0][3] = true; ledMap[0][4] = true; ledMap[1][4] = true; ledMap[2][2] = true; ledMap[2][3] = true; ledMap[2][4] = true; ledMap[2][5] = true; ledMap[3][1] = true;
      ledMap[3][2] = true; ledMap[3][5] = true; ledMap[3][6] = true; ledMap[4][1] = true; ledMap[4][2] = true; ledMap[5][1] = true; ledMap[5][2] = true; ledMap[6][1] = true;
      ledMap[6][2] = true; ledMap[6][5] = true; ledMap[6][6] = true; ledMap[7][2] = true; ledMap[7][3] = true; ledMap[7][4] = true; ledMap[7][5] = true;
    break;

    case 129: // Dier. u Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[0][6] = true; ledMap[1][1] = true; ledMap[1][2] = true; ledMap[1][5] = true;
      ledMap[1][6] = true; ledMap[2][1] = true; ledMap[2][2] = true; ledMap[2][5] = true; ledMap[2][6] = true; ledMap[3][1] = true; ledMap[3][2] = true; ledMap[3][5] = true; 
      ledMap[3][6] = true; ledMap[4][1] = true; ledMap[4][2] = true; ledMap[4][5] = true; ledMap[4][6] = true; ledMap[6][2] = true; ledMap[6][5] = true;
    break;

    case 130: // é Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[1][1] = true; ledMap[1][2] = true; ledMap[2][1] = true; ledMap[2][2] = true;
      ledMap[2][3] = true; ledMap[2][4] = true; ledMap[2][5] = true; ledMap[2][6] = true; ledMap[3][1] = true; ledMap[3][2] = true; ledMap[3][5] = true; ledMap[3][6] = true;
      ledMap[4][2] = true; ledMap[4][3] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[6][3] = true; ledMap[6][4] = true; ledMap[7][4] = true; ledMap[7][5] = true;
    break;

    case 135: // Catalunya c Character
      ledMap[0][3] = true; ledMap[0][4] = true; ledMap[1][4] = true; ledMap[2][2] = true; ledMap[2][3] = true; ledMap[2][4] = true; ledMap[2][5] = true; ledMap[3][1] = true;
      ledMap[3][2] = true; ledMap[3][5] = true; ledMap[3][6] = true; ledMap[4][1] = true; ledMap[4][2] = true; ledMap[5][1] = true; ledMap[5][2] = true; ledMap[5][5] = true; 
      ledMap[5][6] = true; ledMap[6][2] = true; ledMap[6][3] = true; ledMap[6][4] = true; ledMap[6][5] = true;
    break;

    case 144: // É Character
      ledMap[0][1] = true; ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[0][6] = true; ledMap[1][1] = true; ledMap[1][2] = true;
      ledMap[2][1] = true; ledMap[2][2] = true; ledMap[2][3] = true; ledMap[2][4] = true; ledMap[2][5] = true; ledMap[3][1] = true; ledMap[3][2] = true; ledMap[4][1] = true;
      ledMap[4][2] = true; ledMap[4][3] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[4][6] = true; ledMap[6][3] = true; ledMap[6][4] = true; ledMap[7][4] = true;
      ledMap[7][5] = true;
    break;

    case 156: // Pound Character
      ledMap[0][1] = true; ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[0][6] = true; ledMap[1][2] = true; ledMap[1][3] = true;
      ledMap[2][2] = true; ledMap[2][3] = true; ledMap[3][1] = true; ledMap[3][2] = true; ledMap[3][3] = true; ledMap[3][4] = true; ledMap[4][2] = true; ledMap[4][3] = true;
      ledMap[5][2] = true; ledMap[5][3] = true; ledMap[5][6] = true; ledMap[6][2] = true; ledMap[6][3] = true; ledMap[6][5] = true; ledMap[6][6] = true; ledMap[7][3] = true;
      ledMap[7][4] = true; ledMap[7][5] = true;
    break;

    case 154: // Dier. U Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[0][6] = true; ledMap[1][1] = true; ledMap[1][2] = true; ledMap[1][5] = true;
      ledMap[1][6] = true; ledMap[2][1] = true; ledMap[2][2] = true; ledMap[2][5] = true; ledMap[2][6] = true; ledMap[3][1] = true; ledMap[3][2] = true; ledMap[3][5] = true; 
      ledMap[3][6] = true; ledMap[4][1] = true; ledMap[4][2] = true; ledMap[4][5] = true; ledMap[4][6] = true; ledMap[5][1] = true; ledMap[5][2] = true; ledMap[5][5] = true;
      ledMap[5][6] = true; ledMap[7][2] = true; ledMap[7][5] = true;
    break;

    case 160: // á Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[0][6] = true; ledMap[1][1] = true; ledMap[1][2] = true; ledMap[1][5] = true;
      ledMap[1][6] = true; ledMap[2][2] = true; ledMap[2][3] = true; ledMap[2][4] = true; ledMap[2][5] = true; ledMap[2][6] = true; ledMap[3][5] = true; ledMap[3][6] = true;
      ledMap[4][2] = true; ledMap[4][3] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[6][3] = true; ledMap[6][4] = true; ledMap[7][4] = true; ledMap[7][5] = true;
    break;

    case 161: // í Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[1][3] = true; ledMap[1][4] = true; ledMap[2][3] = true; ledMap[2][4] = true;
      ledMap[3][3] = true; ledMap[3][4] = true; ledMap[5][3] = true; ledMap[5][4] = true; ledMap[6][4] = true; ledMap[6][5] = true;
    break;

    case 162: // ó Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[1][1] = true; ledMap[1][2] = true; ledMap[1][5] = true; ledMap[1][6] = true;
      ledMap[2][1] = true; ledMap[2][2] = true; ledMap[2][5] = true; ledMap[2][6] = true; ledMap[3][2] = true; ledMap[3][3] = true; ledMap[3][4] = true; ledMap[3][5] = true;
      ledMap[5][3] = true; ledMap[5][4] = true; ledMap[6][4] = true; ledMap[6][5] = true;
    break;

    case 163: // ú Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[0][6] = true; ledMap[1][1] = true; ledMap[1][2] = true; ledMap[1][5] = true;
      ledMap[1][6] = true; ledMap[2][1] = true; ledMap[2][2] = true; ledMap[2][5] = true; ledMap[2][6] = true; ledMap[3][1] = true; ledMap[3][2] = true; ledMap[3][5] = true; 
      ledMap[3][6] = true; ledMap[5][3] = true; ledMap[5][4] = true; ledMap[6][4] = true; ledMap[6][5] = true;
    break;

    case 164: // ñ Character
      ledMap[0][1] = true; ledMap[0][2] = true; ledMap[0][5] = true; ledMap[0][6] = true; ledMap[1][1] = true; ledMap[1][2] = true; ledMap[1][5] = true; ledMap[1][6] = true;
      ledMap[2][1] = true; ledMap[2][2] = true; ledMap[2][5] = true; ledMap[2][6] = true; ledMap[3][1] = true; ledMap[3][2] = true; ledMap[3][3] = true; ledMap[3][4] = true;
      ledMap[3][5] = true; ledMap[3][6] = true; ledMap[4][1] = true; ledMap[4][2] = true; ledMap[4][3] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[6][2] = true;
      ledMap[6][3] = true; ledMap[6][4] = true; ledMap[6][5] = true;
    break;

    case 165: // Ñ Character
      ledMap[0][1] = true; ledMap[0][2] = true; ledMap[0][6] = true; ledMap[0][7] = true; ledMap[1][1] = true; ledMap[1][2] = true; ledMap[1][5] = true; ledMap[1][6] = true;
      ledMap[1][7] = true; ledMap[2][1] = true; ledMap[2][2] = true; ledMap[2][4] = true; ledMap[2][5] = true; ledMap[2][6] = true; ledMap[2][7] = true; ledMap[3][1] = true;
      ledMap[3][2] = true; ledMap[3][3] = true; ledMap[3][4] = true; ledMap[3][6] = true; ledMap[3][7] = true; ledMap[4][1] = true; ledMap[4][2] = true; ledMap[4][3] = true;
      ledMap[4][6] = true; ledMap[4][7] = true; ledMap[5][1] = true; ledMap[5][2] = true; ledMap[5][6] = true; ledMap[5][7] = true; ledMap[7][2] = true; ledMap[7][3] = true;
      ledMap[7][4] = true; ledMap[7][5] = true; ledMap[7][6] = true;
    break;

    case 181: // Á Character
      ledMap[0][1] = true; ledMap[0][2] = true; ledMap[0][5] = true; ledMap[0][6] = true; ledMap[1][1] = true; ledMap[1][2] = true; ledMap[1][5] = true; ledMap[1][6] = true;
      ledMap[2][1] = true; ledMap[2][2] = true; ledMap[2][3] = true; ledMap[2][4] = true; ledMap[2][5] = true; ledMap[2][6] = true; ledMap[3][1] = true; ledMap[3][2] = true;
      ledMap[3][5] = true; ledMap[3][6] = true; ledMap[4][2] = true; ledMap[4][3] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[6][3] = true; ledMap[6][4] = true;
      ledMap[7][4] = true; ledMap[7][5] = true;
    break;

    case 189: // Cent Character
      ledMap[0][4] = true; ledMap[1][2] = true; ledMap[1][3] = true; ledMap[1][4] = true; ledMap[1][5] = true; ledMap[1][6] = true; ledMap[2][1] = true; ledMap[2][2] = true;
      ledMap[2][4] = true; ledMap[2][6] = true; ledMap[2][7] = true; ledMap[3][1] = true; ledMap[3][2] = true; ledMap[3][4] = true; ledMap[4][1] = true; ledMap[4][2] = true;
      ledMap[4][4] = true; ledMap[5][1] = true; ledMap[5][2] = true; ledMap[5][4] = true; ledMap[5][6] = true; ledMap[5][7] = true; ledMap[6][2] = true; ledMap[6][3] = true; 
      ledMap[6][4] = true; ledMap[6][5] = true; ledMap[6][6] = true; ledMap[7][4] = true;
    break;

    case 190: // Yen Character
      ledMap[0][3] = true; ledMap[0][4] = true; ledMap[1][2] = true; ledMap[1][3] = true; ledMap[1][4] = true; ledMap[1][5] = true; ledMap[2][3] = true; ledMap[2][4] = true;
      ledMap[3][1] = true; ledMap[3][2] = true; ledMap[3][3] = true; ledMap[3][4] = true; ledMap[3][5] = true; ledMap[3][6] = true; ledMap[4][1] = true; ledMap[4][2] = true;
      ledMap[4][5] = true; ledMap[4][6] = true; ledMap[5][1] = true; ledMap[5][2] = true; ledMap[5][5] = true; ledMap[5][6] = true; ledMap[6][1] = true; ledMap[6][2] = true;
      ledMap[6][5] = true; ledMap[6][6] = true;
    break;

    case 214: // Í Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[1][3] = true; ledMap[1][4] = true; ledMap[2][3] = true; ledMap[2][4] = true;
      ledMap[3][3] = true; ledMap[3][4] = true; ledMap[4][2] = true; ledMap[4][3] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[6][3] = true; ledMap[6][4] = true;
      ledMap[7][4] = true; ledMap[7][5] = true;
    break;

    case 224: // Ó Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[1][1] = true; ledMap[1][2] = true; ledMap[1][5] = true; ledMap[1][6] = true;
      ledMap[2][1] = true; ledMap[2][2] = true; ledMap[2][5] = true; ledMap[2][6] = true; ledMap[3][1] = true; ledMap[3][2] = true; ledMap[3][5] = true; ledMap[3][6] = true;
      ledMap[4][2] = true; ledMap[4][3] = true; ledMap[4][4] = true; ledMap[4][5] = true; ledMap[6][3] = true; ledMap[6][4] = true; ledMap[7][4] = true; ledMap[7][5] = true;
    break;

    case 233: // Ú Character
      ledMap[0][2] = true; ledMap[0][3] = true; ledMap[0][4] = true; ledMap[0][5] = true; ledMap[0][6] = true; ledMap[1][1] = true; ledMap[1][2] = true; ledMap[1][5] = true;
      ledMap[1][6] = true; ledMap[2][1] = true; ledMap[2][2] = true; ledMap[2][5] = true; ledMap[2][6] = true; ledMap[3][1] = true; ledMap[3][2] = true; ledMap[3][5] = true;
      ledMap[3][6] = true; ledMap[4][1] = true; ledMap[4][2] = true; ledMap[4][5] = true; ledMap[4][6] = true; ledMap[6][3] = true; ledMap[6][4] = true; ledMap[7][4] = true;
      ledMap[7][5] = true;
    break;
  }

  displayCharacterOnScreenAux(ledMap);
}

void displayCharacterBuzzing(){
  String asciiBinary = "";

  Serial.println("Printng buzzerMap");
  for(int i=0; i<6; i++){
    Serial.println(buzzerMap[i]);
  }

  // Assings the binary number according to buzzers behavior (1: Buzzing, 0: Not buzzing)
  for(int i=0; i<6; i++){
    if(buzzerMap[i] == false){
      asciiBinary += "0";
    }else{
      asciiBinary += "1";
    }
  }

  // Converts binary to decimal
  int asciiDecimal = (byte) strtol(asciiBinary.c_str(), NULL, 2);

  Serial.println(asciiDecimal);

  byte ascii = 0;

  if(myBrailleDots[lastCharacterReaded] == 17){
    // Case of uppercase characters
    for(int i=65; i<=90; i++){
      if(myBrailleDots[i] == asciiDecimal){
        ascii = i;
        break;
      }
    }

    switch(asciiDecimal){
      case 63:
        ascii = 144;
        break;
      case 47:
        ascii = 181;
        break;
      case 18:
        ascii = 214;
        break;
      case 25:
        ascii = 224;
        break;
      case 31:
        ascii = 233;
        break;
      case 11:
        ascii = 39;
        break;
      case 8:
        ascii = 47;
        break;
      default:
        Serial.println("Uppercase error.");
        break;
    }
    
  } else if(myBrailleDots[lastCharacterReaded] == 23){
    // Case of numbers
    for(int i=49; i<=57; i++){
      if(myBrailleDots[i] == asciiDecimal){
        ascii = i;
        break;
      }
    }
  } else if(myBrailleDots[lastCharacterReaded] == 4){
    switch(asciiDecimal){
      case 42:
        ascii = 123;
        break;
      case 34:
        ascii = 60;
        break;
      case 27:
        ascii = 156;
        break;
      default:
        Serial.println("Character prefix error.");
        break;
    }
  } else if(myBrailleDots[lastCharacterReaded] == 21){
    switch(asciiDecimal){
      case 8:
        ascii = 125;
        break;
      case 7:
        ascii = 37;
        break;
      case 26:
        ascii = 36;
        break;
      case 55:
        ascii = 190;
        break;
      default:
        Serial.println("Character prefix error.");
        break;
    }
  } else if(myBrailleDots[lastCharacterReaded] == 20){
    if(asciiDecimal == 48){
      ascii = 189;
    }
  } else{
    // Looks for a match in the ascci-binary array
    for(int i=0; i<255; i++){
      if(i == 36){
        i = 37;
      } else if(i == 49){
        i = 58;
      } else if(i == 65){
        i = 91;
      }

      if(myBrailleDots[i] == asciiDecimal){
        ascii = i;
        break;
      }
    }
  }

  lastCharacterReaded = ascii;

  displayCharacter(ascii);

  // Clears display
  lc.clearDisplay(0);
}

// Management of prefixes
void displayCharacterPrefix(byte characterByte){
  
  if (characterByte >= 48 && characterByte <= 57 && lastCharacterWasNotNumber){
    showableNumberSymbol = false;
    displayCharacter(numericalPrefixByte);
  } else {
    if ((characterByte >= 65 && characterByte <= 90) || characterByte == 62 || characterByte == 128 || 
          characterByte == 154 || characterByte == 144 || characterByte == 181 || characterByte == 214 || 
          characterByte == 224 || characterByte == 233 || characterByte == 165){
      displayCharacter(uppercasePrefixByte);
    } else if (characterByte == 39 || characterByte == 47){
      displayCharacter(prefixByte1);
    }
    else if (characterByte == 123 || characterByte == 156 || characterByte == 60){
      displayCharacter(prefixByte2);
    } else if (characterByte == 125 || characterByte == 37 ||characterByte == 36 ||
                characterByte == 190){
      displayCharacter(prefixByte3);
    } else if (characterByte == 189){
      displayCharacter(prefixByte4);
    }
  }
}

void displayCharacter(byte characterByte){

  // In case of an unadmissible character
  if (myBrailleDots[characterByte] == 99 && lastCharacterReaded != 195 && lastCharacterReaded != 194){
    Serial.println("Not  a translatable character");
    for(int i = 0; i < 3; i++){
      notTranslatableCharacteranimation();
      delay(500);
      lc.clearDisplay(0);
      delay(500);
    }
  } else {
    if(characterByte != 195 && characterByte != 194){
      if (lastCharacterReaded == 195){
        lastCharacterReaded = 255;
        switch(characterByte){
          case 129: // Á Character
            displayCharacter(181);
          break;

          case 161: // á Character
            displayCharacter(160);
          break;

          case 137: // É Character
            displayCharacter(144);
          break;

          case 169: // é Character
            displayCharacter(130);
          break;

          case 141: // Í Character
            displayCharacter(214);
          break;

          case 173: // í Character
            displayCharacter(161);
          break;

          case 147: // Ó Character
            displayCharacter(224);
          break;

          case 179: // ó Character
            displayCharacter(162);
          break;

          case 154: // Ú Character
            displayCharacter(233);
          break;

          case 186: // ú Character
            displayCharacter(163);
          break;

          case 145: // Ñ Character
            displayCharacter(165);
          break;

          case 177: // ñ Character
            displayCharacter(164);
          break;

          case 135: // Catalunya C Character
            displayCharacter(128);
          break;

          case 167: // Catalunya c Character
            displayCharacter(135);
          break;

          case 156: // Dier. U Character
            displayCharacter(154);
          break;

          case 188: // Dier. u Character
            displayCharacter(129);
          break;

          default:
            displayCharacter(characterByte);
          break;
        }
      } else if (lastCharacterReaded == 194) {
        lastCharacterReaded = 255;
        switch(characterByte){
          case 162: // Cent Character
            displayCharacter(189);
          break;

          case 163: // Pound Character
            displayCharacter(156);
          break;

          case 165: // Yen Character
            displayCharacter(190);
          break;

          default:
            displayCharacter(characterByte);
          break;
        }
      } else {
        // Avoid displaying a \n
        if ((characterByte >= 48 && characterByte <= 57) || (characterByte >= 65 && characterByte <= 90) || (characterByte >= 97 && characterByte <= 122)){
          lc.escribirCaracter(characterByte, 0);
        }else if (showableNumberSymbol){
          displayCharacterOnScreen(characterByte);
        }

        // Displays character prefix if necessary
        if(characterNeedsPrefix){
          displayCharacterPrefix(characterByte);
        }
        
        // Displays character
        int thisPin = 2;
        for (mask  = 000001; mask<64; mask <<= 1) {
          if (myBrailleDots[characterByte]  & mask){ 
            digitalWrite(thisPin,HIGH);           
          } else {
            digitalWrite(thisPin,LOW);
          }

          thisPin  = thisPin + 1;   
        }

        // Waits 5 seconds to read the character
        delay(5000);

        // Turn off all buzzers
        digitalWrite(2,LOW);
        digitalWrite(3,LOW);
        digitalWrite(4,LOW);
        digitalWrite(5,LOW);
        digitalWrite(6,LOW);
        digitalWrite(7,LOW);
      }
    }
  }
}

void splitString(String input, char delimiter) {
  for(int i=0; i<10; i++){
    message[i] = "";
  }

  int index = 0; // índice actual en el arreglo de salida
  String part = ""; // subcadena temporal

  // recorrer cada carácter de la cadena de entrada
  for (int i = 0; i < input.length(); i++) {
    char currentChar = input.charAt(i);

    // si el carácter es igual al delimitador
    if (currentChar == delimiter) {
      // agregar la subcadena temporal al arreglo de salida
      message[index] = part;
      part = ""; // reiniciar la subcadena temporal
      index++; // incrementar el índice
    } else {
      part += currentChar; // agregar el carácter a la subcadena temporal
    }
  }

  // agregar la última subcadena al arreglo de salida
  message[index] = part;
}


void loop() {
  if (Serial.available() > 0) {

    // Reads the whole sentence
    String input = Serial.readString();

    splitString(input, '~');

    int state;
    int buzzer;
    float buzzerA;

    int index = 0;

    while(message[index] != ""){

      Serial.println(message[index]);

      // Selects the action by the first character given (w: Write a sentence given, s: Activate or deactivate buzzer given, z: Represent character)
      char action = tolower(message[index].charAt(0));

      switch(action){
        case 'w':
          // Splits and displays the sentence character by character
          for (int i = 1; i < message[index].length(); i++) {
            char character = message[index].charAt(i);
            byte inByte = character;

            // Calls function to display the byte array
            displayCharacter(inByte);

            // Clears display
            lc.clearDisplay(0);

            // Update lastCharacterReaded variable
            lastCharacterReaded = inByte;
            Serial.println(lastCharacterReaded);

            // Update showableNumberSymbol variable
            showableNumberSymbol = true;

            // Update lastCharacterWasNotNumber variable
            if(inByte >= 48 && inByte <= 57){
              lastCharacterWasNotNumber = false;
            }else{
              lastCharacterWasNotNumber = true;
            }

            // 1 second delay between characters
            delay(1000);
          }
        break;

        case 's':
          // Selects the buzzer and the state for that buzzer
          state = message[index].charAt(2) - '0';
          buzzer = message[index].charAt(1) - '0';
          buzzerA = abs(buzzer - 8);
        
          Serial.println("Analyzing buzzer: ");
          Serial.println(buzzerA);
          Serial.println("Which state is: ");
          Serial.println(state);

          if(state == 1){
            // Activates buzzer
            digitalWrite(buzzerA,HIGH);

            // Updates the buzzermap
            buzzerMap[buzzer-1] = true;
          }else{
            // Deactivates buzzer
            digitalWrite(buzzerA,LOW);

            // Updates the buzzermap
            buzzerMap[buzzer-1] = false;
          }
        break;
      
        case 'z':
          // Avoids unnecesary prefixes
          characterNeedsPrefix = false;

          // Displays the character buzzing
          displayCharacterBuzzing();

          // Clears display
          lc.clearDisplay(0);

          // Sets the whole buzzermap to false
          for(int i=0; i<6; i++){
            buzzerMap[i]=false;
          }

          // 1 second delay between characters
          delay(1000);

          // Returns variable to original state
          characterNeedsPrefix = false;

          //Serial.println(lastCharacterReaded);
        break;

        default:
          Serial.println("Error: Incorrect input.");
        break;
      }

      index++;

      lastCharacterWasNotNumber = true;
    }

    Serial.println("RTR");

    Serial.flush();
  }
}