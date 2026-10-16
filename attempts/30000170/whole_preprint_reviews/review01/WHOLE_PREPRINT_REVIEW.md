# Fresh adversarial review of the entire PR263 preprint package

Review 01; 11 October 2026. This is an independent AI adversarial review, not human peer review or proof-assistant certification. No result or publication approval was prescribed. No package/candidate/shared-map edit, Git/provider action, publication, external communication, or outreach was made.

## Verdict

**No mathematical defect found** in any assertion of Theorem 1, Remark 2, or Proposition 3 of the frozen six-page manuscript. I independently derived the normals, metric obstruction, global localization and finite-subgradient support argument, and attempted to falsify their signs, assumptions and quantifiers. The strongest checked result is the exact theorem as written: every fixed SPD real metric, complex monic and full exact-degree coefficient spaces, attained global ties arbitrarily near the bases, whole-epigraph set failure, and the positive Euclidean finite-subgradient function statement.

**One minor standalone-package defect remains:** three stale docstring locators in two verifier files name absent proof files or an absent run command. Correct the locators consistently and produce a newly pinned archive/manifest. The frozen v02 is preserved; this report does not certify any later corrected bytes. A new independent reviewer should review the corrected entire package, as the parent has directed. There is no mathematical repair requested.

Historical alignment and bounded credit survive this review. I found no essential citation/attribution defect and no overclaim of firstness or present-day openness. The explicitly retained unread original bodies still prevent exhaustive historical-priority certification; they do not serve as proof premises.

## Exact version and reproducibility

The package root is `preprint_package_v02` under the parent effort. Exact pins:

| Artifact | SHA256 |
|---|---|
| PACKAGE_MANIFEST.json | `f7c88aaaf5f2e0b9358d141c70582aafe046989392bb23edb1537436bbd239fa` |
| Standalone manuscript source | `caf327484a7068244ab98494eab835f50b84521a6d7ba364007bda31f7478677` |
| Six-page PDF | `6439bda84f32d9a5ac1680e184975df159f51f8c7e44e609fa873dfa8ae78e1f` |
| Twelve-member verification ZIP | `901968e08148f586ba40b96850c230d76e736d9705959ce674dcc09f23f31480` |
| Current candidate CANDIDATE_MANIFEST.json | `c2ea92f1638dfafbd2d17e3600c0ef1951f866cf4eaeaa4f71fd6c0ea4d713b3` |
| Original PR head | `c4eff3253932a504f8e558c8b5f5b1b5e155de0f` |

`check_frozen_package.py` independently checked all 21 selected package bodies against the outer manifest, extracted all 12 ZIP bodies into my own directory, compared every body to the supplied `verification/` copy, and checked exact internal manifest coverage. The ZIP has one directory prefix; no symlink, traversal, duplicate member or undeclared payload was found. The internal hashes cover 11 files and exclude only HASHES.json. Six outer/source/archive duplicate pairs are byte-identical, and deposit metadata exactly equals the metadata file. Both deposit paths agree with the outer published-file list.

From the independent extraction, Python 3.14.6 executed all three standard-library scripts successfully with empty stderr:

| Script | Result |
|---|---|
| verify_exact.py | PASS; 2,005 rational assertions; stdout 1,166 bytes, byte-exact expected output; SHA256 `ea53bd56bd5d17a1a59426337a84b4cdb9db5dc16be545b9ac75be5d4c2339cf` |
| verify_function_boundary.py | PASS; 45 scalar boundary, 1,200 coefficient-support, six adverse-curvature, eight horizontal controls; stdout 5,302 bytes, byte-exact expected output; SHA256 `ccb99ec489ce71926abdcaa973935ab16949898fb4767af6fd060a225fb26509` |
| check_archive_hashes.py | PASS; 11 files; stdout SHA256 `0638d88eb5bc77727a8fa4c2107d2172b0bf35e2c078a74899d58e58e9f8b866` |

The 90-digit Decimal controls are deterministic sampled checks, not interval-certified computations. The exact script verifies identities at finitely many rational path points; neither computes a nonunique projection input and its minimizers. I inspected those scopes in the actual code rather than upgrading PASS into proof certification.

