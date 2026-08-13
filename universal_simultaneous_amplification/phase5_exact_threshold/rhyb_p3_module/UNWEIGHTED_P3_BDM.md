# The `R_hyb` dual-moment inequality for the three-vertex path

Date: 2026-08-13 (America/Los_Angeles)

No graph search or external input is used here.  The calculation is an exact
three-state-orbit proof of the bounded dual-moment inequality from
`RHYB_COMPACTNESS_AND_DUAL_MOMENT.md`.

## Theorem

Let `H=P_3` be the unweighted three-vertex path, with centre `0` and leaves
`1,2`.  Let the three portal loads be arbitrary nonnegative numbers, not all
zero.  At

\[
 r=R_{hyb}=1.5028569127905696\ldots,
\]

the exact separated-module response satisfies

\[
                       D+(r-1)B<0                         \tag{1}
\]

at every positive gate scale.  Equivalently, `P_3` satisfies the bounded
dual-moment inequality (BDM), strictly, for every portal vector.

This is the first proved non-complete module class for BDM.  Unlike a radial
complete module, it has two inequivalent vertex orbits and its two portal
laws differ because the centre has degree two.

## Exact dual data

Put

\[
                       L=2r^2+r+2.
\]

Solving both six-state absorbing chains gives

\[
 b={r^2(4r^3+8r^2+7r+6)\over (r+2)L^2},\qquad
 a={5r+1\over9(r-1)(r+1)}.                              \tag{2}
\]

Here `b=rho_Bd(P_3,r)` and
`a=rho_dB(P_3,r)/(r-1)`.  Type complementation identifies the singleton
atoms of the fitness-`r` OR dual with the individual fixation probabilities
at reciprocal fitness.  On the centre/leaf orbits these are

\[
 \begin{aligned}
 u_0&={2r^3+5r^2+4r+4\over(2r+1)L^2},&
 u_\ell&={2\over L},\\
 v_0&={r+2\over3(r+1)},&
 v_\ell&={1\over2(r+1)}.                               \tag{3}
 \end{aligned}
\]

The inverse-degree vector entering the dB portal law is

\[
                         e=(1/2,1,1).                   \tag{4}
\]

The verifier reconstructs all of (2)--(4) directly from the labelled
chains; they are not assumed inputs.

## Portal-uniform quadratic

Let `x=(x_0,x_1,x_2)>=0` be the portal vector and set

\[
 A=(x\mathbin\cdot\mathbf1)(x\mathbin\cdot e),\qquad
 Q=(x\mathbin\cdot u)(x\mathbin\cdot(ev)),\qquad
 C=r(r-1)^2.
\]

The denominator-cleared BDM gap at gate odds `z>=0` is

\[
 \mathcal G_z=
 C\{(1+z)(1-a)-bz\}A+z\{1+z(1-b)\}Q.                  \tag{5}
\]

As established in the parent reduction, `mathcal G_z>=0` is exactly the
opposite sign of the cleared separator numerator, so it implies (1).

Expand (5) in portal monomials.  Because the two leaves are equivalent,
there are only three coefficient polynomials:

\[
 \Gamma_{XY}(z)=A_{0,XY}+A_{1,XY}z+A_{2,XY}z^2,
       \qquad XY\in\{00,0\ell,\ell\ell\}.              \tag{6}
\]

For vertices `i,j` in the indicated orbits,

\[
 \begin{aligned}
 E_{ij}&=(e_i+e_j)/2,\\
 S_{ij}&=(u_i e_jv_j+u_j e_iv_i)/2,\\
 A_{0,ij}&=C(1-a)E_{ij},\\
 A_{1,ij}&=C(1-a-b)E_{ij}+S_{ij},\\
 A_{2,ij}&=(1-b)S_{ij}.                                \tag{7}
 \end{aligned}
\]

At `R_hyb`, both endpoint coefficients are strictly positive because

\[
 1-a={9r^2-5r-10\over9(r-1)(r+1)}>0,\qquad
 1-b={2(r^2+2r+2)\over(r+2)(2r^2+r+2)}>0.              \tag{8}
\]

It remains to prove that each discriminant is negative.  After cancellation
their denominators are manifestly positive.  Their numerators, in the order
`00,0ell,ellell`, are

\[
\begin{aligned}
p_{00}={}&256r^{14}+320r^{13}-892r^{12}-4524r^{11}
-2231r^{10}+8140r^9+13288r^8-5492r^7\\
&-18284r^6+3000r^5+14804r^4+1712r^3-3920r^2-192r+576,\\[2mm]
p_{0\ell}={}&256r^{14}+320r^{13}-892r^{12}-4524r^{11}
-2343r^{10}+7688r^9+13086r^8-4282r^7\\
&-16803r^6+2390r^5+13017r^4+1552r^3-3144r^2-160r+400,\\[2mm]
p_{\ell\ell}={}&64r^{12}+16r^{11}-255r^{10}-880r^9
+470r^8+1872r^7+971r^6-3148r^5\\
&-1194r^4+3364r^3+241r^2-1116r+324.                  \tag{9}
\end{aligned}
\]

Let

\[
 I=[1502856912/10^9,1502856913/10^9].                  \tag{10}
\]

The hybrid sextic has exactly one root in `I`.  Exact Sturm sequences show
that each polynomial in (9) has zero roots in `I`, and direct rational
evaluation at the left endpoint is negative.  Hence all three discriminants
are strictly negative at `R_hyb`.

Thus every polynomial in (6) is positive for every real `z`.  Every portal
monomial has a nonnegative coefficient and at least one is present when
`x` is nonzero, so `mathcal G_z>0`.  This proves the theorem.

## Scope

The result does not prove universal BDM.  It proves a portal-uniform,
nonradial base case in which genuine rank-two and rank-three stationary flow
is retained.  The weighted path remains a natural next structural case.

## Replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B verify_unweighted_p3_bdm.py
```

The replay independently rebuilds the two labelled absorbing chains,
checks complementation, derives the portal quadratic, and verifies all Sturm
certificates over (10).

