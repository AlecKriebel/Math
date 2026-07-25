# Research log: regular-monodromy obstruction

## 2026-07-25

- Began an independent audit of the translation between Galoisness of the
  Keller function-field extension and regularity of its natural monodromy
  action.  No draft produced by another agent was inspected.
- Fixed notation for a finite separable extension \(L/K\), its normal closure
  \(N/K\), \(G=\operatorname{Gal}(N/K)\), and
  \(H=\operatorname{Gal}(N/L)\).  The natural degree-\([L:K]\) action is the
  faithful transitive coset action \(G\curvearrowright G/H\); its point
  stabilizer is \(H\).  Therefore it is regular exactly when \(N=L\), i.e.
  exactly when \(L/K\) is Galois.
- Verified from Wright's 1981 paper that the Galois case of the Jacobian
  conjecture is valid over every characteristic-zero field (Theorem 3.7 and
  the summary theorem), while Campbell's 1973 proof was over \(\mathbb C\).
- Built GAP 4.16.0 locally in a temporary directory and loaded TransGrp 3.6.5
  to audit the degree \(2\) through \(10\) transitive-action enumeration.
  Added a reproducible script that cross-checks GAP's `IsRegular` result
  against both trivial point stabilizer and group order equal to the degree.

### 13:30 PDT checkpoint

- GAP returned 165 transitive actions in degrees \(2\) through \(10\): 17
  regular and 148 nonregular.  The regular action IDs are
  \(2T1\); \(3T1\); \(4T1,4T2\); \(5T1\); \(6T1,6T2\); \(7T1\);
  \(8T1,\ldots,8T5\); \(9T1,9T2\); and \(10T1,10T2\).
- Recorded the complete 165-row output in `transitive_actions_2_10.tsv`.
  Its SHA-256 is
  `21373021fe85115a27141360626edab1abb83209ec5808b2456ef94609d166f7`.
- Checked the base-field qualification.  Over \(\mathbb C\), arithmetic and
  geometric monodromy coincide.  Over a nonclosed field the original
  extension is tested by arithmetic monodromy; geometric regularity only
  tests Galoisness after base change.  The example
  \(\mathbb R(t^3)\subset\mathbb R(t)\) separates the two statements.
- Located explicit classical prior art: Stacks Project Tag 03SF gives the
  simply-transitive-fiber characterization of connected finite étale Galois
  covers, and Kuiken (1981), pp. 1143--1144, states that a cover is Galois
  exactly when its monodromy group has order equal to the number of sheets,
  hence acts regularly.  Therefore the proposed translation is classical.
- Completed `INDEPENDENT_AUDIT.md`.  The exact counterexample consequences
  include nonregular and nonabelian monodromy, function-field degree at least
  three, and forced \(S_3\) monodromy (with trivial field automorphism group)
  in degree three.
- Completion estimate: **100%** of the assigned independent audit and
  reproducible low-degree enumeration.

### 13:40 PDT port checkpoint

- Ported the four independent audit artifacts into the active repository using
  patch-based edits.  Renamed the independent script to
  `enumerate_regular_actions_independent.g` so the existing root script remains
  untouched.
- Replayed the renamed script with the independent GAP 4.16.0 build and
  confirmed byte-for-byte agreement with the preserved TSV.  This build is
  separate from the root audit's GAP 4.15.1 build.
- Completion estimate: **100%** of the requested artifact port and validation.
