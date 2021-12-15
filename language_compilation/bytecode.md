# Bytecode:
## Table of Contents:
## Bytecode:
### Why Bytecode:
- Walking the AST as demonstrated in jlox is simple and easy to implement and is also potable as it can run on any platform where Java runs. However, this  approach is slow and extremely memroy inefficient. The tree contains a bunch of pointers scattered all over heap memory and each node consumes a lot of this memory. There is basically no good use of spatial locality and hence cache.
- A language can also be designed so it compiles directly to the metal. This results in extremely fast and efficient code as this code is simple and very low level. The problem with machine code is that its hard and modern processor have very complex and diverse architectures. Designing a language that compiles to machine code needs a lot of specialization and familiarity with the target architectures. Such a language is also not portable across processors.

### What Bytecode Is:
- **Bytecode** is a middle-of-the-road solution that tries to combine the simplicity and portability of walking the AST on the one hand, and the speed and memory efficiency of machine code.
- bytecode is basically an emulation of machine code which is "dense, linear sequence of binary instructions." It is cache friendly with low overhead. However, it doesn't run directly 