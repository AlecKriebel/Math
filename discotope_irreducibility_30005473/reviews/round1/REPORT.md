# Fresh adversarial preprint review — round 1

Reviewed author: Alec Kriebel, ORCID 0009-0001-9320-500X. Review began 2026-10-01 UTC / 2026-09-30 America/Los_Angeles. This is an independent AI review, not human peer review or formal certification. No external individual was contacted; no publication, branch change, commit, or push was performed.

## Verdict on the frozen target

**No mathematical defect has been found in the assembled manuscript. One required packaging repair prevents a clean publication-readiness verdict for this frozen archive.** The manuscript's two theorems follow from the stated hypotheses; they answer the exact 2023 exposed-point conjecture and the original 2022 generic purely nonlinear-part conjecture separately. Historical first priority remains unconfirmed, as the manuscript appropriately states.

The inspected objects are the full `paper.tex` and every page of its four-page PDF, source-and-verification archive, upload kit, metadata, source provenance, manifests, pinned checks, and completed bounded priority reports. Frozen identities:

| Object | SHA-256 |
| --- | --- |
| `paper.tex` | `3576dcc78bf1a9188ee8a8b5c56f5914357d90d437767e29dc42e3a85ceedab4` |
| `paper.pdf` | `c13dc861e8e5b5c1d980bdd78d14aff8e4b1a130800c4f942b3bedafbc5f6b2a` |
| `source-and-verification.zip` | `bd03b7a8bee9c8f4efdaac2fcf83f424be3a0570a3c5a57313f70822ce449a85` |
| `zenodo-upload-kit.zip` | `e4f4c499f763f31a053449b97409b5d423338d66177f66805f9ed8a7a30d2b33` |

Initial review verdicts were not consulted before independently deriving this reviewer's proof assessment. Independent child audits separately attempted mathematical falsification and checked archive/reproduction details. Their reports are retained in this folder. The fresh reports necessarily postdate this frozen archive and must be included in the final rebuilt review package.

## Required repair

**P1 — Public archive includes substantial third-party source-text captures despite its exclusion policy.** `build_package.py`, lines 56–73, permits all non-hidden priority JSON recursively. This includes:

- `priority/equivalent_results/web_results_archive.json` (372,235 bytes);
- `priority/equivalent_results/web_results_archive_addendum.json` (99,392 bytes);
- `priority/equivalent_results/citation_subaudit/evidence/search_responses.json` (129,988 bytes).

These are raw retrieval responses, not solely original query and URL/hash evidence. For example, the first archive's `results.open02` is a 3,739-word combined response containing 379 extracted source line markers; the citing-audit capture's `responses.content_checks` contains 3,191 words and 180 source line markers. They reproduce substantial third-party PDF/HTML passages. `PACKAGE_MANIFEST.json` explicitly lists “third-party source PDFs and full-text extracts” as excluded; `priority/README.md` and the equivalent-results report also describe full extracted texts as local-only. The packaged bytes do not satisfy that declared boundary. This is a public-assembly defect; it does not invalidate the proof or the bounded priority findings.

**Exact repair:** explicitly exclude these three raw-response files (or replace the suffix-wide priority selection with an explicit publishable inventory). Retain the concise reports, exact original query strings, retrieval metadata, source URLs/hashes, source-comparison records, and concise original findings. Keep raw response captures, publisher PDFs, page renders and OCR derivatives as local audit evidence. Clarify the artifact list in `priority/equivalent_results/priority_report.md`, lines 137–146, and the citation-subaudit evidence description so that local-only artifacts are unambiguous to a reader of the public ZIP. Rebuild both archives and their manifests/checksums, confirm the raw files are absent, and commission the requested fresh adversary against the resulting hashes.

**Final assembly requirement:** include the completed fresh manuscript/package review artifacts in the rebuilt ZIP. The currently frozen ZIP contains only the historical `reviews/initial_*` reviews. It should not be presented as containing the finished new-manuscript review until this assembly step occurs. This is expected sequencing rather than a second scientific defect.

## Exact conjecture and attribution checks

