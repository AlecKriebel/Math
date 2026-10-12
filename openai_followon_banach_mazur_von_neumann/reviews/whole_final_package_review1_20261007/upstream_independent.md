# Independent upstream proof audit for whole final package review 1

Completed 2026-10-07, approximately 14:43 UTC. Reviewer:
`whole_final_package_reviewer1_20261007/upstream_independent`.
This is a mathematical dependency subreview for the first new whole-package
reviewer, not a separate whole-package review, human referee report, or
publication authorization.

## Scope, independence, and exact artifacts

I extracted and read **all five upstream sections**, not a saved favorable
audit, from the actual frozen archive
`reviews/versions/final_candidate_v1/publication/upload-kit/source-and-verification.zip`.
The archive SHA-256 is
`4dc0129f59789e279318bc2e1ba53a1c3e414fda8a7ba32c8dd1d7f221aee9fc`.
I independently byte-compared every extracted upstream text file, including
the main TeX, references, and figure, to its Git object at
`adc7f1241b42e322a6451854ab7e4b4c146bf78a` in the read-only upstream checkout.
All comparisons passed. The complete section hashes are:

| Section | Lines | SHA-256 |
| --- | ---: | --- |
| 01-introduction.tex | 217 | ddec01dc15fa257e3f1e85004b54225dd43df633bbdfa957de98353c069ce4b2 |
| 02-walk.tex | 390 | 3d1015a1c20d2cfc8a4c8991652d93eed756763cd982cbc28a53fd625b7b3314 |
| 03-liouville.tex | 353 | 7782c390e534a15d35d7aee470ff425fcb6823c4073b29886f3dbffbc8d31622 |
| 04-rigidity.tex | 565 | 9cf9cf2b11fc838326321b4c0384904a303ecec43d732cd748c9204059f4ea60 |
| 05-cohomology.tex | 498 | c6c8e63bac0e543624ac63fd50a046878ba7082a531115111563455682e4d437 |

I also read the **complete frozen candidate** `manuscript/main.tex`, SHA-256
`46a02c0cd03f798459a9cfd8fb1cd5e03c4e599208a2a53750d3b218b7e96dc4`,
and the archive's `VALIDATION_SCOPE.md`, `SOURCE_VERSIONS.json`, upstream
scope statement, and source manifest. I did not read the bundled earlier
favorable mathematical review reports to obtain my proof verdict.

Fresh primary-source checks below used Popa's actual arXiv article, the
original Johnson–Kadison–Ringrose scan, the original CPSS article, and
Blackadar's author-hosted revised book. JKR Lemma 5.4 and Theorem 5.6 were
also checked visually on complete rendered printed pages 90 and 93 because
the OCR confuses the normal and continuous subscripts. Read-only source
downloads/renders remain under the ignored project `tmp` directory.

## Verdict and exact validation boundary

**PASS for the pinned mathematical cohomology input and its faithful use by
the frozen candidate. No substantive gap or counterexample was found.**

The strongest checked conclusion is: using the stated classical normal
reduction, complementary-summand vanishing, and standard finite von Neumann
structure results, the complete pinned manuscript supplies an **actual
ordinary bounded complex multilinear primitive with values in the same
algebra for every higher cocycle on every complex von Neumann algebra**.
In particular it supplies the exact H² and H³ hypotheses needed on the
candidate's fixed algebras P and E, including arbitrary predual density and
all von Neumann types.

This verdict is a mathematical source audit. I did **not** reproduce a Lean
kernel build, successful import, or axiom interrogation, and did not reprove
every cited classical theorem from foundations. No formal certification is
implied. The licensed source archive and candidate disclose these limits.
The human license decision and full publication/tracker protocol are outside
this subreview; their pending status cannot be cleared by my verdict.

## Correct dependency chain

The new finite type-II argument is **not** a passage from the averaged
cocycle to a completely bounded cocycle. It constructs an ordinary bounded
primitive directly. Its chain is:

1. ordinary bounded cocycle → cohomologous separately normal cocycle;
2. finite tracial separable case: Popa finite requirements → one rare-level
   walk → Liouville property → bounded primitive by last-input averaging;
3. uniform primitive norm → finite-input compactness removes separability;
4. explicit central homotopy → uncountable tracial central-piece assembly;
5. classical vanishing treats the non-type-II₁ complementary summand;
6. add back the bounded normal-reduction cochain.

Completely bounded methods occur in the **cited classical complementary
vanishing** result. CPSS p. 636, equation (1.1), expressly states ordinary
continuous vanishing as well as cb vanishing when the type-II₁ central
summand absorbs R. If that summand is zero the condition is vacuous. There
is therefore no inference from small cb norm to small ordinary norm, or
from cb primitives alone to arbitrary bounded cocycles, in the new proof.

