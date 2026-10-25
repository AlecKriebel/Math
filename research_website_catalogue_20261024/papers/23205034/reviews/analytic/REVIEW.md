# Independent analytic review — Zenodo 23205034

**Verdict: the sparse and represented-field reductions are supported; the unconditional corollary retains an unresolved upstream verification dependency.** I found no substantive mathematical defect in the paper's new sparse reduction, its signed characteristic-p descent, or the dense-to-prime-field reduction. I do not certify the separate upstream prime-field factorization breakthrough or its general cyclotomic Hecke zero-free input. Their published theorem statements have the required scope, but posting them and citing prior automated audits do not establish their correctness.

The strongest independently reconstructed result is **Theorem 1 as a deterministic, output-sensitive reduction to dense factorization**, with its stated input model, arbitrary binary multiplicities, at most 2b dense calls, and polynomial nonoracle bit cost in t,b,D,m,L. The resulting reduction to prime-field factorization and the prescribed-degree construction implication are also supported at the stated oracle level. Corollary 3 follows if the cited prime-field algorithm is valid; that additional premise has not been independently discharged by this review.

This is an AI mathematical review, not human peer review, formal verification, or a novelty certificate. No repair was made. All work remained in this review folder, with no website, spreadsheet, Git, publication or outreach action.

## 1. Exact reviewed publication and independence

- Title: *Output-sensitive sparse factorization over finite fields from dense factorization*.
- Author: Alec Kriebel; PDF and record publication date 2026-10-06. The acquired record metadata has no explicit version value.
- Record: <https://zenodo.org/records/23205034>; DOI <https://doi.org/10.5281/zenodo.23205034>.
- Published `paper.pdf`: 104,276 bytes, **9 pages**, SHA256 `6e04d462b5229ad310558afd868f21666377e7b5136fad514a7752b20ea4ea10`, MD5 `bc9914adad331e615df675b0aadb28f9`.
- Published `verification.zip`: 291,388 bytes, SHA256 `96c4bdf7d2944b8e741fefa0fad6c112b25672af700ef5aa837e61353ef5ba68`, MD5 `6cd353daffda25a73949d5324eae069c`.
- The PDF embedded in `published-source/manuscript/paper.pdf` is byte-identical to the freshly acquired primary PDF.
- `manuscript/main.tex` SHA256: `fbabb3ecaf36fa49416e6b7c0bbc32e73be26902bda9d66e9f85228ef6733d58`.
- Authored `SPARSE_CANDIDATE_DERIVATION.md` SHA256: `d67ab2e57978ebadb5b43a80523fba38d2843e301edaad57fe6a173713f67ce5`.

All file lengths, SHA256 values and Zenodo MD5 values were checked against the fresh acquisition receipt. The complete nine-page publication and full authored sparse derivation were read. I independently reconstructed the mathematical reduction before using archived mathematical fixtures for replay. I read the core sparse and dense implementations, their tests, the construction example implementation and reproduction runner. Additional mathematical checkers were inspected for imports and side effects before their clean replay; replay does not mean I independently reconstructed every auxiliary checker or every upstream proof that it purports to corroborate.

I did not read sibling reports or archived reviewer opinions. Historical status/audit assertions embedded in the manuscript, authored candidate derivation and code documentation were not used as evidence of correctness. The runner hashes the frozen fileset and compares regenerated mathematical fixtures; neither operation imports a reviewer verdict into this review. The supplemental historical priority and analytic/geometric review narratives were not consulted.

## 2. Exact claim and output model

The base field is explicitly represented as `K=F_p[T]/(h)`, where p is a binary prime, `L=ceil(log_2 p)`, h is monic irreducible of positive degree m, and elements have m canonical prime-field coordinates. Primality and irreducibility may be promised; the paper also explains a deterministic check for h. A field cardinality without a defining polynomial is not the input model.

The sparse input is a nonzero `f=sum_(i=1)^t a_i X^(n_i)`, with distinct nonnegative binary exponents and nonzero coefficients. Put `N=max n_i` and `b=max(1,ceil(log_2(N+1)))`. The output consists of the leading coefficient and **all distinct monic irreducible factors represented densely**, each with its positive binary multiplicity. Let `D=sum_g deg(g)` be the unweighted total degree of these distinct factors.

