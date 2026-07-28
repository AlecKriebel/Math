# Path and cycle qutrit graph-orbit codes

## Scope and research log

This note has three purposes.

1. It independently audits the all-length complete-graph proof in
   `10_complete_graph_codes.md`.
2. It gives an exact nine-state transfer for every path or cycle syndrome.
3. It proves an all-length endpoint theorem for cycles with constant
   nonzero syndrome.

The theorem proved here concerns a structured family of rank-two
projections in qutrit graph-orbit codes.  It does **not** prove
two-block-positivity for arbitrary rank-two matrices and therefore does
not resolve the Werner-state problem.

- **2026-07-28 14:25 PDT.** Re-derived the 27-character complete-graph
  formula from the two character projectors and reconstructed every
  one-, two-, and three-value case.
- **2026-07-28 14:43 PDT.** Derived the inhomogeneous nine-state path and
  cycle transfers over \(\mathbb Z[\omega]\).
- **2026-07-28 14:51 PDT.** Exact scans found no negative path syndrome
  through length \(10\) and no negative cycle syndrome through length
  \(8\).  These scans are discovery data only.
- **2026-07-28 15:05 PDT.** For the constant cycle word, computed four
  degree-five characteristic polynomials exactly and isolated their
  roots by elementary inequalities.
- **2026-07-28 15:12 PDT.** Completed the all-length sign proof and
  replayed the independent standard-library verifier.

## 1. Endpoint integers and the logical-plane reduction

All vectors and graph adjacencies in this note are over
\(\mathbb F_3\).  Let \(A\) be a symmetric zero-diagonal graph adjacency,
let \(s\ne0\), and let
\[
 |k\rangle_L=Z^{ks}|G_A\rangle,\qquad k\in\mathbb F_3.
\]
For \(a,b\in\mathbb F_3\), define
\[
 K_{a,b}(A,s)=
 \sum_{\substack{t\in\mathbb F_3^n\\s\cdot t=-b}}
 (-1)^{n-w_a(t)}2^{w_a(t)},                                  \tag{1}
\]
where
\[
 w_a(t)=
 \left|\left\{i:(t_i,(At)_i+a s_i)\ne(0,0)\right\}\right|.    \tag{2}
\]
The logical-Weyl calculation proved in
`agent_qutrit_graph_codes.md` gives
\[
 \min_P Q_n(P)=
 \frac{2K_{0,0}+
 \min\{K_{1,0},K_{0,1},K_{1,1},K_{1,2}\}}
 {3^n2^{n-1}},                                                \tag{3}
\]
where \(P\) ranges over the rank-two projections in the logical
three-space.  Each of the four fixed-line numerators
\[
 \Delta_{a,b}=2K_{0,0}+K_{a,b},
 \quad (a,b)\in\{(1,0),(0,1),(1,1),(1,2)\},                  \tag{4}
\]
is attained by taking the omitted logical vector to be an eigenvector of
the corresponding logical Weyl.

Thus it is enough, within any graph-orbit family, to prove the four
integer inequalities \(\Delta_{a,b}\ge0\).

## 2. Independent audit of the complete-graph proof

For the complete graph,
\[
 (At)_i=q-t_i,\qquad q=\sum_i t_i.                            \tag{5}
\]
Insert the two exact character projectors
\[
 \mathbf 1_{\sum_i t_i=q}
 =\frac13\sum_{\chi\in\mathbb F_3}
   \omega^{\chi(\sum_i t_i-q)},\qquad
 \mathbf 1_{s\cdot t=-b}
 =\frac13\sum_{\psi\in\mathbb F_3}
   \omega^{\psi(s\cdot t+b)}.                                \tag{6}
\]
At a site with \(s_i=r\), the local Fourier index is
\(\chi+\psi r\).  The local signed sum is
\[
 f_{q,a,r}(h)=
 \begin{cases}
 3,&q+ar=0,\ h=0,\\
 -3,&q+ar=0,\ h\ne0,\\
 6,&q+ar\ne0,\ h=0,\\
 0,&q+ar\ne0,\ h\ne0.
 \end{cases}                                                  \tag{7}
\]
Indeed, when \(q+ar=0\), the \(t_i=0\) term has signed weight
\(-1\), while the other two terms have weight \(2\).  Otherwise all
three terms have weight \(2\).  Therefore, if
\(n_r=|\{i:s_i=r\}|\),
\[
 9K_{a,b}=
 \sum_{q,\chi,\psi\in\mathbb F_3}
 \omega^{-\chi q+\psi b}
 \prod_{r:n_r>0}
 f_{q,a,r}(\chi+\psi r)^{n_r}.                               \tag{8}
\]
This independently reproduces equation (9) of the complete-graph note,
including both Fourier signs.

