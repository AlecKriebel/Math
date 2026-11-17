# Actual primary interfaces — row 172 adversarial family

Written 2026-11-17 UTC, after the immutable 2026-11-16 23:58 UTC source-first seal. This is a check of the precise imported interfaces, not a claim to have re-proved the general theorems. Current root/peer findings and archived review opinions remain unopened. No peer coordination occurred.

## Raw custody and access

All eight bodies were already accessible in raw local caches. No GET, retry, bypass or new environment was required. Each was personally authenticated with SHA256, byte count and installed pdfinfo before reading. PDF metadata/printed arXiv headers, rather than cache directory names, establish the editions. Those authentication commands exited 0 without a reported diagnostic. Complete layout text extracts are stored here in `primaries/`; the corresponding `.stdout.txt` and `.stderr.txt` files preserve the literal empty extraction streams. The PDFs themselves remain unchanged at the absolute external paths below.

Let C be `/Users/alec/Documents/Math/draft_pr_claimed_solved_800_900_20261012/audits/pr888_30005079`.

| Raw relative path below C | Bytes | SHA256 | PDF pages / edition |
| --- | ---: | --- | --- |
| private_sources/miao_wang_optimal_v2.pdf | 538390 | 85285e55a256fe342d511f716530ed790801d695bdd5f21090ff9d56039b8049 | 32; arXiv:2401.13999v2, 13 April 2026 |
| private_sources/han_li_optimal_arxiv.pdf | 558188 | 939691d9bd0c24444f43b944b91c1ac9684fef628d3b23393cc7f6fd3b5db0ff | 48; arXiv:2009.01010v1 |
| private_sources/han_li_gytd.pdf | 641357 | cd44c6a91351619ffc41aae32bba1d144afb6f9eda11f4dbee74f3677502e9a6 | 61; author g-soliton PDF, metadata creation 21 April 2021; Corollary 31 / Proposition 32 numbering |
| private_sources/wang_zhu_toric.pdf | 221336 | 93aa63348add332cca1df8519bd864065f1956ae5f898e09065651d5f92245b1 | 15; 2004 author version |
| private_sources/owr2022_17.pdf | 1032709 | c997329409f016d06867ecc06dd38c59cea4919aa9ecf34791ed6a95f63345ec | 68; OWR 17/2022, Toric Geometry; PDF metadata 10 February 2023 |
| private_sources/BLXZ_2103.15278v2.pdf | 443588 | 8d56f0d92d9146ea85c53be8c04fc02e90f4b09a57fc3f591a996d1b040c1351 | 30; arXiv:2103.15278v2 header 16 June 2023, manuscript Date 21 June 2023 |
| priority_classical_01/private_tmp/li_li_2103.06439v6.pdf | 530713 | 067c12282bed8d0db4865b8b23d92304d16c444dcfeefe71dcde64864fd3459c | 39; arXiv:2103.06439v6, 1 June 2022 |
| priority_classical_01/private_tmp/miao_wang_2401.13999v1.pdf | 325579 | 56026b5035c471db53153c930fd2d100c227e94417a5674be44fe8833d78ec83 | 28; arXiv:2401.13999v1, 25 January 2024 |

Source URLs, identifying the bodies rather than asserting a fresh live-access test:

- Miao–Wang v2: https://arxiv.org/pdf/2401.13999v2 ; v1: https://arxiv.org/pdf/2401.13999v1 .
- Han–Li optimal degenerations: https://arxiv.org/pdf/2009.01010v1 .
- Han–Li generalized soliton author PDF: https://sites.math.rutgers.edu/~cl1412/papers/g-soliton.pdf .
- Wang–Zhu: https://maths-people.anu.edu.au/~wang/publications/2-AdvMath2004.pdf .
- OWR report: https://ems.press/content/serial-article-files/46955 ; DOI 10.4171/OWR/2022/17.
- BLXZ: https://arxiv.org/pdf/2103.15278v2 ; DOI 10.1017/fmp.2023.5.
- Li–Li: https://arxiv.org/pdf/2103.06439v6 ; DOI 10.1007/s42543-022-00054-0.

The native `source/SOURCE_MANIFEST.json` was opened only after INITIAL, for filenames, URLs, checksums and inspection locators. Its labels of what the old author inspected were visible; they were not adopted as evidence. No old audit judgment was read. Filename discovery also exposed other raw-cache filenames; those unrelated mathematical bodies were not opened.

## Critical interface reconciliation

