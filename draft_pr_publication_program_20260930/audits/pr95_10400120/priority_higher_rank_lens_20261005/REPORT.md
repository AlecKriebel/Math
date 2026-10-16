# Independent bounded priority audit: higher-rank lens formulas and examples

This family did not locate an earlier explicit counterexample satisfying the full ordinary invariant, equal fundamental group, unequal nonzero magnitude conditions in the primary sections examined. The strongest named lead, Hansen–Takata Remark 5.3(a), is not established as such a counterexample. Four exact reconstructions of its specified invariant give equal, nonzero magnitudes; two independently reproduce even the same complex value in the paper's orientation convention. This result removes that lead as demonstrated priority defeat, conditional on the printed formulas. It does not establish worldwide novelty or authorize publication.

## Claim, scope and independent obligations

The accepted parent gate identifies PR95 head `6534ad01e519c719628a18984b108e73cf2e8ead` and verifies the full ordinary SU(5) invariant at WZW level 5, shifted level 10. Its L(5,1) and L(5,2) examples have fundamental group Z/5 and positive unequal S3-normalized squared magnitudes `3475 + 1550 sqrt(5)` and `4025 + 1800 sqrt(5)`. This family's task is priority analysis after that mathematical closure, not a new proof of those values. The exact accepted gate is preserved as `ACCEPTED_PARENT_MATHEMATICAL_GATE.json`.

An older source would defeat the strongest first-counterexample claim if it supplies, or unambiguously establishes, the ordinary full quantum G invariant at a specified group and level for two manifolds with isomorphic fundamental groups, both invariants nonzero, and different absolute values under the same normalization. A general surgery formula, unequal phases, a projective category, a refined spin invariant, or two different theories at dual levels does not by itself meet that criterion. Formula antecedents nevertheless constrain any method novelty claim.

`INDEPENDENT_OBLIGATIONS.md` was written at 2026-10-05T20:48:13.856346Z, before any original `REVIEW.md`. No original `REVIEW.md` was opened in this family. Original budget 2/5 and zero new central PR95 proof-search turns were maintained. Computation was confined to validation of the designated old example. No ranks or replacement levels were scanned. All files created here, including the separately assigned adversary's files, stay in this dedicated folder. No Git, PR, external outreach, publication, preprint, upload, tracker or UI mutations were performed.

## The Hansen–Takata lead

