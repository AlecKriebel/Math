# Current accepted theorem and full alternative proof

The actual PR explicitly claimed the complete original target. Current acceptance is of that full mathematical theorem with the specific known same-scope preprint credited. Firstness, a new existence theorem, a new mechanism and current worldwide openness are not claimed. The following current proof uses compact cores. Historical source/inspection/execution statements in the separately reproduced original refer only to that earlier preparation and are superseded by the current priority adjudication.

# Equal dilatations deep in the Johnson filtration: a convex-core proof

Alec Kriebel — ORCID https://orcid.org/0009-0001-9320-500X. Draft dated 17 October 2026.

This is an alternative proof of a known negative answer. Alper Ferudun, *Unbounded Multiplicity in the Dilatation Spectrum of Every Term of the Johnson Filtration: An Observation on a Question of Farb*, EulerSolve Research Papers, AMR-109-0082, version 1.0, 11 October 2026, Theorem 1.1, DOI https://doi.org/10.5281/zenodo.23301731, already states a theorem containing the entire target below. No firstness, new existence theorem, new mechanism, or current openness is claimed. The present argument uses a compact convex core instead of an arithmetic lattice and virtually free overgroup. No novelty of that alternative is asserted. The passage from subgroup conjugacy to ambient conjugacy is discussed in Anderson’s earlier survey, *Variations on a theme of Horowitz*, section 5 of the author-hosted version cited below. This is classical context; none of that survey’s varying-subgroup uniformity assertions is imported.

## Target and conventions

Let S_g be closed and oriented, g >= 2; Mod_g consists of orientation-preserving mapping classes. Set pi = pi_1(S_g), Gamma_0 = pi, Gamma_(j+1) = [pi,Gamma_j], and

    I_g(j) = ker(Mod_g -> Out(pi/Gamma_j)).

Thus I_g(1) is Torelli. These are Farb's original conventions. For H <= Mod_g, multiplicity at t means the number of Mod_g conjugacy classes containing a pseudo-Anosov f in H with log(lambda(f)) = t. Conjugators are allowed to lie anywhere in Mod_g.

**Theorem.** For each fixed g >= 2 and each fixed finite k >= 3, and for every N >= 1, there are N elements of I_g(k) that are pseudo-Anosov, have one common dilatation, and are pairwise nonconjugate in Mod_g.

This is the negative answer to Farb Question 7.6. The common value may change with N. Powers are included. This does not address ambient primitivity, simple Teichmueller loops (Question 7.7), a single infinite-multiplicity value, or the intersection of all Johnson terms.

## 1. Centrality with the outer convention

Use [x,y] = xyx^-1 y^-1. Let A(a) consist of automorphisms of pi acting identically on pi/Gamma_a. For alpha in A(a) and z in Gamma_j,

    alpha(z) z^-1 belongs to Gamma_(a+j).                    (1)

Indeed, the case j = 0 is the definition. The commutator inclusion

    [Gamma_i,Gamma_j] <= Gamma_(i+j+1)

gives the induction: replacing x in pi and z in Gamma_j by alpha(x),alpha(z) changes [x,z] by an element of Gamma_(a+j+1). Products and inverses preserve the congruence, so this verifies all generators and elements at the next level.

For alpha in A(a), beta in A(b), write alpha(x) = xu and beta(x) = xv, with u in Gamma_a and v in Gamma_b. By (1), modulo Gamma_(a+b),

    alpha beta(x) = xuv,       beta alpha(x) = xvu.

They agree since [u,v] is in Gamma_(a+b+1). Consequently [A(a),A(b)] <= A(a+b). If an outer class is trivial on pi/Gamma_a, choose an automorphism representative. Its induced quotient automorphism is inner. Lift the quotient conjugating element to pi and compose with the inverse inner automorphism. This gives a representative in A(a). Taking representatives for both outer classes and then their commutator proves

    [I_g(a),I_g(b)] <= I_g(a+b).                            (2)

A separating Dehn twist lies in I_g(2). With a basepoint on one side, it fixes generators on that side and conjugates the other side's generators by the separating boundary word or its inverse. The word is in Gamma_1, so the changes belong to [Gamma_1,pi] = Gamma_2. This also holds in genus two. The calculation is compatible with the centrality input in Farb–Leininger–Margalit, proof of Proposition 4.8; it does not infer multiplicity from a least-dilatation estimate.

