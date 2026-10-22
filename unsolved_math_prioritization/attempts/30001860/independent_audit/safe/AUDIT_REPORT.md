# Independent adversarial audit: 30001860 / OWR-11129-006

Audit date: 2026-10-05 UTC. Assigned catalog rank: 707.

## Verdict

**PASS for the scoped mathematical results, with the controlling rank clarification below. The broad asymptotic-value problem remains unresolved in this work: five retained approaches, none a full resolution.**

The frozen proof supports uniform odd-field bounds of 512/log N for GL_N and the full unitary isometry group U_N, 512/log r for Sp_(2r) and SO_(2r+1), and 1024/log r for both SO_(2r) signs, with the stated minimum with 1 and dimension/rank thresholds. Combining only these families with the applicable published LNP lower bound yields the stated q-uniform reciprocal-log order of magnitude. The SL/SU intermediate-group argument yields only the stated fixed-q result.

I found no failing proof step, false uniformity, or counterexample within that scope after independently reconstructing the infinite estimates and checking the primary input. The constants have margin: the written argument gives 460/log n in the unsigned model and 440/log n in the unconditioned signed model.

This is an independent automated mathematical audit, not human refereeing, certification of novelty, an exhaustive literature search, or a claim that the wider problem is globally open. The frozen files remain unchanged.

### Controlling clarification: dimension versus Lie rank

PROOF.md line 193, section 7, says “Exact rank-two and quotient controls.” Its GL_2/SL_2 examples have **natural dimension 2 and semisimple Lie rank 1**. Read that heading as **“Exact dimension-two and quotient controls.”** This is an editorial correction, not a change to a theorem or computation. GL_3 and Sp_4 are the Lie-rank-two matrix controls.

Every lower-bound and asymptotic assertion is controlled by these explicit conditions:

- GL_N and U_N: the upper bound starts at N=2. The LNP lower bound starts at Lie rank N-1 >= 2, equivalently N>=3.
- Sp_(2r), SO_(2r+1), and SO^±_(2r): both the stated upper bound and imported lower bound are used for r>=2.
- SL_N <= H <= GL_N and SU_N <= H <= U_N: the imported lower bound is used only for N>=3; the resulting Theta_q assertion concerns N tending to infinity with q fixed. No q-uniform upper bound is established by the finite-index argument.
- No lower-bound assertion is made for SL_2; its qualifying proportion is zero. The misleading heading must never be used to extend LNP to Lie rank 1.
- The listed asymptotic assertions concern rank growth, not field growth at fixed rank. They are order-of-magnitude bounds, not leading equivalents or convergence of a log-scaled probability.

The README, theorem paragraph, fixed-index paragraph, ATTEMPTS, and STATUS were checked against this interpretation. The theorem paragraph already states the rank threshold and GL/U conversion correctly. No further rank-scope contradiction was found.

## Frozen binding and review boundary

The audited target is the eight authored files named in the 1,582-byte MANIFEST.json with SHA-256:

`f23f0fc8f7f634f9fab4a19077126435f6bc5796b979cea9bd5f68de338348ca`

The main proof is 19,022 bytes, SHA-256:

`a4e69d77d503067a44826c5f946974bbd12f81028a9a8d36df94f344fd8c58fa`

All eight lengths and hashes matched the manifest at entry and final verification. BINDING.json supplies the complete per-file binding and source metadata. No frozen file was edited. The exact current catalog statement and raw prior AI records were not available to this audit. The catalog ID, OWR number, and queue rank are assigned identifiers; the mathematical statement was checked against the primary OWR source rather than an inaccessible catalog body.

All authored files were read. The independent review covered the proof, implementation, reported finite results, provenance claims within the available evidence, status, and retained approaches. The historical repository and literature searches summarized by the author were not independently reproduced; their negative results are not upgraded to exhaustive absence claims.

## Primary-source check

