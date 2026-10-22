# Independent derivation and cross-audit: triangle modular threshold

Review and distribution status: AI-assisted and unrefereed. Acceptance means an
internal AI mathematical audit, not external human peer review or formal
proof-assistant certification. This is a prose edition, not a computational
reproduction package. No new LLT, first-resolution, or priority claim is made.

Recovery scope: all three complete authored mathematical reports were recovered
byte-for-byte and match the previously recorded SHA-256 hashes. The earlier
full evidence packages and their external seals are unavailable in this edition.
Statements below about earlier source inspection and finite checks describe
historical work recorded in those exact reports; they are not claims that the
old supporting packages were recovered or that the checks were newly rerun.

Part I retains the complete independent derivation. Part II retains the complete
mathematical cross-audit of the corrected coverage proof.

# Part I. Triangle modular equidistribution at the standard deviation scale

## Conclusion and scope

For every fixed p in (0,1), let T_n count ordinary, unlabeled triangles in G(n,p). For any sequence of positive integers q_n,

    max_{a in Z/q_n Z} |q_n P(T_n = a mod q_n) - 1| -> 0
    if and only if q_n = o(n^2).

The proposed reduction passes this independent challenge. Its substantive external input is the quantitative uniform local limit theorem of Sah and Sawhney [SS, Theorem 1.1], which supplies the required polynomial error. The rest is proved below. This is a credited consequence of prior local limit results, not a claim to a new local limit theorem or a claim of bibliographic novelty for the modular corollary. The literal triangle question is settled by the reduction; an unrestricted claim about every fixed subgraph is a different statement and is not made here.

No primality, growth lower bound on q_n, divisibility hypothesis, or assumption that the triangle-count support is surjective modulo q_n is used. No claim is made when p depends on n and approaches 0 or 1. All implicit constants may depend on fixed p.

## Exact probability normalization

Write N=binom(n,2), v=p(1-p), and Y_e=1_{e in G}-p. Then the Y_e are independent, centered, and have variance v. Set

    mu_n = E T_n = p^3 binom(n,3),
    sigma_n = sqrt(Var T_n),
    Z_n = (T_n-mu_n)/sigma_n,
    alpha = p^5(1-p),
    D_n = binom(n,2)(n-2)^2.

Every unordered pair of adjacent edges occurs in a unique triangle. Expanding the product for each triangle gives the exact orthogonal decomposition

    T_n-mu_n = L_n + R_n,
    L_n = p^2(n-2) sum_e Y_e,
    R_n = p sum_{unordered adjacent e,f} Y_e Y_f
          + sum_{triangles {e,f,g}} Y_e Y_f Y_g.

Distinct products indexed by distinct edge sets are orthogonal: an edge in the symmetric difference supplies a centered factor appearing only once. There are 3 binom(n,3) unordered adjacent edge pairs and binom(n,3) triangles. Consequently

    sigma_n^2 = alpha D_n
                + 3 binom(n,3) p^4(1-p)^2
                + binom(n,3) p^3(1-p)^3.                  (1)

Equivalently, direct covariance counting gives

    sigma_n^2 = binom(n,3)p^3(1-p^3)
                + 12 binom(n,4)p^5(1-p).                  (2)

The coefficient 12 counts ordered pairs of distinct triangles sharing an edge. In particular, for n>=3,

    sigma_n^2 >= alpha D_n,
    sigma_n^2 ~ (alpha/2)n^4,
    sigma_n ~ sqrt(alpha/2)n^2.                            (3)

Thus q_n=o(n^2) and q_n=o(sigma_n) are equivalent.

## The source theorem actually required

Let phi(x)=(2 pi)^(-1/2)exp(-x^2/2). Sah and Sawhney [SS, PDF p3, Theorem 1.1] fix a connected graph H, take p in (lambda,1-lambda), explicitly define sigma_H to be the standard deviation, and give, for every epsilon>0,

    sup_{z in (Z-mu_H)/sigma_H}
       |sigma_H P((X_H-mu_H)/sigma_H=z)-phi(z)|
       <= C_{H,lambda,epsilon} n^(-1/2+epsilon).           (4)

