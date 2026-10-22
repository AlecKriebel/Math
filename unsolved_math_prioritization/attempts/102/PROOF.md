# GREEN-012: a certified high-density range and exact special cases

**Status: accepted computer-assisted partial result in an independent internal AI audit; unrefereed. The unrestricted problem is not resolved here. No novelty priority is claimed.**

## 1. Statement and interpretation

Let \(G\) be a finite abelian group of order \(N\), let \(A\subseteq G\), and put
\(\alpha=|A|/N\). Let \(T_G(A)\) count ordered tuples
\((x_0,\ldots,x_4,y_0,\ldots,y_4)\in G^{10}\) satisfying
\(x_i+y_{i+j}\in A\) for every \(i\in\mathbb Z/5\mathbb Z\) and
\(j\in\{0,1,2\}\). Coordinates need not be distinct.

This is the 15-edge reading of Ben Green's Problem 12 in
[100 Open Problems, p. 9](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf).
The modulo-5 convention is **a publicly reported author clarification**: a
[6 February 2026 Lean community discussion](https://leanprover-community.github.io/archive/stream/252551-graph-theory/topic/Sidorenko%27s.20Conjecture.20and.20Green%27s.20Open.20Problem.2012.html)
records Kevin Buzzard reporting Green's confirmation. We do not represent the
inspected PDF as explicitly printing that convention or claim private correspondence.
The Deng–Tidor–Zhao discussion on the same PDF page concerns Problem 13, not this problem.

### Main partial theorem

For every such \(G,A\),

\[
\boxed{\alpha\geq 20/23\quad\Longrightarrow\quad
T_G(A)\geq\alpha^{15}N^{10}.}
\]

A slightly stronger exact threshold follows from the proof. Define

\[
F(r)=\frac{160r^2+180r^{5/2}+121r^3}{\sqrt{1+r}}
       -\frac{10r^2+5r^3}{1+r}.
\]

If \(0<\alpha<1\), \(r=(1-\alpha)/\alpha\leq1\), and \(F(r)\leq5\), the same
conclusion holds. The unique positive solution of \(F(r)=5\) is approximately
\(0.15013659159\); thus the resulting density threshold is approximately
\(0.86946194679\). These decimals are explanatory approximations; \(F(r)\leq5\)
and the rational bound \(20/23\) are the exact claims.

The proof is elementary analysis plus a complete, finite combinatorial certificate
for the fixed 15-edge graph. A locally retained verifier checks all \(2^{15}\) edge
subsets. This is explicitly a computer-assisted finite classification, not a claim
that a numerical search proves the unrestricted conjecture. No novelty priority is claimed.

## 2. Kernel notation and moments

Write \(\beta=1-\alpha\), \(g=1_A-\alpha\), and
\(U(x,y)=g(x+y)\), with all averages normalized. For a graph \(J\), let
\(t(J,U)\) denote the average product of its edge kernels. Let \(H\) have vertices
\(0,\ldots,9\) and ordered edge list

\[
E(H)=\bigl((i,5+(i+j\bmod5)): i=0,\ldots,4;\ j=0,1,2\bigr).
\]

Then \(T_G(A)/N^{10}=t(H,\alpha+U)\). Every row of \(U\) has mean zero. No symmetry assumption on \(A\) is made; the two-variable kernel \(U(x,y)=g(x+y)\) is symmetric nonetheless.
For \(\alpha\geq1/2\), \(|U|\leq\alpha\).

Use normalized Fourier coefficients
\(\widehat g(\chi)=\mathbb E_x g(x)\overline{\chi(x)}\), and set
\(q_\chi=|\widehat g(\chi)|^2\). Orthogonality gives

\[
q_1=0,\qquad q_\chi=q_{\bar\chi},\qquad
S:=\sum_\chi q_\chi=\alpha\beta,\qquad
0\leq q_\chi\leq\beta^2.
\tag{1}
\]

The last bound follows, for nontrivial characters, by writing
\(\widehat g(\chi)=-\widehat {1_{G\setminus A}}(\chi)\).
Even-cycle densities are

\[
M_{2k}:=t(C_{2k},U)=\sum_\chi q_\chi^k\geq0.
\tag{2}
\]

Put \(E=M_4\). Cauchy–Schwarz and (1) imply

\[
M_6\geq E^2/S,\qquad E\leq\beta^2S=\alpha\beta^3.
\tag{3}
\]

For clarity, (2) also follows directly from the matrix identity for the symmetric
kernel \(U\): \(U^2\) has Fourier eigenvalues \(q_\chi\), so its \(k\)-th trace is
\(\sum q_\chi^k\). Normalized matrix multiplication uses \(N^{-1}\sum\).

Define
\(C(x,x')=\mathbb E_y U(x,y)U(x',y)\). Its Fourier coefficients as a function of
\(x-x'\) are \(q_\chi\). Therefore the three-neighbor star square norm is

\[
L:=t(K_{2,3},U)=\mathbb E_{x,x'}C(x,x')^3
 =\sum_{\chi\psi\omega=1}q_\chi q_\psi q_\omega\geq0.
\]

Since \(|C(x,x')|\leq S\), and since \(q_1=0\), respectively,

\[
L\leq SE,\qquad
L\leq\beta^2\left(S^2-E\right).
\tag{4}
\]

Indeed, for the second bound sum over \(\chi\psi\ne1\), replace the remaining
coefficient by \(\beta^2\), and use
\(\sum_\chi q_\chi q_{\bar\chi}=E\).

## 3. Three elementary graph bounds

### Three stars

Suppose an edge subgraph \(J\subseteq H\) has three vertices \(v_1,v_2,v_3\)
on one side, each of degree 2 or 3, with no common neighbor. Let
\(D=\deg v_1+\deg v_2+\deg v_3\) and \(e=|E(J)|\). Then

\[
|t(J,U)|\leq\alpha^{e-D}E^{3/2}(L/E)^{(D-6)/2}.
\tag{5}
\]

When \(E=0\), \(g=0\) by Fourier inversion and there is nothing to prove.
Otherwise, integrate each of the three selected vertices first. This gives three
star functions of their neighbor labels. Bound all remaining edge factors in
absolute value by \(\alpha\). Each remaining variable appears in at most two
star functions, because there is no common neighbor.

The inequality \(|\mathbb E h_1h_2h_3|\leq\prod_i\|h_i\|_2\) now applies.
Here is an elementary proof. Average out variables occurring in only one factor;
this does not increase its \(L^2\) norm. Group the remaining variables into the
three pairwise shared blocks \(X,Y,Z\). The factors become
\(a(X,Y),b(X,Z),c(Y,Z)\). Cauchy–Schwarz first in \(X\) gives the bound
\(\mathbb E_{Y,Z}|c(Y,Z)|(\mathbb E_Xa^2)^{1/2}(\mathbb E_Xb^2)^{1/2}\).
Another Cauchy–Schwarz in \((Y,Z)\) gives the product of the three norms.
A degree-2 star has squared norm \(E\), and a degree-3 star has squared norm
\(L\). There are \(D-6\) degree-3 stars, proving (5).

This is a special case of the generalized Cauchy–Schwarz framework discussed in
[Lovász, Subgraph densities in signed graphons and the local Sidorenko conjecture,
Lemma 2.3](https://arxiv.org/abs/1004.3026); the needed case has just been proved here.

### Two squares sharing an edge

Let \(\Theta_{1,3,3}\) be three internally disjoint paths of lengths \(1,3,3\)
with common endpoints. Because \(U\geq-\alpha\),

\[
t(\Theta_{1,3,3},U)
 =\mathbb E_{u,v}U(u,v)\bigl(U^3(u,v)\bigr)^2
 \geq-\alpha M_6.
\tag{6}
\]

### Reflection squares

Suppose \(J\) admits an involutory automorphism exchanging vertex sets \(P,Q\)
and fixing a set \(R\), with no edge between \(P,Q\) or inside \(R\). Conditional
on the labels of \(R\), the two sides contribute identical factors, so
\(t(J,U)\) is an average of squares and is nonnegative. The certificate supplies
and verifies the full involution and partition for every use of this fact.

## 4. Complete finite inventory

Expand

\[
t(H,\alpha+U)=\sum_{J\subseteq E(H)}\alpha^{15-|J|}t(J,U),
\tag{7}
\]

where isolated vertices do not affect the density. A subgraph with a degree-1
vertex contributes zero by the row-mean-zero property. The nonempty subgraphs
with no degree-1 vertex have the following **disjoint** classification:

| Class | Number | Contribution or certificate |
|---|---:|---|
| \(C_4\) | 5 | \(5\alpha^{11}E\) |
| \(C_6\) | 15 | \(15\alpha^9M_6\) |
| \(C_8\) | 25 | nonnegative |
| \(C_{10}\) | 8 | nonnegative |
| \(C_4\sqcup C_4\) | 5 | \(5\alpha^7E^2\) |
| \(C_4\sqcup C_6\) | 5 | nonnegative |
| \(\Theta_{1,3,3}\) | 5 | bounded by (6) |
| Reflection squares | 95 | nonnegative |
| Three-star certificate, \(D=7\) | 160 | bounded by (5) |
| Three-star certificate, \(D=8\) | 180 | bounded by (5) |
| Three-star certificate, \(D=9\) | 121 | bounded by (5) |

There are 624 rows in total. A locally retained combinatorial certificate gives a witness
for every row, indexed by the bit mask in the stated edge order.
A separate verifier enumerates all 32,768 edge subsets,
checks exact coverage, and validates each local witness and the displayed totals.
Its checks do not rely on Python assertions and remain active under `-O` and `-OO`.

## 5. Optimizing the bound

Assume \(1/2\leq\alpha<1\) and \(E>0\). Set

\[
r=\beta/\alpha,\quad z=\sqrt E/\alpha^2,\quad
s=L/(\alpha^2E),\quad D(s)=160\sqrt s+180s+121s^{3/2}.
\]

Equations (3) and (4) give

\[
0<z\leq r^{3/2},\qquad
0\leq s\leq \min\{r,\ r^4/z^2-r^2\}.
\tag{8}
\]

Apply (5) to the last three classes in the inventory. After multiplying by the
expansion coefficients in (7), their total absolute contribution is at most
\(\alpha^9E^{3/2}D(s)\). The five terms from (6) use only
\(5\alpha^9M_6\) of the positive \(15\alpha^9M_6\). Keeping the remaining
\(10\alpha^9M_6\), the five \(C_4\) terms and the five disjoint-square terms,
and then using (3), proves

\[
\frac{T_G(A)}{\alpha^{15}N^{10}}
 \geq 1+z^2\left[5-zD(s)+(5+10/r)z^2\right].
\tag{9}
\]

Since \(D\) is increasing, replace \(s\) by the upper bound in (8). The two
branches meet at \(z_*=r^{3/2}/\sqrt{1+r}\). For \(0<z\leq z_*\), the bracket
in (9) is bounded below by
\(Q(z)=5-zD(r)+(5+10/r)z^2\), which is decreasing: even at \(z=r^{3/2}\),

\[
Q'(z)\leq-140\sqrt r-180r-111r^{3/2}<0.
\]

For \(z_*\leq z\leq r^{3/2}\), set \(s=r^4/z^2-r^2\). Each function
\(z s^{k/2}\), for \(k=1,2,3\), is nonincreasing. Explicitly these are
\(\sqrt{r^4-r^2z^2}\), \(r^4/z-r^2z\), and
\((r^4-r^2z^2)^{3/2}/z^2\). Thus the lower-bound bracket is increasing on this
second interval. Its minimum over the entire interval occurs at \(z_*\) and is
exactly \(5-F(r)\). This proves the refined theorem.

For completeness, \(F\) is strictly increasing for \(r>0\): write it as

\[
\frac{r^2}{1+r}
\left[\sqrt{1+r}(160+180\sqrt r+121r)-(10+5r)\right].
\]

Both positive factors are increasing; the derivative of the bracket is positive,
already from the term \(121\sqrt{1+r}-5>0\), with its other derivative terms
positive. The root stated in Section 1 is therefore unambiguous.

### An exact rational endpoint

If \(\alpha\geq20/23\), then \(r\leq3/20\). At \(r=3/20\), use the exact
rational bounds \(\sqrt{3/20}<3873/10000\) and
\(\sqrt{23/20}>10723/10000\). Their validity follows by squaring. Consequently

\[
F(3/20)
 < \frac{160(3/20)^2+180(3/20)^2(3873/10000)+121(3/20)^3}{10723/10000}
 -\frac{10(3/20)^2+5(3/20)^3}{23/20}<5.
\]

The last comparison is rational arithmetic, reproduced by the checks.
Monotonicity handles every smaller \(r\). Finally, \(A=G\) gives equality and
handles \(\alpha=1\).

## 6. Further exact special cases

### Quotients and cosets

If \(\pi:G\twoheadrightarrow Q\) is a surjective homomorphism and
\(A=\pi^{-1}(B)\), then
\(T_G(A)/|G|^{10}=T_Q(B)/|Q|^{10}\): every quotient tuple has exactly
\(|\ker\pi|^{10}\) lifts. Products of verified examples are also verified,
because densities and normalized tuple counts multiply.

If \(A=a+K\) is a coset of a subgroup, connectedness of \(H\) forces all left
quotient labels to be equal and all right quotient labels to be their common
complement to \(a\). Hence
\(T_G(A)/N^{10}=\alpha^9\geq\alpha^{15}\).

If \(A=G\setminus(a+K)\), let \(q=[G:K]\). Replacing each right quotient label
\(y\) by \(a-y\) identifies the count with the number of proper \(q\)-colorings
of \(H\). Thus its normalized value is \(P_H(q)/q^{10}\). Direct
inclusion–exclusion gives

\[
P_H(q)=q^{10}-15q^9+105q^8-450q^7+1305q^6-2663q^5
       +3825q^4-3710q^3+2175q^2-573q.
\]

The coefficients of \(q^5P_H(q)-(q-1)^{15}\), after substituting \(q=u+2\),
in ascending powers of \(u\), are

\[
(63,369,1735,4585,7495,8821,8072,5740,3085,1220,340,60,5).
\]

They are all positive, proving the desired inequality for every integer \(q\geq2\).
The case \(q=1\) is the empty set. The verifier recomputes the chromatic
polynomial from all edge subsets and checks this polynomial identity exactly.

### Exhaustive finite check

Separate integer enumeration checked every subset of every abelian group of order
at most 16: 25 isomorphism types, 398,350 subsets, represented by 26,300 translation
orbits. No violation was found. The computation uses

\[
T_G(A)=N\sum_{a,b,c,d\in G}
C_A(0,a,b)C_A(a,b,c)C_A(b,c,d)C_A(c,d,0)C_A(d,0,a),
\]

where \(C_A(u,v,w)=|(A-u)\cap(A-v)\cap(A-w)|\). This follows by first fixing
the right labels, independently counting the five left labels, and then translating
the first right label to zero. The comparison is the integer inequality
\(T_G(A)N^5\geq |A|^{15}\), without floating-point tolerances.
This finite check is supporting evidence and a finite special case, not the
basis for the all-group high-density theorem.

## 7. Boundary of the result

Nothing here handles all densities and all subsets. In particular, neither the
high-density criterion, the coset/complement-coset cases, quotient/product closure,
nor the finite enumeration settles the unrestricted GREEN-012 assertion. The
remaining range requires another argument or a counterexample. The source
inspection found no basis for transferring the neighboring DTZ negative-answer
scenario to this problem.
