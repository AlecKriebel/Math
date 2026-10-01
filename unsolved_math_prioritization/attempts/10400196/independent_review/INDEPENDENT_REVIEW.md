# Independent review: 10400196 / Deloup Question 10.21

## Verdict

**PASS_SCOPED_PARTIALS. The original target remains unsolved after five author turns.** No mathematical correction is required. This report binds to FROZEN_MANIFEST.json SHA-256 817c69afe28dc03bb6df72ba87b134c1634dda69b23e87be5e6c86ef441b16a1 and RESULT.md SHA-256 fa7ec89d51cc7f02c83cdcc413f80300166520a6fd69870b8b663d428e8f170c. This is a proof-and-source review of the stated restricted results, not a certification of novelty or a full solution to the source's intended general refinement.

The reviewer did not contribute to the derivation. The original source, the relevant classical theorem statements and their uses, every written author argument, and all five author checks were reviewed. The independent finite checker is separately authored; its limited arithmetic coverage is not substituted for the topological proof audit.

## 1. Exact source and normalization

The actual Question10.21 page motivates a mod16 refinement of the Spin-c Gauss phase with Y-degree1. It does not explicitly state all the naturality, additivity, spin-recovery or non-torsion conventions that a meaningful geometric refinement would need. The packet correctly refrains from using that abbreviation to claim a trivial phase-branch solution or a blanket no-go.

For a nonhomogeneous finite quadratic function the Brown value can be rational modulo8. The Z/3 example has phase1/12, hence Brown2/3. Q/16Z is the appropriate scalar lift group in that normalization. The negative boundary convention in Massuyeau's Lemma12 was checked visually; the author's epsilon convention correctly reconciles it with the positive sentence in the original source. No sign mismatch was found in the retained results.

On a general Spin-c three-manifold, the canonical quadratic function is on H2(M;Q/Z). The explicit diag(0,2),c=(2,0) example really has a nontrivial restriction to its divisible radical. The two displayed sections are group homomorphisms and yield opposite Z/2 quadratic phases. This is a valid obstruction to the naive finite-section prescription, not a denial of the canonical infinite-domain quadratic object.

## 2. Scoped algebraic and additive obstructions

The fourfold isometry between q_+ and q_- is correct: over F2, I+J is invertible and sends odd-weight vectors to their complements. Any additive lift would assign the isometric fourfold sums values4 and12 modulo16. The contradiction works in Q/16Z as well as for integer-valued lifts. The use of Deloup–Massuyeau Corollary2 for the rational-homology degree-zero consequence is valid.

The stronger all-manifold additive obstruction is also valid under its explicit extra hypothesis. Published Example3.3 states genuine orientation-preserving Spin-c diffeomorphism of the two absorbed structures on S2×S1#RP3 when the free Chern label is twice an odd integer. It is not merely a Y1 assertion. Cancellation of the common additive X term forces equal RP3 values, contradicting their unequal mod8 reductions. This does not apply to the restricted rational-homology theorem or rule out every nonadditive interpretation.

The Z/4 retraction obstruction in turn3 is correctly labeled as an extra affine/conjugation-naturality obstruction. Translation by an order-two class is not silently asserted to be a diffeomorphism. The phase-lift torsor description F=F0+8d follows from the exact two-element kernel and preserves precisely the stated finite-type relations. Its deliberately weak piecewise homology-sphere construction is not promoted as the intended answer.

## 3. Canonical odd-Chern theorem

The strongest positive theorem is sound. For a rational homology sphere, H1 is finite and H^1(M;Z)=0. The Bockstein therefore makes Spin→Spin-c injective, and its image is the zero-Chern set. If c(sigma) has odd order, its half in the canonical odd-primary subgroup is unique. Subtracting that half defines a unique spin-induced origin sigma0 and hence a unique spin structure s_sigma, without any arbitrary choice among the spin structures of M.

Nonsingularity of the linking form uniquely represents q_sigma-q0 by b(a,-). Affine naturality identifies a with the corresponding odd-primary class, up to the declared convention. Homogeneity gives the exact translated-square identity and Gauss-phase shift. Since an odd-order a is killed by some odd n, n²q0(a)=0; thus q0(a) has odd order. The inverse eta of Q/2Z→Q/Z on odd-primary torsion exists uniquely and is a group homomorphism.

