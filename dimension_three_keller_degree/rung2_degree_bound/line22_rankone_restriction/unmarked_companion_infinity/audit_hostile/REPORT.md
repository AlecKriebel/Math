# Hostile audit report

**Verdict:** PASS.

The claimed theorem, scope, raw \(E_7\) kernel, legal gauge quotient,
constant \(E_6\) forcing and converse, and \(E_5\) determinant exit all
survived an independent reconstruction.

## Independent method

`verify_unmarked_infinity_pure.py` is dependency-free.  It implements sparse
multivariate polynomial arithmetic over `fractions.Fraction`, differentiates
and expands the full \(3\times3\) Jacobian directly, and computes the two
displayed exact minors by rational elimination.  It does not import SymPy,
invoke PARI/GP, or load matrices from the supplied package.

The audit confirms:

- \(\operatorname{Jac}(P,Q,R)=0\) and the compact \(E_7\) formula on every
  one of the 26 raw coefficient directions;
- the stated nonzero \(18\times18\) raw minor;
- all eight kernel directions, their \(-8\) independence minor, and the
  exact relation expressing the \(z\)-translation jet;
- rank \(18\) and kernel completeness by the independent rank sandwich
  (nonzero 18-minor plus eight independent kernel vectors);
- legality of the two determinant-one target shears and the two affine
  source-translation jets, leaving exactly the four displayed normal
  directions;
- that \(E_6\) contains only the ten claimed variables, linearly and with
  constant coefficients, and has the stated nonzero \(10\times10\) minor;
- the full \(E_6\) converse after those ten variables vanish;
- the four literal \(E_5\) coefficients and the full \(E_5\) specialization;
  and
- singularity of \(L\) after the six forced linear coefficients vanish.

The supplied SymPy, strict PARI/GP, and supplied fail-closed harness also pass
unchanged.

## Division and rank-drop audit

There is no parameter localization in this proof.  Both forcing minors are
nonzero integers.  Thus there are no hidden modulus, resonance, or
rank-drop leaves.

## Scope audit

The theorem is correctly restricted to
\[
 H_4=((p-q)^2,(p+q)^2,0),\qquad (H_3)_3=xq,
 \quad p=x^2,\ q=y^2+xz.
\]
Neither the note nor the verifiers promote this exact joint-orbit exclusion
to all line-\((2,2)\) leading forms.

The audit added one exposition sentence to the primary note explaining that
the omitted constant term is removed by target translation.  No theorem,
formula, verifier, or claimed scope required correction.

## Guards

Run:

```sh
./verify_hostile_strict.sh
./test_hostile_fail_closed.sh
```

The strict wrapper whitelists the complete transcript.  Four mutations
(raw minor, \(E_6\) minor, \(E_5\) literal, and completion marker) are
rejected.  The verifier also succeeds under optimized Python, showing that
its checks do not disappear with `assert`.

This audit is exact evidence about the encoded algebra, not peer review.
