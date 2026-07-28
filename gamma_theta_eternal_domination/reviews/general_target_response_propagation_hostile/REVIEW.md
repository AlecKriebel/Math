# Hostile review: general target-response propagation

Review date: 2026-07-28 PDT

Target:
`math/lemmas/general_target_response_propagation.md`

Target SHA-256:
`d6a0ec8a7daff1cca0094e1929134507364cea3c2c8781fbe24956a3238048d8`

Research-log SHA-256:
`c0d0455c1464da1a2c84e81d2fa6629c76e0899f19bbcf1e0a7648f87d1b271f`

## Verdict

**UNCONDITIONAL PASS.**

The general vertex-star theorem, the equality-family active-set
corollary, componentwise responder-color propagation, the exact
inactive-set identities (17a)--(17d), the common-color extension theorem,
and the general critical full-target obstruction are correct as stated.
The research log accurately describes the proof and its boundary.

I found no occupied attack, multi-guard move, illegal mover, missing
domination rejection, active-set ambiguity, complement reversal,
greatest-family substitution, coloring error, unsupported well-covered
step, or hidden use of the gamma--theta conjecture.  The result is an
all-\(k\) conditional structure theorem; it does not produce the missing
global responder color and does not resolve the conjecture.

## 1. Exact-model and induction audit

I audited the proof against the literal one-guard closure condition

\[
 \forall D\in\mathcal F\ \forall r\notin D\
 \exists u\in D\cap N_G(r):
 (D-\{u\})\cup\{r\}\in\mathcal F.
\]

Every state in \(\mathcal F\) dominates, and \(\mathcal F\) is an
arbitrary eternal family rather than the greatest eternal family.

For the forward implication, write