### Miao–Wang: actual variety, divisor, shift and central pair

Personally read v2 introductory Theorems 1.2–1.5 and Corollary 1.4; Definitions 2.1 and the real-filtration construction; Theorem 2.14 and its global-valuative formulation; all of §3.1 through Theorem 3.2 and its proof; the local geometric formulas distinguishing exceptional E from strict transform H-tilde; and the immediately following smooth/GIT qualification where needed. The actual wording applies to every smooth curve in family 2.23(a), not merely an unstated generic curve. The note's smooth explicit intersection lies there by the independently frozen gradient and genus calculation.

The ordinary strict-transform valuation degenerates to the blowup of the projective cone over the smooth hyperplane quadric, leaving the curve fixed. This is precisely Z in the note, after a complex linear change of quadric coordinates. The primary local chart has u=sq, exceptional divisor q=0, strict transform s=0. This checks that the note uses the strict transform, rather than substituting the exceptional divisor of the original blowup.

The primary shifts the raw strict-transform order by discrepancy one, so its moment coordinate is k/m−1 on [−1,2]. The displayed two quadratic slice densities and the negative-exponential moment equation agree exactly with the independently reconstructed volume density in INDEPENDENT_RESULTS. Theorem 3.2 establishes weighted K-polystability for the unique candidate. Thus the imported factor result includes the needed central ring, parameter, klt Fano central variety and polystability; it does not transfer an unproved product-minimization claim into this note.

The page-12 density/equation/Theorem 3.2 were visually inspected in `primary-pages/mw12.png`, freshly rendered from the authenticated raw body at 140 dpi. The associated streams are retained. Its approximate numerical root is not used as proof of existence, irrationality or optimality.

### Wang–Zhu and Han–Li: sign and scale

Personally read Wang–Zhu Theorem 1.1, Lemmas 2.1–2.2, equation (2.16), and the surrounding moment-map/vector-field normalization. Wang–Zhu uses the positive exponential of its analytic vector field. Han–Li v1 Remark 2.45 explicitly uses the opposite sign and sets g_xi=exp(−<x,xi>); equations (110)–(111) give the matching weak metric equation and Ricci sign. Therefore the note's positive filtration parameter b is not to be negated inside the positive-weight valuation. The analytic Wang–Zhu field corresponds to the negative of that parameter in its convention.

The exact toric x-slice first moment is y/2 times the slice mass. Hence the note's one scalar equation annihilates both toric moments for (0,b); no untested transverse moment is omitted. Full two-dimensional covariance is positive definite because the polygon has interior. The solution is the unique toric candidate, and the smooth toric Fano existence theorem applies.

Han–Li physical/printed page 21 was visually inspected in `primary-pages/hl21.png`. The factorial convention MA_n=omega^n/n! differs from an unnormalized display by a positive constant volume normalization; it does not allow an affine character or a rescaling of valuation weights. The raw shift b*m and subtraction m(a+b) were independently checked before reading these bodies. They yield exactly a(k−m)+bj; a missing b*m would destroy the critical-point equation, as the frozen negative control shows.

### Real special degeneration and global competitor class

Personally read Han–Li v1 Definition 2.8, Remark 2.9, all of “Geometric R-TC I” and Lemma 2.10, the finite-embedding and rational-perturbation discussion; Definition 4.1 and Lemma 4.2; Theorem 1.5; Theorem 5.3 and its proof through the comparison with an arbitrary special configuration. Also read the corresponding BLXZ Definition 2.2 and its finitely generated associated-graded convention.

These are geometric real filtrations generated by finitely many section weights, not finite generation of the entire nonnegative cone of a dense ordered group. The note's Segre associated graded ring and an adapted common anticanonical Veronese embedding meet this interface. Restricting to a Veronese changes degree bookkeeping, not the valuation on rational functions or the canonical parameter per original anticanonical degree. The center is klt Fano with its anticanonical section ring, so the degeneration is special in the precise imported sense.

Han–Li Theorem 5.3 is a criterion for a special real degeneration to minimize the valuative functional when the induced central pair is weighted semistable. The converse proof compares with arbitrary special configurations. Theorem 1.5 then identifies that infimum with the infimum over all real valuations, including those not product-form or invariant. This closes the exact competitor-class gap that convexity of the two-variable product expression alone would leave. The statement at physical/printed page 33 was visually inspected in `primary-pages/hl33.png`; its proof and global comparison were also read in the text.

### Weak product equation and YTD hypotheses

