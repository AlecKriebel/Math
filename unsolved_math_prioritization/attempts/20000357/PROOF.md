# Density degrees under finite covers

## Result and scope

This is an independently written verification of the bounded results associated with AIM Problem 1.18, catalogued as problem 20000357, AIM-ALGEBRAIC_NUMBER_THEORY-0009. The two finite-cover transfer statements, their Galois refinement, the optimal bounds on the minimum density degree, and the explicitly dilated curve-component transfer all hold under the hypotheses below. These are partial answers to the original request for restrictions on density-degree sets. No complete classification or novelty is claimed.

For a number field \(k\), an integral \(k\)-variety \(Z\), and an integer \(d>0\), let

\[
Z_{(d)}=\{z\in Z\text{ closed}:[\kappa(z):k]=d\},\qquad
\delta(Z/k)=\{d>0:Z_{(d)}\text{ is Zariski dense in }Z\}.
\]

Let \(f:X\to Y\) be a **finite dominant** morphism of geometrically integral \(k\)-varieties, with function-field degree \(n=[k(X):k(Y)]\). Dominance is essential. The assertions concern the whole target, not a proper image of a nondominant map. Geometric integrality supplies all the irreducibility used below; ordinary integrality would suffice for the elementary transfer argument.

**Theorem 1.** The following hold:

1. If \(d\in\delta(X/k)\), there is an integer \(m\in\{1,\ldots,n\}\) dividing \(d\) such that \(d/m\in\delta(Y/k)\).
2. If \(e\in\delta(Y/k)\), there is an integer \(m\in\{1,\ldots,n\}\) such that \(em\in\delta(X/k)\).
3. If \(k(X)/k(Y)\) is Galois, the multipliers in both statements can be chosen among the positive divisors of \(n\).

Consequently, when the minima are defined,

\[
a=\min\delta(X/k),\quad b=\min\delta(Y/k)
\quad\Longrightarrow\quad b\le a\le nb.
\]

Both endpoints are attained for every positive cover degree \(n\); for every \(n\ge2\), the upper endpoint can be attained over every prescribed number field.

## Dense opens and residue degrees

Characteristic zero makes the finite function-field extension separable. Generic flatness and generic étaleness therefore give a nonempty open \(V\subset Y\) for which

\[
U=f^{-1}(V)\longrightarrow V
\]

is finite étale of constant rank \(n\). One can see the shrinking directly: the generic fiber is a finite separable field extension; the nonflat and non-étale loci can be removed after shrinking the target, and the rank of the resulting finite locally free algebra is its generic rank \(n\). The map remains surjective because the original finite dominant map is surjective and every fiber of its restriction is nonempty.

Restricting to a dense open does not change density-degree membership. Indeed, if \(Z_{(d)}\) is dense, its intersection with any dense open \(Z^\circ\) is dense in \(Z^\circ\), since every nonempty open of \(Z^\circ\) is open in \(Z\). Conversely, a subset dense in a dense open is dense in \(Z\). Closed points in an open subvariety have the same residue fields as they do in \(Z\).

For a closed point \(Q\in V\), write its finite étale fiber as

\[
U_Q=\coprod_{i=1}^s\operatorname{Spec} L_i,
\qquad \sum_{i=1}^s[L_i:\kappa(Q)]=n.
\]

Each \(L_i\) is a finite separable field extension of \(\kappa(Q)\). The corresponding point \(P_i\in U\) is closed, and the tower law gives

\[
\deg_k(P_i)=\deg_k(Q)\,[\kappa(P_i):\kappa(Q)],\qquad
1\le[\kappa(P_i):\kappa(Q)]\le n.
\]

Thus the degree bound is being used where total fiber rank is controlled. It is not an assertion about arbitrary singular or nonflat fibers of the original map.

## Proof of the two transfer directions

Assume first that \(d\in\delta(X/k)\). The degree-\(d\) points of \(U\) form a dense set. Divide this set into the \(n\) strata specified by the relative residue degree

\[
m(P)=[\kappa(P):\kappa(f(P))]\in\{1,\ldots,n\}.
\]

At least one stratum is dense in \(U\): otherwise their closures would be finitely many proper closed subsets whose union contains \(U\), contradicting irreducibility. Let this stratum have multiplier \(m\). Every image point has degree \(d/m\), so \(m\mid d\).

The image of the dense stratum is dense in \(V\). To check this without assuming the image itself is closed, if its closure were a proper closed subset \(F\subset V\), the stratum would lie in \(f^{-1}(F)\). This inverse image is proper because \(f:U\to V\) is surjective, contradicting density. Therefore \(d/m\in\delta(Y/k)\).

