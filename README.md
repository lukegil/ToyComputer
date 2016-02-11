
### Synopsis
The goal is to create a program which conceptually reflects the computer represented in _Preliminary Discussion on the Logical Design of an Electronic Computing Instrument_. 

There should be two broad sections. 

(i) The simulator, which contains the actual computer. This includes the Memory Organ, Control Organ, and Arithmetic Organ. There will be a `Read` instruction that loads data from a file (aka "Magnetic Tape") into Memory. [^n] There will also be a `Print` instruction, which outputs the value of the accumulator, and a `Dump` instructions, which prints the entire memory.  

(ii) The Interface, which allows you to interact with the machine without typing binary. This converts instructions, decimal numbers, and text into binary[^n]. This will then hopefully allow for a full on GUI 

### Simulator

##### Memory 

The Memory consists of a Selectron, the RAM, and a Selectron Register, an intermediate memory.

**Selectron**  
The  Selectron is a 32 x 32 x 40 matrix. Each "slot" on the 32x32 plain has an address 0 - 1023. Every "slot" has a "word" of 40 bits (1/0). 
*Future Feature* : break the Selectron into 40 32x32 matrices. When a memory address is requested, each bit will be requested from the corresponding place on the 40 plates.

**Selectron Register**  
A 40 bit holding pen.


##### Arithmetic 

The entire arithmetic organ will be largely a black box, doing operations using python builtins, i.e. I won't be building the method to add two binary numbers. This also means there will be no Arithmetic Register.

_Accumulator_   
A 40 bit holding pen for the 'active' number.

_Future Feature_ : Actually implement an Adder...

##### Control  
    
   
###### Elements

**Control Counter (CC)**  
Holds the memory address for the next instruction. Is incremented 1 on each loop of the machine. Can also be set by `GOTO` and `IFZERO`. 

**Control Register (CR)**  
Holds the second instruction when a word is pull from the Selectron Register, since there are two instructions per word.

**Function Table Register**  
Executes instructions

**Control Flip-flop**   
Simply specified in _Preliminary Discussion_ as a flip flop that tells the machine whether to read the next instruction from CC or CR. If 0, Read from CC. IF 1, CR.


###### Instructions

The control has two sets of instructions. The first governs how instructions are pulled and executed. It is the builtin loop of:

* Check "Control Flip-flop" for whether to read CC or CR
* Move Control Counter (CC) value to Function Table Register (FR)
* Increment CC, flip Control Flip-flop
* Move word from Selectron(address) to Selectron Register
* Move first half of word to FR; move second half to Control Register (CR) 
* Execute instruction in FR
* Check Control Flip-flop for whether to read CC or CR
* Move instruction in CR into FR
* Execute instruction in FR

The second is the individual instructions. 

###### Orders

_Structure_ : An order is an 8 bit order and a 12 bit memory location. Only 6 bits of the order and 10 of the memory will be used. 

There are three large omissions from the orders. First, the absolute value versions of the Addition instructions are left off (cuz fuck that). Second, the shift instructions for Selectron ->  Arithmetic Register and Accumulator -> AR. Both are important for multiplication / roots. Since I'm not manually doing the math, it's not needed.  Third, I'm excluding multiplication and division. Both can be built out of addition and subtraction.

> Uh I think I now need Abs values, since I otherwise dont know how to tell inequalities. With an abs value you add the abs value of a number to itself. If it's 0, the number was negative. 

**Addition**   


<table border=1>
<tr>
<th>Instruction</th>
<th>Binary Equivalent</th>
<th>About</th>
<tr>
<td>ADDNEW</td>
<td>00000001</td>
<td>Clear Accumulator; Add number<br> in position X in the Selectron <br>to the Accumulator</td>
</tr>
<tr>
<td>SUBNEW</td>
<td>00000010</td>
<td>Clear Accumulator; Subtract <br> number in position X in the<br> Selectron to the Accumulator</td>
</tr>
<tr>
<td>ADD</td>
<td>00000011</td>
<td>Add number in position X in the Selectron<br> to the Accumulator</td>
</tr>
<tr>
<td>SUBTRACT</td>
<td>00000100</td>
<td>Subtract number in position X in the Selectron<br> from the Accumulator</td>
</tr>
</table>




