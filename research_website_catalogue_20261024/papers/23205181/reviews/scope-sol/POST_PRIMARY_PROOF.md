# Full-original scope proof after source-first freeze

2026-11-17 UTC. This continues the immutable HAND_PROOF.md. It is an
independent parameter-and-interface reconstruction, followed by direct
reading of the actual pinned primary sections; it is not a new blind
family after that exposure. No current peer/root finding was opened.

## 1. What the threshold proves

For every inverse pairing permitted by the native model, a row originating
in E excludes one S successor, a row in S excludes one E successor, and a
row in O excludes one O successor. The counts in the 3-by-3 quotient are
therefore exact, without any assertion of independence of consecutive
turns. A class-constant positive vector is a vector on the full alphabet.
For any nonnegative matrix M and f>0, Mf<=lambda f bounds its spectral
radius by lambda in the weighted sup norm. Thus this use does not require
an irreducibility hypothesis hidden outside the quotient. Conversely,
Mx>=mu x>0 implies ||M^h x||>=mu^h||x|| and rho(M)>=mu. The actual word
sum is 1^T M^(h-1)1, including the zero contributions of nonreduced words.

The nine strict lower cross-multiplication margins and three strict upper
margins, exact row ratios, prefactors, and h=1 boundary were derived in the
sealed HAND_PROOF.md. They prove growth at 4, 8, 16 and contraction at 32;
these exhaust the smaller dyadic orders in the theorem's domain q>=4.
No monotonicity theorem or floating eigenvalue is needed to establish the
least order. The stronger claim that every q>=32 contracts is not needed
for the stated least-order conclusion. The q=2 congruence obstruction is
a separate obstruction to the unchanged vertex-count prescription, not a
global nonexistence result.

The Perron-vector equality rho(M)=rho(Q) in the manuscript is also sound:
a positive Perron vector of the strictly positive Q lifts, while the
weighted-norm argument bounds every eigenvalue of the whole M by that
same eigenvalue. Dependence on which ordinary points mate with the extras
does not enter these counts.

## 2. Actual q=32 random law and prescriptions

I read the complete random.tex primary, not a statement that its q=128
theorems automatically generalize. At q=32, m=1 mod 4 makes both
(33m-1)/4 and 33(m-1)/4 integral. For each side separately, ordinary and
extra letter occurrences are respectively 33m and 33(m-1). Therefore
the two slots of each inverse pair have equal cardinality within that
side. No matching between A and B is assumed. Balanced per-line quotas
have total demand (33/604)m+O(1)<m-1 for sufficiently large m, even with
the reserved A root. The uniform O(1) in mixed turn counts follows from
seven fixed balanced distributions over 1057 line classes; its constant
does not grow with m. Parity is independent of chosen matching because
it concerns prescribed label sets. All ordinary line intersections are
odd (1 or 33), Fano-complement intersections are even, and the full-seven
self-intersection occurs at exactly the distinguished root. Degrees
are 33, 37, 40.

The random variables are independent uniform bijections within the fixed
inverse pairs on each side, before girth conditioning. The native proof's
switch is on two matches of one such bijection. It preserves the types
and the already prescribed matches; being distant by >2L prevents a new
short cycle. A reversal of the switch is uniquely recovered from the new
images of x and preimages of y, including overlap of the two slot sets.
This is a counting injection, not an assumption of independence after
conditioning. The conditioned bound applies for each feasible prefix;
an infeasible prefix has probability zero.

Let A0=2|T|/p. With q=32, A0<2^17 and d*=40<2^6. Taking c0=1/100,
c0 log A0<17/100 and 2c0 log d*<12/100, since log 2<1. Thus the expected
number of bad edges is O(log(n) n^(17/100))=o(n), and excluding distant
edges for a switch costs O(40^(2L+2))=O(n^(12/100))=o(n). Initial bad
edges can be removed because each bijection has np-O(1) matches, so
the conditioned sample space is genuinely nonempty for sufficiently large
admissible m. Quantitatively, r_n=33+O(40^(2L+2))=o(n). For fixed C1 and
E<=C1L, multiplying the per-edge bounds gives
(np)^(-E) exp(O(E(E+r_n)/n))=(np)^(-E) exp(o(L)). This is uniform over
the needed short patterns; it is not extended without proof to an
arbitrary linear-size E.

## 3. Linear exposures, expansion, and closures

For a k-set failing factor-two expansion, its 33k half-edges force at
least r=ceil(33k/2) distinct edges within an enlarged 2k-set. Thus
16.5k<=r<=17k. For a fixed 2k-set, there are at most 4|T|k^2 possible
prescriptions. The binomial bound gives (C2 k)^r with
C2=8 e |T|/33. If k<=eta n and 17eta<p/4, all r sequential denominators
are >=np/2 once n is sufficiently large because r_n=o(n).

