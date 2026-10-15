# PR375 / 30004293: independent diagonal upper-bound audit

Checkpoint: 2026-10-03T07:06:48Z. Completion estimate: 95% of the assigned diagonal audit. Frozen head: `36c29bb039471f132889d577c9322d78925b62dd`.

**Verdict: PASS for the frozen Turns 3–4 upper results. No mandatory mathematical correction found. The sharp prefix-growth problem remains unresolved.** The independent derivation also identifies a stronger possible upper result; it is separated below and must receive another adversarial audit before promotion. No candidate file or five-turn history was modified.

The exact accepted frozen upper statement is

    limsup log M(D) log log D / log D
        <= (log 3 - 1)(log 2)^2 = 0.04737857129996504...  almost surely.

Here the independent 1/n subset model and finite subsets are essential. M(D) is the largest subset-sum coefficient of A intersect [1,D]. The source's unrestricted infinite-set display, the annular beta_k thresholds, this subexponential upper scale, and a sharp log-log prefix exponent are distinct claims. The target constant is valid and explicitly nonsharp.

## Independence and sources

The complete Green OWR contribution, printed pp. 3164–3167, was read before candidate content, as were the FGK v3 model, Theorem 2, complete Lemma 2.1 proof and remark, flag definitions, and the deletion/quotient method in Sections 4.1–4.2. The published FGK model and complete tensor-lemma proof/remark were compared. Input hashes, sizes, PDF metadata, access methods, and private source paths are in SOURCE_ACCESS_IDENTITY.json. Raw PDFs and extracted text are confined to ignored `tmp/`.

The model, target, route and controls were written before candidate inspection. INDEPENDENCE_SEAL.json was created at 2026-10-03T06:59:57.148471Z and binds those files and the initial independent control streams. Only then were frozen author documents, verifiers and historical review read. No sibling report or root mathematical verdict was read before that seal. The historical review is corroboration only.