Fresh independent controls add 1,761 rational assertions: arbitrary stable-root chart identities including edges; an exact counterexample to dropping the nonnegative right-side restriction before squaring; the classical quartic/umbrella coordinate identity; 16 coupled SPD metric stress cases in dimensions 4, 5, 6 and 7, with conditioning exponents up to 80; and exact adverse-curvature zero-discriminant cases. Those also pass and are explicitly finite. They supplement the analytic checks in `COLD_ANALYTIC_CHECKS.md`, which carry the universal and limiting conclusions.

All six PDF pages were rendered and visually read, and the complete PDF text was extracted and compared with the source. Equations, signs, theorem numbering, proof conclusion, references and disclosures agree. There was no clipped or missing argument or rendering defect. Source in the archive is exactly the reviewed standalone source. No build-generated auxiliary source is needed for a reader to inspect the argument.

## Adversarial mathematical findings

| Assertion | Independent mechanism and attacks | Finding |
|---|---|---|
| Monic limiting normal | Factor roots as `-it,-t²+it`; independently compute all four real derivatives. Active root is simple with strict real-part gap at each fixed t. Outward sign is positive in Im b. Taylor support plus a sufficiently small actual metric step excludes both local and remote competitors. | The sequence consists of actual proximal normals; no unsupported uniform root gap or uniform Taylor bound is used. |
| Every fixed coefficient metric | Covectors represent normals as `G^-1 n_t`; exact distance difference is `t⁴(e^TGe+2t e^TGf+t² f^TGf)-2 tau t³`. | Negative for sufficiently small t for each fixed SPD G and fixed tau>0, including coupled metrics. No uniform threshold over all metrics is claimed. |
| Multiple attained global monic nearest points | Continuous discriminant formula makes S closed; coercive fixed SPD distance makes every infimum attained. Apply the finite-dimensional closed-set projection equivalence contrapositively on an arbitrary neighborhood. | Empty projections are independently excluded, so the non-singleton values contain at least two global minimizers. Stable inputs have their sole zero-distance projection at themselves; the resulting inputs are unstable. |
| Full exact degree | Compute the two leading-coordinate gradient entries independently: after scaling, `(t³/2,-t²)`. Limit is nonproximal in all six ambient directions. | A monic-slice obstruction is not silently imported into the larger ambient set. |
| Full global competitors/degree loss | A fixed metric ball around `(1,0,0)` can be chosen with leading coefficient bounded away from zero. Stable intersection is compact. For an input within R/3, every boundary/outside point is farther than 2R/3, while the stable base is closer than R/3. | Global minimizers of the clipped and exact-degree sets agree and exist. Degree-zero leading limits cannot compete for these inputs. Global closedness of the full set is not assumed. |
| Whole epigraph, mixed metric | Smooth outward covector is `(gamma_t n_t,-1)`, scaled positively to `(n_t,-1/gamma_t)`. Its horizontal limit pairs to t³ with the zero-height path; H-norm squared is order four. | Correct in every fixed joint SPD metric. A mixed metric may tilt the representing vector; the manuscript distinguishes it from the horizontal covector. Full-degree epigraph closedness is only local. |
| Closed boundary chart | Imaginary root translation gives `(x,U,V)` with `U=u+y²/4,V=v-xy/2`; reverse the unsquared inequality only after enforcing its nonnegative right side. Check x=0 and U=0 separately. | Exactly `x>=0,U>=0,V²<=x²U`. Dropping U>=0 at x=0 would falsely admit w²-1, which the manuscript does not do. |
| Real coefficient control | Real monic stability is the closed convex orthant. An SPD squared distance is strictly convex. | Unique projection for real quadratics; no real-only general negative claim is supported or made. |
| Proposition 3, subdifferentials | Off-ray scalar Phi gradients have norm `1/(2sqrt|D|)`; negative-ray intervals and the zero half-plane have actual local supports. Bounded off-ray gradient limits at zero are impossible. A smooth invertible `(a,b)->(a,D)` coordinate map transports all three subdifferentials both ways. | Correct under the proximal-limit subgradient convention as well as the regular-limit convention. The constant-coefficient component `v_b=-2q` prevents hidden cancellation of diverging q. |
| Proposition 3, uniform support and strictness | A fixed v0-neighborhood bounds q by M. With `|D|<1/(16M²)`, relevant bases lie on L. Convex-ray support controls every comparison point; the exact discriminant remainder is `(Delta a)²`. | Support curvature M works; increasing to M+1 yields strict slack at least `||Delta||²/2` for every distinct comparison, as the cited definition demands. No comparison-subgradient restriction is inserted. |
| Function/set distinction | Moving coefficient gradients diverge as 1/(2t), while the set witness scales to a horizontal epigraph covector. | It does not test a neighborhood of any fixed finite `(v0,-1)`. The negative whole-set and positive finite-subgradient claims are compatible. |

