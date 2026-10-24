# Mapping class rigidity audit of the 21.129 reduction

Checkpoint: 2026-10-24T19:58:08Z. Scope: only the conditional implication from a quasi-isometry between irreducible pure central quotients, one of mapping class type, to commensurability. Local audit completion estimate: 100%. This is not an estimate of completion of 21.129. No Git operations or external communications were performed.

## Verdict

The mapping class step passes this audit. No counterexample or unfilled hypothesis was found in this step. The complete BKMM theorem, rather than its shortened introduction, is essential at rank 3. A uniform proof using the finite center also avoids needing an extra center calculation in complexity 2.

This verdict assumes the earlier product argument has already supplied a quasi-isometry of the individual factors. It does not infer a quasi-isometry of central quotients merely by cancelling a cyclic factor from an arbitrary quasi-isometry of the original Artin groups.

## Exact notation and claim

For an irreducible spherical type T, let P_T be its pure Artin group, Q_T=P_T/Z(P_T), and bar(A_T)=A_T/Z(A_T). These are different quotients. The claim audited is:

If Q_T is quasi-isometric to Q_S, and S is A_n or B_n with n at least 3, or D_4, then A_T and A_S are abstractly commensurable.

The proof is conditional on the published inputs below, with no new theorem about the remaining exceptional Artin types assumed.

## BKMM statement and boundary cases

Cached source: `priority/sources/bkmm2012.txt`.

- Section 2.1.1, printed p.789, text lines 375–388: surfaces have punctures rather than boundary circles, complexity is max(3g-3+n,0), and MCG means the extended mapping class group, allowing orientation reversal. The standing ambient-surface assumption is complexity at least 2.
- The shortened introductory Theorem 1.2, printed p.782, text lines 61–65, assumes complexity strictly greater than 2. It cannot alone justify the A_3/B_3 case.
- The complete Theorem 1.2, Section 10, printed p.875, text lines 4468–4472: for a finitely generated group Gamma quasi-isometric to MCG(S), there is a finite-index Gamma' and a homomorphism Gamma' -> MCG(S)/Z(MCG(S)) with finite kernel and finite-index image. This is the version needed here.
- Immediately before that statement, text lines 4465–4466, the center is finite in the cases where it is nontrivial, and is trivial when complexity is greater than 2.
- Section 10.4, printed pp.883–884, text lines 4830–4858, proves the finite-kernel and finite-index conclusions. It explicitly treats S_(1,2) by first using MCG(S_(1,2))/Z as an index-5 subgroup of MCG(S_(0,5)), then restricting Gamma to a finite-index subgroup.
- The exceptional surface in the self-quasi-isometry classification is S_(1,2), not S_(1,3). For S_(1,2) the hyperelliptic involution gives the order-2 central kernel and the quotient embeds with index 5 in MCG(S_(0,5)); see printed p.883, text lines 4810–4828. This exception does not invalidate complete Theorem 1.2.

For A_n the surface is S_(0,n+2), with complexity n-1. Thus n=3 gives S_(0,5), complexity 2, and is covered by the complete theorem. For D_4 the surface is S_(1,3), complexity 3, and neither the complexity-2 issue nor the S_(1,2) exception applies. Rank 2 leads to complexity 1 and is handled by the separate known dihedral commensurability class, outside this claim.

## Torsion-free domain and the finite center

Cumplido–Paris Proposition 3.1(2), printed pp.508–509, text lines 241–272, gives P_T isomorphic to Q_T x Z. Consequently Q_T embeds in P_T. Their Corollary 3.2, printed p.509, text lines 303–305, also gives Q_T as a finite-index subgroup of bar(A_T) with trivial center. Soroko Proposition 3(4), printed p.4, text lines 191–204, supplies an especially direct torsion-free input: P_T is bi-orderable, and so is Q_T by its embedding. A bi-orderable group has no nonidentity finite-order element.

