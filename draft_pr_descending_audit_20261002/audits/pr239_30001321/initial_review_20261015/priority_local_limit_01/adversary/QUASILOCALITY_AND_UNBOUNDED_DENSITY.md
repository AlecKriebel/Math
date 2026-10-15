# Finite-alphabet quasilocality versus an unbounded stationary density

Independent mathematical addendum requested 2026-10-15 UTC. This proves two
lemmas, then states a conditional incompatibility. It does **not** identify the
BMP correction field with the JRS invariant density, and it makes no assertion
that an unread BMP1999 theorem is false.

## 1. Uniform finite-cylinder oscillation forces boundedness

Let `S` be a finite set, `I` a countable index set, and `Omega subset S^I` a
nonempty configuration space. Let `Phi:Omega -> R` be finite valued. Suppose
there are finite sets `K_m subset I` such that

`osc_m(Phi) := sup{|Phi(eta)-Phi(zeta)|:
                  eta,zeta in Omega, eta|K_m=zeta|K_m} -> 0`.

Then `Phi` is bounded. Indeed choose `m` with `osc_m(Phi)<=1`. There are at
most `|S|^|K_m|` nonempty cylinder classes. Choose one configuration in each.
The finitely many representative values have finite maximum absolute value
`A`. Every configuration agrees with its class representative on `K_m`, so
`|Phi|<=A+1` everywhere. If the condition is imposed only on a common full-
probability domain, the same proof gives essential boundedness on that domain.

The conclusion requires **uniform oscillation in the function's values**, not
merely `L2` cylinder approximation, convergence in probability, or a covariance
bound. Finite-alphabet local approximants are automatically bounded, but their
norms could grow with `m`; one fixed approximant with uniformly bounded error
already suffices for boundedness of `Phi`.

## 2. The JRS density is essentially unbounded for a genuine two-atom law

Assume `0<r<1/2` and that the i.i.d. scalar environment takes values `r` and
`1-r`, **both with positive probability**. The latter condition matters: a
one-atom deterministic law has stationary density one and is not covered by
the construction.

Use the parity shear `Y_t=(X_t+t)/2` to obtain the span-one `{0,1}` model.
JRS Proposition 3.1 constructs the past-environment martingale

`f_T(omega)=sum_z pi^omega_{-T,0}(z,0)`

in these sheared coordinates, with `f_T -> f` in `L2`. In particular, for the
sigma-field `G_T` of the last `T` complete environment layers,

`E[f | G_T]=f_T`.

We show that `ess sup f_T` grows at least linearly in `T` by an event of
positive probability, and conclude that `f` cannot be essentially bounded.

### A deterministic inward-funnel kernel

On the original integer line let `P` be the nearest-neighbor transition matrix
with right-jump probabilities

`a_x = 1-r for x<=0;    a_x = r for x>=1`.

The drift points toward the central edge `{0,1}`. Put `d=1-2r>0`. Directly
checking each column gives

`sum_x P(x,y)=1+d[1_(y=0)+1_(y=1)]`.

Write `u_T(y)=sum_x P^T(x,y)`. Although the vector of initial ones has infinite
total mass, each coordinate sum is finite by the bounded jump range. Iterating
the displayed column-sum identity therefore gives the exact finite identity

`u_T(0)=1+d sum_(s=0)^(T-1)[P^s(0,0)+P^s(1,0)]`.             (F1)

No positive-recurrence convergence theorem is needed to lower-bound this sum.
Set `rho=r/(1-r)<1` and `A=(1-rho)/2`. The probability distribution

`pi_x=A rho^(-x)` for `x<=0`,

`pi_x=A rho^(x-1)` for `x>=1`

has total mass one and satisfies detailed balance for `P`; in particular
`pi_0=pi_1=A>0`. For every `n>=0`, reversibility and Cauchy–Schwarz yield

`P^(2n)(0,0)
 = sum_z P^n(0,z)P^n(z,0)
 = pi_0 sum_z P^n(0,z)^2/pi_z
 >= pi_0 [sum_z P^n(0,z)]^2 / sum_z pi_z
 = pi_0`.

Retaining just these even terms in (F1),

`u_T(0) >= 1+d pi_0 ceil(T/2) -> infinity`.                  (F2)

This argument handles the original chain's period two explicitly.

### Positive-probability finite environment events

To determine the endpoint-zero column sum over `T` steps it is enough to know
the environment at the finite backward parity cone

`C_T={(-k,x): 1<=k<=T, |x|<=k, x congruent k mod 2}`.

There are `sum_(k=1)^T(k+1)=T(T+3)/2` such sites. Impose the deterministic
pattern `p_(-k,x)=a_x` on this cone. Both values of `a_x` are atoms with positive
probability, so the finite event `E_T` has positive probability. No assignment
outside this cone can affect any path that ends at zero at time zero.

At time `-T`, sheared starting coordinate `z` corresponds to original starting
position `x=2z+T`. Consequently the sheared finite-past column sum on `E_T` is

`f_T = sum_z P^T(2z+T,0) = sum_x P^T(x,0) = u_T(0)`.

The middle equality holds because all starting positions of the other parity
have zero transition probability to zero after `T` steps. Thus (F2) is a lower
bound for `f_T` on an event of positive probability.

If `f<=B` almost surely for a finite constant `B`, conditional expectation
would give `f_T=E[f|G_T]<=B` almost surely for every `T`. Choose `T` so large
that the right side of (F2) exceeds `B`; the event `E_T` contradicts that bound.
Therefore

`ess sup f=infinity`.

This conclusion concerns the stationary density from JRS, not a tail of the
single-origin coarse discrepancy. The small probabilities of the funnel
events are entirely compatible with strong concentration statements of other
quantities.

## 3. Exactly what follows, and what does not

If an earlier result has a real correction field `Phi` on a finite alphabet
with the **uniform cylinder-oscillation** property in Section 1, then `Phi` is
bounded. It cannot equal the JRS `f` almost surely for the genuine two-atom law
of Section 2. Equality in distribution would also be impossible.

An identification `Phi=f` must nevertheless be proved before this can constrain
an interpretation of the earlier result. The two lemmas alone do not show that
the earlier theorem is false, that its correction is the same invariant
density, that a secondary account states every hypothesis, or that its
definition of quasi-concentration is literally the uniform oscillation
condition used here. In particular, `L2` quasilocal approximation would not
force boundedness and would present no contradiction.

The JRS input is the already independently retrieved full primary source
`https://www.math.utah.edu/~firas/Papers/walkers.pdf`, SHA256
`6dfd26c58e1f8bbc5e45ba2bbcedf9d96fcb10d1356d65b0ae0c3596c92e5690`,
Proposition 3.1. The finite-alphabet lemma is stated under the exact mathematical
condition supplied in the request; source-specific identification is left open.

## 4. Checkable controls

`check_inward_funnel.py` computes `P^T(x,0)` by exact rational backward
recursion. It verifies (F1), the linear lower bound (F2), parity, and even-time
return lower bounds for `T=0,...,64` at `r=1/10,1/4,2/5`. No truncated-chain or
floating-point approximation is involved. The analytic argument proves the
claim for every `T` and every `0<r<1/2`.