Conversely, let \(e\in\delta(Y/k)\), and let \(T\subset V\) consist of all degree-\(e\) closed points. Its full inverse image, meaning all closed points in all its finite fibers, is dense in \(U\). Here is a direct argument. Given any nonempty open \(O\subset U\), the complement \(F=U\setminus O\) is proper and closed. A finite map is closed. Every irreducible component of \(F\) has dimension strictly smaller than \(\dim U=\dim V\), and its finite image has that same dimension. Hence \(f(F)\) is a proper closed subset of \(V\). Choose \(Q\in T\setminus f(F)\). Its nonempty fiber lies entirely in \(O\), proving the claimed density.

Partition this full inverse image by relative residue degrees \(m\in\{1,\ldots,n\}\). Irreducibility again makes one stratum dense. Every point in that stratum has degree \(em\), proving \(em\in\delta(X/k)\).

Applying the first assertion to \(a\) gives \(a=me\ge e\ge b\). Applying the second assertion to \(b\) gives some \(bm\in\delta(X/k)\) with \(m\le n\), hence \(a\le bm\le nb\). This proves the minimum inequalities.

## The Galois refinement

Suppose \(L=k(X)\) is Galois over \(K=k(Y)\), with group \(G\) of order \(n\). A further shrinking makes the preceding étale cover a \(G\)-torsor. For clarity, this does not assume that \(X\) was normal initially. First take \(V\) inside the smooth, hence normal, locus of \(Y\); its finite étale inverse image is also normal. It is the normalization of \(V\) in \(L\), so the \(K\)-automorphisms in \(G\) extend to this model. On the étale locus the normalization cover is a \(G\)-torsor. Equivalently, the generic torsor isomorphism extends after removing a further proper closed subset.

Let \(Q\in V\) be closed. Its fiber is a torsor under the **constant** group \(G\) over the field \(\kappa(Q)\). The group acts transitively on its closed components. If \(P\) is one component and \(D_P\subseteq G\) is its stabilizer, there are \(n/|D_P|\) components; all have the same residue degree \(m\), since the \(G\)-action gives isomorphisms between them. Their total rank is \(n\), so

\[
(n/|D_P|)m=n,\qquad m=|D_P|\mid n.
\]

One may also identify geometric points of the fiber with \(G\). The absolute Galois group of \(\kappa(Q)\) acts by translations commuting with \(G\); the orbit sizes, hence the residue degrees, are subgroup orders. The same finite-partition arguments now use only \(m\mid n\). No claim about ramification is needed because all density statements were restricted to this open.

## Optimal minimum bounds

For \(X=Y=\mathbb P^1_k\), any degree-\(n\) self-map gives \(a=b=1\), so the lower endpoint is attained for every \(n\). The identity covers \(n=1\) for both endpoints.

For the upper endpoint, fix \(n\ge2\). Clark's established index-existence theorem, Corollary 4 of [Clark], supplies a smooth projective geometrically integral genus-one curve \(C/k\) of index \(n\). The index is the positive generator of the subgroup of \(\mathbb Z\) generated by the closed-point degrees. Thus an integer linear combination of finitely many closed points is a \(k\)-divisor \(D\) with \(\deg D=n\). This is an actual divisor, not merely a \(k\)-rational point of a Picard scheme.

Let \(\mathcal L=\mathcal O_C(D)\). Riemann–Roch on a genus-one curve gives \(h^0(C,\mathcal L)=n\). After passage to an algebraic closure, for every geometric point \(p\), the line bundle \(\mathcal L(-p)\) has positive degree \(n-1\), so \(h^0(\mathcal L(-p))=n-1\). Hence \(\mathcal L\) is geometrically globally generated.

Choose a nonzero \(k\)-section \(s_0\). For each of its finitely many geometric zeros \(p\), the \(k\)-sections vanishing at \(p\) form a proper \(k\)-linear subspace of \(H^0(C,\mathcal L)\). Properness follows from geometric global generation and cohomology base change. A vector space over the infinite field \(k\) is not the union of finitely many proper linear subspaces. Choose \(s_1\) outside their union. The pair has no common zero and defines a morphism

\[
g:C\longrightarrow\mathbb P^1_k,
\qquad g^*\mathcal O_{\mathbb P^1}(1)\simeq\mathcal L.
\]

It is nonconstant, finite, and of degree \(n\). Hilbert irreducibility for a finite morphism from a geometrically integral curve to \(\mathbb P^1\) over a number field gives infinitely many rational base points whose scheme-theoretic fibers are integral of degree \(n\). Such a fiber is a single closed point, not a sum of smaller-degree points. The resulting infinitely many points are dense in \(C\).

More generally, composing \(g\) with any degree-\(r\) self-map of \(\mathbb P^1\), for \(r\ge1\), and applying the same theorem gives \(nr\in\delta(C/k)\). Every closed-point degree on \(C\) is divisible by \(n\), by the definition of index. Therefore

