# Priority audit updated 24 July 2026

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
2. the adjacent-42 fold proves a true base-row distance bound of 80 and a
   special-coordinate bound of 41, reducing the complete distance-41
   boundary to 39 reciprocal `q` pairs with two root profiles each; its
   complementary anti-fold removes endpoint orientation, collapses these to
   30 support instances, and has one independently certified exclusion;
3. a dependency-free primitive-eight reduction plus exact margin norms gives
   a separate sharp necessary-condition boundary at distance 34;
4. the exact 2-adic formulation reduces the first two special-construction
   layers to 169 structural bits and identifies a five-lag Frobenius-square
   obstruction with no first-order tangent repair; the full residual is one
   rank-one ten-sparse carrier, and two natural nonlinear comb completions
   are exactly excluded;
5. the projective five-comb quotient has rank nine, an exact physical
   high-lag boundary table, and a dependency-free dyadic compression theorem;
   its diagonal/common-type family is solver-excluded, while the
   distinct-lobe theorem exposes 721,984 larger inventories and the first
   primitive-eight vertical joins remove more than 70% of prior survivors;
6. a multiplier row-sum theorem closes the order-18, quartic, and sextic
   fixed-compression `LP(333)` families by exact integer enumeration, while
   proving that order three is the first viable boundary;
7. the independent fixed-`q` telescope reduces to the empty class `TU(41)`;
8. the surviving order-three `<10>` quotient has exactly 1,756 row-sum words,
   22 Eisenstein shards, a strict primitive-nine jet, an invertible
   characteristic-37 transfer, a labelled `F_729` field split, a rank-18
   pinned trit lift, an exact integral primitive-nine criterion, a
   five-independent-condition profile ideal, an exact full-LP zero-moment
   gate, a local-global CRT closure, a lossless prime-167 finite-field split,
   a 24-element formal symmetry reducing 22 targets to seven, and a
   three-fiber unit-phase factorization whose complete 39-component phase
   system is also lossless modulo 167 and splits into four parameterized
   finite-field cones; four exact shell theorems exclude
   `n_9=6,5,4,3`, and a fifth complete classification finds exactly five
   profile-zero symmetry orbits at `n_9=2`; the dense-shell quadratic
   correction algebra is `F_27 x F_27` and supplies an exact 729-character
   compression for `n_9=1,0`; the phase
   cone has an exact row-Galois/trace inverse, fixed-origin and
   profile-support cuts, a lookup-free binary physicality decoder, and an
   independent 13-factor mod-seven sieve; all 22 aggregate shards survive
   the ideal, but every stored ideal witness fails the zero gate, and the
   coupled `<121>/<211>` lanes share a separate exact 1,296-word boundary;
9. the safe-prime Sidelnikov calculation gives an exact prime-83 PAF identity
   and a 41-bit inverse-pair orientation obstruction that closes its
   degree-two independently decimated extension.

These results are worth preserving as a compact internal manuscript. Nothing
will be circulated, submitted, posted, or sent by this project. The
radius-18 CP-SAT corpus is now secondary: its uncertified leaves no longer
limit the stronger dependency-free adjacent-42 distance-80 theorem, though
they remain useful historical artifacts.

The openly available recent `LP(333)` papers and March 2026 status report
have been inspected.  The symmetric/symmetric observation is prior; the
skew/skew and mixed equations were not located but are incremental
specializations, not paper-leading results.  Project policy prohibits all
external outreach; no contact drafts or recipient lists are retained.

## A. Adjacent-42 and primitive-eight seed-distance obstructions

**Priority assessment: strongest likely-new theorem-sized result; high
confidence in the repository proof, provisional confidence in literature
priority.**

A July 2026 companion report already records the basic equivalence between
an exact lift in Eliahou's special form and `BS(84,83)`, an analytic raw
distance lower bound of 64, and a solver-backed distance-17 statement for a
128-modular lift.  The basic translation is therefore prior.  The
distance-80 theorem below is a strict improvement, and no counterpart was
found there for the adjacent-42/anti-fold structure or the special-distance
41 classification.

