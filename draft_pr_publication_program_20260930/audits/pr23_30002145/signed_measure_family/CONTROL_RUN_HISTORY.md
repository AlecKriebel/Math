# Fresh control run history

2026-10-01 20:00 UTC — First run of fresh_controls.py stopped before mathematical checks:

```
File fresh_controls.py, line 66:
  h1 = int(ym > -s.Rational(1, 2)) - 2*int(ym > s.Rational(1, 2))
TypeError: int() argument must be a string, a bytes-like object or a number, not 'BooleanFalse'
```

The code converted SymPy BooleanTrue/False directly to int. The correction converted these predicates to Python bool first. No equation, expected result, or numerical tolerance changed. The next run exited 0 and wrote fresh_results.json with all 19 checks passing. This runtime failure does not falsify the mathematics, but is preserved for reproducibility.

2026-10-01 20:03 UTC — Count correction: the first successful receipt contains seventeen checks, not nineteen as first stated above and in the 20:00 log checkpoint. That receipt is preserved as fresh_results_initial_17.json, and the corresponding script is preserved in ignored tmp/fresh_controls_initial_17.py. Two connected-domain globalization countercontrols were then added. The final run exited 0 and fresh_results.json contains nineteen checks. The final report distinguishes the two runs.
