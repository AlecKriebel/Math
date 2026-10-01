# Round 1 independent targeted mathematical falsification

Reviewer task: `round1_math_falsifier`. Started 2026-10-01 03:56:03 UTC.

## Scope and independence

This review reads the manuscript `paper.tex` and the two supplied primary-source PDFs only. It does not read prior verdicts, initial review reports, the parent review, canonical verification scripts, or their outputs. All scratch material is confined to `tmp/round1/math_falsifier/`. No canonical source edits, branches, commits, pushes, releases, publication, or external contact are performed.

The finite review goal is to try to falsify Theorems 1 and 4 and their supporting mechanisms, then provide independent checkable reasoning and any actionable proof defects. Completion estimates below refer to this finite review, not to a probability that the theorem is true.

## Research log

- 2026-10-01 03:56:03 UTC — 0% complete. Began a fresh proof-first read without consulting earlier reviews.
- 2026-10-01 03:58:48 UTC — 45% complete. Re-derived the support face formula, analytic-image prime-ideal argument, and general-position transpose-surjectivity mechanism. Extracted the two primary sources; their definitions and conjecture statements match the manuscript targets. No counterexample or proof defect found in this first pass. Exact adversarial constructions and source-page inspection remain.
- 2026-10-01 04:02:05 UTC — 85% complete. Visually checked GM2022 pp. 146, 149, 167 and Meroni2023 p. 830. A fresh dependency-free exact script passed 30 GP subset-rank checks across six block types, a nonorthogonal R^5 perturbation with two annihilated blocks, and exact polynomial reduction of the nongeneric separator. Checked rank-one and lower-dimensional repeated-disc boundary cases. No actionable mathematical defect found. Final synthesis and consistency check remain.
- 2026-10-01 04:05:04 UTC — 100% complete. Finished the independent report and checked its numerical, source, and claim descriptions against the fresh outputs and reviewed source files. At the parent's request, copied the independently created exact script and its results into this review folder so the final report has public, preserved verification artifacts. Final verdict: no actionable mathematical proof defect found in the stated Theorems 1 and 4.

Reviewed file identities (SHA-256):

- `paper.tex`: `3576dcc78bf1a9188ee8a8b5c56f5914357d90d437767e29dc42e3a85ceedab4`.
- `geometry_discotopes_publisher_2022.pdf`: `76d7033365db98c4cc4ce166aaa5bda2b1aaa25d5ba3386d3d66651a849c9adb`.
- `owr_2023_15.pdf`: `32c4fbd8b25f445613300ed0a00ba2082d653a154a3b2f64734f19c678d351ff`.

## Verdict

**No actionable mathematical proof defect found.** The finite proof arguments for Theorems 1 and 4 survive the targeted falsification attempts below. No correction to `paper.tex` is requested by this review.

This is an independent mathematical audit with checkable reasoning and finite corroborating calculations. It is neither formal proof certification nor human peer review, and it does not establish historical priority or conclusions about the entire complex critical locus.

## Exact claims and success criteria

- Theorem 1: for a finite nonempty Minkowski sum of origin-centered ellipsoidal balls, each of intrinsic dimension at least two, the complex Zariski closure of its exposed points is irreducible. The claim includes repeated summands, coincident spans, rank-deficient total spans, and dependent support radicals.
- Theorem 4: if the sum is full-dimensional and the spans satisfy (GP) for every index subset, then the complex Zariski closures of exposed points and of `D^partial intersect boundary(D)` coincide.
- A falsification would be a qualifying discotope with reducible exposed-point closure; a qualifying GP boundary representation outside that closure; or a failure in the connectedness, analytic identity, exact face, transpose, or generic-witness deductions. Merely finding a reducible larger complex incidence/critical variety would not falsify either stated theorem.

## 1. Complex analytic-image irreducibility

Target: `paper.tex` lines 109–130.

I tried to exploit complex coefficients, real rather than holomorphic analyticity, intersections of algebraic components, and a noninjective parametrization. None produces a gap.

Independently, let `I` be the complex polynomials vanishing on `F(U)`. If `PQ` vanishes there and `P` does not, continuity gives a nonempty real open set on which `P(F(u))` is nonzero. Pointwise complex multiplication then forces `Q(F(u))=0` on that set. Both real and imaginary parts of `Q composed with F` are real analytic. A real analytic function on a connected open set that vanishes on a nonempty open subset vanishes everywhere. Thus `Q` belongs to `I`, and `I` is a proper prime ideal.

