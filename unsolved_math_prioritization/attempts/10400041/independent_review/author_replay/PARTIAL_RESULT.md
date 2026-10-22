# Self-delta link homotopy: split-block criterion and higher-interaction gap

Status: original arbitrary-link classification unresolved, 2/5. Independent review pending. Results here are a restricted consequence of prior classifications and an elementary obstruction to incomplete invariant lists. No novelty claim.

## 1. Exact original category and later source boundaries

Ohtsuki's 2002 problem collection, printed p.415 (PDF p.43), Problem 2.19 is due to Yoshiyuki Ohyama. It asks for necessary and sufficient conditions for two links with more than two components to be delta link homotopic. Immediately above, this is defined using delta moves whose three participating arcs all lie on the same component. Thus the relation is self-delta equivalence, also called self-C2 equivalence, not unrestricted delta equivalence or ordinary link homotopy. Source: https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf .

We use tame ordered, oriented closed links in oriented S^3, equivalently R^3 after choosing a point at infinity. Ordering and orientation are preserved. This convention is explicit in the cited two-component classification and the recent pretzel paper. String-link endpoints, arbitrary component permutations, and smooth/topological four-dimensional concordance are not substituted for this relation.

For a mu-component link L=K_1 union ... union K_mu, write a_j(L) for its Conway coefficient of z^j and define

delta_1(L)=a_(mu-1)(L),
delta_2(L)=a_(mu+1)(L)-a_(mu-1)(L) sum_i a_2(K_i).

Nakanishi–Ohyama, *Delta link homotopy for two component links, III*, J. Math. Soc. Japan55 (2003),641–654, Theorem3, proves that this pair is complete for two-component links. Source: https://www.jstage.jst.go.jp/article/jmath1948/55/3/55_3_641/_pdf . The full higher-component classification does not follow.

Yasuhara, *Self delta-equivalence for links whose Milnor's isotopy invariants vanish*, https://arxiv.org/pdf/math/0610492v3 , Theorem1.3, classifies n-component closed links under the hypothesis that all Milnor invariants of length at most 2n-1 with each index occurring at most twice vanish. Within that class the length-2n invariants give a criterion. Corollary1.5 recognizes the unlink by vanishing of all Milnor invariants with each index occurring at most twice. These statements do not classify arbitrary pairs with nonzero lower invariants. Remark1.6 explicitly warns that the unlink statement does not hold unchanged for string links; Remark1.8 warns against extending its two-parallel link-homotopy test to arbitrary pairs. The clasper proofs are credited and not reconstructed here.

Nakanishi–Shibuya–Tsukamoto's April4,2026 preprint *The Conway polynomials and Self Delta-equivalence of pretzel links*, https://arxiv.org/pdf/2604.03698v1 , Theorem1.8, claims a classification within enhanced pretzel diagrams with at least three components. It does not claim arbitrary-link classification. We verified that scope and definitions, not every diagrammatic step of its proof; no implementation of its cyclic-sequence criterion is used here.

## 2. Restriction to sublinks is a rigorous necessary test

**Lemma.** If two ordered oriented links are self-delta equivalent, then any corresponding sublinks are self-delta equivalent.

**Proof.** Follow a finite sequence of ambient isotopies and self-delta moves. Under deletion of components, a move on a deleted component disappears. A move on a retained component remains a self-delta move, since its three arcs belonged to that component and its supporting ball was disjoint from all other link arcs. Restricting ambient isotopies gives isotopies of the retained sublinks. QED.

Thus the two numerical invariants of every corresponding two-component sublink must agree. Milnor invariants with no repeated indices are also preserved, because self-delta equivalence implies link homotopy; the latter implication and invariance are recalled in Yasuhara's introduction. Neither necessity statement is promoted to a complete criterion.

## 3. Exact classification for a fixed split partition into blocks of size at most two

**Proposition.** Fix a partition of the ordered component labels into blocks, each containing one or two labels. Suppose both links are split unions along this partition: their block sublinks can be placed in pairwise disjoint three-balls. Then they are self-delta equivalent if and only if the Nakanishi–Ohyama pair agrees on every two-label block. One-label blocks impose no condition.

