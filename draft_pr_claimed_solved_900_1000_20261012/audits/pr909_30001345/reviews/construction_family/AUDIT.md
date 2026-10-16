# Independent construction and analytic-topology audit of PR909 / problem 30001345

Date: 2026-10-15 UTC. Family: analytic/algebraic construction and local topology. Immutable candidate head: `d186dea31791cd3e8acf6829e0b65d01849623b8`.

## Decision and exact scope

**PASS for the construction and analytic-topology gate. No required mathematical correction in this family's scope.** The proposed polynomial gives a reduced flat complex deformation, including at parameter zero, with a finite simultaneous normalization, nine normalization disks, and a uniform transverse boundary representative. For every complex `0 < |t| < 1/4`, the representative contains exactly twelve ordinary triple points; its central fiber has one ordinary ninefold point. The singularities have total delta 36 on every fiber. The independently checked elementary blowup computation gives rough `K·(K+D)` totals 7 and 12.

This decision does not establish priority, novelty, present-day openness, or unrestricted equivalence of an imported problem with every later conjecture. Those are separate gates. In particular, the central normalization has nine components, so this is not a unibranched or parametric deformation in the later source's sense. No original acceptance file, prior audit verdict, or original checker was read or executed. The mathematical reconstruction and attempted falsification began from `frozen_v2/PROOF.md`, the charter, identity preflight, and private source record only.

The frozen proof SHA256 is `561b189c2091eaeccccf89fdd933b2300ec676a871d7229ebfaf8c806962fe8b`. The frozen package-manifest SHA256 is `a8376fa67c497c4b31522364ac87163cdd6f5ec42961893981c44f0d95f0ee02`. Both match the supplied identities.

## Claim reconstructed before attempted falsification

Let `w` be a primitive cube root of unity and `q ∈ {1,w,w²}`. Put

\[
F=(x^3-y^3)\bigl(64y^3-(t-x-2y)^3\bigr)\bigl((t-x-2y)^3-64x^3\bigr).
\]

The nine factors are

\[
a_q=x-qy,\quad b_q=qx+(4+2q)y-qt,\quad c_q=-(1+4q)x-2y+t.
\]

The success criterion is stronger than obtaining the two numerical invariant totals: the family must be flat as a holomorphic representative, all fibers must be reduced, special-fiber base change of the normalization must actually normalize that fiber, no singularity may escape the representative, and the entire boundary union must remain a disjoint embedded link. The critical limiting cases are `t=0`, arbitrary nonreal parameters, the edge of the parameter disk, and intersections where three total-space components meet.

## Factorization, directions, and completeness of singularities

The products of the three factor groups are exactly the three displayed cubic factors. For example, with `z=x+2y-t`, the `b` product is `z³+64y³=64y³-(t-x-2y)³`. The `c` product is `(t-x-2y)³-64x³`. Thus there is no discarded scalar, vanishing parameter factor, or restriction to `t ≠ 0` in the factorization. The coefficient of `x⁹` is `-65` for every parameter.

Independently in projective coordinates, the groups `X=w^iY`, `Y=w^jZ`, `Z=w^kX` meet at the three coordinate vertices and the nine points

\[
[\,w^{i+j}:w^j:1\,].
\]

Exactly one line from each group passes through each of the latter points, namely indices `i,j,-i-j`. Distinct pairs `(i,j)` give distinct points. No coordinate vertex lies on a line from another group. This exhausts the 36 line pairs in twelve groups of three. Distinct projective lines have distinct local tangent directions at their intersection; all twelve points are ordinary triple points.

The infinity `X+2Y+4Z=0` avoids coordinate vertices. At the other nine points its absolute value is at least `4-2-1=1`. Therefore every pair intersection is affine and no two affine lines are parallel. Their nine distinct spatial directions remain distinct when all their intercepts become zero at `t=0`. Consequently every fiber is a union of nine distinct reduced lines; at zero it has exactly one ordinary ninefold singularity. For nonzero complex `t`, multiplication by `t` is an affine complex isomorphism, so it preserves the complete incidence list. Complex phases create no extra case.

The independent exact controls in `boundary_controls.py` work in `Q[w]/(w²+w+1)`. They verify the full factorization, all 36 nonzero spatial-direction determinants, all twelve intersections and their three-line incidences, and the exact Euclidean geometry used below. They do not import the candidate checker.

## Polynomial and holomorphic flatness

