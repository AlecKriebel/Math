# Turn 2: superpolynomial tails above the N^(1/4) coarse scale

**30001321 / OWR-4081-005. Unreviewed scoped partial, author turn 2/5.** The original quantifier over *every* diverging scale is still unresolved. This turn proves a superpolynomial tail on a restricted, explicitly stated scale range; it does not answer Berger's conjecture in full.

Use the i.i.d. merely elliptic nearest-neighbor model and notation of
`TURN_1.md`. In particular p_(s,x) is in (0,1) almost surely, q=E p,
a=q(1−q), delta=E[p(1−p)]>0, sigma²=a−delta, v=2q−1,
mu_s(x)=P_omega(X_s=x), and F_s contains environment layers before s.
Set I_s=sum_x mu_s(x)². All partitions below are deterministic.

## 1. Scoped theorem

For every gamma>1/4, fixed epsilon>0 and K>0, there are finite
constants C_K,N_0, depending on the environment law, gamma, epsilon
and K, such that for every N>=N_0, every integer M>=N^gamma and
every partition into M-site intervals,

    P_env(L_(N,M)>epsilon)<=C_K N^(−K).                     (1)

The constants are uniform in interval alignment. No uniform ellipticity
constant is assumed. For gamma>=1/2 it suffices to apply the result
with a smaller fixed exponent in (1/4,1/2). We prove that range.

The new input beyond turn1 is an all-order occupation-moment bound and
a common good-overlap event for exponentially many terminal tests.

## 2. Uniform conditional overlap bound

Let D be the half-difference chain (turn1, equation(2)), and put
u_n(d)=P_d(D_n=0). Besides g_n=u_n(0)<=C/sqrt(n+1), we need

    0<=u_n(d)<=u_n(0) for every integer d.                  (2)

Here is a direct proof. The functions u_n are symmetric. If
v_n(d)=u_n(d)−u_n(d+1), d>=0, then for d>=1

 v_(n+1)(d)=a v_n(d−1)+(1−2a)v_n(d)+a v_n(d+1),

while

 v_(n+1)(0)=(1−2delta−a)v_n(0)+a v_n(1).

All coefficients are nonnegative because delta<=a<=1/4.
Initially v_0(0)=1 and v_0(d)=0 for d>=1, so induction proves (2).

Given F_s, two independent quenched replicas start at time s with
joint law mu_s tensor mu_s, and their future annealed half-difference
has exactly this Markov kernel. Consequently, for every t>=0,

 E_env[I_(s+t) | F_s]
   =sum_(x,y) mu_s(x)mu_s(y) u_t((x−y)/2)
   <=g_t<=C/sqrt(t+1).                                      (3)

The common parity makes every displayed half-difference an integer.
The t=0 case uses I_s<=1. Future layers are independent of F_s;
no independence of the random variables I_s across time is asserted.

## 3. All occupation-sum moments

For any deterministic starting time s and length L>=1, let

    V_(s,L)=sum_(j=0)^(L−1) I_(s+j).

Equation (3) gives E[V_(s,L)|F_s]<=A_L, where
A_L=sum_(j=0)^(L−1) g_j<=C sqrt(L). More generally, for every integer
k>=1,

    E[V_(s,L)^k | F_s]<=k! A_L^k<=k! C^k L^(k/2).          (4)

To see this without an independence assumption, expand the kth power
and order its time indices nondecreasingly, at cost at most k!.
Condition at the penultimate time. The conditional expectation of
the sum over the last index, including equal indices, is at most A_L
by (3). Iterating removes all indices and gives (4). Products of
earlier I's are nonnegative and measurable at each conditioning time.
Repeated indices cause no difficulty because the conditional bound
at time gap zero is I_s<=1.

Thus for any fixed eta>0 and k,

    P(V_(s,L)>N^eta sqrt(L))<=k! C^k N^(−k eta).            (5)

The starting time and length can depend deterministically on N.
Choosing k separately for each desired power gives a superpolynomial
bound. This is a statement about an occupation sum, not an unsupported
all-moment bound on a single I_N.

## 4. Scalar martingale tail inequality used below

