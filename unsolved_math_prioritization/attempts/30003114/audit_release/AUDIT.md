# Independent adversarial audit: problem 30003114

## Verdict and binding

**PASS FOR SCOPED PARTIALS. The intended uniform counting problem is not resolved.**

All five authored partial proofs were read completely and checked independently. No mandatory mathematical or source-metadata correction was found. This is an audit of a bounded five-approach research checkpoint, not a proof, disproof, novelty certificate, or exhaustive worldwide-status determination for the target.

The audited author archive is LITTLEWOOD_30003114_SAFE_PACKET.zip, 16,914 bytes, SHA-256 443d5dc030e08c32e7a758c0eb1f5ab63eb8673f0a4dfd13930f2a60f568f228. Its MANIFEST.json is 1,186 bytes, SHA-256 913457490b8f076c4a5035e6bcb32016a69dfe1a6c97a56ad396fc16882e23cf. The eight archived members matched the eight frozen directory files exactly. The freeze was not edited. No remote write or publication was performed.

## 1. What is, and is not, the target?

Write a=9/10, b=19/20, and let P_d be the ternary coefficient family of degree at most d. The audited formulation is

exists C>0, for every reduced p/q in [a,b], exists c_(p/q)>0, for every integer d>=1:

    #{P in P_d : |P(p/q)| < c_(p/q) exp(-Cd)} < exp(d/100).

C is independent of the rational parameter and d. The prefactor may depend on the parameter, but not d. All logarithms in the authored arguments are natural. Zero is one polynomial and is included. Leading zero coefficients do not create duplicate polynomials within a fixed coefficient-vector length.

The selected public dataset row, index 11898, has ID 30003114 and problem number OWR-14603-013. Its statement explicitly contains modulus bars and the correct closed interval, ternary family, exponential threshold, and counting exponent. Positivity of the prefactor is explicit in the author's survey, Question 4.13. The positive-degree convention is an openly stated intended interpretation: neither zero-prefactor triviality nor the d=0 strict-inequality defect is a substantive resolution.

