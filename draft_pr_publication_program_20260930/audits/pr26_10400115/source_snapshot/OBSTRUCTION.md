# 10400115: algebraic-coefficient braid representations remain unresolved here

**Outcome:** no full solution. The generic-specialization route is blocked by a uniform injectivity gap. The elementary observations below are not claimed as new mathematics or as a solution for \(n\ge4\).

**Exact target:** for each fixed \(n\), does there exist some finite \(d\) and an injective homomorphism
\[
B_n\longrightarrow\mathrm{GL}_d(\overline{\mathbb Q})?
\]
The dimension is unrestricted. A faithful representation over a function field, an infinite product of representations, or a family separating every finite collection of words does not settle this question.

## 1. Source audit

The exact source is [Ohtsuki, *Problems on invariants of knots and 3-manifolds*](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), Problem 6.7, printed p.470 (PDF page98). The bar over \(\mathbb Q\) was visually checked. The dataset title is truncated; the intended title is “Faithful braid-group representations over algebraic numbers.” The source identifies \(n\ge4\) as the unresolved range and explains that faithfulness over two-variable Laurent polynomials does not establish an algebraic specialization.

A recent relevant primary result is [Nancy Scherich, *Discrete real specializations of sesquilinear representations of the braid groups*](https://msp.org/agt/2023/23-5/agt-v23-n5-p03-s.pdf), *Algebraic & Geometric Topology* 23 (2023), 2009–2028, DOI [10.2140/agt.2023.23.2009](https://doi.org/10.2140/agt.2023.23.2009). Theorem1.1 and Corollary3.10 give algebraic Salem-number specializations with discrete image, including Lawrence–Krammer representations. Their conclusions are discreteness, not injectivity. Example3.11 supplies a discrete specialization for \(B_4\), without a faithfulness assertion. The statements and the full relevant sections were inspected; no occurrence of “faithful” appears in the extracted article text.

No full resolution of the exact target was located in the current search. This is a limited literature check, not a certificate that no solution exists in the literature.

## 2. Algebraic coefficients are equivalent to rational coefficients when degree may increase

**Proposition.** A finitely generated group has a faithful finite-dimensional representation over \(\overline{\mathbb Q}\) if and only if it has one over \(\mathbb Q\).

**Proof.** The finitely many entries of a finite generating set of matrices generate a number field \(K\). All group matrices have entries in \(K\), including inverses. Viewing \(K^d\) as a \(\mathbb Q\)-vector space gives an injective homomorphism
\[
\mathrm{GL}_d(K)\hookrightarrow\mathrm{GL}_{d[K:\mathbb Q]}(\mathbb Q).
\]
The reverse implication is immediate. \(\square\)

Thus increasing the field from \(\mathbb Q\) to its algebraic closure does not remove the existence difficulty here. This says nothing about preserving the matrix degree.

## 3. The precise specialization gap

Let \(\rho\) be a faithful Laurent-polynomial representation of a finitely generated group. For each nonidentity word \(w\), at least one entry of \(\rho(w)-I\) is a nonzero Laurent polynomial. For any finite collection of nonidentity words, one can avoid all their zero sets simultaneously at rational parameters, while also avoiding denominator and determinant zeros. This gives faithful behavior on arbitrary prescribed finite sets.

Faithfulness of one specialization would require avoiding the exceptional sets for **all** nonidentity words at once. A countable union of proper algebraic sets can cover every algebraic point. Neither Zariski genericity nor a finite word search bridges that gap.

The following two-generator example shows that this issue is substantive, even before addressing braids. Let \(x\) be indeterminate and set
\[
a=\begin{pmatrix}x&0\\0&1\end{pmatrix},\qquad
b=\begin{pmatrix}1&1\\0&1\end{pmatrix}
\quad\text{in }\mathrm{GL}_2(\mathbb Q(x)).
\]
Let \(G=\langle a,b\rangle\), with its faithful inclusion into this matrix group. Writing \(U(f)=\begin{pmatrix}1&f\\0&1\end{pmatrix}\), we have
\[
a^kba^{-k}=U(x^k),\qquad U(f)U(g)=U(f+g).
\]
Hence \(U(f)\in G\) for every \(f\in\mathbb Z[x,x^{-1}]\).

For any nonzero algebraic specialization \(x=\alpha\), choose a nonzero integer polynomial \(f\) with \(f(\alpha)=0\). Then \(U(f)\ne I\) over \(\mathbb Q(x)\), but its specialization is \(I\). Consequently **every valid algebraic specialization of this faithful two-generator representation is unfaithful**. The excluded value \(\alpha=0\) makes \(a\) singular.

This is a counterexample to a general specialization inference, not a counterexample to Bigelow's braid-group question. It does not establish that a particular Lawrence–Krammer specialization fails.

## 4. A printed low-strand error, and the correct easy case

The source's adjacent remark says that \(B_3\) embeds in \(\mathrm{GL}_2(\mathbb Z)\). That assertion is false as printed.

Indeed, the center of \(B_3\) is infinite cyclic. Under a hypothetical faithful representation into \(\mathrm{GL}_2(\mathbb Z)\), its generator would have infinite order. It cannot be scalar, since the only invertible integral scalar matrices are \(\pm I\). But the centralizer of any nonscalar two-by-two rational matrix \(C\) is the commutative algebra \(\mathbb Q[C]\). The whole image of \(B_3\) would lie in that centralizer and be abelian, a contradiction.

The intended easy case over algebraic numbers is nevertheless valid. Put
\[
U=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
V=\begin{pmatrix}1&0\\-1&1\end{pmatrix}.
\]
The assignment
\[
\sigma_1\mapsto2U,\qquad\sigma_2\mapsto2V
\]
defines a faithful representation \(B_3\to\mathrm{GL}_2(\mathbb Q)\).

To verify faithfulness, let \(e:B_3\to\mathbb Z\) send each generator to1 and let \(\phi\) send the generators to \(U,V\). The standard modular-group presentation identifies the induced map
\(B_3/\langle z\rangle\to\mathrm{PSL}_2(\mathbb Z)\) as an isomorphism, where \(z=(\sigma_1\sigma_2)^3\). The displayed representation is \(\rho(g)=2^{e(g)}\phi(g)\). If \(\rho(g)=I\), determinants give \(4^{e(g)}=1\), hence \(e(g)=0\). Its projective image is trivial, so \(g=z^k\); then \(0=e(g)=6k\), giving \(g=1\). In particular \(\rho(z)=-64I\), so the central kernel of the untwisted modular representation has not been overlooked.

For \(n=1\) the group is trivial and for \(n=2\) it is infinite cyclic, which embeds by \(1\mapsto2\in\mathbb Q^\times\). These low-strand cases do not address the requested general problem.

## 5. Honest stopping point

No argument was found making one algebraic specialization injective on all braid words, and no obstruction to all finite-dimensional algebraic representations of \(B_n\) was proved. Discreteness of recent Salem-number specializations does not supply this missing assertion. Nor does an infinite family of rational representations with trivial joint kernel yield one finite-dimensional faithful representation.

The route is therefore marked **blocked**, after one substantive investigation. It should be reopened only with a mechanism giving uniform injectivity, a genuinely different algebraic-coefficient construction, or an exact later theorem. Finite searches can test a proposed construction but cannot settle this gap by themselves.
