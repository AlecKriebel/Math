# Literature, release, and submission-metadata audit

**Package audited:** `K2P_Principal_D_Plus_Referee_Package_20260826.zip`  
**Audit date:** 26 August 2026 (America/Los_Angeles)  
**Scope:** current primary-source attributions, bibliography metadata, public
data/code/tag/release claims, submission declarations and licenses, and
internal date/version consistency. The package was treated read-only. No
person was contacted.

Package-relative paths below are rooted at:

`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-26_r3/isolated/k2p_principal_d_plus_submission_referee`

## Outcome for this audit layer

- **Load-bearing literature attributions: PASS.** The cited theorem numbers and
  scopes checked below support the uses made in the article. In particular,
  Brits et al. arXiv v3 still supports the level-1 JC/K2P/K3P statement used by
  this paper, while its separate arbitrary-level result is JC-only in the
  operative v3 theorem body.
- **Bibliographic record metadata: PASS except for two currentness/date
  presentation issues.** All thirteen DOI-bearing bibliography entries agree
  with current DOI/publisher metadata. The three versioned non-DOI entries also
  resolve to the stated records.
- **Public data/code availability: PASS at the time of audit.** Every one of the
  489 files in the attached ZIP is present byte-for-byte in the public tagged
  project subtree. The tag exists and dereferences to the commit stated below.
- **Submission metadata and licenses: PASS as internal declarations.** ORCID
  name/path were independently verified. Email, funding, contribution, and
  competing-interest statements are internally consistent; the latter three
  are necessarily author declarations, not facts a referee can independently
  certify.
- **Human metadata/release status: HOLD for small corrections.** The supplement
  contains an impossible 21/25 August verification chronology, and its
  companion-work DOI note is no longer current without qualification. The
  phrase “immutable source tag” also overstates what an ordinary unsigned Git
  ref guarantees. These are not mathematical defects and, under the requested
  protocol, should not alter the scientific ACCEPT/HOLD/REJECT recommendation.

## Numbered findings

### 1. Definite internal date contradiction in the recent-source note

**Classification:** presentation/attribution; definite; non-mathematical.  
**Package locations:**

- `proof_compression_submission/supplement/supplement.tex:896-899` says,
  “Citation metadata were checked on 21 August 2026”.
- The same table, at `supplement.tex:940-944`, cites
  `arXiv:2607.12919v3` and explicitly says that v3 is dated 25 August 2026.
- `proof_compression_submission/article/references.bib:180-190` likewise binds
  the citation to v3 and 25 August 2026.
- The contradiction is printed on page 23 of
  `proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf`.