Reducing all four base rows modulo `z^42-1` reveals that Eliahou's thirteen
residual lags cancel exactly: the folded seed is periodically flat with
energy 14. Every exact `BS(84,83)` has folded energy 334. If `E` is the
number of equal separation-42 endpoint pairs, the folded energy is `2+4E`;
the target needs `E=83`, while the seed has only three. A single base-sign
change toggles at most one pair, proving a global base-row Hamming lower
bound of 80.

In special `(s,q)` coordinates this first gives distance at least 40.
Equality would consist entirely of `s` changes and keep `q` fixed,
contradicting the exact `TU(41)` reduction. Hence the special-coordinate
distance is at least 41. The complete distance-41 cost split leaves only
zero, one, or two `q` changes. Fixed `q` is closed; the unique single-`q`
center change fails at `z=-1`; and the two-`q` case must be one reciprocal
pair plus 39 `s` changes. Roots `+1,-1` reduce 80 shell-compatible pairs to
39, each with exactly two joined outer profiles. The minimum base shell is
equivalently an 80-sparse ternary norm equation in `Z[C_42]`. This is a much
stronger true repair-distance theorem than the earlier radius-34
necessary-condition bound.

The complementary reduction modulo `z^42+1` is the most important new
refinement of this boundary. On a seed-opposite separation-42 pair, either
endpoint flip zeros the same anti-fold cell. The 39 `s` changes therefore
become an orientation-free 39-cell support, and the 39 root-compatible
reciprocal `q` pairs collapse to 30 distinct support instances. Pair-sum and
pair-difference normalization gives a first affine lift over `F_2` of rank
exactly 21 in every reciprocal-`q` case, including support-weight parity.
Exact MacWilliams counts prove that this binary layer alone leaves many
supports.

Exactly one anti-fold instance is currently a certified exclusion:
canonical case 0, the long `q` representative 0. Its 39,580-variable,
127,589-clause CNF includes only redundant modulo-two and modulo-four
consequences of the exact integer equations. Standalone CaDiCaL produced a
binary DRAT proof, and independent `drat-trim` replay returned `VERIFIED`.
The checked proof package records formula and proof hashes, solver/checker
versions, and a standard-library artifact verifier. Canonical case 1, the
long representative 2, has one solver-UNSAT observation but no checked
proof; the other 28 distinct instances are `UNKNOWN`. Thus the anti-fold
theorem and the one certified leaf are suitable for the internal manuscript,
but they do not establish a distance-41 exclusion, `BS(84,83)`
nonexistence, or `H(668)` nonexistence.

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
fixed compression and every pure-axis equation, and the elementary Paley-row
lift is exactly impossible by a group-algebra denominator obstruction. The
later row-sum theorem now closes the entire fixed-compression quartic family,
so the old energy-112 constructor is a historical non-candidate rather than
a construction checkpoint.

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

The first dyadic root sieves add two exact but deliberately scoped filters.
At roots `+1,-1`, an arbitrary-placement relaxation rejects 2,576,920 of
1,864,410,112 weighted inventory-map products (0.1382%) but no complete
surviving core/profile cell. In the narrower vertical-pair slice, roots
`+1,-1,i` cumulatively reject 906,241 of 23,823,872 inventory/core products
(3.8039%) and eleven complete cells. The larger percentage is not valid for
arbitrary carrier placement. These are worthwhile supporting computations,
not a five-comb nonexistence theorem.

The vertical-pair slice now also has an exact primitive-eight coefficient
split. Writing the completed evaluation as `E+zeta_8 O` produces one
rational norm equation and one vanishing `sqrt(2)` coefficient. Retained
full joins reduce core 4 from 724,564 previous survivors to 140,007 and core
27 from 229,408 to 65,868. The additional rejection rates are 80.6771% and
71.2878%. These percentages remain vertical-pair-only, and the current join
still relaxes compatibility between the even and odd high-lag projections.

