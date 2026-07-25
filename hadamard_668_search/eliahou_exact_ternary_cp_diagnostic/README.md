# Case-1 exact ternary CP-SAT diagnostic

This package tests the exact 78-trit fold-plus-causal formulation
for open Eliahou long case 1 (`L`, reciprocal `q` index 2).  It is a
bounded diagnostic only.  It constructs no base sequence or `H(668)`,
and neither of the two `UNKNOWN` results excludes a root profile.

## Exact model

For every eligible support cell `j`, the model uses endpoint Booleans

```text
lower_j + upper_j <= 1,
u_j = lower_j + upper_j,
t_j = lower_j - upper_j.
```

It imposes, over the integers:

```text
sum u_j = 39
4 exact signed root-profile equations
20 anti-fold equations
21 plus-fold equations
41 causal equations C_43,...,C_83
```

The lag-83 causal equation is a tautology in this case, but it is retained
in the requested-equation inventory.  Every distinct Boolean conjunction
is created once and shared among all equations.  The resulting model for
either root profile has:

```text
78 ternary coordinates
156 endpoint Boolean variables
5,928 shared Boolean conjunctions
6,085 CP-SAT proto variables, including one constant
17,949 proto constraints
  17,863 Boolean clauses
      86 linear constraints
18,407 nonconstant equation occurrences before CP-SAT presolve
```

The source ternary polynomials, their Boolean expansions, and the direct
four-sequence correlations agreed in `4,080` scalar checks from 24
deterministic random ternary assignments.

If CP-SAT reports a model, the script reconstructs the original physical
lengths `84,84,83,83`, checks all 83 nonzero aperiodic correlations, the
shell, and the four exact roots.  No candidate is accepted from the solver
alone.

## Bounded case-1 run

On 2026-07-25, using OR-Tools 9.14.6206 with four workers:

```text
profile 0 = ((-3,4),(-5,-4))
  status                  UNKNOWN
  elapsed                 300.03 seconds
  peak process RSS        277.13 MB
  reported branches       51,133
  reported conflicts      2,891
  physical replay         not applicable (no model)

profile 1 = ((6,-5),(4,5))
  status                  UNKNOWN
  elapsed                  62.68 seconds
  peak process RSS        321.83 MB
  reported branches       1,788,048
  reported conflicts      649,592
  physical replay         not applicable (no model)
```

The second run was deliberately interrupted after the first full profile
showed no useful contraction.  OR-Tools returned a normal `UNKNOWN`
response on interruption.  Its faster branch/conflict rate shows a large
heuristic difference between the two root profiles, not mathematical
progress toward SAT or UNSAT.

## Proof-capability assessment

A proof-capable Boolean/pseudo-Boolean encoding is mechanically plausible:
each of the 5,928 shared products needs three clauses, endpoint exclusion is
clausal, and the remaining conditions are 87 requested integer equalities
(one tautological).  Most divided coefficients have magnitude one or two;
the largest is 126.

The bounded CP-SAT run does **not** make a proof search look tractable.
Profile 0 remained `UNKNOWN` after five minutes with very weak global
contraction.  Translating this raw system to CNF plus DRAT/LRAT would be
technically straightforward, but there is no current evidence that its
UNSAT proof would fit host-scale time or storage.  A new mathematical
decomposition or contraction should precede any proof-producing run.

## Reproduction

From the repository root:

```text
PYTHONDONTWRITEBYTECODE=1 \
  /Users/alec/Documents/tmp/hadamard-env/bin/python \
  hadamard_668_search/eliahou_exact_ternary_cp_diagnostic/diagnose_case1_cp_sat.py \
  --audit-only --random-audit-samples 24
```

To repeat the completed bounded profile:

```text
PYTHONDONTWRITEBYTECODE=1 \
  /Users/alec/Documents/tmp/hadamard-env/bin/python \
  hadamard_668_search/eliahou_exact_ternary_cp_diagnostic/diagnose_case1_cp_sat.py \
  --profiles 0 --seconds 300 --workers 4 --random-audit-samples 24
```
