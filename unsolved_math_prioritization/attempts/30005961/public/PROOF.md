# Verified calculations and construction obstructions

## 1. Conventions and imported dependencies

All varieties below are over \(\mathbf C\). “Strict Calabi–Yau threefold” means
smooth, connected, projective, simply connected, and \(K_X\simeq\mathcal O_X\).
For an automorphism, write \(d_p(f)\) for its dynamical degrees.
A map is primitive when no dominant rational map \(X\dasharrow B\),
\(0<\dim B<3\), semiconjugates it to a birational selfmap of \(B\).

The following published inputs are used, not reproved:

- **Dynamical input:** \(d_1(f)\) is the spectral radius on \(N^1(X)_\mathbf R\);
  entropy is \(\max_p\log d_p(f)\). Dynamical degrees agree under equivariant
  generically finite rational maps. A birational threefold map with
  \(d_1\ne d_2\) is primitive. See [OT, §3 and Theorem 4.1](https://arxiv.org/abs/1306.1590).
- **Geometric input:** \(X_3\) and \(X_7\) are smooth projective simply connected
  crepant resolutions with trivial canonical bundle. A strict Calabi–Yau
  threefold with a birational \(c_2\)-contraction is one of these two.
  A maximal \(c_2\)-contraction exists whenever a nontrivial one exists.
  See [OS, Theorems 3.3–3.4 and Lemma–Definition 4.1](https://arxiv.org/abs/math/9909175).
- **Nef eigenvector input:** a linear automorphism preserving the nef cone has a
  nef eigenvector for its spectral radius, by the finite-dimensional
  Perron–Frobenius theorem for a closed pointed full-dimensional cone.

Here a \(c_2\)-contraction is a surjective morphism \(\phi:X\to B\) to a normal
projective variety with connected fibers, positive-dimensional image, and
\(c_2(X)\cdot\phi^*H=0\) for an ample divisor \(H\) on \(B\).
We use the original OS direction of maximality: every \(c_2\)-contraction factors
through \(\phi_0\), so \(\phi=\mu\circ\phi_0\).

Simple connectedness implies \(b_1=0\), hence \(H^1(X,\mathcal O_X)=0\).
Serre duality and \(K_X\simeq\mathcal O_X\) then give
\(H^2(X,\mathcal O_X)=0\). Hodge symmetry yields \(h^{1,0}=h^{2,0}=0\).
These vanishings are consequences here, not replacements for simple connectedness.

## 2. Attempt 1: change the automorphism on the scalar quotient

Let \(E=\mathbf C/(\mathbf Z+\mathbf Z\zeta_3)\), \(A=E^3\), and
\(X_3\to A/\langle\zeta_3 I\rangle\) be the known resolution.
For an integer \(m\ge3\), put
\[
 P_m=\begin{pmatrix}0&1&0\\0&0&1\\-1&m&0\end{pmatrix},\qquad
 P_m^{-1}=\begin{pmatrix}m&0&-1\\1&0&0\\0&1&0\end{pmatrix}.
\]
Thus \(P_m\in\mathrm{GL}_3(\mathbf Z)\), with determinant **\(-1\)**.
It commutes with the scalar group, descends to the quotient, and lifts to the
blow-up of its singular-point ideal, an invariant ideal. The inverse lifts too,
so the lift is biregular. This is the known quotient mechanism, not a new geometry.

Its characteristic polynomial is \(p_m(t)=t^3-mt+1\).
There is one root in each of
\((-(m+1),-1)\), \((0,1)\), and \((1,m+1)\): the endpoint signs are respectively
\((- ,+)\), \((+,-)\), and \((-,+)\). A cubic has no further roots.
Call them \(\alpha<0<\beta<\gamma\). Since their sum is zero,
\(|\alpha|=\beta+\gamma>\gamma>1>\beta>0\).
The eigenvalues on holomorphic one-forms of \(A\) are these roots. Wedge products
therefore give
\[
 d_1(P_m)=\alpha^2,\qquad d_2(P_m)=\alpha^2\gamma^2>d_1(P_m)>1.
\]
The generically finite equivariant map from \(A\) to \(X_3\) transfers these
numbers. The dynamical input proves primitivity and positive entropy.

**Exact gap:** the underlying variety is always \(X_3\). Neither varying \(m\)
nor taking powers supplies a further underlying threefold. The original OT
family uses \(m=3a^2\); the calculation above is only an elementary extension
of that known mechanism, with no novelty claim.

## 3. Attempt 2: vary the finite quotient

### 3.1 The scalar subcase cannot vary the elliptic period freely

Suppose an elliptic-curve automorphism acts on its one-form by a scalar \(\xi\),
and quotient \(E^3\) by the diagonal action. A necessary condition for a smooth
resolution to have trivial canonical bundle is \(\xi^3=1\). Indeed, a nonzero
holomorphic three-form on a smooth resolution restricts to the smooth quotient
locus; its pullback extends across the finite omitted set of \(E^3\). It must be
a nonzero invariant multiple of the unique three-form on \(E^3\). The action on
that form is multiplication by \(\xi^3\).

A nontrivial scalar satisfying this condition has order three. The elliptic
curve then has the equianharmonic complex structure; this returns the same
scalar quotient. Order two, four, or six scalar actions do not fix the
three-form. An arbitrary resolution is not a remedy for that obstruction.

### 3.2 A larger obstruction for isolated abelian quotients

Let \(A\) be an abelian threefold, and let a finite group \(G\) act freely away
from finitely many points. Assume \(Y=A/G\) has a projective crepant resolution
\(\nu:X\to Y\) which is an isomorphism over the free quotient locus, and assume
\(X\) is strict Calabi–Yau. Then \(X\simeq X_3\) or \(X_7\).

To see why the classification applies, choose a general sufficiently ample
surface \(S\subset Y\) avoiding the finite exceptional set. Its inverse image
\(\widetilde S\subset A\) is a finite étale cover of \(S\). On this surface
\[
 q^*(T_Y|_S)=T_A|_{\widetilde S},
\]
which is trivial. The pullback of \(c_2(T_Y|_S)\) is zero, and integration over
the finite cover gives \(\int_S c_2(T_Y|_S)=0\). As \(\nu\) is an isomorphism
near \(S\), this is \(c_2(X)\cdot\nu^*H=0\). Thus \(\nu\) is a birational
\(c_2\)-contraction. The geometric input gives the conclusion. If the quotient
is everywhere étale, its fundamental group contains the infinite finite-index
subgroup \(\pi_1(A)\), and it is not strict.

This published classification is also stated in [Gachet, Theorems 1.1–1.2](https://jep.centre-mersenne.org/articles/10.5802/jep.277/).
The hypothesis concerning a finite nonfree locus is essential to the argument:
quotients with fixed curves are not excluded by this proof.

### 3.3 Explicit check of the second known example

For the Klein-quartic abelian threefold \(A_7\), the order-seven action \(g\)
has eigenvalues \(\zeta,\zeta^2,\zeta^4\) on holomorphic one-forms.
The unit \(F=1+g\) has inverse \(-(g+g^3+g^5)\), because
\((1+g)(g+g^3+g^5)=-1\). Its descent to \(X_7\) is biregular by the unique
projective crepant-resolution result; see [Oguiso, §4.1 and Lemma 4.6](https://arxiv.org/html/2401.04386v3).

Set
\[
 a=2+2\cos(2\pi/7),\quad b=2+2\cos(4\pi/7),\quad
 c=2+2\cos(6\pi/7).
\]
They satisfy \(a>b>1>c>0\) and \(abc=1\).
Indeed, they are the three roots of \(t^3-5t^2+6t-1\), as the exact cyclotomic
calculation checks. Consequently
\[
 d_1(F)=a,\qquad d_2(F)=ab=1/c>a>1.
\]
The same holds on \(X_7\), proving primitivity by the imported criterion.
This is verification of the known example. Its inverse reverses the degree
ordering, without changing the underlying threefold.

## 4. Attempt 3: use a surface product and a diagonal finite quotient

Let \(S\) be a smooth projective surface, \(E\) an elliptic curve, and
\(G\subset\mathrm{Aut}(S)\times\mathrm{Aut}(E)\) finite. Let \(G_E\) be its
image in \(\mathrm{Aut}(E)\). The projection induces a surjective morphism
\[
 (S\times E)/G\longrightarrow E/G_E.
\]
Suppose \(u=(u_S,u_E)\) normalizes \(G\). Then \(u_E\) normalizes \(G_E\),
and it induces an automorphism of the quotient curve. If \(u\) induces a
birational map \(f\) on any smooth projective model \(X\) of \((S\times E)/G\),
the resulting dominant rational map \(\pi:X\dasharrow E/G_E\) satisfies
\(\pi f=\overline{u_E}\pi\). Its base has dimension one. Thus **this particular
induced map is imprimitive**, regardless of its entropy or whether \(X\) is strict.

The product \(S\times E\) itself is not simply connected. Some diagonal quotient
resolutions can remove that defect, but they do not remove the displayed
fibration for product-induced maps. This argument does not classify all
abstract automorphisms of all such quotient resolutions.

## 5. Attempt 4: upgrade birational examples to biregular ones

### 5.1 Elementary Picard-rank obstruction

**Lemma.** A smooth projective threefold of Picard number at most two admits
no positive-entropy biregular automorphism.

For rank one, the integral action on \(N^1\) is multiplication by \(1\), since
it preserves the ample ray. For rank two, suppose the action \(M\) had spectral
radius \(r>1\). Since \(M\in\mathrm{GL}_2(\mathbf Z)\), its determinant has
absolute value one. Nonreal conjugate eigenvalues would both have modulus one;
therefore it has distinct real eigenvalues \(u,v\), with \(|u|=r\),
\(|v|=r^{-1}\). Choose real eigenvectors \(e_1,e_2\).

The cubic intersection polynomial
\(C(x,y)=(xe_1+ye_2)^3\) satisfies \(C(ux,vy)=C(x,y)\).
The coefficient of \(x^iy^{3-i}\) can be nonzero only if
\(u^iv^{3-i}=1\). Its absolute value is \(r^{2i-3}\), and the exponents
for \(i=0,1,2,3\) are \(-3,-1,1,3\). None is zero. All coefficients vanish,
contradicting the positive cube of an ample class. Hence \(d_1=1\), and the
entropy vanishes. This also proves the corresponding assertion in every odd
dimension by replacing three with that dimension. □

For strict Calabi–Yau manifolds of rank two, the stronger finiteness of the
whole automorphism group is already [Oguiso, Theorem 1.2](https://arxiv.org/abs/1206.1649).
Our lemma is an elementary obstruction, not a new finiteness theorem.

### 5.2 Wehler and resolution pitfalls

For a generic smooth hypersurface of multidegree \((2,2,2,2)\) in
\((\mathbf P^1)^4\), the birational group is infinite but the biregular group
is trivial; see [Cantat–Oguiso, Theorem 1.3](https://arxiv.org/abs/1107.5862).
Birational primitivity or dynamical-degree computations on that model therefore
do not meet the requested biregularity condition.

Nor can one simply resolve indeterminacy by arbitrary blow-ups while retaining
trivial canonical bundle. If \(b:\widetilde X\to X\) blows up a smooth center
of codimension \(r\ge2\) in a smooth threefold with \(K_X\sim0\), then
\(K_{\widetilde X}\sim(r-1)E\). For ample \(H\) on \(\widetilde X\),
\(E\cdot H^2>0\), so this canonical divisor is not numerically trivial.
The statement does not prohibit crepant birational modifications; it identifies
why an unrestricted resolution does not prove the target.

## 6. Attempt 5: exploit the second Chern class or deform known examples

### 6.1 What a positive-entropy nef eigenvector actually gives

Let \(f\in\mathrm{Aut}(X)\) have \(\lambda=d_1(f)>1\), and choose a nonzero
nef class \(D\) with \(f^*D=\lambda D\). Naturality of Chern classes and
invariance of intersection numbers give
\[
 (\lambda^3-1)D^3=0,\qquad (\lambda-1)c_2(X)\cdot D=0.
\]
Thus \(D^3=0\) and \(c_2(X)\cdot D=0\).
Moreover, its ray is irrational: if it contained a nonzero rational vector,
\(\lambda\) would be rational. Both \(\lambda\) and \(\lambda^{-1}\) are
algebraic integers, since \(f^*\) and its inverse preserve the integral divisor
lattice. A rational algebraic unit is \(1\) or \(-1\), a contradiction.

This proves the existence of a real boundary class only. It neither proves nor
disproves that another nonzero **rational** nef class is orthogonal to \(c_2\).
It also does not produce a line bundle or any sections of one.

### 6.2 A precise conditional obstruction

**Proposition (deduction from OS).** Suppose a strict Calabi–Yau threefold
\(X\) has a primitive biregular automorphism and a nonzero numerical class of
a semiample line bundle \(L\) satisfying \(c_2(X)\cdot L=0\).
Then \(X\simeq X_3\) or \(X_7\).

A sufficiently divisible power of \(L\), followed by Stein factorization,
gives a \(c_2\)-contraction with positive-dimensional base. Positivity of the
base dimension follows because a semiample line bundle giving a constant map
is numerically trivial. Take the maximal contraction \(\phi_0:X\to B_0\).

For any \(f\in\mathrm{Aut}(X)\), \(\phi_0 f\) is another \(c_2\)-contraction,
so maximality gives a morphism \(f_B:B_0\to B_0\) with
\(\phi_0 f=f_B\phi_0\). Applying the same argument to \(f^{-1}\) and using
surjectivity of \(\phi_0\) shows that \(f_B\) is invertible. Primitivity
therefore forces \(\dim B_0=3\). A generically finite contraction with connected
fibers in characteristic zero is birational. The classification gives the
conclusion. □

In particular, a new target example would force at least one of the following
properties to fail on that variety:

- the nonzero real nef \(c_2\)-null face contains a nonzero rational class;
- every nef integral divisor is semiample.

Neither property is proved here. Their conditional consequence is already
[Oguiso's OWR Proposition 11](https://doi.org/10.4171/owr/2024/32).
Assuming them would reverse the goal and exclude new examples; assuming their
failure would not construct a variety.

### 6.3 Rigidity does not yield a deformation family

The two known examples are rigid. For a Calabi–Yau threefold, contraction with
a nowhere-zero three-form identifies \(T_X\) with \(\Omega_X^2\), so the
infinitesimal deformation space is \(H^1(T_X)\simeq H^{2,1}(X)\).
Its vanishing leaves no local deformation parameter at either known example.
This closes the naive small-deformation route only; it says nothing decisive
about an unrelated variety or a singular transition.

## 7. Final boundary

No theorem in this note excludes all new strict Calabi–Yau threefolds, and no
construction supplies one. Fixed-curve quotient actions, crepant changes of
model outside the rank-two setting, and genuinely new nef-cone geometry remain
outside the proved obstructions. No proposal in these directions was completed
within the five-attempt budget. The target remains unresolved.
