# Fresh narrow priority audit

Audit date: 2026-08-15.

## Verdict

**Proceed, with conservative novelty framing.** The theorem suite is coherent and materially sharper than a collection of technical lemmas, but several components sit close to established neural-code machinery. The paper must not claim first priority for the maximal-intersection core, morphism algebra, or the open-convex monotonicity theorem. The strongest apparently distinct contributions are the finite polytopal monotonicity construction, the three universal reductions (especially the binary-meet normal form), the rational bridge theorem, the fixed-arrangement one-neuron theorem, and the protected-supercode/finite-atlas package.

The higher-dimensional open-convex versus polytope-convex conjecture remains explicitly open in the December 2025 covering-relations paper. No indexed source located through 2026-08-15 announced a universal proof or a curved-only code.

## Theorem-by-theorem comparison

| Theorem in this paper | Closest prior result | Exact difference | Novelty confidence | Citation / source | Action |
|---|---|---|---|---|---|
| Bounded realization | Standard witness truncation; used implicitly throughout convex-code literature | Same-dimension bounded normalization stated explicitly | Low | Cruz et al.; general convexity folklore | Treat as normalization only |
| Polytope monotonicity | Cruz et al. prove open-convex monotonicity | Explicit finite polytopal cap construction preserving every atom and threshold equality | Moderate-high | Cruz et al., *On Open and Closed Convex Codes* | Headline theorem; request expert proof audit |
| Max-intersection core | Cruz et al. Prop. 4.3 constructs the core by hyperplanes and proves max-intersection-complete convexity | Bounded polytopal formulation and combination with polytope monotonicity | Low for core; moderate for combination | Cruz et al. | Attribute directly; do not claim core novelty |
| Cover/deletion reductions | Jeffs develops the code-minor poset; Jeffs-Trang classify covering relations | Universally quantified equivalence schemes linking the conjecture to immediate covers and single nonmaximal deletion | Moderate | Jeffs; Jeffs-Trang | Present as reductions, not classification |
| Binary-meet deletion reduction | Intersections of maximal words are standard; no exact deletion normal form located | Inclusion-minimal maximal-family argument and nondecreasing-cardinality schedule ensure two strict surviving superwords | Moderate-high | no exact match found in narrow search | Headline theorem; cautious “we prove” wording |
| Rational interval bridge | Order-forcing and line-segment traces occur in neural-code literature | Every binary-meet deletion yields a covered strict-trunk interval code whose complete endpoint preorder is rationalizable, including simultaneous events | Moderate-high | Jeffs, order-forcing; Bukh-Jeffs for planar interval techniques | Headline theorem; invite scrutiny of endpoint extension/rationalization |
| Fixed-arrangement one-neuron polyhedralization | Finite arrangements and separation are classical; planar polygonalization handles all neurons in dimension two | Any-dimensional exact replacement of one convex selector over a fixed finite polytopal arrangement | High | no exact neural-code theorem located | Headline theorem |
| Intersection-morphism theorem | Jeffs' morphism formalism and trunk-preimage description | Explicit finite-intersection commutation and no-retraction corollary | Low-moderate; likely implicit | Jeffs, *Morphisms of Neural Codes* | Appendix only; no novelty claim |
| Protected supercode | Witness-preserving inner approximation is a natural idea, but usually insufficient for exact code preservation | Proves one-sided finite error `C ⊆ D ⊆ Δ(C)`, exact protected witnesses, same maxima | Moderate | no exact statement located | Main theorem; emphasize one-sidedness |
| Whole-word repair atlas | Compactness/subcovers are classical | Finite source-contained complete-word patches cover every unwanted closed carrier; eliminates local analytic infinity without claiming globalization | Moderate | no exact statement located | Main theorem; state limitation immediately |
| Sequential repair calibration | No close published calibration located | Exact rational demonstration that later hull enlargement recreates a forbidden word, synchronized repair succeeds | Moderate as example | none located | Keep concise; verifier-backed |

## Sources audited

- Curto et al., *What Makes a Neural Code Convex?*
- Cruz, Giusti, Itskov, Kronholm, *On Open and Closed Convex Codes*
- Jeffs, *Morphisms of Neural Codes*, and erratum
- Lienkaemper, Shiu, Woodstock, *Obstructions to Convexity in Neural Codes*
- Jeffs and Novik, *Convex Union Representability and Convex Codes*
- Kunin, Lienkaemper, Rosen, *Oriented Matroids and Combinatorial Neural Codes*
- Bukh and Jeffs, *Planar Convex Codes Are Decidable*
- Jeffs and Trang, *Covering Relations in the Poset of Combinatorial Neural Codes*
- Current indexed literature searches for the exact phrases and mechanisms in the theorem table

## Priority language approved for the manuscript

Use “we prove,” “we give,” or “we reduce” for the mathematical statements. Avoid “first,” “new,” “novel,” “sharpest,” or “complete” except when describing a proof internal to the paper. State that the priority audit did not locate exact prior formulations but that search absence is not proof of novelty.
