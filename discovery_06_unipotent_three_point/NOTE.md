# A 14-variable polynomial map with everywhere unipotent Jacobian and a three-point fiber

**Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol (OpenAI)**

Branch draft prepared 22 July 2026. Not peer reviewed.

> **Verification warning.** Alec Kriebel is a complete amateur exploring the
> limits of AI-assisted mathematics and cannot independently verify these
> claims. This note and its exact certificates are released for expert
> checking. Priority and minimality statements have the deliberately narrow
> scope stated below.

## Abstract

We give an exact rational polynomial vector \(g\in\mathbb Q[Z]^{14}\), with
24 monomials, such that

\[
 \det(I+sJg)=1
 \qquad\text{in }\mathbb Q[s,Z],
\]

and such that \(I+g\) has three displayed rational points in one fiber.
Generically, \(Jg\) is regular nilpotent, with the single Jordan block
\((14)\). The generic degree of \(I+g\) is three and its geometric monodromy
is \(S_3\).

For the image operator

\[
 E(\xi^\alpha p(Z))=\partial_Z^\alpha p(Z),
\]

put \(A=-\sum_{j=1}^{14}\xi_jg_j\) and \(b=x+y+u_{11}\). Then

\[
 E(A^m)=0,\qquad E(bA^m)\ne0
 \qquad(m\ge1).
\]

Thus the Special Image Conjecture fails in dimension 14, with an obstruction
at every exponent. A degree-seven homogeneous companion in 15 variables and
a homogeneous Hessian-nilpotent companion in 30 variables are recorded at
the end. The dimension and term counts are proved optimal only within the
stated constant-state realization ansatz.

## 1. The three-variable source

Put \(u=1+xy\) and

\[
\begin{aligned}
F_1&=u^3z+y^2u(4+3xy),\\
F_2&=y+3xu^2z+3xy^2(4+3xy),\\
F_3&=2x-3x^2y-x^3z.
\end{aligned}
\]

Use the identity-linear normalization

\[
 \Phi=(F_3/2,F_2,F_1)=X+H_2+H_3+\cdots+H_7. \tag{1}
\]

Its homogeneous pieces are

\[
\begin{array}{c|ccc}
d&H_{d,1}&H_{d,2}&H_{d,3}\\ \hline
2&0&3xz&4y^2\\
3&-\tfrac32x^2y&12xy^2&3xyz\\
4&-\tfrac12x^3z&6x^2yz&7xy^3\\
5&0&9x^2y^3&3x^2y^2z\\
6&0&3x^3y^2z&3x^2y^4\\
7&0&0&x^3y^3z.
\end{array} \tag{2}
\]

Direct differentiation gives \(\det J\Phi=1\). The points

\[
 r_0=(0,0,-\tfrac14),\quad
 r_+=(1,-\tfrac32,\tfrac{13}2),\quad
 r_-=(-1,\tfrac32,\tfrac{13}2) \tag{3}
\]

all map to \((0,0,-1/4)\).

## 2. Three state chains

Take state coordinates, in this order,

\[
 U=(u_{11},u_{12};u_{21},u_{22},u_{23},u_{24};
 u_{31},u_{32},u_{33},u_{34},u_{35}). \tag{4}
\]

Let \(B\in\operatorname{Mat}_{3\times11}(\mathbb Q)\) select the three chain
heads, so \(BU=(u_{11},u_{21},u_{31})^T\). Let
\(N=J_2\oplus J_4\oplus J_5\), where every \(J_e\) has ones immediately
above the diagonal. Finally put

\[
C=\begin{pmatrix}
H_{3,1}\\H_{4,1}\\
H_{3,2}\\H_{4,2}\\H_{5,2}\\H_{6,2}\\
H_{3,3}\\H_{4,3}\\H_{5,3}\\H_{6,3}\\H_{7,3}
\end{pmatrix}. \tag{5}
\]

Define

\[
 g(X,U)=\bigl(H_2(X)+BU,-C(X)-NU\bigr). \tag{6}
\]

In the coordinate order \(Z=(x,y,z,U)\), this is

\[
\begin{aligned}
g_1&=u_{11},&
g_2&=3xz+u_{21},&
g_3&=4y^2+u_{31},\\
g_4&=\tfrac32x^2y-u_{12},&
g_5&=\tfrac12x^3z,\\
g_6&=-12xy^2-u_{22},&
g_7&=-6x^2yz-u_{23},\\
g_8&=-9x^2y^3-u_{24},&
g_9&=-3x^3y^2z,\\
g_{10}&=-3xyz-u_{32},&
g_{11}&=-7xy^3-u_{33},\\
g_{12}&=-3x^2y^2z-u_{34},&
g_{13}&=-3x^2y^4-u_{35},\\
g_{14}&=-x^3y^3z.
\end{aligned} \tag{7}
\]

