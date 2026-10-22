# Independent mathematical review, round 2

The strongest verified mathematical conclusion is the full stated theorem, relative to the explicitly identified standard Teichmuller-disk and free-character theorems. No mathematical repair is requested. This is an internal AI review, not external human peer review or a formal proof-assistant certificate. The package as a whole has a separate actionable publication-coordinator finding F01.

The claim is: each fixed closed oriented genus g>=2 and finite depth k>=3 admits, for every N>=1, N pseudo-Anosovs in I_g(k) with one common exact dilatation and pairwise distinct orientation-preserving Mod_g conjugacy classes. Neither genus nor depth varies with N. The common value may vary; powers are permitted.

## Filtration and explicit deep element

Use Gamma_0=pi and Gamma_(j+1)=[pi,Gamma_j], not the more common one-based lower central series. For A(a)=ker(Aut(pi)->Aut(pi/Gamma_a)), induction on commutators gives alpha(z)z^-1 in Gamma_(a+j) for z in Gamma_j. Indeed [Gamma_i,Gamma_j] is contained in Gamma_(i+j+1), and both errors in replacing [x,z] are in Gamma_(a+j+1). Normality handles conjugates and multiplication of generators. If alpha(x)=xu and beta(x)=xv, their composites agree modulo Gamma_(a+b) because alpha(v)=v and beta(u)=u in that quotient, and uv=vu there. Thus [A(a),A(b)]<=A(a+b). Every outer class trivial on the nilpotent quotient has an automorphism representative inducing a quotient inner automorphism; its conjugating element lifts to pi, so an inverse inner adjustment supplies a representative in A(a). No assumption that an arbitrary representative acts trivially is needed.

A separating twist conjugates generators on one side by a boundary word in Gamma_1. Its errors lie in [Gamma_1,pi]=Gamma_2, proving I_g(2) membership, including g=2. The all-genus separating filling pair is a correctly scoped import from Aougab-Taylor Lemma2.2; Farb's source also states it. For a minimal filling pair, the complementary disks give mu=2g-2+F>=2g-1. Separation gives mod-two intersection zero. Thus mu is even and >=4. The exceptional mu=2 two-cusp boundary case cannot occur here.

The matrix multiplication is valid for every determinant-one C=(p,q;w,s):

    [V,C]=(1+mu*q*s, -mu*q^2;
            mu*(s^2-1)-mu^2*q*s, 1-mu*q*s+mu^2*q^2),
    trace=2+mu^2*q^2.

Starting from U=(1,mu;0,1), c_1=A and c_r=[B,c_(r-1)] lie in I_g(2r). For r>=2, q_r=-mu^(2^r-1) and trace C_r=2+mu^(2^r)>2. The sign formula is not incorrectly applied at r=1. Taking r=max(2,ceil(k/2)) makes I_g(2r)<=I_g(k). The proof requires membership only; it makes no unsupported assertion of exact filtration level.

## Endpoint separation and compact core

An eigenline corresponding to endpoint 0 would require q=0. Since q_r is nonzero, neither endpoint is 0. The parabolic V^M maps z to z/(1-M*mu*z); every fixed nonzero finite endpoint tends to 0, and infinity maps to -1/(M*mu). Both images therefore eventually lie in a small neighborhood of 0 disjoint from the original two endpoints. The images stay distinct because each Mobius map is injective. This proves existence of M without a numerical limiting argument. Normality keeps B^M c B^-M at the same chosen depth.

For hyperbolics with four disjoint endpoints, choose disjoint closed boundary intervals. A repelling half-plane lying strictly inside its interval maps, under a sufficiently large positive power, from the complement to an attracting half-plane strictly inside the attracting interval. One exponent works for both elements by taking a maximum. The side pairings and ping-pong give a free group, while strict separation puts the limit set strictly inside the paired intervals. The ideal boundary of the exterior fundamental region is disjoint from that limit set. Its intersection with the closed convex hull has no ideal accumulation, hence is compact in H2; its translates cover the hull. This is the real Schottky compact-core argument, with no finite-index or arithmetic assumption. Nontrivial elements are hyperbolic. Relations in H would map to relations in the free image J, proving derivative faithfulness on H itself.

## Uniform fusion and every ambient conjugator

Choose a compact K in X=Hull(Lambda(J)) with JK=X. Discreteness of G<=PSL2(R) makes S={s:sK intersects K} finite. If K is inside B(o,R), all such s move o by <=2R; that set of isometries is compact, since its fiber stabilizer SO(2) is compact. A discrete subgroup is closed and has finite intersection with a compact set.

