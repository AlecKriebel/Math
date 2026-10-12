# Cold supplementary priority audit: Orban de Xivry 2013 thesis

## Decision

**Preserve bounded GO for the precisely framed, carefully credited complex quadratic proof note.** No exact accepted A–C prior statement was found in the complete relevant Chapters 2 and 4 read here. The thesis is a genuinely relevant complex coefficient projection source, not a matrix-only or real-only source. Its recovery removes the earlier body-access gap for this thesis. It does not clear unconditional novelty, firstness, or present-day openness, and it does not clear the separate 2013 Automatica article or other unread originals.

This is a source comparison, not a manuscript/package review or publication approval. It does not reprove the accepted mathematics. The comparison target remains the exact root-accepted result pinned by `ROOT_SCOPED_MATH_SOURCE_ACCEPTANCE.json`: for every fixed positive-definite real coefficient inner product, arbitrarily close to `z^2` in monic or full exact-degree complex quadratic coefficient space there is an unstable polynomial with two distinct attained global nearest closed-half-plane stable polynomials; the whole abscissa epigraph fails set prox-regularity. No finite-subgradient function-prox-regularity disproof is included.

## Independent reading and source version

Primary: François-Xavier Orban de Xivry, *Nearest Stable System*, UCLouvain PhD thesis, 2013. The [actual primary repository PDF](https://research.dial.uclouvain.be/bitstreams/930fe0d3-f488-439c-bce1-37a8dc368917/download) opens publicly and contains 214 pages, 1,902,385 bytes. Its SHA-256 is `c7cbf9c976969fc4f89205d47a22126d755bbd6b22da79941c59e6ee0bfe8db6`. PDF metadata identifies a PhD dissertation, author F.-X. Orban de Xivry, produced by pdfTeX, with creation/modification 14 June 2013. The recovery-supplied item identifier is `650a4c86-3c4c-439e-9a8f-54c4d42eab7f`; that record route did not render through the web tool, so this audit does not independently certify its access-label text. The actual official bitstream was accessible. Printed page 1 is PDF page 19.

Before reading any recovery-agent conclusion, I read:

- **Complete Chapter 2**, printed pp31–67, PDF pp49–85, including problem setting, perturbation bounds, singularities, necessary/sufficient local conditions, all benchmark cases, and chapter conclusion.
- **Complete Chapter 4**, printed pp135–181, PDF pp153–199, including complex polynomial algorithms, root parameterizations, numerical examples, reflection-coefficient comparison, weighted objectives and conclusion.
- Complete final conclusion, printed pp183–185; preliminary definitions printed pp2–3,9–14,24–29; actual Chapter 3 printed p74 and pp89–91; bounded theorem-statement windows on pp93–96 (Theorems 3.7–3.10), not all intervening proofs.
- Rendered visual checks of printed pp56,66,144,178, including the singularity drawing and exact complex example signs.

Tool outputs that truncated intermediate pages were reread in later bounded calls; those truncations are not counted as full reads. The relevant chapter body/text/captions were read, but this is not a visual audit of every graph or an independent validation of every theorem in the thesis. A focused full-extracted-body scan supplements actual reading. The recovery agent’s conclusions and the new six-page manuscript were **not read** for this comparison.

## Exact scope comparison

| Actual thesis material | What is already present | Exact gap from accepted A–C |
|---|---|---|
| pp2–3,33–37 | Real-valued inner products on complex data; arbitrary norm mentioned; minimization over the closure of the stable set; matrix or monic polynomial data in real or complex coefficient space | Merely formulating projection does not state local nonuniqueness for every fixed real coefficient metric. |
| pp41–43, Theorem 2.2 and Example 14 | Normal-matrix/eigenvalue perturbation bounds and spectral-space alignment for a nearest normal stable matrix | Unitary freedom preserves **eigenvalue distance**, not Frobenius distance from a fixed coefficient input. It is not two distinct global nearest coefficient systems. |
| pp55–57 | Real parameterized stability-boundary singularities, attributed to Mailybaev–Seyranian, Levantovskii and Arnold, with real cubic slices | Classical geometric/first-order background; no full complex quadratic coefficient curvature or metric-projection theorem here. Do not call the shape new. |
| pp58–62, Theorems 2.7–2.8 | Necessary normal-cone condition involving abscissa subgradients and horizon subgradients; sharp-minimum sufficiency for other affine-constrained problems | Necessary conditions alone do not prove nearest attainment or nonuniqueness. Horizon normals are known background, not an invention of this note. No uniform quadratic support failure or whole-epigraph set claim is stated. |
| pp62–67, Conjecture 2.10 and Example 22 | Nilpotent matrix benchmark; a real `n>2` local-optimality conjecture; competing complex `2x2` numerical solutions | Full matrices have extra degrees of freedom beyond the companion coefficient slice. The reported competing local solutions have unequal stated objectives, no global optimality proof, and are at a fixed input, not an arbitrary-neighborhood theorem. Example 22 also has an exact printed arithmetic inconsistency, detailed below. |
| p74, Theorem 3.2 | Unique analytic-center **Lyapunov certificate P** for a fixed strictly stable matrix | Uniqueness of the auxiliary certificate is not uniqueness of nearest stable coefficient projection. |
| pp89–91, Theorem 3.4/Corollary 3.5; statement windows pp93–96 | Barrier auxiliary global-value limit, stationary convergence, and a distance-to-optimal-value bound under a common-certificate hypothesis | No second nearest minimizer, no local failure of projection uniqueness. I do not independently certify all of these proof statements. In particular, a global-value convergence argument should not be silently strengthened into unique minimizer convergence. |
| pp135–137, Theorem 4.1 | A convex simplex description for real discrete-time monic polynomials with prescribed coefficient signs | A restricted real unit-disc family; unrelated to the complex quadratic cusp conclusion. |
| pp144–154, equations (4.13)–(4.16) | Explicit **complex monic coefficient** formulation via companion matrices; Euclidean coefficient distance; projections onto internal Dikin ellipsoids | This is direct prior complex coefficient algorithm work and should be acknowledged. Its convex-subproblem minimizer is not a globally nearest point of the whole closed stable set. |
| pp155–167 | Root parametrization `ri=-ci^2+i di`, valid for real or complex continuous-time polynomials, nonlinear least squares and root-to-coefficient differentiation | Root labels/signs can represent the same polynomial. Parameter multiplicity or algorithm starts do not supply two distinct coefficient minimizers. No accepted A–C theorem is stated. |
| pp167–174,181 | The thesis’s account of Moses–Liu uses real discrete-time reflection parameters and explicitly says its algorithm does not handle complex polynomials | This strengthens understanding of **the method as reported here**, not an independent clearance of the unread Moses–Liu original’s complete contents. |
| pp175–180, equation (4.71) | Complex weighted coefficient objective `||L*(a-x)||^2`, motivated by frequency/H2 weights; feasibility discussion of future algorithm modifications | Prior weighted projection formulation is real. It is not the accepted theorem for every arbitrary SPD real coefficient inner product, and it has no nonuniqueness or epigraph assertion. |

The exact polynomial problem (4.14) uses a fixed monic leading coefficient. The accepted full exact-degree extension, with leading coefficient also variable and controlled away from zero, is not stated in this chapter. The algorithm often stays strictly inside the stability region; the accepted target is closed-half-plane stability, including repeated boundary roots and attained global minima. These distinctions must be checked rather than conflated.

## Checkable near-match falsification

### Example 22’s displayed distance is inconsistent

Printed p66 displays `nu0=2/3+i/2`, `A=[[0,1],[nu0,0]]`, `J=[[0,1],[0,0]]`, and a candidate with diagonal `-0.2218` and off-diagonals `0.9467-i0.0355`, `0.0276-i0.0740`. The printed candidate distance is `0.8321`, versus `||A-J||=5/6`.

Treating the four-decimal displayed entries as exact rational values, direct Frobenius arithmetic instead gives

`||A-Xhat||_F^2 = 378168221/450000000`, so `||A-Xhat||_F = 0.9167190542605975 > 5/6`.

The displayed rational candidate is strictly stable: for roots `-tau +/- sqrt(q)`, with `tau=0.2218`, `q` the product of the off-diagonals, exact rational checks give `Re(q)<tau^2` and `(Im(q))^2<4*tau^2*(tau^2-Re(q))`.

Conjugating the **input** to `nu0=2/3-i/2` gives distance `0.8320900338571809`, reproducing `0.8321` after rounding. That is a plausible sign correction, **not an author-verified correction**. The printed display therefore does not substantiate its claimed closer alternative as written. Even a corrected experiment would only be local numerical full-matrix evidence with unequal distances, not the accepted global multiple-nearest coefficient theorem.

### Example 14’s unitary freedom is a different objective

For `A=diag(-1,1)`, take `X1=diag(-1,0)` and its unitary swap `X2=diag(0,-1)`. They have the same stable spectrum and the same minimum eigenvalue-matching squared distance `1` from `A`. Their actual coefficient/Frobenius squared distances are respectively `1` and `5`. Consequently, the unitary nonuniqueness mentioned in the spectral-distance argument is not a nearest-coefficient nonuniqueness example.

`exact_orban_checks.py` reproduces both checks using rational arithmetic and separately labels the numerical evaluations and the unverified intended correction. Its receipt certifies no global optimality, all-metric theorem or literature absence.

## Gate update and remaining limits

The earlier report’s **unrecovered Orban thesis** row is superseded: a primary reading copy now exists, and the complete relevant Chapters 2 and 4 have been inspected. That access gap should not remain on a current-facing missing-body list. It is appropriate to cite this thesis as prior work on complex monic coefficient projection and its algorithms, with this bounded no-match finding. It is not appropriate to call its entire 214-page body or all cited originals “cleared.”

No essential mathematical/source/attribution HOLD for a direct credited note emerged from this supplement. The all-metric global nonuniqueness and whole-epigraph obstruction still require the accepted proof, which is separate from this audit. Unconditional new-result/application-priority clearance remains unavailable, notably because the Moses–Liu/Combettes–Trussell originals, separate Orban article and other listed bodies remain incomplete. No present-day-openness claim follows from a thesis’s historical literature statements.

UTC checkpoints and percentage estimates are in `RESEARCH_LOG.md`. `SUPPLEMENT_VERDICT.json`, `SOURCE_PROVENANCE.json`, `FOCUSED_BODY_SCAN.json` and `EXACT_ORBAN_CHECKS.json` bind the version, extents and calculations. No manuscript, shared primary, provider, Git, DOI or Sheet write or external communication was performed. Completion: **100% of this bounded supplementary audit**; publication remains unapproved and wider historical priority remains incomplete.
