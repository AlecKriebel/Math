# PR1310 / 2449: independent computational certificate review

Review completed 2026-10-22 UTC. Family completion: 100% for this assigned numerical review; overall sweep remains 80%. This report does not grant whole-paper, priority, publication, or merge acceptance.

## Result

**Both numerical obligations are reconstructible and pass a fresh, independent exact-integer reconstruction.** The omitted historical executables and raw certificates do not establish a mathematical refutation, and their absence is no longer a numerical blocker for the explicitly tested formulas: new authored programs and all accepted slab results are provided here. This reconstruction does not authenticate the omitted historical program or record bytes identified only by hashes.

The global one-cut family has exactly one stationary minimum. Its parameter and value satisfy

    0.025715536866527 < q_* < 0.025715536866528,
    1.834430475762661 < Lambda(q_*) < 1.834430475762662.

The exact rational comparator

    T = 1.83443047576266171109075363512901884952989750747

is strictly larger than the freshly enclosed minimum. The all-parameter reference/scalar calibration is strictly positive for every required finite k, using different accepted subdivisions and sufficient smaller margins. Conditional on the analytic supporting, adjoint, block, and circle inequalities being correct, these numerical obligations give the strict finite-polynomial lower bound. They do not independently prove those analytic inputs or Tao's supremum theorem.

No counterexample to either numerical gate was found. Initial failed proposals in the newly authored generator were repaired by widening untrusted proposal boxes and subdividing; they were never accepted from approximate signs. Those implementation repairs are not defects attributed to the PR.

## Immutable inputs and actual reading boundary

The actual current PR head is `4ce3fbd19d499c7a16aa46ca416ad3305ef3d286`; all 21 changed-file Git blob identities match the parent's binding. Complete source bytes of those 21 files, including the full QUEUE and nested public manifests, are retained privately in `private_sources/captures.json.gz`. The live PR body matches the parent's body SHA-256 `0bc9309de239d57d18ac15d02007c0f5961fc9bac17d981d9e0522bf1fb5c26e`. The later global appendix explicitly supersedes the earlier seven-file upper-bound report; the earlier pending-certificate statements were not treated as the current claim.

Read directly: the live body; current scope and eligibility; the operative theorem, numerical sections, target linkage, strictness/recovery interfaces of `PROOF.md`; both complete certificate proof notes; the complete kernel audit; acceptance/README/verification/source/edition metadata and review overview; relevant end-to-end audit sections; the older packet's scope and fixed-candidate witnesses. No claim is made to have independently re-proved every analytic section or all historical audit prose. All pinned files were captured and authenticated even where their content was only used for provenance.

Fresh Wang PDF and public companion verifier have exactly the historically cited bytes:

- Paper: 488,289 bytes, SHA-256 `3a7e857b12e59f24af17f36a30030b0ad6368c2d59955ef58e643400917565ad`.
- Verifier: 110,762 bytes, SHA-256 `e84b94b40a27d2f3e254d4d14393a49c79ac4db57e4b55010441d4e04eff9616`.

The relevant manuscript certificates, numerical appendix and source-code conversion/root/soft/finite/terminal regions were statically inspected. The complete 3,335-line verifier was retained but its old unused mixed-Fourier machinery and optional supremum checks were not audited line by line. **No source-author Python, source-author executable, Lean code, installer, or third-party numerical library was executed.** Only the new authored standard-library programs in this folder ran.

Fresh original EHP PDF: 4,304,732 bytes, SHA-256 `5d20ad770563e425ac3343e31581859a24facabf744f10489b8f8d201b0ec12a`. Its defining monic product, strict `|f|<1`, real-axis convention and printed p.131 Problem 1 were read; p.131 was also rendered and visually inspected. The 1958 question allows the interval I_r=[-r,r]; modern EP1038 and this PR concern r=1. No all-r answer is certified by this review. The modern official page returned HTTP403 in the web tool; its wording was not pretended to have been freshly read there.

## Independent arithmetic and why it encloses the continuum

`check_certificate.py` is newly authored, uses only Python's standard library, and represents closed real intervals by integer endpoints over S=2^240. Inputs are exact rationals or decimal strings. It rejects float constructors. Products use all four corners, reciprocal excludes zero and rounds signed divisions outward, and squares crossing zero have lower endpoint zero. Integer square root is rounded outward.

