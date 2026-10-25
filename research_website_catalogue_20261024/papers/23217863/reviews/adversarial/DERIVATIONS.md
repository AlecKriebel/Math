# Independent derivations and boundary audit — row103

The complete actual manuscript/control source was read and the substantive EARLY_LEDGER sealed before any foreign or bundled upstream body or archived/current assessment. The following expands that reconstruction with independently inspected primary interfaces. The complete original theorem, including arbitrary predual density, is the object under review.

## 1. Actual-image cohomology gives the needed estimates

For fixed A, each ordinary bounded multilinear cochain space is Banach and the standard differential is bounded. Thus Z^k=ker d is closed. Actual H3=0 means im(d:C2→C3)=Z3, so the induced map C2/Z2→Z3 is a bounded bijection of Banach spaces. Its inverse is bounded. Enlarging the inverse norm gives K with inf_z||f-z||<=K0||df||<K||df|| for nonzero df; choose a representative attaining the enlarged inequality. For df=0 take z=f. Actual H2=0 similarly makes d:C1→Z2 onto. Open mapping gives a size bound L on some primitive of each z, again allowing a strict enlargement to accommodate unattained infima and choosing zero for z=0. No bounded linear selection or complemented kernel is used.

This is precisely why reduced cohomology or merely dense coboundaries would be insufficient. The upstream theorem's definitions and proof give actual bounded primitives on ordinary cochains; see UPSTREAM_PROOF_AUDIT. H3=0 also implies the closed-B3 condition of Roydor, but the target directly uses its own stronger H2/H3 version.

## 2. Reflection, involution and the quadratic correction

Put R_n f(a)=f(a_n*,...,a_1*)*. Reversing the standard differential matches its two outer terms and pairs the merge at j with the merge at n+1-j. The sign ratio is (-1)^(n-1). With s_n=(-1)^((n-1)(n-2)/2), the recurrence s_(n+1)/s_n=(-1)^(n-1) gives d(s_nR_n)=(s_(n+1)R_(n+1))d in every degree. These are conjugate-linear isometric involutions on cochain space, despite preserving complex multilinearity of each cochain. Real averaging z with S2z retains the approximation bound for symmetric Delta and is still a cocycle. Averaging h with S1h gives dh=z and retains the primitive bound. S1-fixed h preserves *.

Expanding associativity of mu=m+Delta gives

dDelta(x,y,z)=Delta(Delta(x,y),z)-Delta(x,Delta(y,z)),

so ||dDelta||<=2delta². Choose z=dh with ||Delta-z||<=2Kdelta² and ||h||<=L(delta+2Kdelta²). For g=id+h and b=g^-1 the exact algebraic calculation, before evaluation at bx,by, is

g(mu(u,v))-g(u)g(v)=(Delta-dh)(u,v)+h(Delta(u,v))-h(u)h(v).

It follows that the transported product differs from m by at most

4[2Kdelta²+2Ldelta²+4L²delta²]=(8K+8L+16L²)delta²

when delta<=1/(2K), delta<=1/(4L). No commutation of h with multiplication or positivity of h is assumed.

Choose the manuscript's delta_A=min(1/(2K),1/(16L),1/(2D)). Then delta_(n+1)<=Ddelta_n²<=delta_n/2 and sum||h_n||<=4Ldelta_0<=1/4. Each correction is invertible, and the ordered products g_(n-1)...g_0 form an operator-norm Cauchy sequence; their displacement from id is at most exp(sum||h_n||)-1<=exp(1/4)-1<1/2. The limit is invertible by its distance from id, preserves * and conjugates the original mu to m. Uniform bounds on the products justify passing to the limit in the intertwining identity. The original unit need not be a unit for mu; when it is, the onto algebra isomorphism sends it to the original unit. An exact M2 gauge control deliberately uses a product with a different unit.

## 3. Halving imports and a single fixed source

The actual Roydor paper defines ordinary bilinear defects and its Theorem3.2 assumes precisely that the source finite typeI homogeneous components have even degree. Its proof begins by halving the unit and using an M2 matrix system over the commutant. It does not use separable predual, a normal near-isomorphism or cb bounds. Lemma3.1 supplies unital self-adjoint surjective corner maps, with inverse bound1+988sqrt(t); Theorem3.2 supplies max defect3147585sqrt(t). Its proof uses T(e_ij)≈g_ij+h_ji off the diagonal, as explicitly stated immediately before the mistyped Claim4 heading and in Claim7. The target uses that consistent relation.

For the central target projection q, y diamond z=qyz+(1-q)zy is the direct sum of a C*-product and its opposite, so it has the original norm, involution and unit. The map F is a unital self-adjoint isomorphism onto this underlying Banach space. On central direct sums the bilinear defect norm is the maximum of the block norms. Thus

||F^-1(Fx diamond Fy)-xy|| <= (1+988sqrt(t))3147585sqrt(t)||x||||y||.