Fix u and first conjugate it in J to put ONE axis point x in K. This same x is retained for every t with v=tut^-1 in J. Then tx lies on the axis of v, which is in X. For some j in J, jtx lies in K. Consequently s=jt is in the same finite S and jvj^-1=sus^-1. There is at most one displayed representative per s, so at most |S| intrinsic classes. K and S are independent of u and length. Proper powers, torsion in G, large centralizers and an infinitely generated overgroup G do not add a factor.

The compactness hypothesis is essential. In F(a,b), set J=ker(phi), phi(a)=0 and phi(b)=1. All b^n a b^-n lie in J and in one F-conjugacy class. If two were J-conjugate, the resulting centralizer equation in <a> would give n-m=0 after applying phi. Thus their J-classes are infinite; this J does not have a compact core. The actual proof never applies the lemma to the entire infinitely generated deep term.

The standard unique invariant Teichmuller disk theorem, precisely restated in Leininger Theorem3.2, forces every z in Mod_g conjugating f to h in H to preserve the fixed disk: h stabilizes D and zD. Its derivative lies in the FULL discrete stabilizer image G, not merely the two-generator image. Mapping-class conjugacy therefore implies G-conjugacy. Since H->J is faithful, the fusion bound applies. Injectivity of the entire disk stabilizer is neither asserted nor required.

## Universal traces and all-m free nonconjugacy

The actual Horowitz page648 was visually inspected in this round: stage exponents are 2m and 2m-1, and the cyclic form has closing exponent 4m. The number of sign choices is 2^m. These different uses of m are not confused.

At level m, U=W_(m-1) has y-syllables of absolute exponent <=2m-2. Cyclic reduction yields U^epsilon y^(2m-1) U^-epsilon y^(4m). The positive odd syllable 2m-1 is unique, its negative is absent, and the closing 4m marker is unique. These markers fix the cyclic alignment and recover U^epsilon as an exact reduced word. For m>1, U's highest positive odd marker distinguishes a previous choice from the inverse of any previous choice; for m=1, U=x and x differs from x^-1. Induction recovers all signs. This handles the empty set of y-syllables in U at m=1 and proves every-m nonidentity/nonconjugacy, without assuming primitivity.

For trace universality at stage j, put P=U^-1 y U and Q=y. The displayed recursion is P^(2j)Q^(2j-1)P^(2j). Flipping the jth sign substitutes P'=U y U^-1. The pairs (P,Q) and (P',Q) have equal trace P, trace Q and trace(PQ), the last by cyclic trace invariance. Every later word is the same word in the corresponding pair. The rank-two SL2(C) trace polynomial identity therefore gives equality for every representation, one sign change at a time. The use is universal, not inferred from integral examples.

The free projective representation lifts after choosing the two generator lifts in SL2(R). Every word is hyperbolic because J is convex cocompact, not merely because words have a common trace. Thus |t_m|>2. Hyperbolic H2 length is 2 arcosh(|t_m|/2), while log lambda is HALF that length. The eigenvalue formula in the paper follows, with the factor two correct. For fixed g,k,H,J,C, choosing 2^m>=CN leaves at least ceil(2^m/C)>=N ambient classes.

## Historical route and older-theory boundary

The original eight-file proof is retained verbatim in a clearly marked historical section. Its square-grid charts make every signed saddle holonomy integral; horizontal and vertical singular connections give rank two. All affine self-maps and their inverses permute these connections, hence preserve the same lattice. After choosing its basis, the entire orientation-preserving derivative group lies in PSL2(Z). Its normal index-six commutator subgroup is torsion-free free rank two. A finitely generated subgroup's finite covering core has only finitely many possible vertices from which a fixed cyclically reduced conjugacy word lifts closed. This gives the uniform fusion bound, including proper powers. The proof does not assume the twist group has finite index in the full stabilizer. The genus-two six-branch-point sphere cover gives separating lifts with eight minimal intersections and disk complements; a base bigon becomes a quadrilateral, so it introduces no upstairs bigon.

The conservative Kapovich assembly is a present-day deduction, not an independently established earlier solution date. Its ambient torsion-free free group is the modular commutator subgroup, not Mod_g; the deep subgroup need not be finitely generated. Individual affine lifts to the orientation cover suffice for the full projective derivative lattice containment; a coherent choice of lifts is unnecessary. The optional FLM small-component incidence seed remains source-qualified/unreconstructed and is not used by the current paper. Neither this route nor the main route promotes orientation reversal, inversion, ambient primitivity, simple loops, one value of infinite multiplicity or the intersection of all depths.

INDEPENDENT_MATH_RESULTS adds 2,058 exact generic commutator cases, 24 deep/endpoint cases, q-zero controls and five finite word levels in rational, trivial and changed-lift representations. All pass. These are consistency checks only. Deep Teichmuller theorems and the cited character theorem remain stated imports, and no formal certification is claimed.
