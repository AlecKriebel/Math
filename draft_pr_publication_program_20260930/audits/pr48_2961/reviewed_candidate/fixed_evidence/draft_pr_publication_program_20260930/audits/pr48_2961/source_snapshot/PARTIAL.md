# Four-manifold diffeomorphism groups: transfer obstructions

**KP-4.85 remains unresolved.** This note gives a source correction and two concrete obstructions to transferring known quasimorphisms to the required group. Its main estimate is a consequence of classical commutator compression, not a claimed new discovery. Separate adversarial AI review passed; see [the report](review/REVIEW.md). This has not undergone human peer review.

## 1. The full target

The question asks for a closed orientable smooth four-manifold \(X\) such that
\[
\sup_{f\in G}\operatorname{cl}_G(f)=\infty,
\qquad G=\operatorname{Diff}^{\infty}_0(X).
\tag{1}
\]
Here \(G\) is the full identity component, and \(\operatorname{cl}_G\) counts commutators whose two factors lie in \(G\). By Mather–Thurston perfectness, every element has finite commutator length; the question is whether the lengths have a uniform bound. We use \([a,b]=aba^{-1}b^{-1}\), with composition acting on the rightmost argument first.

The target is stated in K3, Problem 4.85, pp.259–260 [K3]. It is also exactly Question 3 on p.489 of Webb's Oberwolfach report [W20], corresponding to the duplicate dataset record 30004403 / OWR-17471-009. These are one mathematical target, not two independent problems.

If disconnected manifolds are admitted by the word “manifold,” it suffices to consider a connected component: a compact manifold has finitely many components, its identity component of diffeomorphisms is the product of their identity components, and commutator length in a finite direct product of perfect groups is the maximum of the component lengths. The reverse inequality follows by padding shorter factorizations with trivial commutators.

Neither an unbounded norm on a subgroup, nor unbounded commutator length in a universal covering group, is by itself (1). The same caution applies to fragmentation length.

## 2. A known four-dimensional class omitted by an overbroad remark

Tsuboi's published Theorem 1.1(2) states that an even-dimensional compact manifold admitting a handle decomposition without middle-index handles has commutator width at most four in the smooth identity component [T12, p.142]. It applies in dimension four whenever there are no 2-handles. The regularity restriction \(r\ne\dim X+1\) poses no issue for \(r=\infty\).

