# Original PR263 source alignment: independent decision

Reviewed UTC: 2026-10-11. Frozen original head: `c4eff3253932a504f8e558c8b5f5b1b5e155de0f`. Problem: 30000170 / OWR-783-002. This review assesses source scope; independent mathematical families determine proof acceptance. No prior review verdict is used as a premise.

**Decision: SOURCE-QUALIFIED GO for the submitted complex coefficient nearest-stable projection result as a negative answer to the printed Question 1, and for the separately stated whole-epigraph set result. HOLD for any unqualified claim resolving real-only stability or standard function prox-regularity.** This is a conditional source-fit decision, not approval of mathematical correctness, novelty, priority, or present openness.

The submitted scope is not merely first-order evidence for its claimed projection target. If Theorems A and B pass mathematical review, they establish the negation of local uniqueness in the complex quadratic case. Theorem C separately negates whole-epigraph set prox-regularity. Neither should be inflated into the finite-subgradient function conjecture.

## Printed question and why the fit is source-qualified

I read and visually inspected the entire Lewis contribution, printed pp.104–106, in [OWR 2/2005](https://ems.press/content/serial-article-files/45976?nt=1), DOI 10.4171/owr/2005/02. The numbered question is on printed p.106 / PDF page38. A separately retrieved [author-posted three-page version](https://people.orie.cornell.edu/aslewis/publications/oberwolfach.pdf) corroborates the question and operative paragraph, with small wording differences from the printed report.

The report defines stable by maximum root real part at most zero. Its final question asks whether each degree-k polynomial sufficiently close to s^k has a unique nearest stable polynomial. The preceding paragraph describes local unique projection onto the abscissa epigraph and calls the question an essential ingredient. It does not state an equivalence. The opening application expressly uses real polynomials; the question itself omits field, normalization, and metric.

Thus complex coefficient scope is a supported interpretation, not an assumption explicitly printed in Question 1. Three independent primary passages support it:

- The actual report reference [Burke–Overton 2001](https://sites.math.washington.edu/~burke/papers/reprints/37-va-abs-poly.pdf), printed p.1651, defines complex polynomial space and its monic affine space. Printed p.1663 gives real coefficient inner products in translated monomial bases, including the ordinary basis at zero.
- [Burke–Lewis–Overton 2005](https://sites.math.washington.edu/~burke/papers/reprints/53-va-polys-GL.pdf), printed pp.263–264, defines complex polynomial space and restricts analysis to the open set of exact degree n. Printed p.266 supplies the real Euclidean coefficient pairing. Printed p.267, Lemma1, treats monics as a separate slice for tangent calculations.
- Lewis's related [Eigenvalues and nonsmooth optimization](https://people.orie.cornell.edu/aslewis/publications/focm-paper.pdf), p.9, defines the stable monic set in C^n. Its p.15 / Section1.7 adopts an epigraph-based geometric definition of prox-regularity. The [2007 survey](https://people.orie.cornell.edu/aslewis/publications/07-nonsmooth.pdf), printed p.172, explicitly states the complex monic theorem before again discussing nearest points in the whole epigraph.

These sources justify answering the literal complex projection version. They do not recover the author's unstated intention with certainty. A future title, abstract, status row, or manuscript must identify the complex coefficient convention and its inferential basis. A real-only interpretation remains an excluded question. Clarification of the intended field by an outside author could reduce that residual historical ambiguity, but this independent project forbids outreach; no contact or outreach draft has been made.

## Quantifiers and metric mapping

| Source component | Submitted theorem | Source-fit assessment |
|---|---|---|
| degree-k near s^k | arbitrarily close to z^2 in degree2 | Sufficient to negate a universal affirmative answer across degrees. It establishes the answer for k=2, not a classification for every k. If a different fixed k is prescribed, the submitted theorem does not claim to settle it. |
| closed-half-plane stability | roots have real part ≤0 | Exact match; imaginary-axis roots are admitted. Strict stability would be a different nonclosed approximation question. |
| field omitted in Question1 | complex coefficients treated as real coordinates | Supported by the directly cited complex theory and related Lewis expositions; retain the omission and field inference in the claim. |
| monicity omitted | monic and full exact-degree quadratics proved separately | Covers either coefficient-domain convention. The full theorem must continue to use actual ambient normals/localization, not mere inheritance from a monic slice. |
| nearest metric omitted | ordinary Euclidean coefficient metric and every fixed positive-definite real coefficient inner product | Covers the concrete Hilbert conventions of the cited theory, including fixed translated bases. Does not settle arbitrary norm or root-matching metrics. |
| nearest stable polynomial | existence of arbitrarily close inputs with two or more global nearest stable degree2 polynomials | The proposed use of the local projection characterization has the required conclusion. It is not an explicit formula for inputs or minimizing pairs. Mathematical reviewers must accept closedness and full-degree localization. |
| whole epigraph projection prose | direct set non-prox-regularity at (z^2,0) | Exact negative conclusion for that geometric property. Distinct from the finite-subgradient formulation below. |

The degree language is important. A degree2 counterexample answers “does this property hold generally for degree-k polynomials?” negatively. It is not proof that local projection fails at s^k for every k≥2. No such stronger all-degree theorem should appear in the acceptance wording.

## Why the function conjecture remains open within this submission

[Burke–Lewis–Overton 2005](https://sites.math.washington.edu/~burke/papers/reprints/53-va-polys-GL.pdf), printed p.291, conjectures function prox-regularity of root max-functions where the root function is twice differentiable and explicitly cites Rockafellar–Wets Definition13.27. Its reference14 on p.292 identifies *Variational Analysis* (1998). This is a distinct formulation; the source conjecture must not be silently replaced by the whole-epigraph statement.

[Poliquin–Rockafellar 2010](https://www.heldermann-verlag.de/jca/jca17/jca0849_b.pdf), printed pp.203–205, specifies localization near a finite subgradient v and the corresponding epigraph normal (v,-1). In the submitted proof, the unscaled gradients have scale 2/[t(t²+4)] and their imaginary constant-coordinate component diverges. The bounded epigraph normals have height component −t(t²+4)/2 and tend to a horizontal normal. Their failure therefore does not test prox-regularity relative to any fixed finite (v,-1). The exclusion in original PROOF.md is correct and necessary.

[Poliquin–Rockafellar–Thibault 2000](https://sites.math.washington.edu/~rtr/papers/rtr170-LocalDiffDistance.pdf), printed pp.5233–5234, Definition1.1, Proposition1.2, and Theorem1.3(a),(k), supplies the separate set theorem: in finite dimensions, local unique projection for a closed set is equivalent to set prox-regularity. This verifies the type of result the submission invokes; the independent mathematics audit must check its hypotheses for the stable set and the full exact-degree localization.

Consequently the strongest source-fitting acceptance wording is:

> In complex coefficient space, local uniqueness of nearest closed-half-plane stable quadratics fails arbitrarily close to z², both for monic and full exact-degree polynomials and every fixed coefficient Hilbert metric. The abscissa epigraph also fails set prox-regularity there. This negatively answers the complex coefficient version of Lewis's printed Question1; it does not settle the real-only variant or standard finite-subgradient function prox-regularity.

This is an original-writing summary of the submitted scope, not a source quotation.

## Consistency repairs if Root accepts the mathematics

The frozen original is evidence and should remain unchanged. A subsequent accepted package should repair the current-facing disposition globally:

1. `STATUS.md`, `RESULT.md`, and `TURN_STATE.json` still say independent source verdict/campaign classification pending. They conflict with original `QUEUE.md` and the later original `independent_review` verdict. Replace the current-facing pending status with the precise scoped acceptance, and retain a dated historical record of the earlier hold.
2. The opening and final scope discussion of `PROOF.md` retain requests for future source review. Preserve the proof argument, but make its administrative statement agree with the accepted scoped verdict and explicit exclusions.
3. Any queue/status field named `claimed_solved` must carry the complex projection/whole-epigraph set qualifier. It cannot stand for the imported unqualified function conjecture. If the campaign formally requires that conjecture as an additional target, the disposition is a mathematically accepted first-turn partial for that expanded campaign, with the remaining substantive budget handled separately.
4. Correct the related Lewis epigraph-definition locator from Section1.6 to Section1.7 (p.15) wherever that attribution is present in current-facing source/review notes. Section1.6 discusses partial smoothness; the epigraph function definition is in Section1.7.
5. Distinguish external-source uncertainty from proof uncertainty: the missing field in OWR is a disclosed inference, while the finite-subgradient claim is expressly outside the theorem. Neither should be described as though another computation settles it.

## Read extent, version, and access limits

Complete relevant extents were read, not only search snippets:

- OWR: complete Lewis contribution printed104–106 / PDF36–38, including references; all three pages visually inspected. SHA256 matches original `source_manifest.json`.
- Burke–Overton 2001: printed1651–1652 for field/domain/stability,1663 for pairing,1675 for finite versus horizon subgradients; p1651 visually inspected. No full-paper mathematical review claimed.
- Burke–Lewis–Overton 2005: printed263–267 for complex/exact-degree/metric/monic distinction and291–292 for concluding conjecture and its reference;266 and291 visually inspected. Published DOI10.1007/s10107-005-0616-1 version posted by Burke; hash matches original.
- PRT2000: printed5233–5235 for full set definition and complete Theorem1.3, including clause(k). No independent proof of PRT claimed.
- PR2010: complete printed203–205; p205 visually inspected. Publisher-posted PDF; hash matches original.
- Lewis related essay: p9 and complete pp14–15; author-posted file is hash-pinned, with no edition date inferred solely from its filename.
- Lewis2007: complete printed172 / PDF7. Only field and geometric-description evidence is used; its separate strict-stability terminology is not imported over OWR's explicit ≤0 definition.
- Author-posted Lewis three-page contribution: full text, with operative paragraph checked against the printed report. Printed OWR version controls when phrasing differs.

The complete imported record `../IMPORTED_PROBLEM_RECORD.json`, recovered read-only from the local SQLite cache by Root, was subsequently read in full. Its statement SHA256 is `ce2f9c7d034f93093611d0deb7b332a502123afa0909a12696b0864aecb27519`, matching the catalog. Both `statement` and `clean_statement` insert “Equivalently”; `original_statement` does not. The record's `statement_verification` concerns notation and preservation of supplied formulations, not a proof of equivalence. The complete printed source calls the projection question an essential ingredient and does not assert that equivalence. The corrected source claim must therefore discard the imported equivalence, while retaining the two distinct formulations and the standard-function exclusion. The record's dated 2026-08-21 triage and `open` field supply no present-openness or correctness certification.

All source PDFs, extracted full texts, and rendered pages are in ignored `private_reading/` and must remain private reading copies. Portable metadata and this paraphrased review are the publishable evidence. No broad novelty audit has been conducted. The unrecovered Cross thesis noted in original sources is not evidence of openness or firstness and is not needed to establish source alignment. No provider write, shared Git/worktree mutation, external communication, or outreach preparation was performed.