\[
\delta(C/k)=n\mathbb Z_{>0}.
\]

For \(C\to\mathbb P^1\), it follows that \(a=n\), \(b=1\), and \(a=nb\). The use of Clark here is a named theorem dependency, not a new proof of index existence or an assumption of a period-index conjecture. The construction does not assert that these degree-\(n\) covers are Galois.

## Relative degrees for non-Galois and Galois examples

Consider the finite degree-three map

\[
f:\mathbb P^1_{\mathbb Q}\to\mathbb P^1_{\mathbb Q},\qquad t\mapsto t^3+t.
\]

For \(r\in\mathbb Q\), let \(q=r^3+r\). The fiber polynomial factors as

\[
T^3+T-q=(T-r)(T^2+rT+r^2+1).
\]

The quadratic discriminant is \(-3r^2-4<0\), so the quadratic factor is irreducible over \(\mathbb Q\). Its closed point has relative degree two over the rational base point \(q\). The full cubic discriminant is \(-4-27q^2\ne0\), so these fibers are on the étale locus. The function \(r\mapsto r^3+r\) is strictly increasing on \(\mathbb R\), so distinct rational \(r\) give distinct fibers and distinct quadratic points. This relative-degree-two stratum is infinite and hence dense.

The cover is non-Galois: its generic irreducible cubic \(T^3+T-u\) has discriminant \(-4-27u^2\), which is not a square in \(\mathbb Q(u)\) because its geometric zeros have odd order. An irreducible cubic extension is Galois only if its discriminant is a square. Thus \(m\mid n\) genuinely fails pointwise, and even on a dense stratum, for non-Galois covers. This example alone does not refute every stronger possible set-level inclusion between the two density spectra.

An ancillary sharpness example for possible Galois residue multipliers is \(t\mapsto t^n\) over \(k=\mathbb Q(\zeta_n)\). It is a cyclic Galois cover of degree \(n\), étale over \(\mathbb G_m\). Fix \(m\mid n\) and vary rational primes \(p\) unramified in \(k\). At every place over \(p\), the valuation of \(p\) is one, so \(T^m-p\) is Eisenstein and has degree \(m\) over \(k\) (the case \(m=1\) is immediate). Its root \(t=p^{1/m}\) lies over \(p^{n/m}\in k\). Distinct primes give distinct fibers, so every allowed divisor \(m\mid n\) occurs densely for this one cover. This is a statement about residue strata, not an additional classification theorem.

## Curve-component transfer

Here a nice curve is smooth, projective, and geometrically integral over \(k\). Following Viray–Vogt [VV], define \(\delta_{\mathbb P^1}(C/k)\) as the set of degrees of \(\mathbb P^1\)-parameterized closed points. By their Lemma 4.1.4 this is exactly the set of degrees of finite morphisms \(C\to\mathbb P^1_k\). If

\[
W_C^d=\operatorname{im}(\operatorname{Sym}^d C\to\operatorname{Pic}_C^d),
\]

a degree-\(d\) closed point \(x\) is AV-parameterized when there is a \(k\)-abelian subvariety \(A\subseteq J_C=\operatorname{Pic}_C^0\), with \(\operatorname{rank}A(k)>0\), such that \([x]+A\subseteq W_C^d\). The set of such degrees is \(\delta_{\mathrm{AV}}(C/k)\). This containment is a containment of subvarieties. It does not say that every rational point of \(W_C^d\) has an effective divisor representative over \(k\), or that every effective divisor is a closed point.

**Theorem 2.** For a finite degree-\(n\) morphism \(f:C\to D\) of nice curves,

\[
n\delta_{\mathbb P^1}(D/k)\subseteq\delta_{\mathbb P^1}(C/k),
\]

and, for each integer \(r\ge2\),

\[
rn\delta_{\mathrm{AV}}(D/k)
\subseteq\delta_{\mathrm{AV}}(C/k)\cap\delta_{\mathbb P^1}(C/k).
\]

The first inclusion follows by composing a degree-\(e\) map \(D\to\mathbb P^1\) with \(f\).

For the second, let \(x\in D\) be an AV-parameterized point of degree \(e\), witnessed by \([x]+A\subseteq W_D^e\). Pullback and the norm on Jacobians satisfy

\[
f_*f^*=[n]:J_D\to J_D.
\]

This follows on divisors from \(f_*f^*(Q)=nQ\), including the ramification and residue multiplicities. It implies \(\ker(f^*)\subseteq J_D[n]\), a finite group scheme. Thus \(B=f^*(A)\subseteq J_C\) is an abelian subvariety of positive rank: an infinite-order element of \(A(k)\) remains infinite-order under a homomorphism with finite kernel.

