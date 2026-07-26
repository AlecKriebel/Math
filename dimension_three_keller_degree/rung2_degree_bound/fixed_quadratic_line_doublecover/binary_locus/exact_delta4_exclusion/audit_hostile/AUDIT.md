# Hostile assembly audit of the exact-\(\delta=4\) umbrella

**Final verdict:** **PASS**

**Audited object:** the revised candidate in the parent directory

**Audit scope:** exact-\(\delta=4\) inside the binary locus of frozen global
row `Q2-E2-A1-B2-D1-N2`, and no larger claim

The theorem and its proof are correct as written at that scope.  The
canonical exact-\(\delta=4\) incidence locus is the disjoint union of
exactly six stabilizer orbits, all six bridge entries point to the correct
full-lower family theorem, every lower theorem retains arbitrary lower
terms, and the contact atlases have no uncovered pivot or boundary.
Nothing in the umbrella closes the containing global row or implies a
degree-\(\ge5\) theorem.

This verdict applies to the repaired final snapshot.  Earlier snapshots
encountered during the live audit had fail-closed assembly defects; they are
listed under “Repairs forced by this audit.”

## 1. Denominators and immutable scope

The immutable global taxonomy has fourteen disjoint inclusive leading
leaves.  Its checksum verifier passes.  The leaf containing the present
binary locus is

\[
\texttt{Q2-E2-A1-B2-D1-N2}
\]

(fixed quadratic divisor times a line double cover), and both
`FROZEN_TAXONOMY_v1.md` and the current
`CERTIFIED_EXCLUSION_STATUS.md` still label that leaf **open**.  The
umbrella therefore cannot be read as a global-row exclusion.

Inside that row, the reconciled high-incidence denominator is the blinded
audit's

\[
19\text{ exact-}\delta=3+
6\text{ exact-}\delta=4+
1\text{ dependent power fibre}=26.
\]

The final `FAMILIES.json` points directly to that canonical
`DENOMINATOR.json`, not to the superseded \(17+6+1\) primary ledger.  The
reconciliation replay passes and confirms that the two primary defects
were confined to exact-\(\delta=3\): a missing doubled-nonbranch guard and
an invalid reciprocal quotient.  Neither defect changes the six
exact-\(\delta=4\) orbits.

## 2. Why there are exactly six disjoint orbits

For constant-linearly independent \(\alpha,\beta\), Hilbert--Burch gives
deficits \(0\le k_i\le2\) and
\[
k_1+k_2=\delta.
\]
Thus exact \(\delta=4\) has the unique shape \(\{2,2\}\).  Since
\(\gamma=8h^2pq\), the gcd is supported only at the two fixed roots and
the two branch points.  The division-free local valuation formulas in the
blinded denominator then exhaust the possible multiplicities.

For squarefree \(h\), degree three of \(R\) leaves only the mechanisms
\((f,e)=(3,1)\) and \((2,2)\), where \(f\) is the fixed-root contribution
and \(e\) the number of bare branch contacts.  Saturating the four possible
degree-four divisibility systems by the root-cover boundaries leaves
exactly
\[
s^2+5,\qquad 5s^4-6s^2+5,\qquad
(s^2-4s+1)(s^2+4s+1).
\]
After the stabilizer quotient these are the three isolated moduli
\(\kappa=-16/5,16/5,16\).

For doubled nonbranch \(h=L^2\), the exhaustive cubic calculation leaves
the three signatures
\[
L^4,\qquad pL^3\ \text{up to }p\leftrightarrow q,\qquad pqL^2.
\]
The branch-square, two-branch, and one-branch charts have no independent
exact-\(\delta=4\) solution.  The constant-dependent case is instead the
unique power fibre and has gcd degree five.

Disjointness is intrinsic:

- squarefree and doubled \(h\) have different root-multiplicity type;
- the three doubled signatures have factor partitions \(4\), \(3+1\),
  and \(2+1+1\);
- the three squarefree orbits have different fixed/contact incidence and
  different exceptional modulus;
- reciprocal roots at \(\kappa=16/5\) are one orbit because both branch
  contacts are present, and the reciprocal presentation at
  \(\kappa=-16/5\) exchanges the selected fixed root and branch.

There is consequently neither overlap nor a seventh orbit.

