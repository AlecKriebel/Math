# PR1224 / 2302 / EP783: independent original-scope and prior-result decision

**Decision: the full fixed-C near-minimum asymptotic claim qualifies under an interpretation explicitly permitted by the original problem. Its proof is accepted relative to the stated classical analytic dependencies, with the candidate's local repairs. The exact/eventual optimizer and general harmonic rigidity are not resolved. No DOI for the full general-modulus target was authenticated, so no four-cell tracker proposal or new upload is authorized by this review.**

This is an internal AI-assisted mathematical review, not conventional human peer review, a formal proof certificate, or a priority claim. Audit family completion is 100% on sealing; overall parent goal remains 79%. This family was completed before starting PR1226.

## Fresh scope and pinned materials

A fresh GWS CLI numeric data-filter read preceded mathematical review: spreadsheet `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`, sheetId `1254632077`, all 43 columns, no row bound, 191 populated rows. The problem ID, EP783/title/modulus/Dickman/Tao/Chojecki/PR aliases tested yielded no target match. Raw workbook content is private.

The live draft is pinned to head `8e54e3afc45191e870739ba7997713d691de89a2`, base `4b27092a448d53b61408355ce44ec38d103a1ce4`. All eight actual changed files were materialized independently; sizes/hashes are in `PINNED_BINDINGS.json`. The comparison contains no QUEUE edit. `AUDIT.md` has 29,054 bytes, SHA-256 `8a9c0cc8e780410fec9a1aeac2b1eb1f894e468ab25a537804412c6b7cd20587`; the finite `PROOF.md` has 4,437 bytes, SHA-256 `4be00c28ca3be4fcc3c721bd6961cf4cef510a8054cf10cd9597b41213a4b58d`.

The original 1973 article was freshly fetched from the Rényi archive. Its printed page 135, PDF page 19, was read and visually inspected. Erdős asks which pairwise-coprime moduli under a reciprocal budget minimize the uncovered count, proposes a descending prime tail, and expressly allows that it at least nearly gives the minimum. Thus the sharp leading value and an asymptotically attaining tail are a complete answer to that near-minimum reading, even though Tao calls it a weak form or one interpretation. This does not justify marking every possible exact optimizer question solved.

The original uses a strict budget `<c1` in (14.3), but (14.4) uses a non-strict tail budget; this minor convention cannot change the fixed-C leading answer. For the strict class, tails constructed at `C-ε` are feasible eventually and have limiting density `ρ(exp(C-ε))`; let ε decrease to zero. The lower bound for the non-strict class also bounds the strict class. Positivity and continuity give the same asymptotic value and ratio-near-optimality for fixed C. Likewise `a<n` versus `a<=n` changes the objective by at most O(1) and the endpoint reciprocal mass by O(1/n).

Fresh exact PDFs all match the historical candidate pins:

- Erdős 1973, 22 pages: SHA-256 `da5a584aa60527424b7deded98398f8ab359758a3a62ea5bf60e1f2f7d803a71`, 2,991,424 bytes.
- Tao, *Sieving by coprime numbers*, 22 February 2026, third version, 8 pages: `05f46d174d9e25b49930e5481c249f915afb96c58c1ee300dede3f9f5c7b93d6`, 292,271 bytes.
- Chojecki January note, 6 pages: `621a7c899a1fd9834c73fae4273d33aebb89f5c98682911da4fd2144bbaaabe3`, 125,197 bytes.
- Chojecki February note, 25 pages: `40606c7d7a545e3e0790a58df287f363acf3ff46f676bc3170b0b16b81f9dfce`, 191,166 bytes.
- Granville–Soundararajan, arXiv:math/0308009v1, 21 pages: `93849e7e9c7d161776d58ff1bffcd804355f80c5b343edc1dc8e9e2d48757d70`, 230,845 bytes.

Tao's entire eight-page proof was read freshly. The January note was read, and the February statement, budget construction, fixed-cutoff compactness/stability, and final reduction were inspected for the claims actually used. The GS introductory lower-value statement, Section 2 dictionary, and Theorem 5 on page 14 with its equality statement were inspected in the primary paper. This review imports the published classical prime-sieve theorem; it does not certify all 21 pages' numerical bounds or the entire dependency closure. The original target page, Tao's displayed Bonferroni formula, and the February fixed-error reduction were also visually checked. No author program was run.

## Independent core proof assessment

