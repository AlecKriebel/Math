# PR615: root recheck of the classical implication

Checked 2026-10-21 UTC. Provisional pending the new independent adversary; no
publication, row, closure or merge operation follows from this note.

## Claim and exact scope

The original is Knill's 19 October 2000 item10, read afresh at
https://people.math.harvard.edu/~knill/seminars/intr/ . The question asks for
positive Liouville measure outside the maximal almost-periodic invariant region
and the positive-Lyapunov-exponent region. Genericity and weak mixing occur in a
separate guess. The candidate interprets almost periodicity as precompact L2
Koopman orbits for every observable. It does not address a prescribed exact,
Euclidean, mechanical, analytic, contact or weakly mixing class.

The whole original proof and prior connecting proof were read, rather than
treating the old closure comment as mathematical authority. All24 original
science artifacts match the actual immutable PR head, and their standard-library
replays pass unchanged:3248 author and2460 independent exact checks, six and
eight algebra controls, and four real manifest mutations. These finite tests
supplement, rather than certify, the analytical argument.

## Checkable connecting deduction

Let alpha be irrational and F(x,y)=(x+alpha,y+x) on the area-one torus.
F^n=(x+n alpha,y+n x+alpha n(n-1)/2) and
DF^n=[[1,0],[n,1]]. The Fourier pullback sends (k,l) to(k+l,l), with
phase exp(2 pi i k alpha). An invariant L2 vector has constant coefficient
magnitudes on every infinite l!=0 chain, hence all those coefficients vanish;
irrationality leaves only constants for l=0. Thus F is ergodic. Translates of
exp(2 pi i y) at distinct integer times are orthogonal by integration in x.

Form N=(T2 x R)/((z,t)~(Fz,t-1)). The invariant area and dt descend to closed
forms beta,tau with integral(beta wedge tau)=1. R=partial_t is the complete
Reeb flow. On M=N x(0,1), omega=beta+tau wedge dE is symplectic, H=E is
globally real, and i_R omega=dH. Its full Liouville measure is
(beta wedge tau)dE, of total volume one. E is constant, so the open ambient
interval causes no escape or completeness defect. This is the standard
cosymplectic Hamiltonian extension, restricted to an invariant interval.

The global frame (partial_x-t partial_y,partial_y,partial_t,partial_E)
descends under the mapping-torus gluing. The full tangent derivative and its
inverse are I+sL and I-sL, L(V1)=V2, L^2=0. Both have norm at most1+|s|;
every tangent exponent, including transverse energy, is zero. Equivalence of
smooth metrics along each compact invariant energy level suffices even for this
noncompact finite-volume ambient.

The real suspension flow is ergodic: a flow-invariant function has zero
distributional t derivative and is therefore a function of z; time-one
invariance and F-ergodicity make it constant. Time one alone is not ergodic.
For a measurable flow-invariant C subset M, apply Fubini to its indicator at
countably many rational times, then strong continuity to extend to all times.
Fiber ergodicity gives C=N x J modulo null sets for measurable J. If C has
positive volume, the measurable fundamental-domain observable exp(2 pi i y)
has an orthogonal integer-time orbit on C after normalization. Hence no
positive invariant region is almost periodic. A pure-point clock factor is
not a positive invariant subset with entirely almost-periodic L2 dynamics.
Energy disintegration is precisely beta wedge tau, not an unrelated area
measure. This closes the full-volume, all-subsets and transverse-exponent gaps.

The compact variant uses N x S1_E with the same form and a genuinely smooth
real periodic h(E) which agrees with E on an interval of length1/4. Then
X_H=h'(E)R, h'=1 and h''=0 on that band. All preceding conclusions hold there.
The candidate's cutoff supplies such h and is zero near the circle seam; it
does not confuse a circle coordinate with a global real Hamiltonian. Any good
ambient region meeting the band positively would restrict to a forbidden good
region. This compact modification is elementary and introduces no new
Hamiltonian-realization mechanism.

## Direct primary input and priority boundary

Anzai1951, *Ergodic skew product transformations on the torus*, §6 Theorem6,
equation39 and corollary, printed pp91–92, is the exact m=1 skew shift and
spectral mechanism. Root read the institutional primary PDF through the web
reader and visually inspected both complete relevant cached rendered pages.
The theorem acts on H0-perpendicular, not H0; the corollary explicitly states
ergodicity and continuous spectrum on that perpendicular space.
https://doi.org/10.18910/11966

De León–Saralegi1993, *Cosymplectic reduction for singular momentum maps*,
Lemma3.2 p5036 and §6.1 p5042, prints the exact symplectic form and Hamiltonian
h(x)+s, including the h=0 Reeb realization. Root visually inspected both full
relevant cached primary pages and checked the plus sign and contraction
convention. The fresh web fetch timed out; this is reuse of a hash-bound prior
primary download, not a claim of a new successful retrieval.
https://doi.org/10.1088/0305-4470/26/19/032

Root checked both cached PDFs against the prior source ledger:
Anzai1557995bytes/SHA256738ade609fd24342fad59f0111eb43029a41b4119b92e3a458ed64a5b6169e91;
de León957467bytes/SHA25625469746eb0ead7d1f5377da273efba8cbd1d9ca1518738a6390863e2f7b84e6.
Their URLs and exact locations are retained in the historical SOURCE_LEDGER.
No third-party full text is copied into the public checkpoint projection.

The unrestricted existence conclusion follows directly from these named older
mechanisms and the explicit elementary deductions above. No stronger new
target can be substituted to preserve eligibility. This supports rejecting
publication as a genuinely new resolution under the user's priority rule.
It does **not** establish an earlier article explicitly answering the later
named Knill question, nor a worldwide firstness determination. An attributed
expository note remains mathematically possible but is outside this sweep's
new-full-solution publication scope. The existing draft manuscript is preserved.