These facts prove well-definedness, diffeomorphism naturality, reduction to Brown, orientation behavior and connected-sum additivity of

    epsilon R(M,s_sigma) - 8 eta(q0(a)).

For a Y-surgery, first homology, Chern class, the canonical half and the compatible spin origin all transport naturally. The quadratic correction is unchanged by each surgery; Rochlin has zero two-Y alternating difference by the source's local proof. Therefore the restricted invariant has degree at most1. The integral homology-sphere Poincaré/S3 pair lies in this class, is Y1-equivalent and has different Rochlin values, proving exact degree1. This argument uses a valid rational-homology calibration rather than the source's separate T3 example.

The class is closed under the surgeries and connected sums being asserted. It includes all spin-induced rational-homology structures, odd-order H1, and the exponent-two 2-primary case. A nonzero higher-two-primary Chern component is genuinely outside this construction; the proof does not erase that limitation.

## 4. Characteristic surgery and higher-two-primary failures

For nonsingular symmetric B and characteristic c, the generalized Brown congruence was derived correctly from the homogeneous van der Blij formula and a completed square. An integral Wu vector exists by the characteristic-two kernel/image argument. The difference of the resulting expression and signature(B)-c^T B^-1 c is exactly8w^Tz.

The representative change is -4(c^Tz+z^TBz), and the parenthesis is even. The rho cocycle identity is an exact integer identity before reducing modulo2. The stated correction laws for representatives, congruences, ordinary stabilizations and arbitrary odd stabilization labels are correct. Together with actual link isotopy and the cited Spin-c Kirby theorem they are sufficient for descent, without claiming to construct the correction.

The fixed +4-framed-unknot example is a genuine same-link, same-structure ambiguity: c=2 and10 differ by2B, their defects differ by8 modulo16, and the finite quadratic function is unchanged. The two principal spin-origin computations also differ by8. The general characteristic-sublink formula includes the needed nonbinary-representative term; the relevant sublink is proper by the characteristic parity condition, so the Arf term is defined.

For the two-Y cube, Brown invariance makes the defect sum divisible by8. The proposed parity equation is necessary and sufficient after descent. No unproved common-matrix presentation is used.

## 5. Floer route and final remaining parity

The correction-term congruence gives the canonical lift -4d on all rational homology Spin-c spheres, in the positive discriminant convention. Its failure of degree1 is rigorously demonstrated using the exact sourced orientations and Floer groups:

- P=-Sigma(2,3,5): d=-2, chi_red=0, Casson1;
- Q=Sigma(2,3,7): d=0, chi_red=-1, Casson-1.

Both have Rochlin8. The integral-homology Y2 classification makes them Y2-equivalent, and the source's necessary finite-type implication forces every degree<=1 invariant to agree on them. Their -4d values8 and0 do not. This is a valid obstruction to this particular canonical lift, rather than an argument against all possible lifts.

The Euler-corrected F_E=8(chi_red-d/2) is a well-defined scalar lift, and on integral homology spheres it equals8 Casson=R modulo16. On a general two-Y cube its degree-one condition is exactly the **evenness** of Delta2(chi_red-d/2). Brown invariance supplies integrality only. The paper's torsion identification and the cited augmentation-ideal theorems do not supply the missing parity: their domain and degree bounds are correctly stated, and the elementary Z[Z/4] example shows why ideal membership alone cannot imply coefficient evenness. No realization of that algebraic example as a surgery defect is claimed.

## 6. Computational audit and disposition

All frozen author artifacts and primary source PDFs were hash checked. Each of the five author checks was replayed byte-for-byte. The separate independent checker verifies exact odd-primary/cyclic square-completion and naturality calculations, characteristic matrix cocycles, stabilization, the explicit failures and the Floer/parity bookkeeping. Precise counts and hashes are in the companion receipts. These controls do not prove the general topological statements, which were reviewed in the written arguments and cited primary results.

Recommended outcome: **unsolved5/5 with reviewed scoped results**. Preserve the exact canonical odd-Chern theorem, the explicit hypotheses of every obstruction, the sign/domain caveats and the original higher-two-primary, positive-Betti torsion-Chern and general non-torsion normalization gaps. No further author search is supplied by this review, and no historical novelty is certified.
