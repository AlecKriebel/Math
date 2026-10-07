# Self-audit and acceptance boundary

## Current disposition

Five genuine mathematical approaches have been completed. The original geometric classification is **unresolved**. No full-solution or novelty claim is made. The packet offers rigorously argued partial results, subject to independent review of the arguments and cited dependencies.

## Counted approaches

1. **Normal-fan rigidity for triangles:** exact support-space proof and independent translation-identity proof; global small-γ conclusion uses established existence and rigidity.
2. **Transport and coercivity:** prove \(C^2\) dependence, stationarity, quadratic interaction control, and global sufficiency in the plane.
3. **Parallelogram integral comparison:** exact sign calculation classifying this subclass.
4. **Normal-direction continuation:** compute the negative square Hessian, construct an actual quotient chart, and apply the implicit function theorem to obtain nonsymmetric quadrilaterals.
5. **Degenerating-facet analysis:** derive the vertex-cut expansion and prove both signs by equilateral and thin-obtuse triangle examples.

Source retrieval, duplicate checks, formula sanity checks, and packaging are not counted as mathematical approaches.

## Delicate points checked

- **Source identity:** the DOI's authors are Bonacini, Cristoferi, Topaloglu. The source's non-even anisotropies include triangles and nonsymmetric quadrilaterals.
- **Source scope:** general-dimensional model, planar explicit classification passage; no replacement of the Riesz exponent by a fractional-perimeter exponent.
- **Stronger variations:** sliding and tilting theorems cannot be used to impose a square or equilateral-triangle conclusion in the fixed-normal problem.
- **All exponents:** the transport Hessian is controlled by \(|x-y|^{-\alpha}\) on the two-dimensional bulk. No assertion that a same-facet boundary Hessian is absolutely integrable for \(\alpha\ge1\) is made.
- **Cross-triangle pairs:** one continuous piecewise-affine map is used globally. Its Lipschitz derivative estimate controls pairs on different reference triangles as well as those on one triangle.
- **Exact area constraint:** support coordinates are restricted to a smooth area level set; the linear stationarity cancellation is followed by a second-order area remainder.
- **Translations:** the global energy comparison uses optimally aligned translates. The local four-normal chart fixes two support numbers using a unique translation, leaving exactly one constrained shape direction.
- **Global conclusion:** not inferred from stationary side averages alone. Existence, quasiminimizer rigidity, quantitative Wulff coercivity, and the quadratic interaction estimate are all required and recorded.
- **Square Hessian factor:** first derivative is \(2(M_b-M_a)\); the resulting second derivative is \(-4\alpha\) times the positive square integral. A second reduction to a one-dimensional integral was numerically checked.
- **Parallelogram angles:** both plus and minus cross terms have the same strict comparison after swapping integration variables. The proof covers every angle in (0,π), not only rectangles.
- **Nonsymmetric examples:** their normals explicitly fail to be two antipodal pairs. Thus they cannot accidentally be rhombi. Their exact supports are supplied by an implicit existence theorem, not by floating-point root finding.
- **Vertex cuts:** these are used to examine boundaries of allowed-normal families for the Riesz-only classification strategy. They are not claimed to be fixed-normal variations of the original triangle or to lower its full crystalline energy.
- **Thin-triangle limit:** restricted to \(0<\alpha<1\). Dominated convergence, the convolution polynomial, the closed-form integral, and the strict sign are supplied explicitly.
- **Smooth polygon hypothesis:** all sides have positive length and successive normals meet transversely. No unproved smooth parametrization through a vanishing side or a nonsimple higher-dimensional vertex is assumed.

## Verification

`verify_formulas.py` passes 12 parallelogram sign/symmetry checks, four square-Hessian consistency checks, and three thin-triangle convolution checks. These are floating-point sanity checks only. The strict signs and limit identities used in the proofs are established analytically.

The source PDF files are kept separately from this authored packet. The accompanying source-manifest metadata records source titles, URLs, byte counts, and hashes. No source text or source PDF is part of the authored packet.

## Remaining mathematical gaps

The equal-average system is not solved for arbitrary normal fans or arbitrary numbers of sides. Local continuation does not classify remote branches, prove global uniqueness, or control facet collapse. Higher-dimensional nonsimple polytopes are outside the transport proof's stated scope. A stronger interpretation demanding an explicit geometric classification therefore remains completely open here, even though the planar minimality property has an implicit integral criterion.

## Review priority

An independent reviewer should first scrutinize Approach 2's global sufficiency chain and Approach 4's use of the full constrained support chart. These are the most consequential partial claims. The known triangle observation must retain its 2022 attribution. The packet must not be promoted to a solved status solely because the implicit criterion is an equivalence.
