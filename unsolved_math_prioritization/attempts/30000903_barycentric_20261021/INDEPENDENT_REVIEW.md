# Independent mathematical review of the general g theorem proof

## Verdict and exact scope

**PASS for Proposition C, Lemma D, and Theorems A and B in the identified manuscript, with the standard Macaulay raising operator.** Independent reconstruction of the argument found no mathematical gap. No corrective mathematical patch is required for this chain. The proof establishes the numerical, nonsymmetric g-theorem property for every positive integer sequence with h0 = 1 and i h_i^2 >= (i+1) h_(i-1) h_(i+1). Newton's inequalities consequently give the property for positive-coefficient real-rooted integer polynomials with constant coefficient 1.

This is a scoped mathematical review, not a claim of journal refereeing, formal proof verification, priority, or novelty. It does not establish the other part of OWR-1782-017: real-rootedness after barycentric subdivision of every nonsimplicial polytope boundary. It also does not establish the stronger Kruskal-Katona conjecture. A nonsymmetric numerical g-theorem property is not itself a claim that the original vector is a simplicial-polytope h-vector.

Review date: 2026-10-21 UTC.

## Reviewed object and method

The reviewed object is Alper Ferudun, *Real-Rooted Integer Polynomials Satisfy a g-Theorem: Proof of a Conjecture of Brenti and Welker*, dated October 17, 2026, publicly labelled an unrefereed note.

- Public deposit record: https://zenodo.org/records/23430747
- PDF retrieval URL recorded for the supplied object: https://zenodo.org/api/records/23430747/files/OWR-1782-017-paper.pdf/content
- PDF basename: `OWR-1782-017-paper.pdf`
- PDF byte count, independently checked: 156596
- PDF SHA-256, independently checked: `e38749f8ac54f08d01916145dc1870d2947d45f2e7afe05aa56e8e65fbc7e062`

The verdict is bound to these PDF bytes. Its scope is the theorem statements on page 2, the standard binomial operator on pages 3-4, the hypotheses and shape lemma on pages 4-5, Proposition C on page 5, Lemma D on pages 5-7, and the deductions of A/B on page 7. The supplied text extraction was read, an additional extraction of pages 4-7 was made from the PDF, and all four of those pages were rendered and visually inspected to check mathematical symbols and boundary cases. The associated supplied verification report was not used or read for this review. No downloaded author script was executed. The checks below were independently authored.

## Conventions and hypotheses

Write M_k(a) for the classical Macaulay operator: if a = sum_j binom(a_j,j) is its strictly decreasing k-binomial expansion, then M_k(a) = sum_j binom(a_j+1,j+1), and M_k(0)=0. This is a raising operator. All conclusions below use it, not a lower-shadow operator or a literal transcription of a different operator from a historical source.

For a positive sequence h with h0=1, put rho_i=h_i/h_(i-1), lambda_i=i rho_i, and g_i=h_i-h_(i-1). The assumed inequality is equivalent to lambda_(i+1)<=lambda_i. Positivity then gives rho_(i+1)<=i rho_i/(i+1)<rho_i. Thus the ratios greater than 1 form an initial segment. The coefficients increase strictly to their first peak, can have one adjacent equality there, and then decrease strictly. Expressions involving an index beyond d in the displayed shape statement are understood as omitted; this is only an endpoint convention.

For integer coefficients the increasing differences are positive integers, exactly what is required to apply M_k. If the first peak is r=0, h1<=1 forces h1=1; when d>=2 the first assumed inequality would say 1>=2h2, impossible. Thus the only r=0 case under the stated positive-degree hypotheses is (1,1). For d=1, or for r<=1 in any permitted dimension, all requested Macaulay comparisons are vacuous. These endpoint cases cause no gap.

## Proposition C reconstructed

Fix 1<=k<=d-1 with g_k>0 and put L=lambda_k, so L>k. Since h_(k-1)=k h_k/L,

    g_k = h_k (L-k)/L.

