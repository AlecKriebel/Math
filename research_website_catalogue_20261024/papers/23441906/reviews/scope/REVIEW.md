# Scope and source audit: Zenodo 23441906

**SCOPE COMPLETE — no mathematical PASS assigned.** This is an acquisition, manuscript-scope, attribution and conditional-content audit. Independent mathematical reviews and the root disposition remain separate. No source repair or publication action was performed.

## Identity and authenticated edition

The exact queue entry is row 62, work `Z-23441905`, record `23441906`, titled **A simple brace outside asymmetric products of two trivial braces**, DOI `10.5281/zenodo.23441906`. The fresh record and printed manuscript agree on version **1.0.0** and **17 October 2026**. The author is Alec Kriebel, ORCID `0009-0001-9320-500X`. The record calls it an open preprint with CC BY 4.0 licensing.

Every public asset was freshly acquired from the record API, rather than copied from the historical local audit. Zenodo MD5 values, byte counts and independently computed SHA-256 hashes agree. The main PDF also matches the queue SHA.

| Published asset | Bytes | SHA-256 |
|---|---:|---|
| `simple-brace-counterexample.pdf` | 73,549 | `dc8205d726236da7d61870806ed713ba329dbf4cdfdf049e5570d967d6b7e35e` |
| `simple-brace-counterexample-source-and-verification.zip` | 1,116,255 | `8cc6e65647ff267cb2bd57e5ba5dda4cfc05f72ac11e527517131d9422a8d93d` |

The ZIP contains 79 regular files. Each member was read with CRC checking; absolute/traversal paths, duplicate names and nonregular/symlink entries were rejected by the extraction routine. Originals remain unchanged. `sources/receipt.json`, `extraction-integrity.json` and `reader-pdf-map.json` bind the raw public bytes and extraction.

There is one distinct reader PDF, five pages long. The embedded `output/pdf/simple-brace-counterexample.pdf` is byte-identical to the public main PDF. It is not a second supplement. The candidate therefore has no separate supplement link and offers the full source/verification ZIP once.

## Reading and support boundaries

All five current PDF pages were read. The first page was rendered and visually inspected, including the full abstract, date, version and group exponents. The deposited `main.tex` supplied the literal abstract and exact displayed definitions. The complete original `audit/inputs/PROOF.md` and the `verification/verify_all.py` interface were read. `support-map.json` maps all 79 members by role and hash.

The wrapper names four unchanged standard-library mathematical programs: `audit/reviews/construction_01/check_construction.py`, `audit/reviews/obstruction_01/check_boundaries.py`, `audit/reviews/finite_01/check.py`, and `audit/root_reproduction/symbolic_ingredients.py`. It describes ordinary/optimized replay and expected-result comparisons in temporary mirrors. **This scope role did not execute those programs, inspect their historical result bodies, or infer correctness from old success claims.** Independent mathematical reviewers must establish their actual current outputs and proof relevance.

The older full-proof support contains additional fixed-set, center and derived-subgroup checks in its §7; these are not additional claims introduced into the current five-page page candidate. Its final proof-only packaging discussion reflects a retained earlier support edition, whereas the current public ZIP actually contains the programs and receipts listed above. Neither that historical packaging statement nor the historical computation counts were used as current acquisition evidence.

## Exact mathematical scope mapped

The following are claims of the assessed manuscript, not mathematical conclusions certified by this scope audit.

- A **left brace** has an abelian additive group, a multiplicative group, and `a∘(b+c)=a∘b−a+a∘c`. It is not an arbitrary skew brace with nonabelian addition. The star operation is `a∗b=λₐ(b)−b`; it need not be associative in a general left brace.
- **Simple** means the nonzero brace has only the ideals `0` and itself. An ideal is additive, lambda-invariant and multiplicatively normal. This is not simplicity of the multiplicative group, and it cannot be replaced by a test of arbitrary left ideals or coordinate subspaces.
- Theorem 1 is an **existence statement** for a particular brace of order `20,000=5⁴·2⁵`. Its additive group is `C₅⁴×C₂⁵`; its multiplicative group is `(C₅³⋊τ C₂)×(C₂⁴⋊M C₅)`. The involution negates the first and third coordinates of `F₅³`, and `M` rotates the five coordinates of the four-dimensional binary even-weight subspace. It claims a nonabelian metabelian multiplicative group and abelianness of **every** multiplicative Sylow subgroup; it does not assume those Sylows are normal.
- The construction uses `R=xF₅[x]/(x⁵)`, the even-weight `V⊂F₂⁵`, and an extra `F₂` coordinate. Its logarithm/exponential are finite identities through degree four, with denominators invertible in characteristic five. No infinite-series or characteristic-zero assumption is present.
- The nonpresentation assertion is invariant under **every brace isomorphism** and every choice of two trivial factors or coordinates. It is not merely failure of a selected bilinear parameterization, a particular factor order, or a chosen factor size.
- Lemma 2 is universal for **finite** braces with a two-trivial-factor asymmetric-product presentation and abelian multiplicative Sylow subgroups. It assumes neither simplicity nor metabelianity. It asserts `(a∗b)∗c=0` for all three elements in the **same additive Sylow subbrace**. The left association and same-prime restriction matter; it makes no unrestricted mixed-primary triple-product assertion.
- The general presentation starts from a **normalized symmetric 2-cocycle**, not biadditivity as an extra premise. The manuscript derives biadditivity from brace admissibility in the trivial-factor specialization. Its additive primary part can have a twisted group law, especially at two; the argument uses cardinality and closure rather than an unjustified direct-product splitting.
- On the particular 5-primary subbrace, star multiplication is ordinary ring multiplication and the displayed witness is `(x∗x)∗x=x³≠0`. The written argument, not a finite enumeration of possible presentations, is intended to make the exclusion universal.
- There is no least-order claim, full classification of finite simple braces, exclusion of products with nontrivial factors, or exclusion of general matched products. The paper claims no new general asymmetric/matched-product formalism.

