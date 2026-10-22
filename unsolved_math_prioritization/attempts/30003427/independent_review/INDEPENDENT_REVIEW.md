# Independent review: finite bid–ask consistency, 30003427

## Verdict

**PASS_FULL_ALGORITHMIC_CLASSICAL_CONSEQUENCE. No mandatory mathematical correction.** The candidate supplies a terminating exact finite-data characterization in the literal source model, with the computation qualification and possible nonattainment stated explicitly. This is a classical-method consequence, not a claim of short financial inequalities, practical calibration software, new quantifier elimination, or historical priority.

The exact reviewed proof is `PROOF.md`, SHA-256 `f16fc7625a94fe83d84ee76e8a105b2cec898036c28ef8d04d7aab4f1c5bc65c`. The frozen author manifest SHA-256 is `a6d128e3bde50ac32e657dd2ccb391b14bb07989d97a27c38585f07b6c0e9fe2`. All twelve author artifacts and six pinned source files match their hashes. The reviewer did not contribute to the candidate before freeze and did not alter it.

## 1. Literal source scope

I read and visually inspected OWR 13/2017, printed p. 697. The requested object is a necessary-and-sufficient consistency criterion for finite call panels at multiple dates, with an associated smallest spread bound. The source explicitly assumes finite probability spaces and discrete dates. It expresses doubt about simple conditions but does not impose a formal efficiency or short-form requirement.

The candidate gives more than another infinite-dimensional existence criterion: an explicit uniform tree-size bound permits a finite first-order formula, and a specified classical elimination procedure removes every model variable. This is a valid algorithmic characterization in quote data alone for each finite quote shape. The source-scope PASS is for that precise algorithmic reading. It is not a resolution of a separate calendar-vertical-basket sufficiency question or of the desire for useful elementary market inequalities.

For exactly represented rational or real-algebraic data, construction, quantifier elimination, univariate root isolation and endpoint testing are terminating mathematical algorithms. For arbitrary real inputs, the output remains a formal semialgebraic condition in parameters; the proof correctly avoids promising finite-bit computation on noncomputable real numbers. The provided scripts compile and test the system, but do not execute general elimination. Their output-size safeguard is a software limitation, not a theorem restriction.

## 2. Exact model, discounting and positivity

I checked Gerhold–Gülüm Definitions 2.1, 2.2 and 2.4 both in arXiv v2 and in the full final publisher XML provided by Europe PMC. The final definition retains a strictly positive stock bid. Its arbitrary adapted settlement reference and its shadow martingale are distinct processes. The reference lower bound is imposed at positive dates; the spread bound also applies at time zero. The proof preserves all of these conditions.

The discounted formulation is equivalent: two positive values R and Z at distance at most epsilon can be enclosed by their positive minimum and maximum, giving a permissible bid and ask. No midpoint condition is introduced. Conversely both values in a spread of width epsilon have that distance bound. Positive deterministic bank factors preserve the inequalities under rescaling, and the cash-settlement payoff discounts to the asserted positive part.

A nontrivial initial sigma field is harmless here because its physical law is not fixed by the input. Replacing it by the trivial sigma field and the initial shadow by E[Z_1] retains the deterministic initial interval by convexity, leaves later conditional martingale equations intact, and preserves every unconditional quote expectation. There is no initial reference variable to preserve. The extra strike restriction used in some source inequalities is not part of Definition 2.4; optionally intersecting the admissible set with that range is correctly described.

## 3. Conditional finite support, including auxiliary references

The principal compression proof is valid. At each original filtration atom, the original conditional vector consists of the next shadow value and conditional expectations of all q recorded payoffs. Its barycenter lies in a finite convex hull in R^(q+1), so at most q+2 actual children suffice. Zero weights can be discarded. Importantly, the recursive step uses original conditional continuation values at the retained node. Backward induction from actual terminal payoff vectors proves that subsequent child reductions preserve these values, including calls paid earlier and then held constant.

Thus every retained node keeps its actual reference and shadow labels, all pathwise constraints, and all local martingale equations. The reference need not be a function of shadow history. The candidate explicitly avoids the invalid shortcut of applying a shadow-path cubature theorem to an auxiliary observable that may not be shadow-path measurable.