Apply complete BKMM to Gamma=Q_T. Its finite-index subgroup Gamma' is torsion-free, hence its finite kernel is trivial. Thus Gamma' is isomorphic to a finite-index subgroup of M/Z(M), where M is the relevant extended mapping class group.

To conclude commensurability with M, it is enough that M has a finite-index torsion-free subgroup L: since Z(M) is finite, L intersects Z(M) trivially, and L -> M/Z(M) is an injection of finite-index image. Therefore M/Z(M) is commensurable with L and with M. This argument avoids any dependence on asserting separately that Z(MCG(S_(0,5))) is trivial. The cited sources provide the required L in every application below.

## Mapping class models

### A_n and B_n

Cumplido–Paris Lemma 6.4, printed p.516, text lines 595–600, identifies Q_(A_n) with the pure orientation-preserving mapping class group PM(S_(0,n+2)). This subgroup has finite index in the extended MCG, by the puncture-permutation and orientation maps defined immediately before the lemma. It is torsion-free by the preceding pure-Artin argument. Hence Q_(A_n) is quasi-isometric and commensurable to MCG(S_(0,n+2)).

For B_n, use Cumplido–Paris Theorem 2.4(1), printed p.507, text lines 197–198, together with Proposition 3.1(3) and Corollary 3.2: A_(B_n) and A_(A_n) are commensurable, their full central quotients are commensurable, and then Q_(B_n) and Q_(A_n) are commensurable. There is no need to claim a literal identification of Q_(B_n) with a pure sphere mapping class group.

### D_4

Soroko Theorem 5, printed p.5, text lines 242–260, identifies bar(A_(D_4)), the full Artin group modulo its center, with PM(S_(1,3)). It also gives the extended group as

M*(S_(1,3)) = bar(A_(D_4)) semidirect (S_3 x Z/2).

Thus bar(A_(D_4)) has index 12 in the extended group. By Cumplido–Paris Corollary 3.2, Q_(D_4) is a finite-index subgroup of bar(A_(D_4)); hence it is a finite-index torsion-free subgroup of the extended mapping class group.

The distinction between bar(A_(D_4)) and Q_(D_4) is necessary: Soroko Theorem 7/Table 1, printed pp.7–8, text lines 368–429, gives order-2 and order-3 torsion in bar(A_(D_4)). Thus the pure mapping class group PM(S_(1,3)) is not itself the torsion-free domain used to kill BKMM's kernel. No such confusion is required for the reduction.

## Complete conditional deduction

Let S be one of the stated mapping class types. Choose its extended mapping class group M. The models above give Q_S commensurable, and therefore quasi-isometric, to M; for B_n use the A_n model through commensurability. From Q_T quasi-isometric to Q_S, BKMM gives an injective map of a finite-index subgroup of Q_T onto a finite-index subgroup of M/Z(M). The finite-center argument above shows

Q_T commensurable to M/Z(M) commensurable to M commensurable to Q_S.

A finite-index isomorphism of Q_T and Q_S can be multiplied by the identity on Z. Since P_T=Q_T x Z and P_S=Q_S x Z, and the pure Artin groups have finite index in their Artin groups, this proves A_T commensurable to A_S.

The deduction does not require T and S to have equal ranks, though equal rank may already have been established elsewhere in the reduction. It therefore excludes every known noncommensurability comparison involving an A_n/B_n factor (n at least 3) or a D_4 factor, provided that the individual central factors have first been matched by quasi-isometry.

## Remaining gaps and recommended precision

No local gap remains in this conditional mapping class implication. The unchecked dependencies are the factor-matching step, the rank step, and the completeness/currentness of the literature classification; they are outside this audit.

For a final presentation, cite the complete BKMM Theorem 1.2 in Section 10, explicitly name S_(0,5), and state which quotient is torsion-free. The finite-center argument above is a useful replacement for an unsupported assertion that every mapping class target used here has trivial center. The D_4 model should always identify bar(A_(D_4)) with PM(S_(1,3)) and then pass to its finite-index subgroup Q_(D_4).