**Necessity** follows from Section2 and the two-component theorem.

**Sufficiency.** By the cited theorem, each pair of two-label block sublinks is related by self-delta moves and isotopies. Any two knots are related by delta moves, by the Matveev/Murakami–Nakanishi classification quoted in both primary papers; for a knot every delta move is self, so the one-label blocks are also equivalent. Choose finite realizing sequences. After ambient isotopies placing each split block in a designated ball, each sequence can be performed inside that ball: a finite sequence and its isotopy tracks have compact support in R^3, which can be compressed into the interior of the designated ball, with its initial and final embeddings adjusted by isotopies there. Performing the sequences in disjoint balls gives the full-link equivalence. No crossing between distinct blocks is introduced. QED.

This is a consequence of established one-/two-component classifications, not a new general classification. Its split-partition hypothesis is essential. The next example shows why agreeing on every two-component sublink is insufficient without it.

## 4. Global Conway data plus all pairs still miss higher interactions

Let B be the Borromean rings and, for each mu>=4, define L_mu=B split-union U_(mu-3), where U_k is a split k-component unlink. Compare L_mu with the mu-component unlink U_mu, with corresponding component labels.

Both full Conway polynomials vanish, because each link is split with an extra unknot. One quick skein proof of the identity Conway(L split-union unknot)=0 uses a Reidemeister-I curl: its positive and negative crossing diagrams both represent L, while the oriented smoothing is L split-union unknot. The skein relation gives z Conway(L split-union unknot)=0. Consequently both global delta_1 and delta_2 are zero.

Every two-component sublink of L_mu is a two-component unlink: this is the Brunnian property of B, and the other components are split unknots. Thus all two-component sublink delta pairs agree with those of U_mu, as do their pairwise linking numbers and component knot types.

Nevertheless L_mu is not self-delta equivalent to U_mu. By Section2 such an equivalence would restrict to one between B and the three-component unlink. But the Borromean triple Milnor invariant is plus or minus one, whereas the unlink value is zero; pairwise linking numbers vanish, so its usual lower-order indeterminacy is zero. This nonrepeating-index invariant is preserved by link homotopy, hence by self-delta equivalence. The obstruction also survives forgetting order or reversing orientations, since nonzero versus zero is unaffected.

For source-grounded verification of the standard Borromean fact, Cha–Powell, *Nonconcordant links with homology cobordant zero-framed surgery manifolds*, Pacific J. Math.272 (2014),1–33, Section2, Lemma2.1 proof, recalls that a Borromean component is a commutator of meridians of the other two. Source: https://msp.org/pjm/2014/272-1/pjm-v272-n1-p01-p.pdf . In the truncated Magnus expansion, with x mapped to 1+X and y to 1+Y,

E(x y x^(-1) y^(-1)) = 1 + X Y - Y X + terms of degree at least three.

This certifies the absolute value one of the first nonzero triple coefficient under compatible meridian/longitude choices; orientation conventions can change the sign and are immaterial here. The link-homotopy invariance itself is the standard Milnor theorem cited in Yasuhara, not proved by this formal computation.

This example rules out a particular inadequate data set: the two invariants of the full link together with all two-component sublink pairs. It does not rule out the stronger collection of invariants of all sublinks, since its Borromean three-component sublink is additional information. It is not a counterexample to the original request, which asks for an unknown complete criterion.

## 5. Frozen remaining gap and checks

No necessary-and-sufficient criterion is supplied for arbitrary ordered oriented links with more than two components. The split-block hypothesis, lower-Milnor-vanishing hypothesis, and pretzel-family restriction cannot be deleted. Closed-link Milnor invariants with indeterminacy are not silently treated as a complete vector of integers. Concordance and two-parallel tests are not substituted for self-delta equivalence.

The executable controls check noncommutative Magnus identities, finite label/sublink bookkeeping, and exact algebraic invariance of the formal delta_2 expression under multiplying the link and one component Conway polynomial by the same normalized knot factor. They do not construct an arbitrary link from formal polynomials or certify any imported clasper theorem. The geometric Borromean and split-block arguments are given above, with prior results explicitly identified. Separate adversarial review is required.