The theorem also gives an L1 bound, but that bound is not used here. The source's definition of copies in Section 5, PDF p28, sums once over each edge subgraph H' isomorphic to H; it does not count labeled embeddings. Taking H=K_3 gives exactly T_n. Choose, for example, lambda=min(p,1-p)/2. For fixed 0<epsilon<1/2 define delta_n=C_{p,epsilon}n^(-1/2+epsilon). Equation (4) says uniformly over every integer k that

    |P(T_n=k)-g_n(k)| <= delta_n/sigma_n,
    g_n(k) = sigma_n^(-1) phi((k-mu_n)/sigma_n).            (5)

It follows that delta_n sqrt(log n)->0. The constant is independent of k and q_n. The main result is therefore not obtained by applying a fixed-q modular theorem with an unverified dependence on q, nor by summing a qualitative local limit error over the entire support.

## Independent concentration estimate

Changing one edge can change T_n by at most n-2. Reveal the N independent edge indicators successively. The conditional-expectation martingale has, at each step, conditional range length at most n-2. Hoeffding's exponential bound for a centered variable of range length c is exp(lambda^2 c^2/8). Iterating and optimizing the exponential Markov inequality gives both tails:

    P(|T_n-mu_n|>t) <= 2 exp(-2t^2/D_n).

Using (3), for all B>0 and n>=3,

    P(|T_n-mu_n|>B sigma_n) <= 2 exp(-2 alpha B^2).        (6)

Choose the explicit window

    B_n = sqrt((4/alpha) log n).

Then (6) is at most 2n^(-8). This strength, rather than mere tightness, permits multiplying the discarded probability by q_n=O(n^2).

## The modular summation estimate

Suppress the subscript n. Let h=q/sigma and suppose h<=1 and B>=1, conditions valid eventually if q=o(sigma) and B=B_n. For a residue a, write A_a=a+qZ and take the central interval |k-mu|<=B sigma. It contains at most 2B sigma/q+1 members of A_a. Hence (5) gives the uniform central comparison

    q sum_{k in A_a, |k-mu|<=B sigma}|P(T=k)-g(k)|
       <= (2B+h)delta.                                    (7)

The omitted probability mass costs at most

    q P(|T-mu|>B sigma) <= 2q n^(-8).                     (8)

For completeness, the omitted Gaussian mass also has a uniform bound without multiplying a full integer-lattice error by q. The normalized residue grid consists of points x_j=(a+jq-mu)/sigma, spaced by h. On the positive tail, each interval [x_j-h,x_j] lies in the nonnegative half-line and phi(u)>=phi(x_j) there, provided x_j>B>=h. Those intervals have disjoint interiors. The negative tail is treated with [x_j,x_j+h]. Thus

    q sum_{k in A_a, |k-mu|>B sigma}g(k)
       = h sum_{j: |x_j|>B}phi(x_j)
       <= 2 integral_{B-h}^{infinity}phi(u)du
       <= 2 barPhi(B-1),                                  (9)

where barPhi is the standard normal upper tail.

The full Gaussian grid is uniformly close to 1. Put theta=(a-mu)/q. Poisson summation for the Gaussian, whose Fourier transform under exp(-2 pi i xi x) is exp(-2 pi^2 xi^2), gives

    q sum_{k in A_a}g(k)
       = h sum_{j in Z}phi(h(j+theta))
       = sum_{m in Z}exp(-2 pi^2 m^2/h^2)exp(2 pi i m theta).

The Gaussian series is absolutely convergent, so the identity and the following uniform bound involve no convergence interchange problem:

    |q sum_{k in A_a}g(k)-1|
       <= 2 sum_{m>=1}exp(-2 pi^2 m^2/h^2)
       <= 2r/(1-r),  r=exp(-2 pi^2/h^2).                 (10)

