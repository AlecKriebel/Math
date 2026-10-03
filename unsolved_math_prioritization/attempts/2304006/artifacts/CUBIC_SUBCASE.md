# The sharp complex cubic subcase

## Result and scope

For physicists' Hermite polynomials,
\[
H_1(z)=2z,\qquad H_2(z)=4z^2-2,\qquad H_3(z)=8z^3-12z,
\]
every polynomial
\[
P(z)=1+H_1(z)+aH_2(z)+bH_3(z),\qquad a,b\in\mathbb C,
\]
has a zero in the closed strip
\[
|\operatorname{Im}z|\le c_3,
\qquad
c_3=\frac{\sqrt3}{2}\sqrt{1+u^2}
   =0.9036697472260109\ldots,
\tag{1}
\]
where \(u\) is the unique positive root of
\[
4u^3+3u-1=0.
\tag{2}
\]
The constant \(c_3\) is optimal for this cubic family.

This is a rigorous complex-coefficient special case and an exact lower bound on any universal constant in the full sparse-Hermite problem. **The global question for arbitrary \(2\le n<m\) remains unresolved by this argument.** No assertion of novelty or literature priority is made.

## 1. Root-coordinate identity

Suppose first that \(b\ne0\), and write
\[
P(z)=K(z-r_1)(z-r_2)(z-r_3),\qquad K=8b\ne0.
\]
Let \(s_1=r_1+r_2+r_3\), \(s_2=r_1r_2+r_1r_3+r_2r_3\), and \(s_3=r_1r_2r_3\). The ordinary-power expansion is
\[
P(z)=8bz^3+4az^2+(2-12b)z+(1-2a).
\]
Coefficient comparison gives
\[
-Ks_1=4a,\qquad Ks_2=2-\frac32K,\qquad -Ks_3=1+\frac12Ks_1.
\]
Consequently
\[
2s_3+s_2+s_1+\frac32=0.
\tag{3}
\]
Set \(w_j=2r_j+1\). Substituting \(r_j=(w_j-1)/2\) into (3) yields
\[
F(w_1,w_2,w_3):=w_1w_2w_3+w_1+w_2+w_3+2=0.
\tag{4}
\]
This identity is valid with repeated roots.

## 2. Excluding mixed upper/lower configurations

We first prove an elementary fact about (4). If
\[
w_1=x+iy,\qquad w_2=v+it,\qquad y,t>\sqrt2,
\]
then \(w_3\) has positive imaginary part.

Indeed, \(|w_1w_2|\ge yt>2\), so the denominator below cannot vanish, and (4) gives
\[
w_3=-\frac{w_1+w_2+2}{w_1w_2+1}.
\]
Multiplying by the conjugate of the denominator and collecting terms gives the exact identity
\[
\operatorname{Im}w_3
=
\frac{t(x+1)^2+y(v+1)^2+(y+t)(yt-2)}{|w_1w_2+1|^2}>0.
\tag{5}
\]
Complex conjugation proves the corresponding lower-half-plane statement.

Now suppose, for contradiction, that all three roots satisfy
\[
|\operatorname{Im}r_j|>c_3.
\tag{6}
\]
Then \(|\operatorname{Im}w_j|>2c_3>\sqrt2\). By the pigeonhole principle, two of the three \(w_j\) lie in the same upper or lower half-plane. After conjugating the whole identity (4), if necessary, assume two lie in the upper half-plane. Formula (5) forces the third into the upper half-plane too. Applying (6) again, all three lie in the same open half-plane
\[
D=\{w:\operatorname{Im}w>2c_3\}.
\tag{7}
\]

## 3. A self-contained half-plane polarization lemma

The next elementary lemma supplies the only consequence of the Grace–Walsh–Szegő theorem needed here. It is proved below, so the cubic result does **not** depend on accepting that theorem externally.

**Lemma.** Let \(h\in\mathbb R\), \(N\ge1\), and let \(f\ne0\) be a polynomial of degree \(d\le N\) having no zero in \(D_h=\{w:\operatorname{Im}w>h\}\). For \(\zeta\in D_h\), the polynomial
\[
g(w)=f(w)+\frac{\zeta-w}{N}f'(w)
\tag{8}
\]
also has no zero in \(D_h\), and its degree is at most \(N-1\).

