# Independent audit: real vanishing subspaces of elementary symmetric polynomials

Problem 30005519; OWR-13750332-001; catalog rank 799.
Audit date: 5 October 2026 (UTC).

## Verdict and scope

**PASS.** The frozen author packet proves the complete cleaned target, with correct credit to Alper Ferudun's explicitly unrefereed preprint, version 1.0 of 30 September 2026. For each positive integer n and each even r >= 2, the largest real vector-space dimension of a subspace of R^n on which e_r is identically zero is min(n,r-1). When r >= 4 and n >= r-1, every subspace attaining dimension r-1 is a coordinate subspace.

The recommendation is **already_solved**, after one substantive reconstruction approach out of five, with the qualification that the inspected prior is unrefereed. This is a mathematical verification of the stated theorem, not a journal acceptance, editorial solved-status, originality, or priority claim. The separate star-transform theorem is outside this audit.

The author freeze was verified before review, extracted to a separate working directory, and not edited. Its eleven archive members match the expected safe payload. All ten files covered by its manifest match their lengths and SHA-256 values. The manifest itself matches the supplied independent hash. Normal and optimized execution of the frozen verifier reproduce all 710,862 checks and the exact original result bytes.

## Independent reconstruction of the proof

Here e_j(x) is the sum of all products of j distinct coordinates, e_0=1, and e_j=0 for j>n. Every dimension below is a real vector-space dimension.

### 1. Adjacent coefficients and real-rootedness

