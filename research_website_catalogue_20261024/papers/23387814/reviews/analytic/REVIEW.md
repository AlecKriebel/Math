# Independent analytic review — Zenodo 23387814

**Verdict: PASS for the stated mathematical theorem.** No substantive mathematical defect was found in the five-page version 1.0 manuscript. The claim is a counterexample to the specific proposed lower bound, not a priority claim, a calculation of the exact Seshadri constant, or a result for all polarizations on one fixed surface.

This is an internal analytic review, not human peer review or proof-assistant certification. The proof uses standard algebraic geometry, and the finite computations corroborate rather than replace its existence and ampleness arguments.

## Published object and coverage

Title: *A Minimal-Surface Counterexample to a Seshadri Lower Bound*, Alec Kriebel, 14 October 2026, Zenodo 23387814, version 1.0.

- Published PDF: `sources/seshadri_counterexample.pdf`, five pages, SHA256 `8f50f329fac5b30ffea3d98f82e36ec71af0d3d5df44e38a21f992eb45aa4c48`.
- Published ZIP: `sources/verification_package.zip`, SHA256 `6af7c815f863d44ba4b24708d5ae70bec4d5e0fd55789114083a605c08a27a20`.
- Main source: `sources/published-source/seshadri_counterexample_verification/seshadri_counterexample.tex`; exact source hash is recorded in `verdict.json`.

Read all five PDF pages, all main TeX, the original author's full `PROOF.md`, and the five mathematical helper programs listed under replay below. Visually inspected the current PDF's pencil/cover/intersection pages and the primary-source pages displaying the original lower bound and cyclic-cover formula. There are no other reader PDFs in the published verification ZIP. Dedicated historical reports/verdicts, acceptance files and sibling reviews were not read.

Before opening submitted helpers, I reconstructed the geometric proof and wrote `fresh_controls.py`: diagonal-lattice computations, symbolic all-degree inequalities, the singular-curve algebra and local cover checks. The published mathematical helpers were then read and replayed. Incidental author-status language in the manuscript and original `PROOF.md`, and comments describing old audit code, were encountered; none was used as evidence of correctness. Executing a helper's fresh assertions is distinguished from accepting an old verdict.

## Exact target and source authentication

The theorem requires, for every integer `d >= 7`, a smooth integral projective surface over **C**, an **ample integral** line bundle `L`, and a **special closed point** `x`, with

`K_S` ample, `K_S^2 = 6(d−1)(d−3)`, `L^2 = 6`, and

`epsilon(S,L;x) <= 1/(d−1) < 1/(2 + (K_S^2)^(1/4))`.

The question is authenticated in Szemberg's [2007 preprint](https://arxiv.org/pdf/0711.0584v1), final question on p. 7; in his [Oberwolfach contribution](https://ems.press/journals/owr/articles/3471), Conjecture 2 on printed p. 1124 (PDF p. 24); and in [*A primer on Seshadri constants*, v2](https://arxiv.org/pdf/0810.0728v2), Question 6.1.6 on p. 17. The fourth root encloses `|K_S^2|` alone. The additive 2 is outside the root. The universal conjecture has no Picard-rank-one or very-general-point restriction. The cited original article also proves narrower results, but the final question and the Oberwolfach formulation explicitly move beyond that restriction.

The construction produces an arbitrary ample integral polarization, not the canonical polarization, an adjoint polarization, or a globally generated line bundle. Since the question is universal in `L` and `x`, one such `L` and one special point suffice to contradict it. `K_S^2 > 0` in the constructed examples, so the absolute value creates no ambiguity.

## Analytic reconstruction

### 1. The singular plane curve and integral pencil (published p. 2)

Set `f_d = Z(X^(d−1)−Y^(d−1)) + X^d`. In `C[X,Y][Z]`, its two coefficients are coprime: any divisor of `X^d` is supported on `X`, whereas `X` does not divide `X^(d−1)−Y^(d−1)`. It is a nonconstant linear polynomial over `C(X,Y)`. Gauss's lemma therefore gives irreducibility over `C[X,Y,Z]` and an integral plane curve.

