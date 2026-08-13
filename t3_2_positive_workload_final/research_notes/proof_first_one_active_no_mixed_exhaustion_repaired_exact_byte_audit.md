# Exact-byte hostile audit of the repaired one-active no-mixed exhaustion

**Independent proof-first audit, 2026-08-12 PDT.**  This audit freezes the
exact target

```text
research_notes/proof_first_one_active_no_mixed_exhaustion_repaired.md
SHA-256 9fb1828f5660ffae83e6e1a08a0cb33ce8bd2813d7394a90187d9bccc64895c4
361 lines, 13182 bytes
```

and its load-bearing stochastic dependency

```text
research_notes/proof_first_one_active_bellman_flat0_prelude_repaired.md
SHA-256 f8ad11189d41fc5f1d09d0cf306c90d77a9b2b4b18cd00fe3dc06918d762c19b
```

The verdict is **STRICT PASS** at these exact bytes.  The scope is the
terminal one-active branch for support pairs which are globally nonmixed in
the exact raw two-active classifier.  A pair with any mixed cell must first
be routed to its completed pair-level theorem, as the target explicitly
requires.

## 1. Independent literal universe replay

The binary universe has 1,013 supports of size at least two and 23,436
unordered disjoint support pairs.  For each of the three active-coordinate
pairs, the audit applied the frozen ordered classifier in the seven cells
represented by

\[
 (1,1),(2,3),(1,2),(1,3),(3,2),(2,1),(3,1).
\]

Thus coordinate exchange was included literally.  Requiring equal
available/shielded output for the two supports in all 21 cells leaves exactly
9,489 globally nonmixed pairs.

With masks traversed in increasing integer order, unordered pairs stored in
that order, each support encoded by its displayed complex-name list, and
compact JSON used for the sorted row list, the independent set fingerprint is

```text
2271e87dd16daddd0731a45274af0c7f47f775565cf2ea00d2505a71a3ab9095
```

The first-category histogram is exactly

\[
\begin{array}{c|rrrrrrrr}
&Q/B&Q/F0&Q/F1&B/B&B/F0&F0/F0&F0/F1&D/F0\\ \hline
\#&6050&1352&54&1224&731&19&54&5.
\end{array}
\]

There are no D/B, D/D, or B/F1 pairs.  This independently reproduces every
entry and the total in (7.1).

## 2. Dormant support classification

After Q, F0, F1, and B fail, binaryity leaves exactly the three D shapes in
(2.4).  If the degree-one block contains (X), coordinatewise dominance is
automatic and the linkage is B.  If it contains (X+U), B-failure excludes
every lower complex carrying (U); the (X+V) statement is symmetric.  If
both mixed degree-one complexes occur, the only possible lower complex is
zero.  No fourth shape exists.

For the single-token shape

\[
 \{X+U\}\cup S,\qquad\varnothing\ne S\subseteq\{0,V,2V\},
\]

the audit replayed all seven rows of (3.2).  Each displayed first-cell status,
every complete survivor list, and every second-cell opposition is exact.  In
the first row both surviving partners are available where the D support is
shielded; in the other six rows all survivors are shielded where it is
available.  The symmetric single-token shape is therefore mixed as well.

The only possible D support is consequently

\[
 L_D=\{0,X+U,X+V\}.
\]

## 3. Exact five partners and invariant

Deleting (L_D) leaves

\[
 \{X,U,V,2X,2U,U+V,2V\}.
\]

On the (UV) equality wall, an S partner must be contained wholly in one of
the unary, quadratic, or bounded-(X) shells.  The bounded-(X) shell stays
shielded in both open chambers and is excluded.  The unary shell supplies
\(\{U,V\}\); the quadratic shell supplies its three two-vertex subsets
and full three-vertex support.  These are exactly the five partners in (4.1),
and the independent 9,489-row replay returns exactly those five D/F0 pairs.

Every reaction in both linkages preserves

\[
 H=X-U-V.
\]

With (U,V) bounded and (H) fixed on the communicating class, (X) is
bounded.  This branch uses an exact physical invariant, not a potential
handoff.

## 4. F1/B separation and remaining categories

The audit replayed every cell of (5.1).  The first two F1 shapes have no
disjoint B partner with the same displayed shielded status.  For
\(\{X+U,X+V\}\), the sole equality-wall survivor is \(\{0,X\}\), and
the second displayed (UV) cell separates it.  The three-vertex F1 shape
uses the whole degree-one menu and leaves no disjoint B support.  Hence a
globally nonmixed B/F pair is B/F0.

The resulting alternatives are exhaustive and disjoint under the stated
priority:

1. Q;
2. flat/flat;
3. B/B;
4. B/F0; or
5. one of the five D/F0 invariant pairs.

## 5. Analytic and stochastic interfaces

For Q, a nonzero outgoing edge from the enabled source $2X$ contributes
$-\Theta(X^2\log X)$ to factorial entropy.  Every other source contributes
at worst $O(X\log X)$ in the fixed inactive box.  Strong connectivity
guarantees such an outgoing edge, so the generator is coercively negative.

For flat/flat, every reaction preserves (X) exactly.  Different constant
active degrees in the two linkages do not affect that conclusion.

For B/B, the target does not silently invoke the formal two-active statement
of the marked theorem.  Section 2 of the pinned f8ad prelude explicitly
reproves the dimension-free identity, actual-target simple path, all-clock
Bellman recursion, one-active endpoint bound

\[
 p_c(x-t+c)=O(X^{-1}),
\]

bounded episode depth, positive endpoint moments, and physical-duration
moments.  Both linkages use the same proper marked potential.

For B/F0, the pinned prelude gives exit-first disjoint absorption, an
(X)-independent finite transient phase before top access, an exactly-once
degree-zero launch handoff, coercive top/Bellman reward, and the exhaustive
negative-or-exit-or-finite-class split.  It assumes no uniform activation
probability.

The composition is chart local.  A physical structural exit contradicts
terminality; the proof does not follow the endpoint into another chart and
switch potentials there.  Thus it makes no unsupported global common-(W)
claim.

## 6. Render replay

The exact target was independently rendered with Pandoc's single-backslash
TeX-math reader, both to MathJax HTML and through Tectonic to PDF.  Tectonic
produced zero stderr bytes.  The seven-page
letter-sized PDF was visually checked page by page; all tables, fingerprints,
equation tags, and theorem blocks render without clipping or overflow.

## 7. Frozen verdict

**STRICT PASS** for SHA-256

\begingroup\scriptsize\ttfamily
9fb1828f5660ffae83e6e1a08a0cb33ce8bd2813d7394a90187d9bccc64895c4
\par\endgroup

The support exhaustion is exact, the five residual pairs have a literal
class invariant, and the only stochastic residual is covered by the
separately frozen and exact-byte-audited f8ad prelude.
