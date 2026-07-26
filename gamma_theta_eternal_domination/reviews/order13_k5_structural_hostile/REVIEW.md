# Hostile review: order-13, parameter-five structural note

## Verdict

**ACCEPT_BOUNDED_STRUCTURAL_REDUCTION_WITH_ATTACHMENT_NOTATION_CAVEAT**

This verdict accepts the note only at its stated boundary: Proposition 5 is a
conditional structural reduction relative to the accepted campaign inputs,
not an exclusion of the \((n,k)=(13,5)\) slice and not a resolution of the
gamma-theta conjecture.  The proposed attachment enumeration is coverage
sound as a template, but it would not become a certified finite result without
the canonical-generation proof, complete manifest, and independent exact
checks that the note itself requires.

Reviewed target:

- `math/working/order13_k5_structural.md`
- size: 11,188 bytes
- SHA-256:
  `1761c537ce293f1d7e36fd32786ffad0a67f2f7fe9dd4af6aceed346ccec6d37`

The target was not edited during this review.

## Source audit: Reed's bound

The exact hypothesis used in Lemma 1 is correct:

> If a graph \(H\) has order \(n\) and minimum degree at least three, then
> \(\gamma(H)\leq 3n/8\).

The official Cambridge page for B. Reed, *Paths, Stars and the Number Three*,
*Combinatorics, Probability and Computing* 5(3) (1996), 277-295, DOI
`10.1017/S0963548300002042`, states this theorem in its abstract.  The same
unqualified hypothesis and conclusion are stated as Theorem 2 in the retained
official open-access paper by Henning, Schiermeyer, and Yeo:
`literature/sources/henning_schiermeyer_yeo_2011_p12.pdf`, SHA-256
`418199b3a9f9c92974046a6c92b0b11b24cdec51e034f5aa23168c4bdfbb4285`.

Source caveat: the full Reed article was not retained locally and was not
available as open full text in this bounded review.  The exact statement is
nevertheless independently fixed by the publisher's official abstract and an
official open-access journal restatement.  No connectedness or regularity
hypothesis is present.  The note's use of Reed is therefore valid.  At
\(n=13\), \(3n/8=39/8<5\), so integrality gives
\(\gamma(G)\leq4\), contradicting \(\gamma(G)=5\).

Publisher record:
<https://www.cambridge.org/core/journals/combinatorics-probability-and-computing/article/paths-stars-and-the-number-three/6BDDD72CC73D2F579000429D47F22FD4>

The note correctly keeps the Kostochka-Stocker result separate: that stronger
bound is for connected cubic graphs and is not used for an arbitrary graph
with minimum degree at least three.

## Accepted-input audit

The uses of C-048, C-050, and C-051 agree with the frozen accepted statements.

1. **C-048.**  It supplies \(\delta(G)\geq2\), no simplicial vertex, and
   nonadjacent neighbors for any degree-two vertex.  Combined with Reed, this
   forces \(\delta(G)=2\).  Thus, for a degree-two vertex \(v\) with
   \(N(v)=\{a,b\}\), the inference \(ab\notin E(G)\) is valid.
2. **C-050.**  Relative to the accepted through-order-12 frontier, an
   order-13 counterexample is a minimum-order counterexample.  The note does
   not claim an unconditional order-13 exclusion.
3. **C-051 with \(\{v\}\).**  Since
   \(Q=G-N[v]\) has ten vertices, it is nonempty and has
   \(\gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=4\), is well-covered, and has
   \(\theta(Q)=4\) by the minimum-counterexample consequence.
4. **C-051 with \(\{a,b\}\).**  The set is independent.  With attachment
   sets \(A=N_G(a)\cap V(Q)\) and \(B=N_G(b)\cap V(Q)\),
   \[
   G-N_G[\{a,b\}]=Q-(A\cup B)=R.
   \]
   Hence the stated nonemptiness, well-coveredness, and four parameter-three
   equalities for \(R\) follow.
