# Independent audit of the prior EP730 proof

## Verdict and exact scope

**Conventional mathematical verdict: ACCEPT.** The argument in Will Blair's pinned public `compute/full_density/proof.md` proves the original infinitude question, and the stronger existence of infinitely many consecutive positive pairs. The proof is accepted relative to the explicitly stated classical Kummer, reciprocal-prime Mertens, and fixed-modulus prime-number-theorem inputs. All of the argument's arithmetic, Fourier, counting, limiting, and final-transfer steps have been reviewed below. No unresolved mathematical gap was found. This is an audit of a prior proof, not a new solution or a novelty claim.

**Formal-verification verdict: NOT REPRODUCED.** Lean, Lake, imports, author scripts, and other third-party code were not installed, built, or executed. The source declares an unconditional terminal theorem with the correct target. Bounded static evidence supports the author's exclusion of two admitted experimental declarations from the theorem's proof dependencies. It does not independently establish the elaborated axiom footprint or replay the kernel.

**Registry verdict: UNVERIFIED.** The inherited Palomar JSON endpoints returned HTTP 403. They were not retried through another route. The registry identifier in the author's README is an author claim, not independent registry acceptance.

**Documentation corrections:** the July audit's PNT repository/revision and description of the exact moduli used are stale relative to the current source pin. These are provenance and implementation-description corrections, not mathematical counterexamples. Details appear below.

## Source identity and attribution