**Flow Control**  

<table border=1>
<tr>
<th>Instruction</th>
<th>Binary Equivalent</th>
<th>About</th>
</tr>
<tr>
<td>GOTOLEFT</td>
<td>00000101</td>
<td>Shift the Control to left-hand<br>instruction of the <br> given Selectron address. Set CFF accordingly.</td>
</tr>
<tr>
<td>GOTORIGHT</td>
<td>00000111</td>
<td>Shift the Control to right-hand<br>instruction of the <br> given Selectron address. Set CFF accordingly.</td>
</tr>
<tr>
<td>LEFTIFZERO</td>
<td>00001000</td>
<td>Same as GOTOLEFT, <br>but only if the number<br> in the accumulator is 0</td>
</tr>
<tr>
<td>RIGHTIFZERO</td>
<td>00001001</td>
<td>Same as GOTORIGHT, <br>but only if the number<br> in the accumulator is 0</td>
</tr>
</table>

**Transfers**  
<table border=1>
<tr>
<th>Instruction</th>
<th>Binary Equivalent</th>
<th>About</th>
<tr>
<td>TRANSFER</td>
<td>00001011</td>
<td>Move number in Accumulator<br> to position X</td>
</tr>
<tr>
<td>REPLACELEFT</td>
<td>00001111</td>
<td>Replace the value in the Left-hand<br> instruction at position X <br>with the value in the Accumulator</td>
</tr>
<tr>
<td>REPLACERIGHT</td>
<td>00010000</td>
<td>Replace the value in the Right-hand<br> instruction at position X <br>with the value in the Accumulator</td>
</tr>
<tr>
</table>

**Prints**  
<table border=1>
<tr>
<th>Instruction</th>
<th>Binary Equivalent</th>
<th>About</th>
<tr>
<td>PRINT</td>
<td>00010001</td>
<td>Print value in Accumulator</td>
</tr>
<tr>
<td>DUMP</td>
<td>00010011</td>
<td>Print contents of Selectron</td>
</tr>
</table>

**Sample Programs**    
All completely useless by themselves. Instructions have either .0 or .1 for the left or right side of a word

(i) Count from 1 to 100 and print the result (numbers in decimal)
```
0.0 ADDNEW Address_501 #move the address at 500 to Acc
0.1 ADD Address_502 #add 1 
1.0 TRANSFER Address_501 #move back to Memory
1.1 ADDNEW Address_500  #move the address at 501 to Acc
2.0 SUBTRACT Address_502 #subtract 1
2.1 RIGHTIFZERO Address_4 #gone through loop, print.
3.0 GOTOLEFT Address_1
3.1 TRANSFER Address_500
4.0 PRINT 
...
500 99
501 1
502 1

```

(ii) Find the average of two numbers and print it

```
#add the two numbers
0.0 ADDNEW Address_500
0.1 ADD Address_501
1.1 TRANSFER Address_505

#start loop
1.1 ADDNEW Address_503 #this will be our answer
2.0 ADD Address_504
2.1 TRANSFER Address_503

#Subtract the divisor from the dividend
3.0 ADDNEW Address_505
3.1 SUBTRACT Address_502

#If we got to zero, we've gotten the answer
4.0 RIGHTIFZERO Address_5

#if not, save the number and start over
4.1 TRANSFER Address_505
5.0 GOTO loop start

#print the number
5.1 TRANSFER Address_503
6.0 PRINT

...

# numbers 
500 7
501 82
502 2
503 0
504 1
505 0
```


### The Interface

In short, this is the "compiler". The first version will only do the translation of keywords (e.g. ADD) to their codes, decimals to binary, and fake-ascii to binary.

 **Notes**

[^n]: Not sure how I can load from memory and not overwrite things? How can you tell a whole block is empty?
[^n]: It seems like a fun problem would be to code a bubble sort of a bunch of names. Ascii is actually too memory intensive for the machine's 40bit words (8 bits / character in ascii) so  will have to cut down the set. 