**Proof.** If \(d=0\), this is immediate. Otherwise factor
\(f(w)=A\prod_{j=1}^d(w-\alpha_j)\), with \(\operatorname{Im}\alpha_j\le h\).
Suppose \(w\in D_h\) and \(g(w)=0\). Since \(f(w)\ne0\), put
\[
S=\frac{f'(w)}{f(w)}=\sum_{j=1}^d\frac1{w-\alpha_j}.
\]
Equation (8) implies \(S\ne0\) and
\(\zeta=w-N/S\).
Write \(y=\operatorname{Im}w-h>0\). Each summand satisfies
\[
-\operatorname{Im}\frac1{w-\alpha_j}
=\frac{\operatorname{Im}(w-\alpha_j)}{|w-\alpha_j|^2}
\ge \frac{y}{|w-\alpha_j|^2}.
\]
Summing and applying Cauchy–Schwarz gives
\[
-\operatorname{Im}S
\ge y\sum_{j=1}^d\frac1{|w-\alpha_j|^2}
\ge \frac{y}{d}|S|^2.
\]
Therefore
\[
\operatorname{Im}\frac{N}{S}
=\frac{-N\operatorname{Im}S}{|S|^2}
\ge \frac{Ny}{d}\ge y.
\]
It follows that
\(\operatorname{Im}\zeta=\operatorname{Im}w-\operatorname{Im}(N/S)\le h\), a contradiction. Finally, if \(d=N\), the leading coefficient in (8) cancels; if \(d<N\), its degree is already at most \(N-1\). ∎

## 4. Applying the lemma to the diagonal cubic

The diagonal of (4) is
\[
f(w)=F(w,w,w)=w^3+3w+2.
\]
Equation (2) gives the factorization
\[
f(w)=(w+2u)\bigl(w^2-2uw+3+4u^2\bigr).
\]
Its roots are
\[
-2u,\qquad u\pm i\sqrt{3+3u^2}.
\tag{9}
\]
By (1), the largest imaginary part among them is \(2c_3\). Thus \(f\) has no zero in the open half-plane \(D\) in (7).

Apply the lemma with \(N=3\) and \(\zeta=w_1\). It gives a polynomial with no zero in \(D\):
\[
g_1(w)=f(w)+\frac{w_1-w}{3}f'(w)
      =w_1w^2+2w+w_1+2
      =F(w_1,w,w).
\]
Apply it again to \(g_1\), now with \(N=2\) and \(\zeta=w_2\). We obtain
\[
g_2(w)=g_1(w)+\frac{w_2-w}{2}g_1'(w)
      =w_1w_2w+w+w_1+w_2+2
      =F(w_1,w_2,w),
\]
which also has no zero in \(D\). But \(w_3\in D\) and (4) asserts \(g_2(w_3)=0\), a contradiction. This proves the upper bound in (1) for \(b\ne0\).

## 5. Degenerate quadratic boundary

If \(b=a=0\), the zero is \(-1/2\). If \(b=0\) and \(a\ne0\), write
\[
P(z)=4a(z-r_1)(z-r_2).
\]
Coefficient comparison gives
\[
r_1+r_2=-\frac1{2a},\qquad
r_1r_2=\frac1{4a}-\frac12.
\]
Hence
\[
(r_1+1/2)(r_2+1/2)=-1/4.
\tag{10}
\]
At least one factor in (10) has modulus at most \(1/2\). The associated root satisfies
\[
|\operatorname{Im}r_j|\le|r_j+1/2|\le1/2<c_3.
\]
The quadratic bound \(1/2\) is sharp: with \(a=(1+i)/4\),
\[
1+2z+a(4z^2-2)=(1+i)(z+1/2-i/2)^2.
\]

## 6. Sharpness of the cubic constant

Take
\[
r=-\frac12+\frac{u}{2}+i\frac{\sqrt3}{2}\sqrt{1+u^2},
\qquad
K=\frac1{\frac34+\frac32r^2},
\qquad
a=-\frac{3rK}{4},\qquad b=\frac K8.
\tag{11}
\]
Here \(2r+1\) is the upper nonreal root in (9), so
\[
4r^3+6r^2+6r+3=0.
\tag{12}
\]
The denominator in (11) is nonzero: \(\operatorname{Re}r<0\) and \(\operatorname{Im}r>0\), so \(r^2\) is not real. Definition (11) ensures that the cubic, quadratic and linear coefficients in
\(1+2z+aH_2(z)+bH_3(z)\) equal those in \(K(z-r)^3\). For the constant coefficient, the needed identity is
\[
1+\frac32rK=-Kr^3,
\]
which follows by multiplying (12) by \(K/4\) and using \(K(3/4+3r^2/2)=1\). Thus
\[
1+2z+aH_2(z)+bH_3(z)=K(z-r)^3.
\tag{13}
\]
All three zeros therefore have imaginary part exactly \(c_3\), proving sharpness.

For a radical form, real cube roots give
\[
u=\frac12\left(\sqrt[3]{1+\sqrt2}+\sqrt[3]{1-\sqrt2}\right).
\]

## 7. Primary theorem reference and dependency record

The conceptual coincidence principle is stated as Theorem 11, pp. 478–479, in Julius Borcea and Petter Brändén, “Pólya-Schur master theorems for circular domains and their boundaries,” *Annals of Mathematics* **170** (2009), 465–492, DOI [10.4007/annals.2009.170.465](https://doi.org/10.4007/annals.2009.170.465), [publisher PDF](https://annals.math.princeton.edu/wp-content/uploads/annals-v170-n1-p14-p.pdf#page=16).

That theorem applies to a symmetric multiaffine complex polynomial and a circular domain, with the additional hypothesis that the polynomial has full total degree or the domain is convex. It asserts a coincident diagonal point in the same domain with the same polynomial value. Definition 4 on p. 473 explicitly includes open affine half-planes. Here both extra hypotheses hold: \(F\) has degree three and \(D\) is convex.

The published theorem and its domain definition were checked directly in the publisher PDF. That paper cites the classical theorem rather than providing a proof at that point. Accordingly, Sections 3–4 above give a complete elementary proof of the special half-plane nonvanishing consequence actually used; the bibliography is context, not an unproved dependency. In particular, the strict open-half-plane issue and the possibility of a degree drop in a polar derivative are both addressed explicitly.

## What does not generalize automatically

The decisive cubic-specific input is the root identity (4) and its sign formula (5). A half-plane coincidence theorem alone does not handle the disconnected complement of a horizontal strip. For larger sparse-Hermite degrees, ruling out configurations with roots in both distant half-planes would require a new argument. The proof here supplies neither a universal upper bound for all \(n,m\) nor a counterexample to the full statement.
