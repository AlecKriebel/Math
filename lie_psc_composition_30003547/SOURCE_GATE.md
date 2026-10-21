# Source gate for positive scalar curvature concordance composition

Checked 20 October 2026. Queue row 1831; catalogue ID 30003547; source key OWR-15579-004.

## Verdict

**The original problem is recovered. It concerns Lie manifolds, not the established closed-manifold concordance group.** Bohlen's 2024 survey still identifies the corresponding concordance questions as open. No later solution of this target was verified in the present search. The source poses a research program rather than a completely axiomatized conjecture: dimension, concordance conventions at infinity, and a precise algebraic universal property must not be silently invented.

This is source and status recovery only. No proof attempt, queue edit, or publication was performed.

## Original question and provenance

Karsten Bohlen, joint work with Elmar Schrohe, *Positive scalar curvature metrics on manifolds with controlled geometry at infinity*, printed pp. 2275–2278, especially the paragraph crossing pp. 2277–2278, in *Analysis, Geometry and Topology of Positive Scalar Curvature Metrics*, Oberwolfach Reports 14 (2017), no. 3, 2223–2298, DOI 10.4171/OWR/2017/36. The workshop was 6–12 August 2017; the report was published 5 July 2018. [Official record](https://ems.press/journals/owr/articles/15579); [official PDF](https://ems.press/content/serial-article-files/46701).

The requested construction is an appropriate operation on the concordance classes of compatible PSC metrics in the Lie-manifold category, using a chosen compatible PSC metric as reference. The motivating paragraph seeks a relation with spin bordism through secondary rho invariants and identifies a Lie-manifold extension of PSC surgery as a needed ingredient. It supplies neither an operation formula nor group or torsor axioms. No dimension threshold or fundamental-group condition is stated. Its analytic discussion uses a spin Dirac operator; the final question does not separately restate a spin hypothesis. The catalogue statement faithfully identifies this question, but its claim to be self-contained should not substitute for these missing conventions.

## Geometry and analytic hypotheses

The foundational paper is Bohlen–Schrohe, *Getzler rescaling via adiabatic deformation and a renormalized index formula*, J. Math. Pures Appl. 120 (2018), 220–252, DOI 10.1016/j.matpur.2017.07.016. The inspected [author manuscript, arXiv:1607.07039v3](https://arxiv.org/abs/1607.07039v3), §§1–2 and 7, makes the analytic setup explicit:

- A compact manifold with corners \(M\) compactifies the complete interior \(M_0\). The finitely generated projective Lie algebra \(\mathcal V\) of boundary-tangent vector fields gives a rank-\(n\) algebroid \(A\), with \(\Gamma(A)=\mathcal V\) and \(A|_{M_0}\cong TM_0\).
- Compatibility means a smooth positive-definite metric on \(A\), not an arbitrary complete metric on \(M_0\). A spin structure here is a lift of the oriented frame bundle of \(A\).
- The index results impose nondegeneracy/renormalizability and appropriate integrating-groupoid hypotheses. Theorem 1.2 uses strong amenability and polynomial growth. These are hypotheses of the analytic theorem, not a recovered list of necessary conditions for every possible composition construction.
- Section 7 constructs the secondary structure class in \(K_0(C_r^*(\mathring G_F))\). It does not establish the sought composition on metric classes.

The pair-groupoid restriction on the interior is not an assumption that \(\pi_1(M_0)\) is trivial. Likewise, the displayed graded-index setup is not a license to impose an unstated dimension restriction on the open question.

## Positivity and the two different boundaries

The OWR analytic discussion takes its scalar curvature minimum over the compact base \(M\), not just over compact subsets of \(M_0\). **Inference from this setup:** positivity of the smoothly extended scalar curvature on all of \(M\) gives a uniform positive lower bound on the complete interior. Positivity only at each point of \(M_0\), with infimum zero at infinity, is a weaker condition and cannot be substituted in the invertibility argument. The informal question itself does not separately formalize that distinction.

Zenobi's [*Adiabatic groupoid and secondary invariants in K-theory*, arXiv:1609.08015v2](https://arxiv.org/abs/1609.08015v2), Remark 3.22, explicitly uses uniformly positive scalar curvature for Dirac invertibility. Definition 3.23 defines groupoid spin-bordism objects with product metrics near the bordism boundary. These existing index/bordism constructions do not by themselves give the missing metric-class operation.

For scope control, separate:

1. **The temporal ends of a concordance**, where the usual convention is a PSC metric on a cylinder restricting to \(g_i+dt^2\) near each end.
2. **The boundary faces of the compactification**, which describe controlled geometry at infinity, not ordinary finite-distance boundary components of \(M_0\).

The OWR does not specify whether every representative must equal the reference metric near all compactification faces, whether boundary algebroid data are merely fixed, or precisely what product Lie structure is imposed on the cylinder. These are unresolved formulation choices in this recovery, not established source hypotheses. A cylindrical-end subclass with fixed end metric must be labeled a restriction. A universal finite-distance product-collar requirement at infinity must not be added.

## Concordance is not isotopy or cylinder concatenation

The customary PSC concordance relation is geometric, through a PSC cylinder; isotopy is a path of PSC metrics. They must not be equated without a theorem in the stated category. A path is not automatically a PSC cylinder with its unmodified product-in-time metric, and noncompact uniform control requires attention.

Gluing two existing, collar-compatible PSC concordance cylinders at a shared endpoint composes the cylinders. That does **not** define an operation on two arbitrary concordance classes of metrics relative to a reference metric: it presupposes matching intermediate metrics and existing concordances. In particular, it cannot manufacture a concordance from an arbitrary class to the reference class. No groupoid inverse assertion is needed for this distinction.

**Interpretation, not an additional theorem:** the reference metric and surgery requirement make the natural intended target a surgery-mediated algebraic construction on endpoint-metric concordance classes. Its well-definedness would have to include independence of auxiliary surgeries and representative choices while preserving the specified Lie geometry and PSC control. An arbitrary set-theoretic operation, gluing already-known concordances, or a disjoint-union law on varying manifolds is not a resolution. The source does not specify a unique group, torsor, identity/inverse law, or compatibility equation for rho invariants.

## The closed-spin result cited by the catalogue

Xie–Yu–Zeidler, [*On the range of the relative higher index and the higher rho-invariant for positive scalar curvature*, arXiv:1712.03722v3](https://arxiv.org/abs/1712.03722v3), published in Advances in Mathematics 390 (2021), 107897, DOI 10.1016/j.aim.2021.107897, is a different theorem.

For a **closed spin manifold of dimension \(n\ge5\)** admitting PSC and \(\Gamma=\pi_1(M)\), the paper recalls Stolz's free transitive action of \(R^{\mathrm{spin}}_{n+1}(B\Gamma)\) on PSC concordance classes. Choosing a reference metric identifies this torsor with an abelian group. Proposition 4.1 proves agreement with the Weinberger–Yu group law using the same reference metric; no simply connected or torsion-free hypothesis is required for that comparison.

The latter construction uses an interior connected sum of two cylinders, further surgeries eliminating the kernel of \(\Gamma*\Gamma\to\Gamma\), and a PSC extension from three prescribed boundary metrics to a fourth. The extension is product near the boundary. This is not ordinary connected sum of endpoint manifolds, nor bare concatenation of concordances. Applying it to controlled noncompact interiors requires new arguments rather than deleting the word “closed.”

## Later status evidence and search boundary

- **Direct unresolved-status evidence:** Bohlen, [*Index theory of pseudodifferential operators on Lie structures*](https://imar.ro/journals/Mathematical_Reports/Pdfs/2024/3_4/5.pdf), Mathematical Reports 26(76) (2024), no. 3–4, 255–287, DOI 10.59277/mrar.2024.26.76.3.4.255. Section 6, p. 284, lists the concordance-class questions among open problems; reference [8] is the exact OWR contribution. The article was received 28 June 2023. The published 2024 statement is stronger evidence than a generic negative search, but does not prove absence of later progress.
- **Related, not a solution:** Bohlen–Lescure, [*A geometric approach to K-homology for Lie manifolds*](https://smf.emath.fr/publications/une-approche-geometrique-de-la-k-homologie-des-varietes-de-lie), Ann. Sci. ENS 56 (2023), 1747–1776, DOI 10.24033/asens.2566, concerns geometric cycles and Fredholm index reduction. This pass inspected publication metadata and abstract, not its complete proof.
- **Newer primary manuscript screened:** Bohlen, [*A Volterra Calculus for Lie Groupoids*, arXiv:2511.00991v2](https://arxiv.org/abs/2511.00991v2), revised 21 September 2026, develops parabolic/heat-kernel calculus. Abstract, introduction and a full-text term search disclosed no concordance-composition or PSC-surgery theorem. This is a scope screen, not a proof audit.

**Status wording justified by this pass:** original target recovered; explicitly unresolved in the author's 2024 survey; no complete Lie-manifold composition construction verified as of this check. A fully quantified research claim must first declare its admissible Lie structures, positivity at infinity, temporal/side-boundary conventions, equivalence relation and algebraic target. Do not record the already-known closed-spin theorem as a solution of this row.