1. The OWR problem on printed page 2154 was read in extracted text and inspected visually. It requires even order and fixed-space dimension in [N/3,2N/3), with the upper endpoint strict. It actually prints O(log N). As a probability is at most 1, that literal subquestion is vacuous for N>=2; it is not a solution of the asymptotic-value question.
2. The inspected LNP author-hosted article-in-press version explicitly discusses experimental evidence for a reciprocal-log upper bound on page 3. The audit treats this as a separately sourced nontrivial target, not an unannounced correction of OWR.
3. LNP Theorem 1.1 and Table 1 were checked in both text and a page rendering. The hypotheses are odd prime-power q and semisimple rank at least 2. Its fixed-space interval is exactly the required one. The lower bound is 1/(5000 log_2(rank)), or log(2)/(5000 log(rank)) in natural-log notation. Taking H equal to each listed matrix group is within the theorem; the SL/SU intermediates are also explicitly included.
4. LNP Lemmas 2.1-2.3, sections 3.1-3.4, and section 5(i),(v),(vi),(vii) were read for the imported equality, Frobenius conventions, tori, and group scope. The audit relies on these published structural/counting inputs, not an independent reproof of Steinberg's counting theorems.
5. LNP's introductory use of GU terminology could be confusing. The operative definition in section 3.1 is the fixed-point group of the inverse-q Frobenius on GL_N. That is the unitary isometry group used in this proof, with determinant quotient order q+1. The audit does not transfer the upper bound to unitary similitudes.

The EMS article landing page was independently opened and confirmed publication identity. The web PDF reader rejected the LNP URL's application/x-pdf content type; the available local primary PDF, whose size and SHA-256 match the frozen source metadata, was inspected instead. No website failure is represented as a successful new PDF retrieval.

Public primary references:

- F. Lübeck, A. C. Niemeyer, C. E. Praeger, *Finding involutions in finite Lie type groups of odd characteristic*, Journal of Algebra 321 (2009), 3397-3417. DOI: https://doi.org/10.1016/j.jalgebra.2008.05.009 . Inspected author version: https://www.math.rwth-aachen.de/~Frank.Luebeck/preprints/powerinvReprint.pdf .
- *Computational Group Theory*, Oberwolfach Reports 8 (2011), 2113-2161, problem session p. 2154. https://ems.press/journals/owr/articles/11129 ; DOI: https://doi.org/10.4171/OWR/2011/37 .

## Proof audit, step by step

### 1. Jordan and eigenvalue reductions: pass

For commuting semisimple s and unipotent u in odd characteristic, their orders are coprime, with the latter odd. Thus |su|=|s||u|, u disappears on taking the half-order power, and the remaining odd power of the involution s^(|s|/2) is unchanged. This includes nonsemisimple group elements exactly; it is not an assumption that random elements are semisimple.

The eigenvalues of s have orders dividing |s|. An eigenvalue attains -1 under the half-order power precisely when its order has the largest nonzero 2-adic valuation. Eigenvalues with smaller valuation give +1. Multiplicities, including repeated eigenvalues, are retained. If the maximum valuation is zero, the element has odd order and is excluded.

The involution fiber identity follows by disjointness of fibers and conjugacy-orbit counting, with each fiber contained in the involution's centralizer. In GL, the single involution class for each prescribed plus-space dimension has centralizer GL_k x GL_(N-k). The strict versus maximal 2-parts in the two factors give the displayed convolution, without a missing class-size or factorial factor.

### 2. Imported maximal-torus identity: pass in the exact scope used

The formal setup is a connected reductive algebraic group over the algebraic closure of a finite field, a Frobenius endomorphism F, and its finite fixed-point group. “Connected” concerns the algebraic group, not a topology on a finite abstract group. GL, Sp, and SO in the specified characteristics, and the unitary/type-D twists, fit this setup; a disconnected full orthogonal group is not silently substituted.

The actual set here is P(G^F,I), where I is a union of rational conjugacy classes of involutions selected by the natural fixed-space dimension. Thus LNP Lemma 2.3 applies in its own stated pre-involution form. The author's more general wording about semisimple-dependent conjugacy sets also follows from the same counting proof, but no such extension is needed to validate this application.