The mathematical gates for other reviewers are therefore explicit: the general cocycle-to-biadditivity step and primary-subbrace reasoning; the group-coordinate isomorphism and lambda additivity; the proof for **every** nonzero ideal; and the isomorphism-invariant obstruction, with finite computations serving as controls rather than substitutes for universal proofs.

## Original question and primary interfaces

Fresh primary bodies are retained under `cache/primary-sources/`, with byte hashes and access receipts. Exact portions read are recorded in `primary-interfaces.json`; no claim of reading every page of every primary paper is made.

| Primary source and exact inspected interface | Scope relevance |
|---|---|
| Cedó, *Finite simple left braces: constructions and problems*, OWR 51/2019, printed pp. 3226–3228; Problem 9 on printed p. 3228 / PDF page 22 | The original question has precisely the finite, nontrivial, simple, metabelian and abelian multiplicative Sylow hypotheses stated in the current note. It asks about two trivial left-brace factors, with no size or elementary-additive restriction. The original problem page was also rendered and inspected. |
| Bachiller–Cedó–Jespers–Okniński, arXiv `1705.08493v1`, §3, Theorem 3.1 and surrounding formulas, PDF pp. 6–7 | Supplies the left-brace version of the normalized symmetric-cocycle asymmetric product, with the exact twisted addition, semidirect multiplication and lambda formula. Its bilinear discussion is explicitly a special case; it is not the complete initial definition. Lemma 3.2 states the ideal star-closure tool. |
| Cedó–Jespers–Okniński, arXiv `2001.08905v1`, §2, Theorem 2.2, Lemmas 2.1 and 2.3, PDF pp. 2–3 | Repeats the general definition and subtraction/lambda formulas. It explicitly distinguishes the twisted additive extension from the ordinary direct product, and gives a characteristic-two obstruction to a naive splitting. The universal invariant must retain this distinction. |
| Bachiller, arXiv `1511.08477v3`, §4, Definition 4.1, Theorem 4.2, Definition 4.3 and Example 4.6, PDF pp. 11–14 | Provides the established matched-product framework and decomposition over additive primary left ideals. A matched-product realization alone does not prove simplicity, and being outside two **trivial** asymmetric factors does not exclude this broader construction. |

The original Catino–Colazzo–Stefanelli 2016 published page was located. The search service exposed its Section 3 / Theorem 3 right-brace construction, but direct page opening returned HTTP 403 and no authenticated full publisher PDF was acquired. The needed **left-brace** interface was checked in the two fresh primary author-preprint bodies above, both explicitly crediting that theorem. This distinction is retained; the audit does not claim a complete newly downloaded 2016 body or exact final-journal-version comparison.

The 2020 *Abundance* publisher page confirms the cited bibliographic attribution but requires subscription for the PDF. It is background here: the current construction and all-ideal proof are presented directly. No theorem proving all examples belong to a known family is imported. The recent papers and inaccessible Rump bodies discussed in the manuscript's historical priority paragraph were not independently screened for every possible implication in this scope assignment. Consequently no present-day novelty, priority or continuing-open-problem conclusion is supplied.

Attribution is preserved to Cedó's question; Catino–Colazzo–Stefanelli's asymmetric products; Bachiller's matched products; Bachiller–Cedó–Jespers–Okniński and Cedó–Jespers–Okniński's simple-brace constructions; and established radical-ring, truncated-logarithm and orthogonal-action methods. The conditional page should say it addresses the original question, not advertise a new construction formalism or certify a first-ever resolution.

## Conditional candidate and abstract fidelity

`content.json` is **candidate-only**, conditional on separate mathematical review and root publication approval. It supplies the complete original abstract, a plain explanation, exact theorem scope, proof mechanism, limitations, five primary-source attributions, a professional substantive-collaboration invitation and the published ZIP link. `follow_up` is `null`: this scope audit established no unusually strong new research question to recommend.

The entire TeX abstract was extracted to `abstract.tex.txt`. `abstract-check.json` compares the content abstract directly to that actual source after only explicit accent, mathematical-symbol and whitespace conversions. All original sentences remain; no historical audit sentence was silently removed from the abstract. The explanatory prose contains no dated verification replay or numerical test-count narrative. Version/date are the actual v1.0.0 / 17 October 2026 edition, without backdating an earlier proof-support history.

The candidate's status is an unrefereed preprint and it discloses extensive AI use. The invitation requests substantive mathematical collaboration; no outreach has been initiated or prepared for a named person. Coauthorship is tied to contribution, not merely endorsement or submission.

## Independence and exact disposition

The fresh record description, current manuscript, and necessary original proof contain incidental historical mathematical acceptance and priority-screen claims. These were encountered and are explicitly itemized in `independence.json`; none was adopted as fresh evidence. Archive filenames exposed assessment/status names, but dedicated historical review, priority, implication and expected-result bodies were kept opaque. No current sibling mathematical findings or reports were read.

**Strongest scope conclusion:** the exact five-page edition and all public supporting bytes are authenticated; the complete current manuscript is read; its terminology, original question, general asymmetric-product interface, existential/universal distinctions and public-content boundaries are mapped. **Remaining mathematical disposition:** separate analytic/adversarial reviews and root assessment. This scope audit assigns no mathematical PASS and does not authorize promotion.

The final custody check confirms both public assets and all 79 extracted files remain byte-identical. There were no changes to the completed JC review, no repairs to this paper, and no site, spreadsheet, Git, deployment, UI or external-communication actions.