## E. Multiplier row-sum obstruction and order-three boundary

**Priority assessment: compact independent fixed-compression proofs now
subsumed by stronger July 2026 full-family exclusions; the order-three ID3
front end and its deeper algebra remain potentially new.**

Ramos, Hulak, and de Queiroz now prove that all fixed common-multiplier
subgroups of order at least nine are impossible at length 333, together with
one order-four and one order-six subgroup.  Their paper IDs 20, 12, and 8
strictly contain the column-only `h=18,9,6` families below because the public
theorem does not assume our prescribed length-37 compression.  The present
enumerations are therefore retained as compact independent proofs and as the
front end of the surviving order-three chain, not as headline novelty.

For a fixed-compression column-only multiplier subgroup `H` of size `h`, sum
all 37 column-lag equations. If `x` is the zero-column word, `t` is the
pointwise sum of the nonzero class words, and `s=x+h t`, every candidate must
satisfy

```text
Re PAF_s(0)=297,       Re PAF_s(a)=-37  (a=1,...,4).
```

The zero-column equations leave exactly 972 QPSK words, one free
normalization orbit, all with nonzero real PAF `-1`. After fixing a canonical
core, a small nonnegative integer energy census is complete. It has no state
for `h=18`; for `h=9` it has 40 states and 29 PAF profiles but no target; for
`h=6` it has 2,376 states and 971 profiles but no target. Replaying all 972
cores gives 38,880 quartic and 2,309,472 sextic states with zero hits. This
closes all three restricted families exactly and supersedes their bounded
CP-SAT searches, but the conclusions themselves are now subsumed by the
stronger public full-family results.

Here `h=3` is the first surviving member of this particular column-only
fixed-compression chain `H_18 superset H_9 superset H_6 superset H_3`; it is
not a statement that all larger multiplier families were first excluded
here.  Public paper ID3, `H_3=<10>`, remains open.  At `h=3`, the same
projection is feasible. A warning-clean dependency-free
C++ enumeration checks 46,503,026 energy-and-sum words and finds exactly
1,756 full row-sum PAF words. Every word admits the exact zero-column
signature lift. After complementing the high-weight binary channels, that
lift is equivalent to 24 three-subsets of `Z/9` with signed incidence
margins and four cyclic difference totals equal to 18. The complete
1,756-word histogram audit has no unresolved or infeasible row and therefore
proves that this pure-axis layer does not prune the catalog.

The nontrivial three-row Fourier channel has a second exact factorization.
Each 100-state Gaussian class catalog is a product of two ten-state binary
profiles, and the compressed system becomes a complementary pair of
`H`-invariant Eisenstein sequences with energy 167. Seven of the original 20
real equations are fixed-sum dependencies, leaving 13 independent integer
conditions. The 1,756 rows collapse to 22 aggregate shards in six norm-pair
types. A local ramified-prime sieve keeps 3,334/10,000 choices per opposite
class pair, but all 22 shards have pinned surviving witnesses. This is a
clean structural theorem and useful solver reduction, not an obstruction by
itself.

A primitive-nine ramified expansion restores information erased by the
three-row profile. In `F_3[pi]/(pi^6)`, `pi=1-zeta_9`, the zero-column power
is 5 and the defect `167-5=162` has integral `pi`-valuation 24. The first jet
digit is exactly the 3,334/10,000 Eisenstein pair sieve; digits two through
five contain new nonzero/nonzero class products. A pinned local survivor
first fails digit two, proving that the higher digits are strict. No complete
row-sum catalog entry is yet excluded, so this is a theorem-sized propagation
layer rather than a negative result.

The fully labelled jet has an exact semisimple column-algebra split

```text
F_3[C_37]^H ~= F_3 x F_729 x F_729.
```

Column negation is the third Frobenius iterate in both field factors. Lucas'
theorem fixes jet digits zero through two from the residue profiles, while
the square-zero ideal `pi^3 R` makes digits three through five linear in
within-residue placement. A pinned row-695 lift passes all 222 mod-three jet
equations and four exact row-direction equations. This is an explicit
survivor, not a catalog exclusion.

