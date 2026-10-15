# Root mathematical audit: PR359 / OWR-4132-003

## Claim, status and independence

The submitted hypothesis is the exact common-boundary conjecture in Keller's
contribution to OWR49/2009, printed2713–2715. For the specified Möbius map and
tanh feedback, on **all** probability densities with relative L1 topology,
the basin of the constant density is both stable basins' common boundary.
The audit finds a complete proof within that exact scope, with no mandatory
mathematical correction identified. Formal acceptance, priority disposition,
preprint preparation/reviews, merging and publication remain separate pending
steps. Counts and previous PASS declarations are not premises of this verdict.

Root's source-first reconstruction was sealed before reading candidate proof
and program contents, but after reading the PR description and preliminary
family observations. It is explicitly **not** a blind fourth independent
family. The three fresh families sealed their own reconstructions independently
before candidate access. Their distinct mechanisms are quantitative backward
feedback, topology/rough-density transport, and exact continuous algebra.
One algebra family finished reading the complete arXiv variant after candidate
access; its primary author-paper logical reconstruction was completed before
access. This sequence is disclosed rather than silently upgraded.

## Original question and credited prerequisites

Put I=[-1/2,1/2], D={u in L1(I):u>=0 a.e., integral u=1}, phi(u)=integral xu,
G(m)=A tanh(Bm/A), 0<A<=2/5, 6<B<=16. Define

    f_r(x)=((r+4)x+r+1)/(2rx+2),
    T_r(x)=f_r(x) or f_r(x)-1, with cut -r/4,
    F(u)=P_{T_{G(phi(u))}}u.

Let W={u:F^n u ->1 in L1} and B± denote the other two fixed-point basins.
The exact target is W=boundary_D B+=boundary_D B-. The candidate also proves
W=closure_D(union_n F^{-n}({1})), a precise and stronger intermediate statement.

The prior Bardet–Keller–Zweimüller theorem supplies exhaustive convergence to
the three densities and openness of B±. Its Proposition4 supplies contact of
both boundaries with1 through the normalized integral-representation class
D0. These are credited inputs, not new results. Root read the full author
manuscript, including all relevant proofs and AppendixA, and visually checked
the original OWR model and question. Its appendix includes numerical support
for an S-shapedness hypothesis; this audit does not relabel those published
source checks as an independently validated symbolic proof of the whole
prior global theorem. The new inverse estimate is proved independently.

D0 consists of mixtures of w_y=(1-y²/4)/(1-xy)², |y|<=2/3. Its densities lie
between1/2 and2; it is compact and not L1-dense even in W. The symmetric
density4 on the two endpoint intervals of length1/8 is in W and has distance
at least1 from D0. Therefore approximation by this core cannot resolve the
question. The finite-system alpha=1/2 mixture conjecture is a separate open
question and is not claimed. Neither A=0 nor B=6 is included in this theorem.

## Topology and the exact remaining obstacle after turn1

The factorization uses h_r(x)=(x+r/4)/(1+rx), h_r^{-1}=h_{-r}, T_r=T0∘h_r.
Density pushforward Q_r under h_r is a signed-L1 isometry. Joint strong
continuity follows from continuous approximation and isometry, without
operator-norm continuity. K(u)=Q_{G(phi(u))}u is a homeomorphism: for targetv,
the equation rho=G(integral h_{-rho}v) has a unique root because its mean
decreases with rho. The residual increases by at least the parameter change,
has opposite endpoint signs, and its root has Lipschitz constant B/2 in v.
The inverse is Q_{-rho(v)}v.

For v=P0w put q=w/(v∘T0) on positive fibers and q=1 on zero fibers.
Both inverse-branch values of w vanish on an almost-everywhere zero fiber;
the equal allocation therefore still gives P0q=1. The section
R_w(z)=q(z∘T0) is positive, fixes w, and is an L1 isometry in z.
Thus P0 and F=P0K are continuous open surjections on D. If B is either
stable basin, F^{-1}B=B. Continuity and openness yield
F^{-1}(boundary_D B)=boundary_D B, in the relative topology. The prior seed
at1 propagates to all finite preimages. Disjoint openness and exhaustive
convergence give boundary_D B± subset W and closedness of W.

This does not yet give equality: finite compositions of continuous sections
have no stated modulus uniform in their growing length. Treating that missing
modulus as available would transfer the central difficulty. Turn3 supplies
new quantitative control instead.

