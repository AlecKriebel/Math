# Hostile source-and-scope audit, 26 July 2026

**Audit timestamp (UTC):** 2026-07-26T03:49:00Z  
**Scope:** the current `NOTE.md` and `paper.tex`, Gallagher's published
all-seed construction, Brink's Theorem 13, the Campbell--Razar--Wright
regular-action translation, and a fresh collision search.  
**Posture:** no person was contacted; this is an internal audit, not peer
review.

## Verdict

No fatal correctness defect was found.  The main theorem is correctly scoped:
over \(\mathbb C\), every Gallagher seed satisfying the displayed
polynomiality hypotheses and having degree \(d-1\geq2\) gives a
dimension-three Keller counterexample of generic degree \(d\) and geometric
monodromy \(S_d\).

The result is mathematically sound but its novelty is deliberately narrow.
Gallagher supplies the maps, the all-seed inverse equation, and their generic
degrees; Brink supplies the entire two-free-coefficient \(S_d\) theorem.  The
only candidate addition is noticing, checking, and recording their immediate
combination, including exact recovery of the Keller root field.  It should
continue to be described as an attributed Brink--Gallagher corollary, not as a
new monodromy theorem.

## Source-by-source findings

### Gallagher

The full text of Gallagher's 20 July record, not only its abstract or
explainer, was checked:

- Theorem 1 is uniform in every polynomial \(p\) satisfying
  \(p(0)=0\), \(p(1)=-c\), \(\int_0^1p=0\), with \(b,c\ne0\) and
  \(p'(1)/c\ne-2\).  It proves that the displayed apparently rational
  coordinates are polynomial and that their Jacobian is \(bc\).
- Proposition 1 proves that a seed of degree \(e\) has generic fibre degree
  \(e+1\), using the same inverse equation and recovery appearing in the
  present draft.
- Lemma 1 and Corollary 1 supply a seed of every degree \(e\ge2\).
- Gallagher does not compute monodromy in that paper.

Thus the draft's indexing
\(\deg p=d-1\), generic degree \(d\), and range \(d\ge3\) are correct.  The
word “admissible” is terminology introduced by the present note for exactly
Gallagher's stated hypotheses; it does not silently enlarge the family.

Source: A. Gallagher, *An infinite family of counterexamples to the
Jacobian Conjecture in dimension three: every generic fiber degree
\(n\ge3\) occurs*, Zenodo record
[21479195](https://zenodo.org/records/21479195).

### Brink

The full text surrounding Brink's Theorem 13 was checked.  For \(n\ge3\),
fixed \(a_{n-1},\ldots,a_2\in K\), and
\(\operatorname{char}K\nmid n(n-1)\), it states exactly
\[
 X^n+a_{n-1}X^{n-1}+\cdots+a_2X^2+SX+T
\]
has Galois group \(S_n\) over \(K(S,T)\).  This is stronger than an
existence-after-specialization statement and applies verbatim after
normalizing
\[
 \Phi(T)-PT+cQ.
\]
Here \(P,Q\) are algebraically independent because
\((A,B,C)\leftrightarrow(BC,AC^2,C)\) is birational and the Keller
coordinates are algebraically independent.  There is no exceptional
admissible seed: all coefficients of degree at least two may be arbitrary
fixed elements of \(\mathbb C\).

Source: D. Brink, *On alternating and symmetric groups as Galois groups*,
Israel J. Math. **142** (2004), 47--60,
[Theorem 13](https://doi.org/10.1007/BF02771527).

### Geometric versus arithmetic group

Brink gives \(S_d\) over \(\mathbb C(P,Q)\).  Since \(\mathbb C\) is
algebraically closed, this is already the geometric splitting-field group.
Adjoining the independent transcendental coordinate \(C\) replaces the
splitting field \(E\) by \(E(C)\), so the group remains \(S_d\).  The recovery
identity
\[
 H'(w)=p(w)-P=-c\gamma
\]
rules out a denominator branch at the generic root and identifies the
natural root action with the action on the generic fibre.  The theorem does
not infer geometric monodromy from the arithmetic PARI specializations; the
current verification prose correctly labels those as consistency checks.

### Campbell--Razar--Wright translation

The accompanying Track B obstruction is correct in the stated
\(\mathbb C\)-scope.  If \(N/K\) is the normal closure of \(L/K\), with
\(G=\operatorname{Gal}(N/K)\) and
\(H=\operatorname{Gal}(N/L)\), the faithful natural action is \(G\) on
\(G/H\).  It is regular exactly when \(H=1\), equivalently \(N=L\),
equivalently \(L/K\) is Galois.  Campbell--Razar--Wright then implies that a
Keller map with this property is an automorphism.  Hence a Keller
counterexample over \(\mathbb C\) has nonregular (and therefore nonabelian)
geometric monodromy.

This equivalence must not be exported unchanged to a nonclosed ground field:
regular **arithmetic** monodromy tests whether the original extension is
Galois; regular geometric monodromy tests the base-changed extension.  The
current Track B note states this warning correctly.

## Degree and group checks

- \(d=2\): the only transitive action is regular \(C_2\), so it is excluded.
- \(d=3\): regular \(C_3\) is excluded and natural \(S_3\) is realized.
- \(d=4\): regular \(C_4,V_4\) are excluded; \(D_4,A_4,S_4\) survive the
  obstruction, and the weighted lift realizes \(S_4\).
- \(d=6\): regular \(C_6\) and regular \(S_3\) are excluded; the natural
  degree-six \(S_6\) is realized.

The abstract name of a group is insufficient: for example, \(S_3\) is
nonregular in degree three and regular in degree six.  The ledger correctly
uses permutation actions rather than abstract isomorphism classes.

## Fresh priority check

The following newly visible records were checked in addition to the sources
already listed in `PRIORITY_AUDIT.md`:

- *Exact Fibers, Image, and Geometry at Infinity of the Marked-Root Keller
  Family*, public GitLab snippet
  [6012790](https://gitlab.com/-/snippets/6012790), concerns maps
  \(K_n:\mathbb C^n\to\mathbb C^n\) with generic degree \(n(n-2)\).  It does
  not state the Gallagher all-seed \(S_d\) monodromy corollary.
- F. Santibañez-Leal, *The Jacobian counterexample, validated and extended*,
  Zenodo record
  [21579022](https://zenodo.org/records/21579022), contains no monodromy or
  Galois calculation.
- Fresh exact-phrase and site-restricted searches of arXiv, MathOverflow,
  GitHub, and GitLab found the already-recorded finite
  \(3\le d\le13\) Gallagher-tower computation, but no explicit public
  all-degree, all-admissible-seed Brink--Gallagher statement.

This is source-specific negative evidence, never a guarantee of worldwide
priority.

## Minimal correction proposal

No theorem statement needs correction.  One sentence in `NOTE.md` should be
made algebraically precise:

```diff
- Equation (6) is irreducible over \(\mathbb C(P,Q)\): after viewing it as
- a polynomial in \(Q\), it is linear with nonzero constant coefficient
- \(c\), and Gauss's lemma applies.
+ Equation (6) is irreducible over \(\mathbb C(P,Q)\): in
+ \(\mathbb C[P,T][Q]\) it is linear in \(Q\) with unit leading coefficient
+ \(c\), hence prime; it is primitive as a polynomial in \(T\), so Gauss's
+ lemma applies.
```

The existing phrase calls \(c\) a “constant coefficient” even though it is
the coefficient of \(Q\).  This is only a wording defect; `paper.tex`
already uses the correct unit-coefficient formulation.

For priority posture, add the two 26 July records above to the next
timestamped delta in `PRIORITY_AUDIT.md`.  No stronger novelty wording is
warranted.