The next ratio is at most L/(k+1). Substitution therefore gives

    (k+1) g_(k+1) <= g_k [L-1-k/(L-k)].                  (C1)

No assumption about the sign of g_(k+1) has been used. On the other side, lambda_i>=L for i<=k and h0=1 imply h_k>=L^k/k!. Hence, with u=k/L in (0,1),

    y := (k! g_k)^(1/k) >= L(1-u)^(1/k).

The elementary logarithmic inequality ln x<=x-1, applied to x=1/(1-u), gives ln(1-u)>=-u/(1-u). Applying exp z>=1+z gives

    (1-u)^(1/k) >= 1-u/[k(1-u)].

Multiplication by L, using Lu/k=1, yields

    y >= L-1-k/(L-k).                                  (C2)

Since g_k is positive, (C1) and (C2) combine without a reversal of inequality to give

    g_(k+1) <= g_k y/(k+1)
            = (k! g_k)^((k+1)/k)/(k+1)! = Phi_k(g_k).

This verifies Proposition C. In fact the logarithm and exponential comparisons are strict here, so the claimed strict strengthening is valid. A negative right-hand bracket in (C1) is harmless: the argument never takes a fractional power of that bracket or of g_(k+1). The only fractional power has positive argument k!g_k. The denominator L-k is positive. The argument also works when k=1. The normalization h0=1 is genuinely used in the product lower bound and has not been silently dropped.

## Lemma D reconstructed

The claim is M_k(a)>=Phi_k(a) for every integer a>=1 and k>=1. Its equivalent exact-integer form is

    [(k+1)! M_k(a)]^k >= (k! a)^(k+1).

Let n be the largest upper index in the k-binomial expansion and write a=binom(n,k)+b. The greedy expansion gives

    0<=b<binom(n,k-1).

For k>=2 its remainder is the (k-1)-binomial expansion of b, so

    M_k(a)=binom(n+1,k+1)+M_(k-1)(b).

The b=0 case uses M_(k-1)(0)=0 rather than an invalid application of an induction hypothesis stated only for positive a.

For k=1, M_1(a)=a(a+1)/2>=a^2/2. For n=k and k>=2, the remainder bound says 1<=a<=k, and M_k(a)=a. The desired inequality reduces to k!a<=(k+1)^k. It follows from k!a<=k k!, the arithmetic-geometric mean estimate k!<=((k+1)/2)^k, and k<=2^k. This small-leading-index case is essential and is explicitly handled in the manuscript.

Now suppose k>=2 and n>=k+1. Define

    P=k! binom(n,k), beta=k!b, p=k/(k-1), q=(k+1)/k,
    beta_max=kP/(n-k+1), P'=P+beta_max=(n+1)P/(n-k+1).

Induction reduces the claim to

    (n+1)P+(k+1)(beta/k)^p >= (P+beta)^q                 (D1)

on 0<=beta<=beta_max. Extending the actual permitted beta range to this closed interval is safe because it only strengthens the sufficient statement.

Convexity bounds (P+beta)^q above by the chord P^q+m beta between P and P', and the mean value theorem gives 0<m<q(P')^(1/k). For any c>0, minimizing (k+1)(beta/k)^p-c beta over beta>=0, using beta=k s^(k-1), gives the exact lower bound

    -c^k [(k-1)/(k+1)]^(k-1).

Consequently the left side minus the right side of (D1) is greater than

    (n+1)P-P^q-gamma_k P',
    gamma_k=(k+1)(k-1)^(k-1)/k^k.

It suffices that

    (n+1)-P^(1/k) >= gamma_k (n+1)/(n-k+1).             (D2)

The product defining P has arithmetic mean n-(k-1)/2, so the left side is at least (k+1)/2. Because n>=k+1, the ratio on the right is at most (k+2)/2. Finally gamma_2=3/4, and for k>=3,

    ln(gamma_k)<=1/k-(k-1)/k=-(k-2)/k<=-1/3,