The last inequality uses m^2>=m. Equations (7)-(10) prove the explicit estimate

    Delta_n := max_a |q_n P(T_n=a mod q_n)-1|
       <= (2B_n+h_n)delta_n + 2q_n n^(-8)
          + 2barPhi(B_n-1) + 2r_n/(1-r_n).               (11)

If q_n=o(sigma_n), each term tends to zero: delta_n B_n->0, q_n=O(n^2), B_n->infinity, and h_n->0. This proves sufficiency.

A second check of (10) does not need Poisson summation: on each interval [h(j+theta),h(j+theta+1)], the absolute difference between its integral and h times the left endpoint value is at most h times the integral of |phi'| over the interval. Summing gives the uniform estimate

    |h sum_j phi(h(j+theta))-1| <= h integral_R |phi'|
                                   = sqrt(2/pi)h.

This weaker estimate also suffices for the full stated range.

## Necessity and the varying frequency issue

First, a CLT follows independently from the edge projection above. The standard i.i.d. Bernoulli CLT yields

    L_n/sqrt(Var L_n)
      = sum_e Y_e / sqrt(Np(1-p))  =>  Normal(0,1).

By (1), Var R_n=O_p(n^3), Var L_n=alpha D_n=Theta_p(n^4), and Var L_n/sigma_n^2->1. Therefore R_n/sigma_n->0 in L2. Slutsky's theorem gives

    Z_n => Normal(0,1).                                  (12)

Suppose Delta_n->0 but q_n is not o(sigma_n). There is a subsequence with q_n/sigma_n>=eta>0. Passing to a further subsequence, c_n=sigma_n/q_n tends to some finite c in [0,1/eta]. Since sigma_n->infinity, q_n>=2 eventually on this subsequence. The sum of the q_n-th roots of unity is zero, so

    |E exp(2 pi i T_n/q_n)|
      = |sum_{a=0}^{q_n-1} exp(2 pi i a/q_n)
                      (P(T_n=a mod q_n)-1/q_n)|
      <= sum_a |P(T_n=a mod q_n)-1/q_n|
      <= Delta_n.                                       (13)

But after centering, the modulus on the left is

    |E exp(2 pi i c_n Z_n)|.

The changing frequency cannot simply be substituted into (12) without justification. Here it is immediate from E|Z_n|<=sqrt(E Z_n^2)=1:

    |E exp(2 pi i c_n Z_n)-E exp(2 pi i c Z_n)|
       <= 2 pi |c_n-c| E|Z_n|
       <= 2 pi |c_n-c| -> 0.

The fixed-frequency implication of (12) now gives

    |E exp(2 pi i T_n/q_n)| -> exp(-2 pi^2 c^2)>0,         (14)

contradicting (13). The case c=0 is included and gives limit 1. More quantitatively, along any such subsequence,

    liminf Delta_n >= exp(-2 pi^2 c^2).

Thus relative uniformity requires q_n=o(sigma_n), and by (3) q_n=o(n^2).

## Adversarial checks on the scope

