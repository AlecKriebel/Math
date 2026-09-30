# Configuration-dependent Yamabe cones: low-point topology and a four-point obstruction

**30000264 / OWR-1050-015. Scoped partial results; the general source problem remains unresolved. Two substantive approaches. Separate review pending. No historical-priority or human-peer-review claim.**

## 1. The source asks about a family

Bahri's full contribution in OWR 29/2005, printed pp.1658–1660, defines the real symmetric interaction matrix
\[
A(a)_{ii}=0,\qquad A(a)_{ij}=|a_i-a_j|^{-1}\quad(i\ne j)
\tag{1}
\]
for distinct concentration points. It then displays the negative-cone family over
\[
B_p=F_p(S^3)=\{(a_1,\ldots,a_p):a_i\ne a_j\},
\]
and, on p.1659, the ambient pair
\[
\bigl(B_p\times(\mathbb R^p\setminus\{0\}),\,S_p\bigr),
\qquad
S_p=\{(a,u):u\ne0,\ u^TA(a)u\le0\}.
\tag{2}
\]
The dataset's isolated set notation suppresses this dependence on \(a\). Diagonalizing one fixed matrix does not determine the topology asked for in the surrounding source.

The report first writes the reciprocal-distance matrix in \(\mathbb R^3\), then uses the compactified configuration space on \(S^3\). Below, the low-point statements hold for **any continuous positive off-diagonal weights** on that ordered configuration space, so no choice of spherical distance normalization affects them. The four-point example uses exactly the Euclidean reciprocal-distance matrix (1); it also realizes the usual chord-distance model on the round sphere. No quotient by permutations or by \(u\mapsto-u\) is introduced.

We retain the positive off-diagonal sign explicitly printed in the 2005 display. Bahri's later 2016 paper uses the negative interaction matrix on printed p.949. Negating a matrix exchanges its positive and negative inertia and cannot be done silently. We record both sign effects where useful, without claiming that either convention resolves the full Yamabe variational problem.

**Results obtained.**

1. The homotopy type of each individual nonpositive fiber is determined, including zero eigenvalues.
2. For \(p=2,3\), a continuous diagonal congruence gives a global product description of \(S_p\).
3. Already at \(p=4\), admissible reciprocal-distance matrices have different fiber homotopy types. The projection is consequently not a locally trivial bundle across the eigenvalue-zero locus.
4. A credited recent inequality implies regularity of the total zero boundary for \(p\le5\) in the Euclidean model; regularity does not determine its global topology.

The remaining general problem is described in §6.

## 2. Fixed fibers, with the weak inequality preserved

Let \(A\) be any real symmetric matrix, with \(r_-\), \(r_0\), \(r_+\) negative, zero and positive eigenvalues. By an invertible linear change of coordinates,
\[
u^TAu=-|x|^2+|y|^2,\qquad
x\in\mathbb R^{r_-},\quad y\in\mathbb R^{r_+},\quad
z\in\mathbb R^{r_0}.
\]
The nonpositive punctured cone is
\[
C_{\le}(A)=\{(x,y,z)\ne0:|y|^2\le|x|^2\}.
\]
The homotopy
\[
(x,y,z)\longmapsto(x,(1-t)y,z),\qquad0\le t\le1,
\tag{3}
\]
is a strong deformation retraction onto
\((\mathbb R^{r_-}\oplus\mathbb R^{r_0})\setminus\{0\}\).
It never passes through zero: if \(x=z=0\), the inequality already forces \(y=0\), which was excluded. Thus
\[
C_{\le}(A)\simeq S^{r_-+r_0-1}
\tag{4}
\]
when \(r_-+r_0>0\); otherwise the cone is empty.

For the strict cone, \(x\ne0\). Shrinking both \(y\) and \(z\), then radially normalizing \(x\), gives
\[
C_{<}(A)\simeq S^{r_--1}
\tag{5}
\]
when \(r_->0\), and the strict cone is empty otherwise. In particular, replacing \(\le0\) by \(<0\) can change the answer at a singular matrix.

When \(r_0=0\), there is a stronger explicit homeomorphism:
\[
C_{\le}(A)\cong S^{r_--1}\times(0,\infty)\times\overline B^{\,r_+},
\tag{6}
\]
obtained from \(x=r\theta,\ y=rw,\ |w|\le1\). These are elementary spectral-theorem consequences, not a solution of the configuration-dependent problem.

## 3. Complete product descriptions for two and three points

Write \(C_p=J_p-I_p\), the matrix with zero diagonal and all other entries one.

