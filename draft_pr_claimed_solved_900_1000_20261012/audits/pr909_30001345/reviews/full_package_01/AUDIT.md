# Full-package adversarial review 01 — PR909 / problem30001345

## Decision

**PASS for rigorous mathematics, accurate source attribution, reproducibility, and truthful preprint presentation under the expressly attributed classical-corollary framing.** No required or optional technical, mathematical, source, code, PDF, metadata, or editorial correction remains in this frozen candidate under that framing.

`required_issues=[]` and `optional_issues=[]`.

This is the first new whole-package review, not final project acceptance or a completed sequence of reviews. It does not establish a new construction, method, first priority, present-day openness, independent human peer review, or resolution of the later unibranched conjecture. The frozen candidate itself correctly declines those claims. The separately recorded administrative disposition boundary remains distinct from this technical verdict.

## Identity, evidence, and independence

The review began by reading the complete final `note.tex`, then recording `INDEPENDENT_PRE_CROSSCHECK.md` before reading previous family verdicts. The theorem, geometric incidence, factorization, analytic flatness, component-product integral closure, special-fiber normalization, fixed-ball boundary link, local canonical calculation, all-n argument, and n=2 boundary were reconstructed at that stage. Subsequently the complete original frozen proof, all seven current family reports and their digest maps, operative checkers, release tools, source/priority records, framing/synthesis records, metadata and actual live PR description were cross-checked.

This is a new clean-context AI review, not a blind review: the assignment supplied coefficients, expected pins, source leads, and the administrative scope. The final note was a starting input. The initial mathematical derivation preceded family verdicts; the additional finite checker was written after later code inspection and is not falsely presented as a pre-inspection implementation. Shared family primary PDFs were used read-only with their actual fingerprints; this reviewer did not independently download them or redo the literature-wide priority search. No other reviewer or human was contacted. Communication was limited to internal progress reports to the parent.

All writes are confined to `reviews/full_package_01/`. Original and candidate files, Git/index/branches, PR, tracker, Zenodo and external accounts were not modified. The retained trusted environment was reused; nothing was installed or deleted.

Authenticated identities:

| Artifact | Verified identity |
|---|---|
| `PREPUBLICATION_FREEZE.json` | SHA256 `c58e74cd19d42ac1b867dc9add2f6c3ab9075248dcac0e19432f851ccba7509f`; every one of its 14 listed byte lengths/hashes matches |
| Archive | 300566 bytes; SHA256 `291becf72ccd6345701711ab8523cf0966b042ce147e907cefdeb4bece014fd0` |
| External package-manifest anchor | SHA256 `0189e0ecd7bb39a1ed3899ee785cfc9f48bae7fdf386cd3002fd0a4849b70313`; 105 payload files and the self-excluded manifest, with no duplicate ZIP names |
| Separate and archived PDF | Identical 71492 bytes; SHA256 `44ddb6ad4b454398ef50f0f3e52a8810eb6c88638ba05e8d32055712a8bd0a75`; four pages |
| Original | Head label `d186dea31791cd3e8acf6829e0b65d01849623b8`; every one of 28 `ORIGINAL_SNAPSHOT.json` files matches |
| Original proof | SHA256 `561b189c2091eaeccccf89fdd933b2300ec676a871d7229ebfaf8c806962fe8b` |

The original snapshot is also bound by the externally authenticated archive, which contains it and the same 28 historical files. This review did not independently fetch all original Git blobs; it authenticates the supplied snapshot and current live head against the supplied immutable identity. `AUTHENTICATION.json`, `FAMILY_MANIFEST_CHECK.json` and `LIVE_PR_CHECK.json` preserve these distinctions. All seven current family maps have matching public bytes and self-excluded manifest treatment.

## Exact claim and independent mathematical reconstruction

The actual theorem is existence over all complex |t|<1/4 of a reduced flat holomorphic plane-curve family in the open unit ball, with finite simultaneous normalization, nine normalized disks on every fiber, a common smooth disjoint transverse boundary link, one central ordinary ninefold point, and exactly twelve ordinary triple points on each nonzero fiber. All singularities remain inside radius 1/2. Total delta is 36 throughout, while the sum of rough K(K+D) rises from 7 to 12. The all-n extension asserts excess n²−4 for every integer n>=3. These are precise existence statements for the constructed central tangent directions.

