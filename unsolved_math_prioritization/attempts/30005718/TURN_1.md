# Turn 1: all-size boundary certificates for the matrix-recursion problem

**Target:** 30005718 / OWR-14298007-013. **Date:** 2026-10-02.  
**Substantive author count:** 1/5. **Status:** partial; the original ultra-log-concavity question remains unresolved.

## 1. Exact question and normalization

The source is Germain Poullot's Problem6 in [OWR58/2023, pp.3308–3309](https://ems.press/content/serial-article-files/48169). Its concrete recursion is

\[
\begin{pmatrix}T_{n+1}\\Q_{n+1}\\C_{n+1}\end{pmatrix}
=\begin{pmatrix}z&1+z&1+z\\0&1+z&z\\z+z^2&0&1+z\end{pmatrix}
\begin{pmatrix}T_n\\Q_n\\C_n\end{pmatrix},
\quad
(T_4,Q_4,C_4)=(z^4+2z^3,z^4,2z^4+2z^3).
\]

Write V_n=T_n+Q_n+C_n=∑_k v_{n,k}z^k and d_n=deg V_n=floor(3(n−1)/2). The ULC convention used here is the one matching degree-d_n homogeneous Lorentzian polynomials: the sequence v_{n,k}/binom(d_n,k), for 0≤k≤d_n, is log-concave and has no internal zeros. Equivalently,

\[
\Delta_{n,k}:=k(d_n-k)v_{n,k}^2
-(k+1)(d_n-k+1)v_{n,k-1}v_{n,k+1}\ge0,
\qquad 1\le k<d_n.
\tag{1}
\]

Leading zeros are retained. Dividing V_n by z^3 changes the ULC normalization, so ULC of the divided polynomial is not silently substituted for (1).

**Results of this turn:** (1) is proved for k=4 whenever this is an interior index, and for k=d_n−1 for every n≥4. The endpoint k=3 and lower indices are automatic because v_{n,k}=0 for k<3. Explicit formulas for the top three coefficients are given below. A general unipotent-leading-matrix lemma yields a finite certificate method for any fixed tail band of a polynomial-matrix recursion. No proof of the remaining interior inequalities is claimed.

## 2. A positive two-state reduction

For every n≥4,

\[
D_n:=T_n-Q_n=\frac{C_n}{1+z}.
\tag{2}
\]

This holds initially. If it holds at n, then

\[
T_{n+1}-Q_{n+1}=zT_n+C_n=zQ_n+(1+2z)D_n,
\]

and C_{n+1}=(1+z)(zT_n+C_n), proving the induction. Consequently

\[
\begin{pmatrix}D_{n+1}\\Q_{n+1}\end{pmatrix}
=N(z)\begin{pmatrix}D_n\\Q_n\end{pmatrix},
\quad N(z)=\begin{pmatrix}1+2z&z\\z+z^2&1+z\end{pmatrix},
\quad (D_4,Q_4)=(2z^3,z^4),
\tag{3}
\]

and V_n=(2+z)D_n+2Q_n. This reduction is a direct use of the rank-two structure behind the source's eigenvalue calculation, not a claimed new diagonalization result.

The coefficient supports in (3) are intervals: D_n has positive coefficients on [3,a_n], and Q_n on [4,b_n]. Initially (a_4,b_4)=(3,4). Multiplication in (3) gives

\[
a_{n+1}=\max(a_n+1,b_n+1),\quad
b_{n+1}=\max(a_n+2,b_n+1).
\]

The intervals overlap or touch, so no internal zero is created. Thus b_n=a_n+1 at even n and b_n=a_n at odd n; V_n is positive exactly on [3,a_n+1]. This recovers the source's degree d_n and supplies the no-internal-zero condition.

## 3. The lower-end inequality

Let m=n−4 and strip the common z^3 only for coefficient calculation. Put d_m=D_n/z^3 and q_m=Q_n/z^3. Their first coefficients from (3) are

\[
[z^0]d_m=2,\quad [z^1]d_m=4m,\quad
[z^2]d_m=5m^2-4m,
\]
\[
[z^0]q_m=0,\quad[z^1]q_m=2m+1,\quad
[z^2]q_m=3m^2.
\]

