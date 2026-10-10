# Independent adversarial audit: 2650 / KOU-21.141

Audit date: 3 October 2026 (UTC).
Frozen author manifest audited: SHA-256 `93334356491d6719b98b628ebb4b011fcb6438428b46e454935d544702fd1ff7`.
Scope: all 15 manifest payload files, all five mathematical attempts, source hypotheses, and deterministic controls. No author files were changed, no remote writes were made, no nested worker was used, and no sixth proof-search attempt was undertaken.

## Verdict

**HOLD for one narrow source-hypothesis clarification.** The scoped mathematical conclusions survived this audit; no false counterexample, false positive special case, or invalid chain/limit calculation was found. The hold concerns the direct use of Chatzidakis–Zalesskii Theorem 5.1 in `turn_01.md:74–76` without addressing that source's global faithfulness convention. The same issue is correctly addressed for Theorem 6.8 in Attempt 2. A short repair using the package's already established lemmas suffices; no additional research is required.

After that repair and regeneration/rechecking of the manifest, the appropriate verdict is **PASS as exhausted, unresolved, scoped partial progress**, never PASS as a solution to the original problem. Two stale script paths are nonblocking documentation errors.

## Required repair R1: Theorem 5.1 and nonfaithful actions

In the corrected v2 paper, Section 2.2 explicitly makes actions faithful by default. Attempt 1 applies Theorem 5.1 directly to a subgroup action on the standard amalgam tree, which can have a nontrivial kernel. Its unqualified citation therefore omits a source hypothesis. This is a repairable justification gap, not evidence that the asserted finite-presentation consequence is false.

Replace the paragraph beginning “In particular a K having finitely many maximal vertex stabilizers” by an equivalent version of the following:

> For a faithful K-action with finitely many maximal vertex stabilizers up to K-conjugacy, Chatzidakis–Zalesskii Theorem 5.1 supplies the finite decomposition required above. For a nonfaithful action, first factor out its kernel N. If the action fixes a vertex, K is already finitely presented by coherence of that stabilizer. Otherwise the tree has an edge and N lies in a polycyclic edge stabilizer; hence N is polycyclic and finitely presented. The vertex stabilizers of K/N are the former vertex stabilizers modulo N and are coherent by Lemma Q of Attempt 2. Maximal vertex stabilizers and their conjugacy classes correspond under this quotient, while quotient edge stabilizers remain polycyclic and finitely generated. Apply Theorem 5.1 and the finite-decomposition criterion to K/N. Lemma E of Attempt 2 then lifts finite presentability to K. These elementary permanence facts are proved in Attempts 2–3. The unresolved step is still to establish the requisite stabilizer finiteness, or another suitable decomposition, for every finitely generated K.

This replacement deliberately only asserts the needed finite-presentation conclusion for the nonfaithful action. If the author wants instead to assert an actual lifted graph decomposition of K, that lifting should be stated and justified separately. It is unnecessary for the argument here.

There is no circular dependency: the finite-decomposition lemma does not depend on its later application paragraph; Lemmas E and Q are independent of that paragraph; the polycyclic finite-presentation induction uses Lemma E only.

## Nonblocking repairs R2–R3

- `turn_04.md:101`: change `checks/chain_obstruction.py` to `chain_obstruction.py` in the flat frozen publication package.
- `turn_05.md:81`: change `checks/power_commutator_frontier.py` to `power_commutator_frontier.py`.

The README's executable instructions already use the correct flat paths, and those instructions successfully reproduce the controls.

## 1. Target, category, and scope

The supplied primary Notebook page image was independently inspected. Printed page 198 has exactly Problem 21.141, asking about coherent pro-p factors with polycyclic amalgamation, and attributes it to P. A. Zalesskii. It is unmarked, unlike adjacent 21.142. The author correctly retains the pro-p meaning of coherence and makes the proper-amalgam convention explicit. This audit does not infer resolution or universal literature completeness from an unmarked entry.

