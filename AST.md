#### Code Sample

Let us look at some simple code implementing the greatest common divisor of two numbers.

##### Implementation 1 (Euclid's Algorithm)

**Python code** (7 lines)

```
def gcd(a, b):
	if a == b:
		return a
	elif a > b:
		return gcd(a-b, b)
	else:
		return gcd(a, b-a)
```

**AST String**

```
Module(
    body=[
        FunctionDef(name='gcd',
            args=arguments(args=[Name(id='a'), Name(id='b')], vararg=None, kwarg=None, defaults=[]),
            body=[
                If(test=Compare(left=Name(id='a'), ops=[Eq], comparators=[Name(id='b')]),
                    body=[Return(value=Name(id='a'))],
                    orelse=[
                        If(test=Compare(left=Name(id='a'), ops=[Gt], comparators=[Name(id='b')]),
                            body=[
                                Return(
                                    value=Call(func=Name(id='gcd'),
                                        args=[BinOp(left=Name(id='a'), op=Sub, right=Name(id='b')), Name(id='b')],
                                        keywords=[],
                                        starargs=None,
                                        kwargs=None))],
                            orelse=[
                                Return(
                                    value=Call(func=Name(id='gcd'),
                                        args=[Name(id='a'), BinOp(left=Name(id='b'), op=Sub, right=Name(id='a'))],
                                        keywords=[],
                                        starargs=None,
                                        kwargs=None))])])],
            decorator_list=[])])

```

**AST Tree Visualization** (only node types)

```
1:Module
└── 2:FunctionDef
    ├── 8:If
    │   ├── 18:If
    │   │   ├── 37:Return
    │   │   │   └── 38:Call
    │   │   │       ├── 43:BinOp
    │   │   │       │   ├── 47:Name
    │   │   │       │   │   └── 48:Load
    │   │   │       │   ├── 46:Sub
    │   │   │       │   └── 44:Name
    │   │   │       │       └── 45:Load
    │   │   │       ├── 41:Name
    │   │   │       │   └── 42:Load
    │   │   │       └── 39:Name
    │   │   │           └── 40:Load
    │   │   ├── 25:Return
    │   │   │   └── 26:Call
    │   │   │       ├── 35:Name
    │   │   │       │   └── 36:Load
    │   │   │       ├── 29:BinOp
    │   │   │       │   ├── 33:Name
    │   │   │       │   │   └── 34:Load
    │   │   │       │   ├── 32:Sub
    │   │   │       │   └── 30:Name
    │   │   │       │       └── 31:Load
    │   │   │       └── 27:Name
    │   │   │           └── 28:Load
    │   │   └── 19:Compare
    │   │       ├── 23:Name
    │   │       │   └── 24:Load
    │   │       ├── 22:Gt
    │   │       └── 20:Name
    │   │           └── 21:Load
    │   ├── 15:Return
    │   │   └── 16:Name
    │   │       └── 17:Load
    │   └── 9:Compare
    │       ├── 13:Name
    │       │   └── 14:Load
    │       ├── 12:Eq
    │       └── 10:Name
    │           └── 11:Load
    └── 3:arguments
        ├── 6:Name
        │   └── 7:Param
        └── 4:Name
            └── 5:Param
```

**ANT Stats**

```
Number of nodes: 48

Name 15
Load 13
Return 3
Param 2
Compare 2
Sub 2
Call 2
BinOp 2
If 2
FunctionDef 1
Gt 1
Eq 1
arguments 1
Module 1
```

**AET Stats**

```
Number of edges (including blank ones): 70

ctx 15
id 15
body 4
args 4
left 4
value 3
right 2
func 2
starargs 2
ops 2
keywords 2
kwargs 2
test 2
op 2
comparators 2
orelse 2
decorator_list 1
name 1
vararg 1
kwarg 1
defaults 1
```

##### Implementation 2 (Iteration)

**Python code** (9 lines)

```
def gcd(a,b):
  limit = a
  if a>b:
    limit = b
  gcd = 1
  for i in range(2,limit+1):
    if a%i == b%i == 0 and i>gcd:
      gcd = i
  return gcd
```

**AST String**

