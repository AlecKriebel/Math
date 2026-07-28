# Hostile review: full-target facet propagation

Review date: 2026-07-28 PDT

Target:
`math/working/full_target_facet_propagation/NOTE.md`

Target SHA-256:
`e3aabbc4ebc10f5039129b89c28873655114172124c2796e5f9abfaf19e216d7`

## Verdict

**UNCONDITIONAL PASS.**

Theorem 2.1, Definition 2.2 and its consequences, Theorem 3.1,
Corollary 3.2, Theorem 4.1, and Corollary 4.2 are correct in the stated
one-guard-moves model.  I found no occupied attack, all-guards
substitution, complement reversal, family/greatest-family conflation, or
circular use of the gamma--theta conjecture.

The note's boundary is also accurate.  It proves a new conditional
full-target structure theorem and isolates a global responder-color
intersection problem.  It does not prove the full \(k=3\) case or the
universal conjecture.

An earlier presentation ambiguity in the order-12 control was corrected
before this current-byte verdict.  There are no remaining findings.

## 1. Exact-model and dependency audit

I audited against the literal condition

\[
 \forall D\in\mathcal F\ \forall r\notin D\
 \exists u\in D\cap N_G(r):
 (D-\{u\})\cup\{r\}\in\mathcal F,
\]

where every state in \(\mathcal F\) dominates.  Every attack used by the
target proof is unoccupied, every retained successor differs in exactly
one guard position, and every rejected move is rejected because it is
either not along a \(G\)-edge or would produce a nondominating state.

The imported maximum-independent-state statement is exactly C-010.  Its
short proof applies to an arbitrary eternal family of triples: successive
attacks on unoccupied vertices of an independent triple increase the
number of guards on that triple by one, because a guard already on the
triple cannot answer.  Thus every independent triple is indeed in the
arbitrary family \(\mathcal F\) used here.

The two finite-control attributions are also within scope:

- C-060's accepted line-graph proof gives the one-guard equality for
  \(G=\overline{L(K_{3,3})}\), while the elementary three-edge-coloring of
  \(K_{3,3}\) gives \(\theta=3\).
- C-074 is the exact order-12 graph and greatest-family control; C-073
  supplies the accepted full-response-list framework.  The target does not
  transfer a greatest-family fact to an arbitrary family in a theorem.

Hashes of the exact accepted dependencies inspected are recorded in
`evidence.json`.

## 2. Theorem 2.1: vertex-star propagation

The proof correctly separates the only two nontrivial intersection sizes.

### Two shared vertices

With

\[
 T=\{v,u,p\},\qquad T'=\{v,u,q\},
\]

