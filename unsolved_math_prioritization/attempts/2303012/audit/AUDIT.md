# Independent adversarial audit: Kjellberg Problem 3.12

- Problem: 2303012 / AMR-022-3012, queue rank 569
- Audit date: 4 October 2026 UTC
- Verdict: **PASS as `already_solved`, 1/5**
- Frozen author-manifest SHA-256: `b7c33cc6ea9aa6757e260c9bfc0648af2f9840122d0e94a793d492685e1629ba`
- Frozen proof SHA-256: `3f0e7cb57827f803d78ce601a1b5195c3efaf2e53ce3432af65955e040ce77fd`

## 1. Decision and its limits

The frozen packet correctly identifies an exact prior affirmative resolution, rather than a new solution. Benedicks's Corollary 3, printed p. 67, supplies the requested uniformly bounded upper-half-space remainder in all requested dimensions. The potentially consequential extra hypothesis, Dirichlet regularity of every point of the deleted set, is correctly derived from the target's strictly positive harmonic function and its continuous zero boundary values. I found no mathematical blocker to `already_solved`.

This is an independent mathematical and source audit of a deduction from a published theorem. It is not a formal proof certificate, an exhaustive literature search, or certification that the paper contains no possible undiscovered error. The standard Green-function, Harnack, maximum-principle, and Herglotz results are used as classical potential theory. The original 1974 question leaf remains unexamined. That historical limitation is explicitly disclosed and does not obstruct the exact match between the retrieved 2018 statement and 1980 theorem.

The frozen author files were not edited. Their `independent_review_status: pending` is an authentic pre-audit state; this separate report records the subsequent review. No additional substantive proof-attempt turn was used: this is verification of the complete frozen source-based argument, not an extension of an unfinished candidate.

## 2. Exact target and primary-source identity

I read the entire catalogue statement and imported prior report, and visually inspected Hayman--Lingham's Problem 3.12 and Update 3.12, printed p. 64 / PDF p. 65. The update's bibliography entry [80], printed p. 208, names Benedicks, Arkiv for Matematik 18 (1980), 53--72. I did not infer the specific answer from the update's broader Martin-boundary summary.

The target asks about a domain in R^3 with complement in its separating plane, one fixed radius and one fixed positive lower area bound, and a positive harmonic function continuous on R^3 and zero on the complement. It asks for a single linear vertical term and a uniformly bounded remainder above the plane, including the R^m analogues for m > 3. The infinite-connectivity condition is retained in the source identification. The resolving result has no need for that restriction and therefore covers it.

The mapping uses ambient dimension m = n + 1, vertical coordinate y = x_m, and the measure of the n-dimensional separating hyperplane. In particular n = 2 is the R^3 case; n >= 3 covers the additional requested cases. The paper does not restrict to n = 1 until after Corollary 3. Requiring a subset of measure exactly epsilon and requiring total intersection measure at least epsilon are equivalent here, since Lebesgue measure is nonatomic. The radius is fixed, not quantified over arbitrarily small radii.

I visually inspected the original paper's introductory assumptions, representation formulas, density-lemma statement, and decisive corollary. An independent HTTP download of the original 20-page article returned 200 and reproduced all 682,635 bytes with SHA-256 `a24b38583e76fbb3e14178608099e73dc2b0883e9f070a66032456320ee26811`. Both supplied source PDFs match their frozen hashes.

Primary references:

- W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, [arXiv v2](https://arxiv.org/abs/1809.07200v2), Problem/Update 3.12, p. 64.
- Michael Benedicks, *Positive harmonic functions vanishing on the boundary of certain domains in R^n*, [DOI](https://doi.org/10.1007/BF02384681), Corollary 3, p. 67; [original article](https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7328-11512_2006_Article_BF02384681.pdf).
- Yngve Domar, *On the existence of a largest subharmonic minorant of a given function*, [DOI](https://doi.org/10.1007/BF02589497), Theorem 2 and proof, pp. 431--433; [original article](https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/6940-11512_2007_Article_BF02589497.pdf). Benedicks cites it as 1957; archive metadata uses 1958. The issue scan records communication on 13 March 1957. No publication-priority conclusion depends on this metadata difference.

Benedicks's reference [13], p. 72, attributes the question to Kjellberg, Problem 3.12, p. 163 of the 1974 Canterbury proceedings. The packet properly distinguishes that attribution from having retrieved the 1974 leaf.

## 3. The regular-boundary bridge survives adversarial checking

A fixed-scale area condition alone does not rule out a thin irregular local appendage. Omitting the paper's regularity hypothesis would therefore be a real gap. The packet does not omit it.

Here is the audit of its separate comparison argument. E is closed because it is the complement of a domain. It is a proper subset of the separating plane: deleting the entire plane would disconnect its complement, contrary to the domain assumption. Fix p in E. There is a plane point a outside E with an ambient neighborhood disjoint from E. A ball B centered at p can contain that neighborhood. Its two open half-balls connect through the neighborhood of a; any other point in B on the plane but outside E also connects to a half-ball. Consequently Omega = B minus E is a bounded connected domain.

For any q in Omega choose a closed pole ball K = closure B(q,delta) compactly contained in Omega, with p outside K. Strict positivity and continuity give b = min_boundary(K) u > 0. The Green function of B is finite on boundary(K), so M = max_boundary(K) G_B(.,q) < infinity. On a smooth relatively compact exhaustion Omega_j containing K, compare G_Omega_j(.,q) with (M/b)u on Omega_j minus K. On the inner boundary this follows from domain monotonicity G_Omega_j <= G_B; on the outer boundary the Green function is zero and u is positive. Both compared functions are harmonic away from K. The maximum principle and monotone exhaustion thus yield

    0 <= G_Omega(z,q) <= (M/b)u(z),  z in Omega minus K.

Continuity of u at p now gives an ordinary, unrestricted interior limit G_Omega(z,q) -> 0 as z -> p. This is established for every interior pole q, so there is no ambiguity between different formulations of the Green-function regularity criterion. The criterion makes p regular for Omega. Since Omega and D agree in a neighborhood of p, locality transfers regularity to D. Bounded planar domains are Greenian too, so the argument has no hidden m >= 3 restriction.

I checked the following possible defects and found none: positivity of b, existence of a connected cut-ball domain, exhaustion before any boundary regularity has been established, absence of the pole from the limiting neighborhood, and the final locality step. Smooth exhaustion uses only relatively compact subdomains, whose boundary values are classical; it does not presume the desired regularity of E. If the word positive were instead interpreted as nonnegative, the identically zero case is immediate; otherwise the strong maximum principle supplies strict positivity.

## 4. Analytic dependency chain inspected

Within Benedicks I read Lemma 1 (p. 54), Lemma 2 and (2.3)--(2.4) (p. 55), Lemma 3 and its proof (pp. 55--56), the relevant reflection argument of Lemma 6 (pp. 57--58), and the entire Lemma 8 proof (pp. 63--66), followed by Corollary 3. The dependency chain for the exact conclusion is growth plus escape estimate plus half-space representation. It does not require importing the separate Martin-boundary classification as a replacement for boundedness.

The additional external input to Lemma 1 is Domar's Theorem 2. I retrieved its original 12-page scan, read its statement and proof, and visually checked pp. 431--433. The file is 395,498 bytes with SHA-256 `72b9773cc258c5b4616844459cc1899dfd8257282fcdfc34d588c8f4ca27747c`. This closes the original-source check one step beyond the frozen packet's listed lemmas.

The following are my specific mathematical checks on the chain, rather than claims made by the replay program:

1. **Local boundedness input.** For the majorant |y|^(-n) in dimension k = n + 1, every finite power of log-positive of that majorant is integrable across y = 0: substitute t = -log|y| in the one-dimensional integral. Thus Domar's hypothesis is satisfied. His proof derives a uniform compact bound by a mean-value amplification argument and Holder's inequality, without relying on the later Martin results. To obtain Benedicks's stated strip bound, the part with |y| bounded away from zero is already bounded; the remaining strip is compactly inside the ball.
2. **Global growth.** Symmetrization is legitimate: u(x,y) + u(x,-y) is positive harmonic on the same domain and dominates u. Zero extension across E is subharmonic. The half-space representation gives the vertical bound for large height, Harnack gives the bound away from the plane, and the scaled local boundedness input treats neighborhoods of the plane. The result is a constant A, allowed to depend on u, with u(z) <= A(1+|z|) globally.
3. **Escape estimate.** I visually checked the poorly extracted formulas on printed pp. 64--66. In the matrix argument, the row deficit is proportional to eta, the off-diagonal decay exponent is n+1, and the weight is max(R-|j|,K). The near, intermediate, and far sums give contraction after K is chosen proportional to sigma^(-2). The inverse contraction costs sigma^(-1), giving the eta^(-3) factor. Positivity justifies the vector inequality and geometric-series inverse. Rescaling restores h/R. Constants may depend on the fixed dimension; the target requires no uniformity as dimension tends to infinity.
4. **Boundary values of escape probability.** Its values are interpreted as harmonic measure in the slit ball. Interior slit points have the regularity already checked. The meeting of slit and outer sphere does not authorize assuming simultaneously continuous 0 and 1 data there; the harmonic-measure/Perron interpretation used in the paper avoids that issue. The packet explicitly imports this analytic estimate rather than pretending the rational fixtures prove it.

## 5. Independent check of the final implication

Let eta = epsilon/(v_n h^n). For a point a of the separating plane outside E, and a sufficiently large ball of radius L centered there, comparison with the sphere's maximal boundary value and the cited escape estimate gives

    u(a,0) <= A(1+|a|+L) C_n h/(eta^3 L).

For each a choose L at least 1+|a|+h, increasing it if necessary. Then (1+|a|+L)/L <= 2, uniformly in a. Hence the trace is bounded by 2 A C_n h/eta^3. On E the trace is zero. This is a genuinely uniform estimate over the whole separating plane, not merely a bound at each individual point with a location-dependent constant. One may also let L tend to infinity for each fixed a.

The Herglotz representation has a nonnegative linear coefficient c. Continuity on the whole plane means its boundary measure is the density f(x) = u(x,0), not an extra singular measure. The remainder is its Poisson integral. Independently of any finite dimension sweep, its kernel has mass one for every integer n >= 1: radial integration gives the product

    [Gamma((n+1)/2)/pi^((n+1)/2)]
    [2 pi^(n/2)/Gamma(n/2)]
    [Gamma(n/2) Gamma(1/2)/(2 Gamma((n+1)/2))] = 1.

The last factor is the beta integral after r/y = tan(theta). Therefore 0 <= phi <= sup f on the whole upper half-space. This verifies the precise boundedness needed by the target. It does not assert one common linear coefficient on both half-spaces. If two coefficients represented u with bounded remainders, their difference multiplied by y would be bounded for all y > 0; thus they agree. The asserted uniform large-height limit follows immediately.

These calculations are audit checks of the complete frozen argument, not a claim of an independent new proof of the difficult harmonic-measure estimate.

## 6. Replay, scope, and operational checks

All of the following passed independently:

- External frozen-manifest SHA-256 anchor.
- Exact file-set, size, and SHA-256 verification for the nine files listed by that manifest.
- `verify.py`: 50 exact Poisson normalization fixtures, 108 rational cancellation fixtures, and 12 rational coefficient-uniqueness fixtures.
- `verify.py --source-dir ...`: both private source PDFs match the recorded bytes and SHA-256 values.
- The no-source replay equals the saved `CHECKS.json` as a JSON object.
- Python compilation of both author scripts, with bytecode redirected outside the frozen packet.
- The independently downloaded Benedicks PDF equals the author's source byte-for-byte.
- The proposed queue-row patch changes only Status (`queued` to `already_solved`) and Turns (`0/5` to `1/5`); every other parsed cell is identical.

The script assertions that status is `already_solved` and gap is null are metadata consistency checks, not evidence for those mathematical judgments. Fifty dimensions do not prove an all-dimensional statement; finitely many rational substitutions do not prove a universal inequality; hashes identify bytes, not truth. The all-dimensional conclusion rests on the original theorem and the analytical reasoning above.

The imported report's claimed 2018 open status is contradicted by the actual primary sources. No fabricated failed attempts or novelty claims should be added. The proposed `already_solved`, 1/5 disposition is appropriate.

This audit did not perform new exhaustive repository searches. It inspected the packet's recorded bounded-search evidence and makes no stronger no-duplicate claim. Publication must continue to exclude all source PDFs, page images, extracted source text, raw reports, and private working material. Only the authored audit files explicitly listed in `AUDIT_MANIFEST.json` (and that manifest) are audit publication candidates. No remote writes or source uploads were performed.

## 7. Findings

- Blocking mathematical findings: none.
- Blocking reproducibility findings: none.
- Required correction to frozen proof: none.
- Historical qualification to retain: original 1974 question page not retrieved.
- Epistemic qualifications to retain: source-based, AI-assisted, unrefereed, not machine-verified, and no novelty or first-priority claim.
- Final recommendation: accept the frozen packet and this separate audit as an exact prior-resolution correction, `already_solved`, 1/5.
