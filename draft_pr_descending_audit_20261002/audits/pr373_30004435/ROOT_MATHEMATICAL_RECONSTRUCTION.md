# Root reconstruction of all five scoped claims

Provisional mathematical PASS for the written scopes; original Question C remains
unsolved5/5. Full candidate programs, stored receipts, historical review, publication
metadata and fresh sibling proof artifacts remain unopened at this seal. The root
source-first baseline was sealed first. Brief arriving sibling progress messages
are disclosed in the verdict seal; they do not replace any argument below.

The original requested theorem covers every stationary finite-alphabet process
and requires a proof without entropy. Known entropy-based equality is credited.
The five turns supply distinct restricted results and explicit obstructions;
none supplies a reduction of all stationary processes to those restrictions.
No novelty, human peer review, proof-assistant verification or full resolution
is certified. The root read all five TURN mathematical files completely.

Turn1 exact reduction: for bounded finite-coordinate f, reverse martingale
convergence of projections onto the decreasing completed half-line fields gives
L2 convergence to the respective tail projections. Continuity of norm proves
the claimed squared-defect limit. Cylinder indicators linearly span an L2-dense
algebra on the countable product; two norm-one conditional-expectation projections
agree on that algebra iff they agree everywhere. Applying to an indicator in
either tail yields equality of completed fields. Increasing finite-window
conditioning first converges to each fixed half-line projection; it licenses
the ordered N-then-m limits only. Stationarity supplies no diagonal interchange.

Finite Markov support: stationary mass on transient states is zero by the bounded
chance of absorption in a closed class; positive support has no outgoing edge
to a zero-mass state by pi P=pi. Restrict to finitely many closed irreducible
classes. Class C with period d has cyclic subclasses of conditional mass1/d.
The time-zero class/phase Z is recovered from any distant state by subtracting
its time index modulo d; thus it is measurable in all three tails. For a common
multiple D, P^D on each phase is primitive. A positive power has common row
minorization epsilon=number_of_states times its least entry. Coalescent coupling
gives uniform geometric convergence to the phase-conditioned stationary law.
This avoids entropy and retains the distinction between D-stationarity and
unit stationarity after conditioning on a periodic phase.

The bilateral upper bound is independently justified by the actual bridge
formula. For central path y[-r,r], endpoints i=Y[-m],j=Y[m], m a multiple of D,
its probability given finite outside windows is

    P^(m-r)(i,y[-r]) product_{k=-r}^{r-1}P(y[k],y[k+1])
        P^(m-r)(y[r],j) / P^(2m)(i,j).

Markov factorization cancels outside transitions; increasing outside windows
retains this same endpoint formula. Under Z, compatible endpoint and central
phases have limits d*pi_C(y[-r]), d*pi_C(j) and d*pi_C(j), respectively. The
denominator is bounded away from zero eventually, uniformly on the finite active
support. Incompatible paths are identically zero. The limiting probability is
the correct Z-conditional central path probability. Reverse martingales along
this cofinal sequence identify the bilateral projection with conditioning on Z;
cylinder density proves bilateral tail=sigma(Z). Both one-sided fields lie
between sigma(Z) and the bilateral field. This is a credited classical result,
not an inferred consequence of ordinary alpha mixing.

Alternation shows sigma(Z) can be nontrivial while invariant events are trivial:
the shift swaps its two phases. A tail field is shift-preserved as a collection,
not fixed pointwise event by event. For the two-state epsilon-flip chain,
0<epsilon<1 gives trivial tails, but epsilon down to0 gives a mixture of constants
with a nontrivial common tail. The n-block total variation from that limit is
exactly1-(1-epsilon)^(n-1), bounded by(n-1)epsilon. Shift registers of L iid
bits forget their initial state after L steps and have trivial tails. The
infinite-register limit retains every earlier bit in every future half-line
but has iid trivial past tail. Its infinite single-spin alphabet is explicitly
excluded from the original theorem. Neither limiting example contradicts it.

Turn2 deterministic observation: pullback of every completed observed bilateral
tail event lies in the hidden bilateral tail, so it is h(Z). Conditional on Z=z,
the D-skeleton is stationary with geometric cylinder correlation bounds. Word
indicator averages have variance at most C/N; Chebyshev on N=j^2 is summable and
bounded indicators fill the intervening indices. The same covariance estimate
handles negative indices, without reversibility. Deleting finitely many sampled
blocks changes no limit. Therefore each conditional word probability p_Z(w) is
measurable in either completed observed tail, simultaneously for countably many
words. These coordinates identify the finite quotient Q of phases by their
observable laws.