All conclusions were checked in the category of pro-p groups: subgroups and normal closures are closed, generation is topological, presentations use finite sets of pro-p relators, and quotient images of compact subgroups are closed. No argument silently replaces finite pro-p presentability by abstract finite presentability. No requirement that the original coherent factors be finitely generated was introduced.

## 2. Finite proper graph criterion: PASS

For a finite proper graph of pro-p groups, the continuous Mayer–Vietoris segment

`H^1(K,F_p) -> direct_sum H^1(A_v,F_p) -> direct_sum H^1(A_e,F_p)`

gives

`sum_v d(A_v) <= d(K) + sum_e d(A_e)`.

This is a finite-dimensional kernel/image argument and remains valid when vertex finite generation is initially unknown. Finite `H^1` is precisely finite topological generation for a pro-p group. A closed subgroup of a coherent group is coherent, so the resulting finitely generated vertex groups are finitely presented.

The independent presentation check is direct: use the vertex presentations, one stable letter for each edge outside a maximal subtree, and one edge relation for each selected topological edge generator. Agreement on a topological generating set implies agreement on the entire compact edge group by continuity. The construction's generator and relator bounds are correct. No finite presentation of an edge group is needed.

The `H^2` bound also follows from the next exact segment, with the image contributed by `H^1` of the edges and the remaining image inside the finite direct sum of vertex `H^2` groups. No infinite graph or infinite-product cohomology claim is used. The bounds are correctly described as nonminimal.

The obstruction to the naive abstract-tree proof is real: pro-p geodesics need not be finite ordinary edge paths, and a profinite quotient need not possess a liftable maximal subtree. The author does not claim these missing properties.

## 3. Polycyclic edge subgroups: PASS

Intersecting a finite closed subnormal series with a closed subgroup gives a finite closed subnormal series. Every successive factor embeds continuously into the corresponding procyclic factor; compactness makes its image closed. Each factor is therefore procyclic. Induction yields finite topological generation, with a bound by the original series length, and finite pro-p presentability via the extension lemma.

This verifies precisely the closed-subgroup/Noetherian property needed in all five attempts. It does not assert finite generation of arbitrary intersections with an arbitrary finitely generated normal group. The notes explicitly avoid that stronger and false inference.

## 4. Extension, quotient, and finite-index permanence: PASS

**Extension lemma.** The proposed finite presentation includes the kernel relators, lift-conjugation relations, and lifted quotient relators. The natural map to the actual extension shows that the presented image of N embeds: its composite with the map to P is the original embedding of N. Conjugation agrees on a generating set and thus on N; because the prescribed maps are automorphisms, the image is normalized in both directions. The resulting quotient is Q, so the residual kernel lies in the embedded N and is trivial. Allowing pro-p words on the right-hand sides is essential and correct.

**Coherent quotient lemma.** The preimage of a finitely generated closed subgroup L of C/N is generated by finitely many lifts and generators of N. It is closed and finitely generated, hence finitely presented. Adjoining relations killing those generators kills exactly the closed normal subgroup N. The hypothesis that N is finitely generated is used and not omitted.

**Finite-index permanence.** Intersections with open subgroups are open; Schreier gives their finite generation. Passing to the core produces an open normal finitely presented subgroup using pro-p Reidemeister–Schreier. The remaining quotient is a finite p-group, which is finitely presented. The extension lemma finishes. This applies even when the ambient coherent group itself is not finitely generated.

## 5. Procyclic and virtually procyclic edges: PASS

The corrected v2 source's Theorem 6.8 supplies a finite proper graph with vertex and edge groups conjugate into original stabilizers, under procyclic edge hypotheses. Its source does not provide a replacement with merely bounded finite rank.

Attempt 2 correctly repairs the source's faithfulness convention: the action kernel lies in a procyclic edge stabilizer, is finitely generated and finitely presented, and can be factored out. Quotient vertex stabilizers are coherent by Lemma Q; the finite-presentation conclusion is then lifted by Lemma E. A fixed vertex or an edge-free tree is handled separately.

