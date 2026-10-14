# Primary-source priority, version and attribution verification

Checked 2026-10-07 05:51 UTC (2026-10-06 Pacific). Scoped verification completion: 100%. This is primary-source verification support for complete-package reviewer 3, not an independent certification of the upstream analytic proof or worldwide priority.

## Scope and independence

Read `/Users/alec/Documents/Math/AGENTS.md`, the project's `research/ORIGINAL_REQUEST.txt`, and current `main.tex` before comparator primary-source reading. Also inspected current README, intended Zenodo metadata, source-archive bibliography, source hash manifest, upstream primary manuscripts and their citation information. Did not open previous complete-package review reports/responses or research-history/conclusion files. A live-agent inventory query incidentally displayed short completed-agent status summaries from review 2; those conclusions were not used. This exposure is why this report is characterized as primary-source verification support rather than the fresh complete-package verdict. The separate comparator agent received only instructions, original target and current manuscript, and independently checked DT/DKST; its report is `priority-comparator-dt-dkst.md` in this asset directory.

No candidate, upstream clone or Git mutation; no communication with external individuals. Only this report and the comparator report were written in the allowed review asset directory.

## Finding

No substantive priority, attribution, version or metadata mismatch was found in the inspected current candidate. Its defensible contribution is an explicit fixed-width restriction and full finite-window transference consequence of the newly available continuous annular theorem. The inspected earlier sources contain narrower theorems and established reduction machinery. This is evidence against duplication within those sources; neither a failed search nor these source checks establish exhaustive novelty. The candidate makes no first-priority claim and credits the continuous analytic breakthrough to the supplied upstream author.

## Exact candidate checked

SHA256:

| File | Hash |
|---|---|
| `main.tex` | `b487be2a3233d56facde9713681733e5e6d7a8539ff6d78a94cf7d7db796f10f` |
| `README.md` | `d735b20b62f2a3cf5fbba5eae95cc5a42d1b2e7faec890035742d25aaf11c252` |
| `zenodo-deposit.json` | `5cff48980a8898e552f0b1945235b3cb3a8725b295ea351fdb010d0f3e8a3845` |
| `publication/upload-kit/source.zip` | `651984b7acf1186de939b437ec7216e90a34d06681ff3e6fc41f0bee89c45f6d` |
| `publication/upload-kit/verification-supplement.zip` | `36fa0e0213bce168fb1abda715fb3fd133d914dc1ceb5bcdf1624a998abc5fc9` |

The archived `main.tex` hash equals the workspace source hash. I inspected the bibliography in the source archive, not earlier priority conclusions in the verification supplement.

## Comparator theorem and version checks

### Becker–Durcik