the hypothesis \(v\in L_T(x)\) puts
\(\{u,p,x\}\) in \(\mathcal F\).  The attack at \(q\) is unoccupied.
The guard at \(u\) is not adjacent to \(q\), since \(u,q\in T'\).  Moving
\(x\) would leave \(\{u,p,q\}\), which misses \(v\), since \(u,p\) are
nonadjacent to \(v\) in \(T\) and \(q\) is nonadjacent to \(v\) in \(T'\).
Eternal closure therefore forces the only remaining guard \(p\) to move
and retains \(\{u,q,x\}=T'-v+x\).  Closure itself supplies the otherwise
unstated edge \(pq\).

### One shared vertex

With

\[
 T=\{v,a,b\},\qquad T'=\{v,p,q\},
\]

start from \(\{a,b,x\}\in\mathcal F\) and attack \(p\).  An \(x\)-move
would leave a state missing \(v\), so one of \(a,b\) moves; relabeling the
chosen mover gives \(\{b,p,x\}\in\mathcal F\).  Now attack the still
unoccupied \(q\).  The guard at \(p\) cannot move because \(pq\notin E(G)\),
and an \(x\)-move would again leave a state missing \(v\).  Hence \(b\)
moves and \(\{p,q,x\}=T'-v+x\) is retained.

The edge \(vx\) is already part of the original response membership.
Interchanging \(T,T'\) proves the reverse implication.  No uniqueness of a
defender was assumed where closure allowed a choice.

Consequently the physical active set \(A_x\) is well-defined, every facet
meets it, and it is disjoint from \(N_{\overline G}(x)\), exactly as stated.

## 3. Theorem 3.1 and cross-component overlap

For a ridge exchange

\[
 T=\{u,v,p\},\qquad T'=\{u,v,q\},
\]

the two exchanged responses have the literal same successor
\(\{u,v,x\}\).  If that successor belongs to \(\mathcal F\), its domination
of \(p\) and \(q\) forces both \(px\) and \(qx\) to be \(G\)-edges, because
\(u,v\) are nonadjacent to each omitted vertex.  If it does not belong to
the family, neither exchanged endpoint is active.  Thus \(p\) and \(q\)
have the same active status.

In a proper three-coloring of \(H'=\overline{G-x}\), the common ridge
vertices use two colors and both exchanged endpoints use the third.
Therefore the responder-color set is exactly invariant along a ridge
step.  It is nonempty because every independent facet must answer the
attack at \(x\).

For (3.4), a complement neighbor \(r\) of \(x\) cannot be active.  In any
triangle containing \(r\), it is the unique vertex of its color; hence
that color cannot occur in the component responder set.  This also makes
Corollary 3.2 exact: when two ridge components share a physical support
vertex, Theorem 2.1 synchronizes that vertex's active status, and the
triangle coloring makes membership of its color equivalent to membership
of that vertex.

## 4. Theorem 4.1 and Corollary 4.2

The chain

\[
 \gamma(G-x)\le i(G-x)\le\alpha(G-x)\le\gamma^\infty(G-x)
\]

and hypothesis (4.1) force \(i(G-x)=\alpha(G-x)=3\).  Hence \(G-x\) is
well-covered.  Extending a singleton vertex to a maximal independent set
then proves that every deletion vertex belongs to an independent triple,
which is the support-coverage step needed in Theorem 4.1.

If color \(w\) lies in every component responder set, take any
\(w\)-colored deletion vertex \(v\) and a facet containing it.  The facet
has one vertex of each color, so responder-set membership forces
\(v\in A_x\), hence \(vx\in E(G)\).  Therefore no \(w\)-colored vertex is
adjacent to \(x\) in \(\overline G\), and coloring \(x\) by \(w\) is a
proper extension.  The original setup has \(\alpha(G)=3\), so
\(\alpha(G)\le\theta(G)\le3\) gives \(\theta(G)=3\).

In Corollary 4.2, a full state gives the root component all three colors.
Equation (3.4) then excludes every complement neighbor of \(x\) from its
support.  Every other component set is nonempty.  Since any nonempty total
intersection would invoke Theorem 4.1 and contradict
\(\theta(G)>3\), the total intersection is empty.  One component gives
intersection \(\{1,2,3\}\); exactly two give the nonempty set of the sole
nonroot component.  Thus at least three components are forced.  This
component count uses all of the stated hypotheses and no hidden
minimal-counterexample assumption.

## 5. Independent computation

The clean-room checker imports no campaign evaluator or target-lane code.
It exhausted every labeled graph through order five and, for each graph
with \(\alpha=3\), every nonempty eternal subfamily of its dominating
triples.  It checked the target identities for:

| quantity | checked |
|---|---:|
| labeled graphs | 1,099 |
| graphs with \(\alpha=3\) | 593 |
| arbitrary eternal triple-subfamilies | 9,021 |
| target/family instances | 19,006 |
| proper deletion-coloring instances | 282,156 |
| Theorem 4.1 hypothesis/coloring instances | 5,676 |
| failures | 0 |

No small instance met all hypotheses of Corollary 4.2, so that corollary is
supported by the direct proof rather than a finite positive instance.

The same checker independently decoded the labeled order-12 record and
found:

- \((\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3)\);
- all 127 dominating triples in the greatest eternal family;
- seven independent triples avoiding \(x=0\), all ridge-isolated;
- \(A_x=\{1,2,3,4,5,7,9\}\);
- \(N_{\overline G}(x)=\{6,8,10,11\}\);
- responder-color-set multiset
  \[
    \{\{1,2,3\},3\cdot\{1,3\},3\cdot\{2,3\}\};
  \]
- common responder color \(3\) for the displayed full-graph coloring; and
- \(\gamma(G-x)=2\), confirming that it is outside Theorem 4.1.

For \(G=\overline{L(K_{3,3})}\), direct construction found

\[
 (\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3),
\]

with a connected graph, all 48 dominating triples surviving, and exactly
six maximum independent triples, each an isolated ridge component.

## 6. Current-byte order-12 coloring distinction

The current text now says precisely that the partition in (5.1), which
contains \(x=0\), is the unique anchored coloring of the **full graph**
(equivalently, the unique anchored deletion coloring that extends over
\(x\)).  This is exact.  The deletion \(G-x\) has two proper colorings
anchored at \(1,2,3\): the displayed restriction has responder-color
intersection \(\{3\}\), while the other has empty intersection and does
not extend over \(x\).  The current wording distinguishes these facts and
does not suggest that every deletion coloring extends.

## 7. Reproduction and artifact hashes

Run:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/full_target_facet_propagation_hostile/independent_check.py
```

The strict run was deterministic and warning-free.

- checker SHA-256:
  `6b256ce5db748465f43ff01e6a1271eaa0546803bdfab6f164cbee0b1717fb14`
- evidence SHA-256:
  `3cd57981831cde9f7bc2dde01f103da4139e9b9d5e4f708a2af48886bf0e8c44`
