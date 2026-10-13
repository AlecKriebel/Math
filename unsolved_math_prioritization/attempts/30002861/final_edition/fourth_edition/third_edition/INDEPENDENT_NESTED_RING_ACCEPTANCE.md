# Independent acceptance of the nested-annulus extension

## Decision and accepted scope

**Accepted.** The separate additive [nested-ring proof](THIRD_PASS_NESTED_RING_EXTENSION.md) correctly excludes every balanced closed core in its specified family: the central six-vertex triangulation followed by any positive finite number of six-vertex annuli, with an independently chosen forward or reverse diagonal orientation on each entire annulus.

The family has unbounded size, with 6(n+1) support vertices and 12n+4 support triangles for n>=1. The result permits arbitrary admissible nonsymmetric coordinates and nonconvex intermediate rings. Convexity is needed only for the terminal boundary of the closed support, where it follows from the accepted support theorem.

This is an additional theorem within the same third documented substantive pass, not a new counted pass.

The exclusion is of these complete closed core topologies. It is not a full-rank theorem for every larger full triangulation containing them. In such a larger triangulation, the three original four-stars force the initial twelve vertices only; they do not automatically force every vertex of every further ring into a closed component. Irregular proper components and their possible straight boundary vertices require separate analysis. The additive manuscript explicitly retains this limitation in its opening scope and Section 4.

## 1. The one-annulus lemma covers all degeneracies allowed by the model

Take independent homogeneous vectors A,B,C and S=A+B+C. For an old boundary triangle of colors A,B,C write its known weighted vectors as

    A+aS, B+bS, C+cS.

Independent expansion gives its determinant as (1+a+b+c)det(A,B,C). The first factor cannot vanish because this is an actual nondegenerate triangle of the known inner region.

For the new opposite weighted vector Z=(u,v,w) in this basis, the old boundary-edge balance is

    (u-v)(1+a+b+c)=0.

Thus u=v and Z belongs to span(C,S). The two generators C,S are independent, so the decomposition

    Z=gamma C+pS

exists and is unique. This conclusion does not divide by gamma, and it does not assume gamma is nonzero. Nor does it require S to be a finite point in the affine chart.

After this argument is applied to all six old boundary edges, every new weighted vector lies on its appropriate color line. Consider the annulus edge whose endpoint sum is gamma C+pS+B+bS. Its opposite vertices have vectors

    A+aS, delta A+qS.

Their cross product in the A,B,C basis is

    (0, a delta-q, q-a delta).

Consequently q-a delta=0 is equivalent to their linear dependence. These are two distinct geometric vertices of the conforming triangulation with nonzero homogeneous weights, so this factor cannot vanish. This is a model-wide distinctness assumption, not a genericity assumption or an unproved nonzero parameter condition.

The raw edge balance is

    (gamma-1)(q-a delta)=0.

It therefore forces gamma=1. In particular:

- If delta=0, the opposite new vector is qS. Nonzeroness of that vector forces q nonzero, and the same equation still gives gamma=1.
- If gamma=0 provisionally, the equation contradicts distinctness of the opposite vertices. Hence this permitted intermediate case is excluded by the equation, rather than silently omitted.
- If a known or new weighted vector represented a forbidden coincidence, the distinctness factor would expose it. No such coincidence is admitted by the fixed model.
- No weight sum, last homogeneous coordinate, gamma, or delta is divided by.

I reconstructed both annulus face lists independently and checked every old boundary-edge factor and every radial-edge normalization. There are six first-stage factors and twelve radial factors per orientation. Each radial equation has precisely the form (gamma_current-1)(p_opposite-a_old gamma_opposite), up to the determinant-order sign. This verifies the local incidence used by the argument, rather than checking only an isolated algebraic template.

The normalization fixes the actual face-normalized weighted vectors to base coefficient one. It does not rescale each vertex independently after balance has been imposed.

## 2. Mixed annulus orientations and induction are legitimate

Reversing the cyclic indices i to -i preserves the four central triangular faces as unoriented triples and exchanges the forward and reverse first annulus. This was checked on the exact face sets. The original pencil-collapse lemma therefore covers either orientation of the first annulus. Reversing determinant order can change an equation's overall sign but not its zero set or the nondegeneracy assumptions.

That initial lemma uses only the twenty-one edges interior to the first twelve-vertex region. Adding later annuli does not change either opposite vertex of any of those edges, so the lemma continues to apply. Its six boundary equations are not needed to establish the initial pencil.

For a subsequent annulus, each old boundary edge has one known opposite vertex in the preceding region. The inductive hypothesis covers that vertex as well as both edge endpoints. All new balance equations used are interior to the enlarged region and hence satisfy the accepted homogeneous equation. The one-annulus lemma therefore extends the same A,B,C,S representation throughout the next ring.

A reverse choice at any later stage is just the same local proof with reversed boundary indexing. It imposes no global consistency restriction on the choices made on other annuli. Extending the colors from the actual triangle incidences gives a three-periodic color sequence on every ring, with opposite terminal vertices always sharing a color.

This local induction proves every finite n. Checks of finitely many orientation sequences are supplementary regressions, not the reason arbitrary n is covered.

## 3. The terminal boundary gives the same finite sign contradiction

The terminal boundary has six vertices, each of induced degree four. The accepted support theorem therefore makes all six strict corners of a convex hexagon; no straight subdivision occurs on that boundary.

Each opposite terminal pair shares a color and lies on one of the three distinct lines span(A,S), span(B,S), span(C,S). Its points are distinct, so its line is that whole color line. The three opposite diagonals consequently concur at S. Strict convexity makes their segment intersection finite and interior before any affine normalization is taken.

After translating that point to the origin, the two weighted vectors of an opposite pair have the same nonzero planar numerator because both have base coefficient one. Their two geometric displacements are oppositely directed. Their weights must therefore have opposite signs.

The actual exterior triangle at each terminal boundary edge is supplied by the original full mesh, not by an artificial choice of added points. Closedness and the exterior-attachment classification place its opposite vertex on the required supporting-line extensions. The already audited boundary positivity lemma applies on every terminal side, giving the same sign to all six terminal weights. This is the contradiction.

There is no assumption about finiteness or interiority of S at earlier rings, nor any assumption that an intermediate ring is convex. All finiteness and order arguments occur at the terminal strictly convex support boundary.

## 4. Independent mathematical verification

The independent propagation calculation checks the three generic determinant identities, the full distinctness cross product, the cases delta=0 and gamma=0, all twelve boundary-line factors and twenty-four radial normalization factors across the two annulus orientations, and the first-annulus reversal equivalence.

It additionally generates all 62 forward/reverse orientation sequences with one through five rings, extending colors from triangle incidences. It verifies vertex/edge/face counts, exact terminal boundary, terminal induced degrees, opposite terminal colors, and 4,830 interior-edge color configurations. The last checks are generic color identities, not numerical samples of geometric coordinates.

Four negative controls reject the wrong line-membership sign, a base normalization of minus one, the wrong distinctness factor, and treating the zero-delta case as automatically balanced.

The exact determinant and incidence conventions are given in [REPRODUCTION.md](REPRODUCTION.md). The all-n mathematical conclusion rests on the explicit one-annulus argument and induction above.
