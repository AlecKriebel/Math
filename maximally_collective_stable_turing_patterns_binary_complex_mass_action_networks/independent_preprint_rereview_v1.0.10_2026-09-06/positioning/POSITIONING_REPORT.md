# Independent positioning and scope referee — v1.0.10

Reviewed commit: `953c836a12b9d9d474521feb4a96e218c1155203`.

**Recommendation in this review lane: accept the present exposition and literature positioning. No required correction was found.** The previous CSV finding N3 is closed. This conclusion concerns the fit between claims, theorem scope, and the checked literature; independent mathematical, computational, and PDF audits are separate.

## Prior finding N3: closed

Both `literature/theorem_comparison.csv:15` and `public/repository/literature/theorem_comparison.csv:15` now map the Conradi–Mincheva–Uecker row to:

| Field | Current value |
| --- | --- |
| Exact diffusion law | `no` |
| Nonlinear branch | `numerical continuation` |
| Stable branch | `numerically stable segments` |

The current main manuscript credits sufficient spatial-instability conditions and numerical continuation with stable segments (`manuscript/main.tex:1217–1223`). Section 4.3 of the primary paper shows a subcritical stationary branch that becomes stable after a fold. Thus the repaired table and manuscript credit are supported. The authors also investigate time-dependent states elsewhere; the main manuscript makes no claim that their work excludes such states. [Conradi, Mincheva, and Uecker, Sections 3–4](https://arxiv.org/html/2605.16049v1).

`CSV_COLUMN_WITNESS.json` records both parsed rows and their hashes, avoiding reliance on visual comma counting.

## Claim and quantifier check

| Potential overstatement | What the released text actually states | Assessment |
| --- | --- | --- |
| Stable patterns for every positive rate choice | Abstract and introduction quantify lower principal-block stability over positive-equilibrium realizations; stable patterns are supplied by particular exact designs. The main localization theorem is at lines 330–345, the conditional diffusion law at 515–541, and the chosen design begins at 621. | The quantifiers are separated correctly. No claim that every positive rate vector has a positive equilibrium is required. |
| Complete stability classification | Lines 515–522 explicitly leave the full homogeneously stable domain unclassified. Lines 576–577 require a separate spectral certificate to exclude wave instability. | The exact law is a stationary crossing and positive-real-eigenvalue law, not a full wave-instability criterion. |
| Intrinsic wavelength selection on arbitrarily large domains | Lines 105–107 define stationary Neumann bifurcation on a fixed interval and disclaim intrinsic finite-wavelength selection under domain enlargement. | Accurate for the actual fixed-interval bifurcation. |
| Strictly mass-conserving or globally bounded reaction system | Scope at lines 154–163 identifies one semipositive conservation law and excludes the term “mass conserving.” The vector has a zero component and does not bound X1. | The fixed-integrated-mass phase-space terminology is explained and does not imply a strictly positive conserved total. |
| Nonlinear stability inferred from linear instability | The normal form, positive small branch, complementary spectral gap, and local H1 stability are distinguished in the theorem and proof. Numerical illustrations are expressly not proof. | No exposition-level conflation remains. The proofs themselves are reviewed in the mathematical lanes. |
| Constant-optimal diffusion design or a complete Pareto frontier | The trade-off theorem states a topology-specific strict stationary lower bound and a square-root exponent match. It explicitly excludes constant optimality and a complete global frontier. The chosen family's product remains fixed under allocation. | Title, subtitle, abstract, theorem, and conclusion are consistent about exponent optimality. |
| Biological realization or dimension-uniform nonlinear control | Abstract, scope, and limitations identify a synthetic construction and local conclusions for each fixed dimension. | No biological validation, global-attraction, or dimension-uniform robustness claim is made. |

The bioRxiv plain-text abstract and SIADS cover letter preserve these substantive distinctions. In the abstract expressed using n=m+1, `23(91n−274)/63` and `8(n−3)` agree with the main manuscript's m-formulas. The user-confirmed funding, competing-interest, and submission declarations are not reopened by this review.

## Primary literature cross-check

The novelty position is a conjunction of restrictions and conclusions: an indexed binary-complex classical mass-action family in arbitrary dimension; localization for every positive-equilibrium realization; positive diagonal stationary diffusion design; and exact local stable nonlinear constructions. It is not a claim to have first found Turing instability, large unstable principal subsystems, nonlinear stable patterns, or diffusion design in general.

The following checks support the present distinctions:

- **Conradi–Mincheva–Uecker (2026):** sufficient conditions for networks admitting monomial steady-state parameterizations, with numerical stationary and time-dependent continuation in a finite example. Current credit for stable numerical branches is correct. [Primary preprint](https://arxiv.org/html/2605.16049v1).
- **Villar-Sepúlveda–Champneys–Krause (2025):** general reaction–cross-diffusion design at fixed linearized kinetics or fixed transport. The paper expressly works with generally non-diagonal diffusion and separates linear design from weakly nonlinear questions. The current main text accurately identifies that distinction; numerical PDE illustrations in that work do not supply the present realization-wide mass-action theorem. [Primary article](https://link.springer.com/article/10.1007/s00285-025-02274-1).
- **Waters–Yates–Dawes (2024/2025):** the 2025 work analyzes nonlinear amplitude equations and stable patterns in two-species minimal schemes, including degenerate quintic cases. Current text and table credit nonlinear and stable results and retain the molecularity and dimension distinctions. The published bibliographic year, volume 471, and article 134427 are correct. [Primary article](https://www.sciencedirect.com/science/article/pii/S0167278924003774).
- **Vassena–Stadler (2024):** the general unstable-core result uses parameter-rich kinetics; the primary article explicitly distinguishes classical mass-action restrictions. The manuscript does not identify unstable cores with its principal-block localization theorem. [Primary article](https://doi.org/10.1098/rspa.2023.0694).
- **Paul–Adetunji–Hong (2024):** the primary article considers 23 reaction networks, analytical exclusions, and a finite parameter screen with simulations. Its publication date is 27 September 2024, volume 15, article 8380; a search snippet that displayed a neighboring 2025 article was not a bibliographic correction. [Primary article](https://www.nature.com/articles/s41467-024-52591-0).

Several additional adjacent papers were considered without turning an optional bibliography expansion into a mandatory revision:

- **Woolley (2025), Bespoke Turing patterns with specific nonlinear properties:** explicit two-population kinetic design and weakly nonlinear pattern transitions. Section 2 fixes two populations. This is relevant broader design context, but does not reproduce the indexed all-realization binary-complex family or its heterogeneity exponent theorem. A citation could be useful in a later broader introduction; its omission does not contradict the present claim. [Author-hosted published paper, Section 2](https://orca.cardiff.ac.uk/id/eprint/177056/1/woolley-bespoke-turing-patterns-with-specific-nonlinear-properties.pdf).
- **Ahmad Shaberi et al. (2025), Optimal network sizes for most robust Turing patterns:** random-matrix statistics, two diffusing species, and additional immobile components. Its optimization concerns occurrence in sampled ensembles. This does not conflict with the present all-mobile topology-specific exact contrast bound. [Primary preprint](https://arxiv.org/abs/2410.11513).
- **Sostar–Džeroski (2026), Minimal Mass-conserving Reaction-diffusion Networks for Cell Polarity:** the accessible primary abstract reports enumeration of three-component four-reaction motifs and a computational atlas. That scope is distinct from maximal localization in every dimension. Only the primary abstract was accessible in this check; no claim of full-paper verification is made. [Primary preprint abstract](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7082764).
- **Brocchieri–Soresina (2 September 2026):** structural Turing conditions for cross-diffusion arising from fast-reaction limits in an SKT framework. Its transport mechanism is outside the positive diagonal setting here. [Primary article](https://link.springer.com/article/10.1007/s11587-026-01168-8).
- **Nandan–Nghe–Unterberger (2026):** diluted-regime autocatalytic cores and stationary regimes, with no theorem supplying the present stationary diffusion-law and nonlinear pattern combination. [Primary article](https://link.springer.com/article/10.1007/s00285-026-02357-7).

This is a bounded update search and primary-source comparison, not a proof that no unindexed or inaccessible competing result exists. No concrete novelty conflict or missing mandatory attribution emerged.

## Disclosure and preprint metadata

The manuscript explicitly reports AI assistance with discovery, symbolic derivation, code, testing, organization, and editing, disallows AI authorship, and contains the author's responsibility statement. This addresses the visible disclosure content required by the current SIAM policy; actual human accountability remains the author's responsibility, not something an automated referee can establish. No new author confirmation is requested. [SIAM AI policy, version 2.0, effective May 2026](https://epubs.siam.org/artificial-intelligence).

The citation file identifies version 1.0.10, uses the concept DOI as a concept identifier, and labels the 1.0.9 DOI as a preceding version. It does not invent a version 1.0.10 DOI. Root's separate DataCite check (`documents/DOI_METADATA.json`) confirms that preceding-version relationship and locates the newly registered exact version 1.0.10 DOI, `10.5281/zenodo.22559244`. Adding that now-available exact DOI is optional metadata maintenance; the existing precise release-tag citation is accurate. The fixed source snapshot and current submission metadata give the correct title and sole author. A preprint service's eventual moderation or category decision is not a mathematical defect or an unfulfilled referee repair.

## Conclusion

N3 is repaired. No new required exposition, novelty, citation, or scope change is supported by this review. Any optional broader-literature additions should be distinguished from the closed acceptance checklist.
