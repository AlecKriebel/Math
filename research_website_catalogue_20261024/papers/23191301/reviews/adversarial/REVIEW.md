# Independent adversarial review — Zenodo 23191301

**Verdict: PASS for the exact published mathematical scope. No substantive defect found.**

Paper: *Nonconvexity of fixed odd-power sum-of-squares cones*, Alec Kriebel, version 1.0, 6 October 2026, six pages. Inventory row 50.

Main PDF SHA256: `78930bbd8e727df2de0ca64ac3b5994a7e3392a289bd9058a4fc8dce02fd9e66`.

Verification ZIP SHA256: `680fb649cc1288684611fd2767334c5c9d9b62f8be086441319539704551033c`.

## Exact claim and success criterion

For an even positive degree m and a positive odd integer q, C(n,m,q) consists of real homogeneous degree-m forms f whose qth powers are sums of squares of real polynomials. The stipulated nonnegativity of f is automatic for odd q. The theorem asserts that C(3·10^62,6,3) is nonconvex: the N=10^62 disjoint copies of the coefficient-1 modified Motzkin sextic belong to this set, but their average does not. It further asserts, for every fixed odd q≥3, nonconvexity of C(n(q),6,q) for some finite dimension depending on q.

The review required both the membership of every summand and a valid separating functional for the average, not merely an inability to find an SOS. It also required a proof for arbitrary fixed odd q, rather than extrapolation from the degree-18 numerical certificate. The stated claim is not ternary nonconvexity, a smallest dimension, an explicit common dimension for all odd exponents, a parameter classification, or nonconvexity of the union over exponents.

All six manuscript pages, including the complete appendix identity and references, were read. The pertinent mathematical source and complete supplied checker/harness were inspected. No sibling reviewer conclusions or dedicated historical priority/review verdict body was read.

## Adversarial proof analysis

### 1. The seed and its fixed-power membership

For p=x⁴y²+x²y⁴+z⁶−x²y²z², AM–GM applies to three nonnegative terms and gives p≥2x²y²z²≥0 for every real triple, including coordinate zeros. The coefficient is 1, not the coefficient-3 original Motzkin form. Fresh exact polynomial arithmetic verifies the complete displayed identity for p³ with all sixteen positive-weight square terms of degree nine. It explicitly rejects use of the same identity for the coefficient-3 form.

The seed is not SOS, independently of any global separation theorem. The verified positive local functional satisfies L(p)=−1. A second check is the original dehomogenized argument: if p(x,y,1) were a sum of squares of degree-at-most-three polynomials, the restrictions to either axis force each factor to have the form a+xy·ℓ with ℓ affine linear. The degree-two and degree-three cross terms must vanish, leaving x²+y²−1 as a sum of squares of affine linear polynomials, impossible at the origin. A homogeneous SOS would dehomogenize to such an SOS.

For every odd q≥3, p^q=p³·(p^((q−3)/2))² is SOS by multiplying each square factor. The exponent is a nonnegative integer exactly under the stated hypothesis. Disjoint variable embedding preserves both homogeneity and the explicit SOS representation. Positive scaling also preserves membership.

### 2. Closedness and separation at the larger degree

The finite-degree SOS cone is closed for the reason actually supplied, not because arbitrary linear images of PSD cones are closed. Write a convergent sequence as vᵀQ_jv with Q_j positive semidefinite. The Gaussian moment matrix G for all monomials of degree at most d is positive definite: a nonzero polynomial has positive Gaussian square integral. Coefficient convergence bounds the Gaussian integral, and λ_min(G)·tr(Q_j)≤tr(Q_jG) bounds the PSD matrices. A subsequence therefore converges to a PSD Gram matrix for the limit.

A non-SOS form of degree m remains outside the degree-at-most-2d SOS cone. Otherwise the highest-degree square parts above m would sum to zero as a polynomial, forcing every such part to vanish. Repeating gives an ordinary SOS of the original form. This excludes a hidden use of higher-degree square cancellation.

Finite-dimensional strong separation from the closed convex cone yields L₀ nonnegative on the cone and strictly negative at p. Adding a sufficiently small positive multiple of the Gaussian functional preserves L₀(p)<0 and makes its moment matrix positive definite. Its constant value becomes positive, so division normalizes L(1)=1 without reversing the separating sign. The functional is constructed separately for each d=qm/2. The proof does not extend the explicit degree-18 moment table to larger q.

