# Turn 5 — A precise simultaneous-surgery theorem and the remaining interpretation gap

AI-assisted mathematical proof candidate; independent review pending. Fifth and final author turn. Original OWR conjecture remains unresolved; no sixth author search.

## 1. Define the broad operation explicitly

Fix a finite quiver Q with at most two arrows in and out at every vertex. Give its arrows a fixed order. Complete Q to a single blossoming quiver by adding distinct incoming/outgoing blossom arrows at each vertex until the original vertex has two of each. This depends only on Q and the fixed ordering, not its relations. Give every completed arrow its oriented PPP lozenge, with four distinct corners s,v,t,f and sides 0=s-v, 1=v-t, 2=t-f, 3=f-s.

For a quadratic locally gentle ideal J, the original permitted/forbidden table at each vertex extends to a 2×2 relation permutation matrix. There is always an extension: the original relation table and its complement are partial matchings; completing rows and columns of size at most two extends them to complementary permutation matrices. If both extensions are possible, use the first in the fixed order. An entry in this matrix glues side 2 of the incoming arrow to side 3 of the outgoing arrow; an entry outside it glues side 1 to side 0, with endpoints identified as in PPP Definition 4.6.

Define a **simultaneous local seam replacement** as follows. Choose any set U of original vertices. At each chosen vertex, cut all four of its glued seams and change the completed relation permutation matrix to its other value, re-pairing the same eight exposed sides by the preceding rule. Carry this out simultaneously at every chosen vertex. The endpoints must be valid completed locally gentle tables; one may additionally require them to restrict to ideals J,J'⊆I for a fixed string algebra A=kQ/I. This definition imposes no requirement of a finite-dimensional intermediate state, no preservation of topology and no assertion about isotopy of labels. It is a deliberately broad, fully specified combinatorial move.

## 2. General constructive theorem

Any two quadratic locally gentle covers J,J' of the same fixed Q admit one simultaneous local seam replacement between their standard cell-complex models, using at most |Q0| vertices and four seams per changed vertex. This holds with loops and parallel arrows, without saturation, and in particular when both covers are finite-dimensional.

Proof. Use the common blossoming quiver and lozenges just defined. Compare their two chosen completion matrices at each original vertex. A 2×2 relation permutation matrix has only two possibilities. Where the matrices agree, the four seam identifications agree. Where they differ, all four identifications change to the opposite choice. Let U be precisely the set of differing vertices and make these replacements.

The seams assigned to distinct original vertices use disjoint sides: the seams at the target of an arrow use its t-adjacent sides 1,2, while those at its source use its s-adjacent sides 0,3. This remains true for loops, since these are four distinct sides of the lozenge. Thus no seam is cut twice and simultaneous replacement is unambiguous. After replacement every side pairing, including its endpoint identification, is exactly the pairing prescribed by J'. Unglued boundary sides are unchanged as a set. Taking the quotient by these identifications yields precisely the endpoint model for J'. This proves the theorem at the full cell-complex level, rather than just at the level of topology invariants.

The common blossoming quiver has |Q1|+Σ_v(2−indeg v)+Σ_v(2−outdeg v)=4|Q0|−|Q1| arrows. Each of |Q0| vertices contributes four seams. A certificate lists the changed vertices and old/new seam pairings, of size O(|Q0|+|Q1|), and can be produced and checked in linear time after incidence lists and relation lookup tables have been built. This is a certificate for the defined move, not an algorithm recognizing an unspecified source equivalence.

If J,J'⊆I, both quotient algebras remain A=(kQ/J)/(I/J)=(kQ/J')/(I/J'). Their labels can be reconstructed separately by the established labelled-surface construction of Baur–Coelho Simões. The theorem does **not** prove that a prescribed geometric label-transport rule realizes this reconstruction during seam replacement. Such a rule is another part of the source-equivalence gap.

## 3. Why the finite locus issue does not obstruct this theorem

The two finite covers in turn 2 differ at two vertices. Their simultaneous certificate changes eight seams and directly obtains the other finite cover; no infinite intermediate algebra is asserted to be an allowed stage. Sequentially changing those same vertices necessarily visits an infinite cover. Thus the distinction between a collection move and a sequence of finite one-vertex moves is mathematically substantive.

For the acyclic family of turn 4, even sequential switches stay finite and change genus by one in the displayed selected family. Hence finite-dimensionality by itself does not force the explicitly defined seam replacement to preserve topology.

## 4. What this does and does not establish about the original question

There are two rigorous conditional implications:
1. If the OWR's permitted rotations include all simultaneous local seam replacements, including the required label reconstructions, then any two finite covers are equivalent by the theorem above.
2. If the OWR's permitted rotations are required to preserve the underlying oriented homeomorphism type, then the turn-1 finite-cover example disproves uniqueness, with the connected unbounded family of turn 4 strengthening the obstruction.

Neither antecedent has been established from the retrieved source. These are two possible readings, not a dichotomy exhausting every intermediate equivalence. In particular an allowed move could change topology yet still be narrower than all seam replacements. OWR printed p.443 says only 'rotating certain collections of tiles'; the full contribution and expanded paper provide no recovered formal definition matching the operation here. Xin–Zhang (2026) uses a specified label/dissection-preserving homeomorphism relation, and cannot silently supply the missing source definition.

Accordingly the final disposition is original **unsolved 5/5**, with substantial scoped theorems and a precise formulation boundary. No statement that the original conjecture is solved, false, already resolved, or meaningless is warranted. The fixed-string-algebra parameter is clear; what is not pinned is the move equivalence. No author contact or priority claim was made.

## 5. Reproducibility and credit

`python turn5/verify_surgery.py` enumerates all degree-constrained simple directed quivers on at most three vertices, including loops, and all their gentle quadratic relation tables, including nonsaturated choices. Across 283 quivers and 8,401 ordered pairs of covers it checks common blossoming, side uniqueness, the exact four-seam change at every differing vertex, and reconstruction of the entire endpoint seam set. A separate parallel-arrow example checks the two-vertex simultaneous replacement. All 63,847 exact assertions pass; stdout is frozen in turn5/verification.json. The general proof covers quivers beyond this finite set.

The seam construction and inverse correspondence are credited to Palu–Pilaud–Plamondon, https://arxiv.org/abs/1807.04730v2, Definition 4.6 and Theorem 4.10. The local cover choices are credited to Xin–Zhang, https://arxiv.org/abs/2608.14360, Remark 2.2. The labelled algebra construction is credited to Baur–Coelho Simões, https://arxiv.org/abs/2403.07810, Theorem 3.1. Original source: https://ems.press/content/serial-article-files/47001, Baur pp.441–444, conjecture p.443. These standard ingredients, not invention of surface models, underlie the deductions here. No novelty certification.

Informal completion estimate: 55%; the allowed source move and label transport remain decisive gaps. Five genuine author turns are complete, and no sixth search is undertaken. Final status awaits independent review.
