# Independent adversarial audit: algebra and finite-index transfer

**Disposition: PASS within the assigned family; no repair requested.** This is an independent mathematical audit of a completed candidate, not formal or human peer-review certification. It does not establish novelty. The original effort counter remains 1/5.

## Independence and exact scope

Candidate: PR #872, problem 30006628, frozen head `e3d77731b45b5f463df46e769faa01d65fe193ec`. Its candidate PROOF.md hash is pinned in DECISION.json. I read this candidate first, saved INDEPENDENT_RECONSTRUCTION.md, and did not open inherited audit verdicts, second-review reports, original checkers, or acceptance files while forming this assessment. The public test program was authored separately from the candidate's checker.

Assigned questions: free-product normal forms, torsion and inversion, legitimate triangular presentation and link convention, all three length residues, a finite-index image for arbitrary fixed finite inverse-closed generating alphabets in arbitrary nontrivial finitely generated factors, and the final property-(T) transfer. I also checked interactions with the spectral and probability argument on paper. This family has not independently re-proved the external matrix Chernoff theorem or performed a priority search; those are separate obligations for complete acceptance.

## 1. Normal forms and torsion

Write F=*G_i and regard B_i as actual nonidentity elements in the i-th factor, with disjoint factor tags. The free-product normal-form theorem makes every reduced B-word an actual distinct element of F. Equality is not affected by torsion inside a factor or by relations among several alphabet elements within a factor: neither can identify two distinct already reduced syllable strings. Distinct syllable lengths therefore cannot label the same block element. This argument requires no effective solution of the factor word problems.

Inversion reverses the syllable string and inverts each letter. An even-length fixed point is impossible because its central two syllables would be inverse elements of the same factor, contradicting reducedness. At length 2s+1, an inverse-fixed word is x c x^{-1}, with c a self-inverse alphabet letter. Its count is at most |W_s| times the fixed number of such letters. Thus deletion has order O(lambda^s), compared with an endpoint-class main term of order lambda^{2s}. Uniform exponentially small relative error follows from the fixed finite endpoint set and positive Perron coordinates. At s=0 use W_0={empty word}; this has no asymptotic consequence.

Only order-two block elements are removed. A block conjugate to a factor element of order three or any higher finite order may remain. That is legitimate: a formal generator can map to an element with additional relations in a quotient image. No embedding of the triangular group is made or needed.

## 2. The triangular group is an honest presentation

Choose one representative from each pair {w,w^{-1}} in the inverse-free block set. The other representative is its formal inverse. Different lengths give different pairs. This constructs a finite formal generating set independently of whatever relations its eventual image satisfies.

A cyclic adjacent formal cancellation would mean the underlying free-product blocks are inverse normal forms. The final syllable of the first and initial syllable of the second would then lie in the same factor. Sampled cyclically reduced syllable relators disallow precisely this. The argument applies at the last/first corner as well as the two ordinary cut positions, and mixed block lengths do not introduce an exception. Retaining only samples with three inverse-free blocks therefore yields cyclically reduced formal relators of length three and no link loops.

The candidate's edge {u^{-1},v} is the image, under the single vertex permutation x->x^{-1}, of the source convention {u,v^{-1}}. Apply that same permutation at all three corners; the entire multigraph and its degree-normalized spectrum are unchanged. Repeated relator occurrences can be represented by repeated attached triangular 2-cells. The fundamental group is unchanged, while corner edges carry their occurrence multiplicities. No independent-corner assumption is hidden here. The criterion is a presentation/link criterion: it does not require labels to survive as distinct group elements after quotienting.

