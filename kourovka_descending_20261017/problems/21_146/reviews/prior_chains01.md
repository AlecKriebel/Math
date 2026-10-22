# Independent adversarial audit: controlled chains and geometric finiteness

**Checkpoint:** 2026-10-17 20:45:31 UTC (2026-10-17 13:45:31 PDT).

**Assigned audit completion:** 100% for the first independent reconstruction of §§6–7, including the use of Lemma 5.2. This measures completion of this audit, not confidence that the entire manuscript or research problem is settled. No global discovery-completion percentage is asserted by this scoped review.

**Source:** OpenAI, *A universal group of type F∞*, September 23, 2026; cached `literature/prior_claim_universal_Finfinity_20260923.pdf` and corresponding text. Pinned primary version: <https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-universal-group-of-type-F-infinity-September-23-2026/paper.pdf>.

**Independence:** I reconstructed the chain and product-module arguments without reading other audit verdicts. This is an adversarial conditional check, not acceptance of a public prior claim by authority.

## Scoped conclusion and exact remaining gap

I found no fatal error or missing inference in Proposition 6.2, Lemma 6.1, or §§7.1–7.4, **conditional on the exact finite-diagram hypotheses and the finite-idempotent assertion Lemma 3.1**. In particular, the manuscript does not commit the two most plausible errors: it does not tensor a non-equivariant homotopy over the group ring, and it does not interchange a product with an infinite direct sum.

The strongest result independently checked here is this implication:

> Let $f:U\to U$ be injective, factor as $U\xrightarrow a P\xrightarrow b U$ through a finitely presented group, and admit the two finite commuting-image orthogonal-additivity diagrams specified in Theorem 5.1. Assuming Lemma 3.1 for the actual indexing systems, the supplied proof establishes that $T(U,f)$ is finitely presented and has type $F_\infty$, with $U$ embedded.

The remaining global gap for this reviewer is to independently establish Lemma 3.1 and the actual construction of those diagrams with a common injective distinguished map (especially Proposition 4.1 and Corollary 4.2). Neither the universal theorem nor Kourovka 21.146 is promoted to a verified solution by this scoped audit. The separate finite-group and envelope audits must be combined before such a verdict.

## 1. Precise claim and quantifiers

For every finite symmetric $A\subset U$ containing $1$, and for every fixed $n\ge0$, Proposition 6.2 asserts

\[
\exists k\ge0\;\exists\text{ finite bound }B\;
\forall z\in Z_n(C_*^A(U))\;\exists y\in C_{n+1}^B(U):
\quad\partial y=(f^k)_*z.
\]

For $n=0$, $Z_0$ here means the augmentation kernel. In positive degree it means ordinary cycles. The exponent and output bound precede the cycle quantifier. The length and coefficients of $y$, and its absolute vertex locations, can depend arbitrarily on $z$. This is exactly sufficient for the later product argument; there is no need for a filling-length estimate or algorithm.

The fixed-degree chain group $C_q^A(U)$ is free over $\mathbb ZU$ with a **finite** basis: translate the first vertex to $1$, and the other $q$ vertices all belong to $A$. The complex can have arbitrarily many degrees, but only finitely many degrees occur in any one induction stage. No global finite-rank assertion is needed.

## 2. Adversarial check of Lemma 6.1

The maps $H_q$ are ordinary abelian-group homomorphisms. They are allowed to be non-equivariant. Extending them by zero for $q\ge n$ and setting

\[
F'=F-\partial H-H\partial
\]

does produce a chain map in **every** degree, because $F$ is a chain map and $\partial^2=0$. The lower homotopy equations imply $F'_0=c_0$ and $F'_q=0$ for $0<q<n$. For an $n$-cycle $z$, the truncation $H_n=0$ gives $F'z=Fz$. This is not an unsupported assertion that $F'_n=F_n$ on all $n$-chains.

I checked the three comparison steps:

1. The Alexander–Whitney map $D$ is compatible with normalization, since every split of a consecutive repetition has a degenerate factor. Its factors retain the input bound.
2. The shuffle map $S$, with sign counting vertical-before-horizontal inversions, preserves the two coordinate bounds. The manuscript's inductive construction of $R$ in $\partial R+R\partial=\Delta-SD$ uses only the simplex's vertex set in each coordinate. The full tuple complex on $V\times V$ is contractible by prepending a vertex; normalization does not obstruct that contraction. For positive-degree inputs the residual to be coned is a cycle, and for degree zero the residual is zero.
3. With the tensor differential convention stated in the paper,
   \[
   K(a\otimes b)=H(a)\otimes F(b)+(-1)^{|a|}F'(a)\otimes H(b)
   \]
   has
   \[
   \partial K+K\partial=(F-F')\otimes F+F'\otimes(F-F')
   =F\otimes F-F'\otimes F'.
   \]
   The cross terms cancel with precisely the displayed sign. Thus $L=RF+SKD$ satisfies the required homotopy equation.

On an $n$-cycle, all intermediate bidegrees disappear after $F'\otimes F'$. In the two remaining bidegrees the degree-zero factor is the vertex $1$. Summing over the cycle yields

\[
(F'\otimes F')Dz=(1)\otimes F'z+F'z\otimes(1)
=(1)\otimes Fz+Fz\otimes(1).
\]

This works for $n=1$ as well; there are then no intermediate bidegrees. Applying $m(u,v)=h_1(u)h_2(v)$ yields additivity. The commuting-image assumption makes $m$ a group homomorphism, and changes the two finite coordinate bounds $B_1,B_2$ into the finite bound $h_1(B_1)h_2(B_2)$. Symmetry follows because the two image subgroups commute. Thus this step genuinely controls simplex types, even though individual paths in $H_0$ can wander far from their input vertices.

**Attempted falsification that fails:** non-equivariance would prevent a direct tensoring of $H$ with a right module. The proof never performs that operation. It uses $H$ only on ordinary chains to establish Proposition 6.2, and later fills ordinary chains separately in each coefficient coordinate and coset.

## 3. Reconstruction of Proposition 6.2

For degree zero, $f(U)\subset b(P)$, and $b(P)$ is finitely generated. A finite symmetric generating set $S$ therefore supplies a path from $1$ to every $f(u)$, all of whose edges have difference in $S$. Arbitrary path lengths are harmless. Their boundaries give $f_*(u)-(1)$, hence fill every reduced zero-cycle with one common bound. Finite presentation is more than this base step needs; it is used later for the presentation of the torus.

At the degree-$n$ stage, a controlled partial homotopy through degree $q-1$ has obstruction

\[
w_a=F(a)-H_{q-1}(\partial a)
\]

on each normalized $q$-simplex $a$. Applying the previous homotopy equation to $\partial a$ shows $\partial w_a=0$. For $q=1$, the apparent extra term is $c_0\partial a=0$, so the endpoint case is valid. The controlled maps supply one finite bound for **all** obstructions $w_a$, despite infinitely many translated simplices.

The degree-$q$ induction hypothesis applies to every cycle of this bound, producing one exponent $r$ and output bound. Postcomposition of $F$ and previous $H_i$ by $f^r$ preserves the earlier equations because $f^r(1)=1$. Each mapped $w_a$ then has a finite filling within the common bound; choose such a filling for every basis element and extend linearly. No equivariant choice is claimed or needed. There are only finitely many $q<n$, so one final iterate and bound suffice.

For this partial homotopy, Lemma 6.1 applies to each of finitely many orthogonal relations in both diagrams. A finite union of their output bounds puts every required equality in the **same** homology group $H_n(C_*^B(U))$. Lemma 3.1 therefore applies to those homology classes, not to unrelated groups. Both identity indices represent $(f^{k+1})_*z$, since $h_{2,I}=h_{3,I}=f$. Its annihilation by both $2$ and $3$ makes it zero over $\mathbb Z$. A zero homology class has a finite filling by the definition of these direct-sum chain groups. This completes the quantified induction without circularity.

**Essential boundary condition:** replacing the common output bound by a bound depending on each cycle would invalidate the subsequent product argument. The actual induction supplies the stronger, needed statement.

## 4. Product coefficients and the HNN map

For $M=(\mathbb ZJ)^I$ and the finite simplex-type set $S_q(A)$,

\[
M\otimes_{\mathbb ZU}C_q^A(U)
\cong\bigoplus_{s\in S_q(A)}(\mathbb ZJ)^I
\cong\prod_{\alpha\in I}\left(\bigoplus_{s\in S_q(A)}\mathbb ZJ\right).
\]

The second interchange is justified by finiteness of $S_q(A)$. Each coordinate can have an arbitrary finite group-ring support. There need not be one finite support common to all coordinates. Conversely, such families with a common finite set of simplex types do determine a tensor, by collecting each type's coefficient into one element of $M$.

Every tensor chain has a finite input bound because it is a finite sum of simple tensors, each ordinary chain using finitely many types. Boundary preserves each left $U$-coset. Thus a cycle decomposes coordinatewise into finitely many coset cycles, and each translates back to an ordinary cycle of one common bound $A$. Degreewise inclusions of bounded complexes remain injective after tensoring because they are inclusions of subsets of a free basis, hence split inclusions; no flatness of $M$ is presumed.

The HNN chain map has the right direction:

\[
F(m\otimes c)=mt\otimes f_*c,
\quad (ju_0,\ldots,ju_i)\longmapsto
(jtf(u_0),\ldots,jtf(u_i))=(ju_0t,\ldots,ju_it).
\]

The relation $ut=tf(u)$ proves both well-definedness on balanced tensors and independence of coset origin. Applying Proposition 6.2 to all component cycles gives the **same** $k,B$. Choosing a finite filling for each component, translating by $jt^k$, and adding within each coordinate leaves each coordinate finite. The finite-type identification above reassembles the fillings into a tensor chain. Component collisions at the output merely add chains; they do not spoil finiteness or the boundary identity. Consequently $F^k[z]=0$.

Local nilpotence gives a well-defined additive inverse $(1-F)^{-1}x=\sum_{r\ge0}F^rx$, since each sum terminates and one may take the maximum of exponents for two inputs. In the HNN long exact sequence, the two adjacent maps at degree $n\ge2$ involve positive degrees $n$ and $n-1$; both are invertible. Hence $H_n(J,(\mathbb ZJ)^I)=0$. No assertion at degree zero is needed.

I also checked the tree and mapping-cone justification: the coset graph has one outgoing edge per vertex and strictly increasing integer height; a least-height vertex in an undirected cycle would need two outgoing edges. Normal forms $t^pu t^{-q}$ show every forward ray reaches the distinguished forward ray. Thus it is a connected tree, giving exactly the displayed cone resolution and coefficient multiplier $t$.

## 5. From homology to $F_\infty$

The finite-presentation hypothesis is genuinely used, not suppressed. Lemma 5.2 exhibits $T(U,f)\cong T(P,ab)$ by inverse maps; the substitutions $p\mapsto tb(p)t^{-1}$ and $u\mapsto a(u)$ check directly using the torus relations. A finite presentation of $P$ therefore yields one for $J$.

For Lemma 7.1, start with a finite presentation complex $X_2$. At stage $n$, its universal cover $Z$ is $n$-dimensional and $(n-1)$-connected, with finite-rank free cellular modules through degree $n$. Extend it with arbitrary higher cell orbits to a contractible free $J$-complex $Y$. Let $I$ index **all** cellular $n$-cycles of $Z$. Finite rank in degrees $n,n-1$ realizes their universal family as a cycle of $(\mathbb ZJ)^I\otimes C_*(Y)$. The assumed homology vanishing bounds this family by one tensor, which involves only finitely many basis elements $c_1,\ldots,c_s$ of $C_{n+1}(Y)$. Coordinate projection then expresses every cycle as an $\mathbb ZJ$-linear combination of $\partial c_j$. This proves finite generation of the cycle module; it is not an assumption that submodules of finite free modules are finitely generated.

Since $n\ge2$ and $Z$ is $(n-1)$-connected, Hurewicz identifies this cycle module with $\pi_n(Z)$ (there are no $(n+1)$-cells in $Z$). The identification respects deck transformations, with basepoint changes canonical in a simply connected space. Finitely many sphere representatives therefore give finitely many downstairs $(n+1)$-cell attachments killing $\pi_n$. Lower connectivity remains intact. Induction produces a finite skeleton in every degree, and cellular approximation plus Whitehead makes the union's universal cover contractible. This proves geometric $F_\infty$, rather than only $FP_\infty$.

## 6. Independent exact computation

`prior_chains01_check.py` implements normalized integral chains directly, with no numerical arithmetic or dependencies. It exhaustively checked 4,998 identities on a three-vertex tuple complex, in total degrees through four: the Alexander–Whitney chain equation, shuffle chain equation, controlled $R$ recursion, signed tensor homotopy $K$, and combined $L$ equation for truncation levels $n=1,2,3$. It includes simplices with nonadjacent repeated vertices. Execution at this checkpoint returned:

```
PASS: 4998 exact integral chain identities on 3 vertices; degrees through 4.
```

This is a consistency check of signs, normalization, and boundary cases. It does not test the finite-idempotent lemma, faithful envelopes, arbitrary groups, or the uniform quantifiers; those points require the mathematical reconstruction above or separate audits.
