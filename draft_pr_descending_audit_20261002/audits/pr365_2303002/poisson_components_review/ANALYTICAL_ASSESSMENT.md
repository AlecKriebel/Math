# Sealed analytical assessment of the frozen packet

All eighteen frozen target files were read completely after BASELINE_SEAL.json
and before this assessment seal. No candidate verification program has yet been
executed. Historical PASS assertions were read only as candidate claims.

## Mathematical judgment

SOURCE_PROOF.md proves the required entire, nonconstant, finite harmonic claim
with the correct n>=3 quantifier. Its first two lemmas coincide in mechanism
with the independently derived Poisson saturation argument. No circular use
of the target theorem occurs. The candidate is a credited exposition, not new
mathematics. Historical source provenance and zero discovery-turn claims remain
records to check, not quantities mathematically inferable from the theorem.

Step1: For probability measure on the sphere |zeta|=R, the proposed kernel
R^(n-2)(R^2-|x|^2)/|x-zeta|^n equals
(1-|x|^2/R^2)/|theta-x/R|^n. It has mean one for each interior x and kernel
values one at x=0. The two extremal inequalities are exactly L_n(s), K_n(s)
in the independent baseline. Nonnegativity permits multiplying a spherical
average by the upper bound. x must be fixed before R tends to infinity;
the proof does so. Supremum need not be attained: liminf >= f(x) for every
x gives liminf >= sup f. The argument remains valid at M=0 (then f=0), but
Step2 correctly divides only by positive suprema of nonzero functions.

Step2: Disjoint positivity makes f/M+g/N <=1 even if M,N are not attained.
The limit of each finite nonnegative spherical average is one. Their sum
would tend to two, contradicting its bound by one. This does not claim that
a bounded subharmonic function is constant. An explicit control threshold is
provided in the independent baseline, strengthening this into a finite-radius
analytic contradiction once high-value witness points have been chosen.

Step3: The component boundary has u=a by continuity and connected-ball
selection. A component of a Euclidean open set is open. At a point outside
A but on its boundary, u-a tends to zero; zero-pasting is therefore continuous.
For comparison on a ball, a connected component of A intersected with that
ball is bounded and has compact closure. The function u-a-H is continuous
on that closure; its boundary is contained in the sphere or partial A. H>=0
throughout the ball, so both boundary types have nonpositive difference. The
maximum principle needs no smooth component boundary. A positive maximum
would force constancy on the bounded piece and contradict boundary values.
Thus every component piece is subharmonic after pasting, and two bounded-value
components would contradict Step2. Euclidean boundedness is not used as a
substitute for bounded u. Independently, bounded positive superlevel components
are impossible by the maximum principle, but that is not sufficient to select
the nested chain and is not the candidate's inference.

Step4: At any real level a, {u>a} is nonempty because sup u=infinity.
If it has one component, all high values occur there. If it has at least two,
at most one can have bounded u, so at least one has unbounded u. This remains
true for infinitely many components; no finite pigeonhole argument is used.
For b>a, any component of {u>b} meeting A lies wholly in A, because it is
a connected subset of {u>a}. If only one such child exists, all values above
b within A lie there, forcing unbounded values. If two or more exist, the
global Step3 obstruction ensures at least one child is unbounded in value.
This provides nested A_j at every integer j and requires only countable
dependent choices. Strict levels >j ensure every polygon interior is high;
using closed superlevels instead would remove openness and invalidate the
polygonal-connectedness argument.

Step5: For an open connected domain, reachability by finite polygons is
relatively open, and its complement is relatively open, proving all points
are reachable. x_j in A_j and x_(j+1) in A_(j+1) subset A_j justify each join.
Continuously parametrizing one finite polygon per [j,j+1] gives compatible
endpoints and a continuous curve. If H is any threshold, all blocks j>H lie
above H, including their interiors; their endpoints also lie in the nested
sets. Every compact spatial set has a finite maximum M_C of continuous u.
All blocks j>M_C avoid C. Only finitely many earlier blocks and pieces remain,
so preimages of compact sets are closed and bounded, hence compact. This is
properness and spatial local finiteness, stronger than vertex escape. No
injectivity, ray, prescribed rate or arcwise monotonicity is assumed.

