# Independent exact-statement priority assessment: Stoimenow 2010 and PR177

Prepared before exposure to any sibling reviewer or Root scientific assessment. This is an independent bounded-source review, not a novelty clearance or a recommendation to promote PR177. The overall PR177 completion estimate remains 40% and is outside this reviewer’s authority.

## Result

The supplied 46-page primary body does **not contain an explicit negative Nullstellensatz statement for the full algebra of finite-order link invariants, nor an equivalent theorem formulated with principal ideals, radicals, actual-link zero sets, and nonactual algebra characters**. The paper’s relevant published result is the full finite-type braiding-polynomial mechanism, not merely polynomiality for a selected list of quantum invariants. The exact proposed counterexample is a short mathematical consequence of that mechanism plus elementary linking-number facts and polynomial evaluation. That proximity substantially limits any novelty claim: absence of the target’s wording from this one paper is not positive evidence of new mathematics.

Strongest independently checked statement here: in the ordinary uncompleted complex algebra V, either for all oriented finite-component links with a uniform finite order for each invariant, or for fixed m >= 2 components, the proposed g and f give g in J_actual(Z_actual(fV)) but g not in sqrt(fV). A complete check is given below. This establishes validity of the described mechanism; it does not establish historical novelty.

## Source identity and read scope

A. Stoimenow, *Application of Braiding Sequences, I: On the Characterization of Vassiliev and Polynomial Link Invariants*, Communications in Contemporary Mathematics 12(5) (2010), 681-726, DOI 10.1142/S0219199710003944.

The user-supplied local PDF has SHA256 86b9466b99f2cf67656b49311e67b97267c807d6c0f99d746a874c74379ca508 and 46 pages. PDF page r corresponds to printed page 680+r. The complete layout text was read in six ordered blocks covering PDF pages 1-46. Critical statements on PDF pages 9, 10, 11, 29, 30, and 34 were also visually checked. PDF page 42 / printed page 722 was visually inspected because its rotated numerical table is not adequately captured by the layout extraction. The table concerns concrete knot-polynomial examples for the linear-independence argument; its numerical entries were not independently recomputed.

No other reviewer’s report, Root report, manuscript, or queue was read. No other individuals or chats were contacted. The PDF, extraction, and page renders are third-party private reading material and are not deliverables. This report uses paraphrase and original derivation, with no quoted theorem paragraphs.

## Exact statement ledger and relevance

