# Preserved initial implementation failure

The first clean-room compile failed before any mathematical check ran:

```text
File "referee.py", line 368
  Generator expression must be parenthesized
```

Cause: the `key=repr` argument to `sorted` was placed syntactically inside the
generator expression in the newly written colour-refinement routine.  This is
an implementation-only failure.  It was preserved before moving `key=repr`
outside the generator expression.
