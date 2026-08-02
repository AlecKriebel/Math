# Mesoscopic repeated modules beyond the `3/2` threshold

Date: 2026-08-02 (America/Los_Angeles)

No literature search or external contact was used.  Exact reductions, proved
class exclusions, and numerical reconnaissance are labeled separately.

## 1. Outcome

No construction beyond `R_sim >= 3/2` was found in this bounded search.
Orders six, seven, and eight were searched at `r=1.51`, with attachment laws
eliminated globally rather than optimized heuristically.  The nearest
separated-module candidate was still locally dB-suppressing.  A load-aware
early-migration search at order six was also negative.

Two rigorous results make this a useful closed checkpoint.

1. **PROVED:** In both the separated-center trace and a weak complete
   coupling of repeated modules, some globally optimal attachment law is
   supported on at most two module vertices.  Thus the attachment part of an
   order-eight search reduces exactly to 36 vertex pairs and a one-dimensional
   calculation.
2. **PROVED CLASS NO-GO:** Any construction obtained by replacing the
   vertices of a connected weighted-regular macrograph by identical
   weighted-regular modules, and every macro edge by a uniform complete
   bipartite block, ties the complete-graph Bd fixation probability exactly.
   The module and macro orders may both diverge and all internal and outer
   scales may depend on population size.  Hence this broad regular
   repeated/mesoscopic class can never be a strict simultaneous amplifier.

Neither result is a universal obstruction.  Nonregular module attachment and
more than one module type remain open.

## 2. Exact repeated-module trace

Let `H` be a connected weighted graph on `m` vertices, with internal weighted
degrees `d_i`.  Take `M` labelled copies.  Between vertices `i` and `j` in
two distinct copies put the weak edge

\[
 \varepsilon h_i h_j,\qquad h_i>0.
\tag{1}
\]

Let `f_i^U(r)` be fixation in the isolated module from a mutant at `i`, and
let

\[
 b_i^U(r)=f_i^U(1/r)
\tag{2}
\]

be fixation of a single resident introduced at `i` in an otherwise mutant
module.  Put

\[
 \alpha_U={1\over m}\sum_i f_i^U(r).
\tag{3}
\]

In the successive rare-edge trace, a mutant module and a resident module
compete through successful introductions.  Directly summing the Bd rates in
the two directions gives the ratio

\[
 q_B(h)=r\,{\sum_i h_i f_i^B\over\sum_i h_i b_i^B}.
\tag{4}
\]

Indeed, the common source factor `sum_i h_i/d_i` cancels.  For dB, direct
summation over the dying target gives

\[
 q_D(h)=r^2\,
 {\sum_i(h_i/d_i)f_i^D\over\sum_i(h_i/d_i)b_i^D}.
\tag{5}
\]

The fixed-module states therefore form a complete macrograph with forward to
backward ratio `q_U`.  Its fixation probability from one mutant module tends
to `1-1/q_U` when `q_U>1` and `M -> infinity`.  Uniform initialization first
has to fix its initial module.  Consequently the full post-establishment
limits are

\[
 R_B(h)=\alpha_B\left(1-{1\over q_B(h)}\right)_+,
 \qquad
 R_D(h)=\alpha_D\left(1-{1\over q_D(h)}\right)_+.
\tag{6}
\]

This is not a branching-only score: the macro fixation factor is included.
A finite construction would still require the standard quantitative
rare-edge coupling, as in the proved center-triangle family.

## 3. [PROVED] Two-vertex reduction for repeated modules

Fix a proposed common value `T<min(alpha_B,alpha_D)`.  From (4)--(6), the
condition `R_B(h)>=T` is the linear inequality

\[
 \sum_i h_i\left{
 r f_i^B- {\alpha_B\over\alpha_B-T}b_i^B
 \right}\ge0.
\tag{7}
\]

The dB condition is

\[
 \sum_i h_i\left{
 {r^2 f_i^D-\alpha_D b_i^D/(\alpha_D-T)\over d_i}
 \right}\ge0.
\tag{8}
\]

Normalize `sum_i h_i=1` and map vertex `i` to the two coefficients in
(7)--(8).  Feasibility says exactly that their convex hull meets the closed
positive quadrant.  If it does, maximize the first coordinate subject to the
second being nonnegative.  This is a linear program on a simplex with one
additional half-space.  It has a basic feasible optimum supported on at most
two vertices, and its first coordinate remains nonnegative.  Therefore:

> For every feasible `T`, there is a feasible attachment supported on at most
> two vertices.  In particular, a maximizer of `min(R_B,R_D)` has support at
> most two.

Strictly positive attachment weights are recovered whenever the inequalities
have positive margin by giving the other vertices sufficiently small positive
weights.  Thus zeros used in discovery do not create a false strict
candidate.

## 4. [PROVED] Two-vertex reduction for the center window

For the separated module / growing-center trace, put

\[
 p=1-{1\over r},\quad
 x=\sum_i{h_i\over d_i},\quad
 y_B=\sum_i h_i b_i^B,\quad
 y_D=\sum_i{h_i b_i^D\over d_i},\quad H=\sum_i h_i.
\tag{9}
\]

