# Independent primary-source baseline

Reviewer family: mapping-class geometry and positive factorization. Candidate narratives, code, outputs, statuses, history, prior reviews, and sibling mathematical findings have not been read at this checkpoint. Only supplied URL/hash routing and target title were used.

## Exact source target and quantifiers

B. Wajnryb, “Relations in the mapping class group,” in B. Farb (ed.), Problems on Mapping Class Groups and Related Topics, printed pp. 125–127, PDF pages 131–133 (zero based). Printed p.126 was also visually inspected.

Let B_6=A_5 have generators a_1,...,a_5 with adjacent braid relations and distant commutation. Define c=a_1a_2a_3a_4 and h=a_5a_4a_3a_2a_1^2a_2a_3a_4a_5, and Q=B_6/<<c^5h^{-1}>>. The explicit algebraic question is whether EVERY finite positive word w on these five fixed generators whose image in Q equals c^10 must have length 40, 30, or 20 AND whether its tuple of generator factors is Hurwitz equivalent in Q to respectively c^10, (a_1a_2a_3a_4a_5)^6, or h^2. No word-length cutoff and no finite image restriction occur. The question is stronger than merely checking the three proposed representatives share a quotient image.

The adjacent geometric question is about oriented genus-g surfaces with ONE boundary component, every pair of factor curves intersecting in 0 or 1 point, and product equal to the single positive boundary twist. The A_5 question is motivated by g=2; the source's sentence excluding the additional D_6 curve is explicitly tentative. A rigorous correspondence between the specified abstract Q and a mapping-class group cannot be assumed from this motivation.

Auroux, same book, printed pp.130–137: mapping-class factorizations correspond to fibrations with the specified boundary/section data; Hurwitz moves and global conjugation are distinct equivalences. Closed genus-two classification requires irreducible singular fibers and transitive monodromy, and c^10 fails that transitivity condition. Capping boundary weakens equivalence (Wajnryb, printed p.127). Auroux's bound question permits only homologically nontrivial curves or curves separating two components each containing a boundary.

Baykur–Monden–Van Horn-Morris, arXiv:1412.0352v2 (18 Aug 2015) and Algebraic & Geometric Topology 17 (2017), 1527–1555, DOI 10.2140/agt.2017.17.1527: Gamma_g^n fixes boundary pointwise and its isotopies do likewise. L(Phi) is supremum over ALL nonseparating positive Dehn-twist factorizations. Theorem A gives L(single genus-two boundary twist)=40, and genus-one boundary twists have fixed nonseparating length 12, but neither result alone gives the three Hurwitz classes in Q. Proposition 1 assumes n>=1 in the paper's discussion; capping all boundaries erases the integral abelianization that supplies the length bound. Proposition 19/Question 20 distinguishes subgroup-constrained and ambient factorization lengths; the printed wording has a restriction-versus-internal-factorization ambiguity, so it is not used as a classification theorem for Q.

## Success criteria for this audit

1. Check every presented mathematical theorem against its actual quantifiers in the frozen candidate.
2. Verify any geometric use of c^10, h^2, and the five-chain central word with correct surface genus, boundary components, capping map, and Hurwitz equivalence group.
3. Independently derive controls, then inspect candidate computations. A finite quotient may certify that any genuine Q equality passes a necessary image test. Positive acceptance in finite targets cannot certify equality or Hurwitz equivalence in Q without a sufficiency theorem.
4. Require an exact lift/faithfulness or normal-closure argument before transferring a mapping-class classification to Q.
5. Any asserted solution must cover all word lengths. A finite length ceiling needs proof for Q, not solely empirical search or geometric motivation.

## Predetermined falsifiers and boundary controls

- Abelianization of Q: braid relations force a_i to one class and c^5=h gives 20x=10x, hence Q_ab=Z/10. This necessary constraint allows 50,60,...; it does not prove the requested ceiling.
- Finite-image collision: if one target identifies inequivalent positive words (for example using the finite order of a generator), accepted image equality is not enough. Test actual kernel, not only relations.
- Torus boundary control: A=[[1,1],[0,1]], B=[[1,0],[-1,1]] satisfy ABA=BAB and (AB)^6=I in SL_2(Z), while (t_a t_b)^6=t_boundary in the one-boundary torus. A closed homology representation loses boundary twist.
- Chain controls: two curves (genus one, one boundary) exponent 6; three curves (genus one, two boundaries) exponent 4; four curves (genus two, one boundary) exponent 10; five curves (genus two, two boundaries) exponent 6. Cap one component only when invoking a one-boundary target.
- Symmetric monodromy control: the four-generator chain fixes a sixth marked point and so is not transitive in S_6; the five-generator chain is transitive. The closed transitive theorem must not be applied to the first.
- Distinguish standard-generator positive words, conjugate twists, arbitrary nonseparating curves, and pairwise-0-or-1 curves.

## Provenance and access protocol

All three primary-source downloads match the supplied exact byte lengths and SHA-256. Full receipts are in source_fetch_receipts.json. PDFs, extracts, and render are in ignored private/sources. They were fetched directly from the source URLs. The original equation was independently transcribed after visual inspection of printed p.126. No external individuals were contacted. No Git/service/candidate mutation has occurred.
