# Independent verification: Kourovka Notebook 16.45

Publication edition: 1.0.0, 21 September 2026 (America/Los_Angeles).
Audit execution timestamps are recorded in UTC, on 22 September 2026.

## Verdict and exact scope

The structural argument and independently reconstructed finite calculations
support the claimed counterexample:

    G = F_29^2 ⋊ <[[0,28],[1,0]], [[2,7],[12,28]]>,
    |G| = 100920,  b_f(G) = b(G) = 3 < 4 = mu′(G).

The base invariant includes all permutation representations, including
nonfaithful and intransitive actions. A base has stabilizer equal to the
action kernel. The independence invariant allows sets that do not generate
the ambient group. These match Cameron's question. No minimum-order claim
is made. The audits are independent AI work lanes within one Codex task;
they are not external human peer review or formal proof certification.

## Review families

| Family | Mechanism and evidence | Status | Remaining gap |
|---|---|---|---|
| Structural | Re-derive subgroup/base correspondence; classify subgroups missing V; prove the normal-subgroup reduction | Supports theorem; see structural_referee.md | No substantive gap identified |
| Exact computation | New implementation from the mathematical specification, before reading bundle code; exhaustive complement lattice and explicit affine closures | PASS; see independent_computation.md and independent_check_results.json | Does not encode the universal structural proof |
| Original sources | Official September 2026 notebook and Cameron's 2010, 2014, and 2024 accounts | Conventions confirmed; see source_referee.md | Priority search is bounded, not exhaustive |

## Correction made before publication

The supplied manuscript stated that R2 R3, R1 R3, R1 R2 have orders 4, 6, 10.
Their actual orders are **4, 3, 10**. The projective product orders are 2, 3,
5 and the generated pair subgroup orders remain 8, 12, 20. This is a factual
correction to a supporting sentence; it changes neither the construction nor
any theorem. The current manuscript includes the corrected orders.

Other revisions supply author/ORCID metadata, a proof overview, attribution of
the foundational subgroup formulations, Cameron's 2024 published discussion,
explicit review limits, and reproducibility instructions. The complement-core
argument now follows directly from the already proved normal-subgroup lemma.

## Checkable evidence

The new checker reconstructs 120 matrices and all 76 actual subgroups. It
checks 1,215,450 proper-subgroup quadruples and finds no irredundant one;
among 67,525 triples it finds 900 irredundant triples and no faithful one.
All 30 line stabilizers have order four. It checks the SL(2,5) isomorphism
on all 14,400 products. Affine closures reproduce order 100,920 and omission
orders 120, 6,728, 10,092, 16,820. The faithful three-family has subgroup
orders 58 and pair intersection orders two. The characteristic-11 example
has deletion intersection orders 11, 11, 5, 2, confirming the stated boundary.

The all-actions upper bound is mathematical: every subgroup missing V has
faithful base invariant at most two; the restriction lemma bounds faithful
bases by three; every nontrivial normal subgroup contains V, reducing the
remaining actions to the complement. No full subgroup enumeration of G,
floating-point optimization bound, catalogue identification, or unproved
generalization in the characteristic is used.

## Reproduce

From the project directory, run:

```sh
make verify
python3 audit_2026_09_21/independent_check.py
python3 audit_2026_09_21/structural_check.py
```

Use ordinary Python (not `python -O`) for the additional audit scripts,
which contain assertions. The supplied principal verifier uses explicit
checks even under optimization. Rerunning audit scripts updates their dated
result files. No external person was contacted in this audit.

## Fresh extracted-package check

The source ZIP was extracted into a new directory. All supplied checksums
passed before execution, and `make audit` completed successfully, including
all three additional audit/comparison commands. The separate delivery log
records this check. The final nine-page PDF was rendered and visually reviewed;
the final compiler log has no warnings or unresolved references.