Writing x=k/n<=1 and D=2C2/p>1, the union bound is at most
(e/2)^(2k) x^(-2k) (D x)^r
 <= ((e/2)^2 D^17 x^(29/2))^k.
Both inequalities r/k>=33/2 and r/k<=17 are used: the former on x,
the latter on D. This checks the rounding rather than replacing r by
one real exponent in both factors.

For eta=10^-6, use e<3 and D<48*1064*1057/33^2
=53983104/1089<50000. Then C3 eta^(29/2) is bounded above by
(9/4)*50000^17*10^-87 =6866455078125/(4*10^19)<1/2.
Also 17eta<p/4 follows from 71876<33000000. This is a concrete check
on the otherwise unspecified small fraction, without claiming a numeric
threshold n for all o(n) errors. For k<=sqrt(n), the sum is bounded by
a geometric series with base C3 n^(-29/4)->0; for larger k<=eta n the
tail is at most sum_{k>sqrt(n)}2^-k->0.

On this expansion event each radius R=ceil(log_2 n)+1 ball has more
than eta n vertices. Spacing centers by 2R+1 on a geodesic makes their
radius-R balls disjoint; at most 1/eta such balls fit in a side. The
diameter is therefore O(log n)=dL, with a freshly chosen finite d.
No connectivity of an entire side is claimed or required.

The planar closure proof deletes at most two edges at a basepoint;
every remaining vertex has degree at least 31, hence at least three.
At least 3*2^(k-1)>n nonbacktracking k-walks start there for
k=ceil(log_2 n)+1, so two end together. Reducing their difference
leaves a nonempty based immersed loop, because the equal-length walks
were distinct. Its first and last edges avoid the deleted ones. Joining
an immersed segment with two such loops and a shortest return path
preserves all original occurrences and costs at most dL+4k. This
recovers D0>=d+8/(c0 log 2)+8. There is no residual use of degree 129.

## 4. Bounded paths: the multiplicity and quantifier interfaces

The entire patterns.tex proof was read. Its small-image rank estimate
depends only on girth L and size CL: after pruning and suppressing,
a minimum-degree-three graph with r weighted edges has enough short
nonbacktracking walks to force r<=4C(ceil(log_2(8r))+1). Thus r is
bounded independently of n. Marked chains and traversal multiplicities
are bounded for each fixed K0,C,I, and their integer length choices
have polynomial entropy in L.

The stage inequality is a concrete incidence statement: at a vertex,
all traversal incidences except the two possible interval endpoints
pair with another half-edge. Hence 2 max_e m_e<=sum_e m_e+a(z), giving
sum_j V_j<=H+iota and sum_j(V_j-E_j-k_j)<=0. The fixed root is counted
only at stage one. This pays for the possible rooted interval without
assuming all paths are cyclic or that all stages are independent.

The common near-grid argument has s->infinity and s=o(L), with an
o(1) fractional displacement for all finitely many comparison offsets.
Its omitted end and grid fragments cost o(L), uniformly for a fixed
pattern complexity. Self-translation links have a nonzero step because
paired positions must use distinct underlying edges; their equality
graph is a forest with only O(kappa s) free letters. A self-reflection
would have either a fixed inverse letter or an adjacent inverse pair
in its central overlap, incompatible with the inverse involution and
reducedness. Non-self-linked components obey 2z<=S+b by counting the
distinct occurrence partners of a maximum-multiplicity block.

Minimum positive turn weight at q=32 is 1/33 (p=33/1057>1/33);
therefore log-weight bins have an upper linear bound a0s. The exact
q=32 word decay gives their lower bound delta s/2 and cardinality
exp(2d-delta s). At each stage, vertex-turn counts times conditional
edge prescriptions bound the expected number of injective realizations
by n^(V-E-k) exp(-sum d+o(L)). Restricting to assignments that extend
across the whole linked component permits the minimum-bin block to
count even if absent from that stage. This avoids multiplying unrelated
word counts.

Combining deterministic first-moment upper bounds B_j yields
log product B_j <= -delta H/2+a0 b0+o(L). Choose
epsilon=min(1/4,delta/(16(1+a0))) before K0,C,I. Some stage then has
B_j<=exp(-delta H/(4M)); Markov at that single stage is sufficient.
There is no probability-product/independence inference. Pattern entropy
exp(o(L)) is beaten by that fixed positive exponential rate.

## 5. Unbounded arrangements to the fixed bounded system

The complete planar.tex extraction fixes constants in this order:
types,c0,delta; epsilon,d; D0; U; eta_separator; K0; C,I; then n.
The separator fraction here is distinct from the small-set expansion
fraction above. U>=96D0/epsilon makes total appended closure length
<=epsilon H0/32. Euler's identity for the regular neighborhood works
even for disconnected pairings: sum(ell_Q-2chi(Q))=2N0-4. Monogons
are excluded except at the single exceptional break; marking opposite
good digon gaps produces at most 6N' comparison pairs.

