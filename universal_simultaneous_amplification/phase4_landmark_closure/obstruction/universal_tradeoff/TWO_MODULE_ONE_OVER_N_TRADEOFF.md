# Exact `1/n` Bd--dB tradeoff for two weak complete modules

Date: 2026-08-02 (America/Los_Angeles)

## Status

The rare-event formulas and the asymptotic theorem below are **PROVED**.
They resolve the cross-rule question for two internally complete modules
whose sizes, proportions, and internal weighted-degree scales may all vary
with population size.

The result has two parts.

1. If both module sizes diverge, the graph is dB-suppressing by
   `(1-1/r)/n+o(1/n)`, independently of its two degree scales.  Thus two
   genuinely mesoscopic weak modules cannot occur in an eventually
   dB-amplifying family.
2. If one module remains bounded and the weak-cut graph nevertheless dB
   amplifies, its scale ratio is forced into a range where Bd is suppressing
   by an explicit positive constant times `1/n`.

Consequently, at every fixed `r>3/2`, eventual strict dB amplification
forces Bd suppression throughout this two-module model.  In fact the
implication remains true for every fixed `r>1`; the threshold `3/2` only
makes the list of possible bounded modules especially short.  This is a
family theorem, not a universal graph theorem.

## 1. Model and separation convention

Let `A,B` be complete modules of sizes `ell,m>=2`, with `n=ell+m`.  Give
every internal `A` edge weight `alpha/(ell-1)`, every internal `B` edge
weight `beta/(m-1)`, and every cross edge a common positive weight
`epsilon`.  The parameters `ell,m,alpha,beta` may vary with `n`.  Put

\[
 \sigma=\frac{\beta}{\alpha}.
 \tag{1}
\]

We first take the exact separated weak-cut limit `epsilon->0` with the other
parameters fixed.  The notation `rho_U^0` denotes this limit.  Every
diagonal sequence for which

\[
 \rho_U(G_n,r)-\rho_U^0(G_n,r)=o(n^{-1}),
 \qquad U\in\{\mathrm{Bd},\mathrm{dB}\},
 \tag{2}
\]

inherits all conclusions.  Condition (2) is the precise meaning of the
weak-cut regime here.  It can always be enforced by choosing the positive
cross weight sufficiently small after the four finite module parameters
are fixed.  The standard finite-state separation proof is the one in the
companion sharp-cut note: internal absorption precedes a second cross event,
failed introductions return to the same homogeneous macrostate, and the
first successful introduction determines the next macrostate.

All graph weights remain fitness-independent.  If a single diagonal is
needed simultaneously for a countable set of fixed fitnesses, ordinary
diagonalization over rational fitness intervals gives (2) on every compact
subinterval of `(1,infinity)`.

## 2. Local fixation quantities

Fix `r>1` and put

\[
 a_r=1-\frac1r.
 \tag{3}
\]

Direct solution of the complete-graph count chains gives

\[
 b_j(r):=\rho_{\rm Bd}(K_j,r)
 =\frac{a_r}{1-r^{-j}},
 \tag{4}
\]

\[
 d_j(r):=\rho_{\rm dB}(K_j,r)
 =\frac{a_r(1-1/j)}{1-r^{1-j}}.
 \tag{5}
\]

It is useful to remove the uniform-initialization factors:

\[
 \mathcal B_j=\frac{j}{1-r^{-j}},
 \qquad
 \mathcal D_j=\frac{j-1}{1-r^{1-j}}.
 \tag{6}
\]

Thus `j*b_j=a_r*B_j` and `j*d_j=a_r*D_j`.

## 3. Exact successful macro-change odds

Suppose module `A` is mutant and `B` resident.  Under Bd, the raw
favorable-to-adverse cross-introduction ratio tends to `r*beta/alpha`.
Multiplying by the exact fixation probabilities of the introduced mutant
in `B` and the introduced resident, at reciprocal fitness, in `A` gives

\[
 \boxed{
 Z_{{\rm B},A}
 =\sigma r^m\frac{r^\ell-1}{r^m-1}.}
 \tag{7}
\]

When `B` is mutant,

\[
 \boxed{
 Z_{{\rm B},B}
 =\sigma^{-1}r^\ell\frac{r^m-1}{r^\ell-1}.}
 \tag{8}
\]

For dB, the raw ratio when `A` is mutant tends to `r^2*alpha/beta`.
Using

\[
 \frac{d_m(r)}{d_\ell(1/r)}
 =\frac{\ell(m-1)}{m(\ell-1)}
 r^{m-2}\frac{r^{\ell-1}-1}{r^{m-1}-1}
\]

gives

\[
 \boxed{
 Z_{{\rm D},A}
 =\sigma^{-1}\frac{\ell(m-1)}{m(\ell-1)}
 r^m\frac{r^{\ell-1}-1}{r^{m-1}-1},}
 \tag{9}
\]

and

