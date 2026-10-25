# JC legacy article identity reconciliation

Completed 2026-10-25 UTC. Subtask completion: **100%**. This is a publication-lineage decision for an already reviewed and published paper, not a new mathematical review, scientific clearance, priority assessment, or journal assessment.

## Recommendation

**The old HTML article is eligible for an article-level redirect to the existing canonical page for record 22089373.** The best-supported identity is an earlier standalone presentation whose complete result was incorporated into a later unified manuscript in the same paper line. It is not a separately maintained companion result requiring a second canonical research page.

Exact mapping recommended for root adjudication:

- Old document: `docs/papers/s-tc-jc-sharp-boundary/index.html`, served at `https://aleckriebel.github.io/Math/papers/s-tc-jc-sharp-boundary/` (and its `index.html` spelling).
- Destination: `https://aleckriebel.com/research/strong-tree-child-level-2-jukes-cantor-identifiability/`.
- Scope: HTML article only. **Do not redirect or replace the old `paper.pdf` with the new 33-page PDF.** They are different editions with different titles, dates, scope, pagination, and bytes. Preserve the old PDF, source module, archived release artifacts, and audit history.

This recommendation goes beyond the previous pending receipt because it establishes documentary incorporation and provenance. It does **not** contradict that receipt's observations about different PDF bytes or scopes. If a downstream rule insists on byte-identical *editions* rather than one page per distinct *work*, the old and new PDFs fail that narrower test; that must not be misreported as an exact-edition match. Under the programme's actual one-page-per-distinct-work goal, the later unified paper is the corresponding destination.

No redirect, website edit, spreadsheet edit, source edit, Git operation, release, deployment, or external communication was performed. The prior `jc-legacy-correspondence-20261025.json` is preserved unchanged.

## Claim and decision criteria

The question is whether the old article describes (a) a historical manuscript now incorporated into the canonical paper, or (b) a distinct companion work that merely shares a topic. Different titles and hashes alone distinguish editions, not necessarily works. Shared topic, author, directory, or a repository-wide concept DOI alone cannot establish identity either.

An affirmative work-level correspondence requires a specific map from the old result to the new actual manuscript, compatible graph/model conventions, a documentary development/publication chain, and an inventory disposition that is supported rather than assumed. A separate paper-specific publication and a surviving distinct scientific payload or explicit companion treatment would weigh against a redirect.

The evidence meets the former criteria. No distinct residual theorem or separately maintained companion publication was found for this old article. The conclusion is an evidence-based **bibliographic/work-level inference**, not a claim that Zenodo formally records the old PDF as an earlier version of concept 22089372.

## What was read and authenticated

The complete old HTML article and all ten pages of its actual PDF were read. Fresh text was extracted from the local PDF, whose SHA-256 matches both the preserved receipt and a fresh fetch from GitHub at the receipt's exact remote commit `19073d1aadc794c57bcbffa112bac938e8f58268`. All ten old pages were rendered and inspected. The new actual main PDF's title, abstract, principal statements, convention, sharpness sections, interpretation, and reproduction passages relevant to identity were read; the source text and supplement were consulted to resolve the complete witness and proof relationship. Main pages 1, 2, 23, 26, 27, 28 and supplement pages 5–6 were rendered for direct comparison. This was not another full-paper proof audit.

Fresh official public GETs captured the paper and support records, both concept endpoints, both version-history endpoints, the five named earlier Zenodo releases, the repository release version listing, GitHub tag/ref metadata, release metadata, the old article's commit history, the consolidation commit, and the tagged v1.1.7 manuscript and research log. Every successful capture has a receipt and SHA-256 under `public/`.

The published paper PDF was fetched independently from both record 22089373 and support record 22064121. Both fresh payloads equal the already reviewed main PDF. The tagged v1.1.7 `main.tex` exactly equals the manuscript source inside the published source ZIP. This binds the documentary research log and the article's incorporation passages to the released source, rather than merely to a later unbound local draft.

## Content relationship: the old paper is retained in full as the Theta result

The old manuscript is *Full-Dimensional Jukes–Cantor Ambiguity in Weakly Tree-Child Level-2 Networks: An exact four-leaf construction and an all-taxa extension*. Its main theorem is full-dimensional regular JC overlap of dimension `2n` for a nonisomorphic, non-triangle-related pair in `W_TC \\ S_TC`, for every `n >= 4`.

