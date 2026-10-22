# Independent reconstruction of the candidate04 theorem

This checks the supplied proposed mechanism. It adds zero substantive proof responses and makes no claim to having discovered the mechanism before the task disclosed it. The conventions are those of the actual Harvey contribution (joint with Park and Ray), Question3, OWR50/2017, p3021/MFO35, and Otto Definition2.3. The filtration concerns ordered smooth string links through their usual oriented closures. Superscripts denote ordinary derived subgroups.

The theorem under examination is: for every m>=3 and finite integer k>=1, there is gamma in P_m^(k) whose standard oriented closure is outside the integral smooth1-solvable class. Consequently P_m^(n+2) is not contained in F_n^m for every m>=3,n>=1. Different finite depths may require different witnesses. There is no element asserted in the intersection of all derived terms, and no explicit arbitrary-depth word is supplied. P1 is trivial and P2 is cyclic, making positive derived terms trivial in those boundary cases.

## Universal pointwise obstruction

Let L have pairwise linking numbers zero and let W be an integral1-solution in Otto's actual geometric sense. The zero-framed surgery M has H1(M;Z)=Z^m with meridional basis. The inclusion-induced isomorphism H1(M;Z)->H1(W;Z) extends the homomorphism taking every meridian to -1. Denote its rank-one signed rational local system by Q_alpha. Both families L_i,D_i of the embedded framed surface basis have fundamental group in the commutator subgroup. It is essential that this is true of the dual surfaces as well.

Compact smooth W has a finite CW model. Choose lifts of cells. Evaluating each group-ring differential at the sign representation gives an integer matrix. Reducing it modulo2 gives the ordinary differential: augmentation and the sign specialization agree in characteristic2. A minor nonzero over F2 has odd determinant and remains nonzero over Q. Thus rank_Q(d_j^alpha)>=rank_F2(d_j), for both j=2 and j=3, and equal chain dimensions give

    dim_Q H2(W;Q_alpha) <= dim_F2 H2(W;F2).

The integral UCT sequence is

    0 -> H2(W;Z) tensor F2 -> H2(W;F2) -> Tor(H1(W;Z),F2) -> 0.

The integral basis makes H2(W;Z) free of rank2r; the integral H1-isomorphism makes the Tor term zero. Hence the upper bound is2r. Replacing mod2 homology by ordinary rational homology without this UCT step would be invalid in the presence of2-torsion; no such replacement occurs here.

On each solution surface the sign system is trivial. A flat nonzero coefficient together with its oriented fundamental cycle therefore defines an absolute local-coefficient2-class. Distinct surfaces are disjoint except for each unique dual intersection. Framed embedded surfaces admit disjoint normal push-offs, so self-pairings vanish. The single transverse dual point contributes a unit +1 or -1 under the sign system. Changing one chosen coefficient sign in a pair gives the block [[0,1],[1,0]]. The2r classes consequently have a nonsingular hyperbolic pairing. Pairing a hypothetical linear dependence with all these classes forces every coefficient to zero. They are independent even before knowing whether the ambient form has a radical; the dimension bound makes them a full basis and rules out any additional radical. Both the ordinary and twisted signatures vanish. For r=0 the same bound gives twisted H2=0. Extension to complex coefficients preserves the real symmetric inertia.

Toffoli's formula(1.1), with rank-one unitary representation extending over W, is rho(M)=sign(W)-sign_alpha(W), hence zero. In his one-colour surgery formula(4.21), take theta=1/2. All components may be one colour; the colour-splitting condition is automatic. Pairwise linking zero makes Seifert framing zero, and the entire framed linking matrix is zero. Its signature and the sum correction vanish. The formula therefore gives rho(M)=-sigma_L(-1). The domain excludes1 only, so this is the pointwise link signature even at Alexander roots. No averaged knot invariant, acyclicity assumption or extra nullity correction has been imported. Thus sigma_L(-1)=0.

## Nonhomomorphy on the pure group

Write s(gamma)=sigma(hat gamma) with positive trefoil signature-2. GG TheoremA and Remark1 give bounded defect for ordinary link closure signatures on B3. Their p575 supplies the homogeneous quasimorphism q=lim s(gamma^r)/r and the sufficient bound |q-s|<=6.

Let x=sigma1,y=sigma2,a=x^2,b=y^2,h=y x^2 y^-1,z=(xy)^3. All four are pure. In the Artin group,

    a h b = x^2 y x^2 y = x(xyx)xy = x(yxy)xy = (xy)^3 = z.