The claim is polynomial in t,b,D,m,L, not in the number of nonzero terms of the output factors. It is not a polynomial-time routine for producing just one small factor while ignoring a potentially huge remaining output. A squarefree sparse polynomial can have D=N; that case carries no sublinear-in-N promise. Repeated factors can make N exponentially larger than D, which is the regime addressed by the compressed descent.

Theorem 1 asserts at most 2b calls to complete dense factorization over K, each of degree at most `(b+1)D`, with polynomial nonoracle bit cost. Using the direct prime-Frobenius reduction, at most `2b(b+1)D` prime-field calls of that same maximum degree suffice. Constants and monomials require none. Zero is rejected, rather than assigned a nonexistent finite unique factorization.

Theorem 2 is the established dense reduction: a degree-n input over represented K reduces to at most mn prime-field calls in the trace version, or n in the direct prime-Frobenius version, each of degree at most n; sums of queried degrees are bounded by mn² and n² respectively. It does not supply the prime-field algorithm by itself.

For irreducible construction, the requested degree d can be encoded in binary, but the output is dense and contains d+1 coefficients. The cost is polynomial in numeric d, m and L. A polynomial-in-log(d) construction is not asserted. The same numeric-degree restriction applies to the optional extraction of roots of `X^r-a`.

## 3. Independent reconstruction of the sparse reduction

### 3.1 Exact multiplicity of a known nonzero factor

For monic irreducible `g!=X` of degree delta, the formal root alpha in `E=K[Z]/(g)` is nonzero. Finite fields are perfect, so g is separable and `alpha*g'(alpha)!=0`. Consequently its exponent in f equals the order at Y=0 of

`sum_i (a_i alpha^(n_i))(1+Y)^(n_i)`.

The actual integer n_i must be retained even though a powering subroutine may reduce exponents internally when evaluating alpha^n. Replacing n_i by their residues modulo alpha's multiplicative order changes the polynomial in Y and destroys multiplicity information.

At each node, split n=pq+r into the occupied residues only. The polynomial is `sum_r (1+Y)^r H_r(Y^p)`. Each child is nonzero: its exponents q are distinct within a residue bucket, and substitution by 1+Y is injective. If the child's first nonzero term is `(nu_r,c_r)`, take v=min nu_r and form `P(Y)=sum_(nu_r=v)c_r(1+Y)^r`.

For s active distinct residues, the first s binomial coefficient columns are invertible. Indeed the column polynomials `binom(r,j)` have degrees j and leading coefficients 1/j!, with all j<p. Their evaluation determinant is a nonzero Vandermonde times the invertible factorial denominators. Thus P's first nonzero coefficient has j<s<=p. Inactive children start at order at least p(v+1), whereas pv+j<p(v+1). The parent's first term is exactly `(pv+j,P_j)`. A one-term node is a nonzero constant at Y=0 and terminates.

This proves both the valuation algorithm and `e_g(f) mod p <= t-1`. For X the valuation is simply the smallest input exponent. No degree-N expansion, full p-residue scan, or root enumeration is involved.

The explicit stack has at most b digit levels and t(b+1) occupied nodes. At each level the supports partition the original t terms, so the sum of squared support sizes over all levels is at most t²(b+1). Initial alpha powers cost O(tb) quotient-field multiplications, and subsequent work uses O(t²(b+1)) additions/prime-scalar operations. Dimension delta over K gives the conservative polynomial bound stated in the paper. Every binomial recurrence denominator is below p and invertible; p need not fit a machine word.

### 3.2 Visible factors and the exact Padé stopping certificate

After removing X, assume U(0)!=0. Local expansion at a root of a separable irreducible g shows that U'/U has a genuine simple pole precisely when e_U(g) is nonzero modulo p. Therefore the reduced denominator G is the squarefree product of exactly these visible factors. Contributions from different factors cannot cancel the pole at a root of g, and deg(P)<deg(G) in the reduced fraction P/G.

