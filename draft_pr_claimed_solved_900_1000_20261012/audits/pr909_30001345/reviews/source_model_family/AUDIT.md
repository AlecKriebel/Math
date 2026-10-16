# Independent primary-source and exact-target audit

## Result

**PASS WITH EXPLICIT SCOPE.** No source-model counterexample to the frozen theorem was found. It addresses the unrestricted, summed rough-invariant reading of the original OWR questions. It does not address the explicitly parametric Conjecture 3.8 of the 2014 article. This is a target-fidelity judgment, conditional on the separately audited construction and calculations, not a novelty judgment.

The source questions do not spell out a summation convention or resolve every possible implicit intention. The full contribution strongly supports summing the nearby singularities: the next page introduces every nearby singular point in a fixed ball and then compares their sum with the central invariant. The candidate expressly states this interpretation and declines to infer unstated author intent. Thus it has not silently replaced a stated unibranched problem with a multibranch one. Any title, status field or publication that omits this qualification would make a materially stronger claim than this audit accepts.

## Exact identity and independence

Target: problem 30001345, OWR-4086-003, draft PR909. Frozen head supplied in preflight: d186dea31791cd3e8acf6829e0b65d01849623b8. Independent on-disk hashes agree:

- Imported statement SHA256: 04659a41696199fa4b3ea5b3ee9856b6360bdee29908ab8d7629e3c3fefce28d.
- Imported raw review SHA256: a431e9225db12e6062fdd887fd74d3b67edfcc990e85d6fd4f2972b5c09c90fb. Recomputed as SHA256 of `json.dumps([raw["problem"], raw["prior_research"]], sort_keys=True).encode()` with Python default JSON settings. The wrapper-file hash is different and is not substituted. The parent supplied this canonicalization after a first unsuccessful search among object encodings; the arithmetic was rerun here against the actual raw record.
- Frozen proof SHA256: 561b189c2091eaeccccf89fdd933b2300ec676a871d7229ebfaf8c806962fe8b.
- Original package manifest SHA256: a8376fa67c497c4b31522364ac87163cdd6f5ec42961893981c44f0d95f0ee02.

The assignment disclosed the proposed geometry and scope. I read the imported record and authenticated the primary-source assumptions, then wrote SOURCE_MODEL_PRE_CANDIDATE.md before opening frozen_v2/PROOF.md. No candidate audit verdict was read. The original frozen source manifest was inspected only afterward to compare retrieval fingerprints. This was independent derivation of source scope, not a blind review of an unknown proposal. The current branch was read-only confirmed as main. No original, index, Git, PR, Sheet or publication mutation was made.

## What the complete sources establish

### Original report

The official EMS report is volume 6 (2009), report 43/2009, published 30 June 2010. The contribution begins within printed p.2446 and ends with references at the top of p.2448; the following Cadman contribution is separate. Full pages and transitions were inspected.

Visual inspection confirms that Definition 1 and Questions 2-3 use a **barred** invariant, with displayed value K(K+D). The imported plain M loses this typography; the proof restores it. The initial germ and questions have no explicit irreducibility or one-branch assumption. Parametric codimension motivates the question, while fixed local geometric genus/delta constancy motivates Question 3. Proposition 5 subsequently imposes one branch for its signature estimate; the later cusp/node assumption serves the estimate. These are not stated antecedents of Questions 2-3. The candidate does not claim to satisfy them.

The report prints a fine-invariant formula with +N². The journal version uses -N². This source discrepancy must not be silently normalized when quoting the old report; it does not affect this construction because only ordinary points with N=0 occur.

### Published 2014 article and the current arXiv version

The Osaka institutional record identifies the journal PDF as the Version of Record, 51(3), July 2014, pp.573-583. The full mathematical body, definitions, conjecture and later theorem assumptions were read. Section 2 requires flatness, a fixed transverse ball and central locality. Definition 2.1 distinguishes rationality from unibranchedness: parametric requires both. Definition 3.3 permits multibranched germs; Remark 3.4 changes another multibranch normalization by branch count minus one. Definition 3.5 specifies fine versus rough; Conjecture 3.8 explicitly restricts the summed inequality to parametric deformations. Assumption 5.1 also requires a cuspidal central singularity for the later signature theorem.

Current arXiv is still v3, submitted 24 September 2009. On this retrieval its current and versioned PDFs are byte-identical. The preprint uses Definition 2.2 for parametricity and Definition 3.4 for the fine invariant. It lacks the journal's Remark 3.4 and Conjecture 3.8. A citation to arXiv v3 cannot by itself authenticate those published additions. Its general deformation condition D1 explicitly permits a bunch of disks.

### Classical arrangement attribution

Roulleau-Urzua, Annals 182 (2015), pp.287-306, Proposition 3.1 and its complete proof on pp.291-292, give the same dual Hesse divisor, nine lines and twelve 3-points. Their p.290 convention defines k-points by distinct local line directions, so these are ordinary triple points. The candidate equation differs only by factor order and an overall sign, hence defines the same divisor. The acknowledgements call Proposition 3.1 classical and credit Comessatti, citing [CC93, §2]. This authenticates the attribution and warns against claiming arrangement novelty; it is not a completed priority investigation.