## 2. A hyperbolic element at the prescribed depth

Choose filling separating curves a,b in minimal position, possible for every g >= 2 (Farb, section 7.2; Aougab–Taylor, Lemma 2.2). Set A = T_a, B = T_b and mu = i(a,b). The graph a union b has mu vertices, 2mu edges, and F >= 1 disk faces. Euler characteristic gives mu = 2g-2+F >= 2g-1. Separating curves have even intersection, hence mu >= 4, also for g = 2. No sharp intersection estimate is needed.

Thurston's construction gives a half-translation flat structure and a Teichmueller disk D stabilized by A and B. In suitable coordinates their projective derivatives have lifts

    U = (1 mu; 0 1),       V = (1 0; -mu 1).                (3)

For a single pair the shear parameter is exactly its geometric intersection, by the one-by-one intersection matrix in Leininger, section 5.1.

The standard disk theorems used here are Leininger Theorems 3.1–3.2, printed pp. 1314–1315. The full disk-stabilizer derivative

    rho : Stab_Mod_g(D) -> PSL(2,R)

has discrete image and finite kernel. Hyperbolic derivative implies pseudo-Anosov, with log(lambda(f)) = hyperbolic translation length(rho(f))/2. A pseudo-Anosov stabilizes a unique Teichmueller disk. The latter is Bers's theorem as restated by Leininger; the original Bers proof is not independently rederived here. No injectivity on the whole stabilizer is assumed.

Define c_1 = A and c_r = [B,c_(r-1)]. By (2), c_r belongs to I_g(2r). For a determinant-one C = (p q; w s), direct multiplication gives

    [V,C] = (1+mu*q*s,                    -mu*q^2;
              mu*(s^2-1)-mu^2*q*s,       1-mu*q*s+mu^2*q^2).

Thus its upper-right entry is -mu*q^2 and its trace is 2+mu^2*q^2. Starting with q = mu for U, the recursively selected lifts C_r satisfy

    (C_r)_12 = -mu^(2^r-1),
    tr(C_r)  = 2+mu^(2^r) > 2,              r >= 2.         (4)

Choose r = max(2,ceil(k/2)) and c = c_r. Then c belongs to the fixed I_g(k) and its derivative is hyperbolic. Its fixed-point set avoids 0, because (C_r)_12 is nonzero. The parabolic V^M sends every projective boundary point other than 0 towards 0 as M grows: V^M(z) = z/(1-M*mu*z), including projective convergence from infinity. Choose M so the two fixed points of rho(d), for d = B^M c B^-M, lie in a neighborhood of 0 disjoint from those of rho(c). Normality gives d in the same I_g(k).

## 3. High powers and compactness

The two hyperbolics rho(c),rho(d) have four distinct endpoints. Choose disjoint closed boundary intervals about them, and geodesic repelling half-planes with their ideal intervals inside the respective repelling intervals. For a sufficiently large common power L, each image of the complementary half-plane is an attracting half-plane inside the corresponding attracting interval. The four closed half-planes are disjoint even at infinity.

Their side pairings produce the classical Schottky fundamental region P, exterior to their interiors, and ping-pong makes the two powered elements a free basis. Compactness, rather than mere absence of parabolics, is the crucial additional property. Every limit-set cylinder with a given first letter lies in the image under that letter of one of the three allowed next-letter intervals. These finitely many images are strictly inside its paired interval. Therefore the ideal boundary of P misses the limit set Lambda. If X is the closed convex hull of Lambda in H^2, its ideal boundary is precisely Lambda. The set P intersect X has no ideal accumulation point and is compact. Its translates cover X. Thus X/J is compact for

    H = <c^L,d^L> <= I_g(k),       J = rho(H).

The free matrix generators imply that their mapping-class lifts freely generate H and that rho restricted to H is injective: any nontrivial freely reduced word would have nonidentity image. So H and J are isomorphic free groups of rank two. Every nonidentity element of the convex-cocompact Schottky group J is hyperbolic, and every nonidentity element of H is pseudo-Anosov. The groups H,J are fixed now, before N varies.

## 4. Compact-core fusion lemma

**Lemma.** Suppose J <= G <= PSL(2,R), G is discrete and J is convex cocompact. A G conjugacy class of hyperbolic elements contains at most C distinct J conjugacy classes of elements of J, where the finite constant C depends only on J and G.