For a finite martingale with increments D_j, |D_j|<=b, set
Q=sum_j E[D_j²|F_(j−1)]. The elementary Bernstein–Freedman estimate
in a sufficient form is

 P(|sum D_j|>=u, Q<=w)
    <=2 exp(−u²/[4(w+bu)]), u,w>0.                         (6)

For completeness, e^x<=1+x+x² for |x|<=1 gives
E[e^(lambda D_j)|F_(j−1)]<=exp(lambda² E[D_j²|F_(j−1)])
when lambda b<=1. The corresponding exponential supermartingale
has expectation at most one. On the event with sum D_j>=u and Q<=w,
its terminal value is at least exp(lambda u−lambda²w). Take
lambda=u/[2(w+bu)], and apply the same argument to −D_j. This proves
(6) directly. In particular we apply it to a joint event; we do not
condition the martingale law on a future good event.

This is a standard scalar concentration method, not a novelty claim;
the proof is included to fix the exact constants and hypotheses.

## 5. Parameters and the truncated terminal law

Fix gamma in (1/4,1/2), and put

    beta=(gamma+1/4)/2,
    eta=(gamma−1/4)/4,
    r=N^beta,
    ell=floor(N^(2beta)/(log N)²),
    m=N−ell.                                               (7)

For large N, 1<=ell<=N/2, r/M→0 uniformly over M>=N^gamma,
and r/sqrt(N)→0. Define the probability measure

    nu_N(A)=E_env[mu_N(A)|F_m]
           =sum_x mu_m(x) T_ell 1_A(x),                    (8)

where T is the averaged-walk semigroup. This averages only the last
ell environment layers. Its environmental expectation is the averaged
N-step law.

We first show that the coarse interval masses of nu_N are
superpolynomially close to the averaged law.

## 6. Common variance control for bounded terminal tests

For a deterministic |f|<=1, expose layers before m in (8).
The turn1 martingale formula applies with gradients
T_(N−s−1) f(x+1)−T_(N−s−1) f(x−1), whose absolute value is
at most C/sqrt(N−s), by the total variation of the shifted binomial
kernel. Thus every increment has absolute value at most C/sqrt(ell),
and its predictable quadratic variation is at most

    C sum_(s=0)^(m−1) I_s/(N−s).                           (9)

Partition these time indices into deterministic dyadic blocks B_j
on which N−s−1 lies in [2^j ell,2^(j+1)ell). Their lengths are at
most h_j=2^j ell, and there are O(log N) nonempty blocks. By (5),
the event

    E_N={sum_(s in B_j) I_s<=N^eta sqrt(h_j) for every j}

has superpolynomially small complement. This one event is independent
of the choice of f. On E_N, (9) is at most

    C N^eta sum_j h_j^(−1/2)<=C N^eta/sqrt(ell).            (10)

Apply (6). For every fixed u>0,

 P(|nu_N(f)−P f(X_N)|>u, E_N)
   <=2 exp(−c_u sqrt(ell)/N^eta)
   <=2 exp(−c_u N^(beta−eta)/log N).                        (11)

The constants are uniform over all such deterministic f. The good-event
failure is kept outside the union over tests in the next step.

## 7. Finite sign tests and tail truncation

Let W_N=[vN−sqrt(N)log N,vN+sqrt(N)log N], and let C_N be the
partition cells intersecting W_N. Their number J_N satisfies

    J_N<=C N^(1/2−gamma)log N+2.                            (12)

The L1 discrepancy on these cells is the maximum over the 2^J_N
sign functions f=sum_(j in C_N) e_j 1_(I_j), e_j in {−1,1}, of
nu_N(f)−P f(X_N). Each f is deterministic and bounded by one.
Using (11) and a union bound, while charging P(E_N^c) only once,
gives a superpolynomial tail. Indeed

    beta−eta > 1/2−gamma,

so the negative exponential in (11) dominates J_N log 2.

The averaged probability of W_N^c is at most C exp(−c(log N)²)
by the bounded-i.i.d.-increment tail bound. The expectation of
nu_N(W_N^c) is the same averaged probability, so Markov's inequality
makes a fixed positive tail mass superpolynomially unlikely. Cells
outside C_N are contained in W_N^c. Consequently

 P(sum_j |nu_N(I_j)−P(X_N in I_j)|>u)
   is superpolynomially small for every fixed u>0.          (13)

