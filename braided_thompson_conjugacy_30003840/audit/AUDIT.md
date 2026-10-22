# Independent audit of braided Thompson conjugacy reductions

**Verdict: PASS for the stated partial results and unresolved disposition.** No complete solution of conjugacy in F_br or T_br is established. No HOLD-level mathematical defect was found. Two citation improvements and one local packaging correction are listed below; they do not change a theorem or any of the five attempts.

Audited on 2026-10-03 UTC by a reviewer uninvolved in the five attempts. The object reviewed was the frozen twelve-file packet at commit `adad7feb99476804e871218302214b58c5cca58d`, branch `wip/braided-thompson-conjugacy-30003840`, repository `AlecKriebel/Math`. The frozen packet was not edited. This audit added no sixth mathematical attempt and made no remote write.

## Identity and reproducibility

- The eleven content hashes in SHA256SUMS all pass. SHA256SUMS is itself the twelfth intended file.
- All twelve files were independently fetched from the immutable GitHub commit and compared byte for byte with the local packet. All twelve match. The comparison is recorded in `remote_snapshot_verification.json`.
- Running `python -B verify.py` produces output byte-identical to the submitted `verify_results.json`.
- An independent standard-library checker, `independent_controls.py`, was written without importing the submitted checker. Its output is `independent_controls_results.json`. These controls test implementations and examples; the mathematical review below is the basis for accepting the unbounded statements.
- The live branch name was found. This audit identifies the reviewed content by immutable commit rather than assuming that a movable branch always retains this head.

## Source scope and required small repairs

The original OWR report was independently opened. Theorem 44 concerns V_br; Question 48 asks about both F_br and T_br, and the following discussion does not claim to solve either subgroup problem. The packet correctly preserves that distinction. The relevant target is Witzel's cyclically permuting braid version of T, rather than one of the punctured-surface groups also called a braided T. [OWR report, pp. 1594–1598](https://ems.press/content/serial-article-files/46748)

