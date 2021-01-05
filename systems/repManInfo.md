# Representing and Manipulating Information:
- *I will skip many of the very obvious information such as "everything in computers is 0's and 1's".*

## Intro and Motivation:
- A bit is useless by itself, but multiple bits grouped together can be used to encode different types of information, be it characters, negative or nonnegative numbers, etc. 
- In this document we will study three different types of encodings: **unsigned** encodings which is used to represent whole numbers, **two's complement** encodings used to represent **signed** integers, and **floating-point** encodings which are a binary version of scientific notation used to represent real numbers.- We will also discuss issues that that perplex novices such as **overflow** which happens when we try to represent a number that requires more bits than what we used to represent it. 
- Integer arithmetic in computer, however, respects traditional algebraic properties such as associativity and commutativity and all that jazz.
- Floating-point arithmetic can does not respect some algebraic rules due to so called *precision*. Consider the following two examples:
	+ ***3.14 + (1e20 - 1e20) = 3.14***
	+ ***(3.14 + 1e20) - 1e20 = 0***
- Integers are precise while floats are just approximations to real numbers.
- Having only a hazy idea about how how numbers are represented in computers can lead to some confusing results and cause security vulnerability. You have no choice but sit down and spend a little time trying to understand how these work.
- Several binary representations of numbers are used such as *hexadecimal* and *octal* and these are crucial to understand machine-level code.
- *Bit-level* manipulation is also a crucial in understanding code generated and optimized by the compiler. 
- Understanding this document will allow you to make a strong connection between actual real numbers and integers and their computer representation and have a stronger awareness of the capabilities and limitations of computers.  

## Information Storage:
- Instead of accessing bits directly, we use *bytes* which are blocks of 8 bits. Bytes are the smallest addressable unit of the memory. 
- As we've mentioned before, the machine-level program views memory as a very large array of bytes called *virtual memory*. Each byte is identified by a number called its **address**. The set of all possible addresses is called the *virtual address space*. 
- The sequence of bytes are themselves grouped into *program objects*, meaning instructions, program data and control information. However, while the compiler keeps information about data *types*, the actual machine level program treats data as just a sequence of bytes and has no idea about data types?!!!!

### Hexadecimal Notation:
- A single byte consists of 8 bits. In binary notation, its value ranges from ***00000000<sub>2</sub>*** and ***11111111<sub>2</sub>***, that is the range between ***0<sub>10</sub>*** and ***255<sub>10</sub>*** decimalwise. 
- Binary notation is too long and it would be tedious to use decimal notation to represent bits because it is hard to convert between the two. Instead we use ***hexadecimal*** or **base-16** which represented numbers using this sequence **`0 1 2 3 4 5 6 7 8 9 A B C D E F`** where `A` through `F` represents numbers 10 through 15. Written in hexadecimal, byte values can range between ***00<sub>16</sub>*** and ***FF<sub>16</sub>***. Only two hexes can represent the 8 bits in a byte. The conversion between binary and hex notation should be extremely easy even when dealing with very large values. 
- In C, numeric constants preceded by **`0x`** or **`0X`** are interpreted as hexes. The characters `A` through `F` can be upper, lower or even mixed case so ***FA1D37B*** can be represented as **`0xFA1D37B`**, **`0XFA1D37B`**, **`0xfA1D37B`**, etc. From now on,w e will use C notation for representing hex numbers. 
- Converting between binary and hex and vice-versa should be fairly obvious. Just remember that when given a binary number that is not a multiple of 4, make sure to start with right and take the reminder from the leftmost bits and pad their left with leading zeros. 
- When a decimal number ***x*** is a power of 2 such that ***x = 2<sup>n</sup>***, it is easy to convert it to binary and hexadecimal forms. To convert it to binary you just prepend ***n*** zeros to a 1 so that a ***2<sup>5</sup>*** becomes ***100000***. For hex, you divide the number of zeros by 4 and perpend the result to the number. As for the remainder, you raise 2 to to it. For example ***x = 2048 = 2<sup>11</sup>***. We divided ***11*** by ***4*** and we get ***2*** zeros. The remainder of this division is ***3***, we raise 2 to this 3 and get ***8***. We prepend 2 zeros to 8 and get ***0x800***. ***2048 = 0x800***.
- Converting decimal to hexadecimal notation in the general case involves repeatedly dividing the decimal number by ***16*** resulting in a quotient ***q*** and a remainder ***r*** such that ***x = q · 16 + r***. We then replace r with its equivalent hex symbol and use it as the least significant digit. We repeat the same operation for the quotient for the rest of the number. For example to convert the decimal ***75132*** to hex we do t75132he following:
	- ***75132  =  4695 · 16 + 12		(D)***
	-  ***4695  =  293 · 16 +  7		(7)***
	-   ***293  =   18 · 16 +  5		(5)***
	-   ***18   =    1 · 16 +  2		(2)***
	-    ***1   =    0 · 16 +  1		(1)***