There are exactly 24 displayed monomials. Consequently

\[
 A(\xi,Z)=-\sum_{j=1}^{14}\xi_jg_j(Z) \tag{8}
\]

also has 24 monomials, in 28 indeterminates, and total degree eight.

## 3. The determinant pencil and regular nilpotency

The Jacobian pencil has block form

\[
 I+sJg=
 \begin{pmatrix}
 I_3+sJH_2&sB\\
 -sJC&I_{11}-sN
 \end{pmatrix}. \tag{9}
\]

Because \(N^5=0\), the lower-right block has determinant one and

\[
 (I-sN)^{-1}=I+sN+s^2N^2+s^3N^3+s^4N^4. \tag{10}
\]

The chain definition gives \(BN^kC=H_{k+3}\) for \(0\le k\le4\), with
absent components interpreted as zero. Hence the Schur complement is

\[
\begin{aligned}
I_3+sJH_2+s^2B(I-sN)^{-1}JC
 &=I_3+\sum_{d=2}^7s^{d-1}JH_d(X)\\
 &=J\Phi(sX).
\end{aligned} \tag{11}
\]

Therefore

\[
 \boxed{\det(I+sJg)=\det J\Phi(sX)=1.} \tag{12}
\]

The characteristic polynomial of \(Jg\) is \(\lambda^{14}\), so
Cayley--Hamilton gives \((Jg)^{14}=0\) everywhere. The exact entry

\[
 \bigl((Jg)^{13}\bigr)_{1,5}=-3x^6y^4z \tag{13}
\]

is nonzero. Thus the generic nilpotency index is 14, forcing Jordan type
\((14)\) and generic rank 13.

## 4. The rational three-point fiber

For a source point \(r\), put \(U(r)=(I-N)^{-1}C(r)\). The last eleven
coordinates of \((I+g)(r,U(r))\) then vanish, while the first three are
\(\Phi(r)\). Thus (3) lifts to

\[
\begin{aligned}
p_0={}&(0,0,-\tfrac14;0,0;0,0,0,0;0,0,0,0,0),\\
p_+={}&(1,-\tfrac32,\tfrac{13}2;-1,-\tfrac{13}4;
-18,-45,\tfrac{27}2,\tfrac{351}8;\\
&\hspace{35mm}-\tfrac{63}4,\tfrac{27}2,\tfrac{297}8,
-\tfrac{27}4,-\tfrac{351}{16}),\\
p_-={}&(-1,\tfrac32,\tfrac{13}2;1,\tfrac{13}4;
18,45,-\tfrac{27}2,-\tfrac{351}8;\\
&\hspace{35mm}-\tfrac{63}4,\tfrac{27}2,\tfrac{297}8,
-\tfrac{27}4,-\tfrac{351}{16}).
\end{aligned} \tag{15}
\]

Direct substitution gives

\[
 (I+g)(p_0)=(I+g)(p_+)=(I+g)(p_-)
 =(0,0,-\tfrac14,0,\ldots,0). \tag{16}
\]

## 5. Generic degree and monodromy

For a target \((Y,V)\), the state equations give

\[
 U=(I-N)^{-1}(V+C(X)),\qquad
 \Phi(X)=Y-B(I-N)^{-1}V. \tag{17}
\]

Thus \(I+g\) is stably equivalent to \(\Phi\times I_{11}\). The cubic inverse
resolvent for the unnormalized \(F\) is

\[
 2a\tau^3-b\tau^2+2\tau-c=0 \tag{18}
\]

over a target \((a,b,c)\). It is generically irreducible with nonsquare
discriminant, so the generic degree is three and the geometric monodromy is
\(S_3\). These source assertions, including exact certificates, are proved
in Discovery 04. The same holds for \(I+g\).

For every nonzero scalar \(s\), elimination from \(T_s=I+sg\) similarly
gives

\[
 s^{-1}\Phi(sX)=Y-sB(I-sN)^{-1}V. \tag{19}
\]

Thus every nonzero member of the pencil remains noninjective and has generic
degree three and monodromy \(S_3\).

## 6. Consequences for named injectivity conjectures

The derivative of \(T=I+g\) is everywhere unipotent, yet (16) shows that
\(T\) is not injective. This supplies an explicit counterexample in dimension
14 to the Unipotent Jacobian Univalence Conjecture recorded by Campbell and
to the corresponding all-eigenvalues-one form of Chamberland's injectivity
conjecture.

