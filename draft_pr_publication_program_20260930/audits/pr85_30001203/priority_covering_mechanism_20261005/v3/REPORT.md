# V3: authenticated Sussmann1974 quotient note and public-source followup

This is a narrow supplement to the preserved v1/v2 general-mechanism priority audit of PR85, target30001203/OWR-3394-020. It does not reopen proof search or authorize promotion/publication. The original submission head and mathematical gate remain unchanged. Central proof-search0; original budget1/5. V1/v2 artifacts and all source/input/gate files are preserved.

## Strongest verified new result

**All three pages of Sussmann's 1974 AMS note have now been read and visually checked. The note provides general quotient-regularity and fibre-map criteria, but it does not print any observation-Gramian, curvature, or complete target counterexample.** It explicitly defers proofs and its nonlinear-realization application to other works. This resolves the prior access gap for this particular announcement; it does not resolve access to the later proof and minimal-realization papers or clear overall priority.

The official source is *On quotients of manifolds: a generalization of the closed subgroup theorem*, Bulletin of the AMS80(3), May1974, printed pp.573–575, communicated10October1973. [Official AMS PDF](https://www.ams.org/journals/bull/1974-80-03/S0002-9904-1974-13502-0/S0002-9904-1974-13502-0.pdf). The supplied file has268476bytes and SHA256`9901afd6652d7859e8d4e4cc76933a8e8b63d7966387f022a82c911ae4eb315d`; both match the inspected local primary. PDF text extraction and all three rendered pages were checked.

## Definitions and exact announced theorems

The ambient `M` is a smooth (`C∞`), Hausdorff, paracompact manifold, and `R` is an equivalence relation. A *regular* relation gives `M/R` a manifold structure, permitted to be non-Hausdorff, with quotient projection `π_R` a submersion. *Local regularity* and *local closedness* mean the corresponding condition on `R∩(U×U)` for a neighborhood `U` of every point. A symmetry vector field preserves related pairs under its simultaneous flow wherever both flows exist. `S∞(R,M)` consists of such fields on open domains. Transitivity means their values span each tangent space. `R`-transitivity adds that the field's domain contains both members of each pair in `R`.

| Printed location | Exact logical statement and qualifications |
|---|---|
| p.574, Theorem1 | `R` is locally regular exactly when it is locally closed and `S∞(R,M)` is transitive. |
| p.574, Theorem2 | For connected `M`, `R` is regular exactly when it is locally closed and `S∞(R,M)` is `R`-transitive. |
| p.574, Theorem2′ | For arbitrary `M`, the same conditions characterize *almost regularity*: each quotient component has a smooth structure making its preimage's quotient projection a submersion. Quotient components may have different dimensions. |
| p.574, category qualification | The preceding local/regularity results also hold in the real analytic category using analytic symmetry fields. This qualification preserves the corresponding theorem premises; the paper's illustrative parenthetical is not treated as an independent theorem dropping local closedness. |
| p.574, Theorem3 | For connected smooth `M`, regularity is equivalent to local closedness plus transitivity of the *everywhere-defined* symmetry fields. A disconnected version uses almost regularity. |
| p.575, Theorem4 | For connected smooth `M`, regularity together with the quotient projection being a *fibre map* is equivalent to local closedness plus existence of a transitive family of complete, everywhere-defined symmetry fields. A disconnected version again uses almost regularity. |

The note additionally states that a regular quotient is Hausdorff exactly when `R` is closed. Theorems3/4 use smooth compact-support arguments; the author does not claim their analytic necessity directions, while reporting analytic sufficiency. Theorem4 is illustrated by closed-subgroup quotients and identifies proper-submersion/Ehresmann theory as another special case. “Fibre map” is retained in the author's terminology; it is not silently strengthened to a finite two-sheet cover or an injective projection.

## Exact target comparison

These are general theorems supporting the old quotient mechanism. Their conclusions concern quotient manifolds, submersions, and fibre maps; they do not imply global injectivity of an observation map. A nonsingular finite cover is compatible with the broad quotient setting, but the note does not select a hyperbolic surface, prescribe a two-point fibre, use Nash embedding, set observed dynamics to zero, or compute `P_T=Tπ*g`. It states no metric-realization, negative-curvature, completeness-of-Gramian, or uniform-Gramian-bound result. The complete target construction is absent from the entire three-page primary, not merely from an abstract.

The motivation on p.573 anticipates that, under suitable conditions, controllable nonlinear systems have controllable observable realizations. It does not spell out those systems assumptions here and expressly sets that application aside. This cannot be substituted for a theorem directly applicable to the smooth zero-dynamics target. This followup leaves v2's dimension-one vacuity precision and later-chapter A3 comparison intact.

## References and legitimate access followups

The 1974 bibliography has four items. Palais1957 and Serre1965 are foundational quotient/Lie sources. Item3 identifies the forthcoming full proof as *A generalization of the closed subgroup theorem to quotients of arbitrary manifolds*, later JDG10(1):151–166(1975), DOI10.4310/jdg/1214432680. Item4 is *Observable realizations of nonlinear systems*, then submitted. Its title is not identical to the eventual1976/77 *Existence and uniqueness of minimal realizations* title. Their bibliographic identity is not inferred without evidence. The already inspected Hermann–Krener1977 bibliography separately cites a forthcoming autonomous observable-realization paper and the minimal-realization work; these are distinct followup leads, not proof that every title is one paper.

The new DOI request redirects to the correct JDG volume10 **issue1** landing page. This corrects the issue2 route/metadata recorded in v1, while preserving v1 verbatim. The corrected publisher page still returned security-check HTML, including an observed iframe leading to an additional-security-check page; no challenge bypass was attempted. The author homepage's observed “papers available” link leads to an index expressly limited to papers since1989 and supplies neither1975 nor1976/77 primary. The author's vita confirms1975pp.151–166 and labels the minimal-realization work1977,10(3):263–284. [Author index](https://sites.math.rutgers.edu/~sussmann/currentpapers.html), [author vita](https://sites.math.rutgers.edu/~sussmann/vita-public.pdf).

The Springer minimal-realization page remains a subscription preview. Its primary abstract specifies real analytic state manifolds, complete analytic vector-field families, and arbitrary analytic outputs; its reference list cites both the1975 proof and1974 announcement. The publisher reports December1976, while the author's vita uses1977. Neither date difference changes priority relative to2026. No full theorem-level minimal-realization text was obtained, and its content is not cleared by its abstract. [Publisher page](https://link.springer.com/article/10.1007/BF01683278).

Five precise new followup searches and the observed link traversal are archived in `ACCESS_RESULTS.json`. The raw DOI response and access receipt are preserved, and failed HTML is not counted as a paper. No derivative citation or nearby PDF was treated as the missing primary. The parent independently handles the Krishnaprasad Allerton1977 source, so this family does not duplicate that adjudication.

## Remaining gap and bounded verdict

The AMS1974 announcement is now fully inspected and does not itself contain the complete exact target. The1975 proof,1976/77 minimal-realization paper, and identity/content of the submitted observable-realization reference remain unresolved primary-text gaps. Other v2 gaps, including the original ECC2009 complete contents and Crouch1981 fulltext, remain. This finding supplies an older, exact quotient theorem for attribution; it is neither an affirmative full-target priority collision nor a novelty clearance.

All new files are confined to this v3 folder. No individual was contacted and no outreach prepared. No Git/index/remote, PR, tracker, publication, editor, submitted-file, gate, or other shared-file write occurred. Bounded followup completion:100%; worldwide priority remains uncertified.
