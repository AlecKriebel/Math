# Independent adversarial priority review: PR #1205 / problem 30004665

Checkpoint: 2026-10-17 16:36:46 UTC (09:36:46 America/Los_Angeles). Assigned priority review completed: 100%. Clearance for a **new full-solution preprint**: **not granted**. This is a priority objection, not a mathematical refutation of the certified canonical-coordinate example.

## Recommendation and exact limit

Treat this package as a reproducible **consequence of prior source data and prior minuscule-weight results**, unless a separate, accurately attributed clarification paper is deliberately pursued. I do not recommend promoting it as an independently new resolution of a currently open string-cone conjecture. The same example, including its entire 22-term support, already occurs in the original authors' software repository after the established monomial coordinate change. Its nonredundancy is covered by their minuscule-weight results. The decisive canonical exponent 2 is obtained by a triangular integer calculation from that old support.

There remains an important distinction: I did **not** locate an earlier source explicitly saying that this exact example refutes the canonical-W converse printed in the 2021 Oberwolfach report. Existing data plus a published theorem need not imply that the authors noticed or published that conclusion. Thus a disposition may accurately say **“new-result priority not established; exact example predates this attempt and the conclusion is an immediate literature consequence.”** It should not assert **“Koshevoy and Mironov explicitly published this counterexample/the correction”** without additional evidence. Negative searches do not establish first priority.

A short clarification could responsibly point out the coordinate issue and give independent exact certificates, while crediting the pre-existing example and avoiding any claim to solving the later string-coordinate conjecture. Whether such a clarification merits a new preprint is distinct from this workflow's intended promotion of a novel full solution. It should not be published with a claim to a newly discovered example or an unqualified new solution of the authors' currently stated conjecture.

## Independently retrieved primary evidence