The new manuscript is *Strong Tree-Childness Is a Sharp Generic-Identifiability Boundary for Level-2 Jukes-Cantor Networks*, Zenodo version 1.1.7. It adds the positive strong-class theorem and triangle-free Omega family of dimension `2n+1`. Its §§9.3–9.4, theorem 9.3, proposition 9.4, and supplement §6 incorporate the old triangle-containing result. The following are concrete identity witnesses, not a topic-level resemblance:

| Old actual manuscript | New actual manuscript | Comparison |
|---|---|---|
| Theorem 1.1, p.2 | Theorem 9.3, p.26 | Same quantified all-`n` weak-but-not-strong, non-`T`, regular open overlap theorem, dimension `2n`. |
| §§2.1–2.2, pp.2–4 | §2.1 and model definitions; §9 | Same fixed simple, one-step reticulation-preserving rooting universe and strictly open displayed-tree JC domain. The later paper explicitly locks those conventions. |
| Arc lists (2)–(4), p.4 | Arc list (9), p.27 | Identical internal arcs and exchange of leaf 1 and leaf 4 at `B` and `E`; the old `N,N'` are renamed `K_4,K'_4`. Same theta path lengths and cycle lengths `3,5,6`. |
| Proposition 3.1, p.5 | Proposition 9.4, p.27 | Same tree-child displayed rooting, bad rerooting on `B→C`, and leaf-1 triangle/nontriangle attachment separator. |
| Six Fourier equations (5)–(10), pp.5–6 | Equation (10), p.27, and p.28 | Same six polynomials, same eight-dimensional localized irreducible locus, same positive smooth branch. |
| Exact quadratic polynomial (15), p.6 | Equation (11), p.28; supplement §6, pp.5–6 | Same `43337075β²−36083110β+7336259` and isolating interval `(441/1250,3529/10000)`. |
| Parameters (14), (16), pp.6–7 | Supplement §6, pp.5–6 | Same source multipliers and target rational functions of `β`, including the strict root-edge factorization `(2/3)(3/4)=1/2`. |
| Common orbit tensor (17)–(18), p.7 | p.28 | Same fourteen rational coordinates. |
| Jacobians (19)–(20), p.7 | p.28; gauge orders in supplement p.6 | Same two factorized determinants, with denominators `16384` and `32768`. |
| Lemma 6.1 and all-`n` proof, p.8 | §9.1 and theorem 9.3 proof, pp.24,28 | Same positive analytic cherry inverse and `8+2(n−4)=2n` induction; same preserved attachment separator. |
| §8 and appendix A, pp.9–10 | §11, appendix A; support bundle `sharpness/theta/` | Same exact-coordinate/field proof mechanism is retained in the frozen Theta component and later proof package. |

The new paper contains the old negative theorem and its mechanism, rather than merely citing it as another paper. The new main article and reader supplement reproduce its central proof and witness. The newer abstract and public canonical page both explicitly mention the triangle-containing second family. The canonical page thus actually represents the content to which the old article introduced readers.

The additions are substantial; incorporation does not make the two PDFs the same edition. Conversely, substantial additions do not by themselves create a companion work when the earlier manuscript is retained as part of a unified paper line.

## Development and release provenance

