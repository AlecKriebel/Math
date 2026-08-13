# Derivative exact-byte audit: residual 336 dead-ray certificate

**Audit date:** 2026-08-12 PDT.

## 1. Exact artifacts and verdict

This audit freezes the extended finite-support artifacts

~~~text
src/all_active_residual_levelset_336_certificate.py
SHA-256 4149b682d1222bd3327548b0eb95921f7aae20663816b345b48285239c12f93d

tests/test_all_active_residual_levelset_336_certificate.py
SHA-256 6f5802976d4de479a0728648248a2291f5d518e04de29b9b7053802eb7f1b9c2
~~~

> **STRICT PASS.**  The extended certificate preserves every previously
> certified 336-row output and adds the exact homogeneous dead-ray identity
> \(360=168+144+48\), with 270 dead rays whose bulk coordinate belongs to
> the lower support and four common-catalyst lower patterns occurring 12
> times each.  Its new dead-ray fingerprint is
> `c968fadc060af8225121efc84aa17380e11c41e677ed107d2d078c63d0f241fe`.

This is a finite support/descriptor theorem only.  It does not enumerate
orientations, rate vectors, population states, or reaction histories, and it
does not prove any stochastic estimate.

## 2. Preservation of the original 336 identity

The old exact-byte audit at SHA-256
`c77001576c75accddf91a86c70b8edd25d7edea3afb636ce2a956f5c185b075d`
certified the theorem/certificate/test triple whose certificate and test
hashes were `5b15d5ec...` and `18ce0f03...`.  Those old source/test hashes
must not be used as hashes of the extended files.

The extended executable independently replays the complete old output:

* 46,872 ordered disjoint support pairs;
* 5,169 mixed-atlas seed pairs and a 27,894-pair symmetry orbit;
* 18,978 pairs outside the orbit;
* 146 removed by a strictly positive invariant, leaving 18,832;
* all 68 active-only invariant-gap pairs retained, with zero selected rows;
* 169 all-active descriptors;
* exactly 336 corrected feasible failing incidences on 336 distinct pairs;
* equality of the selected and independently geometric incidence tuples;
* weights \((312,8,8,8)\);
* top sizes and top deficiencies \((154,126,48,8)\);
* lower-support counts \((86,86,86,78)\);
* full deficiencies \((120,130,66,18,2)\);
* linkage sides \((168,168)\); and
* 312 quadratic-only versus 24 unary-containing top supports.

The original two exact encodings are unchanged:

~~~text
d0c31db81db2400e0ead6e4a1a86b237fbf3b8bbb597340856a2756e9f6c884d
2bd4025f29d20ea4af467d46704c598652c9332ac4e32df18669cb7eb75c75a0
~~~

The added functions are downstream of this selection and do not alter its
definitions or output.

## 3. Independent dead-ray classification replay

Restrict the selected incidences to descriptor weight \((1,1,1)\).  These
are exactly the 312 homogeneous rows.  For each row and each coordinate
\(X\), declare the pure \(X\)-ray dead precisely when \(2X\notin T\).
Internal rank two implies at least one of \(X+Y,X+Z\) lies in \(T\): without
a carrier, the top support lies in the one-dimensional quadratic shell on
the other two coordinates.

The three symbolic cases are disjoint and exhaustive.

1. Both \(X+Y\) and \(X+Z\) occur: **two carrier**.
2. Exactly one carrier, say \(X+Y\), occurs and \(2Z\in T\): **dyadic**.
3. Exactly one carrier occurs and \(2Z\notin T\): rank two forces the exact
   **common-catalyst** support
   \(\{X+Y,Y+Z,2Y\}\).

An independent replay reconstructed this classification directly from the
raw selected rows without calling the certificate's
`homogeneous_dead_ray_rows()` function.  It returned

\[
  360=168\;\text{two-carrier}
      +144\;\text{dyadic}
      +48\;\text{common-catalyst}.                   \tag{3.1}
\]

A selected incidence can contribute more than one dead ray, so 360 rays
from 312 rows is consistent and intentional.

## 4. Lower-support relabelling

For each dead ray, relabel the dead coordinate, the chosen carrier
coordinate, and the opposite coordinate as \((X,Y,Z)\).  Relabel the unary
lower support through the same permutation.  Exactly 270 of the 360 rows
contain the bulk coordinate \(X\) in that lower support.  Thus a proof that
silently assumes \(X\notin U\) misses most dead-ray incidences.

Within the 48 common-catalyst rays the relative lower supports are exactly

\[
 \{X,Y\},\qquad \{X,Z\},\qquad \{Y,Z\},\qquad
 \{X,Y,Z\},                                           \tag{4.1}
\]

each with multiplicity 12.  The resulting sorted JSON payload includes the
support pair, descriptor, dead coordinate, kernel name, and relabelled lower
pattern.  Its exact SHA-256 fingerprint is

~~~text
c968fadc060af8225121efc84aa17380e11c41e677ed107d2d078c63d0f241fe
~~~

The independent raw reconstruction reproduced all counts and patterns.

## 5. Executable replay and scope

Running the extended regression test against the extended certificate gives
six passing tests.  The new test asserts (3.1), the 270 bulk-in-lower count,
the four 12-row patterns, and the exact fingerprint; the other five tests
reassert the complete original 336 identity and geometry.

The replay is finite and support-level.  It licenses the analytic proof to
use the three dead-ray kernels and all four lower-support patterns, but does
not license any activation, service, Foster, or recurrence assertion.  Those
remain separate analytic obligations.

## 6. Render replay

This audit was converted independently with Pandoc's single-backslash
TeX-math reader and rendered through Tectonic on letter paper.  The render
has no overfull, underfull, undefined-reference, or missing-glyph diagnostic.
Every page was visually inspected.