Duplicating an actual child and its continuation subtree, while splitting its weight into strictly positive pieces, fills a full b-ary tree without adding model restrictions. Extra filtration labels are permitted. There are b^T leaves, b=q+2, and every node has positive probability. This full-tree representation does not assume that different leaves have different prices.

Beiglböck–Nutz Theorem 5.1 supplies the credited martingale Tchakaloff context. The direct finite-tree proof is sufficient on its own for the source's finite models; no infinite-support, compactness or measure-selection extension is needed.

## 4. Polynomial system and equivalence

Every displayed constraint has the claimed meaning. Local conditional probabilities are positive and sum to one. The weight recursion gives positive leaf probabilities and unit mass at each level. Conditional martingale equations are imposed at every node, rather than merely enforcing unconditional means. The reference and shadow domains preserve strict positivity and the lower bound.

The three positive-part constraints are exact: c is nonnegative, lies above r-k, and equals one of 0 and r-k. For r-k positive the first root is excluded; for r-k negative the second is excluded; at zero both roots coincide. Thus no spurious payoff branch survives. Quote expectations use the appropriate level weights. All constraints are polynomial of degree at most two after discounting; the number of variables is explicit from the full-tree bound.

Necessity follows by compression and padding. Conversely the leaves with recursively defined weights and history filtration give a finite probability space, actual conditional probabilities, adapted reference/shadow values, the required martingale, calibrated calls and reconstructed stock spreads. There is no missing cross-date constraint or signed-measure relaxation.

## 5. Quantifier elimination and optimization boundary

The classical real-closed-field elimination theorem applies to this finite conjunction, including its strict inequalities. Quantifying all tree variables yields a quote-only Boolean formula. For algebraic inputs its one-dimensional epsilon set can be decomposed into finitely many points and intervals with algebraic endpoints and exact inclusion flags. Empty sets, unbounded components, identically vanishing specialized polynomials and strict endpoint exclusions are covered.

A nonempty admissible set is bounded below by zero, so its infimum is finite. Testing the endpoint distinguishes an attained minimum from a nonattained infimum. This does not require the set to be closed or monotone; the reference lower bound indeed becomes stronger when epsilon increases. Algebraic sampling in a nonempty semialgebraic fiber produces an algebraic model if requested. No assertion about numerical optimizer reliability or computational tractability is inferred.

## 6. Nonattainment example

The two-state, two-date model has the exact advertised mean-one shadow and strictly positive labels for each 0<epsilon<1/4. Its high-state reference-shadow distance is epsilon/3, and every low-state call is out of the money. The quoted call expectations follow exactly, and both dates share the same state after time one.

At epsilon zero, the zero-cost butterfly forces absence of mass in the open interval between the extreme strikes. The call spread then fixes upper-tail mass at 3/4, including the upper endpoint, and the upper-strike call fixes its first moment at one. The complementary event has mass 1/4 but would have zero first moment, contradicting strict positivity. The argument handles both strike endpoints correctly. It proves exclusion of epsilon zero while all sufficiently small positive epsilon remain feasible, hence a nonattained infimum of zero. It makes no claim about the full admissible set in that example beyond what is proved.

## 7. Independent controls and disposition

The author's 16,697-assertion receipt and generated example system replay byte-for-byte. My separately written checker, which imports no author code, passes 5,661 exact assertions. It obtains supports by enumerating affine-independent convex supports rather than the author's nullspace-pruning implementation. It checks conditional compression and positive padding on models with identical shadow histories but different adapted reference values, evaluates the saved polynomial formula with a separate exact AST evaluator, and tests invalid mutations. It also checks the strict-positive nonattainment identities and includes a negative example demonstrating why preserving only global marginal means is insufficient.

The finite computations support the concrete algebra and encoding. They do not replace the source/model proof, Carathéodory theorem or real quantifier elimination, and no general CAD computation was run. The portable checker accepts an optional attempt-directory argument; by default it uses the parent of the published review directory. Python and SymPy are required.

Recommended disposition is a credited classical-consequence result, with the exact algorithmic scope prominent and one substantive author turn recorded. No further four turns are mathematically required for the literal characterized target once the parent accepts this independent full-scope verdict. Any broader request for short explicit calendar inequalities or efficient implementation remains separate. The parent retains the publication gate; this report does not create a PR, update a queue, certify novelty, or represent human peer review.