5. **C-051 with \(\{v,q\}\).**  Every \(q\in Q\) is nonadjacent to \(v\).
   Direct set subtraction gives
   \[
   G-N_G[\{v,q\}]=Q-N_Q[q],
   \]
   so the local parameter-three projection is valid for every \(q\in V(Q)\).

No one-guard/all-guards model substitution occurs in these steps.

## Direct proof checks

The clique-cover argument is exact.  A four-clique partition of \(Q\), plus
\(\{v,a\}\) and \(\{b\}\), proves \(\theta(G)\leq6\).  Since the assumed
counterexample has \(5<\theta(G)\), integrality proves
\(\theta(G)\geq6\), hence \(\theta(G)=6\).

If \(a\) is complete to a part \(C_i\) of any four-clique partition of
\(Q\), replacing \(C_i\) by \(C_i\cup\{a\}\) and adding
\(\{v,b\}\) makes a five-clique partition of \(G\).  This contradicts
\(\theta(G)=6\); the symmetric argument applies to \(b\).  The resulting
non-completeness condition is valid for every minimum partition.

The stated eternal-response observation is also correct but is only a
necessary filter.  In a state \(\{v\}\cup I\), an attack at \(a\) can be
answered only by \(v\) or a guard in \(I\cap A\).  If \(v\) moves to \(a\),
the successor must dominate \(b\) through \(I\cap B\), because
\(ab\notin E(G)\).  The note does not overstate this as a sufficient
strategy condition.

## Attachment-template coverage

Fixing a distinguished degree-two vertex \(v\) reconstructs a unique triple
\((Q,A,B)\): \(Q=G-N[v]\), \(A=N_G(a)\cap V(Q)\), and
\(B=N_G(b)\cap V(Q)\).  Conversely, a kernel \(Q\), two masks \(A,B\), the
edges from \(a,b\) prescribed by the masks, and the two edges \(va,vb\)
reconstruct the graph with that distinguished vertex.  Quotienting by
\(\operatorname{Aut}(Q)\) and the swap \(a\leftrightarrow b\) therefore
cannot omit an isomorphism type.  Graphs with several eligible choices of
\(v\) may occur more than once before global canonicalization, which is a
deduplication issue rather than a coverage gap.

The filters in Section 5 are necessary conditions or exact final evaluators.
They may generate extra cases, but that does not threaten coverage.  The note
correctly says that an exclusion additionally requires a canonical coverage
proof and manifest; no exclusion is claimed here.

## Required notation correction

Equations (3.5), (3.6), and (3.10) use \(N_Q(a)\) and \(N_Q(b)\), although
\(a,b\notin V(Q)\).  Under the intended attachment convention the arguments
are correct, but the notation is formally undefined.  Before this note is
promoted into a manuscript claim, define explicitly
\[
N_Q(a):=N_G(a)\cap V(Q),\qquad
N_Q(b):=N_G(b)\cap V(Q),
\]
or use the right-hand sides throughout.  In Proposition 5, “a nonsimplicial
graph” would also be clearer as “a graph with no simplicial vertex.”

This is a documentation-level caveat, not a failed mathematical inference,
so it does not change the bounded acceptance verdict.

## Independent replay

The replay is solver-free, imports no campaign implementation, performs no
graph-class enumeration, and needs no network.  It freezes the target and
nine dependencies, checks the note's claim-boundary language and order-13
arithmetic, and tests the set identities, reconstruction map, and clique
obstruction on four small synthetic attachment cases.

Run from the repository root:

```sh
python3 reviews/order13_k5_structural_hostile/audit.py
```

Expected final verdict:

```text
ACCEPT_BOUNDED_STRUCTURAL_REDUCTION_WITH_ATTACHMENT_NOTATION_CAVEAT
```

The replay is evidence for the audited identities and frozen inputs only.  It
does not evaluate eternal domination and is not a finite exclusion
certificate.
