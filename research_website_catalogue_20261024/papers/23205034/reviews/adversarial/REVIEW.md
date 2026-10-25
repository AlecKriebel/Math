# Independent adversarial review — Zenodo 23205034

**Overall gate: DEFER — unresolved independent validation of load-bearing upstream theorems.**

**The new sparse reduction passes this review as a deterministic Turing reduction to dense factorization.** The established dense-field and construction transfers also survived the checks described below. I found no substantive defect in those reductions and no counterexample to the paper's unconditional corollary. However, I have not independently validated the complete proofs of the two upstream breakthrough preprints on which that corollary depends. Their existence, matching hashes, and correct theorem statements do not establish their correctness. This verdict therefore does not clear the entire paper for promotion as an unconditionally verified result.

This is an AI mathematical review, not conventional human peer review or a novelty certificate. DEFER here identifies a review-coverage gap, not a demonstrated false theorem or a specific missing step in the published manuscript. No repair is proposed or performed.

## Immutable target and reading scope

The target is the nine-page published *Output-sensitive sparse factorization over finite fields from dense factorization*, dated October 6, 2026.

- PDF `paper.pdf`: SHA256 `6e04d462b5229ad310558afd868f21666377e7b5136fad514a7752b20ea4ea10`.
- ZIP `verification.zip`: SHA256 `96c4bdf7d2944b8e741fefa0fad6c112b25672af700ef5aa837e61353ef5ba68`.
- Fresh public `sources/receipt.json`: SHA256 `96afc6d5191575cb48406f80f4bf90ea3617b645ff3acc93cd3a75cb4fce73c9`, retrieved 2026-10-25T00:43:20.885565+00:00.
- Current TeX: SHA256 `fbabb3ecaf36fa49416e6b7c0bbc32e73be26902bda9d66e9f85228ef6733d58`.
- The PDF embedded in the ZIP is byte-identical to the separately published PDF.

I read all nine PDF pages, including every main statement, proof, complexity paragraph and limitation. Mathematical support read includes the complete `SPARSE_CANDIDATE_DERIVATION.md`, `agent_notes/construction_reduction.md`, and `agent_notes/extension_reduction.md`. I read the full production sparse and dense reference implementations, their sparse tests, the independent extension multiplicity checker, and the reproduction driver. Other bundled checker executions were replayed, but this report does not claim a line-by-line audit of every historical checker or every upstream page.

Independence qualification: the mathematical support files mix derivations with historical workflow/status and review summaries. Those summaries were incidentally encountered and ignored as evidence. No archived standalone verdict/report was deliberately consulted; no current sibling mathematical opinion was read. A proposed child import task could not proceed because that child was occupied by a parent-assigned review, so the primary inspection here was performed by this reviewer. Public primary-source bytes were downloaded afresh into this review's own directory.

## Strongest verified result

For the promised explicitly represented field `K=F_p[T]/(h)`, with p prime and h monic irreducible of degree m, let a nonzero sparse polynomial have t nonzero terms, distinct nonnegative binary exponents, maximum exponent N, and `b=max(1,ceil(log2(N+1)))`. Let D be the sum of the degrees of the distinct monic factors that will be returned densely; multiplicities are binary integers.

Theorem 1's deterministic reduction uses at most 2b dense-factorization calls of degree at most `(b+1)D`, and polynomial nonoracle bit work in t,b,D,m,L. Its bound includes arbitrary characteristic-divisible multiplicities. The direct prime-Frobenius transfer then needs at most `2b(b+1)D` prime-field polynomial-factorization calls at the same degree bound. Constants and monomials have explicit trivial branches.

This is an output-sensitive statement for **dense distinct factors plus binary multiplicities**. It is not polynomial in sparse factor term count, not polynomial in log of a requested dense construction degree, and not a factoring algorithm for general arithmetic circuits. Numeric D and the explicitly supplied field representation are legitimate input/output parameters. None of the reduction algorithms enumerates p or the numeric sparse degree N.

## Adversarial audit of the reduction

### Known-factor multiplicities

For an irreducible `g != X`, the root alpha in `K[Z]/(g)` is nonzero and separable. The order of `f(alpha(1+Y))` is therefore the multiplicity of g. The actual integer exponents must be retained even though modular powering reduces them internally; reducing the exponent labels by alpha's multiplicative order would destroy this order information.

Grouping by the low base-p digit gives the stated recursive expansion. Child polynomials are nonzero because their exponent lists remain distinct and their weights nonzero. Among the minimum-order children, the polynomials `(1+Y)^r` with distinct residues r form an invertible low-binomial-coefficient system: the factorial denominators used have index below p. The first nonzero coefficient lies before the next possible child's contribution. This validates the parent order `pv+j`, including cancellations, a zero order, and arbitrarily large order.