1. Arbitrarily slow approach to the threshold. If q_n=sigma_n/L_n rounded to a positive integer, for any L_n->infinity, (11) holds. No requirement L_n>>log n or even L_n>>sqrt(log n) occurs. The central error depends on B_n and h_n, not on their product with L_n. Gaussian discrepancy vanishes for every h_n->0.
2. Bounded q, including composite q. Equations (7)-(11) are uniform for q>=1. The case q=1 is exactly uniform without calculation. No finite field or prime modulus argument is present.
3. Nonmonotone q. The proof is sequencewise, and necessity uses a subsequence if q_n is not little-o. No monotonicity or convergence of q_n/sigma_n is assumed initially.
4. Support and lattice. The theorem uses the full integer lattice, not only values already known to be attainable. All residue classes are included in (11). Their eventual positive probability follows from the conclusion when Delta_n<1; it is not assumed. For q comparable to or larger than sigma_n, Fourier obstruction (14) suffices regardless of which residues are attained.
5. Mean phase. The factor exp(2 pi i mu_n/q_n) need not converge. Taking the modulus removes it exactly.
6. A qualitative additive LLT alone does not justify the selected window: if its normalized error were only delta_n=o(1), one would not know delta_n sqrt(log n)->0. A direct L1 bound of order n^(-1/2+epsilon), multiplied by q_n, only proves a much smaller range. Both shortcuts are avoided.
7. Gaussian density versus Gaussian cell mass. The source (4) uses density samples. A central unit cell integral differs uniformly from g_n(k) by O(sigma_n^(-2)) using the bounded derivative of phi. It would therefore also be harmless here, but no conversion is needed.

## Berkowitz cross-check and source defects

[B, PDF p7, Theorem 5] states an integral characteristic-function error O_epsilon(n^(-1/2+epsilon)) for the correctly centered normalized triangle count. The same page's Corollary 1 gives the uniform pointwise probability error O_epsilon(n^(-5/2+epsilon)) with lattice (Z-p^3 binom(n,3))/sigma_n. This agrees with (5) and (3). Theorem 2, PDF p3, gives the L1 error O(n^(-1/2+epsilon)).

The retained PDF visibly contains notation defects. They are not extraction errors:

- PDF p1 calls sigma the variance, although Section 2.2, PDF p4, defines sigma^2=Var(T) and normalizes by sigma.
- PDF p2, Theorem 1, uses p^3 binom(n,2) in the displayed Gaussian center. The introduction and p7 Corollary 1 use the correct binom(n,3).
- PDF p9 displays sigma~p^(5/2)(1-p)^(1/2)n^2/2. Its exact variance formula (3), PDF p8, and the independent calculation (1) instead give denominator sqrt(2).
- PDF p9, Theorem 6, prints O_epsilon(n^(.5-epsilon)), while p7 Theorem 5 states the decaying exponent -.5+epsilon. The p9 proof ends with O_epsilon(n^(-.5+2epsilon)), consistent with a decaying bound after reparameterizing epsilon.
- PDF p7, Lemma 4, also loses the lattice step h_n in its displayed conclusion and has inconsistent tail notation in its displayed proof. That lemma is neither imported nor repaired here; (7)-(9) are independent.

The arXiv landing page gives v3 dated 21 March 2017, while the retained PDF title page has internal date 27 November 2024. We identify the actual bytes rather than treating either date as a separate theorem version. These defects are why (4), from the clean Sah-Sawhney statement and its Section 5 conclusion, is the primary premise. This audit does not claim to certify every line of either paper's proof.

## Prior credit and reading limits

Scott and Tateno's 2009 OWR contribution [ST], PDF pp55-56 / printed pp1279-1280, already gives relative modular uniformity for every integer q=o(n^2/log n), without primality, and a triangle local limit theorem. It also explicitly notes the obstruction when q is of order the standard deviation. The present proof makes the sharp modular threshold rigorous using the later quantitative LLT. Their final conjecture concerns fixed subgraphs more generally; it must not be conflated with the literal triangle statement.

Directly inspected for this challenge:

- [SS] PDF pp1-3 for theorem context and exact Theorem 1.1; p5 for the normal-density definition; p25 for the fixed-size normalization; Section 5, PDF pp28-31, for unlabeled copies, exact mean/standard-deviation normalization, and concluding rate. The p3 page was rendered and visually inspected. Full PDF/text retained and hashed. The deep Fourier/decoupling proof in other sections is used as an established theorem, not independently reproved.
- [B] PDF pp1-4 and pp5-9 for the printed theorem statements, normalizations, variance formula, and high-level local-limit derivation. Pages 2, 7 and 9 were rendered and visually inspected. Full PDF/text retained and hashed. Later technical lemmas were not independently audited.
- [ST] the contribution on PDF pp55-56 was read in the retained layout extraction. Full report retained and hashed, but unrelated contributions were not substantively read.
- ArXiv landing pages for [SS] and [B] were reopened on 11 October 2026 and agree with the retained version labels. No current-status assertion beyond that metadata is required by the proof.