Torus weights are |C|/|W| for F-conjugacy classes, rather than uniform weights over torus classes. Replacing the weighted sum by a uniform Weyl element gives exactly the cycle models. This is why arbitrary uniform involution sampling or uniform torus-class sampling would be invalid substitutes.

### 3. Unsigned and signed models: pass

- In GL a cycle of length d has a cyclic torus factor of order q^d-1 and d natural eigenvalue positions.
- In U the order is q^d-(-1)^d. The conjugations of a factor parameter use powers of -q, which preserve its 2-part order because q is odd. The scalar involution acts on the whole d-position block.
- In Sp and odd SO, the signed Weyl group projects uniformly to S_r. For any fixed projected permutation, cycle-sign products are independent unbiased signs: each cycle product is the product of independent coordinate signs on disjoint coordinates. Positive and negative cycles give orders q^d-1 and q^d+1, respectively, on 2d natural positions.
- In odd SO the extra eigenvalue is exactly +1. Its exact admissible mass window is (2r+1)/6 < M <= (2r+1)/3. It is legitimate to retain only M>r/3 for the upper bound. The proof does not incorrectly identify the original odd-SO event with the Sp event.
- For even SO, plus type restricts to an even number of negative cycles and minus type to an odd number. Each event has probability 1/2. The twisted F-conjugacy description amounts to the odd coset of the signed Weyl group. Splitting of some type-D Weyl conjugacy classes preserves the total element weights. The inequality P(A | parity) <= 2 P(A) needs no independence between A and parity and is therefore valid.

For every family the fixed-space window is converted to the minus-space window with reversed strictness: N/3 < minus dimension <= 2N/3. All dimensions and rank factors in this conversion were checked.

### 4. Coefficient identity: pass

The coefficient of exp(sum_d w_j(d) z^d/d) counts normalized permutations all of whose cycles have color j. Selecting the m labels for those cycles, then requiring every remaining cycle color to be at most j-1, gives the product of coefficients in the author formula. The binomial label count cancels the normalization factorials. The requirement m>=1 rules out an absent maximum color. In the signed case the independent sign averages may be taken before cycle enumeration. The code uses b_(j-1), not b_j, in this exact partition of colors.

The recurrence in verify.py is the derivative identity k c_k = sum_(d=1)^k w_d c_(k-d). Arithmetic is rational; no floating-point decision affects the coefficient or matrix membership results. The signed model implemented there is Sp, not parity-conditioned SO. The audit separately checks the latter models.

### 5. Cycle pointing and acceptance bounds: pass

Pointing a d-cycle in a normalized permutation costs 1/d; its mass contribution supplies d. A specified color-j cycle is already accepted under the cutoff at j, and its complement is an independent uniform permutation on n-d points. This establishes E[M_j 1_(E_j)] = sum_d w_j(d) B_j(n-d), including the empty complement convention B_j(0)=1. Markov's inequality with threshold n/3 gives the displayed factor 3/n. The target's upper endpoint can safely be dropped only because this is an upper bound.

For fractional avoidance, the cycle-index series is (1-z)^(-1)(1-z^L)^(rho/L). Its degree-m coefficient is the partial binomial sum through floor(m/L), equal to the product over i of (1-rho/(L i)). This also holds for m<L, when the empty product is 1. Taking logarithms and bounding the harmonic sum gives the stated decay. The acceptance-probability comparison is coefficientwise probabilistic coupling, so it does not rely on unjustified coefficient inequalities for arbitrary analytic functions.

### 6. High-layer tail and dyadic sum: pass

Put K=floor(n/h) >=1 and write n=hK+r with 0<=r<h. For d=hs,

floor((n-d)/(2h)) = floor((K-s)/2).

This identity handles the remainder correctly, including the n=d endpoint. Pairing the repeated values gives at most 2 sum_(i<=ceil(K/2)) i^(-alpha), bounded by 4 K^(1-alpha) for 0<alpha<=1/2. Thus cycle pointing gives at most 12w K^(-alpha)/h. Since K>=n/(2h), this is at most 24w h^(-1)(n/h)^(-alpha). There is no hidden dependence on q or on the number of low layers.