so gamma_k<=exp(-1/3)<3/4. The right side of (D2) is therefore at most 3(k+2)/8<=(k+1)/2 for k>=2. This proves (D2), then (D1), and closes the induction.

All signs, normalization factors and exponent conversions in this chain agree with the rendered manuscript. The excluded n=k case cannot be folded into the same estimate: at k=n=2, (D2) is false. That is not a gap because the preceding small-index argument covers it. At the closest stated small case k=2,n=3, (D2) reduces to 5/2>=sqrt(6), which is true.

## Deduction of the theorems

For each 1<=k<=r-1, the shape lemma gives g_k>0 and integrality gives a permitted positive integer input to Lemma D. Proposition C and Lemma D then give

    g_(k+1)<=Phi_k(g_k)<=M_k(g_k).

This proves A together with the previously verified shape. It does not assume symmetry or require a coefficient beyond h_d.

For a positive-coefficient real-rooted polynomial of degree d, Newton's inequalities give

    h_i^2/(h_(i-1)h_(i+1))
       >= [(i+1)/i] [(d-i+1)/(d-i)]
       >= (i+1)/i,             1<=i<=d-1.

Dropping the extra factor gives the precise hypothesis of A, so B follows. Repeated roots are permitted by Newton's inequalities. No inference from real-rootedness to strictness of the normalized Newton inequalities is needed.

## Independent exact computations

`INDEPENDENT_CHECKS.py` is an independently written corroboration script. It uses only Python arbitrary-precision integers and fractions, not numerical root solvers, floating point powers, or the author's programs. `INDEPENDENT_CHECK_RESULTS.json` contains the completed results.

- Lemma D: every 1<=k<=32 and 1<=a<=10000, totaling 320000 evaluations; no failures.
- Lemma D binomial boundaries: 2150 further evaluations for 1<=k<=64, sampling n in {k,k+1,k+2,2k,5k,10k,100k} and valid positive a at binom(n,k)-1, binom(n,k), binom(n,k)+1, binom(n+1,k)-2 and binom(n+1,k)-1; no failures. Duplicates within a given boundary selection are removed. These evaluations can overlap the dense sweep.
- Estimate (D2), manuscript (10): 6489 evaluations for 2<=k<=64, every k+1<=n<=k+100 and n in {100k,1000k,10000k}; no failures. Each test uses the equivalent comparison P<=R^k for positive rational R, avoiding root approximations.
- Proposition C: every nonincreasing lambda sequence of dimensions 2 through 8 on the rational grid {1/2,1,3/2,2,5/2,3,4,5,6,8,12}, giving 75570 ULC sequences. All 226386 indices with g_k>0 pass, including 150993 comparisons with positive g_(k+1) and 75393 automatic nonpositive-next cases. The positive-next cases satisfy the exact strict powered inequality.
- Theorem A: every positive integer sequence with h0=1, dimension 1 through 7, each other coefficient at most 24, and the assumed ULC inequalities, totaling 84083 sequences. All shapes and 134483 Macaulay comparisons pass. This includes 11349 sequences with an adjacent equality at the first peak.

Script SHA-256: `6b61cf275ba56027f41bcef20a68437af7d9590a3fb7cfcc6e8cd17d0bfce144`.

Results JSON SHA-256: `3987b10f03ac412f1c0e5d1e4aaf156fd74b47f2d18a0a65f90e7f3b19c35934`.

These finite computations corroborate, rather than prove, the unbounded statements. The universal acceptance rests on the preceding analytic reconstruction.

## Limitations and use of this verdict

The review did not audit priority searches, historical attribution, the claimed typo in the original Oberwolfach source, every downstream corollary, source-code packaging, or the author's own verification report. It does not certify a public consensus or a refereed resolution. Classical binomial representation and Newton's inequalities are accepted as standard prerequisites.

