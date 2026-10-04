# Independent universal semilinear obstruction for PR344

The following proof was derived from the frozen general dual equations after the permitted first candidate read. It allows arbitrary k-valued matrix coefficients and does not infer an algebraic-closure claim from a finite prime-field search.

Let k be any perfect field of characteristic p, sigma(a)=a^p, and M have ordered basis e0,...,e5. Let F be sigma-semilinear and V sigma^(-1)-semilinear with

    F e0=e1, F e1=e2, F e3=e4;
    V e0=e5, V e3=e2, V e5=e4;

all other basis images zero. These maps satisfy FV=VF=0. Define the dual by the actual contravariant convention

    F^D(phi)=sigma o phi o V,
    V^D(phi)=sigma^(-1) o phi o F.

This convention was independently verified against Hoshi Definition 2.3, manuscript pages 5–6, after the first candidate assessment was frozen. It agrees with the source-only derivation. In the dual basis the matrices are V^t and F^t because the displayed coefficients are in the prime field; the respective semilinear scalar actions still remain.

There is no assumption that an intertwiner P has prime-field entries. Suppose P:M->M^D is k-linear and satisfies P F=F^D P and P V=V^D P. By composition it intertwines the second iterates. The original second iterates are

    F^2(e0)=e2, V^2(e0)=e4,

with every other basis second image zero. On the dual, the only nonzero basis second images are

    (F^D)^2(e4*)=e0*, (V^D)^2(e2*)=e0*.

Write P(e0)=sum_i c_i e_i*, with c_i in the unrestricted field k. Semilinearity then gives

    P(e2) = (F^D)^2(P(e0)) = sigma^2(c4) e0*,
    P(e4) = (V^D)^2(P(e0)) = sigma^(-2)(c2) e0*.

Both images lie in k e0*. The two-dimensional subspace k e2 + k e4 therefore has image of dimension at most one. Consequently P has a nonzero kernel. **No intertwiner can be an isomorphism**, for any perfect k. Equivalently, every solution of the complete semilinear matrix equations has determinant zero. The argument neither drops Frobenius twists nor solves only the prime-field equations.

For M_n=M direct-summed with n−3 rank-two standard supersingular blocks, the two squares vanish on the additional summands, as do both dual squares there. The same forced images of e2 and e4 prove non-self-duality for every n>=3.

To connect this obstruction to the literal source question, take k to be an algebraic closure of F_p with p>3. The integral basis u=e1+e3+e5, v=e2+e4, w=2e1+e3, z=e2, a=e0, b=e1 has determinant 1; the flag by (u,v) and (u,v,w,z) has standard supersingular rank-two graded modules. Contravariant equivalence reverses its filtration and yields qss elliptic p-torsion factors. Each factor is deformable and has im F=im V. Hoshi Lemma 4.9 applies with its section-global deformability assumption, and its Definition 4.8 gives actual supersingular elliptic factors over our already algebraically closed k.

The subspace L=span(e0,e3,e5) complements im F=span(e1,e2,e4), and V maps its basis to independent vectors e5,e2,e4. Since im F=ker V and im V=ker F, the module is deformable (Hoshi Definition 3.4). As a W(k)-module through W(k)->k, it has pM=0 and finite length six. All finite Honda conditions in Remark 3.5.1 hold: the composites equal multiplication by p=0, V|L is injective, and L/pL->M/im F is an isomorphism. Proposition 3.11(2), on its p-torsion W-category for p!=2, therefore produces the required p-killed finite flat W-group. Proposition 3.11(5) identifies its reduction with the module just considered. Its special fiber has rank p^6 also by the three elliptic p-torsion factors and multiplicativity of rank in exact finite-group sequences; finite flatness fixes the same rank over W.

The same construction works after adding the standard blocks with Honda subspaces span(x). A W-level self-duality would reduce to special-fiber self-duality, contrary to the universal semilinear obstruction. Thus both the special fiber and the W-group in these examples are non-self-dual for every p>3 and n>=3.

This is a counterexample to automatic self-duality under the special-fiber-qss hypothesis. It does not furnish a principally polarized Jacobian or answer the Coleman conjecture. The proof uses the cited classical classification, which this audit checks for applicability and does not re-prove. No originality or priority claim follows from the present audit.

Primary-source links: [Takao report](https://ems.press/content/serial-article-files/47479), [Hoshi revised manuscript](https://www.kurims.kyoto-u.ac.jp/~yuichiro/rims1911revised.pdf).