[HT math/0209403v2](https://arxiv.org/pdf/math/0209403v2), printed p44, Remark 5.3(a), names the sl4 invariant with subscript 6 and the pair L(64,9), L(64,25). The remark concerns separation of complex invariants; it does not assert unequal absolute values. The PDF was authenticated at SHA256 `a00c189a481c1c7f5ccb14968e4d3b29abe7e560d3bb416f13ba56ae795e609e`, rendered and visually read at this location. This is not an OCR confusion between sl4 and Psl4 or between 6 and another subscript.

The same lead occurs already in [v1](https://arxiv.org/pdf/math/0209403v1), posted 30 September 2002 at 12:15:32 UTC. The specified v2 was posted 2 February 2003 at 04:35:03 UTC. The published 2004 journal version could not be retrieved from its correct publisher PDF endpoint (HTTP 403). No conclusion about an erratum, changed journal remark, or historical cause of the discrepancy below is claimed.

The paper's definitions give `r = m kappa`, with `m = 1` for A3 and quantum-group parameter `exp(pi i/r)`. Simples are the shifted open alcove in the full weight lattice. Thus this example is full ordinary SU(4), WZW level `k = kappa - h∨ = 6 - 4 = 2`, with the ten dominant weights `(a,b,c)` satisfying `a+b+c <= 2`. It is not a PSU(4) restricted category. The paper defines L(p,q) by surgery coefficient `-p/q`. Reversing this convention conjugates the values and leaves their magnitudes unchanged. Both lens spaces have fundamental group Z/64.

For A3 in long-root squared length 2 normalization:

- `rho = (3,1,-1,-3)/2`, with squared norm 5;
- rank 3, six positive roots, coroot-lattice covolume 2;
- both Dedekind symbols `S(9/64)` and `S(25/64)` equal `-63/32`.

### Exact direct formula

`ht_old_example_exact.py` specializes the first expression of Theorem 5.1, printed p39. It enumerates all 64^3 coroot classes in the simple-root basis

`nu = (a,-a+b,-b+c,-c)`

and all 24 Weyl permutations with their signs. With `z = exp(2 pi i/384)`, each signed term has the integer exponent

`18 q |nu|^2 + 6 <nu,q rho - w rho> - <rho,w rho>`.

The full signed histograms are preserved for q=9 and q=25. Reduction in the exact cyclotomic ring, using `Phi384(x) = x^128 - x^64 + 1`, gives the same polynomial for both:

`P = 6144 (z^27 + z^59 - z^91)`.

Exact multiplication by the conjugate gives `P conjugate(P) = 75497472`. The theorem's squared denominator is `4 * 384^3 = 226492416`. Consequently the squared magnitudes are exactly `1/3`, rather than a numerical closeness claim. The Dedekind and framing factors have unit modulus.

### Independent full modular surgery

`modular_old_example_exact.py` independently constructs the full ten-object SU(4) S and twist matrices in Q(zeta48), checks all 100 exact unitarity entries and obtains `S00^2 = 1/24`. It performs continued-fraction surgery for

- 64/9: `[8,2,2,2,2,2,2,2,2]`;
- 64/25: `[3,3,2,2,3,2]`.

After its explicitly stated framing correction, both positive-chain computations give

`(-zeta48^2 + 2 zeta48^10)/3`.

This uses the opposite orientation to HT. Its magnitude square is exactly `1/3` because `zeta48^8 + zeta48^-8 = 1`. A preceding floating diagnostic agrees to rounding error and is explicitly not used as the exact certificate.

### Independent adversarial reconstruction

The distinct child family `independent_old_example_adversary` was assigned to falsify the conversion, category, coroot lattice, cyclotomic reductions, phase and normalization. Its [report](independent_old_example_adversary/AUDIT_REPORT.txt) records two additional implementations that import neither local calculation script.

Its determinant-based negative-surgery calculation uses strict-coordinate subset labels and a generically constructed cyclotomic modulus in Q(zeta96). It verifies `S^2=C`, `S S*=I`, `(S Theta)^3=C`, actual surgery matrices, `Phi(U)=3`, and the exact value in HT's convention. Its second calculation uses Theorem 5.1's six-sine-product expression, a different unimodular coroot basis, and exact integer histograms in Q(zeta768). It checks 16,777,216 signed terms per q; even the unreduced histograms agree.

Both yield

`tau_6^sl4(L(64,9)) = tau_6^sl4(L(64,25))`

`= -(zeta96^12 + zeta96^28)/3 = -exp(5 pi i/12)/sqrt(3)`.

Therefore both squared magnitudes are `1/3`; since `tau(S3)^2 = 1/24`, both S3-normalized squares are `8`. These values are nonzero. The adversary found no defect in the supplied root lattice, level, exponents, covolume, normalization or cyclotomic moduli.

**Source discrepancy retained:** the printed assertion of complex separation conflicts with the paper's formulas and four exact reconstructions. We do not assert that this audit establishes an erratum or explains what the authors intended. Conditional on the specified printed invariant and formulas, this old example does not refute the magnitude conjecture. A different level or invariant would need its own sourced exact certificate; none was substituted here.

## Adjacent primary literature

`SOURCE_LEDGER.json` supplies exact URLs, version/publication dates, byte hashes, retrieval outcomes and read boundaries. `SEARCH_SCOPE.json` records 34 bounded queries, archived result batches, and limits of the local capture. Search snippets and secondary catalogues were only navigation aids.

[Hansen–Takata's 2002 conference paper](https://msp.org/gtm/2002/04/gtm-2002-04-006s.pdf), published 19 September 2002, already gives general higher-rank quantum lens formulas and asymptotics. Selected definitions, lens formula and theorem sections were read; a whole-text search did not locate the designated explicit pair. It establishes formula ancestry, not an examined explicit magnitude counterexample. The separate HT generalized-Gauss-sum work named as in preparation in the preprint references was not located by bounded exact-title/author searches; its publication status and contents remain unknown.

[Guadagnini–Pilo v1](https://arxiv.org/pdf/hep-th/9612090v1) reports numerical SU(3) agreement for lens spaces with p<=20 and shifted coupling 3<=k<=50. Section 5 describes the L(8,1)/L(8,3) and L(15,1)/L(15,2)/L(15,4) tables as phase distinctions. Selected table rows and all captions/claims used here were read, not every row of all tables. This finite numerical evidence is not a general proof and does not provide the specified SU(5) pair.

[Zhang q-alg/9612034v1](https://arxiv.org/pdf/q-alg/9612034v1), posted 29 December 1996 with a printed 1995 manuscript date, gives exceptional G2, F4 and E8 odd-root constructions and lens formulas, including squared-magnitude formula (14). All ten pages of extracted text were read. No explicit unequal nonzero pair or claim resolving the magnitude conjecture was located. No new pair was derived from that formula. The manuscript's request-only figures were not requested.

[Zhang–Carey, CMP 182 (1996), 619–636](https://link.springer.com/article/10.1007/BF02506419), was accessed via publisher metadata/abstract and selected cached PDF text of an author upload. That accessible text explicitly uses gl(r) for its A-series construction and excludes orthogonal spinorial analogues; its lens section supplies general recurrences. No explicit unequal nonzero pair was located in the examined section. Raw PDF retrieval from the author-upload URL returned 403; publisher PDF retrieval returned HTML, which is labeled as such in the ledger. Mathematical OCR is partly garbled, and this was not a full reliable read.

Takata's [1996 PSU(n) lens paper](https://www.worldscientific.com/doi/10.1142/S0218216596000497) was found at the primary publisher but its full text remained inaccessible. Its projective title cannot be promoted to a full SU(n) magnitude claim without reading the category and examples.

[Gang's 2009 v1](https://arxiv.org/pdf/0912.4664v1) gives general U(N) lens localization formulas and cites HT as the known formula source. Selected introduction, terminal lens derivation, discussion and references were read. Its v1 comparison assumes an unproved general-q sector sign. U(N) is not silently identified with full SU(N); v2 and the final article remain unread. No explicit matching nonzero SU(5) magnitude comparison was found in the examined sections.

[Kubo–Yokoyama's 2021 v1](https://arxiv.org/pdf/2108.09300v1) supplies SU(N)/U(N) matrix models and exact level-rank tables. The manifold parameter throughout the inspected definitions and tables is `L_b(n,1)` with q fixed to 1. Tables vary n and compare different level-rank theories, and include zeros. They do not compare the same-p pair L(5,1), L(5,2). Its spin, level and phase conventions require their own bridge before ordinary invariant values could be imported. Selected tables and discussion were read; later v2/final paper remain unread.

## Process evidence and limitations

Every mathematical calculation has actual exact argv, operator and child PIDs, UTC start/finish, exit, full stdout/stderr and executed script hashes in its `processes/*.json` record. The five exact/diagnostic runs are:

| Record | Operator / child PID | UTC interval on 2026-10-05 | Exit |
|---|---|---|---|
| `processes/ht_old_example.json` | 8492 / 8500 | 20:50:12.912445–20:50:20.787491 | 0 |
| `processes/modular_old_example.json` | 9860 / 9894 | 20:51:55.108758–20:51:55.150248 | 0 |
| `processes/modular_old_example_exact.json` | 11566 / 11574 | 20:53:51.381441–20:53:51.444312 | 0 |
| `independent_old_example_adversary/processes/independent_surgery.json` | 17047 / 17055 | 21:00:43.673213–21:00:43.790729 | 0 |
| `independent_old_example_adversary/processes/independent_sine_product.json` | 18395 / 18403 | 21:02:31.042714–21:02:31.569701 | 0 |

The direct histogram and exact modular calculations used standard Python integer/Fraction arithmetic. Floating values in the direct script are display diagnostics and are excluded from its exact certificate. The adversary preserves executed bytes separately and records NumPy 2.3.5 for its integer sine-product computation. Source PDFs, extracted text and rendered pages are private local evidence, not publication assets.

`PROCESS_LIMITATIONS.md` discloses two initial failed extraction launches: a nonexistent bundled pdftotext path raised before a child launched; complete error traces are in the tool transcript, operator PIDs were not captured. They performed no mathematical calculations. Successful extraction reruns and all calculations have complete records. The initial runner's earlier version was replaced with a launch-error handler; it was not separately pinned, while every calculation script is pinned and remains unchanged. Early web outputs were not all separately archived on disk; the query ledger distinguishes this from calculation capture. The first integrity-verifier run also failed because it treated documentary copies of process JSON as fresh executions and expected duplicate stderr files. Its exact source and failure streams are preserved; the verifier now checks the two actual process directories. No mathematical calculation failed. Bibliographic cross-checks corrected the GP journal volume/pages/DOI, removed an unsupported Zhang journal attribution and unverified Takata pages, and distinguished Ohtsuki volume label 2002 from actual publication 1 June 2004.

## Bounded priority verdict and exact remaining gap

**This family finds no established earlier full magnitude counterexample in the examined primary sections. The named HT old example has verified equal nonzero magnitudes. Method novelty must acknowledge decades-old higher-rank lens surgery formulas. First-counterexample priority and worldwide novelty remain unestablished. No publication clearance is given.**

The specific remaining gaps are the historical cause of HT Remark 5.3(a)'s conflict, the inaccessible final HT journal text/any erratum, Takata 1996 full text, the unlocated HT Gauss-sum follow-up, a reliable full Zhang–Carey source, unexamined sections and later corrected versions of the later papers, and literature beyond this bounded family search. These are access/priority gaps, not transferred mathematical proof obligations or evidence that an older counterexample exists. The original conjecture/history family remains independent and supplies its own adjudication.

Closure consists of this report, ledgers, all calculation/source bytes, full process captures, the separately sealed adversarial packet, `INTEGRITY_CHECK.json`, `CLOSED_MANIFEST.json`, and `CLOSURE.json`. The manifest covers every file recursively except itself and the final closure record, whose hashes are linked from `CLOSURE.json`. The research log's 100% estimate denotes completion of this bounded audit, not mathematical novelty or publication approval.