**Proof.** Let X be the convex hull of Lambda(J) and choose compact K contained in X with JK = X. The quotient X/J is compact, so such a K exists. The set

    S = {s in G : sK intersects K}

is finite by properness. Explicitly, put K in an R-ball about o. Every s in S has d(o,so) <= 2R. The corresponding set of orientation-preserving isometries is compact, since the stabilizer of o is compact; its intersection with discrete G is finite.

Fix hyperbolic u in J. Its axis lies in X. Conjugate u inside J to place an axis point x in K. **Keep this single u and x fixed before considering all ambient conjugators.** If v = tut^-1 belongs to J, t in G, then tx is on the axis of v, so it lies in X. Some j in J satisfies jtx in K. The element s = jt lies in S and

    jvj^-1 = sus^-1.

Every J class in this ambient class therefore has a representative on a list indexed by S. Take C = |S|. The point x depends on u, while K and S do not, so the bound is uniform in u and its length. Proper powers have the same axis and require no change. No finite generation of G, arithmetic property, finite index, centralizer bound or length bound is used. QED.

Take G = rho(Stab_Mod_g(D)). If zfz^-1 = h for nonidentity f,h in H and any z in Mod_g, then h stabilizes both D and zD. Uniqueness of the pseudo-Anosov invariant disk gives zD = D. Therefore rho(f),rho(h) are G conjugate. The isomorphism H -> J identifies their intrinsic conjugacy classes. At most C H classes can consequently merge in a single ambient Mod_g class. A finite kernel of rho on the full stabilizer causes no additional loss: only injectivity on H and the necessary implication to derivative conjugacy are used.

## 5. Horowitz families

Horowitz's Example 8.2 constructs 2^m pairwise nonconjugate nonidentity words at each level m, with equal trace under every representation of F(x,y) to SL(2,C). His recurrence is

    W_0 = x,
    W_j = W_(j-1)^(-epsilon_j) y^(2j)
          W_(j-1)^(epsilon_j)  y^(2j-1)
          W_(j-1)^(-epsilon_j) y^(2j)
          W_(j-1)^(epsilon_j),      epsilon_j in {+1,-1}.   (5)

The exponents 2j are linear; 2^m is the number of sign choices. Here is the trace and conjugacy argument, independently of finite evaluations.

Each word is freely reduced and begins and ends in x or x^-1. If U = W_(m-1), a cyclic form is

    U^(epsilon_m) y^(2m-1) U^(-epsilon_m) y^(4m).

The positive odd syllable y^(2m-1) is unique and its inverse syllable is absent. The closing y^(4m) is also unique, because the y-syllable exponents in U have absolute value at most 2m-2. These two markers anchor cyclic comparison and recover U^(epsilon_m). For m > 1 the preceding level's odd marker distinguishes U from the inverse of any other choice of U; for m = 1 use x != x^-1. Induction recovers every sign. Thus all 2^m conjugacy classes are distinct and nontrivial.

For any word in P,Q in SL(2,C), its trace is a polynomial in tr(P),tr(Q),tr(PQ), by Horowitz Theorem 3.1 and Corollary 3.14. Flipping the sign at stage j replaces the pair (U^-1 y U,y) by (U y U^-1,y), where U = W_(j-1); the later words have exactly the same expression in the corresponding pair. The trace coordinates agree, since conjugation preserves tr(y) and cyclicity gives

    tr(U^-1 y U y) = tr(U y U^-1 y).

Flipping signs one by one proves the universal common-trace identity.

## 6. Exact dilatation and ambient multiplicity

Use the free basis c^L,d^L to identify H with F(x,y). Freely choosing lifts of those generators lifts its projective representation to SL(2,R). The words in (5) have one common trace t_m under this chosen lift, and |t_m| > 2 because every word is nonidentity in the Schottky group. Hence

    ell_m = 2 arcosh(|t_m|/2),
    lambda_m = exp(ell_m/2) = (|t_m|+sqrt(t_m^2-4))/2 > 1.

The 2^m H classes have exactly this same pseudo-Anosov dilatation. By the compact-core fusion bound, they give at least ceil(2^m/C) ambient Mod_g classes. For any N choose m with 2^m >= CN. This proves the theorem, with g,k and the entire subgroup H fixed before m varies.

## Verification and disclosure

