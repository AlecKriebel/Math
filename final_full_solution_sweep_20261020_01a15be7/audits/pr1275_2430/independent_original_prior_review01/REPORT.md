# Independent original-source, mathematical, and existing-publication audit: PR1275 /2430 /Erdős995

The accepted claim is a full negative answer to the **modern literal Erdős995 question**. It is already proved in Boon Suan Ho, *Counterexamples for lacunary dilates via dyadic spike blocks*, arXiv:2604.18535v2, Theorem1.6, proved in Section7 using the blocks and trial construction of Sections2–4. The paper precedes this PR. No new publication of this result is warranted. No material mathematical objection remains in that theorem's required chain after this review. This conclusion does not grant acceptance to the other results in the same paper.

The existing registered DOI, **10.48550/arXiv.2604.18535**, resolved with HTTP200 to the matching arXiv family. DataCite identifies it as a findable preprint, version2, with the exact title and Boon Suan Ho as author. The freshly fetched versioned PDF matches the PR's cited SHA256 exactly. Both fresh numeric-gid43-column spreadsheet reads contained191rows and no matching result/DOI/title/PR identity. `PROPOSED_ROW.json` supplies a qualified, literal four-string A:D proposal with B blank. It is a local proposal for root adoption and a further live duplicate check; no row, DOI, record, PR, branch, or publication was changed here.

## Claim, source identity, and chronology

For each fixed finite real p with 2<=p<infinity, there exist a real mean-zero f in Lp(T) and **one deterministic** increasing integer sequence n_j=2^{m_j}, n_{j+1}/n_j>=2, such that on one full-measure set E_p,

    limsup_{N->infinity} [sum_{j<=N} f(n_j x)]/[N(log N)^(1/p-epsilon)] = +infinity

for every real epsilon>0 simultaneously. f and the sequence may depend on p. They are fixed before x and the subsequent epsilon. N counts selected samples, not the size of the selected exponents or n_N. Taking p=2 gives the full negative answer to the modern universal o(N sqrt(log log N)) assertion, even in the mean-zero subclass.

The exact immutable PR head is `2e653ea299ef15d42b783901139454d29aec39bb`; base is `4b27092a448d53b61408355ce44ec38d103a1ce4`. All five actual added file bodies and the PR description were read: ACCEPTANCE.json, ARTIFACT_MANIFEST.json, AUDIT.md, README.md, SOURCES.json. The actual diff has no QUEUE.md edit. `PR_SOURCE_RECEIPTS.json` authenticates each body by size, SHA256, and Git blob SHA1. The embedded manifest's four content hashes and full five-file inventory agree. The 23862-byte PR audit is source-scoped; it credits Ho and does not claim a new counterexample. Provisional missing-status eligibility is appropriate because the PR verifies a full original negative, even though the full result is already public.

The live PR was created2026-10-11T20:34:01Z. arXiv/DataCite records first submission on2026-04-20T17:29:29Z and v2 on2026-04-21T17:55:07Z. Thus the accepted proof is a concrete prior source relative to this PR, without needing a global firstness inference. Current arXiv metadata lists only v1 and v2, with v2 current. The exact checked PDF is609251bytes, SHA256 `f88b36a072d66476c5948061b7f2fc4d61dc536bbc5df5aa5bd3cdd2a84a82d0`.

## Original problem and precise provenance

Fresh primary sources were recovered from the Erdős author archive and the official Erdős Problems site. The original paper is Paul Erdős, *Problems and results on diophantine approximations*, Compositio Mathematica16 (1964),52–65. Its printed57–58 (PDF6–7) were both read in text and visually checked from the scan. It assumes a lacunary sequence with n_(k+1)>(1+c)n_k for a fixed c>0, and evaluates a periodic f at fractional parts. Ho's ratio>=2 satisfies the strict condition with c=1/2. Using T=R/Z is the same fractional-part convention. No mean-zero restriction is needed for the superlinear question; subtracting the integral changes the sum by O(N), and Ho's examples have mean zero already.

