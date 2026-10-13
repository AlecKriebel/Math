# PR373 source-first independent baseline

This is preparation for the next descending review, before candidate mathematical
prose, programs, stored assertion receipts, prior review or any PR373 sibling proof
has been read. Only the live draft routing body, immutable filenames, and source
locator/hash metadata have been used. No disposition for PR373 is reached here.
The source-first seal records its actual creation UTC. Workflow15%; full original
method resolution0%. The preceding PR374 acceptance remains in progress.

The exact target is Jeffrey Steif's Question C in Oberwolfach Report11/2020,
PDF32/printed632. For every two-sided stationary finite-alphabet process X,
the completions of the past tail intersection_n sigma(X_k:k<=-n) and future
tail intersection_n sigma(X_k:k>=n) coincide. Equality is already a theorem;
the requested contribution is a proof using probability theory without entropy.
An entropy proof, an ergodic-only result, or a proof for selected model classes
does not resolve this method problem. No exhaustive current priority verdict is
made by reading these sources. The bilateral tail need not equal either side:
the original paragraph explicitly gives finite-state bilaterally deterministic
examples with both one-sided tails trivial. Infinite-alphabet examples with
unequal tails do not contradict the stated finite-alphabet theorem.

Four freshly downloaded PDFs match every pinned primary byte length and hash.
Read directly: OWR32–33; Al-Najjar–Shmaya13–14 including Theorem5.2/Example6.1;
Lemanczyk thesis111–116, AppendixB.1–B.3; Bressaud–Fernandez–Galves1–9,
definitions, normalized transition probabilities, full maximal-coupling and
agreement-length comparison. Visually inspected OWR32, Al-Najjar–Shmaya13,
thesis112 and BFG8. Thesis extraction/rendering emits a retained37-byte font
warning with exit0; the inspected formulas are legible. BFG's arXiv manuscript
is version1 dated1998; its generated draft cover also contains2018. The stored
filename1999 is not evidence of the arXiv cover date.

Al-Najjar–Shmaya explicitly cites Weiss Section7 and says tail equality relies
on finiteness and entropy. Its theorem uses that identity, rather than furnishing
the requested method. Lemanczyk identifies the tails with the Pinsker algebra
through conditional-entropy arguments. These are credited known results, not
probability-only resolutions. Its finite Markov class/phase description is also
classical. The thesis's initial setting is ergodic; do not silently use it as an
all-stationary source. BFG supplies a credited coupling mechanism for normalized
chains with complete connections; its nonnormalized potential/variational
discussion must not import entropy into a claimed probability-only proof.

Independent finite-state mechanism: a stationary finite Markov chain has mass
only on closed communicating classes. Each class has period d and cyclic phase;
let theta be the closed class and time-zero phase. Theta can be read from any
remote state after adjusting its known time index. Conditional on theta, each
d-skeleton transition is primitive and converges uniformly in total variation
within its phase. For a finite central cylinder, Markov conditioning reduces
its dependence on a remote future to endpoint state distributions; uniform
convergence makes a future-tail event independent of every central cylinder.
The reverse transition P*(j,i)=pi_i P(i,j)/pi_j on active states proves the past
statement. Conditional tail0–1 and theta measurability yield both tails=sigma(theta).
An explicit two-wing Markov bound is required for a bilateral extension; ordinary
strong mixing alone never licenses that extension.

Independent hidden-state mechanism: for a finite state-emitting HMM, augment the
hidden chain with its emitted symbol, dropping zero-mass states. The augmentation
is a finite Markov chain with the same closed-class phases. Observable tails are
subfields of sigma(theta). With D a common multiple of class periods, the law
conditional on theta is stationary and ergodic under the D-step shift. Empirical
frequencies of every finite observed word along positive or negative D-multiples
recover its full observable conditional law Q_theta. Thus the observable quotient
of theta by equality of Q_theta is recoverable from either tail. A tail event
measurable in sigma(theta) is constant on phases with the same observable law,
so no additional hidden phase can survive in the observed tail.