The three complete authored reports are recovered byte-for-byte. Earlier supporting evidence packages are unavailable in this edition; no fresh verification of those packages is claimed. File integrity and numerical controls below do not constitute a machine proof of the asymptotic theorem. The mathematical conclusion rests on the cited theorem and the explicit argument above.

## Public references

[SS] Ashwin Sah and Mehtaab Sawhney, Local limit theorems for subgraph counts, arXiv:2006.11369v1, 19 June 2020, Theorem 1.1 and Section 5. https://arxiv.org/abs/2006.11369v1 . Related journal DOI: https://doi.org/10.1112/jlms.12523 .

[B] Ross Berkowitz, A Quantitative Local Limit Theorem for Triangles in Random Graphs, arXiv:1610.01281v3, 21 March 2017 version label, especially PDF p7 Corollary 1 and p8 variance formula. https://arxiv.org/abs/1610.01281v3 .

[ST] Alex Scott, joint work with Atsushi Tateno, On the Number of Triangles in a Random Graph, in Combinatorics and Probability, Oberwolfach Report 23/2009, pp1279-1280. https://ems.press/journals/owr/articles/3473 and https://doi.org/10.4171/owr/2009/23 .

# Part II. Independent audit of the coverage proof

## Exact reviewed artifact and decision

Reviewed artifact: the corrected authored coverage proof, distributed here as PROOF.md with nonmathematical editorial changes.
Final reviewed byte count: 18,430.
Final reviewed SHA-256: 502a87ee33d99bd62bd30e605c1537373e9c6ccccc47eace3e198cb2933f1c04.
The reviewed original has been recovered byte-for-byte against this pin; ACCEPTANCE.json separately binds the editorial public edition.

Decision: PASS for the sharp fixed-p triangle modular equivalence in Sections 3-7, and PASS for the independently reconstructed ordinary-unlabeled 2K2 obstruction in Section 8. The clean Sah-Sawhney Theorem 1.1 is an explicitly imported prior theorem. No substantive gap remains in the reduction after the two minor repairs below. This mathematical review does not purport to reprove the source's deep Fourier argument or validate every ancillary bibliographic claim about other papers in the coverage table.

The initial reviewed version was 18,417 bytes, SHA-256 1c687940fe6ca27dbfece45a9c8224eb652e32c579b60b73a949ba9d431f0537. Two corrections were requested and are present in the final version:

1. The nondegenerate sigma-normalized concentration calculation starts at n>=3. At n=2, sigma=0 and an event written |T-mu|>=R sigma would have probability one.
2. The general shifted-mesh integration lemma explicitly assumes f in L1(R), as well as integrable derivative. The original written assumptions otherwise permitted f=1, for which the displayed finite quantities are not defined. The Gaussian application already satisfies the repaired hypotheses.

Neither issue changed the asymptotic triangle conclusion. Acceptance is attached only to the final hash above.

## Independent mathematical checks

The probability proof was derived independently before reviewing the coverage proof. Part I above contains this second derivation, using a residue-grid Gaussian tail and Gaussian Poisson summation rather than the coverage proof's larger global-tail window and bounded-variation estimate.