\[
 \boxed{
 Z_{{\rm D},B}
 =\sigma\frac{m(\ell-1)}{\ell(m-1)}
 r^\ell\frac{r^{m-1}-1}{r^{\ell-1}-1}.}
 \tag{10}
\]

Both pairs have the exact scale-free product

\[
 Z_{{\rm B},A}Z_{{\rm B},B}
 =Z_{{\rm D},A}Z_{{\rm D},B}=r^n.
 \tag{11}
\]

The probability of global fixation from the corresponding homogeneous
one-mutant-module macrostate is `Z/(1+Z)`: failed introductions return to the
same state, while the first successful adverse introduction gives global
extinction and the first successful favorable introduction gives global
fixation.

Consequently

\[
 \rho_{\rm Bd}^0
 =\frac\ell n b_\ell(r)\frac{Z_{{\rm B},A}}{1+Z_{{\rm B},A}}
 +\frac mn b_m(r)\frac{Z_{{\rm B},B}}{1+Z_{{\rm B},B}},
 \tag{12}
\]

\[
 \rho_{\rm dB}^0
 =\frac\ell n d_\ell(r)\frac{Z_{{\rm D},A}}{1+Z_{{\rm D},A}}
 +\frac mn d_m(r)\frac{Z_{{\rm D},B}}{1+Z_{{\rm D},B}}.
 \tag{13}
\]

These formulas are exact in the separated weak-cut limit for every finite
choice of the four module parameters.

## 4. Exact complete-comparison corrections

Define local budgets

\[
 E_{\rm B}=\mathcal B_\ell+\mathcal B_m-\mathcal B_n,
 \qquad
 E_{\rm D}=\mathcal D_\ell+\mathcal D_m-\mathcal D_n,
 \tag{14}
\]

and macro-failure charges

\[
 L_{\rm B}
 =\frac{\mathcal B_\ell}{1+Z_{{\rm B},A}}
 +\frac{\mathcal B_m}{1+Z_{{\rm B},B}},
 \tag{15}
\]

\[
 L_{\rm D}
 =\frac{\mathcal D_\ell}{1+Z_{{\rm D},A}}
 +\frac{\mathcal D_m}{1+Z_{{\rm D},B}}.
 \tag{16}
\]

Substitution in (12)--(13) gives the exact identities

\[
 \boxed{
 \frac{n}{a_r}
 \{\rho_{\rm Bd}^0(G,r)-\rho_{\rm Bd}(K_n,r)\}
 =E_{\rm B}-L_{\rm B},}
 \tag{17}
\]

\[
 \boxed{
 \frac{n}{a_r}
 \{\rho_{\rm dB}^0(G,r)-\rho_{\rm dB}(K_n,r)\}
 =E_{\rm D}-L_{\rm D}.}
 \tag{18}
\]

The charges are nonnegative.  These are the requested exact `1/n`-scale
comparison corrections.

## 5. Two genuinely mesoscopic modules

### Theorem 2

Suppose `ell_n->infinity` and `m_n->infinity`, with no restriction on their
proportions or on `sigma_n`.  Then, for every fixed `r>1`,

\[
 \boxed{
 \rho_{\rm dB}(G_n,r)-\rho_{\rm dB}(K_n,r)
 \le-\frac{a_r}{n}+o(n^{-1}).}
 \tag{19}
\]

In particular, such a family is eventually dB-suppressing.

#### Proof

Write

\[
 \mathcal D_j=(j-1)+e_j,qquad
 e_j=\frac{(j-1)r^{1-j}}{1-r^{1-j}}\longrightarrow0.
 \tag{20}
\]

Since `n=ell+m`,

\[
 E_{\rm D}=-1+e_\ell+e_m-e_n=-1+o(1).
 \tag{21}
\]

Equation (18), `L_D>=0`, and the separation error (2) prove (19).  Notice
that no cut-scale or proportion estimate is used.  QED.

This gives a stronger conclusion than a cross-rule tradeoff: actual strict
dB amplification is already impossible when both weak modules are
mesoscopic.

## 6. One bounded module: sharp cross-rule implication

It remains to let `ell=k` be fixed and `m=n-k->infinity`.  Define

\[
 C_{k,r}=\frac{k}{k-1}r(r^{k-1}-1),
 \tag{22}
\]

and

\[
 \sigma_{k,r}
 =\frac{r(k-r^{k-1})}{k-1}.
 \tag{23}
\]

The local budget limits are

\[
 E_{\rm D}\longrightarrow
 e_{\rm D}(k,r)
 =\frac{k-r^{k-1}}{r^{k-1}-1},
 \tag{24}
\]

\[
 E_{\rm B}\longrightarrow
 e_{\rm B}(k,r)=\frac{k}{r^k-1}.
 \tag{25}
\]

The small-mutant-module odds obey, uniformly in the positive scale ratio,

\[
 Z_{{\rm D},A}=\frac{C_{k,r}}\sigma\{1+o(1)\},
 \qquad
 Z_{{\rm B},A}=\sigma(r^k-1)\{1+o(1)\}.
 \tag{26}
\]

