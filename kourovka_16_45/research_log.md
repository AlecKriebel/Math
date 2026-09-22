# Research and verification log

Session date: 19 September 2026. This log records work actually performed;
it does not claim external review, background activity, or unrun experiments.

## 1. Source audit and reduction

Read the current official notebook, September update, Cameron's 2010
exposition, and the 2014 manuscript/exposition. Fixed the correspondence
b = Cameron b_2 and mu' = Cameron mu*. Established the coset-union subgroup
characterization, c_cap = mu', and the restriction lemma. Kept arbitrary,
normal, and trivial intersection bottoms separate throughout.

## 2. Exploratory exact lattices plus non-certifying optimization

Constructed groups and multiplication tables directly, enumerated actual
subgroups in C++, and used a SciPy MILP model to discover intersection ranks.
Actual completed examples and exploratory (mu', b, b_f) results were:

| Case | Group order | Exploratory ranks |
|---|---:|---|
| C1 | 1 | (0,0,0) |
| C6 | 6 | (2,2,2) |
| Q8 | 8 | (2,2,1) |
| Q8 x C2 | 16 | (3,3,2) |
| D8 | 8 | (2,2,2) |
| S3 | 6 | (2,2,2) |
| A4 | 12 | (2,2,2) |
| S4 | 24 | (3,3,3) |
| A5 | 60 | (3,3,3) |
| UT4(2) | 64 | (4,4,4) |
| SL2(3) | 24 | (2,2,2) |
| GL2(3) | 48 | (3,3,3) |
| SL2(5) | 120 | (3,3,2) |
| PSL2(7) | 168 | (4,4,4) |
| S5 | 120 | (4,4,4) |

These runs are recorded in the exploratory result JSONs and
`logs/examples_initial.log` / `logs/examples_second.log`. The MILP outputs
were used to find structure, not as premises of the final upper bound.
Some other case names exist in the driver but were not run.

Q8 demonstrated that a faithful-only gap is insufficient: its quotient by
the center supplies the missing all-actions rank. SL2(5) supplied the more
useful pattern mu' = b = 3 but b_f = 2. Its unique involution forces a
faithful intersection family to include an odd-order subgroup, and those
subgroups have prime order.

An attempted GAP installation was unsuccessful because the container's
package repository was not reachable. No GAP computation is claimed.
The supplied Python/C++ implementations replaced that optional approach.

## 3. Affine construction and the crucial line bound

Constructed matrix realizations of the binary icosahedral complement over
F29 and F11. Found an explicit independent triple with omission subgroup
orders 8, 12, and 20. In characteristic 29, all 30 projective-line stabilizers
have order 4; in characteristic 11, the 12 line stabilizers have order 10.
Data and discovery output are retained in the BI_29/BI_11 files and
`logs/affine_discovery.log`.

The structural explanation is injectivity of a line stabilizer into F_p^*.
At p=29 its order divides gcd(120,28)=4. A subgroup of the affine group that
intersects V in a line is consequently a faithful scalar extension of C29
by a cyclic 2-group, whose independence number is at most 2. Subgroups
meeting V trivially embed in the complement. This covers all subgroups
not containing V and yields the faithful bound 3 by restriction.

Irreducibility and C_G(V)=V show that every nontrivial normal subgroup
contains V. This is the step that covers all nonfaithful representations.
It is a proof about every normal subgroup, not a catalogue enumeration.

## 4. Witnesses and adversarial tests

Added one translation to the independent complement triple to get an
independent 4-set. It generates all 100920 affine elements. Its four omission
subgroups intersect in a nonnormal order-2 subgroup of the complement.
Their normal cores have orders 1,1682,1682,1682 and destroy rank-4 essentiality.

Constructed a faithful minimal 3-family of order-58 subgroups; every pair
intersects in a distinct involution subgroup and the triple intersection is 1.

Explicitly refuted an overbroad characteristic-independent version by
constructing a faithful minimal 4-family over F11. Its subgroup orders are
110,110,242,605, with deletion-intersection orders 11,11,5,2. This is included
in the final Python verifier and the proof, not merely a failed search.

## 5. Final exact certification

Wrote and ran standalone standard-library Python and independent C++17
verifiers. Neither reads a catalogue or a numerical optimizer's answer.
Each enumerates all 76 actual subgroups of the 120-element complement,
checks all 1,215,450 proper-subgroup four-families and all 67,525 three-families,
and verifies the matrices, line stabilizers, affine independent set, and
faithful base witnesses. Both report PASS.

A separate comparison converts both subgroup outputs to sets of actual
matrices; all 76 agree despite different element indexing and generation
order. The comparison script is included and was run successfully.

Two misleading-indentation compiler warnings in the initial C++ formatting
were corrected with braces and line breaks. The final compilation, with
-Wall -Wextra -pedantic, has no warnings, and the final verifier was rerun
successfully. Both the initial warning log and final empty warning log are
retained. No failed mathematical check occurred in the final verifiers.

The finite programs certify explicit finite premises. The complete upper
bound over all affine subgroup families is the structural proof in the
manuscript, not a full enumeration of the affine subgroup lattice.

## 6. Manuscript and handoff

Created `proof.tex` and compiled `proof.pdf` twice with pdfLaTeX. All eight
pages were rendered and visually inspected; no clipped text or broken
mathematical glyphs was observed. The source and compilation logs are kept.

The mathematical claim is resolved by the counterexample in this bundle.
No Lean proof was written or compiled, no external referee reviewed the work,
and no external contact, purchase, or publication occurred. Independent
rerunning and external mathematical review remain handoff actions, not
unproved lemmas hidden in the presented argument.