I independently read the publisher PDF of [Gesmundo–Meroni (2022)](https://lematematiche.dmi.unict.it/index.php/lematematiche/article/download/2338/1156/6734) at Definition 3.3 (printed p.149), the parameter conventions (pp.146–147), the earlier special cases, and Conjecture 8.2 (p.167), with visual checks of the definition and conjecture pages. Its target is the complex closure of sums of relative summand-boundary points lying on the total boundary. The original paper assumes full dimension after replacing the ambient space by the sum's span.

I independently read the exact definition and Conjecture 1 on printed p.830 of the [official 2023 OWR report](https://publications.mfo.de/bitstream/handle/mfo/4031/OWR_2023_15.pdf?sequence=4), including the adjacent explanation of genericity. Its target is the exposed-point closure. The manuscript correctly separates this E from the 2022 S, and does not rely on their definitions being automatically equivalent.

The earlier generic low-boundary-dimension and two-dimensional cases and the full-dimensional-summand case receive explicit credit, as does the original support-gradient analysis. The Kucharz–Kurdyka observation was checked visually on printed p.95 of the [primary 2017 article](https://ruj.uj.edu.pl/server/api/core/bitstreams/52a654f7-4489-46d9-8157-6c7715c24f3e/content): the opening step in the proof of Proposition 4.3 explicitly gives the real analytic-image irreducibility mechanism. The candidate credits this precursor and independently proves the complex-coefficient version. It makes no false claim to have discovered that general analytic principle.

## Independent mathematical reconstruction and falsification

### Connected regular-normal domain

For injective real A_i of rank m_i, ker(A_i^T) has codimension m_i, including repeated matrices and coincident spans. With every m_i at least two, each enlarged excluded space M_i+Rx or M_i+Ry in Lemma 2 has dimension at most d−1. A finite union of these proper real subspaces cannot exhaust R^d. Choosing z outside the enlarged spaces rules out every point of both open segments entering any M_i. The endpoints are also regular. This proves the stated two-segment path construction without a general-position assumption.

There is no d=1 exception hidden in this reasoning: an existing rank-at-least-two summand already forces d≥2. The finite nonempty summand hypothesis excludes the empty-sum issue. Lower-dimensional total sums leave extra normal directions but do not change the individual kernel codimensions or connectivity.

### Exact exposed-face parametrization

The support formula follows by maximizing (A_i^T u)·v over the unit ball. If A_i^T u is nonzero, Cauchy–Schwarz gives exactly one maximizing v and hence exactly one support point. If it is zero, every point of the positive-dimensional disc maximizes.

For any decomposition of a point in the sum, the support deficit is a sum of nonnegative individual deficits. It vanishes exactly when each term vanishes. Thus the exposed face of the sum is exactly the Minkowski sum of the individual faces. Fixing points of the other faces embeds any nonsingleton summand face into that sum by a translation, so cancellation cannot turn it into a singleton. Conversely, a sum of singleton faces is singleton. Consequently Exp(D)=F(U) is an exact set equality, not a dense-subset claim. Repeated discs and nonunique representations do not invalidate it.

Every real radicand on U is strictly positive. The positive square-root branch is analytic there, regardless of dependence among quadratic forms, and no complex square-root continuation is used. Neither injectivity nor immersion of F is needed. Lower-dimensional and repeated/coincident examples therefore remain covered by the same proof.

### Complex irreducibility rather than merely real irreducibility

The vanishing ideal of F(U) is proper because U is nonempty. For arbitrary complex-coefficient P,Q with PQ vanishing on F(U), if P does not vanish identically, continuity gives a nonempty open region where P∘F≠0 and therefore Q∘F=0. The real and imaginary parts of Q∘F are real analytic. Connected openness and the identity theorem force both to vanish everywhere. This proves primality in C[X], directly establishing complex irreducibility.

The manuscript's elementary identity-theorem justification is valid: at a limit of neighborhoods of vanishing, continuity of all derivatives makes every Taylor coefficient vanish at the limit point; a convergent local Taylor series then supplies a vanishing neighborhood. This is stronger than connectedness of the image alone and avoids the false inference that an arbitrary real irreducible polynomial must remain irreducible over C. No hidden algebraic-independence or complex critical-locus hypothesis appears.

### Generic S=E bridge and limiting perturbation

The inclusion E⊆S follows because every individual regular support point is on its relative summand boundary. In the other direction, full dimensionality ensures a nonzero supporting normal at the chosen boundary point. A representation by summand-boundary points maximizes that normal term by term, by nonnegative support deficits.

For the killed set J, all its spans lie in u-perp. GP therefore forces sum(m_j)≤d−1 and linear independence of all concatenated columns A_J. Hence A_J^T is surjective. Representing x_j=A_j v_j with unit v_j is legitimate for every ellipsoid because A_j is a linear homeomorphism onto its span; orthonormality is unnecessary. Solving A_J^T w=(v_j)_j is exactly the dual prescription needed.

With epsilon>0, every killed summand satisfies A_j^T(u+epsilon w)=epsilon v_j, and its support point equals x_j exactly. For a remaining summand with a_i=A_i^T u≠0 and b_i=A_i^T w, the explicit bound epsilon<||a_i||/(2||b_i||) suffices when b_i≠0; if b_i=0 it imposes no bound. The finite minimum preserves all remaining nonvanishing conditions. Their support points converge by continuity. A complex algebraic set is closed in the ordinary complex Euclidean topology, so the real limiting point belongs to E. There is no interchange of an algebraic closure with an unsupported limit operation.

The zero killed-set case is handled directly. A positive epsilon is essential for the prescribed rather than negated killed support points, and the manuscript uses the correct sign. If J is nonempty, the perturbed normal cannot become zero because one of its images equals a nonzero epsilon v_j. No perturbation-gap or cancellation assumption remains.

### Genericity witness

For each subset of summands, concatenated maximal rank is the nonvanishing of at least one maximal minor; its failure is algebraic. Finitely many subsets give one Zariski-open condition. Distinct real Vandermonde columns furnish a simultaneous witness: any k≤d columns are independent because the first k rows already form an invertible Vandermonde matrix; more than d columns contain d independent ones. This covers all prescribed block sizes m_i≤d and is independent of ellipse shape. If the total dimension is at least d, the same witness makes the total span all of R^d. In a smaller total span the original source's ambient reduction applies. The bridge therefore covers every feasible generic type in the stated conjecture.

### Boundary cases and the separating example

Rank-one summands cannot be admitted into the universal conclusion: one segment has two exposed points, and the disc-plus-segment example has two distinct complex conics. The conics are irreducible over C and distinct for a>0; each real open semicircle is dense in its conic. There is no missing connecting exposed arc when the horizontal normal coordinate vanishes, since the exposed face then includes a segment.

In the repeated-disc example, the total span is R^3. The normal e3 exposes 2B_xy+e3; e3 belongs to this face and is representable by three relative boundary points. On every regular normal, setting a=2u1/r and b=u1/s gives a²+Y²=4, b²+Z²=1 and X=a+b. These identities make the displayed P vanish. P(e3)=16 separates e3 from the entire complex closure E, rather than only from one support parametrization or its real image. The example demonstrates S≠E outside GP without making a stronger claim that S is always reducible there.

## Distinct exact stress evidence

`math_stress.py` and `math_stress_results.json` are independently constructed supplementary checks. They use CPython 3.14.6 and SymPy 1.14.0 in the fresh archive-audit environment. They do not modify any canonical manuscript or original snapshot. All assertions passed.

The main new test uses ranks (2,2,3) in R^5, with nonorthonormal Vandermonde blocks. All seven nonempty subset ranks satisfy GP. The first four columns lie in e5-perp and have top-four determinant 12; the third block has rank three and is not killed. Two unrelated rational unit targets are prescribed simultaneously through the exact transpose solve. The test verifies the killed support points identically for positive epsilon and the remaining summand's limit. This stresses the actual mixed-rank, multiple-kernel mechanism with a nontrivial dual solve rather than assuming coordinate orthogonality. It also checks an independent squared-auxiliary reduction of P, its separating value 16, and the reduction of three repeated rank-two discs in R^4 to one scaled lower-dimensional ellipse.

These are finite corroborations. The universal proof assessments above are mathematical deductions from the hypotheses, not extrapolations from the checks.

The separate fresh proof falsifier also independently reconstructed both theorems without reading this report, the historical reviews, or the canonical scripts. Its `math_falsifier.md` records no actionable mathematical defect and a distinct dependency-free exact construction, 30 subset-rank checks across six types, an explicit two-kernel perturbation, and exact separator reduction. Reproducible inputs and outputs are retained publicly in `math_falsifier_exact_checks.py` and `math_falsifier_exact_results.json`. The same reviewer tested the failure of the analytic lemma for a merely smooth map into two coordinate axes, supporting why real analyticity rather than smoothness is the operative hypothesis.

## Bounded priority and document assessment

I read the completed exact-target, equivalent-results and citation-subaudit reports only after deriving my own mathematical assessment. Their distinction among the exact target, existing ingredients, earlier special cases, and unconfirmed application priority is appropriate. Source and retrieval limitations are explicitly recorded. The manuscript, abstract, README and Zenodo description all avoid asserting historical first priority or claiming the entire complex critical locus, degrees, or birationality has been settled.

I independently spot-checked the older full-rank radical support theorem (Chirikjian–Shiffman, Theorem 1.1), the componentwise convex-duality statement in Sinn's Corollary 3.4, and the 2026 Operatopes full text's discotope references. These checks corroborate the reports' exact gaps: a full-rank support formula, a componentwise duality theorem, and class inclusion respectively are not documentary evidence of the complete theorem being presented here. The standard analytic mechanism really is older. A bounded negative search does not prove first priority, and the package does not claim it does.

All four PDF pages were rendered and visually inspected. Equations, section transitions, mathematical symbols, references, hyperlinks, page numbers, title, author and ORCID are legible and coherent. I found no layout error or source/PDF statement discrepancy. The AI and unrefereed-status disclosures are clear. The metadata's title, author, version/date, citation identifiers, claim scope and license division match the manuscript and documentation.

The archive audit's full integrity/reproduction conclusions are recorded separately in `archive_audit.md`; concise target, integrity, environment and pristine-rebuild evidence is in `archive_evidence.json`, with no raw third-party captures. Fresh reruns passed in the pinned CPython 3.14.6 / SymPy 1.14.0 / mpmath 1.3.0 environment; the original output was byte-exact and all 16 original snapshot files remained unchanged and matched the immutable local Git commit. A pristine extracted rebuild reproduced both ZIPs byte-for-byte. All member hashes, archive integrity, metadata and kit consistency passed. No credentials, installed dependencies, symlinks, unsafe paths, or third-party PDFs were located. The source-text-capture defect above remains the material exclusion failure.

The repair above must be made before promoting the package as clean; a subsequent independently commissioned review must bind the rebuilt artifacts. This review does not authorize publication execution.
