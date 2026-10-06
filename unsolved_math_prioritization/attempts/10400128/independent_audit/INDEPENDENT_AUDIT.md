# Independent adversarial audit: Seifert optimistic limits

Problem 10400128; AMR-103-0128; rank 876. Review date: 2026-10-06.

## Decision and exact scope

**Accept the frozen packet as a correct bounded partial and source-scope audit. The original target remains unresolved by this work, with five substantive approaches used out of five. No mathematical correction patch is required.**

The accepted claims are the polynomial upper bound, a pair of branch-corrected formal saddle candidates for the specified +8 unknot-surgery expression, the classical RP3 zero-subsequence obstruction to an ordinary all-level logarithm, the explicitly conditional residue-class and logarithm-lift lemmas, and the positive identity-mapping-torus subclass. This acceptance does not assert that any candidate is the canonical optimistic value of a manifold. It is not a solution, a counterexample to the original formal question, an exhaustive current-openness certificate, or a novelty certificate.

The original seven authored files are preserved byte for byte. Their statements that review was pending at the author freeze and that publication had not occurred are historical snapshot statements. This audit and ACCEPTANCE.json supply the independent review decision; they do not rewrite that historical snapshot. No publication was performed during this review.

## 1. Input identity and prior-attempt gate

The independently supplied archive and external-manifest pins were checked before parsing the archive or running validation code. The archive is 16,466 bytes, SHA-256 005f042404c7c3b14d36c93d04ad8f4738a39766cf66b5af4dc383b41b07930a. The external manifest is 2,063 bytes, SHA-256 cb7c318946b5d130312ee7fe9cfc87c7bf44012b7bbbc8bbac0f283eecbb0c6f. It remains an external binding, not a self-authenticating member of the author archive.

The complete catalog, problems, and research-results inputs were byte-count and SHA-256 checked against the three pins in INPUT_METADATA.json before their JSON contents were used. The target is unique in the catalog and complete-problem input. The rank is 876; the catalog has zero prior proof turns, a five-turn limit, and a desk-review assessment. The complete problem and associated inherited report, rather than a brief synopsis alone, were read. The exact sorted-JSON pair hash is 5c408effe6dd330a79176efb04d0a93fc40fa034e86c4136492d039720a011e1, and the statement hash is af34092e6189c7b445f208882029ccbfb2b86c22096f9f6f8e2be00218be1892. Both match.

The inherited report contains generic literature-status triage and a request for a thorough literature search. It contains no substantive proof attempt to count or invoke as a prior-attempt skip. Its upstream partial-progress classification does not establish that the present target has been resolved.

Fresh read-only searches of AlecKriebel/Math were made for pull requests in all states using 10400128, AMR-103-0128, and optimistic-limit terminology. Default-branch code searches used 10400128 and optimistic. All five searches returned no matches. This validates the reported bounded negative observation; it is not proof of historical absence across every branch, deleted artifact, or differently named discussion.

## 2. Exact source and normalization

The official Ohtsuki reading copy was hash-checked, its target page independently rendered, and printed page 482 (PDF page 110) inspected visually. Section 7.1, printed page 471, was also read. Problem 7.13 concerns the optimistic value of log(tau_N)/N for Seifert fibered 3-manifolds. The adjacent discussion explicitly treats the rigorous formulation as unsettled. The problem is not stated only for integral homology spheres or only for three exceptional fibers. The 2 pi i factor in the preceding conjectural formulation must not be inserted into the problem's requested quantity without explanation. The packet handles this distinction correctly. Primary source: https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf

The normalization is consistent throughout the authored proofs:

- q=exp(2 pi i/N), N>=3, with actual SU(2) level N-2 and the stated rational-power lift.
- Positive real quantum dimensions d_j=sin(pi j/N)/sin(pi/N), not unknot-normalized colored Jones values equal to 1.
- D_N^2=N/[2 sin^2(pi/N)], tau_N(S3)=1, Z_N(S3)=D_N^(-1), and tau_N=D_N Z_N.
- For the one-component positive-surgery presentation, its signature is +1 and the blow-up correction is B_1^(-1), giving tau_N(M_p)=B_p/B_1. This is not an omitted D_N factor or a correction by B_1^p.

