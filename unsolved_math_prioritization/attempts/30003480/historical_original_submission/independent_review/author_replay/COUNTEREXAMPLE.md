# Binary Gram loci cannot be cut out by one polynomial inequality

**30003480 / OWR-15428-003. Complete negative candidate; independent review pending. Two substantive approaches. No priority or human peer-review claim.**

## 1. Exact source and result

For a real tensor T in (R²)^{tensor n}, let M_i(T) be its 2 by 2^{n−1} mode-i flattening and put d_i(T)=det(M_iM_i^t). The source's Gram locus is
\[
 G_n=\{(d_1(T),\ldots,d_n(T)):\|T\|_F\le1\}.
\]
It is the image of the **closed Frobenius unit ball**, not of unnormalized tensors and not merely of a fixed-rank stratum. It lies in C_n=[0,1/4]^n. Seigal's OWR report, printed p.1226, points to Conjecture1.5 in *Gram determinants of real binary tensors*, Linear Algebra Appl.544(2018),350–369. The latter conjecture, printed p.354, explicitly asks for one polynomial inequality inside C_n for n>=4.

### Theorem

For every n>=3, there is **no** real polynomial P(d_1,...,d_n) such that
\[
 G_n=\{d\in C_n:P(d)\ge0\}. \tag{1}
\]
The same impossibility holds if C_n is replaced by the known convex hull
\[
 H_n=\{d\in C_n:d_i\le\sum_{j\ne i}d_j\ \text{for every }i\}. \tag{2}
\]
Thus the answer is negative even allowing an arbitrary replacement polynomial, not just the one proposed in the source. The statement concerns a polynomial in the determinant coordinates themselves; auxiliary quantified variables and unions of polynomial regions are different descriptions. For n=2 the locus is the diagonal segment and is cut out inside C_2 by −(d_1−d_2)²>=0. For n=1 the determinant is zero and −d_1²>=0 suffices.

We also give an all-positive rational counterexample to the particular Conjecture1.5 formula in Section6. The proof of the general theorem uses only the credited marginal-eigenvalue polygon inequality, an explicit real three-factor realization, elementary polynomial multiplicities and a rank-one slice. It does not depend on the printed three-factor semialgebraic formula in Seigal's Theorem1.4.

## 2. Marginal eigenvalues: the ball normalization is essential