Primary sources: [Green's OWR contribution](https://ems.press/content/serial-article-files/46829), [FGK arXiv v3](https://arxiv.org/pdf/1908.00378v3), [published FGK](https://link.springer.com/content/pdf/10.1007/s00222-022-01177-y.pdf). Mao–Song v2 and the divisor-power paper are separate unaudited scopes in this audit. Their threshold/divisor claims are not used to deduce sharp prefix behavior. This audit does not reconstruct the entire published entropy lower-bound proof or certify novelty.

## Universal flag and reconstruction checks

The largest-pivot scan is deterministic and complete: every recorded binary column raises the rational span modulo the diagonal by one dimension, and integers are strictly descending. Distinct subsets force distinct row signatures across the recorded columns, so k<=2^t. Coordinate degeneracy therefore cannot silently remove the rank lower bound. Binary columns common to all subsets have zero quotient image and add no residual quotient choice.

Upward rounding puts each recorded integer in its stated unit logarithmic band. Every nonpivot entry above the next rounded endpoint has its column in the current flag space. Tied bands are empty, rather than an assumption failure. The cube-section bound follows by an injective projection to dimension-many coordinates. Identifying zero and one gives at most 2^(j+1)-1 diagonal classes. This holds for every rational flag that occurs; finite enumeration is not the justification.

For each residual set and coarse datum, quotient assignments determine residual sums, and independent pivot classes make the pivot tuple unique for each such sum. Multiple assignments with the same sum cannot create additional original realizations. Invalid, repeated, nonintegral or residual roots are discarded. The finite Bernoulli probability ratio is exactly product 1/(K_j-1). Summing the residual probabilities does not claim that random deletion preserves their distribution. The source's corresponding proof confirms the same essential root-elimination mechanism.

Turn 3 encodes empirical frequencies for fixed k, making its unspecified k-dependent constants legitimate only in the fixed-parameter order used there. Its subpolynomial conclusion follows by countable intersections after the dyadic Borel–Cantelli argument. Turn 4 removes these frequencies and counts all ordered binary pivot columns and bands by [2^k(L+3)]^t. All ordered subset labels are already represented by the incidence columns; there is no omitted family-order factor.

## Uniformity, constant and probability modes

Turn 4's one-sided cumulative regularity bound transfers to every residual subset. Summation by parts has nonnegative h_j-h_(j-1), and consequently pays only (u+2)h_t. It does not pay one independent error per bin. The positive first coefficient is a=log3-1; every later coefficient log((2^(j+1)-1)/(2^j-1))-1 is negative. Bounding them at their appropriate opposite endpoints yields exactly a-c(t+a), including t=1.

The stated R includes the vector count, bin count, probability-weight factor and regularity error. Thus q=cL-R>=1 permits the geometric sum with factor less than two. There is no implicit k-dependent constant in the lemma. With k=floor(L/(log L)^3), t_0=ceil(log_2 k), u=sqrt(L)log L and c=(a+epsilon)/t_0, all admissibility conditions hold eventually; t_0R=o(L), q tends to infinity, and the first exponent is at most -epsilon L/2. The occupancy exception is at most 2(L+3)exp(-(log L)^2/3), summable on dyadic D. First Borel–Cantelli needs no independence of these events.

The deterministic convolution inequality m(B union C)<=2^|B|m(C) is used in the correct direction. The count law applies to the deterministic growing cutoff D^c. Since t_0~log L/log2, the contribution is (a+epsilon)(log2)^2 L/log L; the two log2 factors are required. The log k term is negligible. Monotone interpolation covers all D, and a countable epsilon=1/m intersection supplies a single probability-one event. Open/closed annular endpoint changes have vanishing probability, as already stated in Turn 1. The upper beta_2 identity recovered by the method is known and credited.

## Other-turn scopes

The other author turns were read for their boundaries and replayed after the seal. Turn 1 supplies credited annular amplification, tail determinism, and cutoff comparisons; Turn 2 supplies sparse-support controls and the elementary prefix count law; Turn 5 uses the explicit pointwise Turn 4 probability estimate for fixed logarithmic moments. The much larger raw moments and rare polynomial peaks in Turn 5 do not contradict the almost-sure upper result. This diagonal audit does not replace a separate complete independent reconstruction of those other turns.

None of the five-turn claims determines a finite matching upper exponent for log M(D)/log log D. Fixed-cardinality boundedness, fixed-k thresholds, tail determinism and annealed raw moments do not fill that exact gap.

## New independent audit derivation

INDEPENDENT_DERIVATION.md supplies a candidate-free proof route using a further rank restriction. If a same-sum family has diagonal quotient rank at least r, choose 1 and r independent incidence columns and restrict to r+1 rows giving an invertible submatrix. The resulting r+1 equal-sum subsets have full quotient rank r. Therefore it is sufficient to count full-rank witnesses in dimension r+1, with at most 2^(r(r+1)) ordered binary bases. Absence of such a witness bounds every high-window fiber by 2^(r-1).

With uniform logarithmic occupancy and exact deletion/reinsertion odds, the written argument takes r=floor((log T)^2), D=exp(T), and log y of order T/r. Its union exponent is -delta T+O((log T)^5). It derives

    log M(exp(T)) = O(T/(log T)^2 + (log T)^2),

and hence a zero limsup at the frozen Turn 4 normalization. This is a **separate audit deduction awaiting another independent adversarial check**, not a replacement theorem in the original five-turn packet, a novelty certification, or a sharp prefix exponent. The pending verification must inspect the quotient-row restriction, all root eliminations, witness union count, exact odds, occupancy transfer and growing-parameter uniformity. The written derivation and full independent controls are available for that check; no raw source or author code is used in them.

## Reproducible evidence and remaining work

Initial independent controls passed 25 cube-generated spaces; 3,750 subset-sum fibers; 2,694 row restrictions and exact pivot recoveries; 970 cases with tied integer logarithmic pivot bands; 2,187 exact deletion identities; and 2,304 convolution comparisons. The rank, root and probability checks use exact rational arithmetic. The initial numerical logarithmic identities are supplementary; the written inequalities are analytic. A second exact insertion-kernel control covers every one of the 62 collision realizations on [2,8], with 32,768 ghost assignments and 508 valid distinct roots. Its rational Taylor certificate proves the strict coefficient sign used in the independent derivation.

The post-seal private replay verified all 54 frozen snapshot objects, including the 53 target objects, both SHA-256 and Git blob identities; every referenced author/publication/historical-review manifest binding; all five author receipts byte-exactly (150,925 assertions); and the historical independent receipt byte-exactly (8,390 assertions). PRIVATE_REPLAY.json records every binding, runtime and stream hash. Complete standard-output and standard-error files are public owned audit artifacts. The candidate copies are under ignored tmp only. The original five-source PDF bundle was not replayed; only this auditor's three primary sources were independently retrieved.

Mandatory candidate mathematical fixes: none found for the assigned upper scope. Remaining original gap: sharp growth, a finite matching log-log upper exponent, and convergence on that scale. Remaining new-audit gap: separate adversarial confirmation before promoting the stronger zero-normalized deduction. Root integration/publication is outside this agent's mutation scope; no Git, remote, DOI, Zenodo or external-communication action was taken.