When both isolated averages exceed `p`, the exact leading center-degree
window `(z_B,z_D)` has ratio

\[
 {z_D\over z_B}
 ={r(r-1)^2(\alpha_B-p)(\alpha_D-p)\over p^2}
 {xH\over y_By_D}.
\tag{10}
\]

Normalize `H=1`.  The attachment-dependent factor has the form

\[
 F(h)={a\mathbin\cdot h\over
 (b\mathbin\cdot h)(c\mathbin\cdot h)},
\quad a_i={1\over d_i},\quad b_i=b_i^B,
\quad c_i={b_i^D\over d_i}.
\tag{11}
\]

Let `h_*` maximize (11) and fix `B_*=b dot h_*`.  On the polytope

\[
 \{h\ge0:\ \mathbf1\mathbin\cdot h=1,\ b\mathbin\cdot h=B_*\},
\tag{12}
\]

maximize `(a dot h)/(c dot h)`.  A linear-fractional function at a convex
combination is a positive weighted average of its values at the combined
points, so it has a maximizing vertex of (12).  Every vertex of (12) has at
most two positive coordinates.  Since `b dot h` is fixed, that vertex also
maximizes (11).  This proves the reduction.

On a pair `(i,j)`, write `h=t e_i+(1-t)e_j`.  The stationary equation is

\[
 A'BC-A(B'C+BC')=0,
\tag{13}
\]

where `A,B,C` are affine in `t`; (13) has degree at most two.  Endpoints and
its roots in `(0,1)` give the exact global attachment optimum.

## 5. [PROVED] Regular repeated-module no-go

Let `H_m` be any connected undirected weighted graph in which every vertex
has the same internal weighted degree `d`.  Let `B_M` be any connected
undirected weighted macrograph in which every macro vertex has weighted
degree `Delta`.  Replace every macro vertex by a copy of `H_m`; for a macro
edge of weight `a_xy`, join every vertex in copy `x` to every vertex in copy
`y` with edge weight `epsilon a_xy`.  Every resulting vertex has degree

\[
 d+\varepsilon m\Delta.
\tag{14}
\]

Thus the full graph is weighted-regular for every positive `epsilon`.  If a
state has `k` mutants and boundary weight `W(S,S^c)`, its two Bd changing
probabilities have ratio

\[
 {T^+(S)\over T^-(S)}
 ={rW(S,S^c)\over W(S^c,S)}=r,
\tag{15}
\]

using symmetry of the weights and equality of all degrees.  The usual
one-dimensional harmonic equation, derived from (15), gives

\[
 \rho_{Bd}(G,r)={1-r^{-1}\over1-r^{-|V(G)|}},
\tag{16}
\]

exactly the complete-graph Bd baseline.  Therefore no member of this class is
a strict Bd amplifier, at any size or fitness.  In particular the conclusion
continues to hold when `m=m_N`, `M=M_N`, `d`, `Delta`, and `epsilon` all vary
with `N`, with both module and macro scales diverging.

This excludes regular clique replacements, regular mesoscopic modules,
regular macro expanders, and arbitrary multiscale choices of their two edge
weights.  Any positive repeated-module construction must introduce a
nonvanishingly relevant nonregular attachment profile (although the amount of
nonregularity may itself tend to zero).

## 6. [NUMERICALLY OBSERVED] Searches at `r=1.51`

`search_modules_6_8.py` builds all four isolated subset chains directly and
uses Sections 3--4 to eliminate attachments.  With
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`, the recorded random plus local
screens gave:

| module order | best separated score | `alpha_Bd` | `alpha_dB` |
|---:|---:|---:|---:|
| 6 | `-0.01616` | `0.36886` | `0.32159` |
| 7 | `-0.02703` | `0.35793` | `0.31072` |
| 8 | `-0.03122` | `0.35164` | `0.30653` |

The infinite complete baseline is `p=0.337748344371...`; hence these were
rejected already by local dB establishment.  The best recorded order-six
weak repeated-module common limit was about `0.2956`, also below `p`.

Targeted singular searches were likewise negative:

- a `3+3` internally resolved two-block module had best
  `alpha_dB about 0.31500`;
- a `2+4` split had best separated score about `-0.02454`;
- the favorable four-vertex two-dimer primitive plus two optimized helper
  vertices had best separated score `-0.0203031`, with
  `alpha_dB about 0.31745`;
- a load-aware order-six early-migration search using the exact colony chain
  and center-load derivative reached balanced coefficients only near
  `(-0.04314,-0.04309)`.

These values are discovery evidence only.  They do not bound all weighted
modules of the displayed orders and are not used in any proof.

## 7. Status

- **PROVED:** both global two-vertex attachment reductions.
- **PROVED:** exact Bd tie for the regular repeated/mesoscopic replacement
  class.
- **EXACTLY CHECKED:** the regular-class degree and state-ratio identities in
  the independent verifier.
- **NUMERICALLY OBSERVED:** no order-six through order-eight candidate in the
  recorded searches at `r=1.51`.
- **OPEN:** a nonregular repeated-module construction beyond `3/2`, a
  multiple-module-type mixture beyond `3/2`, and the universal value of
  `R_sim`.

