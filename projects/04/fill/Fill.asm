// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LISTEN)
  @KBD
  D=M
  @FILL
  D;JNE
  @UNFILL
  D;JEQ

(FILL)
  @SCREEN
  D=A
  @start
  M=D
  @KBD
  D=A
  @end
  M=D-1
(LOOP1)
  @start
  D=M
  @end
  D=D-M
  @LISTEN
  D;JGT
  @start
  A=M
  M=-1
  @start
  M=M+1
  @LOOP1
  0;JMP
   
(UNFILL)
  @SCREEN
  D=A
  @start
  M=D
  @KBD
  D=A
  @end
  M=D-1
(LOOP2)
  @start
  D=M
  @end
  D=D-M
  @LISTEN
  D;JGT
  @start
  A=M
  M=0
  @start
  M=M+1
  @LOOP2
  0;JMP