The passage to the complex Zariski closure is legitimate: a polynomial vanishes on `F(U)` exactly when its closed zero set contains that closure. This identifies the two vanishing ideals directly. A proper prime vanishing ideal defines an irreducible complex algebraic set. No statement about a complex square-root branch, a complexification of `U`, algebraicity of `F`, or the differential rank of `F` is needed.

The manuscript's short proof of analytic uniqueness is also valid. At a limit of points where the function vanishes locally, every derivative vanishes by continuity. The convergent Taylor expansion at the limit is therefore zero on a neighborhood. The set of local-vanishing points is both open and relatively closed in connected `U`.

Attempted failure when analyticity is weakened is real: the smooth map `(g(-t),g(t))`, with `g(t)=exp(-1/t^2)` for `t>0` and `g(t)=0` otherwise, maps the connected real line into two different coordinate axes and has reducible Zariski closure. The function is not analytic at zero. This supports the exact analytic hypothesis used here; it is not a counterexample to the lemma.

Status: verified by an independent prime-ideal argument. Remaining mathematical gap: none identified within the stated hypotheses.

## 2. Path connectivity of the normal domain

Target: `paper.tex` lines 93–107 and 155–166.

For `x` outside each forbidden subspace `M_i`, a segment from `x` to `z` can meet `M_i` only if `z` lies in `M_i + R x`: solving `(1-t)x+tz in M_i` for `z` gives this containment for every `t>0`. Since `codim(M_i)>=2`, adding one line leaves `M_i + R x` proper. The same applies to `y`. A point `z` outside the finite union of these proper subspaces therefore provides two safe segments. The finite-union existence argument uses the nonzero product of real nonzero linear forms and the fact that a nonzero real polynomial cannot vanish at every real point.

I tested the antipodal obstruction (`y=-x`) with the smallest admissible case `R^2 minus {0}`. The intermediate point is selected off their common line, so the two segments avoid zero. The construction also handles coincident kernels, a common positive-dimensional kernel, and full-rank summands (whose forbidden kernel is `{0}`). For an intrinsic rank `m_i`, `ker(A_i^T)` has codimension exactly `m_i`, independently of the dimension of the total sum. Thus reducing the total span does not invalidate connectedness.

Status: verified. Remaining gap: none. The codimension-two hypothesis has a concrete boundary failure at rank one, detailed in section 6.

## 3. Exact exposed faces and support parametrization

Target: `paper.tex` lines 132–167.

An intrinsic-rank injective representation always exists. For an initially noninjective ball map, singular-value decomposition followed by projection of the original unit ball onto its nonzero singular directions produces the intrinsic-dimensional unit ball, so the manuscript does not inadvertently alter a disc.

For an injective `A_i`, maximizing `u dot A_i v` over `||v||<=1` is maximizing `(A_i^T u) dot v`. A nonzero coefficient gives the unique unit vector `v=A_i^T u / ||A_i^T u||` by equality in Cauchy–Schwarz. A zero coefficient makes the whole positive-dimensional disc maximize. Mapping the unit sphere by this injective map gives precisely the relative boundary.

I tried to make a nonsingleton summand face disappear through cancellation in the Minkowski sum. This is impossible because choices in a Minkowski sum are independent: fix one point in every other face; the resulting translate of the nonsingleton face remains a nonsingleton subset of the sum face. Conversely singleton faces sum to a singleton. Equality of total support value and linear value is equivalent to equality in every nonnegative support deficit. This proves both the sum-of-faces identity and the exact equality `Exp(D)=F(U)`.

There is no ambient-interior hypothesis in this step. Even a lower-dimensional compact sum has exposed points defined by nonzero ambient linear functionals, and precisely the normals in `U` expose singleton faces. The origin lies in every forbidden kernel and is excluded because the sum is nonempty.

Status: verified. Remaining gap: none.

## 4. GP perturbation and simultaneous boundary choices

Target: `paper.tex` lines 177–221.

The potentially strongest hidden-assumption test was whether different boundary choices on several annihilated discs can be recovered by one perturbation, especially when their bases are not orthonormal.