For the same pinned profile tuple, the upper placement data has an exact
54-trit parameterization. Its affine jet system has rank 18 and nullity 36
before the integer margin and row-correlation constraints. A reduced model
produced a second fully labelled certificate, independently replayed through
the same 226 equations. The rank statement is profile-specific and should
not be generalized to all 1,756 rows.

The exact cyclotomic-integer layer is strictly stronger. Since
`Phi_9(x)=x^6+x^3+1`, primitive-ninth-root vanishing for each column lag is
equivalent to equality of its three correlation counts at row lags separated
by three. This yields 72 new displayed integer equations outside the zero
column. Both pinned modular certificates fail all 36 nonzero
column-class/residue groups, although every defect is divisible by three.
This proves strictness on actual labelled lifts, not infeasibility of row
695 or any catalog row.

The exact integer condition also has two new low-dimensional forms.  Before
within-residue placement, each nonzero profile Fourier coefficient must lie
in the Eisenstein ideal

```text
3(1-omega) Z[omega].
```

Reversal gives six displayed tests and the aggregate moment makes one
dependent, so only five new finite-ideal conditions are independent.  A
passing profile tuple uniquely determines all 36 exact correlation targets.
All 22 earlier characteristic-37 witnesses fail this ideal, but a complete
certificate corpus supplies a different passing profile tuple for every one
of the 22 aggregate shards.  The result is therefore a strict
assignment-level filter, not a shard exclusion.

The full Legendre equation imposes a stronger profile condition.  Its
adjusted plus-support intersection is 167 at every row lag, so the
order-three Fourier correlation must satisfy `D_t=0` on all thirteen column
parts.  Exact replay excludes every stored ideal-compatible tuple: one fails
on ten nonzero classes and 21 fail on all twelve; the original row-695
profile and stored same-shard witness both fail all twelve.  This is a useful
correction and an exact 22-object audit,
but it excludes no aggregate shard and the equation itself is the existing
full Eisenstein channel rather than a newly discovered general identity.

The zero gate now has two exact finite closures.  Combining the
`(1-omega)^3` profile ideal with the complete characteristic-37 transfer
puts any residual in `37(1-omega)^3 Z[omega]`; its least nonzero norm,
36,963, exceeds the universal Cauchy bound 27,889.  More strongly, on total
energy 167, reduction modulo 167 is already lossless: equality in Cauchy
would force a nonzero order-37 translation eigenvector whose energy is
divisible by 37, contradicting 167.  The order-three invariant algebra then
splits explicitly as

```text
F_167(omega)[C_37]^H = F_(167^2) x F_(167^12) x F_(167^12),
```

with a checked involution, inverse CRT, and complete parameterization of the
two-channel modular complementarity cone.  Together with the full phase
extension below, the prime-167 program is the strongest likely-new
contribution in the order-three lane.  Its proof is short and general, its
finite-field structure is mechanically replayed, and it is worth a focused
internal write-up.  Literature priority remains provisional, and it does
not supply a small-alphabet profile point.

The spectral-unit refinement is a substantive strengthening on the actual
profile alphabet.  A primitive Fourier value lies in the degree-24 field
`Q(omega,zeta_37)^H`; its absolute norm is the product of twelve positive
spectral energies, each strictly below 167.  Either prime-167 primitive
coordinate vanishing would instead make that norm divisible by `167^12`.
Therefore both channels are CRT units, the unitary ratio `A B^(-1)` is
always legal, and the four ambient cone branches collapse to one torus on
physical candidates.  This is worth including as a central lemma in the
focused prime-167 write-up.  It remains a structural reduction rather than
existence or nonexistence evidence.

