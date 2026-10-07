# Review 02: independent priority, publication eligibility, and metadata scope

## Verdict and limits

**Scoped PASS: no substantive priority, attribution, scope, or metadata defect found in the frozen-v2 candidate.** The publication is eligible as the expanded attributed consequence and verification note actually described in the title, abstract, README, and metadata, provided the independently assigned mathematical reviewers validate the positive Bernoulli cost input and the direct calculation. This is not a mathematical certification of the upstream lower bound and not a certificate of global first priority.

The simple cost-limit proof and its counterexample target were already literally public in the author's preliminary triage. The frozen note says so. Its separately written, cost-independent cellular proof is materially different from that publicly recorded argument and adds a checkable proof of the exact presentation's asphericity and all-degree vanishing. That constitutes actual extra proof content under the original request. It does not establish priority for either the fixed-price construction or the relation-level counterexample. Methods and consequences remain largely classical.

No candidate file was changed. No external individual was contacted. No Git operation, remote deposit, tracker mutation, upstream mutation, comment, issue, release, or other publication action was performed. Prior complete-package reviewer verdict files were not opened or used. The requested priority audit and dated addenda were examined as source material; they were not accepted as certification.

## Exact candidate and source identification

The review was against `/Users/alec/Documents/Math/openai_followon_cost_betti/verification/frozen-v2`, original project `REQUEST.txt`, and root `/Users/alec/Documents/Math/AGENTS.md`. SHA-256 values:

| Frozen candidate file | SHA-256 |
|---|---|
| `publication/main.tex` | `7475979d063f5ad6e9e85f09fca5eca6f1beb83a83f654bc9011854dc8c4182a` |
| `publication/paper.pdf` | `d2af46715d94a23d4c51b25a4b78e5e2dab64cd7cae3fa61f2349194e5fc6f75` |
| `publication/README.md` | `8d6624ff1ef3030a50ea94fb8b346d2e70d4fa234b17ea398fcb700c50adcdba` |
| `zenodo-deposit.json` | `2c8d034e5ab30787c747b8e9bb195f332cd6a63f421147a8e2656cd1d39ae4de` |
| `publication/cost-betti-source-and-verification.zip` | `d88ca91ab6d75388f61e5103c7f4a189fe3bab4a7349312313e4d06ea3a72d8b` |

`local_read_manifest.json` identifies 31 locally inspected instruction, frozen-package, priority, upstream, companion, and license-practice files with hashes. `fetched_source_manifest.json` identifies independently fetched primary documents, versions, retrieval times, hashes, and byte counts. `archive_priority_manifest.json` pins the priority records actually bundled. `search_coverage.json` records the new web queries and local corpus searches. Inspection copies in `primary_sources/` are ignored and are not a publication supplement.

## Public disclosure reconstructed from sources

1. **Classical target and reduction.** Gaboriau's [published 2002 paper](https://numdam.org/item/10.1007/s102400200002.pdf), Corollary 3.16, printed p. 126, identifies all group and relation Betti numbers for free probability-measure-preserving actions. It imposes no ergodicity condition. Corollary 3.23, p. 128, is the relation inequality `Cost(R)-1 >= beta_1(R)-beta_0(R)`; the question immediately follows on p. 129. His [FAQ](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/FAQ.pdf), p. 1, gives precisely the corrected relation-level equality. These are exact numbered statements, not abstract-based inferences. The inspected journal PDF hashes to `7a9bc905ccda760eb2e214ed37cea28c1842bfad60369f1e1926767846ce70ae`.

