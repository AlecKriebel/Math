# Separated unequal-clique stars: an exact leading-order no-go

Date: 2026-08-01 (America/Los_Angeles)

Status: **PROVED for the stated separated-scale limit.**  This is not a
universal obstruction for arbitrary graph families.  In particular, it does
not by itself control a boundary diagonal in which the scale-separation error
is comparable to a vanishing comparison gap.

No literature search or external contact was used.

## 1. Family and order of limits

Take one center clique of size \(c\ge2\) and \(M\) leaf cliques, each of size
\(l\ge2\).  Every center--leaf pair of vertices is joined by a common weak
edge.  There are no edges between distinct leaf cliques.  Normalize the
internal weighted degree of a leaf vertex to one and let the internal weighted
degree of a center vertex be \(z>0\).  The weak cross-edge scale tends to zero
fast enough that a clique hit by one invader becomes monomorphic before the
next cross-clique event, with probability tending to one.

For fixed \(c,l,M,z,r\), this trace-process statement follows directly from
the finite absorbing chain: internal absorption has finite mean time, while
the total cross-event rate is linear in the cross-edge scale.  The resulting
module chain is then taken to \(M\to\infty\).  Since
\(c/(c+Ml)\to0\), a uniformly placed initial mutant starts in a leaf clique
with probability tending to one.

## 2. Clique establishment probabilities

Write \(a_s^U(r)\) for fixation from a uniformly placed mutant in an isolated
\(s\)-clique and \(b_s^U(r)=a_s^U(1/r)\) for reverse invasion by one resident
into an all-mutant clique.  Direct solution of the mutant-count chains gives

\[
 a_s^{\rm Bd}=\frac{(r-1)r^{s-1}}{r^s-1},\qquad
 b_s^{\rm Bd}=\frac{r-1}{r^s-1},
 \tag{1}
\]

and

\[
 a_s^{\rm dB}=\frac{s-1}{s}\frac{(r-1)r^{s-2}}{r^{s-1}-1},\qquad
 b_s^{\rm dB}=\frac{s-1}{s}\frac{r-1}{r^{s-1}-1}.
 \tag{2}
\]

Thus \(a_s^{\rm Bd}=r^{s-1}b_s^{\rm Bd}\) and
\(a_s^{\rm dB}=r^{s-2}b_s^{\rm dB}\).

## 3. Effective star chain

Let \(h\in\{0,1\}\) be the center-clique type and let \(k\) be the number of
mutant leaf cliques.  In the trace chain put

\[
 A=\Pr\{(0,k)\to(1,k)\text{ before }(0,k-1)\},
\]

and

\[
 B=\Pr\{(1,k)\to(1,k+1)\text{ before }(0,k)\}.
\]

These probabilities do not depend on \(k\) away from the boundaries.  If
\(f_{h,k}\) is macro-fixation probability, then

\[
 f_{0,k}=Af_{1,k}+(1-A)f_{0,k-1},\qquad
 f_{1,k}=Bf_{1,k+1}+(1-B)f_{0,k}.
 \tag{3}
\]

Putting \(x_k=f_{1,k}-f_{0,k-1}\) gives

\[
 x_{k+1}=\gamma x_k,\qquad \gamma=\frac{1-A}{B}.
 \tag{4}
\]

Consequently a leaf-start macro fixation probability tends to
\(1-\gamma\) as \(M\to\infty\) when \(\gamma<1\), and to zero when
\(\gamma\ge1\).

### Bd rates

Cross reproduction is inversely proportional to the **source** internal
degree.  Omitting common positive factors, the two competing rates at
\(h=0\) are

\[
 r a_c^{\rm Bd},\qquad b_l^{\rm Bd}/z,
\]

and at \(h=1\) they are

\[
 r a_l^{\rm Bd}/z,\qquad b_c^{\rm Bd}.
\]

Substitution in (4) gives

