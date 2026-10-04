# The sharp area constant in Function Theory Problem 6.88

## Result and scope

For every normalized univalent holomorphic map
\[
f(z)=z+a_2z^2+\cdots\quad(z\in\mathbb D),\qquad A=\operatorname{area}f(\mathbb D)<\infty,
\]
the largest universal constant in
\[
|a_2|\le 2-cA^{-1/2}
\]
is
\[
\boxed{c=\sqrt{27\pi/8}}. \tag{1}
\]
This is a consequence of the published minimum-area theorem of Dov Aharonov, Harold S. Shapiro and Alexander Yu. Solynin (1999; alternate proof 2006), not a new solution. An especially simple sharpness witness is \(f(z)=z+z^2/2\).

The accompanying existence assertion involving boundary length also holds: when \(\ell=\mathcal H^1(\partial f(\mathbb D))<\infty\), one may take
\[
c_1=2\sqrt\pi\,c=\pi\sqrt{27/2}
\quad\text{in}\quad |a_2|\le 2-c_1/\ell. \tag{2}
\]
No optimality of this particular perimeter constant is claimed. The original Problem 6.88 explicitly asks for the best area constant, then states a perimeter existence conjecture. A stronger, separate question asking for the sharp perimeter constant is not settled here.

## 1. Published theorem used

Put \(a=|a_2|\). The Aharonov–Shapiro–Solynin theorem gives the exact minimum image area
\[
M(a)=\begin{cases}
\pi(1+2a^2),&0\le a\le 1/2,\\
\displaystyle\frac{27\pi}{8(2-a)^2},&1/2<a<2.
\end{cases} \tag{3}
\]
The theorem is stated as Theorem 4, printed p. 109, using the two branches of (4.10) in Theorem 3, p. 106, of:

D. Aharonov, H. S. Shapiro and A. Yu. Solynin, *Minimal area problems for functions with integral representation*, J. Analyse Math. **98** (2006), 83–111, [DOI](https://doi.org/10.1007/BF02790271), [author-posted text](https://www.academia.edu/31230874/Minimal_area_problems_for_functions_with_integral_representation).

That paper attributes the solution to the same authors' *A minimal area problem in conformal mapping*, J. Analyse Math. **78** (1999), 157–176, [DOI](https://doi.org/10.1007/BF02791132). The 1999 full proof was not obtained. The 2006 statement and proof were read in public author-posted OCR. Equation (3) is a published external theorem input to the short deduction below, rather than something established by numerical tests.

For a fuller analytic derivation at the level of classical representation and circular-symmetrization theorems, see the project's earlier [prescribed-coefficient proof](https://github.com/AlecKriebel/Math/blob/54f5bfe3cde5da6778bbd20e373fc433a7ed45fe/unsolved_math_prioritization/attempts/2306017/PROOF.md), Section 2 for the typically-real Dirichlet-energy bound and Section 3 for passage to all univalent functions. Its [repaired audit](https://github.com/AlecKriebel/Math/blob/54f5bfe3cde5da6778bbd20e373fc433a7ed45fe/unsolved_math_prioritization/attempts/2306017/audit/REPAIR_AUDIT_PASS.md) supersedes, without erasing, its [original unsuccessful audit](https://github.com/AlecKriebel/Math/blob/54f5bfe3cde5da6778bbd20e373fc433a7ed45fe/unsolved_math_prioritization/attempts/2306017/audit/ORIGINAL_AUDIT_NOT_PASSED.md). The repaired argument uses ordinary conformal radius and a negative slit; the disputed biangle comparison is not needed. No full-class equality classification from that earlier reconstruction is needed here.

## 2. Universal lower bound for the constant functional

Bieberbach's second-coefficient theorem gives \(a\le2\). Equality forces a rotated Koebe map, whose area is infinite, so here \(0\le a<2\). Since \(A\ge\pi>0\), the desired bound is equivalent to
\[
(2-a)^2 A\ge 27\pi/8. \tag{4}
\]

If \(1/2<a<2\), equation (4) follows immediately from the second branch of (3).

If \(0\le a\le1/2\), the area identity
\[
A=\pi\sum_{n\ge1}n|a_n|^2\ge\pi(1+2a^2)
\]
and the exact polynomial identity
\[
(2-a)^2(1+2a^2)-\frac{27}{8}
=\frac{(1-2a)^3(5-2a)}8\ge0 \tag{5}
\]
prove (4). This proof includes \(a=0\) and \(a=1/2\); neither an endpoint limit nor a restriction to positive coefficients is being silently imposed. The area identity follows by integrating the power series of \(f'\) on disks of radius \(r<1\), using orthogonality, and then letting \(r\uparrow1\).

Taking the nonnegative square root of (4) proves the inequality with the constant (1).

## 3. Sharpness, and explicit attaining examples

Let \(q(z)=z+z^2/2\). If \(q(z)=q(w)\), then
\[
(z-w)\left(1+\frac{z+w}{2}\right)=0.
\]
For distinct \(z,w\in\mathbb D\), the second factor cannot vanish because \(|z+w|<2\). Thus \(q\in S\). It has
\[
a=1/2,\qquad A(q)=\pi(1+2/4)=3\pi/2,
\]
so
\[
(2-a)\sqrt{A(q)}=\frac32\sqrt{3\pi/2}=\sqrt{27\pi/8}.
\]
Any constant larger than (1) therefore fails for this single bounded-image map. Together with Section 2, this proves optimality.

There are also explicit attaining maps for every \(1/2<a<2\). Set
\[
\tau=\tfrac23(2-a),\quad k(z)=\frac{z}{(1-z)^2},\quad
p_\tau(z)=k^{-1}(\tau k(z)),\quad F_\tau(z)=\frac{q(p_\tau(z))}{\tau}. \tag{6}
\]
The inverse branch fixes zero. Since \(k\) maps \(\mathbb D\) onto \(\mathbb C\setminus(-\infty,-1/4]\), the range of \(p_\tau\) is a disk with a terminal negative radial slit removed. Hence \(F_\tau\) is univalent. The defining equation gives
\[
p_\tau(z)=\tau z+2\tau(1-\tau)z^2+O(z^3),\qquad
F_\tau(z)=z+(2-3\tau/2)z^2+O(z^3).
\]
The removed segment and its polynomial image have area zero. Consequently
\[
A(F_\tau)=\tau^{-2}A(q)=\frac{3\pi}{2\tau^2}
=\frac{27\pi}{8(2-a)^2}.
\]
This supplies attaining maps and independently fixes the denominator 8. It does not classify all equality cases. Rotating the maps in the normalized way realizes the corresponding complex second coefficients.

In particular, at \(a=1\), the constructed map has area \(27\pi/8\). Therefore the denominator 7 displayed in the 1999 publisher's HTML abstract is not a valid stronger lower bound; it conflicts with an explicit map. The proof uses the 2006 theorem and independently verified normalization, not that corrupted abstract formula.

## 4. The perimeter addendum

Write \(\Omega=f(\mathbb D)\). For finite boundary length \(\ell=\mathcal H^1(\partial\Omega)\), the planar isoperimetric inequality gives
\[
4\pi A\le\ell^2. \tag{7}
\]
For a Jordan domain this is the classical rectifiable-curve inequality. For a general open set with finite area and finite topological-boundary length, use its finite-perimeter form \(4\pi|\Omega|\le P(\Omega)^2\) together with \(P(\Omega)\le\mathcal H^1(\partial\Omega)\). These are standard geometric-measure versions of the same classical theorem. If boundary length is instead counted with multiplicity along a conformal boundary trace, that length is no smaller, so (7) remains sufficient.

Combining (1) with (7),
\[
2-a\ge\frac{\sqrt{27\pi/8}}{\sqrt A}
\ge\frac{2\sqrt\pi\sqrt{27\pi/8}}\ell
=\frac{\pi\sqrt{27/2}}\ell.
\]
This proves (2). For \(\ell=\infty\), interpreting \(1/\ell=0\) reduces the statement to Bieberbach's inequality. No finite-length hypothesis was needed for the area result. The perimeter deduction proves existence, not the sharp perimeter problem discussed separately on p. 109 of the 2006 paper.

## Conclusion and verification limits

The exact area question is already solved by the published theorem; the stated perimeter existence addendum is its elementary isoperimetric consequence. The 2018 catalogue update is stale. This item shares its decisive theorem with catalogue ID 2306017 and must not be counted as a separate discovery.

The reproducible controls check rational algebra, endpoint normalization and negative controls. They do not prove the external minimum-area or isoperimetric theorem, authenticate OCR, or replace independent review. The present proof is a complete mathematical deduction from explicitly identified published/classical theorem inputs.
