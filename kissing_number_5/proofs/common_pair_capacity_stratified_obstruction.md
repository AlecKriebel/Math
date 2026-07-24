# Stratified common-pair capacities and an exact degree-three obstruction

## Scope

This note strengthens the common-pair projection inequality by allowing an
arbitrary selected set of base pairs.  It then proves:

**Fixed-support theorem.**  No 41-point spherical kissing code has all inner
products in
\[
 S=\left\{-\frac{77}{100},-\frac7{10},-\frac{11}{25},
           -\frac9{100},\frac{499}{1000}\right\}
\]
with ordered pair multiplicities
\[
 (170,6,262,652,550).
\]

The proof uses only two stratified capacity rows and three scalar
consequences of the total-degree-three Bachoc--Vallentin matrices.  It
excludes every nonnegative real triangle measure with the required
marginals, so neither integrality nor graph realizability is assumed.

This is a fixed-support theorem, not a reduction of arbitrary kissing codes
to \(S\), and hence not a global upper bound for \(\tau(5)\).

## 1. Arbitrary base subsets

Let \(C\subset S^4\) be a kissing code.  Fix \(0<b\leq1/2\).  For an
ordered base pair \((y,z)\), write \(q=\langle y,z\rangle\).  The projection
theorem in `common_pair_capacity_hierarchy.md` proves, whenever
\(-1\leq q\leq0\),
\[
 \#\{x\ne y,z:\langle x,y\rangle,\langle x,z\rangle\geq b\}
 \leq M\!\left(\frac{2b^2}{1+q}\right),              \tag{1}
\]
with the value at \(q=-1\) interpreted as zero.

Because (1) holds separately for every base pair, it can be summed over
any chosen collection of base pairs.  In normalized pair/triple notation,
for every measurable \(B\subseteq[-1,0]\),
\[
 \int {\bf1}_{\{t\in B,\ u\geq b,\ v\geq b\}}\,d\nu
 \leq
 \int_B M\!\left(\frac{2b^2}{1+t}\right)\,d\alpha(t).
 \tag{2}
\]
No regularity of \(B\) is needed for a finite code: both measures are
finite atomic counting measures.

On a finite support \(s_0,\ldots,s_{r-1}\), selecting
\(B=\{s_i\}\) gives the exact-color row
\[
 \sum_T c_{i,b}(T)n_T
 \leq
 M\!\left(\frac{2b^2}{1+s_i}\right)E_i,              \tag{3}
\]
where \(E_i\) is the unordered color-\(i\) edge count and
\(c_{i,b}(T)\) counts edges of color \(i\) in triangle type \(T\) whose
other two colors are at least \(b\).  Repeated colors cause no orbit factor:
each qualifying geometric base edge is counted once on both sides after
converting ordered base pairs to unordered edges.

The earlier cumulative row
\[
 \sum_{s_i\leq a}\sum_T c_{i,b}(T)n_T
 \leq M\!\left(\frac{2b^2}{1+a}\right)
       \sum_{s_i\leq a}E_i
\]
remains valid, but is weaker because it lets the least favorable capacity
at \(a\) apply to every deeper edge.  In particular, unused deeper edges
cannot supply capacity to a shallower edge in (3).

## 2. The two rows used here

For \(b=499/1000\), the pair counts give
\[
 E_2=131,\qquad E_3=326.
\]
At \(s_2=-11/25\),
\[
 p_2=\frac{249001}{280000}>\frac34,
\]
so (3) has capacity one:
\[
 \sum_Tc_{2,b}(T)n_T\leq131.                         \tag{4}
\]
At \(s_3=-9/100\),
\[
 p_3=\frac{249001}{455000}>\frac12,
\]
so (3) has capacity four:
\[
 \sum_Tc_{3,b}(T)n_T\leq1304.                        \tag{5}
\]
All inequalities include equality at the code constraint
\(\langle x,y\rangle=1/2\).

## 3. Three degree-three harmonic forms

There are exactly 21 sorted triangle types \(T=(i,j,k)\) on \(S\) whose
\(3\times3\) correlation determinant is nonnegative.  Let \(x_T\geq0\)
be their putative unordered triangle masses.  The five edge marginals are
\[
 \sum_T\operatorname{mult}_i(T)x_T
 =(3315,117,5109,12714,10725)_i.                    \tag{6}
\]