For a checkable adverse-curvature example, take `q=M>0`, base `a=D=0`, comparison `a=i tau,D=0,b=-tau²/4`. The linear-support deficit is `-M tau²/2`, while squared coefficient displacement is `tau²+tau⁴/16`. This independently confirms the required sign and why curvature may depend on the fixed finite subgradient. The manuscript uses the correct sign and quantifiers.

The PRT invocation was checked in its actual primary Definition 1.1, Proposition 1.2 and Theorem 1.3(a),(k), and the relevant Proposition 3.5 proof. Its hypotheses are a closed set and the finite-dimensional weak-closedness condition; the manuscript meets them with S or compact C. Local uniqueness there concerns the actual global nearest-point mapping. The PR2010 primary definition is strict, localizes the finite limiting proximal subgradient and the base value, and its p205 epigraph correspondence specifies `(v0,-1)`. The manuscript's stronger support inequality satisfies those requirements; its direct smooth-coordinate proof does not rely on an unqualified nonlinear parameter-metric transfer.

## Primary source and historical alignment

I completed the mathematical cold analysis before opening external previous reviewer reports. The package's authored priority memorandum was read for source locators and scope; its reviewer claims were not used as certification. My actual body extents are bounded and are pinned in `PRIMARY_SOURCE_PINS.json`:

- Lewis2003: complete Section 8 pp166–168, including the complex Euclidean monic definition and stable-set question. OWR2005: complete Lewis contribution pp104–106. The latter printed question omits coefficient field, normalization and metric and does not print the imported “Equivalently.” The manuscript explicitly qualifies its complex reading. OWR's surrounding real Belgian-chocolate example does not supply an unambiguous real-only field statement for Question 1. BLO2005's complex exact-degree domain and its concluding finite-function conjecture were separately checked; the latter is not refuted here.
- PRT2000 and PR2010: the essential definitions, theorem statements, epigraph correspondence and relevant projection/composition proof passages described above. BO2001: actual complex monic introduction and first-order normal/subgradient framework. These are credited classical tools, not asserted novel results.
- Bottema1956: all four printed body pages, with the real quartic boundary equation; KO2013: actual opening geometry pp1–2, relevant equations and bibliography. The standard local conversion `x=(a1+a3)/2,V=(a1-a3)/2,U=(a2-2)/(a2+2)` turns the normalized quartic boundary into `V²=x²U` near a2=2. It is a geometric identification, not a preservation of a fixed coefficient projection metric. The manuscript gives proper limited classical credit.
- Cross2010: actual title/author/year; Definition 5.22, complete Example 5.38 pp120–123 and the real quadratic discussion pp131–133. I did not independently reread all of Chapter 5. Its two-parameter coefficient map has zero derivative at the origin. The printed abscissa at (c,0) is c, not zero, but the corrected support comparison remains larger than c; thus the negative parameter-function conclusion persists. Parameter projection multiplicity there can represent the same polynomial and does not furnish distinct ambient coefficient minimizers.
- Moses–Liu1991: actual recovered author-linked OCR problem statement and Section III, with complete-body keyword inspection. Its real monic disk coefficient objective is weighted Euclidean and it recognizes possible nonuniqueness. I do not independently certify the original Figure 1 or typeset body, which remain unrecovered. The manuscript attributes only the supported recognition and earlier approximation framework.
- Orban2013: complete polynomial Chapter 4 pp135–181, including its complex monic coefficient formulation p144, root algorithms and weighted coefficient objective pp175–180; actual relevant Chapter 2 pp55–67, plus title page. I did not claim to reread all 214 pages or all Chapter 2. No exact all-fixed-real-SPD arbitrary-neighborhood quadratic tie theorem or whole-epigraph assertion was found in these actual extents. The source is correctly credited as prior complex polynomial work and is not dismissed as matrix-only or real-only.

