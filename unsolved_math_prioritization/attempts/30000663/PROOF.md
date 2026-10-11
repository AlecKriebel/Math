# An equivariant étale endomorphism with a ramified quotient

## Review and distribution status

This is an AI-assisted, unrefereed authored reconstruction of an already published example. The review consists of one independent reconstruction plus review of that reconstruction, not a second independent mathematical audit. The internal AI mathematical audit is not external human peer review or formal proof-assistant certification. This eight-file prose edition is not a computational reproduction package. No source-author code, executable checker, copied source document, dataset contents, raw output, or private coordination material is distributed. File hashes authenticate bytes, not mathematical truth.

## Conclusion and attribution

The answer to the question indexed as 30000663, OWR-1452-027, is negative under its stated hypotheses. There is a smooth normal affine complex surface, an effective action of the connected reductive group \(\mathbb G_m\), and an étale endomorphism commuting with that very same action whose induced quotient endomorphism is ramified.

The example is the degree-two specialization of Dubouloz and Palka's published construction in *The Jacobian Conjecture fails for pseudo-planes*, Advances in Mathematics 339 (2018), 248–284, [DOI 10.1016/j.aim.2018.09.020](https://doi.org/10.1016/j.aim.2018.09.020). The precise inspected version is [arXiv:1701.01425v2](https://arxiv.org/pdf/1701.01425v2), Theorem D and Example 4.3. The argument below independently verifies this specialization. No novelty is claimed.

## Exact question

Miyanishi's contribution to *Affine Algebraic Geometry*, Oberwolfach Report 01/2007, printed p. 74 (PDF p. 70), considers a normal affine complex variety, an effective algebraic group action, and an unramified endomorphism commuting with the action. It then asks whether the induced endomorphism of the algebraic quotient is unramified. See the [original report](https://ems.press/content/serial-article-files/46087?nt=1) and [report metadata](https://doi.org/10.4171/owr/2007/01).

The question does not require surjectivity, properness, factoriality, dimension two, or Euler characteristic one. The Euler-characteristic condition occurs in a separate automorphism question. The factorial-surface condition occurs in a separate additive-group special case. In particular, neither condition may be added to the quotient question. The printed assertion that the answer is positive for connected reductive groups is false with the hypotheses stated on that page: the example below has \(G=\mathbb G_m\).

## Surface and action

Work over \(k=\mathbb C\). Set

\[
 A=k[x,y,z]/(F),\qquad F=x^2y-z^2+1,\qquad X=\operatorname{Spec}A.
\]

The polynomial \(F\), regarded as a polynomial in \(y\) over the UFD \(k[x,z]\), is primitive because \(x^2\) and \(1-z^2\) are relatively prime. It is linear and irreducible over \(k(x,z)\). Gauss's lemma therefore shows that \(A\) is a domain. It has dimension two.

The partial derivatives are

\[
 F_x=2xy,\quad F_y=x^2,\quad F_z=-2z.
\]

Their simultaneous vanishing would force \(x=z=0\), at which \(F=1\). Thus \(X\) is smooth everywhere by the hypersurface Jacobian criterion. In particular it is normal.

Let

\[
 a\cdot(x,y,z)=(ax,a^{-2}y,z),\qquad a\in k^*.
\]

This is an algebraic action preserving \(F\). It is effective: a scalar fixing every point must fix \((1,0,1)\), hence must be \(1\).

## The endomorphism and its equivariance

Define

\[
 \varphi(x,y,z)=(2xz,y,2z^2-1).
\]

These are polynomials, so there is no excluded divisor in the definition. The polynomial identity

\[
 F(2xz,y,2z^2-1)=4z^2F(x,y,z)
\]

shows that they define a morphism \(X\to X\). Directly,

\[
 \varphi(ax,a^{-2}y,z)
 =(2axz,a^{-2}y,2z^2-1)
 =a\cdot\varphi(x,y,z).
\]

The action on the target is identical to the action on the source. No power map, isogeny, or other twist of \(\mathbb G_m\) is being used.

## An algebraic étaleness proof covering every point

Use \((u,v,w)\) for target coordinates and put

\[
 B=k[u,v,w]/(u^2v-w^2+1).
\]