These identities follow by comparing coefficients in (3), starting from d_0=2,q_0=z. For example, [z²]d_{m+1}−[z²]d_m=10m+1, and [z²]q_{m+1}−[z²]q_m=6m+3. Hence

\[
v_{n,3}=4,\quad v_{n,4}=12n-44,
\quad v_{n,5}=4(n-4)(4n-17).
\tag{4}
\]

These low-coefficient formulas agree with the credited formulas in Poullot's later paper; the ULC certificates obtained from them are what is needed here.

For n=2r+4, d_n=3r+4, direct substitution in (1) gives

\[
\Delta_{n,4}=32r(96r^2+47r+11)\ge0.
\tag{5}
\]

For n=2r+5, d_n=3r+6,

\[
\Delta_{n,4}=16(192r^3+414r^2+321r+83)>0.
\tag{6}
\]

Here r≥0. At n=4 the index4 is not interior, so (5) is only a consistent endpoint identity. For every n≥5 it proves the first inequality involving three nonzero adjacent coefficients.

## 4. A fixed-tail certificate lemma

**Lemma.** Let K(w) be a polynomial matrix with constant coefficient K(0)=I+J, where J^h=0. In the quotient ring modulo w^(q+1),

\[
(K-I)^{h(q+1)}=0,
\quad
K(w)^r=\sum_{\ell=0}^{h(q+1)-1}\binom r\ell(K(w)-I)^\ell
\pmod{w^{q+1}}
\tag{7}
\]

for every integer r≥0. Therefore every coefficient of w^j, j≤q, in K(w)^r is a polynomial in r of degree at most h(q+1)−1.

**Proof.** Write K−I=J+wR(w). Expand a product of h(q+1) factors noncommutatively. A nonzero term modulo w^(q+1) uses at most q factors from wR(w). These split the remaining J factors into at most q+1 consecutive blocks. If each block had length at most h−1, the word would have length at most (q+1)(h−1)+q=h(q+1)−1, a contradiction. Thus some block contains J^h, and the term is zero. The ordinary binomial identity applies to I+(K−I), since I commutes with every matrix, yielding (7). ∎

**Matrix-recursion criterion.** For a recursion A(z)^r with degree s and unipotent leading matrix, set K(w)=w^s A(1/w). After accounting for fixed initial and output polynomial vectors and their reversal shifts, any prescribed finite number of highest coefficients can be obtained by a finite binomial expansion (7). ULC, ordinary log-concavity, or endpoint monotonicity inequalities in that band become polynomial inequalities in r. A polynomial expansion with nonnegative coefficients in r (or in r−r_0 after a finite initial check) is a sufficient, fully finite certificate for all r in the indicated range.

This is a tool for a **fixed tail band** under an explicit leading-matrix hypothesis. It does not prove the entire coefficient row ULC or unimodal and does not apply to every nonnegative polynomial matrix without checking the hypothesis.

## 5. Applying the lemma to the highest coefficients

Write N(z)=I+zA+z²B, with

\[
A=\begin{pmatrix}2&1\\1&1\end{pmatrix},\qquad
B=\begin{pmatrix}0&0\\1&0\end{pmatrix}.
\]

Since B²=0,

\[
K(w):=w^3N(1/w)^2
=P+wR+w^2S+w^3I,
\]
\[
P=AB+BA=\begin{pmatrix}1&0\\3&1\end{pmatrix},\quad
R=A^2+2B=\begin{pmatrix}5&3\\5&2\end{pmatrix},\quad
S=2A=\begin{pmatrix}4&2\\2&2\end{pmatrix}.
\tag{8}
\]

The leading matrix P=I+J has J²=0. Let

\[
U(w)=(1+2w,2w),\qquad b(w)=(2w,1)^T,
\qquad L(w)=B+wA+w^2I.
\]

Reversing the scalar output V_n/z³ in (3) gives

\[
w^{d_n}V_n(1/w)
=\begin{cases}
w^{-1}U(w)K(w)^r b(w),&n=2r+4,\\
w^{-1}U(w)L(w)K(w)^r b(w),&n=2r+5.
\end{cases}
\tag{9}
\]