The general result rests on the written proof and named standard imports. Exact checks of the matrices and finite trace-word families are supplementary consistency evidence; they do not prove the infinite quantifiers or distinguish ambient mapping-class conjugacy by themselves. The latter uses the full-stabilizer and compact-core arguments above. A separate source-only reconstruction and its independent adversarial review support this route, without constituting external human peer review or formal certification. No complete current publication package or completed publication review is asserted by this authoring draft.

AI tools were used extensively in research, proof development, verification, literature searches and writing. Additional AI agents performed adversarial mathematical checks. This is unrefereed, has not undergone external human peer review, and has no proof-assistant certification. The author is responsible for the claims and final text.

## Primary references and exact locators

- James W. Anderson, *Variations on a theme of Horowitz*, in *Kleinian Groups and Hyperbolic 3-Manifolds*, London Math. Soc. Lecture Note Ser. 299, Cambridge University Press, 2003, DOI https://doi.org/10.1017/CBO9780511542817.015. The contextual citation is specifically section 5 of the author-hosted version, PDF pp. 18–20 / running pp. 487–489: https://eprints.soton.ac.uk/29876/1/horowitz.pdf . The fixed-subgroup compact-core lemma above is proved directly, and no stronger varying-subgroup uniformity statement from Anderson Lemma 5.4 is used. The institutional catalogue’s final range 307–341 differs from the publisher-deposited registry range 307–342; neither is conflated with the author-PDF running pages, and the paper citation omits that disputed final range.
- Benson Farb, *Some problems on mapping class groups and moduli space*, in *Problems on Mapping Class Groups and Related Topics*, Proc. Sympos. Pure Math. 74 (2006), 11–55, DOI https://doi.org/10.1090/pspum/074/2264130. Our exact question locator is the **author-hosted volume version**, Question 7.6, printed p. 51 / PDF p. 58, and the filtration is printed p. 14 / PDF p. 21: https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf . Its pagination differs from the published chapter; no final-page correspondence is inferred.
- Alper Ferudun, *Unbounded Multiplicity in the Dilatation Spectrum of Every Term of the Johnson Filtration: An Observation on a Question of Farb*, EulerSolve Research Papers AMR-109-0082, version 1.0, 11 October 2026, Theorem 1.1, PDF p. 2, DOI https://doi.org/10.5281/zenodo.23301731. This already records the target theorem and states stronger extensions. Only the present orientation-preserving original target is asserted here; no extended-group, inversion or computational extension is adopted from that paper.
- Robert D. Horowitz, *Characters of free groups represented in the two-dimensional special linear group*, Comm. Pure Appl. Math. 25(6) (1972), 635–649, DOI https://doi.org/10.1002/cpa.3160250602; Example 8.2, pp. 648–649 / PDF pp. 14–15; Theorem 3.1 and Corollary 3.14, pp. 638–641. Primary body: https://www.math.purdue.edu/~eremenko/Pdf/horowitz.pdf .
- Christopher J. Leininger, *On groups generated by two positive multi-twists: Teichmueller curves and Lehmer's number*, Geom. Topol. 8(3) (2004), 1301–1359, DOI https://doi.org/10.2140/gt.2004.8.1301. Full-stabilizer and length theorem 3.1, p. 1314; unique invariant disk theorem 3.2, p. 1315; section 5.1, pp. 1319–1321; Lemma 6.3, p. 1323. Primary publisher PDF: https://msp.org/gt/2004/8-3/gt-v8-n3-p10-s.pdf .
- Benson Farb, Christopher J. Leininger and Dan Margalit, *The lower central series and pseudo-Anosov dilatations*, Amer. J. Math. 130(3) (2008), 799–827, DOI https://doi.org/10.1353/ajm.0.0005. Preprint https://arxiv.org/abs/math/0603675, section 4.2, proof of Proposition 4.8, PDF p. 20; definition and centrality context PDF pp. 2–3. This is background for (2); our outer centrality calculation is supplied explicitly.
- Tarik Aougab and Samuel J. Taylor, *Pseudo-Anosovs optimizing the ratio of Teichmueller to curve graph translation length*, arXiv:1510.00995, Lemma 2.2, preprint pp. 3–4, https://arxiv.org/abs/1510.00995. Only existence of separating filling pairs is needed; its numerical bound is not used.


## Immutable original arithmetic argument, reproduced verbatim

# Unbounded Johnson-filtration dilatation multiplicities