I expanded all 27 terms of (8), grouped conjugate terms, and checked the
three syndrome strata independently:

- If \(s\) uses one value, nonzeroness forces that value to be \(1\) or
  \(2\).  After exchanging \(1\) and \(2\), the formulas are
  \[
  \begin{aligned}
  K_{0,0}&=3^{n-1}(1+2(-1)^n),\\
  K_{1,0}=K_{0,1}=K_{1,2}&=3^{n-1}2^n,\\
  K_{1,1}&=3^{n-1}(1-(-1)^n).
  \end{aligned}                                               \tag{9}
  \]
  Hence the minimum numerator is zero for odd \(n\) and is strictly
  positive for even \(n\).

- If \(s\) uses two values with positive multiplicities \(x,y\), the
  potentially negative remainder in \(K_{0,0}\) has total absolute
  coefficient \(9\), and the corresponding remainder for \(K_{0,1}\)
  has total absolute coefficient \(6\).  Every \(a=1\) expression is
  either termwise nonnegative or is bounded below by
  \[
  6^{x+y}-3^x6^y-6^x3^y
  =6^{x+y}(1-2^{-x}-2^{-y})\ge0.                             \tag{10}
  \]
  The last inequality follows because \(x,y\ge1\).

- If all three values occur, the \(a=1\) expressions reduce exactly to
  \[
  9K_{1,b}=
  3^{n_0}6^{n_1+n_2}
  +6^{n_0}3^{n_1}6^{n_2}
  +6^{n_0+n_1}3^{n_2}>0,                                    \tag{11}
  \]
  and the remainder bounds for \(K_{0,0}\) and \(K_{0,1}\) are again
  \(9\) and \(6\).

The small exceptional length in the two-value case is \(n=2\), for
which direct substitution in (8) gives \(K_{0,0}=9\); the other bounds
already apply.  Thus the strata are exhaustive and the inequalities are
valid at every length.  I found no algebraic or logical gap in the
complete-graph proof.  Its numerical scan is genuinely unnecessary for
the theorem.

## 3. A nine-state transfer for every path and cycle

