# An exact barrier for the split quadratic-kernel spectrum

## Status

This note gives an exact 41-row counterexample to an abstract
split-spectrum attack on the quadratic kernel.  It satisfies the separate
rank-five and rank-fourteen PSD decompositions, both resulting Ky Fan
constraints, the constant diagonal, and the nonpositive off-diagonal sign
condition after the rank-one shift.  It is not a spherical code because it
violates the lower endpoint of the common-source entry range.

The note also proves that this lower endpoint prevents the same extension
when the first 40 rows are the \(D_5\) code.  Thus it isolates exactly what
the spectral/sign abstraction forgets.

## The kernel split for a genuine code

For a code Gram matrix \(G\), write
\[
P_2(t)=\frac{5t^2-1}{4},\qquad
H_2=P_2[G],
\]
\[
R=\frac12G+\frac45H_2,\qquad
K=R-\frac3{10}J.
\]
Then
\[
R_{ij}=g_{ij}^2+\frac12g_{ij}-\frac15,\qquad
K_{ij}=(g_{ij}+1)(g_{ij}-\tfrac12).
\]
Consequently
\[
\begin{aligned}
&R\succeq0,\quad \operatorname{rank}R\leq19,\quad
 R_{ii}=13/10,\\
&K_{ii}=1,\quad K_{ij}\leq0\quad(i\ne j).
\end{aligned}                                      \tag{1}
\]
The two PSD summands have ranks at most 5 and 14, diagonals \(1/2\) and
\(4/5\), and traces \(N/2\) and \(4N/5\).  Therefore
\[
\sum_{i=1}^5\lambda_i(R)\geq\frac N2,\qquad
\sum_{i=1}^{14}\lambda_i(R)\geq\frac{4N}{5}.        \tag{2}
\]
For a genuine common source \(g_{ij}\in[-1,1/2]\), one also has
\[
-\frac{21}{80}\leq R_{ij}\leq\frac3{10}
\qquad(i\ne j).                                    \tag{3}
\]

## A 41-row exact abstract counterexample

Start with the 40 normalized \(D_5\) roots \(x\).  Define two feature maps
\[
a(x)=\frac{x}{\sqrt2},\qquad
b(x)=xx^{\mathsf T}-\frac15I.
\]
Their inner products are
\[
a(x)\mathbin{\cdot}a(y)=\frac12(x\mathbin{\cdot}y),
\]
\[
\langle b(x),b(y)\rangle_F=(x\mathbin{\cdot}y)^2-\frac15
=\frac45P_2(x\mathbin{\cdot}y).
\]
The linear features live in dimension 5 and the traceless symmetric
features in dimension 14.  Both have squared norms \(1/2\) and \(4/5\).

Append a forty-first abstract row with features
\[
a_*=\frac{e_1}{\sqrt2},\qquad b_*=-b(e_1).
\]
Let \(A,B\) be the two feature Gram matrices and put
\[
R=A+B,\qquad K=R-\frac3{10}J.
\]
Then, exactly,
\[
A\succeq0,\quad\operatorname{rank}A=5,\quad A_{ii}=1/2,
\]
\[
B\succeq0,\quad\operatorname{rank}B=14,\quad B_{ii}=4/5,
\]
so \(R\succeq0\), \(\operatorname{rank}R\leq19\), and \(R_{ii}=13/10\).
At order 41,
\[
\operatorname{tr}A=\frac{41}{2},\qquad
\operatorname{tr}B=\frac{164}{5},
\]
and the variational proof of (2) applies verbatim.

For an old root put \(t=e_1\mathbin{\cdot}x\).  The possible values are
\(0,\pm1/\sqrt2\), and
\[
R_{*,x}=\frac12t-\left(t^2-\frac15\right).
\]
Thus
\[
\begin{array}{c|c|c}
t&R_{*,x}&K_{*,x}\\ \hline
0&1/5&-1/10\\
1/\sqrt2&-3/10+\sqrt2/4&-3/5+\sqrt2/4\\
-1/\sqrt2&-3/10-\sqrt2/4&-3/5-\sqrt2/4.
\end{array}                                        \tag{4}
\]
Every entry in the last column is negative.  The old-old entries satisfy
\(K_{xy}\leq0\) because they come from the genuine \(D_5\) code.  Hence
the full order-41 matrix satisfies every condition in (1)--(2).
Moreover, \(K\) has rank at most 20 and at most one negative eigenvalue,
because it is a rank-one negative perturbation of \(R\succeq0\).

This refutes any proposed \(N\leq40\) theorem based only on the split PSD
ranks, their traces or Ky Fan consequences, the constant diagonal, and
the \(Z\)-matrix sign condition on \(K\).

The deliberately missing constraint is visible in (4):
\[
-\frac3{10}-\frac{\sqrt2}{4}<-\frac{21}{80}.
\]
Thus the counterexample violates the lower half of (3), and its two
features do not arise from one common point \(x_*\).

## Why the full interval blocks this particular extension

The failure is not an artifact of the chosen sign \(b_*=-b(e_1)\).
Suppose the old 40 linear and quadratic features remain those of \(D_5\),
while a new row has any linear feature of squared norm \(1/2\) and any
quadratic feature of squared norm \(4/5\).  Since the old linear features
span \(\mathbb R^5\), write the new one as \(u/\sqrt2\) for a unit vector
\(u\).

The quadratic feature is even on each antipodal root pair:
\[
b(x)=b(-x).
\]
If its inner product with the new quadratic feature is \(c_x\), the two
combined entries against \(x\) and \(-x\) are
\[
c_x+\frac12u\mathbin{\cdot}x,\qquad
c_x-\frac12u\mathbin{\cdot}x.
\]
For both to lie in the interval (3), whose width is \(9/16\), it is
necessary that
\[
|u\mathbin{\cdot}x|\leq\frac9{16}
\quad\text{for every }D_5\text{ root }x.            \tag{5}
\]

Let \(a\geq b\) be the two largest absolute coordinates of \(u\).
Choosing their signs gives a \(D_5\) root with
\[
|u\mathbin{\cdot}x|=\frac{a+b}{\sqrt2}.
\]
Since the remaining three coordinates have absolute value at most \(b\),
\[
1\leq a^2+4b^2\leq\frac54(a+b)^2.
\]
Therefore
\[
\max_{x\in D_5}|u\mathbin{\cdot}x|
\geq\sqrt{\frac25}>\frac9{16},                     \tag{6}
\]
where the last inequality follows after squaring:
\(2/5>81/256\).  This contradicts (5).

This is only a \(D_5\)-based obstruction.  It does not show that every
possible 40-row base, much less every hypothetical 41-code, has the same
property.

## Exact remaining gap

The abstract split spectrum and Lorentzian sign pattern do not distinguish
40 from 41.  A viable kernel proof must use at least one genuinely
common-source condition, such as the full entry range (3), the nonlinear
identity
\[
R_{ij}=g_{ij}^2+\frac12g_{ij}-\frac15,
\]
or higher cycle compatibility shared by \(G\) and \(H_2\).  The interval
alone blocks the displayed extension of \(D_5\), but no
classification-free contradiction at order 41 is proved.

## Reproduction

Run

```sh
python3 verifiers/verify_split_kernel_abstract.py
python3 -m unittest tests.test_split_kernel_abstract -v
```

The verifier uses exact arithmetic in \(\mathbb Q(\sqrt2)\).