The monic polynomial `-F/65` gives a free `C[y,t]`-module with basis `1,x,...,x⁸`. Since `C[y,t]` is free over `C[t]`, its quotient ring is flat over the polynomial parameter line. This is an actual module argument, not a numerical inference from delta.

Here is a separate direct analytic argument, avoiding any dependence on a total-space normality or UFD assertion. At an arbitrary point over `t=t0`, translate the parameter to `s=t-t0`. Let

\[
A=\mathbb C\{x-x_0,y-y_0,s\},\qquad M=A/(F).
\]

If `s g=F h` in `A`, reduction modulo `s` gives

\[
0=\overline F\,\overline h\quad\text{in }\mathbb C\{x-x_0,y-y_0\}.
\]

This ring is a domain, and `F(x,y,t0)` is a nonzero germ: it is a polynomial in `x` with constant nonzero leading coefficient `-65`. Hence `h=s h1`; cancellation in the ambient power-series domain gives `g=F h1`. Multiplication by `s` on `M` is injective. Every nonzero germ in `C{s}` is a unit times a power of `s`, so `M` is torsion-free over `C{s}`. A torsion-free module over a DVR is flat: its finitely generated submodules are free and it is their directed union. This proves analytic flatness at every point, including component intersections and `t=0`.

Restriction to the open ball changes none of these local rings. The argument does not require the open-ball projection to be proper.

## Total-space normality and the finite normalization

The total space `X={F=0}` is reduced but **not normal** at points where components meet. For `t ≠ 0`, its singular/non-normal locus consists locally of triple intersections along twelve distinct lines in the three-dimensional total space; these lines meet at the origin. No part of the proof requires `X` itself to be normal.

Each total-space component `Hi={ell_i=0}` is a smooth plane. Its `x` coefficient is nonzero, so `(y,t)` are global algebraic coordinates on it and its map to the base is smooth. For

\[
R=\mathbb C[x,y,t]/(F),\qquad S=\prod_{i=1}^{9}\mathbb C[x,y,t]/(\ell_i),
\]

the map `R→S` is injective: the intersection of these distinct principal prime ideals is their product. This follows successively from primality and nonassociation; an appeal to irreducibility of the total space would be incorrect. `S` is a finite `R`-module because it is a finite product of cyclic quotient modules. Its total fraction ring is the product of the nine component fraction fields. The polynomial rings of the planes are integrally closed, so `S` is integrally closed in that product. Any element integral over `R` is also integral over `S`, since the same monic equation has coefficients in `S`; hence it lies in `S`. Conversely every element of `S` is integral over `R` by finiteness. Thus `S` is precisely the integral closure of `R`.

The same local proof applies analytically: the prime factor ideals define smooth plane germs, their product is the family equation, and the component local rings are normal smooth analytic local rings. This uses the foundational normality of a smooth complex space, not a delta-constant or simultaneous-normalization theorem. The finite union of the closed component inclusions is the analytic normalization.

Specialization must be checked separately; normalization does not in general commute with base change. Here

\[
S/(t-t_0)S=\prod_i\mathbb C[x,y]/(\ell_i(x,y,t_0))
\]

is the disjoint union of nine distinct smooth lines for **every** `t0`, including zero. The same integral-closure argument on the fiber proves it is that fiber's normalization. The induced normalizations are finite and the normalized total family is smooth over the base. There is no hidden identification of the nine central disks and no assumption of an irreducible special fiber.

## One uniform ball: singularity bounds and disk geometry

Write `B°={|x|²+|y|²<1}`, `Bbar={|x|²+|y|²≤1}`, and `Delta={|t|<1/4}`. Use the complex analytic space `X°=X∩(B°×Delta)` for holomorphic assertions and its closed-ball closure for boundary assertions.

At `t=1`, the three vertex coordinates are `(0,0),(1,0),(0,1/2)`. For the other nine points, both numerators have modulus one and the possible denominator squared norms are

\[
49,31,31,19,19,13,13,7,7.
\]

Their spatial squared norms are therefore `2` divided by those values. All twelve affine singular points have norm at most one. Thus the sharper uniform estimate

\[
\|p(t)\|\le |t|\le1/4
\]

holds even on the closed parameter disk. In particular, all pair intersections stay well inside the radius-`1/2` ball. The weaker bound in the candidate is already sufficient and correct.

For any one component write its equation `a x+b y+c t=0`, and set

\[
N=|a|^2+|b|^2,\quad
p(t)=-\frac{ct}{N}(\bar a,\bar b),\quad
v=\frac{(-b,a)}{\sqrt N}.
\]

