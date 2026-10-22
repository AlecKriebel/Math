# Independent audit: bounded-polynomial partial sums

Problem identification: rank 1032; problem 2304003; AMR-022-4003.

Audit date: 2026-10-08 UTC.

## Disposition

**ACCEPTED AS PARTIAL PROGRESS; ORIGINAL QUESTION UNRESOLVED.**

The five mathematical approaches in the frozen report are valid with its stated conventions. No mathematical correction or change to the frozen package is required. There is no demonstrated general sharp growth law for naturally ordered, arbitrary-support term-count truncations, no general exact degree-bounded formula, and no novelty certification. Literature retrieval, software checks, and packaging do not add mathematical approaches.

The accepted snapshot is the archive with SHA-256 `0e66432923a00ba78a2926096779430a0bbfb630edfcf299fcc20e77c6417989` and 15,909 bytes. Its twelve regular-file members were independently compared byte-for-byte with the supplied public and external files. Original files and the archive were preserved.

The results accepted are:

- `C(N,k) <= [k+sqrt(k(N-k)(N-1))]/N` for `1<=k<N`, and `C_N <= (1+sqrt(N))/2`.
- `C_N >= log(N)/pi - O(1)`.
- `A(d,k) = log(min(k,d-k))/pi + O(1)` uniformly for `1<=k<d`; `A(d,d)=1`.
- `A(3,2)=2/sqrt(3)`, and the same value for an arithmetic-progression triple of fixed exponents.
- `U_N` has square-root order. That assertion does not supply a square-root lower bound for `C_N`.

The sole software caveat found is diagnostic: sufficiently deep JSON nesting exits nonzero without success output but produces a Python recursion traceback instead of a structured JSON error. This is fail-closed under the documented nonzero-exit contract and does not require changing the accepted bytes.

## 1. Definitions, endpoints, and approximation issues

The report keeps three genuinely different objects separate: `A(d,k)` permits zero coefficients in `d` consecutive slots; `C(N,k)` has exactly `N` nonzero terms on increasing nonnegative integer exponents, with no degree bound; `U_N` permits an arbitrary selected subset. In particular, the largest exponent cannot be replaced by `N-1`. None of the supplied degree-bounded arguments makes that substitution.

For a fixed finite support, every coefficient has magnitude at most the circle norm, by Fourier coefficient extraction. Thus its norm unit ball is closed and bounded in finite-dimensional coefficient space. The dense problem has a maximum. The variable-support term-count problem is correctly stated using a supremum; no unsupported global compactness claim appears.

For a fixed support and a fixed cut, allow zero coefficients temporarily. Fill only zero slots with coefficients tending to zero and divide by `max(1, ||P_epsilon||)`. Uniform convergence on the circle gives convergence both of the full polynomial and of the retained polynomial. The support slots on each side of the cut remain fixed, all resulting coefficients can be chosen nonzero, and the limiting objective is unchanged. This proves the report's nonzero-coefficient approximation assertion. It also justifies padding a construction by tiny new terms: adding `h` new coefficients of magnitude at most epsilon increases the norm by at most `h epsilon`; scaling by `1+h epsilon` is enough.

To reduce complex coefficients to real coefficients, select a point `zeta` maximizing the retained modulus and replace the polynomial by `eta P(zeta z)` with unimodular eta making that retained value nonnegative real. Averaging this new polynomial with its coefficientwise conjugate preserves that value at 1 and does not increase the circle norm. Any vanished coefficients are restored by the preceding approximation. The reverse inequality is automatic since real coefficients are a subclass. This concerns the full circle norm, not the norm on the real interval.

The maximum principle transfers all the polynomial norms between the circle and closed disk. The empty cut has value zero. A complete cut has supremum one; a first-coefficient/first-term cut also has supremum one, since its coefficient is bounded by one and the other coefficients can tend to zero. Thus the boundary cases `d=1`, `N=1`, `k=1`, and `k=d` or `k=N` cause no singular formulas. Outside the disk there is no uniform exponent-independent bound even for one term, as the report correctly warns.

## 2. Approach 1: coefficient energy

At a circle point let the retained and omitted sums be `A` and `B`, with `k` and `l=N-k` terms. Cauchy-Schwarz applied separately to the two disjoint coefficient sets gives

    |A|^2/k + |B|^2/l <= sum |a_j|^2 <= 1.

The last inequality follows from Parseval and the uniform bound. The reverse triangle inequality gives `|B| >= max(|A|-1,0)` because `|A+B|<=1`. For `x=|A|>=1`, clearing positive denominators yields

    N x^2 - 2 k x + k(1-l) <= 0.

