# Reviewed partial results: universal four-point interpolation families

**30005016 / OWR-9790358-014. Original outcome: unsolved, 5/5 substantive author turns.** Independent review passes the scoped results below, with no required mathematical correction. The unrestricted minimum remains undetermined; restricted construction obstructions do not settle it.

For a characteristic-zero field K, let m_4(K) be the minimum number of fixed four-dimensional subspaces of K[x,y] such that every set of four distinct points in K² is interpolated by at least one member. The spaces may have arbitrary polynomial degree. A separate worst-case question asks for the best bound across fields, with families allowed to depend on K.

## Accepted scope

- For K=Q(t), m_4(K)=1, by a credited specialization of Cornelissen's 1999 polynomial injection and an elementary Vandermonde argument
- For every algebraically closed characteristic-zero K, 4≤m_4(K)≤5; the lower bound uses the classical local-cohomology formula for a linear subspace arrangement
- The corresponding worst-case characteristic-zero bound lies between four and five
- Over R, the unrestricted bounds proved in this packet are only 2≤m_4(R)≤5
- For number fields, the value one is stated only conditionally on the relevant Bombieri–Lang hypothesis, via Poonen's theorem
- Two explicitly described mixed four-space construction classes fail; this does not rule out arbitrary four-space families
- Restricting every space to span{1,ℓ,ℓ²,ℓ³} gives exact minimum six; unrestricted spaces already admit a five-member cover, so six is not an answer to the original problem

The uniform upper bound five is credited to the earlier staircase construction. The function-field injection is credited to Cornelissen, and the number-field implication to Poonen. No historical-priority or independent-discovery claim is made.

## Source and the field caveat

The exact interpolation problem is in [OWR 7/2022, printed p. 423](https://ems.press/content/serial-article-files/46948). It permits arbitrary characteristic-zero fields and imposes no degree bound. The source's blanket three-point preamble needs a field qualification because the same Q(t) injection yields a single three-dimensional interpolation space. That corrects the preamble; it does not resolve the meaningful parameterized four-point question. The separately headed spline question is not part of this target.

The proof uses [Cornelissen, Proposition 8](https://webspace.science.uu.nl/~corne102/docs/abc.pdf), [Poonen, Theorem 1.1 and Remark 1.2](https://math.mit.edu/~poonen/papers/QQ.pdf), and [Álvarez Montaner–García López–Zarzuela, Theorem 1.2 and Corollary 1.3](https://web.mat.upc.edu/josep.alvarez/pdf/aim03.pdf). Source access and literature limits are explicit in the frozen gate and independent review. Later inaccessible full texts have not been treated as evidence of either a resolution or a novelty claim.

## Reading order and exact remaining gap

1. [Source gate](SOURCE_GATE.md)
2. [Turn 1](TURN_1.md): field dependence, credited injection, real sign obstruction, five-space cover
3. [Turn 2](TURN_2.md): unrestricted algebraically closed lower bound four
4. [Turn 3](TURN_3.md): obstruction to two directional cubics plus two quadratic extensions
5. [Turn 4](TURN_4.md): exact directional minimum six and complete 720-row certificate
6. [Turn 5](TURN_5.md): a further mixed-family obstruction allowing arbitrary high-degree fourth generators
7. [Independent full review](independent_review/INDEPENDENT_REVIEW.md)

For algebraically closed fields the unresolved alternative is an unrestricted four-space construction versus an obstruction excluding every such family. Real and arithmetic field-specific values require their own arguments. A Čech/local-cohomology lower bound over algebraically closed fields cannot be transferred to real or rational point sets by an unjustified Nullstellensatz step.

## Reproducibility and preservation

All five author checker outputs replay exactly, totaling 20,944 exact assertions, and all 720 CSV rows reproduce byte-for-byte. The independent checker passes 5,796 exact algebra and combinatorial controls. It reconstructs the collision interval from component intersections, checks the full six-equation incidence matrix for every slope assignment, includes vertical directions in the five-direction construction, and derives the quartic discriminant from a symbolic Sylvester matrix. These finite checks supplement the written mathematical review.

Run the author scripts check_turn1.py through check_turn5.py with Python 3; turn 5 requires SymPy. Run the independent script from the attempt directory:

    python independent_review/INDEPENDENT_CHECKS.py --packet .

The 29 public author files at commit 3e86c9c69a92b2df5bfd3ff276399e5272e6ca92 are retained with all nine independent-review files. Publication restores the original frozen CRLF bytes of TURN_4_CERTIFICATE.csv; the earlier WIP normalized that one CSV to LF. All other author files are byte-identical to the WIP. See the mandatory [byte-audit addendum](independent_review/BYTE_AUDIT_ADDENDUM.md), which corrects the initial review’s text-readback claim. Historical pending-review text remains unchanged; this file and REVIEWED_STATE.json give the current disposition. PUBLICATION_MANIFEST.json binds the full compact public packet. Source PDFs, rendered pages and raw imports are not redistributed.

This is AI-assisted research and review, not human peer review or formal verification. The original target is unresolved after its five-turn budget; no further author search is part of this packet.