At `[0:0:1]` the local equation has order `d−1`, with tangent cone `x^(d−1)−y^(d−1)`. Characteristic zero makes its `d−1` linear factors distinct. For the singular locus, `f_Z=0` gives `X^(d−1)=Y^(d−1)`. If either coordinate is zero, both are zero, giving the marked point. Otherwise `f_Y=−(d−1)ZY^(d−2)=0` forces `Z=0`, and then `f_X=dX^(d−1)` cannot vanish. Thus there is no other singular point. This proof is uniform in the asserted degrees. The independent exact controls also check a rational parametrization and the squarefree tangent cone; these finite checks are corroboration.

Let `N_e=e(e+3)/2`. All reducible or nonreduced degree-`d` forms occur among products of degrees `a` and `d−a`, `1 <= a <= d−1`. Each multiplication map is projective, so its image is closed, and

`N_d−N_a−N_(d−a) = a(d−a) >= d−1`.

The last inequality follows from the exact factorization

`a(d−a)−(d−1) = (a−1)(d−a−1) >= 0`.

The join of this bad locus with the fixed irreducible form has dimension at most `N_d−d+2`, strictly below `N_d` for `d>=3`. A direction outside its closure defines a projective line that misses the entire bad locus. This excludes reducible members throughout the pencil, not merely its two generators or general members. A nonreduced plane polynomial of degree at least two has a nontrivial factorization and is included in the excluded locus.

The remaining requirements on the second generator are nonempty open conditions in the same irreducible projective parameter space: smoothness, nonvanishing at the marked point and transverse intersection with the smooth part of `C_0`. They can therefore be imposed together with the join-complement requirement. For transversality, the complete degree-`d` system restricts to an immersion of the smooth curve locus; it separates tangent directions. Bertini applies to that smooth open locus, and avoiding the single singular point prevents a missing boundary intersection. Bézout then gives exactly `d^2` distinct simple base points, none at the marked singularity.

No numerical choice of the second generator is supplied or needed for this existence theorem: the construction is specified by a nonempty open choice, not an algorithmically enumerated pencil. This distinction is consistent with the full proof.

At a transverse base point the two generators are local parameters `(u,v)`. The blowup resolves the ratio `[u:v]` in one step. Its exceptional curve maps isomorphically to the pencil base, so it is a section. Each pencil member is smooth at those base points and its strict transform is exactly a fibre, with no exceptional vertical component. Consequently **every fibre is integral and reduced**, and the marked high-multiplicity point is untouched by the blowups. General fibres are smooth, leaving finitely many nonsmooth fibre values.

### 2. The first ample polarization (p. 2)

On the blowup `Y`, take `H^2=1`, `H.E_i=0`, `E_i.E_j=−delta_ij`, and `F=dH−sum E_i`. Directly, `F^2=0`, `F.E_i=1`. With `A=2F+E_1`,

`A^2 = 4F^2+4F.E_1+E_1^2 = 3`, `A.E_1=1`, and `A.F=1`.

The fibre class is nef. For every integral curve other than `E_1`, intersection with the effective curve `E_1` is nonnegative. If `F.D>0`, then `A.D>0`. If `F.D=0`, the map from the curve to the pencil base is constant: on its normalization, the degree of the pullback of `O(1)` is zero. Thus it is vertical; the all-fibres-integral-and-reduced property makes it the whole fibre, giving `A.D=1`. The exceptional case `D=E_1` was checked separately. Together with `A^2>0`, this checks every hypothesis of the surface Nakai–Moishezon criterion. There is no illicit inference from positivity on a finite list of curves.

### 3. The double cover, smoothness and integrality (pp. 2–3)

Choose four distinct smooth fibre values, excluding the marked one. A connected double cover of `P^1` branched simply at these four values exists: a squarefree quartic gives its affine equation, and its smooth projective completion has genus one by Riemann–Hurwitz. Even quartic degree gives no extra branch point at infinity. The map is finite flat of degree two; the same holds after base change to `Y`.

The fibre product `S` is smooth off the four branch fibres because the cover is étale there and `Y` is smooth. This remains true above singular points of unbranched fibres: the fibre may be singular while its ambient surface remains smooth. At a branch fibre, the original fibration is smooth, so the local equation can be written `w^2=t` in smooth coordinates `(u,t)` on `Y`. Its derivative in `t` is a unit, proving smoothness. Thus no normalization, resolution or contraction is silently changing the intersection numbers.

