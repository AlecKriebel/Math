# Priority audit updated 23 July 2026

This is a provisional mathematical-priority review, not a legal opinion and
not a guarantee that every unpublished manuscript has been found.  It records
the searches made, separates new-looking claims from known or incremental
material, and identifies what must be strengthened before submission.

## Executive verdict

The new theory-first reductions change the priority assessment. The strongest
current internal paper is now theorem-led, not a solver-led local-search
report:

1. the adjacent cyclic-fold theorem turns `BS(84,83)` exactly into the
   intersection of cyclic complements at 84 and 83, with a prime-83
   oriented-SDS construction target;
2. a dependency-free primitive-eight reduction plus exact margin norms proves
   that every exact `BS(84,83)` is at raw distance at least 34 from Eliahou's
   seed;
3. the exact 2-adic formulation reduces the first two special-construction
   layers to 169 structural bits and identifies a five-lag Frobenius-square
   obstruction with no first-order tangent repair; the full residual is now
   factored as one rank-one ten-sparse carrier, and two natural nonlinear
   comb completions are exactly excluded;
4. the projective five-comb quotient has rank nine, an exact physical
   high-lag boundary table, and a dependency-free dyadic compression theorem;
   its diagonal/common-type family is completely solver-excluded, while the
   distinct-lobe theorem exposes 721,984 genuinely larger inventories;
5. the sextic `LP(333)` quotient reduces an order-six multiplier family to
   108 binary signs and 298 exact row-signature shards after both axes are
   factored; a residual `C3` theorem cuts 1,658,700 compatible signature
   sextuples to 552,912 signature-level orbits;
6. the independent fixed-`q` telescope reduces to the empty class `TU(41)`;
7. the quartic-residue `LP(333)` quotient reduces a motivated subfamily to 45
   QPSK phases and 16 remaining mixed equations after both axes are solved;
8. the safe-prime Sidelnikov calculation gives an exact prime-83 PAF identity
   and a 41-bit inverse-pair orientation obstruction that closes its
   degree-two independently decimated extension.

These results are worth preserving as a compact internal manuscript. Nothing
will be circulated, submitted, posted, or sent by this project. The
radius-18 CP-SAT corpus is now secondary: its uncertified leaves no longer
limit the stronger dependency-free radius-33 exclusion, though they remain
useful historical artifacts.

The openly available recent `LP(333)` papers and March 2026 status report
have been inspected.  The symmetric/symmetric observation is prior; the
skew/skew and mixed equations were not located but are incremental
specializations, not paper-leading results.  Project policy prohibits all
external outreach; no contact drafts or recipient lists are retained.

## A. Primitive-eight fixed-`s` and distance-34 obstruction

**Priority assessment: strongest likely-new theorem-sized result; high
confidence in the repository proof, provisional confidence in literature
priority.**

Evaluation at `z=exp(pi*i/4)` reduces each base sequence to four signed
residue sums. Splitting over `Q(sqrt(2))` forces a rational 16-square equation
of energy 334 and an irrational bilinear cancellation. Eliahou's base seed
has rational energy 1614.

A dependency-free dynamic program exhausts the sixteen bounded coordinates
and proves that the rational sphere cannot be reached in fewer than 33 raw
sign changes. It then exhausts all 1,350 targets on that first shell: 66 pass
the irrational equation and none can satisfy both exact margin norms. This
proves the complete raw radius-33 exclusion without trusting a solver. An
explicit distance-34 sign witness passes the two root equations, both margin
norms, and all endpoint-quad products, so the combined necessary-condition
bound is sharp.

The same calculation supplies an exact fixed-`s` theorem. The fixed `A,C`
sequences alone contribute `807+24*sqrt(2)>334`; the nonnegative `B,D`
norms cannot repair the excess. A still shorter `z=1` proof observes that
the remaining row sums would have to represent 321 as two squares, which is
impossible modulo 3 and 9. This is independent of the fixed-`q` theorem.

The proof is elementary once the right root is chosen, but the application
to Eliahou's explicit seed and the sharp distance computation were not found
in the sources already checked. `VARIABLE_Q_ROOT8.md` states the result and
`variable_q_root8.py` checks every finite step.

