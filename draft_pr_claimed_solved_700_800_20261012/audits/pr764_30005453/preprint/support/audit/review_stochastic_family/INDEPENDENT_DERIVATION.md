# Independent stochastic derivation before historical audit conclusions

Recorded 2026-10-14 05:02:17 UTC. Review completion estimate: 50%.
Input read: frozen `author_v2/PROOF.md`, and applicable AGENTS instructions.
No historical audit conclusion has been read at this checkpoint.

## Hypothesis and criterion

For a countable undirected simple graph with degree at most D, strictly
positive vertex rates at most P, deterministic positive integer initial
edge counts (each finite, without a uniform initial bound), and 0<alpha<1,
the proposed stochastic conclusion is simultaneous coordinatewise almost
sure convergence to the unique strictly positive equilibrium. The existence,
uniqueness and complete-trajectory rigidity lemma are separate deterministic
premises whose use must be explicit. Uniqueness among all nonnegative
equilibria is a different, false statement when alpha>0.

## Graphical construction, including the infinite graph

Give each vertex an independent rate-p_v Poisson process with independent
uniform marks. A firing's choice requires the counts on the finitely many
incident edges immediately before firing. Those counts depend only on earlier
firings of that vertex and its neighbors. A causal ancestor chain is therefore
bounded by chains moving through the D+1 vertices consisting of the current
vertex and its neighbors, with strictly decreasing times. For a fixed edge
and time horizon T, the expected number of length-n such ordered chains is
at most 2 (D+1)^(n-1) P^n T^n/n! (a harmless larger bound also suffices).
This tends to zero as n tends to infinity. Every event has finitely many
immediate ancestors, because finitely many involved Poisson processes have
finitely many events on [0,T]. An infinite ancestor tree would have an
infinite chain by the finitely branching tree lemma. Thus the ancestor set
is finite almost surely. Taking a countable intersection over edges and
integer T constructs all counts consistently. Coincident events at two
vertices have probability zero, also after the countable union over vertex
pairs. Initial counts only supply local finite constants, so their spatial
supremum need not be finite. Isolated vertices do not affect any edge.

In the natural filtration of all clocks and marks, the edge counting process
I_e has predictable intensity lambda_e=N_e(t-)^alpha q_e, where
q_e=p_u/S_u(N(t-))+p_v/S_v(N(t-)). Each endpoint's probability is at most
one, so lambda_e<=p_u+p_v<=2P. Since every count is at least one, q_e<=2P.
There is no global finite total-rate requirement.

## Exact transform and normalized martingale law

H(n)=sum_{j=1}^{n-1}j^(-alpha) has jump H(n+1)-H(n)=n^(-alpha).
Integral comparison gives

    (n^c-1)/c <= H(n) <= (n^c-1)/c+1,
    c=1-alpha.

Consequently H(n)=n^c/c+O(1), uniformly in the positive integer n.
Writing Q_e=int q_e ds, the compensated counting-process integral is

    H(N_e(t))-H(N_e(0))=Q_e(t)+M_e(t),
    <M_e>(t)=int N_e(s-)^(-alpha) q_e(s) ds <= Q_e(t)<=2Pt.

This is genuinely square integrable on finite intervals: the jump integrand
is at most one and the intensity has the deterministic bound 2P. No unstated
stopping/local-integrability extension is needed. Using N(t-) in the
predictable integrands is essential; using N(t) inside ordinary time
integrals changes nothing because the jump times form a countable null set.

Let A=1+Q and L=int A^(-1)dM. Then E<L>(t)<=1 for every t, hence L is
an L2-bounded martingale and converges almost surely. Since A is continuous
and of finite variation, integration by parts gives

    M/A=L-A^(-1) int L dA.

On Q tending to infinity, the weighted Cesaro limit of the integral term
is the limit of L. Thus M/Q tends to zero. This proof is pathwise after
martingale convergence and does not assume independence across edges,
deterministic Q, or positive uniform vertex-rate lower bounds.

## Linear growth without a spatially uniform random time

