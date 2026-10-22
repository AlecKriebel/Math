# Independent adversarial review: 30005718

**Verdict: PASS for the explicitly scoped partial results. No mandatory mathematical correction. Original all-size problem remains unresolved; all five substantive author turns are consumed.**

Review completed 2026-10-03. The review is a fresh audit of the complete frozen packet, not a claim to have recovered an earlier review. No sixth author research turn was conducted.

## 1. Exact version, recovery, and scope

Repository: AlecKriebel/Math. Frozen branch: `math/30005718-ulc-matrix-wip`. Its head was read directly and remains `b31d30a0651f3a9f1310a0473a20a6b2204fc624`.

The reviewed folder is `unsolved_math_prioritization/attempts/30005718`. All 41 files were reconstructed and checked against their Git blob SHA-1 identities and byte lengths. The final author manifest has SHA-256 `69c4c24dde28eab7cb569ede2ce93d0bf326453aac88c6b897d0b2d926def6e0`; its 40 bindings and all five historical manifests, 152 bindings in total, pass. The author packet contains a review request and historically accurate `independent_review: pending` fields, but no independent-review report. No old review was recovered from this packet or the current local filesystem. The complete branch-name search returned only the author branch, and the numeric all-state PR search and exact-head PR collection were empty. These searches do not assert that no unindexed historical review could ever exist.

I read the source gate, all five turn proofs, all research logs and turn ledgers, final statement, manifests, and all checker source code. Original bytes remain untouched. This report is additive and supplies the independent verdict for that version.

The target is the original polynomial V_n=T_n+Q_n+C_n, n>=4, from Poullot's specified three-state matrix and starting vector. Its actual degree is d_n=floor(3(n-1)/2). ULC means log-concavity of v_(n,k)/binomial(d_n,k), with the initial zero coefficients retained and no internal zeros. The relevant exact margin is

    k(d-k)v_k^2 - (k+1)(d-k+1)v_(k-1)v_(k+1).

The full target asks for every n; eventual ULC, ordinary log-concavity, or a fixed-width band cannot be substituted for it. The qualitative request for general polynomial-matrix methods is addressed only by sufficient criteria with explicit hypotheses.

## 2. Primary-source audit and credit

