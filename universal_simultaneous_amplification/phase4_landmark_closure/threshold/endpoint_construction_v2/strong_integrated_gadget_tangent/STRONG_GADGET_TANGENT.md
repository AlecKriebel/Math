# Strong integrated finite-gadget tangent cone

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Scaling and exact coefficient formula

Let a fixed gadget have `s` labelled vertices, symmetric internal weights
`a_ij>=0`, and portal loads `x_i>=0`.  In a graph with a large unit clique
of order `C`, give internal gadget edge `ij` weight `C a_ij` and join gadget
vertex `i` to every clique vertex with edge weight `x_i`.  Put

\[
                         d_i=x_i+\sum_j a_{ij}.           \tag{1}
\]

At least one portal is positive and every `d_i` is positive.  A dilute
growing population of such gadgets has density `q/C->0`; different gadgets
interact only at second order.

For rule `U`, let `u_U(X)` be the probability that the limiting local chain,
started with mutant gadget set `X` and no core mutants, produces a surviving
core lineage.  The local chain is finite and follows directly from the update
rules:

- under Bd, internal parent--target rate is `fitness(i)a_ij/d_i`, resident
  core recovery of mutant `i` has rate `x_i`, and a mutant `i` creates a
  successful core mark at rate `(r-1)x_i/d_i`;
- under dB, gadget vertex `i` dies at rate one and chooses among internal
  neighbors plus resident core load `x_i`, while all mutant gadget vertices
  together create successful core marks at rate
  `(r-1) sum_(i in X) x_i`.

Write `u_U(i)=u_U({i})`, `p=1-1/r`, and `P=sum_i x_i`.  The local singleton
terms alone are not the population tangent.  Substitution of

\[
                         f_X(k)=1-r^{-k}\{1-u_U(X)\}      \tag{2}
\]

into the exact core-count/gadget-mask generator gives the resident-gadget
residuals

\[
 s_B=r\sum_i x_i u_B(i)-(r-1)\sum_i{x_i\over d_i},      \tag{3}
\]

\[
 s_D=r\sum_i{x_i u_D(i)\over d_i}
           -(r-1)(P+r-1).                               \tag{4}
\]

The leading core branching generator maps `k r^{-k}` to
`-(r-1)k r^{-k}`.  Hence the ordinary-singleton Poisson term is
`s_U/[Cr(r-1)]`.  Averaging all singleton starts and subtracting the exact
complete-graph baselines yields

\[
 \boxed{B_H={\sum_i u_B(i)\over p}-s+{s_B\over(r-1)^2},}\tag{5}
\]

\[
 \boxed{D_H={\sum_i u_D(i)\over p}-s+1+{s_D\over(r-1)^2}.}\tag{6}
\]

The `+1` in (6) is the `-p/C` term of the complete dB baseline.  Equations
(3)--(6) reproduce the independently audited one-heavy-leaf formulas when
`s=2`, `x=(1,0)`, and `a_12=tau`.

Mixing `lambda` ordinary common-hub leaves per gadget changes the vector to

\[
                  (B_H+\lambda/(r-1),D_H-\lambda).       \tag{7}
\]

The necessary separator and optimally balanced coefficient are

\[
 S_H=D_H+(r-1)B_H,qquad M_H=S_H/r                       \tag{8}
\]

when the equalizing leaf count is nonnegative.  The optimizer uses the exact
version of (7), including the boundary case `lambda=0`.

## 2. Exact portal-clone obstruction

Set every internal leading weight to zero, but allow arbitrary positive
portal loads `x_1,...,x_s`.  Each gadget vertex is an independent portal
clone.  Its local singleton probabilities are

\[
 u_B(i)={r-1\over r-1+x_i},\qquad
 u_D(i)={(r-1)x_i\over1+(r-1)x_i}.                      \tag{9}
\]

Substitution into (3)--(6) gives the exact all-order identity

\[
 \boxed{B_H=0,qquad
 D_H=-\sum_{i=1}^s{(x_i-1)^2\over1+(r-1)x_i}\le0.}      \tag{10}
\]

Equality holds exactly when every `x_i=1`, in which case the defect is
asymptotically indistinguishable from adding ordinary clique vertices.  Thus
the most persistent optimizer boundary is an exact equality class, never a
strict simultaneous amplifier.

This obstruction holds for every order and every positive portal vector.  It
also describes internal weights `a_ij=o(1)` by continuity.  It is a broad
parameterized class theorem, not an obstruction for arbitrary positive
internal matrices.

## 3. Bounded hostile search

`search_integrated_gadgets.py` optimized all entries of a complete symmetric
internal matrix and every portal load for orders three through seven.  It
used the finite local chains and full coefficients (3)--(7), not the
local-only proxy.  Fitness values were `1.51`, `1.55`, and `2`.

No strict positive balanced coefficient was found.  Two boundary mechanisms
recurred:

1. all internal weights tend to zero and all portals tend to one, giving the
   exact equality (10);
2. two vertices form a strong pair with vanishing portals while the remaining
   vertices become portal clones.  This converges to the already-proved rare
   `K_2` tangent.  At `r=1.51` its optimized separator is approximately
   `-0.0287897442`, already below zero.

Interior discovery runs were strictly negative.  Representative best
balanced values before explicitly seeding the equality boundary were about
`-0.0194` at `r=1.51`, `-0.0904` at `r=1.55`, and `-0.2615` at `r=2`.
After the equality seed is included, every order returns zero from below.

These optimization statements are **NUMERICALLY OBSERVED** and do not prove
the all-matrix sign.  The formulas (3)--(6), labelled lumping audit, and
portal-clone obstruction (10) are **PROVED / EXACTLY COMPUTED**.

## 4. Outcome

This bounded cycle found no family improving

\[
                         R_*=1.5028569127905696\ldots .
\]

It closes the full portal-clone boundary exactly and explains why unconstrained
optimizers falsely appear to approach a new optimum there.  Weighted strong
integrated gadgets with genuinely positive internal matrices remain an open
class; no numerical lead survived the corrected far-field calculation.
