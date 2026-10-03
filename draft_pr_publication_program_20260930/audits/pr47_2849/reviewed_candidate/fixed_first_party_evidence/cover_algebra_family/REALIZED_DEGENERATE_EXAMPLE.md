# A realized target-premise degenerate rational sphere

This is an independently authored reconstruction of a known example, not a novelty claim. It verifies the false-route correction to the closing paragraph of the exact original PR47 `OBSTRUCTION.md`. The primary source is Sivek–Zentner, *A menagerie of SU(2)-cyclic 3-manifolds*, Theorem1.2, presentation(2.1), Proposition6.1 and Remark6.2, [author PDF](https://zentner.app.uni-regensburg.de/menagerie.pdf). That PDF was read temporarily and its SHA256 is `e3595453cbe70e44a6fa0f57137228218910c6c5d0223dfc9add2171e1a92f67` (461253 bytes); no foreign body is retained here.

Take the closed oriented Seifert manifold
\[
Y=S^2((3,1),(3,1),(3,2))
\]
in the source's convention. Its fundamental group has presentation
\[
G=\langle c_1,c_2,c_3,h\mid [h,c_i]=1,
c_1^3h=c_2^3h=c_3^3h^2=1,\ c_1c_2c_3=1\rangle.
\]

**Rational sphere.** The integral abelianization matrix, with columns \(c_1,c_2,c_3,h\), is
\[
M=\begin{pmatrix}3&0&0&1\\0&3&0&1\\0&0&3&2\\1&1&1&0\end{pmatrix}.
\]
Its determinant is \(-36\), and its determinantal divisors are \(1,1,3,36\). Hence
\(H_1(Y;\mathbb Z)\cong\mathbb Z/3\oplus\mathbb Z/12\), of order36. Closed orientability and Poincaré duality then imply \(Y\) is a rational homology3-sphere. The independently authored exact controls check every minor needed for these invariant factors, rather than assuming the answer from a determinant alone.

**Every SU(2) representation is abelian.** Identify SU(2) with unit quaternions. Write each noncentral element as \(\cos\theta+v\sin\theta\), with unit imaginary \(v\) and \(0<\theta<\pi\). For elements with angles \(\theta_1,\theta_2\),
\[
\operatorname{Re}(q_1q_2)=\cos\theta_1\cos\theta_2-
\langle v_1,v_2\rangle\sin\theta_1\sin\theta_2.
\]
Suppose a representation \(\rho:G\to SU(2)\) had nonabelian image. Since \(h\) is central in \(G\), \(\rho(h)\) commutes with every image element. The centralizer of a noncentral SU(2) element is a circle; if \(\rho(h)\) were noncentral, the entire image would lie in that circle. Therefore \(\rho(h)=\pm1\).

If \(\rho(h)=1\), each \(q_i=\rho(c_i)\) satisfies \(q_i^3=1\). Its angle is0 or \(2\pi/3\). If one \(q_i=1\), the product relation says the other two are inverses and they commute. Otherwise all angles are \(2\pi/3\), and \(q_1q_2=q_3^{-1}\) has real part \(-1/2\). Thus
\[
-\tfrac12=\tfrac14-\tfrac34\langle v_1,v_2\rangle,
\]
which forces \(v_1=v_2\). Then \(q_1,q_2\) commute and so does \(q_3=(q_1q_2)^{-1}\).

If \(\rho(h)=-1\), then \(q_1^3=q_2^3=-1\) and \(q_3^3=1\). A central \(q_1\) or \(q_2\) is \(-1\), and a central \(q_3\) is1; any of those cases makes all generators commute using the product relation. Otherwise the first two angles are \(\pi/3\) and the third angle is \(2\pi/3\). The identical real-part equation again forces \(v_1=v_2\). All cases contradict nonabelianity. Thus the target's universal representation premise holds, including its central and endpoint cases. This is a genuine manifold example, unlike the quartic germ.

**Nonzero normal deformation cohomology, directly.** Put \(\omega=e^{2\pi i/3}\), and choose \(\chi(c_1)=\chi(c_2)=\chi(c_3)=\omega\), \(\chi(h)=1\). This satisfies every relator and gives a noncentral abelian SU(2) representation \(\rho_\chi=\operatorname{diag}(\chi,\chi^{-1})\). For either \(a=\omega\) or \(a=\omega^2\), a rank-one cocycle has four values \((u_1,u_2,u_3,u_h)\). The commutator relations imply \((1-a)u_h=0\), so \(u_h=0\). The cube relations contribute no further restrictions because \(1+a+a^2=0\); the product relation is
\[
u_1+a u_2+a^2u_3=0.
\]
Thus the cocycle space has complex dimension2. Coboundaries span the nonzero vector \((a-1,a-1,a-1,0)\), which satisfies the relation. Hence
\[
\dim_\mathbb C H^1(Y;\mathbb C_{\chi^2})=1,
\qquad \dim_\mathbb R H^1(Y;\operatorname{ad}\rho_\chi)=2.
\]
Degree1 group cohomology equals the manifold's local-system cohomology, so no asphericity assumption is needed for this calculation. The two independent cocycle constraints and coboundary ranks are checked exactly in `exact_controls.py`.

**A relevant finite cyclic cover.** The quotient sending every \(c_i\) to1 in \(\mathbb Z/3\) and \(h\) to0 corresponds to the regular torus cover of the base orbifold \(S^2(3,3,3)\). It is exactly the kernel of \(\chi^2\), hence an adjoint-kernel cover permitted by the definition of cyclic finiteness. One construction is \(T^2=\mathbb C/(\mathbb Z+\mathbb Z\omega)\), on which multiplication by \(\omega\) has order3 and three fixed points; its quotient orbifold is \(S^2(3,3,3)\). Pulling back the Seifert fibration yields a regular3-fold manifold cover \(\widetilde Y\to Y\), a circle bundle over \(T^2\). The source's Euler-number convention gives \(e(Y)=-4/3\) and \(e(\widetilde Y)=-4\). The circle-bundle presentation has abelianization \(\mathbb Z^2\oplus\mathbb Z/4\), so \(b_1(\widetilde Y)=2\). This agrees with the two nontrivial rank-one eigensummands of dimension1 and zero invariant eigensummand.

Consequently, the general claim that every target-premise reducible has zero normal cohomology is **false**. The example establishes neither the value of \(I^\#(Y)\) nor a counterexample to KP3.51. It only makes the correct remaining route precise: any general proof must control actual degenerate reducible Floer data, or use other information that bypasses that control; it cannot first prove universal cyclic finiteness.