The numerator's constant coefficient is zero in both cases, so no negative power actually occurs. For the top three coefficients only terms through w³ in that numerator matter. By (7), it is enough to use the exact identity

\[
K(w)^r=\sum_{\ell=0}^{7}\binom r\ell(K(w)-I)^\ell\pmod{w^4}.
\tag{10}
\]

Multiplying the explicit 2×2 matrices in (8)–(10) gives the following formulas. This is an exact finite polynomial identity in r, not interpolation from sample values.

For **n=2r+4**, put d=3r+4. Then

\[
a:=v_{n,d}=3r+4,
\]
\[
b:=v_{n,d-1}=\frac{(r+1)(9r^2+21r+8)}2,
\]
\[
c:=v_{n,d-2}=\frac{r(3r+2)(27r^3+102r^2+177r+142)}{40}.
\tag{11}
\]

For **n=2r+5**, put d=3r+6. Then

\[
a=1,\qquad b=\frac{9r^2+31r+24}{2},
\qquad c=\frac{(r+1)(r+2)(27r^2+81r+64)}8.
\tag{12}
\]

The leading coefficients in (11)–(12) recover Poullot's Theorem5.6. The next two formulas supply the needed adjacent ULC comparison.

For even n, substituting (11) yields

\[
\begin{aligned}
20\Delta_{n,d-1}={}&486r^7+4131r^6+12879r^5+19170r^4\\
&+15039r^3+7479r^2+3376r+960.
\end{aligned}
\tag{13}
\]

For odd n, (12) gives

\[
4\Delta_{n,d-1}
=162r^5+1431r^4+4914r^3+8201r^2+6660r+2112.
\tag{14}
\]

All coefficients in (13)–(14) are positive. Thus the last interior ULC inequality holds strictly for every n≥4. At n=4 it includes a zero coefficient below the support and is already automatic; the same formula remains valid.

## 6. Why this does not yet prove the full claim

The missing inequalities are

\[
\Delta_{n,k}\ge0\quad\text{for }5\le k\le d_n-2,
\tag{15}
\]

for all n. The interval in (15) grows with n, so fixed-tail certification cannot by itself complete the proof. Ordinary log-concavity or unimodality in that entire interval has also not been established here.

There is a concrete obstruction to treating (3) as an unrestricted ULC-preserving map on its components. Both inputs D=1 and Q=100z are ULC, while their first output is 1+2z+100z², which is not even log-concave. Moreover, along the actual orbit, D_6/z³=2+8z+12z²+5z³ fails degree-three ULC: 2·8²<6·2·12. Thus dividing by a convenient monomial and asserting preservation would be invalid. A successful induction must retain the actual degree normalization and use stronger coupled invariants, or employ a different all-interior argument.

The source's qualitative request for tools for general matrix recursions is partially addressed by §4, under stated hypotheses. It is not a universal classification of ULC-preserving matrices.

## 7. Exact controls and attribution

`python3 checks/verify_turn1.py` uses only the Python standard library. It verifies (10) and (11)–(14) symbolically with rational polynomial arithmetic; it also compares the two-state identities, boundary formulas, and all four source polynomials against the unreduced original recursion through n=500. Every ULC test uses each polynomial's actual degree. These bounded tests do not prove (15).

The source's degree and leading coefficient formulas, its matrix recursion, and low coefficient formulas are credited to Poullot. The current primary paper [arXiv:2411.14102v3](https://arxiv.org/abs/2411.14102v3), Proposition5.4, Theorems5.6–5.7 and Conjecture6.2, and [Juhnke–Poullot arXiv:2504.20739v3](https://arxiv.org/abs/2504.20739v3), Example3.8/Problem3.9, confirm the exact recurrence and leave its full log-concavity/unimodality open. Counterexamples in the latter paper concern other polytopes. No historical novelty claim is made for this partial result or for the elementary truncated-matrix technique.

**Completion estimate:** approximately15%, a subjective planning estimate. **Sharp original-scope gap:** prove or refute (15) uniformly in n, while preserving the binomial degree normalization. The target remains unsolved after substantive turn1 of5.
