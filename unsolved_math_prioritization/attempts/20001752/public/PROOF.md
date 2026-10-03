# A quasimodular summation formula for the E8 midpoint Mellin value

## Scope and result

For the normalized sphere-packing auxiliary function in dimension eight, this note proves
\[
\int_0^\infty f_8(r)r^3\,dr
=\int_0^\infty \widehat f_8(r)r^3\,dr=\frac1{15}.
\tag{1}
\]
The Fourier convention is
\[
\widehat f(y)=\int_{\mathbb R^d}f(x)e^{-2\pi i x\cdot y}\,dx,
\qquad f_d(0)=\widehat f_d(0)=1.
\]
All functions called radial Schwartz functions below belong to
\(\mathcal S_{\rm rad}(\mathbb R^d)\); primes mean derivatives of their radial profiles.

The analogous numerical identification in dimension 24 is **not settled here**.
We prove an exact auxiliary identity there, and give a convergent real integral
for the midpoint moment, but do not identify its value with a simpler named
constant. Thus the combined problem has a partial result, with its entire
8-dimensional part proved.

## 1. A continuous summation functional

Write
\[
E_2(\tau)=1-24\sum_{n\ge1}\sigma_1(n)q^n,
\qquad q=e^{2\pi i\tau},\quad\operatorname{Im}\tau>0,
\]
and set
\[
E_2^2=\sum_{n\ge0}a_nq^n,\qquad
E_2^3=\sum_{n\ge0}b_nq^n.
\]
In particular \(a_0=b_0=1\), \(a_1=-48\), and \(b_1=-72\).
For a smooth radial profile define
\[
\mathcal D f(r)=\begin{cases}f'(r)/r,&r>0,\\f''(0),&r=0.\end{cases}
\]
Smooth radial functions are even at the origin, so this extension is valid.
Let \(r_n=\sqrt{2n}\).

**Theorem 1.** For every \(f\in\mathcal S_{\rm rad}(\mathbb R^8)\),
\[
\boxed{
M_f(4)=\frac1{24}\sum_{n\ge0}a_n(f+\widehat f)(r_n)
 +\frac1{432}\sum_{n\ge0}b_n\mathcal D(f+\widehat f)(r_n).
}
\tag{2}
\]
Both series converge absolutely. In particular, if \(\widehat h=h\),
\[
M_h(4)=\frac1{12}\sum_{n\ge0}a_nh(r_n)
 +\frac1{216}\sum_{n\ge0}b_n\mathcal Dh(r_n).
\tag{3}
\]

### Proof

The divisor estimate \(\sigma_1(n)\le n^2\) gives polynomial bounds for
\(a_n,b_n\) by convolution. Schwartz decay, \(r_n\asymp\sqrt n\), and
continuity of the Fourier transform on Schwartz space show that the right side
of (2) is an absolutely convergent continuous linear functional. The left side
is continuous as well: boundedness controls its integral on \([0,1]\), and any
Schwartz seminorm of order greater than four controls its tail.

It is enough to verify (2) on
\(G_\tau(r)=e^{\pi i\tau r^2}\), \(\operatorname{Im}\tau>0\).
Indeed these complex Gaussians span a dense subspace of radial Schwartz space,
as proved in [CKMRV22, Lemma 2.2]. One can also see this by approximating a
compactly supported radial function written as
\(g(|x|^2)e^{-\pi |x|^2}\): Fourier inversion for the smooth compactly supported
one-variable function \(g\), followed by Riemann sums, approximates it in every
Schwartz seminorm by complex Gaussians. Compactly supported radial functions
are dense by cutoff.

In dimension eight,
\[
\widehat G_\tau=\tau^{-4}G_{-1/\tau},\qquad
\mathcal DG_\tau=2\pi i\tau G_\tau,
\qquad M_{G_\tau}(4)=-\frac1{2\pi^2\tau^2}.
\]
Put \(X=E_2(\tau)\) and \(c=6/(\pi i)\). The standard transformation law is
\[
E_2(-1/\tau)=\tau^2(X+c/\tau).
\tag{4}
\]
The two sums in (2), with their displayed coefficients, therefore become
\[
\frac1{24}\{X^2+(X+c/\tau)^2\}
+\frac{\pi i}{216}\tau\{X^3-(X+c/\tau)^3\}.
\]
Since \(\pi i c=6\), expanding cancels both the \(X^2\) and \(X/\tau\)
terms, leaving
\[
\frac{c^2}{72\tau^2}=-\frac1{2\pi^2\tau^2}.
\]
This is precisely the Gaussian Mellin integral. Continuity and density prove
(2), and (3) follows. \(\square\)