Let `μ(A)=Σ1/a`, and let `σ_N(A)` be the fraction of integers at most N divisible by none of A. Fix C while N grows, allowing A to vary. The certified statement is

`min_{A⊂{2,...,N}, pairwise coprime, μ(A)<=C} σ_N(A)=ρ(exp(C))+o_C(1)`.

The error is uniform over the admissible sets, and the maximum-length feasible descending prime tail attains it asymptotically.

For the upper bound, choose the maximal number of descending primes whose reciprocal sum stays at most C, and let y be the next prime. Divergence of the prime reciprocal series gives existence of that next prime eventually; for every fixed B the reciprocal sum of primes in `(B,N]` eventually exceeds C, so y tends to infinity. The unused budget is less than `1/y=o(1)`. Mertens gives `log y/log N=exp(-C)+o(1)`. The surviving integers are exactly y-smooth. A sandwich between fixed exponents `exp(-C)±η`, followed by η tending to zero, yields density `ρ(exp C)`. This avoids any unproved uniform Dickman assertion for an arbitrarily moving parameter.

The January statement about deleting a bounded number of boundary primes is not justified by a bare o(1) Mertens error; after deletion the exact smooth-number identity at the old cutoff is false. February's definition of a maximal feasible cutoff y gives y=N and an empty tail. Both are repaired by choosing the maximal number of descending primes, with its actual next-prime cutoff. At C=log 2, an overlap-free proof can instead start above sqrt(N), remove the smallest such primes until feasible if necessary, and track the vanishing reciprocal loss; no claim that the exact greedy cutoff is always above sqrt(N) is needed.

For the lower bound, pairwise coprimality supplies an injection from composite moduli at most X into primes at most sqrt(X). Consequently the reciprocal mass of composites above Z is O(Z^(-1/2)), uniformly in A. Removing them changes σ by at most their reciprocal mass, directly by the union bound.

Bonferroni for the genuine events `{a divides n}` gives truncated inclusion-exclusion in reciprocals of products, plus a factorial tail `C^(r+1)/(r+1)!`. For each fixed degree j, the ordered largest modulus is at least `Q^(1/(j-1))`, with `Q` the product of the earlier ones, and at most `N/Q`. Therefore a nonempty last-modulus sum has `N/Q>=N^(1/j)`. Prime counting plus the composite injection bounds its cardinality by `O(jN/(Q log N))`. Summing over prefixes bounds all normalized floor errors by `O(r exp(C)/log N)`. The j=1 case is direct, avoiding division by j-1.

Tao's middle indicator in equation (2.1) is printed as the gcd-one event. For composite moduli it is different: 4 does not divide 2, but gcd(2,4) is not one. Replacing only that indicator by the avoidance event makes the displayed floor formulas and Bonferroni proof exactly consistent. This is a local correction, not a missing central theorem.

Choose r large first, then fixed Z large, then N large. The scales `z_j=Z^(r^(2j))`, j=0,...,r, contain r consecutive annuli. One has reciprocal mass at most C/r. Remove that annulus, put the lower remaining moduli in A1 and the upper in A2. All A2 elements are prime. The product expansion has extra degrees r+1 through **2r inclusive**, bounded by the factorial tail. The extra low-degree terms crossing N constrain the largest prime to a multiplicative interval of ratio at most `z_-^r` above `z_+`, whose reciprocal mass is `O(r log z_-/log z_+)=O(1/r)`. This proves uniform splitting. Tao's undefined `z2`, omitted endpoint `j=2r`, mistaken `q_(j-1)` index, and undefined `z_(-1)` annulus are corrected by `z_+`, inclusive degree, last-small-element index, and annuli j=1,...,r. All bounds survive.

For fixed z_-, eventually `z_-^r<=N`, so the small truncated sum is its finite Euler product plus a factorial tail. Thus

`σ_N(A)=Π_(a∈A1)(1-1/a) σ_N(A2)+O_C(ε)`.

For completeness about the classical dependency's dictionary: GS uses a multiplicative Euler-product parameter Θ, not literally the reciprocal sum μ. In the present A2 all primes exceed fixed Z; hence `log(1/Θ)=μ(A2)+O(Σ_(p>Z)1/p²)=μ(A2)+O(1/Z)`. Its classical uniform lower-value theorem, or a subsequence compactness application of its definition of g(w), therefore gives `σ_N(A2)>=ρ(exp(μ(A2)))-O_C(ε)` after Z is chosen large. One must not simply identify Θ with exp(-μ) for sets containing a fixed small prime. The small-prime contribution here is separately retained in the Euler product, so no such unsupported identification is needed.

