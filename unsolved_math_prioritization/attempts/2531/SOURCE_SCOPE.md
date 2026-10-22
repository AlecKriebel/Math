# Exact source and prior gate: 2531 / KOU 21.22

## Question and convention

The exact question is whether the **standard restricted wreath product** G wr H of two finitely generated Hopfian groups is Hopfian. Write

    W=G^(H) semidirect H,

where G^(H) is the group of finitely supported functions H->G, with pointwise multiplication, and H acts by left translation: (h.f)(y)=f(h^{-1}y). Thus

    (f,h)(g,k)=(f (h.g),hk).

Hopfian means that every surjective self-homomorphism is injective. It does not mean co-Hopfian, and the action is the regular action on H, not an arbitrary transitive permutation action. Both finite and infinite acting groups are included.

The October 2026 current primary notebook, Problem21.22 on printed/PDF180, was downloaded and visually checked:
https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt.pdf .
It attributes the question to H. Bradford and F. Fournier-Facio, and records the connection of the abelian/nilpotent cases with Kaplansky's direct-finiteness conjecture. It has no solved or unverified-solution marker. The editors' current page and separate October updates were checked; the update file has no new 21.22 annotation:
https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21upd.pdf .
The older alglog copy has different pagination and does not control this current locator.

## Credited 2024 primary results

Bradford and Fournier-Facio, *Hopfian wreath products and the stable finiteness conjecture*, Mathematische Zeitschrift308 (2024), Paper58, 28pages, DOI10.1007/s00209-024-03589-3:
https://link.springer.com/article/10.1007/s00209-024-03589-3 .
The published PDF was retrieved at https://d-nb.info/1355447615/34 . The introduction, relevant definitions and Sections2 and5 arguments were read. Its Question1.14 is the exact negative-existence formulation of the present target, and Question1.15 isolates the nonabelian finite-rank free-base case as a further open special case.

The following are known inputs, not new discoveries in this packet:

- Theorem1.3/4.11: the universal assertion for finitely generated abelian bases is equivalent to Kaplansky direct finiteness; direct and stable finiteness as universal group-ring conjectures are equivalent.
- Theorem1.5 gives the precise finite-abelian primary-component matrix criterion. Corollary1.6 includes torsion-free abelian bases and appropriate sofic, bi-orderable or unique-product acting-group cases.
- Theorem5.5 and Corollary5.6 extend the universal reduction to finitely generated nilpotent bases, with all upper-central layers included.
- Definition2.1 calls a morphism basic when it sends the restricted base into itself. Lemma2.14, with its Hopfian quotient hypothesis retained, then makes the base restriction surjective and the quotient map an automorphism. Proposition2.6 supplies automatic basicity for abelian bases with finitely generated infinite acting group. This automatic-basicity conclusion is not silently extended to nonabelian bases.
- Proposition5.1 gives normal-subgroup commutator constraints. Proposition5.2 and Remark5.4 give positive just-non-solvable/just-non-property cases under their stated incompatibility assumptions. They do not settle all centerless bases.

The characteristic-zero group-ring result does not remove the positive-characteristic stable-finiteness obstruction in the abelian case. No claimed solution of Kaplansky's conjecture or unrestricted wreath Hopficity is adopted.

## The newer permutational example does not answer this target

D. H. Kochloukova, *Hopfian combinatorial wreath products*, arXiv:2602.19235v1, 22February2026:
https://arxiv.org/abs/2602.19235 . The full PDF, introduction, Proposition2.2 and Corollary2.3 were inspected. The negative example uses

    B=<h,t | t^{-1}ht=h^{m+1}>, H_0=<h>, X=B/H_0,
    (Z/mZ) wr_X B, m>=2.

The acting group is Hopfian, but the coordinate action has the nontrivial infinite stabilizer H_0. It is not the regular action on B required by KOU21.22. The induced-module endomorphism calculation uses the relation h.v=v in K[B/H_0]; that relation is absent in the regular group ring K[B]. Thus the displayed one-sided inverse is not a one-sided inverse for the same operators on the regular module. The paper's own introduction distinguishes the restricted case X=B from this coset action. No original counterexample follows by renaming X or ignoring the stabilizer.

Current exact-title, basic/centerless-epimorphism and wreath-Hopfian searches located this relevant newer paper, but no verified complete solution of the regular two-Hopfian-factor assertion. This is a bounded literature check, not a priority certificate or proof of absence of other work. No outside researcher was contacted.

## Prior-attempt gate

The requested https://www.unsolvedmath.com/problems/2531 returned an internal retrieval error. The authorized fallback record is ulamai/UnsolvedMath at revision37e53eabe540fb458758e198be61634bd02ee008. The complete cached problems/research files were checked against the repository's byte-length and SHA-256 manifest; the full target record was read and its prior research report under KOU-21.22 is null. The only catalogue record matching both Hopfian and wreath-product wording is this target.

Live exact-ID/alias and Hopfian-wreath PR searches, branch search and target-path history are empty. Exact alias/Hopfian default-branch code searches find no proof; the bare numeric search mostly finds unrelated certificate integers. All-ref ID/title/path checks across494 mirrored refs found no actual prior attempt. The catalogue is eligible, queued0/5, rank415, with no readiness hold; the related-target-groups and active state files have no matching entry. The recently completed group-ring cohomology target30000590 concerns a different module-finiteness property and does not resolve stable finiteness or this question.

Repository and queue instructions were read. Source work uses zero substantive turns; new proof work is counted separately. The target receives up to five genuine author turns, full independent review before publication, and no promotion of a restricted case into the original theorem. Raw sources and imported records remain local-only.