For the dyadic sum, h>sqrt(n) contributes less than 2/sqrt(n). For h<=sqrt(n), log(n/h)>=log(n)/2. With L=log(n)/(2c), each summand is bounded by four times the integral of x^(-2) exp(-L/x) over [h,2h]. These dyadic intervals do not overlap in their interiors, and the whole positive-axis integral is 1/L. Hence the remaining contribution is at most 8c/log n. This is an infinite argument; finite stress tests are merely ancillary.

### 7. GL and U low/high layers and uniformity: pass

For odd q, a=v2(q-1), b=v2(q+1) satisfy min(a,b)=1. Odd cycle lengths have valuation a in GL and b in U; even lengths have valuation a+b+v2(d)-1 in both. Swapping a and b is therefore exact for U.

For j<a, the geometric sum of marking bounds is below 1/2 and uniform acceptance is at most 1/2. Their combined contribution is at most 3 n^(-1/2). At j=a, every even-length cycle has acceptance at most 1/2, giving 2^(1/4) n^(-1/4). In the gap a<j<a+b only even cycles can be marked; their marking bounds again sum to less than 1/2 and give at most 2*2^(1/4) n^(-1/4). Empty ranges create no missing case. Altogether this is at most 7 n^(-1/4).

For j>=a+b, h=2^(j-a-b+1) is at least 2. A nonzero marking weight is possible exactly on multiples of h, and on d=hk it is 1/(2*2^v2(k)). Every multiple of 2h has cutoff acceptance at most 1/2. Taking w=1/2 and rho=1/2 gives 12/h times exp(-log(n/h)/(4h)). Layers with h>n are absent. The dyadic lemma gives 384/log n + 24/sqrt(n).

Finally log n <= n^delta/delta yields 7 n^(-1/4) <=28/log n and 24 n^(-1/2)<=48/log n. The total is at most 460/log n, below 512/log n. Arbitrarily large a or b merely shift or extend geometric low-layer ranges; their totals remain bounded. The proof therefore permits q to vary with dimension.

### 8. Signed layers and even-orthogonal factor: pass

Let c=max(a,b)>=2. At every length, one sign has valuation 1 and the other at least c. Thus the j=1 cutoff acceptance is at most 3/4. For 2<=j<c the averaged marking bounds sum to less than 1/4, with the same acceptance cap; the two contributions are each at most n^(-1/4). For j=c, even lengths have acceptance at most 3/4, giving 2^(1/8)n^(-1/8). The sum is bounded by 4n^(-1/8).

For j>=c+1, h=2^(j-c) is at least 2 and only positive cycles divisible by h can be marked. Averaging signs gives w<=1/4; on multiples of 2h acceptance is at most 3/4. The high-layer bound is therefore 6/h times exp(-log(n/h)/(8h)). Its dyadic sum is at most 384/log n+12/sqrt(n). Adding the low contribution gives (32+384+24)/log n =440/log n. With n=r this proves the unconditioned signed upper bound; conditioning costs at most 2, which is covered by 1024/log r for both even orthogonal signs.

### 9. Lower-bound combination and exclusions: pass under the clarification

For GL/U, LNP uses semisimple rank ell=N-1. For the other listed families it uses ell=r, including r=2. Logarithms of N and N-1 are comparable for N>=3; moreover the displayed lower bound is exactly log(2)/(5000 log ell). Consequently the stated uniform Theta(1/log ell) assertion follows for precisely the named families as ell tends to infinity.

For H between SL and GL, Q(H)=Q(GL) intersect H in the same natural representation. This gives p(H)<= [GL:H]p(GL), with index at most q-1; the unitary index is at most q+1. These constants are allowed to depend on fixed q and are not uniformly bounded when q varies. The imported lower bound applies to the same intermediates at N>=3. No claim for an arbitrary larger group or central quotient follows from this argument.