Step6: h=M-u is finite, nonnegative and entire harmonic. Its spherical mean
about zero equals h(0), making both Poisson inequalities valid. Their limiting
constants tend to one for each fixed x. Even if h(0)=0 both sides are zero
already, so the argument includes that edge case. A nonconstant entire harmonic
u is unbounded above. The proof also works in n=2; n=1 can be resolved by the
affine formula and is outside the stated source question. Constant harmonic
functions, including positive constants, fail the +infinity target and are
excluded. Positive entire harmonic functions are constant; no exceptional
nonconstant positive harmonic case is omitted.

Step7: The source bounded subharmonic example has value -1 throughout the unit
ball, including the origin, radial outside part -r^(2-n), supremum zero and
distributional Laplacian (n-2)dS on the unit sphere. It is a genuine bounded
nonconstant subharmonic example for n>=3, yet outside the unbounded-above
theorem. Multiplicative/additive normalizations do not fix that hypothesis.
The candidate correctly excludes discontinuous subharmonic recertification.
Upper semicontinuity alone need not make {u>a} open; hence the proof cannot be
silently extended to the general discontinuous case.

## Source and historical consistency

Independent PDF hashes and reads support the target, assumptions and attribution
without depending on historical PASS. The source update credits Fuglede's
existence theorem and Carleson's polygonal strengthening. Carleson's printed
thinness criterion has an apparent literal direction issue; the submitted
explicit Poisson argument does not rely on it. Neither the source's compressed
argument nor its editorial update is treated as a novelty certificate.

The eighteen-file packet is internally clear about credited already_solved0/5,
pending historical fields versus completed wrapper review, no author discovery
attempt, and no claim that a fixed ray or quantitative rate is sufficient.
The prior gate limits its scope to accessible prior attempts. Its stated 403
live branches and 379 recovered refs are historical claims, not newly verified
by this family; enumerating all private remote objects is prohibited and would
not be needed to verify the credited source disposition.

## Program review and execution plan

Every line of the three candidate Python files was read. verify_source_alignment
has standard-library Fraction assertions and prints a sorted JSON receipt; it
has no writes or external calls. Its count derives as 10*(300+15)+105*5=3675.
The original check_independent performs nine author-manifest checks, two PDF
checks, 18*91 kernel checks and 18 zero-ratio equalities, for 1667 total. Its
absolute /workspace path is historical and cannot be executed directly in this
workspace. The portable wrapper reads that byte-identical script, substitutes
one exact path literal in memory, and in math-only mode omits precisely the
two PDF hashes, giving 1665. It writes no files. The wrapper's source mode
does not omit or weaken source checks.

Execution will use byte-identical private copies of all eighteen small target
files, plus temporary PDF decompressions inside this review's ignored private
subtree. Full stdout, stderr and exit status will be saved losslessly as gzip,
with stored and logical hashes. Whole receipts will be compared bytewise,
including the explicit expected 1665 adjustment for math-only mode. Source,
nested manifest, Git blob/mode and PR/API scope will be checked independently.

New controls will test exact kernel scaling, radial extremal signs, derivative
one-sided Liouville factors, truncation surface mass, strict-level necessity,
unbounded-domain versus unbounded-value distinctions and vertex-only path
failure. Deliberately wrong radius normalization, unsigned/nonpositive data,
and discontinuity scope are to be rejected. Finite exact computations are
sanity evidence; the analytical proof above supplies the universal claim.

## Assessment before executions

No mathematical defect found in the full required harmonic claim. Strongest
verified result: credited affirmative path theorem with proper entire-tail
and continuous-subharmonic scope. Exact gaps: historical inaccessible-object
provenance cannot be certified; general discontinuous extension and stronger
path requirements are not independently proved. Credited resolution:100%;
audit workflow:65%; new authored discovery turns:0; new theorems:0.