The map `S→B` is proper and surjective with connected geometric fibres, each the corresponding original integral fibre. If `S` were a disjoint union of two nonempty open-and-closed pieces, connected fibres would make their proper images disjoint closed subsets covering `B`, contradicting the connectedness of `B`. A smooth variety's irreducible components cannot meet; hence a connected smooth `S` is integral. It is projective as the closed fibre product inside the product of projective varieties. These facts justify treating `S` as the surface required by the question.

The branch divisor is a disjoint union of four smooth fibres and has class `4F`. The covering line bundle is `O_Y(2F)`, pulled back from `O_(P^1)(2)`. The cyclic-cover canonical formula gives

`K_S = pi^*(K_Y+2F)`.

Equivalently, Hurwitz gives `K_S=pi^*K_Y+R`, and the reduced ramification divisor has line bundle `pi^*O_Y(2F)`. The factor `2F` is essential: using `F` would not establish the required canonical positivity.

### 4. Ample canonical class and minimality (p. 3)

Since `K_Y=−3H+sum E_i`, write

`N=K_Y+2F=(2d−3)H−sum E_i=(d−3)H+F`.

For every exceptional curve, `N.E_i=1`. Every other integral curve has a plane image of positive degree `e`, so

`N.D=(d−3)e+F.D >= (d−3)e > 0` for `d>=4`.

Furthermore `N^2=(2d−3)^2−d^2=3(d−1)(d−3)>0`. Thus Nakai–Moishezon proves `N` ample. The finite surjective pullback is ample: by projection, for any curve upstairs its canonical degree is a positive degree times `N` intersected with its image curve, and its square is `2N^2>0`; Nakai applies directly on `S` as well. This establishes canonical ampleness, not just bigness or nefness.

A smooth rational curve of self-intersection `−1` would satisfy `K_S.E=−1` by adjunction, impossible for an ample canonical class. Thus the smooth projective surface is minimal and of general type. The intermediate blowup is nonminimal, but the final surface is not being identified with it. Its lifted exceptional sections are genus-one curves of square `−2` and canonical degree 2, consistent with this conclusion.

### 5. The marked curve and exact numerical violation (pp. 3–4)

Set `L=pi^*A`. Finite pullback makes this an ample integral line bundle, with `L^2=2A^2=6` and `K_S^2=2N^2=6(d−1)(d−3)`.

Over the unbranched marked value, `B` has two distinct complex points. Base change of the whole fibre is therefore a disjoint union `C'` and `C''`, each scheme-isomorphic to `C`. This remains valid for a singular integral fibre. In particular `C'→C` has degree **one**, although `pi:S→Y` has degree two. At the marked point upstairs, `mult_x(C')=d−1`, and projection gives `L.C'=A.C=1`. The defining Seshadri infimum therefore supplies the upper bound `1/(d−1)` without any claim to have minimized over all curves.

For `d>=7`, positive denominators make the desired comparison equivalent to `d−3 > (6(d−1)(d−3))^(1/4)`, then to `(d−3)^3>6(d−1)`. My independent universal positivity check sets `d=q+7`, yielding

`(d−3)^3−6(d−1) = q^3+12q^2+42q+28 > 0` for every integer `q>=0`.

This proves the whole quantified range, not merely tested degrees. At `d=7`, `K_S^2=144`, and `144<4^4=256` proves `1/6 < 1/(2+144^(1/4))`. At `d=4,5,6`, the cubic comparison margins are `−17,−16,−3`: the displayed curve gives no violation there. No lower bound on those other examples follows from this failure of one test curve.

## Imported results and attribution