The GL_2 formula and SL_2 zero result are correct. The two sequences of odd prime powers have v2(q-1)=1 and v2(q-1)=k+2 as stated, so field growth at fixed dimension has incompatible limits. The GL_3 central-scalar example correctly detects the strict upper endpoint and invalidates an arbitrary-lift projective predicate. It does not refute the separately defined image-set predicate in LNP's projective corollary.

## Independent controls and replay

The authored program was rerun with its output redirected outside the frozen bundle. Its output JSON is byte-for-byte identical to the frozen verification_results.json. All asserted controls passed.

The independent program imports no author functions. It makes the following algorithmic changes:

- GL matrices are constructed from ordered independent columns. Determinants used for the special subgroup are evaluated by the Leibniz formula rather than elimination.
- Sp_4(3) is enumerated by closure under eight explicit symplectic transvections. Each generator preserves the form; obtaining the known 51,840-element order establishes that the closure is the full group. This does not reuse the author's symplectic-basis enumeration.
- The cyclic involution is extracted by first taking the odd cofactor of the group order and then repeated squaring, without computing the full element order or prime-stripping it.
- Fixed spaces are counted by testing all vectors; their dimensions are recovered from exact powers of q, without Gaussian rank computation.
- Torus probabilities are summed over integer partitions with their exact 1/z_lambda weights. A joint distribution tracks maximum color, mass, and sign parity, with colors obtained by enumerating exponents in cyclic 2-groups. No exponential-series coefficient recurrence is reused.

All five matrix controls match:

- GL_2(3): 12/48 = 1/4; SL_2 count 0/24.
- GL_2(5): 150/480 = 5/16; SL_2 count 0/120.
- GL_2(7): 504/2016 = 1/4; SL_2 count 0/336.
- GL_3(3): 5,265/11,232 = 15/32; SL_3 count 3,159/5,616.
- Sp_4(3): 17,010/51,840 = 21/64.

All 198 GL/U/Sp coefficient outputs agree with independent partition enumeration. Additional exact controls cover signed parity and the odd-SO window for 28 field/rank combinations, 255 fractional-avoidance identities, and 105 nonzero cyclic-color probabilities. The results file also records exact cycle-pointing checks, bounded low/high-stratum stress checks, valuation checks, and floating-point dyadic stress tests; only the latter are numerical rather than exact. The report's infinite derivations, not these finite controls, justify the theorem.

The negative controls detect changing the strict endpoint, collapsing all positive 2-adic valuations to a single even-order color, forgetting even-orthogonal parity, reusing linear rather than unitary arithmetic, extending the rank threshold to SL_2, using an arbitrary projective lift, and deleting the avoidance exponential from the dyadic argument. See NEGATIVE_CONTROLS.md and independent_results.json.

## Disposition of the five retained approaches

1. Semisimple spectral reduction: valid exact reduction; not a full asymptotic-value solution.
2. Centralizer/fiber decomposition: valid exact identity; not a full asymptotic-value solution.
3. Fixed-rank arithmetic and quotient controls: valid counterexamples to proposed conflations; not a rank-growth resolution.
4. Unsigned torus/cycle proof: valid scoped uniform upper bound and, with LNP, order of magnitude; no leading equivalent.
5. Signed extension and finite-index transfer: valid scoped upper bounds and fixed-q extension; no additional family or leading-equivalent completion.

**Overall: partial, five approaches retained, zero full resolutions.** No value or existence of lim log(rank)*p(G), oscillation classification, full conformal/disconnected/Spin/half-spin coverage, or projective-predicate completion is proved. No novelty or global-openness certification is issued.

## Safety of the audit package

The safe audit package contains only authored analysis/code, counts, hashes, public source metadata, and verification results. It excludes source PDFs, source text extracts, source images, raw catalog/prior-AI records, and private coordination. Private visual-inspection intermediates are outside the safe package and its manifest. No remote writes or helper delegation were performed in this audit.
