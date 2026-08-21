# Complete primary decomposition of the generic unmarked contact chart

**Exact candidate checkpoint:** 2026-07-25T14:31:00Z  
**Status:** primary exact decomposition complete; independent saturation
audit pending; not peer reviewed.

## 1. Generic chart

When \(a_2c_0b_1\ne0\), the residual source and target actions give
\[
a_2=c_0=b_1=1,\qquad b_2=0.
\]
Write \(a=a_3,b=b_3,c=c_2,d=c_3\).  The leading forms are
\[
\begin{aligned}
P&=p(pq^2+aq^3),\\
Q&=p(p^3+p^2q+bq^3),\\
R&=p^3+\frac34p^2q+cpq^2+dq^3.                  \tag{1}
\end{aligned}
\]
Let \(\lambda,\mu\) be the two constant contact coefficients.

## 2. The \(d=0\) component

After solving the first four equations triangularly, a lexicographic
elimination basis ends in
\[
(2a-1)^3(10a-3)(20a-13)=0.                      \tag{2}
\]
The three resulting points are:
\[
\begin{array}{c|c|c|c}
a&b&c&d\\ \hline
1/2&-1/8&1/8&0\\
3/10&-7/120&0&0\\
13/20&-7/32&7/32&0.
\end{array}
\]
After the chart divisor \(q\) is removed, their three minors have,
respectively, the further common factors
\[
p(2p+q),\qquad p^2,\qquad p(8p+7q).              \tag{3}
\]
Thus none lies in exact \(\delta=1\).

## 3. The \(d\ne0\) component

The last contact equation gives
\[
8a\mu-8b\lambda-b=0.                             \tag{4}
\]
There is no solution with \(a=0\).  For \(a\ne0\), solve (4), the first
contact equation, and the next linear equation.  Two possible pivot
failures occur:
\[
D=32ac+3a+24b,\qquad E=24a-16c-9.
\]
The \(D=0\) branch is the point
\[
(a,b,c,d)=\left(\frac12,-\frac18,\frac3{32},-\frac1{128}\right),
\]
and the \(E=0\) branch is
\[
(a,b,c,d)=\left(\frac12,-\frac18,\frac3{16},\frac1{64}\right).
\]
Both lie in the \(a=1/2\) family below; the second has a higher gcd.

On \(DE\ne0\), two residual equations have \(c\)-resultant
\[
\begin{aligned}
\mathrm{const}\cdot a(2a-1)^{16}(20a-13)
 &(128a^2-96a+17)^9\\
 &\cdot(160a^3-384a^2+310a-85).                 \tag{5}
\end{aligned}
\]
The quadratic factor in (5) has no contact point.  The value
\(a=13/20\) forces \(d=0\), already treated.  The two remaining
components are:

1. The one-parameter family
   \[
   a=\frac12,\quad b=-\frac18,\quad
   c=4d+\frac18,\quad
   \lambda=\frac12,\quad\mu=-\frac5{32}.
   \]
   Its exact open is \(d(64d-1)\ne0\).  The complete lower identities
   force
   \[
   L(1,-4,2u_1)^T=0,
   \]
   as proved in `HALF_CONTACT_EXCLUSION_NOTE.md`.

2. The cubic coefficient-field component
   \[
   160a^3-384a^2+310a-85=0.
   \]
   Its three minors share the chart divisor times an explicit monic
   quadratic, so its gcd degree is at least three; see
   `CUBIC_CONTACT_GCD_NOTE.md`.

Consequently the generic unmarked chart contains no exact-\(\delta=1\)
Keller map with nonzero tangent.

## 4. Verification and disclosure

`verify_generic_contact_decomposition_sympy.py` reconstructs every contact
equation, the \(d=0\) elimination, both pivot-failure branches, the
resultant (5), the empty quadratic factor, and the two surviving
components.  Leaf-level SymPy and independent PARI/GP replays are run by
`verify_unmarked_delta1_all_strict.sh`.

The component **completeness** presently has one primary elimination
implementation and awaits an independent hostile saturation replay.  It
is therefore not promoted as independently verified.  Exact leaf checks
do not by themselves prove that no component was lost while clearing a
pivot.  This work is AI-assisted, not peer reviewed, and not a scholarly
priority claim.