## B. Adjacent folds and the prime-83 oriented SDS

**Priority assessment: strongest constructive theorem; likely new, with
provisional literature confidence.**

For general `BS(n+1,n)`, simultaneous complementarity of the padded
modulo-`n+1` fold and endpoint-folded modulo-`n` fold is exactly equivalent
to all aperiodic equations. At `n=83`, the prime fold becomes 41 charged
supplementary-difference equations on inverse pairs of `Z/83`, with 45
anchored size profiles and a relative norm equation over
`GF(2^82)/GF(2^41)`.

This is a genuine construction reduction: first build one prime-fold object,
then test its finite bank of 564,898 multiplier/phase lifts at modulus 84.
Any pass is already an exact base sequence. The checker verifies the theorem
exhaustively at small orders and checks every order-83 coefficient identity.
The local literature reviewed so far does not state this formulation, but a
full priority claim would require broader lawful source comparison.

The reduction now has a complete implementation and strict verifier. Its
best retained nonexact state has quarter-energy 14 and 11 bad independent
lags. An exact structured neighborhood around that point contains no prime
fold; the result is local and must not be described as evidence of
nonexistence.

The identity `167=2*83+1` also produces a binary Sidelnikov word and a
one-zero skew companion whose PAFs sum to `-2`. The natural endpoint
completion, zero-fill variant, degree-two product family, and all independent
decimations of that family are exactly excluded. The decisive necessary
condition is equality of the 41 inverse-pair orientation fingerprints; the
only catalog intersection violates the row-energy bound. This is a clean
supporting theorem, but it excludes one algebraic family rather than the
prime fold itself.

## C. Finite 2-adic lift and quartic QPSK quotient

**Priority assessment: substantial internal theory; promising supporting
sections, not yet standalone existence results.**

The special construction has an exact 84-parameter reciprocal `q` skeleton.
At the seed, the next layer is an 82-rank linear system in `s`, leaving an
85-dimensional fiber. The finite Hensel tower has degrees
`1,2,4,8,16,32,64`; Eliahou's point first fails at five degree-8 lags forming
a Frobenius square. The augmented Boolean-Jacobian rank is 201 versus
coefficient rank 200, exactly ruling out a first-order tangent repair.

The complete seed defect further factors as

```text
14 + 32*N((z^42-1)(1-z^4+z^8-z^12+z^16)).
```

The literal 30-variable reciprocal chord has no modulo-32 point. A
unit-circle root of the common comb excludes every repair that retains this
factor in all four sequences, even with overlapping integer quotients. A
second exact argument exhausts 256 labelled `BS(4,3)` boundaries and 80,896
endpoint pairs to exclude the orthogonally staged disjoint completion.

The same calculation gives a positive construction reduction. The
alternating comb belongs to a minimum complementary octet. Opposite
separation-42 polarizations, doubled, produce 32 flat channels of energy 320;
their supports pack into lengths `(84,84,83,83)` with exactly 14 singleton
holes. Cancelling the packing cross terms would give an exact base sequence.
This is presently the most concrete nonlinear construction target, but it is
not itself a matrix or an existence theorem.

Independently, the `LP(333)` pair becomes one QPSK array on `Z_9 x F_37`.
Quartic residues form a `(37,9,2)` difference set, yielding an exact
45-phase, 22-equation multiplier quotient. A checked table satisfies the
fixed compression and every pure-axis equation; 16 mixed equations remain.
The elementary Paley-row lift is exactly impossible by a group-algebra
denominator obstruction. An axis-preserving constructor reduced its quotient
energy from 1536 to 112, but still misses 14 of the 18 remaining quotient
orbits. This is a strong construction checkpoint, not a candidate and not a
theorem about existence in the quotient.

Both reductions look new in the sources inspected, but neither finds an
exact object. They should be presented as construction frameworks with
clearly marked conjectural next steps.

## D. Projective, paired-lobe, and dyadic five-comb theory

**Priority assessment: strongest new finite construction framework; high
confidence in the dependency-free theorems, provisional literature
confidence, solver-only confidence in the common-family exhaustion.**

