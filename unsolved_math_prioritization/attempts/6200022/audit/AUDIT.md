# Independent audit of Delzant diagonal convex cores

## Decision

**Accept the frozen disposition and both authored geometric arguments.** The universal compact convex core existence assertion for Problem 22 is false, and the negative resolution is already explicit in Dey and Liu's published work. The weighted free tree proof rules out every nonempty invariant cocompact convex subset. Under the separate, explicit proper CAT(0) hypotheses, a closed invariant cocompact convex subset does give equivariant homeomorphisms of its visual boundary with each factor boundary.

No proof correction is required. This acceptance is a conventional adversarial mathematical audit, not formal proof certification. No novelty is established or claimed. The broader cell-like equivalence question in neighboring Problem 21 is not resolved by this work.

Audited target: 6200022, AMR-061-0022, catalog rank 809. Audited author archive SHA-256: `2ed1cf89f1d8e3ea19184fa5bd14b840a2e12183b0ab4c1f0b690c9eea4f1e62` (16,021 bytes). All nine archived payloads agree byte-for-byte with the author directory. The archive and author files were preserved. This separately authored audit is bound by its own manifest and receipt.

## Identity and literature scope

The complete supplied target record, complete corresponding research report, and catalog entry were read, including nested record fields. The required Python-default sorted JSON digest of `[record, reports.get(problem_number, {})]` is `14935ce8c0a28dc4f82299acb615159f9c02d1373854aaeda75f545db8efb245`; it agrees with the catalog and author metadata. All three complete corpus byte counts and hashes were independently recomputed. The supplied earlier work is triage, not evidence of an earlier substantive solution attempt.

Kapovich's survey was checked at printed page 7, including the preceding Problem 21 and the geometric-action setup. The author freeze correctly identifies Thomas Delzant's Problem 22. The survey dates its PDF October 24, 2007 and describes the 2005 workshop origin. Its parenthetical use of the factor spaces in the boundary question needs the explicitly disclosed interpretation as their visual boundaries. The survey's local-compactness convention is on printed page 2. The negative example consists of proper trees, so it meets both the stated audited setting and the relevant standard setting of the question. The separate positive proposition is accepted only with its explicit properness and closedness assumptions.

Dey and Liu's public version 1 was independently inspected at Question 1.1, Theorem 1.2 and Corollary 1.5; pages 1 and 2 were also visually checked. It explicitly identifies Delzant's Problem 22 and states the negative answer. The theorem assumes proper CAT(0) factors, properly discontinuous isometric actions, and a single group element that is rank one in both factors; a convex-cocompact diagonal action then forces proportional marked translation lengths. The tree example satisfies these hypotheses. The stronger surface and symmetric-space conclusions have the additional hypotheses in Corollary 1.5; they are not asserted for arbitrary CAT(0) spaces here. EMS Press independently confirms online publication July 4, 2025, DOI 10.4171/GGD/908. The subscription article PDF was not accessed. This audit verifies the source statement and its applicability, and does not claim to have independently certified the entire general rigidity theorem.

Guilbault and Mooney's Examples 2.2 and 2.4 contain the relevant weighted free tree pair. Attribution to that construction is appropriate; a priority claim for the midpoint presentation would be unsupported. One substantive route followed by stopping at a verified prior resolution is appropriate. The remaining four permitted routes need not be invented.

Sources:

- [Kapovich survey](https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf), printed pages 1, 2 and 7.
- [Dey and Liu public preprint](https://arxiv.org/abs/2408.03462v1), Question 1.1, Theorem 1.2 and Corollary 1.5.
- [EMS Press publication record](https://ems.press/journals/ggd/articles/14298926).
- [Guilbault and Mooney public preprint](https://arxiv.org/abs/1011.1298v1), Examples 2.2 and 2.4.

## Independent reconstruction of the obstruction

Let F(a,b) act on its two metric Cayley trees by left multiplication. In the first all edges have length 1; in the second a edges have length 1 and b edges length 2. The geometric realizations, including edge interiors, are locally finite complete real trees with positive lower edge-length bound, hence proper CAT(0) spaces. Left multiplication preserves edge labels and lengths. The actions are free and proper and their quotients are finite metric roses. Thus both factor actions are geometric. Product distances below are Euclidean product distances, not the sum metric.

For an arbitrary positive integer n, take w = a^(4n)b^(4n). The factor distances from identity to w are 8n and 12n. A product geodesic uses the same fractional parameter in both factors. Its midpoint is therefore

    p_n = (x_n,y_n) = (a^(4n), a^(4n)b^n).

For an arbitrary group vertex g, put A = d_1(x_n,g) and B = d_1(y_n,g). Edgewise d_2 >= d_1, the ordinary triangle inequality in the first tree gives A+B >= n, and the sum-of-squares inequality gives

    d(p_n,(g,g))^2 >= A^2+B^2 >= (A+B)^2/2 >= n^2/2.

Taking an infimum over every group element, rather than a finite list of vertices, proves distance from p_n to the full diagonal orbit is at least n/sqrt(2). This is an unbounded-family proof.

For the optional exact formula, the branch point or gate of g onto [x_n,y_n] is a vertex a^(4n)b^k with 0 <= k <= n. The paths from each endpoint to g pass through this gate in both weighted trees, so deleting the off-segment part cannot increase either coordinate distance. At the gate the squared product distance is k^2+4(n-k)^2. Completing the square gives

    k^2+4(n-k)^2 = 4n^2/5 + 5(k-4n/5)^2.

The nearest integer to 4n/5 lies in [0,n], giving the exact formula in the freeze. The argument covers arbitrary off-segment vertices and all integers n; enumeration is unnecessary.

### The quantifier over every convex candidate

Suppose C is any nonempty invariant convex subset with compact quotient; this paragraph does not require C to be closed. Select q in C, and set D = d(q,o). The function c -> distance(c,Gq) is continuous and invariant, so it descends to the compact quotient and has a finite upper bound. Increasing that bound slightly yields R such that every point of C is within R of some gq. This argument needs no compact fundamental-domain choice and no attained infimum.

The midpoint c_n of [q,wq] belongs to C. Busemann convexity of a CAT(0) metric, applied to the two pairs of endpoints (o,q) and (wo,wq), gives d(p_n,c_n) <= D. Choose g_n q within R of c_n. Isometry invariance gives d(g_n q,g_n o)=D. Consequently

    distance(p_n,Go) <= D+R+D,

uniformly in n. This contradicts the established lower bound. It excludes every nonempty invariant cocompact convex candidate, with no assumption that it contains the chosen orbit or is its convex hull. Requiring closedness or minimality cannot fix the contradiction.

As controls, the marked lengths of a are (1,1), while those of b are (1,2); there is no common scale factor. Nontrivial translations of these trees have axes and cannot bound Euclidean half-planes, so a is rank one in both factors. The Dey–Liu obstruction therefore applies independently. Conversely, when all edge lengths are changed by a single factor c>0, the equivariant homothety graph is closed, convex and cocompact: both coordinates traverse corresponding segments with identical fractional parameters. Thus the obstruction is not an assertion that all diagonal actions fail.

## Independent reconstruction of the boundary proposition

Assume that G acts geometrically on proper CAT(0) spaces X_1 and X_2, and that C is nonempty, closed, convex, invariant, with compact quotient. Fix o in C. Closedness makes C proper and complete in the product; convexity gives the induced geodesic CAT(0) metric. Properness of a factor action implies properness of the diagonal action and its restriction to C. In particular C also has a geometric G action, including when stabilizers are finite rather than trivial.

Fix either factor and denote its restricted projection by f:C -> X. It is 1-Lipschitz and sends every constant-speed geodesic to a constant-speed geodesic, possibly constant. Apply the geometric-action orbit theorem to C and X using a common word metric on G. Their orbit maps are quasi-isometries and f(go)=g f(o). Extending the comparison from the coarsely dense C orbit with the 1-Lipschitz inequality yields constants A>=1 and B>=0 such that

    d_C(u,v) <= A d_X(f(u),f(v)) + B.

Moreover f(C) contains G f(o), hence is coarsely dense in X. No claim that f(C) is closed or surjective is used. Properness and cocompactness of both group actions are the essential coarse comparison hypotheses.

### Rays and uniform projected speed

For a unit ray r from o, f(r(t)) is a geodesic with fixed speed s(r). Substitution into the comparison inequality gives t <= A s(r)t+B, so s(r)>=1/A on sending t to infinity. The 1-Lipschitz inequality gives s(r)<=1. Consequently every source ray projects to a genuine ray, and the corresponding unit ray in X is

    beta_r(u) = f(r(u/s(r))).

If unit rays from different basepoints stay at bounded distance, their images at the same parameter stay at bounded distance. The difference of their distances from their respective projected basepoints is then bounded as well. Those distances are s t and s' t, so s=s'. Their normalized projected rays are asymptotic. Thus the endpoint construction is independent of the representative or basepoint, and f equivariance makes the endpoint map G equivariant.

In the compact-open ray model of the visual boundary, s(r) is read from d_X(f(o),f(r(1))), so it is continuous. Its uniform lower bound prevents arbitrarily large reparametrizations on bounded time intervals. More explicitly, if r_j -> r on compact intervals, then s_j -> s and, for u<=T,

    d_X(beta_rj(u),beta_r(u))
    <= sup_{v<=AT} d_C(r_j(v),r(v)) + T |1/s_j-1/s|.

Both terms tend to zero. This proves cone-topology continuity without using a false general quasi-isometry boundary-extension assertion.

### Injectivity and the reverse direction

If two rays r and r' based at o project to the same endpoint, uniqueness of rays based at f(o) in X gives

    f(r(u/s)) = f(r'(u/s'))

for every u. The coarse comparison gives distance in C at most B. Distances from o therefore differ by at most B, so u |1/s-1/s'|<=B for all u and s=s'. The original rays then have uniformly bounded distance. Based at the same point in a CAT(0) space, they coincide; equivalently they represent the same boundary point. This establishes injectivity, including the potential different-speed case.

For surjectivity, start with an arbitrary unit ray alpha in X from f(o). Coarse density supplies c_n in C with d_X(f(c_n),alpha(n))<=R for one uniform R. Write L_n=d_C(o,c_n) and ell_n=d_X(f(o),f(c_n)). Then

    |ell_n-n|<=R,    n-R<=L_n<=A(n+R)+B.

In particular L_n tends to infinity. Properness and Arzela–Ascoli give a subsequence of unit segments r_n:[0,L_n] -> C converging on every compact interval to a unit ray r from o. Let s_n=ell_n/L_n be their projected speeds. Since L_n<=A ell_n+B, their lower limit is at least 1/A, and their upper bound is 1. On a further subsequence s_n -> s>0. Alternatively s_n is read at parameter 1 for sufficiently long segments, so compact convergence already gives s=s(r).

Let beta_n be the unit-speed segment in X from f(o) to f(c_n). For fixed u and sufficiently large n, comparison of the two segments at fractional time u/n gives

    d_X(beta_n(u ell_n/n),alpha(u)) <= Ru/n.

Moving along beta_n from parameter u ell_n/n to u adds at most Ru/n, because |ell_n-n|<=R. Therefore

    d_X(beta_n(u),alpha(u)) <= 2Ru/n.

The bound is uniform for u in a fixed compact interval. But beta_n(u)=f(r_n(u/s_n)), whose compact limit is f(r(u/s)). It follows that alpha(u)=f(r(u/s)) for every u. Every target endpoint is attained.

Both proper-space visual boundaries are compact Hausdorff in their ray topologies. A continuous bijection between them is a homeomorphism. This also gives continuity of the inverse, rather than merely a set-theoretic inverse: every convergent target sequence has inverse subsequences in the compact source, and injectivity forces each subsequential limit to be the unique inverse limit.

If one of these geometric-action spaces is bounded, properness makes it compact and properness of the action makes G finite. Cocompactness then makes all the other spaces bounded. All relevant visual boundaries are empty. The stated boundary homeomorphism has the same vacuous interpretation in this case. For unbounded spaces the preceding ray proof applies.

A homeomorphism has singleton fibers, so it is cell-like. The proposition establishes the conditional assertion with stronger maps than requested. It provides no such conclusion in the absence of the compact convex candidate. Arbitrary CAT(0) quasi-isometries need not extend to visual boundaries; the affine-geodesic property proved above is indispensable to this argument.

## Adversarial verification and limitations

The frozen author's 77,142 exact auxiliary checks were replayed with and without optimization, from relocated copies and after archive extraction. All author-listed 20 integrity negative runs were independently repeated and rejected. The expanded independently implemented suite in VERIFY_TESTS.json records four positive and 28 negative runs for each of the author and audit packages, including self-symlink, rehashed semantic target changes, and rehashed false arithmetic output. These expanded counts include overlapping mutation categories from the original 20 controls. Normal, optimized and relocated verification all pass.

The audit checker independently tests a wider integer-weight family, with b weights 2 through 6, 30 midpoint cases per weight, exact completed squares and minima, all 1,457 reduced words of length at most 6 for seven offset cases, and the scalar normalization estimate used in surjectivity. It performs 27,534 exact finite auxiliary checks. These calculations neither establish nor simulate the infinite CAT(0) arguments. Those arguments were reconstructed in the preceding sections and are the grounds for mathematical acceptance.

The audit package includes only authored analysis, code, results and public verification metadata. It excludes third-party PDFs, extracted text, images, corpus records, private correspondence and coordination material. Hashes bind bytes, not mathematical truth. The unsigned manifest detects localized mutation under a trusted expected package; replacing the verifier and every digest together produces a different package and is not prevented without the externally recorded archive hash.

The author's bounded repository search history was inspected as a report and was not repeated by this audit. No claim about every historical branch follows. No remote mutation, publication or external communication was made. The original freeze's historical statement that audit was pending remains unchanged; this separate acceptance report records the subsequent audit outcome.
