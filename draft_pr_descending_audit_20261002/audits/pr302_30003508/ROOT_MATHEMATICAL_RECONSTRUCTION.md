# ROOT reconstruction of PR302

2026-10-05. Original submitted status `claimed_solved`; exact head
`eb6e0e999521d84a65f9857d338cad76b84d30db`; historical author count2/5.
This is a new analytical reconstruction, supplementary to original finite
controls and three independent current families. It is not priority clearance,
human peer review, a formal proof-assistant certificate, or publication authority.
Acceptance remains pending until all new reports and their custody close.

## Claim, assumptions and source comparison

The claim is pointwise-in-parameter almost-sure consistency from observations
`X_0,...,X_(N Delta)` at a fixed known positive lag, for an unknown smooth
symmetric tensor S and unknown smooth invariant density mu on a known bounded
connected smooth domain in dimension at least2. Known positive lower/upper
bounds for S and mu are model assumptions. The generator is
`L=mu^(-1) div(S grad)` with natural conormal reflection. Local uniform
consistency of S and div S is claimed; only the separately clipped tensor is
claimed to converge globally in L2. No rate, nonreversible result, arbitrary
sensor-noise model, rough-domain theorem or quadrature/eigensolver error theorem
is inferred.

ROOT visually read the whole Reiss contribution on printed pp1507–1509 of the
official OWR24/2017 PDF, including its final multidimensional question. Its
fixed-lag, stationary, reversible divergence-form setting, unknown density and
matrix coefficient match this model. It leaves the estimator and retained
spectral count unspecified. Its use of Neumann conditions together with
self-adjoint divergence form supports the natural conormal interpretation;
ordinary Euclidean normal reflection cannot silently replace this condition.
The supplied result gives a convergence analysis in a stated smooth class;
it does not claim every rough positive-definite field or domain is covered.
The source's empirical noise does not by itself specify additional sensor
noise. The official report is DOI10.4171/OWR/2017/24, published28April2018;
the event/report year is2017. Historical novelty remains unestablished.

## Density conjugation and exact spectral formula

Let P be the self-adjoint transition operator on L2(mu dx). The unitary map
`U f=sqrt(mu) f` gives `T=U P U^(-1)` on H=L2(dx), with kernel
`q(x,y)/sqrt(mu(x)mu(y))`, where q is the stationary pair density. True
eigenvalues are strictly positive `kappa=exp(Delta nu)`. No fixed-lag logarithm
alias occurs in this reversible positive self-adjoint model.

For the estimated real symmetric finite-rank T_n put
`M_n=mu_n^(-1/2)` and `W_n=M_n T_n`. If phi is an orthonormal eigenfunction
of T_n, `W_n phi=kappa u` with `u=phi/sqrt(mu_n)`. Thus the evaluation
functional e_n and differential-jet functional B_n each supply one factor
kappa. Their identities are exactly

    A_n=B_n g(T_n) B_n*,
    b_n=(mu_n/Delta) B_n h(T_n) e_n*,

where `g(t)=t^2`, `h(t)=t^2 log(t)` for t>0, and both vanish for t<=0.
Consequently the weighted normal equations contain kappa^4, with one
logarithm only in b_n. This handles negative empirical eigenvalues, zero
crossings and repeated/split eigenvalues by continuous operator functions,
rather than by an unjustified individual eigenvector alignment.

Uniform positive density bounds, global uniform convergence of mu_n and its
local C2 convergence control both density multipliers and all required x
derivatives. The L2 kernel convergence gives T_n-to-T operator convergence.
The Hilbert-valued x-derivative convergence gives W_n-to-W as operators into
local C2. Hence B_n/e_n converge uniformly on each compact interior set.
Continuous functional calculus on an eventually common bounded spectral
interval proves convergence of A_n and b_n. Small positive eigenvalues cause
no singular h limit, since `t^2 log t` tends to zero. Finite initial empirical
eigenvalues greater than1 are not interpreted as population-generator
eigenvalues and do not affect this eventual argument.

## Identification and ridge

For every true eigenfunction the generator equation yields `b=A theta`, where
theta consists of the independent symmetric entries of S and div S. If
`xi* A(x) xi=0`, positivity of all kappa^4 forces `xi.Ju_k(x)=0` for every k.
Every compactly supported smooth test function lies in all powers of the
conormal operator: repeated application of the local differential expression
keeps its support away from the boundary. Eigenfunction partial sums converge
in every graph norm. Standard smooth elliptic boundary regularity and Sobolev
embedding then give C2 convergence for a sufficiently high power. This is an
imported classical elliptic theorem, not a consequence of an algebra test.

