# PR 378: source and effective-range audit

**Scoped mathematical PASS for Turn 1 and its source/coordinate qualifications. Full executable and wrapper replay PASS with source verification explicitly omitted. No mandatory correction found within this audit.** The original all-arrangement claim remains unproved by this packet. This conclusion does not certify historical novelty, present global open status, human peer review, or acceptance.

Frozen head: `5da73632ab7a621de7b62edb5f70dfb8017e4a50`. All 47 files in `snapshot_manifest.json` match their frozen size and SHA-256. No candidate, root, historical, or other family artifact was changed. No Git/index/service write or outreach occurred. The special-arrangement proofs and fractional-cover proofs are assigned to other independent families; their numerical receipts were replayed here, but this report does not substitute for those proof audits.

## Source-first record and semantic target

Before candidate or old-review reads, I fetched, read, rendered and inspected the complete literal Szemberg contribution at printed 3295--3297. Its displayed conjecture on 3297 is epsilon(P^2,O(1);Z)=1/k with k the maximum collinear subset of Z over **all projective lines**. The complex-field setting comes from the contribution's surrounding context and cited primary paper; reduced distinct lines and nonempty finite Z are necessary conventions rather than an explicit full hypothesis list in that one-sentence conjecture. A pencil with at least two distinct lines has r=k=1 and epsilon=1. A single line gives empty Z and no 1/0 target. Report/workshop year 2019 is distinct from EMS publication on 19 November 2020. [Literal report](https://ems.press/content/serial-article-files/46833), [publisher dates](https://ems.press/journals/owr/articles/17296).

Pokora's v3 Question 3.1, page 6, instead defines its maximum over arrangement components. That formula is potentially stronger, and no equivalence of the two maxima is assumed. The paper explicitly works over C. Its arXiv v3 date is 7 October 2018 and displayed manuscript date is 9 October 2018; its journal citation is from 2019. [Primary v3](https://arxiv.org/pdf/1711.09364v3), [version history](https://arxiv.org/abs/1711.09364).

The CMI Hanumanthu--Roy--Subramaniam manuscript is dated 19 July 2024; Question 1.1, page 2, uses maximum points on a line, excludes pencils, and works over C. Its presentation is historical evidence about the question's scope, not a current completeness search. [Primary manuscript](https://www.cmi.ac.in/~krishna/sc-curve-config.pdf).