If `J` is the set of annihilated discs, all their spans lie in the proper hyperplane `u^perp`. If their dimension sum were at least `d`, (GP) would force their span sum to have dimension `d`, a contradiction. Their dimension sum is therefore at most `d-1`, and (GP) now forces exact additivity of dimension. Equivalently, the concatenated column map `A_J` is injective. With Euclidean transpose, `rank(A_J^T)=rank(A_J)` equals its target dimension, so `A_J^T` is surjective. This remains true for arbitrary full-rank, nonorthonormal shape matrices.

The equation to solve is exactly `A_j^T w=v_j`, where `x_j=A_j v_j` and `||v_j||=1`. It is not the superficially similar equation `Q_j w=x_j`. Using the former, `A_j^T(u+epsilon w)=epsilon v_j`, and for every positive epsilon the support point is exactly `A_j v_j=x_j`. Negative epsilon would change the sign; the proof explicitly takes positive epsilon. On a nonannihilated block the coefficient begins nonzero and stays so for sufficiently small epsilon. A finite minimum of the individual bounds suffices. The perturbation is itself nonzero since at least one annihilated block evaluates to a nonzero vector. If `J` is empty, the original normal already belongs to `U`.

Full dimensionality is used appropriately: a generator `x` on the boundary of the compact convex body has a nonzero supporting normal. Every summand in any specified boundary representation must maximize that normal because its nonnegative support deficit contributes to a sum of zero. Every exposed point lies on the ambient boundary under this same full-dimensionality hypothesis. Finally, the complex algebraic set `E(D)` is Euclidean closed; inclusion of every Euclidean limit generator implies inclusion of its Zariski closure. The direction of this closure argument is correct.

**Independent exact stress test.** Let `c(t)=(1,t,t^2,t^3,t^4)^T` in `R^5` and take blocks `(c(0),c(1))`, `(c(2),c(3))`, `(c(4),c(5))`. All subset ranks satisfy (GP). Use

`u=(0,-6,11,-6,1)`,

so the six column evaluations are `(0,0,0,0,24,120)`. Prescribe arbitrary different unit choices `v_1=(3/5,4/5)` and `v_2=(-5/13,12/13)`. Exact rational elimination gives

`w=(3/5,142/65,-171/65,42/65,0)`.

The first four column evaluations of `w` are exactly the prescribed vector entries; the last two are `(43/5,1724/65)`. Thus the third block remains nonzero for every positive epsilon, while the first two support points equal the prescribed choices exactly. Numerical evaluation of only the remaining normalized vector gives successive full-point errors approximately `0.3450`, `0.03541`, `0.003550`, `0.0003551` for epsilon `1/10`, `1/100`, `1/1000`, `1/10000`. The exact identities and general continuity proof, rather than these numerics, establish convergence.

Status: verified. Remaining gap: none. The failure of surjectivity in coincident spans is real and explains why the theorem includes (GP).

## 5. Generic parameter-space witness and primary target match

Target: `paper.tex` lines 223–234.

For each index subset, failure of the required concatenated rank is the common zero set of its maximal minors. There are finitely many subsets, so their union is Zariski closed. Each block's full rank is included in the same reasoning. For distinct real `t` values, any `k<=d` Vandermonde columns have a nonsingular `k by k` minor in the first `k` rows; its determinant is a product of their nonzero pairwise differences. More than `d` columns contain a nonsingular `d`-column subset. Partitioning all columns into the required block sizes therefore supplies a simultaneous real witness for every subset, for every specified `m_i<=d`. This is stronger than merely demonstrating a witness separately for each subset.

The finite script independently checked every nonempty subset in six types: `(d;sizes)=(2;2,2)`, `(4;2,2)`, `(5;2,2,2)`, `(6;2,3,4)`, `(7;2,2)`, `(6;6,2,3)`, totaling 30 exact rank checks. These include rank sums below, equal to, and above the ambient dimension and a full-dimensional summand. They corroborate, and do not replace, the general Vandermonde argument.

The primary sources were checked from both extracted text and rendered pages. GM2022 p. 146 parametrizes discs by linearly independent basis vectors and defines genericity in that parameter space; p. 147 assumes the total sum is full-dimensional after restriction to its span. Definition 3.3 on p. 149 defines the closure of sums of relative disc-boundary points that lie on the sum boundary. Conjecture 8.2 on p. 167 asks for irreducibility of that `S` for generic types without one-dimensional summands. Meroni2023 p. 830 defines the exposed-point closure `E` and Conjecture 1 asks its irreducibility under intrinsic ranks at least two. The manuscript's two-target distinction is accurate; the primary sources do not justify identifying `S` and `E` in every nongeneric configuration.