- Exact moments and count convention: the triangle is counted once; the projection and both exact variance forms agree. The leading variance is p^5(1-p)n^4/2, so sigma is of order n^2. The covariance multiplier 12 binom(n,4) is correct.
- Concentration: sigma^2>=alpha D holds exactly. The coverage proof's R^2=(16/alpha)log n gives probability at most 2n^(-32). For R>=4, (R-1)^2/2>=R^2/4; alpha<=1/4 makes the full Gaussian integer-grid tail at most 2n^(-16). Multiplication by q<=sigma=O(n^2) is therefore valid.
- Quantitative LLT: the normalized rate n^(-1/2+epsilon), uniform over all integers, is directly present in Sah-Sawhney Theorem 1.1. Standard deviation and unlabeled-copy normalization were checked in the source. Taking epsilon<1/2 makes the central-window error vanish.
- Central counting: an interval of length 2R sigma has at most 2R sigma/q+1 representatives of each residue. The exact relative comparison cost is delta(2R+q/sigma), with both factors correctly retained.
- Gaussian mesh: the corrected integrability conditions hold for phi. Its total variation is sqrt(2/pi), so the all-shift error bound sqrt(2/pi)q/sigma is valid. The independent Poisson identity supplies an additional check.
- Sharpness: if q is not little-o(sigma), pass to a subsequence with sigma/q converging to finite r>=0. The mean phase is removed by modulus. The estimate E|Z_n|<=1 justifies the varying frequency and the limiting modulus exp(-2pi^2r^2)>0. It contradicts relative uniformity because the first nontrivial Fourier coefficient is bounded by Delta_n.
- Edge cases: q=1, bounded and composite q, oscillating q, q arbitrarily slowly smaller than sigma, q of order sigma, and q much larger than sigma are all covered. No global-support surjectivity is assumed. The span-one observation in the coverage proof is correct but is not needed as a hidden extra premise.
- Cell convention: Taylor's midpoint estimate has uniform error ||phi''||_infinity/(24 sigma^3), so the source's density-sample LLT implies the original Gaussian cell-mass LLT at the stated rate.

## Independent check of the 2K2 reconstruction

For the number W of unordered adjacent edge pairs, A=N(n-2) is correct. A fixed wedge has 4n-10 distinct wedges sharing exactly one edge, giving B=A(4n-10) ordered pairs. Conditional on M=m, the exact variance identity

    Var(W|M=m)=A(pi_2-pi_4)+B(pi_3-pi_4)+A^2(pi_4-pi_2^2)

follows by separating equal, singly overlapping, and edge-disjoint wedge pairs. The expansion pi_j=r^j-binom(j,2)r^(j-1)(1-r)/N+O(N^-2), with fixed p and m=floor(pN), is uniform for j=2,3,4. Its n^4 terms cancel because B-4A^2/N=-2A. The remaining terms are O_p(n^3).

The conditional Chebyshev interval has O_p(n^(3/2)) integer values and fixed positive conditional mass. A pigeonhole atom therefore has size Omega_p(n^-3/2) conditional on M=m. The central binomial mass P(M=floor(pN)) is Omega_p(n^-1), yielding an unconditional atom Omega_p(n^-5/2). The independent centered-edge expansion for the disjoint-pair count gives variance Theta_p(n^6), so this is a factor Omega_p(sqrt n) above the Gaussian scale. Every step is valid for ordinary unlabeled copies; no homomorphism or labeled-embedding substitution occurs.

The newly authored finite controls independently enumerate all simple graphs for n=4,5,6, verify the conditional variance identity in every edge-count stratum, verify the combinatorial overlap count and cancellation, and check the unconditional variance at p=1/5,1/2,4/5. These controls supplement the algebra; they are not a substitute for the asymptotic argument.

## Scope and provenance

The historical source verification is described in Part I above and summarized with its recovery limits in SOURCES.json. In particular, the quantitative triangle premise is directly source-checked. The independent review does not claim an exhaustive priority search or verify every statement about sparse modular counts, joint counts, or current journal status. The historical report records no source-author code execution. Acceptance is specific to the reviewed mathematical text. Every mathematical step is preserved in this editorial edition; later mathematical changes require a new audit.
