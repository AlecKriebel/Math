# Source-first reconstruction and independent expectations

UTC start: 2026-10-03. The task instruction exposed proposed mechanism names
(Tor/Bockstein, products, quotient duality, support), source locators, and two
claimed control counts. No candidate proof, checker, historical stream, root
verdict, or sibling verdict was read before this file and its controls were sealed.

## Exact question and conventions

The literal OWR 43/2006 question is on printed 2590 (PDF page 12), in Davis's
contribution beginning printed 2588: does virtually type FP imply that the total
integral group-ring cohomology is finitely generated as a group module? The
immediately preceding formulas identify the cohomology modules as right modules.
AGT 6 (2006), printed 1289 (PDF page 1), expressly defines cohomology using left
coefficient modules and explains that the commuting right action on ZG descends
to a right action on H*(G;ZG). Thus the object is the graded direct sum of these
right ZG-modules. This is neither abelian finite generation nor a cup-algebra
generation assertion.

I use FP in its finite-resolution sense: an augmented exact resolution of the
trivial left ZG-module Z by finitely generated projectives, with finitely many
nonzero terms. Brown's own lectures, printed/PDF 11, Definition 2.8, distinguish
this from FP-infinity. Virtually FP permits torsion in the ambient group; a
nontrivial finite group is virtually FP but has infinite integral cohomological
dimension. Its regular-coefficient cohomology is still concentrated in degree 0.

For FP groups, P_i^*=Hom_ZG(P_i,ZG) are finitely generated projective right
ZG-modules. Their bounded cochain complex has finite support in cohomology.
Its top cohomology is a finitely generated cokernel. The lower kernels need not
be finitely generated merely because the terms are. Most crucially, arbitrary
bounded projective complexes over a group ring are not necessarily the dual of
an augmentation resolution of Z. A putative counterexample from such a complex
must supply that group realization and verify exact augmentation before it can
answer the question.

## Primary positive model, and its exact limits

The AGT proof is integral through Section 6. Corollary 3.3 (printed 1300), Lemma
4.1 (1302–1304), Lemma 4.6 (1305), and Lemma 4.8 (1307) use explicit integral
bases and abelian direct summands. The quotients A^T/A^{>T} are free abelian and
cyclic as right modules (they are quotients of a_T A). Theorem 4.5 (1305, proof
1308) gives associated graded right modules, with finitely many summands from
finite chamber cohomology. Lifting generators through the finite filtration gives
finite generation. Lemma 4.7's passage from cochains to cohomology uses this
abelian freeness. It is not justified for arbitrary tensor factors without Tor.

Example 5.2 (1309–1310) explicitly rules out a right-module direct-sum splitting
in general, despite the abelian splitting. Section 7 expressly changes the base
to Q. Its Hecke/building formulas cannot silently be read as integral theorems.
This literature establishes a special class, not an answer for all virtually FP
groups. No bounded literature check can certify that the universal question is
currently open or that a conditional reduction is novel.

## Integral product formula and criterion

For finite projective augmentation resolutions of A and B, their tensor over Z
is a projective resolution for A x B. The underlying Z-complexes are free, and
the augmentation sequences split as abelian complexes, so exactness survives
tensoring. Finite projectivity gives the corresponding dual cochain identification
with C_A tensor_Z C_B. The cohomological integral Kunneth sequence is

0 -> direct_sum_{i+j=n} H^i(A;ZA) tensor_Z H^j(B;ZB)
  -> H^n(A x B; Z[A x B])
  -> direct_sum_{i+j=n+1} Tor^Z_1(H^i(A;ZA),H^j(B;ZB)) -> 0.

