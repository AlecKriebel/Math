# Round 2: localization, minimality, and direct finiteness

Checkpoint: **2026-09-26 05:03 UTC / 2026-09-25 22:03 PDT**. Assigned re-review completion: **100%**. This percentage measures the assigned audit, not the whole research program.

Final source reviewed: `submission_review_2026-09-25/manuscript/main.tex`, SHA-256 **`d79e9fcddad89606de769b672205d09f0e846e135d27a5419ba7b362095a1716`**. The earlier first-round source was SHA-256 `9ef5716ef8c663ae0cb012899b4eea67a7500fee6006e2ce0e3f61e99803f51c`. I read the full source diff and the revised assigned sections. No manuscript edits, commit, push, or external communication were performed by this reviewer.

## Disposition

**Closed: no remaining substantive mathematical finding in the assigned sections.** The all-n localization/minimality mechanisms remain unchanged and valid under the matrix hypotheses audited separately. The added determinant argument is a correct direct proof of actual finiteness, including the scalar subgroup; it does not establish only projective finiteness. The revised abstract and limitations accurately state the scope relevant to this review.

## First-round items and transient second-round findings

| Item | Final disposition |
|---|---|
| Wenzl parameter citation | **Closed.** Lines 565–566 now cite Theorem 3.6(b), p. 379, for the parameter; Eq. (3.2) remains the correct uniqueness reference at line 557. The formula agrees with the original Wenzl scan inspected in round 1. |
| Unverified journal/preprint numbering | **Closed by removal.** The uncertain GHR definition/conjecture and Rowell–Wang conjecture pinpoints have been removed. General citations preserve the intended attribution, while the checked GHR §5.6, Prop. 4.12, Def. 4.13, and low-dimensional results remain. No mathematical statement was weakened or substituted. |
| Abstract called the reflection's condition a braid relation | **Closed.** The initial second-round hash `eda01047b2fb4b168a7acadd01e54057e1b0899eb5fa994e3f28349b67f97cad` said that the reflection itself satisfies the braid relation. Lines 66–68 now explicitly assign that relation to the **associated Hecke operator**. This agrees with the modified cubic identity for the reflection in Proposition `prop:circle`. |
| Reference to removed generalized-matrix table | **Closed.** The initial second-round source still mentioned a preceding residual table for the old GHR generalized operator near lines 1053–1056. That sentence and the now-unused named operator were removed. Current lines 1043–1052 stop at the accurately qualified opposite/local-basis comparison. |

The last two issues were reported to the parent reviewer, corrected there, and re-read in the exact final hash above.

## All-n localization and minimality

Re-reviewed lines 466–775. Apart from the citation improvements, the specialized Hecke presentation, *-structure, partial-trace normalization, trace-annihilator argument, quotient inclusions, and dimension-three calculation are mathematically unchanged from the independently checked first round.

The logical sequence remains valid:

1. The local quadratic and Yang–Baxter relations give a unital *-representation of the specialized algebra, without assuming it is semisimple.
2. The unnormalized partial trace `Tr_2(P)=2I_4` gives the normalized Markov coefficient `1/2`; consistency and uniqueness identify the whole trace family.
3. Taking `y=x*` in the trace annihilator and using faithful finite matrix trace proves its equality with the kernel.
4. Tensor compatibility proves the exact pullback identity for annihilators, so quotient tower inclusions are injective and intertwine the actual braid generators.
5. The checked GHR quotient/category identification then supplies ordinary unitary localization in the intended sense.

For minimality, both eigenvalues survive any two-strand injective localization. The dimension-two cited obstruction is unchanged. The dimension-three proof still invokes Lechner's character theorem/classification before eliminating `eta=1/3,2/3` by the explicit `T,T^perp` kernel contradictions. It does not assume that a generic embedding preserves the target trace. The positive target norm remains `1/18` in both cases.

Keeping the optional four-strand alternative **in research evidence only is appropriate**. The manuscript proof is complete with its accurately disclosed external input. Replacing it would introduce an additional four-strand projector identity and verification obligation without repairing a defect. The evidence route is not silently used by any current theorem or abstract claim.

## Direct finiteness proof

Re-reviewed the Clifford-frame setup and the new argument at final-source lines 1252–1310. All stages are justified for every fixed `n>=2`:

- A Hermitian Pauli word `P` has `P^2=I`. For a Pauli word `Q`, conjugation by `exp(i pi P/4)` fixes `Q` when `P,Q` commute and produces `iPQ` when they anticommute. Thus each quarter-turn normalizes the finite Pauli group including the phases `{+1,-1,+i,-i}`. The scalar factor `kappa` does not affect conjugation.
- The already-proved global conjugacy transports this action to the displayed conjugated frame for the five-word operator. The frame is fixed at each strand number, independent of the braid word.
- Conjugation gives a homomorphism from `G_n` to the automorphism group of a finite group. Its kernel centralizes every element of the frame. Since Pauli words span the full matrix algebra, this centralizer consists precisely of scalar matrices, intersected with `G_n`.
- The two local eigenvalues have multiplicities eight, so `det(R)=(-1)^8 q^8=q^2=kappa`. An adjacent placement on `n` sites has determinant `det(R)^(4^(n-2))`. Since `4^(n-2)=1 mod 3`, this is again `kappa`, including the boundary case `n=2`.
- Therefore determinants of arbitrary positive and negative braid words lie in the cube roots of unity. A scalar element `lambda I_N`, with `N=4^n`, has determinant `lambda^N`; cubing gives `lambda^(3N)=1`. Hence the scalar kernel has at most `3N` elements.
- A group with finite kernel and finite image is finite. This proves the ordinary group is finite; no closure or compactness inference and no unproved bound on the orders of arbitrary products is involved.

This closes a possible hidden gap in the shorter argument “Clifford implies finite”: the full unitary Pauli normalizer contains all unit scalars, so controlling the scalar kernel really is necessary. The new proof supplies that control exactly. The attribution to the established quaternionic finite-image phenomenon remains appropriate; no new all-n group classification is claimed.

## Abstract, provenance, and limitations

Re-reviewed the abstract, introduction contribution paragraph, verification/provenance section, and limitations. The abstract now explicitly acknowledges the known classification input for dimension three. Its all-strand equivalence and local-opposite language match the displayed comparison theorem; it does not claim a stronger direct local equivalence without a site reversal. The title and limitations do not turn a five-term presentation into an unsupported minimum-support theorem or claim classification outside the chosen reflection circle.

The revised verification section correctly distinguishes five checking routes from five independent arithmetic implementations and states that finite checks do not replace all-n proofs or external classification. The discovery search is explicitly neither reproducible nor claimed exhaustive. The reported public/private chronology and author metadata were not newly independently investigated in this mathematical re-review; their factual audit belongs to the separate provenance task. I found no contradiction between their revised wording and the mathematical scope.

The general dependency limits from round 1 remain: this review accepts the explicitly cited category identification and classification inputs, and the local matrix identities have their own audit. It does not promote the optional four-strand evidence to a manuscript premise, infer local equivalence from equal eigenvalues, or infer all-n truth from the supplied small-n verification programs.

**Strongest verified result:** the revised manuscript retains the valid all-n ordinary unitary localization and minimality argument, and now contains a complete direct finite-image argument that bounds the scalar kernel. All findings raised by this reviewer are closed in the exact final-source hash recorded above.
