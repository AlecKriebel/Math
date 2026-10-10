# Five-approach log

Date: 2026-10-04 UTC. Times below describe this bounded investigation.
All five count as substantive mathematical approaches. Tool calls and source
triage are not separate attempts. Full-target completion estimates are rough
planning judgments, not calibrated probabilities.

## 1. Radial curvature and singularity order (17:17–17:19)

Mechanism: solve or inspect the radial Gauss-curvature equation, compare the
integrated metric length against density divergence, and test the sign of the
curvature hypothesis.
Result: exact family λ_a=a r^(a-1)/(1-r^(2a)), 0<a<1, has κ=-4, density
blow-up on both boundary components of a punctured disk, and finite length to
0. Flat power densities give a simpler control; disk-wide subcritical powers
fail the lower-curvature assumption. None refutes the free-arc theorem.
Gap: this excludes some boundary sets but does not find the weakest positive
hypotheses. Full-target completion estimate: 15%.

## 2. Conformal flattening and derivative control (17:19–17:20)

Mechanism: pull λ back by a conformal chart and apply the known disk boundary
lemma. Nonzero continuous boundary derivative transfers blow-up in both
coordinates; Dini smoothness is a standard sufficient assumption.
Result: explains why C² is stronger than the naive chart proof needs.
Obstruction: for a general Jordan chart, |φ'| may tend to zero, so multiplying
an unspecified divergent function by |φ'| does not preserve divergence.
No necessity of Dini smoothness follows. Full-target completion estimate: 20%.

## 3. Exterior approximation and a curvature-controlled cutoff (17:20–17:22)

Mechanism: compare a blowing-up supersolution with hyperbolic metrics of
outward neighborhoods, prove density convergence by normalized covers and
Montel, then multiply by (R²-|z-ξ|²)^(-1) to close a local patch.
Result: Theorems A and B, including a uniform punctured-disk lower barrier
and a last-crossing proof in the original domain. This avoids the derivative
bottleneck. Constants and curvature scaling are explicit.
Obstruction: the normal-limit image only lies in int(cl G); thin defects
can disappear unless the local component is regular-open.
Full-target completion estimate: 45%.

## 4. Transport local completeness rather than density (17:22–17:24)

Mechanism: use d_(λ|P)^P≥d_λ^Ω and a Carathéodory boundary homeomorphism;
apply the established disk local-completeness estimate and cancel |φ'| in
the hyperbolic density quotient.
Result: reverse implication for free-Jordan patches. Combined with approach
3 it yields the no-differentiability equivalence in Theorem C.
Obstruction: a general boundary set need not admit these patches.
Full-target completion estimate: 55%.

## 5. Distinguished-set and endpoint obstruction tests (17:24–17:26)

Mechanism: pull back the disk hyperbolic metric by f_a=((1-z)/2)^a and
compare with the isolated-singularity classification; test whether smoothness
of the ambient boundary alone determines the answer.
Result: positive real-analytic constant-curvature metric on D blows up at
Γ={1} but has finite length there. Thus relative openness/freeness and the
geometry of Γ itself cannot be omitted. Slit interiors can be covered
componentwise, while the argument does not classify slit endpoints or
arbitrary thin boundary sets.
Gap: no necessary and sufficient general criterion, no minimum among all
boundary hypotheses, and no priority proof. Full-target completion estimate:
55%; final status is unresolved/partial, not a 55%-proved theorem.

After approach 5, only proof exposition, exact controls, source verification,
and package freezing were performed. Further research requires a new
user-authorized budget or a genuinely distinct target; independent audit may
check or reject the present artifacts but must not silently extend the search.