I independently recalculated the disclosed Orban Example 22 issue before consulting the prior supplement. For its printed input and four-decimal candidate, squared Frobenius distance is exactly `378168221/450000000`, giving 0.916719... rather than printed 0.8321 and exceeding the Jordan candidate distance 5/6. A conjugated input reproduces 0.832090..., but intended author correction is unknown. Its candidate is strictly stable by exact rational checks. This is a caveat in a cited source, not a defect in this theorem or an imported proof premise; the package treats it correctly. The corresponding calculation is saved in `ORBAN_EXAMPLE22_INDEPENDENT_CHECK.json`.

Bibliographic title, author, year, printed page/volume information and the essential claim locators agree with the actual inspected bodies for all eleven manuscript references. Some DOI/repository URLs did not render through the web tool, but primary reading copies and their bibliographic records were available; that tool limitation is not a verified broken citation. Source provenance is explicitly an aggregation of 44 timestamped snapshot records, not 44 distinct fully read bodies. Earlier UNKNOWN rows for subsequently recovered works are superseded by the later records and top-level current-gap fields.

The remaining original bodies are explicitly retained: Combettes–Trussell1992, the separate Orban–Nesterov–Van Dooren2013 journal article, full Cross2009 talk and other original geometry readings. Recovery of a thesis does not clear the separate journal article. Neither partial reading nor historical open-question language establishes absence, firstness or current openness. No newly discovered essential literature/source HOLD arose; this bounded finding is not a priority certificate.

## Current-facing source consistency

The current candidate's 23 payload bodies and all external decision/report pins match its exact manifest. I read its PROOF, RESULT, STATUS, SOURCE_SCOPE, CURRENT_REVIEW_PROVENANCE, TURN_STATE and repair summary and checked the actual claims against the manuscript. They preserve complex field qualification, all fixed SPD metrics, full-degree localization, horizontal covector distinction, positive auxiliary-function result, prior-source credit, and publication-pending status. Nine preserved original request/review/control paths are explicitly historical; their old conclusions are not represented as certification of the current standalone manuscript or its auxiliary proposition. The core derivations agree. `CANDIDATE_CONSISTENCY_CHECK.json` binds this finding to the exact candidate bytes.

The current candidate does not itself include the Proposition 3 proof; it calls that an independently accepted auxiliary result awaiting final incorporation/review. The standalone manuscript includes the proof, and this review has now independently checked it. Those different artifact roles are stated, so this is not a hidden missing proof in the publication package.

## Defect requiring the next package revision

**D1 — stale standalone verifier docstring locators, low severity, no mathematical effect.**

1. `verification/verify_exact.py:5` says the analytic proof is in `PROOF.md`; the archive has no such file. The correct deliverable is `nonunique_nearest_stable_complex_quadratics.tex` and the separate PDF.
2. `verification/verify_function_boundary.py:2` names `AUDIT_REPORT.md`; the archive has no such file.
3. `verification/verify_function_boundary.py:5` says `Run: python3 check_controls.py`; the actual standalone script is `verify_function_boundary.py`.

The same bytes occur inside the ZIP. The README and repaired stdout point to the right manuscript and commands, so reproduction through the README succeeds. Nevertheless, these are concrete contradictory standalone-package instructions. Repair both source copies, the ZIP bodies and hashes/manifest consistently; inspect related repository provenance copies to distinguish genuine historical-only context from current-facing instructions. Verifier arithmetic and expected output need not change if only docstrings change. Rerun both verifiers and hash checker after the repair and deliver a new exact manifest for fresh whole-package review.

One nonblocking provenance observation: root `BUILD_STDOUT.txt:4–5` names the v01 build path and is outside the 21-file selected manifest and published ZIP. This is compatible with v02 reusing an unchanged manuscript/PDF after an auxiliary output repair; it is not evidence of a v02 PDF recompilation. Label it as reused historical build evidence, remove it from a reader-facing package, or regenerate it for the next version if desired. No source/PDF mismatch was found.

## Remaining boundaries and completion

This audit is complete for the frozen version and the stated bounded source comparison. The work still does not provide explicit unstable input/minimizer pairs, all-degree or real-only classifications, general nonlinear parameter/matrix metric transfer, one uniform curvature constant for all finite subgradients, exhaustive historical priority, human peer review, or formal certification. None is claimed by the manuscript.

The exact publication package is not clean until D1 is fixed and the revised bytes are freshly reviewed. The verified mathematics survives; no claim weakening is requested. Parent owns the repair and next-review decision. Timestamped checkpoints with progress percentages are in `RESEARCH_LOG.md`.