The modular relation gives |B_1|=D_N and in particular nonvanishing. Framing-anomaly scalars have modulus one. The alternative twist sign mentioned in the packet cancels in an even-framing numerator; the corresponding blow-up phase must still be changed coherently. This is sufficient for the claimed modulus and zero results and does not purport to identify every convention's complex phase. Orientation reversal conjugates the invariant. The packet correctly defines M_p by surgery instead of relying on a potentially opposite lens-space orientation convention.

The standard unitary TQFT, gluing, surgery, and Verlinde-state-space facts are accepted classical inputs, not newly constructed or independently re-proved theories in this packet. Their use is explicit and mathematically consistent.

## 3. Audit of the mathematical arguments

### 3.1 Polynomial upper bound

For a genus-g handlebody state v, the unitary gluing estimate gives |Z_N(M)|<=||v||^2. Its double is the connected sum of g copies of S2 x S1. Using Z_N(S2 x S1)=1 and the connected-sum factor D_N gives ||v||^2=D_N^(g-1). For g=0 this correctly recovers Z_N(S3)=D_N^(-1). Multiplication by D_N yields |tau_N(M)|<=D_N^g.

Since D_N is asymptotic to N^(3/2)/(sqrt(2) pi), this proves only the claimed exponential-scale upper bound. It neither establishes a lower bound nor rules out zeros or exponentially small subsequences. The packet explicitly avoids the invalid implication that a polynomial upper bound proves a logarithmic limit of zero. No error found.

### 3.2 Formal +8 surgery candidates

The exact identity d_j=q^((1-j)/2)(1-q^j)/(1-q) verifies the surgery numerator

B_8 = q^(-1)/(1-q)^2 sum_j q^(2j^2-j)(1-q^j)^2.

The -j term contributes the amplitude z^(-1), not a quadratic action at order N. Expressing each 1-q^j as (q)_j/(q)_(j-1) gives cancelling dilogarithm terms when their homogeneous linear parts agree. On a specified local logarithm lift t, the remaining potential is 2t^2. Its exponent is N times that potential divided by 2 pi i. Thus the formal exponentiated stationarity condition is exp(4t)=1, not exp(2t)=1 or an ordinary derivative condition imposed before branch correction.

At t_m=pi i m/2, the correction -2 pi i m t makes the first derivative vanish and leaves the second derivative equal to 4. Direct substitution gives V_m=pi^2 m^2/2. For m=1,2, z=i,-1, the amplitudes are -2,-4, so neither critical point is excluded by a zero amplitude. They occur at interior scaled indices 1/4 and 1/2. Their action difference is 3 pi^2/2, not a multiple of 4 pi^2. Changing a lift at the same point by m -> m+4k changes the action by 4 pi^2 m k+8 pi^2 k^2, a multiple of that period. Dividing the two displayed actions by 2 pi i gives -i pi/4 and -i pi.

These are valid formal outputs under Murakami's specified recipe, whose own definition permits a selected solution and whose remarks warn of contour and solution ambiguities. They are not stationary points of one globally specified corrected potential: each uses the appropriate integer branch correction, as the packet says. Nor is either shown to lie on a contributing contour or to dominate the actual discrete sum. No surgery-presentation invariance is proved. Consequently the correct accepted conclusion is candidate multiplicity for this expression, not impossibility of a rigorous formulation or falsity of the original problem. Primary prescription: https://arxiv.org/abs/math/0005289

The retained standard surgery prefactor does not justify an arbitrarily winding logarithm. Its polynomial-size contribution and bounded phase convention are consistent with separating the displayed leading formal action. No correction needed.