1. The old public article advertises August 9, 2026; the PDF itself prints only August 2026. The old package's `AUDIT_REPORT.md`, dated August 9, calls the surviving narrow result a standalone manuscript after withdrawal of an earlier positive-classification attempt. Its README calls that result the replacement for the withdrawn older positive release. These are historical scope statements.
2. Official GitHub article history records withdrawal on August 10 UTC (`1a245c9...`), assembly of the sharpness-only candidate (`0f3224b...`), and finalization of the verified sharpness release (`0c66eef...`). The corresponding local date is August 9. The date is compatible with the page's publication metadata.
3. The v1.1.7 tagged research log begins August 9 at 20:15 Pacific by opening the closure programme **from the verified weak-class release**, freezing its theorem and verifiers. At 20:27 it records replay of that weak theorem from parent commit `0c66eefc`, including the same rank-eight and quadratic-field payload. This is a direct development chain from the old manuscript; it explicitly does not promote that weak theorem into the strong class.
4. Named GitHub/Zenodo release v1.0.0 was published August 15. Its public description identifies one Outcome A source package with the strong-class classification and both Omega and Theta weak-class sharpness results. Its GitHub assets include a later main manuscript and supplement. Subsequent named releases v1.1.0, v1.1.2, v1.1.3 and v1.1.4 continue that same unified paper line, with proof/replay/submission hardening descriptions.
5. The tagged log records the August 15 consolidation of every active and historical directory for this project under `s_tc_jc_landmark_closure/`. The old article's only later commit, `8fbf2c358eb4ac1e35ce20a0eb30dde42a458c60`, updates its two source links to that consolidated historical module. It does not revise the August 9 scope or create a separate newer theorem.
6. The annotated v1.1.7 tag object is `4da193e200195bcb239acaf29e69a22c215e23b9`, targeting commit `858fc82595910c9e7dd96a8350551248214d624d`, dated August 23 at 09:57:16 UTC. The exact source `main.tex` matches the published source. The certificate envelope binds a separate payload-source commit `fef87ba874b3476ff0383095c67c031ba8c0dc23`; those are distinct roles, not inconsistent manuscript identities.
7. The support deposit was created August 23. The direct-paper record was created August 25 and states publication date August 23. Preserve the direct-paper edition date August 23; do not silently substitute the old page's August 9 date or confuse record creation with publication date.

Two numbering systems must not be confused: the older package's withdrawn `1.1.1` positive attempt and August 9 sharpness-only `2.0.0` audit precede the later unified `stc-jc-sharp-boundary-v1.0.0`/`v1.1.x` release line. Similar numbers are not evidence of the same release.

A historical integration directive found inside the **rejected convention-closure** audit says not to submit the standalone weak ambiguity paper separately if incorporated. Because that directive belongs to rejected material, this decision does **not** treat it as active authority or as proof of incorporation. The actual published manuscript, tagged history, public release descriptions, and source hashes supply the incorporation evidence independently.

## Exact Zenodo identities and what they do not prove

| Record / concept | Publication and role | Documentary conclusion |
|---|---|---|
| Record `22089373`, DOI `10.5281/zenodo.22089373`; concept `22089372`, DOI `10.5281/zenodo.22089372` | Preprint, version `1.1.7`, publication date `2026-08-23`. Fresh `/versions` response contains exactly one record, `22089373`, index 0. Concept endpoint resolves to it. | The canonical direct-paper publication. Zenodo does not formally register the old PDF as a prior version of this concept. |
| Record `22064121`, DOI `10.5281/zenodo.22064121`; concept `22064120`, DOI `10.5281/zenodo.22064120` | Dataset/certificate and reproducibility package, version `1.1.7`, date `2026-08-23`; contains byte-identical article and supplement PDFs. Fresh `/versions` contains exactly one record. | Same current paper's support record, not a second paper. Direct-paper metadata explicitly gives `isSupplementedBy` this DOI. No other related identifier in that direct record asserts a formal old/new version relation. |
| Records `21940945`, `21944479`, `21974911`, `21985363`, `21989619` | Named repository releases for the unified STC/JC paper, August 15–18; each points to its GitHub tag with `isSupplementTo`. | Documentary prior releases in this paper line. Their repository concept is `21753404`, not `22089372`. |
| Repository concept `21753404`, DOI `10.5281/zenodo.21753404` | Fresh versions listing has 19 records spanning JC, mass-action, amplification and diffusion releases. | Not a scientific-work identity. Membership alone cannot merge papers. |

The `v1.1.7` **tag** exists. The official GitHub release-by-tag endpoint returned HTTP 404 for v1.1.7, while earlier v1.0.0 and v1.1.4 releases returned 200. This is recorded accurately; no v1.1.7 GitHub Release is invented. The published Zenodo record, tag/source binding and deposited bytes are sufficient for this identity task.

## Frozen queue reconciliation

The frozen 203-work queue already has one canonical entry `Z-22089372`, record `22089373`, spreadsheet row **53**, inventory index **66**. It gives:

- Row **44**, index **57**, old ambiguity title: `superseded_or_presentation_copy`, canonical record `22089373`; prior semantic relation `historical_edition_or_subsumed_manuscript`.
- The five named earlier JC releases above and support record `22064121`: explicit `related_named_release_or_support_record` dispositions under `Z-22089372`.
- Rejected cleanup-convention attempt at row **250**: excluded separately; it is not this published paper and is not being rehabilitated.

The archived old-PDF candidate supplies a checksum-bound old manuscript at named JC release `21940945` and the later named releases. It also records incidental copies in `22032277`, `22039095`, `22050742`, `22058969`, `22062080`, `22074358`, `22478273`, `22559244`, `22625980`, which are releases for other programmes. Those incidental copies do not establish additional papers. Existing archive-member evidence is preserved; this task did not redownload the 0.8 GB repository ZIPs or claim fresh whole-archive hash verification.

**No queue expansion or redefinition is recommended.** The older named records that could have raised an omitted-work concern are explicitly accounted for. The source relationship now supports, rather than merely assumes, row 44's incorporation disposition. No newly discovered eligible paper record is left unaccounted for by this check.

A title scan of the frozen reconciled public inventory is preserved in `evidence/public-inventory-title-scan.json`. It finds the named records above and other separately queued phylogenetic papers (including 22168797, 22395326 and 22729545). This task does not infer identity or recommend redirects for those papers from shared terminology; it leaves their separate dispositions intact.

## Historical wording and adversarial alternatives

The old page's heading says “The strong-class theorem remains open here,” and its PDF expressly leaves both strong-class classification and triangle-free weak-class identifiability outside its scope. These statements describe the August 9 manuscript and the withdrawal at that time. They are not evidence of a defect in the later August 23 deposit. The old page has not incorporated the later outcome; its “here” wording and date must be read historically.

The following contrary explanations were tested:

- **Different title/hash/page count means distinct paper:** disproved as a sufficient test by the exact old-result-to-new-section map and tagged development lineage. It establishes different editions, which are preserved.
- **Same topic/project/repository concept means same paper:** rejected as insufficient. The repository concept groups unrelated research; the decision instead uses specific proof/witness incorporation and publication descriptions.
- **The later paper merely uses an earlier companion theorem:** possible in general, but here the actual theorem, construction, proof, witness, and verifiers are retained within a unified paper, the tagged programme starts from that frozen manuscript, and the named public releases describe the combined result. No separate paper-specific Zenodo publication or distinct residual companion payload for this old article was identified.
- **The old open wording defeats the new claim:** rejected as an edition-date error. This task grants no new scientific pass and makes no claim about whether the later proof succeeds beyond root's existing clearance.
- **A formal Zenodo version chain decides everything:** rejected. There is only one version under the direct-paper concept; older repository releases have a different, scientifically heterogeneous concept. The work-level decision is documentary, not a fabricated DOI relationship.

The residual limit is explicit: no formal `isNewVersionOf`/`isPreviousVersionOf` DOI link joins the ten-page PDF to 22089373. The conclusion is correspondence by documented incorporation and publication lineage, not formal concept membership or PDF identity. No exact remaining identity uncertainty requires another paper page under the programme's stated rule.

## Evidence and integrity

- `lineage-matrix.json` records stages, dates, identifiers, source locations and the old/new content map.
- `record-hashes.json` authenticates primary local inputs and every public payload/receipt used here.
- `decision.json` is the bounded machine-readable recommendation, including the exact HTML target and explicit PDF prohibition.
- `protected-input-baseline.json` and `protected-input-final.json` show the protected inputs remained unchanged.
- `validation.json` records 67 successful artifact/bibliographic consistency checks; its scope expressly excludes a scientific pass.
- `evidence/queue-selection.json` and `evidence/legacy-inventory-candidate.json` preserve selected frozen inventory evidence.
- `evidence/*-actual-pdf.txt`, per-page text and contact sheets preserve the actual reading basis.
- `public/` contains raw official responses, old exact-commit article/PDF, current record PDFs, tagged source/log and receipts, including the v1.1.7 release 404.

No proof replay was needed or claimed for this bibliographic task. No journal submission, priority, new scientific-PASS or external outreach conclusion is made.
