# Independent audit of the Ueno rationality routes

## Verdict

**Qualified pass after two controlling corrections.** The five retained approaches support an unfinished 5/5 investigation, with no full solution, no counterexample to either original question, and no verified prior unconditional resolution. The exact domain and dominant-component replacements in `CONTROLLING_CORRECTIONS.md` are mandatory when interpreting the frozen packet. An unqualified claim that the old model-side open suffices, or that the full unsaturated fivefold affine intersection is integral, does not pass.

The original manifest and all seven payload hashes match the supplied freeze. The author's 32 exact checks replay with identical JSON. A separate executable passes 115 exact controls, including an independently chosen smooth plane cubic and two new counterexamples to overbroad model-domain/component assertions. These computations verify algebra and reject specified invalid inferences. Their number does not turn the investigation into a research proof.

No frozen original was edited. No source PDF, source extract, screenshot, dataset record, raw connector response, or private coordination is part of the safe audit. No remote write or queue change was made.

## Exact target and limits of source binding

The [original OWR report](https://ems.press/content/serial-article-files/46562?nt=1), printed pages 816-819, concerns the diagonal order-six quotient of the equianharmonic elliptic curve. The explicit affine convention y^2=x^3-1 and g(x,y)=(omega x,-y) agrees with [Catanese, Oguiso and Verra](https://arxiv.org/abs/1506.01925), Definition 1.1. Here omega has order three and g has order six. The dimension is n, not the group order.

The questions at OWR page 818 are rationality of X_{4,6} and unirationality of X_{5,6}. COV Question 1.4 additionally asks rationality of X_{5,6}. That stronger question must stay separate. Smooth resolutions are birational to the finite quotient; their ordinary rationality, stable rationality, and unirationality are function-field properties. No use of a special resolution changes the questions.

The available descriptor IDs and public-source labels identify the intended subject, but the full imported problem text and raw prior AI report remain unavailable. Their statement/report hashes have not been recomputed. The original live target-page retrievals recorded HTTP 403; this audit does not claim to have inspected those live contents. The source-grounded mathematical target is clear, while literal equality with missing imported records is unverified.

[Oguiso's 2024 paper](https://arxiv.org/abs/2401.04386), Remark 1.3(3), still discusses the relevant rationality and unirationality questions. [Mellit's arXiv record](https://arxiv.org/abs/1705.02931) and the [published article](https://www.tandfonline.com/doi/pdf/10.1080/10586458.2019.1691088) retain conditional statements. These are positive statements about inspected sources. They are not a proof that no later solution exists anywhere.

## Route 1 Invariant field and birational model

The diagonal group fixes every ratio w_i=x_i/x_1 and v_i=y_i/y_1. Let F be the field they generate. The formula for T=x_1^3 lies in F, and y_1^2=T-1. Hence the full product field L has degree at most six over F. Since F is fixed by a faithful order-six group, [L:L^g]=6. The inclusions F subset L^g subset L force equality F=L^g. This is a sound fixed-field argument and does not need a claim that each radical has its maximal possible degree separately.

The automorphism is genuinely the full diagonal order-six action. Its square fixes the y-coordinates and its cube fixes the x-coordinates; those proper subgroups have larger invariant fields. Allowing independent actions in the separate factors would fail to fix the ratio generators and is a different quotient. The independent checks explicitly distinguish these cases.

Elimination is correct: the resultant of the two linear equations in q is 2U times the intended cubic relation. The inverse formulas recover all invariant generators, and the original positive witness establishes a nonempty chart after the corrected restrictions. In particular taking cube roots is only how one lifts a point to E^n; it is not a rational inverse to affine space.

Two errors would result from a literal unqualified reading of the original model discussion. First, the listed nonzero product can hold with T=0. Second, geometric integrality of the generic fiber does not remove vertical components from the unsaturated total affine intersection. The companion correction gives explicit counterexamples, a full replacement chart, both inverse compositions, and verification on the dominant component. With that correction, the function-field reduction passes.

## Route 2 Cubic surface over the two-variable field

Over K=C(s,t), all four diagonal coefficients are nonzero. Their partial derivatives are nonzero scalars times the coordinate squares, so the projective cubic surface is smooth even after algebraic closure. A smooth projective hypersurface of dimension two in P^3 is geometrically integral: distinct positive-degree components would intersect and cause singularities. The 27 displayed points with z=1 and cube-root coordinates are distinct K-points.

COV Theorem 3.4 applies under precisely the available hypotheses: characteristic different from two and three, a primitive cube root, the indicated diagonal form, and smoothness. It supplies a dominant map of degree at most six from P^2_K. Spreading its coefficients over an open of the rational two-dimensional base gives a dominant rational map from a rational fourfold over C. This proves the cited preexisting unirationality result, not rationality.

COV Theorem 3.5 is a classification criterion for these smooth diagonal cubic surfaces with a rational point. The audit visually checked the precise theorem statement; it is not being applied to arbitrary cubic surfaces or to the total fourfold. The three coefficient-pairing ratios, up to reciprocals, have valuations two at s=0, t=0, and s-t=0 respectively. Valuations of cubes are multiples of three. Therefore no allowed pairing quotient is a cube and the K-surface is not K-rational. The removed base divisors remain legitimate valuations of K; restricting the geometric base open does not change its rational function field.

A modification birational over this same K cannot change that answer. A birational reorganization over C that changes the embedded base field remains possible. There is no argument here for total-space nonrationality or stable nonrationality.

## Route 3 Fivefold generic complete intersection

Work over K=C(s,t,r), not over a degenerate specialized base or the full unsaturated A^7 scheme. Each column of the 2-by-5 coefficient matrix is nonzero, and all ten two-column minors are nonzero. The independent script extracts the matrix from the homogeneous equations, recomputes the minors, and checks that all their prime factors are among the factors inverted by B_5.

At a singular point of the complete intersection, a nonzero combination of the two gradient rows would vanish. In characteristic zero each nonzero coordinate would force its coefficient column into the one-dimensional kernel of that combination. Pairwise column independence allows at most one nonzero coordinate. The defining equations then force its nonzero column times its cube to vanish, impossible. This proves geometric smoothness, not merely smoothness at sampled rational points.

The first equation is an irreducible cone over a smooth cubic surface and does not involve w_5. The second has a nonzero w_5^3 coefficient, so it is not a multiple. The projective intersection has codimension two. It is nonempty, for example at the all-ones point, and has dimension two. Over an algebraic closure its Koszul resolution

0 -> O(-6) -> O(-3)^2 -> O -> O_S -> 0

and vanishing of intermediate cohomology on P^4 imply H^0(O_S)=the ground field. Thus S is geometrically connected. Smooth components cannot meet, so geometric connectedness and smoothness imply geometric integrality. These are the hypotheses missing from a shortcut that only asserts a smooth complete intersection without identifying a component or connectedness.

Adjunction gives K_S=O_S(1), an ample line bundle. The degree is nine, hence K_S^2=9. Twisting the Koszul resolution by O(1) gives h^0(K_S)=5. The general-type assertion follows from the ample canonical bundle; no classification theorem over an unspecified ground field is silently invoked.

A geometrically unirational surface in characteristic zero would admit a generically finite separable dominant map from a rational surface after resolving indeterminacy. A nonzero regular two-form on S would pull back to a nonzero regular two-form there, contradicting birational invariance and the vanishing on a smooth rational surface. Thus S is not geometrically unirational. In positive characteristic the separability point would require separate treatment; the audit makes no such extension.

This blocks the direct method that parametrizes this generic surface over its fixed base. It does not show that X_{5,6} is non-unirational over C. The rational total-space/general-type generic-fiber control rules out that invalid inference.

## Route 4 Alternative projection and genus one

For the projection to (w_2,w_3,w_4), the coefficient triple (A,B,C) consists of independent one-variable cubics in independent coordinates. The coefficient map is dominant and generically finite. Projection of the irreducible fourfold model to these three coordinates is dominant; its equation imposes a relation involving s and t, not a relation among the w-coordinates alone.

The homogeneous plane cubic is generically smooth. The author's (1,2,3) smooth specialization replays. Independently, the audit uses (2,5,11); in each of the three projective charts the ideal of homogeneous partial derivatives has Groebner basis [1]. Euler's identity in characteristic zero makes vanishing of the equation automatic when all partials vanish. The three charts exhaust projective space, so this proves geometric smoothness of that member. Projectivity makes the image of the singular incidence closed in coefficient space; consequently the generic member is smooth.

A smooth plane cubic is geometrically integral and has genus one. The point [0:0:1] is rational and has partial derivatives B and -C in the two relevant directions, so it is smooth at the generic parameters. The corrected dominant chart remains dense in this generic fiber, as explained in the controlling correction. Thus the alternative field extension really has an elliptic generic curve. Riemann-Hurwitz excludes nonconstant maps from P^1 to that curve after algebraic closure in characteristic zero. This is again a relative obstruction only.

## Route 5 Conditional curve counting

Mellit's later article does not supply an unconditional rationality proof. The arXiv v3 conditional statements correspond to published Conjectures 6.2-6.4. The author-provided Sage source has finite-field experiments enabled. This audit inspected the setup and counting code without executing that external program. The packet does not elevate Monte Carlo observations to a characteristic-zero theorem.

The packet's strengthened conditional lemma is valid with its stated incidence and normalization assumptions. The curves must be geometrically integral and generically rational, the parameterization must not count duplicate labels as distinct curves, uniqueness must hold at general points of both the variety and the selected divisor, the relevant curve must not lie in the divisor, and the section must lift to its normalization. After shrinking, the genus-zero generic curve with that rational point is P^1 over the divisor field. The resulting map from Z times P^1 has irreducible image containing Z and a curve escaping Z, so its image has dimension n. A unirational Z then gives a unirational total space. For rationality, rational Z and the one-point intersection hypothesis make the map generically one-to-one; characteristic zero converts that into a birational map.

The kernel divisors are correctly identified with E^3 and E^4 by solving for the last coordinate. Addition and integer or complex multiplication commute with the diagonal sixth-root action. Their finite quotients are therefore the required lower-dimensional quotient types; passage to resolutions preserves the associated function fields. Formal linear equivariance checks supplement, rather than replace, this group-variety argument.

What is absent is a characteristic-zero generic count for the actual H_144 and H_13824 curve families together with every needed incidence/intersection assertion. The lemma cannot be applied unconditionally without that input. The finite-field degree-drop example and finite-sample branch example are exact controls against two invalid routes to filling the gap. The second counts distinct geometric points and explicitly has nonreduced sampled fibers, so it is not falsely presented as a counterexample to a correctly controlled scheme-length computation.

## Inference boundaries and the neighboring record

The following implications are deliberately not made:

- finite degree of a dominant map does not imply degree one;
- nonrationality over a chosen function-field base does not imply nonrationality of the total field over C;
- general type or genus one for a chosen generic fiber does not obstruct rationality of the total space over C;
- a square in the coefficient ratios need not be a cube;
- generic integrality does not imply global integrality before removing vertical components;
- samples in finite characteristic or at finitely many parameters do not establish a characteristic-zero generic incidence theorem;
- rational connectedness, unirationality, ordinary rationality, and stable rationality are not interchangeable.

The graph morphisms from A^2 with t=y^2-x^3 and from A^3 with t=x^5+y^5+z^5 provide the first two geometric countercontrols: the total fields are rational while the generic projective fibers are elliptic and smooth quintic general-type surfaces respectively.

ID 30002830, OWR-13500-011, is supported by the method-specific question on printed page 819: a birational change of the cubic-surface description to establish rationality of the same fourfold. It overlaps the fourfold objective of ID 30002829 and excludes the fivefold objective. The present packet examines that surface, explains why a modification over the fixed K cannot work, and tries another projection. It does not rule out or construct a C-birational change mixing the base and fiber coordinates. Therefore the overlap is substantial but method-specific coverage is partial. No exact imported-record duplication is verified. This audit supplies no mathematical basis to call the neighboring question solved, fully covered, or exhausted, and consumes none of its attempt budget.

## Final disposition

The substantive local outcome remains unfinished after five retained approaches. The lower-dimensional theorem and the fourfold unirationality theorem are prior results. Both original questions remain unanswered by this packet, and fivefold rationality remains an unanswered stronger related question. A local recommendation of exhausted 5/5 means the bounded investigation ended; it is not a theorem that all possible mathematical approaches were exhausted. Independent verification establishes the repaired partial results and their limits, with no novelty or global-current-openness claim.