The source must not be quoted as literally containing the modern formula. On printed58:

* Equation(15) gives lower examples with infinite limsup after division by **N(log log N)^(1/2-epsilon)**.
* Equation(16) gives an upper limit zero after division by **N(log N)^(1/2+epsilon)**.
* The prose discusses the considerable gap between these scales. It does **not** literally print the modern o(N sqrt(log log N)) question.

The exact modern universal little-o question is freshly authenticated at `https://www.erdosproblems.com/995`, its LaTeX view, and its history. The history contains a2025-10-20 entry with that precise formulation, predating Ho's April2026 paper. The site's Er64b bibliography identifies the1964 source. Therefore the result fully answers the actual modern problem2430/EP995 being audited, while the row/report preserve the difference between the modern formulation and the1964 displays. This distinction is provenance, not a reason to discard the full modern negative. The current site's question presentation or forum labels are not used as proof of correctness or of formal peer review.

## Primary proof read scope and access

The actual Ho v2 PDF was read for Theorem1.6 on page4, its introduction and statement context, the entire required chain on pages7–16, and Section7 on pages21–23. This covers the dyadic spike definition; Lemma2.1 on digit independence; Lemmas3.1–3.3 on floors and moments/convergence; Definition3.4 and Lemma3.5 on local trials; the stage definitions(4.1)–(4.14); Lemmas4.1–4.2; and the full proof of Proposition4.3. Remark7.1 was also read, but is not needed to refute995. The conclusion and acknowledgements on page26 were read. Theorem1.6, schedule, master lower bound, and Section7's parameter/quantifier displays were visually cross-checked using the retained rendered pages4,13,16,22,23. Printed Erdős57–58 were visually checked separately. Page11 was rendered but is not claimed as an additional image-inspected page. Essential formulas are not accepted from search snippets.

Sections5,6,8 and their separate claims are outside this audit's acceptance. Some adjacent text was necessarily observed, and the metadata abstract advertises other results; neither observation extends the mathematical verdict. In particular, this report does not certify the paper's Fourier-tail/EP996 theorems, an epsilon-free logarithmic endpoint, optimal secondary-log factors, or consecutive dyadic powers/bounded exponent gaps.

The fresh arXiv source archive contains exactly two ordinary files: `00README.json` (220bytes) and `lacunary-v2.tex` (74646bytes). Every member was read as bytes and hashed without running or compiling it. The TeX source was retained as source support; the mathematical read claims above refer to the actual PDF body, not to a claim of line-by-line review of all TeX. `PUBLISHED_SOURCE_INDEX.json` records all member hashes. The archive SHA256 is `675af05fd07147c32c6fb6c76e147d9995accda686e2fd108bab985a82aff8a8`, and the TeX SHA256 is `bac88b4f5d77b2fb103179647a5a339b3101a48fb31157f89e1ea1b659aa8506`. The accepted proof requires no author code, numerical certificate, or undisclosed dataset. All downloaded bodies, raw ledger responses, extracts, and images are retained privately and ignored; public files contain authored analysis and hash receipts.

## Independent falsification and universal proof

The following derivation checks the complete mechanism independently. The finite checker supplements it and cannot establish any universal real-p or almost-everywhere claim by sampling.

### 1. Centered spike, independence, and a real-p block bound

Write theta=2^(-d), h=sqrt(2^d-1), g=1/h. The spike is

    phi_d = (1_[0,theta) - theta)/sqrt(theta(1-theta)).

It has values h and -g, integral0, and variance1. After dilation by2^v, it depends on binary coordinates v+1,...,v+d. Disjoint finite collections of coordinates are independent under Lebesgue measure; the dyadic expansion ambiguity is a null set and the half-open interval convention defines the function everywhere.