[Official arXiv history](https://arxiv.org/abs/2603.20173) lists Lars Becker and Polona Durcik, with only v1, submitted 2026-03-20 17:48:52 UTC. In [v1, Corollary 1.4 and discussion of (1.8)](https://arxiv.org/html/2603.20173v1), the averages are `n^-1 sum_{i=0}^{n-1} f1(T^i x)f2(T^-i x)`. The full pointwise variation bound requires `1/r < min(3/2-1/p,1/2)` and the BHT exponent range; thus every r>2 is covered at output p=3/2. The paper expressly distinguishes arbitrary commuting S,T averages from this single-generator theorem. It does not state the candidate's arbitrary two-generator symmetric Hilbert variation theorem. The main.tex characterization is accurate at the relevant exponents. No subsequent arXiv version or correction notice was present in the checked official history.

### Demeter

[Official arXiv history](https://arxiv.org/abs/math/0601277) lists Ciprian Demeter, only v1, submitted 2006-01-12 08:56:51 UTC. [Theorem 1.2 in v1](https://arxiv.org/pdf/math/0601277v1), pp.1–2, proves almost-everywhere convergence of symmetric Hilbert sums with factors `f(tau^n x)g(tau^-n x)` for bounded inputs. Remark 1.3 extends convergence to the stated usual BHT input range. Section 3.3 gives a fixed-width one-dimensional cell restriction and singular-kernel comparison before ergodic transfer. These are genuine antecedents to the mechanism, but the action still has one generator, and the theorem does not give arbitrary-commuting full r>2 pointwise Hilbert variation. The candidate's sentence about opposite powers is correct. No later arXiv version was listed.

### Demeter–Thiele and Durcik–Kovač–Škreb–Thiele

[DT v1](https://arxiv.org/pdf/0803.1268v1), Section 6, footnote 36, explicitly describes the R²-to-Z² cell reduction and orbit-array transference. The surrounding proved convergence concerns two-parameter Cesàro averages, while the triangular Hilbert operator is an analytic goal. [DKST v3](https://arxiv.org/pdf/1603.00631v3), Theorem 1, proves L4×L4-to-L2 norm 2-variation for arbitrary-commuting averages: the sum is of output norm squares, not the pointwise partition supremum inside the output norm. Section 5, pp.24–25, integrates positive-area phases. This mechanism already appears in [DKST v1](https://arxiv.org/pdf/1603.00631v1), Section 6. The separate comparator report records the v1/v3 chronology and the weaker first-version estimates. Neither source duplicates the candidate's Hilbert variation theorem. The candidate's exact section pointers and named authors are supported.

### Additional singular-kernel restriction precedent

[Blasco–Carro–Gillespie, author-hosted primary manuscript](https://www.uv.es/~oblasco/Investigacion/BO/BCG.pdf), Proposition 3.6, pp.12–13, uses cell overlap, half-integer truncations and a `c/n+O(n^-2)` kernel comparison to prove uniform bounds for the one-dimensional discrete BHT. Theorem 3.7, pp.13–14, transfers a bounded operator with factors `T^n f T^-n g`, under an additional intertwining condition. It is **not** an arbitrary pair of commuting transformation generators and states neither the candidate's full pointwise r>2 variation nor its arbitrary-commuting convergence theorem. It is another machinery precedent. [Berkson–Demeter, final journal paper](https://jot.theta.ro/jot/archive/2010-063-002/2010-063-002-014.pdf), Theorem 1.3/Corollary 1.4, likewise extends opposite powers of one operator/transformation, not two arbitrary generators.

Adding Demeter Section 3.3 and BCG Proposition 3.6 as extra explicit machinery citations would be reasonable, but is optional: the candidate already credits classical transference and specific modern cell/phase precedents, calls the theorem a consequence and does not claim invention of these ideas.

## Upstream authorship, version and correction scope

The read-only clone and its manuscript-specific [README](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Annular-variation-of-the-triangular-Hilbert-transform-at-the-symmetric-point-October-5-2026/README.md) identify the author as OpenAI and supply the exact BibTeX. That block is preserved verbatim in `source.zip/references.bib`; main.tex additionally provides the exact immutable commit URL. The primary annular introduction's Theorem 1.1 has exactly the candidate's complex L3×L3-to-L^(3/2) pointwise rational-partition supremum, all positive scales, unrestricted finite length and every r>2. The note identifies this as an external input rather than re-proving it.

At this audit, `git ls-remote --heads --tags https://github.com/openai/math.git` returned only `refs/heads/main`, at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Live raw `main` copies of repository README, manuscript README, introduction, consequences and Lean scope had byte-for-byte equal SHA256 values to the pinned clone. All 15 entries in the candidate SOURCE_HASHES manifest independently matched both stored source copies and original pinned files. No newer main version was identified. This does not claim a complete correction search outside the inspected repository and official paper histories.

The family 082 scope file explicitly identifies the older maximal manuscript, not annular variation; the candidate's limited formalization disclosure is correct. I did not validate any Lean proof here.

## Public chronology limits

The manuscript date is October 5, 2026. The pinned local Git history contains a single initial commit, with author/committer time 2026-10-06 14:58:50 -07:00. The [public commit page](https://github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a) and manuscript are accessible at the audit time. Commit creation time and manuscript date do not independently establish the earliest public disclosure time. GitHub repository/commit-history API requests returned HTTP 403 rate-limit errors, so their public-creation/history metadata was not obtained. The candidate correctly refrains from turning manuscript dates into public-priority assertions.

## Package claim correspondence

The title, abstract, scope section, README and intended Zenodo description agree on commuting invertible transformations, complex L3 inputs, symmetric odd Hilbert sums, every r>2, L^(3/2) maximal/variation bounds and almost-everywhere/norm convergence with maximal-tail convergence. They attribute the continuous breakthrough to OpenAI, describe the new work as restriction/transference, and exclude one-sided Cesàro, r=2 and noncommuting conclusions. Author/ORCID is Alec Kriebel / 0009-0001-9320-500X; no invented affiliation/coauthor. AI use and absence of conventional human peer review are explicit. Metadata's immutable `isDerivedFrom` URL points to the exact annular source. No substantive repair is required by this scoped audit.
