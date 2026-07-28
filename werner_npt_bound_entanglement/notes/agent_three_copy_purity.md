# The three-copy rank-two projection inequality

## Scope and status

Let
\[
P=|u\rangle\langle u|+|v\rangle\langle v|
\]
be a rank-two orthogonal projection on
\(\mathcal H=A\otimes B\otimes C\), where \(u,v\) are orthonormal.
This note studies the exact endpoint inequality
\[
Q_3(P)\geq0.
\tag{1}
\]
If \(\rho=P/2\), direct expansion of the endpoint partial-trace form gives
\[
Q_3(P)
=\frac32-
\left(
2\sum_{i<j}\operatorname{Tr}\rho_{ij}^2
-\sum_i\operatorname{Tr}\rho_i^2
\right).
\tag{1a}
\]
Thus (1) is exactly the purity inequality
\[
2\sum_{i<j}\operatorname{Tr}\rho_{ij}^2
-\sum_i\operatorname{Tr}\rho_i^2\leq\frac32.
\]

The full inequality (1) is **not proved or refuted here**.  Two useful exact
results are established:

1. (1) is reduced to a single sharp crossed-purity inequality, with all
   constants checked.
2. The tempting stronger inequality on a single decomposable replica
   product \(u\otimes v\) is false by a four-term exact certificate.  Its
   failure is exactly compensated by the two diagonal replica products
   \(u\otimes u\) and \(v\otimes v\), giving a zero code projection.

A second exact sparse certificate rules out a natural attempt to prove the
remaining crossed inequality using only the holomorphic concurrence
pairing \(\sum_i\operatorname{Tr}S_i^2\).

All arguments below are dimension-independent unless a qutrit basis is
explicitly used in a certificate.

## 1. Swap sectors

On two replicas of \(\mathcal H\), let \(F_i\) swap the two copies of the
\(i\)-th physical factor and put
\[
\Pi_R=
\prod_{i\in R}\frac{I-F_i}{2}
\prod_{i\notin R}\frac{I+F_i}{2},
\qquad R\subseteq\{A,B,C\}.
\tag{2}
\]
For a vector \(w\) and an orthogonal pair \(u,v\), define
\[
a_R(w)=\|\Pi_R(w\otimes w)\|^2,\qquad
c_R(u,v)=\|\Pi_R(u\otimes v)\|^2.
\tag{3}
\]
Since \(w\otimes w\) is symmetric under the global swap,
\[
a_R(w)=0\quad\text{if }|R|\text{ is odd}.
\tag{4}
\]

The sector weight of \(P\) is
\[
\begin{aligned}
p_R(P)
&=\operatorname{Tr}[(P\otimes P)\Pi_R]\\
&=a_R(u)+a_R(v)+c_R(u,v)+c_R(v,u).
\end{aligned}
\]
On the range of \(\Pi_R\), the global swap has eigenvalue
\((-1)^{|R|}\), and hence
\[
\Pi_R(v\otimes u)=(-1)^{|R|}F_{ABC}\Pi_R(u\otimes v).
\]
In particular the last two terms have equal norms, so
\[
\boxed{\quad
p_R(P)=a_R(u)+a_R(v)+2c_R(u,v).
\quad}
\tag{5}
\]

For three copies, the endpoint sector formula is
\[
\boxed{\quad
Q_3(P)=\sum_{|R|=2}p_R(P)-3p_{ABC}(P).
\quad}
\tag{6}
\]
This follows directly from
\[
Q_3(P)=2^{-3}\sum_R(-3)^{|R|}p_R(P)
\]
and the parity traces
\[
\sum_{|R|\ {\rm even}}p_R(P)=3,\qquad
\sum_{|R|\ {\rm odd}}p_R(P)=1.
\]

## 2. Exact crossed-purity reduction

For a unit vector \(w\), write
\[
\rho_i^w=\operatorname{Tr}_{\bar i}|w\rangle\langle w|,
\qquad
e(w)=3-\sum_{i=A,B,C}\operatorname{Tr}[(\rho_i^w)^2].
\tag{7}
\]
The number \(e(w)\) is nonnegative, being the sum of the three
one-versus-rest linear entropies.

For the orthogonal pair \(u,v\), put
\[
x_i=\operatorname{Tr}(\rho_i^u\rho_i^v),
\qquad
y_i=\operatorname{Tr}(\rho_{\bar i}^u\rho_{\bar i}^v)
     =\left\|\operatorname{Tr}_{\bar i}|u\rangle\langle v|\right\|_2^2.
\tag{8}
\]
The second equality is the elementary swap contraction.

### Proposition 1

For every orthonormal \(u,v\),
\[
\boxed{\quad
4Q_3(P)
=e(u)+e(v)+2\sum_i(x_i-2y_i).
\quad}
\tag{9}
\]
Consequently \(Q_3(P)\geq0\) is exactly equivalent to
\[
\boxed{\quad
\sum_i(2y_i-x_i)\leq\frac{e(u)+e(v)}2.
\quad}
\tag{10}
\]