The official [OWR 58/2023](https://ems.press/content/serial-article-files/48169), printed pp.3308-3309, Problem 6, was downloaded, text-read, and both complete pages were visually inspected. The matrix, initial polynomials, summation defining V_n, all-n quantifier, and the homogenization/Lorentzian remark match the packet. The preceding M-convex/Pluecker questions really belong to a different problem; the imported background contamination is correctly identified. The source's sequence subscript and its supposed constant coefficient v_(n,4)=4 are typographical inconsistencies; the recurrence gives v_(n,3)=4.

[Poullot 2411.14102v3](https://arxiv.org/abs/2411.14102v3), Proposition 5.4, Theorems 5.6-5.7, Example 5.8 and Conjecture 6.2, were checked. The exact recurrence, eigenvalues, degree, leading coefficients, and fixed-low-coefficient polynomial facts are prior material. The paper explicitly retains ordinary log-concavity as a conjecture. [Juhnke-Poullot 2504.20739v3](https://arxiv.org/abs/2504.20739v3), Example 3.8/Problem 3.9, reproduces this same family and retains its unimodality/log-concavity question. General negative examples for other polytopes do not answer this instance.

The author-linked [Flajolet-Sedgewick book](https://ac.cs.princeton.edu/home/AC.pdf), printed pp.586-589, was checked. Theorem VIII.8 gives compact-saddle uniformity and full expansions under its stated assumptions. The packet does not apply its scalar positivity assumptions blindly to a Perron eigenvalue with potentially negative Taylor coefficients. It gives the required matrix spectral bound and a separate small-saddle argument. The methods are classical; the review does not certify historical novelty of any scoped consequence.

All four downloaded PDFs match the frozen source hashes exactly: OWR `416426fae5c204fbcf574be1da44b34c7cab126ded75d6b4e44f730e4a92d2ac`; Poullot `a7353e014d1c6d4e6361dd5553ac0e758d714edfa750c5e8739a4f98e5bdbbcc`; Juhnke-Poullot `b159a2a3798fad8748ff632128f41fc3e4f115c9b1b031a6a732834531d2eece`; book `0ea919997c052b567fad61407092f79d6ce9dd17934c7e9f124dcde3390d5584`. They are verification inputs, not republication deliverables.

## 3. Turn 1: reduction and all-size boundary inequalities

The invariant T-Q=C/(1+z) holds initially and is preserved by the original matrix. It yields the exact positive transfer

    N(z) = [[1+2z,z],[z+z^2,1+z]],
    z^(-3)V_(m+4) = (2+z,2) N(z)^m (2,z)^T.

The degree/support induction in the packet is valid, including n=4 and both parities. In particular, cancellation cannot create internal zeros: all relevant recurrence coefficients are nonnegative and the support intervals overlap or touch.

The lower formulas v_3=4, v_4=12n-44, v_5=4(n-4)(4n-17) give the displayed positive polynomial margins. Index k=4 at n=4 is an endpoint rather than an interior comparison; the proof correctly separates that case.

The unipotent truncation lemma is sound despite noncommuting matrices. In a length h(q+1) word in J+wR, at most q positive-degree factors leave at most q+1 J blocks; otherwise some block has length at least h. This proves the claimed nilpotence modulo w^(q+1) and a finite binomial expansion, for every nonnegative integer row parameter.

The two-step reversal K=w^3 N(1/w)^2 has constant I+3E_21. The parity shifts and cancellation of the apparent w^(-1) term are correct. The top-three formulas and their degree-normalized margins agree both symbolically and with the unreduced source recurrence. The unrestricted-preservation counterexample and the stripped D_6 counterexample are valid warnings, not counterexamples to V_n.

**Turn 1 passes.** It proves first/last ULC comparisons and an explicitly fixed-tail method, not the growing interior.

## 4. Turn 2: compact proportional bands

I independently differentiated the Perron eigenvalue and verified the exact alpha, variance, amplitude and inverse-variance-gap formulas with a separate rational-function implementation in SymPy. The numerator positivity groupings for variance and gap are valid for t>sqrt(5); all denominator factors have the asserted signs. Thus alpha increases bijectively from 0 to 3/2 and

    1/s - 1/alpha - 1/(3/2-alpha) > 0.

There is no unverified periodic-saddle assumption. For theta not divisible by 2pi, each diagonal entry 1+c*rho*exp(i*theta) has strictly smaller modulus than its positive-real value. A positive Perron vector turns this into strict domination of both weighted row sums. Compactness gives a uniform away-from-zero norm ratio below 1; powering the matrix therefore suppresses every competing arc. Near the positive real axis, separated eigenvalues give analytic projections and a uniform spectral gap.

The first corrected saddle expansion is sufficient for adjacent coefficients. Its error is uniformly relative O(m^(-3/2)), not merely O(m^(-1)). The explicit first correction is smooth in alpha, so its adjacent second difference has smaller order. The three un-differentiated residual errors remain O(m^(-3/2)); no unjustified differentiability of the residual is used. The strictly positive inverse-variance gap has a positive minimum on every fixed compact band, dominating these errors. Enlarging the band before taking neighbors handles the endpoints correctly.

The generic criterion states analytic dominance, aperiodicity/suppression, positive variance and a strict binomial-variance gap. Its sufficiency is justified by the same proof; it is not a universal preservation classification.

**Turn 2 passes.** Its quantifier is eventual strict ULC on each fixed proportional band, with a band-dependent threshold.

## 5. Turn 3: marking, unimodality, and fixed edges

The zero-factor marking lemma correctly retains matrix order. In the degree-ell term at least r-ell transfer factors have degree zero, including when endpoint vectors contribute positive degree. Multiplication by the other nonnegative factors preserves the coefficientwise inequality. The case r-ell<=0 is trivial. For N one may take gamma=1; for the reversed K one may take gamma=5/3. The extra factor w in the reversal is correctly responsible for h+2 and r-h-1 in the upper inequality.

The proposed overlap constants are valid: m>=256 makes the lower and upper strict-monotonicity intervals overlap the log-concave middle sufficiently. Strict ordinary log-concavity makes the positive adjacent ratios strictly decrease there. Their crossing can therefore yield one maximum or two adjacent equal maxima, but no separated maxima. This uses no computable value for the separate asymptotic threshold.

For fixed lower j, the finite binomial expansion of N^m makes the coefficient a polynomial of degree j, with leading coefficient 4F_(2j+2)/j!. Cassini gives the positive normalized leading margin claimed in the text. Fixed j is essential.

The maximal-word arguments at the reversed edge correctly handle the endpoint annihilations. Even parity permits at most 2h+1 factors, with the unique alternating R,J pattern of weight 3^(2h+1). Odd parity permits at most 2h, with weight 3^(2h). Positive-degree endpoints and higher-degree matrix factors strictly decrease the maximum length. Consequently the stated polynomial degrees, factorial leading coefficients and positive leading ULC margins follow, including h=0 conventions.

The characterization of a hypothetical unbounded sequence of violations is sound: compact proportional bands exclude positive limiting edge proportions, while finitely many fixed-distance theorems exclude bounded distances. It does not promote either argument to uniform shrinking-edge control.

**Turn 3 passes.** Eventual whole-row unimodality and eventual strict ULC at each fixed edge distance are correctly scoped.

## 6. Turn 4: the main analytic risk, reviewed in detail

### Uniform small-saddle lemma

This is the essential step and cannot be certified by finite algebra tests alone. I checked the proof directly.

If f(z)=az+sum_(ell>=2)b_ell z^ell with a>0, convergence on a larger disk bounds the weighted tail sum by a*rho/2 for all sufficiently small rho. The inequality 1-cos(ell*theta)<=ell^2(1-cos(theta)) is valid for every integer ell. It gives a uniform full-circle bound with large parameter m*rho comparable to j=m*alpha, even if some coefficients of the analytic functions are negative. A positive real amplitude near zero and a nonzero analytic Lambda are sufficient here.

For each fixed ell, D^ell f / alpha extends analytically at zero, as does D^ell A/A. The angular Taylor remainder after order six has an extra factor rho: it is O(rho*|theta|^7), uniformly on the chosen disk, because every angular derivative of f has zero constant coefficient. Multiplication by m therefore gives O(j*|theta|^7). After y=sqrt(j)*theta, this is O(j^(-5/2)|y|^7). This justifies the required uniformity as rho tends to zero; a generic remainder bound independent of rho would not suffice.

On |theta|<=j^(-2/5), the cubic perturbation is uniformly small and the positive quadratic coefficient has a common lower bound. Exponential Taylor remainders admit a Gaussian majorant times a fixed polynomial. Outside that interval the angular estimate is exponentially small in j^(1/5), which also dominates the additional sqrt(j) from division by the leading integral. Amplitude expansion through order four and phase expansion through order six suffice through the second correction. Odd Gaussian moments vanish. Thus analytic B_1,B_2 and a uniform relative O(j^(-5/2)) follow. The separate `GAUSSIAN_SECOND_CORRECTION.txt` gives the full second-order expression independently reconstructed from integer partitions of the expansion order.

### Adjacent differences and lower edge

S=-alpha*log(alpha)+an analytic function, so S''''=O(alpha^(-3)). A step q in coefficient index produces q^2/(m*s)+O(j^(-3)) from mS and -q^2/(2j^2)+O(j^(-4)) from the logarithmic prefactor. Smooth bounded derivatives of b,b_1,b_2 give the smaller differences claimed in the packet; the final residual is not differentiated. Hence the displayed O(j^(-5/2)+m^(-2)) curvature error is valid uniformly.

For the actual two-state model, the minus eigenvalue has strictly smaller positive linear derivative at zero. Bounding its modulus on the entire small circle yields exp(-c*m*rho), and comparison to the main saddle gives only the harmless sqrt(j) factor. The gap limit is positive, independently checked exactly. Most importantly, the original monomial shift k=j+3 gives -7/(2j^2) in the binomial curvature. Subtracting from the coefficient curvature leaves

    D_0(rho)/m + 3/j^2 + O(j^(-5/2)+m^(-2)).

One first chooses J to absorb the j^(-5/2) term and then M to absorb m^(-2), independently. The finite set j<J has a common threshold by Turn 3. There is no missing mesoscopic interval and no limit-order interchange.

### Upper edge and parity

The substitutions lambda(1/x^2)=x^(-3)L(x) and H(1/x^2)=x^(-3)E(x) were independently verified as exact algebraic identities. The second branch is obtained by x->-x. The resulting even/odd projections give exactly the two coefficient identities in Turn 4, including r=0 and the canceled pole. This avoids the false shortcut of assuming uniform suppression of the two original eigenbranches at infinity.

Both upper amplitudes are analytic and positive at zero; Kappa(0)=1 and Kappa'(0)=3. Adjacent h values require step q=2, correctly used in the curvature calculation. For s/alpha<=6/5 and h>=5, the lower bound 4/(r*s)>=3/(2h) holds in both parities. The residual can be absorbed uniformly into 1/(10h). On h<=r/4, the binomial curvature is at most 12/(11h). The strict separation 7/5>12/11 therefore proves the shrinking upper band; the remaining bounded h values are covered by Turn 3.

The complement of the two fixed-width proportional edge regions lies in one compact bulk band once m is large. Taking the maximum of the three thresholds is legitimate. This proves eventual strict ULC at every interior positive coefficient simultaneously, with the zero conventions already checked.

**Turn 4 passes.** It proves existence of a finite N, but supplies no effective numerical N. In particular, n<=500 computations do not supply the missing overlap.

## 7. Turn 5: finite certificates with infinite scope, but fixed bands

The degree bounds are proved before interpolation. At lower j, finite powers of N-I give coefficient degree at most j, and the ULC margin degree at most 2j+1. The upper word-length bounds give margin degree at most 4h+3-2p. They are polynomial identities for all integer r>=0, including the initial zero coefficients outside the support.

An exact Newton expansion with nonnegative coefficients is a valid universal certificate on nonnegative integers. The first positive Newton coefficient identifies the strictness threshold because binomial(r,ell)>0 for r>=ell. The first-row formulas agree with positive central support and the interior-index requirement in each parity. The sufficient criterion is correctly distinguished from a necessary condition.

I independently regenerated the 200 complete vectors through a different scalar recurrence, derived by Cayley-Hamilton:

    F_(m+2)=(2+3z)F_(m+1)-(1+3z+z^2-z^3)F_m,
    F_0=4+4z, F_1=4+16z+12z^2+z^3.

I used the explicit signed binomial transform, rather than importing the author's iterative differences. The 14,360 coefficients reproduce the complete canonical certificate hash `63f530185b41356c61167ba5cd16b5a3d1d70bb837cd4d8b86c9bb4b00e29e2b` and the author's optional certificate bytes. Every stated coefficient is nonnegative; all first-strict and highest-coefficient claims pass. Separate off-grid evaluation points also match, without being used as the justification for universality.

These certificates cover only original k=4,...,63 and upper distance h=1,...,40, in both parities. No inference to unbounded j or h is supported.

The degree-six n=7 stripped polynomial was checked with a separate exact root-count implementation: four negative real roots, no nonnegative roots, and gcd with its derivative equal to 1. Its remaining two roots are a nonreal conjugate pair. Thus the direct real-rootedness shortcut fails, while ULC may still hold. This is already qualitatively anticipated by the source's non-real-rootedness observation; no new original counterexample is claimed.

**Turn 5 passes.** Its universal quantifier is over row sizes inside the explicit fixed bands.

## 8. Replays, independent controls, and limitations

All five frozen author stdout receipts replayed byte-for-byte: 748,998; 33,114; 676,415; 33,428; 16,063 assertions, total **1,508,018**. The 25 separate 80-digit diagnostics also replayed byte-for-byte. They remain non-interval diagnostics and are excluded from every exact-proof count.

The independent checker passes **202,120** assertions in the complete local review environment, including 41 Git identities/lengths, 152 historical/final bindings, four source hashes, 14,360 independently regenerated Newton signs, exact scalar row controls through n=500, independent spectral/algebraic checks, Gaussian correction arithmetic and exact root counts. This number includes provenance and finite controls; it is not a count of independently proved theorems. The uniform analytic proofs were reviewed separately in Sections 4-6 above.

For a portable run without local PDFs and the optional generated coefficient file, the same mathematical checks run, with five fewer optional binding comparisons. Raw source PDFs and page images are not necessary public outputs; absence is reported by the source-binding count rather than disguised as a fresh source check.

## 9. Final disposition and correction requirements

No mandatory mathematical correction was identified in the reviewed version. Preserve all five frozen turns. Add this independent review rather than retroactively rewriting historical pending-review fields. A public entry point should identify the review result and retain `unsolved`, 5/5, for the original problem.

The strongest valid conclusion is that every sufficiently large V_n is ULC in the original degree normalization. The possible exceptional rows below the unspecified N remain a finite but not effectively bounded gap. The exact n<=500 checks and fixed Newton bands do not close it. Neither a full all-n theorem nor a classification of arbitrary polynomial matrices, a numerical N, or certified historical novelty has been established.

This mathematical PASS confers no publication or repository-write authorization. No repository upload, PR creation, or QUEUE change was performed during this review.