The homomorphism \(B\to A\) sends \((u,v,w)\) to \((2xz,y,2z^2-1)\). Consider the target opens

\[
 U_1=D(w+1),\qquad U_2=D(v(w-1)).
\]

On \(U_1\), the inverse image has coordinate ring

\[
 A[1/z]\cong B[1/(w+1)][t]/\bigl(t^2-(w+1)/2\bigr).
\]

The isomorphism sends \(t\) to \(z\); its inverse sends \(x\) to \(u/(2t)\), \(y\) to \(v\), and \(z\) to \(t\). Here \(t\) is a unit since \(t^2=(w+1)/2\). Substitution using \(u^2v=w^2-1\) verifies \(x^2y=z^2-1\). The displayed polynomial is monic of degree two, and its derivative \(2t\) is a unit. Consequently this is a finite étale algebra of rank two.

On \(U_2\), both \(v\) and \(w-1\) are units, and the inverse image has coordinate ring

\[
 A[1/(xy)]\cong B[1/(v(w-1))][s]/\bigl(s^2-(w-1)/(2v)\bigr).
\]

The isomorphism sends \(s\) to \(x\); its inverse sends \(x\) to \(s\), \(y\) to \(v\), and \(z\) to \(u/(2s)\). In this algebra \(s\) is a unit and

\[
 \left(\frac{u}{2s}\right)^2
 =\frac{u^2v}{2(w-1)}=\frac{w+1}{2},
 \qquad s^2v=\frac{w-1}{2}.
\]

These identities verify the equations and both directions of the isomorphism. Its defining monic polynomial has invertible derivative \(2s\), so this too is finite étale of rank two. The indicated inverse-image localization follows also from

\[
 \varphi^*(v(w-1))=2y(z^2-1)=2x^2y^2.
\]

These two inverse images cover \(X\): if \(z\ne0\) the point is in the first; if \(z=0\), the equation \(x^2y=-1\) forces both \(x\) and \(y\) to be nonzero, putting the point in the second. Thus \(\varphi\) is étale at every point, including every point over \(x=0\) and \(z=0\). This proof is algebraic and establishes flatness as well as unramifiedness; it does not infer étaleness merely from a generic Jacobian.

## Independent differential check at the exceptional loci

The ambient derivative is

\[
 D\varphi=
 \begin{pmatrix}
 2z&0&2x\\
 0&1&0\\
 0&0&4z
 \end{pmatrix},\qquad \det D\varphi=8z^2.
\]

For \(z\ne0\), this is an isomorphism of ambient tangent spaces. Differentiating \(F\circ\varphi=4z^2F\) on \(X\) shows that it maps the source tangent plane into the target tangent plane; both have dimension two. Its restriction is therefore an isomorphism. In particular this covers \(x=0\), where \(z=\pm1\), including \((0,0,\pm1)\).

For \(z=0\), write a tangent vector as \((\dot x,\dot y,\dot z)\). The source tangent equation is

\[
 2xy\dot x+x^2\dot y=0.
\]

The image point is \((0,y,-1)\), whose target tangent equation is \(\dot w=0\). The tangent map is

\[
 (\dot x,\dot y,\dot z)\longmapsto(2x\dot z,\dot y,0).
\]

Because \(x,y\ne0\), a vector in its kernel has \(\dot z=\dot y=0\), and then the source tangent equation forces \(\dot x=0\). Thus the map between the two tangent planes is again an isomorphism. Equivalently, using source local coordinates \((x,z)\) and target étale coordinates \((u,v)\), the local determinant at \(z=0\) is \(-4/x^2\), not zero. The zero ambient determinant at this locus is therefore not a ramification certificate for the surface morphism.

## The invariant ring and ramified quotient

Give \(k[x,y,z]\) weights \(1,-2,0\). A weight-zero monomial \(x^iy^jz^\ell\) has \(i=2j\). Therefore the weight-zero subring is \(k[x^2y,z]\). Since \(F\) has weight zero, the grading descends to \(A\), and its degree-zero part is

\[
 A^{\mathbb G_m}=A_0
 =k[q,z]/(q-z^2+1)=k[z],\qquad q=x^2y.
\]

