# Intake and scope review — Zenodo 23393596

**Disposition: SCOPE COMPLETE; mathematical review and publication clearance pending.** This assignment authenticates sources, maps the exact model and primary interfaces, and prepares conditional editorial content. It does not issue a mathematical PASS or report a fresh mathematical-program execution.

## Identity and complete custody

Frozen queue row 69, work Z-23393595, identifies *Deep derived pure braids need not be 1-solvable*, Zenodo 23393596, version 1.0, publication date 15 October 2026. Fresh API metadata and both public assets match. The current manuscript explicitly prints “October 15, 2026 (version 1.0)”. Record creation is 2026-10-15T11:19:16.531335+00:00; it is recorded separately rather than treated as evidence of an earlier deposit or priority.

The four-page main PDF is 70,040 bytes, SHA256 `6547831e57c6eb01e7f4632ff67230f1e93d4ca6fec353e128b9c97a1f2c8b89`. The source/verification ZIP is 548,369 bytes, SHA256 `a123728e0e8e8c6160738d6703bb757fe285a04c29872d2441d168c33bb2f106`. Fresh metadata SHA256 is `d050764d8262d87e06c92a2cf3cadc90543828368d83e14460c91a341cf517a0`. The receipt binds original URLs, resolved URLs, retrieval times, byte lengths, Zenodo MD5 and SHA256. The all-assets set is exactly the frozen queue set.

Safe extraction covered all 213 regular members, with paths/types/CRC checked, hidden `.gitignore` members included, original archive permission bits preserved, and every member individually hash-bound. There are no nested archives. The single embedded `note.pdf` is byte-identical to the public main PDF, so there is only one distinct reader. Finalization rehashed all 2 public assets, 213 members and 7 fresh primary PDFs. These are custody checks, not mathematics.

## Complete manuscript and necessary-support reading

Read all 4 current PDF pages and all 273 TeX lines. Read the original 148-line explicit-witness `PROOF.md`, the 59-line strengthening `PROOF.md`, the 286-line original exact certificate checker,428-line planar Goeritz reconstruction and336-line Burau/Meyer reconstruction, plus runtime requirements. No published helper was imported or executed. The complete per-member map distinguishes these readings from 213 catalogued files; it does not silently claim to have read every historical document.

Dedicated historical audit, acceptance, priority, verdict and replay bodies stayed opaque. Filenames/hashes were inventoried. The current paper and two necessary proof bodies contain incidental historical status, priority and proof-response accounting language; mathematical program bodies contain expected values, comments and status labels. Those exposures are disclosed, and no previous reviewer conclusion, runtime result or priority search is adopted. No sibling report was read.

## Exact target, quantifiers and conventions

The group is the classical **disk pure braid group** P_m, regarded as ordered oriented smooth string links; the containment is about their represented string-link concordance classes. The derived series is the ordinary one G^(0)=G, G^(j+1)=[G^(j),G^(j)], with commutator xyx⁻¹y⁻¹. It is not a power subgroup, lower central series, rational derived series or surface braid group. Closure means the standard oriented braid/string-link closure in S³, not a topological closure of a subgroup; there is no group operation on unbased closed links.

The exact main statement is: for **every m≥3 and every finite integer k≥1**, there exists a braid in P_m^(k) whose standard closure is not **integrally smoothly 1-solvable**. The witness may depend on k. No one braid in the intersection of all derived terms is asserted. The consequence sets k=n+2 and uses F_n^m⊂F_1^m to conclude P_m^(n+2)⊄F_n^m for every m≥3 and integer n≥1. This neither asserts failure of the prior n=0 inclusion nor contradicts the degenerate m=1,2 cases: P₁ is trivial and P₂≅Z, so their positive derived terms are trivial.

Otto Definition 2.3 supplies a compact smooth four-manifold with boundary equal to zero-framed surgery, an integral H₁ isomorphism to Z^m, an integral H₂ basis of framed embedded oriented surfaces in hyperbolic pairs, and **both** surface families’ fundamental groups in the ordinary nth derived subgroup. The paper’s n=1 obstruction uses these exact conditions. A rational or merely topological substitute is outside the advertised scope. It does not claim a stronger0.5-solvability obstruction.

## Proof interfaces requiring the independent mathematical gates

1. The closure signature s on B₃ has bounded defect and a homogenization q with |q−s|≤6. Published formulas give q(a)=q(b)=q(h)=−2 for a=σ₁²,b=σ₂²,h=σ₂σ₁²σ₂⁻¹, while z=(σ₁σ₂)³=ahb has q(z)=−4. These are the ingredients for nonhomomorphism on P₃. The values require universal power/signature formulas, not sampled powers.
2. If a homogeneous quasimorphism vanishes on a finite derived termN, normality and homogeneity show it is constant on N cosets. It descends to the solvable quotient, where amenable rigidity makes it a homomorphism. The manuscript supplies this argument and credits stronger published solvable-quotient defect restriction. Neither amenable rigidity nor the general persistence principle should be advertised as new.
3. The local-coefficient obstruction is pointwise at −1. The all-meridian sign character extends over a 1-solution by the integral H₁ isomorphism. Signed cellular matrices reduce modulo 2 to ordinary ones, giving a twisted H₂ dimension bound. The framed surface classes are locally trivial and have nondegenerate hyperbolic pairings; their number saturates the bound. Ordinary and twisted signatures vanish. Toffoli’s compatible-framing surgery formula with zero linking matrix identifies the rho defect with minus the ordinary signature. The source domain includes −1 without an Alexander-root exclusion. The dimension/surface/radical argument remains a mathematical proof obligation, not an inference from a numerical signature.
4. Choose v with q(v)≠0 at the desired derived depth, then take a **positive power** whose ordinary signature is nonzero. Positive-derived membership gives zero pairwise linking numbers. Adding split vertical strands preserves group membership and adds split unknots, preserving signature. No homomorphism property of the raw signature on the whole concordance group is assumed.

