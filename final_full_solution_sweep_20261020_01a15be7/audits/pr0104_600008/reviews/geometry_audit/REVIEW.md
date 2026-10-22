# PR104 independent adversarial geometry review

**Verdict:** PASS for the stated analytic theorem, including its separate equator-map and full-arc conventions. No substantive mathematical gap or counterexample was found. This is not priority clearance and not a finite algebraic Cayley criterion.

## Independence and exact input

The reviewer read the pinned `original_head/ANALYTIC_CRITERION.md`, author checker, source manifest and bibliography, then recorded `INDEPENDENT_DERIVATION.md` before reading historical verdicts. The reviewer never read `original_head/review/REVIEW.md` or the historical review results. The primary sources were independently downloaded and their relevant complete PDF pages rendered and visually inspected. The fresh source hashes match the original manifest.

- Mathematical artifact SHA256: `608217a2ffc120a965b165f5b6065edd83f8cf94c5e77f0f95a0326640db2dae`.
- Author checker SHA256: `4c3c7d42bff5772827044916fd7b62cfa3fa8e2be2a08b9788ec8bcd91be2040`.
- Exact downloaded-source hashes and rendered pages: `SOURCE_RECEIPT.json`.
- Independent script and receipts: `independent_checks.py`, `INDEPENDENT_CHECKS.json`, `AUTHOR_REPRODUCTION.json`.

## Original problem and scope