### 3.3 Classical RP3 obstruction

For odd N, the involution j -> N-j has no fixed label and preserves d_j. The squared-twist ratio is (-1)^N=-1, so the surgery numerator cancels exactly in pairs. This is an identity for every allowed odd shifted level, not a numerical asymptotic observation. The denominator is nonzero.

For even N, f(j)=exp(pi i j^2/N) is genuinely N-periodic, which is essential for both completing-square index shifts. Expanding sin^2 gives F=(1-exp(-pi i/N))G/2. The character-orthogonality calculation gives |G|^2=N; the shift reduction in that calculation is legitimate precisely because f is periodic. Combining the factors and |B_1|=sqrt(N/2)/sin(pi/N) gives |tau_N|=1/[sqrt(2) cos(pi/(2N))]. These equalities, with even N>=4, imply the stated liminf=-infinity and limsup=0 for N^(-1)log|tau_N|.

The author-hosted Kirby-Melvin manuscript's equation (5.12) and following paragraph were visually checked. They record the stronger positive real even-level value in that convention and the odd-level vanishing. Its page 51 is manuscript/PDF pagination, not journal pagination. The packet's credit is accurate. Its own proof needs only the modulus and does not silently force that stronger phase statement into every ribbon convention. Source: https://math.berkeley.edu/~kirby/papers/Kirby%20and%20Melvin%20-%20The%203-manifold%20invariants%20of%20Witten%20and%20Reshetikhin-Turaev%20for%20sl%282%2C%20C%29%20-%20MR1117149.pdf

Zeros cannot be repaired by any logarithm branch or multiplication by a nonzero normalization. The example invalidates an all-level ordinary-log replacement, while leaving the formal optimistic question intact. It is correctly credited as classical, not novel.

### 3.4 Conditional expansion and branch lemmas

On a fixed residue class modulo a common phase denominator, all rational phases become constants. A finite union of exponent ladders d_s-r/h is bounded above and locally finite. If a combined coefficient survives, there is a highest surviving exponent and a positive gap to lower exponents. Taking the full Poincare expansion sufficiently far establishes a relative O(N^(-delta)) remainder, hence eventual nonvanishing and the stated logarithmic rate zero. A bounded argument contributes o(1) after division by N. The finite-phase, rational-phase, full-expansion, and nonzero-combined-coefficient hypotheses are indispensable and are present.

If all coefficients cancel, the expansion gives no such conclusion. The two abstract controls 1+(-1)^N and 1+(-1)^N+exp(-N) share the indicated all-orders expansion but behave differently on the odd class. They are explicitly not presented as further WRT examples. Proposition 2 provides the actual WRT zero control.

Adding 2 pi i floor(alpha N) to a logarithm preserves its exponential and changes its scaled limit by 2 pi i alpha. The statement is only about unconstrained pointwise logarithms; it does not claim this freedom survives a specified analytic interpolation. The distinction between a phase-unwrapped logarithm and a bounded-argument logarithm is correct. No error found.

### 3.5 Positive identity mapping tori and the Verlinde prefactor

For the identity cobordism with product structure, the TQFT trace is the state-space dimension. Thus Z_N(Sigma_g x S1)=v_g(N), and the sphere-one invariant is D_N times that positive number. There is no omitted D_N normalization. For g=0, sum_j S_(1j)^2=1; for g=1 the sum has N-1 unit summands. For g>=2, putting k=N-2, taking zero marked points in the source's (1.2), and substituting (1.1) gives

v_g(N)=(N/2)^(g-1) sum_{j=1}^{N-1} sin(pi j/N)^(2-2g).

Daskalopoulos-Wentworth Theorem 1.4 states the relevant equality with dimensions for g>=2, under the stated positive-integer level hypothesis. The bridge to the unitary SU(2) state spaces and trace is the classical modular-functor input already acknowledged by the author. The theorem is not being asserted at genus zero or one without that separate input. Source: https://math.umd.edu/~raw/papers/verlinde.pdf

