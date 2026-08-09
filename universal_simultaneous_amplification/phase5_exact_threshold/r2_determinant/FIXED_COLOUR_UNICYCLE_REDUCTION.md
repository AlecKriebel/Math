# Fixed-colour row mixtures and the unicycle cancellation

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note gives two exact forms of the still-open fixed-colour numerator
problem on the complete-to-actual active ray.

1. A fixed Bernstein level is a uniform sum of row-mixed Markov-tree
   determinants, and each such determinant has an exact root-response form.
2. The same coefficient is a sum of coloured functional-unicycle
   circulations.

Both identities are **PROVED**.  Three tempting local strengthenings are
**EXACTLY REFUTED**, already on the reversible weighted triangle with edge
weights `(1,10,3)`: a single row-location determinant can be negative, and
a single spanning unicycle packet can be negative at the first nonzero
colour level.  Even summing every attachment forest before judging a fixed
directed cycle can be negative.  Thus a proof must average simultaneously
over colour locations and directed cycles.  The global fixed-colour sign
remains **OPEN**.

## 1. Setup and root controls

Let `Y` be the active state space, put `m=|Y|` and `d=m-1`, and retain

\[
 K_\alpha=(1-\alpha)K_0+\alpha K,
 \qquad q=H-c_0\mathbf1.
\tag{1}
\]

Let `t(alpha)` be the row vector of in-tree cofactors of `I-K_alpha`.
Write its natural degree-`d` Bernstein expansion as

\[
 t(\alpha)=\sum_{j=0}^d {d\choose j}t_j
 \alpha^j(1-\alpha)^{d-j},
 \qquad n_j=t_jq.
\tag{2}
\]

Thus `n_j` is the fixed-colour numerator control.  The desired all-order
certificate is

\[
 n_j\geq0\qquad(0\leq j\leq d).
\tag{FC}
\]

Coefficient extraction from
`t(alpha)(I-K_alpha)=0` gives the exact vector recurrence

\[
 \boxed{
 (d+1-j)t_j(I-K_0)+j,t_{j-1}(I-K)=0,
 }
\tag{3}
\]

for `0<=j<=d+1`, with `t_{-1}=t_{d+1}=0`.  This includes stationarity of
the two endpoint tree vectors.

Let

\[
 h=(I-K_0+\mathbf1\nu_0)^{-1}q,
 \qquad \Delta=K-K_0.
\tag{4}
\]

Since `(I-K_0)h=q`, equation (3) also gives

\[
 \boxed{
 t_{j-1}\Delta h
 =n_{j-1}+{d+1-j\over j}n_j,
 \qquad1\leq j\leq d+1.
 }
\tag{5}
\]

This is the exact tridiagonal colour-current form of `(FC)`.

## 2. Row-mixed determinant identity

For a set `C subseteq Y`, define `K_C` by using the row of `K` at sources
in `C` and the row of `K_0` elsewhere, and put

\[
 A_C=I-K_C+q\nu_0.
\tag{6}
\]

Let `tau_x(K_C)` denote the in-tree cofactor rooted at `x`.  Then

\[
 \boxed{
 \det A_C
 =\sum_{x\in C}\tau_x(K_{C\setminus\{x\}})\,\Delta h(x).
 }
\tag{7}
\]

Indeed, if `nu_C` is the stationary row of `K_C` and `Z_C` its total tree
weight, the determinant lemma and tree theorem give

\[
 \det A_C=Z_C\nu_Cq.
\]

But stationarity and `(4)` imply

\[
 \nu_Cq=\nu_C(I-K_0)h
 =\nu_C(K_C-K_0)h
 =\sum_{x\in C}\nu_C(x)\Delta h(x).
\]

Finally, the cofactor rooted at `x` does not use row `x`, so
`tau_x(K_C)=tau_x(K_(C minus {x}))`, proving (7).

There is a useful fixed-level consequence.  Define

\[
 u_j={1\over {m\choose j}}
       \sum_{|C|=j}\det A_C.
\tag{8}
\]

Row multilinearity says that the `u_j` are the degree-`m` Bernstein
controls of the same numerator.  Degree elevation from (2) gives

\[
 \boxed{
 u_j={m-j\over m}n_j+{j\over m}n_{j-1}.
 }
\tag{9}
\]

Summing (7) gives the equivalent leave-one-root form

\[
 {m\choose j}u_j
 =\sum_{x\in Y}\Delta h(x)
   \sum_{\substack{D\subseteq Y\setminus\{x\}\\|D|=j-1}}
       \tau_x(K_D).
\tag{10}
\]

Equation (10), rather than a sign for one chosen `C`, is the smallest
row-location average available from this route.

### Exact failure of a single-location sign

Take the reversible triangle

\[
 w_{01}=1,\qquad w_{02}=10,\qquad w_{12}=3.
\tag{11}
\]

Use bit masks for `B`.  For the singleton row set

\[
 C=\{(B,v)=(2,0)\},
\]

the exact determinant is

\[
 \boxed{\det A_C=-{891\over524288}<0.}
\tag{12}
\]

At this state `Delta h=-9/44`.  In fact five of the nine singleton
locations have a negative root-response contribution before their fixed
level sum cancels.  Hence neither (7) nor a root-by-root version of (10)
has the required sign.

## 3. Spanning-unicycle circulation

Orient every active in-tree toward its root.  In a tree contributing to
`n_j`, attach one additional complete edge from the root.  Ignoring a
self-loop, this creates a directed spanning functional graph with one
cycle.  Conversely, deleting a distinguished complete-coloured cycle edge
recovers the rooted tree.