The exact sparse-shell theorem is the strongest direct profile-space
exclusion so far.  Opposite-quartet geometry and divisibility of every
norm-nine letter by 3 make the two highest-energy sectors linear modulo 9.
Only 552 words in `(n_9,n_3,n_0)=(5,3,16)` and 288 words in `(6,0,18)`
reach detached all-37-lag replay, and none is exact.  Independent exhaustive
quartet enumeration, a separate weighted DP, sanitizer runs, and external
hashes confirm the result.  This appears potentially new and is suitable as
a theorem in a focused order-three write-up: it eliminates two of seven
complete type sectors, not merely sampled profiles.  Its scope remains
restricted—five sectors, the labelled phase lift, and `H(668)` are open.

The prime-163 extreme-sector theorem is a genuine exact pruning result, but
its proper publication role is supporting rather than headline.  The
factorization
`163=(14+3 omega)(11-3 omega)`, cyclotomic Frobenius order 12, Kronecker
unit rigidity, and Fourier inversion combine to forbid
`A A^*=163 delta_0` with `A(0)=-1`.  This eliminates 1,617,192 locally legal
assignments in each of the two norm-pair `(163,4)` targets.  The ingredients
are classical; the application and exact sector census appear useful and
potentially new, but literature priority is provisional.  Because
nonextreme `(37,130)` local witnesses remain, this is neither a whole-shard
obstruction nor existence/nonexistence evidence for `LP(333)`.

The sparse-`B` relative-norm screen is a useful follow-on lemma.  In those
same two targets, normalized `B`-energy six has only 396 structural words.
Total positivity and the quadratic CM norm equation reduce them to 17 field
types; exact odd valuations at inert primes over 11 and 101 rule out 13
types, or 312 words and 26 of 34 lift-safe orbits.  A guaranteed cyclic
`rnfisnorm` replay shows that the other four types are genuine field norms,
so 84 words remain.  The finite classification and local certificates appear
new in this setting, but the underlying Hasse-norm and inert-valuation tools
are classical.  This belongs as supporting exact pruning, not as a headline:
relative-norm solvability does not produce a physical complementary
`A`-profile and the sector remains open.

The exact profile equation also has formal symmetry
`C6 x C2_A x C2_B`.  It gives seven target orbits, but only
`C6 x C2_B` transports the canonical labelled zero words, leaving twelve
lift-compatible orbits.  This distinction prevents an invalid quotient at
the phase stage.  A deterministic 24-variable constructor implements the
seven formal targets with exact quartet states, full target stabilizers,
direct zero equations, semantically pinned atomic checkpoints, and detached
  exact replay.  It now applies the independently verified shell cut
`n_9<=2`.  No long campaign has been run on the hardened model, and
solver-reported exhaustion would still require a proof-producing SAT/PB
translation.  The symmetry theorem is useful supporting mathematics; the
constructor is research infrastructure, not publication evidence.

The profile energy equation has now yielded four complete shell exclusions.
The `n_9=6` endpoint reduces to 288 aggregate-compatible assignments and
twelve symmetry orbits.  At `n_9=5`, the local quartet equation forces all
three norm-three letters into one quartet; an affine modulo-nine join reduces
34,634,136 aggregate/local assignments to 552 exact replays.  At `n_9=4`,
the six norm-three letters occupy only `2+2+2`, `3+3`, or `4+2` quartet
patterns; a streaming enumeration checks 27,468,720 oriented frames and
345,984 exact-aggregate modulo-nine survivors.  Exact integer correlation
rejects every survivor in these three shells.  At `n_9=3`, a
signed-uniformizer skeleton quotient leaves 38,296 canonical skeletons and
479,850 modulo-nine/exact-aggregate survivors.  Only two survive modulo 27;
both fail an independent cubic characteristic-37 moment, and detached exact
replay rejects all 479,850.  Thus the four shells prove `n_9<=2`.

This sequence is new-looking and mechanically complete.  It is worth
including as a supporting theorem package because it demonstrates a
nontrivial descent through adjacent energy shells without a general-purpose
solver.