The complete common-type projective quotient has rank nine. Row-sign
normalization gives exactly 4,096 maps and row-pair symmetries reduce them to
1,440 orbits. The complete physical modulo-four hole fiber is
label-independent, with 256 completions. Lags 83 and 82 fix the outer hole
geometry, and lags 81 through 78 reduce to a 10,934-row exact table whose
projective image has 2,434 rows.

All 48 complementary quartets and all 32 structural label cores were then
modeled with arbitrary type permutation, projective labels, orientations,
holes, all 83 aperiodic equations, and exact row norms. The 1,536 records are
all `INFEASIBLE`. The corpus is integrity-checked and source-pinned, but has
no independent UNSAT certificates. This is a clean restricted-family
computational claim, not a theorem about arbitrary five-comb packings.

The stronger contribution is constructive and dependency-free. For
same-word polarized carriers, self-cancellation is exactly an ordered pair of
complementary quartets. For distinct lower and upper lobe words used with
both polarizations, it is exactly one complementary octet. Exact
classification gives 1,246 octets and 768,512 sorted directed-pair
inventories, of which 721,984 lie beyond separate lower/upper quartets. The
rank-nine projective quotient and physical high-lag table survive unchanged.

Independently, all dyadic norm equations through order 16 are equivalent to
one periodic-autocorrelation identity for four length-16 integer
compressions. The root/bucket basis determinant is `-256`; physical parity
gives exactly 1,589 energy shells. These statements have standard-library
verifiers and independent audits. They look theorem-sized and are likely
worth a focused internal note, but a priority claim still needs broader
literature comparison.

A further `z=1` theorem eliminates structural projective core zero for every
carrier inventory, including the distinct-lobe family. Its labels force
carrier row sums `(x,x,y,y)`, while the physical hole fiber would require
165 or 166 to be a sum of two squares. This removes 128 of the 1,440
row-orbit representatives without trusting the common-family solver corpus.
The exact checker reconstructs the affected high-lag rows and all 768,512
paired-lobe root profiles. This is a clean supporting lemma rather than a
standalone existence result.

## E. Sextic order-six `LP(333)` quotient

**Priority assessment: promising new exact construction reduction; high
confidence in the repository derivation, provisional literature confidence.**

Invariance under multiplier 64 modulo 333 gives a `9 x 7` QPSK quotient on
the six cosets of `<2^6>` in `F_37^*`. There are 34 reversal-inequivalent
quotient lag equations. The zero column is necessarily an `LP(9)` word;
symmetry fixes its 972-element orbit and leaves 108 Boolean signs. The
remaining length-nine words have only 28 real-PAF signatures, and the
row-axis condition splits into 298 three-plus-three meet-in-the-middle
shards. The signature channel and a resume-safe shard runner are implemented.

After canonicalizing the zero column, the compression-preserving residual
symmetry is exactly the class rotation `C3`. It is induced by decimation 226
modulo 333; its cube is multiplier 64. The dependency-free verifier
reconstructs the complete 972-word normalization orbit, all 298 invariant
shards, and the physical correlation action. Of 1,658,700 compatible ordered
signature sextuples, exactly 18 are fixed and Burnside's lemma leaves 552,912
signature-level orbits. This count is not a full word-orbit or solution-orbit
count.

An explicit table satisfies every pure row and pure column equation, while
20 of 24 mixed quotient cells remain nonzero. The checker expands all 333
positions and reproduces the residual energy exactly. It also proves that
the quadratic-residue order-18 quotient and a logarithmically shifted
template are impossible. The 34 equations should not be called linearly
independent: fixed compression supplies seven affine relations.

This is a more compact current construction target than the quartic quotient.
It is not an existence result until an exact quotient is found and expanded
through the full `H(668)` verifier. The strengthened exact model has 2,979
variables and 2,923 constraints; a 20-second pilot remained `UNKNOWN` with no
candidate, so no negative result is claimed.

## F. Radius-18 exclusion around Eliahou's seed

**Priority assessment: superseded computational result; likely new, with
moderate confidence.**