GG Remark3 supplies s(x^ell)=1-ell on positive two-strand powers. A separate third strand adds a split unknot and preserves signature. Conjugacy of x and y and of h with a then gives q(a)=q(b)=q(h)=-2. GG's three-strand Lemma4.1 gives s(alpha Delta3^4)=s(alpha)-8. Since z^2=Delta3^4 and s(1)=0, s(z^(2r))=-8r for every positive r, and q(z)=-4. A homomorphism on P3 would give q(z)=-6. This contradiction proves the required nonhomomorphy on P3 itself; nonhomomorphy on B3 alone would not establish it.

## Finite derived depth and ordinary signature

Suppose a homogeneous quasimorphism f vanishes identically on a normal subgroup N. For g in G,u in N, normality gives (gu)^r=g^r u_r with u_r in N. Applying the defect bound once gives

    |r f(gu)-r f(g)| <= D(f).

Division by r proves exact coset constancy, hence descent to a homogeneous quasimorphism on G/N. For N=G^(k), finite k>=1, this quotient is solvable and amenable. Calegari Proposition2.65 and its complete invariant-mean argument force the descended map to be a homomorphism. Pullback contradicts nonhomomorphy. Thus q is nonzero somewhere on every finite P3^(k). This group fact is prior: Kawasaki etal2025Lemma7.12 proves the stronger exact defect-restriction identity for a solvable quotient and is explicitly credited.

Choose v in P3^(k) with q(v)!=0. A positive r with r|q(v)|>6 gives s(v^r)!=0 because q(v^r)=r q(v) and |q-s|<=6. The power step is necessary; it does not assert s(v)!=0 for the same initial representative. Powers stay in the derived term. Pairwise linking numbers are stacking homomorphisms on pure braids, so they vanish on every positive derived term and on this power. The closure is algebraically split. The universal obstruction above implies v^r is outside F1^3. Adding separate vertical strands is a homomorphism preserving derived membership; the standard closure adds split unknots and preserves signature. This proves all m>=3. Otto's decreasing filtration gives F_n^m subset F1^m for n>=1; set k=n+2.

## Explicit witness and exact arithmetic

The preserved original is a separate k=3/n=1 construction. For a=x^2,b=y^2,c=[a,b],d=a^-1ca,e=b^-1cb,u=[c,d],v=[d,e],beta=[u,v], normality gives c,d,e in P3', u,v in P3'', beta in P3'''. Free reduction gives104 letters,23 alternating pairs, zero exponent sums, purity and pairwise linking0.

The planar reconstruction first builds the standard closure rotation system, then its faces and checkerboard colours. It checks104 crossings,208 edges,106 faces and49 alpha faces including the exterior. Each sigma1 block meets the exterior and one anchor; each sigma2 crossing joins successive bounded alpha regions including the seam. The signed crossing contributions yield the48-dimensional matrix, and the oriented exceptional correction is sum A=0. Exact rational congruences give inertia(23,25,0); separate Bareiss elimination gives determinant-7154819319988224. Signature is therefore-2. Erle's literal previous-block off-diagonal sign conflicts with the source diagram. Even B-block lengths mask this on the witness by a diagonal sign congruence; the actual mixed-parity control has distinct inertias(2,1,0)/(1,1,1). Agreement of witness inertia alone would not validate that source correction.

The independent Meyer computation uses E=im(A^-1-I) intersect im(I-B), lifts to the kernel of [A^-1-I,-(I-B)], and the form Omega(x+y,e). Kernel ambiguity lies in the radical; comparing the E form and full kernel pullback handles singular and zero-dimensional cases without inverses of singular A-I. The source's two-strand calibration fixes the positive skew-form scaling and trefoil convention. All104 terms are exactly compared:50 positive,48 negative,6 zero, sum2 and closure signature-2. Finite arithmetic supports this explicit example; it does not prove the universal topology/group statements above.

## Priority boundary

Fresh byte authentication and relevant-source inspection found no complete predecessor in this bounded evidence. The general inputs are explicitly prior. BK2015's displayed pure braid x^-4 y x^2 y has linking(-2,1,1), checked independently by strand labels, so ambient commutator membership does not put it in P3'. Otto's older example is a commutator of first-derived pure braids; its stated proof does not give third-derived membership. Kuzbaryv2 and the published DiPrisa–Framba theorem concern a quotient by the normal closure of pure braids; the quotient kills every target pure braid, so nonsolvability there does not provide this obstruction. CHH arXivv3 supplies related rho/pure-braid machinery but no inspected complete bridge to every finite P3 derived depth and F1. Actual2012 journal bytes remain unauthenticated. The author-hosted scl version is not asserted byte-identical to its2009 first edition. These bounded checks establish neither firstness nor current openness.

Mathematical gap found for the stated theorem: none under the credited foundations. Publication package gap: R7 in the new finalizer's dependency-authentication order, detailed in FULL_AUDIT.md. No new mathematical mechanism or proof response is added by this reconstruction.
