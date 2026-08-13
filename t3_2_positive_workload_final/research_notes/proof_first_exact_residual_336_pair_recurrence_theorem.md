# Exact residual 336 pair recurrence theorem

**Proof-first composition theorem, 2026-08-12 PDT.**  This note composes the
frozen finite support certificate with the two frozen global stochastic
theorems for the homogeneous and anisotropic level-set families.  It proves
positive recurrence for every fixed pair in the exact residual 336 set, for
every strongly connected labelled orientation and every fixed positive rate
vector.  It does not enumerate orientations, rates, population states, or
reaction histories.

## 1. Certified pair set

Let \({\mathfrak P}_{336}\) be the projection onto ordered support pairs of
the rows returned by the certificate function selected_incidences, in the
frozen files

~~~text
src/all_active_residual_levelset_336_certificate.py
SHA-256 4149b682d1222bd3327548b0eb95921f7aae20663816b345b48285239c12f93d

tests/test_all_active_residual_levelset_336_certificate.py
SHA-256 6f5802976d4de479a0728648248a2291f5d518e04de29b9b7053802eb7f1b9c2
~~~

An incidence is an ordered disjoint support pair together with an all-active
tier descriptor.  The certificate proves

\[
 \#\{\text{incidences}\}
 =\#\{\text{distinct ordered pairs}\}
 =336,                                                 \tag{1.1}
\]

and that the selected set equals the geometric level-set set.  For every
row, the certificate function levelset_geometry identifies a unique side
\(T\), the other side \(R\), a positive weight \(h\), and a scale \(s>0\)
such that

\[
 \dim\operatorname{span}(T-T)=2,\qquad
 h\cdot y=2s\ (y\in T),\qquad
 R=\{0\}\cup U,\quad h\cdot u=s\ (u\in U),             \tag{1.2}
\]

where \(U\) consists of two or three distinct unary complexes.  The two
independent row fingerprints are

~~~text
d0c31db81db2400e0ead6e4a1a86b237fbf3b8bbb597340856a2756e9f6c884d
2bd4025f29d20ea4af467d46704c598652c9332ac4e32df18669cb7eb75c75a0
~~~

The exact weight split is

\[
 336
   =312\,[h=(1,1,1)]
      +8\,[h=(1,1,2)]
      +8\,[h=(1,2,1)]
      +8\,[h=(2,1,1)].                                \tag{1.3}
\]

The same certificate proves that the 312 homogeneous top supports are
entirely quadratic, whereas all 24 anisotropic top supports contain a unary
complex.

The six focused certificate tests were replayed with the project’s modern
Python runtime and pass.  This finite computation certifies support identity
and normal form only; it contains no stochastic orientation or population
search.

## 2. Network realizations and theorem

Fix a pair in \({\mathfrak P}_{336}\).  On each of its two supports choose
an arbitrary finite strongly connected labelled directed graph, with
arbitrary fixed positive rate constants.  The union of the two linkage
graphs defines the stochastic mass-action chain on \(\mathbb Z_{\ge0}^3\).
The side \(T\) and lower side \(R\) are the unique sides selected by
(1.2); their position in the ordered pair is immaterial.

> **Theorem 2.1 (exact 336 pair theorem).**  Every such stochastic
> mass-action chain is nonexplosive.  Every closed irreducible population
> class is positive recurrent.  Equivalently, every infinite closed class
> has finite mean hitting time to a finite subset and hence a unique
> stationary probability; finite closed classes are positive recurrent
> trivially.

This assertion is global on each fixed population class.  It is not a
chart-local drift statement and requires no additional chart-switching or
terminal-exit lemma.

## 3. Homogeneous branch: 312 pairs

For a row with \(h=(1,1,1)\), equation (1.2) and binaryity give

\[
 T\subseteq\{2A,2B,2C,A+B,A+C,B+C\},
 \qquad
 R=\{0\}\cup U,                                       \tag{3.1}
\]

where \(T\) has internal rank two and \(U\) contains two or three unaries.
This is exactly the scope of the frozen global homogeneous theorem

~~~text
research_notes/proof_first_336_h111_workload_occupation_theorem.md
SHA-256 e3c484cdbda44949ba070dae6c911a2c7de465064857b61b5d9883e9dd03bdff

research_notes/proof_first_336_h111_workload_occupation_exact_byte_audit.md
SHA-256 740d929dfa460818df2cd134fc6beba70d015c7409f3c74ce0979316b8d4af89
~~~

That theorem is already global across every boundary face.  It symbolically
exhausts every top-dead pure ray into the two-carrier, dyadic, or
common-catalyst kernel; invokes exact all-clock physical-time macros for
those kernels; proves uniform top-service exposure on the compact activated
region; and applies one workload-only random-time Foster theorem on each
fixed class.  Catalyst-free invariant faces are open-unary reductions and
are proved positive recurrent directly.  Thus Theorem 2.1 holds for all
312 homogeneous pairs, for arbitrary strong orientations and positive
rates.

## 4. Anisotropic branch: 24 pairs

For an anisotropic row, permute the species so that \(h=(1,1,2)\).  Write
the weight-one species as \(A,B\) and the weight-two species as \(C\).
Equation (1.2) forces

\[
 R=\{0,A,B\}.                                         \tag{4.1}
\]

The unique unary complex on top level \(2s\) is \(C\), and the certificate
says every anisotropic top support contains a unary.  Therefore

\[
 T=\{C\}\cup Q,\qquad
 Q\subseteq\{2A,A+B,2B\}.                             \tag{4.2}
\]

Rank two forces \(|Q|\ge2\).  Hence (4.1)--(4.2) are exactly the scope of
the frozen global anisotropic theorem

~~~text
research_notes/proof_first_336_h112_quotient_foster_theorem.md
SHA-256 9206aa2b07aa802e4d06a769b3b60d520b2dbd12752312497aa5b41156780d48

research_notes/proof_first_336_h112_quotient_foster_exact_byte_audit.md
SHA-256 992448ad8b6520f014e783adb26a4f9b393b0e6a5f38c3a6262dd9b2fa0c1764
~~~

That theorem uses the single proper marked potential

\[
 V(x,t)=H(x)+\epsilon\frac{F(x,t)}{H(x)+1},
 \qquad H=A+B+2C,                                     \tag{4.3}
\]

and a finite all-clock episode menu which tiles every face of the trajectory.
Its physical-time Foster inequality gives finite mean hitting of a finite
marked set; forgetting the mark proves positive recurrence of the physical
class.  Coordinate permutation preserves explosion times, communicating
classes, and recurrence.  Thus Theorem 2.1 holds for all \(8+8+8=24\)
anisotropic pairs.

## 5. Exhaustion and classwise conclusion

The alternatives in (1.3) are disjoint and exhaustive.  Sections 3 and 4
therefore cover all

\[
                              312+24=336              \tag{5.1}
\]

certified fixed pairs.  Both analytic dependencies retain every physical
clock, include actual reaction endpoints, prove nonexplosion, and conclude
positive recurrence on each fixed irreducible class.  No inference from
orientation enumeration, bounded reaction depth, stationary averaging, or
a drift-or-exit terminal condition enters the composition. \(\square\)
