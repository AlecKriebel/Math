# General 41-point quarter-grid H1/H2 moment lattice

This note removes the geometric-centering hypothesis from the earlier H1/H2
congruences.  It is needed for the `r12` endpoint, whose centroid is nonzero.

Let \(m_a\) be the unordered pair multiplicities for
\(a\in\{-4,-3,\ldots,2\}\), and put

\[
 M=\sum_a m_a=820,\qquad
 A=\sum_a a\,m_a,\qquad
 Q=\sum_a a^2m_a.
\]

For \(b_a=5a^2-16\), also put

\[
 S=\sum_a b_a^2m_a.
\]

The integer-scaled H1 and H2 centered *spectral* second moments are

\[
 X_1=5Q-11808,\qquad
 X_2=7S-1133568.
\]

Here spectral centering subtracts the mean nonzero eigenvalue.  It does not
assert that the point centroid is zero.

## Pair-moment selectors

Pointwise,

\[
 a^2\equiv a\pmod2,
\]

so

\[
 \boxed{X_1\equiv5A+2\pmod {10}}.
\]

The two exact H2 pointwise congruences are

\[
 b_a^2\equiv16+15a\pmod {30},
\]

and

\[
 b_a^2\equiv15a^2-150a+256\pmod {300}.
\]

Since \(M=820\), they give

\[
 S\equiv10+15A\pmod {30},
\]

\[
 \boxed{X_2\equiv105A+82\pmod {210}},
\]

and the stronger joint selector

\[
 \boxed{X_2\equiv21X_1-1050A+40\pmod {2100}}.
\]

When \(A\) is even these reduce to the earlier centered selectors
\(X_1\equiv2\pmod {10}\), \(X_2\equiv82\pmod {210}\), and
\(X_2\equiv21X_1+40\pmod {2100}\).  Geometric centering specifically gives
\(A=-82\), but parity is all that enters these reductions.

## Third H2 moment

Let \(R\) be the sum of the H2 numerator product
\(b_{a_{ij}}b_{a_{ik}}b_{a_{jk}}\) over ordered distinct triples.  As before,

\[
 R\equiv0\pmod {30}.
\]

For

\[
 Y_2=49R-36288S+4933287936
    =49R-5184X_2-943128576,
\]

one obtains, without a centering assumption,

\[
 \boxed{Y_2\equiv66\pmod {210}},\qquad
 \boxed{Y_2\equiv10X_2+2\pmod {49}}.
\]

## Exact `r12` endpoint

For

\[
 (m_{-4},\ldots,m_2)=(12,35,199,40,279,0,255),
\]

direct substitution gives

\[
 A=-81,\quad Q=2363,\quad X_1=7,
\]

\[
 S=162115,\quad X_2=1237\equiv187\pmod {210}.
\]

Also

\[
 164+2A=2,
\]

so if \(B=4G\), then
\(\mathbf1^{\mathsf T}B\mathbf1=2\), equivalently the squared norm of the
point centroid is \(1/2\).  The endpoint is therefore not geometrically
centered.

All selectors in this note require empirical integer pair/triple counts.
They do not apply to an arbitrary continuous pseudodistribution.

## H1 third-moment branches

Let

\[
 P=\sum_{i,j,k\ {\rm distinct}}a_{ij}a_{ik}a_{jk}.
\]

Every unordered triple occurs six times, so \(P=6T\) for an integer \(T\).
If \(D_1\) is the centered third spectral moment of the ordinary Gram
kernel, then

\[
 Y_1=800D_1
   =\frac{25}{2}P-2160Q+3636864
   =75T-432X_1-1464192.
\]

Consequently

\[
 \boxed{Y_1+432X_1+1464192\equiv0\pmod {75}}.
\]

The exact rank-five spectral inequality is

\[
 \boxed{9X_1^3-2Y_1^2\ge0}.
\]

For \(Q=2362,\ldots,2368\), these two conditions leave the following finite
branches:

\[
\begin{array}{c|c|l}
Q&X_1&Y_1\\ \hline
2362&2&-6\\
2363&7&9\\
2364&12&-51,\ 24\\
2365&17&-111,\ -36,\ 39,\ 114\\
2366&22&-171,\ -96,\ -21,\ 54,\ 129,\ 204\\
2367&27&-231,\ -156,\ -81,\ -6,\ 69,\ 144,\ 219,\ 294\\
2368&32&-366,\ -291,\ -216,\ -141,\ -66,\ 9,\ 84,\ 159,\ 234,\ 309,\ 384.
\end{array}
\]

This table constrains empirical K3 data; it does not eliminate an integer
pair-count profile by itself.
