# Turn3: eventual unimodality and fixed-distance edge ULC

**Target:**30005718 / OWR-14298007-013. **Substantive author count:**3/5.  
**Status:** partial. The full all-size ULC question remains unresolved.

## 1. Results

Use m=n−4, F_m=z^(−3)V_n=∑_j c_m,j z^j, and D_m=deg F_m=floor(3(m+1)/2). The original ULC normalization is still by binom(d_n,k), with d_n=D_m+3 and k=j+3.

This turn proves:

1. Explicit all-size coefficient-ratio inequalities force the lower coefficients to increase and the upper coefficients to decrease on regions of linear width.
2. Combined with TURN_2's eventual strict ULC in proportional bands, these imply that **V_n is unimodal for every sufficiently large n**, with either one maximum or two adjacent equal maxima. The threshold is not computed, and this does not settle unimodality for every n.
3. For every fixed positive integer j, the original ULC inequality at k=j+3 is eventually strict as n→infinity. For every fixed positive integer h, the inequality at k=d_n−h is eventually strict, in both parities.

Thus any sequence of ULC violations with n→infinity must occur at distances from the two support ends that tend to infinity but are sublinear in n. This is a sharper remaining gap, not a proof excluding such violations.

## 2. A coefficient-ratio criterion for polynomial matrices

**Lemma (marking zero-degree factors).** Let A(z) be a nonnegative polynomial matrix, with constant matrix P=A(0), and suppose its linear coefficient satisfies A_1≥gamma P entrywise, gamma>0. Let u(z),b(z) be nonnegative polynomial row/column vectors, and put Z_r(z)=u(z)A(z)^r b(z)=∑_ell z_r,ell z^ell. Then

\[
(\ell+1)z_{r,\ell+1}\ge
\gamma(r-\ell)z_{r,\ell}
\quad(\ell\ge0).
\tag{1}
\]

The assertion is trivial when r−ell≤0; no division by a zero coefficient is used.

**Proof.** Since A'(z)≥gamma P coefficientwise, and u',b' are nonnegative, differentiation gives

\[
Z_r'(z)\ge\gamma\sum_{i=0}^{r-1}
u(z)A(z)^iP A(z)^{r-1-i}b(z)
\]

coefficientwise. Expand the coefficient of z^ell as a sum over choices of degrees in the r factors and both endpoint vectors, and over intermediate matrix indices. The marked sum on the right counts each nonnegative contribution once for each matrix factor chosen at degree zero. At most ell factors have positive degree, so at least r−ell are zero-degree factors. This proves (1). It is valid for noncommuting coefficient matrices. ∎

In particular z_r,ell+1>z_r,ell whenever z_r,ell>0 and gamma(r−ell)>ell+1. This is a finite, all-size sufficient criterion for an increasing coefficient segment. Applying it to a reversed recursion can give a decreasing segment at the opposite end.

## 3. Linear-width monotonicity at both ends

For the two-state N(z)=I+zA+z²B in TURN_1, A≥I entrywise. Apply (1), with gamma=1 and the endpoint vectors u=(2+z,2), b=(2,z)^T, to obtain

\[
(j+1)c_{m,j+1}\ge(m-j)c_{m,j}.
\tag{2}
\]

Consequently

\[
c_{m,j+1}>c_{m,j}\quad\text{if }j<(m-1)/2.
\tag{3}
\]

To treat the other end, use the reversal matrices of TURN_1:

\[
K(w)=P+wR+w^2S+w^3I,
\quad
P=\begin{pmatrix}1&0\\3&1\end{pmatrix},\quad
R=\begin{pmatrix}5&3\\5&2\end{pmatrix}.
\]

Here R≥(5/3)P entrywise. Let a_r,h=v_n,d_n−h be the reversed coefficients, with n=2r+4 or2r+5. In both cases, the polynomial with coefficients shifted once,

\[
Z_r(w)=w\sum_{h\ge0}a_{r,h}w^h,
\]

has the form U K^r b or U L K^r b from TURN_1, with all endpoint coefficients nonnegative. Applying (1) at ell=h+1 gives

\[
(h+2)a_{r,h+1}\ge\frac53(r-h-1)a_{r,h}.
\tag{4}
\]