## Reconstructed walk and Liouville checks

### Finite free requirements and the center

Popa's Theorem 0.1(a) permits the coordinate subalgebra and ambient factor
both to be P. Non-intertwining with the coordinate relative commutant holds
because a nonzero diffuse factor corner cannot embed in scalars (or their
finite matrix amplification). P^ω is a factor, so the full ultraproduct
relative commutant is scalar. The cited conclusion is thus the ordinary
scalar-trace freeness needed here. Repeatedly adjoining a Haar unitary and
reapplying the theorem is legitimate: finite adjunction preserves separable
predual in the faithful tracial representation. This produces a free finite
Haar family free from the fixed coefficient algebra in the **same**
ultrapower. The proof does not assume the coefficient algebra amenable and
does not invoke the different centralizer case 0.1(b).

Unitary representatives exist by lifting a bounded self-adjoint logarithm
and exponentiating; finite requirements can consequently be met at a
single coordinate. In a path test each path has a label occurring exactly
once in the entire tuple. Grouping the other free generators into the
coefficient algebra, the distinguished-letter string is reduced whenever
the tested group word is reduced. Expanding coefficient scalar/centered
parts leaves centered nonempty Haar-word blocks alternating with centered
coefficient blocks. Every trace vanishes, including non-cyclically-reduced
tested words.

For a separable finite algebra with center, the direct integral is applied
**only at the separable stage**. Countably many generating sections yield
countably many fiberwise 2-dense unitary sections by exponentiating rational
self-adjoint polynomials. Finite word-trace requirements are open in the
fiber 2-topology and their success sets are measurable. The first successful
tuple selection is measurable and globally bounded (unitary), so integrating
the fiber traces gives the asserted global finite requirements. This does
not try to use a standard measurable factor decomposition for the later
arbitrary nonseparable algebra.

At level ℓ, the huge but finite set of path tests is chosen before choosing
the finite unitary tuple. On a labeled sampling space the four failure
probabilities are bounded respectively by

\[
 \tfrac{16}{15}\ell\sqrt{p_\ell},\quad
 K_\ell^{-1},\quad (2K_\ell^2)^{-1},\quad
 \ell e^{-p_\ell^{-1/2}}.
\]

All tend to zero. Repeated labels are counted before evaluation, so distinct
labels representing the same algebra element do not invalidate the
probability calculation. The resulting theorem needs scalar moment
convergence only; no norm convergence of sampled polynomials is asserted.

### Martingale endpoints and exact ultrapower identities

For a bounded harmonic T, D(g)=T(g)g* gives an L²(M)-valued martingale
Z_n=D(W_n). The increment orthogonality identity gives the uniform bound
E‖Z_n−Z_k‖₂²≤e_k→0. The operator-norm ball is 2-closed by ultraweak
compactness and faithful trace testing, so support points a,b of a
nonconstant limiting law belong to M with the same operator-norm bound.

The forward and reverse endpoints are not incorrectly declared independent.
Their approximating half-prefixes use disjoint increment sets and are
independent; symmetry supplies the reverse inverse prefix's correct law.
The two mean-square replacement estimates and Markov's inequality give a
strictly positive lower bound for simultaneous neighborhoods of a and b.

Concatenation is applied only to signed blocks with **pairwise distinct
unsigned indices**. This is exactly what is needed for their increments to
remain independent. At each fixed tuple size m, the endpoint conditioning
mass c_m is first positive; the later walk time is then chosen so all other
finite bad-event probabilities total less than c_m/2. There is no unjustified
uniform lower bound in m or interchange of limits.

The first tracial ultrapower gives exact free Haar moments and the signed
first-letter identities. Bounded-ball 2-continuity is explicitly uniform
on each fixed operator-norm ball, preserves the tracial null ideal, and
passes to the quotient map using bounded representatives. The same proof
applies for the second ultrapower, despite its nonseparability. Freeness
from a or b is not asserted or used.

## Reconstructed first-letter rigidity checks

The Haagerup length estimate is not used on arbitrary sampled products.
It is used on the exact free Haar family in the first ultrapower, whose
faithful trace moments determine scalar polynomial norms. Its included
proof splits by the exact boundary cancellation count; for each count,
unique suffixes give orthogonal input/output decompositions, and each
matrix block is bounded by the coefficient Hilbert–Schmidt norm.