## Probability-space inverse and full continuous contraction

Let J=[-1/2,3/2], b_r(z)=(2z-r-1)/(r+4-2rz), and Z a J-valued random
variable on an arbitrary probability space. Solve r=G(E b_r(Z)) and put
V(Z)=b_r(Z). The residual derivative is at least1 since
partial_r b_r=-(1-4b_r²)/(4-r²). The unique root lies in[-A,A].
Along a bounded interpolation, differentiation under expectation and the
scalar implicit function theorem are justified by bounded smooth derivatives
on a compact rectangle for each fixed A>0. With X=V(Z), q=1-4X²,
beta=G'(EX)/(4-r²) and D multiplying by f'_r(X),

    dot X=(Id-beta q E/(1+beta E q))D^{-1}dot Z.

This is a path derivative of bounded scalar functions; it is not a claim of
Fréchet differentiability on a full L1 or L2 neighborhood. Branch labels in
the later coupling need not be independent. Arbitrary weights are allowed.

The original candidate's rank-one bound and40-interval rational covering
certificate are correct. Its exact maximum31935269/35322000 is below91/100,
which is below(24/25)². Endpoint coverage, monotonicity and integer square-root
ceilings supply a full continuous inequality, rather than sampled evidence.

The fresh backward family derives the simpler stronger bound independently.
For m=E q, s=E q², C=1+beta/4, m²<=s<=m. In the basis1 and the normalized
q-m, the rank-one operator has matrix

    [[1/(1+beta m),0],[-beta sqrt(s-m²)/(1+beta m),1]].

It is the identity on the orthogonal complement. The determinant of C Id
minus its Gram matrix equals

    beta²[(C m-1/4)²+C(m-s)]/(1+beta m)² >=0.

The lower diagonal is beta/4; for beta>0 this proves positive semidefiniteness.
The cases beta=0 or constantq follow directly. Thus norm²<=1+beta/4.
Root independently checked this matrix, determinant and degeneracies.

For a=|r|, the feedback identity gives g=B(1-r²/A²)<=16-100a². Also
||D^{-1}||<=(2+a)/(2(2-a)). The squared inverse bound simplifies to
W(a)=(2+a)(4-13a²)/(2(2-a)³), a in[0,2/5]. The exact identity

    7(2-a)³-5(2+a)(4-13a²)
      =172(a-13/43)²+12/43+58a³ >0

gives W(a)<7/10<(21/25)². Integrating the path derivative yields contraction
kappa=21/25. It remains uniform as A tends to0 through positive values and
B decreases to6 from above; no uniform G'' estimate is used. The algebra
family independently gives a distinct Bernstein-positivity proof of the
original envelope. Neither new calculation imports candidate program code.

## Rough-density approximation and total variation

Fix u in W and work on (I,u dx). Its orbit variables X_j are bounded even
if u is not in L2. Put u_j=F^j u, epsilon=||u_n-1||1 and
J_n(y)=-1/2+integral_{-1/2}^y u_n. The terminal map is AC, nondecreasing and
onto, displaces by at mostepsilon, and sends the nonatomic law of X_n to
uniform law despite flat intervals. Let A_j in{0,1} be the original branch
labels, f_{r_j}(X_j)=X_{j+1}+A_j. Set Y_n=J_n(X_n), then
Y_j=V(Y_{j+1}+A_j), rho_j=G(EY_j).

The law restricted to each branch event is dominated by the next total law.
Its smooth inverse-branch image is AC. Backward induction proves every Y_j
has a density, feedback is self-consistent and the initial densityv_n has
F^n v_n=1. No change-of-label independence is used. Common labels cancel
in the input difference, giving delta_j<=kappa^{n-j}epsilon and
Delta_j=|rho_j-r_j|<=16kappa^{n-j}epsilon. For kappa21/25,
sum Delta_j<=84epsilon, independent of n.

The deterministic maps H_n=J_n and
H_j=b_{rho_j}(H_{j+1}(T_{r_j}(x))+A_j(x)) glue at the old cut because
both sides map to b_{rho_j}(1/2)=-rho_j/4. They are AC, nondecreasing,
onto and endpoint-fixing. Composition here preserves AC because each inner
old branch is smooth bi-Lipschitz and each outer inverse branch is smooth;
an unrestricted composition-of-AC-functions assertion would be false.
Every finite old cylinder pulls back derivative-exception null sets to null.

