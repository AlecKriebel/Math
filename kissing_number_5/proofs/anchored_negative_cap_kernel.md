# Anchoring the exact cap kernel on negative neighborhoods

## Scope

This note derives a universal pair/triple inequality from the exact
degree-10 cap kernel and evaluates it on two relaxation witnesses.  The
inequality has strict positive slack on both witnesses, so it does not
improve the global kissing-number bound and is not integrated into the
fixed-support separator.

The exact evaluations are stored in
`certificates/anchored_negative_cap_kernel_evaluations.json` and rebuilt by
`verifiers/verify_anchored_negative_cap_kernel.py`.

## Universal inequality

Let \(C=\{x_1,\ldots,x_N\}\subset S^4\) be a kissing code, with
\(g_{ij}=\langle x_i,x_j\rangle\).  Let \(F(u,v,t)\) be the rational
positive kernel certified in `one_sided_cap_degree10_bound.md`.

Fix an anchor \(x_i\), use the axis \(e=-x_i\), and select
\[
S_i^-=\{x_j:j\ne i,\ g_{ij}\leq0\}.
\]
Every selected point has height
\(\langle e,x_j\rangle=-g_{ij}\geq0\).  The positive-kernel identity,
which includes diagonal ordered pairs, gives
\[
\sum_{j,k\in S_i^-}F(-g_{ij},-g_{ik},g_{jk})\geq0.       \tag{1}
\]
This uses only the rational PSD Gram factors of the kernel.  The separate
upper bounds on \(F\) used to prove the cap cardinality bound are not needed
for (1).

Summing (1) over all anchors yields
\[
\boxed{
\sum_{\substack{i\ne j\\g_{ij}\leq0}}
F(-g_{ij},-g_{ij},1)
+
\sum_{\substack{i,j,k\ {\rm distinct}\\
                 g_{ij}\leq0,\ g_{ik}\leq0}}
F(-g_{ij},-g_{ik},g_{jk})
\geq0.}                                                \tag{2}
\]
The second sum is over ordered triples.  Thus (2) depends only on pair and
triple incidence data.

Height zero is included because the selection uses `<= 0`, the hemisphere
is closed, and the polynomial kernel extends to all determinant
boundaries.  Contact endpoints \(g_{jk}=1/2\) are also allowed.

More generally, one may replace \(S_i^-\) by
\[
S_i(a)=\{x_j:g_{ij}\leq-a\},\qquad 0\leq a\leq1,        \tag{3}
\]
or by any union of support color classes.  Every such subset still obeys
the same positive-kernel inequality.

## Exact finite-support form

Suppose the inner-product support is \(t_0,\ldots,t_{m-1}\), with ordered
pair counts \(D_q\) and unordered triangle counts \(n_{abc}\).  For a set
of selected colors \(A\), the diagonal contribution is
\[
\sum_{q\in A}D_qF(-t_q,-t_q,1).                        \tag{4}
\]
For a sorted triangle type \((a,b,c)\), let
\(\operatorname{Orb}(a,b,c)\) be its distinct permutations.  Its
off-diagonal contribution is
\[
\frac{6n_{abc}}{|\operatorname{Orb}(a,b,c)|}
\sum_{\substack{(q,r,s)\in\operatorname{Orb}(a,b,c)\\q,r\in A}}
F(-t_q,-t_r,t_s).                                      \tag{5}
\]
Repeated edge colors are therefore counted with their correct point-order
multiplicity.  Equations (4)--(5) are what the verifier evaluates.

For a normalized BV measure, the same expression is divided by \(N\):
the stored \(\alpha\) weights replace \(D_q/N\), and each stored
orbit-total \(\nu\) weight replaces \(6n_{abc}/N\).

## Results on the two witnesses

For the integral degree-four local witness, the full negative-neighborhood
sum is exactly
\[
\frac{
33440393620797272740801835188828891048973941239795699976293362234459
}{
5960908800000000000000000000000000000000000000000000000000000000
}>0.                                                    \tag{6}
\]
All four nested height-threshold cuts and all \(2^4-1=15\) nonempty
subsets of its four negative colors also have positive slack.  The least
is the singleton color \(-7/10\), with exact value
\[
\frac{
33037599819260055905345037469986242171068226742394809
}{
172480000000000000000000000000000000000000000000000
}>0.                                                    \tag{7}
\]

The historical all-harmonic witness contains enough triple-orbit data for
the same calculation.  In its \(1/N\)-normalized measure, the full
nonpositive-neighborhood sum is
\[
\frac{
26407138392301733848990492625733627382223972020675381837
}{
235947187357642181836800000000000000000000000000000000
}>0.                                                    \tag{8}
\]
All five nested height thresholds, including height zero, and all
\(2^5-1=31\) nonempty subsets of its nonpositive support colors are
positive.  The minimum is the singleton inner product \(-1\), equal to
\[
\frac{732355219678528111893675574143}
{31250000000000000000000000000}>0.                     \tag{9}
\]
Multiplying (8)--(9) by \(41\) gives the unnormalized anchor sums.

These are evaluations of abstract pair/triple measures.  Neither witness
is asserted to arise from one simultaneous edge-colored graph or from a
Gram matrix.

For code-point axes, the two signs \(e=\pm x_i\) are the complete natural
pair/triple-level family: \(e=x_i\) on positive neighborhoods was already
evaluated in `local_hybrid_degree4_rank_color_clique_barrier.md`, while
\(e=-x_i\) is (2).  On either finite support, varying a height threshold
produces exactly the nested prefixes checked above; allowing arbitrary
unions of eligible color classes gives the stronger exhaustive 15- and
31-cut audits.  Axes such as normalized \(x_i+x_j\) or \(x_i-x_j\) are
materially different, but summing their kernel inequalities depends on two
anchors and two further points, hence on genuine four-point rather than
pair/triple data.  The present witnesses do not contain enough information
to evaluate those axes.

## Independent sanity check

The verifier constructs all 40 normalized \(D_5\) roots through their exact
rational Gram matrix.  Each closed negative neighborhood has 27 points.  It
computes (1) directly from all anchors and also reconstructs the same number
from pair and unordered-triangle counts using (4)--(5).  Both routes give
\[
\frac{1087466194763554237052274055420597}
{260436079411200000000000000000}>0.                    \tag{10}
\]

Thus the aggregate combinatorics, diagonal convention, repeated-color
multiplicities, zero-height convention, and positivity direction have an
independent genuine-code check.  The route is valid but currently blocked:
the kernel and all natural support-induced threshold/subset variants have
large positive slack on the strongest available witnesses.