#### Proof

For a normalized replica product \(r\otimes s\), its sector probabilities
are the Walsh transform of the swap moments
\[
\langle r\otimes s|F_T|r\otimes s\rangle
=\operatorname{Tr}(\rho_T^r\rho_T^s).
\tag{11}
\]
For \(r=s=w\), complementary reductions of the pure state \(w\) have
equal purity.  Summing the three sectors of size two gives
\[
\sum_{|R|=2}a_R(w)
=\frac14\left(3-\sum_i\operatorname{Tr}[(\rho_i^w)^2]\right)
=\frac14e(w).
\tag{12}
\]

For the orthogonal pair \(u,v\), the empty and full swap moments are
respectively \(1\) and \(0\).  The singleton moments are the \(x_i\)'s,
while the two-site moment on \(\bar i\) is \(y_i\).  The Walsh transform
therefore gives
\[
\begin{aligned}
\sum_{|R|=2}c_R(u,v)
  &=\frac18\left(3-\sum_i x_i-\sum_i y_i\right),\\
c_{ABC}(u,v)
  &=\frac18\left(1-\sum_i x_i+\sum_i y_i\right).
\end{aligned}
\tag{13}
\]
Hence
\[
4\left(\sum_{|R|=2}c_R-3c_{ABC}\right)
=\sum_i(x_i-2y_i).
\tag{14}
\]
Substitute (5), (12), and (14) in (6).  This proves (9), and (10) is
just a rearrangement. \(\square\)

The stronger geometric-mean inequality
\[
\sum_i(2y_i-x_i)\leq\sqrt{e(u)e(v)}
\tag{15}
\]
would imply (10) by arithmetic--geometric mean.  It is precisely the
two-by-two determinant/Cauchy form needed for positivity on every positive
rank-two matrix, not only the equal projection.  No proof of (15) is
obtained here.

## 3. Exact refutation of the replica-product sector inequality

A proposed shortcut is
\[
\sum_{|R|=2}c_R(u,v)\stackrel{?}{\geq}3c_{ABC}(u,v)
\tag{16}
\]
for every \(u,v\).  It is false, even for orthogonal real vectors supported
on local qubit subspaces.

Set
\[
\begin{aligned}
u&=\frac{-|000\rangle+|010\rangle+|101\rangle+|111\rangle}{2},\\
v&=\frac{\phantom{-}|000\rangle-|010\rangle+|101\rangle+|111\rangle}{2}.
\end{aligned}
\tag{17}
\]
They are orthonormal.  Direct contraction gives
\[
\langle u\otimes v|F_T|u\otimes v\rangle
=
\begin{cases}
1,&T=\varnothing,\\[2mm]
\frac12,&0<|T|<3,\\[2mm]
0,&T=\{A,B,C\}.
\end{cases}
\tag{18}
\]
The Walsh transform (11) is therefore
\[
c_\varnothing=\frac12,\qquad
c_R=\frac18\quad(|R|\text{ odd}),\qquad
c_R=0\quad(|R|=2).
\tag{19}
\]
In particular,
\[
\boxed{\quad
\sum_{|R|=2}c_R-3c_{ABC}=-\frac38.
\quad}
\tag{20}
\]

Equivalently, with
\[
W_3=\prod_{i=A,B,C}(2F_i-I)+I-2F_{ABC},
\tag{21}
\]
whose sector eigenvalues are \(8\) at level two, \(-24\) at level three,
and zero at levels zero and one,
\[
\langle u\otimes v|W_3|u\otimes v\rangle=-3.
\tag{22}
\]
Thus neither (16) nor positivity of the isolated spectral cross term can
be used.

The actual code projection is not negative.  Indeed, each vector in (17)
has one-site purity \(1/2\) at all three sites, so
\[
e(u)=e(v)=\frac32.
\tag{23}
\]
Equations (13) and (20) give
\[
\sum_{|R|=2}a_R(u)
=\sum_{|R|=2}a_R(v)=\frac38.
\]
Using (5)--(6),
\[
Q_3(P)=\frac38+\frac38+2\left(-\frac38\right)=0.
\tag{24}
\]
This is not an accidental cancellation.  Put
\[
a=|010\rangle-|000\rangle,\qquad
b=|101\rangle+|111\rangle.
\]
Then \(u=(a+b)/2\), \(v=(-a+b)/2\), while \(a/\sqrt2,b/\sqrt2\) are
orthogonal product vectors differing in all three local factors.  Thus
(17) is merely a rotated basis of a known zero code.  The rotation makes
the cross term maximally negative while leaving the projection unchanged.

## 4. A holomorphic concurrence bound and its exact obstruction

