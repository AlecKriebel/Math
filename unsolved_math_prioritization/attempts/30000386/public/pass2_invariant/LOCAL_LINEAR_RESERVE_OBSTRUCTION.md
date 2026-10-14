# Sharp mass cost of a local linear one-round reserve

Status: exact obstruction for a precisely stated certificate class.
This is not an impossibility theorem for arbitrary online strategies,
nonlinear hazards, or hazards restricted to specially structured fields.

## 1. One-step certificate class

Let `N={-1,0,1}^2` be the nine next positions relative to a current
position. A nonnegative local linear test is specified by weights
`w_v>=0`, `v in N`. Call the test robust if for **every** nonnegative
field `g:N->[0,infinity)`,

`sum_{v in N} w_v g(v) < 1`

implies that after any one unit point update to `g`, at least one of the
nine resulting values is strictly below one. Such an update models a
boundary announcement at the next lethal time. Point updates outside
`N` do not affect the condition.

This robustness requirement is equivalent to

`sum_{v in A} w_v >= 1 for every eight-element subset A of N`.

**Necessity.** If some such subset has weight sum below one, set `g=1`
on those eight positions and `g=0` on the ninth. The linear test passes,
but updating the ninth position makes every possible move lethal.

**Sufficiency.** If fewer than two positions had value below one, there
would be an eight-element subset with all values at least one, making
the linear test at least one. Thus a field passing the test has at
least two subunit positions. A single point update can affect at most
one of them, leaving a safe choice.

## 2. Sharp minimum mass and uniqueness

Write `S=sum_v w_v` and `M=max_v w_v`. The eight-subset condition is
equivalent to `S-M>=1`. Since `M>=S/9`,

`1 <= S-M <= 8S/9`,

and therefore

`S >= 9/8`.

Equality forces `M=S/9`, which means that all nine weights are equal.
Thus the unique minimum-mass robust test is

`w_v=1/8 for every v in N`.

The usual uniform one-step smearing already achieves the optimal mass
within this class. Merely making its local weights nonuniform cannot
remove the `9/8` inflation.

## 3. Consequence for repeated local positive linear smoothing

Suppose a chain of one-round deadline reductions uses convolution
kernels `W_1,...,W_k`, each supported in `N` and satisfying the robust
test above. The effect of a remote single point bomb after all these
reductions is the nonnegative kernel

`K_k=W_1*...*W_k`.

Nonnegative convolution multiplies total masses, so

`||K_k||_1 >= (9/8)^k`.

Its support lies in `[-k,k]^2`, with at most `(2k+1)^2` points. Hence

`||K_k||_infinity >= (9/8)^k/(2k+1)^2`,

which diverges with `k`. Therefore neither the total update mass nor
its peak can remain uniformly bounded through arbitrarily long chains
of these locally robust positive linear reductions. Likewise, the
largest average over a side-three square is at least one ninth of this
peak and is unbounded.

This rules out repairing unrestricted deadline coupling solely by
choosing nonuniform weights in the same local linear reserve scheme
and hoping for a uniform mass or concentration budget. It does not rule
out nonlinear tests, simultaneous treatment of several deadlines,
configuration-sensitive field restrictions, or different online states.

## 4. Concrete limitation of the uniform profile recursion

The exact recursive certificate in `CONCENTRATION_PROFILE_LEMMA.md`,
when every gap equals one, has `L=3,w=0` and denominator

`D=9[1-c(3)]`.

The current-deadline delta kernel is always one of its update types, so
`c(3)>=1/9` and `D<=8`. Every positive step therefore multiplies the
oldest update kernel's mass by at least `9/8` and expands its support by
at most one in each direction. The preceding bound eventually forces
`c(3)>=1`, at which point a positive next denominator is impossible.
This is an analytic finite-failure argument, not merely tested horizons.

The exact-rational implementation in `profile_certificate.py` locates
the first nonpositive denominator of this specific recursion at its
27th consecutive one-round smoothing. That calculation identifies an
earlier failure than the crude analytic bound; it does not imply a
losing game with 28 allowed times.