The [versioned arXiv primary record](https://arxiv.org/abs/2607.12919v3)
reports v3 at 25 August 2026 11:37:51 UTC (after v1 on 14 July and v2 on
29 July). Therefore the whole displayed table cannot have been checked on
21 August as written. This is not merely a timezone issue.

**Effect:** no effect on the mathematical use of Brits et al.; it defeats only
the stated provenance date for the table. The package's static source audit did
not catch it: `adversarial_review/audit_article_sources.py:890-893` checks
citation-key closure, and lines 1035-1048 check approved metadata literals, but
neither checks dates against cited-version dates.

**Minimal remedy:** change the lead sentence to “checked through 25 August
2026”, or say precisely that the table was checked on 21 August and the Brits
entry was updated on 25 August. Rebuild the supplement PDF, source archive,
source-bound audit/manifests, public source tag, and distributed referee ZIP;
publish new sidecar hashes. A new tag is preferable to moving the existing
tag.

### 2. The exact companion v1.1.4 citation is valid, but the unqualified DOI note is no longer current

**Classification:** current-metadata/presentation; factual exact-version
citation, but stale if read as the current status of the companion work;
non-mathematical.  
**Package locations:**

- `proof_compression_submission/article/references.bib:167-177` cites the
  companion JC work specifically as GitHub release v1.1.4 at source commit
  `b5b855f5e6552e1d87f32d90851ea2def5330364`.
- `proof_compression_submission/supplement/supplement.tex:945-948` repeats that
  exact release and concludes, “no DOI is claimed.”
- The statement is printed on supplement PDF page 23.

The cited [GitHub v1.1.4 release](https://github.com/AlecKriebel/Math/releases/tag/stc-jc-sharp-boundary-v1.1.4)
exists, was published 18 August 2026, and its release text itself says that no
DOI was claimed or created. Its annotated tag object
`e8ecbb646fee118899947d48d715a8a256fc4f04` dereferences to exactly the printed
commit `b5b855f5e6552e1d87f32d90851ea2def5330364`. Thus the bibliography is not a
fabricated or mismatched exact-version citation.

However, before the present K2P package was built, the same companion work had
later v1.1.7 DOI-bearing records:

- preprint: [DOI 10.5281/zenodo.22089373](https://doi.org/10.5281/zenodo.22089373),
  issued 23 August 2026, version 1.1.7;
- certificate/reproducibility dataset:
  [DOI 10.5281/zenodo.22064121](https://doi.org/10.5281/zenodo.22064121),
  issued 23 August 2026, version 1.1.7.

DataCite metadata give the same companion title, author and ORCID and identify
the first record as a preprint and the second as its certificate dataset. The
public annotated tag `stc-jc-sharp-boundary-v1.1.7` also exists (tag object
`4da193e200195bcb239acaf29e69a22c215e23b9`, commit
`858fc82595910c9e7dd96a8350551248214d624d`) and is labelled “DOI-bearing
submission package v1.1.7.”

**Effect:** no mathematical defect in the K2P paper and no falsity in the
specific v1.1.4 citation. The wording is nevertheless misleading in a section
called “Recent-source verification note” unless “no DOI” is expressly scoped
to that older release. This finding is separate from the K2P paper's own
no-DOI statement, which was verified and remains true for this version.

**Minimal remedy:** either update the companion citation to v1.1.7 and include
the current preprint/dataset DOIs, or retain the exact v1.1.4 citation and write,
“the cited v1.1.4 release itself claimed no DOI; later v1.1.7 records are …”.
Any source change requires the same source/PDF/manifest/tag/archive reseal
listed under Finding 1.

### 3. “Immutable source tag” is too strong for the actual Git object

**Classification:** reproducibility wording; low severity; current access and
byte binding pass.  
**Package locations:**

- `proof_compression_submission/article/main.tex:1822-1832` (article PDF page
  24);
- `proof_compression_submission/supplement/supplement.tex:963-968`
  (supplement PDF page 23);
- `proof_compression_submission/README.md:84-88`;
- `proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.md:58-64`;
- `proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json:1663-1674`.

The public [K2P source tag](https://github.com/AlecKriebel/Math/tree/k2p-same-biorxiv-v1.0.2/k2p_level2_identifiability_closure)
exists as an annotated tag:

- tag ref/object: `ae537c7e2dacdc1026b30b65fe04daca57b4fd84`;
- peeled commit: `cb7559e0ba5fd72f94bce5941208be0838be878d`;
- tagger timestamp: 26 August 2026 19:10:00 PDT;
- annotation: “K2P-SAME positive-domain bioRxiv submission source v1.0.2.”

`git verify-tag` reports “no signature found.” An ordinary Git tag name is a
repository ref and can be moved or deleted by an authorized repository actor;
the content-addressed tag object and commit IDs are stable, but the package
does not print the commit ID next to the tag. “Immutable” is therefore a policy
or intention, not a technical property proved by this distribution.

**Effect:** none on present accessibility or byte identity. It weakens the
long-term permanence claim if the ref is later changed.

**Minimal remedy:** call it a “versioned annotated source tag” and print the
peeled commit SHA (`cb7559…`) beside it. A protected release/deposit can be
added later only by the author; no such external action is needed to correct
the current wording.

### 4. Historical crosswalk log ends before the final v1.0.2 closure

**Classification:** nonblocking provenance-log completeness.  
**Package location:**
`proof_compression_submission/crosswalk/RESEARCH_LOG.md:38-63` records the
24 August v1.0.0 checkpoint at 98% and says its then-generated files were stale
by design, but contains no later entry recording the final v1.0.2 generation.

The current manifest, README, crosswalk, PDFs and tag consistently say v1.0.2,
so this chronological research log is not a competing authority and creates no
current version ambiguity. The optional minimal remedy is a final dated log
entry pointing to the v1.0.2 manifest/tag. No theorem artifact needs change if
the log is left historical.

## Primary-source attribution matrix

| Submission claim or citation | Primary check | Result |
|---|---|---|
| Brits et al. v3, article `main.tex:137-140`, supplement `:940-944` | [arXiv v3 record](https://arxiv.org/abs/2607.12919v3) and [v3 HTML](https://arxiv.org/html/2607.12919v3): Theorem 4.9 is full level-1 identifiability for JC, K2P or K3P modulo reticulation placement in triangles. Lemma 5.5 and the operative arbitrary-level discussion in v3 are JC-only. | **PASS.** The paper invokes only Theorem 4.9. The supplement accurately disclaims reliance on the narrowed arbitrary-level result. The external preprint retains one stale introductory sentence mentioning arbitrary-level K2P, but the theorem body/discussion control; this is not a submission defect. |
| Huber et al., `main.tex:146-148`, `:942`; supplement `:932-935` | [Springer version of record](https://link.springer.com/article/10.1007/s11538-025-01510-5): Figure 8 depicts the two semi-directed level-2 generators and Lemma 4.2 gives their exhaustive classification. | **PASS.** Exact lemma/figure attribution. |
| Englander et al., `main.tex:148-153`, `:466`; supplement `:936-939` | [Official bioRxiv API](https://api.biorxiv.org/details/biorxiv/10.1101/2025.04.18.649493/na/json) lists v1 24 Apr 2025, v2 9 Oct 2025, v3 23 Dec 2025, v4 4 Jul 2026. Locally archived primary v4 XML, `/Users/alec/Documents/Math/s_tc_jc_landmark_closure/reviews/final_standard_convention/sources/englander_649493v4.source.xml`, SHA-256 `1323dec9322099afb9f49e11554c92d1fe78e4b29c5ee03ba8942690ae2e8c38`, contains Propositions 2.9-2.10 (JC/K2P quartet signs), Theorem 2.11 (different displayed quartets), and Corollary 2.12 (tree of blobs). | **PASS.** The table's “Englander et al. (2025)” is consistent with the original issue year even though the cited content is v4 (2026) and the BibTeX key ends in `2026`. |
| Holtgrefe et al. quartet paper, supplement `:925-928` | [Springer version of record](https://link.springer.com/article/10.1007/s11538-025-01549-4) gives Bull. Math. Biol. 87:168 and records the correction published 14 Jan 2026. | **PASS.** |
| Holtgrefe et al. semi-directed paper, `main.tex:238`; supplement `:929-931` | [Springer version of record](https://link.springer.com/article/10.1007/s12064-025-00453-8) was online 10 Dec 2025 and is volume 145, article 4 (2026). | **PASS.** BibTeX year 2026 is the volume year; the `-025-` DOI and 2025 online date do not make it inconsistent. |
| Ardiyansyah, `main.tex:141-144`; supplement `:921-924` | [Versioned arXiv record](https://arxiv.org/abs/2104.12479v1), submitted 26 Apr 2021, states the simple/semisimple level-2 invariant scope. | **PASS.** |
| Cox--Gross--Martin | [Springer version of record](https://link.springer.com/article/10.1007/s11538-025-01506-1), Bull. Math. Biol. 87:132 (2025), is specifically about group-based models on 3-sunlets. | **PASS.** |
| Gross et al. level-1 paper | [Springer version of record](https://link.springer.com/article/10.1007/s00285-021-01653-8), J. Math. Biol. 83:32 (2021), has the stated level-1 Markov-process distinguishability scope. | **PASS.** |
| Gross--Long | [SIAM version of record](https://epubs.siam.org/doi/10.1137/17M1134238), SIAGA 2(1):72-93 (2018), has the stated network-distinguishability scope. | **PASS.** |
| Bochnak--Coste--Roy, `main.tex:795`, `:1419`, `:1457` | [Springer book record](https://link.springer.com/book/10.1007/978-3-662-03718-8). Theorem 2.2.1 is the Tarski--Seidenberg projection theorem; Proposition 2.8.2 is the equality of semialgebraic dimension with the dimension of the real Zariski closure; Section 2.8 is the relevant dimension section. | **PASS.** Exact numbered uses are consistent. |
| Remaining foundational references: Kimura; Evans--Speed; Sturmfels--Sullivant; Semple--Steel; Hollering--Sullivant | DOI/publisher records match the titles, authors, venues, years, volumes and page ranges in `references.bib`. Their uses are background/scope rather than a hidden imported K2P level-2 classification. | **PASS.** |

All thirteen DOI-bearing entries were queried independently through current
Crossref/primary publisher records; no author, title, venue, year, volume,
issue, page/article-number, or DOI mismatch was found:

`10.1007/BF01731581`, `10.1214/aos/1176349030`,
`10.1089/cmb.2005.12.204`, `10.1093/oso/9780198509424.001.0001`,
`10.1007/978-3-662-03718-8`, `10.1137/17M1134238`,
`10.1016/j.jsc.2020.04.012`, `10.1007/s00285-021-01653-8`,
`10.1007/s11538-025-01506-1`, `10.1007/s11538-025-01549-4`,
`10.1007/s12064-025-00453-8`, `10.1007/s11538-025-01510-5`, and
`10.1101/2025.04.18.649493`.

## Public tag, archive, data and code audit

### Exact public-source binding

The attached archive has:

- SHA-256
  `86a286be82ce3c211f556eaa24cf1120aa42e41f716b46cb8752c1d2546053ba`;
- 489 file members below
  `k2p_principal_d_plus_submission_referee/`;
- matching adjacent sidecar
  `K2P_Principal_D_Plus_Referee_Package_20260826.zip.sha256`.

I independently computed each ZIP member's Git blob SHA-1 and compared it to
the public tag's `k2p_level2_identifiability_closure/` subtree at commit
`cb7559e0ba5fd72f94bce5941208be0838be878d`:

- archive members checked: **489**;
- missing from tagged subtree: **0**;
- blob mismatches: **0**.

The tagged subtree contains 655 files, so it is a superset rather than a
minimal mirror of the referee ZIP. That does not contradict the article's
claim that the exact files are contained there.

### Five-file submission source archive

The adjacent `K2P_SAME_bioRxiv_Source_20260826.zip` has SHA-256
`ce90c2856989ebbdf3084889fd5e6e96298e81f82a198b946e381c303873e744`
and a matching sidecar. It contains exactly the five declared source files;
each is byte-identical to the referee package:

| Path | SHA-256 | Result |
|---|---|---|
| `article/main.tex` | `d64574e30ef3dac38c91613938a6ce29f7b07688ea791013c56a45e9af0e75c3` | MATCH |
| `article/references.bib` | `d1b3b50f6e276cc147471dcab9f30ed3a9b629fddc19ffb7fea58d427ee5de6b` | MATCH |
| `supplement/supplement.tex` | `7b28e0ff620b24256f4eebe61fc233dc21df8ffd7b4b552b51eb579712358bc4` | MATCH |
| `supplement/compression_tables.tex` | `22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81` | MATCH |
| `supplement/certificate_appendix.tex` | `936e8d1879acd224affb053489a618dcfe8d7a7a2a5500bc8f0f85dd1b16794d` | MATCH |

### Release/DOI boundary

The GitHub API returns HTTP 200 for the exact tag ref and HTTP 404 for a
GitHub Release at `k2p-same-biorxiv-v1.0.2`. Exact-tag and exact-title DataCite
searches returned no K2P DOI record. Therefore these package statements were
verified at the audit time:

- article `main.tex:1824-1829`: this K2P version claims no DOI;
- supplement `supplement.tex:967-968`: no GitHub Release, Zenodo deposit or DOI
  is claimed in this version;
- README `:87-88`, crosswalk `:63-64`, and manifest `submission_metadata`
  agree.

This is verification of the stated current release boundary, not a proof that
no unrelated or later deposit can ever exist. It must not be confused with the
companion JC work's later DOI records in Finding 2.

## Submission metadata and license reconciliation

| Field | Package locations | Independent/status check | Result |
|---|---|---|---|
| Author and ORCID | `article/main.tex:70-76`; `supplement.tex:41-47` | [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X) public API returns path `/0009-0001-9320-500X/person`, given name Alec, family name Kriebel. | **PASS** |
| Corresponding email | same title blocks; `main.tex:1822-1839`; `supplement.tex:959-960`; README/crosswalk/manifest | `me@aleckriebel.com` is identical everywhere and matches the Git tagger metadata. The mailbox was not tested because contact is forbidden. | **PASS as internal metadata** |
| Sole-author contribution | `main.tex:1834-1839`; README `:84-86`; crosswalk `:58-61`; manifest | Same sole-author responsibility statement throughout. | **PASS as author declaration** |
| Funding | `main.tex:1841-1843`; `supplement.tex:959-961`; README/crosswalk/manifest | “No specific funding supported this work” is identical throughout. | **PASS as author declaration** |
| Competing interests | `main.tex:1845-1847`; `supplement.tex:960-961`; README/crosswalk/manifest | “The author declares no competing interests” is identical throughout. | **PASS as author declaration** |
| Licenses | `LICENSES.md:1-38`; `main.tex:1827-1829`; `supplement.tex:961-963`; README/crosswalk/manifest | `LICENSES.md` contains an operative CC BY 4.0 grant/link for paper, supplement, figures, tables and certificate data, plus the full MIT permission and warranty text for code. | **PASS** |
| Generative-AI disclosure | `main.tex:1849-1858`; `supplement.tex:970-975` | Explicit, mutually consistent disclosure; correctly says separately implemented programs are not independent human review. | **PASS** |

Relevant hashes:

- `LICENSES.md`:
  `9f8d28b470f185905d0469d45168d72d56d0152a1667a299328a3af00041465e`;
- `REVISED_REFEREE_BUNDLE_MANIFEST.json`:
  `c65d4c7ce4d094f7d1e85ecfea2604c5948c345c11f9fb726505301d898f5fc2`;
- article PDF:
  `2bca627d072cf96c850a7196be9101a7e061499bbcc61ebbb8ff256d4bf864b9`;
- supplement PDF:
  `4bdcfe32cf3dbcd586d9bf68f3d287e4f5f58aa3384aa5daaf454fde3e361621`;
- static source audit JSON:
  `59f401307c0cce25ff2d7570789fd89da78e5d642814d870589b965549a272a5`.

## Other apparent date/version mismatches that reconcile

- `EnglanderEtAl2026` is only an internal BibTeX key. Its printed bibliographic
  year 2025 matches first posting/DOI issuance; the note correctly identifies
  the 4 July 2026 v4 content.
- Holtgrefe et al. has a DOI containing `025` and a December 2025 online date,
  but the final volume is Theory in Biosciences 145:4 (2026); year 2026 is
  appropriate.
- `pdfinfo` reports both PDFs created at 25 August 2026 17:00 PDT, while the
  build report says 26 August. `PDF_BUILD_REPORT.json` records
  `SOURCE_DATE_EPOCH=2026-08-26T00:00:00Z`, which is exactly 25 August 17:00
  PDT. This is deterministic timezone rendering, not stale PDFs.
- Historical reports are explicitly labelled historical/superseded. In
  particular, `adversarial_review/ADVERSARIAL_ARTICLE_AUDIT.md:1-19` demotes
  its older hashes, and `FRESH_ADVERSARIAL_R2_DISPOSITION.md:87-133` contains a
  filled final PASS section. No unlabeled historical hash was found competing
  with the current manifest in this metadata/release layer.

## Search boundary and novelty caution

Targeted arXiv searches for combinations of “Kimura 2-parameter”,
“semi-directed”, “level-2”, “tree-network distinguishability”, and
“identifiability” returned the close works already cited here, most notably
Brits et al., Gross et al., and the quartet level-2 paper. No additional public
primary source stating the same K2P strong-tree-child level-2 principal-domain
classification was located in that search. This is search evidence only, not
an exhaustive priority or novelty guarantee.

## Minimal ordered actions

1. Correct the supplement's 21/25 August verification-date sentence.
2. Qualify the companion v1.1.4 “no DOI” statement or update it to the current
   v1.1.7 preprint and dataset DOIs.
3. Replace “immutable source tag” with “versioned annotated source tag” and
   print peeled commit `cb7559e0ba5fd72f94bce5941208be0838be878d`.
4. Rebuild/reseal every artifact whose source hash changes: PDFs, five-file
   source ZIP, static audit, source/revised-bundle manifests, public source tag,
   referee ZIP, and sidecar SHA-256 files. Use a new tag rather than silently
   moving v1.0.2.

No mathematical theorem, computation, finite census, certificate, or proof
text needs alteration because of this audit.