The checked proof may be cited as an independently reviewed, unrefereed proof of the general positive-integer real-rooted g-theorem assertion, provided the standard Macaulay interpretation and this exact source hash are retained. It does not justify reporting the combined record as solved while the nonsimplicial barycentric-subdivision real-rootedness assertion remains untreated. There are no must-fix findings in the reviewed C/D/A/B chain.

## Associated authored deliverables and residual review

**PASS for the mathematical content and stated limitations of the final `AUTHOR_AUDIT.md` and all five approaches in `RESIDUAL.md`.** This additional verdict is bound to the following exact files, independently rehashed after the requested minor corrections:

- `AUTHOR_AUDIT.md`: SHA-256 `f660c9a98858aaeed8e78a50e7aae3eb5d80fa67f621e75f894941566a36a553`.
- `RESIDUAL.md`: SHA-256 `e6f8583f2ac17943ae6454a699dc06ace5a492f4184ed4613bcf38e96e1faa6e`, 17992 bytes.
- `verify_residual.py`: SHA-256 `3bcb65206175505846551f21c4ad2a97888096fdba3a0a41f634a9d63acac8f7`, 2927 bytes.
- `RESIDUAL_CHECK_RESULTS.txt`: SHA-256 `4cb4b6012c1638af44fbf5eb85188464379a3805a31f7f3a57bd91a363399343`, 770 bytes.

The author-side audit's C/D/A/B reconstruction agrees with the independent proof analysis above. The local PDF, ZIP and supplied verification-report byte counts, SHA-256 hashes and MD5 checksums were independently recomputed against the saved deposit record; all match. This checksum check did not read or execute the supplied verification report or author programs. The historical source-typo and priority claims remain outside this review's independent bibliographic scope.

### Residual approach 1

The specialization H_P(t)=Phi_P(1+t,2t) and gamma_k=2^k delta_k have the correct dimension and factor-of-two normalization. Factoring at a negative delta-root gives reciprocal negative roots of the displayed quadratic, while a nonreal delta-root cannot lift to a real t. The t=-1 factors and degree-zero case are accounted for. Thus the root equivalence is correct, not merely one implication.

