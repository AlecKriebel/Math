# E-6322, pass 2: anisotropic stationarity obstruction

Date: 2026-10-16. The frozen E-6322 density, coefficients, full comparison class, and boundary-data requirements are unchanged.

## Result and status

**No full-class singular minimizer or counterexample has been constructed.** The result here excludes a weighted-homogeneous candidate family whose leading positive-energy and inverse-determinant energies can have matching radial powers. The exclusion uses a necessary Euler equation on compact subsets away from the singular point. It does not assume the Euler equation is valid across that point.

Unlike the affine-sphere examples in pass 1, the angular data in this result may be nonaffine, and the traces on small spheres need not be affine.

## 1. Candidate and exact hypotheses

After translating the reference and target origins, consider an exact core

\[
y_i(r\theta)=r^{\alpha_i}\phi_i(\theta),\quad i=1,2,3,\qquad
0<r<1,\quad \theta\in S^2,
\]

with

\[
0<\alpha_1\le\alpha_2\le\alpha_3,\qquad
\phi\in C^2(S^2;\mathbb R^3).
\]

Let \(p_i=\nabla y_i\) be the rows of \(Dy\). Their exact scaling is

\[
p_i(r\theta)=r^{\alpha_i-1}A_i(\theta),\qquad
A_i=\alpha_i\phi_i\theta+\nabla_S\phi_i.
\]

Put

\[
s=\alpha_1+\alpha_2+\alpha_3,\quad \gamma=s-3,\quad
j(\theta)=\det\begin{pmatrix} A_1(\theta)\\ A_2(\theta)\\ A_3(\theta)\end{pmatrix}.
\]

Assume

\[
\gamma>0,\qquad j(\theta)>0\quad\text{for every }\theta\in S^2.
\]

Thus \(J=\det Dy=r^\gamma j(\theta)\), and \(\min_{S^2}j>0\). Admissibility in the frozen energy is ensured by

\[
\alpha_1>1/2,\qquad s<9/2.
\]

These sufficient bounds follow from \(|Dy|^6\le C r^{6\alpha_1-6}\), \(J^{-2}\le C r^{-2\gamma}\), and the inequality \(|\operatorname{cof}F|^3\le C|F|^6\). The nonstationarity proof below itself only needs the core smoothness, positive angular determinant, and the strict exponent inequality stated next.

## 2. Main exclusion lemma

**Lemma.** Under the hypotheses above, if

\[
\eta:=2(3\alpha_1+\alpha_2+2\alpha_3-6)>0,
\]

then the map cannot satisfy the benchmark Euler–Lagrange equation on the punctured core. Consequently, no admissible full-class local or global minimizer can have this exact core.

The last implication is justified entirely away from the origin: a sufficiently small compactly supported additive variation inside the punctured core preserves positive determinant and finite energy, since the candidate is \(C^2\) there and its determinant has a positive minimum on the support. Local minimality therefore implies the classical Euler equation on every such compact subset.

### 2.1 A ray where the two lower-exponent components vanish

First, \(\phi(\theta)\ne0\) for every \(\theta\). If all three components vanished, the radial column of the derivative would vanish there, contradicting \(j>0\). The map extends continuously to \(y(0)=0\), and the origin is its only zero.

There exists \(\theta_0\in S^2\) such that

\[
\phi_1(\theta_0)=\phi_2(\theta_0)=0.
\]

Here is a degree argument spelling out the existence. Let \(\delta=\min_{S^2}|\phi|>0\). The degree \(\deg(y,B_1,z)\) is constant for \(|z|<\delta\). Choose a nonzero point \(x\) sufficiently close to the origin that \(0<|y(x)|<\delta\), and set \(z=y(x)\). Its preimage is compact in the punctured ball and consists of finitely many regular points, because the Jacobian is positive everywhere in that punctured ball. The degree is the number of those points, hence at least one. The same nonzero degree holds at \(z=(0,0,t)\) for \(0<|t|<\delta\), so such a point has a preimage \(r\theta_0\). The first two components of that preimage equation give the desired zeros of \(\phi_1,\phi_2\).

At this angle,

\[
p_1\cdot\theta_0=p_2\cdot\theta_0=0.
\]

Their cross product is nonzero, because \(J>0\). Consequently, with a nonzero constant \(\kappa\),

\[
C_3:=p_1\times p_2
=\kappa r^{\alpha_1+\alpha_2-2}\theta_0
\quad\text{along this ray.}
\]

### 2.2 Exact barrier contribution to the third Euler equation

The third row of the first Piola stress contributed by \(dJ^{-2}\) is

\[
P^{\rm bar}_3=-2dJ^{-3}C_3.
\]

Since \(\operatorname{div}C_3=0\),

