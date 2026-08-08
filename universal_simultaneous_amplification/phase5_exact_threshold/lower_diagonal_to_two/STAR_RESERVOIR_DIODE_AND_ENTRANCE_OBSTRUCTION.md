# The star--reservoir diode and its separated entrance obstruction

Date: 2026-08-08 (America/Los_Angeles)

## Status and scope

Two exact facts are proved here.

1. A star placed between two large clique reservoirs is a genuine diode in
   the same direction for Bd and dB.  The two-interface favorable/adverse
   odds products are displayed exactly below; the dB product gains a factor
   tending to `r^4`, while the Bd product is exponentially stronger in the
   number of leaves.
2. This does **not** produce a lower construction when the reservoirs and
   antennas resolve before their cross events.  For every fixed `r>5/3`, a
   cycle with at least two clique reservoirs and one star antenna per
   reservoir is eventually dB-suppressing, even if fixation is granted with
   probability one after the initially occupied component fixes.

The second statement is an obstruction only for the explicitly separated
component architecture.  It identifies the necessary escape: the
star--reservoir coupling must act before a singleton in its clique or star
locally absorbs, and its positive entrance correction must be of order at
least the inverse reservoir size.

## 1. Exact isolated components

Fix `r>1`.  Write `K_C` for the unit clique of order `C` and `S_L` for the
unit star with `L` leaves.  Let `k_U^+` be uniform-singleton fixation in
`K_C` at fitness `r`, and let `k_U^-` be fixation of a singleton type of
relative fitness `1/r`.  Direct solution of the count chain gives

\[
 k_B^+={1-r^{-1}\over1-r^{-C}},\qquad
 k_B^-={r-1\over r^C-1},                              \tag{1}
\]

\[
 k_D^+={C-1\over C}{1-r^{-1}\over1-r^{-(C-1)}},\qquad
 k_D^-={C-1\over C}{r-1\over r^{C-1}-1}.             \tag{2}
\]

Consequently

\[
 {k_B^+\over k_B^-}=r^{C-1},\qquad
 {k_D^+\over k_D^-}=r^{C-2}.                         \tag{3}
\]

For the star, let `H_U(q)` and `E_U(q)` denote fixation at relative fitness
`q` from the hub and from one specified leaf.  The changing-event equations
on `(hub type, mutant-leaf count)` give

\[
 H_D(q)={qL+1\over(q+1)(L+1)},\qquad
 E_D(q)={q(qL+1)\over(q+1)L(L+2q-1)}.                \tag{4}
\]

For Bd put

\[
 \theta_q={L+q\over q(qL+1)},\qquad
 D_q={q\over L}+{1-\theta_q^L\over1-\theta_q}.
\]

Then

\[
 H_B(q)={q\over LD_q},\qquad E_B(q)={q^2\theta_q\over D_q}. \tag{5}
\]

At `q=1` the expressions are read by continuity.  Equations (4)--(5) are
obtained from the two changing events in each orbit state, not imported
fixation formulas.

The rooted forward/reverse ratios simplify to

\[
 {E_D(r)\over H_D(1/r)}
 ={r(L+1)(Lr+1)\over L(L+r)(L+2r-1)},                \tag{6}
\]

\[
 {E_B(r)\over H_B(1/r)}
 ={L(L+r)\{r(Lr+1)\}^L\over (L+r)^L(Lr+1)}.         \tag{7}
\]

## 2. Exact two-interface diode odds

Join a source `K_C` weakly to all `L` leaves, using distinct reservoir
vertices, and join the hub weakly to a target `K_C`.  Cross weights tend to
zero relative to all internal edges, so an introduction locally absorbs
before the next cross event.  Cross-weight magnitudes cancel from the
favorable/adverse odds at each interface.

For Bd the source--leaf interface contributes

\[
 r{1\over C-1}{E_B(r)\over k_B^-},
\]

and the hub--target interface contributes

\[
 r{C-1\over L}{k_B^+\over H_B(1/r)}.
\]

Their product is

\[
 \boxed{\mathcal O_B
 =r^{C+1}{L+r\over Lr+1}
   \left\{{r(Lr+1)\over L+r}\right\}^{L}.}          \tag{8}
\]

For dB the corresponding degree factors are reversed.  The two interface
odds are

