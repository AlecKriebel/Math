# The full Milnor algebra in ordinary order two for two-string links

## Result and scope

Let \(SL_2\) consist of smooth, unframed, ordered, upward-oriented two-string links with fixed matching endpoints. Let \(\mathcal V_{\le2}\) be the rational-valued ordinary Vassiliev invariants of order at most two, including constants, and let
\[
\mathcal M_{\le2}=\mathcal V_{\le2}\cap\mathbb Q[\mu_I:I\text{ any multi-index}],
\]
where all the based string-link Milnor invariants are allowed, including repeated indices. Then
\[
\boxed{\mathcal M_{\le2}=\operatorname{span}_{\mathbb Q}\{1,\ell,\ell^2\}},
\qquad \ell=\mu_{12}=\operatorname{lk}.
\]

The argument applies to the intersection with the **entire** Milnor algebra. It does not assume that an initially given polynomial in Milnor invariants has weighted degree at most two, so cancellations between higher-degree expressions cause no gap. In fact, the proof identifies all rational order-at-most-two smooth-concordance invariants as the displayed three-dimensional space.

## Published inputs

1. J.-B. Meilhan, *On Vassiliev invariants of order two for string links*, [arXiv:math/0402036v2](https://arxiv.org/pdf/math/0402036v2), Definitions 1.1–1.3, §2.1 and Theorem 2.4, preprint pp. 1–5. The fixed-endpoint, ordered, upward convention and the ordinary framing-independence relation are explicit. For two strings the theorem says that every \(v\in\mathcal V_{\le2}\) has an expansion
   \[
   v=c_0+c_1\ell+c_2\ell^2+b_1a_1+b_2a_2+d w,
   \tag{1}
   \]
   where \(a_i=a_2(\widehat{L_i})\), and
   \[
   w(L)=a_2(p(L))-a_1(L)-a_2(L).
   \tag{2}
   \]
   Here \(p\) joins the two bottom endpoints to each other and the two top endpoints to each other using the standard caps. This is Meilhan's \(V_2\); the notation \(w\) avoids confusing it with the vector space of invariants. Section 2.1 also gives \(a_2\) of the unknot and trefoil as 0 and 1. The journal version is J. Knot Theory Ramifications 14 (2005), 665–687.
2. J.-B. Meilhan and A. Yasuhara, *Characterization of Finite Type String Link Invariants of Degree <5*, [arXiv:0904.1527v1](https://arxiv.org/pdf/0904.1527v1), §2.1.4 and §5.1, especially preprint p. 22. Their Milnor convention allows repeated indices, and §5.1 explicitly states concordance invariance of Milnor invariants in the fixed-endpoint string-link setting. It cites A. J. Casson, *Link cobordism and Milnor's invariant*, Bull. London Math. Soc. 7 (1975), 39–40, [DOI 10.1112/blms/7.1.39](https://doi.org/10.1112/blms/7.1.39). No reduction to nonrepeating indices is made here.
3. T. D. Cochran and S. Harvey, *The geometry of the knot concordance space*, [author-hosted arXiv v2](https://math.rice.edu/~shelly/publications/arxiv_geometry_knot_conc.pdf), introduction, preprint pp. 1–2: smooth concordance classes form a group under connected sum; the inverse is the orientation-reversed mirror, and the identity is the unknot. This supplies the standard smooth-sliceness fact \(K\mathbin\#(-K)\sim U\).
4. J. Conant, *Chirality and the Conway polynomial*, [published paper](https://topology.nipissingu.ca/tp/reprints/v30/tp30110.pdf), Topology Proceedings 30 (2006), 153–162, §1, p. 154, explicitly recalls multiplicativity of the Conway polynomial under connected sum. The retained [arXiv:math/0503648v2](https://arxiv.org/pdf/math/0503648v2) gives this fact in §1, p. 1. The mirror/reversal identities used below also follow immediately from the Conway skein characterization, so no knot-table calculation is required.

The auxiliary geometry below is proved directly. No special theorem about satellite operators, concordance filtrations, or weighted Milnor-algebra generation is needed.

## Three null-concordant tests

Let \(T\) be the long trefoil and put \(S=T\mathbin\#(-T)\). Its closure is the square knot. It is smoothly concordant to the trivial long knot. The corresponding long concordance can be fixed on the two endpoint collars; equivalently one cuts open the standard based knot concordance along a product strip. The familiar slice construction can also be seen by taking the product of a knotted arc with an interval in a four-ball; its boundary is the arc's closure summed with its reverse mirror.

The Conway identities
\[
\nabla_{K\#J}(z)=\nabla_K(z)\nabla_J(z),\qquad
\nabla_{\overline K}(z)=\nabla_K(-z),\qquad
\nabla_{K^r}(z)=\nabla_K(z)
\]
give \(a_2(S)=a_2(T)+a_2(-T)=2\). These identities follow from the normalized Conway skein characterization; the first can also be obtained from block-diagonal Seifert matrices. Only the even coefficient \(a_2\) is used, so mirror and orientation conventions do not change the value.

Let \(E_1\) be obtained from the trivial two-string link by tying a copy of \(S\) into the first strand, in a small ball disjoint from the second strand. Apply the long null-concordance inside that ball times the concordance interval and keep the second strand fixed. Thus \(E_1\) is concordant to the identity. Its linking number is zero; the component coefficients are \((2,0)\); and its plat is the same local knot \(S\), with an otherwise unknotted closing arc. Hence \(w(E_1)=2-2-0=0\). Similarly a local copy on the second strand gives a null-concordant \(E_2\), with component coefficients \((0,2)\) and \(w(E_2)=0\). Reversing the second strand when tracing the plat does not affect its Conway polynomial.

For the third test, choose a smooth long concordance rectangle
\[
A:I\times I\hookrightarrow (D^2\times I)\times I
\]
from \(S\) to the straight long unknot, standard on the two endpoint collars. Its oriented rank-two normal bundle is trivial. Prescribe a nonzero normal field to be the usual parallel direction along the top edge and the two endpoint edges. These three edges form a contractible proper boundary arc, so this prescription extends to a nonzero normal field on all of the rectangle. Choose the associated tubular neighborhood small enough that the two push-offs by \(\pm\varepsilon\) are disjoint.

The two push-offs give a fixed-endpoint, labeled concordance of two-string links whose top is the identity. Write \(C(S)\) for its bottom. Both bottom strands have the upward orientation of \(S\), and forgetting either strand gives a long knot isotopic to \(S\). Consequently its component coefficients are \((2,2)\). Its linking number is zero, since it is concordant to the identity. In particular its induced parallel framing is the zero-linking framing. This avoids assuming that an arbitrarily prescribed bottom framing extends across a concordance.

At the bottom the normal field sweeps out an embedded narrow ribbon rectangle \(R\subset D^2\times I\) along \(S\). Its long edges are exactly the two components of \(C(S)\). Because the normal field is standard near both endpoint edges, the short edges of \(R\) are exactly the prescribed plat caps, after the harmless collar adjustment used to form the plat. Thus \(p(C(S))=\partial R\). The boundary of this embedded disk is the unknot, even though its core is a knotted long arc. Therefore
\[
w(C(S))=0-2-2=-4.
\]

The three null-concordant tests have coordinate rows
\[
\begin{array}{c|rrrr}
&\ell&a_1&a_2&w\\\hline
E_1&0&2&0&0\\
E_2&0&0&2&0\\
C(S)&0&2&2&-4.
\end{array}
\tag{3}
\]
The determinant of the last three columns is \(-16\). There is no claim that these three auxiliary test links have free three-dimensional exteriors; no such claim is needed in this global algebra lemma.

## Proof of the algebra statement

Every Milnor invariant is constant on smooth concordance classes, and hence every polynomial in any finite collection of them is constant on concordance classes. This assertion is independent of the finite-type orders of the generators appearing in that expression.

Take \(m\in\mathcal M_{\le2}\). Its ordinary order bound permits expansion (1). As all three links in (3) are concordant to the identity, subtracting the value at the identity gives
\[
2b_1=0,\qquad 2b_2=0,\qquad 2b_1+2b_2-4d=0.
\]
Over \(\mathbb Q\), this forces \(b_1=b_2=d=0\), so \(m\) belongs to the displayed span. Conversely, \(\ell=\mu_{12}\) has ordinary order one; its square has order at most two, and constants are allowed. All three therefore belong to \(\mathcal M_{\le2}\). They are independent because two-string pure braids realize every integer linking number. This proves the equality.

## Alternative published framework and cautions

Habegger–Masbaum, *The Kontsevich integral and Milnor's invariants*, author preprint dated 7 April 1999, [author-hosted source](https://webusers.imj-prg.fr/~gregor.masbaum/K39.ps.gz), §4 and Theorem 15.1, provides a second route: finite-type concordance invariants are governed by the tree quotient, and an order-two connected tree with only two colors vanishes rationally by antisymmetry. In the unframed specialization only the mixed strut remains in order one, giving the same three filtered dimensions. However, that paper is explicitly framed. The elementary proof above is preferable for this application because it never imports a framing variable or assumes a filtered version of an unfiltered algebra-generation assertion.

Meilhan–Yasuhara Theorem 5.9 is not a statement that order-two integral concordance invariants are determined just by linking: it includes Arf and mod-two Milnor information. Our rational-coefficient argument, including division by 2 and 4, must not be advertised over arbitrary coefficient groups.

This lemma settles only the algebraic input at two strands and order two. By itself it neither proves a free-exterior witness nor answers the independent nontriviality question for the kernel of restriction to free-exterior string links.
