# An explicit four-adic construction for Holland's Problem 5.51

**Target:** 2305051 / AMR-022-5051.
**Status:** complete candidate, awaiting separate adversarial review.
**Priority:** unestablished. The absorbed-walk method, smooth singular measures,
Herglotz–Zygmund correspondence, and converse Fatou theorem are classical.

## 1. Statement and meaning of the construction

Problem 5.51 in [Hayman–Lingham's 2018 source](https://arxiv.org/abs/1809.07200),
printed p.105, asks for an explicit Blaschke product \(B\) with \(B(0)=0\)
such that \((1+B)/(1-B)\) is Bloch. Existence is part of the source statement.
The candidate below supplies an entirely specified recursion, rational inner
approximants with algebraic coefficients, and an explicit modulus of locally
uniform convergence. It uses no unspecified covering map, generic parameter,
existential choice of a measure, or unevaluated search for a good Frostman shift.
It does not supply a short closed-form list of the individual zeros.

Identify the circle with \(\mathbb R/\mathbb Z\), and normalize its Lebesgue
measure to have mass one. Write \(\zeta(x)=e^{2\pi i x}\).

### The integer recursion

Start with the cyclic list \(v^{(0)}=(1)\). Given
\(v^{(n)}=(v_0,\ldots,v_{4^n-1})\), replace each entry by four children,
simultaneously using the old list. Indices of the old list are cyclic.

- If \(v_j=0\), its children are \((0,0,0,0)\).
- If \(v_j>0\), set
  \[
  e_1=\begin{cases}+1&v_{j-1}\ge v_j,\\-1&v_{j-1}<v_j,\end{cases}
  \qquad
  e_4=\begin{cases}+1&v_{j+1}>v_j,\\-1&v_{j+1}\le v_j.\end{cases}
  \]
  Take \((e_2,e_3)\) to be the first pair, in the order
  \((-1,-1),(-1,+1),(+1,-1),(+1,+1)\), satisfying
  \(e_1+e_2+e_3+e_4=0\). The children are
  \((v_j+e_1,v_j+e_2,v_j+e_3,v_j+e_4)\).

There is always such a middle pair. In every nonzero parent exactly two
increments are \(+1\), and two are \(-1\). The first two nontrivial lists are

\[
v^{(1)}=(2,0,2,0),
\]
\[
v^{(2)}=(1,3,3,1,0,0,0,0,1,3,3,1,0,0,0,0).
\]

For \(N=4^n\), define \(p_{n,j}=v^{(n)}_j/N\) and
\(\zeta_{n,j}=e^{2\pi i(j+1/2)/N}\). Here is the promised explicit sequence:

\[
 F_n(z)=\sum_{j=0}^{N-1}p_{n,j}
              \frac{\zeta_{n,j}+z}{\zeta_{n,j}-z},
 \qquad
 B_n(z)=\frac{F_n(z)-1}{F_n(z)+1}.
 \tag{1}
\]

Terms of weight zero are omitted. The answer is

\[
 \boxed{\quad B(z)=\lim_{n\to\infty}B_n(z).\quad}
 \tag{2}
\]

**Theorem.** The limit in (2) is an infinite Blaschke product, \(B(0)=0\),
and \(F=(1+B)/(1-B)\) is a Bloch function. Each \(B_n\) is a finite Blaschke
product given by a rational function with algebraic coefficients. Moreover,
for \(0<r<1\),

\[
 \sup_{|z|\le r}|B(z)-B_n(z)|
 \le \frac{4\pi r}{(1-r)^2}\,4^{-n}.
 \tag{3}
\]

The proof follows. All uses of established analytic theory are identified.

## 2. Positivity, consistency, and neighboring intervals

Let \(I_{n,j}=[j4^{-n},(j+1)4^{-n})\), periodically interpreted, and
let \(f_n\) equal \(v^{(n)}_j\) on \(I_{n,j}\).

Induction gives:

\[
0\le f_n\le n+1,\qquad \int_0^1 f_n=1,\qquad
\mathbb E(f_{n+1}\mid\mathcal F_n)=f_n,\qquad
|f_{n+1}-f_n|\le1,
\tag{4}
\]

where \(\mathcal F_n\) is the four-adic partition. Indeed, a positive integer
parent stays nonnegative after adding \(\pm1\), and its four child values
sum to four times the parent. A zero parent stays zero.

We also have the uniform circular neighbor bound

\[
 |v^{(n)}_{j+1}-v^{(n)}_j|\le2.
 \tag{5}
\]

Within one parent, child values differ by at most 2. Across two positive
parents with unequal values, the facing signs move the two values toward one
another, so their new signed difference is the old difference minus twice its
sign. If the parents are equal and positive, the facing signs are \(-1,+1\),
giving difference 2. If one parent is zero and the other is positive, the
positive value is at most 2 by induction, and its facing child has value one
less. If both are zero, both children are zero. This proves (5), including the
cyclic boundary.

The consistent interval masses

\[
 \mu(I_{n,j})=4^{-n}v^{(n)}_j
 \tag{6}
\]

define a probability measure on the circle. For example, take any weak limit
of \(f_n(x)\,dx\); consistency fixes all four-adic interval masses. The bound
\((n+1)4^{-n}\to0\) shows that atoms are impossible (use at most two adjacent
cells around a point), so grid endpoints cause no ambiguity. Those interval
masses determine the measure uniquely; hence the full sequence converges.

## 3. The measure is singular, and has no finite positive derivative

Under Lebesgue measure, the successive values along a four-adic path form a
simple symmetric random walk started at 1 and absorbed at 0: each positive
parent has exactly two upward and two downward children. The placement of
those children changes no conditional transition probability.

For completeness, fix an integer \(M>1\). The walk hits \(\{0,M\}\) almost
surely: in each block of \(M\) steps before exit, the chance of taking enough
consecutive downward steps to exit is at least \(2^{-M}\). Stopping the bounded
martingale at this exit gives probability \(1/M\) of hitting \(M\) first.
The probability of never hitting 0 is consequently at most \(1/M\) for every
\(M\), and is zero. Thus almost every Lebesgue path eventually enters a cell
with mass zero. The countable union of all such cells has full Lebesgue measure
and zero \(\mu\)-measure. Therefore \(\mu\) is singular.

There is a stronger, pointwise fact that will eliminate the singular inner
factor. For **every** circle point \(x\), follow the nested half-open cells
\(I_n(x)\), using the indicated convention at grid endpoints. Then

\[
 \frac{\mu(I_n(x))}{|I_n(x)|}=f_n(x)
 \tag{7}
\]

either becomes identically zero, or changes by exactly \(+1\) or \(-1\)
at every step. In neither case can it converge to a finite positive number.
In particular, the measure cannot have a finite positive ordinary density at
any point, where ordinary density includes all shrinking intervals containing
the point. The same assertion holds for one-sided intervals at grid endpoints.

## 4. A global Zygmund bound, hence a Bloch Herglotz transform

Define the continuous periodic primitives

\[
 H_n(x)=\int_0^x(f_n(t)-1)\,dt.
\]

Every difference \(f_{n+1}-f_n\) has mean zero on each generation-\(n\) cell
and absolute value at most 1. Therefore

\[
 \|H_{n+1}-H_n\|_\infty\le4^{-n},\qquad
 \|H-H_n\|_\infty\le\tfrac43 4^{-n},
 \tag{8}
\]

for a continuous periodic limit \(H\). Since \(H_0=0\), also
\(\|H\|_\infty\le4/3\). Consistency shows that \(dH=d\mu-dx\).

For \(0<h\le1/4\), choose \(n\ge1\) with
\(\ell=4^{-n}\le h<4\ell\). The interval from \(x-h\) to \(x+h\) meets at
most nine consecutive generation-\(n\) cells. By (5), differences of the
values of \(f_n\) on this interval are bounded by 18, a deliberately loose
bound. Hence

\[
 |H_n(x+h)+H_n(x-h)-2H_n(x)|
 =\left|\int_0^h(f_n(x+t)-f_n(x-t))\,dt\right|\le18h.
\]

The error from (8) is at most \((16/3)\ell\). Thus

\[
 |H(x+h)+H(x-h)-2H(x)|\le24h.
 \tag{9}
\]

For \(h>1/4\), the same bound follows from \(\|H\|_\infty\le4/3\).
In particular, for arbitrary adjacent arcs of equal length, including arcs
crossing the origin,

\[
 |\mu((x,x+h])-\mu((x-h,x])|\le24h.
 \tag{10}
\]

Now set

\[
 F(z)=\int_0^1\frac{e^{2\pi ix}+z}{e^{2\pi ix}-z}\,d\mu(x).
 \tag{11}
\]

We use the classical **Herglotz–Zygmund correspondence**: the Herglotz
transform of a finite positive measure on the circle is Bloch if and only
if its masses on adjacent equal-length arcs differ by at most a constant
times their length. The precise criterion is recalled in the proof of
Theorem 3.5, printed p.333, of
[Aleksandrov–Anderson–Nicolau (1999)](https://doi.org/10.1112/S002461159901196X).
This is a standard analytic input, not a new assertion or the existence
construction requested by the problem. Applying it to the proved global
estimate (10) gives

\[
 \sup_{z\in\mathbb D}(1-|z|^2)|F'(z)|<\infty.
 \tag{12}
\]

Also \(F(0)=1\) and \(\operatorname{Re}F>0\).

## 5. The Cayley transform is a pure Blaschke product

Put \(B=(F-1)/(F+1)\). It is a holomorphic map into the disk and \(B(0)=0\).
The Poisson integral \(\operatorname{Re}F\) has radial limit zero almost
everywhere because \(\mu\) is singular. Since

\[
 1-|B(z)|^2=\frac{4\operatorname{Re}F(z)}{|F(z)+1|^2}
 \le4\operatorname{Re}F(z),
\]

the bounded analytic function \(B\) is inner. It is nonconstant: a constant
\(F\) with this normalization would have Lebesgue, not singular, Herglotz
measure.

**The remaining issue is essential:** a locally uniform limit of finite
Blaschke products can have a singular inner factor. We exclude it explicitly.

Suppose the canonical inner factorization of \(B\) contains a singular factor
\(S_\nu\) with a nonzero positive singular measure \(\nu\). At
\(\nu\)-almost every point \(\xi\), \(P[\nu](z)\to+\infty\)
nontangentially, and therefore \(|S_\nu(z)|\to0\). This usual singular-measure
boundary fact follows from \(\nu(I)/|I|\to\infty\) at \(\nu\)-almost every
point and the lower Poisson-kernel bound in each Stolz cone. The other inner
factor is bounded by 1, so \(B(z)\to0\) nontangentially at such a point.
Consequently \(F(z)\to1\), and \(\operatorname{Re}F(z)\to1\).

Use the classical **converse Fatou theorem for positive measures**: a finite
nontangential limit \(L\) of a positive Poisson integral implies ordinary
boundary density \(L\) of its measure. The theorem of Loomis, with ordinary
and symmetric derivatives carefully distinguished, is stated on printed
pp.207–208 of
[Carmona–Donaire (1999)](https://doi.org/10.2140/pjm.1999.191.207).
Its disk form, in normalized angular coordinates, gives

\[
 \frac{\mu(I)}{|I|}\longrightarrow1
 \quad\text{as intervals }I\ni\xi\text{ shrink to }\xi.
 \tag{13}
\]

This applies also when \(\xi\) is an endpoint of the four-adic cells. Indeed,
the limit over intervals with the point strictly inside implies each
one-sided limit: append an interval of relative length \(\varepsilon\) on the
other side and use positivity, then let \(\varepsilon\downarrow0\).
Equivalently one may use the ordinary derivative of the distribution function.

Equation (13) contradicts (7), with \(L=1\). Thus \(\nu=0\), and \(B\)
is a Blaschke product without a singular inner factor. The normalization
\(B(0)=0\) has not required any shift or change of variable.

It is infinite. A nonconstant finite Blaschke product attains the value 1
on the circle and has nonzero boundary derivative there. Its Cayley transform
has a simple boundary pole, whose derivative violates (12). This cannot be
the present \(B\).

## 6. The explicit approximants and their convergence

By (6), the atomic probability measure
\(\mu_n=\sum_j p_{n,j}\delta_{\zeta_{n,j}}\) has exactly the same masses
as \(\mu\) on every generation-\(n\) cell. Formula (1) is its Herglotz
transform and Cayley transform. For \(|z|\le r\), the derivative with respect
to \(x\) of the Herglotz kernel has modulus at most
\(4\pi r/(1-r)^2\). Moving all cell mass to the cell midpoint therefore gives

\[
 \sup_{|z|\le r}|F(z)-F_n(z)|
 \le\frac{2\pi r}{(1-r)^2}\,4^{-n}.
 \tag{14}
\]

Both transforms have positive real part. The identity

\[
 B-B_n=\frac{2(F-F_n)}{(F+1)(F_n+1)}
\]

and \(|F+1|,|F_n+1|\ge1\) prove (3). Thus (1)–(2) specify the answer with
a known compact-uniform error bound.

Each \(F_n\) is rational. On the circle away from its finitely many atoms
it is purely imaginary, so \(|B_n|=1\) there. At an atom its pole becomes
a removable point of \(B_n\) with value 1. Positivity excludes any zero of
\(F_n+1\) in the disk. Hence \(B_n\) is a rational inner function, and
therefore a finite Blaschke product. Its coefficients are algebraic because
the weights are rational and the \(\zeta_{n,j}\) are roots of unity.

If a polynomial form is desired, let \(J_n=\{j:p_{n,j}>0\}\) and write

\[
 Q_n(z)=\prod_{j\in J_n}(\zeta_{n,j}-z),\qquad
 P_n(z)=\sum_{j\in J_n}p_{n,j}(\zeta_{n,j}+z)
                 \prod_{k\in J_n\setminus\{j\}}(\zeta_{n,k}-z).
\]

Then \(B_n=(P_n-Q_n)/(P_n+Q_n)\). This is a finite algebraic formula at
every stage, not an appeal to an unknown conformal map. The zeros of the limit
give its usual canonical infinite-product representation; a separate
closed-form zero list is not claimed.

## 7. Attribution and validation boundary

Kahane's absorbed-walk construction of singular Zygmund measures and Cantón's
four-adic neighbor-directed refinements are prior methods. The recursion here
fixes unit steps, only the absorbing barrier at zero, and every endpoint and
middle-child choice. Its finite-positive-density exclusion is checked
pointwise rather than inferred from almost-everywhere singularity.

The strong existence theorem of Aleksandrov–Anderson–Nicolau, Theorem 2,
already produces interpolating Blaschke products with much stronger prescribed
derivative decay by a covering-map construction. This candidate does not claim
a new existence theorem or a stronger decay theorem. Its proposed answer to
Holland is the explicit recursion (1)–(2), with proof that this particular limit
has no singular factor and has the required Bloch Cayley transform.

The accompanying exact checker tests finite stages and local transition cases.
It does not replace the all-stage induction, the converse Fatou theorem, or the
Herglotz–Zygmund criterion. The current literature audit establishes no priority
claim. Separate review must assess both correctness and whether this explicit
recursive construction meets the source's request.