Let \(M_k(x)\) denote the standard fixed-\(N\)
Bachoc--Vallentin block of total degree three and harmonic degree \(k\).
Every genuine code has \(M_k(x)\succeq0\).  We use only the scalar forms
\[
\begin{aligned}
 v_0&=(1/5,1/4,-1,-1/2),\\
 v_1&=(1/3,8/15,-1),\\
 v_2&=(3/4,1),
\end{aligned}
\qquad
 q_k(x)=v_k^{\mathsf T}M_k(x)v_k\geq0.              \tag{7}
\]
Write
\[
 q_k(x)=c_k+\sum_T a_{kT}x_T.
\]
Exact evaluation gives
\[
\begin{aligned}
c_0&=\frac{7521382450606171}{80000000000000000},\\
c_1&=\frac{24172438575674461301}{7380000000000000000},\\
c_2&=\frac{15594576145087318011}{820000000000000000}.
\end{aligned}                                      \tag{8}
\]

## 4. Exact Farkas contradiction

Use the equality multipliers
\[
 y=(-3001,-2658,-627,1134,1554),
\]
the nonnegative upper-row multipliers
\[
 \mu=(13920,7622)
\]
for (4)--(5), and the nonnegative BV multipliers
\[
 \eta=(434743,282109,252632)
\]
for (7).  For every triangle type define
\[
 d_T=
 \sum_i y_i\operatorname{mult}_i(T)
 -\mu_2c_{2,b}(T)-\mu_3c_{3,b}(T)
 +\sum_{k=0}^2\eta_k a_{kT}.                         \tag{9}
\]

Exact rational enumeration of all 21 determinant-feasible types gives
\[
 d_T<0\quad\hbox{for every }T,
\]
with largest coefficient
\[
 \max_Td_T
 =-\frac{2801589051645351149}{29520000000000000}<0. \tag{10}
\]
On the other hand, (4)--(8) imply
\[
\begin{aligned}
\sum_Td_Tx_T
&\geq
 \sum_i y_i(6)_i
 -13920(131)-7622(1304)
 -\sum_{k=0}^2\eta_kc_k\\
&=
\frac{529486113987585345823187}
     {5904000000000000000}
>0.                                                  \tag{11}
\end{aligned}
\]
But \(x_T\geq0\) and (10) give
\(\sum_Td_Tx_T\leq0\), contradicting (11).  This proves the
fixed-support theorem.

## 5. Computer-certified and human-readable parts

The projection and arbitrary-subset arguments, the marginal identities,
and the Farkas implication above are human-readable mathematics.  The only
finite computation is exact evaluation of the 21 Gram determinants, the
three rational BV forms, and the 21 coefficients in (9).

The data are stored in
`certificates/common_pair_capacity_stratified_dual.json`.  The verifier
`verifiers/verify_common_pair_capacity_stratified_dual.py`:

1. checks the SHA-256 hash of the pair certificate;
2. independently enumerates every sorted support triple and retains all
   determinant-zero boundary cases;
3. reconstructs the fixed-\(N\) BV matrices from the polynomialized
   transverse kernels using exact rational arithmetic;
4. verifies (4)--(8), every sign in (9), and the exact value (11).

It uses only the Python standard library and does not import the earlier
cumulative-hierarchy verifier.  Run

```bash
PYTHONPATH=. python3 \
  verifiers/verify_common_pair_capacity_stratified_dual.py

PYTHONPATH=. python3 -m unittest \
  tests.test_common_pair_capacity_stratified_dual -v
```

No solver output, floating-point comparison, strict-PSD assumption, or
integer triangle count is used by the certificate.

## 6. Dependency map

\[
\begin{array}{c}
\text{base-pair projection theorem}\\
\Downarrow\\
\text{arbitrary-subset summation (2)}
\Longrightarrow\text{exact-color rows (4)--(5)}
\\[2mm]
\text{BV kernel positivity}
\Longrightarrow\text{scalar rows (7)}
\\[2mm]
\text{pair marginal identities (6)}
+\text{exact Farkas coefficients (9)--(11)}
\\
\Downarrow\\
\text{no triangle measure}
\Downarrow\\
\text{no code with the stated support and pair counts.}
\end{array}
\]
