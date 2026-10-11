# Turn 1: a canonical-shadow obstruction to the long-slope route

**Scoped partial result; original Problem 12.11 unresolved.** This is the first substantive author turn. It tests whether the known long-filling-slope lower bound automatically covers the alternating-knot shadows singled out in the source. It does not.

## Source and mechanism

Dylan Thurston's shadow-cylinder construction, printed pp.351–352 of *The algebra of knotted trivalent graphs and Turaev's shadow world*, starts with a planar knot diagram in a disk and attaches the mapping annulus. Each corner of a complementary disk region contributes either +1/2 or -1/2 to its gleam. Contributions at repeated incidences are counted separately. The construction also has an auxiliary boundary component; a knot-complement identification must retain the relevant boundary data.

For comparison, Ishikawa–Koda, arXiv:1403.0596v1, Proposition 5.1 and Lemma 5.3, work with a branched special shadow P of a closed orientable 3-manifold. If every region's filling slope exceeds 2pi, the resulting volume has a quantitative lower bound. Their slope expression is

    sl(R)^2 = 4 g(R)^2 + v(R)^2,

where v counts true-vertex incidences with multiplicity. The preprint uses Section 5; citations to Section 6 in later material concern another edition. The theorem is not a statement about arbitrary relative knot shadows. Below we show a second, numerical obstruction even before that domain difference is repaired.

## Proposition: small faces force a short formal slope

Let D be a connected knot or link projection in the sphere with n>=1 crossings, all ordinary four-valent vertices, and choose any complementary face as the outside face. Form its unmodified canonical shadow cylinder in a disk. For each bounded face R let v(R) be its number of corners, counted with multiplicity, and let g(R) be the canonical sum of the signed half-corner contributions.

Then at least one bounded face has v(R)<=3, and for that face

    4g(R)^2 + v(R)^2 <= 18 < (2pi)^2.             (1)

In fact there are at least three faces of valence at most 3 in the spherical diagram; if there are no monogons, there are at least four. Thus at least two, respectively three, remain bounded after any choice of outside face.

### Proof

Write E and F for the edge and face counts of the connected embedded four-valent graph. The handshaking identity gives E=2n. Euler's formula gives F=n+2. Each edge contributes two sides to the facial walks, including repeated incidences, so

    sum_R v(R)=2E=4n,
    sum_R (4-v(R))=4(n+2)-4n=8.                 (2)

Every facial walk has positive length. A face with v>=4 has nonpositive contribution to the second sum, whereas a face with v<=3 contributes at most 3. Therefore there must be at least three such faces. If v>=2 for every face, each positive contribution is at most 2, giving at least four. Removing any single outside face leaves the asserted bounded face. Multiple edges, loops and repeated boundary vertices do not affect these incidence identities.

For a bounded face with v corners, write its corner signs as epsilon_1,...,epsilon_v in {+1,-1}. The canonical construction gives

    2g = epsilon_1+...+epsilon_v.

Hence |2g|<=v and 4g^2+v^2<=2v^2. For v<=3 the latter is at most 18, while (2pi)^2>36 because pi>3. This proves (1). No alternation hypothesis was used, so the assertion includes the alternating examples. QED.

## Exact implications and limits

On the relative shadow cylinder, the quantity in (1) is called a **formal slope expression** here. Lemma 5.3 identifies it with a geometric cusp slope only under its closed special-shadow hypotheses. We do not silently extend that identification to a boundary-marked shadow.

Suppose one changes the boundary setup to obtain a special shadow to which that lemma applies, while retaining any one of these bounded regions with its gleam and true-vertex incidence unchanged. That region then has an actual filling slope at most 3sqrt(2), so the requirement that *all* filling slopes exceed 2pi still fails. A direct cap or conversion that preserves every bounded face cannot make the long-slope theorem applicable.

This does not exclude a more substantial sequence of shadow moves that changes the regions, gleams or incidence counts. It does not exclude a partial-filling construction that leaves the short slopes unfilled. Such mechanisms would need a fresh theorem and a proof that the resulting object still gives the original knot exterior and the required volume estimate. Nor is (1) a counterexample to the requested existence of some other shadow condition.

The conclusion is stronger than merely finding one exceptional diagram: the unchanged canonical planar construction always has this obstruction. Making a diagram alternating cannot supply the missing strict slope hypothesis. Long-slope volume estimates therefore cannot, by themselves, be promoted to a complete answer to the source request.

## Related bounds and the remaining target

Costantino–Thurston's Theorem 3.37 bounds shadow complexity below by a multiple of Gromov norm. For a presented shadow with V vertices this gives a volume upper bound, not the desired lower bound. Their quadratic upper bound for *minimal* shadow complexity can be inverted only when that minimum is controlled; the number of vertices in an arbitrary given shadow is not a lower bound for the minimum.

Lackenby's Theorem 1 already gives a lower bound for prime alternating diagrams in terms of twist number. Simply recognizing a marked planar diagram inside a shadow and repeating that theorem would recover an existing special case. The source explicitly motivates a condition usable for more efficient shadow diagrams. A non-tautological extension requires a structure on the general shadow that controls hyperbolic volume while demonstrably including the alternating construction. No such extension has been established in this turn.

## Verification

The written proof is an Euler-characteristic and triangle-inequality argument valid for all sizes. The exact checker separately tests positive integer face-degree sequences with F=n+2 and total degree 4n, the arbitrary-outside-face assertion, all corner-sign counts for small valences, and the strict rational comparison with 4pi^2. These sequences are arithmetic controls, not an enumeration or a realization claim for planar maps. No numerical topology package or code from downloaded sources is used.