This is an AI-assisted, unrefereed mathematical draft. Acceptance means an internal AI mathematical audit found the stated argument valid with the explicit standard imports; it is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, or worldwide-current-openness claim is made.

Target: Farb Question 7.6, corpus ID 11000082 / AMR-109-0082. The historical candidate has subsequently passed the complete mathematical audit in AUDIT.md. The theorem below is accepted within its exact fixed-genus, fixed-depth, ambient-conjugacy scope, subject to the named standard imports. The original mathematical argument is preserved.

## Claim

For each fixed closed oriented surface S of genus g >= 2 and every fixed k >= 3, the logarithmic pseudo-Anosov dilatation spectrum of I_g(k) has unbounded multiplicity when multiplicity counts Mod_g-conjugacy classes.

The lower central indexing is Gamma_0=pi_1(S), Gamma_{j+1}=[Gamma_0,Gamma_j], and I_g(j)=ker(Mod_g -> Out(Gamma_0/Gamma_j)).

## Imported standard facts and their exact roles

1. There is a filling pair of separating simple closed curves a,b on each S. This is stated in Farb, *Some problems on mapping class groups and moduli space*, section 7.2, printed p.51 of the supplied book, and in the precise existence statement of Aougab-Taylor, *Pseudo-Anosovs optimizing the ratio of Teichmüller to curve graph translation length*, Lemma 2.2 (preprint pp.3–4). Only existence is needed; a and b are fixed afterward. An explicit genus-two construction is also given below.
2. Thurston's construction for a filling pair equips S with a half-translation flat structure q, made from one congruent square for each intersection, such that A=T_a and B=T_b are affine and their projective derivatives are [[1,n],[0,1]] and [[1,0],[-n,1]], where n=i(a,b). The group F=<A,B> is freely generated by A,B; its derivative map is injective. For n>2, every nonidentity element except conjugates of nonzero powers of A or B is hyperbolic in the derivative representation and pseudo-Anosov on S, with dilatation the spectral radius of its derivative. References: Thurston, *On the geometry and dynamics of diffeomorphisms of surfaces*, section 6; Leininger, *On groups generated by two positive multi-twists*, Theorem 3.1 (p.1314), section 5.1 (pp.1319–1321), Lemma 6.3 (p.1323), and the proof of Theorem 6.1 and Proposition 6.4 (p.1326).
3. The Johnson filtration is central in the sense [I_g(1),I_g(j)] <= I_g(j+1). Consequently the lower central series L_1(F)=F, L_{j+1}(F)=[F,L_j(F)] satisfies L_j(F)<=I_g(j), since separating twists lie in I_g(1). This is the containment used explicitly by Farb-Leininger-Margalit, *The lower central series and pseudo-Anosov dilatations*, section 4.2, proof of Proposition 4.8. No stronger indexing convention is needed.
4. The stabilizer of the Teichmüller disk D(q) in Mod_g consists of the mapping classes represented by orientation-preserving affine automorphisms of q. A pseudo-Anosov stabilizes a unique Teichmüller disk. References: Leininger, section 3.2 and Theorems 3.1–3.2 (pp.1314–1315). The latter explicitly states the unique invariant disk theorem, attributed to Bers.
5. Horowitz, *Characters of free groups represented in the two-dimensional special linear group*, Example 8.2, pp.648-649: in a rank-two free group, for every m there are 2^m pairwise nonconjugate nontrivial words whose traces agree for every representation to SL_2(C).

The remaining ingredients and the ambient-conjugacy bound are proved below. Nielsen-Schreier, the free-group cyclic-centralizer/normalizer property, the normal-form description PSL_2(Z)=C_2*C_3, and covering graphs of free groups are elementary group-theoretic inputs.

## 1. The full disk stabilizer has integral derivatives

Scale the congruent squares in q to unit squares. Their sides are glued by maps z -> +/-z+c with c in Z+iZ. All singularities are vertices of these squares. Develop any saddle connection into the plane. Its two endpoints differ by a vector in Z^2: it starts at an integral vertex and all chart changes preserve the integral grid. Include both signs of every saddle-connection vector and let Lambda be their additive span.

Lambda is a subgroup of Z^2. It contains a nonzero horizontal and a nonzero vertical vector: the horizontal and vertical cylinder decompositions have boundary saddle connections in those directions. These boundaries are nonempty, since a closed genus >=2 flat surface has singularities. Hence Lambda has rank two and is a lattice.