## 2. Evaluation for the E8 magic function

Viazovska constructs eigenfunctions \(a,b\) with
\(\widehat a=a\), \(\widehat b=-b\), and
\[
f_8=\frac{\pi i}{8640}a+\frac{i}{240\pi}b.
\]
Thus its positive Fourier eigencomponent is
\[
h_8=\frac{f_8+\widehat f_8}{2}=\frac{\pi i}{8640}a.
\]
Her Propositions 2--4 and equation (38) give the following exact data:
\[
\begin{gathered}
h_8(0)=1,\qquad h_8''(0)=-\frac{21}{5},\\
h_8(\sqrt2)=0,\qquad
\frac{h_8'(\sqrt2)}{\sqrt2}=-\frac1{120},\\
h_8(r_n)=h_8'(r_n)=0\qquad(n\ge2).
\end{gathered}
\tag{5}
\]
For clarity, the quadratic coefficient follows by expanding her regularized
integral formula: its singular rational part gives
\(a(r)=-8640i/\pi+(18144i/\pi)r^2+O(r^4)\);
the regular integral is multiplied by a fourth-order zero and contributes
only \(O(r^4)\). The derivative in (5) follows from
\(a'(\sqrt2)=72\sqrt2 i/\pi\).

Substituting (5) into (3), only the origin and first radial derivative survive:
\[
M_{h_8}(4)
=\frac1{12}+\frac1{216}
 \left(-\frac{21}{5}+(-72)\left(-\frac1{120}\right)\right)
=\frac1{12}-\frac7{360}+\frac1{360}
=\frac1{15}.
\tag{6}
\]

For completeness, the radial Mellin functional equation is
\[
M_{\widehat f}(s)=\pi^{d/2-s}
\frac{\Gamma(s/2)}{\Gamma((d-s)/2)}M_f(d-s).
\tag{7}
\]
At \(s=d/2\) its scalar factor is one. Hence the midpoint functional
annihilates the negative Fourier eigenspace, and
\(M_{f_8}(4)=M_{\widehat f_8}(4)=M_{h_8}(4)\).
This proves (1). Equation (7) and the automatic midpoint equality were
already stated by Cohn and Miller; the evaluation (6) is the step supplied
by the summation formula.

The 2022 Fourier interpolation theorem also proves uniqueness of the
normalized radial Schwartz magic function. That ensures compatibility of the
usual normalized descriptions; uniqueness by itself is not used as a proof
of its Mellin value. No convergence assertion about every numerical sequence
in the 2016 paper is needed or claimed here.

## 3. A dimension-24 lift and an exact auxiliary value

Let
\[
H(\tau)=E_4(\tau)^2=E_8(\tau)
=\sum_{n\ge0}h_nq^n
=1+480\sum_{n\ge1}\sigma_7(n)q^n,
\]
where \(E_8\) in this display denotes an Eisenstein series, not a lattice.
Write
\[
HE_2^2=\sum A_nq^n,\qquad HE_2^3=\sum B_nq^n.
\]
Define a continuous linear functional on radial Schwartz functions by
\[
J_H(f)=\sum_{n\ge0}h_n
\int_{\sqrt{2n}}^\infty f(r)r(r^2-2n)\,dr.
\tag{8}
\]
Polynomial growth of \(h_n\) and Schwartz decay give absolute convergence,
including convergence after taking absolute values inside the integrals.

**Theorem 2.** In dimension 24,
\[
J_H(f)=\frac1{24}\sum_{n\ge0}A_n(f+\widehat f)(r_n)
 +\frac1{432}\sum_{n\ge0}B_n\mathcal D(f+\widehat f)(r_n).
\tag{9}
\]
In particular \(J_H\) is Fourier invariant.

**Proof.** The proof of Theorem 1 applies, since \(H(-1/\tau)=\tau^8H(\tau)\)
and \(\widehat G_\tau=\tau^{-12}G_{-1/\tau}\). Its Gaussian right side
is \(-H(\tau)/(2\pi^2\tau^2)\). The elementary substitution
\(u=r^2-2n\) gives
\[
\int_{\sqrt{2n}}^\infty G_\tau(r)r(r^2-2n)\,dr
=-\frac{q^n}{2\pi^2\tau^2},
\]
so this is also \(J_H(G_\tau)\). Absolute convergence, continuity, and Gaussian
density finish the proof. \(\square\)

Let \(h_{24}=(f_{24}+\widehat f_{24})/2\).
The construction in [CKMRV17, Section 2] gives
\[
\begin{gathered}
h_{24}(0)=1,\quad\mathcal Dh_{24}(0)=-\frac{3587}{910},\\
h_{24}(\sqrt2)=\frac1{156},\quad
\mathcal Dh_{24}(\sqrt2)=-\frac{107}{2730},\\
h_{24}(2)=0,\quad\mathcal Dh_{24}(2)=-\frac1{65520},\\
h_{24}(r_n)=\mathcal Dh_{24}(r_n)=0\quad(n\ge3).
\end{gathered}
\]
Direct multiplication of Eisenstein expansions gives
\(A_0=1,A_1=432\) and \((B_0,B_1,B_2)=(1,408,28872)\).
Consequently
\[
\begin{aligned}
J_H(f_{24})=J_H(h_{24})
&=\frac1{12}\left(1+\frac{432}{156}\right)\\
&\quad+\frac1{216}\left(-\frac{3587}{910}
-\frac{408\cdot107}{2730}-\frac{28872}{65520}\right)
=\frac{20}{91}.
\end{aligned}
\tag{10}
\]
This is a weighted tail integral identity, **not** an evaluation of
\(M_{f_{24}}(12)\). Their kernels differ. No inference equating them is valid.

## 4. A convergent real integral for the remaining midpoint

This section also independently fixes the contour normalizations. Put
\(\Delta=(E_4^3-E_6^2)/1728\), and define
\[
\Phi_8=\frac{(E_2E_4-E_6)^2}{\Delta},
\]
\[
\Phi_{24}=
\frac{25E_4^4-49E_6^2E_4+48E_6E_4^2E_2
+(-49E_4^3+25E_6^2)E_2^2}{\Delta^2}.
\tag{11}
\]
These are the positive-eigenfunction forms from [V17, equation (28)] and
[CKMRV17, equation (2.1)], respectively. Both vanish exponentially at
\(i\infty\). For \(d=8,24\), let \(p=d/4\), and set
\[
I_d=\int_{1/2}^{\infty}
 \frac{\Phi_d(-1/2+it)}{(t^2+1/4)^p}\,dt,
\qquad
K_d=\int_1^{\infty}\frac{\Phi_d(it)}{t^p}\,dt.
\tag{12}
\]
These integrals are absolutely convergent and real, since their nome is
respectively \(-e^{-2\pi t}\) and \(e^{-2\pi t}\).

The four-contour expression for the positive eigenfunction has Mellin period
\[
\begin{aligned}
P_d={}&\int_{-1}^i
 \Phi_d(-1/(z+1))(z+1)^{2p-2}z^{-p}\,dz\\
&+\int_1^i
 \Phi_d(-1/(z-1))(z-1)^{2p-2}z^{-p}\,dz\\
&-2\int_0^i\Phi_d(-1/z)z^{p-2}\,dz
+2\int_i^{i\infty}\Phi_d(z)z^{-p}\,dz.
\end{aligned}
\tag{13}
\]
Here one can choose transformed vertical paths in the first two terms.
The substitutions \(w=-1/(z+1)\), \(w=-1/(z-1)\), and \(w=-1/z\),
followed by periodicity and deformation within the upper half-plane, give
\[
P_d=-2iI_d-4iK_d.
\tag{14}
\]
For example, the first transformed kernel is
\(\Phi_d(w)/[w^p(w+1)^p]\), integrated from \(i\infty\) to
\((-1+i)/2\). The second is its translate by one. Along the downward
vertical path the product \(w(w+1)=-(t^2+1/4)\), and \(p\) is even.
The two terms involving the imaginary axis together give the second term
of (14). All endpoints at infinity decay exponentially.

The Gaussian integral
\[
\int_0^\infty e^{\pi izr^2}r^{s-1}\,dr
=\tfrac12\Gamma(s/2)(-\pi iz)^{-s/2}
\]
and the published constants of the positive eigenfunctions now give
\[
M_{f_8}(4)=\frac{-2I_8-4K_8}{17280\pi},
\qquad
M_{f_{24}}(12)=\frac{120I_{24}+240K_{24}}{113218560\pi^5}.
\tag{15}
\]
Interchanging integrals is justified directly on the transformed contours:
the exponential cusp decay of \(\Phi_d\) dominates any powers introduced by
the radial Gaussian integral. Near each original real endpoint it becomes
exponential decay in the reciprocal cusp parameter. On compact path segments,
Fubini applies without an endpoint issue.

Theorem 1 evaluates the previously unevaluated E8 period as
\(P_8=1152\pi i\), equivalently
\(I_8+2K_8=-576\pi\). The second expression in (15) remains an exact
integral representation, not a recognized constant evaluation.
Independent, non-interval numerical evaluation gives
\[
M_{f_{24}}(12)\approx
0.1778609647296502766456461262418773568.
\]
This agrees with Cohn--Miller's printed digits. It is numerical evidence only.

## 5. Why the direct scalar extension does not isolate the Leech midpoint

One tempting extension replaces \(E_2^2,E_2^3\) by \(E_2^6,E_2^7\).
After the constant and first-order anomaly terms are canceled, its remaining
polynomial is
\[
7\{X^6+(X+y)^6\}-2\frac{(X+y)^7-X^7}{y}
=35X^4y^2+70X^3y^3+63X^2y^4+28Xy^5+5y^6.
\tag{16}
\]
The lower powers do not disappear. Thus it does not produce a pure
\(\tau^{-6}\) Gaussian response, which is required for the dimension-24
midpoint.

More generally, for polynomials \(A(X),B(X)\) over a characteristic-zero field,
consider the formal matching equation
\[
A(X)+A(X+y)-\frac{12}{y}(B(X+y)-B(X))=C y^6.
\tag{17}
\]
Its constant coefficient requires \(A=6B'\). Its \(y^2\) coefficient then
is \(B'''\), so it forces \(B'''=0\). All terms of degree at least two
therefore vanish, implying \(C=0\). This proves an obstruction to this
specific coefficientwise polynomial matching ansatz. It is not an
impossibility theorem for other quasimodular, interpolation, or period methods.

## References

- [CM16] H. Cohn and S. D. Miller, *Some properties of optimal functions for sphere packing in dimensions 8 and 24*, equation (5.2), Conjecture 5.3, and the paragraph following it. [arXiv:1603.04759](https://arxiv.org/abs/1603.04759).
- [V17] M. S. Viazovska, *The sphere packing problem in dimension 8*, Annals of Mathematics 185 (2017), 991--1015. [arXiv:1603.04246](https://arxiv.org/abs/1603.04246).
- [CKMRV17] H. Cohn, A. Kumar, S. D. Miller, D. Radchenko, and M. S. Viazovska, *The sphere packing problem in dimension 24*, Annals of Mathematics 185 (2017), 1017--1033. [arXiv:1603.06518](https://arxiv.org/abs/1603.06518).
- [CKMRV22] The same authors, *Universal optimality of the E8 and Leech lattices and interpolation formulas*, Annals of Mathematics 196 (2022), 983--1082; Lemma 2.2, Theorem 1.7, and Corollary 1.8. [arXiv:1902.05438](https://arxiv.org/abs/1902.05438).
- C. Alfes, P. Kiefer, and J. Mazáč, *Measures, Modular Forms, and Summation Formulas of Poisson Type*, Communications in Mathematical Physics 406, 137 (2025). [Publisher article](https://doi.org/10.1007/s00220-025-05313-6). Related general framework; not cited as a prior evaluation of (1).