The audited author repository is [williamjblair/lean-proofs at f297d710018270c66b296082766334974260bcbc](https://github.com/williamjblair/lean-proofs/tree/f297d710018270c66b296082766334974260bcbc).

The principal conventional source is [the complete positive-density proof](https://github.com/williamjblair/lean-proofs/blob/f297d710018270c66b296082766334974260bcbc/ErdosProblems/Erdos730/compute/full_density/proof.md). Its retained UTF-8 source is 17,246 bytes, SHA-256 `23f69d9b69fe7099d9451c9ef38b47609c99211201ab76433735b89af8adb9d0`. The author's [self-audit](https://github.com/williamjblair/lean-proofs/blob/f297d710018270c66b296082766334974260bcbc/ErdosProblems/Erdos730/compute/full_density/audit.md) is supplementary evidence about the claim, not independent validation.

The repository's [formalization manifest](https://github.com/williamjblair/lean-proofs/blob/f297d710018270c66b296082766334974260bcbc/formalization.yaml) attributes the informal idea to Liam Price's 24 June 2026 forum post, an algebraic follow-up to Tomodovodoo, and the analytic reconstruction/formalization to Will Blair. It expressly describes review as self-assessed and the earlier informal argument as unadjudicated. This audit preserves that attribution; it does not claim to have authenticated the unavailable antecedent manuscript or to settle priority between its contributors.

The original question is in Erdős, Graham, Ruzsa and Straus, [On the prime factors of C(2n,n)](https://www.renyi.hu/~p_erdos/1975-27.pdf), Math. Comp. 29 (1975), at printed page 91. The historically retrieved complete PDF is 1,102,642 bytes, SHA-256 `7c530494dff20efba34c7e022b96d7226273c5ffefc7f87e79c5e13499e124d5`. The earlier inspection of the original question was used; this audit concentrates on the prior proof. This edition does not claim a new PDF retrieval, fresh full-paper reading, or independent review of unrelated results in that paper.

Previously gathered source bytes were hash-checked before this audit. Newly retrieved source receipts were verified against their Git blob identities and, for the main author/PNT projects, the complete pinned trees. SOURCES.json publishes selected public URLs and byte/hash identities; the full working inventory and source bodies are excluded from this prose/metadata edition.

## The original statement and the terminal bridge

Write B(t) = binomial(2t,t), and let supp(N) denote the set of prime divisors of a positive integer N. The question asks for infinitely many distinct positive n < m with supp B(n) = supp B(m). It does not ask for equality of coefficients or prime-adic valuations.

The family is defined by

    T = 5289 = 3·41·43
    P(x) = 42Tx + 11,       Q(x) = 72Tx + 13
    R(x) = 28Tx + 5,        S(x) = 72Tx + 19
    n(x) = P(x)Q(x) − 1

The claimed lower density is in positive integer parameters x, not in n or in all pairs. The exact expansion is

    n(x) = 84591927504 x² + 7076682 x + 142.

Thus n(x) is positive and strictly increasing on nonnegative integers. If more than 107/2500 of the positive parameters survive in lower asymptotic density, there are infinitely many parameters and the map x ↦ (n(x),n(x)+1) is injective. This yields infinitely many distinct positive consecutive pairs, hence the original result. It does not imply positive natural density of n-values; this family grows quadratically.

The [terminal source](https://github.com/williamjblair/lean-proofs/blob/f297d710018270c66b296082766334974260bcbc/ErdosProblems/Erdos730/FullDensityTheorem.lean) declares `candidatePositiveDensity` without an analytic hypothesis and passes it to `pairSet_infinite_of_candidatePositiveDensity`. `FullDensityReduction.lean` expands the former claim to the strict lower-density inequality. `FullDensityCore.lean` defines PairSet using n < m and equality of `centralBinom.primeFactors`, defines GoodParameter with x ≥ 1, and proves injectivity of familyPair. PairSet's ambient type is natural-number pairs, but the actual family has positive entries. The [solution wrapper](https://github.com/williamjblair/lean-proofs/blob/f297d710018270c66b296082766334974260bcbc/PalomarSolutions/Erdos730.lean) uses the same target. The separate Challenge placeholder is not a proof dependency of that wrapper.

## Arithmetic transition criterion

For an odd prime p, let D_p consist of the nonnegative integers whose base-p digits are all at most (p−1)/2. Kummer's theorem gives p ∤ B(t) exactly when t ∈ D_p.

The recurrence (n+1)B(n+1) = 2(2n+1)B(n), together with gcd(n+1,2n+1)=1, shows that an odd prime can change support only at a prime factor of n+1 or 2n+1. If n+1=p^a c with a≥1 and p∤c, the final a digits of n are p−1, so p already divides B(n); it disappears precisely when c∈D_p. If 2n+1=p^a c, then

    n = p^a(c−1)/2 + (p^a−1)/2.

Here c is odd, the lower a digits of n are all (p−1)/2, and adding one forces a forbidden units digit. Thus p enters the support precisely when (c−1)/2∈D_p. For n≥1 the prime 2 divides both central binomial coefficients. These facts establish the full if-and-only-if transition criterion with its positivity and exact-valuation conditions.

The six linear identities and 2PQ−1=3RS check exactly. Their resultant constants are 41,43,1,1,7,6. The residue exclusions show that every pair of branches is coprime, no branch prime is in {2,3,41,43}, P and R are nonzero modulo 7, and Q,S are odd and equal to 1 modulo 3. Moreover 3 divides 3RS exactly once, and (RS−1)/2 has residue 2 modulo 3. The fixed factor 3 therefore creates no obstruction. Prime 7 is not silently dropped.

For p^a exactly dividing a branch L and c=L(x)/p^a, the four quantities tested for membership in D_p are

    ΦP = cQ = (12p^a c² − 41c)/7
    ΦQ = cP = (7p^a c² + 41c)/12
    ΦR = (3cS−1)/2 = (54p^a c² +129c−7)/14
    ΦS = (3cR−1)/2 = (7p^a c² −43c−6)/12.

The product descriptions ensure integrality, including the divisions by 2. The branch slope is a unit modulo every possible branch prime. On its unique root progression x=x₀+p^a k, direct substitution gives

    G(k) = 3024 T² p^a k² + (p^a u_L+b_L)k + v_L,
    (bP,bQ,bR,bS) = (−246T,246T,258T,−258T).

The prime divisors of the b_L are among {2,3,41,43}. Consequently G(k₁)−G(k₂) is (k₁−k₂) times a p-adic unit, and G permutes residues modulo every p^d. Exact valuation deletes the unique input class c=0 modulo p. Its output digit is 0 for P,Q and (p−1)/2 for R,S. If H=(p+1)/2, the exact number of permitted d-digit classes with exact valuation is (H−1)H^(d−1). The prime-7 obstruction to a later quadratic Gauss calculation does not obstruct this permutation argument.

## Event coverage and the two negligible ranges

Let E count all witnessed branch obstructions (x,L,p,a), with x≤X and x≥1. Every bad parameter supplies an obstruction by the exact transition theorem and branch factorization. Hence Bad(X)≤E(X); uniqueness of the obstruction is unnecessary. Split E at a≥2, then at p≤√X, √X<p≤Y, and p>Y for a=1, where Y=√X(log X)². Boundaries are assigned as written, so the split is exhaustive and disjoint.

All branch values are ≤C₀X, where C₀=380827. For p^a≤X and a≥2, set U=X/p^a and r=floor(log_p U). The root progression has at most U+1 integer entries. Padding to p^r-blocks and using permutation gives

    event count ≤ ((U+1)/p^r+1)H^r ≤ 2U(H/p)^r+1.

This also holds when r=0. For each fixed (p,a), r tends to infinity and H/p<1. The normalized first term is dominated by 2/p^a, whose sum over p and a≥2 converges. The number of eligible prime powers is bounded by

    M(Z) ≤ √Z + Z^(1/3) log₂ Z = o(Z).

This controls the extra unit errors and the powers X<p^a≤C₀X, each of which has at most one parameter in its root class. Dominated convergence and this terminal estimate give E_higher=o(X). No Fourier estimate is used for this range.

For the transition range, direct divisibility counts give

    E_transition ≤ 4X Σ_{√X<p≤Y}1/p + 4π(Y).

Mertens makes the prime reciprocal band mass o(1), while π(Y)/X=O(log X/√X). Thus E_transition=o(X).

## Independent review of the fixed-depth Fourier step

Fix r≥1. The required phase is F(t)=pαt²+βt+γ with p odd and p∤αβ, on p^r consecutive inputs modulo q=p^(2r). Translating the input changes β by a multiple of p and preserves its unit condition. Fourier inversion against a digit box has zero-frequency contribution |A|/p^r.

For a nonzero frequency with effective modulus p^m, if m≤r, permutation of residue systems makes the input sum exactly zero. If m>r, complete the interval of length N=p^r modulo Q=p^m. The complete quadratic sum vanishes unless its linear coefficient is divisible by p. In the surviving frequency class its absolute value is p·sqrt(p^(m−1))=p^((m+1)/2), by the ordinary odd-prime unit quadratic Gauss calculation.

The interval Fourier factor satisfies |D_N(s/Q)|≤min(N,1/(2‖s/Q‖)). A shifted grid of Q/p points has at most (Q/p)/u+2 points at distance <1/(2u) from an integer. Integrating this counting bound from 1 to N gives mass at most (Q/p)(1+log N)+2(N−1). Since m≥r+1 implies N≤Q/p, this is at most (Q/p)(3+log N). After division by Q in completion, the incomplete phase sum is at most p^((m−1)/2)(3+log N), and therefore at most

    (2r+3) p^(r−1/2)(1+log p).

The same shifted-grid estimate bounds each digit interval's Fourier mass by p(3+log p). Factoring the box transform digit by digit gives L¹ mass ≤q(3+log p)^(2r). Fourier inversion now gives the claimed discrepancy bound

    (2r+3)3^(2r) p^(r−1/2)(1+log p)^(2r+1).

This verifies the estimate at the quantifiers actually used: r is fixed, a=1, the input block has length p^r, and the constant may depend on r. The proof makes no unjustified uniform-in-depth or arbitrary-prime-power incomplete-block claim.

## Small first powers and interchange of depth limits

For p≤√X, use the unique r≥1 with p^(r+1)≤X<p^(r+2). For each fixed r the primes in that band eventually exceed 43. Therefore p∤3024T² and p∤b_L, including exclusion of the exceptional prime 7 in this fixed-r application. The exact box density is

    δ(p,r) = 4^(−r)(1−1/p)(1+1/p)^(2r−1).

Splitting the root progression into p^r-blocks leaves the main term (X/p+1)δ(p,r), a discrepancy at most a fixed-r constant times Xp^(−3/2)(1+log p)^(2r+1), and a remainder block of length at most p^r. For fixed r, the discrepancy sum divided by X tends to zero by the convergent integer tail. The remainder sum is ≤U^rπ(U)=O_r(X/log X), U=X^(1/(r+1)); the extra main-term units are negligible. Replacing δ(p,r) by 4^(−r) costs a vanishing reciprocal-square tail. Mertens then gives the single-branch fixed-band limsup

    4^(−r) log((r+2)/(r+1)).

One cannot sum these fixed-r estimates without a uniform tail. The separate elementary block estimate is ≤3(X/p)ρ_p^r, where ρ_p=(p+1)/(2p)≤2/3. Put J=floor(log X/(2 log 3))−2. For r≤J the lower endpoint is at least 9 and the Mertens error in a band is O((r+2)/log X). Summing against (2/3)^r makes that error vanish and leaves a convergent tail. For r>J, disjointness of the prime bands bounds the total by (2/3)^(J+1) times Σ_{p≤√X}1/p, which tends to zero. Fixed small primes, including 5 and 7, eventually occur in this deep tail. Thus the required order of limits, first X→∞ and then the depth cutoff→∞, is justified.

With S=Σ_{r≥1}4^(−r)log((r+2)/(r+1)), four branches give limsup E_small(X)/X≤4S. The current Lean source uses the relaxed full lower-half box with density 4^(−r)(1+1/p)^(2r). This is a legitimate enlargement, has the same fixed-r leading term, and changes only the vanishing reciprocal-square error. It does not require the exact-valuation deletion to be formalized into the Fourier box.

## Top prime classification and analytic summation

For large X, every top prime p>Y dividing L(x)=pc satisfies p/c>130 and p²>L(x). The least-digit formulas are then genuinely between 0 and p−1, so they can be compared with (p−1)/2 without an unmentioned wraparound. For P the possible numerator residues of 12c² modulo 7 are 3,5,6; only 3 survives, giving c≡3,4 modulo 7. For R the possible residues of 54c² modulo 14 are 6,10,12; only 6 survives, giving c≡5,9 modulo 14. For Q and S the differences from the lower-half threshold are respectively (p+41c+6)/6 and (p−43c)/6, both positive. They have no top events. The ratio hypothesis p/c>130 is essential and is preserved.

For the paper's divisor-switching argument, write L=Ax+d and Z=AX+d. The relation pc≡d modulo A forces both p,c to be units and p≡dc^(−1) modulo A. Among unit classes c modulo A, precisely one third pass the necessary cofactor restriction:

    P: A=222138, φ(A)=60480, allowed=20160
    R: A=148092, φ(A)=40320, allowed=13440.

Counting primes for each c≤Z/Y and applying the fixed-modulus AP prime theorem is valid because A is fixed. If the allowed cofactor set has density δ=|C|/A, partial summation of its counting function δu+O_A(1) gives

    Σ_allowed c≤Z/Y Li(Z/c)
      = δ Z log(log Z/log Y) + o(Z).

The counting-function error is O_A(Li(Z))=o(Z). Replacing Li(Z/t) by (Z/t)/log(Z/t) has integral error O(Z/log Y). The AP error sums to O_A(Z(1+log(Z/Y))exp(−κ_A√log Y))=o(Z). Dropping the lower prime cutoff costs at most (Z/Y)π(Y)=o(Z). After the factor 1/φ(A), and with Z/(AX)→1 and log Z/log Y→2, each surviving branch has limsup at most (1/3)log 2. Hence E_top has limsup at most (2/3)log 2.

Only qualitative PNT in each fixed AP is actually needed: after a fixed threshold, each prime-counting error is at most ε times its main scale, uniformly over the finitely many reduced classes. The total weighted main scale is O(Z), so taking limsup and then ε→0 proves the same bound. There is no need for uniformity in a growing modulus.

The current Lean file takes a simpler equivalent upper-bound route: the surviving cofactor classes imply p≡±1 modulo 7 for P and p≡±1 modulo 14 for R. Count at most X/p+1 parameters per branch prime, enlarge the upper endpoint to C₀X, and use Abel summation of AP prime reciprocals. Each of the four reduced classes contributes at most (1/6)log 2; the accumulated unit errors are O(π(C₀X))=o(X). `topAnalyticMajorant` and the closing theorems explicitly implement that route.

## Strict numerical margin and completion

The elementary expansion log((1+z)/(1−z))=2Σ_{j≥0}z^(2j+1)/(2j+1), for 0<z<1, gives a strict upper bound by retaining j=0,1 and bounding every remaining denominator below by 5. The six values at z=1/5,1/7,…,1/15 and the geometric tail from r=7 check exactly. The result is

    S < 11117760449158646497 / 89848527388139520000
    log 2 < 1123/1620
    4S+(2/3)log 2 < 21498408212212214497 / 22462131847034880000.

Subtracting the last rational from 2393/2500 gives

    2344391769572639 / 22462131847034880000 > 0.

Consequently limsup Bad(X)/X <2393/2500. Since Good(X)+Bad(X)=X, the lower density of Good is strictly greater than 107/2500. The positive, injective family bridge already checked above completes the original infinitude theorem. Finite observations are not being used to infer this density conclusion.

## Actual pinned imports and admitted declarations

The current [lake-manifest.json](https://github.com/williamjblair/lean-proofs/blob/f297d710018270c66b296082766334974260bcbc/lake-manifest.json) specifies:

- Lean toolchain v4.33.0
- Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`
- ajirving/PrimeNumberTheoremAnd `769d3b81fbff001d9fa7028df0168a8e546cf692`
- LeanArchitect `78dd66840d3efe8c824c699fc03381cec817c271`

The inherited July audit and `pntap_route.md` instead name AlexKontorovich/PrimeNumberTheoremAnd at `d7f9e2bfdcc7e34dfb9328b7494a6d424ff50c96`, Lean/Mathlib 4.29.x. That historical claimed replay is not evidence of replaying the actual current pin. The source-level statements remain appropriate at the actual pin.

The audit's assertion that only moduli 1,222138,148092 occur describes the paper route and an older analytic conjunction, but not the actual terminal implementation, which uses 1,7,14. `PNTAP.lean` proves the generic result for every fixed A>0, so this discrepancy leaves no missing hypothesis in the implementation's stated chain. `RequiredFixedModulusPNTAPInput` still packages the larger moduli, but it is not the exact list of current terminal uses.

Static retrieval covered all 74 Erdős-730 Lean files, two supplementary proof-route documents, the comparator configuration, the author CI configuration and resolved dependency manifest, nine PNT modules in the project-specific import closure, nine LeanArchitect modules, and PNT configuration/manifest files. The reachable nonstandard module graph from FullDensityTheorem has 52 modules: 34 local mathematical modules, nine PNT modules, and nine Architect modules. The unexpanded boundary is Lean, Mathlib, and Batteries. Thus this is not an audit of every declaration in the whole transitive standard-library closure.

In the actual pinned [Wiener.lean](https://github.com/ajirving/PrimeNumberTheoremAnd/blob/769d3b81fbff001d9fa7028df0168a8e546cf692/PrimeNumberTheoremAnd/Wiener.lean#L324-L382):

- `prelim_decay_2`, lines 324–326, has an explicit admitted proof.
- `prelim_decay_3`, lines 343–346, has an explicit admitted proof.
- `decay_alt`, lines 359–382, explicitly uses prelim_decay_3 at line 375.
- After stripping nested comments and strings, the gathered reachable mathematical source contains no other occurrence of any of those names. In particular decay_alt has no downstream textual reference, and the two admitted theorems carry blueprint metadata rather than simp/instance registrations.

The admitted declarations **are in the imported module closure**: FullDensityTheorem → its analytic range files → PNTAP → Consequences → Wiener. That fact alone does not put them in the terminal theorem's proof dependency cone. The inspected active PNT route is WeakPNT_AP → WienerIkeharaTheorem'' → WienerIkeharaTheorem' → the smooth/W21 route, whose decay estimate uses the Fourier identity for an actual twice-differentiable function rather than either admitted experiment. Consequences then converts the von-Mangoldt AP asymptotic to the weighted prime asymptotic, and the local PNTAP file uses Abel summation to obtain the ordinary AP count.

LeanArchitect includes a generic `sorry_using` tactic implementation that calls the meta-level primitive `g.admit` (Architect/Tactic.lean line 96). This is a capability definition, not an extra admitted mathematical theorem. No invocation of sorry_using was found in the gathered mathematical closure. Its blueprint `proofUses` strings are documentation metadata, not a substitute for proof-term dependency inspection.

The bounded lexical evidence therefore supports, but does not certify, exclusion of the two admissions from the actual theorem dependency cone. Automatic elaboration, implicit dependencies, generated proof terms, and the complete trusted-library boundary were not checked by a kernel. The author's `#print axioms` commands are retained source commands; their successful execution and alleged outputs were not reproduced here. A definitive formal acceptance requires a separately authorized clean replay against these exact pins and inspection of the elaborated terminal axiom footprint.

## Independent checks and stopping point

Historically, independently authored standard-library checks passed in normal, `-O`, and `-OO` modes with matching substantive results. They checked polynomial identities, coprimality, the exact transition criterion, p-adic digit counts, top-range classifications under their stated hypotheses, complete CRT counts, and exact rational bounds. Adversarial controls covered the p-adic unit, endpoint deletion, positive-index condition, distinction between prime support and valuation, and detection of admitted source declarations. These were diagnostics; no universal conclusion was inferred from finite samples. This edition omits their code, raw certificates, numerical toy cases, and finite-test ranges.

The complete mathematical audit is finished. Formal replay and independent Palomar acceptance remain unverified. Publication preparation performs byte, editorial-scope and addition-only integrity checks; it does not rerun the historical mathematical checker or execute any third-party source program.

## Review and publication notice

Acceptance here means unrefereed internal AI mathematical review of the written argument relative to its stated classical inputs. The separately authored FOCUSED_AUDIT.md independently checks the fixed-depth Fourier lemma and its first-power application, including the separate uniform depth tail; it is not a second audit of the entire theorem. No external human peer review, journal acceptance, kernel certification, current registry acceptance, exhaustive novelty search, or community-wide adjudication is claimed. The accepted result belongs to the prior work attributed above, with no claim of a new solution by this audit's authors.

The complete general mathematical argument, constants, limits, hypotheses, exceptional-prime treatment, provenance corrections and original-statement bridge above are retained. The only editorial removals are working-package coordination and finite-test details. This edition contains authored analysis and selected public verification metadata, not source documents, code, datasets or a runnable formalization.