Thus the original coefficient row is strictly decreasing at an upper edge whenever its reversed distance h satisfies

\[
0\le h<(5r-11)/8.
\tag{5}
\]

The condition may be empty at small r; no small-r conclusion is inferred from an empty range.

## 4. Eventual unimodality of the complete coefficient row

TURN_2, applied with epsilon=1/4, gives strict ULC and hence strict ordinary log-concavity for all indices j in [m/4,5m/4] once m exceeds its band-dependent threshold. Increase the threshold also to at least256. Put

\[
p=\lfloor m/3\rfloor,\qquad q=\lceil6m/5\rceil.
\]

These and the intervening neighboring indices are inside that proportional band. By (3), c_m,j is strictly increasing for every j≤p. It is strictly decreasing for every edge with index i≥q: indeed its reversed edge distance is h=D_m−i−1, and

\[
h\le(3/2)m+1/2-(6/5)m=(3/10)m+1/2,
\]

while r=floor(m/2) gives

\[
(5r-11)/8\ge(5/16)m-27/16.
\]

The first bound is strictly smaller than the second for m≥256, so (5) applies to all such upper edges.

Within the middle interval, strict ordinary log-concavity says that the adjacent ratios c_m,j+1/c_m,j strictly decrease. The first relevant ratio is greater than1 by the lower-edge bound, and the last is less than1 by the upper-edge bound. Hence the row crosses from increasing to decreasing only once. Equality can occur in at most one adjacent ratio, giving at most two adjacent equal maxima. This proves eventual unimodality for the entire row, including its already-controlled ends. Leading zeros in V_n do not affect this conclusion.

The proof has an unspecified threshold inherited from TURN_2; checking a finite range numerically cannot replace an explicit bound on that threshold. No assertion of unimodality for every n is made.

## 5. Every fixed lower-edge ULC inequality is eventually strict

Let Fibonacci numbers be F_0=0,F_1=1,F_(a+2)=F_(a+1)+F_a. For each fixed j≥0, the coefficient c_m,j is a polynomial in m of degree j. More precisely,

\[
c_{m,j}=C_jm^j+O(m^{j-1}),
\qquad C_j=\frac{4F_{2j+2}}{j!}.
\tag{6}
\]

For j=0 the formula means c_m,0=4 exactly.

**Proof.** Expand N^m=(I+zA+z²B)^m as ∑_ell binom(m,ell)(zA+z²B)^ell. In coefficient degree j, only ell≤j occurs. The coefficient of m^j can only come from ell=j, using zA in every factor and the constant endpoint vectors u_0=(2,2), b_0=(2,0)^T. Thus C_j=u_0A^jb_0/j!. The standard Fibonacci matrix identity for A=[[2,1],[1,1]] gives u_0A^jb_0=4F_(2j+2). This proves (6) directly and agrees with the source's fixed-coefficient polynomial theorem. ∎

The even-index Cassini identity is

\[
F_{2j+2}^2-F_{2j}F_{2j+4}=1.
\tag{7}
\]

It follows either from the determinant-one Fibonacci matrix or by induction using the recurrence F_(2j+4)=3F_(2j+2)−F_(2j). For j≥1, equations (6)–(7) give

\[
(j+3)C_j^2-(j+4)C_{j-1}C_{j+1}
=\frac{16}{(j!)^2}\frac{3F_{2j+2}^2+j(j+4)}{j+1}>0.
\tag{8}
\]

Since d_n=(3/2)m+O(1), the original ULC margin at k=j+3 has leading term

\[
\Delta_{n,j+3}
=\frac32\big[(j+3)C_j^2-(j+4)C_{j-1}C_{j+1}\big]
 m^{2j+1}+O(m^{2j}).
\tag{9}
\]

For each fixed j it is therefore positive for all sufficiently large m, in both parities. This is a fixed-index assertion; its threshold may grow with j. The case j=0 is already automatic from the zero preceding coefficient.

## 6. Every fixed upper-edge ULC inequality is eventually strict

Let a_r,h denote the top-distance coefficients as in §3. The unipotent truncation lemma in TURN_1 first shows that each a_r,h is a polynomial in r. We now determine its leading term for every fixed h≥0:

\[
a_{r,h}=\frac{3^{2h+1}}{(2h+1)!}r^{2h+1}+O(r^{2h})
\quad(n=2r+4),
\tag{10}
\]
\[
a_{r,h}=\frac{3^{2h}}{(2h)!}r^{2h}+O(r^{2h-1})
\quad(n=2r+5).
\tag{11}
\]

For h=0 the odd coefficient is exactly1, so the remainder convention in (11) is harmless.

### Leading-word proof

Put J=P−I=3E_21 and write K−I=J+wR+w²S+w³I. If ell is the greatest word length with a nonzero relevant w coefficient, the leading r^ell coefficient comes from (K−I)^ell divided by ell!. Lower powers in each binomial polynomial affect only lower r degrees. Terms of a given w degree may be organized as words in J and the positive-w-degree factors. Consecutive J factors vanish, since J²=0.

For even n, equation (9) of TURN_1 requires coefficient w^(h+1) in U K^r b. The constant endpoint vectors are e_1^T and e_2. They kill J at the first and last position. With h+1 positive-w-degree factors, the greatest possible word length is2h+1. At that length every positive-degree factor must be wR, and the unique allowed pattern is

\[
(wR)J(wR)J\cdots J(wR).
\]

Its endpoint contraction uses R_12=3 and J_21=3 throughout, giving3^(2h+1). Terms using a positive-degree endpoint lose at least one possible word position; a w² or w³ factor also lowers the maximal length. Thus no larger power of r occurs, and (10) follows.

For odd n, compute exactly

\[
w^{-1}U(w)L(w)=(4+7w+2w^2,\ 1+4w+2w^2).
\]

The reversed polynomial is this row times K^r b, without a division by w. To extract w^h, the constant row allows an initial J, while b(0)=e_2 still kills a final J. The maximal word length is2h; the unique leading pattern is J(wR) repeated h times, and its contraction has weight3^(2h). Positive-degree endpoints and higher-degree factors give shorter words. This proves (11), including h=0 directly.

### Positive ULC leading margins

Write A_h for the leading coefficient in (10) or (11). For h≥1,

\[
\frac{A_{h+1}A_{h-1}}{A_h^2}
=\begin{cases}
\dfrac{h(2h+1)}{(h+1)(2h+3)},&n\text{ even},\\
\dfrac{h(2h-1)}{(h+1)(2h+1)},&n\text{ odd}.
\end{cases}
\]

Consequently

\[
hA_h^2-(h+1)A_{h+1}A_{h-1}
=\begin{cases}
\dfrac{2h}{2h+3}A_h^2>0,&n\text{ even},\\
\dfrac{2h}{2h+1}A_h^2>0,&n\text{ odd}.
\end{cases}
\tag{12}
\]

The original margin at k=d_n−h is

\[
(d_n-h)h a_{r,h}^2-
(d_n-h+1)(h+1)a_{r,h+1}a_{r,h-1}.
\]

Its leading term is3 times the positive quantity in (12), at degree4h+3 in r for even n and4h+1 for odd n. Hence it is eventually positive for every fixed h. Again, no common threshold for unbounded h is claimed.

## 7. Exact remaining region and limitations

Together with TURN_2, §§5–6 imply the following precise restriction. If there is an infinite sequence of ULC violations with m→infinity, and j denotes their index in F_m, then their distance

\[
h_m=\min\{j,D_m-j\}
\]

must satisfy h_m→infinity and h_m/m→0. Fixed-distance violations are eventually excluded by §§5–6, and fixed positive-proportion violations are eventually excluded by TURN_2. This reasoning does not exclude the intermediate regime, for example h_m of order sqrt(m), nor does it settle any finite unverified range.

Eventual unimodality is weaker than the exact all-n ULC conjecture and must not be used as a substitute for it. The fixed-tail criterion, marking lemma and bulk variance criterion have explicit hypotheses and do not classify all nonnegative polynomial matrices. The source's recurrence, degree and fixed-coefficient polynomial facts remain credited; the arguments here use elementary coefficient marking, finite matrix expansions and the prior turn's classical saddle method without a historical-priority claim.

**Original unresolved after3/5 author turns.** The remaining goal is a uniform transition-region ULC argument together with all-size control, or a genuine counterexample to the original normalization. Subjective planning completion estimate40%, not a correctness or novelty probability.
