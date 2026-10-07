# Post-Lie structures with a complex semisimple target

## Disposition and exact scope

This is an author proof candidate for problem 30005737 / OWR-14298013-001, not an independently accepted solution or a historical novelty claim. The original question concerns finite-dimensional complex Lie algebras on the same vector space: the source bracket \(\mathfrak g=(V,[\ ,\ ])\) is perfect and nonsemisimple; the target bracket \(\mathfrak n=(V,\{\ ,\ \})\) is semisimple. The characteristic is zero. No assertion about positive characteristic or infinite-dimensional algebras is made.

The argument below proves the stronger obstruction with “perfect” replaced by “unimodular,” provided its standard Lie-group inputs and global steps pass independent review. Only one substantive author approach was needed to obtain this candidate. Search, source inspection, and exact finite checks are not counted as additional approaches.

## Theorem

Let \(\mathfrak g\) and \(\mathfrak n\) be finite-dimensional complex Lie algebras of the same dimension. Suppose \(\mathfrak g\) is unimodular, \(\mathfrak n\) is semisimple, and there are Lie algebra homomorphisms
\[
j_1,j_2:\mathfrak g\longrightarrow\mathfrak n
\]
whose difference is a linear isomorphism. Then \(\mathfrak g\) is semisimple.

Consequently, if \(\mathfrak g\) is perfect but nonsemisimple and \(\mathfrak n\) is semisimple, there is no post-Lie structure on \((\mathfrak g,\mathfrak n)\).

“Unimodular” means \(\operatorname{tr}(\operatorname{ad}_{\mathfrak g}x)=0\) for every \(x\in\mathfrak g\).

## Standard inputs

The proof uses the following classical finite-dimensional complex Lie theory and elementary topology:

1. A complex Lie algebra has a connected simply connected complex Lie group; a Lie algebra homomorphism from the algebra of a simply connected group integrates uniquely to a holomorphic group homomorphism.
2. Levi decomposition: \(\mathfrak g=\mathfrak s\ltimes\mathfrak r\), with \(\mathfrak s\) semisimple and \(\mathfrak r\) the solvable radical. The simply connected group integrating a semidirect sum is the semidirect product of the simply connected groups integrating its summands.
3. A simply connected complex semisimple group \(S\) admits a compact real form \(K\) and polar decomposition \(S\simeq K\times\mathbb R^{\dim_{\mathbb C}\mathfrak s}\) as smooth manifolds. In particular \(S\) deformation retracts onto the compact connected orientable manifold \(K\), of real dimension \(\dim_{\mathbb C}\mathfrak s\).
4. A transitive smooth Lie-group action identifies the manifold with \(G/H\), for the closed stabilizer \(H\). If \(H\) is discrete, \(G\to G/H\) is a covering map. Compact connected orientable \(m\)-manifolds have \(H_m(-;\mathbb Z)=\mathbb Z\) and no homology above degree \(m\).

These are imported classical inputs, not new claims. The solvable-group contractibility needed below is proved explicitly in Step 4. References and precise source locations are recorded in SOURCES.md.

## Proof

### Step 1. Integrate the transverse pair

Let \(G\) and \(N\) be the connected simply connected complex Lie groups integrating \(\mathfrak g\) and \(\mathfrak n\). Integrate \(j_i\) to holomorphic homomorphisms \(J_i:G\to N\). Define a holomorphic action
\[
A_h(p)=J_1(h)\,p\,J_2(h)^{-1}\qquad(h\in G,\ p\in N).
\]
It is an action because \(A_{hh'}=A_h\circ A_{h'}\).

For \(x\in\mathfrak g\), its fundamental vector at \(p\) is the derivative at \(t=0\) of \(J_1(\exp(tx))pJ_2(\exp(tx))^{-1}\). In the left trivialization \(T_pN\to\mathfrak n\), this vector is
\[
B_p(x)=\operatorname{Ad}_{p^{-1}}j_1(x)-j_2(x).
\]
At the identity \(e\), \(B_e=j_1-j_2\) is invertible. The inverse function theorem applied to the orbit map at the identity of \(G\) therefore gives a nonempty open orbit \(U=G\cdot e\).