Pullback of effective divisors is effective of degree multiplied by \(n\). As a statement about geometric effective classes, it yields

\[
f^*[x]+B\subseteq W_C^{ne}.
\]

Multiplying effective divisors by \(r\) yields

\[
rf^*[x]+[r]B\subseteq W_C^{rne}.
\]

Since multiplication by \(r\) is surjective on the abelian variety \(B\), its image is \(B\), and hence

\[
rf^*[x]+B\subseteq W_C^{rne}. \tag{*}
\]

Only surjectivity as a morphism of varieties is used here. Surjectivity of \(B(k)\xrightarrow{[r]}B(k)\), which can fail, is not being assumed.

The class in (*) must still acquire a closed-point representative. This is where the cited result and Hilbert irreducibility enter. Viray–Vogt Proposition 5.2.1 states that for \(r\ge2\) there is a degree-\(re\), \(\mathbb P^1\)-parameterized closed point \(z\in D\) with \([z]=r[x]\). Their Lemma 4.1.1, or the basepoint-free pencil interpretation, gives a map \(g:D\to\mathbb P^1_k\) of degree \(re\) having \(z\) as a rational fiber. In particular,

\[
g^*\mathcal O(1)\simeq\mathcal O_D(rx).
\]

The composed map \(h=g\circ f:C\to\mathbb P^1\) has degree \(rne\). Hilbert irreducibility, in the form stated in [VV, Proposition 3.3.1], gives a rational \(t\) for which the fiber \(w=h^{-1}(t)\) is a single closed point of exact degree \(rne\). Since all rational fibers of \(h\) have the same divisor class,

\[
[w]=[h^*(t)]=rf^*[x].
\]

Now (*) says \([w]+B\subseteq W_C^{rne}\), so \(w\) is AV-parameterized. It is also \(\mathbb P^1\)-parameterized because it is a closed fiber of \(h\). This proves the stated inclusion. No fiber of \(f\) was silently treated as a single point.

At the undilated degree \(ne\), the unconditional conclusion established by this argument is only \(f^*[x]+B\subseteq W_C^{ne}\). If this translate contains the class of some degree-\(ne\) closed point \(v\), then \([v]+B=f^*[x]+B\), and \(v\) is AV-parameterized. The present argument does not guarantee such a point. In particular, it does not establish \(n\delta_{\mathrm{AV}}(D/k)\subseteq\delta_{\mathrm{AV}}(C/k)\). Reducibility of \(f^*x\) is an obstruction to that formal pullback argument, not a counterexample to the stronger inclusion itself.

## Residual questions and dependencies

The original AIM problem asks broadly which restrictions exist and which are sharp. The proved statements do not determine all possible pairs of spectra, all dense residue multipliers of a given cover, or reverse relations between the curve-component sets. Nor do they establish the undilated AV inclusion just discussed. The cubic example concerns residue behavior, not every conceivable set-level strengthening. These limits prevent classifying the broad original problem as completely solved.

The substantive outside inputs are Clark's index-existence theorem; Hilbert irreducibility over number fields; Viray–Vogt's Proposition 5.2.1 and the equivalence between pencils and \(\mathbb P^1\)-parameterized points; and standard facts about finite étale covers, dimensions of finite morphisms, Riemann–Roch, Picard varieties, and norm/pullback. No global novelty assessment follows from the proof. This audit verifies the stated consequences of these existing results rather than independently reproving every dependency.

## References

- [AIM] American Institute of Mathematics, *Degree d points on algebraic surfaces*, [Problem 1.18 and its remarks](http://aimpl.org/degreedsurface/1/). The exact source capture and inspection scope are recorded separately.
- [Clark] Pete L. Clark, *There are genus one curves of every index over every number field*, Journal für die reine und angewandte Mathematik 594 (2006), 201–206; [DOI](https://doi.org/10.1515/CRELLE.2006.040), [author-hosted text](https://plclark.github.io/PeteLClark/Research/crelle.pdf), [arXiv record](https://arxiv.org/abs/math/0411413). Corollary 4 is on physical page 2 of the inspected author-hosted PDF.
- [VV] Bianca Viray and Isabel Vogt, *Isolated and parameterized points on curves*, Essential Number Theory 5 (2026), 1–47; [DOI](https://doi.org/10.2140/ent.2026.5.1), [published PDF](https://msp.org/ent/2026/5-1/ent-v5-n1-p01-s.pdf), [arXiv record](https://arxiv.org/abs/2406.14353). The cited published version has 48 physical PDF pages because the cover precedes printed page 1. Proposition 5.2.1 occupies printed pages 26–27, physical pages 27–28.