Every affine self-map permutes saddle connections; its derivative sends each signed holonomy vector to another signed holonomy vector. Its inverse does too, so it preserves Lambda exactly. The derivative has determinant one, by orientation and preservation of total area of the compact surface. Thus, modulo sign, the derivative of the entire disk stabilizer belongs to

L = SL(Lambda)/{+/-I},

which becomes PSL_2(Z) after choosing a positively oriented basis of Lambda. No claim that F has finite index in the disk stabilizer is used. No claim that the disk stabilizer itself has finite index in L is used.

## 2. A fixed rank-two purely pseudo-Anosov subgroup at the chosen depth

Fix k>=3. In F define u_1=B and u_{j+1}=[A,u_j], where [x,y]=xyx^{-1}y^{-1}. Then u_j belongs to L_j(F), so u_k belongs to I_g(k). It is nontrivial: u_2=[A,B] is nontrivial, and if [A,u_j]=1 then u_j is a power of A; for j>=2 its abelianization in F is zero, so that power would be trivial, contrary to induction.

Put v_k=B u_k B^{-1}. The normality of L_k(F) gives v_k in L_k(F). The elements u_k,v_k do not commute. Otherwise B would preserve the maximal cyclic subgroup containing u_k, by the cyclic-centralizer and malnormality properties of a free group, and therefore B would itself belong to that cyclic subgroup. This is impossible because u_k has zero abelianization and B does not.

Thus H=<u_k,v_k> is freely generated by these two elements. It is contained in L_k(F) and in [F,F]. Every nonidentity element of H has zero abelianization in the A,B basis and therefore cannot be F-conjugate to a nonzero power of A or B. Fact 2 makes every such element pseudo-Anosov with hyperbolic derivative.

For completeness, n=i(a,b)>2: for a filling pair, Euler characteristic gives n>=2g-1, while n is even since a is separating. Hence n>=4 for g>=2.

Write Hbar for the injective derivative image of H in L. Since H<= [F,F], we have Hbar <= [L,L]. Let K=[L,L]. From L=C_2*C_3, K has index six, is torsion-free and is a free group of rank two. Normality and freeness can also be seen from the kernel of C_2*C_3 -> C_2 x C_3: it acts freely on the Bass-Serre tree, and the quotient graph has Euler characteristic -1.

## 3. Uniform conjugacy fusion in an ambient virtually free group

**Lemma.** Let K be a finitely generated free group and J<=K be a nontrivial finitely generated subgroup. There is a finite constant V(J) such that one K-conjugacy class contains at most V(J) distinct J-conjugacy classes. If K is normal of index d in L, then one L-conjugacy class contains at most d V(J) distinct J-conjugacy classes.

**Proof.** Model K by a finite rose and J by its covering graph. The union of immersed closed loops in the covering is a finite graph Y, after discarding any basepoint tail; this is the finite core for the finitely generated subgroup J. Let V(J) be the number of its vertices.

Choose a nonempty cyclically reduced word w representing the specified K-conjugacy class. Any J-conjugacy class in that K-class is represented by an oriented closed immersed loop in the covering projecting to w, after cyclically selecting its starting point. Such a loop lies in Y. A lift of the fixed word w is uniquely determined by its initial vertex. Thus there are at most V(J) possible loops, and hence at most V(J) J-conjugacy classes. This remains valid for proper powers; no primitivity assumption is used.

If K is normal of index d, fix representatives r_1,...,r_d for L/K. The L-conjugates of x in K lie in the union of the K-conjugacy classes of r_i x r_i^{-1}. Apply the first part to each of at most d such classes. QED.

Apply this to J=Hbar <= K <= L. Its core graph is fixed once g,k,a,b have been fixed. Put C=6 V(Hbar). This finite C is independent of all later trace words and dilatations.

## 4. Ambient mapping-class conjugacy reduces to L-conjugacy

If x,y in H are nontrivial and t x t^{-1}=y in Mod_g, then y stabilizes both D(q) and tD(q): the former because y is affine for q, the latter because x stabilizes D(q). By the unique invariant disk theorem (Fact 4), tD(q)=D(q). Fact 4 therefore gives an affine representative of t, and its derivative belongs to L by section 1.