| Anchor | Published content, paraphrased | Relation to PR177 |
|---|---|---|
| Theorem 1.1, printed 682 / PDF 2; proof at printed 702-703 / PDF 22-23 | A finite-type invariant is characterized by polynomial behavior on braiding sequences together with a polynomial crossing-number bound; the bound’s degree tracks finite-type degree. The statement includes links, tangles, and graph embeddings. | Broader characterization, but no ideal or zero-set conclusion. The growth half is not needed for the counterexample. |
| Section 2.5, printed 689-690 / PDF 9-10 | Finite type is defined by the crossing-difference rule after linear extension to formal combinations. Orientation is required for links, tangle strands, and graph edges. Invariant values are taken on a fixed underlying object, so links have an arbitrary but fixed number of components. Values in C are explicitly allowed, besides Z, Q, and R. | Supplies the relevant coefficient and fixed-component scope. Formal combinations are used to define finite type, not introduced as algebraic zero-locus points. |
| Definitions 2.2-2.3, printed 690-691 / PDF 10-11 | A crossing can be replaced by an odd signed number of half twists, either with parallel or opposite strand orientations. Several crossings give a family with odd integer parameters. Polynomial degree means total degree over all those parameters. | The even closed-two-braid family fits after a linear change of parameter and one fixed crossing. The formal half-integer point is outside the actual family. |
| Theorem 2.1, printed 691 / PDF 11, explicitly credited to reference [63] | For each finite k, an invariant has finite-type degree at most k exactly when every braiding polynomial has total degree at most k. | This is the decisive mechanism for **each member of the entire ordinary algebra**, because each invariant has some finite k. No common finite degree bound over the entire algebra is necessary. |
| Lemma 4.1, printed 704 / PDF 24 | A bound on Conway coefficients is proved, with its degree-one case identifying the two-component linking-number invariant. | Consistent with the standard linking-number input; it does not construct g, f, or an ideal. |
| Proposition 4.1 and Corollaries 4.3-4.4, printed 705-706 / PDF 25-26 | Finite-degree link invariants are determined by certain finitely described braiding families and by bounded-crossing positive or alternating links; a sharper knot version follows. | Determination on these large actual-link classes does not imply radical equality for the much narrower zero set g=0. |
| Section 4.3, printed 707-708 / PDF 27-28 | Torsion-valued invariants and their standard polynomial forms modulo p are considered separately. | Positive-characteristic periodicity cannot replace the characteristic-zero polynomial evaluation required here. |
| Definitions 4.3-4.6 and Theorem 4.4, printed 708-710 / PDF 28-30 | Extended and periodically extended invariants are introduced. Algebraic dependence is defined by a finite polynomial relation with rational coefficients on a set of **knots**. Certain subsets mixing finite-type invariants and specified Jones/Q evaluations have the same algebraic-dependence status on all knots as on special alternating knots; a related braid statement is given for a smaller collection. | This is a statement about finite polynomial relations and testing classes, not about ideals and radicals in the full complex invariant algebra. It supplies no counterexample equivalent to the target. Here g vanishes identically on knots, so the proposed witness is inherently a link result. |
| Corollary 1.1, printed 683-684 / PDF 3-4; proof at printed 711 / PDF 31; Theorem 4.5, printed 710 / PDF 30 | Nonconstant invariants determined by finitely many selected link-polynomial coefficients or certain expansion coefficients cannot be finite type, with respective conditions on the determining function. | The coefficients in question are the ordinary link-polynomial coefficients, not the entire finite-type algebra. These are not Nullstellensatz theorems. |
| Theorem 1.3, printed 684 / PDF 4; Section 5, printed 713-723 / PDF 33-43; Corollary 5.1 and Problem 5.1, printed 714 / PDF 34 | Linear independence of admissible Jones, skein, and Kauffman coefficients is established except for specified familiar relations. The linear-function finite-type consequence is sharpened; algebraic independence and coefficient-value surjectivity are posed as further questions. | Linear independence and these open questions concern a different collection of invariants. They neither state nor negate the target radical failure. The existence of open coefficient questions is not evidence of novelty for PR177. |
| References [63], [68], [23], printed 724-726 / PDF 44-46 | The paper credits Stoimenow 2000 for the braiding-polynomial approach, Trapp 1994 for twist sequences, and discusses Eisermann 2003 for geometric characterization. | The polynomiality mechanism predates 2010. Those sources need their own primary-body review before any claim about earliest priority. |

A whole-body term scan found no occurrences of Nullstellensatz, ideal, radical, or completion. This is supporting indexing evidence only. The substantive determination above rests on reading the complete body and the actual scope of its algebraic-dependence and determination statements.

## Exact derivation: what the paper supplies and what must still be added

Let V be the algebra of complex-valued finite-order invariants of oriented links, with pointwise operations, without any completion. Fix m >= 2 if desired. For all component counts use the two-component family below; for a fixed m append m-2 split unknots.

1. **Linking input and membership in V.** Temporarily label components and write ell_ij for pairwise linking number. A crossing change between distinct components changes exactly the relevant ell_ij by 1 up to sign; its second crossing difference is zero. Hence ell_ij has type at most 1. Finite-type products have type at most the sum of their types, by the crossing-difference product rule. Therefore the symmetric, label-independent invariant

   g(L) = sum_{i<j} ell_ij(L)^2

   has type at most 2, and f = g(4g-1) has type at most 4. The same bounds are uniform when the number of components varies. The source’s Theorem 2.1 supplies the next step; it does not itself specify these two invariants or their product ideal.

2. **Actual-link zero set.** Each ell_ij(L) is an integer, so g(L) is a nonnegative integer on every actual link. Consequently f(L)=0 if and only if g(L)=0. Since the constant invariant 1 belongs to V, the zero set of I=fV equals the zero set of f. It is nonempty: the m-component unlink is an example, and knots also belong to the global zero set. Thus g belongs to J_actual(Z_actual(I)). This uses actual integer linking numbers, not arbitrary complex characters.