This step does not assert independence of interval masses.

## 8. Controlling the actual last ell layers

Extend the lattice intervals to the corresponding real half-open
intervals. Let B_N be the integer positions x for which x+v ell lies
within distance r of a partition boundary. Couple the actual endpoint
with the real translated position X_m+v ell. Unless X_m lies in B_N
or |X_N−X_m−v ell|>r, both belong to the same cell.

Put D_N(omega)=P_omega(|X_N−X_m−v ell|>r). The averaged last
ell increments are independent bounded increments, so

    E_env D_N<=C exp(−c r²/ell)
              <=C exp(−c(log N)²).                        (14)

Therefore D_N exceeds any fixed positive constant with
superpolynomially small environment probability.

Choose a deterministic M-periodic function f_B:Z→[0,1], obtained by
restricting a real piecewise-linear function, which equals one on B_N,
vanishes beyond distance 2r from the shifted boundaries, and has
Lipschitz constant at most 1/r. For all large N the boundary strips
are disjoint, since r/M→0.

Unimodality of the averaged binomial masses implies that the mass of
one residue class modulo M is at most C/M+C/sqrt(m). One way to see
this is to compare the sum along each arithmetic progression with the
integral of its unimodal linear interpolation, adding at most two
maximum masses; the parity sublattice changes only the constant.
There are at most C(r+1) relevant residues in the support of f_B.
Hence, uniformly in alignment,

    E_env mu_m(f_B)<=C r/M+C r/sqrt(N)→0.                  (15)

For this test, every semigroup gradient is at most 2/r. Its layer
martingale increments are at most 2/r and its predictable variance is
at most C V_(0,m)/r². By (5), outside a superpolynomially small event
V_(0,m)<=N^eta sqrt(N). Estimate (6) then gives, for fixed u>0,

 P(mu_m(f_B)−E_env mu_m(f_B)>u)
   <= superpolynomial error
      +2 exp(−c_u/[N^(eta+1/2−2beta)+N^(−beta)]).           (16)

The exponent diverges as a positive power, because
2beta−1/2−eta>0. Equations (15)–(16) prove that mu_m(B_N) exceeds
a fixed positive constant with superpolynomially small probability.

For completeness, let bar_mu be the cell distribution of X_m+v ell
under the quenched law up to m. The coupling inequality for L1 gives

 ||mu_N(coarse)−bar_mu||_1<=2mu_m(B_N)+2D_N(omega).

Using an independent averaged last segment from the same mu_m gives

 ||nu_N(coarse)−bar_mu||_1
     <=2mu_m(B_N)+2C exp(−c(log N)²).

Thus the coarse L1 distance between mu_N and nu_N is at most the
sum of these bounds, and has a superpolynomial fixed-epsilon tail.
Combining with (13) proves (1).

## 9. What this does and does not establish

All uses of ellipticity in this proof reduce to fixed-law constants
q in (0,1) and delta>0. In particular the theorem covers the exact
source's merely elliptic formulation; no unannounced uniform bound is
introduced. Both biased and symmetric averaged walks and all
deterministic interval alignments are included.

The source quantifies over every M_N→infinity, including subpolynomial
scales. The proof above cannot cover those by choosing gamma after N:
gamma is fixed, and its positive exponent margins enter the high-moment
and concentration arguments. The obstruction in this method is the
last-layer boundary smoothing, which requires r much larger than
N^(1/4), while still requiring r much smaller than M_N. Thus the
original conjecture remains unresolved after two substantive turns.

No claim is made that a counterexample must exist below this threshold,
or that the threshold is sharp. The all-moment occupation bound is a
proved tool; an all-moment bound on the instantaneous overlap or a
legitimate slow-scale rare-event construction remains separate work.

Credit for replica and exposure methods remains as in TURN_1.md.
The scalar exponential-supermartingale argument is the classical
Bernstein–Freedman method, reproduced here in the needed form. No
novelty or priority assertion is made for this partial theorem.
