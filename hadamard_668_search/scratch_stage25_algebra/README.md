# Stage-2.5 local algebra audit

## Verdict

The two stage-2.5 phase witnesses do **not** expose a singular component,
a common Hessian radical, or a viable Newton/Hensel contraction.  Their
local algebra instead looks like the generic overdetermined transition
predicted for digit 3.

This is a negative diagnostic, not an exclusion theorem.  More importantly,
both witnesses fail the independently certified row-margin/trivial-character
join.  They are points of the displayed phase system only, not viable
partial `LP(333)` lifts.

## Exact replay

The audit reads
`../phase_second_digit/higher_digits/stage_2_5_witnesses.json`, rebuilds the
first-digit affine chart and delayed `E1(origin)` hyperplane, and checks the
stored affine and placement hashes against exact phase arithmetic.

The preferred witness is candidate 0, profile `h2-222222-0`:

```text
affine hash:
ce5861a0988fbfec2f22cefd1f66e9c17fdeac934f0f83f2cfb6f700389dfa17

placement hash:
3e349b2e8dd9666d3bc2fffc74fbeef73badc2b17cdd61b2addf77f34c4a267c
```

Its delayed row has

```text
(A,Q)=(-9,0),
F=A+(3Q-A)omega=(-9,9),
lambda digits 0..8 = (0,0,0,0,0,2,1,1,1).
```

Thus that one row passes not only delayed digit 3 but also digit 4.  Eleven
of the other eighteen digit-3 cubics remain nonzero.  Candidate 2 provides
an independent comparison: its delayed row has `(A,Q)=(9,6)`, sixteen
other digit-3 cubics are nonzero, and its delayed digit 4 is nonzero.

## Certified local geometry

All ranks below are exact ranks over `F_3`.

| quantity | candidate 0 | candidate 2 |
|---|---:|---:|
| delayed-row ambient dimension | 35 | 35 |
| digit-2 Jacobian rank | 18 | 18 |
| digit-2 tangent dimension | 17 | 17 |
| restricted digit-2 Hessian ranks | `16^5,17^13` | `16^4,17^14` |
| common digit-2 Hessian radical | 0 | 0 |
| remaining-cubic Jacobian rank on tangent | 17 | 17 |
| full digit-2 plus remaining-cubic Jacobian rank | 35 | 35 |
| common cubic-Hessian radical on tangent | 0 | 0 |

Candidate 0's restricted cubic-Hessian ranks are
`15^1,16^8,17^9`; candidate 2's are `15^2,16^5,17^11`.
The stacked Hessian rank is 17 in both cases.

Candidate 0's extra delayed digit-4 equation is genuinely new at this
point:

```text
rank of its 35-variable polar form                 = 12
quadratic-function span rank, before -> after      = 18 -> 19
Jacobian rank with the digit-2 equations           = 19
extended tangent dimension                         = 16
remaining-cubic Jacobian rank on extended tangent  = 16
```

So even the extra zero digit contracts the tangent in the generic direction;
it does not reveal a flat family.

## Exact Newton obstruction

On each 17-dimensional digit-2 tangent, the eighteen remaining cubic
gradients have rank 17 and one row relation.  For candidate 0 the relation
is

```text
(2,0,0,2,2,1,2,2,2,1,2,1,0,0,0,0,1,1).
```

Its pairing with the current cubic residual vector is `1`, not zero.
Candidate 2 has the same one-dimensional obstruction, also with syndrome
`1`.  Therefore the complete first-order correction system is
inconsistent at both points.

Two finite checks sharpen this statement for candidate 0:

- Imposing the linearized corrections for all eleven currently violated
  cubics leaves an affine six-space.  Exact evaluation of all `3^6=729`
  points finds **no** digit-2 root.
- Of the eighteen leave-one-out cubic correction systems, twelve have a
  unique solution and six are inconsistent.  Every one of the twelve
  unique corrections fails the exact digit-2 equations.

For candidate 2, correcting its sixteen violated cubics leaves a line;
none of its three points is a digit-2 root.  Fourteen of its leave-one-out
systems have a unique correction and four are inconsistent; every unique
correction fails digit 2.

These are exact statements about the named affine sheets.  They do not
exclude other points of the 35-dimensional system.

## Low-degree consequence audit

Degree-3 XL on candidate 0's full delayed-row hyperplane has:

```text
35 variables
18 quadrics + 18 cubics
666 XL rows in 8,401 reduced monomials
full rank                         666
cubic projection rank            648
quadratic-or-lower intersection    18
linear-or-lower intersection        0
constant-only intersection          0
```

The eighteen quadratic-or-lower rows are exactly the original quadrics.
Thus this degree-3 span gives no refutation and no new linear or quadratic
consequence.  This matches the earlier profile-1 XL signature.  It says
nothing about consequences of degree 4 or higher.

## Interpretation

### Theorems/certificates from this audit

- exact replay of both stored phase witnesses;
- every displayed rank, radical dimension, and gradient relation above;
- inconsistency of the two full first-order correction systems;
- exhaustive failure on the explicitly defined correction sheets;
- absence of a degree-3 XL refutation or new lower-degree consequence.

### Heuristic interpretation only

- These regular, full-rank points give no evidence for an exceptional
  digit-2 component on which digit 3 collapses.
- Newton displacement from these points is a poor search direction.
- The shared rank pattern is evidence that the candidate-0 extra row digit
  is accidental rather than structural.

None of those interpretations proves that the digit-3 system is empty.
Because both points fail the row-margin join, this local analysis should
not receive further headline search time unless a row-compatible witness
with materially different geometry is found.

## Reproduction

The default command performs the exact replay, rank audit, degree-3
hyperplane XL audit, and the small correction-sheet enumerations:

```bash
python3 scratch_stage25_algebra/analyze_stage25_local.py --candidate 0
python3 scratch_stage25_algebra/analyze_stage25_local.py --candidate 2
```

The optional `--include-xl` flag attempts a substantially slower affine
substitution onto the tangent itself.  It is not needed for any conclusion
reported here.