The complete `n_9=2` continuation is more significant than another
exclusion: it finds exactly five genuine profile-zero symmetry orbits after
14,715,744 raw signed skeletons and 10,201,038 detached exact replays.  Their
orbit sizes are `24,12,12,12,24`; one has medium-support partition `222222`
and four have `422220`.  All five pass independent all-37-lag,
characteristic-37, prime-167, aggregate, and orbit checks.  Each then has 54
placement trits with first Hensel rank/nullity `18/36`.  This appears to be
the first exact classification of this structured profile shell and is
publication-worthy as part of the order-three theorem package.  It remains
a quotient-level classification: none of the five is yet an `LP(333)` or a
Hadamard matrix.

The complete next placement digit strengthens the internal theorem package
but weakens its value as a construction milestone.  On each of the five
orbits the first digit leaves `F_3^36`; the next digit has eighteen
independent quadratic polar forms.  Six structured combinations are the
row-residue layer of a ramified `F_27 x F_27` coordinate algebra, and exact
quadratic Fourier inversion proves that their map onto `F_3^6` is
surjective, with every fiber close to `3^30`.  The companion common-centroid
calculation has rank 1,295 in 1,296 endomorphism variables, so only scalar
endomorphisms survive and a free rank-two ramified-module Hensel lift is
impossible.  These are new-looking structural results, not evidence that a
full labelled lift is near: a lone second-digit witness would be expected
to be abundant.

For the remaining `n_9=1,0` shells, the six first quadratic correction forms
generate the exact algebra `F_27 x F_27`, with projective ranks 12 and 6 and
sum `2I`.  After the true local and aggregate affine rows are imposed, Gauss
bounds show that this radial combination attains every right-hand side on
every nonempty fiber.  This rules out a tempting anisotropy shortcut, while
giving a lossless 729-character count for the complete six-coordinate
quadratic map.  The algebra theorem and compression are likely useful
supporting results; the surjectivity statement is not an existence result
for a profile, and the two dense shells remain unclassified.

After profiles are fixed, every active residue fiber is a signed cube root
of unity.  The identity `active=3-Norm/3` shows that total profile norm 54
forces exactly 54 Eisenstein phases for every viable tuple, while the fixed
zero column makes physical frame energy 167 automatic. The primitive-nine
equation becomes one six-sequence periodic complementary-frame identity plus
one directed cross-fiber identity. The third cubic-basis equation is the
adjoint of the second. This explains the 36 independent mixed-column integer
conditions and provides a materially smaller exact architecture for the next
labelled lift. It is a structural factorization, not yet an obstruction.

The entire phase factorization is now lossless modulo 167 as well.  For the
diagonal equation, Cauchy equality would make support a union of 37-cycles.
For the directed cross equation, the twisted three-fiber operator has orbit
length 3 at zero column lag and 111 otherwise.  Support 167 is divisible by
none of these, so modular vanishing forces exact vanishing coefficient by
coefficient.  In `F_(167^2) x F_(167^12)^2`, the three primitive equations
form the annihilator of a three-dimensional twisted orbit plane.

Recombining the three fibers over the irreducible ninth-root field gives the
stronger semisimple presentation

```text
F_(167^6) x F_(167^12)^6.
```

Star pairs the six primitive factors, reducing all 39 prime-field component
conditions to one Hermitian cone over `F_(167^6)/F_(167^3)` and three
bilinear cones over `F_(167^12)`.  The direct ninth-root bridge, six factor
orbits, rank-13 invariant CRT, universal star action, generic and both-axis
parameter recoveries, branch exhaustiveness, and solution counts are
independently checked.  This is theorem-sized structural progress and should
lead the order-three portion of an internal paper.  It parameterizes the
modular norm cone, not the sparse zero/unit inverse-CRT intersection, so it
is not an existence result.