For 0<lambda<=1, B>=100, integers L>=1,D>=d+2,U>=0, choose

    64 B^2 L/lambda <= 2^d < 128 B^2 L/lambda,
    F(x) = sqrt(lambda/L) sum_(q=1)^L phi_d(2^(U+qD)x).

The L spike windows are disjoint, so the block has mean0 and squared L2 norm lambda. Its deterministic negative floor is delta=sqrt(lambda L/(2^d-1)). Since2^d-1>=2^(d-1),

    delta <= lambda/(4 sqrt(2) B) <= lambda/B.

Thus the unspecified floor constant C3 can safely be chosen as1, uniformly in L and all placement parameters. This removes any growth of the error with stage length.

For every real finite p>=2, an elementary bound avoids any need to reconstruct Rosenthal's original proof. Let Y count spikes. Then Y~Binomial(L,theta), t=L theta<=lambda/(64B^2)<=1, and

    F=A(Y-t),   A^2=lambda/[L theta(1-theta)] <256B^2.

For integer r>=1, Pr(Y=r)<=t^r/r!, whence

    E(Y^p) <= t sum_(r>=1) r^p/r! = C_p t.

The series is finite by the ratio test for every fixed finite real p. Since t^p<=t and |a-b|^p<=2^(p-1)(|a|^p+|b|^p),

    E|F|^p <= C'_p B^p t <= C''_p lambda B^(p-2).

No integer-p assumption, cancellation heuristic, or central-limit approximation enters this estimate. The source's standard real-p Rosenthal application is also compatible with these exponents. For finite diagnostics the checker uses m=ceil(p), sum r^p/r!<=sum r^m/r!=e Bell(m)<3 Bell(m), giving an explicit enlarged constant and exact rational power enclosures.

### 2. Lp convergence and a single evaluation representative

Choose explicitly a_k=2^(-k-2), k>=1, and set lambda_k=a_k B_k^(-(p-2)). Then lambda_k B_k^(p-2)=a_k, and

    sum_k ||F_k||p <= C_p^(1/p) sum_k a_k^(1/p) <infinity.

Minkowski and completeness give convergence in Lp, hence L1, to a real mean-zero f. This uses the geometric budget allowed by the source; an arbitrary summable a_k alone would not imply summability of its p-th roots. It does not rely on independence across different blocks.

For an independent almost-everywhere convergence argument, each F_k has mean0 and is bounded below by -delta_k with delta_k=lambda_k/B_k. Thus integral|F_k|=2 integral F_k^-<=2delta_k. Since sum delta_k is finite, Tonelli implies sum |F_k(x)|<infinity almost everywhere, with the same L1 limit f. On one common full-measure set E0,

    f>=-mu,   f-F_k>=-mu for every k,
    mu=sum_k delta_k <= [sum_k a_k]/100^(p-1) = 1/[4*100^(p-1)] = M_p.

These inequalities follow by taking the convergent series of the other block floors; no stochastic domination is substituted for a pointwise floor. Define a representative of f arbitrarily, say0, off E0. Intersect E0 with the preimages of E0 under the countably many measure-preserving maps x->2^{m_j}x. This remains full measure. All evaluations used below now have simultaneous floors for every selected j and every block k. No point-dependent choice of the sequence and no uncountable intersection is made.

### 3. Exact local amplification

A trial uses exponents M+rD, 1<=r<=ell, with1<=ell<=L/8 and M+D>=0. Expanding the double sum groups variables

    Z_h=phi_d(2^(U+M+hD)x),  2<=h<=L+ell,

with weights w_h=#{(q,r):1<=q<=L,1<=r<=ell,q+r=h}. The weights sum to L ell and are at most ell. They equal ell precisely on the closed interval ell+1<=h<=L+1, containing **L-ell+1** indices. Every Z_h has the same spike probability theta and their windows are disjoint.

On the event of at least one positive spike in that central interval, keep its weight ell and charge every other variable its negative floor. This gives

    trial sum >= ell[sqrt(lambda/L) h - sqrt(lambda L)g].

