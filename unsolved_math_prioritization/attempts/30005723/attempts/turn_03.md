# Attempt 3 of 5: geometry, scaling, and multiplier constraints

3 October 2026. Mechanism: force any multiplier by its symmetries and positivity.
Estimated full-target completion: 25%; necessary conditions proved, uniqueness
not proved.

## Exact scaling

For radius R>0 define U_Rh(x)=R^(−n/2)h(x/R), a real L²-unitary. Then

    A_m U_R = R^−2 U_R A_(mR),
    χ_R U_R = U_R χ_1.

Functional calculus and transported Sobolev domains give

    B_(m,R) U_R = U_R B_(mR,1),
    M_−(m,R) U_R = R U_R M_−(mR,1).                           (3.1)

If M_− is a multiplier f_(m,R), then

    f_(m,R)(x)=R f_(mR,1)(x/R).

Thus only the dimensionless mass-radius product is relevant to shape. At zero
mass this transports the unit-ball parabola to π(R²−|x|²)/R in this convention.
We make no claim that a possibly differently normalized general-radius source
formula can be used without checking its modular-parameter convention.

## Symmetry and signs

Spatial rotations commute with A_m and χ_1, hence with the Sobolev projections,
B_m and M_−. If M_− is a measurable multiplication operator, uniqueness of its
multiplier implies f(Rx)=f(x) almost everywhere for each rotation R. Equivalently
the multiplier has a radial representative. In dimension 1, reflection makes
it even.

For compactly supported momentum-data tests g in the ball, the modular entropy
quadratic form is a positive multiple, in the convention of the report, of
⟨g,M_−g⟩. The complementary subspace has inverse modular operator. Thus a
multiplier compatible with both entropies must have

    f≥0 almost everywhere in D,    f≤0 almost everywhere in Dᶜ.              (3.2)

For tests inside D, comparison with the containing tangent wedge with normal e
and its explicitly known multiplier yields

    ⟨g,M_−g⟩ ≤ ∫_D 2π(1−x·e)|g(x)|² dx.

Under the multiplication hypothesis this implies f(x)≤2π(1−x·e) a.e. For a
countable dense set of e on the unit sphere, taking the intersection of the
full-measure sets proves

    0≤f(x)≤2π(1−|x|),   almost everywhere in D.               (3.3)

The countable-set step is required; choosing a test-dependent pointwise
direction inside an operator inequality without first obtaining pointwise
multiplier inequalities would be invalid.

## Failed uniqueness route

The conformal parabola π(1−r²) satisfies the interior bounds, but so do many
other radial functions. For example a convex combination of that parabola
with 2π(1−r), with a coefficient depending on m, satisfies (3.3). Their
satisfying necessary inequalities does not make them modular generators.

One could try to force the parabola from the universal high-energy local term.
The scalar analysis around equations (80)–(81) of Arias et al. is not a theorem
identifying this entire continuum block with that term. Likewise the
Figliolini–Guido continuity theorem controls modular groups/resolvents, not
their derivatives on a fixed common Cauchy-data core. No required uniqueness
or block-limit theorem was established here.

**Outcome:** exact scaling, radialness, and conditional pointwise bounds;
the remaining uniqueness step is substantial and unresolved.