Let
\[
S_i=\operatorname{Tr}_{\bar i}|u\rangle\langle v|,
\qquad
Z=\sum_i\operatorname{Tr}(S_i^2).
\tag{25}
\]
There is a short exact Cauchy bound for \(Z\).

### Proposition 2

For every orthonormal \(u,v\),
\[
\boxed{\quad |Z|\leq\sqrt{e(u)e(v)}.\quad}
\tag{26}
\]

#### Proof

Let \(\Pi_i^-=(I-F_i)/2\), acting on two replicas, and define
\[
\mathcal C(w)=\bigoplus_{i=A,B,C}\Pi_i^-(w\otimes w).
\]
Because
\[
\|\Pi_i^-(w\otimes w)\|^2
=\frac12\left(1-\operatorname{Tr}[(\rho_i^w)^2]\right),
\]
one has
\[
\|\mathcal C(w)\|^2=\frac12e(w).
\tag{27}
\]
Orthogonality of \(u,v\) and a direct index contraction give
\[
\left\langle
\Pi_i^-(u\otimes u),\Pi_i^-(v\otimes v)
\right\rangle
=-\frac12\,\overline{\operatorname{Tr}(S_i^2)}.
\tag{28}
\]
Thus
\[
\langle\mathcal C(u),\mathcal C(v)\rangle=-\frac12\overline Z.
\]
Cauchy--Schwarz and (27) prove (26). \(\square\)

It would be enough to supplement (26) with
\[
\sum_i(2y_i-x_i)\leq |Z|.
\tag{29}
\]
That implication is false.  Here is an exact sparse certificate.  Define
\[
\begin{aligned}
u={}&\frac{-|221\rangle+|010\rangle-|200\rangle
{}+|021\rangle+|210\rangle}{\sqrt5},\\
v={}&\frac{i|012\rangle+i|212\rangle-i|202\rangle+|000\rangle}{2}.
\end{aligned}
\tag{30}
\]
Their supports are disjoint, so they are orthonormal.  Direct contraction
gives the following rational table:
\[
\begin{array}{c|ccccc}
i&
\operatorname{Tr}[(\rho_i^u)^2]&
\operatorname{Tr}[(\rho_i^v)^2]&x_i&y_i&
\operatorname{Tr}(S_i^2)\\ \hline
A&13/25&5/8&1/2&1/20&0\\
B&11/25&5/8&2/5&1/20&0\\
C&13/25&5/8&3/20&9/20&0
\end{array}
\tag{31}
\]
Therefore
\[
Z=0,\qquad
\sum_i(2y_i-x_i)=\frac1{20}>0,
\tag{32}
\]
which disproves (29).  The genuine projection inequality remains safely
positive:
\[
e(u)=\frac{38}{25},\qquad e(v)=\frac98,
\]
and Proposition 1 gives
\[
4Q_3(P)
=\frac{38}{25}+\frac98-\frac1{10}
=\frac{509}{200},
\qquad
Q_3(P)=\frac{509}{800}>0.
\tag{33}
\]

Thus the holomorphic concurrence vector controls one coherent polarization
of the crossed term, but not the phase-insensitive marginal overlaps that
make up all of (10).

## 5. A sector-refined sufficient inequality

The exact decomposition above identifies a particularly sharp sufficient
target.  If one could prove
\[
\boxed{\quad
3c_{ABC}(u,v)
\leq
\sum_{|R|=2}c_R(u,v)
+\sum_{|R|=2}\sqrt{a_R(u)a_R(v)},
\quad}
\tag{34}
\]
then (1) would follow immediately.  Indeed, (5)--(6) and
\(a+b\geq2\sqrt{ab}\) would give
\[
\begin{aligned}
Q_3(P)
&=\sum_{|R|=2}
\bigl(a_R(u)+a_R(v)+2c_R(u,v)\bigr)
-6c_{ABC}(u,v)\\
&\geq
2\sum_{|R|=2}
\left(\sqrt{a_R(u)a_R(v)}+c_R(u,v)\right)
-6c_{ABC}(u,v)\geq0.
\end{aligned}
\]
Inequality (34) has not been proved.  It retains the three separate
double-antisymmetric sectors and is strictly more structured than applying
Cauchy--Schwarz only after summing them.

## 6. What is and is not resolved

Established exactly:

- the sector identity (5);
- the exact projection reduction (9)--(10);
- the exact product-sector counterexample (17)--(22);
- exact diagonal compensation and equality of its code projection;
- the holomorphic concurrence estimate (26);
- the exact obstruction (30)--(33) to using that estimate alone.

Not established:

- the sharp crossed inequality (10);
- its stronger determinant form (15);
- the sector-refined sufficient inequality (34);
- a negative rank-two code projection.

Accordingly, this note does not settle the three-copy projection case.  It
does rule out two attractive shortcuts with exact certificates and leaves
the unresolved compensation in the scalar form (10).