Write `R(t)=ρ(exp t)`. Since `1-1/a=R(1/a)` for a>=2, and classical Dickman log-concavity gives `R(x)R(y)>=R(x+y)`, the product and prime lower bound are at least `R(μ(A1)+μ(A2))-O_C(ε)>=R(C)-O_C(ε)`. Let ε tend to zero. This is the matching uniform lower bound. Dependencies are the classical GS/Hildebrand prime-sieve lower theorem, prime counting/Mertens, fixed-parameter Dickman asymptotics, and Dickman positivity, continuity and log-concavity. Their complete historical proof chain and GS numerical inequalities were not newly interval-certified. These are explicit accepted mathematical inputs, not computational assumptions or unidentified hard replacements of the target.

## Stronger claims and finite controls remain separate

The candidate's fixed-power-cutoff prime stability is a fixed-u compactness/equality argument. GS Theorem 5 supplies the step-function equality case at w>2. Domination of exclusion measures by dt/t on a fixed compact interval gives weak compactness, endpoint nullity, and continuity of the finite-series objective. This supplies a positive stability modulus for that fixed interval. Chojecki's Corollary 35 requires the missing small-prime condition and total error `2δ+o(1)`, not `δ+o(1)`; using a smaller input tolerance repairs its application above one fixed cutoff.

The general reduction's ε is fixed before N grows. Its claimed vanishing errors are only O(ε)+o(1), and its cutoff u depends on the requested tolerance. An arbitrary small fixed loss does not become o(1); a diagonal loss tending to zero may force u to infinity, outside the proved fixed-u stability modulus. This is the exact remaining bridge for general harmonic rigidity. The candidate correctly does not claim a counterexample to that theorem or global openness. Its two-parameter composite-mass argument can recover vanishing composite reciprocal mass and tightness, but tightness does not give one fixed cutoff with o(1) mass loss.

The corrected derivative for `u^(3/2)ρ(u)` is `u^(1/2)((3/2)ρ(u)-ρ(u-1))`. The integral identity `uρ(u)=∫_(u-1)^uρ(v)dv<=ρ(u-1)` proves the needed decay for u>=2. Choosing the strictness tolerance first, then the scale/error small enough for that tolerance, avoids the printed circular ε choice. These repairs are compatible with the limited composite-mass conclusion; they do not supply the missing cutoff uniformity.

At N=100, C=1/2, the exact greedy prime tail has uncovered count 62; replacing 17 and 23 by 7 is feasible and leaves 57. Both sets are prime, pairwise coprime, and products of any two exceed 100, so the floor counts have no overlaps. The independently written standard-library checker reconstructs the tail rather than trusting its list, checks both exact rational budgets and both direct/floor counts, and also tests Bonferroni on every coprime subset of `[2,15]` for N<=40. Three Python modes produce identical successful outputs. These are finite diagnostics; they do not disprove any fixed-C eventual statement. No claim of global optimality of the replacement is made.

## Publication/accounting disposition and exact limits

The bounded fresh search of the author manuscript titles and DOI registries did not authenticate a DOI for Tao's full general-modulus theorem or the corrected general result. The public PDFs exist and their exact bytes are authenticated. GS's journal DOI `10.4064/aa115-4-1` and arXiv DOI are identifiers of the classical prime-case dependency; they must not be substituted as if the whole general-modulus target had been published under them. No absence of all possible DOIs is proved.

Therefore this review produces a safe authored result record with the public source URLs, correct authorship/dependencies and a null target DOI. It produces **no A:D proposal**, performs no tracker write and makes no upload. Lack of a target DOI is an accounting limitation, not permission to republish an existing author's contribution. No current journal acceptance is inferred from Tao's historical no-journal-plan discussion, which was not used in the mathematical decision.

Strongest verified full result: the sharp fixed-C asymptotic near-minimum and a correctly budgeted attaining prime tail for all pairwise-coprime moduli. Exact remaining gaps: general harmonic rigidity's cutoff-uniformity bridge; exact/eventual optimizer classification; target DOI authentication. None invalidates the full original permitted near-minimum result. All raw PDFs/text/renderings, workbook content, API responses and pinned copies are private evidence, not public payloads. No external communication, service write, Git mutation or generated-skill command occurred in this family.