It also gives a concrete failure of Kulikov's \(JN(14)\). For any
\(c\in\mathbb C^{14}\), put \(N_c(Z)=c-g(Z)\). Then \(JN_c=-Jg\) is
nilpotent, and fixed points of \(N_c\) are exactly the points of
\((I+g)^{-1}(c)\). The value in (16) gives three rational fixed points, while
a generic \(c\) gives three geometric fixed points.

These statements concern algebraic injectivity conjectures. They should not
be confused with the classical dynamical Markus--Yamabe conjecture, which has
older counterexamples, or with valid theorems using singular-value rather
than eigenvalue bounds.

## 7. Failure of \(\operatorname{SIC}(14)\) at every exponent

For \(n\) pairs of variables define

\[
 E_n:\mathbb C[\xi_1,\ldots,\xi_n,Z_1,\ldots,Z_n]
 \longrightarrow\mathbb C[Z],\qquad
 E_n(\xi^\alpha p)=\partial_Z^\alpha p. \tag{20}
\]

The Special Image Conjecture says that \(\ker E_n\) is a Mathieu--Zhao
subspace. We use the following scalar-parameter inversion identity.

**Lemma 1.** If \(\det(I+tJg)=1\), \(A=-\xi\cdot g\), and \(Q_t\) is the
formal inverse of \(I+tg\), then for every polynomial \(p\),

\[
 p(Q_t(Z))=\sum_{m\ge0}\frac{t^m}{m!}E_n(pA^m). \tag{21}
\]

**Proof.** Apply the Abhyankar--Gurjar inversion formula to
\(I+tg=I-H_t\), where \(H_t=-tg\). The determinant factor is one, and the
multinomial theorem collects the terms of total \(\xi\)-degree \(m\). The
identity is valid \(t\)-adically because every coefficient receives only
finitely many contributions. \(\square\)

Taking \(p=1\) in (21) gives

\[
 E_{14}(A^m)=0\qquad(m\ge1). \tag{22}
\]

Now specialize the inverse target to

\[
 Z_*=(\tfrac12,0,1,0,\ldots,0), \tag{23}
\]

and let \(\tau\in t\mathbb Q[[t]]\) be the unique solution of

\[
 \tau+t\tau^3=\frac t2. \tag{24}
\]

Eliminating the zero state target in \(I+tg\), then using (18), gives