1. **Denis Mironov's `crystal` repository.** [Current repository](https://github.com/mironovd/crystal), [original addition](https://github.com/mironovd/crystal/commit/573b512df531ec2d349ed05b3aa9f385989e13dd), and [subsequent rename](https://github.com/mironovd/crystal/commit/0d6e564cf5e69d79c1074d5d1e3e72ac700904d6). The addition commit records 2020-03-06 15:05:34 UTC and adds `crystal.D4.out.xz`. Three minutes later the file was renamed to `crystal_D_4.out.xz` without changing Git blob `9b36ab3e50cd8ae8a6eb42e4c805d3bd689ab506`.
2. I fetched the current file, the original addition's file, and the file at the 2022-05-29 repository snapshot `aedc5e79ce529f4cc93fd33b0a79700b1edee98a`. They are byte-identical: 86,624 compressed bytes, SHA-256 `b7022bbc90d285f7827b7146254e91359639af6c2c38ef71a68db7098084119b`. Commit dates are repository-recorded timestamps, not a separately timestamped archival attestation. The dated 2022 paper below independently identifies this public repository as its implementation.
3. **Koshevoy–Mironov, 2022, EasyChair Preprint 8975, “F-Polynomials and Newton Polytopes.”** [Landing page](https://easychair.org/publications/preprint/z55N), [PDF](https://easychair.org/publications/preprint/z55N/open). The landing page and PDF both identify October 3, 2022. The paper gives the BK/GHKK coordinate correspondence and the computation method, and refers readers to this repository. Its lattice-voidness conjecture is different from the target converse.
4. **Koshevoy–Schumann, 2022.** [Published article](https://link.springer.com/article/10.1007/s10801-022-01144-z), DOI `10.1007/s10801-022-01144-z`. Theorem 6, printed p.1049, covers minuscule summands' nonredundancy. Definition 9 and Proposition 5, p.1043, give the monomial isomorphism between canonical potential and string functions. Theorem 2 also covers the bounded-exponent string case. The later Conjecture 3 concerns the string function, so it is not disproved by this example.
5. **Schumann, joint work with Koshevoy, OWR 20/2021.** [Primary report](https://ems.press/content/serial-article-files/46898), printed pp.1123–1125. The target converse is printed in canonical W coordinates at p.1125. The same page already states the minuscule summands' nonredundancy. Thus that facet feature is explicitly prior even at the original report stage.
6. **Koshevoy–Mironov 2023 and 2024 conference materials.** [2023 abstract](https://pca-pdmi.ru/2023/files/51/FpolyNewton-pca.pdf), [2023 slides](https://pca-pdmi.ru/2023/files/51/F-poly-Newton%283%29.pdf), [2024 slides](https://pca-pdmi.ru/2024/files/30/coefficients-pre2.pdf). These document BK/GHKK computations and later coefficient work. They do not, in the inspected material, explicitly state this canonical-W counterexample or a correction of the 2021 converse. No inference from lattice voidness to all monomials being vertices was used: that inference would be invalid in general.

Retrieved originals, metadata responses, extracted text, and rendered inspection images are kept under the ignored `sources/` directory. `RETRIEVALS.json` and `RETRIEVALS_MORE.json` give URLs, retrieval times, byte counts, hashes, and response headers. No author software was executed, no person was contacted, and no material was sent to another ongoing agent.

## Exact comparison, independent of the broad priority survey

The old compressed file's **Case 267** has the exact reduced word

`(1,2,3,2,4,2,1,2,3,2,4,2)`.

Its four root components have **14, 1, 5, 2** BK/string monomials, respectively. I parsed the printed layered monomial lists using a restricted syntax-tree parser, not `eval` and not the author's program. I built the triangular matrix K from the word and Cartan matrix, using the established coordinate rule

- K[k,k] = 1;
- K[k,k+] = 1 when the next occurrence exists;
- K[k,l] = Cartan(i_k,i_l) for k < l < k+;
- other entries vanish.

For the convention y_k = X_k^(-1), the row relation is **b = a K**, where b is a string exponent row and a is its canonical y exponent row. Because K is upper triangular with diagonal 1, recover a by the elementary recurrence

`a[j] = b[j] - sum(a[k] * K[k,j] for k < j)`.

This produces **exactly** the 22 distinct canonical support rows in the submitted proof, with no extra or missing row. All old b rows have entries in {-1,0,1}. The two exceptional a rows are already the images of these particular old printed monomials:

| Old printed string monomial | Recovered canonical y exponent row |
| --- | --- |
| t1 | (1,1,1,1,1,2,1,1,0,1,0,0) |
| t2*t4*t6/t7 | (0,1,1,1,1,2,1,1,0,1,0,0) |

Thus the canonical exponent-2 observation is not a new support computation. The full exact comparison, K matrix, every old string row, and every recovered canonical row are in `PRIOR_DATA_COMPARISON.json`. Run `python3 compare_prior.py` from this directory to reproduce the comparison after the retrieved originals are present. The checker reads the candidate only at the final set-equality comparison; the historical rows and reconstructed canonical rows come directly from the old file and the coordinate formula.

The old file is a **support** enumeration, not in itself a universal coefficient certificate. In particular, counting its monomial entries does not prove coefficients are one in arbitrary nonminuscule cases. Here roots 1,3,4 are minuscule and root 2's single term is t12. The candidate's independent mutation proof also establishes all coefficients are one. The priority objection does not depend on inferring coefficients from a support list.

## Facet property is prior theory, not merely numerical coincidence

The nontrivial components here have simple-root labels 1,3,4, the three minuscule fundamental weights in this D4 labeling. Root 2 has only the final-position term, t12. The old minuscule nonredundancy result therefore covers every nontrivial component; cross-component independence is also part of the source framework (OWR Proposition 2; KS Proposition 3/Lemma 4). An invertible monomial map transports the linear inequalities, so these conclusions give the canonical facet property as well. Alternatively the published sufficient string-coordinate theorem applies to the complete historical support, whose absolute exponents are all at most one.

This is a prior **theorem application**, not a claim that the old data file literally printed facet certificates. The candidate's integer separating-vector table is a useful independent validation artifact. Its value does not supply priority for the same theorem application or erase the exact older example.

The published proof of Theorem 2 asserts that multiplicity-freeness is preserved by the monomial isomorphism. That implication is invalid as a general statement, and this example demonstrates its failure in these coordinates. This creates room for a carefully attributed clarification of the proof/coordinate distinction, but does not make the full historical example new. The adverse priority recommendation does not treat the later string-coordinate conjecture as solved or the sufficient theorem's statement as refuted.

## Search and reading limits

Primary materials inspected: complete old Case267; repository metadata and commit history; the 2022 EasyChair paper; the 2023 abstract and slides; targeted KS published sections on the coordinate map, sufficient theorem, minuscule theorem, and final conjectures; the three-page Schumann report; targeted 2024 coefficient slides. The latest arXiv record for `2109.14439` displays only its original September 29, 2021 version. The current Springer article page did not identify a linked correction in the material inspected.

Targeted web searches included the exact 12-letter word with and without spaces; the paper title with counterexample/correction/erratum; canonical potential/multiplicity-free; and Koshevoy/Mironov with Newton/vertices. These did not identify an explicit prior correction in a primary source. Results from this research repository or derivative catalogues were not counted as independent prior art. This is not an exhaustive proof of absence or a claim of first publication.

Visual inspection: OWR PDF page39 (printed1125); KS PDF pages13 and19 (printed1043 and1049). Other PDFs were text-inspected as noted above; the generated rendering images for other pages are retained as retrieval/inspection aids, not claimed visually inspected.

## Disposition options for the parent

- **Recommended for the current novel-solution pipeline:** do not grant publication clearance; record the exact prior-data match and theorem application, and classify the novelty claim as a literature consequence/priority failure. If closing, explain that bounded priority finding, not a false mathematical statement and not a claim that the original authors explicitly announced this counterexample.
- **Possible repaired scope:** an explicitly attributed short clarification about the canonical-vs-string coordinate error, framed as an observation from pre-existing examples with independent certificates. It must cite Mironov's exact historical Case267 and distinguish its own certificate/expository contribution. It must not claim to resolve KS2022 Conjecture3 or to have discovered the exact example first.

This subagent has not changed a PR, staged/committed anything, or published a preprint. Parent review and disposition remain outstanding.