Its reduced discriminant is `k*l*(N-1)`; the larger root is the claimed expression. That root is at least one because `k*(N-1)-l = N*(k-1)>=0`, so the argument also covers `x<1`. No ordering hypothesis was used.

Writing `t=k/N` and `u=2t-1` gives

    2R-1 = u + sqrt(N-1)*sqrt(1-u^2) <= sqrt(N).

The last inequality is ordinary two-dimensional Cauchy-Schwarz. Complete and empty cuts satisfy the same global upper bound separately. Maximizing over integer cuts is bounded by this continuous optimization, without any claim that the relaxed bound is sharp.

**Audit result:** correct for arbitrary support and arbitrary subsets; insufficient by itself to detect exponent ordering.

## 3. Approach 2: analytic kernel and strict finite-degree gap

Set `c_j=binom(2j,j)/4^j` and `Q_r=sum_{j=0}^r c_j z^j`. Squaring the binomial series proves that the coefficient of `z^j` in `Q_r^2` is one whenever `0<=j<=r`. In the circle integral of `P(z) z^(-r) Q_r(z)^2`, the constant term pairs `a_j` with the coefficient indexed by `r-j`. Since P has no negative exponents, exactly `0<=j<=r` contributes. The use of a square rather than an absolute square inside this integral is intentional and correct.

Taking absolute values gives the weighted integral bound by `integral |Q_r|^2`, which equals `G_r=sum c_j^2`. Rotating the variable extends the estimate from evaluation at 1 to the whole retained-polynomial norm. The Stirling expansion `c_j^2=1/(pi*j)+O(j^-2)` has summable remainder, giving an absolute, parameter-independent additive constant in `G_r=log(r+1)/pi+O(1)`.

For `r>=1`, equality in the final bound forces `|P|=1` wherever `Q_r` does not vanish on the circle. There are at most finitely many exceptional points; continuity gives `|P|=1` everywhere. If a polynomial has different lowest and highest nonzero exponents `a<b`, the Fourier coefficient of `|P|^2` at `b-a` is the single nonzero product of those extreme coefficients. Constant modulus therefore forces a monomial. A norm-one monomial gives retained value at most one, whereas `G_r>1`. Since the finite-dimensional dense extremum is attained, its value is strictly below `G_r` for every fixed finite d and `k=r+1>=2`. This proves strictness without asserting a d-uniform positive gap.

The reversed polynomial `z^(d-1) P(1/z)` is analytic with reversed coefficients and the same circle norm. Its first `l=d-k` slots bound the omitted tail by `G_(l-1)`. The triangle inequality for retained sum = full sum minus tail yields the second upper bound `1+G_(l-1)`. The retained-side bound is `G_(k-1)`. The indices and the restriction `k<d` are correct.

For arbitrary sparse support, the argument instead depends on an exponent cutoff after removing an initial monomial factor. It gives no replacement of that cutoff by the number of nonzero retained terms.

**Audit result:** correct bound, asymptotic, strictness, and limitation.

## 4. Approach 3: positive kernel and dense/term-count lower bounds

The sine coefficient calculation for `sign(sin t)` is correct: even coefficients vanish and odd coefficients are `4/(pi*j)`. Convolution with the nonnegative normalized Fejer kernel has magnitude at most one. Multiplication by `i exp(i s t)` moves all Fourier modes into nonnegative exponents and has unit modulus. Using `i sin(jt)=(exp(ijt)-exp(-ijt))/2` produces exactly the signs and factor `2/pi` in the report's `F_s`.

Every displayed odd-index coefficient is nonzero, since `1<=j<=s` and `s+1-j>0`. The negative and positive exponent blocks are disjoint, the central coefficient is zero, and there are exactly `2 ceil(s/2)` nonzero terms. Evaluating the negative block at one gives `-B_s`. The identities

    sum_{odd j<=s} 1/j = H_s - H_floor(s/2)/2,
    sum_{odd j<=s} 1/(s+1) = ceil(s/2)/(s+1)

give the claimed logarithmic asymptotic with absolute error. Positivity of the kernel establishes the norm on the entire circle, without sampling.

For the dense embedding let `m=min(k,d-k)` and `s=m-1`. Multiplying by `z^(k-m)` moves the center to exponent `k-1`; negative terms lie strictly below that center and positive terms begin at exponent k. Consequently the first k slots select exactly the negative block. The minimal exponent is nonnegative, and the maximal exponent is at most `k+m-2<=d-2`. When `m=1`, the zero construction is unnecessary: the constant polynomial supplies the required lower bound one.