The candidate source gate accurately distinguishes these formulations, cites the historical workshop announcement through 12 lines, credits standard families, and disclaims a full resolution. The Harbourne--Roe reference gives prior work on estimating generic-point constants by excluding abnormal classes; it is method background, not a direct proof for every specified arrangement or the exact Turn 1 algorithm. [Primary prior paper](https://arxiv.org/pdf/math/0309064). I have not certified the candidate's search-history statements, campaign-alias searches, present literature completeness, or novelty.

Independence is explicitly bounded: the assignment disclosed PR/problem identity, mechanism labels, source URLs, head, and claimed replay totals 214070/93918. The independent source reconstruction, code and complete new control output were hash-sealed before any candidate, old-review or family-verdict content. `SOURCE_FIRST_SEAL.json` preserves v1 unchanged. `SOURCE_FIRST_SEAL_V2.json` seals a pre-candidate correction of two prose typos (2850 grid cases and r=8<k^2=9). This is source-fresh semantic/mechanistic reconstruction within disclosed scope, not fully blind discovery. The exact-minimum argument below was checked after reading the candidate; the original sealed reconstruction independently derived the finite decision reduction.

## Independent reconstruction and candidate comparison

For any nonempty finite point set, a line attaining k gives epsilon<=1/k, and no line can violate that bound. If an irreducible reduced degree-d curve violates it, d>=2, 0<=m_i<=d and M=sum m_i>=kd+1. The upper multiplicity bound also follows by intersecting with a general line through the point. The genus inequality is

    sum m_i(m_i-1) <= (d-1)(d-2).

It is valid for arbitrary singularities, including nonordinary ones, and for m_i=0 or 1. One may prove it from the integral strict transform and adjunction, as the candidate does, or from delta-invariants and nonnegative geometric genus. Infinitely near singularities and additional singularities do not weaken the inequality. Arrangement multiplicities must not replace the test-curve m_i.

My independent argument balances integer multiplicities. For M=qr+s, 0<=s<r, the minimum quadratic cost is g_r(M)=r q(q-1)+2qs, which is nondecreasing. Thus all violating degrees satisfy

    (k^2-r)d^2 + (2k+3r-rk)d + 1-3r <= 0.

For 0<r<k^2, let A=k^2-r, B=2k+3r-rk, C=1-3r. The independently reconstructed cutoff is

    D0=floor((-B+sqrt(B^2-4AC))/(2A)),

computed exactly with `isqrt`. The candidate uses D=max(ceil(r/(2k)),D0), a valid possibly larger cutoff. Its monotonicity substitution is used only once M>=r/2 has been ensured. There is no hidden use of that substitution at small M. Its coefficients, root floor, and positive-tail argument are correct.

The algorithm is a terminating exact specification under an **explicit exact field K contained in C with exact arithmetic and decidable equality**. Algebraic coordinates, represented exactly, suffice. Some effectively presented transcendental extensions also suffice. Numerical approximations or merely computable complex numbers do not suffice uniformly: equality to zero is undecidable for their general approximation representation. Candidate Turn 1 states the needed exact-field hypothesis; the shorter final summary is read under that definition. No polynomial-time complexity is claimed.

Pair-line enumeration computes k over all C-lines: any line containing at least two K-points is their K-defined join. For each bounded degree and multiplicity vector, chart Taylor conditions form a finite homogeneous linear system. Its rank is unchanged under extending K to C. Consequently there is no missing complex-coefficient or irreducibility oracle.

A reducible/nonreduced polynomial with total multiplicity T decomposes additively across components, and degree/T is at least one component's ratio. Therefore every tested d/M with a nonzero kernel is an upper bound for epsilon even if actual T>M. Conversely every violating integral curve supplies its true genus-admissible vector, with degree bounded by D. These true ratios belong to a finite set, so their infimum is attained and included. Taking the minimum of 1/k and all nonzero-kernel candidate ratios therefore yields the **exact epsilon**, as claimed. It is not merely a threshold decision. The genus screen is asserted only for irreducible true witnesses, not arbitrary reducible forms; that distinction preserves completeness.

## Adversarial controls and exact gap

The equality boundary r=k^2 is outside the candidate's certified range. For k>=4, the remaining linear coefficient in the genus quadratic is negative and yields no uniform degree cutoff. The exact controls include r=16,k=4,d=4t,m=(t+1,t,...,t), where M=16t+1>kd and the genus inequality survives for t=1,2,10,100,1000 (indeed every t>=1). These are necessary numerical classes, not constructed curves. Small equality cases can behave differently; the strict range is a sufficient regime, not a complete classification.

The sealed new code uses only standard-library rational arithmetic. Full projective incidence lists, actual jet matrices, row reductions and nullspaces are retained in `independent_full_output.json`; no output is reduced to a count. Its nine controls include pencils/single-line boundaries, a triangle, a five-line arrangement, seven conic points plus one off-conic point, a genuine nodal cubic order-two condition, and a reducible xy condition that fails the irreducible conic genus bound. The conic countercontrol has r=8,k=3,D0=2, eight seven-point tests and exactly one nonzero kernel. It demonstrates a violating 2/7 polynomial for an arbitrary point set, while making no arrangement-singular-set claim. A 2850-case exact cutoff grid through k=20 verifies root and integer-genus relations. All stored nullspace vectors are checked by exact matrix multiplication.

The strongest verified research statement in this family is the exact finite Seshadri computation for supplied exact-field points with r<k^2. The remaining original gap is a uniform arrangement argument: no theorem here shows all arrangement singular sets lie in that range or makes all finite tests negative. Necessary multiplicity feasibility alone is not curve existence. The original remains unresolved **by this packet**.

## Complete replay and binding semantics

A private runtime used Python 3 and SymPy 1.14.0. Every executable was inspected before running; all snapshot files remained unchanged. The complete stdout and stderr of each run are retained privately under `private_replay_outputs/`, with hashes and all parsed fields in `replay_receipt.json`.

- `check_turn_1.py` through `check_turn_5.py`: every complete stdout byte-matches its frozen JSON, including ranks, deficient subsets, incidence counts, certificate branches, sample ranges, examples and scope text. Their assertion counts are 29137, 245, 17734, 35371 and 131583.
- `REPLAY_ALL.py`: complete output is `{"all_receipts_byte_exact": true, "assertions": 214070, "manifest_entries": 62, "source_files_checked": 0}`. The 62 entries are repeated historical/final manifest entries, not 62 unique files.
- Old `review/independent_checks.py`: the **entire** 2348-byte JSON stdout equals `INDEPENDENT_CHECKS.json`, not merely its 93918 total. The 38 scope counts, 21320 cutoff cases, branches, geometry records, q<=2 all-line limitation, deletion count and final scope all match.
- Old `review/verify_review.py --author-dir ...`: verifies its review-manifest bindings, pinned author manifest, 36 stored author-file/blob bindings, complete author receipts and old independent receipt. Complete output is `{"author_assertions": 214070, "independent_assertions": 93918, "review": "PASS", "source_files_checked": 0, "source_note": "Raw source files absent; source verification explicitly omitted"}`.

The wrapper's historical `REMOTE_BINDING.json` binds author commit `dd1736df47b536de489f8e5a651f22a1ebca6205`. Its recorded Git blob hashes recompute correctly from the frozen author bytes. This is local replay of stored bindings; no fresh remote-fetch claim is made. The 47-file freeze independently binds the reviewed files to the assigned later head.

The snapshot has no `sources/` directory. Therefore the six-file source-validation branch was **not executed** and the historical `AUTHOR_REPLAY.json` with source_files_checked=6 is not reproduced verbatim. Both wrappers accurately emit zero and disclose omission. Separately, freshly fetched OWR, Pokora v3 and CMI curve-config PDFs match their three candidate source-manifest sizes and SHA-256 values. The old screenshot and two other source PDFs were not verified in this family. No absence is promoted into successful validation. Source copies, renderings/extracts and the private runtime are excluded from the public allowlist.

Completion estimate: 100% of this scoped source/effective/replay audit, pending independent adversarial sign-off by the coordinating audit. This percentage is not completion of the mathematical conjecture. No full-conjecture percentage is inferred from finite checks.