Equality of all nonnegative contiguous words determines the full two-sided
conditional law: translate a finite cylinder by a sufficiently large multiple
of D and sum gaps out of a contiguous word. If z and z' have the same observable
law, an observed event h(Z) has the same conditional probability in both; because
it is an indicator this forces h(z)=h(z'). Positive phase masses also make any
chosen unconditional null representative null under each such component. This
proves all three observed tails=sigma(Q); no sigma-field intersection/join is
commuted. Stochastic finite emissions are explicitly reduced to supported joint
states, with P_joint((i,a),(j,b))=P(i,j)e_j(b) and stationary pi_i e_i(a).

All-length certificate: M_a=diag(1_{f(i)=a})P and P1=1 give word probabilities
alpha_z M_word1. V_k spans all words of length at most k. Its recursion is
V_{k+1}=span(V_k, M_a V_k over a). If it stops growing it is invariant forever;
if it grows, dimension rises at least one. Starting at dimension1 in ambient
dimension s, V_{s-1} is sufficient. An annihilating row difference on that space
therefore annihilates every word, including the empty word for s=1. Rational
arithmetic makes the computation checkable. The author's stochastic-emission
bound uses supported joint-state count, so it does not overclaim a sharper bound.
There is no finite-state or finite-word-space representation of arbitrary
stationary laws established here.

Turn3 uniform infinite-memory criterion: g is a measurable probability vector
on every history, and agreement bounds v_k are nonnegative, nonincreasing,
v_0<1 and summable; existence of a compatible stationary law is assumed. A fresh
uniform maximal coupling with common mass at least epsilon=1-v_0 has a branch
U<=epsilon forcing agreement regardless of histories. Each disjoint l-block of
forcing uniforms has probability epsilon^l, independently. Thus the stopping
time tau of l consecutive agreements satisfies
P(tau>n)<=(1-epsilon^l)^floor(n/l). At tau the histories match at least l symbols.
The first later disagreement after another k-l agreements has conditional
probability at most v_k; a finite-horizon union bound followed by monotone
convergence bounds any future failure by sum_{k>=l}v_k. When tau<=n and no later
failure occurs, the entire infinite outputs after n agree. The displayed b(n)
is consequently a genuine whole-path total-variation bound uniform over histories.
First fix l to make its tail small, then let n grow, then let l grow: b(n)->0.
No unjustified finite expected last-disagreement time or sharp rate is asserted.

For almost every actual conditioning past, the future law is the successive g
kernel law by the conditional chain rule on finite words and countable-product
uniqueness. Comparing any two histories and mixing the second history gives
the claimed conditional future-event bound. Regular conditional distributions
exist on the finite-alphabet product. Its alpha consequence bounds correlation
between an arbitrarily remote event and any fixed central cylinder, by stationary
translation. A tail event is independent of all cylinders and hence itself.
The past case uses the same past/future coefficient with events interchanged,
not a reverse g kernel. Two stationary compatible laws have their fixed finite
blocks within b(n) at remote positions; stationarity and n->infinity identify
all block laws. This proves uniqueness conditional on existence, not existence
for every merely measurable g. There is no bilateral conclusion here.

The explicit binary g has probabilities in[1/4,3/4], v_k=2^(-k-1) exactly,
summable tail2^(-k), and dependence on every past coordinate. Its uniformly
convergent series is continuous on compact histories. The append transition
is Feller; Cesaro averages have a weak cluster point and telescoping invariance,
yielding a stationary history-chain law. A two-sided stationary extension of
that chain identifies every history coordinate with the corresponding earlier
appended symbol, by countably many shift identities. Consequently g really is
the conditional next-symbol law of its resulting symbol process. This existence
argument is probability/compactness based. Uniform overlap and summable continuity
are significant extra assumptions; arbitrary stationarity does not imply either.

Turn4 decisive finite-mean coding: the fixed shift-invariant conull domain G
makes a decisive centered block's label well defined. For each radius finitely
many blocks are possible, so minimal radius R and all decoder labels are
measurable without an algorithmic admissibility oracle. At site k>=N>=m,
search radius at most k-m only in input[m,2k-m]. A decisive label agrees with
the actual output whenever R_k<=k-m. Entire remote decoded and true vectors
differ with probability at most e(N,m)=sum_{k>=N}P(R>k-m), by stationarity and
the union bound; no independence is needed. Finite integer mean makes this
tail sum tend to0 for each fixed m.

For a completed output tail event A, choose a Borel event in each remote output
vector representing A modulo null sets. Substituting its decoded vector gives
an event in the input half-line with symmetric-difference probability at most
e(N,m). A subsequence with summable error converges almost surely to1_A, proving
A belongs to that completed input field. Do this for every integer m. The past
decoder is the reversed finite-window construction; the bilateral decoder uses
both sides with error at most2e(N,m). No off-support arbitrary filling is required,
and completions/intersections are handled eventwise with countably many choices.

Thus corresponding tail inclusions are proved. Trivial input tails transfer
triviality; finite-mean finitary inverse codes give equality in both directions
and transfer input one-sided equality. Mere inclusion in a common nontrivial
input tail does not imply output left/right equality; the author explicitly
does not infer it. The iid run code queries k+2^L where L is the forward zero
run ending at the first1. This query is always strictly after that first1,
including L=0. Fixing any centered radius smaller than2^L permits two conull
extensions changing only the query bit and the output; radius2^L sees both
the first1 and query. Thus least radius is exactly2^L and has infinite mean
because P(L=l)=2^(-l-1). This only obstructs the sufficient proof's integrability
assumption; it is no unequal-tail counterexample. Its future-only code already
has a direct right-tail inclusion without that assumption.

Turn5 arbitrary standard-Borel mixtures: component laws mu_theta are invariant
under one fixed D-step shift and have alpha_theta(n)->0, without uniform rates.
For a word indicator sampled at multiples of D, fixed-word overlap contributes
only finitely many covariance lags and all other covariances tend to0 by alpha
mixing. Cesaro covariance sums make variance tend to0. Boundedness permits
dominated convergence over theta, giving joint L2 convergence to p_Theta(w)
for both positive and negative sampling times. Deleting finitely many samples
puts every limit in every completed half-line field. Conditional D-stationarity
and countably many word probabilities determine full two-sided random law M.
Therefore sigma(M) is included in both tails. This step requires no parameterwise
choice of strong-law subsequences, common rate, or identifiable latent labels.

For the upper bound, alpha mixing plus D-stationarity makes each component's
one-sided tails trivial by cylinder independence, translating by suitable
multiples of D. A single global tail representative A agrees with countably
many remote representatives under the mixture; disintegration makes all those
equalities hold in almost every component simultaneously. Thus mu_theta(A) is0
or1. Conditional indicator variance is zero and1_A=M(A), a measurable evaluation
of the random observable law, almost surely. The conclusion is the observable-law
quotient, not every redundant theta label. Bilateral equality is proved only
under separate component bilateral triviality. For mixtures of finite-state
hidden models with common finite hidden-state bound s, adjoining class/phase
and D=lcm(1,...,s) supplies that hypothesis through the earlier finite-chain
proof; no global rate over models is needed. For use as an original-source
subclass, the author separately assumes the mixture is unit stationary.

The uniform Bernoulli(p) mixture has posterior mean(k+1)/(N+2), uniform success
count law1/(N+1), and mean square sampling error1/(6N). Conditional independence
of two disjoint size-N blocks gives E[(K-L)^2]=N/3, hence the displayed defect
N/[3(N+2)^2]. It is a finite-window defect; the half-line limit has already
identified p. The common tail is the nontrivial nonatomic sigma(p), while a
redundant independent label is excluded.

For irrational rotation, the specific binary itinerary is a telescoping floor
difference, not an assumption of iid symbols. From a future starting at m,
V={U+m alpha} and cumulative n count reveal1{V>=1-{n alpha}}. These dense
threshold comparisons recover V as a countable supremum, including0, and then
U. The past sums reveal1{V<{n alpha}}; dense comparisons recover the same phase.
The formulas hold at equality thresholds with the stated weak/strict signs.
This is explicit measurable recovery in each remote half-line, so both tails
and the bilateral field are the full sigma(U). Irrational translation is
ergodic by its Fourier coefficients but no power is mixing: an increasing
sequence of translates tending to the identity makes an interval correlate
to its mean rather than squared mean. Because the coding generates U, strong
mixing of its binary process would force ordinary mixing of that generated
system via cylinder approximation, a contradiction. This source-admissible
example rules out the suggested universal conditional-mixing reduction while
satisfying tail equality. Fourier/density facts are credited classical boundary
tools, not a claimed all-process probability-only solution.

Exact remaining gap: no argument here forces the cylinder tail-projection defect
to zero for every stationary finite-alphabet law, with no mixing, hidden-state,
summable-kernel or finite-mean invertible coding assumption and without entropy.
All claimed partial mechanisms have direct proofs above. Next gates are code
inspection, whole author/old-review reproduction, immutable scopes/source/queue
checks, distinct adversarial verdicts and a fresh whole-package final reviewer.