For a coloured spanning unicycle `U`, let `Cyc(U)` be its directed cycle
and define

\[
 \Psi(U)=\sum_{\substack{e\in Cyc(U)\\e\ {\mathrm{complete}}}}
          \{h(\operatorname{tail}e)-h(\operatorname{head}e)\}.
\tag{13}
\]

The cycle telescopes, so equivalently

\[
 \Psi(U)=-\sum_{\substack{e\in Cyc(U)\\e\ {\mathrm{actual}}}}
          \{h(\operatorname{tail}e)-h(\operatorname{head}e)\}.
\tag{14}
\]

If `A_j=binom(d,j)n_j` is the unnormalised fixed-colour root sum, the
root-edge construction proves

\[
 \boxed{
 A_j=\sum_{\substack{U\ {\mathrm{spanning\ unicycle}}\\
                      U\ {\mathrm{has}}\ j\ {\mathrm{actual\ edges}}}}
       w(U)\Psi(U).
 }
\tag{15}
\]

For a fixed uncoloured unicycle, put

\[
 \ell_e={K(e)\over K_0(e)},\qquad
 \delta_e=h(\operatorname{tail}e)-h(\operatorname{head}e).
\]

After factoring the positive complete weight of `U`, its whole level-`j`
colour packet is

\[
\begin{aligned}
 \Phi_j(U)
 &=\sum_{\substack{A\subseteq E(U)\\|A|=j}}
   \left(\prod_{e\in A}\ell_e\right)
   \sum_{e\in Cyc(U)\setminus A}\delta_e\\
 &=-\sum_{e\in Cyc(U)}
   \delta_e\ell_e\,
   e_{j-1}\bigl((\ell_f)_{f\in E(U)\setminus\{e\}}\bigr).
\end{aligned}
\tag{16}
\]

Thus `(FC)` is an aggregate circulation inequality over all spanning
unicycles.  Formula (16) is exact, but its individual summands do not have
the desired sign.

### Exact failure of a single-unicycle sign at `j=2`

On the same triangle (11), take the seven-cycle through active states

```text
(2,0) -> (6,0) -> (4,1) -> (5,1) ->
(4,0) -> (2,2) -> (3,2) -> (2,0).
```

Attach the remaining states `(1,1)` and `(1,2)` to `(2,0)`.  This is a
spanning unicycle.  Along the cycle, the exact likelihood ratios and
potential increments are

\[
 (\ell_e)=\left({20\over11},{3\over2},{1\over2},{20\over11},
 {6\over13},{20\over13},{2\over11}\right),
\tag{17}
\]

\[
 (\delta_e)=(1,-1,1,-1,0,1,-1).
\tag{18}
\]

Both attachment edges have likelihood ratio `2/11` and zero potential
increment.  Direct substitution in (16) gives

\[
 \boxed{\Phi_2(U)=-{4804\over1859}<0.}
\tag{19}
\]

This is the first nonzero global colour order: `n_0=n_1=0`, while `n_2`
is strictly positive off the complete kernel.  Therefore even the
quadratic certificate requires cancellation between different unicycle
skeletons.  A path reversal or cycle rotation that treats one unicycle at
a time cannot prove `(FC)`.

### Exact all-minors grouping, and why one cycle is still too small

There is a canonical way to sum all attachment forests before testing a
cycle.  For a directed simple cycle `C`, put

\[
 F_C(\alpha)=
 \det (I-K_\alpha)_{Y\setminus C,Y\setminus C}
\tag{20}
\]

and orient the edges of `C` cyclically.  The all-minors forest theorem and
the distinguished-root-edge construction give

\[
 \boxed{
 N(\alpha)=\sum_C F_C(\alpha)
 \sum_{e\in C}K_0(e)\delta_e
       \prod_{f\in C\setminus\{e\}}K_\alpha(f).
 }
\tag{21}
\]

Thus each summand in (21) contains every forest attaching the off-cycle
states to `C`.  This is a strictly larger grouping than (16), but it still
does not have a pointwise sign.

On the triangle (11), take

```text
(2,0) -> (6,0) -> (3,2) -> (2,0).
```

The complete degree-eight Bernstein polynomial contributed by this cycle
and **all** of its attachment forests is

\[
 -{9\alpha(7\alpha+13)
 (2709\alpha^4-9824\alpha^3-60233\alpha^2
 -355368\alpha+646932)\over139375149056}.
\tag{22}
\]

Its degree-eight Bernstein controls are zero at level zero and strictly
negative at every level `1<=j<=8`; for example the level-one control is

\[
 -{783\over11534336}<0.                                  \tag{23}
\]

The verifier enumerates all 362 directed simple cycles of the nine-state
active chain and checks (21) independently at rational interpolation
points.  Hence (22) is an obstruction to the natural cycle-plus-forest
unit, not a bookkeeping artefact.  Cancellation across different cycles
is essential.

## 4. Consequence for the next proof step

The exact surviving target is the fixed-level sum (10), equivalently the
all-unicycle sum (15).  The three refutations show that the grouping must keep
both of the following at once:

1. all choices of the actual-coloured source locations at a fixed `j`;
2. all spanning-unicycle completions of the resulting coloured cycle.

The triangle sum-of-squares certificate demonstrates that this larger
grouping can be positive.  No universal involution or forest-square
decomposition of that size is presently known.