Logarithms use exact power-of-two reduction to [1,2] and 96 atanh terms with the positive geometric remainder `2 t^193/(193(1-t^2))`. The same method encloses log 2. Exponentials scale to [0,1/8], sum through degree 60 and add `(v^61/61!)/(1-v/62)` before repeated outward squaring; negative values use reciprocal. All arithmetic and truncation errors stay in the intervals, including errors smaller than a lattice unit. No fixed epsilon padding certifies a value.

Ordinary floats propose root boxes. Before any Newton contraction, opposing endpoint signs and nonzero derivative signs are verified uniformly over the complete parameter slab, with the physical branch ordering checked. The mean-value identity justifies each parametric interval-Newton intersection. A poor float proposal causes a rejected slab or subdivision, never acceptance. First/second derivatives are ordinary derivatives, with product cross term 2f'g' and the correct implicit second derivative. The independent soft-series helper provides only value and **first derivative** enclosures; its placeholder second derivative is not used in any soft acceptance.

`check_block_certificate.py` adds a rational Machin enclosure for pi, sine/cosine Taylor remainders after validated reduction to [-4,4], and the actual interior sine maximum on (0,pi). Cosine is monotone on the used (0,pi) interval. The point sine routine also handles nX through n=80 by exact interval period reduction, so Fourier terms do not rely on machine sine. All reference square roots, logs, Poisson ranges, physical root sides, density positivity, denominators, adjoint mass and cap inequalities are checked. The source author's fixed decimal guards or parsed Arb/mpmath endpoints are not part of this acceptance path.

The h-function lower bound retains 80 nonnegative sine-square terms and subtracts the full rigorous tail `1/(2*80^2 X^2)`. Decreasing h is evaluated at an outward upper cap. In the affine regime the retained n=1 square is accompanied by a derivative test over all 32 closed rational mass-coordinate cells. In the constant regime the nonnegative square sum is discarded. These are lower bounds over the whole positive mass rectangle, not sampled block masses.

## Certificate 6.1: fresh full coverage

The newly accepted cover is:

| Region | Exact domain | Accepted finite slabs | Sufficient derivative bound |
|---|---|---:|---|
| Singular tail | 0 <= r <= 1/50 | One closed box | -0.788 < Lambda_r < -0.737 |
| Left bulk | 1/50 <= r <= 27/100 | 32 | Lambda_r < -0.0040994 |
| Convex tube | 27/100 <= r <= 28/100 | 2 | Lambda_rr > 3.8091 |
| Right bulk | 28/100 <= r <= 87/200 | 66 | Lambda_r > 0.0078791 |
| Regular soft | 1/10 <= q <= 6181/50000 | 77 | Lambda_q > 0.08106 |
| Final soft | 6181/50000 <= q <= q_s | 1 | Lambda_q > 2.4457 |

All displayed bounds are weakened outward summaries of the exact rational records, not acceptance inputs. There are 178 finite slabs plus the closed singular tail. Exact recursive rational subdivisions cover each range; explicit final coverage checks verify every endpoint and adjacent equality. The separate exact exponential comparison proves `1/10 < exp(-200/87) < q_s`, so changing charts leaves genuine overlap. The q_s endpoint has opposite exact signs at 0.123630684649383 and 0.123630684649384; strict monotonicity of `(1+q)d+2q log q` identifies its unique zero.

The r=0 tail uses q(0)=0 and the proved monotone bounds `q<=exp(-50)` and `q_r<=2500 exp(-50)`. The fixed z boxes include the regular limiting roots 1/2 and 3/2. Thus no positive unexamined cutoff stands in for zero.

The final soft slab is restricted to admissible q<=q_s even though its numerical enclosure extends slightly farther. Its lower y boundary is zero and its lower existence sign is the analytic identity `D(q,0)=(A-s)/s<=0`. Its positive upper sign and strictly positive D_y are actually checked. The conditions y>=0, 1-qC>0 and w<0.03 give the correct real deflation branch. No root is asserted for inadmissible q>q_s.

Opposite derivative signs are checked at dyadic points surrounding `r_c +/- 10^-30`, strictly within the convex tube. Strict convexity and the complete outer signs give exactly one stationary point and a global family minimum. Fresh width substitution gives

    1.834430475762661711090753635120553436511864256655884976379752017...
      <= L <=
    1.834430475762661711090753635129018849529897507462271417764406995...