Status: verified. Remaining gap: none in the sufficiency of the stated open condition or in its coverage of feasible generic full-dimensional types. This review does not assert the exact failure locus of irreducibility itself is closed, nor is that needed for the usual assertion that the property holds outside a proper algebraic exceptional set.

## 6. Boundary attempts: repeated, lower-dimensional, rank-one, nongeneric

**Repeated lower-dimensional rank-two discs.** Two identical unit discs in the first coordinate plane of `R^5` sum to the radius-two disc in that plane. The excluded common kernel has codimension two; the exposed-point closure is

`X_1^2+X_2^2=4`, `X_3=X_4=X_5=0`.

Over `C`, the substitution `s=X_1+iX_2`, `t=X_1-iX_2` identifies its coordinate ring with `C[s,t]/(st-4)`, an integral domain. Thus repeated radicals and a three-dimensional common kernel produce an explicit irreducible boundary case, not a counterexample. Coincident spans with different ellipsoidal shapes retain the same codimension-two kernel and analytic positive-radical formula; the proof uses no radical independence.

**Rank-one obstruction.** For the interval, the support map on `R minus {0}` gives two points and a reducible closure. For a unit disc plus `[-a,a]e_1`, the rank-one summand removes the normal line `u_1=0`. The two resulting components map to the open semicircles of centers `a e_1` and `-a e_1`. Each arc is Zariski dense in its nonsingular complex conic, and the conics are distinct for `a>0`. Their union is reducible. This tests the exact threshold excluded from Theorem 1; it does not invalidate the stated theorem.

**Nongeneric separator.** For two identical `xy` unit discs and one `xz` unit disc, the boundary representation `e_3=e_1+(-e_1)+e_3` is valid. The normal `e_3` has face `2B_xy+e_3`, hence this point is in the generating set for `S`. Simultaneous transpose prescriptions for the coincident first two discs are incompatible when their unit choices are `e_1` and `-e_1`, showing exactly where the GP perturbation mechanism fails.

For a regular support normal, set `a=2u_1/r`, `b=u_1/s`, `Y=2u_2/r`, `Z=u_3/s` and `X=a+b`. Then `a^2+Y^2=4` and `b^2+Z^2=1`; consequently `X^2+Y^2+Z^2-5=2ab`. The manuscript's polynomial reduces identically to zero modulo these two relations. The fresh dependency-free polynomial computation performs that reduction exactly with rational coefficients and obtains the zero remainder. It also obtains `P(0,0,1)=16` exactly and checks three independently chosen regular support points. Since `P` vanishes on the exact exposed image, its zero set contains the entire complex Zariski closure. Thus `e_3` is separated algebraically, rather than just from a specific real parametrization branch. Extra branches in the zero set of `P`, if any, would not affect this one-way inclusion argument.

Status: all stated examples verified; they impose the advertised boundaries on the conclusions. Remaining gap: none identified.

## Checkable artifacts and limitations

The preserved independent script [math_falsifier_exact_checks.py](math_falsifier_exact_checks.py) uses only the Python standard library (`fractions`, `itertools`, `math`, `json`). It creates all its matrices and polynomial expressions from scratch, without reading canonical verification code or prior outcomes. Its saved output is [math_falsifier_exact_results.json](math_falsifier_exact_results.json). Run `python3 reviews/round1/math_falsifier_exact_checks.py` from the research folder to reproduce the output. All assertions passed. Exact rational calculations establish the matrix ranks, transpose identities, separator remainder, and separator value; floating-point numbers are used only to illustrate convergence already proved by continuity. The preserved files were copied unchanged from this review's isolated scratch folder.

The research mechanism families checked here are: analytic/algebraic closure; convex faces and intrinsic rank; linear dual perturbation and parameter genericity; and explicit edge constructions and exact elimination. Each surviving route has its supporting deduction above. No route transfers a central proof obligation to an unsupported stronger statement, and no unresolved mathematical gap within the stated two theorems was found.

This report assesses these finite mathematical claims and their primary-source alignment. It does not re-audit packaging, publication state, source priority beyond the two provided target PDFs, LaTeX compilation, AI provenance, or the manuscript's full bibliographic history.