The power map is polynomial in coefficients. Its inverse image of the relevant closed SOS cone is therefore closed; the auxiliary closedness statement about C(n,m,q) is valid. Closedness is not confused with convexity.

### 3. Arbitrarily many disjoint blocks and the finite sign

The product functional is defined monomial by monomial on a finite space having degree at most 2d in each block. Every polynomial of total degree at most 2d lies in that domain. For a square of a polynomial H of total degree at most d, each block's exponent in H is at most d. Its moment matrix is exactly a principal submatrix of the finite Kronecker product M^⊗s. Positive semidefiniteness of finite tensor products therefore proves nonnegativity on all required squares. There is no representing measure, infinite tensor product or numerical construction of the enormous global matrix.

The partition expansion counts assignments of the q labelled factors. For a set partition with r blocks, the number of injective assignments to copies is (s)_r and the moment product is the product of a_|B|. This also works for s<r because the falling factorial vanishes. Exactly one partition has q blocks: all singletons. Consequently the expression is a polynomial in s with leading coefficient a₁^q. For fixed odd q and a₁<0 this coefficient is strictly negative, while all collisions have smaller degree. A real polynomial with negative leading coefficient is negative for all sufficiently large finite integers. No exchange of infinite limits or limits of functionals is used.

An SOS representation of S_s^q could not evade the functional through square factors of degree above d, by the same highest-degree argument. Thus negativity excludes every real-polynomial SOS representation.

### 4. The explicit 220-dimensional local certificate

The displayed moments specify all monomials through degree 18. The crucial degree-six values for x⁶ and y⁶ are 2^24, as confirmed in the typeset PDF and TeX. Coordinate parity splits the degree-at-most-nine monomials into blocks of sizes 35,35,35,20,35,20,20,20, totaling 220.

Fresh code builds these matrices directly from the manuscript table, using lexicographic monomial order. It finds 220 strictly positive rational LDL pivots and checks the complete exact LDL reconstruction in every block, independently establishing the positivity proposition. It also reproduces all twenty printed leading minors at order three. Thus the principal finite positivity claim is independently checked without relying on supplied success flags or copied Schur traces.

The manuscript's compressed inductive certificate is sound as an additional proof mechanism. Its Gaussian new-row matrix G is positive definite; A is positive definite by induction; C=BᵀA⁻¹B is positive semidefinite. Therefore G^(-1/2)CG^(-1/2) is PSD and its largest eigenvalue is at most its trace. The strict trace inequality gives T_rG−C positive definite, which is precisely the required Schur complement. Blocks with no new rows are unchanged. The replay rebuilds and authenticates all 24 exact rational traces and strict inequalities.

### 5. Explicit finite cubic obstruction and convexity

Fresh sparse expansion gives a₁=−1, a₂=11292·10^53 and a₃=35039520·10^116. For N=10^62, the exact value is

`N a₃ − 3N(N−1)a₂ − N(N−1)(N−2)`.

Since a₂≥1, it is at most `N{a₃−(N²−1)}`. Indeed, `3(N−1)+(N−1)(N−2)=N²−1`. The displayed strict inequality `35039520·10^116 < 10^124−1` is correct and was checked as an integer comparison. Dividing the polynomial by positive N only multiplies its cube by a positive scalar, preserving exclusion.

All N summands belong to the same finite-dimensional set. A convex set contains each finite convex combination by induction, so the exhibited average outside is sufficient. An explicitly prescribed pair of partial sums need not be tested; if a pair is wanted, the least failing prefix supplies an earlier prefix and one next summand. The proof makes only this existential pair claim. Adding unused variables preserves the counterexample because restricting them to zero would preserve any hypothetical SOS.

## Boundary and falsification controls

The following attempted failure modes do not invalidate the published theorem:

- q=1 is the SOS cone itself; the non-SOS seed does not belong to it. The membership step is explicitly restricted to q≥3.
- Even q would have positive leading coefficient in this construction and every nonnegative f has the trivial even-power square representation. The theorem does not include even q.
- Hilbert cases where nonnegative forms are already SOS lack the required non-SOS seed and are not contradicted.
- The scalar 0 is harmless; the exhibited seed and its sum are nonzero. Negative scalar closure is never needed.
- The local moment functional is not integration against a positive real measure, since it is negative at a nonnegative polynomial. Only positivity on the specified truncated squares is used.
- Convexity after allowing the exponent to grow does not imply fixed-q convexity. The published predecessor theorem changes the exponent to k+ℓ−1.
- The nonexplicit functionals for larger q are not asserted rational or given the same explicit dimension bound. Their finite existence suffices for the second theorem assertion.