Cutoff affine and quadratic polynomials prescribe arbitrary gradients and
symmetric Hessians at an interior point. Their jets span all coordinates,
so xi=0. Continuity and compactness yield strictly positive compact-interior
coercivity alpha_E. No unknown excitation assumption is introduced. It may
be badly conditioned and no class-uniform lower bound is asserted.

For positive ridge lambda_n tending to zero, eventually
`A_n >= alpha_E I/2`. The exact error identity is

    theta_n-theta=(A_n+lambda_n I)^(-1)
       [(b_n-b)+(A-A_n)theta-lambda_n theta].

Every term tends to zero uniformly on E. No noise/ridge relative-rate rule
is missing because the limiting local matrix is already nonsingular. This
does not give coercivity at the reflecting boundary. Clipping the symmetric
tensor to the known convex ellipticity interval is nonexpansive and uniformly
bounded; pointwise interior convergence on a countable exhaustion and dominated
convergence give its global L2 result. No analogous global assertion about
unclipped divergence or tensor derivatives is made.

## Empirical construction and dependence

The finite-order extension followed by smooth mollification depends only on
the known domain. Its signed kernels need not be densities. Reflection
moment matching through order6 supplies sufficient regularity for the needed
mixed derivatives; differentiating the mollifier gives every fixed-order
kernel bound. Boundary bias is corrected by extension, not by unmodified
convolution of a function abruptly set to zero outside the domain.

The symmetric adjacent-pair kernel has feature span of dimension at most
n_j+1 and can be indefinite. This is permitted by the deterministic theorem.
Smooth saturation of the empirical invariant density and normalization give
an unconditional positive lower bound. On eventual uniform consistency the
saturation is inactive and the normalization tends to1, so its C2 limit is
the true density.

For a centered pair observable Z_i and lag l>=1, endpoint conditioning gives
`Cov(Z_0,Z_l)=<r,P^(l-1)s>`, with r/s mean zero and conditional-expectation
L2 norms at most sqrt(Var Z_0). This includes overlapping consecutive pairs
at l=1; no independent-pair assumption occurs. The positive spectral gap
gives a geometric covariance bound and therefore variance at most a finite
parameter-dependent constant times `||F||_infty^2/n`.

For the prescribed dyadic sample count2^j and bandwidth h_0/(j+1), the worst
mixed second-derivative pair summand is polynomially bounded in j. An
epsilon-net in dimension2d with `epsilon=2^(-j/(4d))` has at most a constant
times2^(j/2) points. Chebyshev/union bounds at threshold1/(j+1) give a
summable constant times `(j+1)^(4d+10)2^(-j/2)`. Borel–Cantelli plus the
polynomial Lipschitz bound extends convergence from the net to the whole
closed domain. The neighborhood extension justifies interpolation even on a
nonconvex domain. Finite multi-index sets share one probability-one event.
The analogous one-state argument gives C2 density convergence. Reusing a
dyadic prefix covers every sample size tending to infinity.

Smooth positive-time heat-kernel regularity follows from smooth conormal
elliptic spectral estimates: polynomial eigenvalue counting and derivative
bounds are dominated by positive-time exponential eigenvalue decay. No
empirical eigenpair consistency is hidden in that regularity statement.
The resulting mixed-uniform convergence is stronger than all three exact
deterministic hypotheses. Observation-dependent finite rank, multiplicity
and negative spectrum are consequently compatible with the same pathwise
argument. An eigenvector-free finite-feature/operator formula also gives
measurability, without choosing a discontinuous eigenvector labeling.

## Evidence and exact current gap

ROOT ran unchanged writable copies of both original author verifiers and the
historical independent verifier under unoptimized Python3.9.6/SymPy1.14.0.
The11+42 author controls and1905 historical controls reproduce every saved
JSON value; both author receipt files reproduce exact bytes. This verifies
their finite algebra/bookkeeping claims and supplements the analytic proof.
It does not experimentally prove almost-sure convergence or elliptic
regularity. Complete actual native PID/argv/cwd/time/stream/source/interpreter
custody is in ROOT_ORIGINAL_CONTROL_REPRODUCTION.json and root_reproduction.

No mandatory mathematical defect has been found by this ROOT reconstruction.
The exact remaining gate is closure, whole-body custody authentication and
reconciliation of three new independent family reports, including their
primary elliptic/source evidence. Historical priority requires a separate
in-depth audit after that mathematical gate. Estimated math-review progress70%,
priority0%, PR workflow25%; the overall descending goal remains active.