Applying the preceding deformation lemma once on V produces F Phi^-1, a *-isomorphism onto the target with the diamond product and hence a Jordan *-isomorphism onto its original product. Every deformation constant belongs to the fixed algebra V; none belongs to the moving pV.

## 4. Full central carrier survives

Let w=c_D(k), z=theta^-1(w). Roydor's center map and approximate order estimate, applied to unital self-adjoint T^-1, give

h-z <= [2(1+t)140sqrt(t)+2(1+t)sqrt(2t+t²)]1 = alpha(t)1.

Each of the two norm errors carries the inverse norm1+t; this factor has not been dropped. For small t, alpha(t)<1. Centrality of z makes h(1-z) a projection. Compress by1-z; a nonzero projection has norm1, contradicting the strict alpha<1 bound. Therefore h<=z, and full carrier of h forces z=1 and w=1. Complementary projections use unitality and the same estimate. This does not assume a trace or separability.

## 5. Odd finite degrees, arbitrary centers

Write O as the bounded central product of its finite odd degree-n summands, n>=3. Choose rank n-1 e on each summand; e and f=1-e are full. E=eOe halves and fOf is abelian. A rounded target q and its complement remain full by section4. Lemma3.1 compressions have uniform errors tending to0. Applying the actual commutative conclusion of Proposition2.13 to the f corner makes (1-q)D(1-q) abelian. A full abelian corner forces D to be typeI.

Use the SINGLE fixed E in section3 to get J:E→qDq. Full corners identify their centers with the original centers; the restriction of J therefore gives beta:Z(O)→Z(D). A Jordan *-isomorphism and its inverse are positive order isomorphisms (positivity follows by squares of self-adjoint square roots). Order bijections preserve every existing supremum. Hence J and beta are normal, including for arbitrary center density. In particular, the countable source partition z_n is sent to a target partition w_n with join1.

On w_n the q corner is homogeneous degree n-1. Homomorphism/antihomomorphism decomposition preserves finite degree. Its n-1 orthogonal equivalent abelian projections have central carrier w_n in D. The remaining w_n(1-q) is abelian and full on w_n. Abelian projections with equal central support are equivalent: compare them centrally, and if p is subequivalent to abelian q, the subprojection of q is a central multiple of q; equality of carriers forces that central multiple to be all q. Apply the symmetric argument on the complementary comparison summand. Thus w_n is a sum of n equivalent abelian projections, so w_nD is homogeneous degree n, with center matching z_nO. Finite matrix classification identifies the algebras; their bounded central products identify O and D.

The directly inspected Nelson primary notes prove the full-corner center formula, equal-carrier abelian equivalence, typeI decomposition/classification and typeII halving without a separable-center condition. The typeI classification is used only in finite degree here. Infinite cardinal degrees belong to the halving P part; no cancellation such as kappa+1=kappa is used to reconstruct an odd finite degree.

## 6. Global quantifiers and the predual direction

M=A directsum P directsum O has only THREE fixed source central pieces. P halves, and E=eOe is the second fixed deformation algebra. Universal all-algebra cohomology applies directly to both; there is no assertion that the cohomology of a noncentral corner follows from a central restriction of M. Apply the ordinary center map/compressions to match these three target central pieces. A finite list of inequalities tending to0 in the original distortion and at most two fixed positive deformation thresholds yields one epsilon_M>0, independent of N, all target corners, odd degrees and center densities. Strict BM bounds supply some sufficiently small-distortion map without assuming attainment of an infimum.

For any predual Banach isomorphism S, S*:N→M has the same norm and inverse norm. Inverting maps shows BM is symmetric, so BM(M,N)<=BM(M_*,N_*). This direction suffices; the converse inequality for general near-isomorphisms is unnecessary. Exact Jordan *-isomorphisms are normal order isomorphisms and induce isometric preadjoints. Conversely an algebra-space isometry need not itself be unital or Jordan, but Kadison's theorem supplies a Jordan *-isomorphism; the predual case follows by adjoint and is also explicit in Sherman's actual Theorem1.1/proof for p=1. The literal0/∞ distance convention deals with M=0; no exception is omitted.

## 7. Exact mechanism controls and limits

The own script was inspected before execution. It compares52 formal terms of dS_n=S_(n+1)d for n=1,...,8, with a negative control omitting the S3 minus sign. It verifies the exact defect/associativity identities on16 M2 basis pairs and64 basis triples over rational numbers for a noncommutative transported associative product with a different original unit. It verifies dJ+Jd=id-cut on62 C² basis tuples in degrees1,...,5, and identifies57 cases where a cut alone fails. These are finite exact mechanism diagnostics, not proofs of the infinite-dimensional vanishing theorem, general reflection formula, or all-degree central homotopy. The universal arguments are the term pairing, exact expansions, quantitative inequalities and actual proof audit above and in UPSTREAM_PROOF_AUDIT.md.

No mathematical defect or substantive proof gap was found in the complete original result, within the explicit classical interfaces audited. No new universal numerical threshold, associative orientation, formal kernel proof, exhaustive novelty certification or unconditional result for arbitrary C*-algebras is inferred.