All maps are right Z[A x B]-linear. The sum is finite for FP factors. Natural
splitting as right modules is not asserted. If both factors have finitely
generated total modules, every tensor term is finitely generated (pair the
generators). Under that hypothesis the product has finitely generated total
cohomology if and only if its finite direct sum of Tor terms is finitely generated:
necessity uses the quotient, and sufficiency lifts generators in this short exact
sequence. This is a conditional exact criterion, not a proof of the unknown
Tor finite-generation assertion. Flatness over Z of one factor's cohomology
eliminates Tor. Flatness of cochain terms alone does not eliminate Tor of their
cohomology. Field tensor calculations do not settle the integral assertion.

For C_m=(Z --m--> Z), degrees 0 and 1, H^1=Z/m. The tensor C_m tensor C_n
has d0=(m,n)^t and d1=(-n,m). With g=gcd(m,n) it has H^1=Z/g and H^2=Z/g.
The former is precisely the Tor term, one degree below the tensor term. The
provided code records unimodular Smith certificates and the connecting map
sending the kernel generator (m/g,n/g) to n/g mod n in ker(m:Z/n -> Z/n).
These are free abelian cochain controls, expressly not group counterexamples.

## Integral coefficient connecting map

The coefficient sequence 0 -> ZG --p--> ZG -> F_pG -> 0 gives the natural right
module sequence

0 -> H^n(G;ZG)/p -> H^n(G;F_pG) -> H^{n+1}(G;ZG)[p] -> 0.

It detects the integral p-kernel, not merely a mod-p Bockstein. For C_4 and p=2,
the integral connecting class is 2 mod 4, nonzero, whereas its reduction mod 2
is zero. Rationalizing erases every such control. A Prüfer p-group has zero
rational tensor and zero quotient modulo p but has nonzero p-kernel and is not
finitely generated. This is an algebraic detection boundary, not a realization
as H^n(G;ZG). Integral torsion, primes, exponent bounds, and total-degree
support must be tracked explicitly in any proposed reduction.

## Extension framework and independent expectations

Sharifi, Homological Algebra, Theorem 4.3.12 is the Hochschild-Serre theorem on
printed/PDF 97 in the freshly fetched version, not page 86. Its primary proof
factors invariants through N-invariants and uses the latter's right adjunction
to exact inflation to preserve injectives. It yields the additive spectral
sequence H^p(Q;H^q(N;ZG)) => H^{p+q}(G;ZG). The action convention is supplied
by naturality for commuting coefficient endomorphisms. This theorem alone
does not prove module finite generation, spectral-sequence collapse, or novel
extension closure.

For N of finite type FP, extension of group-ring coefficients through ZN -> ZG
commutes with the finite projective Hom complexes and their cohomology because
ZG is free as a left ZN-module. The resulting H^q(N;ZG) has a semilinear Q
action, whose twisting must be handled explicitly. If Q is an integral duality
group of dimension d with Z-flat dualizing module D, then duality can convert
the Q-cohomology to homology of a twisted induced module, concentrated in
degree d. This is a legitimate special mechanism only after the induced-module
identification, Z-flatness hypothesis, right G-action, and generator lifting
are checked. One must not replace those hypotheses with a field calculation.
Brown's primary lecture proof printed/PDF 25–27 treats the stronger free
abelian D case and exposes the dual-complex construction. It does not on its
own supply every possible flat-but-not-free extension theorem.

## Falsifiable controls and promotion rule

The independent script tests 144 integral tensor/Smith/connecting cases, 96
integral coefficient connecting cases, 36 shifted free-factor cases, a
noncommutative S3 right-action case, a genuine infinite C2 augmentation
resolution versus its invalid finite truncation, and two support/detection
boundaries. It rejects zero-Tor, wrong Tor degree, rational-only, left-residual
action, wrong action-composition, and flat-cochains-imply-flat-cohomology
shortcuts. The first seal binds the complete script, this reconstruction, and
full output before candidate reads.

Target success requires a proof or group counterexample under the exact
virtually FP integral/right-module conventions. Correct closure lemmas,
computational algebra controls, and precise remaining gaps are valid partial
results; none is promoted to a full solution, novelty finding, or merge certificate.