No closedness of the image of \((J_1,J_2)\) in \(N\times N\) is assumed or needed.

### Step 2. A global determinant has no zeros

Fix bases of \(\mathfrak g\) and \(\mathfrak n\), and put
\[
f(p)=\det B_p.
\]
This is a globally defined holomorphic function on \(N\), and \(f(e)\ne0\).

Equivariance of each homomorphism \(J_i\) gives
\[
B_{A_h(p)}
=\operatorname{Ad}_{J_2(h)}\circ B_p\circ\operatorname{Ad}_{h^{-1}}.
\tag{1}
\]
Indeed,
\[
\begin{aligned}
B_{A_h(p)}
&=\operatorname{Ad}_{J_2(h)}\operatorname{Ad}_{p^{-1}}
  \operatorname{Ad}_{J_1(h)^{-1}}j_1-j_2\\
&=\operatorname{Ad}_{J_2(h)}
  (\operatorname{Ad}_{p^{-1}}j_1-j_2)\operatorname{Ad}_{h^{-1}}.
\end{aligned}
\]
A connected unimodular Lie group has \(\det\operatorname{Ad}_h=1\): its determinant character has zero differential, hence is constant on the connected group and equals one at the identity. This applies to \(G\) by assumption and to \(N\) because a semisimple Lie algebra is perfect and therefore unimodular. Taking determinants in (1) yields
\[
f(A_h(p))=f(p).
\]
Thus \(f\) is the nonzero constant \(f(e)\) on \(U\). The identity theorem on the connected complex manifold \(N\) implies
\[
f(p)=f(e)\ne0\quad\text{for every }p\in N.
\tag{2}
\]
Hence the infinitesimal action is an isomorphism at every point, and every orbit is open. Since \(N\) is connected and is partitioned into disjoint open orbits, it has only one orbit. The action is transitive.

This is the essential completeness step: transversality at the identity alone would not give a transitive action. Unimodularity and the global determinant establish transversality everywhere.

### Step 3. The orbit map is a diffeomorphism

Let \(H\le G\) stabilize \(e\). It is closed as the inverse image of \(e\) under a continuous orbit map, and its Lie algebra is \(\ker B_e=0\). It is therefore discrete. The orbit-stabilizer theorem identifies \(N\) holomorphically with \(G/H\). The map \(G\to G/H\) is a covering because \(H\) is a closed discrete subgroup. Both \(G\) and \(N\) are connected and simply connected, so that covering has one sheet. Thus \(H=\{e\}\), and
\[
G\simeq N
\tag{3}
\]
as complex manifolds, in particular as smooth manifolds.

The covering conclusion is obtained after proving transitivity and identifying the actual closed stabilizer. It is not inferred merely from a surjective local diffeomorphism.

### Step 4. Homology forces the radical to vanish

Write \(\mathfrak g=\mathfrak s\ltimes\mathfrak r\), and let \(S,R\) be the connected simply connected complex groups integrating \(\mathfrak s,\mathfrak r\). The action of \(\mathfrak s\) on \(\mathfrak r\) integrates because \(S\) is simply connected and Lie algebra automorphisms of \(\mathfrak r\) integrate uniquely on \(R\). The simply connected group \(R\rtimes S\) has Lie algebra \(\mathfrak g\); uniqueness of simply connected integration identifies it with \(G\). In particular, \(G\) has underlying manifold \(R\times S\).

For completeness, \(R\) is contractible. Induct on \(q=\dim_{\mathbb C}\mathfrak r\). The claim is immediate for \(q=0\). If \(q>0\), solvability implies \([\mathfrak r,\mathfrak r]\ne\mathfrak r\). A nonzero linear functional vanishing on the derived algebra has a codimension-one ideal \(\mathfrak r'\) as kernel. Choose \(x\notin\mathfrak r'\). Then
\[
\mathfrak r=\mathbb Cx\ltimes\mathfrak r',
\]
since \(\mathbb Cx\) is a one-dimensional subalgebra. Integrating this semidirect product identifies the simply connected \(R\), as a manifold, with \(\mathbb C\times R'\), where \(R'\) is simply connected and solvable. Induction gives \(R\simeq\mathbb C^q\) as smooth manifolds.