The first bracket term is at least4 sqrt(2)B; the second is at most lambda/(4 sqrt(2)B)<=B. Hence the trial sum is at least2B ell, with ample slack. Multiple positive spikes help. No independence of this good event from the other F_i is required because their lower floors are pointwise.

Writing nC=L-ell+1>=7L/8, we have nC theta<=L theta<=1 and

    Pr(good)=1-(1-theta)^nC >=nC theta/2 >7lambda/(2048B^2)
            >= c0 lambda/B^2,  with c0=1/1024.

This is a direct rare-event estimate, not a Gaussian approximation.

### 4. Deterministic schedule and independence of good events

Take eta=1/20. At a trial with P selected samples already present, ell=ceil(20(P+1))=20(P+1), and the new count is P+ell. For T trials beginning with count P0, the identities are exact:

    (P_t)+1=(P0+1)21^(t-1),
    ell_t=20(P0+1)21^(t-1),
    Nstar+1=(P0+1)21^T,
    L=8ell_T=160(P0+1)21^(T-1).

Thus each ell_t<=L/8, P_t<=eta ell_t, and N_t=P_t+ell_t<=(1+eta)ell_t. These N's count samples even when exponent gaps become extremely large.

Choose d by the depth inequality, D=d+2, U=V_previous^max+1, and V^max=U+LD+d-1. The new block's first bit is U+D+1=V_previous^max+D+2, after the previous last bit V_previous^max+1. This verifies the source's block independence if one uses its independent-series route; the elementary convergence proof above already suffices.

Choose the first M nonnegative and large enough that M+D>m_previous^last and U+M+D+1>Omega_previous. Within a stage set

    M_(t+1)=M_t+(L+ell_t)D+d+2.

The full raw digit range of a trial is from U+M+2D+1 through U+M+(L+ell)D+d. Its good-event coordinates lie inside this range. The next raw range starts strictly after the preceding range ends; the first range of a new stage lies beyond Omega_previous. Omega can be taken to be the last trial's raw maximum, as in the paper. Good events for all stage/trial pairs therefore depend on disjoint digit coordinates. Within each trial, the individual windows also do not overlap. The new first selected exponent minus the old trial's last is (L+2)D; across stages the initial inequality gives a strict increase. Consequently all selected integer m_j are increasing, and n_j=2^{m_j} has ratios>=2.

Every parameter is fixed from p, the chosen budgets, and preceding finite parameters, before x or epsilon is considered. The successful endpoint selected later in the proof is an observation within this already fixed sequence, not an adaptive choice of n_j.

### 5. Shielding the complete partial sum

At a successful trial endpoint N=P+ell, split the full sum into: all P earlier selected terms of f; the active block F_k on the new ell terms; and f-F_k on those ell terms. On the common representative set, their lower bounds are respectively -mu P, 2B_k ell, and -mu ell. Therefore

    sum_(j<=N) f(n_j x) >=2B_k ell-mu N,
    (1/N)sum_(j<=N)f(n_j x) >=2B_k/(1+eta)-mu >=B_k-mu.

All previous samples and all future/other blocks have been charged. Replacing the full sum by the trial alone, or assuming that other blocks average to zero after conditioning on a hit, would be invalid. Neither is needed here.

### 6. Recursive growth budget, including p=2 and nonintegral p

Fix Gamma>=8/c0=8192. For a proposed B at stage k, take

    lambda=a_k B^(-(p-2)),
    T=ceil[Gamma B^2/lambda log(k+1)]
     =ceil[Gamma B^p/a_k log(k+1)].

The previous count P0 is already fixed. The exact count identity implies

    log Nstar(B) <= K_k B^p,
    K_k=log(P0+1)+(Gamma/a_k*log(k+1)+1)log21,