```
Module(
    body=[
        FunctionDef(name='gcd',
            args=arguments(args=[Name(id='a'), Name(id='b')], vararg=None, kwarg=None, defaults=[]),
            body=[Assign(targets=[Name(id='limit')], value=Name(id='a')),
                If(test=Compare(left=Name(id='a'), ops=[Gt], comparators=[Name(id='b')]),
                    body=[Assign(targets=[Name(id='limit')], value=Name(id='b'))],
                    orelse=[]),
                Assign(targets=[Name(id='gcd')], value=Num(n=1)),
                For(target=Name(id='i'),
                    iter=Call(func=Name(id='range'),
                        args=[Num(n=2), BinOp(left=Name(id='limit'), op=Add, right=Num(n=1))],
                        keywords=[],
                        starargs=None,
                        kwargs=None),
                    body=[
                        If(
                            test=BoolOp(op=And,
                                values=[
                                    Compare(left=BinOp(left=Name(id='a'), op=Mod, right=Name(id='i')),
                                        ops=[Eq, Eq],
                                        comparators=[BinOp(left=Name(id='b'), op=Mod, right=Name(id='i')), Num(n=0)]),
                                    Compare(left=Name(id='i'), ops=[Gt], comparators=[Name(id='gcd')])]),
                            body=[Assign(targets=[Name(id='gcd')], value=Name(id='i'))],
                            orelse=[])],
                    orelse=[]),
                Return(value=Name(id='gcd'))],
            decorator_list=[])])
```

**AST Tree Visualization** (only node types)

```
1:Module
└── 2:FunctionDef
    ├── 71:Return
    │   └── 72:Name
    │       └── 73:Load
    ├── 29:For
    │   ├── 41:If
    │   │   ├── 66:Assign
    │   │   │   ├── 69:Name
    │   │   │   │   └── 70:Load
    │   │   │   └── 67:Name
    │   │   │       └── 68:Store
    │   │   └── 42:BoolOp
    │   │       ├── 60:Compare
    │   │       │   ├── 64:Name
    │   │       │   │   └── 65:Load
    │   │       │   ├── 63:Gt
    │   │       │   └── 61:Name
    │   │       │       └── 62:Load
    │   │       ├── 44:Compare
    │   │       │   ├── 59:Num
    │   │       │   ├── 53:BinOp
    │   │       │   │   ├── 57:Name
    │   │       │   │   │   └── 58:Load
    │   │       │   │   ├── 56:Mod
    │   │       │   │   └── 54:Name
    │   │       │   │       └── 55:Load
    │   │       │   ├── 52:Eq
    │   │       │   ├── 51:Eq
    │   │       │   └── 45:BinOp
    │   │       │       ├── 49:Name
    │   │       │       │   └── 50:Load
    │   │       │       ├── 48:Mod
    │   │       │       └── 46:Name
    │   │       │           └── 47:Load
    │   │       └── 43:And
    │   ├── 32:Call
    │   │   ├── 36:BinOp
    │   │   │   ├── 40:Num
    │   │   │   ├── 39:Add
    │   │   │   └── 37:Name
    │   │   │       └── 38:Load
    │   │   ├── 35:Num
    │   │   └── 33:Name
    │   │       └── 34:Load
    │   └── 30:Name
    │       └── 31:Store
    ├── 25:Assign
    │   ├── 28:Num
    │   └── 26:Name
    │       └── 27:Store
    ├── 13:If
    │   ├── 20:Assign
    │   │   ├── 23:Name
    │   │   │   └── 24:Load
    │   │   └── 21:Name
    │   │       └── 22:Store
    │   └── 14:Compare
    │       ├── 18:Name
    │       │   └── 19:Load
    │       ├── 17:Gt
    │       └── 15:Name
    │           └── 16:Load
    ├── 8:Assign
    │   ├── 11:Name
    │   │   └── 12:Load
    │   └── 9:Name
    │       └── 10:Store
    └── 3:arguments
        ├── 6:Name
        │   └── 7:Param
        └── 4:Name
            └── 5:Param
```

**ANT Stats**

```
Number of nodes: 73

Name 21
Load 14
Store 5
Assign 4
Num 4
Compare 3
BinOp 3
Param 2
Gt 2
Eq 2
Mod 2
If 2
And 1
BoolOp 1
FunctionDef 1
For 1
Add 1
Call 1
Return 1
arguments 1
Module 1
```

**AET Stats**

```
Number of edges (including blank ones): 99

id 21
ctx 21
left 6
body 5
value 5
targets 4
n 4
op 4
right 3
comparators 3
orelse 3
ops 3
args 3
test 2
starargs 1
kwarg 1
iter 1
keywords 1
decorator_list 1
vararg 1
kwargs 1
func 1
target 1
name 1
values 1
defaults 1
```