The original-question PDFs and the cyclic-cover formula were checked at their exact printed locations; URLs, hashes and reading scopes are retained in `primary_interfaces.json`. The cyclic-cover interface in [Fuentes García, Section 2, p. 3](https://arxiv.org/pdf/math/0511547v2) assumes a smooth surface and a smooth reduced branch divisor linearly equivalent to `nM`. Here `n=2`, `M=2F`, and the disjoint smooth branch fibres meet those assumptions. Its later Seshadri theorems for ramification points or Picard-rank-one bases are not used.

For Bertini, the complete degree-`d` system on `P^2` is globally generated and defines a Veronese immersion. Its restriction to the smooth open curve locus remains an immersion. These are the precise hypotheses of [Stacks, Lemma 33.47.3](https://stacks.math.columbia.edu/tag/0FD4), separately giving general smoothness and transverse intersections. For Nakai–Moishezon, all varieties in question are smooth projective surfaces and the divisors are integral Cartier divisors; the proof verifies positive square and positive intersection with every integral curve. No uniform positive lower bound on all normalized curve classes is required by that criterion.

The first pencil polarization is classical: [Ein–Lazarsfeld, Example 3.1, p. 182](https://numdam.org/item/AST_1993__218__177_0/), [Bauer, Proposition 3.3 and proof](https://arxiv.org/pdf/math/9903072v1), and [Bauer–Szemberg, Proposition 2.1](https://arxiv.org/pdf/1011.0979v1) describe it. Bauer's finite-degree use is asymptotic in the cited argument; the present manuscript supplies its own explicit singular curve and join-dimension existence proof for each degree used, so there is no unsupported specialization from “large enough” to `d=7`. The related canonical-polarization double-cover example in [Bauer–Szemberg, Example 1.3](https://arxiv.org/pdf/0801.3245v1) has canonical curve quotient `1/2`, and does not establish this smaller quotient for the present arbitrary polarization. Ein–Lazarsfeld Example 3.7 concerns unbounded very-ampleness indices, a different assertion. These attribution distinctions check out. No exhaustive priority search was undertaken.

## Computation and reproducibility

Fresh evidence written before reading submitted helpers:

- `fresh_controls.py` and `fresh_controls.json`: full diagonal intersection lattices for `d=3..30`; singular curve, tangent squarefreeness, parametrization and local cover controls for `d=3..15`; symbolic factor-degree codimension identity and all-degree comparison identity. No floating roots are used.

Five submitted mathematical scripts were fully read and freshly executed, all returning exit code zero with empty stderr:

| Published script | Fresh replay evidence |
|---|---|
| Original author `verify_formulas.py` | 97 degree rows; polynomial/dimension/cover/Noether identities |
| Original author `verify_intersections.py` | 27 degree rows; full blowup lattice and split-fibre degree |
| Original `audit/independent_checks.py` | 60,731 assertions; symbolic incidence-ring and other controls; exact comparison with saved numerical outputs |
| `reviews/geometry01/geometry_controls.py` | 1,183 controls; branch algebra, local smoothness and failure modes, upstairs lattice |
| `reviews/pencil01/fresh_controls.py` | 28,945 controls; singular scheme, factor dimensions, local blowup, exact thresholds and negative controls |

Each source hash, stdout hash and timestamp appears in `published_replay_receipts.json`. Outputs are retained as fresh files in this analytic directory. The helpers under historical review directories were read as mathematical code only; their historical reports and verdicts remain unread. Their descriptions do not make them independent of this submission for the present review. The new analytic derivation and pre-helper controls supply the independent component here.

Execution used the existing Math environment with SymPy 1.14.0 and mpmath 1.3.0. The first fresh-control attempt under system Python failed because SymPy was absent; a structural-expression equality in my fresh script was replaced with an algebraic zero-difference check. Both were reviewer implementation/environment issues, not paper defects. The corrected fresh controls passed. No paper or published helper was edited.

The release's global packaging/priority-acceptance wrapper was not run: it would add historical-status and packaging checks rather than a missing mathematical test. This is a replay of all five relevant mathematical programs, not a claim of byte-for-byte full release-workflow re-execution. No formal proof checker was used.

## Boundaries and final disposition

**Strongest verified claim:** for every integer `d>=7`, the published construction yields a smooth integral minimal complex projective surface with ample canonical bundle, `K_S^2=6(d−1)(d−3)`, an ample integral polarization of square 6, and an integral curve through a point with Seshadri quotient `1/(d−1)` strictly below the specific proposed lower bound. The analytic proof checks the existence, all-curve positivity, smoothness, connectedness, degree and multiplicity issues that finite code cannot establish by itself.

**Exact remaining limits:** there is no unresolved mathematical step in the stated theorem identified by this review. Historical priority and the question's immediately-prepublication open status are not established; the paper itself explicitly declines those claims. An exact Seshadri value, a numerical second pencil generator, arbitrary-point or very-general-point violation, Picard-rank-one violation, and a vanishing infimum on one fixed surface are not proved and are not required for the theorem. The standard foundational results are applied rather than re-proved formally. Independent expert review remains distinct from this internal analysis.

No repair, website, promotion, spreadsheet, Git, UI or outreach action was taken. Completion: 100% of the assigned analytic review.