Put
\[
 \eta(u,v)=
 \begin{cases}
 -1,&(u,v)=(0,0),\\
 2,&(u,v)\ne(0,0).
 \end{cases}                                                  \tag{12}
\]
Index a \(9\times9\) matrix by ordered pairs in
\(\mathbb F_3^2\).  For \(r,a,\psi\in\mathbb F_3\), define
\[
 \boxed{
 (M_r^{a,\psi})_{(x,y),(y',z)}
 =\mathbf1_{y=y'}\,
 \eta(y,x+z+ar)\,\omega^{\psi r y}.}                         \tag{13}
\]
There are only 27 nonzero entries.

### Lemma 3.1 (path and cycle formulas)

Let \(s=(s_1,\ldots,s_n)\).

For the path \(P_n\), let
\[
 \ell_{(x,y)}=\mathbf1_{x=0},\qquad
 r_{(x,y)}=\mathbf1_{y=0}.
 \]
Then
\[
 \boxed{
 K_{a,b}(P_n,s)=
 \frac13\sum_{\psi\in\mathbb F_3}\omega^{\psi b}
 \ell^\mathsf T
 M_{s_1}^{a,\psi}\cdots M_{s_n}^{a,\psi}r.}                  \tag{14}
\]

For the cycle \(C_n\), \(n\ge3\),
\[
 \boxed{
 K_{a,b}(C_n,s)=
 \frac13\sum_{\psi\in\mathbb F_3}\omega^{\psi b}
 \operatorname {Tr}
 \left(M_{s_1}^{a,\psi}\cdots M_{s_n}^{a,\psi}\right).}       \tag{15}
\]

#### Proof

Write the path boundary values as \(t_0=t_{n+1}=0\).  At site \(i\),
\[
 (At)_i=t_{i-1}+t_{i+1}.
\]
Consequently its signed weight in (1) is
\[
 \eta(t_i,t_{i-1}+t_{i+1}+a s_i).                            \tag{16}
\]
Insert
\[
 \mathbf1_{s\cdot t=-b}
 =\frac13\sum_{\psi\in\mathbb F_3}
 \omega^{\psi(b+\sum_i s_it_i)}.                             \tag{17}
\]
The transition
\[
 (t_{i-1},t_i)\longrightarrow(t_i,t_{i+1})
\]
then has precisely the weight (13).  Summing the initial state with
\(t_0=0\) and the final state with \(t_{n+1}=0\) gives (14).

For a cycle, the same transition states close up.  Summing all closed
state walks is the trace of the transfer product, proving (15).
\(\square\)

Equations (14)--(15) are exact over the Eisenstein integers
\(\mathbb Z[\omega]\), and the final character sum is an ordinary
integer.  The state space does not grow with \(n\).  The matrices for
different syndrome symbols do not commute, however, so an arbitrary
syndrome is a noncommutative word problem rather than a single-matrix
spectral problem.

## 4. Constant-syndrome cycles: exact characteristic polynomials

We now take
\[
 A=A(C_n),\qquad s=(1,\ldots,1).                             \tag{18}
\]
Write
\[
 M_{a,\psi}=M_1^{a,\psi},\qquad
 Z_{a,\psi}(n)=\operatorname {Tr}(M_{a,\psi}^n).              \tag{19}
\]
Then
\[
 K_{a,b}=\frac13\sum_{\psi=0}^2
 \omega^{\psi b}Z_{a,\psi}(n).                              \tag{20}
\]

### Lemma 4.1 (the four spectral polynomials)

For the six relevant transfers,
\[
 \det(\lambda I-M_{a,\psi})=\lambda^4p_{a,\psi}(\lambda),    \tag{21}
\]
where
\[
 \begin{aligned}
 p_{0,0}(\lambda)
 &=\lambda^5-3\lambda^4-12\lambda^3+36\lambda+108\\
 &=(\lambda^2-6)
   (\lambda^3-3\lambda^2-6\lambda-18),                       \tag{22}\\
 p_{0,1}(\lambda)=p_{0,2}(\lambda)
 &=\lambda^5+3\lambda^4+6\lambda^3
   +36\lambda^2+36\lambda+108,                              \tag{23}\\
 p_{1,0}(\lambda)
 &=\lambda^5-6\lambda^4+6\lambda^3
   -18\lambda^2+36\lambda+108,                              \tag{24}\\
 p_{1,1}(\lambda)
 &=\lambda^5+6\omega\lambda^3
   -18(1+\omega)\lambda^2+36\lambda+108,                    \tag{25}\\
 p_{1,2}(\lambda)&=\overline{p_{1,1}(\overline\lambda)}.
                                                                    \tag{26}
 \end{aligned}
\]

#### Proof

Order the states as
\[
 (0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2).
\]
Substitution in (13) gives each sparse \(9\times9\) matrix.  Exact
fraction-free expansion of \(\det(\lambda I-M_{a,\psi})\) gives
(21)--(26).  This is a finite polynomial identity, not a floating-point
eigenvalue computation.

For an independent replay, `verify_path_cycle_graph_codes.py` constructs
the matrices directly from (13), computes the nine power traces, and
uses the Newton identities
\[
 kc_k+\sum_{j=1}^k c_{k-j}\operatorname {Tr}(M^j)=0           \tag{27}
\]
to recover every characteristic coefficient.  It checks exact
divisibility by \(k\) in \(\mathbb Z[\omega]\) and obtains the five
displayed coefficients followed by four exact zeros.  This proves the
listed determinant identities. \(\square\)

Complex conjugation gives
\[
 Z_{0,2}=Z_{0,1}\in\mathbb Z,\qquad
 Z_{1,2}=\overline{Z_{1,1}}.                                 \tag{28}
\]
Therefore the fixed-line numerators are
\[
 \boxed{\Delta_{0,1}=Z_{0,0}+Z_{0,1},}                       \tag{29}
\]
and, for \(b=0,1,2\),
\[
 \boxed{
 \Delta_{1,b}
 =\frac23Z_{0,0}+\frac43Z_{0,1}+\frac13Z_{1,0}
  +\frac23\operatorname {Re}(\omega^bZ_{1,1}).}              \tag{30}
\]

## 5. Exact root bounds

The following elementary bounds are deliberately looser than the true
root moduli.  Their advantage is that each has a short exact
certificate.

### Lemma 5.1

The roots contributing to (22)--(25) have the following properties.

1. \(p_{0,0}\) has a positive root
   \(\beta\in(49/10,5)\).  Its other four roots have modulus \(<5/2\).
2. Every root of \(p_{0,1}\) has modulus \(<4\).
3. \(p_{1,0}\) has a positive root
   \(\alpha\in(5,51/10)\).  Its other four roots have modulus \(<4\).
4. Every root of \(p_{1,1}\) has modulus \(<4\).

#### Proof

For the first assertion, put
\[
 c(x)=x^3-3x^2-6x-18.
\]
Exact substitution gives
\[
 c(49/10)=-1781/1000<0,\qquad c(5)=2>0.                     \tag{31}
\]
The two critical points are \(1\pm\sqrt3\), and
\[
 c(1\pm\sqrt3)=-26\mp6\sqrt3<0.                             \tag{32}
\]
Thus \(c\) has exactly one real root \(\beta\), and it lies in the
interval in (31).  Its other two roots are a conjugate pair.  Their
squared modulus is \(18/\beta<180/49<4\), because the product of the
three cubic roots is \(18\).  The remaining roots of \(p_{0,0}\) are
\(\pm\sqrt6\), whose modulus is \(<5/2\).

For \(p_{0,1}\), suppose that \(z=re^{i\theta}\) is a root with
\(r\ge4\), and put \(u=\cos\theta\).  The root equation can be written
\[
 z^3(z^2+3z+6)=-36(z^2+z+3).                                \tag{33}
\]
After taking squared moduli and moving the right side to the left, the
result is
\[
 D(r,u)=A(r)u^2+B(r)u+C(r)=0,                                \tag{34}
\]
where
\[
 \begin{aligned}
 A(r)&=24r^2(r^6-648),\\
 B(r)&=6r(r^8+6r^6-432r^2-1296),\\
 C(r)&=r^{10}-3r^8+36r^6-1296r^4+6480r^2-11664.
 \end{aligned}                                               \tag{35}
\]
Here \(A(r)>0\).  Direct expansion gives the exact discriminant
certificate
\[
 4A(r)C(r)-B(r)^2=12r^2g(r^2),                               \tag{36}
\]
and, on writing \(v=r^2-16\ge0\),
\[
 \begin{aligned}
 g(16+v)={}&5v^8+580v^7+29300v^6+828640v^5\\
 &+14081120v^4+143116480v^3+808017152v^2\\
 &+2044037632v+829776128>0.                                 \tag{37}
 \end{aligned}
\]
Thus the quadratic in (34) has positive leading coefficient and
negative discriminant, so it is positive for every real \(u\), a
contradiction.

For \(p_{1,0}\), exact substitution gives
\[
 p_{1,0}(5)=-37<0,\qquad
 p_{1,0}(51/10)=1045791/100000>0.                            \tag{38}
\]
Choose a real root \(\alpha\) in this interval.  Synthetic division
gives
\[
 \begin{aligned}
 \frac{p_{1,0}(z)}{z-\alpha}
 ={}&z^4+(\alpha-6)z^3+(\alpha^2-6\alpha+6)z^2\\
 &+(\alpha^3-6\alpha^2+6\alpha-18)z-\frac{108}{\alpha}.
                                                                    \tag{39}
 \end{aligned}
\]
On \(5<\alpha<51/10\), the absolute values of the four nonleading
coefficients in (39) are bounded respectively by
\[
 1,\qquad \frac32,\qquad 13,\qquad \frac{108}{5}.             \tag{40}
\]
For completeness, the quadratic coefficient increases from \(1\) to
\(141/100\), while the linear coefficient increases from \(-13\) to
\(-10809/1000\); their derivatives are positive throughout the stated
interval.  The first and last bounds are immediate from
\(5<\alpha<51/10\).
If (39) vanished at \(|z|=r\ge4\), the triangle inequality would give
\[
 r^4<
 r^3+\frac32r^2+13r+\frac{108}{5}.
 \]
After division by \(r^4\), the right-hand ratio is decreasing in \(r\)
and at \(r=4\) is
\[
 \frac14+\frac{3}{32}+\frac{13}{64}+\frac{108}{1280}<1,       \tag{41}
\]
a contradiction.  Hence the quotient's four roots lie in \(|z|<4\).

Finally, if \(p_{1,1}(z)=0\) and \(|z|=r\ge4\), then
\[
 r^5\le6r^3+18r^2+36r+108.
 \]
The ratio of the right side to \(r^5\) decreases with \(r\), while at
\(r=4\)
\[
 6\cdot4^3+18\cdot4^2+36\cdot4+108=924<1024=4^5.             \tag{42}
\]
This contradiction proves the fourth assertion. \(\square\)

## 6. An all-length theorem for constant cycle syndromes

### Theorem 6.1

Let \(C_n\) be the simple qutrit cycle graph, \(n\ge3\), and let
\[
 s=(r,\ldots,r),\qquad r\in\{1,2\}.
\]
Every rank-two projection \(P\) in the graph-orbit code
\[
 \operatorname {span}\{
 |G_{C_n}\rangle,Z^s|G_{C_n}\rangle,Z^{2s}|G_{C_n}\rangle\}
\]
satisfies
\[
 \boxed{Q_n(P)\ge0.}                                        \tag{43}
\]
For \(r=1\), equality occurs at \(n=3\) when the omitted logical vector
is an eigenvector of the logical Weyl \(W_{1,1}\).  For every
\(n\ge4\), the inequality is strict.  Multiplying the syndrome by two
only relabels the four logical Weyl lines.

#### Proof

The four zero eigenvalues in (21) do not contribute to a positive power
trace.  Let the five roots of each \(p_{a,\psi}\) be counted with
multiplicity.  Lemma 5.1 and the triangle inequality give
\[
 \begin{aligned}
 Z_{0,0}(n)&>\beta^n-4(5/2)^n,\\
 Z_{0,1}(n)&>-5\cdot4^n,\\
 Z_{1,0}(n)&>5^n-4\cdot4^n,\\
 |\operatorname {Re}(\omega^bZ_{1,1}(n))|&<5\cdot4^n.
 \end{aligned}                                               \tag{44}
\]

First use (29) and \(\beta>49/10\):
\[
 \Delta_{0,1}>
 (49/10)^n-4(5/2)^n-5\cdot4^n.                              \tag{45}
\]
At \(n=9\), the right side is exactly
\[
 \frac{302434808847949}{10^9}>0.                             \tag{46}
\]
After division by \((49/10)^n\), the two subtracted terms are
\[
 4(25/49)^n+5(40/49)^n,
\]
which decrease with \(n\).  Hence \(\Delta_{0,1}>0\) for every
\(n\ge9\).

For the other three lines, substitute (44) in (30) and discard the
positive term \((2/3)\beta^n\):
\[
 \Delta_{1,b}>
 \frac13\,5^n-\frac83(5/2)^n-\frac{34}{3}4^n.                \tag{47}
\]
The right side is positive precisely when the sufficient inequality
\[
 \frac8{2^n}+34(4/5)^n<1                                    \tag{48}
\]
holds.  At \(n=16\), one minus the left side is exactly
\[
 \frac{53578761089087}{1250000000000000}>0.                 \tag{49}
\]
Both terms on the left of (48) decrease with \(n\), so all three
\(\Delta_{1,b}\) are positive for every \(n\ge16\).

It remains only to check the finite base interval.  Exact transfer
multiplication gives:
\[
\begin{array}{c|r|r|r|r}
n&\Delta_{0,1}&\Delta_{1,0}&\Delta_{1,1}&\Delta_{1,2}\\ \hline
3&54&54&0&54\\
4&882&882&1098&1026\\
5&2430&2430&2430&2430\\
6&18738&19602&20034&22302\\
7&60102&60102&64638&60102\\
8&396738&443394&427842&440802\\
9&1614006&1683990&1736478&1736478\\
10&9464850&10689570&10596258&10417410\\
11&41329926&45499806&45243198&45756414\\
12&223985250&252935298&255023154&252468738\\
13&1031078646&1169139582&1160951454&1162771038\\
14&5394974706&6202555074&6220191042&6228449154\\
15&25611873894&29678381694&29678381694&29603428830
\end{array}                                                   \tag{50}
\]
Every entry is an integer obtained from (19), (29), and (30); the
verifier independently reconstructs the table.  Equations
(45)--(49) cover the remaining lengths.  Thus all four fixed-line
numerators are nonnegative.  Equation (3) proves (43), and (50) proves
the equality and strictness statements. \(\square\)

## 7. Verification and unresolved directions

Run
```
python3 discovery/verify_path_cycle_graph_codes.py
```
from the project directory.  The verifier uses only Python's standard
library and exact integer/rational arithmetic.  It:

1. compares the transfer with the definition-level \(3^n\)-term sum
   through \(n=6\);
2. constructs all six \(9\times9\) transfers from (13);
3. computes their characteristic polynomials over
   \(\mathbb Z[\omega]\) by Newton identities;
4. reproduces every entry of (50);
5. checks the rational endpoint isolations, the shifted polynomial
   certificate (37), and the two eventual-positivity thresholds.

The discovery layer also evaluated every nonzero path syndrome through
\(n=10\) and every nonzero cycle syndrome through \(n=8\), exactly, with
no negative \(\Delta_{a,b}\).  Periodic cycle words of periods at most
five were tested through total length \(40\), again without a negative
value.  None of these finite observations is used in Theorem 6.1.

What remains unresolved inside this ansatz is substantial:

- arbitrary path syndromes at unbounded length;
- arbitrary cycle syndromes at unbounded length;
- even the constant-syndrome path at unbounded length;
- rank-two planes outside qutrit graph-orbit codes.

The main obstruction exposed by the transfer is noncommutativity.
For a constant word, one controls powers of four fixed matrices.  For an
arbitrary syndrome, one must control all products generated by three
signed complex matrices, and the individual matrices have neither
entrywise positivity nor a common evident invariant cone.

Several tempting shortcuts fail:

- Bounding each \(K_{a,b}\) below by zero is impossible:
  \(K_{0,0}\) is negative in genuine equality cases.
- Bounding each negative local factor independently destroys the
  cancellations that make (29)--(30) positive.
- A finite syndrome scan cannot imply a uniform word-product theorem.
- Diagonalizing each transfer separately gives no control over switching
  between the three noncommuting syndrome matrices.

The exact transfer (13) is therefore the useful structural output for
the remaining path/cycle problem, while Theorem 6.1 is the all-copy
conclusion currently justified by it.
