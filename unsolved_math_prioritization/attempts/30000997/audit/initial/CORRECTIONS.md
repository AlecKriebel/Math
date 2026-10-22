# Required reading-note corrections

Original five-turn files are historical and remain unchanged. A correction note may be added by the author before re-review/publication.

## C1: Tensor normalization (required)

Use the packet's convention S=-D_v² Hess_p(d²/2), equal to its displayed coordinate MTW tensor on (u,Dexp_p(v)w). In the convention of Lemma 2.5 of the cited Kim–McCann Riemannian-products paper, cross_KM=2S. Hence at the finite witness:

- Packet S: 7/10−8/π²<0.
- Kim–McCann cross_KM: 7/5−16/π²<0.
- Diagonal orthonormal-null controls: S=2K/3 and cross_KM=4K/3.

No sign, null condition, or asserted local theorem changes. This is independent of the separate positive scaling that results from choosing d² rather than d²/2.

## C2: Smooth-cost domain (required)

Read the opening of TURN_5 as: “Fix a surface point p and v in the interior tangent injectivity domain D_p, so the geodesic from p to exp_p(v) is uniquely minimizing and nonconjugate.” Apply that hypothesis wherever the general Jacobi Hessian is identified with the actual smooth squared-distance Hessian.

Minimizing plus nonconjugate is not sufficient at a cut point with multiple minimizing geodesics. Outside D_p, formulas along a selected geodesic need not represent derivatives of the actual squared distance. The later TURN_5 criterion already uses D_p and needs no algebraic change.

The equatorial examples meet the repaired hypothesis: g_a≥g_round, the shorter equatorial arc has length r<π, and any g_a minimizer must therefore be the unique round minimizer. The independent normal Jacobi factor sin r/r is nonzero. Uniqueness comes from the metric comparison, not from nonconjugacy alone.

## C3: Numerical terminology (recommended)

The script field safe_no_conj_poles is a numerical heuristic, not proof of no conjugate points or admissibility before the cut locus. Describe the rejected shooting branches as “numerically suspected nonminimizing branches”; the approximate shorter competitors have not been interval-certified. These cautions do not affect the exact accepted claims.

## C4: Scope and priority (required to preserve)

Retain exhausted/global unresolved. The complete positive sphere has a certified NNCC failure and certified equatorial null positivity, but global A3w is unproved. No conclusion about novelty follows. Cite Figalli–Rifford–Villani §§2 and 6.1 for earlier Jacobi/angular/surface-of-revolution machinery and Kim–McCann for the known product principle.

## C5: State provenance (administrative)

Do not call the complete local directory byte-identical to the frozen remote directory: TURN_STATE.json differs (remote 226 bytes, local 266 bytes). All 18 other remote entries match local Git blobs, and all 17 author-manifest entries match SHA-256. Both state versions agree that the global problem is unresolved after five turns.