\[
 r^2(C-1){E_D(r)\over k_D^-},\qquad
 r^2{L\over C-1}{k_D^+\over H_D(1/r)},
\]

and hence

\[
 \boxed{\mathcal O_D
 =r^{C+3}{(L+1)(Lr+1)\over(L+r)(L+2r-1)}.}           \tag{9}
\]

Thus, for fixed `r>1`,

\[
 \mathcal O_D\sim r^{C+4},
 \qquad
 \mathcal O_B\asymp r^{C+2L}                        \tag{10}
\]

up to factors subexponential in `C+L`.  The star therefore points from its
leaves to its hub under both rules.  In a hierarchy where the source
interface is faster than the target interface, the effective favorable to
adverse reservoir odds equal the target-interface odds times one plus the
source-interface odds, and are asymptotic to (8)--(9).

## 3. Uniform dB entrance mass

The diode calculation is conditional on having a monomorphic mutant
component.  Uniform initialization imposes a different constraint.

The total dB singleton fixation mass of `S_L` is, directly from (4),

\[
 T_L(r):=H_D(r)+L E_D(r)
 ={(Lr+1)(Lr+L+3r-1)\over
   (L+1)(r+1)(L+2r-1)}.                              \tag{11}
\]

Put `p=(r-1)/r`.  One clique reservoir contributes

\[
 Ck_D^+={(C-1)p\over1-r^{-(C-1)}}=Cp-p+o(1).         \tag{12}
\]

Even if local component fixation is followed by global fixation with
probability one, one reservoir--antenna block therefore has average at most

\[
 U_{C,L}(r)=
 {Ck_D^++T_L(r)\over C+L+1}.                         \tag{13}
\]

The exact leading excess over `p` is

\[
 A_L(r):=T_L(r)-p(L+2).                              \tag{14}
\]

It has the transparent comparison

\[
 \boxed{
 A_L(r)-A_1(r)=
 -{(L-1)(r-1)
 [L^2r+L^2+Lr^2+Lr+r-1]
 \over r(L+1)(r+1)(L+2r-1)}\le0,}                   \tag{15}
\]

and

\[
 A_1(r)=-{2r-3\over r}.                              \tag{16}
\]

Thus a larger antenna only worsens the separated uniform entrance balance.

## 4. The `5/3` class obstruction

Take `m>=2` identical blocks and let

\[
 n=m(C+L+1).
\]

The complete-graph dB baseline is

\[
 \rho_D(K_n,r)
 ={n-1\over n}{p\over1-r^{-(n-1)}}.                 \tag{17}
\]

Multiplying the difference between (13) and (17) by `C+L+1` and using
(12) gives

\[
 (C+L+1)\{U_{C,L}-\rho_D(K_n,r)\}
 =A_L(r)+{p\over m}+o(1).                            \tag{18}
\]

Uniformly over `m>=2,L>=1`, (15)--(16) imply

\[
 A_L(r)+{p\over m}
 \le A_1(r)+{p\over2}
 =-{3r-5\over2r}.                                   \tag{19}
\]

This is strictly negative for every `r>5/3`.

> **Theorem (separated star--reservoir obstruction).**  Fix `r>5/3`.
> Consider any sequence made from at least two identical `K_C` reservoirs
> and one `S_L` antenna per reservoir, with `C->infinity`, `1<=L<=C`, and
> component-separation error `o((C+L)^{-1})` in uniform-singleton fixation.
> Then, for all sufficiently large `C`, its dB fixation probability is
> strictly below that of the complete graph of the same order.  This remains
> true if global fixation is granted whenever the initially occupied local
> component fixes.

The theorem covers the proposed three-scale implementation in which the
star and clique locally absorb before star--reservoir or intermodule portal
events.  It does not cover a coupling that acts while the initial clique or
star is polymorphic.  Such a nonseparated entrance correction is now a
necessary ingredient, not an optional refinement.

## 5. Exact replay

`verify_star_reservoir_diode.py`:

1. solves the star orbit chains exactly for integer orders and both rules;
2. checks (1)--(9) symbolically;
3. checks the entrance identity (15) and the sharp bound (19);
4. confirms the finite comparison at exact rational test parameters.

All computations use exact rational functions.  Floating plots and sampled
fixation probabilities are not used in the theorem.