The physical zero/unit alphabet removes almost all coordinate-degenerate
phase branches.  The same twelve-factor norm gap shows, fiber by fiber, that
a primitive prime-167 coordinate vanishes exactly when the physical word is
zero, and then both primitive coordinates vanish together.  Five words are
forced nonzero at the fixed column, so only the dense and synchronized
`B0`-zero support strata survive: 4,094 of 4,096 ambient joint patterns are
impossible, and the latter stratum has plane rank at least two.  This is a
clean supporting lemma for the phase-algebra write-up.  It does not make the
two surviving inverse-CRT intersections small enough to enumerate and is not
an existence or nonexistence result.

The physical intersection now has three further exact reductions.  First,
the trivial coordinate of either binary channel cannot vanish: its vanishing
would make the nine row margins period three, contradicting their total 167.
The complete row-sum catalog leaves only 1,411 exact nonzero coordinate
pairs, rather than the abstract `167^3+1` norm-minus-one ratios.  Second, a
three-by-three row-Galois inverse recovers the six original fiber CRT triples
from the four cone blocks, and weighted traces recover every physical class
coefficient.  This supplies twelve independent fixed-origin linear
equations, five additional displayed profile-support equations after the
known total, and an if-and-only-if physical decoder: the nine inverse
ninth-root DFT coordinates must be idempotent.  Third, reduction modulo seven
splits the cyclic algebra into thirteen scalar factors over `F_(7^3)`, with
exact 1/9/27 local alphabets and a compact multiplication encoding.

The row-Galois, trace, Parseval, and physicality results materially sharpen
the four-cone theorem and belong with it in an internal write-up.  The
mod-seven factorization is a useful independent sieve and architecture
audit, but is not paper-leading by itself: it does not beat the known
profile-enumeration barrier without another structural reduction.

At the trivial `C_37` character, the six phase sums admit a further exact
transfer: one integer energy and one Eisenstein cross term per channel.
Object-by-object comparison, including multiplicities, proves that this is
exactly the existing 1,756-word row-sum gate in phase coordinates.  It is
valuable search architecture, with reductions of roughly 160,000--321,000
on the diagnostic fixtures, but it is not an independent obstruction or a
publication-leading result.

Two further phase filters are exact but subordinate.  The first
`(1-omega)`-adic digit is affine over `F_3`; it gives 21 rank-18 systems and
one explicit rank-`(16,17)` contradiction on the stored corpus.  The
augmentation-plus-first-characteristic-37 diagonal prefix compresses each
sequence to at most 444 states and the six-sequence join to at most 666, but
all 22 tuples survive it.  Since every one of those tuples already fails the
upstream zero-moment gate, neither census is new exclusion evidence.  The
affine and small-state decompositions are useful methods for a future
zero-moment profile, not standalone publication claims.

There is now a second exact coordinate system at the prime 37. In
characteristic 37, the logarithm `x=exp(u)` turns inversion into `u -> -u`;
order-three invariance kills all moments except multiples of three. With
`v=u^3`, the complete invariant group ring becomes a 13-dimensional
truncated polynomial algebra, and the mixed equations are one norm identity
through degree twelve. The transfer matrix has rank 13 and determinant 11,
so this is equivalent to the full invariant correlation system modulo 37,
not a lossy filter. A 373-fixture audit replays 4,476 physical/cyclotomic
equations. Exact witnesses show all 22 shards survive the first two
nonconstant transfer coefficients joined to the aggregate, energy, and
local mod-three conditions; every pinned witness fails later coefficients.
The theorem is substantial, while the first two layers alone are not an
obstruction.

A frozen lift expands to a `9 x 37` quotient and passes compression, row-sum,
and zero-column equations, but fails 51 of 54 independent nonzero-column
equations. The full `9 x 13` order-three quotient model imposes all 58
reversal-independent equations on 216 primary sign bits and independently
replays any assignment through all 333 lags and the bordered order-668
matrix. Its baseline has 11,790 variables and 11,657 constraints; the
complete corrected `C6 x C2` symmetry leader has 11,857 variables and 11,889
constraints. The B-only involution is the affine action with multiplier 323,
while the initially tempting multiplier 260 is explicitly falsified by a
PAF counterexample. A 60-second full-group pilot remained `UNKNOWN` with no
candidate and carries no negative implication.

