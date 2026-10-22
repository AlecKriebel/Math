# Explanatory addendum to the frozen proof

3 October 2026 UTC. This addendum expands four nonblocking points identified by the [fresh independent audit](audit/AUDIT_REPORT.md). The [frozen proof](release/PROOF.md) and all author/audit artifacts retain their reviewed bytes. No theorem statement or proof dependency is changed.

## 1. Structural hypotheses in the bistellar transfer

In Section 4.3, let the old move support be B_0=alpha*boundary(beta), replaced by B_1=boundary(alpha)*beta. Nevo–Wagner's transfer theorem requires more than the numbered intersection and homology conditions: the skeletal support must be induced, the removed simplex's star must stay in that support, and the two maps must agree on their common subcomplex.

These requirements hold for a missing triangle M common to the old and new complexes. The simplex beta is a missing face before the move, so the support on the move vertices is induced. If M were contained in those vertices, minimality of M as a nonface would force M=beta, which becomes a face after the move. Thus M is not contained in the support. Also M cannot contain alpha: a proper face containing alpha would disappear, contrary to M remaining missing; the exceptional equality M=alpha is impossible because alpha was a face before the move. Adding M therefore preserves both inducedness and the removed-star condition.

Define the first map by the natural old skeleton and its complementary filling disk. A homeomorphism between the two standard move balls fixed on their common boundary defines the map on the new support; elsewhere use the first map. The maps consequently agree on their common complex. Their finite collections of forbidden disjoint-face pairs have disjoint compact images, hence positive separation. A sufficiently close simultaneous relative approximation preserves these separations and produces the required general-position representatives.

## 2. Only the filling disk's interior avoids the 1-skeleton

The boundary of the added triangle is already in the 1-skeleton, and is kept fixed. The intended assertion in Section 4.3 is that the **interior of the filling disk** avoids that 1-skeleton. Contractibility of the complementary PL manifold gives a continuous filling. Its collar moves the disk interior off the move boundary, and relative PL general position makes the disk interior disjoint from the 1-skeleton. Self-intersections of the filling disk are permitted. No embedded-disk theorem or PL-standard complementary 4-ball is required.

## 3. The new-face cone construction uses the old unaugmented skeleton

In the p=3, q=1 case, the new missing triangle is M=v*beta. Use the old **unaugmented** 2-skeleton for the homological cones. The same cone-complement and Alexander-duality calculation gives the required vanishing of reduced H_0 and H_1 there, so this construction does not presume an old missing triangle.

All support edges except beta belong to the old skeleton. Their cone chains can be chosen there with the required support-avoidance property. Send the formal triangle v*beta to M itself, preserve support triangles, and send the remaining formal triangles through v to those old-skeleton cone chains. Consequently no cone chain contains M. In the resulting deleted-product cycle, M is paired exactly with boundary(alpha), giving the stated local linking evaluation. The independent checker constructs and tests 70 such witnesses along its reproducible bistellar sequence.

## 4. Direct original-source locator for the metastable theorem

The existence theorem used in Section 3 is **Claude Weber, Theorem 1, printed p. 2**, in *Plongements de polyèdres dans le domaine métastable*, Commentarii Mathematici Helvetici 42 (1967), 1–27. Its hypothesis is 2m>=3(n+1), with n the finite polyhedron dimension and m the Euclidean ambient dimension. The semilinear category in its Section 1 is the PL category.

- [Original archival article](https://www.e-periodica.ch/cntmng?pid=com-001%3A1967%3A42%3A%3A6)
- [Publisher record](https://link.springer.com/article/10.1007/BF02564408)
- [Skopenkov, corroborating Theorem 8.1](https://arxiv.org/abs/math/0604045)

Substituting n=d and m=2d gives d>=3, including the equality case d=3. The theorem produces a PL embedding; it does not assert that the initial topological embedding was PL, tame, approximable, or isotopic to the resulting embedding. The separate four-dimensional argument handles d=2.