-  The series of divisions above results in the hex **`0x1257D`**.
- The general case of converting hexes to decimal notation is much less tedious. It involves multiplying each hex "digit" by a power of 16 and adding the results, for example:
	- ***0x7AF = 7 · 16<sup>2</sup> + 10 · 16<sup>1</sup> + 15 · 16<sup>0</sup>***
	- ***0x7AF = 7 · 256 + 10 · 16 + 15 · 1***
	- ***0x7AF = 1792 + 160 + 15***
	- ***0x7AF = 1967***

### Data Sizes:
- A computer has a **word size** that indicate the size of a pointer and the width of data bus in that computer. The maximum size of the *virtual address space* itself is determined by the word size. For a machine with ***w***-bit word size, virtual addresses can be between ***0*** and ***2<sup>w</sup> - 1***.
- 32-bit word size machines have access to only a 4 GB virtual address space, hile 64-bit systems have access to exabytes of virtual memory.. That's "almost infinite"!
- 64-bit machines can run code designed for 32-bit machines and the compilers gives you the ability to target either one of the who architectures:
```sh
# This will run on both 32-bit and 64-bit systems
gcc -m32 hello.c

# Only runs on a 64-bit machine
gcc -m64 hello.c
```
- A program can be either a 64-bit or 32-bit program, depending on how it was compiled (and not on the machine where it runs). 
- Computers and compilers can differentiate **data types** based on their formats and lengths. The format would usually be floating point or integer and the lengths of such data types range from 1 byte and 8 bytes in the 64-bit architecture for example. 

<table>
	<thead>
		<tr>
			<th colspan="2">C Declarations</th>
			<th colspan="2">Length in Bytes</th>
		</tr>
		<tr>
			<th>Signed</th>
			<th>Unsigned</th>
			<th>32-bit</th>
			<th>64-bit</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>[signed] <code>char</code></td>
			<td><code>unsigned char</code></td>
			<td>1</td>
			<td>1</td>
		</tr>
		<tr>
			<td><code>short</code></td>
			<td><code>unsigned short</code></td>
			<td>2</td>
			<td>2</td>
		</tr>
		<tr>
			<td><code>int</code></td>
			<td><code>unsigned int</code></td>
			<td>4</td>
			<td>4</td>
		</tr>
		<tr>
			<td><code>long</code></td>
			<td><code>unsigned long</code></td>
			<td>4</td>
			<td>8</td>
		</tr>
		<tr>
			<td> <code>int_32t</code></td>
			<td>uint32_t</td>
			<td>4</td>
			<td>4</td>
		</tr>
		<tr>
			<td><code>int_64t</code></td>
			<td><code>uint_64t</code></td>
			<td>8</td>
			<td>8</td>
		</tr>	
		<tr>
			<td><code>char *</code></td>
			<td></td>
			<td>4</td>
			<td>8</td>
		</tr>
		<tr>
			<td><code>flaot</code></td>
			<td><code>float</code></td>
			<td>4</td>
			<td>4</td>
		</tr>
		<tr>
			<td><code>double</code></td>
			<td></td>
			<td>8</td>
			<td>8</td>
		</tr>
	</tbody>
</table>


### Addressing and Byte Ordering:
### Representing Strings:
### Intro to Boolean Algebra:
### Bit-Level Operations in C:
### Logical Operations in C:
### Shift Operations in C:

## Integer Representations:
### Integral Data Types:
### Unsigned Encodings:
### Two's-Complement Encodings:
### Conversions between Signed and Unsigned:
### Signed vs. Unsigned in C:
### Expanding The Bit Representation of a Number:
### Truncating Numbers:
### Advice on Signed vs. Unsigned:


## Integer Arithmetic:
### Unsigned Addition:
### Two's-Complement Addition:
### Two's-Complement Negation:
### Unsigned Multiplication:
### Two's-Complement Multiplication:
### Multiplying by Constants:
### Dividing by Powers of 2:
### Final Thoughts on Integer Arithmetic:

## Floating Point:
### Fractional Binary Numbers:
### IEE Floating-Point Representation:
### Example Numbers:
### Rounding:
### Floating-Point Operations:
### Floating Point in C:


