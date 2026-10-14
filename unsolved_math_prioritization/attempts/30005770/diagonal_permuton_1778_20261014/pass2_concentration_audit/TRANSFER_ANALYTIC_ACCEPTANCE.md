# Independent analytic audit of the exact 1324 staircase transfer

Date: 14 October 2026. Shared PASS2, row 1778 /30005770.

## Verdict and frozen scope

**Accepted:** the exact two-sided marked-cell weights, their subcritical convergence domain, the exponentially growing incoming-bias example, the conditional exponential-fugacity criterion, and the conditional implication from a strict squared-kernel growth gap to exponential largest-cell concentration.

The strict squared-kernel gap is **unproved**. No actual largest-cell tail, uniform1324 anti-diagonal limit, or universal diagonal theorem is established by these documents. The conditional spectral proof is valid; its enumerative hypothesis is the remaining substantive input.

Reviewed artifacts:

- `pass2_staircase_bias/EXACT_GREEDY_TRANSFER.md`: 14208 bytes, SHA-256 `dfbab3a20d05861a7c4aba868b89a225f2ac5db201a467358f015f6efabe2b03`.
- `pass2_staircase_bias/SQUARED_KERNEL_NEXT_TARGET.md`: 8757 bytes, SHA-256 `f5dfd42ac902e46190f4ca5887752693efa00fb5f95a5af3e5d2646ad63a0dd9`.

The exact canonical encoding in the transfer note's Sections 1–4 was independently accepted by the complementary geometry reviewer in `pass2_bijection_audit/PAIR_LOCAL_KERNEL_ACCEPTANCE.md`, 7439 bytes, SHA-256 `a7b8cbfc9809ea36aafa324fac985c826e6f93457ea36d0f24a245bd6e676161`. This audit checks the analytic consequences using that accepted encoding. No mathematical correction is needed in the pinned final versions.

## 1. Exact law and formal marked weights

Let the states be the nonempty 213-avoiders, with normalized adjacent-pair kernel K(A,C). All state weights are w_A=z^|A|. Every state has positive size, so each fixed coefficient involves finitely many state sequences, patterns and interleavings.

The prefix sum ell_A includes the incoming edge into A, but not A's own size weight. The continuation sum h_A includes every outgoing edge and successor size weight, but likewise not w_A. Their recurrences therefore have exactly the displayed orientations:

    h_A = 1 + sum_C K(A,C) w_C h_C,
    ell_A = 1 + sum_B ell_B w_B K(B,A).

Joining a prefix and a suffix at one distinguished A cell counts each permutation with that marked cell once. If a permutation has several cells with the same normalized pattern, it correctly contributes once for each possible mark. Thus w_A ell_A h_A is the exact marked-cell weight, with no independence or uniform induced-cell assumption.

For M_m=sum_{|A|>=m} w_A ell_A h_A, coefficient extraction and division by the full count a_n gives the exact expected number of cells of size at least m. The largest-cell event is bounded by this count. There is no missing a_k a_(n-k)/a_n or allocation factor: the kernel path representation already counts the full permutations and the denominator is exactly a_n.

## 2. Convergence domain and its limitations

Skew closure gives a_(p+q)>=a_p a_q, and the fixed-pattern exponential bound makes lambda=lim a_n^(1/n) finite. Thus rho=1/lambda is the counting-series radius. For every real 0<z<rho, both F(z) and zF'(z) are finite.

For fixed A, w_A h_A counts permutations whose first normalized state is A; w_A ell_A counts those whose last normalized state is A. Each is bounded by F(z)-1. The full once-marked sum satisfies coefficientwise

    sum_A w_A ell_A h_A <= z F'(z),

since a size-n permutation has at most n nonempty cells. Nonnegativity justifies every rearrangement of the path sums in this domain, and also proves convergence of all displayed individual sums.

These conclusions alone supply no convergence at rho, bounded transfer operator on an unspecified space, symmetry, reversibility, or bound uniform in state size. In particular the first-cell expression lacks ell_A, whereas the arbitrary-cell expression includes it. The first-cell theorem cannot be applied to arbitrary cells by omitting their incoming completion weights.

## 3. Exact incoming-bias calculation

For the increasing state I_k and decreasing state J_m, all horizontal interleavings of an upper I_k and lower J_m avoid1324. Splitting a hypothetical occurrence according to its number of lower points shows that one lower point would require an upper213; two lower points would require an increasing lower pair; three lower points would require a lower132. The all-upper and all-lower cases are also impossible.

The highest lower point is the first lower point in horizontal order. The greedy witness requires exactly r upper points before it, with 1<=r<=k-1. After it, the remaining k-r upper and m-1 lower points can be interleaved in binom(k-r+m-1,k-r) ways. Summing over r gives

    K(I_k,J_m) = binom(k+m-1,k-1)-1.

The endpoint k=1 gives zero, and m=1 gives k-1, as required. Retaining just one-state prefixes I_k gives

    ell_(J_m)(z) >= 1 + z[(1-z)^(-m-1)-(1-z)^(-1)].

For each fixed 0<z<rho, the right side has exponential rate -log(1-z)>0 in m. Therefore a uniform all-state subexponential incoming-weight estimate is false for this exact avoidance-class encoding. This is an actual completion-weight obstruction, not merely an abstract numerical tree example.

The statement remains compatible with negligible probability of a large decreasing terminal cell. Such a cell has h_(J_m)=1 and still contributes its factor z^m; fixed-size probabilities also require coefficient extraction and the full a_n denominator. Incoming exponential growth by itself is not a weak-limit counterexample.

## 4. Exponential-fugacity criterion

Suppose one fixed eta>0 makes

    H(z,exp(eta)) = sum_A exp(eta|A|) w_A ell_A h_A

finite for every real 0<z<rho. For m=ceil(epsilon n), positivity gives

    [z^n]M_m <= z^(-n) exp(-eta m) H(z,exp(eta)).

Set z=rho exp(-eta epsilon/2). This is one fixed strictly subcritical number for each fixed epsilon>0. Since log a_n=n log lambda+o(n), division by a_n yields the logarithmic upper rate -eta epsilon/2. The finite H value is a constant independent of n; no uniform bound as z approaches rho is needed.

This implication is valid. The trivial bound H(z,u)<=uzF'(uz), for u>1 and uz<rho, is also valid because the marked cell's size is at most the total size. But the latter restricted domain does not imply the stronger all-subcritical-z hypothesis with a single u>1. Neither hypothesis is silently assumed to hold.

## 5. Squared-kernel normalization and strict margin

Set

    S_n = sum_(|A|+|C|=n) K(A,C)^2,
    beta = limsup S_n^(1/n),
    B(z)_(A,C) = z^((|A|+|C|)/2) K(A,C).

For real positive z, the squared Hilbert–Schmidt norm is exactly sum_n S_n z^n. The ordinary square K(A,C)^2 counts two choices with the same ordered pair of internal patterns; it cannot be replaced by the ordinary two-cell count sum K or by the reversed product K(A,C)K(C,A). The kernel generally remains non-self-adjoint.

The hypothesis beta<lambda implies a genuine open Hilbert–Schmidt neighborhood beyond rho. The additional bound beta>=4 follows from the accepted I_k,J_m formula with k,m asymptotically equal: its central-binomial square has nth-root limit4. Hence lambda>4 and rho<1/4 under the conditional hypothesis. One can choose

    rho < R < min(1/beta,1/4),    1 < u < R/rho.

Cauchy–Hadamard gives sum_n S_n R^n<infinity. The ordinary state vector e(z)_A=z^(|A|/2) lies in ell^2 for z<R<1/4, because the states are Catalan-enumerated. All boundaries in this choice are strict; an equality beta=lambda would not supply the required margin.

## 6. The subcritical spectral-radius proof is sound

The proof establishes r(B(z))<1 for every 0<z<rho, using the strict Hilbert–Schmidt margin and the exact finite counting series. No infinite-dimensional Perron theorem is needed.

First, operator norm is monotone for bounded positive matrices on ell^2: |Vx|<=V|x| allows the norm supremum to be restricted to nonnegative vectors. Thus entrywise T>=cU>=0 implies T^q>=c^qU^q and r(T)>=c r(U), by the spectral-radius formula.

If r(B(z))>=1 at a subcritical z, choose z<z'<rho. Since every state has size at least one,

    B(z') >= (z'/z) B(z),

and hence r(B(z'))>1. Let T=B(z'). Its Hilbert–Schmidt property makes the finite coordinate compressions T_N=P_N T P_N converge in operator norm to T.

A nonzero compact spectral value theta of T with |theta|>1 is an isolated eigenvalue. Choose a sufficiently small contour around it, contained in {|w|>1} and otherwise in the resolvent. The resolvent identity and norm convergence make the compressed resolvents converge uniformly on that contour. Therefore their Riesz projections converge in norm to the nonzero limiting projection. The compressed projections are nonzero for large N, so some eigenvalue of the finite compression lies inside the contour and r(T_N)>1.

This step is valid for non-self-adjoint operators. It uses isolated-eigenvalue persistence, not general continuity of the spectral radius under arbitrary infinite-dimensional norm perturbations.

For fixed such N, all entries of e_N=P_N e(z') are positive. Let d be their positive minimum. For every q,

    e_N^T T_N^q e_N >= d^2 sum_(i,j)(T_N^q)_(i,j)
                    >= d^2 ||T_N^q||_2.

The second inequality follows by bounding operator norm by Frobenius norm and then by the sum of nonnegative entries. Since r(T_N)>1, the sum over q diverges. But each term is an exact nonnegative weight of canonical paths using only the first N states. Their sum is bounded by F(z')-1, which is finite. This contradiction proves the claimed strict subcritical spectral bound. Irreducibility is not required.

The spectral-radius formula then gives operator-norm convergence of both Neumann series for B and B^T. Applied to e, these yield ell^2 vectors f and g whose coordinates agree with the nonnegative path expansions, namely z^(|A|/2)h_A and z^(|A|/2)ell_A.

## 7. Both weighted vectors receive exponential smoothing

Let D_u be diagonal with entries u^(|A|/2), for the same fixed u>1 chosen above. For every z<rho, uz<R. Squaring the entries of D_u B(z) introduces u^|A|, which is bounded by u^(|A|+|C|). Consequently D_u B(z) is Hilbert–Schmidt, controlled by sum_n S_n(uz)^n. The same argument applies to D_u B(z)^T after exchanging the two indices. Also D_u e(z) lies in ell^2 by Catalan enumeration and uz<R<1/4.

Although D_u itself is unbounded, the equations f=e+Bf and g=e+B^Tg correctly show that f and g are in its domain: the right-hand terms have square-summable weighted coordinates because D_u B and D_u B^T are bounded. Thus D_u f and D_u g belong to ell^2. Cauchy–Schwarz gives

    H(z,u) = sum_A u^|A| f_A g_A
           <= ||D_u f||_2 ||D_u g||_2 < infinity.

The same u works for every z<rho. This proves the exponential-fugacity hypothesis from beta<lambda, and therefore proves the conditional largest-cell theorem. The previously accepted deterministic bound relating the largest cell to distance from the anti-diagonal then gives the conditional weak permuton conclusion.

## 8. Sources, finite checks and remaining scope

The spectral background statements were checked directly in the author's local primary-source PDFs:

- Stéphane Nonnenmacher, *Introduction to Spectral Theory*, Fall2022, Theorem5.1.9, printed pp.67–68, PDF pp.68–69. PDF: 504224 bytes, SHA-256 `c0c6b51c4462b3b80a0fab09e6683e28f7ae16d8142cb34ccf44c56265571bb8`. Public source: https://www.imo.universite-paris-saclay.fr/~stephane.nonnenmacher/enseign/Spectral%20Theory%202022%20chap1-6.pdf . This supports the isolated finite-multiplicity nonzero spectrum of a compact operator.
- Leszek F. Demkowicz, *Lecture Notes on Non-Self Adjoint Operators and Related Topics*, dated4December2024, Theorem1.4 and Lemma1.12, PDF pp.12 and19. PDF: 671344 bytes, SHA-256 `8ae4f77bc8ba2beb660ce3ec44995f9e74839aab5b058eec47e8292cb4e23eac`. Public source: https://oden.utexas.edu/media/pending_reports/book.pdf . This supports the contour projection and compact regular-eigenvalue facts. The perturbative application itself is explicitly proved in the authored note.

The final transfer checker uses explicit runtime failures. Its normal, -O and -OO reports are byte-identical (2347 bytes each, SHA-256 `4831ce5a9a9b09097cd30ae3eb92fb5e5db275faf21826e5adbfd887177819b0`); the script SHA-256 is `f17b5da53e1d5e577700414eb5f562f5931d7cd2538fa6ce2fcc19736330ac24`. These reports compare the complete normalized-state-chain distribution through size8 and record the squared-kernel coefficients 0,1,15,170,1782,18297,187549 at sizes2–8. I inspected the implementation and compared the supplied reports. The complementary reviewer separately enumerated the kernel and full class through size8.

No finite coefficient list establishes beta, its existence as a limit, a strict growth gap, or an asymptotic shape. The remaining analytic route requires an all-size bound proving beta<lambda (or another valid estimate establishing the needed marked-cell tail). This audit accepts only the exact reductions, obstruction and conditional theorem above. It does not claim the universal target, or even its uniform1324 case, is now solved.