Then `p(t)` is the closest point on the line, `v` is a fixed unit direction orthogonal to it, and every point of the line is uniquely `p(t)+zv`. Exactly,

\[
\|p(t)+zv\|^2=\frac{|ct|^2}{N}+|z|^2.
\]

For the `A` lines the distance coefficient `|c|²/N` is zero. For `B0,B1,B2` it is `1/37,1/13,1/13`; for `C0,C1,C2` it is `1/29,1/17,1/17`. Hence for all complex `|t|≤1/4`, every line cuts the closed unit ball in a genuine closed disk with boundary-circle radius squared at least `207/208`.

The restricted normalized total family consequently has the explicit smooth disk trivialization

\[
(t,z)\longmapsto\left(p(t)+\sqrt{1-|ct|^2/N}\,zv,t\right),\qquad |z|\le1.
\]

This map is smooth in both real coordinates of the complex parameter. It is a smooth trivialization of manifolds with boundary, not a claimed holomorphic trivialization of round disks. The corresponding open normalized fibers are open disks. Every restricted fiber has exactly nine normalization components, all with topological genus zero.

## Transversality, boundary isotopy, and properness

On each component the squared radius is `d(t)²+|z|²`, whose differential in the radial `z` direction is nonzero at the boundary because `|z|²≥207/208`. Thus transversality is uniform. Since every intersection of different components lies inside radius `1/2`, their boundary circles are disjoint. This last check is essential: individual component transversality alone would not prove transversality of the reduced union.

Explicitly, the boundary embeddings are

\[
f_i(t,e^{i\theta})=p_i(t)+\sqrt{1-d_i(t)^2}\,e^{i\theta}v_i.
\]

They give a smooth family of embeddings of nine labeled circles into the fixed unit sphere. Along a smooth parameter path they are an isotopy of embedded links. Uniform pairwise disjointness on the compact closed parameter disk also follows from the intersection bound and compactness. If ambient isotopy is desired, along any path extend the displayed link velocity to a vector field on disjoint tubular neighborhoods in the sphere, multiply by a cutoff, and integrate the resulting smooth vector field on the compact sphere. This constructs the usual ambient isotopy and does not assume constancy of the link beforehand.

At zero the curve is a union of nine complex lines through the origin. Positive real radial scaling gives the same link on every smaller centered sphere. Thus the unit-ball representative is local for this homogeneous central singularity. The homogeneous identity `F(rho x,rho y,rho t)=rho⁹F(x,y,t)` permits arbitrarily small ball and parameter radii with the same ratio.

There are three distinct properness statements:

1. The finite normalization map is proper, globally and after restriction by the inverse image of the open-ball target. Noncompactness of the target does not invalidate properness of a finite map.
2. The projection `X°→Delta` of the open-ball analytic representative is **not** proper; its nonempty disk fibers are noncompact. Flatness does not require it.
3. The closed-ball closure projects properly to `Delta` as a map of topological spaces: the inverse image of a compact parameter set is closed in `Bbar×K`, hence compact. The same holds for its normalization with boundary. Closed balls are not complex analytic spaces, so analytic flatness is assigned to the open representative.

The candidate already explicitly makes the open/closed distinction. Adding these three statements would improve clarity but is not needed to repair its proof.

## Delta, rough invariant, and topology consistency

For smooth transverse line branches the delta additivity sequence gives one unit for each unordered pair. The central value is `choose(9,2)=36`, and the twelve triples give `12 choose(3,2)=36`. This is constant total delta in the fixed representative; it is not delta along the marked origin alone. The origin remains one of the triple points in a nonzero fiber.

For an ordinary `r≥3` point, one blowup is a minimal embedded resolution, the exceptional curve has square `-1`, and `r` strict transforms meet it at distinct points. Adjunction gives the exceptional local canonical divisor `K=E`, and therefore `K·(K+D)=E·(C'+2E)=r-2`. This yields `7<12`. The local-resolution family should independently audit invariant conventions; the construction gate itself is independent of them.

There is no contradiction between constant delta and a changed first Betti number of the singular fiber. Nine disks identified at twelve triple points have Euler characteristic `9-12(3-1)=-15`; their incidence pattern is connected, so the nearby singular curve has first Betti number 16. The central union is contractible. The local Milnor sums change from 64 to 48, consistently by 16. These are consistency checks, not an assumption that the singular fibers themselves are topologically trivial.