The [OWR report, printed pp.1125-1126](https://publications.mfo.de/bitstream/handle/mfo/3525/OWR_2016_21.pdf?sequence=1) was independently downloaded and visually inspected. Its counting display omits bars, while the preceding minimum concerns modulus. The [survey, Question 4.13](https://arxiv.org/pdf/1608.04210v1) repeats the omission and explicitly requires a positive prefactor. The frozen packet correctly treats these as source issues, not counterexamples to the repaired dataset target.

In particular, the quantifiers cannot be exchanged to let C depend on q. A count cannot be replaced by a probability without multiplying by 3^(d+1). A root bound for one polynomial cannot bound the number of polynomials. A finite computation cannot settle all positive d. These distinctions are preserved in the freeze.

## 2. Arithmetic separation and bounded denominators: PASS

Every reduced rational in [a,b] has q>=10: for q<=9 its largest fraction below 1 is (q-1)/q<=8/9<a. For a nonzero integer polynomial R of actual degree r, the equation R(p/q)=0 would imply, after multiplication by q^r and reduction modulo q, q divides its leading coefficient. Coprimality of p and q is essential here.

For R=P-Q, the nonzero leading coefficient has magnitude at most 2. Hence evaluation on P_d is injective. Separately, q^d P(p/q) is an integer, giving |P(p/q)|>=q^(-d) for nonzero P. Injection into the integers in the open interval (-tq^d,tq^d) gives exactly the asserted bound

    N_d <= 2 ceil(tq^d)-1 <= 2tq^d+1.

This formula correctly handles integral endpoints and the zero polynomial. At q<=Q with Q>=10, Q^(-d)<=q^(-d); the strict threshold therefore counts only zero. Choosing C=log Q and c=1 proves the scoped bounded-denominator claim for all positive d.

The obstruction to extending this proof is correctly described: for q>exp(C), the factor exp((log q-C)d) grows, and no fixed positive parameter-dependent multiplier can suppress it for every d. This is a failure of the proposed estimate to prove the uniform target, not a counterexample to that target. The independent controls also demonstrate that injection would fail if q>2 were dropped, since at 1/2 the polynomials x and 1-x agree.

## 3. Lacunary conditioning: PASS

For L=22 the exact inequality 3*19^22<20^22 establishes gamma>0. Fixing coefficients outside J={0,22,...,22 floor(d/22)} leaves m=floor(d/22)+1 variable ternary digits.

In the difference of two distinct selected assignments, use the smallest nonzero exponent i. Its coefficient has magnitude at least 1. The remaining coefficients have magnitude at most 2, and their total contribution in absolute value is at most 2 lambda^(i+L)/(1-lambda^L). Thus the difference magnitude is at least

    lambda^i (1-3lambda^L)/(1-lambda^L) >= a^d gamma.

The direction of each inequality is correct: i<=d and 0<a<=lambda<1, while (1-3u)/(1-u) decreases for u<1. Two values in an open interval of radius t cannot have that separation if 2t<=a^d gamma. Each choice outside J therefore admits at most one counted selected assignment, proving N_d<=3^(d+1-m) for every real lambda in the interval and every d>=1 under the stated threshold.

The result is genuinely denominator-free, but its asymptotic count exponent is (21/22)log 3, not 1/100. The probability reformulation includes the complete normalization. Decreasing t without changing this conditioning argument does not by itself improve the count exponent.

The L=21 control rejects the required positivity of gamma. It should not be interpreted as a counterexample to a theorem whose threshold assumption has become empty. This is a scope clarification of the control, not a needed correction to Proposition 2.

## 4. Collision lower bound and necessary C: PASS

This was checked particularly carefully for ordered pairs, diagonal pairs, multiplicity, strict thresholds, and irrational versus rational parameters.

Put n=d+1 and M=2^n. Binary polynomial values lie in [0,T), T=1/(1-lambda), because the finite geometric sum is strictly below T. K=ceil(T/t) half-open bins cover this interval, with a shortened last bin allowed. Same-bin differences have absolute value strictly below t, including when t divides T or t>=T.

If m_j are occupancies, the number of ordered off-diagonal pairs in the same bin is sum m_j^2-M, which is at least M^2/K-M. This lower bound may be negative; that merely makes the subsequent bound weak, not invalid.

A fixed nonzero coefficient difference w has exactly 2^z ordered representations, where z is the number of its zero coordinates. The differing coordinates force their two bits, and each equal coordinate offers two choices. Since w is a nonzero vector, z<=n-1. Even if only some of its representations fall in the selected bins, the upper bound 2^(n-1) remains valid. Consequently

    nonzero counted polynomials >= 2^(n+1)/K - 2.

Adding zero and using K<=T/t+1 gives

    N_d(lambda,t) >= 2^(d+2)t/(T+t)-1.

The difference map must not be treated as injective: already for three bits there are 56 off-diagonal ordered pairs but only 26 nonzero ternary differences. The multiplicity bound is attained by a difference with one nonzero coordinate. Neither rational evaluation injection nor distinctness of binary values is required in this proof.

For the necessary exponent, fix lambda=9/10 and an arbitrary positive c. If 0<C<log 2-1/100, then t_d=c exp(-Cd)<=T eventually. The preceding inequality yields

    N_d >= (2c/T) exp((log 2-C)d)-1.

Its ratio to exp(d/100) tends to infinity, since log 2-C-1/100>0. This contradicts the target for that fixed parameter and every choice of positive c. Hence C>=log 2-1/100 is necessary. The equality case is not ruled out by this reasoning; the freeze does not claim otherwise. Nor does excluding this interval of constants disprove existence of a larger absolute C.

## 5. Jensen, Blaschke products, and Harnack localization: PASS

The analytic argument is valid for every nonzero ternary polynomial of degree at most d, with the origin factor, multiplicities, boundary roots, and no-root case treated as follows.

1. Write P=z^k f with f(0)=+1 or -1. The coefficients of f retain their bound. On |z|<=r=99/100, |f(z)|<=1/(1-r)=100=M. Removing the origin factor is indispensable; P=z^10000 is an immediate negative control for a zero count applied to P itself.

2. Jensen's formula gives sum_(|alpha|<r) log(r/|alpha|)<=log M, since log|f(0)|=0. Applying Jensen on radii below r and taking their limit also covers zeros on |z|=r. Each zero with |alpha|<=R=97/100 contributes at least log(r/R)>0. Thus their number, including multiplicity, is at most K=ceil(log M/log(r/R))=226. The exact rational inequalities (99/97)^225<100<(99/97)^226 independently certify that constant. In fact the integer count can be bounded by 225, but the weaker 226 is valid and needs no correction.

3. Form B from all these zeros, with each multiplicity repeated, using the factors r(z-alpha)/(r^2-conjugate(alpha)z). None has alpha=0. Its poles lie outside |z|=r and each factor has modulus 1 on that boundary. Division cancels the zeros of f, so g=f/B extends analytically to a neighborhood of the closed r-disk. Equivalently it is a polynomial quotient after exact factor cancellation times linear factors. The maximum principle gives |g|<=M throughout that disk. Also |B(0)| is a product of |alpha|/r<1, so |g(0)|>=1.

4. All zeros of g in |z|<R have been removed. Zeros with R<|z|<r may remain, which is why the Harnack disk is R, not r. h=log M-log|g| is nonnegative and harmonic on |z|<R. The needed harmonicity of log|g| follows locally from nonvanishing, or globally from an analytic logarithm on the disk. For x in [a,b], Harnack gives h(x)<=((R+x)/(R-x))h(0)<=96 log M. Therefore |g(x)|>=M^(1-96)=c0=100^(-95).

5. At real x<=b and for |alpha|<=R, the denominator in a Blaschke factor has modulus at most r^2+Rb. Thus each factor is at least A|x-alpha| in modulus, where A=r/(r^2+Rb)=2475/4754 lies strictly between 0 and 1. With delta=min(1,min|x-alpha|), all factors are at least A delta. For delta>0 and N<=K, their product is at least (A delta)^N>=(A delta)^K. If N=0, B=1 and delta=1, and the same weakened estimate remains valid. If delta=0, the desired lower bound is zero and is immediate; no division by delta is needed.

6. Finally x^k>=a^d, because k<=d. Hence |P(x)|>=a^d c0(A delta)^K. Omitting a^d is false: at x=a, P=x^10000 and delta=1, the exact rational comparison a^10000<c0 A^226 reverses that mutant bound.

For C>-log a, rearranging the established inequality under |P(x)|<c0 exp(-Cd) gives delta<A^(-1) exp(-(C+log a)d/K). Eventually the right side is below 1, so a selected root must exist at that distance. The sign of log a and the direction of this implication are correct.

The argument does not count how many distinct polynomials can have roots near the fixed rational point. Rationality rules out an exact nonzero-polynomial root, but does not in this proof yield a denominator-independent separation from roots of unbounded degree. The cited [Breuillard–Varjú Proposition 20 and Theorem 21](https://arxiv.org/pdf/1610.09154v3) have superexponential-scale hypotheses or bounds. In particular, exp(-Cn) eventually exceeds n^(-3n) for every fixed C. Their common-root conclusion cannot be imported at the required scale. The frozen gap statement is accurate.

## 6. Superincreasing products: PASS

If positive integer exponents satisfy m_j>sum_(i<j)m_i, the largest differing index in two subsets shows their sums cannot coincide. Expansion of F=product(1-x^m_j) therefore has one sign per subset sum, so its coefficients are ternary. Each factor has a simple zero at 1 and derivative -m_j there; F has multiplicity exactly s, with first nonzero Taylor coefficient (-1)^s product m_j.

The superincreasing condition gives m_j>=2^j>=j+1. For x in [a,b], all factors are positive. Integrating 1/(1-u) shows -log(1-u)<=u/(1-u) on [0,1). Hence

    -log F(x) <= sum_j x^m_j/(1-x^m_j)
              <= (1/(1-b)) sum_(j>=0) b^(j+1)
              = b/(1-b)^2 = 380.

This proves F(x)>=exp(-380) uniformly in the number of factors and their degrees. For x^k F of degree at most d, x^k>=a^d supplies the stated bound. The empty product also satisfies the claim, with multiplicity zero. The Thue–Morse choice has the claimed degree and multiplicity, but is only one structured family; no general counting conclusion follows.

The overlapping-exponent control (1-x)^2 produces coefficient -2. It demonstrates why unqualified product expansion is invalid, not that superincreasing is a necessary condition for every possible ternary product.

## 7. Independent execution and adversarial controls

The author's verify.py was run with Python optimization disabled, and its stdout was byte-for-byte identical to the frozen VERIFICATION.json. The replay is positive evidence about those exact finite tests only. The independently written verifier does not import the author's script or its functions; it uses a different Horner-recursion enumeration, explicit exceptions, exact integers and fractions, and no network.

The independent run passed:

- 314 rational polynomial families at 44 reduced rational parameters, totaling 314,862 polynomial evaluations and 1,884 threshold checks; all target rationals with q<=50 plus four larger-denominator examples, through degree 9 at the interval endpoints and degree 6 elsewhere.
- 63 collision-bound families on seven parameters, degrees 0 through 8, tested at 89,555 critical thresholds. Monotonicity of the right side and stepwise constancy of the count extend these particular finite-family checks to every positive threshold t; this does not extend their degree or parameter range.
- 86,870 ordered binary pairs for coefficient lengths 1 through 8, verifying every difference-vector multiplicity, plus 90 half-open bin partitions and their strict difference conditions.
- 17 selected-digit families with 4,443 assignments, reaching target degree 110. These are not enumeration of all polynomials through degree 110.
- Exact K, H, A and c0 calculations; 342 rational complex boundary identities and 114 Blaschke-factor distance bounds. These are algebraic controls, not a numerical proof of the imported analytic theorems.
- 46 superincreasing exponent sequences, including empty, dense and sparse examples, with exact Taylor-coefficient checks of multiplicity and the rational logarithmic majorant.
- Fourteen mathematical or proof-step negative controls, including the missing origin factor, incorrect Harnack radius, collision multiplicity, closed threshold, alphabet changes, and quantifier/probability conversion errors.
- Five integrity mutations on temporary copies: changed proof, missing file, extra source file, changed manifest, and symlink substitution. Each was rejected.

The new verifier rejects -O, -OO, or a nonzero PYTHONOPTIMIZE setting before performing the tests. An -O invocation and an environment-driven optimized invocation were tested solely as expected rejection controls; neither is counted as mathematical verification. A temporary author-script copy with its first gamma assertion deliberately reversed failed with AssertionError under ordinary Python. The frozen author copy was never changed.

Some negative controls reject a proof step or hypothesis rather than furnish a counterexample to the original target. In particular denominator dependence, gamma positivity, and probability normalization have exactly that narrower meaning. No test pass is used as an all-degree theorem or a claim of full resolution.

## 8. Source and publication-boundary audit

Four fresh complete PDF downloads exactly matched the frozen public metadata: OWR 729,321 bytes; survey 274,980 bytes; Breuillard–Varjú 395,346 bytes; Kittle–Kogler 933,316 bytes. Their complete SHA-256 identities, inspection scopes, and public links are in SOURCE_AUDIT.json. Relevant source passages were inspected as specified there; the complete external papers' proof systems were not audited.

The [Kittle–Kogler v4 source](https://arxiv.org/pdf/2409.18936v4), dated 17 October 2025 on arXiv, still gives a Mahler-measure-dependent sufficient condition for absolute continuity. For reduced p/q in (0,1), its primitive minimal polynomial is qx-p and its Mahler measure is q. Consequently this cited result does not establish the required denominator-independent finite count. No journal status is inferred beyond the displayed public metadata.

The freshly retrieved dataset row's HTTP response was 8,184 bytes with SHA-256 f95eff36f62c8b246ab4398aaa12b582021745040bbeb0fc1f32d22273d8b5eb. Serializing its parsed JSON with Python json.dumps produced the author's exact 8,774-byte record and SHA-256 cc8359d6b7c3ce8060e97be6a1d64661ab148e75085dd20d5bef9240aeaccfdd. The statement's UTF-8 hash was b757e2a4b80b706a2a1d6365f469e5c548c3f1bdd3ef00680d4ab36c1c6d766e. The author correctly labels its hash as serialization identity, not transport-byte identity.

The complete existing public catalog bytes were independently hashed: 21,735,099 bytes, SHA-256 891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566. Their Git blob SHA-1 bd5c23e4e6c7e1901717a7e596477a7f6dc72425 matched fresh GitHub metadata at the author's pinned commit. The target rank, statement hash, queued status and zero turns at that revision agree. This verifies that snapshot, not the future repository state.

The pinned public whole-corpus manifest was freshly read and its declared hashes and sizes corroborated. Neither problems.json nor research_results.json was downloaded or independently hash-verified by this auditor. A matching live row and catalog statement do not bind all current dataset-server bytes to the pinned dataset revision. Null research fields in this row do not prove the absence of a separate prior research record. The author's historical repository searches are not independently certified as executions; their explicit bounded-observation limitations are appropriate.

Both the author packet and this audit contain authored analysis, code, results and public verification metadata only. They contain no source PDFs, extracts, rendered pages, raw dataset records, private sources, private personal data, or private coordination. The safe-directory and archive allowlists were checked. Public filenames, titles, URLs, sizes, hashes and inspection descriptions are metadata, not bundled source content.

## 9. Required corrections and final disposition

**Mandatory corrections: none.** No author-file change is required to sustain the five stated partial results. The optional integer tightening K=225 and stronger verifier safeguards do not undermine the frozen K=226 proof or its successful assertion-enabled replay.

The final disposition remains five substantive approaches completed, intended problem unresolved, no verified counterexample to its repaired statement, no verified prior resolution, and no novelty claim. The exact open requirement is an upper count below exp(d/100) at one denominator-independent exponential scale for every rational parameter in the closed interval, allowing only a positive parameter-dependent prefactor.