Combining this construction with the two kernel upper bounds proves the uniform formula. If m is k, use the first upper bound; if m is d-k, use the second. The constants do not depend on d or k. Selecting a middle cut gives `max_k A(d,k)=log(d)/pi+O(1)` as d tends to infinity.

For even `N>=2`, set `s=N-1`. It is odd, so there are exactly N nonzero terms, N/2 in each naturally ordered block. The central gap creates no term-count ambiguity. Odd `N>=3` follow by adding one new higher-degree nonzero term, keeping the original retained cut, and letting its size tend to zero after rescaling. The N=1 case is handled by the elementary endpoint. Since `log(N-1)=log(N)+O(1)` uniformly for odd N>=3, the claimed term-count lower bound follows.

As an additional check on uniformity, writing `q=ceil(s/2)` and comparing each `1/(2r-1)` with the integral of `1/(2x+1)` on `[r-1,r]` gives `sum_{r=1}^q 1/(2r-1)>=log(2q+1)/2`. Since `q/(s+1)<=1/2`, one even obtains `B_s >= (log(s+1)-1)/pi`. This is an audit detail, not an additional counted approach or novelty assertion.

**Audit result:** correct norm proof, constants, supports, shifts, all small-parameter cases, and exact-nonzero-term passage. It proves no matching upper bound for arbitrary-support `C_N`.

## 5. Approach 4: exact quadratic certificate

For `omega=(1+i sqrt(3))/2` and `u=1/2-i sqrt(3)/6`, the identities `2 Re(u omega^j)=(1,1,0)_j` hold for `j=0,1,2`. Hence the complex-linear identity reproducing `a_0+a_1` from evaluations at omega and its conjugate is valid for complex coefficients, not merely real ones. The two evaluation nodes have modulus one, and `|u|^2=1/3`, giving upper bound `2/sqrt(3)`.

Independently expanding the Laurent product of `2+4z-z^2` with its reciprocal conjugate gives

    |2+4 exp(it)-exp(2it)|^2 = 25+8x-8x^2,  x=cos(t).

Thus its normalized slack is precisely `8(x-1/2)^2`. Equality occurs at the two stated nodes, so the norm is exactly one rather than merely at most one. The first two coefficients of the normalized polynomial sum to `2/sqrt(3)`. The contact values also align with the dual coefficients: `u*(2+4omega-omega^2)=3` is positive real. The primal and dual values therefore genuinely match.

For support `{e,e+q,e+2q}` with `q>=1`, factoring out `z^e` and using surjectivity of `z -> z^q` on the circle preserves both full and truncated norms. This proves the stated arithmetic-progression extension and does not extend to all three-term supports.

**Audit result:** exact complex-coefficient optimality certificate accepted.

## 6. Approach 5: complementary recursion and subset limitation

At each recursion the old and shifted blocks have disjoint exponents. Thus both polynomials have exactly `N=2^r` coefficients, all equal to plus or minus one. The parallelogram identity proves inductively that their squared moduli sum to `2N` at every circle point. Normalizing either by `sqrt(2N)` makes it feasible.

At one, the recurrence sends a pair `(x,y)` to `(x+y,x-y)`. Starting from `(1,1)`, successive even/odd-depth pairs are `(2^h,2^h)` and `(2^(h+1),0)`. Therefore the first polynomial's coefficient sum is nonnegative and at least half its coefficients are positive. Selecting the positive coefficients gives value at least `sqrt(N)/(2sqrt(2))` at one.

For general N, choose the largest power of two M<=N, so M>N/2, and add N-M tiny new nonzero terms. Select the same original positive subset and rescale. Passing to the supremum yields a uniform lower bound at least `sqrt(N)/4`; the energy upper bound is O(sqrt(N)). No exact optimizing constant is claimed.

These positive coefficients are generally scattered. The recursion neither changes their exponents nor gives an operation to move all positive terms ahead of negative terms while controlling the norm. Reordering the written terms makes an arbitrary subset look like a prefix but abandons increasing-exponent order. Moreover, the original complementary polynomials have dense degree N-1 and hence their natural truncations obey the already proved logarithmic dense upper bound. They cannot themselves witness square-root natural-truncation growth.

**Audit result:** square-root order for `U_N` accepted; transfer to `C_N` correctly rejected.

## 7. Literature and source-inspection boundary

The [publisher's Technau article](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/shapiros-problem-on-polynomials-with-large-partial-sums-of-coefficients/A28628834B07425EC029FE020201585A) and [institutional record](https://tugraz.elsevierpure.com/en/publications/shapiros-problem-on-polynomials-with-large-partial-sums-of-coeffi/) confirm publication on 10 June 2026, Forum of Mathematics, Sigma 14, e69, DOI 10.1017/fms.2026.10213. I inspected relevant passages on published PDF pages 1-4 and 17 in text, page 3 visually, and the publisher's theorem and reference entries.

Technau uses degree strictly below d, so `A(d,k)=M_(k-1,d)`. Theorem 2.1 applies to positive integers d>n and supplies a polynomial whose first n+1 coefficient sum approaches the Landau bound with relative error `O(n^3 exp(-d/(5n)))`. This is not an arbitrary-support term-count result. Theorem 1.3 attributes the exact middle-cut formula to Newman; reference 11 lists the 1978 article and 1979 erratum. I did not inspect either original full text or determine what the erratum corrects. Their DOI opens failed. No stronger erratum claim is supported. This audit verifies these statements and attributions, not the entire cited proofs.

I separately inspected [Hayman and Lingham's PDF](https://arxiv.org/pdf/1809.07200), PDF page 74 / printed page 73, in text and visually. Problem 4.3 specifies a bounded polynomial with N terms and a partial sum but does not explicitly prescribe a degree bound or settle every counting/ordering convention. The report appropriately preserves that uncertainty. Its historical progress statement does not establish present-day global open status. This bounded literature check is not an exhaustive search or a novelty certificate.

## 8. Executable checks and authentication

The original authenticated harness was run anew under actual UID=EUID=1000, Python 3.12.14, in normal, `-O`, and `-OO` modes. In every mode:

- 2,016 energy discriminants, 2,145 Landau coefficients, 64 Fejer polynomials, one quadratic certificate, and 11 complementary pairs passed.
- All 20 supplied malformed cases were rejected.
- A hostile current directory and PYTHONPATH did not cause hostile modules to execute under isolated mode.
- Appending to an existing read-only file and creating a new file in the read-only directory both actually raised PermissionError.
- The authenticated bootstrap passed; modified report/verifier, missing/extra entries, symlink, wrong pin, and four malformed-manifest controls were rejected.
- Original package hashes were unchanged.

An independently written checker, without importing the submitted verifier, additionally checked 8,128 energy cuts, 4,753 kernel coefficients, 9,409 positive-kernel multiplier coefficients, 97 Fejer polynomials including s=0, 8,385 shifted dense cuts, the complete quadratic primal/dual/contact identities, and 10 complementary pairs. It checked exact even-N support counts and an explicit scattered-positive-support case.

The independent input suite tried 64 cases in each optimization mode, including bool/float substitutions at every integer field, huge integers, exponent-to-infinity overflow, oversized decimal literals, missing numeric values, noncanonical/invalid rationals, boundary violations, duplicate keys, truncation, trailing data, invalid UTF-8, oversized input, and deep nesting. Every case exited nonzero with no success stdout. All except deep nesting returned structured JSON errors. Minimum and maximum allowed parameter sets also passed in all modes, including recursion depth 12 for the complementary construction. JSON exponent overflow cannot bypass the exact-int check.

The manifest, bootstrap, and pins independently match the handoff hashes. The bootstrap executes the exact verified in-memory verifier and fixture bytes; optimization does not disable its explicit checks. It authenticates a snapshot relative to trusted pins, not mathematical truth. It is not advertised as a hostile multiuser filesystem isolation mechanism or resource-proof parser.

Separate provenance checking independently matched both dataset byte counts and SHA-256 values, found exactly one problem-ID record with the designated problem number, and confirmed the research-record key. No dataset content is included in this audit.

The programs are ordinary exact-arithmetic tests, not a proof assistant. The infinite-family norm bounds, asymptotics, perturbation limits, compactness, and scope conclusions were reviewed analytically above. Passing finite tests alone would not prove them.

## 9. Source-free allowlist and release boundary

The frozen archive's allowlist is exactly these logical members:

- `public/README.md`, `public/REPORT.md`, `public/fixtures.json`, `public/provenance.json`, `public/sources.json`, `public/verify.py`
- `external/AUDIT_INSTRUCTIONS.md`, `external/MANIFEST.json`, `external/PINS.json`, `external/TEST_RESULTS.json`, `external/bootstrap.py`, `external/test_harness.py`

The new audit allowlist is recorded in `AUDIT_MANIFEST.json`. The authored audit, independent checker, test receipts, dataset-match metadata, source-inspection metadata, and hashes contain no copied source documents, source passages, dataset contents, private source material, or private coordination material. Source PDFs and extracted text are excluded. `AUDIT_MANIFEST.json` itself is authenticated by the separately returned hash.

No publication, queue change, repository mutation, or external outreach was performed during this audit. The precise mathematical disposition remains partial progress with five approaches and unresolved general term-count extremality.