After recursive planar separation, deleted original positions cost
<=2 eta_separator U H0, and a surviving occurrence loses at most one
partner per deleted occurrence. Hence total unpaired length is
<=epsilon H0/16, retained length >=15H0/16, and interval pairs
<=12H0/L. Discarding clusters with excessive unpaired ratio loses
<=H0/16, and excessive comparison density loses <=H0/16. The sole
possible cluster of length <L is an intact exceptional interval; the
presence of an ordinary boundary of length >=L ensures this last loss
is <H0/2. At least 5H0/16 positive length remains. One cluster thus
has L<=H<=CL and the exact fixed (K0,C,I) previously chosen. This
reduction treats every finite arrangement, not just finitely many
preselected arrangements, without a union bound over all their sizes.

## 6. Deterministic topology and the scalar products

The complete topology.tex proof is independent of q. Replacing each
abstract cone by graph basis relator disks is a relative equivalence:
the filled graph is simply connected and acyclic, hence contractible,
and both inclusions are CW cofibrations. A minimal cone picture
representing either a nonzero sphere or a null root-to-distinct-vertex
path has positive immersed boundaries. Preimages of rose midpoints pair
inverse letters. If a pair traverses the same graph edge, the band
lifts through the same abstract cone and decreases total boundary
length by two. In the exterior case the retained component contains
the marked break, preserving graph endpoints. In the inner-splitting
sphere case, cap both sides through the SAME lifted cone; their H2
classes sum to the old nonzero class. At least one remains essential.
This does not assume that the cone image embeds as a contractible
subset. Hence either failure would create precisely the excluded
reduced spherical arrangement. The figures are not cached here; the
complete verbal surgery, word, and lifted homology arguments suffice
for these interfaces, and no claim of inspecting those figures is made.

Once pi2(X)=0, the simply connected two-dimensional universal cover is
acyclic and contractible. A finite-order element would give a prime-order
cyclic subgroup with a finite-length free resolution, contradicting its
nonzero mod-prime cohomology in every degree. Thus the finite cone group
is torsion-free. Killing graph component cycles adds no rose generators;
there are 1064/2=532 geometric rose edges.

The complete algebra.tex calculation is a finite parity argument on
A' x A' and A' x B', not a claim that their vertices all have different
group labels. Each simultaneous-step component contributes a constant
group element. All degrees are odd except (x_A,x_A), giving even
component sizes except the component with that exception, which has
odd size and constant label 1. Therefore ab=1, ac=0. Root protection
ensures only the chosen root contributes identity to c, so c!=0.
No full injectivity of all vertex labels is needed.

Choosing n large enough after all fixed constants gives simultaneous
positive probability of diameter and arrangement exclusion in the
nonempty conditioned law. This proves the full q=32 existential
construction; it does not produce a numerical matching outcome.

## 7. HNN and ring consequences

The original HAND_PROOF.md independently checks the precise HNN words,
two free subgroups by projection to F(x,y), injective base embedding,
and the finite two-dimensional tree of spaces. The explicit cell
eliminations must be applied to the HNN defining subcomplex first and
then transport the r original cells; arbitrary Tietze transformations
do not prove asphericity. With this order the final two-generator,
r-relator presentation is homotopy equivalent to the original HNN
complex. A torsion element of an HNN extension is conjugate into the
base, so torsion-freeness is preserved. These are supplied proofs of
the mechanism, not a new embedding theorem or priority assertion.
I did not fetch the historical HNN publication or another survey to
replace these explicit proofs with an uninspected citation.

For the ring statement, ae=eb=0 while ea and be are not asserted zero.
The maps r -> (ar,er) and (u,p) -> bu+p are inverse right-module maps,
so eR is nonzero cyclic projective and [eR]=0 in K0 even though eR!=0.
The independently written shift example is only an infinite endomorphism
ring control, not a fake group-ring witness. Scalar group-basis and
F2-to-K injections preserve the relations for characteristic-two fields.
No field map to odd or zero characteristic is available. A torsion-free
group with at most one generator is trivial or Z, whose field algebra
is a domain; the two-generator minimum follows only in the stated
class of examples. No new discovery or universal first-priority claim
is added by these classical consequences.

## Outcome and exact gap

The full original mathematical claims pass this scope family. No
substantive proof gap was found after these interface reconstructions.
The exact unprovided objects (numerical sufficiently-large n, matching,
relator list, reduced support, multiplication certificate) are limitations
the native text explicitly discloses, not missing evidence for a claimed
explicit construction. The sole finite native run verifies its finite
label-model scope only. This is not full formal verification, human
refereeing, an exhaustive historical-priority audit, or publication
authority. Default research follow-up is null.