We first recall the polygon inequality of Higuchi–Sudbery–Szulc, *One-qubit reduced states of a pure many-qubit state: polygon inequalities*, PRL90(2003),107902, [arXiv:quant-ph/0209085v2](https://arxiv.org/abs/quant-ph/0209085v2). Its necessity applies in particular to real tensors. The short argument is included to make the input and normalization explicit.

Let a normalized real tensor have one-mode Gram matrices rho_i, all of trace1, and let lambda_i in[0,1/2] be their smaller eigenvalues. Then
\[
 \lambda_i\le\sum_{j\ne i}\lambda_j. \tag{3}
\]
For i=1, take the Schmidt decomposition
\[
 \psi=\sqrt a\,|0\rangle u+\sqrt{1-a}\,|1\rangle v,
 \quad a=\lambda_1,\quad u\perp v,\quad\|u\|=\|v\|=1.
\]
If a=0 the claim is immediate. On each remaining factor let P_j project onto the smaller-eigenvalue eigenvector, and put N=sum_{j>=2}P_j on their tensor product. If w is the product of their larger-eigenvalue eigenvectors, N>=I−|w><w|. Writing p=|<w,u>|² and q=|<w,v>|², orthonormality gives p+q<=1. Therefore
\[
 \sum_{j\ge2}\lambda_j
 \ge a(1-p)+(1-a)(1-q)
 \ge a(2-p-q)\ge a.
\]
Permutation of factors proves(3). This is the published polygon argument, not a new inequality.

Now take an arbitrary nonzero tensor in the unit ball and write s=||T||², so0<s<=1. Each unnormalized Gram matrix has trace s, determinant d_i, and smaller eigenvalue
\[
 a_s(d_i)=\frac{s-\sqrt{s^2-4d_i}}2.
\]
Applying(3) to T/sqrt(s) and multiplying by s gives a_s(d_i)<=sum_{j!=i}a_s(d_j).

Define lambda(d)=a_1(d). We claim that feasibility at **any** s<=1 forces
\[
 \lambda(d_i)\le\sum_{j\ne i}\lambda(d_j). \tag{4}
\]
Suppose instead that(4) fails for i. Then d_i is strictly larger than every other d_j, since lambda is increasing on[0,1/4]. For0<d_j<d_i and s>2sqrt(d_i),
\[
 \frac{d}{ds}\log\frac{a_s(d_j)}{a_s(d_i)}
 =\frac1{\sqrt{s^2-4d_i}}-\frac1{\sqrt{s^2-4d_j}}>0. \tag{5}
\]
Here one can compute the derivative using a_s(d)=2d/(s+sqrt(s²−4d)). Thus every ratio on the left increases with s. A zero d_j contributes zero throughout, and the endpoint s=2sqrt(d_i) follows by continuity. At s=1 the sum of the ratios is less than1, so it is also less than1 at any allowed s<=1, contradicting the necessary polygon inequality at that s. This proves(4), including zero determinants by the preceding convention. The zero tensor is immediate.

For three factors, (4) is also sufficient with a **real tensor of norm exactly one**. Given lambda_i in[0,1/2] satisfying the triangle inequalities, put
\[
 w_0=1-\tfrac12(\lambda_1+\lambda_2+\lambda_3),\quad
 w_1=\tfrac12(\lambda_2+\lambda_3-\lambda_1),
\]
\[
 w_2=\tfrac12(\lambda_1+\lambda_3-\lambda_2),\qquad
 w_3=\tfrac12(\lambda_1+\lambda_2-\lambda_3).
\]
All weights are nonnegative and sum to1; indeed w_0>=1/4. The even-parity tensor
\[
 \sqrt{w_0}|000\rangle+\sqrt{w_1}|011\rangle+
 \sqrt{w_2}|101\rangle+\sqrt{w_3}|110\rangle \tag{6}
\]
has diagonal one-mode Gram matrices with smaller eigenvalues lambda_i, hence determinants d_i=lambda_i(1−lambda_i). This is the three-qubit construction from the same prior polygon theorem, up to flipping all bits.

Consequently the exact three-factor unit-ball locus is
\[
 G_3=\{d\in C_3:\lambda(d_i)\le\lambda(d_j)+\lambda(d_k)
 \text{ for each }\{i,j,k\}=\{1,2,3\}\}. \tag{7}
\]
This equality is proved here from(3)–(6); it is not inferred from finite tensor sampling.

## 3. A polynomial multiplicity obstruction in three factors

Assume a polynomial P gives(1) for n=3. Define
\[
 F(t_1,t_2,t_3)=P(t_1(1-t_1),t_2(1-t_2),t_3(1-t_3)). \tag{8}
\]
The coordinate map in(8) is an analytic diffeomorphism from D=(0,1/2)^3 onto the interior of C_3. By(7), within D membership in G_3 is exactly the three triangle inequalities on the t_i. Moreover the polynomial F is invariant under replacing any one t_i by1−t_i.

Consider the plane
\[
 L=t_1-t_2-t_3=0
\]
and its relatively open patch t_2,t_3>0, t_2+t_3<1/2. Near any point of this patch the other two triangle inequalities are strict. Thus L<0 is inside the locus, and L>0 is outside. The defining property of P implies F>=0 on the former side and F<0 on the latter. By continuity F vanishes on the patch. A polynomial vanishing on a relatively open subset of this plane is divisible by L: after changing coordinates to(L,t_2,t_3), its constant coefficient in L vanishes on an open set and is the zero polynomial.

F is not the zero polynomial, since otherwise P vanishes on the open cube and would include every point of C_3, whereas(7) excludes, for example, sufficiently small t_2,t_3 with fixed t_1>0. Let m>=1 be the exact multiplicity of L in F. The remaining factor is not identically zero on L, so it is nonzero at some point of the open boundary patch. Crossing L there changes the sign of F. Therefore **m is odd**.

The affine involution tau(t_1,t_2,t_3)=(1−t_1,t_2,t_3) fixes F and sends L to the negative of
\[
 L'=t_1+t_2+t_3-1.
\]
It follows that L' has the same exact multiplicity m in F. But the plane L'=0 has a relatively open patch about (1/3,1/3,1/3) lying strictly inside D and all three triangle inequalities. Hence F>=0 on a full open neighborhood of that patch. Choose a point there where the residual factor after dividing by(L')^m is nonzero; such a point exists by exactness of the multiplicity. A real polynomial nonnegative on both sides of a smooth linear factor has **even** multiplicity at such a point. Thus m is even, a contradiction.

This proves that no P exists in the cube.

The same proof works if only equality within H_3 is assumed. Both patches used above map into the interior of H_3. On the first patch, put t_2=b,t_3=c,t_1=b+c. The three determinant-triangle differences are
\[
 d_2+d_3-d_1=2bc,\quad
 d_1+d_3-d_2=2c(1-b-c),\quad
 d_1+d_2-d_3=2b(1-b-c),
\]
all strictly positive. On the second patch sum t_i=1, they are2t_jt_k>0. All coordinates are strictly between0 and1/4. Therefore both sides of the required local crossings stay inside H_3, and the same parity contradiction applies.

## 4. Exact zero-determinant slices transfer the obstruction

For every n>=3,
\[
 G_n\cap\{d_4=\cdots=d_n=0\}=G_3\times\{0\}^{n-3}. \tag{9}
\]
To prove this, a zero Gram determinant means the relevant real mode flattening has rank at most1. For a nonzero tensor it therefore factors as T=S tensor u in that factor. Normalize u to length1, absorbing its norm into S. Then ||S||=||T||, and every other one-mode Gram matrix is unchanged, because contraction with the unit vector contributes a factor1. Repeat for all the zero-determinant factors. The zero tensor causes no exception. Conversely, tensor any three-factor tensor with fixed real unit vectors to obtain the reverse inclusion.

If P_n defined G_n inside C_n, restricting it to d_4=...=d_n=0 would give a polynomial definition of G_3 inside C_3, contradicting Section3. The restricted polynomial cannot evade the contradiction by being zero: that would include the entire three-dimensional cube slice. Likewise H_n intersects this face in H_3 times zero, so the strengthened version follows as well.

This proves the theorem for every n>=3 without requiring a higher-factor sufficiency theorem for the real marginal problem.

## 5. Boundary and scope distinctions

The single-polynomial assertion is ruled out even after granting the source's cube inequalities (and even its convex-hull inequalities). This is stronger than observing that a compact locus needs bounding inequalities in the ambient R^n. The obstruction is to one **additional** polynomial sign condition in the exact source domain.

It does not rule out several polynomial inequalities, Boolean combinations, radical descriptions such as(7), or descriptions with auxiliary variables. It also does not follow merely from the existence of corners or from a numerical picture. The contradiction is the exact multiplicity forced by the same irreducible linear factor after a polynomial symmetry. The higher-factor proof uses the source's closed cube, including zero-determinant tensors; no assertion about an unrelated punctured-domain reformulation is needed.

## 6. Explicit positive counterexample to the proposed polynomial

The primary paper defines
\[
 Q_1(d)=\prod_i\left(\sum_{j\ne i}d_j-d_i\right),\qquad
 Q_2(d)=\tfrac12\prod_{\epsilon\in\{\pm1\}^n}
 \left(\sum_i\epsilon_i\sqrt{d_i}\right).
\]
Its Conjecture1.5 proposes Q_1>=Q_2 inside C_n for n>=4. Take
\[
 d=(2401/10000,\ 81/625,\ 81/625,\ 1/10000).
\]
All coordinates are strictly positive and less than1/4, and every determinant-triangle inequality is strict. The square roots are(49,36,36,1)/100, so the source product can be evaluated rationally, without a numerical radical approximation. It gives
\[
 Q_1=\frac{168760917}{305175781250},\qquad
 Q_2=\frac{23632249608}{2384185791015625},
\]
\[
 Q_1-Q_2=\frac{2589624828909}{4768371582031250}>0. \tag{10}
\]
Nevertheless this point is not in G_4. The smaller eigenvalue function lambda is increasing, with inverse t->t(1−t) on[0,1/2]. Since
\[
 d_1>\tfrac25(1-\tfrac25)=\tfrac6{25},\quad
 d_2=d_3<\tfrac16(1-\tfrac16)=\tfrac5{36},\quad
 d_4<\tfrac1{100}(1-\tfrac1{100})=\tfrac{99}{10000},
\]
we have lambda(d_1)>2/5 while
\[
 \lambda(d_2)+\lambda(d_3)+\lambda(d_4)
 <\tfrac13+\tfrac1{100}=\tfrac{103}{300}<\tfrac25.
\]
This contradicts the necessary unit-ball condition(4). Thus the proposed formula fails even away from zero determinants. The general impossibility theorem in Sections3–4 is not limited to this particular Q_1−Q_2.

### An additional printed-source caution

The printed secondary inequalities in Theorem1.4 are not used as an input. As written on p.354, they have a direction that fails a direct unit GHZ check: the tensor (|000>+|111>)/sqrt2 has determinants(1/4,1/4,1/4). There Q_1=1/64, Q_2=9/512, so the first region fails, and the printed secondary pair expression is1/4>3/16. This is a concrete issue with the displayed characterization. We do not silently repair it, or use it to infer that the entire source's other results fail. The norm, source polynomials and Conjecture1.5 were visually checked in the published PDF; the argument above instead rederives the needed three-factor characterization from the earlier polygon theorem.

## 7. Provenance and verification

Primary sources: [OWR report, p.1226](https://ems.press/content/serial-article-files/46684); [Seigal's published paper, especially p.354](https://seigal.github.io/seigal2018gram.pdf); [Higuchi–Sudbery–Szulc, full three-page proof](https://arxiv.org/abs/quant-ph/0209085v2), DOI10.1103/PhysRevLett.90.107902. The polygon inequality and real parity-support construction are credited prior results. No historical-priority conclusion is inferred from the literature search.

The checker verifies exact rational tensor weights and determinants, polynomial substitution symmetries, boundary/interior identities and the positive four-factor counterexample. Finite checks do not prove an all-polynomial nonexistence claim; that claim is the multiplicity argument in Section3 and the exact slice in Section4. Separate adversarial review is required before a result PR.
