```
LUXBIN Light Language                                      N. Christie
Request for Comments: 1                                    LUXBIN Project
Category: Standards Track                                  January 2026


         LUXBIN Light Language Specification (LUXBIN/1.0)

Status of This Memo

   This document specifies a photonic programming language standard for
   the LUXBIN ecosystem. Distribution of this memo is unlimited.

Copyright Notice

   Copyright (c) 2026 Nichole Christie. All rights reserved.

Table of Contents

   1.  Abstract ...................................................   2
   2.  Introduction ...............................................   3
       2.1.  Purpose and Goals ....................................   3
       2.2.  Design Philosophy ....................................   4
       2.3.  Scope ................................................   5
   3.  Notation and Conventions ...................................   5
       3.1.  EBNF .................................................   5
       3.2.  Wavelength Notation ..................................   6
       3.3.  Conformance Levels ...................................   6
   4.  Lexical Structure ..........................................   7
       4.1.  Character Encoding (400-700nm) .......................   7
       4.2.  Tokens ...............................................   8
       4.3.  Comments .............................................   9
       4.4.  Whitespace and Timing ................................   9
   5.  Types and Values ...........................................  10
       5.1.  Primitive Types ......................................  10
       5.2.  Composite Types ......................................  12
       5.3.  Type Conversions .....................................  13
   6.  Expressions ................................................  14
       6.1.  Primary Expressions ..................................  14
       6.2.  Operators and Precedence .............................  14
       6.3.  Assignment Expressions ...............................  16
   7.  Statements .................................................  16
       7.1.  Declarations .........................................  16
       7.2.  Control Flow .........................................  17
       7.3.  Function Statements ..................................  19
   8.  Functions and Modules ......................................  19
       8.1.  Function Declaration .................................  19
       8.2.  Parameters ...........................................  20
       8.3.  Return Values ........................................  21
       8.4.  Module System ........................................  21
   9.  Standard Library ...........................................  22
       9.1.  I/O Functions ........................................  22
       9.2.  Math Functions .......................................  23
       9.3.  String Functions .....................................  24
       9.4.  Quantum Functions ....................................  25
   10. Photonic Encoding ..........................................  27
       10.1. Wavelength Mapping ...................................  27
       10.2. Grammar Encoding via Saturation and Lightness ........  28
       10.3. Temporal Encoding ....................................  29
       10.4. Morse-Light Hybrid ...................................  30
   11. Quantum Extensions .........................................  31
       11.1. Diamond NV Center (637nm) ............................  31
       11.2. Ion Trap Wavelengths .................................  32
       11.3. Frequency Comb .......................................  33
   12. Security Considerations ....................................  34
       12.1. Input Validation .....................................  34
       12.2. Resource Limits ......................................  35
       12.3. Quantum Security .....................................  35
   13. Conformance ................................................  36
       13.1. Implementation Requirements ..........................  36
       13.2. Test Suite ...........................................  37
       13.3. Certification ........................................  37
   14. References .................................................  38
   Appendix A: Wavelength Mapping Table ...........................  39
   Appendix B: EBNF Grammar ......................................  41
   Appendix C: Opcode Reference ...................................  45
   Appendix D: Example Programs ...................................  49


1.  Abstract

   LUXBIN Light Language (hereafter "LUXBIN" or "the language") is a
   photonic programming language designed for execution on optical
   computing substrates, quantum-photonic hybrid processors, and
   conventional electronic interpreters operating in photonic emulation
   mode. The language encodes program source text, tokens, and runtime
   values as wavelengths within the visible electromagnetic spectrum
   (400nm to 700nm), enabling programs to be transmitted, stored, and
   executed as structured light.

   LUXBIN provides a complete imperative programming model with first-
   class quantum extensions, a deterministic type system grounded in
   photonic primitives, and a standard library spanning classical I/O,
   mathematical operations, string manipulation, and quantum gate
   operations. The language is intended to serve as the canonical
   software interface for the LUXBIN photonic blockchain, the LUXBIN
   quantum internet protocol stack, and general-purpose photonic
   computing applications.

   This document constitutes the normative specification of LUXBIN
   version 1.0. Conforming implementations MUST satisfy all requirements
   stated herein using the key words defined in Section 3.3.


2.  Introduction

2.1.  Purpose and Goals

   The LUXBIN Light Language exists to address the following objectives:

   (a) Photonic-Native Computation: Provide a programming language whose
       fundamental representation is optical rather than electronic.
       Programs written in LUXBIN are sequences of wavelength-encoded
       symbols that can be transmitted over fiber optic channels,
       processed by photonic logic gates, and stored in optical media
       without intermediate electronic conversion.

   (b) Quantum Integration: Offer first-class language constructs for
       quantum computation, including qubit declaration, superposition,
       entanglement, measurement, and standard quantum gate operations.
       The language MUST support hybrid classical-quantum programs where
       classical control flow governs quantum operations.

   (c) Human Readability: Despite its photonic encoding, LUXBIN source
       code MUST be representable as human-readable UTF-8 text. The
       textual representation serves as the canonical authoring format;
       the photonic encoding serves as the canonical transmission and
       execution format.

   (d) Deterministic Semantics: All classical operations in LUXBIN MUST
       produce deterministic results. Quantum operations produce non-
       deterministic results only at the point of measurement, and this
       non-determinism MUST be explicitly invoked by the programmer.

   (e) Blockchain Compatibility: LUXBIN programs MUST be suitable for
       deployment as smart contracts on the LUXBIN photonic blockchain.
       The language provides resource metering, bounded execution, and
       deterministic gas accounting for on-chain execution contexts.

2.2.  Design Philosophy

   The design of LUXBIN is guided by the following principles:

   (a) Light as First Principle: Every construct in the language has a
       well-defined photonic representation. Wavelengths encode
       characters. Saturation encodes grammatical role. Lightness
       encodes scope depth. Temporal patterns encode control flow.

   (b) Simplicity over Cleverness: The language favors explicit
       constructs over implicit behavior. There is no operator
       overloading, no implicit type coercion beyond the conversions
       specified in Section 5.3, and no hidden control flow.

   (c) Safety by Default: Variables are immutable by default (const).
       Mutable bindings require explicit opt-in (let). Array bounds
       are checked at runtime. Division by zero produces a defined
       error. Quantum measurements consume the qubit.

   (d) Photonic Efficiency: The language is designed so that common
       programs produce compact photonic encodings. High-frequency
       characters map to shorter wavelengths with higher photon energy,
       enabling energy-proportional computation.

2.3.  Scope

   This specification defines:

   - The lexical structure, syntax, and semantics of LUXBIN programs.
   - The photonic encoding of LUXBIN source and bytecode.
   - The standard library of built-in functions.
   - The quantum extension operations.
   - Conformance requirements for implementations.

   This specification does not define:

   - The LUXBIN bytecode virtual machine architecture (see [LUXBIN-VM]).
   - The LUXBIN blockchain smart contract ABI (see [LUXBIN-ABI]).
   - Hardware specifications for photonic processors.
   - Networking protocols for photonic program transmission.


3.  Notation and Conventions

3.1.  EBNF

   The grammar of LUXBIN is specified using Extended Backus-Naur Form
   (EBNF) as defined in ISO/IEC 14977. The following conventions apply:

       =           definition
       ,           concatenation
       |           alternation
       [ ... ]     optional (zero or one)
       { ... }     repetition (zero or more)
       ( ... )     grouping
       " ... "     terminal string
       (* ... *)   comment

   Non-terminal symbols are written in lowercase with underscores
   (e.g., "if_statement"). Terminal symbols are written in double
   quotes (e.g., "if").

3.2.  Wavelength Notation

   Wavelengths are expressed in nanometers (nm) throughout this
   document. The notation W(x) denotes the wavelength assigned to
   character or token x. For example, W('a') = 400.0nm.

   Wavelength ranges are expressed as inclusive intervals using square
   brackets: [400nm, 700nm] denotes all wavelengths w such that
   400nm <= w <= 700nm.

   Frequency is related to wavelength by the standard relation:

       f = c / lambda

   where c = 299,792,458 m/s (speed of light in vacuum) and lambda
   is the wavelength in meters.

3.3.  Conformance Levels

   The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
   "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in
   this document are to be interpreted as described in RFC 2119.

   MUST / REQUIRED / SHALL: An absolute requirement of the
   specification. A conforming implementation that fails to satisfy a
   MUST requirement is non-conforming.

   SHOULD / RECOMMENDED: There may exist valid reasons in particular
   circumstances to ignore a particular item, but the full implications
   must be understood and carefully weighed before choosing a different
   course.

   MAY / OPTIONAL: An item is truly optional. An implementation may
   choose to include the item because a particular marketplace requires
   it or because the implementor feels that it enhances the product.


4.  Lexical Structure

4.1.  Character Encoding (400-700nm)

   LUXBIN source text is encoded as a sequence of photonic characters.
   Each character corresponds to a specific wavelength in the visible
   spectrum from 400nm (violet) to 700nm (red).

   The textual representation of LUXBIN source code MUST use UTF-8
   encoding. Conforming implementations MUST accept UTF-8 source files
   and convert them to the photonic encoding for execution.

   The photonic character set is divided into the following regions:

       [400nm - 430nm]   Lowercase letters a-z (see Appendix A)
       [430nm - 460nm]   Uppercase letters A-Z
       [460nm - 490nm]   Digits 0-9
       [490nm - 530nm]   Operators and punctuation
       [530nm - 570nm]   Whitespace and control characters
       [570nm - 620nm]   Extended characters and string literals
       [620nm - 670nm]   User-defined symbols
       [670nm - 700nm]   Reserved keywords

   Implementations MUST map characters to wavelengths according to the
   table in Appendix A. The mapping is bijective: each character maps
   to exactly one wavelength, and each wavelength maps to exactly one
   character.

   A conforming implementation MUST reject source text containing
   characters outside the defined mapping. Such characters have no
   photonic representation and are therefore not part of the language.

4.2.  Tokens

   LUXBIN source text is divided into the following token categories:

   (a) Keywords: The following identifiers are reserved keywords and
       MUST NOT be used as variable or function names:

           let     const   func    return  if      then
           else    end     while   do      for     in
           break   continue import  export  true    false
           nil     and     or      not

   (b) Identifiers: A sequence of letters, digits, and underscores
       that begins with a letter or underscore. Identifiers are case-
       sensitive. Implementations MUST support identifiers of at least
       255 characters in length.

           identifier = letter , { letter | digit | "_" } ;
           letter     = "a" | ... | "z" | "A" | ... | "Z" | "_" ;
           digit      = "0" | ... | "9" ;

   (c) Numeric Literals: Integer and floating-point literals in
       decimal notation.

           integer_literal = digit , { digit } ;
           float_literal   = digit , { digit } , "." , digit , { digit } ;

   (d) String Literals: Sequences of characters enclosed in double
       quotes. The following escape sequences MUST be supported:

           \"    double quote
           \\    backslash
           \n    newline (530nm pulse)
           \t    horizontal tab (535nm pulse)
           \0    null character (540nm null pulse)

   (e) Boolean Literals: The keywords "true" and "false".

   (f) Nil Literal: The keyword "nil" represents the absence of a
       value.

   (g) Operators: See Section 6.2 for the complete operator table.

   (h) Delimiters: Parentheses, brackets, commas, and colons.

           ( ) [ ] , :

4.3.  Comments

   Comments begin with the hash character "#" and extend to the end of
   the line. Comments are ignored by the lexer and have no effect on
   program semantics.

       # This is a comment
       let x = 42  # This is also a comment

   LUXBIN does not support multi-line comment delimiters. To create a
   multi-line comment, each line MUST begin with "#".

   In photonic encoding, comments are transmitted as a 490nm pulse
   (the "#" character wavelength) followed by the encoded comment text.
   Receivers SHOULD discard all photonic data between a 490nm pulse
   and the next 530nm newline pulse.

4.4.  Whitespace and Timing

   In the textual representation, whitespace characters (space, tab,
   newline, carriage return) serve as token separators. Consecutive
   whitespace characters are treated as a single separator.

   In the photonic encoding, whitespace is represented by timing gaps
   between photonic pulses:

       Space:      530nm pulse, 1 unit duration
       Tab:        535nm pulse, 4 unit duration
       Newline:    530nm pulse, 2 unit duration (statement boundary)
       Blank line: 530nm pulse, 4 unit duration (block boundary)

   A "unit duration" is implementation-defined but MUST be consistent
   within a single program transmission. Implementations SHOULD use a
   unit duration of 1 nanosecond for fiber-optic transmission and
   1 microsecond for free-space transmission.

   Significant indentation is NOT part of the LUXBIN grammar. Block
   structure is determined by keywords (if/end, while/end, func/end),
   not by indentation. However, implementations SHOULD preserve
   indentation in textual source for readability.


5.  Types and Values

5.1.  Primitive Types

   LUXBIN defines the following primitive types:

   (a) photon_int

       A signed integer type with at least 64 bits of precision.
       Conforming implementations MUST support values in the range
       [-(2^63), 2^63 - 1]. Overflow behavior is defined: arithmetic
       overflow MUST raise a runtime error. Implementations MUST NOT
       silently wrap on overflow.

       Photonic encoding: Integer values are encoded as sequences of
       digit-wavelength pulses (460nm-490nm region) preceded by a type
       tag pulse at 461nm.

       Examples:
           let x: photon_int = 42
           let y: photon_int = -17
           let z: photon_int = 0

   (b) photon_float

       A double-precision IEEE 754 floating-point number. Conforming
       implementations MUST support the full IEEE 754-2008 binary64
       format, including positive and negative infinity, negative zero,
       and NaN.

       Photonic encoding: Float values are encoded as IEEE 754 binary64
       bit patterns transmitted as 64 sequential wavelength pulses, each
       encoding one bit. A 0 bit is encoded as 462nm; a 1 bit is
       encoded as 463nm.

       Examples:
           let pi: photon_float = 3.14159
           let e: photon_float = 2.71828

   (c) photon_string

       An immutable sequence of photonic characters. Strings are
       encoded in the visible spectrum and support the full character
       mapping defined in Section 4.1. String length is measured in
       photonic characters, not bytes.

       Conforming implementations MUST support strings of at least
       2^16 characters. Implementations SHOULD support strings of
       arbitrary length limited only by available memory.

       Photonic encoding: Strings are enclosed by 570nm (open quote)
       and 571nm (close quote) delimiter pulses, with each character
       transmitted at its assigned wavelength.

       Examples:
           let name: photon_string = "LUXBIN"
           let greeting: photon_string = "Hello, World!"

   (d) photon_bool

       A boolean type with exactly two values: true and false. The
       keyword "true" evaluates to photonic truth (a 680nm pulse) and
       "false" evaluates to photonic falsehood (a 681nm pulse).

       In boolean context, the following values are falsy: false, nil,
       0, 0.0, and "". All other values are truthy. Implementations
       MUST apply these truthiness rules consistently in all boolean
       contexts (if conditions, while conditions, and/or short-circuit
       evaluation).

       Examples:
           let flag: photon_bool = true
           let done: photon_bool = false

   (e) qubit

       A quantum bit type representing a two-level quantum system.
       A qubit exists in a superposition of the computational basis
       states |0> and |1> with complex amplitudes alpha and beta such
       that |alpha|^2 + |beta|^2 = 1.

       Qubits obey the no-cloning theorem: a qubit value MUST NOT be
       copied. Assigning a qubit to a new variable transfers ownership;
       the original variable becomes invalid. Attempting to use a
       consumed qubit MUST raise a compile-time or runtime error.

       Qubits are measured using the measure() function (Section 9.4),
       which collapses the superposition and returns a photon_int value
       of 0 or 1. After measurement, the qubit is consumed.

       Photonic encoding: Qubits are represented by 637nm pulses
       (diamond NV center emission wavelength) with polarization state
       encoding the quantum state.

       Examples:
           let q: qubit = superpose(0)
           let result: photon_int = measure(q)

   (f) nil

       The nil type has exactly one value, also written "nil". It
       represents the absence of a meaningful value. Functions that
       do not explicitly return a value return nil.

5.2.  Composite Types

   (a) array

       An ordered, zero-indexed collection of values. Arrays in LUXBIN
       are homogeneously typed: all elements of an array MUST have the
       same type. The element type is inferred from the first element
       or declared explicitly.

       Array literals are enclosed in square brackets:

           let numbers = [1, 2, 3, 4, 5]
           let names = ["Alice", "Bob", "Charlie"]
           let empty = []

       Array access uses bracket notation with zero-based indexing:

           let first = numbers[0]    # Evaluates to 1
           let second = names[1]     # Evaluates to "Bob"

       Out-of-bounds array access MUST raise a runtime error.
       Implementations MUST NOT return undefined values or corrupt
       memory on out-of-bounds access.

       Array length is obtained via the len() standard library
       function (Section 9.3).

       Photonic encoding: Arrays are delimited by 510nm (open bracket)
       and 511nm (close bracket) pulses. Elements are separated by
       512nm (comma) pulses.

5.3.  Type Conversions

   LUXBIN supports the following explicit type conversions. Implicit
   type coercion is NOT supported; all conversions MUST be explicit.

   (a) photon_int to photon_float: Always succeeds. The integer value
       is converted to the nearest representable float. Implementations
       SHOULD warn if precision is lost (integers > 2^53).

   (b) photon_float to photon_int: Truncates toward zero. If the
       float value is outside the representable integer range, a
       runtime error MUST be raised.

   (c) photon_int to photon_string: Produces the decimal string
       representation of the integer.

   (d) photon_float to photon_string: Produces the decimal string
       representation with sufficient digits to uniquely identify
       the float value (at least 15 significant digits).

   (e) photon_string to photon_int: Parses the string as a decimal
       integer. Leading and trailing whitespace is ignored. If the
       string does not represent a valid integer, a runtime error
       MUST be raised.

   (f) photon_string to photon_float: Parses the string as a decimal
       float. If the string does not represent a valid float, a
       runtime error MUST be raised.

   (g) photon_bool to photon_int: true converts to 1, false converts
       to 0.

   (h) photon_int to photon_bool: 0 converts to false, all other
       values convert to true.

   Conversion from or to qubit types is NOT permitted. Qubits cannot
   be converted to classical types except through measurement, which
   is a quantum operation, not a type conversion.


6.  Expressions

6.1.  Primary Expressions

   Primary expressions are the atomic building blocks of LUXBIN
   expressions:

       primary = identifier
              | integer_literal
              | float_literal
              | string_literal
              | "true" | "false" | "nil"
              | "(" , expression , ")"
              | array_literal
              | function_call
              | array_access ;

       array_literal  = "[" , [ expression , { "," , expression } ] , "]" ;
       function_call  = identifier , "(" , [ arguments ] , ")" ;
       arguments      = expression , { "," , expression } ;
       array_access   = identifier , "[" , expression , "]" ;

6.2.  Operators and Precedence

   The following table lists all LUXBIN operators from highest
   precedence (evaluated first) to lowest precedence (evaluated last).
   Operators at the same precedence level associate left-to-right
   unless otherwise noted.

       Precedence  Operator(s)         Description
       ---------   -----------         -----------
       1 (highest) ( )                 Grouping (parentheses)
       2           not                 Logical NOT (unary, right-assoc)
       3           ^                   Exponentiation (right-assoc)
       4           * / %              Multiplication, division, modulo
       5           + -                 Addition, subtraction
       5           - (unary)           Unary negation (right-assoc)
       6           < <= > >=           Comparison (relational)
       7           == !=               Equality, inequality
       8           and                 Logical AND (short-circuit)
       9 (lowest)  or                  Logical OR (short-circuit)

   Operator Semantics:

   (a) Arithmetic operators (+, -, *, /, %, ^) operate on photon_int
       and photon_float values. If both operands are photon_int, the
       result is photon_int. If either operand is photon_float, the
       other is promoted to photon_float and the result is photon_float.

   (b) The division operator "/" performs integer division when both
       operands are photon_int (truncating toward zero) and floating-
       point division when either operand is photon_float. Division by
       zero MUST raise a runtime error.

   (c) The modulo operator "%" is defined only for photon_int operands.
       The result has the same sign as the dividend. Modulo by zero
       MUST raise a runtime error.

   (d) The exponentiation operator "^" is right-associative:
       2 ^ 3 ^ 2 evaluates as 2 ^ (3 ^ 2) = 2 ^ 9 = 512.

   (e) Comparison operators (<, <=, >, >=) return photon_bool. They
       are defined for photon_int, photon_float, and photon_string.
       String comparison is lexicographic by wavelength order.

   (f) Equality operators (==, !=) return photon_bool. They are
       defined for all types. Two values of different types are never
       equal (no implicit coercion). Two nil values are equal. Qubit
       equality is not defined and MUST raise a compile-time error.

   (g) Logical AND ("and") evaluates the left operand first. If it is
       falsy, it returns the left operand without evaluating the right.
       Otherwise, it returns the right operand.

   (h) Logical OR ("or") evaluates the left operand first. If it is
       truthy, it returns the left operand without evaluating the right.
       Otherwise, it returns the right operand.

   (i) Logical NOT ("not") returns true if its operand is falsy, and
       false if its operand is truthy.

6.3.  Assignment Expressions

   Assignment in LUXBIN is a statement, not an expression. It does not
   produce a value and MUST NOT appear in expression context.

       assignment = identifier , "=" , expression ;

   Assignment to a "const" binding MUST raise a compile-time error.
   Assignment to an undeclared variable MUST raise a compile-time
   error. LUXBIN does not support implicit variable declaration.


7.  Statements

7.1.  Declarations

   (a) let (mutable binding):

       The "let" keyword declares a mutable variable. The variable
       may be reassigned after declaration.

           let x = 42
           let name = "LUXBIN"
           let flag = true

       Type annotations are optional. If omitted, the type is inferred
       from the initializer expression. If provided, the initializer
       MUST be compatible with the declared type.

           let x: photon_int = 42
           let pi: photon_float = 3.14159

       A "let" declaration without an initializer sets the variable
       to nil:

           let x    # x is nil

   (b) const (immutable binding):

       The "const" keyword declares an immutable variable. The variable
       MUST be initialized at declaration and MUST NOT be reassigned.

           const PI = 3.14159265
           const MAX_SIZE = 1024
           const GREETING = "Hello, Photonic World!"

       Attempting to reassign a const binding MUST raise a compile-time
       error.

7.2.  Control Flow

   (a) if / then / else / end:

       Conditional execution. The condition expression is evaluated;
       if truthy, the "then" block is executed. Otherwise, the optional
       "else" block is executed.

           if condition then
               # truthy branch
           end

           if condition then
               # truthy branch
           else
               # falsy branch
           end

       Chained conditions use "else if":

           if x > 100 then
               photon_print("large")
           else if x > 10 then
               photon_print("medium")
           else
               photon_print("small")
           end

       The "then" keyword MUST appear on the same line as the "if"
       keyword or the condition expression. Implementations MUST NOT
       allow "then" on a separate line from "if".

   (b) while / do / end:

       Loop that executes the body while the condition is truthy.

           while condition do
               # loop body
           end

       Example:

           let i = 0
           while i < 10 do
               photon_print(i)
               i = i + 1
           end

       Implementations SHOULD support a configurable maximum iteration
       count to prevent infinite loops in smart contract contexts. The
       default limit SHOULD be 10,000,000 iterations.

   (c) for / in / do / end:

       Iteration over arrays.

           for element in collection do
               # loop body using element
           end

       The loop variable is scoped to the loop body and is immutable
       within each iteration. Modifying the collection during iteration
       results in undefined behavior; implementations SHOULD raise a
       runtime error if mutation is detected.

       Numeric range iteration:

           for i in [0, 1, 2, 3, 4] do
               photon_print(i)
           end

   (d) break:

       Immediately exits the innermost enclosing while or for loop.
       Using "break" outside a loop MUST raise a compile-time error.

   (e) continue:

       Skips the remainder of the current iteration and proceeds to
       the next iteration of the innermost enclosing loop. Using
       "continue" outside a loop MUST raise a compile-time error.

7.3.  Function Statements

   Function declarations are statements (see Section 8.1). Function
   calls are expressions (see Section 6.1).


8.  Functions and Modules

8.1.  Function Declaration

   Functions are declared with the "func" keyword and terminated with
   "end":

       func function_name(param1, param2, param3)
           # function body
           return expression
       end

   Function names follow identifier rules (Section 4.2b). Functions
   MUST be declared before they are called; forward references are
   not permitted. Implementations MAY perform a two-pass compilation
   to resolve forward references, but this behavior is OPTIONAL.

   Functions are first-class values: they may be assigned to variables,
   passed as arguments, and returned from other functions.

       let add = func(a, b)
           return a + b
       end

   Recursive functions are supported. Implementations MUST support a
   call stack depth of at least 1024 frames. Stack overflow MUST
   raise a runtime error.

8.2.  Parameters

   Function parameters are positional. LUXBIN does not support named
   arguments, default parameter values, or variadic parameters.

   Parameters are local to the function body and shadow any outer
   variables with the same name. Parameter passing is by value for
   primitive types and by reference for composite types (arrays).

       func greet(name)
           photon_print("Hello, " + name)
       end

   Type annotations on parameters are optional:

       func add(a: photon_int, b: photon_int): photon_int
           return a + b
       end

   If a function is called with the wrong number of arguments, a
   runtime error MUST be raised.

8.3.  Return Values

   The "return" statement exits the function and provides a value to
   the caller.

       func square(x)
           return x * x
       end

   If a function body completes without executing a "return" statement,
   the function returns nil.

   A "return" statement with no expression returns nil:

       func do_something()
           photon_print("done")
           return
       end

   The "return" keyword MUST NOT appear outside a function body. Using
   "return" at the top level MUST raise a compile-time error.

8.4.  Module System

   LUXBIN supports a simple module system based on "import" and
   "export" keywords.

   (a) export:

       The "export" keyword makes a declaration available to other
       modules:

           export func calculate(x)
               return x * 2
           end

           export const VERSION = "1.0.0"

   (b) import:

       The "import" keyword brings declarations from another module
       into scope:

           import calculate from "math_utils"
           import VERSION from "math_utils"

       Selective import:

           import { calculate, VERSION } from "math_utils"

       Module paths are strings. The resolution algorithm for module
       paths is implementation-defined, but conforming implementations
       MUST support relative paths (beginning with "./" or "../") and
       SHOULD support absolute paths.

   Circular imports MUST be detected and MUST raise a compile-time
   error. Implementations MUST NOT enter infinite loops during module
   resolution.


9.  Standard Library

   Conforming implementations MUST provide the following standard
   library functions. These functions are available in all LUXBIN
   programs without explicit import.

9.1.  I/O Functions

   (a) photon_print(value)

       Converts the value to its string representation and outputs
       it to the standard photonic output channel (or standard output
       in electronic emulation mode), followed by a newline.

       Returns: nil

   (b) photon_input(prompt)

       Displays the prompt string and reads a line of input from the
       standard photonic input channel (or standard input in electronic
       emulation mode). Returns the input as a photon_string.

       Returns: photon_string

   (c) photon_read(path)

       Reads the entire contents of the file at the given path and
       returns it as a photon_string. If the file does not exist or
       cannot be read, a runtime error MUST be raised.

       Returns: photon_string

       Security: This function MUST be disabled in smart contract
       execution contexts. See Section 12.1.

   (d) photon_write(path, content)

       Writes the content string to the file at the given path. If
       the file exists, it is overwritten. If the file cannot be
       written, a runtime error MUST be raised.

       Returns: nil

       Security: This function MUST be disabled in smart contract
       execution contexts. See Section 12.1.

9.2.  Math Functions

   All math functions operate on photon_int and photon_float values.
   When called with photon_int arguments, they return photon_int if
   the result is exact, or photon_float otherwise.

   (a) abs(x)       - Absolute value. Returns |x|.
   (b) sqrt(x)      - Square root. Returns photon_float. MUST raise
                       error if x < 0.
   (c) pow(base, exp) - Exponentiation. Equivalent to base ^ exp.
   (d) sin(x)       - Sine (x in radians). Returns photon_float.
   (e) cos(x)       - Cosine (x in radians). Returns photon_float.
   (f) tan(x)       - Tangent (x in radians). Returns photon_float.
   (g) floor(x)     - Floor (largest integer <= x). Returns photon_int.
   (h) ceil(x)      - Ceiling (smallest integer >= x). Returns
                       photon_int.
   (i) round(x)     - Round to nearest integer. Ties round to even
                       (banker's rounding). Returns photon_int.
   (j) min(a, b)    - Returns the smaller of a and b.
   (k) max(a, b)    - Returns the larger of a and b.

9.3.  String Functions

   (a) len(s)       - Returns the number of photonic characters in
                       string s (or the number of elements in array s).
                       Returns photon_int.
   (b) concat(a, b) - Returns a new string that is the concatenation
                       of strings a and b. The "+" operator on strings
                       is syntactic sugar for concat().
   (c) slice(s, start, end) - Returns the substring of s from index
                       start (inclusive) to index end (exclusive).
                       Indices are zero-based. Out-of-bounds indices
                       are clamped to [0, len(s)].
   (d) wavelength(s, i) - Returns the wavelength (as photon_float, in
                       nm) of the character at index i in string s.
   (e) char(w)      - Returns the photonic character corresponding to
                       wavelength w (photon_float, in nm). If w is not
                       a valid character wavelength, returns nil.
   (f) upper(s)     - Returns a new string with all lowercase letters
                       converted to uppercase.
   (g) lower(s)     - Returns a new string with all uppercase letters
                       converted to lowercase.

9.4.  Quantum Functions

   Quantum functions operate on qubit values. These functions are the
   sole mechanism for quantum computation in LUXBIN. Implementations
   that do not support quantum hardware MUST provide a software
   simulation of these operations.

   (a) superpose(classical_value)

       Creates a new qubit in a superposition state. If classical_value
       is 0, the qubit is initialized to |0>. If classical_value is 1,
       the qubit is initialized to |1>. A Hadamard gate is then applied
       to place the qubit in equal superposition.

       Returns: qubit

       Photonic encoding: Emits a 637nm pulse (diamond NV center
       wavelength) with the appropriate polarization.

   (b) measure(q)

       Measures a qubit in the computational basis, collapsing its
       state to |0> or |1>. Returns 0 or 1 as a photon_int. After
       measurement, the qubit is consumed and MUST NOT be used again.

       Returns: photon_int (0 or 1)

   (c) entangle(q1, q2)

       Creates a Bell pair by entangling two qubits. Both qubits
       MUST be in a defined state (not previously consumed). After
       entanglement, measuring one qubit instantaneously determines
       the state of the other.

       Returns: nil (modifies q1 and q2 in place)

   (d) hadamard(q)

       Applies the Hadamard gate to qubit q, mapping |0> to
       (|0> + |1>)/sqrt(2) and |1> to (|0> - |1>)/sqrt(2).

       Returns: nil (modifies q in place)

   (e) cnot(control, target)

       Applies the Controlled-NOT gate. If the control qubit is |1>,
       the target qubit is flipped. If the control qubit is |0>, the
       target qubit is unchanged.

       Returns: nil (modifies target in place)

   (f) phase(q, theta)

       Applies a phase rotation gate to qubit q, adding a relative
       phase of theta radians to the |1> component.

       Returns: nil (modifies q in place)

   (g) teleport(q, sender, receiver)

       Performs quantum teleportation of qubit q from sender to
       receiver using a pre-established entangled pair. The sender
       and receiver qubits MUST be entangled before calling teleport.
       After teleportation, the original qubit q and the sender qubit
       are consumed.

       Returns: nil (receiver holds the teleported state)


10.  Photonic Encoding

10.1.  Wavelength Mapping

   The LUXBIN photonic encoding maps source text characters to specific
   wavelengths in the visible spectrum. This mapping is the foundation
   of the light language concept: a LUXBIN program can be literally
   expressed as a sequence of colored light pulses.

   The visible spectrum is divided into regions as described in Section
   4.1. The detailed mapping for lowercase letters (the most common
   characters in LUXBIN source) assigns wavelengths from 400nm (violet,
   letter 'a') to 411.5nm (letter 'z') in increments of approximately
   0.46nm per letter. See Appendix A for the complete table.

   Keywords occupy the reserved region [670nm, 700nm]:

       Keyword     Wavelength
       -------     ----------
       let         670.0nm
       const       671.0nm
       func        672.0nm
       return      673.0nm
       if          674.0nm
       then        675.0nm
       else        676.0nm
       end         677.0nm
       while       678.0nm
       do          679.0nm
       for         680.0nm
       in          681.0nm
       break       682.0nm
       continue    683.0nm
       import      684.0nm
       export      685.0nm
       true        686.0nm
       false       687.0nm
       nil         688.0nm
       and         689.0nm
       or          690.0nm
       not         691.0nm

   When a keyword is encountered during lexical analysis, the entire
   keyword token is transmitted as a single pulse at the keyword's
   assigned wavelength, rather than as individual character pulses.
   This provides efficient encoding and unambiguous parsing.

10.2.  Grammar Encoding via Saturation and Lightness

   Beyond wavelength (hue), LUXBIN photonic encoding uses two
   additional optical properties to encode grammatical information:

   (a) Saturation:

       Saturation encodes the grammatical role of a token:

           100% saturation: Keywords and operators
            75% saturation: Function names and type names
            50% saturation: Variable names and parameters
            25% saturation: Literal values (numbers, strings)
            10% saturation: Comments and whitespace

       Receivers MUST use saturation to disambiguate tokens that share
       the same wavelength but have different grammatical roles.
       Implementations SHOULD emit the correct saturation level for
       all tokens.

   (b) Lightness:

       Lightness encodes the lexical scope depth:

           100% lightness: Global scope (depth 0)
            80% lightness: First nested scope (depth 1)
            60% lightness: Second nested scope (depth 2)
            40% lightness: Third nested scope (depth 3)
            20% lightness: Fourth or deeper scope (depth 4+)

       Lightness encoding is OPTIONAL. Implementations MAY emit all
       tokens at 100% lightness. However, implementations that support
       lightness encoding MUST follow the mapping above.

10.3.  Temporal Encoding

   The timing of photonic pulses encodes structural information:

   (a) Pulse Duration:

       Short pulse (1 unit):  Character within a token
       Medium pulse (2 units): Token separator
       Long pulse (4 units):  Statement separator
       Extra-long (8 units):  Block separator (function/if/while boundary)

   (b) Pulse Gaps:

       No gap:           Characters within a multi-character token
       1 unit gap:        Tokens within a statement
       2 unit gap:        Statements within a block
       4 unit gap:        Blocks within a module

   (c) Clock Recovery:

       Receivers MUST implement clock recovery to synchronize with the
       transmitter's timing. A preamble sequence of eight alternating
       530nm/531nm pulses at 1 unit duration MUST precede every
       program transmission. This preamble allows the receiver to
       establish the unit duration.

   Implementations MUST tolerate timing jitter of up to 10% of the
   unit duration. Pulses that arrive within 10% of the expected time
   boundary SHOULD be assigned to the nearest valid timing slot.

10.4.  Morse-Light Hybrid

   For constrained environments where only a single-wavelength light
   source is available (e.g., a single LED), LUXBIN supports a Morse
   code hybrid encoding:

       - Short pulse (1 unit ON):   dot
       - Long pulse (3 units ON):   dash
       - 1 unit OFF:               intra-character gap
       - 3 units OFF:              inter-character gap
       - 7 units OFF:              word/token gap

   Characters are encoded using International Morse Code mappings.
   Keywords are encoded using a special prefix sequence (dash-dash-
   dash-dot) followed by the keyword's numeric index (0-21) in binary
   Morse.

   The Morse-Light Hybrid encoding is OPTIONAL. Conforming
   implementations MAY support it but are not required to do so.
   Implementations that support Morse-Light Hybrid MUST indicate this
   capability in their conformance declaration.


11.  Quantum Extensions

11.1.  Diamond NV Center (637nm)

   The nitrogen-vacancy (NV) center in diamond is a primary physical
   platform for LUXBIN quantum operations. The NV center emits
   fluorescence at 637nm, which serves as the canonical qubit
   wavelength in LUXBIN.

   Implementations targeting diamond NV center hardware MUST:

   (a) Use 637nm photons for qubit state readout.
   (b) Use 532nm (green) laser pulses for NV center initialization.
   (c) Use microwave pulses at 2.87 GHz for spin manipulation.
   (d) Achieve single-shot readout fidelity of at least 95%.

   The NV center provides the following properties relevant to LUXBIN:

   - Coherence time: T2 >= 1ms at room temperature.
   - Single-qubit gate fidelity: >= 99%.
   - Two-qubit gate fidelity: >= 95% (via dipolar coupling).
   - Operating temperature: Room temperature (300K).

   Implementations running on simulated hardware SHOULD model NV
   center noise characteristics for realistic quantum simulation.

11.2.  Ion Trap Wavelengths

   LUXBIN quantum extensions also support trapped-ion quantum computing
   platforms. The following ion species and wavelengths are defined:

       Ion         Wavelength      Purpose
       ---         ----------      -------
       Ca-40       397nm           Doppler cooling
       Ca-40       729nm           Qubit transition (S1/2 to D5/2)
       Ca-40       854nm           Repumping
       Ba-137      493nm           Doppler cooling
       Ba-137      650nm           Repumping
       Yb-171      369.5nm         Doppler cooling
       Yb-171      435nm           Qubit transition

   Implementations targeting ion trap hardware MUST specify the ion
   species in the program header:

       # @platform ion-trap
       # @ion Ca-40

   Ion trap implementations MUST support the following gate operations
   with the specified minimum fidelities:

   - Single-qubit gates: >= 99.9%
   - Two-qubit (Molmer-Sorensen) gates: >= 99.0%
   - State preparation fidelity: >= 99.5%
   - Measurement fidelity: >= 99.0%

11.3.  Frequency Comb

   A frequency comb is an optical spectrum consisting of equidistant
   spectral lines. LUXBIN leverages frequency combs for multi-channel
   parallel quantum operations.

   A LUXBIN frequency comb encodes multiple qubits simultaneously by
   assigning each qubit to a distinct comb tooth (spectral line). The
   comb parameters are:

   (a) Center frequency: f_c (implementation-defined, typically in the
       optical telecommunications C-band at 1550nm or the visible band
       at 637nm).

   (b) Repetition rate: f_rep (the frequency spacing between adjacent
       comb teeth). SHOULD be between 100 MHz and 10 GHz.

   (c) Number of teeth: N (the number of simultaneous qubit channels).
       Implementations MUST support at least 8 comb teeth.
       Implementations SHOULD support at least 64 comb teeth.

   The frequency of the k-th comb tooth is:

       f_k = f_c + k * f_rep,   k = -N/2, ..., N/2

   Frequency comb operations are exposed via an extended API:

       # @platform frequency-comb
       # @teeth 64
       # @rep-rate 1GHz

   Conforming implementations that support frequency comb MUST
   maintain coherence across all comb teeth for the duration of a
   quantum circuit. Phase drift between comb teeth MUST NOT exceed
   0.01 radians per gate operation.


12.  Security Considerations

12.1.  Input Validation

   All implementations MUST validate input at the following boundaries:

   (a) Source Text: The lexer MUST reject any byte sequence that is
       not valid UTF-8. Embedded null bytes MUST be rejected.

   (b) Photonic Input: Receivers MUST reject pulses with wavelengths
       outside the defined range [400nm, 700nm]. Pulses with undefined
       wavelengths MUST be discarded with a warning.

   (c) String Input: The photon_input() function MUST limit input
       length to a configurable maximum (default: 65,536 characters).
       Implementations MUST NOT allow buffer overflow via string input.

   (d) File I/O: The photon_read() and photon_write() functions MUST
       validate file paths to prevent directory traversal attacks.
       Paths containing ".." SHOULD be rejected. In smart contract
       contexts, file I/O MUST be disabled entirely.

   (e) Array Bounds: All array accesses MUST be bounds-checked at
       runtime. Out-of-bounds access MUST raise a runtime error.

12.2.  Resource Limits

   Implementations MUST enforce the following resource limits to
   prevent denial-of-service attacks:

   (a) Maximum execution steps: Configurable, default 100,000,000.
   (b) Maximum memory allocation: Configurable, default 256 MB.
   (c) Maximum call stack depth: Configurable, default 1,024 frames.
   (d) Maximum string length: Configurable, default 16,777,216 chars.
   (e) Maximum array length: Configurable, default 16,777,216 elements.
   (f) Maximum loop iterations: Configurable, default 10,000,000.

   When any resource limit is exceeded, the implementation MUST halt
   execution and raise a resource exhaustion error. The implementation
   MUST NOT crash, hang, or corrupt state.

   In blockchain smart contract contexts, resource consumption MUST
   be metered deterministically to enable gas accounting.

12.3.  Quantum Security

   Quantum operations introduce unique security considerations:

   (a) Qubit Leakage: Implementations MUST ensure that qubit state
       information cannot be extracted by unauthorized parties.
       Quantum memory MUST be securely erased after qubit consumption.

   (b) Side Channels: Implementations SHOULD minimize timing side
       channels in quantum operations. The duration of quantum gate
       operations SHOULD NOT depend on the qubit state.

   (c) Entanglement Verification: Before performing teleportation,
       implementations MUST verify that the entangled pair is genuine
       (not a separable state masquerading as entangled). This MAY
       be accomplished via Bell inequality tests on a statistical
       sample of entangled pairs.

   (d) Quantum Random Number Generation: Implementations SHOULD
       provide access to quantum random number generation for
       cryptographic applications. The measure() function on a
       Hadamard-transformed qubit provides true quantum randomness.

   (e) Post-Quantum Cryptography: Module signatures and smart contract
       authentication SHOULD use post-quantum cryptographic algorithms
       (e.g., CRYSTALS-Kyber, CRYSTALS-Dilithium) to resist quantum
       attacks.


13.  Conformance

13.1.  Implementation Requirements

   A conforming LUXBIN implementation MUST:

   (a) Accept valid UTF-8 source text conforming to the grammar in
       Appendix B and produce correct results for all well-defined
       programs.

   (b) Reject ill-formed programs with meaningful error messages that
       include source location (file, line, column).

   (c) Implement all primitive types (Section 5.1) with the specified
       precision and semantics.

   (d) Implement all standard library functions (Section 9) with the
       specified behavior.

   (e) Enforce all resource limits (Section 12.2) and raise errors
       on violation.

   (f) Support the photonic encoding described in Section 10.1 for
       at least source-to-photonic and photonic-to-source conversion.

   A conforming implementation SHOULD:

   (g) Support quantum extensions (Section 11) via either hardware or
       software simulation.

   (h) Support the module system (Section 8.4).

   (i) Provide a REPL (Read-Eval-Print Loop) for interactive use.

   A conforming implementation MAY:

   (j) Support the Morse-Light Hybrid encoding (Section 10.4).
   (k) Support frequency comb operations (Section 11.3).
   (l) Provide additional platform-specific extensions beyond this
       specification.

13.2.  Test Suite

   The LUXBIN Conformance Test Suite (LCTS) is the normative test
   suite for verifying implementation conformance. The test suite
   consists of:

   (a) Positive tests: Well-formed programs with expected output.
       A conforming implementation MUST produce the expected output
       for all positive tests.

   (b) Negative tests: Ill-formed programs that MUST be rejected.
       A conforming implementation MUST reject all negative tests
       with an appropriate error.

   (c) Quantum tests: Programs exercising quantum operations. These
       tests use statistical validation (e.g., measuring 1000 qubits
       in superposition and verifying approximately 50/50 distribution
       within 5% tolerance).

   The test suite is maintained at the LUXBIN project repository and
   versioned alongside this specification.

13.3.  Certification

   Implementations that pass the full LCTS MAY claim conformance to
   "LUXBIN/1.0". Implementations that pass the LCTS excluding quantum
   tests MAY claim conformance to "LUXBIN/1.0-Classical".

   Certification claims MUST include:

   (a) The LUXBIN specification version (e.g., "1.0").
   (b) The LCTS version and pass rate.
   (c) The platform and operating environment.
   (d) Any optional features supported.


14.  References

   [RFC2119]    Bradner, S., "Key words for use in RFCs to Indicate
                Requirement Levels", BCP 14, RFC 2119, March 1997.

   [IEEE754]    IEEE, "IEEE Standard for Floating-Point Arithmetic",
                IEEE 754-2008, August 2008.

   [ISO14977]   ISO/IEC, "Information technology -- Syntactic
                metalanguage -- Extended BNF", ISO/IEC 14977:1996.

   [LUXBIN-VM]  Christie, N., "LUXBIN Virtual Machine Specification",
                LUXBIN Project, 2026 (forthcoming).

   [LUXBIN-ABI] Christie, N., "LUXBIN Smart Contract ABI
                Specification", LUXBIN Project, 2026 (forthcoming).

   [NV-CENTER]  Doherty, M. W., et al., "The nitrogen-vacancy colour
                centre in diamond", Physics Reports, 528(1), 2013.

   [ION-TRAP]   Bruzewicz, C. D., et al., "Trapped-ion quantum
                computing: Progress and challenges", Applied Physics
                Reviews, 6(2), 2019.

   [FREQ-COMB]  Diddams, S. A., "The evolving optical frequency comb",
                Journal of the Optical Society of America B, 27(11),
                2010.

   [CRYSTALS]   Bos, J., et al., "CRYSTALS -- Kyber: a CCA-secure
                module-lattice-based KEM", NIST PQC Standardization,
                2020.


Appendix A:  Wavelength Mapping Table

   The following table defines the wavelength assignment for lowercase
   Latin letters. This mapping is normative.

       Character   Wavelength (nm)   Color Region    Photon Energy (eV)
       ---------   ---------------   ------------    ------------------
       a           400.00            Violet           3.100
       b           400.46            Violet           3.096
       c           400.92            Violet           3.093
       d           401.38            Violet           3.089
       e           401.84            Violet           3.086
       f           402.30            Violet           3.082
       g           402.76            Violet           3.079
       h           403.22            Violet           3.075
       i           403.68            Violet           3.072
       j           404.14            Violet           3.068
       k           404.60            Violet           3.065
       l           405.06            Violet           3.061
       m           405.52            Violet           3.058
       n           405.98            Violet           3.054
       o           406.44            Violet           3.051
       p           406.90            Violet           3.047
       q           407.36            Violet           3.044
       r           407.82            Violet           3.041
       s           408.28            Violet           3.037
       t           408.74            Violet           3.034
       u           409.20            Violet           3.030
       v           409.66            Violet           3.027
       w           410.12            Violet           3.024
       x           410.58            Violet           3.020
       y           411.04            Violet           3.017
       z           411.50            Violet           3.014

   Uppercase letters (A-Z) are mapped to wavelengths 430.00nm through
   441.50nm using the same 0.46nm increment.

   Digits (0-9) are mapped to wavelengths 460.00nm through 464.14nm
   using a 0.46nm increment:

       Character   Wavelength (nm)   Color Region
       ---------   ---------------   ------------
       0           460.00            Blue
       1           460.46            Blue
       2           460.92            Blue
       3           461.38            Blue
       4           461.84            Blue
       5           462.30            Blue
       6           462.76            Blue
       7           463.22            Blue
       8           463.68            Blue
       9           464.14            Blue

   Operators and punctuation (490nm-530nm region):

       Token       Wavelength (nm)   Description
       -----       ---------------   -----------
       +           490.00            Addition
       -           491.00            Subtraction / Negation
       *           492.00            Multiplication
       /           493.00            Division
       %           494.00            Modulo
       ^           495.00            Exponentiation
       =           496.00            Assignment
       ==          497.00            Equality
       !=          498.00            Inequality
       <           499.00            Less than
       >           500.00            Greater than
       <=          501.00            Less than or equal
       >=          502.00            Greater than or equal
       (           505.00            Left parenthesis
       )           506.00            Right parenthesis
       [           510.00            Left bracket
       ]           511.00            Right bracket
       ,           512.00            Comma
       :           513.00            Colon
       #           490.50            Comment marker
       "           570.00            String delimiter (open)
       "           571.00            String delimiter (close)


Appendix B:  EBNF Grammar

   The following EBNF grammar is the normative definition of LUXBIN
   syntax. It is complete and self-contained.

   (* ==================== Top Level ==================== *)

   program = { statement } ;

   statement = declaration
             | assignment_stmt
             | if_statement
             | while_statement
             | for_statement
             | function_declaration
             | return_statement
             | break_statement
             | continue_statement
             | import_statement
             | export_statement
             | expression_statement ;

   (* ==================== Declarations ==================== *)

   declaration = "let" , identifier , [ ":" , type_name ] ,
                 [ "=" , expression ] , newline
               | "const" , identifier , [ ":" , type_name ] ,
                 "=" , expression , newline ;

   type_name = "photon_int" | "photon_float" | "photon_string"
             | "photon_bool" | "qubit" ;

   assignment_stmt = identifier , "=" , expression , newline
                   | identifier , "[" , expression , "]" , "=" ,
                     expression , newline ;

   (* ==================== Control Flow ==================== *)

   if_statement = "if" , expression , "then" , newline ,
                  { statement } ,
                  { "else" , "if" , expression , "then" , newline ,
                    { statement } } ,
                  [ "else" , newline , { statement } ] ,
                  "end" , newline ;

   while_statement = "while" , expression , "do" , newline ,
                     { statement } ,
                     "end" , newline ;

   for_statement = "for" , identifier , "in" , expression , "do" ,
                   newline ,
                   { statement } ,
                   "end" , newline ;

   break_statement = "break" , newline ;

   continue_statement = "continue" , newline ;

   (* ==================== Functions ==================== *)

   function_declaration = "func" , identifier , "(" ,
                          [ parameter_list ] , ")" ,
                          [ ":" , type_name ] , newline ,
                          { statement } ,
                          "end" , newline ;

   parameter_list = parameter , { "," , parameter } ;

   parameter = identifier , [ ":" , type_name ] ;

   return_statement = "return" , [ expression ] , newline ;

   (* ==================== Modules ==================== *)

   import_statement = "import" , identifier , "from" ,
                      string_literal , newline
                    | "import" , "{" , identifier ,
                      { "," , identifier } , "}" , "from" ,
                      string_literal , newline ;

   export_statement = "export" , ( declaration
                                 | function_declaration ) ;

   (* ==================== Expressions ==================== *)

   expression = or_expression ;

   or_expression = and_expression , { "or" , and_expression } ;

   and_expression = equality_expression ,
                    { "and" , equality_expression } ;

   equality_expression = comparison_expression ,
                         { ( "==" | "!=" ) ,
                           comparison_expression } ;

   comparison_expression = addition_expression ,
                           { ( "<" | ">" | "<=" | ">=" ) ,
                             addition_expression } ;

   addition_expression = multiplication_expression ,
                         { ( "+" | "-" ) ,
                           multiplication_expression } ;

   multiplication_expression = exponentiation_expression ,
                               { ( "*" | "/" | "%" ) ,
                                 exponentiation_expression } ;

   exponentiation_expression = unary_expression ,
                               [ "^" , exponentiation_expression ] ;

   unary_expression = [ "not" | "-" ] , primary_expression ;

   primary_expression = identifier
                      | integer_literal
                      | float_literal
                      | string_literal
                      | "true" | "false" | "nil"
                      | "(" , expression , ")"
                      | "[" , [ expression , { "," , expression } ] ,
                        "]"
                      | identifier , "(" ,
                        [ expression , { "," , expression } ] , ")"
                      | identifier , "[" , expression , "]" ;

   expression_statement = expression , newline ;

   (* ==================== Lexical Rules ==================== *)

   identifier = letter , { letter | digit | "_" } ;
   letter = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" | "_" ;
   digit = "0" | "1" | ... | "9" ;

   integer_literal = digit , { digit } ;
   float_literal = digit , { digit } , "." , digit , { digit } ;

   string_literal = '"' , { string_char } , '"' ;
   string_char = (* any character except '"' and '\' *)
               | '\' , escape_char ;
   escape_char = '"' | '\' | 'n' | 't' | '0' ;

   newline = (* newline character or end of input *) ;


Appendix C:  Opcode Reference

   The LUXBIN bytecode uses a single-byte opcode followed by zero or
   more operand bytes. The following table lists all defined opcodes.
   Opcodes not listed here are reserved for future use and MUST NOT
   be emitted by conforming compilers.

   Opcode  Mnemonic        Operands        Description
   ------  --------        --------        -----------

   (* Stack Operations *)
   0x00    NOP             -               No operation
   0x01    PUSH_INT        i64             Push integer constant
   0x02    PUSH_FLOAT      f64             Push float constant
   0x03    PUSH_STRING     u16(idx)        Push string from constant pool
   0x04    PUSH_TRUE       -               Push boolean true
   0x05    PUSH_FALSE      -               Push boolean false
   0x06    PUSH_NIL        -               Push nil value
   0x07    POP             -               Discard top of stack
   0x08    DUP             -               Duplicate top of stack
   0x09    SWAP            -               Swap top two stack values
   0x0A    ROT             -               Rotate top three values

   (* Variable Operations *)
   0x10    LOAD_LOCAL      u16(slot)       Load local variable
   0x11    STORE_LOCAL     u16(slot)       Store to local variable
   0x12    LOAD_GLOBAL     u16(idx)        Load global variable
   0x13    STORE_GLOBAL    u16(idx)        Store to global variable
   0x14    LOAD_CONST      u16(slot)       Load constant (immutable)
   0x15    DEFINE_LOCAL    u16(slot)       Define new local variable
   0x16    DEFINE_GLOBAL   u16(idx)        Define new global variable

   (* Arithmetic Operations *)
   0x20    ADD             -               a + b
   0x21    SUB             -               a - b
   0x22    MUL             -               a * b
   0x23    DIV             -               a / b
   0x24    MOD             -               a % b
   0x25    POW             -               a ^ b
   0x26    NEG             -               -a (unary negation)
   0x27    INC             -               a + 1
   0x28    DEC             -               a - 1

   (* Comparison Operations *)
   0x30    EQ              -               a == b
   0x31    NEQ             -               a != b
   0x32    LT              -               a < b
   0x33    GT              -               a > b
   0x34    LTE             -               a <= b
   0x35    GTE             -               a >= b

   (* Logical Operations *)
   0x40    AND             -               Logical AND
   0x41    OR              -               Logical OR
   0x42    NOT             -               Logical NOT

   (* Control Flow *)
   0x50    JUMP            i16(offset)     Unconditional jump
   0x51    JUMP_IF_TRUE    i16(offset)     Jump if top is truthy
   0x52    JUMP_IF_FALSE   i16(offset)     Jump if top is falsy
   0x53    LOOP            i16(offset)     Loop back (jump backward)
   0x54    CALL            u8(argc)        Call function with argc args
   0x55    RETURN          -               Return from function
   0x56    HALT            -               Terminate execution

   (* Array Operations *)
   0x60    ARRAY_NEW       u16(len)        Create array with len elements
   0x61    ARRAY_GET       -               Get element: arr[idx]
   0x62    ARRAY_SET       -               Set element: arr[idx] = val
   0x63    ARRAY_LEN       -               Push array length
   0x64    ARRAY_PUSH      -               Append element to array
   0x65    ARRAY_POP       -               Remove and push last element
   0x66    ARRAY_SLICE     -               Slice array: arr[start:end]

   (* String Operations *)
   0x70    STR_CONCAT      -               Concatenate two strings
   0x71    STR_LEN         -               Push string length
   0x72    STR_SLICE       -               Slice string
   0x73    STR_UPPER       -               Convert to uppercase
   0x74    STR_LOWER       -               Convert to lowercase
   0x75    STR_WAVE        -               Get wavelength of char at idx
   0x76    STR_CHAR        -               Get char from wavelength

   (* I/O Operations *)
   0x80    PRINT           -               Print top of stack
   0x81    INPUT           -               Read input, push string
   0x82    FILE_READ       -               Read file, push string
   0x83    FILE_WRITE      -               Write string to file

   (* Type Conversion *)
   0x90    TO_INT          -               Convert to photon_int
   0x91    TO_FLOAT        -               Convert to photon_float
   0x92    TO_STRING       -               Convert to photon_string
   0x93    TO_BOOL         -               Convert to photon_bool

   (* Math Standard Library *)
   0xA0    MATH_ABS        -               Absolute value
   0xA1    MATH_SQRT       -               Square root
   0xA2    MATH_SIN        -               Sine
   0xA3    MATH_COS        -               Cosine
   0xA4    MATH_TAN        -               Tangent
   0xA5    MATH_FLOOR      -               Floor
   0xA6    MATH_CEIL       -               Ceiling
   0xA7    MATH_ROUND      -               Round
   0xA8    MATH_MIN        -               Minimum of two values
   0xA9    MATH_MAX        -               Maximum of two values

   (* Quantum Operations *)
   0xB0    Q_SUPERPOSE     -               Create qubit in superposition
   0xB1    Q_MEASURE       -               Measure qubit
   0xB2    Q_ENTANGLE      -               Entangle two qubits
   0xB3    Q_HADAMARD      -               Apply Hadamard gate
   0xB4    Q_CNOT          -               Apply CNOT gate
   0xB5    Q_PHASE         -               Apply phase gate
   0xB6    Q_TELEPORT      -               Quantum teleportation

   (* Module Operations *)
   0xC0    IMPORT          u16(idx)        Import module
   0xC1    EXPORT          u16(idx)        Export symbol

   (* Photonic Encoding Operations *)
   0xD0    EMIT_PHOTON     f64(wavelength) Emit photon at wavelength
   0xD1    DETECT_PHOTON   -               Detect incoming photon
   0xD2    SET_SATURATION  u8(pct)         Set saturation for next emit
   0xD3    SET_LIGHTNESS   u8(pct)         Set lightness for next emit
   0xD4    PULSE_SHORT     -               Emit short timing pulse
   0xD5    PULSE_LONG      -               Emit long timing pulse

   (* Debug Operations *)
   0xE0    BREAKPOINT      -               Debugger breakpoint
   0xE1    TRACE           u16(line)       Source line trace

   (* Reserved: 0xF0-0xFF for future extensions *)


Appendix D:  Example Programs

   The following examples demonstrate LUXBIN syntax and semantics.
   Each example is a complete, valid LUXBIN program.

   D.1.  Hello World

       # hello.luxbin
       # The canonical first program in LUXBIN Light Language.
       # When transmitted photonically, this program is a sequence
       # of violet-to-red light pulses encoding each character.

       photon_print("Hello, Photonic World!")

   D.2.  Fibonacci Sequence

       # fibonacci.luxbin
       # Computes the first N Fibonacci numbers using iterative
       # approach. Demonstrates variables, loops, and arithmetic.

       func fibonacci(n)
           if n <= 0 then
               return []
           end

           if n == 1 then
               return [0]
           end

           let result = [0, 1]
           let i = 2
           while i < n do
               let prev1 = result[i - 1]
               let prev2 = result[i - 2]
               let next = prev1 + prev2
               result = result + [next]
               i = i + 1
           end

           return result
       end

       # Compute first 20 Fibonacci numbers
       let fibs = fibonacci(20)
       for f in fibs do
           photon_print(f)
       end

   D.3.  Factorial

       # factorial.luxbin
       # Computes factorial using recursion. Demonstrates recursive
       # function calls and conditional logic.

       func factorial(n)
           if n < 0 then
               photon_print("Error: negative input")
               return nil
           end

           if n <= 1 then
               return 1
           end

           return n * factorial(n - 1)
       end

       # Compute and display factorials 0 through 12
       let i = 0
       while i <= 12 do
           let result = factorial(i)
           photon_print(concat(concat(concat("factorial(", i), ") = "), result))
           i = i + 1
       end

   D.4.  Quantum Random Number Generator

       # quantum_random.luxbin
       # Generates true random numbers using quantum superposition
       # and measurement. Each bit is obtained by measuring a qubit
       # in equal superposition, producing genuine quantum randomness.
       #
       # Photonic encoding note: The superpose() calls emit 637nm
       # (diamond NV center) photons. The measure() calls collapse
       # the quantum state and return classical 0 or 1.

       func quantum_random_byte()
           # Generate 8 random bits via quantum measurement
           let value = 0
           let bit = 0
           while bit < 8 do
               let q = superpose(0)         # Create qubit in |+> state
               let result = measure(q)       # Measure: 0 or 1
               value = value + result * pow(2, bit)
               bit = bit + 1
           end
           return value
       end

       func quantum_random_range(low, high)
           # Generate a random integer in [low, high]
           let range = high - low + 1
           let r = quantum_random_byte() % range
           return low + r
       end

       # Generate and display 10 quantum random numbers
       photon_print("Quantum Random Number Generator")
       photon_print("================================")
       let count = 0
       while count < 10 do
           let byte_val = quantum_random_byte()
           let range_val = quantum_random_range(1, 100)
           photon_print(concat("Random byte: ", byte_val))
           photon_print(concat("Random 1-100: ", range_val))
           photon_print("---")
           count = count + 1
       end

   D.5.  Quantum Entanglement Demonstration

       # entanglement.luxbin
       # Demonstrates quantum entanglement: two qubits are entangled
       # into a Bell pair, then measured. The measurements are always
       # correlated (both 0 or both 1).

       photon_print("Quantum Entanglement Demo")
       photon_print("=========================")

       let trials = 100
       let correlated = 0
       let i = 0

       while i < trials do
           # Create two qubits and entangle them
           let q1 = superpose(0)
           let q2 = superpose(0)
           entangle(q1, q2)

           # Measure both qubits
           let m1 = measure(q1)
           let m2 = measure(q2)

           # Check correlation
           if m1 == m2 then
               correlated = correlated + 1
           end

           i = i + 1
       end

       photon_print(concat("Trials: ", trials))
       photon_print(concat("Correlated: ", correlated))
       photon_print(concat("Correlation rate: ",
                           correlated * 100 / trials))
       photon_print("Expected: ~100% for Bell pair")


Author's Address

   Nichole Christie
   LUXBIN Project

   Email: nichole@luxbin.io
```