For B=1,2,4,..., series division computes the first 2B coefficients of U'/U from U's coefficients through index 2B. The B constraints, together with Q(0)=1 and deg(Q)<=B, seek A of degree below B such that the initial series of Q(U'/U)-A vanishes through degree 2B−1.

When B>=deg(G), normalized G is a solution. For any solution, AG−PQ vanishes to order at least 2B but has degree below 2B, hence is zero. For earlier B, the algorithm accepts only after checking the **full sparse polynomial identity** `U'Q=UA`; a long zero Taylor prefix is insufficient. Each product has at most t(B+1) terms before combination, with binary exponents, so the certificate is output-polynomial even when N is huge.

After acceptance, gcd cancellation and monic normalization recover the unique reduced denominator. Doubling stops by `B<=2 max(1,deg G)`. If U'=0, the result is G=1. The denominator is then factored densely and exact multiplicities are determined by the preceding valuation routine.

### 3.3 Polynomial rational representation, carries, and scalar roots

Maintain a polynomial F=U/V with U sparse, V dense, V|U, and nonzero constant terms. Initially U=f/X^a, V=1, and the X multiplicity a is stored separately.

Define the dense residue products

`A_U=product_g g^(e_U(g) mod p)`, `A_V=product_g g^(e_V(g) mod p)`.

Visible-factor discovery supplies precisely the nonzero residues needed for A_U; dense factorization supplies those for V. Since K is perfect, there are unique polynomial pth roots, including their scalar units, in

`U=A_U H_U^p`, `V=A_V H_V^p`.

Because e_U>=e_V, the difference of their floor-divided exponents is nonnegative. Thus `H=H_U/H_V` is a polynomial. If a factor is absent from F, its U and V multiplicities agree and it is absent from H as well; hence radical(H) is contained in radical(F).

It would be wrong to replace H's exponent by `floor(e_F/p)`. For example, at p=2, e_U=2 and e_V=1 give e_F=1 but e_H=1; the signed residue is −1, and `1=-1+2*1`. The manuscript explicitly keeps this carry, rather than making the invalid floor simplification.

Let C0 keep the coefficients at exponents divisible by p and divide those exponents by p. With sigma denoting coefficient Frobenius,

`C0(A_U H_U^p)=C0(A_U) sigma(H_U)`.

This follows directly by expanding the product: the H_U^p exponents are multiples of p. Applying inverse coefficient Frobenius to **both** sections gives

`U_new=sigma^(-1) C0(U)`, `W=sigma^(-1) C0(A_U)`, `V_new=W H_V`.

Then U_new/V_new=H and V_new divides U_new. Both constant terms remain nonzero. Coefficient copying would be correct only over the prime field; the inverse Frobenius is essential over a nontrivial extension and is present in both the proof and implementation.

### 3.4 Denominator bound, stopping, and signed factor ledger

Write v=deg(V) and D_F for the radical degree of F. Because U=FV,

`D_U <= D_F+v`.

The residue-product and section bounds give

`deg(V_new) <= (deg(A_U)+deg(V))/p`
`<= ((p-1)(D_F+v)+v)/p <= v+D_F`.

Since radical(H) is contained in radical(F), D_F never exceeds the original output radical degree D. Induction yields v<=kD after k descents. The sharper residue bound `deg(A_U)<=min(p-1,t-1)D_U` makes its dense construction polynomial in the sparse term count and radical degree, without a numeric-p loop.

The numerator retains at most t terms and its degree is at most floor(deg(U)/p) after each step. This proves termination in at most b descents. It is the numerator degree that shrinks; F's degree need not shrink by p because of carries. A constant terminal numerator forces a constant denominator by divisibility.

For every g, the exact multiplicity recurrence is

`e_F(g)=(e_U(g) mod p-e_V(g) mod p)+p e_H(g)`.

Adding p^k times the signed residue at level k telescopes to the original multiplicity. Intermediate factors may be foreign to the original f and must cancel. The paper's F2 example `U=X^3+X^2+1` correctly introduces `W=X+1`, although X+1 does not divide U. Final zero entries are removed; positive entries and the original leading coefficient give the output. No intermediate unit is silently assumed to be 1.

### 3.5 Bit accounting and output sensitivity

At level k<b, the two dense oracle degrees are at most `(k+1)D` and kD. Their aggregate degree is O(b²D). Applying the direct prime-fixed-algebra reduction therefore gives the stated loose bound of `2b(b+1)D` prime calls, each of degree at most `(b+1)D`.

The remaining representations have polynomial size:

| Object | Bound relevant to bit cost |
|---|---|
| Sparse numerator | At most t terms; binary exponents no larger than original N |
| Dense denominator | Degree at most kD |
| Padé augmented system | O((b+1)D) rows and columns over K |
| Known-factor quotient | At most `(b+1)D` coordinates over K |
| Dense residue product | Degree at most `(t-1)(b+1)D` |
| Field element | m coordinates, each of L bits |
| Coefficient inverse Frobenius | Binary exponent `p^(m-1)`, of O(mL) bits |
| Final multiplicity | At most N, hence O(b) bits |
| Signed ledger / final unused weight | O(b+L+log(b+1)) bits suffice |

The last weight bound is not obtained by pretending that p^b always has O(b) bits. If a level is actually reached, the shrinking numerator implies `p^k<=N`; the final unused multiplication can add L bits. Individual weighted contributions are bounded by polynomial multiples of N and the O(b) levels add only logarithmic overhead.

Gaussian elimination, schoolbook field/polynomial arithmetic, binary powering and deterministic exponent sorting are polynomial in these dimensions. Taking `M=1+t+b+D+m+L`, the displayed Padé and quotient dimensions are O(M²), residue degrees O(M³), and a K operation has the conservative O(m²(L+1)³) bit cost. Direct substitution into the paper's field-operation counts leaves ample fixed-polynomial slack for the stated O(M^24) nonoracle bound. This review supports the polynomial claim and the advertised conservative accounting; it is not a formally verified machine-instruction count or a practical runtime benchmark.

The optional certificate is valid without expansion: check that returned factors are distinct, monic and irreducible, verify each exact original-input valuation, verify `sum e_g deg(g)=N`, and use the original leading coefficient. Unique factorization and degree equality establish completeness. The dense helper that expands powers is correctly not used for huge sparse multiplicities.

## 4. Dense reduction and prescribed-degree construction

For a squarefree degree-u input, CRT identifies `K[X]/(f)` with a product of finite fields. The q=p^m fixed algebra is K^s, with s the number of irreducible components. It is computed by K-linear algebra. For a basis b_i, the elements

`c_ij=sum_(k=0)^(m-1) (t^j b_i)^(p^k)`

are quotient-algebra traces into the prime-field components. They are not coefficientwise traces of arbitrary quotient elements. The trace pairing detects any nonzero component difference: multiplication by that difference is bijective, and the trace map is nonzero as a polynomial of degree p^(m−1)<p^m. This remains valid when p divides m, even though Tr(1) may vanish. Testing all power-basis coordinates t^j is essential.

Each c_ij has minimal polynomial equal to the product of the distinct linear factors from its prime-field component values. Computing the first linear dependence over K gives that same polynomial, with coefficients lying in the canonical F_p. A complete prime-field factorization oracle gives its roots, and gcd refinements separate component supports. There are at most ms calls of degree at most s.

The alternative uses p-Frobenius as an **F_p-linear** map on the um-dimensional space. Its fixed algebra is F_p^s and has s basis vectors, so only s prime calls are required. Treating this map as K-linear would be wrong; the paper does not do so. In either variant a basis separates coordinate pairs, so the final blocks are irreducible.

The squarefree recursion handles multiplicities not divisible by p through ordinary gcd steps, and sends the remaining derivative-zero part through coefficientwise inverse Frobenius. Its dense numeric-degree loops are legitimate because n is dense input size. Disjoint emitted supports and sums of degrees at most n give the stated aggregate oracle bounds. The check for h uses successive Frobenius powers and gcd tests through m/2, so it does not require factoring p−1 or even factoring the integer m.

The prescribed-degree lift is also correct: an irreducible prime-field polynomial of degree md has a p-Frobenius orbit of size md. The p^m action has orbits of size d, so its factors over K all have degree d. Selecting the lexicographically first factor gives a deterministic output when the input prime constructor and factorization oracle are deterministic. No explicit isomorphism or primitive root is needed.

The primary Shoup reduction was checked visually in the original author manuscript, pp. 2–10, particularly Theorem 3.1 and the paragraph after Theorem 4.1. Theorem 3.1 is polynomial in numeric degree and log p with a factorization oracle. Theorem 4.1's displayed instantiated bound contains a p^(1/2) factor; its accompanying text supplies the oracle-reduction implication used here. The distinction is not lost in this review.

The paper's coarse construction ledger is consistent with that proof. Trial division factors the numeric output degree N; a prime q|N needs a degree-at-most-q−1 cyclotomic factor and at most O(NL) successive q-root steps, with queried degrees at most N². Summing over at most O(log(N+1)) distinct prime divisors gives the claimed loose call bound. Artin–Schreier towers handle q=p, and the 2-power branch has the necessary quadratic-extension exception. None requires arbitrary binary integer factorization. The supplied constructor program implements selected examples and fixtures, not every branch of a universal constructor.

## 5. Primary imports and the unresolved unconditional premise

The primary sources actually checked were:

- [Mattarei, Theorem 2, arXiv v2](https://arxiv.org/html/math/0512239v2): its base-p digit-product lower bound on polynomial weight implies the residue multiplicity bound used here. The constructive trie is justified independently above; it is not assumed merely from the citation.
- [Rowland–Yassawi, Proposition 1.9](https://arxiv.org/pdf/1310.8635): the cited pull-out mechanism is classical. Over K rather than F_p, the coefficient Frobenius in the present identity must be retained; the direct coefficient proof and F9 controls verify it.
- [Shoup's original author manuscript](https://shoup.net/papers/detirred.pdf): the needed construction-to-factorization reduction and its degree/representation scope were read from rendered pages because the PDF text encoding is corrupt. Its SHA256 is `00590fb8f0717338530b067626428781991edb840fb74c37cf846f07f50e0644`.
- [Rai, Algorithm 2 and Theorem 4.1](https://arxiv.org/html/2410.04071v1): the degree-md lift and lexicographic factor selection are already explicit there. Rai's own oracle instantiation is randomized/pseudo-deterministic; the lift itself becomes deterministic with deterministic subroutines. This is not an import of an unconditional deterministic oracle from Rai.

The Padé/logarithmic-derivative and dense fixed-algebra arguments were reconstructed directly. This is not an exhaustive priority review of all the paper's background references, and no firstness conclusion is drawn.

The exact pinned upstream inputs were freshly retrieved from commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`:

| Input | SHA256 | Pages | Fresh review scope |
|---|---|---:|---|
| [Prime-field factorization manuscript](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Deterministic-Polynomial-Factorization-over-Prime-Fields-October-4-2026/Deterministic-Polynomial-Factorization-over-Prime-Fields.pdf) | `ed88aa5ba802311a21c4f265bcef43515a16019f4b5afdd7f52ecbd36ce0204d` | 48 | Exact Theorems 1.1/1.2; model and dependency diagram; Section 10 cost interface; Section 11 auxiliary-prime implication; a limited sample of Section 6 geometry |
| [Primitive-root / general Hecke manuscript](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Primitive-roots-for-every-admissible-integer-base-October-4-2026/primitive-roots-all-integer-bases.pdf) | `671ac4b3ece879f614ed8f4b782e61a07805e533f385a694fe4d7afbda3c9365` | 92 | Exact Theorem 1.2, its field/character/height quantifiers, and introduction/dependency description; not a full reconstruction of its analytic proof |

The first states precisely the dense prime-field theorem needed here, including the fixed exponent 10^12 and binary characteristic. Its intermediate reduction instead depends on the **numeric** largest auxiliary prime E. Section 11 uses the second manuscript's general cyclotomic Hecke strip, abelian zeta factorization and a smoothed explicit formula to bound E by a fixed power of B. I checked that conditional implication: the field/discriminant bounds, strip-width exponent margin, cancellation of completely split prime contributions and upward search are compatible with polynomial dependence. An unknown absolute search constant is not a uniformity obstruction because the algorithm searches until a prime is found.

The second input's exact scope is essential: every finite-order Hecke character over every cyclotomic field containing mu_12, with no conductor or height cutoff. A Dirichlet-only or fixed Eisenstein-field result does not justify the varying-field application. **I have not independently validated the full theta/reflection/Poisson/Mellin proof of that theorem or all norm/divisor/splitting steps of the 48-page prime-field algorithm.** Finite local checks are not substitutes.

The [pinned repository README](https://raw.githubusercontent.com/openai/math/adc7f1241b42e322a6451854ab7e4b4c146bf78a/README.md) expressly says that verification stages vary and unformalized results may contain issues. The pinned formalization catalogue has no matching main-result entries for these two manuscript titles; that catalogue search is not proof of absence throughout the repository. No relevant Lean build was reproduced. Historical automated audit assertions in the paper were not independently verified.

Accordingly, the reference statements match the desired premises, but their posting status does not warrant an unqualified import of correctness in this review. **The unconditional Corollary 3 remains dependent on those unresolved upstream proof obligations.** This is a precise review/certification gap, not a demonstrated false theorem, a discovered counterexample, or an assertion that the upstream proofs contain an error.

## 6. Fresh reproduction and independent controls

The published `code/reproduce.py` was run with the current `PUBLICATION_FILESET.json` and an explicit receipt destination inside this review folder. Its source hash checks passed. It copied the frozen package to a temporary directory, removed generated fixtures, regenerated them and compared mathematical data. No published input file was rewritten. The full replay passed:

- Dense unit tests, including 377 exhaustive small monic inputs compared to trial division.
- Dense examples, the independent prime-Frobenius implementation, and 346 direct/trace comparison cases.
- Regenerated construction examples and the coherence negative control.
- Three finite auxiliary-source checkers. Their local numerical/algebraic checks do not validate either full upstream theorem.
- All seven sparse test families, including 960 small monic comparisons, enormous binary multiplicities, signed cancellations, extension coefficients and false Padé prefixes.
- Five independently authored supplemental sparse checker programs, whose generated mathematical fixtures matched the frozen package. The allowed Python-version difference was recorded explicitly.

No PDF build or upstream huge-prime algorithm execution was performed. The bundled prime oracle enumerates F_p and has a size cap; it is appropriate only for its small fixtures and is not polynomial in log p. Some construction examples use a fixed table; those are fixtures, not a universal construction algorithm. This limitation is disclosed in the code and paper.

My fresh `independent_controls.py` passed **63,949 exact assertions in 22 families**. The implementation under test is explicitly separated from the truth calculations. The latter use separately written integer polynomial arithmetic/trial division and an explicit F9 model; no old checker was imported. The controls include:

1. **532** complete sparse factorizations compared with independent trial factorization over F2, F3 and F5, and **975** known-factor valuations compared with repeated polynomial division.
2. **26,265** integer multiplicity pairs covering carries, signed residues and radical containment for p=2,3,5,11,101. The naive `floor(e_F/p)` mutation is explicitly refuted.
3. **1,275** direct Cartier steps on arbitrary quotients with V|U, checking the section identity, new divisibility, denominator bound and numerator shrinkage.
4. Binary-large characteristic p=2^127−1, with **12-term** inputs, D=2, exponents up to **1,016 bits**, and exactly 2,4,9 descent levels. A deliberately failing prime oracle ensured these known one-factor fixtures did not hide numeric-p enumeration.
5. Independent F9 arithmetic checking coefficient inverse Frobenius and known sparse factorizations with non-prime-field scalar units, including 48-bit exponents.
6. Rejection of a long false Padé prefix, and retention of integer exponent information for a factor of multiplicity 1024 at alpha=1.

These are finite exact controls, not universal complexity tests or mathematical proof certificates. Assertion counts describe parameter instances, not independent discoveries. The universal reduction is supported by the analytic argument reconstructed above.

## 7. Strongest result, exact gap, and disposition

**Strongest verified result:** complete sparse factorization with dense distinct-factor output and binary multiplicities reduces deterministically to complete dense factorization with the stated O(b) call count, O(bD) maximum degree, O(b²D) aggregate degree and polynomial bit overhead. The proof handles all multiplicities, extension-field Frobenius, nonmonic units, X factors, constants, signed foreign-factor cancellation and arbitrary binary exponents. The dense-to-prime-field and construction reductions are supported as oracle implications.

**Identified reduction defects:** none. No counterexample to the exact hypotheses was found, and no repair was attempted.

**Exact remaining gap:** this review does not discharge the complete correctness of the pinned 48-page upstream prime-field algorithm or the 92-page manuscript's general-cyclotomic Hecke zero-free theorem. Thus it does not certify the paper's unconditional polynomial-time conclusion. It also does not establish novelty, historical firstness, practical efficiency, formal verification or human peer review.

**Disposition:** the reduction can be described as a checked, unrefereed, AI-assisted output-sensitive reduction. Any public description of unconditional deterministic polynomial factorization must retain the explicit upstream dependency and its unresolved verification status; this review does not authorize an unqualified unconditional headline. No external contact or publication change was made.

Evidence includes `source_identity.json`, `inspected_source_hashes.json`, `reference_receipts.json`, `published_reproduction.json`, the fresh control source/result, `verdict.json` and the timestamped research log. Downloaded reference PDFs/rendered images and copied execution modules are ignored locally; their URLs, hashes and proof notes are retained.