The row-sum obstruction is likely worth publishing as a supporting theorem:
it converts two formerly promising construction searches into exact no-go
results and identifies a sharp viable symmetry boundary. The 1,756-word
order-three reduction is a research framework rather than an existence
result until the mixed equations are solved.

The two coupled subgroups `<121>` and `<211>` also admit a common exact outer
theorem. Row invariance gives a positive-definite five-value equation with
36 Gaussian solutions, 12 realizable repeated-row pairs, 6,048 generic row
words, and exactly 1,296 words after the invariant zero column and fixed
margins. They form 108 extended outer classes. A 21,953-state exact DP proves
all 1,296 survive both zero-column-lag equations. A nonadditive exponent
reversal bijections the two multiplier spaces through this entire row-axis
layer but not through mixed lags. This is a useful sharp boundary, not an
obstruction.

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

1. Eliahou's structured quadruple, crediting the contemporaneous public
   report for the basic exact-lift equivalence with `BS(84,83)`, followed by
   our strict distance-80 improvement over its distance-64 bound;
2. the adjacent cyclic-fold theorem and prime-83 oriented-SDS construction;
3. the adjacent-42 energy fold, distance-80/distance-41 theorems, and the
   39-pair minimum-shell frontier, followed by the orientation-free
   anti-fold, rank-21 binary lift, and one certified case-0 exclusion;
4. the primitive-eight 16-square reduction, fixed-`s` obstruction, and sharp
   distance-34 necessary-condition theorem;
5. the 2-adic/Frobenius reduction, rank-one comb factorization, and the two
   exact nonlinear no-go theorems;
6. the projective quotient, physical high-lag table, dyadic compression
   theorem, distinct-lobe complementary-octet construction, and scoped
   primitive-eight vertical census;
7. the archival compact multiplier row-sum proofs, with the stronger July
   full-family exclusions credited, and the still-open order-three
   difference-family, Eisenstein, primitive-nine,
   characteristic-37, labelled-field, trit, exact-integral, profile-ideal,
   profile-zero, top-four energy-shell exclusions, prime-167 split, exact
   symmetry, unit-phase, lossless full-phase four-cone factorization,
   trivial-branch obstruction, factorwise trace/Parseval inversion,
   lookup-free physical decoder, mod-seven cyclic sieve, and coupled-lane
   boundaries;
8. the safe-prime Sidelnikov identity and orientation-fingerprint exclusion;
9. the fixed-`q` parity telescope and reduction to `TU(41)`;
10. the radius-18 solver report and proof-certification ladder as historical
   supplementary computation;
11. the Legendre inversion lemmas and local searches as appendices or
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

- Arthur F. Ramos, David B. Hulak, and Ruy J. G. B. de Queiroz,
  [Multiplier obstructions for Legendre pairs of length
  333](https://arxiv.org/abs/2607.20765), arXiv:2607.20765 (22 July
  2026), together with its
  [proof-artifact repository](https://github.com/Arthur742Ramos/hadamard-668-multiplier-obstructions).
  Its full-family exclusions subsume our fixed-compression paper IDs
  20/12/8, while paper ID3 `<10>` remains open.
- The same release's
  [Eliahou mod-64 report](https://raw.githubusercontent.com/Arthur742Ramos/hadamard-668-multiplier-obstructions/main/mod64/report.md)
  and
  [fixed-field compression note](https://raw.githubusercontent.com/Arthur742Ramos/hadamard-668-multiplier-obstructions/main/compression_theorem/theorem_note.md).
  These establish priority for the basic `BS(84,83)` lift translation and
  general fixed-field framework, but not the present distance-80 or
  order-three profile algebra.
- [Determining the group that sends each Legendre pair to an equivalent
  Legendre pair](https://arxiv.org/abs/2604.22423), arXiv:2604.22423
  (2026), checked before making priority claims for formal equivalence and
  lex-leader machinery.
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
