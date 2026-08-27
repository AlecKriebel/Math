# Source-convention cross-check

## Source and conventions

The checker targets Lemma 4.1 of Brits, Holtgrefe, van Iersel, and Martin, *On Tree--Network Distinguishability and Full Identifiability of Phylogenetic Networks*, arXiv:2607.12919v2. That level-one lemma and its formulas are retained in arXiv:2607.12919v3. Version 3 removes the separate arbitrary-level K2P claim and records the leaf-order obstruction addressed by this package.

It fixes:

- Fourier order `(A,C,G,T)`;
- Klein addition with `A` the identity and `C+G=T`;
- the K2P identification `a_C=a_T` on every edge.

For exact rational test vectors it evaluates the paper's 3-sunlet rule

```text
q_(x1,x2,x3) = a_(x1) b_(x2) c_(x3)
                [delta d_(x3) f_(x2)
                 + (1-delta) e_(x3) f_(x2+x3)]
```

and independently reproduces the five displayed coordinates:

```text
q_AGG = b_G c_G [delta d_G f_G + (1-delta) e_G]
q_CCA = a_C b_C f_C
q_GAG = a_G c_G [delta d_G + (1-delta) e_G f_G]
q_GGA = a_G b_G f_G
q_TCG = a_C b_C c_G f_C [delta d_G + (1-delta) e_G]
```

The same calculation reproduces the favorable-order factorization

```text
Q = (positive edge monomial)
    * delta * (1-delta) * d_G * e_G * (1-f_G)^2 > 0.
```

## Exact replay

Command:

```bash
python3 src/verify_source_conventions.py
```

Recorded output:

```text
[source conventions] PASS  A,C,G,T order; C+G=T; K2P a_C=a_T
[source conventions] PASS  five explicit Lemma 4.1 coordinates and favorable-order Q factorization
```

Result: **PASS**. This convention check supports, but does not replace, the graph-derived four-switching calculation in `verify_k2p_displayed_trees.py`.

## Theta-core terminology audit

The complete K3P verifier separately reconstructs the suppressed theta core,
its three leaf sides, and its two reticulations. It confirms the unambiguous
fact needed by the collision theorem: the whole core is a maximal strict
level-two nontrivial 3-blob.

For provenance, the verifier also records both readings of the source paper's
printed 2-sub-blob clauses. The literal boundary-vertex enumeration returns six
single-edge candidates, but contracting each produces four external
incidences. The edge-incidence/degree-two-suppression reading returns no proper
suppressible theta substructure. Neither reading removes the full theta
distribution from the source model, and the collision theorem assumes no
additional no-2-sub-blob condition.