for B>=100. K_k may depend on the past and p but **not** on the proposed B. Let epsilon_k=1/[2p(k+2)] and alpha_k=1/p-epsilon_k>0. Then

    B/[log Nstar(B)]^alpha_k >=K_k^(-alpha_k)B^(p epsilon_k) ->infinity.

Here p epsilon_k=1/[2(k+2)]>0. The uniform M_p bound already controls the eventual floor of every future stage. Thus there is a finite integer B_k>=100 such that

    (B_k-M_p)/[log Nstar(B_k)]^alpha_k >=k.

All remaining parameters of that stage are finite once B_k is frozen. Ceilings change the upper bound by a constant and introduce no continuity requirement. This alternative global bound removes any apparent circular dependence on a future mu; the paper's finer bound mu_k(B) in(7.4) is valid as well. At p=2, lambda_k=a_k and T grows like B_k^2, leaving the same positive power. For a nonintegral real p, lambda may be real, which is allowed; one still chooses an integer dyadic depth and integer trial count from the stated inequalities. No restriction to integer p or numerically effective real parameters is silently imposed.

### 7. Almost sure stages and every epsilon on one set

Independence of trials within a stage gives

    Pr(stage k fails) <=exp[-c0 T lambda/B^2] <=(k+1)^(-8).

The failures are summable, so the first Borel–Cantelli conclusion gives eventual stage success almost everywhere. It does not require independence between stages. Intersect this set with the single representative/evaluation set above. For x in this one full-measure set, each sufficiently large stage has a successful endpoint N<=Nstar, with positive average at least B_k-mu. Because alpha_k>0, the signal choice and N<=Nstar imply

    [sum_(j<=N)f(n_j x)]/[N(log N)^alpha_k] >=k.

The endpoints tend to infinity. Given **any** epsilon>0, eventually epsilon_k<epsilon; for those same endpoints, log N>1 and replacing alpha_k by1/p-epsilon only lowers the positive denominator. The quotient remains at least k. Hence all real epsilon>0 work for the same x and the same full-measure set, without intersecting uncountably many epsilon-dependent sets.

For p=2, use epsilon=1/4. The factor (log N)^(1/4)/sqrt(log log N) tends to infinity. The infinite positive limsup above therefore contradicts a universal o(N sqrt(log log N)) bound. This supplies the complete counterexample required by modern EP995, not merely a large finite average or an assertion about a different sampling index.

## Exact diagnostics and adversarial controls

`verify_audit.py` is independently authored standard-library code. It performs no network calls, subprocesses, source-author execution, or filesystem mutations. Every guard uses explicit exceptions and remains active under -O and -OO. It checks actual source/file/blob identities, the nested PR content manifest, every published source archive member, DOI metadata, the retained ledger/proposal shape, and the closed directory seal when requested.

Its mathematical controls include all convolution weights for8<=L<=64 and1<=ell<=L/8; exact rational rare-event probabilities and floors;108 exact moment models with p in{2,5/2,3,7/2,10/3,4}, three costs, two heights, and three lengths; rational power enclosures by integer roots; explicit enumeration of14binary coordinates for three disjoint windows; multistage exact schedules with huge integer L but no sampled layer enumeration; shielding of the old prefix; and rational exponent identities for150(p,k) cases. Negative controls reject overlapping-window independence, the wrong central count, wrong double-sum mass, removal of centering, use of t^p<=t beyond t<=1, omission of the old-prefix loss, and altered manifest hashes. They are diagnostic falsification controls, not a claim that the finite cases prove the infinite theorem. `CHECK_*` and `FINAL_VALIDATION.json` record actual runs; the written derivation above is decisive for all real p, all stages, and the almost-everywhere quantifiers.

## Priority, public record, and accounting limits

The strongest necessary finding is positive: a publicly available, authenticated, complete source theorem already covers precisely the modern problem and the PR's accepted full finite-p strengthening. Ho v2 predates the PR by months. There is no need to establish that Ho was globally first to conclude that this PR must not be republished as a new project solution. The modern2025history entry also prevents treating the exact little-o question as an ad hoc target invented after the counterexample. Earlier upper/lower results in the historical paper do not by themselves give the accepted modern negative; the present proof checks the new scale directly.