To justify the quotient step explicitly, multiplication by the homogeneous degree-zero polynomial \(F\) preserves each weight, so the weight-zero part of the ideal \((F)\) is \(F\,k[x^2y,z]\). The invariants for a torus action are precisely the weight-zero part. No set-theoretic orbit-space assumption is needed.

Thus \(X//\mathbb G_m=\mathbb A^1_z\), with quotient morphism \(\pi(x,y,z)=z\). The induced map is

\[
 \psi(z)=2z^2-1,
 \qquad\pi\circ\varphi=\psi\circ\pi.
\]

Its derivative is \(4z\), zero at \(z=0\). Algebraically,

\[
 \Omega_{k[z]/k[w]}=k[z]\,dz/(4z\,dz),
 \qquad w\longmapsto2z^2-1,
\]

has nonzero fiber at \(z=0\). Hence \(\psi\) is not unramified there. Its ramification index is two because \(\psi(z)+1=2z^2\).

## Exact image and the role of surjectivity

The two target opens above have union

\[
 U=U_1\cup U_2=X\setminus L,\qquad L=V(v,w+1)\cong\mathbb A^1_u.
\]

They are in the image: each rank-two finite étale algebra is faithfully flat, or one can use the explicit formulas below. Thus \(\varphi\) factors as a finite étale degree-two map \(X\to U\) followed by the open immersion \(U\hookrightarrow X\).

For a target point with \(w\ne-1\), choose either nonzero square root \(z\) of \((w+1)/2\), and set \(x=u/(2z)\), \(y=v\). For \(w=-1\) and \(v\ne0\), the target equation forces \(u=0\); take \(z=0\), \(y=v\), and either square root \(x\) of \(-1/v\). These give two distinct preimages in every nonempty fiber.

Conversely, \(w=-1\) forces \(z=0\), which forces \(u=0\) and \(v\ne0\). Every point \((u,0,-1)\), for arbitrary \(u\), is missed. The omitted set is this entire line, not only its origin. The morphism is dominant but not surjective and therefore is not proper. None of surjectivity, finiteness, or properness is assumed in the source question. This example makes no assertion about a version in which surjectivity is added.

## Match to the published construction

Example 4.3 of Dubouloz–Palka displays the family on \(\widetilde S(2,2)=X\) with coordinates

\[
 (\lambda^{-1}xU_{d-1}(z),\lambda^2y,T_d(z)).
\]

Taking \(d=2\), \(\lambda=1\), \(U_1(z)=2z\), and \(T_2(z)=2z^2-1\) gives exactly \(\varphi\). Existence is checked against the converse part of Theorem D, rather than inferred from the example's necessary-form discussion alone. In Theorem D's different normalization, take

\[
 k=r=d=2,\ a=1,\ \alpha=0,\ R_0(t)=4,
 \ R_1(t)=1-2t,\ R_2(t)=1,\ \lambda=2.
\]

Then equations (4.3)–(4.5) reduce to

\[
 4t(1-t)=1-(1-2t)^2,
 \qquad (1-t)R_0R_1R_2=4(1-t)(1-2t),
\]

with the required distinct roots and normalizations; the degree congruence also holds. Formula (4.6) gives our morphism exactly. Theorem D's proof identifies the quotient on the covering surface as \(\operatorname{pr}_z\).

The fiber multiplicities explain the apparent conflict between an étale surface map and a ramified base map. The divisor \(\pi^*(-1)\) has components \(V(y,z+1)\) of multiplicity one and \(V(x,z+1)\) of multiplicity two. The reduced fiber \(z=0\) maps into the latter away from their intersection, with base ramification index two. This is precisely the multiplicity balance in Lemma 2.18. At \(z=\pm1\), each multiplicity-one or multiplicity-two component maps to its counterpart over \(1\), with base ramification index one. The direct algebraic verification above is independent of that lemma's general converse.

## Scope of the conclusion

This is a credited prior negative resolution of the exact quotient question. It also refutes the unrestricted connected-reductive assertion printed with that question. It is not a proof of a new classification, a solution of the ordinary Jacobian Conjecture, an audit of the entire Dubouloz–Palka paper, or a counterexample to an added surjectivity hypothesis.