\[
 Q_{t,x}(Z_*)=\tau',\qquad
 Q_{t,y}(Z_*)=-3\tau,\qquad
 Q_{t,u_{11}}(Z_*)=-\frac{\tau'-1/2}{t}. \tag{25}
\]

For completeness, the first two identities follow from reconstruction of a
preimage of the unnormalized target \((t,0,t)\); differentiating (24) turns
its \(x\)-coordinate into \(t\tau'\). The last identity is the first target
equation \(Q_x+tQ_{u_{11}}=1/2\).

Set \(b=x+y+u_{11}\) and write

\[
 b(Q_t)(Z_*)=\sum_{m\ge0}q_mt^m. \tag{26}
\]

Lagrange inversion in (24) gives

\[
\begin{aligned}
q_{3k}&=(-1)^k\frac{\binom{3k+1}{k}}{2^{2k+1}},\\
q_{3k+1}&=(-1)^{k+1}
 \frac{3\binom{3k+1}{k}}{(3k+1)2^{2k+1}},\\
q_{3k+2}&=(-1)^k\frac{\binom{3k+4}{k+1}}{2^{2k+3}}.
\end{aligned} \tag{27}
\]

Every number in (27) is nonzero. Comparing (21) and (26) proves

\[
 \boxed{E_{14}(bA^m)(Z_*)=m!q_m\ne0\quad(m\ge1).} \tag{28}
\]

Equations (22) and (28) disprove \(\operatorname{SIC}(14)\), with a
nonvanishing obstruction at every possible exponent.

## 8. Optimality inside the constant-state ansatz

This section makes no global minimality claim. Consider only realizations

\[
 \widetilde g(X,U)=(H_2(X)+\widetilde B U,
 -\widetilde C(X)-\widetilde N U) \tag{29}
\]

with constant matrices, nilpotent \(\widetilde N\), and exact Markov
parameters

\[
 \widetilde B\widetilde N^k\widetilde C=H_{k+3}
 \qquad(k\ge0). \tag{30}
\]

Order the eleven distinct tail monomials as

\[
x^2y,\ xy^2,\ xyz,\ x^3z,\ x^2yz,\ xy^3,\ x^2y^3,\ x^2y^2z,\
x^3y^2z,\ x^2y^4,\ x^3y^3z. \tag{31}
\]

Let \(M_k\in\operatorname{Mat}_{3\times11}\) be the coefficient matrix of
\(H_{k+3}\) in these columns, with \(M_k=0\) for \(k\ge5\). For
\(0\le j\le5\), form the finite block Hankel matrix
\(\mathcal H_j=(M_{j+r+c})_{0\le r,c<5-j}\). Their exact ranks are

\[
 11,8,5,3,1,0. \tag{32}
\]

For \(\mathcal H_0\), using the standard block row and block column order,
rows
\(1,2,3,4,5,6,8,9,11,12,15\) and columns \(1,\ldots,11\) give determinant

\[
 275562=2\cdot3^9\cdot7\ne0. \tag{33}
\]

Every realization (30) factors \(\mathcal H_0\) through its state space, so
at least eleven states are necessary. The shifted matrix
\(\mathcal H_1\) factors through \(\widetilde N\), so its rank eight gives
\(\operatorname{rank}\widetilde N\ge8\). Thus dimension 14 is minimal in
(29). Also
\(\operatorname{rank}\widetilde B\ge3\),
\(\widetilde C\) must contain
the eleven monomial inputs. Counting the two terms of \(H_2\) gives

\[
 2+3+8+11=24 \tag{34}
\]

as a term lower bound. Equation (7) attains it.

## 9. Homogeneous companions

Introduce one variable \(w\) and homogenize to degree seven:

\[
 h(Z,w)=\bigl(w^7g(Z/w),0\bigr)\in\mathbb Q[Z,w]^{15}. \tag{35}
\]

This vector has 24 terms and

\[
 \det(I+sJh)=\det(I+sw^6Jg(Z/w))=1. \tag{36}
\]

Thus \(Jh\) is nilpotent. The three points
\((p_0,1),(p_+,1),(p_-,1)\) collide under \(I+h\), and the generic degree
and monodromy remain \(3\) and \(S_3\). The exact checker certifies
\((Jh)^{13}\ne0\), so the generic nilpotency index is at least 14. We do not
claim the exact index here without the separate degree-14 zero certificate.

The standard de Bondt--van den Essen symmetrization gives a 30-variable
homogeneous degree-eight polynomial. For \(A,B\in\mathbb C^{15}\), put

\[
 P(A,B)=i\sum_{j=1}^{15}h_j(A+iB)B_j. \tag{37}
\]

The symmetrization lemma implies that \(\operatorname{Hess}P\) is nilpotent.
The usual linear solve with \(I+Jh(x)^T\) transports any two of the displayed
colliding points to a collision of \(I-\nabla P\). Equation (36), rather than
a several-page expansion, is the sparse certificate.

## 10. Scope and priority

The state-space dimension formula

\[
 3+(4-2)+(6-2)+(7-2)=14
\]

is the classical degree bookkeeping in Kulikov's reduction. The conceptual
existence of a 14-dimensional reduction is not claimed as new. The asserted
contribution is the explicit sparse instantiation, its regular-nilpotent and
three-point-fiber certificates, and the resulting consequence cascade,
especially the every-exponent \(\operatorname{SIC}(14)\) formula.

At the audit cutoff, no earlier public source was located giving this exact
14-variable object or an explicit \(\operatorname{SIC}(n)\) witness for
\(n\le14\). This is provisional evidence, not proof of worldwide priority.
No global smallest-dimension or smallest-term assertion is made.

## References

1. L. A. Campbell, *Unipotent Jacobian Matrices and Univalent Maps*,
   [arXiv:math/9907157](https://arxiv.org/abs/math/9907157).
2. V. S. Kulikov, *Jacobian Conjecture and Nilpotent Mappings*,
   [arXiv:math/9803143](https://arxiv.org/abs/math/9803143).
3. W. Zhao, *Images of Commuting Differential Operators of Order One with
   Constant Leading Coefficients*, J. Algebra 324 (2010), 231--247;
   [arXiv:0902.0210](https://arxiv.org/abs/0902.0210).
4. M. de Bondt and A. van den Essen, *A reduction of the Jacobian conjecture
   to the symmetric case*, Proc. Amer. Math. Soc. 133 (2005), 2201--2205.
5. A. Kriebel, with ChatGPT 5.6 Sol, *Full wreath-product monodromy through
   the third iterate of an explicit Keller map*, Discovery 04 (2026).