The exact output rational endpoints, rather than these shortened displays, are compared with T. Their strict upper comparison passes. This is not just an upper witness or a sampled optimization.

## Certificate 7.1: fresh full reference and scalar cover

The fresh full generator accepted 627 finite parameter slabs plus the same separately verified closed singular tail. A subsequent exact replay recomputed **every** accepted slab, including uniform root validation, Newton contractions, all h sums, positivity/cap checks and affine mass-cell derivative tests.

| Reference | Exact covered parameter range | Slabs | Conservative strict surplus |
|---|---|---:|---:|
| a=1153/500-k/4 | 36/25 <= k <= 21/10 | 527 | >0.02674 |
| a=9/5 | 21/10 <= k <= 21/5 | 77 | >0.01728 |
| Zero platform, simple | 1/50 <= r <= outward upper rho(26631/10^6) | 16 | >0.00252 |
| Zero platform, refined | outward lower rho(26631/10^6) <= r <= outward upper rho(41542/10^6) | 7 | >0.03346 |
| Closed singular tail | 0<r<=1/50 | One box | >0.961762019209 |

These differ from both the original author's and the appendix's slab counts and margin figures. Only the smaller independently sufficient positive bounds above are accepted here. Exact records retain each margin numerator and denominator scale. There is no claim to recover the historical raw records.

For the finite references, C_eff(T)<0, positive adjoint mass, physical negative/ascending positive crossings, strict density positivity, and `0<Rmax<Qmax<pi` are verified uniformly. The exact comparison L<T makes checks at T conservative in the required direction: increasing the target increases C_eff and decreases the surplus. No lower bound on L is silently substituted for this upper comparison.

For terminal references, the algebraically canceled D, Qmax, Rmax and raw slope expressions were rederived from `raw=-uF_u`, `x_u=-H(1-u^-2)`, and `W=-(k+1)F`, with positive inverse-slope factors. They hold at every positive finite r; they are not limiting substitutions. Family minimality proves M0>=L, so C_eff=(L-M0)/R0<=0 can be discarded in this regime. Mere knowledge of a fixed-candidate upper bound would not justify that discard.

The terminal ranges intentionally overlap after conversion from exact rational q cutoffs. At q_cap=41542/10^6, fresh exact checks give g(q_cap)>0.372861191115 and k(q_cap)<21/5. Since g decreases and k' has the stated negative sign, and k(q)->infinity as q->0, these references cover every finite k>=21/5 with strict overlap. The affine range starts at 36/25<29/20; the finite ranges share 21/10. The earlier elementary argument covers 1<=k<=29/20.

In the complete singular tail, the canceled D expression is defined on the independent closed box and D<=0.038237980791. Actual r>0 implies D>0, hence `-log D>=1-D>0.961762019209`. Density positivity is proved by the monotone q(r)/r bound without dividing by an interval containing r=0. No finite reference at r=0 is asserted.

Conditional strictness is sound at this numerical interface: every nonempty target block has positive physical and adjoint masses; multiplying a positive normalized surplus by their product preserves strictness, however small they are. A finite sum therefore stays strictly positive. No uniform degree-independent excess is asserted, and no minimum block-mass cutoff is used. Whether the analytic reduction actually yields exactly this scalar with the claimed hypotheses remains for the independent analytic family/root to adopt.

## Reproducibility and adversarial controls

All complete family generations and all 627-slab block replays were run in normal, -O and -OO modes with explicit exception gates. Corresponding outputs are byte-identical across modes:

- Family output: 66,417 bytes; SHA-256 `05421b934948deca8ac912891a925334dcbe0f1ff743a65ff8f5384aa9bbd722`; 23,535,936 guard calls.
- Complete block replay: 189,370 bytes; SHA-256 `50c8abf776d7ea33d74b4627e5fadcea316690592079971406a53f86fc975ed7`; 142,301,611 guard calls.
- Exact oracle/control output: 159 bytes; SHA-256 `a4031fe58ea0313b8ec04c225b66975c019476bf92b728e2e4804ad6fd0371ef`; 95 exact-oracle checks, seven arithmetic rejections and eleven coverage/false-claim rejections.