Each level partitions at most t terms and the depth is at most b; the sum-of-squared-support bound is consequently polynomial. Inspecting s coefficients rather than p is essential and is respected. The `g=X` valuation is the minimum input exponent. The residue bound `valuation mod p <= t−1` supplies the later dense product bound; it is not merely a numerical observation.

### Exact Padé recovery

The reduced denominator of `U'/U` is precisely the squarefree product of factors with multiplicity nonzero modulo p. This follows from the pole residue at each separable root. Multiplicities divisible by p are invisible, which is why this step alone is not complete factorization.

The truncated series requires only sparse coefficients up to index 2B. With `Q(0)=1`, the reconstruction linear system is correctly sized. The exact identity `U'Q=UA`, checked as a sparse-dense product, prevents false acceptance after a long zero Taylor prefix. At B at least the true denominator degree, `AG−PQ` has both order at least 2B and degree below 2B, proving exactness. Doubling reaches that point within the stated constant factor. No numeric-N scan is hidden in either the identity test or series extraction.

### Cartier descent, carries and transient factors

Maintaining `F=U/V` as a polynomial with V dividing U is sufficient; U itself need not divide a simple sparse expression after removing factors. The multiplicity inequalities imply `H=H_U/H_V` is polynomial. Its radical is contained in that of F, since a factor absent from F has equal U and V multiplicities and equal floor quotients.

The constant-section pull-out identity is valid with coefficient Frobenius on the pth-power factor. Both sections need inverse coefficient Frobenius. Applying it to only the numerator would be wrong over a nonprime field. Nonzero constant terms keep the section denominator nonzero and preserve the invariant.

The denominator estimate is valid even when a new factor is not a factor of the original input: `D_U <= D_F+deg V`, and `deg V_new <= deg V + D_F`. The sparse multiplicity residue bound, independently, keeps `deg A_U <= (t−1)D_U`; thus forming A_U never requires a loop of length p. After k descents, `deg V <= kD`. The shrinking sparse numerator degree, rather than the polynomial quotient degree, proves termination.

Signed ledger contributions correctly handle borrows/carries and transient factors. The identity `e_F=(e_U mod p−e_V mod p)+p e_H` telescopes to the final nonnegative multiplicities. Discarding negative intermediate residues would invalidate the algorithm, but neither the manuscript nor implementation does that. The initial leading coefficient is retained to recover the final unit, including nonmonic extension-field examples.

### Bit complexity and certificates

Dense oracle degrees are bounded by the current radical and denominator degrees, at most `(k+1)D` and kD. Padé dimensions, known-factor quotient dimensions, dense residue products and the number of temporary factor labels are polynomial in the stated parameters. Exponents are binary integers; inverse Frobenius uses exponent `p^(m−1)` with O(mL) bits. Canonical finite-field coordinates prevent coefficient-height growth.

The displayed `M^24` bound is deliberately loose but dominates the schoolbook dimensions and operations described; it does not claim practical feasibility. Polynomial dependence on numeric D is consistent with the requested dense factor output. Sparse output verification uses original-input valuations, irreducibility, leading coefficient and weighted degree equality. It does not expand a huge binary multiplicity into a dense polynomial.

### Dense-field and construction transfers

The q-Frobenius map is K-linear, while p-Frobenius must be treated as F_p-linear. The ambient dimensions in the two variants respect that distinction. The trace-coordinate argument uses all power-basis multipliers, so it remains valid when p divides m and `Tr(1)=0`. Minimal polynomials of p-fixed elements are products over their distinct prime-field component values, justifying both conversion to F_p and complete splitting. Gcd refinements separate component pairs without enumerating the field.

The squarefree recursion handles derivative-zero inputs with inverse coefficient Frobenius. Disjoint emitted supports justify summing oracle-degree bounds; merely multiplying a worst-case per-call cost by the numeric input degree is not needed. The representation test uses repeated modular Frobenius powers and gcds, not factorization of p−1.

The construction lift from degree md over F_p to degree d over K follows from Frobenius orbit lengths. The supplementary proof treats the odd-prime binomial case, Artin–Schreier towers, and the exceptional 2-power case separately. Trial division of md is permitted by dense output size. The claim remains polynomial in numeric d, not log d.

## Reproduction and fresh falsification controls