For an embedded H and an open procyclic C in H, the subspace topology supplies an identity neighborhood in G whose intersection with H is inside C; an open normal U can be chosen inside it. Normality is exactly what justifies `U intersect gHg^-1 = g(U intersect H)g^-1`. All edge stabilizers for `K intersect U` are then closed subgroups of procyclic groups. Schreier and finite-index permanence recover K. The finite-edge case `C=1` and free-product case `H=1` are both legitimate. The rank-two obstruction to this particular shrinking argument is correctly stated.

## 6. Common polycyclic normal kernel: PASS

For `N <= H` normal in both factors, the closed normalizer contains the topologically generating factors, so N is normal in G. The quotient universal property gives the displayed amalgam identity. Properness descends because each `Gi/N -> G/N` is injective. N is finitely generated, so quotient factors remain coherent by Lemma Q.

For a finitely generated closed K in an extension with polycyclic kernel, its image is compact and finitely generated, and its intersection with the kernel is polycyclic and finitely presented. The extension lemma gives finite presentation. This proves the lifting statement with exactly the needed intersection hypothesis.

The normal/central edge special case is valid in arbitrary finite rank. The malnormal analytic quotient application retains both analytic and malnormal hypotheses. The reduction using `core_G(H)` is correct, including core-freeness of the quotient edge. The free-factor example correctly shows that the quotient need not have rank one. It is explicitly not a counterexample to coherence.

## 7. Long chain construction and properness: PASS

Independently eliminating the relations gives `x_i=x^(p^i)` and `y_i=y^(p^(n-i))`, and exactly the displayed `n+1` commutation relators. The map to additive `Z_p^2` sends x and y to its two basis elements. Its restriction to V_i is diagonal multiplication by `p^i` and `p^(n-i)`, an injection. Thus no vertex element can die in the pro-p pushout, proving properness without an abstract residual-p assumption.

Both inclusions of E_i have index p. Hence all n chain edges remain noncollapsible under the usual reduction rule. The map onto `Z_p^2` and the two-generator presentation establish `d(P_n)=2`.

As an independent uniform check on the control matrix, modulo p each x-edge relation has the unique unit coordinate `x_(i+1)`, and each y-edge relation has the unique unit coordinate `y_i`. These are `2n` distinct coordinates. The edge matrix therefore has rank `2n` for every prime p and every n, not only for the enumerated parameters.

## 8. Central subgroup and faithful finite-edge quotient: PASS

The endpoint commutators imply that `x^(p^n)` and `y^(p^n)` both commute with x and y, hence with the entire topologically generated group. They define a continuous map from `Z_p^2` into the center, and its composite with the abelian coordinate map is multiplication by `p^n` on both coordinates. This composite is injective, proving `C_n = Z_p^2`, not merely that C_n has a rank-two image.

The formulas expressing these central generators in every vertex and edge group show that quotienting the whole graph by C_n is legitimate. The quotient vertex and edge orders are `p^n` and `p^(n-1)`, respectively; the displayed factor exponents and both index-p inclusions are correct, including n=1 and trivial factors. Diagonal maps into `(Z/p^n)^2` prove quotient properness independently.

The quotient presentation has abelianization `(C_(p^n))^2` and `d(Q_n)=2`. Endpoint vertex images are the two coordinate axes and are individually embedded. Thus any common element has zero abelian image and is trivial. The kernel of the standard tree action is inside that endpoint intersection, proving faithfulness. All edge subgroups have generator number at most two.

Consequently the family really excludes a bound on the number of reduced edges depending only on d and edge-subgroup generator rank, including within faithful actions. It does not exclude a bound depending on edge orders, a fixed group, a fixed action, or an acylindricity parameter. The text correctly makes each of those distinctions.

## 9. Coherence of the construction: PASS

There are only finitely many finite vertex groups in the quotient graph. Residual finiteness of the pro-p group permits an open normal subgroup avoiding all their nonidentity elements. Normality makes its intersection with all conjugates trivial, so it acts freely on the standard pro-p tree and is free pro-p. Schreier makes it finite rank; closed subgroups of a free pro-p group are free pro-p, so it is coherent. Finite-index permanence gives coherence of Q_n, and polycyclic-kernel lifting gives coherence of P_n.