The two limiting local-budget-minus-small-module-charge expressions simplify
exactly to

\[
 \boxed{
 e_{\rm D}(k,r)
 -\frac{\mathcal D_k}{1+C_{k,r}/\sigma}
 =\frac{k(\sigma_{k,r}-\sigma)}{\sigma+C_{k,r}},}
 \tag{27}
\]

\[
 \boxed{
 e_{\rm B}(k,r)
 -\frac{\mathcal B_k}{1+\sigma(r^k-1)}
 =\frac{k(\sigma-1)}{1+\sigma(r^k-1)}.}
 \tag{28}
\]

### Theorem 3

Suppose (2) holds and

\[
 \rho_{\rm dB}(G_n,r)>\rho_{\rm dB}(K_n,r)
 \tag{29}
\]

eventually along a sequence with `ell=k` fixed.  Then necessarily

\[
 r^{k-1}\le k,qquad
 \sigma_n\le\sigma_{k,r}+o(1).
 \tag{30}
\]

Moreover

\[
 \boxed{
 \rho_{\rm Bd}(G_n,r)-\rho_{\rm Bd}(K_n,r)
 \le-\frac{a_r c_{k,r}}n+o(n^{-1}),}
 \tag{31}
\]

where

\[
 c_{k,r}
 =\frac{k(1-\sigma_{k,r})}
        {1+\sigma_{k,r}(r^k-1)}>0.
 \tag{32}
\]

#### Proof

By (18), (29), and (2), the weak-limit normalized dB comparison is at least
`-o(1)`.  Discarding the nonnegative large-module charge and using (24),
(26), and (27) shows first that `e_D(k,r)>=0`, equivalently
`r^(k-1)<=k`, and then that `sigma<=sigma_(k,r)+o(1)`.  If equality holds in
`r^(k-1)<=k`, the same argument forces `sigma->0`, which is also (30).

Strict convexity of `x^k` at `x=1` gives

\[
 1-\sigma_{k,r}
 =\frac{r^k-kr+k-1}{k-1}>0
 \qquad(r>1).
 \tag{33}
\]

Now discard the nonnegative large-module Bd charge in (17).  Formula (28)
is strictly increasing in `sigma`; (30) therefore bounds the normalized Bd
comparison above by `-c_(k,r)+o(1)`.  This is (31).  QED.

The proof uses the actual strict dB-amplification inequality, not merely its
local consequences.

## 7. Fixed `r>3/2`: complete classification inside the model

Let `ell_n<=m_n` and `n->infinity`.  If `ell_n->infinity`, Theorem 2 rules
out dB amplification.  Otherwise pass to one of the finitely many fixed
values `ell_n=k`.  Theorem 3 applies.

For `r>3/2`, the only possible bounded sizes are

\[
 \begin{array}{c|c}
 \text{fitness range}&\{k\ge2:r^{k-1}\le k\}\\ \hline
 3/2<r\le4^{1/3}&\{2,3,4\}\\
 4^{1/3}<r\le\sqrt3&\{2,3\}\\
 \sqrt3<r\le2&\{2\}\\
 r>2&\varnothing.
 \end{array}
 \tag{34}
\]

At an endpoint the largest listed module has zero dB local budget, forcing
`sigma->0`; the Bd conclusion remains strict.  Since (34) is finite, the
minimum of the positive constants `c_(k,r)` over the applicable sizes is
positive.

We have therefore proved:

### Corollary 4

For every fixed `r>3/2`, in the separated two-complete-module weak-cut
model,

\[
 \boxed{
 \rho_{\rm dB}(G_n,r)>\rho_{\rm dB}(K_n,r)
 \quad\Longrightarrow\quad
 \rho_{\rm Bd}(G_n,r)<\rho_{\rm Bd}(K_n,r)}
 \tag{35}
\]

for all sufficiently large `n`.  More precisely, the Bd deficit is at least
`c(r)/n+o(1/n)` for an explicit `c(r)>0` on every nonvacuous bounded-module
subsequence.  If both module sizes diverge, the antecedent is impossible.

This excludes simultaneous amplification throughout a broad singular model
that includes vanishing class proportions, arbitrary mesoscopic
proportions, and arbitrarily varying internal degree scales.

The same proof works for every fixed `r>1`.  Indeed,
`{k>=2:r^(k-1)<=k}` is finite for each such `r`, and (33) makes every
corresponding `c_(k,r)` positive.  The `r>3/2` specialization is highlighted
because it is the range requested by the obstruction program.

## 8. Boundary of the theorem

The proof uses that each module is an internally complete, hence exactly
solvable, population.  It does not yet cover noncomplete amplifier modules
or a recursively nested hierarchy in which a module's own `1/n` correction
can be positive.  The exact identities (17)--(18) show what a recursive
extension must control: the module-level local budgets before the
nonnegative macro-failure charges are subtracted.
