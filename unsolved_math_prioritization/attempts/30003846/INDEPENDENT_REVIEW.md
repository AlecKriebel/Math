# Independent review of the fast bump decomposition bridge

Date: 8 October 2026. Record: 30003846.

## Verdict

**PASS.** The decomposition theorem in the reviewed supplement is correct for the explicitly defined restricted permutational wreath product, allowing a nonfaithful action of the top group on the indexing set. No mathematical correction is required. This closes the mathematical I0 obligation under that convention.

The reviewed `SCOPE_AUDIT.md` has 14,201 bytes and SHA-256 `ce67d2a0e17b4b445bcaad8e26267c4ac9200ae4fed4a3ab31d61a74673e75c9`. Its accompanying manifest entries and the five cited PDF byte counts and hashes were independently checked and matched. The reviewed files were not changed.

The exact original Questions 71–72 remain **accepted conditionally on the stated restricted permutational interpretation**. This review does not establish that the original report excludes only regular wreath products or only wreath products with faithful indexing action. It preserves the earlier acceptance of the connected classification and its explicit representation, core, and finiteness imports. It does not re-audit those imports, certify Question 109, establish journal acceptance, or support a novelty or worldwide-resolution claim.

## Minimal components and endpoints

For crossing components, unions of supports are open intervals because crossing paths give chains of intersecting intervals. Finiteness guarantees a component with inclusion-minimal union. The containment propagation argument is valid: if an outside support contains one member of a crossing component, a crossing neighbor cannot be disjoint from it, contain it, or cross it. Therefore that neighbor is also inside it.

The strictness needed for the minimality contradiction holds even when the selected component is a singleton. Two nested fast supports cannot share a left endpoint, since their left feet would overlap; they cannot share a right endpoint, since their right feet would overlap. A finite union of supports lying inside a fixed support therefore has both extreme endpoints strictly inside that support. In the contradictory inward-containment case this makes the other component's union a proper subset of the selected union. The supplement establishes the no-shared-endpoint fact immediately after using strictness; moving that observation before the minimality paragraph would improve exposition but is not a mathematical repair.

Every outside bump consequently either contains the selected interval J or has support disjoint from J. When it contains J, each inner bump's two feet lie in its fundamental gap. The convex hull of those feet is the inner open support, so that whole support is in the gap. Taking their union puts J in the gap. Gap-boundary equality causes no failure: the gap is half open and J is open. Outside supports may touch J at boundary points without intersecting it, which is also harmless. Isolated singleton components are covered.

## Signs and the local reduction argument

Inverting a negative generator preserves its cyclic subgroup and its unlabelled feet under the cited inverse-feet convention. It therefore preserves fastness, supports, and crossing components. Neither the number of generators nor the relevant subgroups changes.

For a positive bump with marker m, the source is open at m and the destination contains the image of m. Thus every moved point outside the source enters the destination, including a point initially equal to m. For the inverse, interchanging the two feet gives the same statement. These endpoint conventions are exactly sufficient for the induction.

Deleting a letter that fixes the current point preserves all subsequent point evaluations. Cancelling an adjacent inverse pair also preserves the evaluation. Repeating these operations terminates and produces a word freely reduced and locally reduced at that particular initial point. A single reduction valid throughout J is not needed and is not assumed.

A nonempty reduced word beginning outside all feet ends in the destination of its last letter. At each step the next letter moves the current point, and its source is disjoint from the preceding destination unless the letters are inverse, which free reduction excludes. Applied to the complement generating set, this proves that two points of J in the same H-orbit are equal.

## Consistency on the interval orbit

If Jh intersects J, there is x in J with xh in J, and the local argument gives xh = x. The fixed-point set of h within J is relatively closed. It is relatively open because at a fixed point continuity supplies a neighborhood U in J whose image is also in J; the same pointwise orbit argument then fixes every point of U. Connectedness gives pointwise fixation of all J.

For intersecting Jh and Jk, right multiplication by k inverse reduces to the preceding statement for h k inverse. Hence translated intervals are equal or disjoint. Conjugating the stabilizer statement shows that a setwise stabilizer of any translated interval fixes it pointwise. This avoids any assumption that the action on the family of intervals is faithful.

## Base group coordinates and the split extension

The right-action convention is consistent: the support of t inverse K t is Jt. If Jh = Jk, put q = h k inverse. Then q fixes J pointwise and commutes with every element of K. Since h = qk, conjugation by h and by k agrees on K. The coordinate identification at an orbit interval is therefore genuinely independent of the chosen representative.