Murai-Nevo Theorem 1.1 and Remark 2.2 were directly checked in the [primary PDF](https://arxiv.org/pdf/1102.0096): the collapsed delta-vector has the claimed floor(d/2)-colored realization for polytopal boundaries. For d=4,5 that means a bipartite graph; its edge bound gives the required quadratic discriminant. The d<=3 cases are linear or constant. The resulting d<=5 conclusion is valid and appropriately labelled known rather than novel. The 24-cell calculation has the correct triangular two-faces, octahedral facets, H polynomial and delta discriminant 13248. Using the cube H polynomial for its octahedral facets is valid by the independently checked polarity identity.

### Residual approach 2

The cubic discriminant is correct, as are the two cubic Newton necessary inequalities. Nonnegative discriminant is necessary and sufficient for all three roots of this real cubic to be real, counting multiplicity; positivity then rules out nonnegative roots. The C=0 degeneration is explicitly treated separately.

The disjoint union of two full triangles has face polynomial 1+6z+6z^2+2z^3, is pure and three-colored, satisfies both stated Newton inequalities, and has discriminant -108. Its degree-six lift is exactly the displayed palindromic polynomial and is not real-rooted. Crucially, the report does not claim that the formal cd-polynomial is realized by a convex polytope or even an Eulerian poset. This is a valid obstruction to the proposed sufficient data, not a counterexample to the conjecture. No realizability gap is concealed.

### Residual approach 3

Both recurrences were independently derived by separating a chain at its maximal or marked face. For the marked-face identity, the lower interval has polytope dimension dim(F) and the upper interval has dimension d-dim(F)-1; their sum is d-1, exactly the power needed when converting the derivative of C_P to H_P. The cube's lower and upper face types give the asserted 26+92t+26t^2.

The source condition is accurately stated: [Hlavacek-Solus, Theorem 3.1](https://www.mat.univie.ac.at/~slc/wpapers/FPSAC2021/29Hlavacek.pdf) requires an interlacing ordering of the relative-shelling polynomials. It does not follow just from ordinary shellability. The two symmetric real-rooted summands in the note have a non-real-rooted sum; its gamma discriminant is -16. The note therefore correctly stops short of deriving global real-rootedness from real-rooted interval products.

### Residual approach 4

The refined-Eulerian recurrence has the correct orientation and normalization; its initial dimensions reproduce 1, t and then 1+t, 2t, t+t^2. The cube's mechanically computed cell-count polynomial and the two distinct transformed answers were checked. The actual answer cannot be obtained by using the Boolean formula on nonsimplicial cell counts.

[Brenti-Welker's primary paper](https://arxiv.org/pdf/math/0606356), including its Boolean-cell hypothesis and nonnegative-h assumption, was directly inspected. Applying its theorem to sd(boundary P), which is a simplicial sphere, proves the two-subdivision assertion. Polarity gives isomorphic order complexes and consequently covers simple polytopes from simplicial ones. None of these deductions is used in reverse to infer the missing one-subdivision result. The triangle example correctly demonstrates that such a reverse inference is invalid.

### Residual approach 5

The ab-index derivation identities have the stated normalization. Euler homogeneity gives the specialized derivative 2dtH+2t(1-t)H', so the pyramid and prism formulas follow with coefficients d+1 and 2d+1. The relevant identities and preservation result were checked against the [author-uploaded full text of the 2023 paper](https://www.researchgate.net/publication/369259861_Chain_enumeration_partition_lattices_and_polynomials_with_only_real_roots), Theorems 2.2 and 5.5. Direct arXiv/publisher PDF retrieval was unavailable in this review; this was not represented as successful PDF inspection. The canonical citation remains [arXiv:2205.03796](https://arxiv.org/abs/2205.03796).

The independent sign argument is sound: the highest-degree coefficient remains the original positive leading coefficient, the signs alternate at the input roots, and there is also a root in each exterior interval ending at negative infinity and at zero. Approximation handles repeated roots with fixed degree and nonzero constant term. The revised note explicitly covers d=0. The Cartesian-product and join warnings are appropriate; no unjustified multiplicative closure is asserted.

The separate claim that the cubical case is already covered is supported by [Athanasiadis's primary abstract](https://arxiv.org/abs/2009.02272). The note does not conflate that broader cubical theorem with only the stable-shelling special cases.

### Residual computations and corrections

The final residual script was read before execution and rerun successfully. Its exact symbolic expansions, discriminants and rational root-isolation multiplicity counts agree with the saved results. Its script-coverage wording was narrowed to the actual main numerical examples. The minor d=0 omission in the sign-proof exposition was corrected, and the two extra discriminant assertions were added. There are no remaining must-fix findings in the reviewed residual.

A separate program, `INDEPENDENT_RESIDUAL_CHECKS.py`, was also written without importing the residual script. It explicitly enumerates chains in concrete cube face posets, then constructs the pyramid and prism face posets and enumerates their proper-face chains again. All 15 comparisons, covering cube seeds of dimensions 0 through 4 and pyramid, prism and prism-after-pyramid operations, agree exactly with the differential operators. This independently reproduces the cube, square-pyramid, cube-pyramid and prism-of-cube-pyramid examples from incidences rather than simply reusing their claimed formulas.

- `INDEPENDENT_RESIDUAL_CHECKS.py` SHA-256: `b51e5a287424b24a061265c999f2e5e327f8c2c816e36d41a51d1cbfdb534745`.
- `INDEPENDENT_RESIDUAL_RESULTS.json` SHA-256: `44fe8038465d7129266ad5316146892108993bc8c5e2907c8c8cf44bd699e821`.

This residual acceptance certifies the five stated partial routes, examples and obstructions, subject to the cited standard prerequisites. It does not certify exhaustive search, new results, a polytopal counterexample, or a general solution. The arbitrary nonsimplicial single-subdivision assertion remains unresolved by these deliverables. No publication or queue modification was performed in this review.