For s_r=r^(-1/2)Σg_j, the estimate gives ‖s_r‖≤2. The literal ordered
products of blocks B_d(z)=z(z*z)^d have no scalar terms after free
reduction. Each internally reduced block has positive endpoints and
positive excess one; block boundaries cannot cancel. Surviving repeated
unsigned indices, rather than repetitions erased by cancellation, are
discarded. A noncrossing partial-matching count gives |c_w(r)|≤3^L r^(-q/2)
at surviving length q. There are O_L(r^(q−1)) repeated-index words, hence
their aggregate 2-norm is O_L(r^(-1/2)); the length inequality improves this
to the needed operator-norm error. The retained words satisfy the original
multiplier identities exactly. Applying boundedness of R then gives the
ordered-block identities for s in the second ultrapower, separately for
the adjoint polynomial.

For A=s*s, the leading identity-word assignments are Catalan noncrossing
perfect matchings using d distinct labels. Lower-label assignments have
order O_d(r^(d−1)). The resulting compactly supported Catalan moments
identify the displayed Marchenko–Pastur measure on [0,4]; its zeroth moment
is one and it has no atom at zero. Faithfulness gives zero kernel. Finiteness
then makes the polar isometry V unitary.

For each fixed positive regularization parameter, norm polynomial
approximation applies to sp(A) and its **ordered powers**. Removing the
regularization uses bounded-ball 2-continuity on contraction powers, not
an unsupported norm limit of the polar approximation. Thus positive and
negative powers of V acquire the respective left multipliers.

Finally, uniformly bounded sine sums force a uniform bound on
(a−b)Re H_m(λV). Right multiplication by a reciprocal spectral-arc
function bounds (a−b)e on each short arc. The trace sums these compression
bounds with their own trace weights; it does not introduce the growing
number of arcs. This yields ‖a−b‖₂=0. No commutation of a,b with V and no
special spectral law of V is required. The paper's B(ℓ²(Z)) counterexample
correctly identifies why the final faithful finite trace is essential.

## Cohomology and arbitrary-algebra assembly

The bounded normal-map-to-2-continuity lemma includes its own proof. Small
2-norm inputs are spectrally truncated to small two-sided support, summable
support traces give decreasing tail projections, normality and lower
semicontinuity permit gliding-hump disjoint compressions, and random signs
contradict boundedness of B if their images stay large. This argument permits
a center and does not require a separable predual.

Last-input averaging is contractive. Product ultraweak compactness preserves
multilinearity and the ordinary multilinear bound. On a fixed cochain-norm
ball, tails of the countable measure are uniformly controlled, so P is
pointwise ultraweakly continuous there and the Cesàro cluster limit is
P-fixed. The original normal last-input slice's uniform 2-modulus survives
all translations, averages, and the ultraweak limit. The limit need not
remain normal. Liouville supplies the right-module identity that is
actually needed.

The averaged original cocycle equation has the correct alternating signs:
0=dh+(−1)^(k+1)f, hence g=(−1)^k h and dg=f, with ‖g‖≤‖f‖. The proof
does not falsely assert Pd=dP or that the averaged cochains are cocycles.
It produces a bounded (k−1)-linear map with values in **M itself**.

To remove separability in a tracial algebra, N_E contains E, f(E^k), and
unital matrix systems of every finite size. These countably many generators
give separable predual in the inherited faithful tracial representation.
The matrix systems rule out any finite homogeneous type-I central part:
its finite-dimensional fibers could not contain every M_m unitally.
The trace-preserving normal conditional expectation gives a separately
normal cocycle on N_E. Pulling a uniformly bounded primitive back through
the expectation gives eventual exactness on each finite input tuple;
products of inputs belong to N_E since it is an algebra. Directed finite
sets, not a compatibility assumption among the N_E, give the limiting
primitive by pointwise ultraweak compactness.

For a general type-II₁ summand, a maximal orthogonal family of supports of
normal **center states** partitions its unit, even if uncountable. On each
piece the faithful normal center state composed with the faithful normal
center-valued trace is a faithful normal tracial state. The uniform primitive
bound on these pieces is essential and established before assembly.

Merely assembling restricted primitives would not handle mixed central
inputs. The explicit J_z homotopy does. On a tuple decomposed into zM/qM
entries it inserts q immediately before the first qM input; the merger
with that input contributes +ψ, and every other nonzero face cancels with
the corresponding dJ term. Both outer actions on a qM input vanish in the
zM output module. I checked the signs directly in degree two as well as
the stated first-q cancellation argument in general degree. The degree-one
identity is consistent, and its bound (n−1)‖ψ‖ is uniform in z.

Adding this correction gives dH_i=z_i f on **all** input tuples and a common
finite norm bound. One non-type-II₁ complementary piece has its own finite
primitive bound by classical vanishing, so it causes no infinite supremum
problem. Bounded orthogonal central partial sums form a strongly convergent
net for arbitrary index sets. The bounded direct product therefore yields
a bounded multilinear G∈C_b^(k−1)(M,M), dG=f. Adding the normal-reduction
cochain proves actual-image vanishing for the original ordinary cocycle.

## Primary citation checks and their limits

- [Johnson–Kadison–Ringrose (1972), original scan](https://www.numdam.org/article/BSMF_1972__100__73_0.pdf),
  printed pp. 90 and 93: Lemma 5.4 supplies a bounded correction to a
  separately ultraweak cocycle; Theorem 5.6 identifies normal and ordinary
  continuous cohomology for dual normal modules. M with multiplication
  satisfies this module hypothesis. No separability assumption occurs.
  Fresh downloaded PDF SHA-256:
  `98d03522f5f589ae57572eb9e5c01c07390a166401eaa29578fc424b66d30944`.
- [Popa, arXiv:1308.3982v3](https://arxiv.org/pdf/1308.3982v3),
  Theorem 0.1(a), its following discussion, and Section 1.6: the required
  diffuse abelian free subalgebra exists for Q_n=P=M_n; the ultraproduct
  is a factor. This verifies the exact freeness input, not Popa's full
  incremental-patching proof from scratch.
- [CPSS (2003), original Annals article](https://annals.math.princeton.edu/wp-content/uploads/annals-v158-n2-p07.pdf),
  printed p. 636, equation (1.1), and pp. 638–639: the classical statement
  covers ordinary continuous cohomology for a general von Neumann algebra
  with the stated type-II₁ condition; the cochain complex uses the actual
  image and standard differential. The restated normal reduction also
  agrees with the original JKR theorem. This verifies the exact published
  classical input, not the full CES proof anew.
- [Blackadar, author's revised text](https://bruceblackadar.com/Mathematics/Cycr.pdf),
  III.1.6.3–4 supports the separable central factor decomposition and its
  preservation of type; III.2.5.4(iii) supplies equivalent finite divisions
  of the unit in type II₁; III.2.5.7–8 supplies the faithful normal
  center-valued trace and the resulting tracial state on each central
  state-support piece. The separability restriction of the direct-integral
  theorem is respected by the upstream proof.

The conditional expectation existence/bimodularity used in the finite
tracial algebra is the standard trace-preserving projection theorem; the
needed operations can also be constructed by the L² orthogonal projection
onto L²(N_E). I checked the algebraic use and its scope, not the original
Dixmier/Umegaki papers in full. No claim that all classical inputs were
proved or read in full should be based on this subreview.

## Candidate fidelity and static formal-source limits

The candidate's Theorem 2 states the same ordinary bounded, complex,
self-coefficient, actual-primitive result as upstream Theorem 1.1. The
candidate's explicit standard differential matches the upstream formula.
It uses only degrees two and three. Applying universal vanishing to P and
the fixed noncentral corner E=eOe is legitimate because both are von
Neumann algebras. The candidate explicitly avoids deriving E's cohomology
from a central restriction of M. It does not claim a universal primitive
constant, a universal Banach–Mazur threshold, or normal/cb primitives for
arbitrary ordinary cocycles. Those stronger claims are not supplied by this
audit.

For a limited fresh static check I read actual
`OAI/Analysis/BoundedHochschild/MainResult.lean`, `Main.lean`, the cochain
and differential definitions in `Cochains.lean`, and the cohomology quotient
in `OAI/Analysis/TracialCohomology/Cohomology.lean`. Cochains are
`ContinuousMultilinearMap ℂ ... M`, the differential has all adjacent merge
terms and standard signs, and coboundaries/cohomology use `LinearMap.range`
without closure. The actual selected result has abstract WStar/C*-algebra
hypotheses, no normality/cb restriction on f, and an existential actual
primitive conclusion. This authenticates the statement's conventions only.

`ComparatorChallenges/KadisonRingrose.lean` contains the expected challenge
`sorry`; it is not the solution module. The comparator JSON identifies
`OAI.Analysis.BoundedHochschild.MainResult` as the solution. The latter
has a written proof, but a written static proof is not a reproduced kernel
check. I did not inspect the entire formal dependency closure afresh or
establish the concrete-to-abstract WStar bridge by a kernel experiment.
The frozen candidate's express statement that it relies on the manuscript
proof and has no fresh Lean build is accurate. The redistributed upstream
scope note is an attributed upstream scope claim, not a new certification.

**Required repair from this subreview: none.** The parent should preserve
the formal-verification limitations and should not count this dependency
subreview as a second whole-package reviewer or as a completed publication.
