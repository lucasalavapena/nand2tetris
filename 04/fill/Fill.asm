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

// state 0 for off
// state -1 for on

// TODO WHY AM I NOT USING A lol

@state
M=0
@prevstate
M=0

@16383
D=A

@startoffset
M=D

@24576
D=A

@endoffset
M=D


(LOOP)
    // update previous state
    @state
    D=M
    @prevstate
    M=D

    // get keyboard input
    @KBD 
    D=M

    @UPDATESTATE
    0;JMP

    (TEST)
    @STATEDIFFIND
    0;JMP

    @UPDATE
    D;JNE

(UPDATESTATE)
    @state
    M=0

    @TEST
    D;JEQ

    @state
    M=-1
(STATEDIFFIND)
    @state
    D=M

    @prev
    D=D-M

    @CHANGE
    D;JNE

(UPDATE)
    // Change needed
    @startoffset
    D=M
    @i
    M=D

    @DRAW
    0;JMP

//DRAW
(DRAW)
    // increment counter
    @i
    D=M+1
    M=D


    @endoffset
    D=M-D
    // check if we finished the screen
    @LOOP
    D;JEQ

    @state
    D=M

    @i
    A=M
    M=D

    @DRAW
    0;JMP