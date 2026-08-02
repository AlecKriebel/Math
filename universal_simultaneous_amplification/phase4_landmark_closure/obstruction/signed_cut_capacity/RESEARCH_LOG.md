# Research log: signed cut capacity at fitness `r=3/2`

## 2026-08-02 08:10 PDT

Started from the exact drift bridge in
`cross_sum_three_halves/PRODUCT_AND_DRIFT_CERTIFICATES.md`.  The target is
an occupation-measure or weighted-adjoint control of the sole signed term

\[
 B(S)-\frac{|S|(n-|S|)}{n-1}.
\]

No literature search or external communication is being used.  Pointwise
common corrections, radial monotonicity, and broad numerical searches are
excluded because those routes have already failed or been exhausted.

## 2026-08-02 08:40 PDT

Inserted the conservative arrow-reversed dual `C` between the Bd dual `L`
and geometric-burst dB dual `D`.  The desired product inequality follows
from the two still-open factors

\[
 m_Lm_C\le(m_B^K)^2,
 \qquad
 m_D/m_C\le m_D^K/m_B^K.
\]

The stronger adjoint sum `m_L+m_C<=2m_B^K` survived exact rational checks
and targeted separated-scale optimization through order five.  A proposed
rank-likelihood strengthening initially survived optimization, but a direct
order-six search exposed a star limit.  Simplifying it gave the exact
smallest witness `K_(1,4)`: `h_4-h_3=126581643/905995090>0`.  The desired
sum still has strict gap `14979081573/95582481995` on this witness.

Derived the exact density equations `Cf=-Vf`, `Lg=Vg` and the entropy
identities

\[
 E_{pi_C}V=-E_{pi_C}I_C(f)\le0,
 \qquad E_{pi_L}V=E_{pi_L}I_L(g)\ge0.
\]

Also derived the exact adjacent-rank capacity identity (8)--(9) in
`ADJOINT_LEVEL_CAPACITY.md`.  It isolates a surviving levelwise conjecture
`sum_(|A|=k)(f-g)V>=0`, plus two symmetric-capacity dispersion terms.

Four stronger shortcuts were exactly falsified and preserved:

- level-mean `f` times level-mean `g` exceeds one on a weighted triangle;
- pointwise `(f-g)V` is negative on the four-star;
- pointwise `fg<=1` fails on an explicit integer-weight order-five graph,
  with exact excess greater than `0.0049`.
- rank MLR fails on the unweighted five-star even though the target adjoint
  mean sum retains a strict positive gap.

The exact verifier passes.  For the batching factor, derived the full
rank-boundary flux identity for the geometric burst.  Downward crossing of
boundary `k` comes only from rank `k+1` and has exact capacity
`sum_v (1-x_v)/(1+a x_v)`; upward crossing retains the unavoidable
multi-rank union term.  No monotone dB/C rank ratio survived even the
four-star, so factor two remains open.

## 2026-08-02 09:00 PDT

Derived the exact reversible Poisson reduction.  With `M=(L+C)/2`,
`K=(L-C)/2`, `kappa=|A|-m_B^K`, and `M phi=kappa`,

\[
 2m_B^K-m_L-m_C=\langle K\phi,f-g\rangle_\mu.
\]

Attractiveness proves that `phi` decreases under set inclusion.  Its radial
part is charged with the correct sign by the surviving level-temperature
conjecture, but the within-rank remainder is genuinely negative on stars;
on `K_(1,4)` the radial and remainder contributions are approximately
`0.98483` and `-0.82812`.  A quantitative Dirichlet or conditional-entropy
bound is therefore necessary.

Direct separated-scale optimization of every individual level sign through
order six found no negative value; the smallest order-six result was about
`2.5e-8` near a symmetric boundary.  The adjoint sum itself also survived a
dedicated order-six optimization.

Exactly solved the symbolic weighted-triangle adjoint ranks.  The top gap
`h_2-h_3` has numerator `95 P`, where

\[
P=e_1^3e_3+56e_1^2e_2^2-60e_1e_2e_3-149e_2^3.
\]

Because `P` is affine in `e_3`, its minimum at fixed `e_1,e_2` occurs at a
zero-root or double-root endpoint.  The exact endpoint factors are positive,
proving `h_2>=h_3`, strictly away from equal weights.  The independent
symbolic verifier passes.  The lower triangle boundary remains open.

## 2026-08-02 09:05 PDT

Exposed the adjoint defect as the exact additive vertex potential

\[
 V(A)=r\sum_{i\in A}(1-t_i),\qquad
 t_i=\sum_jP_{ji},\qquad \sum_i(1-t_i)=0.
\]

This reduces each separate level-temperature conjecture exactly to an
aggregate covariance between the zero-sum column imbalance `1-t_i` and the
rank-conditioned inclusion probability of vertex `i`.  It is a meaningful
dimension reduction, but a vertexwise rearrangement is too strong: the
weighted `K_4` with lexicographic edge weights `(1,1,2,3,1,2)` has an exact
negative Bd singleton-pair contribution while the total covariance remains
positive.

Tried to localize the global entropy identities by conditioning on, or
killing outside, a fixed rank.  The exact remaining term is

\[
 \mathcal B_k^Q=\sum_{A\in R_k,B\notin R_k}
 \{\pi(A)Q(A,B)\psi(B)-\pi(B)Q(B,A)\psi(A)\}.
\]

It is the neighboring-rank source forcing for the killed block and has no
fixed sign.  On `K_(1,4)`, numerical evaluation gives negative values for
both an `L` level and a `C` level, compensated by positive entropy
remainders.  Therefore conditional entropy alone does not prove the level
signs; closure would require a quantitative trace/entropy inequality that
dominates the negative boundary forcing.  The verifier now checks the
linear-potential identity, the boundary integration identity over exact
rationals, and the pairwise counterexample.