Thus the construction is a valid obstruction to one uniform-bound approach, with no incoherence or single inaccessible-group claim.

## 10. Inverse limit: PASS

Each relator at level n+1 follows from a level-n commutation relation by taking a p-th power of one entry; the endpoint case uses the x-entry. Therefore `R_(n+1) <= R_n`, with the stated surjective transition maps.

In any finite p-quotient of exponent dividing `p^e`, every level-n relator vanishes once `n >= 2e-1`, since one of i and n-i is at least e. Hence R_n is eventually inside every open normal subgroup of the free pro-p F. Their intersection is trivial. This uses actual finite p-quotients of F and residual finiteness, rather than treating a formal limiting relator as a relation.

Every compatible coset sequence has a nonempty intersection by compactness, proving surjectivity of the canonical map from F onto the inverse limit; the trivial intersection proves injectivity. The isomorphism with free pro-p F_2 is valid. No embedding into a fixed target amalgam is obtained or claimed.

## 11. Restricted infinite commutators and Dickson frontier: PASS

Commutation at (a,b) implies commutation at every coordinatewise greater pair by ordinary positive integral powers. Minimal pairs form an antichain; increasing first coordinates force strictly decreasing second coordinates, which cannot continue indefinitely in the nonnegative integers. Every s has a minimal predecessor by looking inside its finite lower rectangle. These arguments include arbitrary S and the empty set.

The closed normal closure of all relators thus equals that of the finite minimal subfamily. This proves finite pro-p presentability of P(S), with no need for an abstract-word approximation or an unproved infinite-presentation limit. The author correctly distinguishes this from coherence, and from arbitrary commutator families or arbitrary polycyclic amalgams.

## 12. Sources and retained hypotheses

Primary sources were read directly during the audit, not inferred solely from the author's summaries:

- [Chatzidakis–Zalesskii, corrected arXiv v2](https://arxiv.org/pdf/2007.06867v2): Section 2.2 establishes the faithfulness convention; Theorems 5.1 and 6.8 provide the two finite-decomposition inputs. The procyclic restriction is retained. The correction to Proposition 8.2 is unrelated to the arguments audited here.
- [Castellano–Zalesskii, publisher PDF](https://ems.press/content/serial-article-files/33381): Corollary 3.14 has analytic amalgamation and malnormality in one factor; Theorem 3.15 retains k-acylindricity. Neither supplies unrestricted finite-rank accessibility. [Publisher metadata](https://ems.press/journals/ggd/articles/13693811) confirms online publication in 2023 and volume 18 (2024).
- [Snopce–Zalesskii, publisher page](https://doi.org/10.1112/blms.12664): the chordality characterization is credited background, not an unproved input to the new deductions.

This was a targeted source-hypothesis audit, not a claim of exhaustive current literature review or historical novelty.

## 13. Integrity and controls

The manifest hash exactly matches the assigned pin. All 15 payload files match both recorded byte counts and SHA-256 hashes. The complete verification script was executed on a temporary copy, so the frozen source files were not rewritten. Its deterministic outputs were byte-identical to the originals.

Replayed controls passed:

- 128 chain parameter pairs;
- 15 enumerated finite lattice systems;
- 65,536 finite exponent subsets;
- 64 exponent-cover parameters.

These establish integrity and the encoded finite arithmetic/combinatorics only. The universal pro-p statements were separately checked as above. The `universal_proofs_machine_verified=false`, `full_target_solved=false`, five-attempt exhaustion, and no-novelty flags remain appropriate.

## Final disposition

Resolve R1 and preferably R2–R3, regenerate the manifest, and recheck the changed payload. No broader mathematical revision is currently required by this audit. The surviving output consists of finite-decomposition criteria, valid permanence lemmas and special cases, a valid uniform-bound obstruction, and two valid no-go observations. The original coherence problem is still unresolved in the general higher-rank core-free polycyclic-edge case without a qualifying subgroup-decomposition/acylindricity result.