Put \(d=\dim_{\mathbb C}\mathfrak n=\dim_{\mathbb C}\mathfrak g\) and \(s=\dim_{\mathbb C}\mathfrak s\). Polar decomposition makes \(N\) homotopy equivalent to its compact real form \(K_N\), a compact connected orientable manifold of real dimension \(d\). Therefore
\[
H_d(N;\mathbb Z)\cong\mathbb Z.
\]
On the other hand, \(G\simeq R\times S\) is homotopy equivalent to the compact real form \(K_S\), whose real dimension is \(s\). If \(\mathfrak r\ne0\), then \(s<d\), and
\[
H_d(G;\mathbb Z)=0.
\]
This contradicts (3). Hence \(\mathfrak r=0\) and \(\mathfrak g\) is semisimple. This proves the theorem. \(\square\)

## Passage from post-Lie structures to the theorem

A post-Lie product satisfies, for all \(x,y,z\in V\),
\[
\begin{aligned}
x\cdot y-y\cdot x&=[x,y]-\{x,y\},\\
[x,y]\cdot z&=x\cdot(y\cdot z)-y\cdot(x\cdot z),\\
x\cdot\{y,z\}&=\{x\cdot y,z\}+\{y,x\cdot z\}.
\end{aligned}
\]
Let \(L(x)y=x\cdot y\). The last identity says \(L(x)\in\operatorname{Der}(\mathfrak n)\). Every derivation of a finite-dimensional complex semisimple Lie algebra is inner, and its center is zero. There is therefore a unique linear map \(R:V\to\mathfrak n\) satisfying \(L(x)=\operatorname{ad}_{\mathfrak n}(R(x))\).

The middle identity says \(L([x,y])=[L(x),L(y)]\), so injectivity of \(\operatorname{ad}_{\mathfrak n}\) gives
\[
R([x,y])=\{R(x),R(y)\}.
\]
The first identity gives
\[
[x,y]=\{R(x),y\}+\{x,R(y)\}+\{x,y\}.
\]
Consequently both
\[
j_1=R+I,\qquad j_2=R
\]
are Lie homomorphisms \(\mathfrak g\to\mathfrak n\), and \(j_1-j_2=I\). For \(j_1\), expand its target bracket and use the preceding two displayed identities. This reproduces the established transverse-pair construction directly, rather than treating it as an unexplained black box.

Finally a perfect Lie algebra is unimodular: the linear functional \(x\mapsto\operatorname{tr}\operatorname{ad}x\) vanishes on brackets because the trace of a commutator is zero; perfectness says brackets span the algebra. Applying the theorem contradicts the assumed nonsemisimplicity.

## Scope checks and exclusions

- The two brackets are not exchanged. The inner-derivation step uses semisimplicity of the target \(\mathfrak n\), whereas trace zero comes from the source \(\mathfrak g\).
- The simply connected groups are auxiliary integrations. The claim does not assume any particular global form of a group was supplied with the original problem.
- No assertion that every post-Lie structure is complete is used. Equation (2) proves the relevant global action is transitive under the specific unimodularity and semisimple-target assumptions.
- The proof does not need the images of \(J_1,J_2\), or \((J_1,J_2)\), to be closed or algebraic.
- The complex field matters in Step 4: compact real forms of complex semisimple groups have real dimension equal to the complex dimension of the group. The same dimension argument is not asserted for arbitrary real forms.
- The target is not merely reductive. A center can supply contractible directions, and not all derivations are inner. Known reductive-target examples therefore do not contradict this proof.
- No counterexample is claimed. The finite computations are diagnostic checks only, not a substitute for any global step above.
- An isomorphism \(\mathfrak g\cong\mathfrak n\) is not needed for the requested contradiction and is not inferred merely from the manifold diffeomorphism. The established semisimple-source rigidity theorem can be applied after semisimplicity is proved, if that separate stronger conclusion is desired.