\[
 \gamma_{\rm Bd}=\frac{1+x_{\rm Bd}}
 {1+r^{c+l}x_{\rm Bd}},\qquad
 x_{\rm Bd}=\frac{z(r^l-1)}{r^l(r^c-1)}.
 \tag{5}
\]

Since

\[
 a_l^{\rm Bd}=\frac{1-r^{-1}}{1-r^{-l}},
\]

comparison with the large-complete-graph limit \(1-r^{-1}\) is equivalent
to \(\gamma_{\rm Bd}<r^{-l}\).  Equation (5) makes this exactly

\[
 \boxed{z>1.}
 \tag{6}
\]

### dB rates and the essential defense factor

For dB, cross replacement is inversely proportional to the **target**
internal degree.  Moreover, reverse invasion into an all-mutant target has an
extra factor \(1/r\), because all internal competitors have fitness \(r\).
This factor is essential.  The competing rates at \(h=0\) are

\[
 r a_c^{\rm dB}/z,\qquad b_l^{\rm dB}/r,
\]

and at \(h=1\) they are

\[
 r a_l^{\rm dB},\qquad b_c^{\rm dB}/(rz).
\]

Thus

\[
 \gamma_{\rm dB}=\frac{1+x_{\rm dB}}
 {1+r^{c+l}x_{\rm dB}},\qquad
 x_{\rm dB}=\frac{b_c^{\rm dB}}
 {z r^l b_l^{\rm dB}}.
 \tag{7}
\]

The dB comparison is

\[
 a_l^{\rm dB}(1-\gamma_{\rm dB})>1-r^{-1}.
 \tag{8}
\]

Solving (8) for \(z\) gives the necessary and sufficient leading-order
condition

\[
 z<Z_{c,l}(r),
 \tag{9}
\]

where

\[
 \boxed{
 Z_{c,l}(r)=
 \frac{(c-1)\{r^{c+1}(l-r^{l-1})-(l-1)\}}
 {c(l-1)r(r^{c-1}-1)}.}
 \tag{10}
\]

If the numerator in (10) is nonpositive, dB amplification is already
impossible for every \(z>0\).

## 4. Exact incompatibility certificate

For every \(c,l\ge2\) and \(r>1\), one has

\[
 \boxed{Z_{c,l}(r)<1.}
 \tag{11}
\]

Indeed, denominator minus numerator in the proposed inequality is exactly

\[
\begin{aligned}
 D_{c,l}(r)
 &=c(l-1)r(r^{c-1}-1)
  -(c-1)\{r^{c+1}(l-r^{l-1})-(l-1)\}\\
 &=(l-1)(r^c-cr+c-1)
   +(c-1)r^c(r^l-lr+l-1).
 \tag{12}
\end{aligned}
\]

Both parentheses on the last line are strictly positive for \(r>1\), by
strict convexity of \(r\mapsto r^m\) (or the tangent inequality
\(r^m>1+m(r-1)\)).  Hence \(D_{c,l}(r)>0\).

Conditions (6), (9), and (11) are incompatible.  Therefore no separated
unequal-clique star in this regime is a leading-order simultaneous amplifier.

For \(l=2\), the corrected threshold is

\[
 Z_{c,2}(r)=
 \frac{(c-1)\{r^{c+1}(2-r)-1\}}
 {cr(r^{c-1}-1)},
 \tag{13}
\]

which tends to \(r(2-r)=1-(r-1)^2<1\) as \(c\to\infty\).  Omitting the
reverse-invasion defense factor would incorrectly replace this by a quantity
that can exceed one.

## 5. Scope

This certificate excludes a natural and broad construction mechanism: unequal
center and leaf clique sizes, arbitrary positive internal-degree ratio, and
arbitrarily strong scale separation.  It does not exclude nonclique gadgets,
multiple nested scales whose errors are comparable to the limiting gap, or
families without a star-of-modules trace process.