`published-replay.json` records successful clean reproduction with the frozen public fileset authenticated. Fifteen command groups exited zero: dense tests/examples, direct and crosschecked extension reductions, regenerated construction and coherence fixtures, three local upstream finite checkers, the sparse unit suite and five sparse checkers. Generated fixtures were deleted before regeneration and compared against their recorded mathematical fields. The suite includes the advertised 377 small dense inputs, 346 independent extension comparisons and 960 sparse/dense comparisons. It does not execute the huge-characteristic upstream algorithm or prove the analytic zero-free theorem.

Fresh `fresh_controls.py` passed **7,858 exact checks**, also under optimized Python:

- 2,208 independent Hasse-coefficient valuation computations over five prime fields were compared against the exponent-digit trie; its residue and node bounds were checked as well.
- 408 logarithmic denominators were checked by independent dense gcd recovery, together with the adaptive stopping bound.
- Complete factorization controls used 61-, 127- and 521-bit prime characteristics and exponent lengths up to 1,563 bits. A guarded oracle permitted only linear requests and no enumeration; in fact these degree-one-output cases needed zero prime-oracle calls. The runs used 8, 5 and 4 descent levels respectively.
- Two nonprime-field examples used two distinct repeated nonzero factors, a scalar unit and a shifted X factor. Their huge multiplicities and the denominator, visible-degree and residue-product invariants were checked at every level.
- Negative controls tested a misleading zero Taylor prefix, the necessity of retaining full exponent labels, and nontrivial inverse coefficient Frobenius.

The first new reporting run attempted to take the maximum of an empty oracle-query list. This was corrected to report zero calls; no mathematical check had failed. The production files were not modified. Finite successes support the mechanism but are not universal complexity certificates.

## Primary imports: checked scope and exact unresolved gap

The pinned OpenAI factorization PDF was freshly downloaded and has SHA256 `ed88aa5ba802311a21c4f265bcef43515a16019f4b5afdd7f52ecbd36ce0204d` (48 pages). The companion primitive-roots PDF has SHA256 `671ac4b3ece879f614ed8f4b782e61a07805e533f385a694fe4d7afbda3c9365` (92 pages). Both match the paper's pinned commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`; access was successful. URLs and additional TeX hashes are in `primary-imports/receipt.json`.

I checked the prime-factorization Theorems 1.1/1.2 and their distinction between the numeric auxiliary-prime parameter E and its bit length. The advertised unconditional exponent is indeed `10^12`. The full analytic auxiliary-prime section was read: its deduction uses the fixed-width strip for every finite-order Hecke character over cyclotomic fields containing the twelfth roots of unity, specifically `F=Q(mu_(12q))`, followed by abelian zeta factorization for `F(p^(1/q))/F`. This is the required scope; a Dirichlet-only statement would not suffice. The discriminant and smoothed explicit-formula estimates, exponent margins and upward search argument are consistent with that premise. Search does not require knowing the numerical absolute onset constant, so I found no separate effectivity mismatch.

In the 92-page companion I read the exact Theorem 1.2 statement, the full zero-detection/Mellin-continuation section, the cubic theta input statement, the beginning of the Whittaker-normalization appendix, and selected Poisson/Euler-product statements. In the prime-factorization paper I additionally inspected the cyclic-algebra/rank-one-idempotent argument. These checks did not establish a defect, but **they are not a full independent verification of those papers**.

The precise remaining gap is the unchecked chain supplying the unconditional prime-field algorithm: the general-field cubic-theta normalization and required local/global imports (including Kazhdan–Patterson and its correction), the complete reflected moment proof and quadratic-sieve application, the complete Poisson/local Euler-product derivation and its nowhere-zero correction, together with the remaining algebraic separator/divisor algorithm and uniform complexity proof in the 48-page factorization paper. The reviewed Mellin continuation is conditional on the reflected-probe and Euler-product inputs; reading its final contour argument cannot replace verification of those inputs. No relevant Lean build was run, and the paper itself disclaims formal verification of the required varying-field theorem.

For the classical construction import, I visually read Shoup's [author-hosted primary PDF](https://www.shoup.net/papers/detirred.pdf), pages 6 and 8–10, including Theorems 3.1 and 4.1 and their explicit representation/oracle context. Its SHA256 is `00590fb8f0717338530b067626428781991edb840fb74c37cf846f07f50e0644`. The reduction and attribution match. No exhaustive novelty audit was attempted.

## Final disposition

**Conditional algebraic result: PASS. Entire published unconditional package: DEFER pending independent validation of the specific upstream chain above.** There is no confirmed manuscript error and no repair request. The current exact gap is in this review's evidence coverage, not a claim that the authors omitted those proofs. Any later gate can be reconsidered if that missing primary proof verification is supplied. Historical priority and conventional human peer review remain outside this verdict. No website, spreadsheet, Git, Zenodo or outreach action was taken.
