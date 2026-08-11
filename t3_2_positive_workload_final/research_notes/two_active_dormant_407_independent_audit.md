# Independent audit of the frozen hard-interface candidate

Audit timestamp: 2026-08-10 22:04 PDT.

## Verdict

**FAIL as written; analytic repair open.** The exact 407-row selector, the
333-pair union, and the 951-to-317 promotion map replay correctly. The
arbitrary-orientation resistance graph also survives the bounded attacks
below. However, Lemma 7.1 is false with its stated uniform quantifier, and
the pathwise implication used in (8.6) has an exact physical counterexample.
These are proof failures, not a counterexample to recurrence or to T3-2.
All analytic, pair-level, and global flags must remain false.

The audited snapshot hashes were:

    theorem note  35108f62939202b2da02907b4d0171d80578c4a3bbcbccac31ad40b1f73c1500
    certificate   616519a6fcec5d0fd219faad65e5846cd03118d8bb2e2ba47af7ec67e448e315
    focused tests 89f98e9fcce339b979c141eb40d31a2205f266b127d4e40ba824ff2af602dd61

## Evidence that passed

- The focused frozen suite passes 6/6 tests.
- Counts and fingerprints replay for 407 incidences on 333 pairs and 951
  generalized one-active rows mapping three-to-one onto 317 exact hard
  targets.
- A separate maximal-edge search over all 188 normalized hard templates
  finds no positive base return through the claimed down resistance.
- A separate search of all 1,470 pairs of directed Hamilton cycles reproduces
  down resistances 0, 1, and 2 with no bounded violation of the strict upward
  gap.
- The directed-cut argument for existence of a down path remains credible:
  the nonexceptional maximal source must cut to strict service, while the two
  exceptional lower supports force the stated resistance-one or
  resistance-two cut. No Hamilton-cycle assumption is needed for that
  argument.
- The exceptional proper phase is exactly the birth-death chain in (5.2),
  and its factorial product tail is consistent with the claimed fixed-order
  cofactor moments.

The path searches are regressions, not an analytic proof of an unbounded
state-space theorem.

## Exact failure of Lemma 7.1

Use the physical row

    L+ = {A,B,AC},   L0 = {0,2B,AB},
    weight = (0,0,1), caps = (0,0,2),

or, in the note's normalization,

    L+ = {U,I,V+I},  L0 = {0,2U,U+I}.

Take the complete digraph on each linkage; it is strongly connected. From
the zero spectator state, the physical word

    0 -> U+I,  U -> V+I,  I -> U,  I -> U

visits the normalized states

    (U,relative V,I):
    (0,0,0), (1,0,1), (0,1,2), (1,1,1), (2,1,0).

It therefore reaches a no-fast base with positive old-`V` debt and `U=2`.
Repeating the neutral reaction `0 -> 2U` gives historically consistent
positive-debt bases `U=2+2k` of arbitrary size. Choosing, for example,
`U_n` of order `log n` remains inside a one-active tier but makes the first
summand `(1+U_n)^r` in (7.2) diverge. Hence the asserted uniform Green bound
cannot hold.

A viable repair must be start-weighted. It must also remember that cap 2 is
an availability class and may represent an unbounded subpower spectator; it
is not the fixed population two. The prefactor must be carried through the
perturbation, endpoint, duration, and moving-boundary estimates.

## Exact failure of the pathwise step (8.6)

In the same complete strong orientation, the word

    0 -> 2U,  0 -> U+I,  V+I -> U

visits

    (0,0,0), (2,0,0), (3,0,1), (4,-1,0).

The last edge is the first strict old-`V` service, but

    Delta(3V+U) = 3(-1)+4 = +1.

Thus old-active service does not imply a pathwise decrease of the promoted
workload. The common-potential proof needs a signed, start-weighted
expectation estimate for spectator entropy; (8.6) cannot supply it.

## Ordered-tail issue

Equation (5.8) controls the unweighted mass of the remainder after three
paid insertions because the residual Markov kernel has mass at most one.
It does not, without another weighted Green estimate, imply (6.3) with
`(1+J+I+tau)^r` for every fixed `r`. A deterministic cutoff would otherwise
cost a factor `L_n^r`.

This looks repairable for the boundary contribution: use the unweighted
three-insertion probability and the deterministic bound
`Delta F = O(L_n log s_n)` at the included boundary jump. Alternatively,
prove a genuine weighted tail kernel after the third insertion. The present
display does neither.

## Scope check

The candidate does not overclaim all-active compatibility: it explicitly
leaves all-active and global composition open. Its use of an arbitrary fixed
`ell` would be compatible with a later common-potential choice if the
start-weighted one-active repair succeeds.

Reproduce this audit with:

    PYTHONPATH=src python3 -B src/two_active_dormant_407_independent_audit.py
    PYTHONPATH=src python3 -B -m unittest \
      tests/test_two_active_dormant_407_independent_audit.py -v
