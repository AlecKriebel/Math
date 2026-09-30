# Independent review of the cofiber criterion and free-group example

**Verdict: PASS for the stated isomorphism-groupoid criterion and natural left-only example.** The broad imported characterization remains **unsolved, 3/5**, because arbitrary weak-equivalence realizations are outside the proved criterion and the original source leaves the intended variant underspecified. No mandatory mathematical correction was found. Priority is unestablished; this is an independent AI review, not human peer review.

This report covers frozen `PARTIAL_RESULT.md` SHA-256 `e555fda75202524b18fb1ecf3939f83703854abaeccf4ea0aab7d47ee5f6fa24`. The artifact was not changed. Review completed on 2026-09-30 using gpt-6-astra at xhigh reasoning.

## 1. Exact source and construction variant

The full imported statement and Bergner’s complete contribution, printed pp. 1945–1946 of OWR 34/2023, were read. The rendered p. 1946 was inspected. The report describes the polygon-triangulation condition, the left fan condition for cofibration categories, sufficient structures in common examples, and the then-artificial nature of known separating examples. It does not supply a precise universal theorem identifying every possible weak-equivalence construction. The package correctly treats the imported characterization as broader than its own theorem. [Official OWR source](https://ems.press/content/serial-article-files/47483?nt=1)

Carawan’s complete primary preprint was checked at Definitions 3.1, 3.8 and 4.5, Section 5, Propositions 7.1 and 7.7, Lemma 7.2, Section 8 and Proposition 9.1. The current primary record lists v1, 19 May 2024. The ordinary cofibration and Waldhausen axioms used by the package agree with those definitions; a mapping cylinder is not part of the basic assumptions. Proposition 7.1 supplies the left theorem for the maximal-groupoid realization, whereas Proposition 7.7 imposes extra assumptions for its reduction involving general weak equivalences. [Primary preprint](https://arxiv.org/abs/2405.11561)

In particular, taking the nerve of a maximal groupoid is materially different from realizing the category with all its morphisms. A zero object makes the latter classifying space contractible in each degree. An equivalence or failure in a categorical model cannot automatically be moved to an arbitrary realized weak-equivalence category. The candidate retains these distinctions throughout.

## 2. Quotient functor and the marked fiber criterion

Fix a cofibration \(i:A\to X\). An intermediate factorization has two cofibrations \(A\xrightarrow u C\xrightarrow vX\), with \(vu=i\). The quotient square
\[
\begin{matrix}
 C&\longrightarrow&X\\
 \downarrow&&\downarrow\\
 C/A&\longrightarrow&X/A
\end{matrix}
\]
is a pushout: both ways of computing its lower-right object impose the same universal condition of killing the given map from \(A\). Hence its bottom arrow is a cofibration without any monomorphism assumption. This verifies that \(Q_i\) is defined on all of the claimed source category.

Quotient choices are harmless because the groupoid of pushout cones on a fixed diagram is contractible: a cone-compatible isomorphism between any two choices exists uniquely. Chosen quotients may be made functorial by their universal property, or retained as explicit contractible data. No quotient automorphisms are silently discarded.

For the diagonal 13 of 0123, the target consists of the two cofiber triangles with shared object \(A_{13}\), and includes an isomorphism identifying the two copies of that object. Transporting across this isomorphism gives exactly a pair
\[
 (i:A\to X,\;j:B\to X/A).
\]
Thus the use of a groupoid 2-pullback, instead of an unqualified strict pullback, is correct. Nerves of groupoids model 1-types, and their 2-pullbacks compute the corresponding homotopy pullbacks.

Both the first-row chain groupoid and this target project to the groupoid of marked outer cofibrations \(A\to X\). Each projection is an isofibration. For a base isomorphism \((a,x):i\to i'\), the chain transports to \((ua^{-1},xv)\); a quotient subobject transports by the induced quotient isomorphism. These formulas preserve cofibrations and all incidence equations.

Here is a direct audit of the fiberwise equivalence step. Suppose the fiber functors are equivalences. To lift a target arrow over a base isomorphism, first transport its source in the domain isofibration, then lift the remaining arrow in the single strict fiber by full faithfulness. The lift is unique. Target objects lift by fiber essential surjectivity. Conversely, if the total functor is an equivalence, total essential surjectivity followed by transport along the induced base isomorphism gives essential surjectivity in a prescribed fiber. Total full faithfulness restricts to arrows over the identity. Therefore the total comparison is an equivalence if and only if every \(Q_i\) is.

Markings matter: these are fibers over the fixed \(A\), fixed \(X\), and fixed inclusion \(i\). They are not sets of unmarked isomorphism classes. In the monomorphism case, a morphism over a fixed ambient object is unique if it exists, so the groupoids are equivalent to discrete sets. The stated bijection criterion then follows. Its validity in that specialization does not license taking unmarked classes in the general proof.

## 3. The all-degree polygon argument

The degree-three argument is not being used alone. The hypothesis also supplies **every-degree** comparison with the fan at vertex zero, which is available directly from first-row chain reconstruction and is separately credited to Carawan.

For a diagonal flip, erase the diagonal and retain a quadrilateral cell, with all remaining cells triangles. The membrane for this dissection has an \(X_3\) factor on that cell. Each degree-three comparison to a two-triangle membrane respects all four boundary edges and their vertices, because all maps are simplicial face restrictions. It is consequently an equivalence in the relevant slice over the boundary data. Gluing the remaining cells is a homotopy base change, so each of the two refinements is an equivalence of complete membrane spaces.

The map from \(X_n\) commutes with these comparisons. If it is an equivalence for one triangulation, two-out-of-three transfers that conclusion across the flip. This supplies the required coherence; merely exhibiting abstract equivalences between unrelated membrane spaces would not suffice.

The proposed fan-increasing flip exists whenever the triangulation is not already the fan. The union of triangles incident to zero then has an internal frontier edge \(ab\). Its adjacent triangles are \(0ab\) and \(abc\), with \(c\ne0\). Replacing \(ab\) by \(0c\) preserves every existing diagonal incident to zero and adds one. The bounded number of diagonals proves termination. Hence all triangulations are reached from the known fan condition, in every degree.

If the convention requires all polygonal subdivisions rather than only triangulations, refine each cell into triangles. The corresponding lower-degree comparisons replace each cell by its triangulation; homotopy gluing and two-out-of-three then give the same condition for the subdivision. There is no uncovered higher-degree condition in the claimed groupoid theorem.

## 4. Waldhausen free groups and the obstruction

Finitely generated free groups with all homomorphisms form an essentially small category with zero object the trivial group. The claimed cofibrations are free-factor inclusions with finite-rank free complements, transported by isomorphisms. They contain maps from zero and isomorphisms and are closed under composition.

The key pushout claim is valid for an **arbitrary** homomorphism \(A\to B\), not merely an inclusion: the pushout of \(A\to A*F_r\) is \(B*F_r\). Its universal property is the usual free-product universal property, and the resulting object stays finitely generated and free. The induced inclusion is again a cofibration. With isomorphisms as weak equivalences, the gluing axiom follows from functoriality of pushouts under an isomorphism of spans. The construction therefore meets the stated ordinary Waldhausen definition. No unproved cylinder or exact-category axiom is needed.

Let \(w=[c,a]=cac^{-1}a^{-1}\). The automorphism
\[
 \alpha(a)=a,\qquad\alpha(b)=bw,\qquad\alpha(c)=c
\]
has inverse fixing \(a,c\) and sending \(b\) to \(bw^{-1}\), because \(w\) itself is fixed by \(\alpha\). Thus both displayed embeddings of \(F(a,d)\) into \(F(a,b,c)\) are free-factor inclusions.

Killing \(a\) kills \(w\), so both factorizations induce precisely the same marked inclusion \(F(b)\to F(b,c)\). Killing the whole intermediate subgroup gives \(F(c)\) in either case: the normal closures of \(\{a,bw\}\) and \(\{a,b\}\) agree. These are nonabelian quotient identities, not conclusions drawn from matching abelianizations.

The word \(bw=bcac^{-1}a^{-1}\) is not in \(\langle a,b\rangle\), as its reduced word contains \(c\). I checked this independently through a finite quotient: send \(a\) to \((12)\), \(b\) to the identity and \(c\) to \((23)\) in \(S_3\). The image of \(\langle a,b\rangle\) has order two, while the image of \(bw\) is a nontrivial three-cycle. Membership would be preserved by every homomorphism, so this is a second exact nonmembership certificate.

Therefore no isomorphism over the fixed \(X\) identifies the two intermediate images. The identity arrow between their equal quotient subobjects has no lift under \(Q_i\), so that functor is not full. This establishes failure of the criterion.

The direct missing-loop argument is equally valid and avoids relying on the general criterion. On the right-triangulation data, use \(\alpha\) on \(X\) and identities on \(A,B,Y,Z\). The maps commute because \(\alpha\) fixes \(A\) and becomes the identity on \(X/A\). A lift to an automorphism of the original complete flag would require
\(v_0\theta=\alpha v_0\), forcing \(\theta(d)\) to map to \(bw\in\langle a,b\rangle\), contradicting the certificate above. The induced map on the automorphism group of the chosen base object is therefore not surjective. For groupoid nerves this is exactly a failure of surjectivity on the based fundamental group, and precludes a weak equivalence.

The candidate correctly notes that the two full flags become isomorphic if the ambient map is allowed to be \(\alpha\). That arrow has distinct source and target flags; it does not provide an automorphism of the original flag lifting the specified loop. It neither repairs full faithfulness over the fixed target nor refutes the based fundamental-group obstruction.

## 5. Exact checks and scope verdict

The 8,876 author assertions replayed byte for byte from an isolated snapshot. The verifier hash is `22d9f50f0e5846b17795fb0e32dfa046f1e21ec618d8b5a4d57f7adacab66f75`; the reproduced receipt hash is `566aedf01c7f7a217b592930d70d1f66b0cf145a08349868af17ea9dd73f7118`.

The independent standard-library checker passes **6,882** assertions. It uses:

- Finite \(S_3\) quotients, including 24 separating assignments, for a different nonmembership test
- Independent free-word substitution and quotient calculations
- 159 equivariant functors of finite \(C_2\)-action groupoids over \(BC_2\), testing the marked fiber/total-equivalence distinction
- Triangulations generated as noncrossing diagonal sets for polygons with three through eight vertices, checking all 882 directed flips, fan-increasing flips and connectedness
- 364 marked pointed-set interval cases as positive quotient controls

These finite checks support the explicit construction and challenge common mistakes. They do not replace the all-degree homotopy-limit proof, the universal pushout argument or the source-scope audit above.

Reproduction from this review directory:

```sh
(cd author_replay && python verify.py)
python independent_checks.py
```

The theorem is a genuine necessary-and-sufficient **small-diagram criterion for the specified isomorphism-groupoid construction**, rather than a mere assertion that the original comparison maps are equivalences. It checks quotient factorization groupoids in the underlying category. It is not an effective recognition algorithm or a classification of arbitrary \(|wS_\bullet\mathcal C|\).

The natural free-group example fully proves the left-only property for its stated choice \(w=\mathrm{iso}\). The larger imported characterization remains unresolved/source-qualified. Publication should retain **unsolved, 3/5**, the variant limitation and the absence of a priority claim. No mandatory correction remains.
