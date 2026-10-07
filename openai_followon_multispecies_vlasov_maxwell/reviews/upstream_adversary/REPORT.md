# Fresh adversarial audit of the family 362 analytical mechanism

Timestamp: 2026-10-07T04:33:35Z (2026-10-06 in the user's time zone).

This is a meaningful-checkpoint audit of the original global classical
relativistic Vlasov–Maxwell target and its proposed upstream mechanism. It is
not a review of a complete multispecies manuscript or publication package.
No external individual was contacted. The source clone was not changed.

## Exact material inspected

Read the actual family 362 manuscript sources under
`sources/upstream_pinned/preprints/Global-classical-solutions-of-the-three-dimensional-relativistic-Vlasov-Maxwell-system-September-23-2026/build/`:
`sections/introduction.tex`, `setup.tex`, `retarded.tex`, `occupation.tex`,
`direct.tex`, `cancellation.tex`, `direction.tex`, `selection.tex`,
`closure.tex`, and `continuation.tex`. Read `lean/docs/362.md` to distinguish
its stated formalization scope from this paper audit. I did not reproduce a
Lean build or audit all actual Lean dependencies; no formal verification
claim follows from this review.

The seven pivotal central source hashes are:

| Source | SHA-256 |
| --- | --- |
| retarded.tex | eedf365c0be2cefacecc93c2825b4991ccad1d32826d83aa24eb4b63ccf37be2 |
| occupation.tex | c9bd0387061b620018c710dd9f660564adf8c38ff2385ee134923f86bf8d3307 |
| direct.tex | aed0cd43a04c66b5ffb4bb30de2377dafa1eaa58a6c5e7d0c40865662f9e6de1 |
| cancellation.tex | 6b615a3b4ba0fbb6d04ea2e88b441dabdd51f6b33fc976b23407413fc9ae162a |
| direction.tex | aeab95505df9a9d2b8bca153832ea69039eb0fa078788775ea15e34fb8531432 |
| selection.tex | 1ece8e662bff978906fbc1ddc578ea09a89322accee598d043aa3a7403583445 |
| closure.tex | 499230223647c95c6e9d536c78e9cd5dd098a011d9213b733daaab3d8bba8e89 |

## Verdict and strongest checked conclusions

I found no concrete counterexample or substantive analytical gap in the
central occupation/direct/cancellation/direction/selection/closure chain
after independently reading those sources. This is qualified positive
evidence, not certification of the complete upstream theorem or the new
target. The strongest independently checked artifact is the exact signed
kernel identity for arbitrary independent source and receiver
accelerations. A second exact arithmetic check validates the numerical
exponent margins used to rule out unsafe selected bins.

Run `python reviews/upstream_adversary/check_kernel.py` from the project
root. It uses SymPy 1.14.0. The output is:

```
Signed kernel identity residuals: [0, 0, 0]
Identity holds for arbitrary independent source and receiver accelerations.
Exact exponent margins: {'Delta/z': 4/99995, 'H/z upper': 378/935}
```

The symbolic artifact checks an identity, not inequalities, integrability,
solution existence, or all parameter bounds. Those were inspected
analytically as described below.

## Falsification attempts and their results

1. **Source/receiver coupling hidden in the signed identity.**
   `cancellation.tex:49–102` defines the exact identity. I independently
   differentiate its primitive `k0/(r d)` in the symbolic check, allowing
   `u'=b` and `a_t=c` to be arbitrary independent three-vectors. Its residual
   vanishes exactly. The identity uses only the retarded geometric relations,
   `q^{-2}=1-|u|^2`, and `q_X^{-2}=1-|a|^2`. It does not require equal
   accelerations, equal charge signs, or equality of source and receiver
   charge-to-mass ratios.

2. **Cone cap and occupation errors.**
   `occupation.tex:64–122` uses deficit-including angular coordinates.
   The spherical cap bounds follow from the exact Euclidean identities in
   lines 66–71; the inverse-momentum deficits rule out arbitrarily small
   bins at fixed energy. The stable-cell proof in lines 262–300 compares
   source and receiver velocities at the same time only after both are
   controlled over the separation `O(h) <= O(lambda)`. The fixed common-time
   label mass bound uses positive kinetic energy, not signed charge density.
   The joint energy budget in lines 302–416 is shared across `theta,h`, which
   avoids an extra logarithm in the small sector.

3. **Changing projection loses its longitudinal term.**
   `direction.tex:94–102` displays the full derivative of
   `Pi=w(Id-xi⊗xi)/|V_X|`. Its `Pi_t k0` estimate retains the longitudinal
   part of `k0` and costs `theta |K|/(w phi)`. The paper does not replace
   `|k0|` by the smaller transverse bound in this term. The resulting
   coefficient is `O(L^2/w)` at lines 105–123, allowing the baseline
   absolute-force bound to produce `O(w^{1/2} L^3)` without a direction-cell
   count.

4. **Circular direction/occupation improvement.**
   The direction estimate (`direction.tex:22–209`) uses baseline occupation
   and direct estimates only. It does not use the intermediate-angle
   occupation improvement (`direction.tex:222–371`). Its only assumption is
   the common signed bootstrap already being improved. Consequently the
   dependence chain is conditional bootstrap → stable occupation → direct
   bounds → direction counts → improved occupation → selected coefficient
   → strict signed improvement. I found no return edge importing the
   improved occupation estimate into its own direction-count proof.

5. **Exponent window or boundary error.**
   `selection.tex:130–270` first forces an unsafe selected bin into the
   actual regime using only the pure energy bound. Actual occupancy then
   forces it into the improved-occupation window. I independently checked
   the rearrangements. In particular `Delta/z < 4/99995 < 0.001`;
   improved far selection plus the unsafe near coefficient imply
   `beta*y > H/3 + 0.33*z`, while near selection implies
   `beta*y < 0.582*z - 0.29*H`. Hence `H/z < 378/935 < 0.41`, contradicting
   the earlier `H/z > 0.496`. All margins are strict and rational, with
   `beta=29/25`. Constants depending on bootstrap parameters are absorbed
   only after `z>0.66`; this supplies a uniform positive exponent.

6. **Extra logarithm at the spatial transition.**
   `selection.tex:314–394` does not independently count all `theta` bins.
   The radial crossing bound reduces to `D0` times a function of
   `x=n0/D0`, with a positive power for `x<=1` and `x^{-1}` for `x>=1`.
   Since `n0` is proportional to `theta^gamma` with `gamma>0`, both tails
   are geometric. The retained joint budget across `p,phi` then gives the
   claimed scale. The cutoff derivative assignment first factors out a
   common physical multiplier (`cancellation.tex:138–169`) and uses fixed
   neighboring indices. It does not differentiate the discrete selection.

7. **Bootstrap closure is only pointwise or nonuniform.**
   `closure.tex:1–87` restores endpoints using signed bootstrap increments,
   not absolute force. The choices are ordered: fixed ramp fraction, then
   `M`, then `A`, then a sufficiently large `P0`. The finite compact-time
   force bound appears only in the openness argument for fixed `P`; it does
   not enter `M,A,P0`. The momentum-doubling proof in `setup.tex:77–117`
   therefore retains a lower bound of order `1/log P`, whose dyadic series
   diverges.

## Consequences for finite species, including opposite signs

For physical momentum `p_phys=m_b v`, define normalized density
`f_b(t,x,v)=m_b^3 F_b(t,x,m_b v)`. Then number density is `∫f_b dv`,
velocity is `u(v)=v/sqrt(1+|v|^2)`, normalized acceleration is
`V_b'=(e_b/m_b)(E+u_b×B)`, and positive kinetic energy is
`sum_b m_b ∫ q f_b dx dv`.

For receiver species `a` and source species `b`, the retarded interior
force contribution is multiplied by the fixed scalar
`c_ab=(e_a/m_a)e_b`. Source velocity acceleration inside the kernel is
`b_b=u_b'`, which itself includes `e_b/m_b`. The exact symbolic identity
above applies with that acceleration; it is invalid to pull a second
species coefficient outside the geometric total derivative or to assume
source and receiver charge-to-mass ratios are equal. The correct pairwise
identity is simply `c_ab` times the geometric identity evaluated on the
actual two trajectories.

Use a finite disjoint union of species label spaces, not the assertion
that `sum_b f_b` solves a one-species Vlasov equation. Phase volume is
preserved within each species. Each label mass and cone-flux budget is
controlled by the positive weighted energy, with constants allowed to
depend on `m_min^{-1}`, the fixed charges, and the finite species count.
Field budgets remain common because all species use the same Maxwell
field. Source acceleration majorants acquire `|e_b|/m_b`; pair force
majorants acquire `|c_ab|`. These are fixed finite constants and do not
alter exponents or logarithmic summability.

The occupation and selected-coefficient arguments therefore appear
transferable, provided the new manuscript states and proves them under a
simultaneous signed-increment bootstrap across all supported species and
uses `P` larger than the maximum normalized momentum of every species.
This is a stability argument for the proof mechanism, not a summation of
the one-species global theorem. The receiver-coefficient sum must multiply
the actual receiver's `|K_a|` and be checked for every pair before summing
the finitely many sources.

Checked limiting cases:

- `e_a=0`: receiver force and every pair coefficient vanish; motion is free.
- `e_b=0`: its Maxwell source and pair contribution vanish; its own
  distribution still contributes nonnegative kinetic energy.
- Equal-mass `e_1=1,e_2=-1`: cross terms have negative `c_ab`; the identity
  persists and absolute residual bounds use `|c_ab|`.
- Coinciding species with the same mass/charge may be merged by adding their
  densities; retaining labels separately is consistent with this reduction.
- One species with `m=e=1` reduces exactly to the family 362 normalization.
- Extreme fixed positive mass ratios enlarge constants, but do not send
  any coefficient to infinity within a fixed model. There is no uniform
  massless limit claimed by this analysis.
- No neutrality assumption occurs in the geometric or energy arguments.
  Coulomb modification in `continuation.tex:342–397` permits signed compact
  total charge just as it permits nonzero one-species charge.

## Exact remaining gaps before promotion

1. This audit is not a full newly written multispecies proof. The actual
   pairwise force representation, angular occupation inequalities,
   coefficient bound, finite sums, and simultaneous continuity closure must
   appear in the candidate and be reviewed together.
2. The one-species Glassey–Strauss criterion quoted in
   `continuation.tex:444–481` does not automatically become a multispecies
   theorem by citation. Use an exact primary multispecies continuation
   theorem or supply the finite-species continuation proof.
3. Actual Lean declarations, their transitive assumptions, semantic
   agreement, and build reproduction are not checked here. The scope
   document and comparator statement cannot substitute for that work.
4. Priority, authorship, source redistributability, final PDF, metadata,
   clean reproduction, production deposit, and tracker have not been audited
   by this reviewer.

Best-guess checkpoint percentages for this review alone: mathematical
resolution of the requested full project 35%; publication package 0%.
Those values are estimates and are not evidence. Strongest verified
result: exact pair-compatible signed kernel algebra plus checked exponent
contradiction under the manuscript's stated occupation premises.