Consequently the derivatives of x,y are conjugate in L. The injectivity of the derivative on H and the lemma show that a single Mod_g-conjugacy class can contain at most C distinct H-conjugacy classes. Possible finite kernels of the derivative on the full disk stabilizer cannot increase this bound: we need only the necessary implication from mapping-class conjugacy to derivative conjugacy, and injectivity on H.

## 5. Equal dilatations and unbounded ambient multiplicity

Identify H with the abstract rank-two free group using u_k,v_k. Since H is free, its projective derivative representation lifts to an SL_2(R) representation by choosing arbitrary lifts of the two generator matrices. For each m apply Horowitz's Example 8.2 to obtain 2^m distinct H-conjugacy classes represented by nonidentity words w_{m,1},...,w_{m,2^m} with a common trace t_m in this lift.

Every w_{m,i} belongs to the fixed H<=I_g(k), and every nonidentity element of H has hyperbolic derivative. Thus |t_m|>2, and all these mapping classes have the same dilatation

lambda_m = (|t_m| + sqrt(t_m^2-4))/2 > 1.

At most C of these H-conjugacy classes can lie in one Mod_g-conjugacy class. Therefore the multiplicity of log(lambda_m) in the target ambient spectrum is at least ceil(2^m/C), which tends to infinity. Both g and k, and even H itself, were fixed before m varied. QED.

## Scope and limitations

This is not an intrinsic-subgroup counting argument: section 4 and the uniform bound in section 3 are indispensable. It does not vary genus or depth, and it does not use least-dilatation estimates as multiplicity estimates. The common spectral value may change with m, as the question allows. It makes no assertion that one fixed value has infinite multiplicity. Source checking is bounded, so the absence of a directly located earlier answer is not a novelty or worldwide-openness certificate. The subsequent internal mathematical audit checked all imported facts, including the disk-stabilizer identification and the precise two-parabolic classification; see AUDIT.md for the source passages, the explicit free-basis justification, and the acceptance boundaries.

## Explicit fixed genus-two geometric seed

On a sphere draw two transverse simple closed curves intersecting in four points. They cut the sphere into six disks, three on either side of either curve. Mark one point in each disk and take the connected two-fold cover branched over these six points. Its Euler characteristic is 2*2-6=-2, so it is a closed genus-two surface. Each base curve encloses three branch points on each side; its inverse image is a single separating simple closed curve, bounding a once-holed torus on either side. Each complementary disk contains exactly one branch point and therefore lifts to a disk. Each base intersection has two lifts, giving eight intersections upstairs. A complementary base polygon has at least two sides; its branched double cover has twice that many boundary sides. Hence no complementary upstairs region is a bigon. The bigon criterion gives geometric intersection exactly eight, and the two separating lifts fill. This supplies a concrete g=2 seed for the matrices used in the finite algebra checks; no genus changes occur in that calculation.

## Public source links

- Farb, Question 7.6 and context: https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf (PDF p.58 / printed p.51).
- Leininger, *On groups generated by two positive multi-twists: Teichmüller curves and Lehmer's number*, Geometry & Topology 8 (2004), 1301–1359: https://arxiv.org/pdf/math/0304163 ; DOI https://doi.org/10.2140/gt.2004.8.1301 .
- Horowitz, *Characters of free groups represented in the two-dimensional special linear group*, CPAM 25 (1972), 635–649: https://www.math.purdue.edu/~eremenko/Pdf/horowitz.pdf ; DOI https://doi.org/10.1002/cpa.3160250602 .
- Farb, Leininger, Margalit, *The lower central series and pseudo-Anosov dilatations*, American Journal of Mathematics 130 (2008), 799–827: https://arxiv.org/pdf/math/0603675 .
- Aougab, Taylor, *Pseudo-Anosovs optimizing the ratio of Teichmüller to curve graph translation length*: https://arxiv.org/pdf/1510.00995 , Lemma 2.2 (preprint pp.3–4).

## Finite check boundary

The independently authored supplementary finite check (not distributed in this prose edition) evaluates the cited Horowitz recurrence for m=1,2,3,4 under three integral SL_2 representations, one obtained from the n=8,k=3 commutator subgroup. Exact traces agree within each family, and free cyclic-word checks distinguish 2^m conjugacy classes. Normal, -O and -OO runs produce identical receipts. These are illustrative checks only. They do not replace Horowitz's theorem, prove arbitrary-m growth, or by themselves establish ambient mapping-class nonconjugacy. The latter follows from sections 1–4.