3. **Restriction of the entire algebra.** Let L_n be the standard oriented closure of the two-strand braid sigma^(2n), with m-2 split unknots if m is fixed. Then g(L_n)=n^2. For every v in V of order d there is a unique p_v(t) in C[t], degree at most d, with p_v(n)=v(L_n) for all integers n. Theorem 2.1 supplies precisely this finite-type polynomiality mechanism. One can match its odd half-twist parameter x to x=2n-1 by keeping one additional positive crossing fixed.

   For completeness, an independent crossing-difference proof avoids any ambiguity from the source’s non-split convention. Put a_n=v(L_n). The (d+1)-st forward difference is the value of v on the closed singular braid expression

   sigma^(2n+d+1) (sigma - sigma^(-1))^(d+1),

   with the same extra split components. Expanding the expression gives the alternating binomial sum of sigma^(2n+2j), j=0,...,d+1, exactly Delta^(d+1) a_n. Every term resolves the same (d+1)-singular link, so finite type makes the sum zero. In characteristic zero this sequence is the polynomial

   p_v(t) = sum_{j=0}^d (Delta^j a_0) binom(t,j).

   The recurrence extends the interpolation to negative integers as well. This establishes polynomiality for all links in the indicated family and **all** v in the full uncompleted algebra, including invariants of arbitrarily large finite order.

4. **Algebra map and formal point.** Uniqueness on infinitely many integers implies p_(v+w)=p_v+p_w, p_(vw)=p_v p_w, and p_1=1. Thus rho: V -> C[t], v -> p_v, is a unital complex algebra map. Evaluation at t=1/2 gives a unital complex character chi on the whole V, with

   chi(g)=1/4,      chi(f)=0.

   This is a new application step in this derivation, absent from the paper’s statements. The character is nonactual since no actual link has g=1/4. In particular, it is **not** evaluation on the closure of sigma: that closure has one component, and g=0. Passing from the even-exponent two-component family to a formal half-integer parameter does not identify the formal point with the odd-exponent knot. The paper’s formal linear combinations of links used in the finite-type definition also do not turn this character into an actual link.

5. **No power membership in the principal ideal.** If g^N=fq for some N>=1 and q in V, apply chi. The result is (1/4)^N=0, a contradiction. Therefore g^N is not in fV for every N>=1. Hence g is not in sqrt(I), although g vanishes on the nonempty actual-link zero set of I.

These five steps are independently checkable. Steps 1, 2, 4, and 5 are elementary additions around the already published Step 3 mechanism. The paper does not package them into a negative actual-link Nullstellensatz result. The argument nevertheless makes the target a direct, short corollary of an old mechanism, so a claim that full-algebra polynomial restriction is a new achievement would be incorrect on this evidence.

## Boundary and scope findings

- **Fixed component count versus global algebra:** The source normally fixes the underlying link object. For the global algebra, restricting any globally finite-order invariant to two components preserves its finite order; the same proof applies. For each fixed m>=2, add split unknots and use the direct difference proof. The construction does not give a nonzero witness on the knot-only algebra.
- **Non-split convention:** Section 2.3, printed 688 / PDF 8, defaults to non-split links and reduced diagrams unless otherwise stated. Later Section 5 explicitly uses split unions, for example printed 716 / PDF 36. This is a citation-scope detail worth making explicit, especially for appended split unknots. The direct difference proof above supplies all needed split cases without assuming a generality hidden in that convention.
- **No algebra-generation assumption:** The proof never claims that every invariant is a polynomial in linking numbers. It uses the polynomial restriction of each invariant individually. No unsupported structural classification of V is required.
- **No common degree bound:** V is the union over all finite degrees. The algebra map works because each element has a finite restriction polynomial; degrees may increase without bound between elements.
- **Coefficients:** Characteristic zero, here C, is used in interpolation. The source explicitly treats C-valued finite-type invariants. Section 4.3’s mod-p statements are a separate setting.
- **Completion:** Neither the exact proof nor the relevant source theorem is a claim about an arbitrary completed algebra. In a completion in which the geometric series -sum_{k>=0}(4g)^k converges, 4g-1 can become invertible and this particular nonmembership obstruction can disappear. Such a completion must be specified, not silently substituted for the ordinary algebra.
- **Other spectra:** chi is a genuine unital C-character and its kernel is maximal. It lies over I but does not vanish on g. Therefore the failure concerns the restriction to actual-link points; it does not contradict the usual principle of considering all appropriate algebraic points.

## Priority disposition and exact remaining gap

Classification: **published full finite-type polynomiality mechanism; no located explicit/equivalent ideal-zero-locus counterexample in this source; exact target follows by the short added derivation above.** Treat this as a close antecedent that must be cited and may leave only expository novelty. It is not a green light for a new discovery claim.

The bounded-source review is complete. The historical gap remains: independent primary-body review of the earlier cited sources and of literature on spectra or Nullstellensatz-type questions for finite-type invariant algebras is necessary to determine whether these elementary application steps or the counterexample itself were previously published. There is no basis in this review for declaring a positive novelty margin or increasing overall PR177 completion beyond 40%.