[GKT, arXiv:0705.0188v1](https://arxiv.org/pdf/0705.0188v1), printed pp17–18, defines T by going from the equator to the Northern tropic along one null family and returning along the other; Problem 5.2 asks for a parameter condition with specified iteration count and winding. Its Section 4 invariant density agrees with dS. [Tabachnikov (2015), Section 7, printed p62](https://amj.math.stonybrook.edu/pdf-Springer-final/014-0001-3.pdf), instead describes alternating tropic-to-tropic arcs. The printed question asks for conditions on positive a,b,c; its title and Cayley comparison motivate a possible stronger algebraic interpretation, but no determinant or polynomial form is explicitly required in the question's sentence.

The artifact correctly distinguishes the two counts. It resolves the literal analytic parameter-condition question for both interpretations of a step. It does not prove a finite polynomial/determinant condition, historical novelty, or equivalence to arithmetic announcements. Those are exact remaining scope/priority limitations; they must not be erased in promotion.

## Deliberate falsification checks

1. **Global coverage and degeneracies.** For any closed-belt point, E(c)-1=-z²/c≤0 and E(0)-1=cN≥0, where N=x²/a²+y²/b²-z²/c². E'(v)<0 since x,y cannot both vanish in the belt. Thus v is unique, and signed cosine/sine recover t, including the coordinate axes. No general-position hypothesis a>b is needed for this inversion. The signed hemispheres agree precisely at the equator. The compact-boundary map is a homeomorphism; the open-belt chart is nonsingular after using Y.

2. **Metric.** Direct Cartesian differentiation, independently using k=tan(t/2), proves the ellipsoid, normal, cross-term and both metric coefficient identities. On 0<v<c the coefficients have the required Lorentz signs. The formula extends to a=b without division by a-b. The proof does not extend the Lorentz metric into the polar caps.

3. **Equator and tropic.** The equator tail H-τ(c-ε) is sqrt(ε) times an analytic nonzero function; z has the same signed square-root factor, so Y glues smoothly across the equator. Near v=0, τ(v)=v^(3/2) times an analytic nonzero function. The tropic extension is a homeomorphism with a degenerate normal derivative. This is sufficient to take endpoint limits of null curves; no illicit regular Lorentz chart at the tropic is used. Switching the null family yields the expected cusp.

4. **Null geometry.** For a nonzero null tangent X on a Lorentz surface, metric compatibility gives ∇_X X orthogonal to X; in dimension two X-perp equals span(X). Thus the null line curves are exactly unparameterized null geodesics. In the conformal cylinder they have slopes ±1, giving ΔS=2H for either a folded T passage or a full tropic-to-tropic arc. The direction choices yield positive S advance consistently.

5. **Contour identity and signs.** Following the infinity-normalized square root from x>c into the upper half-plane gives R=+i sqrt(|P|) on (0,c) and R=-i sqrt(|P|) on (-a,-b). In both cases z/R is -i times the claimed positive integrand. Upper banks are traversed right-to-left by counterclockwise cut loops. All finite endpoint loops vanish; the outer 1/z term contributes 2πi. Hence I_u+I_v=π with the displayed signs. The quadrant substitution gives I_u=L/2. At a=b the coincident branch-point proof is replaced, correctly, by continuity or direct rotational evaluation.

6. **Winding, periods, orientation.** S/L is a degree-one equatorial coordinate. The ambient angular projection is homotopic to t through ellipses with positive axes; therefore lifted S winding is ordinary winding. This is valid even for ρ>1, when reducing a rotation number modulo one would lose turns. The full-arc map changes boundary component every step, so even n is necessary and sufficient in addition to nρ=r. Exact discrete tests verify q versus lcm(2,q) counting; the axisymmetric a=b=1,c=8 case gives ρ=1, an equator-map fixed point but no closed one-arc chain. Reverse orientation reverses winding; nontrivial positively advancing chains have positive winding.

7. **Uniqueness and limits.** The density is positive, strictly decreasing in c and smooth on the compact angular interval. Its c→0 and c→infinity limits give M→1 and M→0, respectively. This proves the unique positive c for each r/n>0; the implicit-function and strict unequal-axis bounds follow. Common scaling invariance and the a=b formula are consistent. Values a,b,c=0 are excluded and only used as limits.

8. **Discarded torsion inference.** The correction is sound: the displayed quartic differential has two simple poles with nonzero opposite residues ±i/2 at infinity. It is third-kind, so ordinary elliptic-group torsion does not follow from the real circle translation. This does not invalidate the new analytic proof, which does not use that inference.

## Reproducibility and numerical attempts to falsify

After a safety read, the author checker passed all 2,087 assertions under SymPy 1.14.0. The independent checker passed 11 symbolic Cartesian/chart/endpoint identities, 10,469 exact small discrete two-boundary states, and 22 diagnostic checks. These counts are routine controls, not independent proofs of every global statement.

The numerical checks use mpmath 1.3.0 at 60 decimal digits for nonsingularly regularized integrals. Seven parameter triples cover a>b, a<b, a=b, thin/long ellipsoids and scale ratios up to 10^18; all period residuals were below 10^-45. A separate RK4 integrator uses the ordinary chart x=sqrt(a(1-q²))cos(theta), y=sqrt(b(1-q²))sin(theta), z=sqrt(c)q and the two roots of its Cartesian null quadratic. It does not use the proposed v,S,Y coordinates or rotation formula. Four Northern passages, including a multi-turn example, agreed with the predicted S advance within 1.55×10^-9; step refinement was below 1.82×10^-8 in theta. These computations are explicitly diagnostic and are not validated interval certificates.

Reproduce from the repository root:

```sh
final_full_solution_sweep_20261020_01a15be7/private/venv/bin/python final_full_solution_sweep_20261020_01a15be7/audits/pr0104_600008/reviews/geometry_audit/independent_checks.py
```

Only SymPy 1.14.0 and mpmath 1.3.0 are required. The script writes solely in this review folder and reads the pinned original files. It does not perform remote mutations.

## Strongest verified statement and exact gap

For every a,b,c>0, the actual-path lift of the positively advancing GKT equator map is smoothly conjugate to translation by ρ=(1-M)/(2M), with the displayed explicit positive one-dimensional mean M. Thus T^n closes with winding r exactly when M=n/(n+2r); literal full tropic-to-tropic arcs have the additional even-n condition. The stated minimal-period and parameter-uniqueness conclusions hold.

There is **no remaining substantive objection to that analytic theorem**. A finite algebraic Cayley condition is not proved. Historical priority and whether this analytic formulation qualifies as the intended novel open-problem resolution remain separate gates for the root audit. No publication, merge, spreadsheet or Zenodo decision is made by this review.
