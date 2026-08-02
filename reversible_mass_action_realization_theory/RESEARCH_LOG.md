# Research log

## 2026-08-01 20:50 PDT — Program opened

- Opened this project only after the Version 2 tag, GitHub release, automatic
  Zenodo archive, and public project page were frozen and verified.
- Kept the project separate from
  `weakly_reversible_continuum_no_common_factor`; no Version 2 artifact or tag
  is modified by this work.
- Chose the restricted first target: an affine plane together with a
  nonsingular positive rational conic in three variables.
- Identified the exact fixed-support realization map.  For a support with
  directed rates `k`, reducing the three coordinate fields modulo a fixed
  Groebner basis of `(L,Q)` gives a rational linear map `M`, and
  `F_i in (L,Q)` for all `i` if and only if `M k = 0`.
- Recorded the strict-positive feasibility problem and its exact dual
  alternative (Stiemke form): `ker(M)` contains a strictly positive vector
  exactly when no row-space functional is coordinatewise nonnegative and
  nonzero.
- Recorded a local reducedness criterion: if `F=A L+B Q`, smoothness of the
  conic and rank two of the `3 x 2` coefficient matrix `[A B]` at a conic
  point imply equality of the localized steady ideal and `(L,Q)` there.
- Began a generic exact remainder-map utility and an independent seed
  verifier.  These are scaffolding for bounded-support searches, not evidence
  for the unproved universal realization target.

## Next checkpoint

1. Normalize plane conics up to positive-coordinate-preserving affine changes
   that are compatible with integer complexes.
2. Derive support-independent necessary sign conditions from the outgoing
   reaction cones at each source complex.
3. Search small degree-bounded connected reversible supports using exact
   kernel and strict-positivity certificates.
4. Determine whether one support works for an open semialgebraic class of
   ellipses, or whether support changes are unavoidable.
5. Prove or disprove a finite-degree universal support theorem.

No external contact or outreach occurred.

## 2026-08-01 21:00 PDT — Exact seed and toolkit checkpoint

- Completed the standalone seed verifier.  It imports no code or data from the
  earlier project and checks the support, reversibility, connectedness,
  stoichiometric rank, complete `21 x 20` remainder matrix, rank/nullity
  `16/4`, strict positive cone, clean witness, positive parametrized
  continuum, and coordinate gcd one.
- Exact verifier result:

  ```text
  PASS: standalone realization-theory seed verification succeeded
    reversible connected support: 10 complexes, 10 reversible pairs
    stoichiometric rank: 3; unique positive compatibility class
    complete conic-preserving rate family: rank/nullity 16/4
    clean positive witness: (a,b,c,d)=(653,1,70,915)
    conic-plane continuum: positive and pairwise distinct for -1<t<1
    clean coordinate gcd over QQ[x,y,z]: 1
  ```

- Added a reusable exact remainder-map constructor.  An independent invocation
  of that utility on the seed recovered matrix shape `21 x 20`, rank `16`,
  nullity `4`, graph connectedness, and stoichiometric rank `3`.
- Recorded an exact positive-ellipse geometry test, the fixed-support theorem,
  strict-feasibility primal/dual certificates, a local reducedness lemma, and
  the projective closed-locus argument for generic coprimality in
  `FRAMEWORK.md`.
- SHA-256 checkpoints:

  ```text
  2a19941b72c6428b3c84e6e6e576a0b61babb79e320763434013fa1405bbaadb  verify_seed.py
  c04579f7625ba4020bb005f5f459d8d134037ebee7410e914b387fa938c278f6  remainder_map.py
  ed8bc2341761e35d118d6d8aa34feaa15013c9de5d665667b3420308ff261373  FRAMEWORK.md
  ```

- Claim boundary retained: the framework reduces realization to exact finite
  problems and supplies a seed witness, but no universal ellipse-realization
  theorem is claimed yet.