\[
 A=(T\cap T')-\{v\},\quad O=T-T',\quad B=T'-T.
\]

The four sets \(\{x\},A,O,B\) have exactly the disjointness used in the
proof, and \(|O|=|B|\).  At step \(j\), the proposed state

\[
 D_{j-1}=\{x\}\cup A\cup\{b_1,\ldots,b_{j-1}\}\cup O_{j-1}
\]

does not contain \(b_j\), so the attack is unoccupied.  Every guard in
\(A\cup\{b_1,\ldots,b_{j-1}\}\) lies with \(b_j\) in the independent set
\(T'\), and therefore has no move edge.  If \(x\) moves, every remaining
guard lies in \((T\cup T')-\{v\}\), all of whose vertices are
nonadjacent to \(v\).  That successor fails to dominate \(v\) and cannot
belong to \(\mathcal F\).

Thus every legal retained response comes from \(O_{j-1}\).  Closure
guarantees at least one such response.  The proof does not require the
mover to be unique: whichever retained response closure supplies removes
one old vertex and preserves the displayed invariant.  After \(|B|\)
steps the old set is empty and the state is exactly \(T'-v+x\).
Reversing \(T,T'\) is legitimate and proves equivalence.

The edge cases are harmless:

- if \(T=T'\), then \(m=0\) and the conclusion is tautological;
- for \(k=1\), two retained singleton states sharing \(v\) are equal, so
  again \(m=0\);
- larger overlaps merely enlarge \(A\), whose guards are correctly frozen
  by independence of \(T'\);
- \(x\notin T\cup T'\) and \(B\cap D_{j-1}=\varnothing\) prevent state or
  attack collisions.

No step assumes optimality, connectedness, a minimum counterexample, or a
greatest fixed point.

## 2. Equality corollary and the physical active set

The imported maximum-independent-state fact is valid for every eternal
\(k\)-family.  Starting in any retained state and attacking the
unoccupied members of an independent \(k\)-set increases the number of
guards on that set by one at each response.  Hence every independent
\(k\)-set belongs to the arbitrary family \(\mathcal F\) when
\(\alpha(G)=\gamma^\infty(G)=k\).

The vertex-star theorem then makes membership in \(A_x\) independent of
which independent \(k\)-state containing the physical vertex is chosen.
Equation (12) is exact.  If \(T-v+x\in\mathcal F\), that successor must
dominate the omitted vertex \(v\); every member of \(T-\{v\}\) is
nonadjacent to \(v\), so \(vx\in E(G)\) is forced.  Nonemptiness is the
literal response requirement for the unoccupied attack at \(x\).

This remains family-relative throughout.  In the final full-target
corollary, “full response” is consequently read relative to the fixed
family \(\mathcal F\) already in scope; no greatest-family fact is
silently imported.

## 3. Ridge exchanges and \(k\)-coloring

For ridge-adjacent facets

\[
 T=U\cup\{p\},\qquad T'=U\cup\{q\},
\]

the active status of every member of \(U\) is synchronized by the
vertex-star theorem.  The exchanged successors are the literal same set

\[
 T-p+x=U\cup\{x\}=T'-q+x.
\]

If this set is retained, its domination of \(p\) forces \(px\in E(G)\)
because every vertex of \(U\) is nonadjacent to \(p\); the same argument
forces \(qx\in E(G)\).  Thus the exchanged vertices have identical active
status, not merely equal graph adjacency.

Each independent \(k\)-set is a \(k\)-clique of
\(H'=\overline{G-x}\).  A proper coloring with exactly \(k\) available
colors gives every such facet all \(k\) colors.  The ridge \(U\) uses
\(k-1\) colors, so \(p\) and \(q\) receive the same unique remaining
color.  This proves exact invariance of the active-color set along every
ridge path.  The argument also covers \(k=1\): \(U=\varnothing\), all
singleton facets have the sole color, and the common-successor argument
is unchanged.

If a complement neighbor \(r\) of \(x\) is in a component support, then
\(r\notin A_x\).  In a containing rainbow facet it is the unique vertex
of its color, so that color is absent from the component responder set.
This proves (16) with the graph/complement direction correct.

## 4. Exact inactive-set identities

Let \(R_x=V(G-x)\setminus A_x\).  Fix a component \(C\) and a color \(c\).
Componentwise invariance and the rainbow property give the exact
equivalence

\[
 c\in A_C^\kappa
 \quad\Longleftrightarrow\quad
 \text{every \(c\)-colored support vertex of \(C\) lies in \(A_x\)}.
\]

The reverse direction is not vacuous: every facet contains one
\(c\)-colored vertex.  Therefore

\[
 A_C^\kappa
 =
 [k]\setminus\kappa(R_x\cap\operatorname{supp}(C)),
\]

which is (17b).

If the component supports cover all deletion vertices, De Morgan's law
gives

\[
 \bigcap_C A_C^\kappa
 = [k]\setminus
   \bigcup_C\kappa(R_x\cap\operatorname{supp}(C))
 = [k]\setminus\kappa(R_x).
\]

Support overlap causes no problem because the right operation is union.
The intersection is nonempty exactly when \(\kappa(R_x)\) omits at least
one of the \(k\) colors, equivalently when it uses at most \(k-1\)
distinct colors.  The note correctly makes support coverage an explicit
hypothesis; unsupported inactive vertices are not inserted into (17c)
without justification.

Finally, every \(k\)-clique of \(H'\) is an independent \(k\)-set of
\(G-x\), and (12) makes it meet \(A_x\).  Hence no \(k\)-clique lies
inside \(R_x\), proving
\(\omega(H'[R_x])\le k-1\).  For \(k=1\), this says \(R_x\) is empty on
the deletion support and uses the standard \(\omega(\varnothing)=0\)
convention.  For \(k=3\), it is exactly the claimed triangle-free
consequence.

## 5. Common-color extension and well-covered support

Under

\[
 \gamma(G-x)=\alpha(G-x)=\gamma^\infty(G-x)=k,
\]

the parameter chain forces \(i(G-x)=k\).  Since every maximal independent
set has size between \(i\) and \(\alpha\), every maximal independent set
of \(G-x\) has size \(k\).  Extending a singleton to a maximal independent
set therefore puts every deletion vertex in an independent \(k\)-facet.
This is the exact support-coverage step used by the extension theorem.

If \(w\) is in every component responder set, take any deletion vertex
\(v\) of color \(w\) and a facet containing it.  That facet is rainbow,
so \(v\) is its unique \(w\)-colored member and must lie in \(A_x\).
Thus \(vx\in E(G)\), or \(vx\notin E(\overline G)\).  No deletion vertex
of color \(w\) is a complement neighbor of \(x\), and assigning color
\(w\) to \(x\) is proper.  This gives \(\theta(G)\le k\), while the
retained equality setup gives \(\alpha(G)=k\le\theta(G)\), hence
\(\theta(G)=k\).

No assumption that a proper coloring is unique is made or needed.  The
only uniqueness used is the elementary fact that within a rainbow
\(k\)-facet there is one vertex of each color.

## 6. The at-least-three-component corollary

In the critical branch, deletion equality supplies a proper deletion
\(k\)-coloring and the support coverage required above.  A full response
at the root state \(S\) puts all \(k\) colors in the root component set.
Equation (16) then makes the root support disjoint from
\(N_{\overline G}(x)\).  Every component responder set is nonempty by
eternal closure.

If the total intersection were nonempty, the extension theorem would
give \(\theta(G)=k\), contradicting the strict inequality in (21).  With
one component the intersection is all \(k\) colors.  With exactly two,
intersecting the all-color root set with the nonempty nonroot set leaves
that nonroot set.  Both cases contradict empty total intersection, so at
least three components are necessary.  This reasoning is valid for every
\(k\ge1\), including the conditionally vacuous \(k=1,2\) counterexample
branches.

## 7. Independent bounded exhaustive audit

The clean-room checker
`reviews/general_target_response_propagation_hostile/independent_check.py`
imports no campaign evaluator or target proof code.  It enumerates every
labeled graph through order five:

\[
 \sum_{n=1}^{5}2^{\binom n2}=1{,}099.
\]

For every graph and every \(1\le k\le n\), it enumerates every nonempty
subset of the dominating \(k\)-configurations and retains exactly those
subsets satisfying the literal one-guard closure condition.  It therefore
tests arbitrary eternal families, not just greatest fixed points.

The strict deterministic run checked:

| quantity | count |
|---|---:|
| labeled graphs | 1,099 |
| arbitrary eternal families | 60,011 |
| equality families \(\alpha=k\) | 11,257 |
| active incidences | 86,954 |
| cross-state vertex-star comparisons | 5,864 |
| replayed forced transport paths | 57,622 |
| replayed forced attacks | 7,680 |
| equality target facets | 33,234 |
| rainbow facet checks | 357,022 |
| ridge-exchange checks | 17,913 |
| component-invariance checks | 17,184 |
| complement-neighbor checks | 184,876 |
| component inactive-identity checks | 339,838 |
| global inactive-identity checks | 19,018 |
| inactive \(K_k\)-free checks | 27,464 |
| deletion-coloring instances | 336,298 |
| common-color extension witnesses | 25,970 |
| failures | 0 |

The arbitrary eternal-family totals by guard number were:

| \(k\) | eternal families | equality families |
|---:|---:|---:|
| 1 | 5 | 5 |
| 2 | 1,984 | 1,914 |
| 3 | 42,646 | 9,021 |
| 4 | 14,352 | 316 |
| 5 | 1,024 | 1 |

The checker explicitly replayed the induction, verifying that each attack
was unoccupied, frozen guards had no move edge, an \(x\)-move failed
domination, every retained mover came from the current old set, and the
active-set equality reached the stated destination.  It separately
checked the literal common successor on each ridge exchange, the
rainbow-\(k\) property, (17b), (17c), (17d), and every finite instance of
the extension conclusion.

No graph through order five met all strict-counterexample hypotheses of
the final full-target corollary.  That corollary's verdict therefore rests
on the direct proof in Sections 5--6, not on a claimed positive finite
instance.

Reproduce with:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/general_target_response_propagation_hostile/independent_check.py
```

The exact command, counts, and source hashes are recorded in
`evidence.json`.

## 8. Scope and claim discipline

The source correctly states its boundary.  It proves that a common
responder color would extend a deletion coloring and gives an exact
inactive-set reformulation, but the bound
\(\omega(H'[R_x])\le k-1\) does not imply that \(R_x\) uses fewer than
\(k\) colors in the chosen coloring.  The required global color
intersection remains open.  No clique partition, universal theorem, or
conjecture resolution is claimed.
