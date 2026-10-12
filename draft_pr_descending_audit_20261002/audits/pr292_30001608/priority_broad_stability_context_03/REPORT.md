# PR292: bounded broad stability context audit

The broad phenomenon of a positive recurrent stochastic queueing network with
an unstable corresponding deterministic fluid model was proved before the DFC
conjecture. Bramson1999 is a substantive primary precedent. It does not settle
the exact six-rate Deterministic First Chunk conjecture or establish priority
for its all-positive-load solution. A stronger polling example also predates
DFC, but its random fluid limits require careful qualification.

This is a context audit, not a new whole proof review or a worldwide firstness
certificate. I already knew the candidate and ROOT mathematical conclusions
from my completed stochastic review; that familiarity is declared in the initial
scope note. No sibling priority report, mathematical body or verdict was read.
A filename-only inventory accidentally exposed sibling folder/file names; the
exposure and scope error are disclosed in CUSTODY_LIMITS.json. Completed review
namespaces were left unchanged. This report grants no merge, publication,
service, priority or preprint authority.

## Operative primary result: Bramson1999

The complete public publisher PDF was acquired from the download link visible
on the journal page, without authentication or bypass. It is the published
Annals of Applied Probability9(3),818–853 paper, DOI10.1214/aoap/1029962815.
Theorem1 on printed821 proves positive recurrence for sufficiently large integer
L. Theorem2 on printed824 supplies a fluid-model solution starting with zero
mass whose total queue mass has asymptotic lower linear rate1/3. Section4,
printed827–829, defines the scaling and the weaker asymptotic fluid-limit
stability used for recurrence. Section10,850–853, finishes that reduction.

Its fixed-rate network has L+2 stations, two classes per station, exponential
arrivals/services, preemptive static priority and randomized routing through L
parallel middle stations. External arrival rate is1, and gamma lies in(0,1/8).
The service means and priorities are pinned in DERIVATIONS.md. These are bounded
server-capacity queue transitions, rather than DFC's population-dependent peer
contact rates. The stochastic recurrence mechanism uses random emptying of
middle high-priority queues; the deterministic fluid equations admit an unstable
mass path that omits this effect.

The decisive qualifier is that the journal proves asymptotic stability for
fluid limits on events H_z with probabilities tending1 as the initial norm
increases. This is not an unrestricted assertion that every exceptional
pathwise limit is stable. Conversely, the displayed growing solution belongs
to the fluid MODEL equations; the paper does not identify it as a typical
actual stochastic fluid limit. Therefore the title cannot be expanded into an
unqualified stable-process/unstable-true-limit theorem.

