# A first-event obstruction for every separated strong-pair hierarchy

Date: 2026-08-08 (America/Los_Angeles)

## Status

**PROVED for the class stated below.**  The result permits an arbitrary
finite or growing weighted macrograph, arbitrary pair strengths, arbitrary
positive pair--pair conductances, and an arbitrary distinguished starting
pair.  It is not a universal graph theorem: it uses separation to
monomorphic `K_2` states before the next cross event.

The obstruction was isolated while testing recursively nested paired stars.
It explains exactly why the orientation

\[
 A_L=L^3,\qquad W_L=L^6,\qquad C_L=1
\]

has the attractive dB peripheral limit
`(1/2)(1-r^{-4})` but has Bd peripheral fixation tending to zero.

## 1. Exact pair trace

Let macrovertex `i` be a two-vertex pair whose internal edge has strength
`b_i>0`.  Between pairs `i,j`, distribute a symmetric total conductance
`e_ij=e_ji>=0`.  Send every cross conductance to zero relative to the
internal pair strengths so that a discordant pair absorbs before the next
cross event.  Put

\[
 a_i={1\over b_i},\qquad R=r^2.
\]

The isolated `K_2` probabilities, derived from its two changing events, are

\[
 h_{\rm Bd}^+(K_2)={r\over r+1},\qquad
 h_{\rm Bd}^-(K_2)={1\over r+1},
\]

and

\[
 h_{\rm dB}^+(K_2)=h_{\rm dB}^-(K_2)={1\over2}.       \tag{1}
\]

Consequently, after deletion of common positive clock factors, the
successful conversion rates across a mutant--resident edge are

\[
\begin{array}{c|cc}
 &i\hbox{ mutant converts }j&i\hbox{ is converted by }j\\ \hline
 {\rm Bd}&R a_i e_{ij}&a_j e_{ij}\\
 {\rm dB}&R a_j e_{ij}&a_i e_{ij}.
\end{array}                                             \tag{2}
\]

Thus Bd uses source activity and dB uses target activity.  Formula (2) is
valid on every macrograph; no symmetry or lumping beyond pair absorption is
being assumed.

## 2. The topology-independent singleton bound

Start with pair `i` mutant and every other pair resident.  Define

\[
 E_i=\sum_j e_{ij},\qquad
 B_i=\sum_j a_j e_{ij},\qquad
 x_i={a_iE_i\over B_i}>0.                              \tag{3}
\]

Before the first macro type change, the favorable-to-adverse odds under Bd
and dB are respectively

\[
                       R x_i,\qquad {R\over x_i}.       \tag{4}
\]

An adverse first change is extinction.  Therefore, if `F_B(i),F_D(i)` are
the full macro fixation probabilities from pair `i`, including every later
recovery path, then exactly

\[
 \boxed{
 F_B(i)\le {Rx_i\over1+Rx_i},\qquad
 F_D(i)\le {R\over R+x_i}.}                            \tag{5}
\]

This is the key point: later topology can improve the conditional success
after the first gain, but cannot evade (5).

## 3. Sharp scalar envelope

For a uniformly chosen vertex in pair `i`, the initial pair resolves mutant
with probabilities `r/(r+1)` under Bd and `1/2` under dB.  The ideal
leaf-eliminated response, in which every later gate is allowed to succeed,
therefore contains

\[
 c(r)F_B(i)+{1\over2}F_D(i),
 \qquad c(r)={(r-1)r\over r+1}.                        \tag{6}
\]

Put

\[
 s(r)=\sqrt{{2r(r-1)\over r+1}}.
\]

In the interior regime containing the interval used below, differentiating
the right side of (5) gives the unique maximizer

\[
 x_*(r)={r^2s(r)-1\over r^2-s(r)}                      \tag{7}
\]

and the exact envelope

\[
 \boxed{
 M(r)={r^2\{r^2(1+s(r)^2)-2s(r)\}\over
                    2(r^4-1)}.}                       \tag{8}
\]

Let `R_pair` be the unique root in `(1,2)` of

\[
 r^{10}-6r^9+9r^8-12r^7+12r^6+12r^5
       -8r^4-8r^2+4=0.                                \tag{9}
\]

The root is

\[
 R_{\rm pair}=1.6986624639825652\ldots,                \tag{10}
\]

and it is the unique solution in `(1,2)` of

\[
                         M(r)=r-1.                     \tag{11}
\]

The Sturm certificate in the verifier proves uniqueness in `(1,2)` and
isolates the root in `(1698/1000,1699/1000)`.  The radical equation has
opposite exact signs at those endpoints and no later zero, so

\[
                         M(r)\le r-1
       \quad(R_{\rm pair}\le r\le2),                  \tag{12}
\]

with equality only at `R_pair`.

## 4. Class obstruction

Average (6) over any distribution of starting pairs.  Equations (5)--(8)
give

\[
 (r-1){r\over r+1}\,\mathbb E F_B
       +{1\over2}\mathbb E F_D\le M(r).               \tag{13}
\]

At every `r>=R_pair`, (12) makes the ideal leaf-eliminated separator
nonpositive.  Finite post-pair gates can only decrease the two fixation
terms.  Hence:

> **Theorem.**  No separated hierarchy of monomorphic strong `K_2`
> macrovertices can provide a positive simultaneous module-response
> generator at any fixed `r in [R_pair,2]`, regardless of macrograph rank,
> pair-strength heterogeneity, positive conductances, or later recovery
> paths.

At the proposed endpoint `r=2`, the strict numerical-looking gap is the
exact algebraic number

\[
 1-M(2)=1-{2\{4(1+4/3)-4/\sqrt3\}\over15}
        =0.0634756991233559\ldots>0.                   \tag{14}
\]

## 5. Consequence for the lower-bound search

Recursively replacing a peripheral pair by another separated star of
pairs does not escape the theorem.  Every initial mutant still first
resolves inside one `K_2`, after which its first macro change has reciprocal
Bd/dB odds (4).  In particular, the attractive dB bias `r^4` of one paired
star is paid for by the reverse-star Bd suppression.

A construction reaching two must therefore break at least one hypothesis
used above.  The cleanest remaining route is nonseparated entrance: allow a
portal to act while the initial pair is discordant, so that there is no
monomorphic-pair first event to which (5) applies.  A non-`K_2` reservoir or
an interacting positive-density portal network is another possibility.
