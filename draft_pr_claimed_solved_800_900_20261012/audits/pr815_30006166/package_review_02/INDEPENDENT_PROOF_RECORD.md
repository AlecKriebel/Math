# Independent proof reconstruction, sealed before prior verdicts

Recorded 2026-10-14 04:08:53 UTC. Scope: PR 815, upstream problem 30006166,
frozen head 5bee5139501a399da653f634147eab9433774ac7. I first read the current
complete note.tex and text of its five-page note.pdf. I have not read any prior
review verdict, previous_clear seal field, or priority-audit conclusion. I then
read the primary CJMST manuscript's exact Lemmas 2.2/3.1, Definition 3.2's
following paragraph, Corollaries 5.5/7.5, and Theorem 7.3.

## Exact statement and mechanism

The target is a dense G_delta in the full Polish space of continuous actions
of the restricted W = (direct sum over Z of Z) semidirect Z on Cantor space,
whose entire Borel orbit relation is hyperfinite. The auxiliary theorem covers
every Borel W-action admitting a Borel equivariant profinite shift height.
Freeness, minimality, a probability measure, and a conull/comeager phase-space
restriction do not occur. The proof uses imported deep Borel asymptotic-
dimension results, not amenability or a general hyperfinite-union principle.

## Independent deductions and attempted falsifications

1. The finite partition equations for a and t imply all W equations because
   those two elements generate W, including their inverses. For fixed c, their
   truth is locally constant under uniform homeomorphism perturbations: all
   c-fibers are clopen in compact Cantor space. Thus D(c,m) is clopen. There
   are only countably many finite-valued continuous c, since clopen subsets
   are finite unions of basis elements.
2. For a prescribed old equivariant c and m dividing n, the fiber product
   Y has the exact product action and every nonempty atom A of P lifts to
   n/m Cantor copies. An atom-preserving homeomorphism h exists. The first
   coordinate u of h(x) stays in the old P-atom, so alpha(g)u and alpha(g)x
   share a Q-atom; h^{-1} sends gamma(g)h(x) into the P-atom of alpha(g)u.
   A symmetric finite controlling set handles both maps and their inverses.
   This proves density without assuming alpha is free. Reducing h's second
   coordinate gives exactly the prescribed c, not merely an unrelated factor.
3. The countable intersection includes every c selected later. Starting with
   the unique mod-1 map and repeatedly lifting factorial quotients yields one
   compatible continuous p. Compact nonempty +1-invariant image is all of
   the inverse limit. No Borel selection of p in the parameter alpha is needed.
4. At each width m, normalization t^{-r_m(x)} gives a genuine Borel bijection
   with B_m times the m residues. Even if a lamp fixes a point, shift height
   prevents a nonzero-shift stabilizer and determines the coordinate r. The
   conjugation sign is a_{-r}, since t^{-r} a_0 t^r = a_{-r}. The rank-m lamp
   subgroup preserves B_m and may act nonfreely there.
5. The slab graph has degree at most four, so its finite-radius balls are
   finite. Its threshold relations are finite unions of partial move graphs;
   its extended path metric is Borel and proper. CJMST Corollary 5.5 explicitly
   covers any Borel action of a uniform-polynomial-growth group, hence Z^m.
   The paragraph after Definition 3.2 supplies uniformly finite finite-move
   components with fixed finite cover count; disjointization is legitimate.
6. A length-at-most-R slab path changes the base by at most ceil(R) letters
   of the m lamp generators. An R-chain of equal-color endpoints projects
   into one base monochromatic finite-move component; the connecting paths
   need not have that color. Its lifted component has at most m C_R points.
   A simple path in its threshold graph yields diameter at most
   R(m C_R - 1). This proves finite Borel asymptotic dimension with the same
   number of colors for each fixed m at every scale. It does not claim a
   dimension bound uniform across m. For 0 < R < 1 the integer-valued metric
   gives singleton threshold components.
7. For m dividing M, an M-cut is also an m-cut, so old edges persist and
   rho_M <= rho_m wherever old distance is finite. This is stronger than the
   exact next-stage finite supremum required by CJMST Theorem 7.3. That
   theorem allows the dimensions d_n to vary; its statement and proof use
   d_n separately. No freeness hypothesis occurs there.
8. A forward edge omitted at every factorial stage starts at height -1, by
   equality of all residues. Such a point and its entire orbit belong to
   p^{-1}(Z). Every edge in the invariant regular part eventually appears;
   a finite generator path has finitely many edges and hence fits in one late
   stage. Restriction to the invariant regular part removes no intermediate
   path. This gives the exact union relation needed by Theorem 7.3.
9. The embedded integers are a countable Borel subset; their preimage can be
   uncountable. On that full exceptional preimage, h is Borel and normalization
   q conjugates W-related points to N-related points. The converse follows
   by conjugating the N move back. Corollary 7.5 explicitly covers any Borel
   action of a countable local-polynomial-growth group, so E_N on B is
   hyperfinite. Pullback alone would have infinite fibers; the proposed H_j
   also bounds the integer height. Each fixed q=z has exactly one point at
   each height k, namely t^k z, giving finite band classes. H_j is an increasing
   Borel equivalence relation, covers every related pair at a sufficiently
   large stage, and handles all exceptional points. Empty pieces are harmless.
10. Disjoint union of the two invariant finite exhaustions proves the auxiliary
    theorem. The generic height lemma then gives the exact full target.

## Provisional mathematical finding

No counterexample, unsupported central reduction, circular step, quantifier
error, stabilizer issue, or metric-compatibility gap found in this independent
reconstruction. The proof is conditionally sound on the cited published deep
CJMST inputs, whose exact statements have been checked. This is manual
mathematical review, not formal proof-assistant verification. Further package,
primary attribution/priority, original-target, portability, and visual checks
are outstanding; no submission-readiness verdict is yet given.

Best-guess completion: 30% of this adversarial package-review assignment;
the original research attempt budget remains unchanged.