Fresh source/DOI checks found the exact arXiv/DataCite family. Current arXiv metadata has no journal-reference field observed; DataCite's type is Preprint and has no relatedIdentifiers. A Crossref exact-title query returned no exact match among its five results, a DataCite exact-title query returned the one arXiv family, and a Zenodo exact-title query returned zero hits. Supplementary public searches used the exact title, arXiv identifier, author, lacunary terminology, and EP995 aliases. Their secondary snippets are leads only, never mathematical acceptance. A bounded local text search of the top-level Zenodo tool/discoverability folders found no exact-title/arXiv-id package; the working-tree attempt directory was absent (the actual pinned Git objects were used). An initial broad filename search had unrelated numeric matches and is not evidence of absence. These are bounded retrieval facts, not a certificate that no other version, unpublished package, or later journal publication exists. No authenticated Zenodo record/concept DOI or journal DOI is substituted for the registered arXiv DOI.

The DOI resolver returned200 to the matching unversioned arXiv family. Because the DOI identifies a family rather than independently pinning v2, the proposed row names v2 and includes its PDF hash; any future processing should keep that qualification and recheck the live record. The existing source package contains its PDF and all two published source members. No scientific supplement necessary to the accepted analytic proof is missing from that authenticated arXiv package. This statement is not a demand that arXiv mirror a hypothetical unpublished local program.

The spreadsheet schema is exactly A:Original Problem, B:Solution Chat URL, C:DOI, D:Notes. Initial2026-10-22T09:54:09Z and final2026-10-22T10:08:01Z GWS reads used numeric gid1254632077 and all43columns. Both191-row bodies have SHA256 `fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1`. Matching used problem2430, PR1275, title/result terms, author variants, EP995, and DOI/arXiv aliases; no candidate row was found. Naked995 hits at rows83,90,162,179 were inspected and refer to unrelated digits/dates. Do not infer that those rows represent this result. The proposal contains one paper/result-family row and does not add separate rows for finite-p variants or unaccepted theorems.

The source's page26 acknowledges GPT-5.4 Pro for strategy/intermediate formulations/exposition and states the author's responsibility for the mathematics. This is a primary-source AI-use disclosure, not evidence of formal independent human peer review. The PR and this review also use AI extensively in proof development/checking, computational diagnostics, source/priority auditing, and preparation of notes. No formal independent human peer review was established by the inspected records. No such review should be claimed in the tracker.

The principal live sources were the [versioned Ho PDF](https://arxiv.org/pdf/2604.18535v2), [current arXiv record](https://arxiv.org/abs/2604.18535), [published source archive](https://arxiv.org/src/2604.18535v2), [registered resolving DOI](https://doi.org/10.48550/arXiv.2604.18535), [DataCite record](https://api.datacite.org/dois/10.48550/arXiv.2604.18535), [Erdős author-archive original](https://users.renyi.hu/~p_erdos/1964-24.pdf), [modern995 statement](https://www.erdosproblems.com/995), and [statement history](https://www.erdosproblems.com/history/995). All these actual responses were recovered successfully with HTTP200; version/support/read-scope qualifications above apply. The retained receipts supply timestamps and exact bodies' hashes; search result pages are not substituted for these primary bodies.

## Final scoped disposition

**Mathematical full modern EP995 negative: accepted. Existing prior publication identity: authenticated. Novel project solution/new upload: no. Tracker coverage: missing in the two retained191-row snapshots, pending root adoption and another live semantic duplicate check.** The only remaining tasks here are root-owned reconciliation actions; this child has performed none of them and makes no package readiness, mergeability, or service-write declaration. All earlier closed audit directories remain untouched. No contact with any outside individual, other active agent, or chat was initiated.
