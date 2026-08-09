# Singular period-two clone kernels have exact cost twice gain

Date: 2026-08-08 (America/Los_Angeles)

## Status and scope

This note closes a global, finite-amplitude boundary of the growing-rank
adjoint branching normal form.  It is not a perturbation about a regular
kernel and it permits the latent rank, type masses, and all mass ratios to
vary arbitrarily.

Let `I` be a finite type set, let `phi:I->I` be an involution, and let `p`
be any strictly positive probability law.  Consider the deterministic
period-two kernel

\[
                 P_{ij}={\bf1}_{\{j=\phi(i)\}}.       \tag{1}
\]

Fixed points of `phi` are allowed.  This is the maximally singular
negative-correlation boundary of the latent-kernel model.  It is realized
by undirected clone graphs: a two-cycle is a complete bipartite block with
arbitrary unequal side masses, and a fixed point is a complete block.

At fitness two, write `beta` and `sigma` for the uniformly averaged
positive survival probabilities of the exact rare-mutant Bd and dB
branching traces.  Then

\[
 \boxed{\displaystyle
       {1\over2}-\sigma
       =2\left(\beta-{1\over2}\right)\ge0.}          \tag{2}
\]

Thus every positive Bd gain on this boundary pays exactly twice that gain
as dB cost.  In particular no trace-resolved growing-rank diagonal of these
kernels, even with type ratios tending to zero or infinity, can have

\[
 {B_k\over c_k}\longrightarrow b>0,
 \qquad {D_k\over c_k}\longrightarrow0.             \tag{3}
\]

The theorem is global in the type imbalance; it strictly extends the
previously proved *quadratic* period-two equality at a regular base.  It
does not cover a completion whose kernel perturbation is of the same order
as the response, non-deterministic correlated kernels, or order-one
within-colony collisions.

## 1. Exact adjoint branching systems

The `p`-adjoint and temperature of (1) are

\[
 (P^*)_{ij}={p_j\over p_i}{\bf1}_{\{i=\phi(j)\}},
 \qquad
 t_i=(P^*{\bf1})_i={p_{\phi(i)}\over p_i}.           \tag{4}
\]

At `r=2`, the exact survival equations from the diffuse clone trace are

\[
 t_i b_i=2(1-b_i)b_{\phi(i)},                        \tag{5}
\]

\[
 s_i=2(1-s_i)t_i s_{\phi(i)}.                       \tag{6}
\]

These are the full positive survival systems; no weak-heterogeneity
expansion is being taken.  The Perron root is two on every orbit, so the
displayed nonzero solutions are the unique positive solutions.

A fixed point has `t_i=1` and

\[
                         b_i=s_i={1\over2}.          \tag{7}
\]

Now take a two-cycle `{i,j}` and put

\[
                         a={p_j\over p_i}>0.          \tag{8}
\]

Solving (5) gives

\[
 b_i={3\over2(a+2)},
 \qquad
 b_j={3a\over2(2a+1)}.                              \tag{9}
\]

Equation (6) has the reversed solution

\[
                         s_i=b_j,\qquad s_j=b_i.     \tag{10}
\]

One can also obtain (9) without elimination: multiplication of the two
equations in (5) gives

\[
                    (1-b_i)(1-b_j)={1\over4},        \tag{11}
\]

and either equation then gives (9).

## 2. Orbitwise sharp identity

Normalize the mass of the two-cycle to one, so its two masses are
`1/(1+a)` and `a/(1+a)`.  Equations (9)--(10) give

\[
 \beta_a={3(a^2+a+1)\over2(a+2)(2a+1)},             \tag{12}
\]

\[
 \sigma_a={9a\over2(a+2)(2a+1)}.                   \tag{13}
\]

Therefore

\[
 \beta_a-{1\over2}
 ={(a-1)^2\over2(a+2)(2a+1)}\ge0,                  \tag{14}
\]

and direct subtraction gives

\[
 {1\over2}-\sigma_a
 ={(a-1)^2\over(a+2)(2a+1)}
 =2\left(\beta_a-{1\over2}\right).                 \tag{15}
\]

The full type space is a disjoint union of fixed points and two-cycles.
Weighting (7) and (15) by their total `p`-masses proves (2).  Equality with
zero gain occurs precisely when every positive-mass two-cycle is balanced,
`p_i=p_{\phi(i)}`.

## 3. Finite connected realizations and the stopped-chain passage

For rational `p`, take `mp_i` clones of type `i`.  For a two-cycle join the
two clone classes completely with a common positive weight; for a fixed
point join its clone class completely.  The self-omission in a fixed block
is `O(1/m)`.  Add an arbitrarily smaller positive rational spanning
completion between the blocks to make the finite loopless undirected graph
connected.

For any fixed mutant cutoff `K`, first sending the completion kernel to
(1) and then the clone multiplier `m` to infinity makes the stopped finite
type-count chain converge entrywise to (5)--(6).  Uniform singleton
initialization has type law `p` exactly.  Fixation is contained in the event
of reaching `K`; hence, after subsequently sending `K` to infinity,

\[
 \limsup\rho_{Bd}\le\beta,
 \qquad
 \limsup\rho_{dB}\le\sigma.                         \tag{16}
\]

This one-sided passage includes every post-establishment path because it
only uses the necessary event `fixation => hit K`; it does not assume that
independent lineages remain valid after `K` mutants.

For a growing profile let `c_k>0` be the proposed catalyst scale.  Choose
the positive completion, cutoff, and clone multiplier diagonally so all
stopped-chain errors are `o(c_k)`, and require `1/n_k=o(c_k)` so the exact
complete-graph finite-size corrections are negligible.  Put

\[
 G_k=\beta_k-{1\over2}\ge0.
\]

Equations (2), (16), and the exact complete baselines imply

\[
 \rho_{Bd}(G_k,2)-\rho_{Bd}(K_{n_k},2)
                    \le G_k+o(c_k),                 \tag{17}
\]

\[
 \rho_{dB}(G_k,2)-\rho_{dB}(K_{n_k},2)
                    \le-2G_k+o(c_k).                \tag{18}
\]

If the left side of (17), divided by `c_k`, has a positive lower limit,
then `G_k/c_k` has at least that lower limit and (18) is bounded above by
twice its negative.  This proves the catalyst obstruction (3).

## 4. Exact scope ledger

**PROVED:** the atomic adjoint systems (5)--(6), their unique positive
orbit solutions, the sharp global identity (2), arbitrary growing latent
rank and mass imbalance, exact uniform initialization, and the one-sided
post-establishment obstruction (17)--(18).

**NOT PROVED:** the conjectural inequality (2) for every stochastic
kernel; stability under same-scale non-period-two completion; non-diffuse
colony collisions; or a lower construction approaching fitness two.

The surviving catalyst must therefore leave this maximally anticorrelated
deterministic boundary at its response scale, rather than merely send more
type masses to zero or add more period-two blocks.

## 5. Exact replay

`verify_singular_period_two_catalyst.py` reconstructs (4)--(15)
symbolically and checks a growing-rank rational involution by exact
arithmetic.