For a real-rooted nonconstant polynomial P, suppose P'(a)=P''(a)=0. If P(a) were nonzero, writing its real roots with multiplicities as rho_i gives

    (P'/P)'(a) = -sum_i 1/(a-rho_i)^2 < 0.

The left side equals P''(a)/P(a) when P'(a)=0, a contradiction. Hence a is also a root of P. Direct factorization at a shows that a root of P of multiplicity m produces a root of P' of multiplicity exactly m-1. Therefore a multiple root of P' lifts to a root of P with multiplicity one greater. Repeated differentiation preserves real-rootedness by Rolle's theorem, including multiplicities.

Now let P(t)=product_i(t+x_i). If 2<=r<=n and e_{r-1}(x)=e_r(x)=0, the degree-r polynomial Q=P^(n-r) has both its constant and linear coefficients zero: these coefficients are (n-r)! e_r(x) and (n-r+1)! e_{r-1}(x). Thus its zero at t=0 has multiplicity at least two. Lifting through the n-r derivatives forces P to have at least n-r+2 zero roots. Exactly those roots correspond to zero coordinates of x. Consequently x has support of size at most r-2.

The endpoint r=n needs no lift. For r=n+1, e_{r-1}=e_n is the coordinate product, so one zero coordinate gives the same support bound. For r>=n+2 the support bound is automatic. No parity condition was used; applying this lemma with index 3 later is legitimate.

The alternative Descartes argument was also challenged directly. Remove zero coordinates and set E(t)=product(1+x_i t), of degree s. It has s nonzero real roots, counted with multiplicity. Descartes gives s <= V(E(t))+V(E(-t)). A gap of d between successive nonzero coefficients contributes 1 to this sum when d is odd and either 0 or 2 when d is even. This is at most d, and strictly less for d>=3. Since all the gaps sum to s, two consecutive missing coefficients strictly below the leading one would contradict the lower bound. The leading-coefficient cases s=r and s=r-1 are ruled out separately. This proof counts negative as well as positive roots and does not assume all coordinates have the same sign.

### 2. The finite arrangement and the genuine two-plane

Let L have dimension d>=2 and let e_r vanish on L for even r. For each coordinate index set J of size at most r-2 put K_J=L intersect E_J. Suppose every K_J had dimension at most d-2.

Select y outside the finite union of K_J. This is possible because a real vector space cannot be a finite union of proper linear subspaces: extend each to the kernel of a nonzero linear form, and take the product of those forms. A nonzero polynomial cannot vanish everywhere on R^d.

Then select z outside the finite union of K_J+span(y). These subspaces have dimension at most d-1 and are still proper. In particular z is not proportional to y, because J=empty is available. If ay+bz is in K_J, a nonzero b would put z in K_J+span(y), and b=0 with a nonzero would put y in K_J. Therefore U=span(y,z) has U intersect K_J={0} for every J.

The adjacent-coefficient lemma implies that e_{r-1} has no nonzero zero on U. But the curve y cos(theta)+z sin(theta), 0<=theta<=pi, never passes through the origin. Its endpoint values under e_{r-1} are nonzero and opposite, since r-1 is odd. Continuity forces a zero between them, a contradiction.

Thus some J satisfies dim(L intersect E_J)>=d-1. This argument does not assume that L is generic. The plane is deliberately chosen inside the arbitrary given L. Neither a hyperbolicity cone nor an unproved Hessian bound is being substituted for this step.

### 3. Dimension bound and all boundary cases

If n<r, e_r is identically zero and the largest dimension is n. Otherwise any vanishing subspace of dimension at least r contains an r-dimensional vanishing subspace. Applying the previous paragraph gives

    r-1 <= dim(L intersect E_J) <= |J| <= r-2,

which is impossible. A coordinate subspace of dimension r-1 attains the bound because each squarefree monomial of degree r uses a coordinate outside its support.

For r=2, the sparse set is just the origin; the same two-plane argument still works. For n=r, e_r is the coordinate product, consistent with the bound. For n=r-1 the whole ambient space attains dimension r-1. Positive even r is essential: r=0 is outside the claim. The theorem has no missing ambient dimension, degree, support, or genericity regime.

### 4. Classification at maximum dimension

Suppose r>=4, n>=r-1 and dim L=r-1. The sparse-intersection conclusion yields |J|=r-2 and E_J contained in L. Choose w outside E_J and subtract its J-coordinate part, which belongs to L. Then w is nonzero, vanishes on J, and L=E_J direct-sum span(w).

For x in E_J, the disjoint-support generating-polynomial identity gives

    e_r(x+t w)=sum_(i=0)^(r-2) e_i(x) t^(r-i) e_(r-i)(w)=0.

Coefficient extraction in t is valid as a polynomial identity in x and t. Each e_i restricted to E_J, for 0<=i<=r-2, is a nonzero polynomial, so all scalars e_2(w),...,e_r(w) must be zero. In particular e_2(w)=e_3(w)=0. The parity-free coefficient lemma with index 3 implies that w has at most one nonzero coordinate. Since w is nonzero and supported off J, adjoining that coordinate proves that L is a coordinate subspace.

This conclusion covers n=r-1 too. It concerns subspaces of **maximum dimension**, not every subspace maximal under inclusion. For r=4 in R^5, the plane (s,-s,t,t,-t/2) has a full-support point and annihilates e_4. It cannot lie in a coordinate three-space. The proved classification therefore makes it inclusion-maximal despite its dimension 2 being below the maximum 3. The author packet states the dimension restriction correctly; shortened summaries should retain it.

### 5. Independent boundary and overclaim controls

- The r=2 line through (1,1,-1/2) has e_2=0 and is non-coordinate. The r>=4 restriction in the classification is necessary.
- Opposite coordinate pairs yield an r-dimensional e_r-zero space in R^(2r) for odd r. Hence the upper bound cannot be extended to odd degrees.
- Over C, (s,t,omega t,omega^2 t), with omega^2+omega+1=0, gives a two-dimensional e_2-zero space. The field restriction is essential.
- The r=4 full-support plane above refutes Conflitti's adjacent stronger support heuristic. That heuristic is distinct from Conjecture 8. Its credited counterexample is already in Ferudun's Remark 3.4 and belongs to Chirvasitu's reciprocal-block family.
- For an affine zero space a+W, the coefficient of t^r in e_r(a+t w) is e_r(w). Thus W satisfies the vector theorem and has the same upper bound. This extension does not classify translations or assert that an affine zero space must contain the origin.

## Source identity and prior-work checks

Conflitti's original journal PDF was read at the definitions and at page 224, including a fresh visual inspection. Conjecture 8 concerns all real vector subspaces and even degrees. The stronger adjacent heuristic is visibly separate. OWR 21/2023 page 1131 was independently read and rendered: it recalls that conjecture and then states only the n=r+1 special case. The preceding star-transform question is a different question. Both online PDF text endpoints were accessible during this audit.

The complete supplied problems and research-results files were independently hashed and matched to the public pinned repository manifest. The full selected numeric record was read; its cleaned statement asks only Conflitti's question, while its original historical excerpt includes the preceding star-transform sentence. The catalog's Git blob identity, record, statement hash, and review hash were independently recomputed. The review hash is SHA-256 of Python json.dumps([full_problem_record, {}], sort_keys=True), matching the pinned queue implementation. All 6,701 prior-report keys were inspected by program: none starts with OWR, and neither the exact problem code nor numeric ID occurs anywhere in that report corpus. An absent report was not replaced with catalog triage.

Fresh read-only repository checks found no matching numeric-ID code, commit, or branch and no PR matching the exact ID, exact code, or Conflitti. The pinned attempts tree has 63 entries, is not truncated, and lacks this ID. The author's broader prior-attempt checks were reviewed as additional bounded evidence, not as proof of universal absence. No relevant existing authored attempt was established. This audit performed no remote write.

Ferudun's deposited PDF was inspected directly, including the entire relevant Section 3, theorem statements, and its explicit unrefereed status. The stored deposited PDF, record response and companion author report were independently rehashed. The PDF matches the record's byte count and MD5. The author's self-verification report is not treated as this audit. Fresh attempts to retrieve the Zenodo record, API response and deposited PDF were unsuccessful (web-reader errors; direct API/PDF requests returned HTTP 403). Consequently this audit relies on the inspected, hash-identified deposited copy for the precise version and does not claim a successful new download or a check for later changes.

Chirvasitu's arXiv abstract page was independently checked and shows v2 dated 4 August 2025. The relevant Theorem 0.2 scope was read in the available PDF: it concerns e_(n-1), not all degrees at arbitrary ambient dimension. Neither it nor the 2021 star-transform special case is being overstated as the all-n proof. The main proof above is self-contained and does not depend on an unaudited general theorem from either source.

## Reproducibility and publication boundary

The author verifier was run unmodified from a separately extracted freeze with normal Python and python -O. Both produced byte-identical RESULTS.json with 710,862 checks. The independent verifier imports no author code and uses subset enumeration, exact rational arithmetic, and sparse multivariate expansion to challenge adjacent coefficients, derivative identities, Descartes signs, small RREF families, and hypothesis controls. Its results and the optional full-input provenance verifier accompany this audit. No finite computation is asserted to prove the universal theorem.

This payload contains only the audit, correction/qualification record, independently authored code, exact outputs, manifests and public verification metadata. Source PDFs, extracted passages, page images, raw datasets, source archives and private working records are excluded. The original author archive and source files are not bundled into this audit archive.

## References

1. Alessandro Conflitti, *Zeros of Real Symmetric Polynomials*, Applied Mathematics E-Notes 6 (2006), 219-224. https://www.math.nthu.edu.tw/~amen/2006/051014-3.pdf
2. *Tomographic Inverse Problems: Mathematical Challenges and Novel Applications*, Oberwolfach Reports 21/2023, especially p. 1131. https://ems.press/content/serial-article-files/47012
3. Alper Ferudun, *Star Transforms Without Type 2 Singular Directions and Conflitti's Conjecture on Elementary Symmetric Polynomials*, version 1.0, 30 September 2026, unrefereed preprint. https://doi.org/10.5281/zenodo.23062557
4. Alexandru Chirvasitu, *Fano schemes of sub-maximal elementary symmetric functions*, arXiv:2507.19163v2. https://arxiv.org/abs/2507.19163v2