## Computation, independence and incidental exposure

`independent_controls.py` was written before opening the submitted mathematical helper. It uses sparse polynomial arithmetic and Python rational numbers, with no import of a supplied helper or certificate. It gives 55 named checks: full cube identity, homogeneous degrees, coefficient-3 negative control, sample odd-power identities, seed moments, parity splitting, all local pivots/reconstructions, twenty printed minors, explicit finite sign, direct-assignment versus set-partition counting for q=1,…,6 and s=1,2,3, odd/even leading-sign controls, and a small two-block tensor matrix. The partition tests use synthetic moments above degree 18 and are explicitly combinatorial controls, not additional PSD certificates.

The first run failed because my transcription from flattened PDF text read 2^24 as 224 in two moment entries. Source TeX inspection and the subsequently opened helper exposed the transcription error; visual inspection of the published page confirms 2^24. I corrected only my own control, retained its initial version in ignored cache, and reran. This was not a paper defect. Consequently I do not claim the successful controls were completed before any helper exposure; the independent code and its mechanism were already written and do not consume that helper.

After the fresh controls passed, the complete published `verify_package.py` was executed successfully. It verified twelve declared files, authenticated the whole checker stdout against its recorded expected output, required empty stderr, and reported 220 local pivots, twenty initial minors and 24 Schur traces. The exact 13-file package set and both original asset hashes were rechecked unchanged. `replay-receipt.json` binds the executable, certificate, expected-output and fresh output hashes.

No current sibling opinions were read. The manuscript contains earlier-review/priority claims, the checker has historical success labels, and the beginning of `SOURCE_VERSIONS.json` contains earlier reading-extent status while giving source hashes. Those incidental statements were seen and are not evidence for this verdict. The dedicated priority note was not read or adopted. This is an independent mathematical review, not a claim of complete blindness to every historical status phrase.

## Primary-source interfaces

Fresh raw source hashes and the precise reading extent are preserved in `primary-references.json`.

- Berg–Christensen–Jensen (1979), printed pp.163–167, were read visually from the scan. Lemma1 is exactly the dehomogenized coefficient-1 seed. Theorems3–4 provide the historical closure/separation and positive-functional context. The submitted proof gives its own sufficient finite-dimensional argument, so no infinite-dimensional theorem is being silently substituted. Source: https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0243/LOG_0040.pdf.
- Reznick's 2023 Oberwolfach contribution, printed p.779, states the fixed odd-power convexity question and records the coefficient-1 seed within the stated cube-SOS range. Source: https://ems.press/content/serial-article-files/47007.
- Blekherman–Kozhasov–Reznick's published 2026 article, §6 and p.24, supplies the cube identity at parameter a=1. Theorem5.3 increases the exponent and yields convexity only of the union. Relevant passages were checked, not the whole article. Source: https://doi.org/10.1017/fms.2026.10221.
- Barak–Kelner–Steurer, AppendixA LemmaA.5 and proof, gives the corresponding product pseudoexpectation positivity. The manuscript's finite tensor proof verifies its own interface directly. Source: https://eccc.weizmann.ac.il/report/2013/184/.
- The cited Acevedo–Blekherman Lemma2.1 and Blekherman–Riener Proposition6.4 were checked as historical collision/asymptotic precedents, not as substitutes for the exact partition identity. The cited *Stubborn Polynomials* Theorem2.2 was checked for its exponent-increasing statement. No full-body reading of these papers or global priority audit is claimed.

## Final scope and remaining limitations

The strongest verified result is the full stated theorem: the explicit N=10^62 disjoint-copy average disproves convexity of C(3·10^62,6,3), and for every fixed odd q≥3 the finite separation/tensor/counting proof yields a nonconvex sextic fixed-power set in some finite dimension n(q).

No unresolved mathematical gap was identified in that scope. The dimension is only a sufficient bound; neither ternary nonconvexity, minimum dimension, uniform dimension over q, complete classification nor worldwide novelty has been established by this review. The check is AI-assisted mathematical and exact computational review, not human peer review or a formal proof-assistant certificate. No repair, publication action or outreach was undertaken.