For N hidden states, M_y=diag(e_y)P and a starting row u give cylinder probabilities
u M_word 1. Let V_k span M_word1 for words of length<=k. V_0 has dimension1;
V_k grows until invariant under every M_y, and dimension is at most N. Therefore
V_{N-1} already spans all words: if it has stopped it is invariant, and if it
has increased each time it is the whole space. Equality on words of length<=N-1
certifies equality of the entire two phase laws in this common representation.
For two separately represented models the safe bound uses their direct-sum size.
Scope is state-emitting finite HMMs; it is not all stationary finite-alphabet laws.

Independent infinite-memory mechanism: suppose finite-alphabet transitions admit
uniform overlap beta0>0 across every pair of histories and a nonincreasing
agreement variation epsilon_l with summable total. Maximal coupling gives a
mismatch bound delta_l=min(1-beta0,epsilon_l), with delta0<1. The product
eta=product_l(1-delta_l) is positive. Use fresh uniforms to couple actual agreement
length L to an auxiliary process S resetting to0 with probability delta_S and
otherwise increasing. Monotonicity gives L>=S pathwise. At each reset the chance
of never resetting again is eta, so the number of resets is geometrically bounded
and finite almost surely. The probability of any auxiliary reset after time n
tends to0, uniformly over initial histories. Consequently the entire future from
n can be coupled identically with probability tending to1. This establishes a
uniform total-variation memory-loss bound, not merely pointwise coordinate
correlations. Stationary absolute-regularity symmetry then controls the other
side. Summability need not imply a finite expected last mismatch time; do not
assert such a rate. BFG's weaker recurrence criterion with disagreement at a
single time tending to0 is insufficient by itself for this full-future coupling
argument. Zero overlap or merely pointwise continuity are important boundaries.

Independent finitary transfer mechanism: a shift-equivariant coding with a genuine
locally witnessed radius R_n and E R_0<infinity satisfies, for each fixed input cut
a, sum_n P(R_n>n-a)<infinity. Borel–Cantelli implies that only finitely many far-right
output coordinates require input left of a. Locally decided approximants using
only input[a,infinity) eventually agree with the output. A completed output tail
event has a raw tail representative: take limsup of its conditional expectations
on successively farther output sigma fields. This representative is pointwise
unchanged by a finite prefix modification. Applying it to the approximant sequence
makes its preimage input[a,infinity)-measurable modulo null sets for every a.
The reversed argument treats the other tail. A nominal random radius without a
measurable local determination witness is not enough. Infinite mean breaks this
summability argument; it is not by itself a counterexample to tail transfer.

Independent conditional-mixture mechanism: conditional on a standard Borel latent
parameter theta, assume component laws are stationary and have a tail-trivial
mixing condition. A tail indicator equals its conditional probability given theta;
this probability is a function of the full observable component law Q_theta, not
of extraneous latent information. For stationary ergodic components, both-sided
empirical finite-word frequencies recover Q_theta; the countable cylinder basis
permits a single integrated null-set argument. Thus both observed tails identify
the sigma field of observable component laws. They need not identify theta when
the parametrization repeats laws. A nonatomic mixture of Bernoulli(p) laws has
nontrivial tail sigma(p); an unconditional mixture need not itself mix. Bilateral
claims require a separately sufficient conditional mixing assumption.

Two boundary controls: mixing two-state Markov chains with transition epsilon>0
have trivial tails, while their weak limit epsilon=0 is a nontrivial mixture of
constant sequences. Tail sigma fields are not continuous under weak convergence.
For binary irrational-rotation coding X_n=1_[0,1/2)(theta+n alpha), dense translated
partition boundaries separate phases for either one-sided remote sequence, away
from a countable boundary null set; Borel injectivity recovers theta. Both tails
can be full for an ergodic finite-alphabet process. Conditioning on theta is not
a stationary component decomposition, so this model does not fit the preceding
conditional-stationary mixture argument. Neither example is an unequal-tail
counterexample to the original finite-alphabet theorem.

Planned adversarial families are finite Markov/HMM and its exact observable-law
certificate; infinite-memory coupling and its uniform/full-future quantifiers;
finitary transfer and nonatomic conditional mixtures with completion, bilateral
and irrational-rotation boundaries. Each must start independently from primaries,
seal a baseline before candidate prose/code, and seal its mathematical verdict
before old review/program receipts. Universal deductions, credited source claims,
finite computational evidence and unproved generalization gaps must stay distinct.
No author sixth turn, new unrestricted solution, or novelty claim is made here.
