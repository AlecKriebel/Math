# Three distinct Anosov torus maps with pairwise braid relations

**Problem:** 11000147 / AMR-109-0147.  
**Status:** complete candidate for the source's existential question, pending separate adversarial review; historical priority is unconfirmed and this note is not peer reviewed.  
**Scope:** actual orientation-preserving diffeomorphisms of the closed torus, and consequently their distinct mapping classes. All three braid lengths are exactly three.

## 1. Source and interpretation

In B. Wajnryb's *Relations in the mapping class group*, Section 2, the question is:

> Does there exist a set of at least three pseudo-Anosov homeomorpisms such that every pair satisfies a braid relation.

The [author-hosted volume](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf) places this on printed page 124, PDF page 131. Its introductory convention permits compact surfaces, possibly with boundary, and uses isotopy classes of orientation-preserving maps on oriented surfaces. The paragraph immediately following the question explicitly discusses Anosov matrices on the torus. Thus the torus is an allowed surface in the question's convention. No prescribed genus, nonconjugacy, minimal generating set, or faithful Artin-group representation is required here. The surrounding embedding questions are stronger, distinct targets.

We give three distinct, pairwise noncommuting maps. The relations hold as maps, so there is no issue of choosing representatives of mapping classes. We use the source's inclusion of torus Anosov maps in this question; this does not assert that the surface has negative Euler characteristic or a nonempty set of foliation singularities.

## 2. An elementary group lemma

**Lemma.** Let \(a,b\) be distinct elements of a group and suppose
\[
aba=bab.
\]
Set \(c=aba^{-1}\). Then \(a,b,c\) are distinct, every unordered pair satisfies the length-three braid relation, and no pair commutes.

**Proof.** Multiplication of the given relation on the left by \(b^{-1}\) and on the right by \(a^{-1}\) gives
\[
c=aba^{-1}=b^{-1}ab.
\]
Conjugating the relation \(aba=bab\) by \(a\) gives
\[
aca=cac.
\]
Conjugating it by \(b^{-1}\) gives
\[
cbc=bcb.
\]
If \(c=a\), cancellation in \(aba^{-1}=a\) gives \(b=a\), a contradiction. If \(c=b\), then \(ab=ba\). A commuting pair \(x,y\) satisfying \(xyx=yxy\) must be equal, since \(x^2y=xy^2\) and cancellation gives \(x=y\). Hence \(c=b\) is also impossible. This last observation applies to all three pairs and proves their noncommutativity. \(\square\)

In particular, for any conjugacy-invariant class of group elements, a distinct braid-related pair in that class supplies such a triple in the same class. Pseudo-Anosov mapping classes are one example. This lemma does not construct the initial pair on a surface of any specified higher genus.

## 3. Explicit maps on the closed torus

Let \(T^2=\mathbb R^2/\mathbb Z^2\), with column-vector coordinates, and set
\[
A=\begin{pmatrix}3&1\\2&1\end{pmatrix},\qquad
B=\begin{pmatrix}1&-2\\-1&3\end{pmatrix},\qquad
C=\begin{pmatrix}8&-11\\3&-4\end{pmatrix}.
\]
For an integer matrix \(M\) of determinant one, write
\[
f_M([v])=[Mv].
\]
This is a well-defined, smooth, orientation-preserving torus diffeomorphism: \(M\) preserves \(\mathbb Z^2\), its inverse is integral, and its derivative has positive determinant. With ordinary composition, \(f_M\circ f_N=f_{MN}\).

Each displayed matrix has determinant one and trace four. Further,
\[
C=ABA^{-1},\qquad
ABA=BAB=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]
Thus the lemma already establishes the three pairwise braid relations. For direct verification, the other two common products are
\[
ACA=CAC=\begin{pmatrix}7&-10\\5&-7\end{pmatrix},\qquad
BCB=CBC=\begin{pmatrix}5&-13\\2&-5\end{pmatrix}.
\]
The matrices are distinct, and hence so are their induced actions on \(H_1(T^2;\mathbb Z)\). Therefore the three maps are distinct even up to isotopy. By the lemma, they are pairwise noncommuting. In particular, no pair satisfies a length-one or length-two Artin relation.

## 4. Hyperbolicity and the measured foliations

The characteristic polynomial of each matrix is
\[
t^2-4t+1.
\]
Its roots are
\[
\lambda=2+\sqrt3>1,\qquad
\lambda^{-1}=2-\sqrt3\in(0,1).
\]
For each of \(A,B,C\), the two real eigenlines define transverse constant line fields on \(\mathbb R^2\), invariant under integer translations. They descend to two nonsingular foliations of \(T^2\). A nonzero constant linear form annihilating an eigenline defines the corresponding transverse measure by integration of its absolute value. Under \(f_M\), the two transverse measures scale by the reciprocal factors \(\lambda\) and \(\lambda^{-1}\).

For completeness, if \(\ell_s\) annihilates the contracting eigenline and is nonzero on the expanding eigenline, then \(\ell_s M=\lambda\ell_s\). Likewise, a covector \(\ell_u\) annihilating the expanding line satisfies \(\ell_u M=\lambda^{-1}\ell_u\). These equations give the claimed transverse-measure scaling globally. The eigenlines have irrational slope: a rational eigenline of an integral matrix would give a rational eigenvalue, whereas \(2\pm\sqrt3\) are irrational.

The derivative is the same matrix at every point. It contracts one of these line fields uniformly and expands the other uniformly, so \(f_A,f_B,f_C\) are Anosov torus diffeomorphisms, with stretch factor \(2+\sqrt3\). Equivalently, they are the nonsingular torus instances of the invariant-measured-foliation condition used in the source's question.

It follows that
\[
\{f_A,f_B,f_C\}
\]
is the required set of three maps. \(\square\)

## 5. What this construction does and does not establish

The construction answers the stated existential question on an explicitly allowed compact surface. It also shows that extending a distinct length-three braid pair to a triple is an elementary group-theoretic step. The source already credits its referee with the existence of suitable pairs; no discovery of that pair mechanism is claimed here.

All three elements are conjugate, as expected for odd braid relations, and the group they generate is already generated by the first two. These facts do not violate the stated question. They would matter for stronger requirements such as a minimal three-element generating set or a faithful triangular Artin-group representation. Neither such conclusion is asserted. No construction for every prescribed higher-genus surface, or for a one-holed torus with boundary fixed pointwise, is claimed.

The exact computations in the accompanying verifier check the displayed identities and the finite-coordinate realization. The proof above, rather than those finite checks, establishes the torus dynamics and the universal group lemma. A bounded literature search did not establish historical priority; the result should be presented as an elementary explicit answer with that qualification.