For example, \(S^1\times S^3\) has a Morse function with one critical point in each of indices \(0,1,3,4\), obtained by summing Morse functions with two critical points on the two factors. Thus
\[
\operatorname{cl}_{\operatorname{Diff}_0(S^1\times S^3)}(f)\le4
\quad\text{for every }f.
\tag{2}
\]
The standard connected-sum handle construction similarly gives \(\#_k(S^1\times S^3)\) a decomposition with counts \((1,k,0,k,1)\), so the same theorem applies.

Consequently, the K3 remark that only \(S^4\) is understood in dimension four needs qualification. The original Oberwolfach discussion already explicitly records the no-2-handle class [W20, p.488]. This is a correction to the breadth of that remark, not a resolution of the existence question. We do not infer a no-2-handle decomposition merely from the vanishing of \(H_2(X)\).

## 3. Classical compression on a product with an open disk

We recall the algebra behind the portable-manifold bound of Burago–Ivanov–Polterovich [BIP, Theorems 1.18 and 2.2(i)]. This also makes the precise ambient groups in the next section explicit.

**Lemma 1 (commutator compression).** Let \(H\le G\), and suppose the subgroups \(H,FHF^{-1},\ldots,F^mHF^{-m}\) commute pairwise. If
\[
h=c_1\cdots c_m,\qquad c_i=[a_i,b_i],\quad a_i,b_i\in H,
\]
then \(\operatorname{cl}_G(h)\le2\).

**Proof.** Write \(T(g)=FgF^{-1}\) and
\[
A=\prod_{i=1}^mT^i(a_i),\quad
B=\prod_{i=1}^mT^i(b_i),\quad
s_i=c_{i+1}\cdots c_m\ (0\le i<m),\quad
C=\prod_{i=0}^{m-1}T^i(s_i).
\]
All products are in increasing index order. Different conjugate subgroups commute, so
\[
[A,B]=\prod_{i=1}^mT^i(c_i).
\]
Computing \(C\,T(C^{-1})\) component by component gives \(s_0=h\) in \(H\), \(s_i s_{i-1}^{-1}=c_i^{-1}\) in component \(T^i(H)\) for \(1\le i<m\), and \(s_{m-1}^{-1}=c_m^{-1}\) in the last component. Therefore
\[
[C,F]=h\prod_{i=1}^mT^i(c_i^{-1}),\qquad
h=[C,F][A,B].
\tag{3}
\]
For the identity element no commutators are needed. \(\square\)

**Lemma 2.** Let \(M\) be a closed connected smooth manifold. Every element of
\(\operatorname{Diff}^{\infty}_{c,0}(M\times\mathbb R^2)\), where the subscript denotes isotopy to the identity through an isotopy with compact total support, is a product of at most two commutators in that group.

**Proof.** Perfectness of this compactly supported smooth isotopy group is the standard Mather–Thurston input; see [T12, introduction] and [BIP]. Express the given element as a finite product of \(m\) commutators. The supports of all their factors lie in \(M\times B_R\), for some planar disk \(B_R\).

Choose \(L>2R\). A compactly supported smooth vector field on \(\mathbb R^2\) can be chosen equal to \(L\partial_x\) on a neighborhood of the whole compact corridor
\(\bigcup_{0\le t\le m}(B_R+(Lt,0))\). Its time-one map \(u\) satisfies
\(u^j(B_R)=B_R+(jL,0)\) for \(0\le j\le m\). These disks are pairwise disjoint. The map \(F=\operatorname{id}_M\times u\) belongs to the same compactly supported isotopy group. The subgroup generated by the finitely many commutator factors and its first \(m\) conjugates by \(F\) have disjoint supports, hence commute pairwise. Lemma 1 applies. \(\square\)

This is the standard portable-product case of [BIP], reproduced here for scope clarity. It does not assert that the closed product \(M\times S^2\) is a portable manifold.

## 4. Surface stabilization cannot transfer the known lower bound

**Proposition 3.** Let \(M\) be closed and connected, and let \(f\in\operatorname{Diff}^{\infty}_0(M)\). Then
\[
\operatorname{cl}_{\operatorname{Diff}_0(M\times S^2)}
   (f\times\operatorname{id}_{S^2})\le4.
\tag{4}
\]

**Proof.** Choose a smooth isotopy \(f_t\) from the identity to \(f\). Cover \(S^2\) by two open disks \(U,V\) and choose a smooth function \(\chi:S^2\to[0,1]\) such that
\(\operatorname{supp}\chi\) is compactly contained in \(U\) and
\(\operatorname{supp}(1-\chi)\) is compactly contained in \(V\).
For example take slightly enlarged northern and southern hemispheres and a latitude cutoff with plateaus near the two poles.

Define
\[
a(x,y)=(f_{\chi(y)}(x),y),\qquad
b(x,y)=(f\circ f_{\chi(y)}^{-1}(x),y).
\]
Both maps are smooth diffeomorphisms because their second coordinate is unchanged and each first-coordinate map is a diffeomorphism depending smoothly on \(y\). They satisfy
\[
b\circ a=f\times\operatorname{id}_{S^2}.
\]
The paths
\[
a_s(x,y)=(f_{s\chi(y)}(x),y),\qquad
b_s(x,y)=(f_s\circ f_{s\chi(y)}^{-1}(x),y)
\]
are compactly supported isotopies inside \(M\times U\) and \(M\times V\), respectively. Thus \(a\) and \(b\) belong to their compactly supported identity components. Since each disk is diffeomorphic to \(\mathbb R^2\), Lemma 2 expresses each factor as two commutators. Extending those compactly supported factors by the identity places all four commutators in \(\operatorname{Diff}_0(M\times S^2)\). \(\square\)

In particular (4) holds for all powers of each stabilized element, so its ambient stable commutator length is zero. The result concerns this particular subgroup, not all of \(\operatorname{Diff}_0(M\times S^2)\).

There are two useful exact consequences when \(M=\Sigma_g\) has positive genus.

**Corollary 4.** Every homogeneous quasimorphism on
\(G=\operatorname{Diff}_0(\Sigma_g\times S^2)\) vanishes on
\(\{f\times\operatorname{id}:f\in\operatorname{Diff}_0(\Sigma_g)\}\).

Indeed, a homogeneous quasimorphism \(q\) of defect \(D\) is conjugation invariant, satisfies \(|q([a,b])|\le D\), and hence satisfies
\(|q(h)|\le(2k-1)D\) on products of \(k\ge1\) commutators. Applying (4) to \(f^n\) gives \(|nq(f\times\operatorname{id})|\le7D\), so the value is zero. Conjugation invariance follows directly by applying the defect inequality to a conjugate of \(h^n\) and dividing by \(n\); the commutator estimate then follows by writing \([a,b]=(aba^{-1})b^{-1}\).

**Corollary 5.** There is no abstract group retraction from \(G\) to
\(\operatorname{Diff}_0(\Sigma_g)\) whose restriction to \(f\mapsto f\times\operatorname{id}\) is the identity.

If such a retraction existed, applying it to the four-commutator factorization would give a uniform bound of four in \(\operatorname{Diff}_0(\Sigma_g)\), contradicting Bowden–Hensel–Webb [BHW, Corollary 1.3]. Thus the known surface non-uniform perfectness cannot simply be pulled through this product inclusion, even by an abstract retraction. No historical-priority claim is made for these consequences of the classical compression argument.

### Why the same cutoff does not handle arbitrary diffeomorphisms

The proof uses preservation of the second coordinate. For a general isotopy \(F_t\), the point-dependent-time map \(z\mapsto F_{\chi(z)}(z)\) need not be a diffeomorphism.

For an explicit failure, let \(F_t\) be rotation of \(S^2\subset\mathbb R^3\) through angle \(t\) about the third axis, and set \(\tau(x,y,z)=(1+2xy)/2\). This is smooth with values in \([0,1]\). At \(w=(0,1,0)\), the tangent vector \(v=(-1,0,0)\) is the rotation vector field and \(d\tau_w(v)=-1\). The derivative of \(w\mapsto F_{\tau(w)}(w)\) annihilates \(v\), since before applying the invertible rotation matrix it is \(v+v\,d\tau_w(v)=0\). Thus even this elementary isotopy fails the naive general cutoff construction. The same example acts on the sphere factor of a four-manifold product. Proposition 3 therefore supplies no uniform factorization of arbitrary ambient diffeomorphisms.

## 5. Why invariant-measure averaging does not automatically extend

Another possible route starts with a group-valued cocycle \(c(f,x)\) satisfying
\(c(fg,x)=c(f,gx)c(g,x)\), and a quasimorphism \(\psi\) on its target. Assuming all the following integrals exist, define
\[
Q(f)=\int_X\psi(c(f,x))\,d\mu(x).
\]
If \(\mu\) is a probability measure invariant under the acting group, the cocycle identity bounds the defect of \(Q\) by the defect of \(\psi\). Without invariance the same calculation gives only
\[
Q(fg)-Q(f)-Q(g)
=\int_X\psi(c(f,y))\,d(g_*\mu-\mu)(y)+E(f,g),
\quad |E(f,g)|\le D_\psi.
\tag{5}
\]
The extra integral has not been bounded uniformly in \(f,g\). Omitting it is not a valid extension from a volume-preserving subgroup to the full identity component.

There is no invariant Borel probability measure for the full \(\operatorname{Diff}_0(X)\) action on a positive-dimensional closed connected smooth manifold. To see this, take a coordinate ball with closure inside a larger coordinate ball. For every integer \(N\), local smooth diffeomorphisms isotopic to the identity can shrink and move it into \(N\) pairwise disjoint small balls in that larger chart. Invariance would imply its measure is at most \(1/N\), hence zero. A finite cover by such coordinate balls then contradicts total mass one.

This excludes the direct invariant-probability implementation of the route. It does not prove that every possible averaging construction fails, and it does not prove the absence of quasimorphisms on \(\operatorname{Diff}_0(X)\). A replacement for the missing uniformly bounded defect term in (5) would be substantive new input.

## 6. Other scope distinctions and the remaining gap

For an inclusion \(H\le G\), one has \(\operatorname{cl}_G(h)\le\operatorname{cl}_H(h)\), not a lower bound in the ambient group. Proposition 3 is a concrete instance where a known unbounded subgroup commutator length becomes uniformly bounded in the ambient group.

For a central extension \(1\to Z\to\widetilde G\to G\to1\), a homogeneous quasimorphism on \(\widetilde G\) descends precisely when it vanishes on \(Z\). The sufficiency uses additivity on commuting elements, proved by homogenizing the defect inequality for \((az)^n=a^nz^n\). Nonzero values on the central kernel obstruct descent. A universal-cover construction therefore requires this additional check.

Finally, the usual disk fragmentation estimate has the direction
\(\operatorname{cl}_G(f)\le2\operatorname{frag}(f)\), by the two-commutator bound on an open disk [BIP; W20, p.488]. Unbounded fragmentation alone supplies no lower bound on commutator length. Vanishing stable commutator length on a subgroup also does not prove uniformly bounded ordinary commutator length on the full group.

After two substantive routes, the exact missing result is still (1): a sequence of elements in the **full** identity component of one closed orientable smooth four-manifold with ambient commutator lengths tending to infinity. We have produced no such sequence, no nonzero homogeneous quasimorphism on that full group, and no universal uniform bound. The package remains an unresolved partial and source audit.

## References

- **[K3]** R. İ. Baykur, R. C. Kirby and D. Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, [author version](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), Problem 4.85, pp.259–260.
- **[W20]** R. Webb, *Quasimorphisms on homeomorphism groups*, in [Oberwolfach Report 8/2020](https://ems.press/content/serial-article-files/46844), pp.487–489, especially Question 3 on p.489, DOI 10.4171/OWR/2020/8.
- **[BIP]** D. Burago, S. Ivanov and L. Polterovich, *Conjugation-invariant norms on groups of geometric origin*, Adv. Stud. Pure Math. **52** (2008), 221–250, [author manuscript](https://arxiv.org/abs/0710.1412), Theorems 1.18 and 2.2(i).
- **[T12]** T. Tsuboi, *On the uniform perfectness of the groups of diffeomorphisms of even-dimensional manifolds*, Comment. Math. Helv. **87** (2012), 141–185, [published full text](https://ems.press/content/serial-article-files/43279?nt=1), Theorem 1.1(2). This theorem summarizes earlier joint and independent work; the paper's new general even-dimensional theorem assumes dimension at least six.
- **[BHW]** J. Bowden, S. Hensel and R. Webb, *Quasi-morphisms on surface diffeomorphism groups*, J. Amer. Math. Soc. **35** (2022), 211–231, [author manuscript](https://www.math.lmu.de/~hensel/papers/dagger_arxiv.pdf), Theorem 1.2 and Corollary 1.3.