## Explicit finite example and support limits

The source separately sets a=σ₁²,b=σ₂²,c=[a,b],d=a⁻¹ca,e=b⁻¹cb,u=[c,d],v=[d,e],β=[u,v]. The group expression placesβ in the third ordinary derived subgroup. The source states that its freely reduced Artin word has 104 letters, a 48×48 Goeritz matrix has inertia (23,25,0), correction 0 and determinant −7154819319988224, and a second Burau–Meyer computation gives signature −2. Those values are manuscript/certificate claims, **not fresh execution results in this scope assignment**. “104 crossings” describes the displayed word/diagram, not a proved minimal crossing number. No explicit formula at arbitrary depth or word-length bound is supplied by this finite example.

The original checker reconstructs the nested word, follows strand labels, derives the cyclic Goeritz matrix, performs exact rational symmetric elimination and Bareiss determinant computation, and compares a rational Meyer calculation. It uses explicit failure checks rather than removable Python assertions. The separate Goeritz body builds a planar rotation system, faces and checkerboard colours before matrix comparison. The separate Meyer body uses exact rational intersection-image/kernel spaces, including radicals, and compares signatures of equivalent forms. All three bodies were read without execution; their included finite controls and expected outputs are not fresh evidence here. The runtime file identifies the current closed replay as Python ≥3.10/POSIX with standard library only; optional historical recovery machinery uses SymPy 1.14.0.

Erle’s original printed 162–165 were freshly rendered and inspected, including the exterior closure, local crossing signs and exceptional-crossing correction. The off-diagonal index printed in Proposition 2.3 differs from the current-block signs in its accompanying matrix display, as the mathematical support itself flags. The page must not hide that qualification behind a literal invocation of the shorthand formula. Independent reviewers have the raw scan and the geometric reconstruction to examine. This scope review neither repairs the primary nor judges the final witness calculation.

## Actual primary-source inspection and attribution

All main imported interfaces were acquired as fresh full PDFs and inspected in their actual bodies at the stated passages. The ledger gives read extents and hashes; it does **not** claim full reading of every page of all 7 primary PDFs.

- The EMS-published 2017/50 report gives Harvey’s contribution, joint with Park and Ray, on printed 3020–3021. Question 3 literally asks the ordinary-derived containment. Its surrounding definition fixes G^(0)=G and iterated commutators. The report number/workshop year 2017 is distinct from the EMS publication date 19 December 2018. The publisher metadata HTML is separately retained and hash-bound.
- Otto’s published 2014 §2 / Definitions 2.1–2.3 fix the standard closure, smooth/integral model and decreasing filtration.
- Gambaudo–Ghys’s published 2005 Theorem A / Remarks 1–3, the n=3 application of Lemma 4.1 and printed 575 supply the link-signature/quasimorphism and homogeneous-value interfaces. The root-of-unity condition includes−1; there is no knot-only restriction. The finite witness’s Meyer form is described on printed 544.
- Calegari’s author-hosted *scl* at printed 27 and 33 supplies solvable amenability and Proposition 2.65 with proof. The exact fetched book is hash-bound; no byte identity to the publisher’s 2009 file is asserted.
- The published 2025 Kawasaki–Kimura–Maruyama–Matsushita–Mimura Lemma 7.12 and proof say D_G(f)=D_N(f|N) when G/N is solvable. The universal group mechanism is prior work, even though the paper gives its weaker consequence directly.
- Toffoli’s 2022 published article was read at (1.1), Notation 4.9, coloured-framing definitions, Theorem 4.24, Remark 4.25/(4.21), and the Corollary 4.28 interface. Compatible framing and the actual unit-torus domain were checked. The repository’s 37-page body uses online-first pages 1–37, distinguished from final bibliographic pages 404–440.
- Erle’s 1999 version-of-record §2 is relevant only to the separately displayed finite example. The scanned diagrams were inspected, not inferred solely from OCR.

Cha Theorem 8.2 occurs in the original proof as an optional alternative to the explicitly supplied local-coefficient rank argument; it is not imported in the current main proof and was not acquired here. This limit is recorded instead of claiming every historical citation was checked. No exhaustive novelty search or current-worldwide-open-status claim has been made. The original question and classical ingredients are credited without treating old opinions as proof of priority.

## Conditional editorial output

`ABSTRACT.tex` preserves the complete original source abstract. `ABSTRACT.txt` and `candidate.json` preserve every sentence after typography/whitespace-only normalization, checked exactly in `abstract-check.json`. The candidate provides a descriptive title/meta description, full abstract, accessible explanation, finite-depth quantifiers, closure/category boundaries, the explicit third-derived expression, prior-work links, all public assets, concise AI-use/unrefereed status and a professional general invitation for substantive collaboration. It does not reproduce audit counts or dated verification narratives. It is marked candidate-only and grants no mathematical or publication clearance.

Follow-up is null. A missing effective word bound or a smaller finite example is not, by itself, evidence of a substantial publishable direction. No minimality, current openness, firstness, formal proof or independent human peer-review claim appears in the candidate.

## Strongest established intake result and remaining gap

Completed: full queue-matched source custody, all-member safe extraction, one distinct reader, complete current-manuscript/necessary-proof reading, actual primary-body definition/interface mapping, and a full restrained source-bound candidate. Pending: independent analytic proof reconstruction, adversarial falsification, meaningful isolated finite replay and root disposition. The theorem is neither certified nor rejected by this scope-only report. Original published sources are unchanged. No site, Sheet, Git, release, redirect, Zenodo mutation or outreach action occurred.