For \(p=2\), if the off-diagonal entry is \(a>0\), then
\[
A=(\sqrt a\,I_2)\,C_2\,(\sqrt a\,I_2).
\]
For \(p=3\), write
\[
A=\begin{pmatrix}0&a&b\\a&0&c\\b&c&0\end{pmatrix},
\qquad a,b,c>0.
\]
Set
\[
D=\operatorname{diag}\!\left(
\sqrt{ab/c},\sqrt{ac/b},\sqrt{bc/a}\right).
\tag{7}
\]
Then \(A=DC_3D\), since \(D_1D_2=a,\ D_1D_3=b,\ D_2D_3=c\).

For any continuous positive weight family, \(D(a)\) and its inverse are continuous. The map
\[
(a,u)\longmapsto(a,D(a)u)
\tag{8}
\]
therefore gives a homeomorphism over the base from the entire set \(S_p\) to
\(B_p\times C_{\le}(C_p)\). This is an actual global trivialization, not an unproved selection of eigenvectors.

The matrix \(C_p\) has one eigenvalue \(p-1\) and \(p-1\) eigenvalues \(-1\). Consequently,
\[
S_2\cong B_2\times S^0\times(0,\infty)\times[-1,1],
\]
\[
S_3\cong B_3\times S^1\times(0,\infty)\times[-1,1].
\tag{9}
\]
For strict cones, replace the final closed interval by an open interval. When \(p=1\), \(A=0\), so the nonpositive set is \(S^3\times\mathbb R^*\), while the strict set is empty.

For completeness, the configuration-space factors can also be simplified. Identify \(S^3\) with unit quaternions. Left multiplication by \(a_1^{-1}\) fixes the first point at \(1\); stereographic projection from \(1\) sends all remaining points into \(\mathbb R^3\). Hence
\[
F_2(S^3)\cong S^3\times\mathbb R^3,
\qquad
F_3(S^3)\cong S^3\times F_2(\mathbb R^3).
\]
The map \((x,y)\mapsto((x+y)/2,y-x)\) gives
\(F_2(\mathbb R^3)\cong\mathbb R^3\times(\mathbb R^3\setminus\{0\})\).
Thus the positive-sign source convention yields
\[
S_2\simeq S^3\times S^0,\qquad
S_3\simeq S^3\times S^2\times S^1.
\tag{10}
\]
These statements concern labelled points as in the displayed source base.

For the opposite matrix sign, the same diagonal change remains valid but the inertia reverses. In particular the \(p=3\) nonpositive fiber then has type \(S^0\), not \(S^1\). This illustrates why the two source sign conventions must be distinguished.

## 4. Four points: an exact inertia change

Let \(c,s>0\), \(c^2+s^2=1\), and take the four ordered points
\[
(c,s,0),\quad(c,-s,0),\quad(-c,s,0),\quad(-c,-s,0)
\tag{11}
\]
in \(\mathbb R^3\). Their reciprocal-distance matrix is
\[
A=\begin{pmatrix}
0&a&b&d\\
a&0&d&b\\
b&d&0&a\\
d&b&a&0
\end{pmatrix},
\qquad a=\frac1{2s},\quad b=\frac1{2c},\quad d=\frac12.
\tag{12}
\]
The four Hadamard sign vectors diagonalize it, with eigenvalues
\[
a+b+d,\quad a-b-d,\quad -a+b-d,\quad -a-b+d.
\tag{13}
\]

At \((c,s)=(4/5,3/5)\), these are
\[
\frac{47}{24},\quad-\frac7{24},\quad-\frac{17}{24},\quad-\frac{23}{24}.
\]
Thus the nonpositive fiber has homotopy type \(S^2\).

At \((c,s)=(12/13,5/13)\), they are
\[
\frac{281}{120},\quad\frac{31}{120},\quad
-\frac{151}{120},\quad-\frac{161}{120}.
\]
The nonpositive fiber now has homotopy type \(S^1\).

These are genuine distance matrices of four distinct points, not arbitrary positive symmetric matrices. The same coordinates with a fourth zero coordinate lie on the unit \(S^3\), and their chord distances are unchanged. More generally, stereographic projection \(\sigma\) satisfies
\[
|\sigma(x)-\sigma(y)|
=\frac{2|x-y|}{\sqrt{1+|x|^2}\sqrt{1+|y|^2}},
\]
so the spherical chord matrix is a positive diagonal congruence of the Euclidean one. Such a change preserves inertia and gives a fiberwise linear homeomorphism of the cones.

