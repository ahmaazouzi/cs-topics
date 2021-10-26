# Compilers and Interpreters:
- High level languages such as C and Python cannot be understood by computers. We must translate the C and Python source code into something that a machine can make use of. This is done by **compilers** and **interpreters.** These are different types of programs but they are also similar in many ways which we will see later. In this summary, we will see the different steps taken to translate human readable code into something machines can understand and execute (we will also see how high-level lanugages are also translated to other high-level languages).

## Scanning:
- The first step in comilation/interpretation is called **scanning** (or **lexing** or even **lexical analysis**). It basically turns a stream of characters into **tokens** which can be composed of one or more characters. Let's look at how the following C line would be lexed:
```c
// This is a program
int average = (min + max) / 2;  
```
- This line consists of this stream of characters : (**`/`**, **`/`**, **` `**, **`T`**, **`h`**, **`i`**, **`s`**, **` `**, **`i`**, **`s`**, **` `**, **`a`**, **` `**, **`p`**, **`r`**, **`o`**, **`g`**, **`r`**, **`a`**, **`m`**, **`i`**, **`n`**, **`t`**, **` `**, **`a`**, **`v`**, **`e`**, **`r`**, **`a`**, **`g`**, **`e`**, **` `**, **`=`**, **` `**, **`(`**, **`m`**, **`i`**, **`n`**, **` `**, **`+`**, **` `**, **`m`**, **`a`**, **`x`**, **`)`**, **` `**, **`/`**, **` `**, **`2`**, **`;`**, **` `**, **` `** ) which seems kinda incomprehensible even for a human. We need to turn them into the smallest meaningful individual units such as operator symbols, variable names and key words and ignore all white space such as new line and tabs, etc. This stream of characters will then be lexed into (
**`int`**, **`average`**, **`=`**, **`(`**, **`min`**, **`+`**, **`max`**, **`)`**,  **`/`**, **`2`**, **`;`**).