2. **Fixed-price implication already explicit by 2018.** [Popa–Shlyakhtenko–Vaes arXiv v1](https://arxiv.org/pdf/1811.06929v1), Remark 6.6, spans printed pp. 24–25 and expressly links a fixed-price counterexample with a cost–Betti counterexample, using agreement of Betti numbers under the relevant extensions. Its [submission page](https://arxiv.org/abs/1811.06929v1) records November 16, 2018, 17:24:26 UTC. This primary version, independently fetched, hashes to `ee3ce3ec22323c8a8cdbd3cb2b79737528b841f7d6c11b14b6787de916929490`. The manuscript's attribution to PSV Remark 6.6 is supported; no new logical bridge is present.

3. **The precise group/actions/cost bounds are upstream.** OpenAI family 259's introduction defines `Gamma=A*_J(J x <t>)`, `w=ab_1ab_2...ab_99a`, the Bernoulli action and height actions, and Theorem 1.1 supplies both cost bounds with `K=e^96 96^99/95^95`, `alpha<1/200`, and `K alpha^3<1/2`. `group-actions.tex` establishes the factor embeddings and free/p.m.p. properties. `finite-models.tex`, section 5.2, proof of `models:sequence`, lines 222–229 in the pinned source, already proves that `a,u_1,...,u_99` is a free basis. The frozen note explicitly recalls and cites that observation. It does not present a new group, new action, new basis, or independently proved positive cost estimate.

4. **The exact short cost-limit argument was publicly recorded.** The [pinned preliminary audit](https://github.com/AlecKriebel/Math/blob/387962dc519c86b1d1833cb0a41bd3fbddd2b446/openai_followon_triage_20261006/agent_notes/physics_operators_topology.md), line 83, explicitly states `0<=beta_1(Gamma)<=99/M` for every `M`, the limit to zero, transfer to `R_X`, the zeroth correction, and the infimum-group-cost boundary. The [triage report](https://github.com/AlecKriebel/Math/blob/387962dc519c86b1d1833cb0a41bd3fbddd2b446/openai_followon_triage_20261006/REPORT.md), section 7, names the exact target and mechanism. I independently retrieved both pinned public files. Their hashes are respectively `3d53ae0ce77a5d40a657b9695d91ce87b1b08b5eeeef6d085731bd8f4d58d3cf` and `ce51a397fb83f6debe0c6540d2060d61d1e07b615caf25e73cb8ddebb6d77789`, matching the package audit's recorded copies. The triage is conditional on the upstream input surviving validation, but it is still prior disclosure of the complete short conditional proof.

5. **Current upstream version.** A new read-only GitHub `commits/main` fetch and family path-history fetch each give only `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, with commit timestamp October 6, 2026, 21:58:50 UTC. The independently fetched current introduction and finite-model source are byte-identical to the pinned local source, with hashes `6cbfa027e1ddc3efc5dd435347c76c0003f67551749931cf21763e3282cfa1bc` and `84ad9737399e3c4b1ddc0101e18922dcc8dd3cf5b8543cf7391e4993715c21f8`. No later correction was detected in these checked channels. The manuscript's October 5 date is not evidence of public release on October 5; the frozen note correctly distinguishes date and October 6 public version. Git timestamps are not exact proof of when a repository was made public. The source's `INPUTS.md` warning about an intermediate argument is accurately preserved and not converted into a claim of final upstream certification.

## Companion and citation-chain checks

The upstream catalogue has exactly one family-259 manuscript. Searches of all `.tex`, `.bib`, `README.md`, and `INPUTS.md` files for the identifying `b_99`/`b_{99}` or rank-100 amalgam wording locate only that family's introduction, group-actions, finite-models, and scope files. A separate Gaboriau/fixed-price corpus search identifies adjacent percolation and unitarizability papers; their introductions and relevant bibliography entries discuss earlier cost/Betti applications, not this group-specific computation or strict example. The free-uniform-spanning-forest bibliography cites Lyons's 2013 contribution on Betti numbers, cost and FUSF, again as background. No family-259 companion containing the direct computation was identified by the corpus or catalogue.

The upstream bibliography's current fixed-price sources were independently checked as primary manuscripts and version records:

- [Khezeli v4](https://arxiv.org/pdf/2509.08325v4), Theorem 1.1, proves fixed price one for products of two infinite countable groups. The version record remains January 4, 2026. It is a positive result and does not give the target strict example.
- [Slutsky v1](https://arxiv.org/pdf/2607.20273v1), Theorem 1.1, gives a product-neighbourhood criterion for fixed price one; Corollary 1.8 gives first-Betti vanishing for those positive cases. Its version remains July 22, 2026. These statements do not supply a distinct strict cost–Betti relation.
- [Bevilacqua–Bowen v1](https://arxiv.org/pdf/2510.05459v1), Theorems 1.2–1.3 and associated corollaries, give positive metric/infinite-measure criteria. Its version remains October 6, 2025. It does not contain the exact group's cellular calculation.

The bounded new web searches included the exact source title, rank-100 amalgam plus Betti/Fox, the note title, and cost–Betti strictness/counterexample combinations. No indexed identical group-specific direct proof was identified. No claim of worldwide exclusion or firstness follows from this negative search.

## Does the direct calculation add content?

Yes, in the precise proof-content sense used by the original request. The public triage uses the inequality, action invariance, and the sequence of low-cost height actions. The frozen manuscript's Proposition 3 instead follows the chain:

`source free basis -> explicit regular-tree operator -> injectivity of S and t-1 -> explicit triangular cellular boundary -> injective d2 -> aspherical exact presentation -> von Neumann dimension -> all-degree vanishing`.

Neither cost bound occurs in that chain. The cost-independent proof survives if the Bernoulli lower bound fails and does not need the upper cost estimate either. It gives the additional exact presentation claim and makes the operator/dimension mechanism checkable. It is therefore not the same argument padded with a rational parameter choice.

This is a limited contribution, not a novel general method or certified new invariant property. [Linnell's 1992 primary paper](https://personal.math.vt.edu/linnell/research/zerol2.pdf), Theorem 2, printed p. 50, already covers analytic zero divisors for right-orderable groups and hence free groups; the elementary tree proof handles a known special operator without requiring that theorem. Fox's calculus is classical, and the manuscript credits it. A standard aspherical graph-of-spaces plus the already available first-Betti result and Euler characteristic would also give all-degree vanishing. Thus merely enlarging the degree range is insufficient for first priority. The actual additional content is the explicit cost-independent computation and exact presentation verification. The package's `DIRECT_COMPUTATION_PRIORITY.md` accurately states this limitation.

The rational choice `alpha=2^-61`, explicit eta and finite arithmetic diagnostics improve reproducibility but would not by themselves create a new theorem or make a duplicate basic inference eligible as a new solution.

## Scope and metadata consistency

The frozen title is neutral and specific. The abstract, first attribution paragraph, theorem, dependency discussion, README and Zenodo description all identify the construction and positive cost estimate as OpenAI's. They attribute comparison and invariance to Gaboriau, general implication to PSV, and the earlier conditional observation to the public triage. They identify the direct proof as independent of the cost inputs, preserve the separate infimum-group-cost equality, state the full zeroth correction, and do not assert firstness or independent fixed-price discovery. The original manuscript-specific OpenAI BibTeX key, author, title and year are preserved; its URL is pinned for reproducibility.

Author, ORCID and date agree with the original request: Alec Kriebel, `0009-0001-9320-500X`, October 6, 2026. No invented affiliation/coauthor is included. AI use and lack of conventional human refereeing are stated explicitly in main.tex, README, and metadata. Scoped automated audits are not called human peer review or formalization.

The archived priority audits match the separately read project priority audit/addenda byte for byte. Their dated conditional/provisional stages are clearly preserved as historical scope, with the final extra-proof assessment in the direct-computation addendum. They do not overrule later package review or claim publication occurred.

The separately delegated metadata/rights check supplies inventory, hash and PDF-metadata evidence under `metadata_rights/`. It found all 35 ZIP members accounted for: 34 exact manifested payload files plus the manifest itself. Frozen publication and archive copies of the manuscript, PDF and README agree. A concrete comparison of every archived Markdown/TeX/Python file with the upstream TeX/README/INPUTS found only a short attributed status quote and routine mathematical phrases at its 12-token threshold; the upper-bound proof's longest contiguous alphabetic-token match was 10 tokens. No substantial copied upstream prose or third-party code was detected, and no Apache source-notice blocker was identified.

CC BY 4.0 is consistent across the frozen README, metadata and archive declaration. It is inferable for the owned text from the repository Zenodo upload-kit default: `zenodo_deposit_tool/deposit.example.json` uses that license and its README directs new projects to copy the example; established local publication manifests use it, and `openai_followon_bosonic_capacity/LICENSES.md` explicitly identifies it as that default. This is an inference from repository practice, not an invented explicit license selection in the original request.

## Remaining conditions and review completion

No repair is required by this scoped review unless the mathematical reviewers find that the separately added proof or pivotal positive cost input is unsound. In that event, priority eligibility for the full claimed solution must be reassessed; a cost-independent vanishing proof cannot certify a positive cost gap. A new post-review substantive claim would likewise require fresh review of its scope.

Assigned scoped review completion estimate: **100%**. No worldwide-priority completeness percentage is meaningful. This report does not raise the project's mathematical-resolution or publication-package completion percentages and does not certify the deposit/tracker stages.
