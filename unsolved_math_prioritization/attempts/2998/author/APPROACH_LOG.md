# Five-approach record

Target: rank 695, ID 2998, modern K3 Problem 4.122. All five approaches concern the same fixed embedded branch-surface problem. Outcome: partial results; no universal construction or general counterexample. None is counted as a separate solved catalog problem.

## 1. Fixed-degree representation and monodromy enumeration

**Attempt.** Start from Iori–Piergallini's degree-five representation, then try to make its branch surface independent of the total manifold.

**Work.** Checked the primary theorem, its PL/local-flatness conventions, and its monodromy description. Proved that a fixed surface has only finitely many covers of any bounded degree: there are finitely many homomorphisms from its finitely generated complement group to Sym(d), and completion is determined by the complement cover. Tested the simple specialization of the invariant formulas.

**Result.** A universal surface necessarily uses unbounded degree. Simple-only branching cannot work even with unbounded degree, since both chi=2d-chi(S) and sigma=-e(S)/2 impose restrictions. Products of transpositions do not imply simplicity.

**Stop.** The representation theorem changes the branch surface. No surface-preserving nonsimple universalization was found.

## 2. Signature and normal-bundle obstruction

**Attempt.** Rule out every possible fixed embedded surface by the branched-cover signature formula.

**Work.** Inspected the modern signature theorem, its proof scope, and the original Viro formula. Converted upstairs Euler numbers to downstairs cycle data, preserving the factor of the ramification index. Used S^4 and CP^2 as orientation-independent zero/nonzero-signature controls.

**Result.** Every universal surface must have positive and negative normal-Euler components. Those components must be nonorientable. In particular a connected or wholly orientable locus is impossible.

**Stop.** Mixed-sign components permit cancellation. The argument does not rule out all disconnected nonorientable surfaces.

## 3. Euler characteristic and low-complexity branch surfaces

**Attempt.** Combine ramification defects with negative-Euler-characteristic closed total spaces.

**Work.** Proved the stratified Euler formula for arbitrary meridian cycle types. Derived chi(W)>=(2-P)d+P, where P is the positive Euler-characteristic mass of the branch surface. Tested against connected sums of S^1 x S^3 and combined with the signature result.

**Result.** Universality implies P>=3, at least three connected components, and an explicit linear lower bound on the degree needed for W_g. Exact finite arithmetic checks pass.

**Stop.** At least three components survive the scalar constraints. A formal three-component cycle profile gives chi=0 and sigma=0, demonstrating that these scalar tests alone cannot justify general nonexistence; no geometric realization is claimed.

## 4. Fundamental groups and branched completion

**Attempt.** Find an obstruction in the fixed complement group's finite-index subgroups and their quotients.

**Work.** The ordinary complement covering identifies the upstairs complement group with an index-d subgroup. Inclusion into the completed manifold is surjective on pi_1. Applied this to (S^1 x S^3)#(S^1 x S^3), whose fundamental group is F_2.

**Result.** The branch-surface complement group must be large. This excludes finite and virtually solvable complement groups.

**Stop.** Largeness is not a realization theorem for meridional quotients or four-manifold topology. No obstruction to every sufficiently complicated surface complement was found.

## 5. Relative ribbon universality and gluing

**Attempt.** Close the known universal four-ball ribbon construction by doubling or a fixed cap.

**Work.** Read the original universal-surface theorem and concluding component reduction. Distinguished proper ribbon surfaces from closed branch surfaces. Proved that doubling the orientable surface makes all signature contributions vanish. Formulated the simultaneous degree, peripheral-monodromy, and lifted-gluing conditions needed for an alternative cap.

**Result.** Direct doubling cannot represent CP^2. The existing B^4 result does not supply the necessary relative boundary extension for every closed W. A July 2026 representation theorem was checked and also allows the branch surface to vary.

**Stop.** No fixed nonorientable cap satisfying all the relative conditions was constructed. No impossibility theorem for all such caps was proved.

## Overall stopping condition

Five substantive approaches are complete. The packet freezes all proved partials, the exact external theorem dependency, checks, and source limitations. The original target remains unresolved by this work. No remote write was made, and publication must await fresh independent audit of the frozen manifest.