Factors on different translated intervals commute and have trivial finite-product relations, as can be checked by restriction to each interval. Consequently their generated group N is the restricted direct sum of copies of K. Conjugation by h sends the coordinate at Jt to the coordinate at Jth without applying an automorphism to K.

More explicitly, for a finitely supported function f on the orbit set, write beta(f) for the corresponding product of supported conjugates. Then beta(f) conjugated by h equals beta(f to the h), where (f to the h)(omega) = f(omega h inverse). With the identification (f,h) maps to beta(f)h, multiplication is (f,h)(g,k) = (f times g to the h inverse, hk). This agrees with the right-action semidirect-product convention in the cited definition.

The intersection argument is complete. An element of N preserves each orbit interval and fixes their complement, including boundary points and any accumulation points outside the union. If that element also belongs to H, consistency fixes each orbit interval pointwise. It is therefore the identity on the entire ambient interval. The conclusion N intersect H = 1 does not discard a kernel of the indexing action. Together with G = NH, this proves the asserted abstract restricted wreath decomposition.

## Nontriviality and the convention examples

Both factors contain original nonidentity generators and are generated by proper subsets, hence are nontrivial smaller fast groups. When every complementary support misses J, the interval orbit has one member and the splitting is an internal direct product. Otherwise a complementary positive bump contains J in its fundamental gap. All integer translates of that gap are pairwise disjoint fundamental domains, giving infinitely many distinct orbit intervals. This proves the asserted nontrivial infinite indexing action.

The three-bump nonfaithfulness example is correct. If two disjoint inner bumps lie in one outer fundamental gap, the second inner bump fixes every outer translate of the first inner support. Retaining it in H is essential. The crossing-pair example also correctly demonstrates a nontrivial stabilizer of the initial interval, provided the added support is placed in a nonempty foot-free portion inside one support and outside the other, as specified. Such fast configurations exist. Neither example claims that every possible alternative decomposition must have the same indexing defect.

Finally, the unrestricted product is excluded by cardinality: a countably infinite orbit and a nontrivial base group give an uncountable full product, whereas a finitely generated group is countable.

## Exact source and status boundary

The original report's Question 71–72 passage was independently inspected as extracted text and on its rendered printed page 1610. It does not define an indexing action. The definition in Bleak–Brin–Moore Section 3.5, printed pages 15–16, was likewise inspected in text and visually. Its algebraic construction uses finite-support functions and retains the acting group; faithfulness is a separate hypothesis of its subsequent realization lemma. The supplement proves its own split extension and does not misapply that stronger lemma.

One source-precision refinement is recommended: attribute the *explicit finite-support and potentially nonfaithful convention* to Bleak–Brin–Moore Section 3.5 and the supplement's definition. Golan's introduction itself states a permutational-wreath decomposition but does not there separately spell out those two details. This refinement leaves the proof and the supplement's existing conditional verdict intact.

The recommended record status is: **connected classification accepted with explicit imports; decomposition bridge independently accepted under the stated restricted permutational convention; exact original interpretation conditional**. For any unconditional acceptance requiring the narrower regular-only or faithful-action-only exclusion, a matching decomposition or authoritative clarification remains necessary. Do not replace this status with an unqualified claim that the entire original record is solved.

## Primary sources

- [Original Oberwolfach report](https://ems.press/content/serial-article-files/46748?nt=1), printed page 1610, Section 6.
- [Gili Golan, Irreducible fast sets of bump homeomorphisms generate copies of Thompson's groups F_n](https://arxiv.org/abs/2607.10961v1), introduction and definitions. Prior-result attribution remains Golan.
- [Bleak, Brin, Kassabov, Moore and Zaremsky, Groups of fast homeomorphisms of the interval and the ping-pong argument](https://arxiv.org/abs/1701.08321v1), Section 3 and Lemmas 5.1–5.2.
- [Bleak, Brin and Moore, Complexity among the finitely generated subgroups of Thompson's group](https://arxiv.org/abs/1711.10998v2), Section 3.5.
- [Belk and Stott, Pseudo-F_4 is isomorphic to F_4](https://arxiv.org/abs/2303.16868v1), Section 2.1.

This report contains authored mathematical analysis and public verification metadata. It includes no source-document bodies, dataset contents, or private coordination material. No GitHub or queue write was performed.