Both first pages of the pinned reading copy were visually inspected. In this copy, display (1.5) appears to have a prefactor exponent 1/2. Under the zero-marked-point specialization and g>=2, the exponent forced by (1.1)-(1.2) is g-1. The review accepts the packet's precise local observation and derivation. It does not infer a wider theorem failure, speculate about the cause of the printed discrepancy, or claim an independently checked erratum. The inconsistent displayed prefactor is not used in the proof.

For a=2g-2>=2, the j=1 term and sin(pi/N)<=pi/N give the stated lower bound. With m=min(j,N-j), concavity gives sin(pi j/N)>=2m/N, and every m occurs at most twice; the convergent sum of m^(-a) then gives the upper bound. Hence v_g is Theta_g(N^(3g-3)), and tau_N is Theta_g(N^(3g-3/2)). The exceptional g=0,1 powers are respectively 3/2 and 5/2. Positivity makes the ordinary real logarithm unambiguous, and all its scaled rates are zero. These product manifolds are Seifert fibered. Extension to an arbitrary mapping-class trace would lose positivity, and the packet correctly does not make that extension.

## 4. Literature boundary

The source statements used by the packet were re-read in the hash-checked primary reading copies. The broad Hansen theorem has the stated base-genus and exceptional-fiber qualifications, and its sphere normalization differs by D_N. An expansion with possible extra phases is not an already established canonical optimistic-limit prescription. Source: https://arxiv.org/abs/math/0510549

The Andersen-Han-Li-Mistegard-Sauzin-Sun paper treats Seifert integral homology spheres, with its main setup specifying at least three exceptional fibers. Its shifted level and sphere-one normalization agree with those recorded in the packet. Theorem 1.1 and its exact resurgent formula imply the claimed expansion in that stated setting. The live arXiv page checked during this review lists v1 and no journal reference. This supports the word preprint and the subclass distinction, not a claim about human peer review or a full independent audit of its 68-page proof. Source: https://arxiv.org/abs/2510.10678

The published Murakami-Tran main theorem was checked for the alternative root exp(4 pi i/n), odd n, positive coprime torus parameters, p>ab, and gcd(p,ab)=1. None can be suppressed when comparing with Problem 7.13. Source: https://doi.org/10.4171/QT/175

The bounded fresh terminology searches surfaced the original source and Murakami's earlier computations, not a verified all-Seifert resolution. This observation is not an exhaustive literature nonexistence proof. The long external theorems were reviewed for their statements, conventions, and relevance, not independently proved from beginning to end. No external theorem is needed to rescue a gap in the elementary proofs above.

## 5. Validation, distribution, and acceptance limits

There is no executable mathematical checker in the author archive. An independently written, assertion-free static verifier checked the original external bindings, exact seven-member allowlist, each member's bytes and hash, input identity, all eight cited PDF reading-copy pins, and restrained status fields. It executed no code from the archive. Isolated normal and isolated optimized Python runs produced identical substantive results.

Each run rejected 12 negative controls: archive tampering, external-manifest tampering, a missing member, an extra member, a duplicate member, a traversal member, proof-byte tampering, a duplicate manifest entry, solved-status escalation, an approach-cap overrun, novelty escalation, and full-resolution escalation. These are integrity and scope controls, not proofs of topology or asymptotics. The mathematical acceptance is based on the written arguments and source inspection above, not on finite numerical sampling or hash agreement.

The audit package contains only the seven unchanged authored files and three authored audit/acceptance/validation files. It excludes copied source PDFs, source text, screenshots, complete datasets, private coordination, executable review machinery, and hashes of private review machinery. Public input and source-reading-copy verification metadata are permitted and retained. The manifest binding the completed audit archive is external to that archive.

**Final disposition: accepted bounded partial; unsolved, 5/5; no new research approach, no mathematical patch, no novelty claim, and no publication.**