## 3. Complete alias and certificate bridge

The final machine bridge uses canonical IDs literally:

| Canonical ID | Historical primary alias | Certificate directory | Normal-form check |
|---|---|---|---|
| `D4-SF-21C` | `D4-SF-21C` | `d4_sf_21c_exclusion` | \(z=-5,\ \kappa=-16/5,\ R=X^2Y\) |
| `D4-SF-20CC` | `D4-SF-2C2` | `d4_sf_20cc_exclusion` | \(5z^2-6z+5=0,\ \kappa=16/5\) |
| `D4-SF-11CC` | `D4-SF-11C2` | `d4_sf_11cc_exclusion` | \(\kappa=16,\ R=h((z+1)p+4rq)\sim h(p+q)\) |
| `D4-DN-3` | `D4-DN-L4` | `d4_dn3_full_descent` | \(h=L^2,\ R=L^3\) |
| `D4-DN-2C` | `D4-DN-PL3` | `d4_dn2c_full_descent` | \(h=L^2,\ R=L^2(p-2q)\), up to swap |
| `D4-DN-1CC` | `D4-DN-PQL2` | `d4_dn1cc_full` | \(h=L^2,\ R=L(2p^2+pq+2q^2)\) |

Every current `certificate_label` equals its canonical `atlas_id`.
`verify_manifest.py` hard-binds the theorem scope, canonical source path,
canonical schema/status/scope/counts, ordered six IDs, certificate paths,
and six distinct terminal markers.  The aggregate execution plan is
emitted from this already validated manifest, so there is no second
hard-coded list that can silently diverge.

## 4. Arbitrary-lower-term scope

After the fixed \(H_4\) and \(R=(H_3)_3\) are normalized, a completely
general lower map subject only to \(E_7=0\) is represented by:

- six coordinates for the complete \(E_7\) contact kernel;
- eight arbitrary binary cubic integration constants in
  \((H_3)_1,(H_3)_2\);
- three arbitrary binary quadratic integration constants in \((H_2)_3\);
- all twelve coefficients of the two general ternary quadratics
  \((H_2)_1,(H_2)_2\); and
- all nine entries of the linear part.

All six packages compute the \(E_7\) nullities \(0,2,4\), so the six
contact coordinates are bases, not ansätze.  At \(E_6\), the eighteen
variables that actually occur are the eleven binary integration
constants, the six nonbinary coefficients of the first two quadratics,
and \(L_{33}\).  The six binary quadratic coefficients and the other
eight linear coefficients do not occur at that weight, but remain present
in the literal determinant and in the lower descent.  Thus “all 18 lower
variables” is not a restriction of the arbitrary-lower-term theorem.

The chart audit is:

| Family | Complete contact cover | Terminal argument |
|---|---|---|
| `D4-DN-3` | two conjugate plane interiors; punctured intersection; origin | interior \(E_5\) obstruction; intersection \(\det L=0\); origin binary exit |
| `D4-DN-2C` | two conjugate plane interiors; punctured intersection; origin | interior Bézout obstruction; exhaustive \(\mathcal A/\mathcal B\) split; origin binary exit |
| `D4-DN-1CC` | affine line \(\kappa\ne0\) and \(\kappa=0\) | nonzero \(E_4\) obstruction; zero binary exit |
| `D4-SF-21C` | generic contact plane; both rank-six directions; origin | resultant obstruction; fresh boundary obstructions; binary exit |
| `D4-SF-20CC` | affine line \(n\ne0\) and \(n=0\) | nonzero \(E_5\) obstruction; zero binary exit |
| `D4-SF-11CC` | generic contact plane; both conic directions; origin | resultant obstruction; fresh conic obstruction; binary exit |

Each origin and rank-drop boundary is recomputed from the unspecialized
equations rather than obtained by substituting into a formula whose pivot
vanishes.

## 5. Missing-pivot and dependency audit

No missing pivot was found.

- The apparent extra solver-denominator line in `D4-DN-3` is crossed by a
  safe rank-seven pivot independent of that denominator.  The punctured
  intersection's additional \(V=0\) pivot is separately rebuilt.