The uniform inverse sensitivities3/4 and25/96 give
d_j<=3d_{j+1}/4+(25/96)Delta_j, hence d0<=183epsilon/8 and
sum_{j<n}d_j<=181epsilon/2. The log derivative sensitivities1 and35/24 give

    H0'=u_n(X_n)R_n,     |log R_n|<=213epsilon.

The crucial integral is **unweighted Lebesgue measure**. With the original
external parameter sequence, a_n=P_sequence1 remains a mixture of w_y and
is bounded by2. Transfer duality, using monotone truncation if needed,
gives integral|u_n(X_n)-1|dx<=2epsilon. Integrating instead under u dx
would require an uncontrolled square of u_n and would be invalid. Therefore

    ||H0'-1||1<=2epsilon exp(213epsilon)+exp(213epsilon)-1.

For every AC nondecreasing onto H, H_*(H'dx)=dx by antiderivatives of
continuous tests; flats are allowed. Signed-measure pushforward contracts
full total variation. For continuousg its error is bounded by
omega_g(||H-id||infinity)+||g||infinity||H'-1||1. The auxiliary H_*(gdx)
may contain atoms, so this is a measure-level assertion; the actual
H_*(u dx)=v_n dx was independently shown AC. Approximating fixedu by g,
first taking n toinfinity and then the approximation error tozero, proves
v_n->u in L1. No prescribed convergence rate or positivity ofu_n is used.
Since everyv_n is in both closed basin boundaries, this completes the target.

Uniform displacement alone would not suffice: sinusoidal monotone maps
approach identity uniformly while their pushed Lebesgue laws remain at
nonzero total-variation distance. The derivative estimate avoids that error.

## Separate linear finding and reproduction scope

Turn2 is not a premise of the nonlinear result. Its explicit polynomial
x³-3x/20 has mass and field zero but field(P0f)=1/320, so the field kernel
cannot be treated as invariant in the inspected preprint's short argument.
The corrected resolvent eigenfunctional gives the true strong stable kernel.
Strong L1 stability, BV exponential bounds and failure of uniform L1 operator
contraction are correctly distinguished. The checker implements an integer
frequency recurrence rather than a symbolic trigonometric proof; the latter
is checked analytically from the branches. No nonlinear stable manifold is
inferred, and this unrelated correction need not be a focus of the preprint.

Root fully read every submitted proof/program and all37 problem-file records,
including the entire covering CSV and all manifest semantics. The38-file
Git/API/disk binding includes QUEUE. All86 nested file references, both
predecessor edges, historical author-head binding and25 historical blob
identities check. Historical pending-review states remain history, distinct
from the later claimed-solved disposition.

Root's fresh native runs under preexisting Python3.11/SymPy1.14 reproduce all
three author outputs (60,934 assertions), the old independent output
(18,678 assertions), and the wrapper. The original four complete stdout
receipts are byte-exact, stderr is empty, and original/execution copies are
unchanged. New Bernstein/symbolic/topology controls reproduce byte-exactly.
The backward check's numerical maxima differ at floating-point last digits
between runtimes; its exact fields match. The parent caught that packaging
issue before sealing and requested explicit numerical-tolerance semantics.
All native failure streams are preserved rather than silently replaced.

Mathematical review estimate:100% within the original scope and credited
prerequisites. Publication workflow estimate:45%, because final review
closures, priority, preprint/sequential fresh reviews, integration and upload
remain. Neither percentage is a probability of truth or a historical-novelty
certificate. No outside person has been contacted.

## Subsequent closure and source supplement

2026-10-03T22:30:29.528935+00:00: All3 fresh family namespaces are now finallysealed. The parent reproduced the repaired693-byte portable backward verifier exactly under3.11; every exact certificate/control field is enforced exactly, and only the two labeled numerical summaries use absolute1e-12 comparison with their experimental bounds separately enforced. The initial raw-byte mismatch remains preserved. Root freshly downloaded the exact original ESI payload and matched all3 source-manifest files; the original source-enabled wrapper passes. Neither the ESI scan nor the author/arXiv copy is relabelled as the inspected final journal PDF. The historical global theorem remains correctly credited; priority review is active. Workflow estimate45%.