Fresh primary-source checks: [Kotowski--Kotowski, arXiv v2](https://arxiv.org/pdf/1106.2242v2), printed pp.5--7, supplies quotient transfer in Remark 2.10, finite-index equivalence in Remark 2.11, the corner convention in Definition 2.12, and the connected-link gap >1/2 criterion in Theorem 2.13. Its graph convention counts multiple edges. I read these pages and visually inspected the complete page containing the definition and theorem. This supplies the established criterion rather than an independently re-proved theorem.

## 3. Common-suffix identity: every L>=4

Take any a,b in B, even when they belong to the same factor or ab=1. Since there are at least three factors, choose C different from both their factors.

* If L is even, choose a reduced suffix v of length L-1 beginning in C, for example alternating factors C,D,C,D,... . Both av and b^{-1}v are reduced length-L words, hence are not inverse fixed by the even-length argument.
* If L is odd, the asserted range gives L>=5. Choose distinct C,D,E and use the suffix factor pattern C,D,E,C followed by (D,C) repeated (L-5)/2 times. It has length L-1, is reduced, and begins and ends in C. Each of av and b^{-1}v has different first and last factors, so neither can equal its inverse.

Choose any available letter in each indicated factor; closure under products inside B is unnecessary. Exact cancellation in F gives

    (av)(b^{-1}v)^{-1} = av v^{-1} b = ab.

Thus H0=<V_L> contains every two-letter product, regardless of whether ab reduces. This is deterministic and independent of the sampled relators, retained sample count, and residue ell modulo three.

## 4. Normal subgroup, index, and quotient image

Set K=<ab : a,b in B>. For c in B,

    c(ab)c^{-1} = (ca)(bc^{-1}) in K.

Inverse-closedness puts c^{-1} in B, and applying the same inclusion with c^{-1} proves equality. Because B generates F, K is normal. In F/K every pair ab is trivial. Taking b=a gives [a]^2=1, and then arbitrary a,b gives [a]=[b]. Hence F/K is generated by one element of order at most two. This proves [F:K]<=2 without assuming there exists a parity homomorphism on each factor.

We already have K<=H0. Let q:F->G_ell be the random quotient map. Then q(H0) has index at most two; the surjection of coset sets F/H0->G_ell/q(H0) cannot increase the index. The group H_ell generated by all block lengths contains q(H0), so [G_ell:H_ell]<=2 as well. This works for (L,L,L), (L,L,L+1), and (L,L+1,L+1).

Every defining relation of Gamma_ell is a sampled relator under block evaluation. Therefore evaluation gives an epimorphism Gamma_ell->H_ell. Additional arbitrary relations in the factors or the full set of sampled relators can only enlarge its kernel. No replacement of factors by free groups, small-cancellation assumption, or finite presentation of the factors is used.

The property-(T) implication is the correct direction twice: it descends from Gamma_ell to its quotient H_ell and ascends across its finite-index inclusion in G_ell. The latter is the actual finite-index equivalence checked above, not arbitrary subgroup closure. For an additional primary confirmation, I read [Bekka--de la Harpe--Valette, author-hosted February 2007 book version](https://perso.univ-rennes1.fr/bachir.bekka/KazhdanTotal.pdf), Theorem 1.3.4 on printed p.43 and Theorem 1.7.1 with its proof on printed pp.65--67. Discrete groups and their finite-index subgroups satisfy its closedness and finite invariant quotient-measure assumptions. The theorem page was visually inspected.

## 5. Attempted obstructions and exact boundaries

**Parity.** In C2*C2*C2 with singleton factor alphabets, syllable parity is a genuine quotient onto C2. For even L every generator in V_L has even parity, so the bound of two cannot simply be improved to one. A possible residual C2 is compatible with property (T). Odd sampled relators can kill this quotient. For general factors parity need not be a homomorphism; the quotient-by-K proof handles that by possibly making K=F.

**Infinite abelianization of factors.** A surjection F->Z does not generally factor through G_ell: sampled relators impose additional equations. The argument only uses the finite-index image after quotienting. It does not assert factors retain their abelianization, embed, or individually acquire property (T).

**Two factors.** For C2*C2, every odd-length reduced word is inverse fixed, so V_L is empty at odd L. At L=4 its two reduced words generate <(ab)^2>, a subgroup of index four in the infinite dihedral group. Thus the deterministic finite-index lemma would be false with a universal <=2 bound if the three-factor hypothesis were dropped. This is an excluded boundary, not a counterexample to the candidate.

**Small L.** With three C2 factors, V_1 is empty. The deterministic assertion explicitly starts at L>=4, which is enough for ell->infinity. No claim for all small ell or exact threshold d=1/3 is warranted.

**Varying alphabets.** The factors, alphabets and d are fixed before ell varies. Constants in Perron counting, the spectral margin, and the Chernoff comparison need not be uniform over growing alphabets or over d decreasing with ell. The candidate states this limitation.

## 6. Interactions with the rest of the proof

On paper I re-derived the legal-boundary contribution to the mean link: specifying (x,y) fixes two adjacent blocks, their meeting legality is A[first(x),first(y)], and the remaining block count is T_h[last(x),last(y)] after symmetry. The deletion of order-two blocks belongs inside this completion count. Arbitrary factor relations and self-inverse individual syllables do not invalidate it.

The endpoint-compressed limiting walk has type, initial-letter, and terminal-letter components Q, P, and the rank-one stationary reset R. For unequal lengths the negative eigenvalue -1/2 of Q combines with negative P-eigenvalues, giving a positive nonprincipal bound rho/2, still strictly below 1/2. Omitting this sign combination would be an error; the candidate retains it. The inverse-free and finite-index adjustments do not change these type matrices.

I found no group-theoretic obstacle to the probability argument. A whole sampled triangle contributes one independent matrix summand; three correlated corner edges are not separately treated as independent. The deterministic weighted-mean-zero subspace is legitimate in generalized min--max even though it is not the actual-degree mean-zero subspace. These observations do not replace the separate full audit of the precise Chernoff source and constants.

## 7. Independently reproducible finite evidence

Run in this directory:

    python3 -I -S -B check_group_transfer.py
    python3 -I -S -B -O check_group_transfer.py

The independently authored standard-library program imports no candidate checker or previous review. It normalizes free products of cyclic factors (order zero denotes Z) using actual factor multiplication. It tests five models: three involutions; mixed finite torsion; infinite factors mixed with an involution; unequal radius-ball alphabets; and four factors. Both successful output files are byte identical, SHA256 `fcb355ac538a513fc810428fa4574ab8b431dda8bb894fefba707cb911996cd5`.

Per run: 43,720 reduced words; 25,520 even words checked not inverse fixed; 2,880 suffix identities for every L=4,...,23 and every letter pair; 836 conjugation identities; and 137,132 cyclic relators, of which 116,328 give retained triangles and 20,804 are discarded. It checks eight excluded-boundary/deletion controls and three parity controls. The inverse-fixed count upper bound is checked at each enumerated odd length. Triangles include all three length residues; global inverse relabeling is checked on actual corner endpoints.

A test-harness unpacking error selecting two auxiliary factors in the four-factor model was corrected before the successful recorded runs. This was an error in this independent test code, not in the candidate proof. Recorded checks use explicit runtime guards, so optimized Python does not erase them. They corroborate finite algebraic identities and boundary behavior. They are not an asymptotic theorem, spectral simulation, property-(T) decision procedure, or formal proof certificate.

## 8. Final disposition and remaining obligations

No unresolved gap or requested mathematical repair was found in this family. The strongest verified statement is the deterministic lemma: for every admissible fixed alphabet and L>=4, the proposed inverse-pair triangular presentation evaluates onto a subgroup of index at most two in the sampled free-product quotient; if that triangular group has property (T), so does the full quotient. The inverse-fixed deletion estimates and source criterion conventions are compatible with this lemma.

Complete PR acceptance still requires the other independently assigned spectral/probability/model and priority audits and the later preprint/package review loop. This report does not label the result novel, current-worldwide open, human reviewed, or formally verified. Private primary PDFs, extracts and rendered pages are excluded from the public manifest; only retrieval hashes and reading scopes are published.