The projective groups X=omega^i Y, Y=omega^j Z, Z=omega^k X have three coordinate vertices and nine mixed intersections [omega^(i+j):omega^j:1]. At each mixed point exactly A_i, B_j and C_(-i-j) occur. Distinct indices give distinct points, none a vertex. All twelve points are ordinary triples, and 12*C(3,2)=C(9,2)=36 accounts for every pair. This proves completeness, rather than merely substituting a proposed finite singularity list into a Jacobian.

The identification with the dual-flex construction is concrete: the nine line-coefficient vectors (1,−q,0), (0,1,−q), (−q,0,1) are the nine flex points of the smooth Fermat cubic X³+Y³+Z³=0. For example at (1,−q,0), its tangent is X+q²Y=0, and restriction of the cubic to that line is Z³, proving triple contact. The other groups follow by cyclic permutation. Thus the earlier dual-flex example is the stated geometry, not merely a bibliographic configuration with matching counts.

L=X+2Y+4Z misses every intersection: it is nonzero at vertices, and its modulus at a mixed point is at least 4−2−1=1. Consequently no affine pair is parallel. Substitution of Z=(t−x−2y)/4 yields exactly the nine stated factors and the polynomial F, without an extra vanishing parameter factor. Its x^9 coefficient is −65. The central factors therefore have nine distinct directions and every fiber is reduced; multiplication by t identifies each nonzero fiber with the entire affine arrangement.

Polynomial division by the monic multiple −F/65 gives freeness of rank nine over C[y,t]. Analytic flatness also follows directly: in A=C{x−x0,y−y0,s}, s=t−t0, an equality sg=Fh reduced modulo s forces h=sh1, since F_t0 is a nonzero germ in the domain C{x−x0,y−y0}. Cancellation gives g=Fh1. Thus A/(F) is torsion-free over the base DVR and is flat. This includes all component intersections and t=0 and survives open restriction. Delta constancy is not used to assume flatness.

For normalization, the total space is reduced and nonnormal. Every component plane is a smooth graph over (y,t). In the ambient regular factorial ring, the distinct linear prime ideals intersect as their product. Hence the reduced quotient injects into the product S of nine component rings. S is finite as a module, normal, and has the same total fraction ring. If an element of that total fraction ring is integral over the quotient, its monic equation also has coefficients in S, so normality places it in S; conversely S is integral by finiteness. This proves the total-space integral closure. At every fixed t, including zero, the nine factors specialize to distinct smooth lines, and S/(t−t0)S is their disjoint union. This separately proves fiberwise normalization, without assuming normalization commutes with base change in general. The normalized projection is smooth; the original total space is not claimed smooth or normal.

The three vertex chart coordinates are (1,0), (0,1/2), (0,0). Mixed coordinates have both numerators of modulus one and denominator modulus at least one, so their norm is at most sqrt(2)|t|<1/2. For a component ax+by+ct=0, the closest point is p(t)=−ct*(conj(a),conj(b))/(|a|²+|b|²), and v=(−b,a)/sqrt(|a|²+|b|²) is a fixed perpendicular unit direction. Its points are p(t)+zv with norm squared d(t)²+|z|². The A/B/C distance bounds are 0, |t|/sqrt(5), |t|/sqrt(13). Thus every line cuts a disk with a transverse boundary circle p(t)+sqrt(1−d(t)²)e^(i theta)v. All pair intersections are inside radius 1/2, so these circles are disjoint. This verifies the union's boundary, not just componentwise transversality. Along parameter paths these explicit embeddings give an isotopy of links. At zero the cone has the same link at every positive radius, and homogeneity rescales to arbitrary small representatives. The finite normalization remains proper after restriction; open-ball projection need not be proper. The closed ball is used only for boundary/topological statements.