Personally read the generalized-soliton author's setup, equations (4)–(9), Definitions 2–3, Theorems 6–7, Theorem 30 and proof, all of Corollary 31 and the statement/start of Proposition 32. The hypotheses are log/klt Fano geometry, a smooth strictly positive function on the moment polytope, and finite-energy torus-invariant potentials. In this application the twist and boundary vanish and g is an exponential, smooth and bounded above/below on a compact polytope. The factor pair from Miao–Wang is covered by BLXZ Theorem 1.3, read directly, which supplies a weak soliton for general log Fano triples, including singular Z. Corollary 31 supplies bounded relative potentials on a resolution; Proposition 32 supplies smoothness off the exceptional/singular locus. The latter page was visually inspected in `primary-pages/gytd19.png`.

On a resolution of Z times S, the sum of the two bounded relative potentials is bounded and psh in the product anticanonical class. The binomial coefficient cancels the factorials exactly: C(5,3)*3!*2!/5!=1. The factor Hamiltonians add for the canonical product lift. Thus the factor equations multiply into the product equation for the exact parameter already computed algebraically. Bedford–Taylor/non-pluripolar measures of bounded local psh potentials give no mass to analytic pluripolar sets; the klt canonical measure is locally integrable and has no mass there either. The identity on the regular locus therefore extends as the weak equation. This supplies an actual product soliton, rather than assuming an algebraic tensorization theorem for H-minimizers. BLXZ Theorem 1.3 returns weighted K-polystability, hence semistability, for this same triple.

### Absolute uniqueness and canonical steps

Personally read BLXZ Theorems 1.1–1.3, the definitions of h and beta-tilde, Theorem 3.15 and its proof, Lemma 3.16 and proof, and Corollary 3.17. Theorem 1.2 explicitly concerns the unique valuation itself, and identifies the Proj of its associated graded ring as the first center. Theorem 3.15 removes any ambiguity about uniqueness only up to a ray, an automorphism or an equivariant subclass. It applies to the same probability-DH-normalized, non-homogeneous valuative functional used by the note. The trivial valuation is included; the independently checked negative value excludes it. `primary-pages/blxz02.png` was freshly rendered and personally read. Since the first central triple already admits a soliton and is polystable, its polystable second step has the same underlying variety. No smoothness of Z was imposed by this theorem.

### Exact request and limited earlier credit

Personally read Blum's complete two-page OWR contribution, printed 888–889. The request is an explicit nontrivial first center, hopefully with a nondivisorial minimizing valuation. The actual text imposes neither a three-dimensional condition nor a product exclusion. The note's smooth fivefold, singular first center and rational-rank-two valuation address those literal requirements. This is not evidence of historical firstness or of present open status.

For the two explicit prior-credit sentences only, read Miao–Wang v1 title/header and introductory statements through its first factor-optimality corollary, and Li–Li v6 title/abstract plus §6, printed 35–36. The first edition actually bears 25 January 2024 and already states the threefold divisorial result. Li–Li actually provides two SO4 compactification limits, the first with a ray-form optimizer and the second with a two-component direction. Neither the decimal/numerical calculations nor absence of a direction-rationality proof in the inspected passage is promoted into a proof of irrationality or a new priority claim. The note explicitly withholds such a claim. No wider recent-literature or global priority search was performed or needed.

## Finite scope of this reading

The imported theorems remain accepted mathematical inputs, with their exact hypotheses checked against this example; they have not been independently reproved in their full generality. The local geometry, volume density, toric slice, exact moment identities, universal resultant proof, valuation/Segre construction, discrepancy and product-measure calculation were reconstructed before these foreign bodies were opened. Those actual derivations remain in the immutable INDEPENDENT_RESULTS.md.

All five selected primary-page renders exited 0. The BLXZ page-2 render emitted twice the exact diagnostic `Syntax Warning: Bad bounding box in Type 3 glyph`; its 98-byte stderr is retained at `primary-pages/blxz02.stderr.txt`. The displayed page was readable and its actual theorem text was personally inspected. The other render streams are empty. This is an honest reader limitation, not a failed scientific check, and no render was repeated to suppress it.

No original scientific program, support README, verification result, archived audit judgment or current peer/root finding was opened or executed. A native numerical run cannot strengthen the universal irrationality proof or close a missing stability interface. After the actual interfaces above were checked, such a run was unnecessary; scientific/native program executions remain zero. The extraction/render utilities are reader operations, with their literal streams retained, not scientific diagnostics or proof certificates.