Eliahou's 2025 paper constructs and verifies the 64-modular matrix and exposes
the structured seed, but does not report a Hamming-ball repair exclusion.
The current SageMath construction table still lists 668 as unknown, and the
recent public `LP(333)` status report pursues a different compression route.
No located source reports the same `BS(84,83)` radius-18 computation.

The repository's finite decomposition is unusually reproducible: it checks
the margin images, quad quotient, hashes, parent edges, root witnesses, and
the final primitive-7/14 eliminations.  Its important limitation is also
explicit.  OR-Tools CP-SAT does not emit independently replayable SAT/PB proof
transcripts here.  The artifact checker confirms that the recorded
`INFEASIBLE` statuses and all surrounding arithmetic are internally
consistent; it does not prove those statuses without trusting the solver.

If this older computation is ever released as an independent claim, regenerate
all 1,296 finite instances in a proof-producing format (for example CNF plus
DRAT/LRAT, or pseudo-Boolean plus VeriPB). Preserve the proof files, solver
versions, commands, checksums, and a small proof checker.
The existing checker independently validates the twelve decoded root
witnesses, but that witness replay does not certify the twelve subsequent
compression-target infeasibility claims.

The first certification prototype is complete.  Four representative leaves
(radius 16, shell 17, shell 18, and shell-18 primitive 7) regenerate to
deterministic CNF and pass `drat-trim`; final replay used 250 MB peak RSS.
This is 4/1,296 coverage.  One known feasible root model also passes an
independent positive-model checker with the symmetry quotient enabled.  In
addition, all twelve stored root witnesses extend to SAT models of their
exactly pinned, unquotiented v2 CNFs and pass every clause plus independent
mathematical checks.  A separate exhaustive contribution-signature regression
reconstructs all 83 endpoint quads and verifies the exporter's global root
orbit partition for every even four-bit mask.  The exporter also has small
exhaustive regressions.

A naïve batch is not currently responsible.  One hard raw-bit proof grew to
388 MB without finishing; z7+z14 strengthening timed out at 60 seconds and
peaked at 1.785 GB RSS.  The next bounded step is an exact orbit-count CNF for
the six hard root leaves, followed by a proof-size audit before any corpus run.

## G. Fixed-`q` reduction to `TU(41)`

**Priority assessment: likely new reduction; suitable as a theorem inside the
same paper.**

The parity telescope from a hypothetical fixed-`q` repair to
`BS(42,41)` and then `TU(41)` was not found in the searched literature.
Nonexistence at the endpoint is not new: Edmondson, Seberry, and Anderson
totally enumerated inequivalent Turyn sequences of long length below 43, and
their classification has none of long length 42.

The symbolic checker verifies the new reduction.  A separate independent
outside-in enumerator now reproduces the published endpoint: 461/461
canonical depth-five shards, 57,543,021 nodes, and zero solutions.  An
independent Python program exhausts all `2^19` assignments defining the shard
cover; ASan/UBSan regressions reproduce the known small cases at short
lengths 3, 7, and 9.  The computation supports the theorem while continuing
to credit the 1994 classification.

A previous draft also gave an invalid
sum-of-two-squares shortcut.  That shortcut has been removed:
for `BS(42,41)` the relevant identity is
`C^2+D^2=162=9^2+9^2`.  This correction does not affect the reduction.

A promising unproved extension is to test whether the same telescope works
for Eliahou's apparent family
`q_k=(16k+3,2,16k+1,1)`, reducing fixed-`q_k` repair to `TU(8k+1)`.
That is a research direction, not a claim in this milestone.

## H. Legendre-pair symmetry and profile results

**Priority assessment: mixed; supporting material only in its current form.**

The symmetric/symmetric obstruction is already subsumed by the public
modulo-3 multiplier obstruction: inversion is a multiplier congruent to 2
modulo 3.  It should not be presented as a new result.

No explicit prior statement was located for the normalized skew/skew
certificate `v^2+w^2=222` or the mixed certificate
`x^2+3y^2=667`.  These are clean and may be new specializations, but they are
elementary and narrow.  A general theorem for lengths divisible by three
would be more publishable than the isolated `333` cases.

