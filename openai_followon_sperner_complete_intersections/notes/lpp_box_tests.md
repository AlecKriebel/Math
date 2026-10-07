# Independent bounded stable-set audit

Checkpoint: 2026-10-06 22:14 America/Los_Angeles (2026-10-07 05:14 UTC).
Completion estimate: 100% of this local audit, with no inference about completion of the overall research program.

**Verdict: no defect or counterexample found.** Lemma `box:inequalities` in the upstream `05-boxes.tex` passed a line-by-line proof review and independent exhaustive finite checks. The checks support the proof; they do not replace a universal proof.

Run `python3 notes/lpp_box_tests.py` to reproduce `notes/lpp_box_tests.json`. The standard-library script constructs each degree box and the graph of allowed unit transfers directly from the definitions. Stable sets are exactly upper sets in that graph. Including a vertex forces its upper closure, while excluding it forces its lower closure; recursively choosing the largest undecided lex vertex enumerates each stable set exactly once. For boxes of cardinality at most 12, direct scanning of all subsets independently verifies the enumeration and absence of duplicate sets.

The exhaustive domain is all bounds in `{1,2,3,4}^r`, `1<=r<=3`; `{1,2,3}^4`; `{1,2}^5`; Boolean bounds in 6, 7, and 8 coordinates; and `(1,1,1,1,1,2)`, `(2,1,1,1,1,1)`, `(4,1,3,2)`, `(2,4,1,3)`, `(3,2,4,1)`. Every degree from -1 through total capacity plus 1 is checked.

Receipt at 2026-10-07T05:13:56.357736+00:00: 205 bound tuples, 2,138 degree boxes, 63,319 stable sets; 1,558 boxes with bounds not nondecreasing; maximum degree-box cardinality 70; maximum stable sets in one box 9,304. No boxes skipped and no failed checks. There were 43,884 strict shadow comparisons and 39,456 strict comparisons of each endpoint slice.

Checks: all three advertised inequalities, lex initiality of every lex shadow, weak lex-order preservation of the largest-predecessor map, and `|shadow X|=|shadow' X(0)|+|X|-|X(b_r)|`.

## Proof review

1. Removing a unit from the last nonzero coordinate gives the largest predecessor and always respects the bounds. At a first lex difference, strict order can disappear only if the larger vector has one extra unit there and zero tail; equal total degree then forces one unit in the smaller vector's tail, and the predecessors agree. Empty shadows and negative degrees are covered separately.

2. Each slice is stable. Cross-slice shadow containment is exactly an allowed transfer from the last coordinate. Inductive shadow cardinality comparison implies compressed cross-slice containment because both sides are lex initial segments. No ordering of bounds occurs.

3. In the zero-slice argument, the largest omitted vector exists unless that slice is full. The tail-filling identity bounds the remaining units by `v_k-u_k`, which is at most the available capacity at coordinate `k`. All prescribed moves are allowed. They produce a member of the compressed zero slice at or below its largest omitted vector, contradicting its lex initial-segment property. If the preceding degree box is empty, its zero slice is already full and the separate full-slice case applies.

4. Reflection of the complement is stable: an upward transfer out of the reflected complement would reflect to an upward transfer from a member of the original set into its complement. Reflection reverses lex order, making the reflected complement of a lex initial segment a lex initial segment. Applying the already-proved current-dimension zero-slice comparison gives the top-slice comparison. This is not circular.

5. For a positive-last-coordinate shadow vector obtained by an earlier-coordinate multiplication, transfer a last-coordinate unit of its source to that earlier coordinate. The target is in the box, so capacity is available. Stability supplies the last-coordinate predecessor. Adding the last variable therefore bijects nontop members and shadow vectors with positive last coordinate. The zero-slice contribution is precisely the earlier-variable shadow of `X(0)`. The endpoint bounds and earlier-dimensional induction yield the advertised shadow bound.

The induction proves the zero-slice bound, then the top-slice bound, then the shadow bound in each dimension. It never uses an unproved shadow bound in the current dimension.

## Calibration and scope boundary

Stability is essential with arbitrary bounds. In bounds `(2,1)`, degree 1, the nonstable set `X={(0,1)}` has shadow `{(1,1)}`, whereas its lex replacement `Y={(1,0)}` has shadow `{(2,0),(1,1)}`. Thus arbitrary-subset shadow minimization would fail. This does not contradict the lemma: `X` fails the allowed-transfer stability hypothesis.

The local rank-deficit argument in `06-tor.tex` is valid. Each adjacent Koszul rank weakly decreases under a submodule inclusion or quotient map. The deficit is their sum, with the stated direct-sum, shift, and annihilation properties. The endpoint containments have the correct directions: the zero-slice lex endpoint is a submodule of the corresponding earlier-variable lex replacement, and the top-slice containment supplies the desired quotient map. The middle-layer annihilation follows from box stability, including the explicitly treated outside-box monomials. Reduction modulo the last variable is valid because that variable is injective on a polynomial-ring ideal; the coefficient-layer decomposition is linear over the earlier-variable ring.

This audit does not verify earlier reductions producing a box-stable ideal from an arbitrary ideal, or a global lex-plus-powers theorem relying on those reductions. That is the exact remaining scope boundary.
