# Release notes — version 1.0.1

**Release date:** 29 July 2026

**Title:** *Low-Schmidt Rigidity and Tensor-Local Constraints in the
Exceptional Unitary Hecke Yang--Baxter Class*

## Correction summary

Version 1.0.1 is a correction and editorial release. It does not enlarge
any mathematical theorem from version 1.0.0.

1. The title page now reports the public release version `1.0.1`. The
   immutable version 1.0.0 artifact is preserved with its mistakenly printed
   internal version `0.1.0`.
2. Seven labels formerly placed inside unnumbered display environments were
   repaired. Four referenced formulas now use numbered `equation`
   environments; three unused labels were removed.
3. The abstract now says that the paper derives exact structural constraints,
   rather than claiming to determine “the exact structural frontier.”
4. The title and abstract foreground the sharp low-Schmidt theorem:
   exceptional reflections of operator-Schmidt rank at most three exist
   exactly when \(4\mid d\).
5. The manuscript sections were reordered to follow their logical
   dependencies: automatic standardness, tower arithmetic, invariant-leg
   arithmetic and low-Schmidt rigidity, unrestricted rank four, square
   inheritance and the dimension-six leg intersection, then the two
   conditional model classes.
6. The bounded one-sided \(4+2\) reduction and the secondary \(d=4\)
   sitewise orbit were removed from the main narrative. Their exact content
   remains in `manuscript/SUPPLEMENT.md`.
7. Public summaries now state the operator-Schmidt-rank-four hypothesis
   explicitly and distinguish the deterministic exact verifier suite from
   the numerical searches retained elsewhere in the project.

## Mathematical scope

The complete exceptional dimension spectrum remains open. In particular:

- no exact \(d=6\) witness is supplied;
- four-divisibility is not proved at unrestricted operator-Schmidt rank;
- simultaneous rank-four sandwich degeneracy remains possible;
- a one-sided four-dimensional invariant square in \(d=6\) remains possible;
- neither individual leg commutant in \(d=6\) is proved scalar.

## Verification

The central suite contains 10 deterministic exact programs. No theorem
relies on numerical evidence. The correction release was rebuilt
deterministically, checked for valid cross-references, rendered with Poppler,
and visually inspected. Exact artifact digests are recorded in
`SHA256SUMS`.

Version 1.0.0 remains available at
<https://github.com/AlecKriebel/Math/releases/tag/exceptional-ybe-constraints-v1.0.0>.