To see an actual wall crossing, take \(c=\cos\theta,\ s=\sin\theta\) on the interval joining the two examples, which lies in \(0<\theta<\pi/4\). The eigenvalue
\[
\lambda(\theta)=\frac1{2\sin\theta}-\frac1{2\cos\theta}-\frac12
\]
is strictly decreasing, because
\[
\lambda'(\theta)
=-\frac{\cos\theta}{2\sin^2\theta}
-\frac{\sin\theta}{2\cos^2\theta}<0.
\]
It crosses zero exactly once. The first eigenvalue stays positive and the last two stay negative. At the crossing, \((r_-,r_0,r_+)=(2,1,1)\): the weak fiber has type \(S^2\), whereas the strict fiber has type \(S^1\).

The fibers on the two sides have different reduced homology, so the projection to configurations cannot be a locally trivial topological bundle near this locus. The quotation marks around “fiber”-bundle in the report cannot be replaced by an unrestricted vector-bundle or sphere-bundle theorem.

For the opposite sign convention, the same examples instead have weak fibers of types \(S^0\) and \(S^1\). The change persists; it is not removed by a global sign reversal.

## 5. A credited boundary-regularity consequence

Chen–Ge–Jia–Lu, *On a Conjecture of Bahri–Xu* (2021), proves the relevant discrete inequality for \(p=4,5\) and arbitrary ambient dimension (Theorem 3.3), with the cases \(p\le3\) discussed earlier. In the Euclidean reciprocal-distance model this implies that
\[
F(a,u)=u^TA(a)u
\]
has no critical point on its zero set with \(u\ne0\), for \(2\le p\le5\).

Indeed, a zero of its full differential would give
\[
A(a)u=0,\qquad u^T\partial_{a_i}A(a)u=0\quad\text{for every }i.
\]
The published inequality would then have zero left side and strictly positive right side
\[
c(p,3)\sum_{i\ne j}\frac{u_j^2}{|a_i-a_j|^2},
\]
a contradiction. Therefore \(F^{-1}(0)\) is a smooth hypersurface and the total nonpositive set is a manifold with boundary in this Euclidean model. On the link \(|u|=1\), the same argument applies: the Lagrange multiplier in \(Au=\mu u\) is \(\mu=F=0\).

This is a direct consequence of a credited published theorem, not an independent proof of the discrete inequality or a claim about its strongest currently known range. A smooth total boundary is compatible with the fiber topology changing in §4, because the projection to configurations may have critical points on that boundary. It does not identify the topology of the whole set.

## 6. Exact remaining gap

The first approach reduces individual fibers and completely trivializes the \(p\le3\) families. The second tests extension of that method to general \(p\); the four-point family disproves the required constant-inertia premise.

What remains is to determine the topology of the total subset (2), or the relative pair in the source, over the entire ordered configuration space for general \(p\), including how the strata meet along eigenvalue-zero loci and near collision ends. Fiber homotopy types, chamberwise spectral subspaces and boundary regularity do not specify those gluing maps. This attempt has not constructed a global deformation, computed the relevant homology, or classified those attachments.

Accordingly the original problem remains **unsolved, 2/5**. The fixed-matrix calculation must not be promoted to a solution of the source's configuration-dependent question. The exact finite verifier supports the stated algebra, eigenvalue witnesses and deformation identities; it is not a computation of the full topology.

## References and source limitations

- A. Bahri, “Morse lemma at infinity for the sign-changing Yamabe problem,” [OWR 29/2005](https://ems.press/content/serial-article-files/46004), pp.1658–1660. Full report retrieved; the three relevant pages were visually inspected.
- A. Bahri and S. Chanillo, [The Difference of Topology at Infinity in Changing-Sign Yamabe Problems on \(S^3\) (the Case of Two Masses)](https://sites.math.rutgers.edu/~chanillo/yamabe.pdf), Comm. Pure Appl. Math. 54 (2001), 450–478. Its conditional two-mass variational analysis is distinct from a classification of (2) for arbitrary \(p\).
- A. Bahri, [Critical points at infinity in Yamabe changing-sign equations](https://www.numdam.org/item/10.1051/cocv/2016048.pdf), ESAIM COCV 22 (2016), 939–952. Full paper retrieved; its matrix on p.949 uses the opposite off-diagonal sign.
- H. Chen, J. Ge, K. Jia and Z. Lu, [On a Conjecture of Bahri–Xu](https://lu.math.uci.edu/pdfs/publications/2021-2025/66.pdf), Acta Math. Sinica (English Series) 37 (2021), 1721–1742, DOI 10.1007/s10114-021-0027-0. Full published paper retrieved; the inequality and stated \(p=4,5\) scope were checked.

The 2007 Bahri–Xu monograph was identified bibliographically, but its complete text was not retrieved from a primary source in this attempt. The literature check is bounded and is not a certificate that no later global classification exists. The elementary partial results carry no novelty claim.