## Adversarial scope tests

| Possible substitution | Test and result |
|---|---|
| Fine invariant substituted for source rough invariant | No: old displayed K(K+D) and visible bars agree with the candidate definition. Ordinary points also have N=0. |
| Orevkov's multibranch shift silently adopted | No: the proof uses the displayed rough invariant. The branch shift is acknowledged as a different convention. |
| Summed invariant substituted for a single marked section | Explicit choice, supported by subsequent full-source setup. The local value on any one moving triple section is 1, so this is **not** a marked-section counterexample. |
| Multibranch family substituted for a stated unibranch target | No explicit unibranch requirement occurs in OWR Questions 2-3. Yes, such a substitution would fail for published Conjecture 3.8; the proof excludes that claim. |
| Positive genus or changing normalization components evades delta constancy | The proposed family has nine normalized disks both centrally and nearby, total delta 36, and a common boundary link. It passes the rational convention; it fails unibranchedness. |
| Signature/cusp restrictions ignored | Those estimates require later additional hypotheses and are not used or contradicted by the construction. |
| Isolated bare question relied upon without source context | Full OWR contribution, adjacent transitions, and full relevant 2014/arXiv mathematical bodies were read. |

An independent invariant check helps separate the conventions. One blowup of an ordinary r-point (r>=3) gives E²=-1, E.C'=r, K=E and D=C'+E, hence K(K+D)=r-2. The relative divisor is nef on the only exceptional curve because (K+D).E=r-2>=0; its negative part is zero. Therefore the rough/fine sign issue cannot turn 7<12 into a noncounterexample. Under the alternative branch-shifted convention the ordinary-point values would be 2r-3; its total also increases (15 to 36), but that is an observation, not the theorem being audited.

The genus language deserves care. Topological genus of the normalization is zero for all these fibers; the singular curve itself has nonzero first Betti number. One must not use the cusp/node formula b1=2g+R for this nine-boundary, multitriple example. Neither delta constancy nor genus zero alone implies the central fiber is a disk.

## Accepted wording and remaining gap

A suitable theorem-level statement is: the total of Borodzik's displayed rough invariant K(K+D) need not be upper semicontinuous in reduced delta-constant plane-curve deformations with a multibranch central fiber, even with nine normalized disks and a fixed transverse boundary link. This gives a negative answer to the unrestricted literal **summed** formulation in OWR Question 3. It leaves the explicitly parametric Conjecture 3.8 untouched.

The frozen proof already maintains that scope, so no mandatory mathematical wording repair was found in it. Retain those restrictions in the abstract/title/status and avoid saying that the author's intended parametric problem or all M-number conjectures have been solved. If discussing the old fine formula, record the printed sign discrepancy. If identifying the journal conjecture, cite the 2014 version rather than pretending it appears in arXiv v3.

There is no source-model mathematical gap left for the scoped claim. The irreducible/parametric problem, historical intention, and priority of this multibranch observation are outside the accepted result. No in-depth priority search was performed.

## Access and reproducibility limits

Raw PDFs, HTML, extracts and renders remain exclusively in ignored private_sources/. SOURCE_MANIFEST.json records actual URLs, times, byte counts, hashes, page scope and inspection methods. Poppler 26.08.0 extracted text and rendered pages at 110 dpi. The Osaka font encoding corrupts extracted symbols and bars; visual pages 575-577 resolved them. Rendering emitted Type 3 glyph bounding-box warnings, but the inspected pages remained legible.

Two fresh Osaka downloads have different hashes: 2b1e4f05cbab8bf2756e1e91851d35238cdbc3e35d0ffe1747d986568bc1f0ef and 59d404d7b2219276f5fd8313401ee9e9b9336af22d405a41079aeeca533bfd53. Both are 379471 bytes; the 31 differing bytes are within positions 379410-379441 of the second trailer /ID entry (zero-based). Extracted layout text is identical. They are **not byte-identical**, and neither is asserted identical to the original candidate's differently hashed downloads. The OWR and Annals bytes here exactly match the frozen manifest's saved-source fingerprints.

Primary links: [OWR record](https://ems.press/journals/owr/articles/4086), [OWR PDF](https://ems.press/content/serial-article-files/46242?nt=1); [Osaka record](https://ir.library.osaka-u.ac.jp/repo/ouka/all/50809/), [Osaka PDF](https://ir.library.osaka-u.ac.jp/repo/ouka/all/50809/ojm51_03_573.pdf); [arXiv v3](https://arxiv.org/abs/0907.4129v3); [Annals record](https://annals.math.princeton.edu/2015/182-1/p06), [Annals PDF](https://annals.math.princeton.edu/wp-content/uploads/annals-v182-n1-p06-p.pdf).
