# expandpoly
https://www.codingame.com/training/hard/expand-the-polynomial

GOAL
You are given a polynomial that is partially or fully factorized and you have to write a code that fully expands it.
For example, if you are given (x-1)*(x+2)=x²+x-2, its coefficients that are 1 1 -2 and you have to write x^2+x-2.

INPUT
A partially or not factorized polynomial.
OUTPUT
The expanded polynomial written in the standard way:
* x^1 is written x
* 1x^3 is written x^3
* 0x^2 and x^0 are not written
CONSTRAINT
All the coefficients are integers (positive, null or negative).
All coefficients are in decreasing order: (x^3 then x^2 then x^1 then x^0)

EXAMPLE
 INPUT | OUTPUT 
 --- | --- 
(x-1)*(x+2) | x^2+x-2