The structural inputs were checked against the primary texts: Zaremsky's Sections 1.1–1.2 give the fixed-tree braid embeddings, cloning convention, pure kernel and split F extension; his introduction gives torsion-freeness of V_br. Franco–González-Meneses supplies a terminating fixed-strand centralizer-generator algorithm. Their different written conjugator convention does not change the packet's explicitly proved right-coset formula. [Zaremsky](https://ems.press/content/serial-article-files/29861), [Franco–González-Meneses](https://arxiv.org/abs/math/0201243)

Repair R1, citation location: in SOURCE_GATE.md, lines 24 and 29, replace “Witzel, Section 5.3” / “Section 5.3 defines BT” by “Witzel, Section 5.2” / “Section 5.2 defines BT.” The definition is on PDF p. 24, after Corollary 5.10 and before Remark 5.11. Section 5.3 discusses cloning systems. Lemma 5.9 is the correct injectivity reference in Attempt 3 and should not be changed. [Witzel PDF](https://arxiv.org/pdf/1710.02992)

Repair R2, citation completeness: Attempt 4 invokes the classical F conjugacy algorithm as credited, but SOURCE_GATE.md does not give a direct bibliographic entry for that input. Add Belk–Matucci, *Conjugacy and Dynamics in Thompson's Groups*, Geometriae Dedicata 169 (2014), 239–261, or an equivalent original source. This is a supported established theorem, not a mathematical gap. [Belk–Matucci](https://arxiv.org/abs/0708.4250)

Optional literature addition: Lins de Araujo–de Oliveira-Tosti–Santos Rego (2023), Question 5.11, again asks about conjugacy and twisted conjugacy for a family explicitly containing F_br. This supports the limited historical scope but is not proof of present-day nonexistence of a solution. A fresh bounded search found no primary source settling both requested groups; the research page still lists the Bux–Santos Rego conjugacy preprint with the OWR report. [2023 article](https://link.springer.com/article/10.1007/s10711-023-00790-2), [research page](https://ysantosrego.github.io/research-and-publications/)

Repair R3, packaging: the local public directory additionally contains `__pycache__/verify.cpython-312.pyc`, which is unmanifested and not one of the twelve immutable remote files. Exclude it from any final recursive archive. The audit used `python -B` and did not create this file. Preserve only the intended packet plus explicitly selected audit deliverables.

The original corpus hashes, complete queue/history searches, and failed UnsolvedMath access are recorded in the packet; this reviewer did not independently repeat every historical negative search or re-download the entire corpus. The mathematical target was independently verified from the original report, so it does not depend on those negative searches. No historical novelty or exhaustive literature-completeness claim is accepted or needed.

## Braid convention audit

Cloning a general braid is an injective function, not a homomorphism at a fixed strand index. The bottom-index convention requires the matching top index to move under the braid permutation. For pure braids the two indices agree, and the cloning maps restrict to homomorphisms. The packet uses the homomorphism property only for pure kernel braids; expansions of general conjugators and finite-order-quotient elements are diagram expansions with the induced endpoint refinement. No incorrect substitution of a nonpure cloning homomorphism was found.

Parallel clones have zero mutual linking, and each clone has exactly the old strand's linking with every other strand. Crossing contributions belonging to a conjugating braid cancel against its inverse after label transport. Consequently conjugation acts on linking data through the quotient prefix map, with the inverse in the pullback formula exactly where the packet places it. Reversing the global stacking convention reverses the identification of a displayed braid permutation, but does not alter any claimed subgroup separation. The independent checker includes non-involutive conjugating permutations to test this point rather than relying only on transpositions.

## Attempt 1

**PASS.** If b = h a h^(-1), the full transporter is h C_G(a): h^(-1)x centralizes a for every other transporter x. Its intersection with pi^(-1)(Q) is therefore equivalent to the stated intersection of pi(h) pi(C_G(a)) with Q. No equality between pi(C_G(a)) and C_V(pi(a)) is assumed. A subgroup membership algorithm does not turn this infinite coset test into a negative decision procedure.

For the displayed three-strand example, sigma_1^2 has L_12 = 1 and L_13 = 0; conjugation by sigma_2 moves the nonzero entry to L_13. The first/last linking character is preserved by F_br conjugation and by endpoint cloning. The values 0 and 1 prove nonconjugacy in F_br at every refinement, even though the displayed ambient conjugator exists. The argument does not depend on the shape of the three-leaf tree.

## Attempt 2

**PASS.** The function lambda is unchanged by elementary expansion, hence by representative change, and is additive after a common pure-braid refinement. Its equivariance follows from strand-label transport. This is not just fixed-strand linking data: attaching the values to Cantor cylinders is essential.

The twin-run classifier is complete for the stated linking-function orbit, for the following reasons:

1. Equal rows are precisely equal functions z ↦ lambda(x,z) for points in the corresponding cylinders. Their maximal consecutive components are intrinsic to linear order; the analogous components are intrinsic to cyclic order.
2. Deleting a duplicate row and its matching column cannot create a new row equality. If two retained rows differ at a deleted column, they differ at the retained identical column as well.
3. For matching reduced matrices, each pair of corresponding runs can be refined to equal positive leaf counts. Every integer count at least its current count is achievable by binary subdivisions. Order pairing gives an F element; cyclic pairing gives a T element. A run crossing the initial cut causes no obstruction because both endpoints are handled in the cyclic enumeration.
4. All-zero data reduces to one zero entry. Nonadjacent occurrences of equal rows are correctly retained as separate linear runs. No interval length invariant is missing: the allowed tree-pair prefix substitutions can change those lengths.

Thus the four-strand adjacent-edge versus opposite-edge example excludes every T_br conjugator, not merely four-strand conjugators. Both patterns have four distinct intrinsic runs, and cyclic order distinguishes their supported pairs.

The commutator [sigma_1^2, sigma_2^2] has zero linking but the displayed SL_2(Z) image is [[13,8],[8,5]], so it is nonidentity. Injectivity of the fixed-tree braid embedding preserves this nonidentity in K. Its comparison with the identity therefore decisively disproves completeness for group conjugacy. No faithfulness of the two-dimensional representation is required to infer nonidentity from a nonidentity image.

## Attempt 3

**PASS.** The necessity of the simultaneous refinement criterion is sound. Align a conjugator's input endpoint with the first pure-kernel tree; align its output with the second tree, propagating the new refinement back to the input. This only adds carets and preserves the first alignment. Purity makes each input element expand at its two endpoints using the same forest. At the aligned output tree, equality in V_br implies equality of the finite braids by fixed-tree injectivity. Sufficiency is ordinary stacking of the permitted tree-braid-tree conjugator.

At a fixed pair of refinements, the set of braid conjugators is beta_0 C_(B_n)(p_S). Passing the computed centralizer generators to S_n gives exactly its permutation image, not an approximation. The intersection test with the identity subgroup or cyclic rotation subgroup is finite, and storing generator words recovers an actual permitted conjugator. This proof works for nonpure fixed-strand braids as well, as later required by Attempt 5.

Enumerating the finitely many refinement pairs at each leaf count gives a positive semidecision. Proposition 3.2 states the correct logical equivalence: an effective bound on positive witness size yields a decision algorithm, and a decision algorithm plus the semidecision computes such a bound. The bound is on positive instances only; returning zero on negatives is legitimate. Nothing supplies that bound. Failure at any finite stage is not a negative answer for the full problem.

## Attempt 4

**PASS.** With multiplication (a,f)(b,g) = (a alpha_f(b),fg), conjugation by (k,z) gives kernel coordinate

    k alpha_z(a) alpha_(z f z^(-1))(k^(-1)).

After quotient normalization, the quotient equals f exactly when z lies in C_F(f), producing the stated equation

    b = k alpha_z(a) alpha_f(k^(-1)).

Normalization by s(t)^(-1) changes b to alpha_(t^(-1))(b), with no missing cocycle because the chosen F section is a homomorphism. The centralizer action on alpha_f-twisted conjugacy classes is well defined because alpha_z commutes with alpha_f for such z.

Applying lambda gives lambda_b − z.lambda_a = (1−f)nu with the correct signs. Finite-orbit sums telescope. For the increasing Cantor action of F, a finite orbit of an unordered pair fixes both endpoints, so the fixed-pair restriction is valid. The packet does not mistake checking a proposed finite-step nu for deciding the existential infinite-module equation. At f = identity, the zero-linking commutator refutes sufficiency of the abelian condition.

The braid-free special case is exactly the classical quotient conjugacy problem because F embeds by the section. The T extension cannot split: a section would inject a nontrivial finite-order T element into the torsion-free subgroup T_br of V_br. A set-theoretic choice of T lifts would require a factor set; the packet correctly refuses the cocycle-free substitution.

## Attempt 5

**PASS.** The cubes of sigma_1 sigma_2 and sigma_2 sigma_1 both equal Delta^2 by the braid relation. At any three-leaf tree the quotient maps have opposite cyclic steps, giving rotation numbers 1/3 and 2/3, up to the chosen stacking convention. Unequal leaf widths do not affect these three-cycles. Orientation-preserving conjugacy preserves this distinction. The example refutes powers alone, and the packet explicitly acknowledges that it does not refute a method also checking quotient conjugacy.

If y' = d^(-1)y d and c = x^m = (y')^m, any conjugator from x to y' centralizes c on taking mth powers. Conversely such a centralizer conjugator is an H-conjugator. The remaining root-in-centralizer problem is accurately identified and not solved by an implicit assumption.

Lemma 5.2 is valid as stated. After refining by the domains of all powers, each image f^i(P_0) is a genuine cylinder partition. The finite family of m image partitions is permuted by f, including its final-to-initial transition because f^m = identity. Homeomorphisms preserve intersections, so f preserves their common refinement. Cylinders are nested or disjoint, ensuring that its atoms remain cylinders. This establishes both finiteness and effective construction; it does not rely on a uniform grid or on equal interval widths.

For Proposition 5.3, first refine the source of the proposed conjugator so its quotient maps every relevant cylinder to a cylinder, including the pullback of the target input tree. Lemma 5.2 then makes it f-invariant without losing those refinements. The image partition is g-invariant because the quotient conjugator intertwines f and g. The resulting braid equality is at a fixed tree and the conjugator permutation is cyclic. This proves necessity; stacking proves sufficiency. Enumeration still lacks a global bound and does not cover infinite-order quotients through powers.

## Independent controls

The independent checker passes all of the following:

- 90 cabled braid-relation checks in Artin's free-group action, including negative words
- 96 linking-equivariance checks
- 336 pure source-strand cloning and linking checks
- 336 pure-cloning homomorphism checks, plus an explicit negative control showing nonpure fixed-index cloning is not a homomorphism
- 3 exact braid witness checks in the free-group action, including equal cubes and the nontrivial commutator
- 5,625 ordered pairs of binary symmetric zero-diagonal matrices of sizes 1 through 4 for each of the linear and cyclic classifiers, compared against exhaustive common blow-ups through 7 leaves
- 1,296 conjugation equations in a nonabelian finite semidirect product, including 648 normalized centralizer cases
- 1,748 invariant-partition constructions for finite-order T prefix maps with deliberately asymmetric source/target expansions; the largest resulting partition has 20 leaves

The source checker additionally reproduces its claimed 2,240 deterministic matrix-cloning/rotation checks and 24 S_4 transporter checks. Neither checker implements general braid centralizers or proves the global mathematical statements by testing.

## Final disposition

**Accept the five attempts as a correct, explicitly partial research packet. Keep the original problem UNRESOLVED, attempts 5/5.** Apply R1 and R2 when preparing a revised packet, update its hashes, and exclude R3 from packaging. No mathematical theorem needs retraction or weakening.

Do not relabel this work as a solution of Question 48, a negative undecidability result, or a new conjugacy decision algorithm. The unresolved inputs remain an effective global refinement termination mechanism and the relevant nonabelian twisted-conjugacy or root-centralizer orbit decision procedures. There is no sixth attempt in this audit.