For each edge, N_e(t) is at most its initial constant plus the total number
of firings at the two endpoints, so limsup N_e(t)/t<=p_u+p_v<=2P.
For one fixed edge e and epsilon>0, only finitely many edges meet its
endpoints. Their bounds therefore hold simultaneously after a finite random
time depending on this neighborhood. Thereafter

    q_e(t)>=k t^(-alpha),
    k=(p_u/d(u)+p_v/d(v))/(2P+epsilon)^alpha>0.

Thus Q_e diverges and liminf Q_e(t)/t^c>=k/c. The exact transform plus
M/Q tending to zero yields N_e(t)^c/(c Q_e(t)) tending to one, and hence
liminf N_e(t)/t>=(k)^(1/c). Passing epsilon through a countable decreasing
sequence gives the claimed m_e. Countable edge intersections give one event
for all coordinates, while neither m_e nor the neighborhood starting times
are spatially uniform.

Since H(N_e(t))=O(t^c) from the upper count bound and H/Q tends to one,
Q_e(t)=O(t^c), hence M_e(t)/t^c tends to zero. This step has no circular
use of the final stochastic convergence assertion.

## Scaled vertices and trajectory extraction

Define A_v(t)=c t^(-c) int_0^t p_v/S_v(N(s)) ds. The exact transform
then gives, for arbitrary positive integer initial counts,

    (N_uv(t)/t)^c=A_u(t)+A_v(t)+r_uv(t),  r_uv(t)->0.

The additional fixed H(N_uv(0)) term divided by t^c vanishes even when
the spatial supremum of the initial counts is infinite. Nonnegativity and
the edge upper bound imply limsup A_v<=(2P)^c. Integrating the finite
incident-neighborhood upper bound on N gives

    liminf A_v>=p_v/[d(v)(2P)^alpha]=ell_v>0.

For a_v(s)=A_v(exp(s)), the chain rule holds almost everywhere and yields

    a_v'=c[p_v/S_v(X(exp(s)))-a_v].

For each fixed v, the finitely many m_e lower bounds keep the denominator
away from zero eventually and the A_v upper bound controls the second
term. This proves coordinatewise eventual Lipschitz bounds, with constants
allowed to depend on v. Translating by any sequence s_n tending to infinity,
Arzela-Ascoli on each coordinate and compact interval, then a countable
diagonal extraction, gives locally uniform coordinate limits b_v on all of
R. Their bounds are ell_v<=b_v<=(2P)^c, including all real times.

The ordinary meaning of r_e(t)->0 makes its convergence uniform on shifted
compact logarithmic intervals, since their minimum physical time tends to
infinity. The edge power relation therefore gives locally uniform edge
limits X_uv -> (b_u+b_v)^(1/c). Each incident sum is finite; b_v>=ell_v>0
ensures strictly positive denominator limits. The right-hand sides of the
integral equations converge locally uniformly, so the limits are classical
complete solutions of b_v'=c[p_v/T_v(b)-b_v]. No supremum-norm compactness,
infinite spatial sum, or measurability of the chosen subsequence is needed.

Conditional on the separately stated complete-trajectory rigidity lemma,
every such b is z. A fixed coordinate failing to converge would provide
a sequence with a fixed separation at time zero, contradicting that
conclusion after extraction. This proves simultaneous coordinatewise edge
convergence on the same countable probability-one event.

## Boundary and source questions still to inspect

At alpha=0 each endpoint uniformly chooses among its incident edges, and
Poisson thinning gives asymptotic edge rate p_u/d(u)+p_v/d(v). Alpha=1
cannot be included: c vanishes and critical even-cycle equilibria need not
be unique. Empty edge sets give the unique empty array and vacuous convergence;
disconnected graphs pose no additional stochastic requirement. Initially
zero edges are excluded because they remain zero when alpha>0.

On the doubly infinite path, the alternating arrays (2,0,2,0,...) and
(0,2,0,2,...) are nonnegative boundary equilibria for unit vertex rates and
every alpha in (0,1): each denominator equals 2^alpha and the active edge
rate is 2. This is already a rigorous obstruction to literal unrestricted
nonnegative-equilibrium uniqueness. Whether the source expressly restricts
the equilibrium class is the remaining scope check. Historical evidence
and source context have not yet been consulted.