\[
\operatorname{div}P^{\rm bar}_3
=6dJ^{-4}C_3\cdot\nabla J.
\]

On the chosen ray the cross product is radial, so only the radial derivative of \(J\) contributes. With \(j_0=j(\theta_0)>0\),

\[
\operatorname{div}P^{\rm bar}_3(r\theta_0)
=6d\kappa\gamma j_0^{-3}
 r^{\alpha_1+\alpha_2-3-3\gamma}.
\]

Its coefficient is nonzero. This is an exact identity, not merely an upper bound.

### 2.3 Bound for the entire positive part

Let

\[
H(F)=a|F|^6+b|\operatorname{cof}F|^3+c(\det F)^2.
\]

For \(0<r<1\), the ordering of exponents and \(C^2\) angular regularity imply

\[
\operatorname{div}P^+_3(r\theta)=O(r^{4\alpha_1+\alpha_3-6}),
\qquad P^+_3=\frac{\partial H}{\partial p_3}(Dy).
\]

For clarity, the three terms can be checked separately:

- For \(a|F|^6\), \(P^+_3=6a|F|^4p_3\). Its divergence is \(O(r^{4\alpha_1+\alpha_3-6})\).
- Write the cofactor rows as \(C_1=p_2\times p_3\), \(C_2=p_3\times p_1\), \(C_3=p_1\times p_2\). Differentiation with respect to \(p_3\) involves only \(C_1,C_2\). Since \(|\operatorname{cof}Dy|=O(r^{\alpha_1+\alpha_2-2})\), its stress divergence is \(O(r^{3\alpha_1+\alpha_2+\alpha_3-6})\), which obeys the displayed common bound because \(\alpha_2\ge\alpha_1\).
- For \(cJ^2\), the third stress row is \(2cJC_3\). Its divergence is \(O(r^{2\alpha_1+2\alpha_2+\alpha_3-6})\), again no larger than the common bound.

The same bounds hold for derivatives because differentiating a smooth angular factor or a radial power loses at most one radial power. Positive angular determinant also keeps the relevant cofactor row nonzero; no differentiation of a norm at its zero is needed in this calculation.

### 2.4 Contradiction

The positive-minus-barrier divergence exponent is

\[
(4\alpha_1+\alpha_3-6)
-(\alpha_1+\alpha_2-3-3\gamma)
=2(3\alpha_1+\alpha_2+2\alpha_3-6)=\eta.
\]

When \(\eta>0\), divide the third Euler equation on the chosen ray by \(r^{\alpha_1+\alpha_2-3-3\gamma}\) and let \(r\downarrow0\). The positive contribution tends to zero, while the barrier contribution tends to the nonzero constant \(6d\kappa\gamma j_0^{-3}\). This contradiction proves the lemma. \(\square\)

## 3. Balanced scaling is excluded

A natural attempted singular balance matches

\[
6\alpha_1-6=-2\gamma,
\quad\text{equivalently}\quad
s+3\alpha_1=6.
\]

Because \(s>3\), this forces \(\alpha_1<1\). Moreover, \(\alpha_3>\alpha_1\): equality of the smallest and largest exponents would force all three equal, and the balance would then give \(\alpha_1=1\), contradicting \(s>3\).

Under this balanced relation,

\[
\eta=2(\alpha_3-\alpha_1)>0.
\]

Therefore the preceding lemma excludes every admissible exact weighted-homogeneous candidate with these hypotheses and matching dominant energy powers, including nonaffine angular data.

For the frequently tempting exponents \((3/4,3/4,9/4)\),

\[
\gamma=3/4,\quad
\operatorname{div}P^{\rm bar}_3\text{ has exponent }-15/4,\quad
\operatorname{div}P^+_3=O(r^{-3/4}),\quad\eta=3.
\]

Matching energy powers does not match the independent component equations. The slowly varying third component sees a dominant barrier pressure with no positive-energy term at the same order.

## 4. Limits and remaining gap

This is an obstruction, not a counterexample or a proof of E-6322. It relies on an exact weighted-homogeneous core, \(C^2\) angular data, strictly positive angular Jacobian, and the exponent condition \(\eta>0\). It does not cover:

- angular Jacobians that vanish, with lower-order terms restoring positive actual determinant;
- genuinely nonhomogeneous singular cores without a controlled asymptotic expansion;
- weighted cores with \(\eta\le0\);
- singularities occurring only at the boundary;
- or irregular minimizers for which no such core representation is known.

A full counterexample would still require a smooth diffeomorphically compatible full boundary trace, an admissible minimizer, and a rigorous comparison against every finite-energy Sobolev competitor. No calibration accomplishing that has been found. Conversely, these exclusions are far too narrow to imply the benchmark's global determinant lower bound.