The original fresh block-generation guard count is larger because it includes rejected adaptive proposals; the later replay's count does not count those failed proposals. The mathematical slab records are exactly equal. Extra explicit side/range and final coverage guards were added before final replays. The final code bytes and canonical outputs are sealed here. Finite primitive controls corroborate the written inclusion argument; sampling is never used to certify a continuum.

`verify_review.py` validates the seal, every private capture hash/Git identity, mode-output agreement, exact coverage and controls. With `--full`, it additionally regenerates the full family and recomputes every block slab in normal mode. It writes no files. Read `README.md` for commands and scope. This is ordinary mathematical and integer-computation evidence, not proof-assistant certification.

## Publication identity, deduplication and new primary lead

Before mathematical work, the numeric-gid Google Workspace CLI read all 43 columns: 191 rows at 2026-10-22T11:09:33.318800Z, SHA-256 `fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1`. A fresh 11:13:27.201550Z read was byte-identical and is retained in the compressed private capture. No exact problem/PR/digit/source alias row was found; semantic searches of the polynomial, potential, Tao/Wang, constant/theta leads produced unrelated results. This establishes a bounded current ledger observation, not permission to publish.

Wang's current primary result page still says **Proposed**, links a complete paper, source, verifier and Lean project, and credits the work to AI. It is a public prior full-solution claim with the exact target and numerical constant; absence of an authenticated DOI would not permit republishing it as a new result. This certificate review does not authenticate a Zenodo record or create a new tracker row.

A materially important additional primary source was recovered: **Tamás Darvas, Binghui Peng, Runzhou Tao, “A Solution to a Problem of Erdős–Herzog–Piranian”**, at immutable repository head `0804de278fdf1d355aea7b584ac5b67e0955f27b`, paper path `papers/erdos1038/Erdos_1038.pdf`. The primary README dates its addition to July15,2026. The exact PDF has 1,294,822 bytes, SHA-256 `c6baa6e345568142c00724079dcc5f4b1713ca191fad06fe82cba07842c667fa`. Its introduction and Theorem1.1 explicitly claim the same finite-polynomial infimum, indeed also all Borel probabilities, with D=1.834430475762661711090753635125... . AppendixC identifies three interval scripts and two symbolic verifiers, present under a certificates directory. The source credits GPT-5.5 Pro and says the authors verified/revised the argument. Runzhou Tao is a coauthor; he must not be confused with Terence Tao, whose earlier note is a separate cited antecedent.

Only the DPT introduction, theorem, relevant scope/approximation passage, AppendixC and bibliographic statements were read here; its entire proof and scripts were **not** accepted or executed. This is an authenticated full-prior claim and publication-accounting/priority lead, not an independent validation of that alternative proof or a certificate of chronological firstness. A narrow DataCite exact-title search returned zero matches; that cannot prove that no DOI exists. Root should reconcile this source, Wang's source and any current publications before choosing a single result-family record.

A secondary search result advertised DOI `10.5281/zenodo.19549033` as an EP1038 dataset. **The actual fresh primary Zenodo API record is a different physics position paper, “On Finite Execution and the Rate Limit of Nature's Laws: A Response to Gödel's ... (1949)”. That DOI is rejected as EP1038 publication coverage.** No unrelated DOI or a paper proving only a weaker numerical upper bound may be substituted for the full result.

Known aliases and the qualified no-row decision are recorded separately. No public-archive exhaustiveness, worldwide priority, first discovery, human peer review, or current community acceptance is claimed.

## Remaining parent gates and preservation

The numerical/certificate family identifies no remaining numerical objection within the written formulas and domains. Whole-solution acceptance still requires the independent analytic review and the root's adoption of all inputs, plus prior-publication/attribution reconciliation. In particular, this report must not be quoted as a proof of arbitrary-measure lower bounds, all-r EHP extrema, uniqueness of arbitrary minimizing measures, or a reproof of the external supremum theorem.

All source/ledger/PR bodies and the original page image are private research captures, ignored by Git, and explicitly marked private in the inventory. Authored code/results/report are confined to this dedicated folder; prior sealed reviews were not changed. No Git refs/index/branches, shared progress cursor, services, spreadsheet, DOI, upload, PR comment or outside communication was changed. Extensive AI assistance is disclosed; the package is unrefereed and has no formal proof-assistant certification.