- The `D4-DN-2C` intersection ideal
  \(\langle\mathcal Q,\mathcal A\mathcal B\rangle\) is followed by the
  common \(E_4\) conditions and a disjoint exhaustive split:
  \(\mathcal B=0,\mathcal A\ne0\), then \(\mathcal A=0\), including the
  overlap.  Every later localization has its zero boundary handled.
- Both one-line families split nonzero contact from the freshly solved
  origin.
- Both two-dimensional squarefree contact loci treat every rank-drop
  direction and the origin separately.  The swap/Galois identifications
  used to reduce conjugate directions preserve the normalized top data.
- The canonical six rows are parameter-space points with no retained
  internal modulus or undeclared exit.  Their incoming specializations
  from exact-\(\delta=3\) are all present in the reconciled boundary
  ledger.

There is no circular proof dependency.  The denominator audit uses no
lower exclusion.  The six lower proofs use only their normalized top orbit
and the homogeneous Jacobian identities.  The umbrella then combines the
independent denominator statement with those six theorems.

Some implementations deliberately share algebraic infrastructure:
`D4-SF-20CC` reuses the squarefree SymPy determinant engine, and the DN
descents reuse their full-contact rebuilds.  This does not create an
unchecked common-mode dependency: every family wrapper also runs a
separate exact reconstruction (PARI/GP or clean-room SymPy), and every
wrapper has a live required-failure mutation.

The only external theorem used at a surviving zero-contact chart is Moh's
unconditional bounded-degree plane theorem.  The resulting plane Keller
map has degree at most four, strictly within the quoted bound.  The third
coordinate is a triangular lift, so no form of the open plane Jacobian
Conjecture is assumed.

## 6. Strict replay and mutations

The revised aggregate wrapper was run in full.  It emitted:

```text
EXACT_DELTA4_MANIFEST_PASS_6_OF_6_CANONICAL_19_6_1
DELTA_GE3_RECONCILIATION_STRICT_PASS_26
D4_SF_21C_FULL_STRICT_PASS
D4_SF_20CC_FULL_STRICT_PASS
D4_SF_11CC_FULL_STRICT_PASS
D4_DN3_FULL_FAMILY_EXCLUSION_STRICT_PASS
D4_DN2C_FULL_DESCENT_STRICT_PASS
D4_DN1CC_FAIL_CLOSED_STRICT_PASS
EXACT_DELTA4_SIX_FAMILY_EXCLUSION_STRICT_PASS
```

The hostile wrapper in this directory additionally copies the bridge into
an isolated temporary layout and requires each of the following mutations
to fail with its intended diagnostic:

| Mutation | Required rejection |
|---|---|
| canonical ID | membership/order mismatch |
| certificate alias | label/ID mismatch |
| certificate directory | binding mismatch |
| terminal marker | binding mismatch |
| canonical denominator path | source-path mismatch |
| theorem scope | scope mismatch |
| canonical count \(19\mapsto18\) | canonical-count mismatch |

The optimized-Python and deleted-family failures are also exercised by the
candidate aggregate.  Marker enforcement is exact-line enforcement, and
the family run plan comes only from the validated bridge.

## 7. Scope conclusion

The proved statement is:

> no noninvertible degree-four Keller map in the binary fixed-quadratic
> line-double-cover locus has exact gcd degree \(\delta=4\).

It excludes six fine incidence families.  It does not exclude the other
twenty fine high-incidence families, the lower-incidence strata, the
nonbinary part of the same global leaf, or any of the other thirteen
global leaves.  The immutable global denominator and current row status
are unchanged, and the universal dimension-three degree floor remains
four.  In particular, this audit makes no inference of degree at least
five.

## 8. Repairs forced by this audit

The first snapshot examined was not releasable:

1. it bridged through the superseded primary \(17+6+1\) source and did not
   bind canonical aliases, paths, or markers;
2. its aggregate ran a second hard-coded family list;
3. the `D4-DN-1CC` wrapper did not yet invoke its hostile reconstruction
   or contain a required-failure mutation; and
4. an intermediate repaired verifier still accepted mutations of the
   canonical source path, theorem scope, and advertised \(19+6+1\) counts.

The final audited snapshot repairs all four defects.  They are recorded
here so that the PASS verdict cannot be mistaken for approval of the
earlier bridge.

The calculations and this audit are AI-assisted exact-computation
research, not peer review.