## Falsification attempts and edge cases

| Attack | Result and exact reason |
|---|---|
| A factor repeats or vanishes at special parameter | No: the 36 spatial determinants are nonzero independently of `t`; no factor is proportional to a parameter factor. |
| Clearing denominators secretly introduces `t=0` multiplicity | No: exact factorization has nine distinct linear total-space and central-fiber factors; `x⁹` coefficient is `-65`. |
| Analytic flatness fails at a triple locus or at the ninefold origin | No: the direct `s`-torsion cancellation proof holds in every ambient convergent local ring. |
| Smooth total components fail to give the total-space normalization | No: explicit finite integral-closure computation in the total fraction product proves it. |
| Normalization fails after specialization | No: special fibers are explicitly the disjoint nine smooth distinct lines. |
| An intersection escapes or a component disappears for nonreal parameters | No: scaling is complex linear; the bounds depend only on `|t|`, and each line distance is uniformly less than one. |
| Individual transversality hides a singular boundary union | No in the stated disk: all pair intersections have norm ≤1/4. Negative control at `t=1` detects the failure outside that disk: the three individually transverse `B` lines collide at `(1,0)` on the sphere. |
| Parameter restriction is inessential | False: for `B1`, `d(t)²=|t|²/13`, so `|t|²=13` produces tangency and a collapsed boundary circle. The exact control detects it. |
| Nine normalization disks conceal a lost branch or changing genus | No: each of the nine factors cuts a genuine disk; the explicit normalized disk bundle includes `t=0`. |
| Ball closure is implicitly treated as a complex analytic space | No: section 6 states the open-ball analytic convention. Properness clarification is optional. |
| Numerical checks are mistaken for a proof for all complex `t` | No: universal bounds and algebraic identities are written above. The exact code supplements them. |
| General Fermat extension uses an unsupported finite-range extrapolation | No: the root-of-unity incidence mechanism works for every integer `n≥3`; the same infinity estimate and line-distance bounds apply. The central multiplicity is `3n`; total delta is `3 choose(n,2)+3n²=choose(3n,2)`, and rough excess is `n²-4`. Values `n<3` are outside the asserted extension. |

The control suite refuses Python optimization because its checks use assertions. An actual `-O` invocation was verified to fail before printing any PASS output. A second ordinary run reproduced `boundary_results.json` byte-for-byte.

## Primary-source authentication used in this audit

Complete primary PDF bodies, rather than search snippets, were retrieved from the publisher/institution and kept in ignored `private_sources/`. Complete relevant pages were read visually in addition to text extraction. Public source metadata and body hashes are in `SOURCE_RECORDS.json`; no PDF body, extract, or rendered source page appears in the public manifest.

The [OWR report](https://ems.press/content/serial-article-files/46242?nt=1), printed pp. 2446–2448, defines the displayed rough intersection invariant. Its deformation setup on p. 2447 uses a fixed transverse ball, a central local link, and multiple nearby singular points. The claimed construction satisfies those geometric conditions directly. The questions themselves do not explicitly impose irreducibility; this observation alone is not treated here as a complete target-binding verdict.

The [published Osaka paper](https://ir.library.osaka-u.ac.jp/repo/ouka/all/50809/ojm51_03_573.pdf), Section 2 and Definition 2.1, specifies flatness, transversality, and locality, then distinguishes rational from unibranched and parametric deformations. The nine-disk construction is rational in that definition and fails its unibranched condition. The paper's parametric conjecture therefore remains outside this audit's positive result.

No external theorem about delta-constant equinormalization, link constancy, or generic properness was invoked to supply a missing construction step. The proofs use elementary module algebra, explicit component integral closures, the standard normality of smooth analytic local rings, and the explicit link parametrization.

## Required and optional corrections; exact remaining gap

Required corrections in this family's scope: **none**.

Optional clarifications: explicitly state that the original reducible total space is nonnormal while its component normalization is smooth; spell out which projection is proper; give the displayed link/disk formulas if a more constructive isotopy argument is useful. The existing proof is already sufficient without these additions.

The strongest verified result is the complete multibranch delta-constant construction with the stated local representative and numerical rough-invariant jump. The remaining work lies outside this family's gate: independent target/invariant-binding decisions, independent computation-package assessment, any priority/novelty audit, and review of any later rewritten release package. No claim of having completed those gates is made here. No external contact, Git mutation, PR write, release, or original-file repair was performed.