The 21 compressed profiles are sampled, not exhaustive, and are a tiny subset
of a landscape for which the March 2026 status report claims an exhaustive
9-compression computation with 12,017,243 compatible configurations.  The
profile-4 and profile-19 finite-neighborhood results are independently
verified and computationally substantial, but they prove only local
minimality in explicitly defined move graphs.  They are useful validation
data and negative search evidence, not evidence that `LP(333)` is globally
impossible.

## Recommended paper and release plan

Maintain one compact internal paper organized around:

1. Eliahou's structured quadruple and its exact translation to `BS(84,83)`;
2. the adjacent cyclic-fold theorem and prime-83 oriented-SDS construction;
3. the primitive-eight 16-square reduction, fixed-`s` obstruction, and sharp
   distance-34 theorem;
4. the 2-adic/Frobenius reduction, rank-one comb factorization, and the two
   exact nonlinear no-go theorems;
5. the projective quotient, physical high-lag table, dyadic compression
   theorem, and distinct-lobe complementary-octet construction;
6. the sextic and quartic QPSK construction reductions;
7. the safe-prime Sidelnikov identity and orientation-fingerprint exclusion;
8. the fixed-`q` parity telescope and reduction to `TU(41)`;
9. the radius-18 solver report and proof-certification ladder as historical
   supplementary computation;
10. the Legendre inversion lemmas and local searches as appendices or
   supplementary experiments.

Use a title that states the local scope, such as *Exact local obstructions
around a 64-modular Hadamard matrix of order 668*.  Do not imply a
nonexistence theorem for `H(668)`, `BS(84,83)`, or `LP(333)`.

If the user independently decides to publish in the future, the remaining
priority checks are:

- obtain and inspect the full text of Shalom Eliahou's 2026
  [update on modular Hadamard matrices](https://doi.org/10.1007/s10801-026-01544-5);
- decide whether to omit the superseded radius-18 solver claim or upgrade its
  statuses to independently replayable certificates;
- freeze a tagged release with all inputs, hashes, versions, and checkers.

The independent `TU(41)` enumeration is complete.  Full-text access to the
2026 article was not lawfully available during this audit. No author contact
will be attempted; priority language must remain provisional unless lawful
public sources resolve the overlap question.

## Sources checked

- Shalom Eliahou,
  [A 64-modular Hadamard matrix of order 668](https://ajc.maths.uq.edu.au/pdf/93/ajc_v93_p422.pdf),
  *Australasian Journal of Combinatorics* 93(2) (2025), 422-427.
- Shalom Eliahou,
  [An update on modular Hadamard matrices](https://doi.org/10.1007/s10801-026-01544-5),
  *Journal of Algebraic Combinatorics* 64 (2026); metadata and abstract
  checked, full body unavailable in the audit environment.
- G. M. Edmondson, Jennifer Seberry, and M. R. Anderson,
  [On the existence of Turyn sequences of length less than
  43](https://documents.uow.edu.au/~jennie/WEBPDF/1994_03.pdf),
  *Mathematics of Computation* 62 (1994), 351-362,
  [doi:10.1090/S0025-5718-1994-1203733-8](https://doi.org/10.1090/S0025-5718-1994-1203733-8).
- Dragomir Ž. Đoković,
  [Classification of base sequences `BS(n+1,n)`](https://arxiv.org/abs/1002.1414),
  enumerating `n <= 30`, not the present `n=83` case.
- Przemysław Chojecki,
  [Computational Search for a Hadamard Matrix of Order 668 via Legendre
  Pairs of Length 333](https://www.ulam.ai/research/frontier-had.pdf),
  status report, March 2026.
- Ilias Kotsireas, Roberto Gallardo-Cava, Ana Isabel Gómez, and Domingo
  Gómez-Pérez,
  [On the search of binary Legendre pairs of length
  `pq^2`](https://doi.org/10.1016/j.jsc.2026.102606),
  *Journal of Symbolic Computation* 138 (2027), article 102606.
- Matteo Cati and Dmitrii V. Pasechnik,
  [A database of constructions of Hadamard
  matrices](https://arxiv.org/abs/2411.18897), 2024.
- [SageMath's current Hadamard construction
  documentation](https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/matrices/hadamard_matrix.html),
  which lists 668, 716, 892, and 1132 as unknown in its implemented range.