Primary links: [journal paper](https://doi.org/10.1214/aoap/1029962815),
[public publisher PDF](https://projecteuclid.org/journalArticle/Download?urlid=10.1214%2Faoap%2F1029962815).
PDF244345 bytes, SHA256 af8799eb0ce4822d3f27961753bc9205036e2d2e9a20ef3a0d845995e21d370a.

## Materially different primary polling example

The Duke-hosted Bramson lecture draft, dated May15,2006 on its cover, discusses
this example in Section5.5. Its hosting Last-Modified2007 is not the document's
authorship date or evidence of identity with a later published book. The draft
pointed to Foss–Kovalevskii1999, which I then acquired from the author's public
archive and read as a complete41-page author version. The journal bibliography
is Queueing Systems32,131–168, DOI10.1023/A:1019187004209. The author version
has placeholder journal pagination; publisher-final body identity is not claimed.

The polling model has two stations, two heterogeneous servers, independent
exponential arrival/service times, arrival rate1 at each station, exhaustive
service, and zero walking times under Assumption3.1. Server locations and
passive/active status supplement the two queue counts in the Markov state.
Theorem3.3 gives positive recurrence and ergodicity under explicit inequalities.
Remark3.6, author pages29–30, chooses service rates4/5,4/5,11/6,7/6 and proves
failure of the usual uniform finite-time, almost-sure fluid contraction.

At each microscopic emptying interface the fluid limit retains a random branch.
One branch produces a deterministic growing path with
35q1(t)+24q2(t)=35+3t. A genuine random fluid limit follows each fixed finite
prefix of that path with strictly positive probability. This establishes more
than existence of an arbitrary relaxed deterministic solution. It establishes
less than positive probability of infinite growth: the forever-growing branch
has probability0. The paper's generalized stopping-time criterion instead
implies almost-sure finite random-time draining and some Lp stability.

My independent rational check gives cycle multipliers2,2/5,5/6 with probabilities
1/10,1/10,4/5 and expected multiplier68/75<1. It separately confirms the
weighted derivative3 and finite-prefix probabilities. This computation is an
algebra control and a check of the interpretation; it does not replace the
primary paper's weak-limit/contraction theorem.

Primary links: [author bibliography](https://tvims.nsu.ru/foss/foss.html),
[author archive](https://tvims.nsu.ru/foss/art.zip),
[journal DOI](https://doi.org/10.1023/A:1019187004209).
Archive113875 bytes SHA256 fda608d0392fcef66ff7b38860e6d1f73c19c87bfd7cdc23b07a6e5563f16be9;
ART.PS326442 bytes SHA256 cc469ebea7b6027ba24fb8085dd2a7bab9b73ead1bebdba716226e9b9550552f.

## Exact comparison with DFC

The authenticated January5,2011 author proof's Section2, Definition2.1 and
Theorem2.2 use arrival intensities multiplied by N, states divided by N, and
fixed physical time. Its Section3.2, Figure2 and Conjecture3.6 specify DFC.
The original source retains A and B as invisible waiting-room peers; the
contact denominator is X+Y+1. Its deterministic large-system ODE has an open
set of divergent trajectories, as stated in Proposition3.5. This is a distinct
claim from an unstable path in nonunique priority fluid equations or a random
polling fluid limit whose support has arbitrarily long growing prefixes.

| Feature | Bramson1999 | Foss–Kovalevskii1999 | Exact DFC target |
|---|---|---|---|
| State | 2(L+2) queue counts | Two queue counts plus server modes | Four counts(A,B,X,Y) |
| Service mechanism | Fixed station capacity; static priorities | Exhaustive moving servers; interface branching | Six rates with nonlinear peer interactions and permanent seed |
| Load conclusion | Fixed gamma, sufficiently large L | Explicit service inequalities; exhibited parameter example | Every fixed real lambda>0 |
| Scaling | Initial norm divides state and multiplies time; fixed rates | Same time/space scaling; random weak limits | N multiplies arrivals; state/N; fixed time |
| Instability shown | Growing relaxed fluid-model solution | No uniform deterministic-time a.s. drain; positive support of growing finite prefixes | Open divergent set for unique interior deterministic ODE |
| Exact DFC recurrence supplied? | No | No | Requires its own proof |

The common conceptual theme is that microscopic randomness can matter for
stability even when a coarse deterministic description grows. Similarity of
theme supplies context and citations; it does not give a reduction of the
DFC generator to either preceding model. In particular the fixed-rate
time-accelerated queueing limits do not become the DFC high-arrival-rate family
by replacing a symbol. Long-time stationary stability and large-system
fixed-time convergence are different limits. No interchange is justified here.

The all-positive-load interpretation is the exact candidate claim and ROOT's
accepted formalization of the unqualified parameterized2011 conjecture. I do not
present it as a literal universal quantifier quotation from the source. The
broader example does not certify DFC novelty, and inability to find an exact
DFC theorem in these few sources does not establish absence elsewhere.

## Limits and held verdict

Stolyar–Ramakrishnan1999 was identified as another lead from the primary draft
and official institutional metadata. Its author-page request reset and old
conference download redirected to a404 page. No operative Stolyar theorem was
read, and no abstract/title-only conclusion is used. The draft's
Dai–Hasenbein–VandeVate2004 distribution-dependent example was read as context,
but its bounded deterministic version is expressly not positive Harris recurrent
under that book's definition; it is not promoted to the needed stable-stochastic
precedent. Those original primary papers were not acquired in this bounded audit.

Read scope, exact derivations, source pins, full actual native streams, negative
attempts, and custody qualifications are held in this namespace. All raw
copyrighted bodies, extracted text, rendered images and raw HTTP records are
private. Only this independently written comparison, DERIVATIONS.md and
SOURCE_PINS.json are suitable for a public-selection review; no automatic
publication is authorized.

Disposition: broad stochastic/deterministic stability mismatch is established
prior context; stronger polling fluid-limit claims need the stated probability
and stability qualifications. Neither acquired primary settles the exact
six-rate all-load DFC recurrence conjecture. Exact worldwide priority remains
outside this audit. No change to the completed mathematical review is implied.