For an ordinary r>=3 point, one blowup gives E²=−1 and E.C'=r. Adjunction uniquely fixes the exceptional-supported local canonical divisor K=+E. With D=C'+E, rough K(K+D)=E(C'+2E)=r−2. Delta additivity for relatively prime branches gives delta=C(r,2). A node is already normal crossing and has rough zero, agreeing with r−2 at r=2. Therefore the actual ordinary-nine point gives (delta,rough)=(36,7), while twelve ordinary triples give (36,12). K+D is relatively nef on the single exceptional curve, with intersection r−2>=0, so N=0 for these points. No fine-sign convention changes the calculation. No arbitrary extra smooth-point blowup, branch-shifted convention, or analytic normal form x^r−y^r is silently substituted.

For every n>=3 the same exact-order root-of-unity argument gives three ordinary n-fold vertices and n² other triples, exhausting all pairs. The same L bound works for every n, and the same component, flatness and boundary reasoning applies. The analogous polynomial has leading coefficient (−4)^n−1, never zero. Pair and invariant arithmetic gives

    3*C(n,2)+3*n²=C(3n,2),
    3*(n−2)+n²−(3n−2)=n²−4.

This proves the universal extension structurally, independently of finite loops. At n=2 the nearby inventory is three nodes and four triples; delta15 and rough4 agree with the central ordinary-six point. At n=1 the nominal vertex points are smooth, so the r−2 singular-point formula is inapplicable there; that case is outside the claim.

No hidden central unibranchness, irreducibility, open-ball properness, arbitrary-tangent-moduli adjacency, or equinormalization theorem supplies an unproved central step. The origin marked section has nearby rough value1<=7, so a marked-section conclusion is not inferred. Nine normalization disks have zero geometric genus but do not constitute a unibranched central fiber.

## Primary-source and priority checks

Complete relevant primary pages were inspected directly, including twelve rendered page images. Actual shared-body hashes, exact page scopes and upstream retrieval provenance are recorded in `SOURCE_INSPECTIONS.json`; raw bodies/extracts/renders are privately ignored and excluded from this public map.

* **[OWR, DOI10.4171/OWR/2009/43](https://ems.press/content/serial-article-files/46242?nt=1), printed2446–2448:** the visible bar and displayed K(K+D) identify the rough invariant. Questions2–3 themselves contain no sum or unibranch hypothesis. The following fixed-ball setup uses multiple nearby singularities and compares sums; later one-branch/cusp-node hypotheses serve specialized estimates. This supports the note's declared unrestricted summed reading, without proving an unstated authorial intention.
* **[Published Borodzik2014, DOI10.18910/50809](https://ir.library.osaka-u.ac.jp/repo/ouka/all/50809/ojm51_03_573.pdf), printed575–578:** Definition2.1 makes parametricity rational AND unibranched. Definition3.3 fixes the selected rough convention; Remark3.4 warns of the other multibranch shift; Conjecture3.8 assumes parametricity. Page578 supplies the contraction precedent and ordinary d−2 value. Its positive-genus Hirano example is not relabeled the present delta-constant theorem. The journal passage, rather than an earlier arXiv version lacking additions, supports these citations. OWR and journal fine-sign differences are immaterial because N=0 here.
* **[De Jong–van Straten1998, DOI10.1215/S0012-7094-98-09513-8](https://download.uni-mainz.de/mathematik/Algebraische%20Geometrie/DvS-Publikationen/Deformation%20theory%20of%20sandwiched%20singularities%20-%201998.pdf), printed475–476,480,502–504:** Definition4.2 requires delta constancy and a normalization product; picture deformations admit ordinary multiple points. Example6.6 gives exactly nine dual-flex lines, twelve triple points, no further intersections and an explicit incidence list. This is affirmative deformation-theoretic precedent. These pages do not state the rough-M inequality.
* **[Plamenevskaya–Starkston2023, DOI10.2140/gt.2023.27.1083](https://msp.org/gt/2023/27-3/gt-v27-n3-p04-p.pdf), printed1109,1193–1195:** Definition2.7 specifies the delta-constant/simultaneous-normalization setting. Example8.7 explicitly scales the constant terms of straight-line equations to zero. Its illustrative configuration has eleven lines; its statement applies to arrangements generally. This supplies the established mechanism, not a previously stated rough-M comparison.
* **[Hirzebruch1983, DOI10.1007/978-1-4757-9286-7_7](https://hirzebruch.mpim-bonn.mpg.de/id/eprint/244/1/hirzebrucharr.pdf), printed118–120:** the p119 table supplies 3n lines, n² triples and three n-fold points, with the overlapping n=3 categories expressly interpreted as twelve triples. The note's classical all-n attribution is supported.

The seven family reports consistently support the scoped mathematics, separate source intent from text, record historical and runtime limitations, and reject stronger novelty/current-open framing. Prior construction plus standard scaling and the ordinary-point value yields the theorem by the explicit bridge above. That establishes classical-corollary status; it does not establish earlier publication or awareness of the exact7-to12 rough-M failure. Neither this review nor the bounded prior searches certify firstness or current openness. The candidate consistently credits configuration, method and invariant precedent, and makes the appropriate narrower claim.

## Executed controls and release-code inspection

The actual archive was safely extracted only after external authentication. Every extracted payload was independently compared with its externally pinned manifest before supplied code was run. Work directories and mutation fixtures remained outside the extracted closed package. The retained CPython3.14.6/SymPy1.14.0/mpmath1.3.0 environment was reused. Historical Python3.12.14 process claims are not newly authenticated by this cross-version replay.

`verify_package.py`, `run_checked.py`, the separate hardened verifier, historical verifier/wrapper/checkers, current exact/boundary/invariant controls, and build/freeze/metadata/guard tools were read. The release verifier enforces strict keys and integer types, duplicate/nonfinite JSON rejection, exact regular-file/directory inventory, safe names, byte lengths/hashes and fixed original provenance pins. Full replay requires an external package-manifest digest. A manifest stored beside its own payload cannot supply trust by itself; both the documentation and the review preserve that qualification.

Crucially, `worker()` validates the actual disposable copy before executing any copied wrapper/checker and validates copy/source again afterward. The child wrapper enforces isolated, nonoptimized execution. Result comparison checks exact recursive scalar types, so booleans and floats cannot masquerade as integers. Historical audit A's assertions and direct optimized weakness remain documented; its supported wrapper and current isolated normal execution preserve active assertions. Historical permissive schemas/inventories are handled by the separately pinned28-file verifier without changing original bytes. Code and documentation make no sandbox/signature/concurrent-attacker/formal-proof claim.

Fresh evidence, separate from saved original PASS files:

| Control family | Result |
|---|---|
| Initial normal full archive replay | PASS; original28 files and all current mathematical controls reproduce |
| Four reviewer-controlled full replays | Normal, −O, −OO and genuinely inherited PYTHONOPTIMIZE=2 all PASS with identical output SHA256 `75945efbfa735b92d5df83bfa676c733e0b3c0eb920a7cb179e96d6bbfddca7f`; all four checker guards report isolation1/optimization0 |
| Reviewer's independent exact implementation | PASS: projective incidence/completeness, factorization, −65 coefficient, all12 Jacobian substitutions, exact norms/distances, n2 equality, bad infinity, perturbed line, and generic nine-line node controls |
| Reviewer-controlled release negatives | All22 PASS: floating/duplicate/nonfinite/self-listed metadata, wrong provenance, unlisted/missing/symlink/FIFO/tampered payloads, wrong/missing external anchor, invalid work location, mismatched/symlink separate PDF, strict nested result types, false assertion, and a corrupted mathematical checker rejected before execution |
| Fresh frozen guard-harness replay | All140 hostile inventory runs, four unchanged baselines, four false-assertion runs, and four post-copy wrapper-corruption runs PASS, without timeouts |
| Metadata regeneration in a private copy | Byte-identical to the actual frozen descriptor; two declared files exist and match the intended note/archive |

The reviewer perturbation changes a different coefficient from the prior independent checker and gives18 points; it is not mislabeled as the prior20-point fixture. All authenticated package bytes remain unchanged and no pycache/pyc appeared in it. Diagnostic stderr hashes depend on temporary paths and are not mathematical output invariants. Finite checks supplement the written universal/analytic proofs; none proves priority, source intent or a universal assertion by sampling.

## PDF, metadata and global consistency

All four complete final PDF pages were rendered at105dpi and visually read. Text, mathematical glyphs, the theorem/proof transition, continuing homogeneity sentence, local invariant calculation, extension, limitations, disclosure and references are legible without clipping or overlap. The complete source agrees with the visible PDF and archived PDF identity. This reviewer did not recompile TeX or certify accessibility tagging; those are not represented as completed checks.

The note, README, actual generated Zenodo descriptor, live PR title/body, and current framing preserve the same unrestricted summed rough-M theorem and classical status. Author name, ORCID0009-0001-9320-500X, preprint type, version1.0, local publication date2026-10-14, CC BY4.0 author-material license, source DOIs and two file paths are consistent. The descriptor is locally regenerated exactly; no deposit was staged or published. The actual live title is “30001345: attributed multibranch rough-M counterexample; claimed_solved”; its corrected body is an exact read-only match to `PR_DESCRIPTION_CORRECTED.md`, and the live PR remains open/draft at the pinned original head.

Historical source-access records are not converted into fresh retrievals by hash checks. Original acceptance/audit files and older synthesis stages remain explicitly historical evidence. Their prior limitations and priority-pending stages are explained by the later framing/priority records, rather than silently rewritten. The recovery label stays “1 verified/5; earlier-attempt count unavailable”; no total one-attempt history, five completed author turns, extra proof-search turn or human peer review is certified. The final note and metadata explicitly disclose extensive AI assistance and unrefereed status. No raw third-party source body is redistributed.

## Disposition boundary and exact remaining gap

At the freeze timestamp, `PUBLICATION_FRAMING.md`, priority synthesis and freeze acceptance field explicitly recorded the proposed attributed route as pending disposition and new sequential whole-package reviews. During this review the parent reported a reasoned working assumption to proceed under existing authorization with the honestly attributed corollary, after substantial opportunity for an optional user preference; the parent expressly did not treat silence as approval. That administrative update did not alter these frozen bytes or the mathematical judgment. Historical pending statements are true as snapshot records; any later final administrative record must state the actual current disposition and completed review sequence consistently, rather than present this freeze as publication acceptance. This known workflow boundary is not a proof defect or a request for new mathematical novelty.

The strongest verified result is the complete explicit multibranch delta-constant counterexample7<12 with all claimed analytic/local conditions, and the universal classical Fermat excess n²−4 for n>=3. No technical mathematical gap remains for that assertion. The exact earlier publication/recognition of the rough-M comparison and an unstated2009 intention remain historically undetermined. The unibranched2014 conjecture remains outside the assertion because its central-fiber hypothesis fails. No inference of a new/currently open problem's resolution is supported. This review does not authorize acceptance, merge, staging, publication or a changed queue designation.

## Public artifacts and reproduction

`MANIFEST.json` lists the curated public files with exact byte lengths/hashes and excludes itself to avoid recursive hashing. Only the privately ignored `tmp/` tree contains source extracts/renders, API bodies, copied scripts, extracted packages and disposable fixtures. `verify_review.py --expected-manifest EXTERNAL_REVIEW_SHA256` checks this review map, all14 frozen artifacts, the original28 files and all105 archived payloads. Add `--extract` to recreate the authenticated private extraction if absent. With the trusted runtime and normal isolated Python, add `--replay` to rerun the exact checker plus the four-mode/22-negative suite, storing fresh receipts privately. All writes remain in this review directory; the source-body inspection is not falsely rerun by that command.

Suggested invocation from this directory:

    TRUSTED_PYTHON -I -B verify_review.py --expected-manifest EXTERNAL_REVIEW_SHA256 --replay

Trust is explicitly in the reviewed script/manifest supplied through an external record, runtime, dependencies, operating system and SHA256. This review is reproducible evidence, not a formal proof assistant, signature system or independent human referee report.
