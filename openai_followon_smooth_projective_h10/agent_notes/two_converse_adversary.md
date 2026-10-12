# Independent adversarial audit of the pointwise 2-converse

Checkpoint: 2026-10-06 America/Los_Angeles. Source checkout was read only at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. No external individual was contacted and no Git mutation was made. Compact text only was written because of the disk constraint.

This reviewer was assigned the original downstream requirement and the pinned source, without a favorable mathematical summary. The source is the family 004 companion `A-pointwise-2-converse-for-elliptic-curves-with-rational-two-torsion-September-24-2026/build/`.

## Verdict and scope

**No concrete false lemma or arithmetic counterexample was established in this pass. This is not a clean verification verdict for the pointwise 2-converse.** Several subtle algebraic steps withstand an independent reconstruction, recorded below. The central new arithmetic construction still has not been independently verified end to end by this auditor. In particular, I did not reproduce the complete weighted optimal-embedding/reduction correspondence or every target-side Selmer-cone map and nullhomotopy claimed in the assembly proposition.

The exact downstream use is:

`E_l : y^2 = x(x-l)(x+3l)`, full rational 2-torsion, and `dim_F2 Sel_2(E_l/Q)=3`. The finite 2-Selmer bound gives `corank_Z2 Sel_{2∞} <= 1`. The companion's claimed theorem then supplies rank equality and finite Sha, including finite Sha[2∞]. The finite 2-Selmer dimension alone does **not** eliminate the possibility of rank zero with a divisible 2-primary Sha contribution of corank one. I found no independent shortcut that removes this dependency for all the prime parameters used downstream.

Completion estimates: 65% for this bounded adversarial audit of the designated arithmetic interfaces; no claim of completion of the upstream theorem proof audit or the project publication package. The estimate represents coverage, not evidence of correctness.

## Material inspected

- `ring-limits.tex`: the two stated outputs; finite Artin models; fixed-diagram limits and target-side compression; Kummer local conditions and derived degree zero; finite-precision ring-class characters; local acyclicity; uniform residual sizes; all-sequence evaluation; exact common kernel; outer DVR construction; characteristic-zero irreducibility and finite Chebotarev realization.
- `ring-determinants.tex`: split local models; derivative descent at 2; paired functional; determinant switch; inner/outer rank reduction; terminal minor; central specialization and local indices; group-ring unused-prime correction; Schur elimination; bounded clearing; arithmetic assembly; coefficient-bit and binary transfer; missing-vertex conclusion.
- `nonvanishing.tex`: both witness propositions and the complete progression-moment/sieve proof.
- `coefficients.tex`: even coefficient comparison, Kummer detector, the explicit finite Schwartz/weighted ternary theta bridge and its orientation count, odd detection, and minimum-depth normalization.
- The relevant collected interfaces and corank formulas in `pointwise.tex`. The full graph/address construction and the rest of the final pointwise assembly were not assigned to this reviewer and have not been fully independently reconstructed here.

## Independently reconstructed checks

### 1. Exact Frobenius identity and the extra bit at 2

`ring-determinants.tex`, `rd:exact-frobenius`, is correct. In the quotient by `F^2-aF+l=0`,

`(F-a)(aF-(l+1)) = aF^2-(a^2+l+1)F+a(l+1) = a-(l+1)F`.

An independent integer companion-matrix calculation checked 66 pairs `-5<=a<=5`, `1<=l<=11` odd, with no discrepancy; the polynomial calculation is the universal verification, not the finite test. The manuscript explicitly requires one extra bit in `v_2(l+1)>=a+1` for the derivative's finite coordinate. I did not find a missing factor of 2 in this displayed calculation.

The descent argument also explicitly descends once from the field of complete conductor and clears a uniformly killed torsion coefficient obstruction. It does not multiply a factor once per derivative prime. Thus a purported counterexample based only on the number of derivative primes would not attack its stated mechanism.

### 2. A bounded Artin model does not by itself bound torsion

The source correctly separates these issues. Its finite Artin contraction uses nilpotence and splits the residual complex into its cohomology and disks. This construction admits a direct homological perturbation reconstruction even for the locally constant cochain modules, which are flat over the finite coefficient ring. Compactness of bounded matrices preserves specified finite diagrams but does not supply arithmetic maps absent at finite level.

The manuscript explicitly notes the toy complex `[O --2^i--> O]`: bounded size with unbounded torsion. The outer argument is intended to add genuine arithmetic switches before obtaining a nonzero terminal minor. I could not invalidate it merely by invoking that toy example; such an objection would ignore an explicit hypothesis of `rd:outer-bound`.

### 3. Schur-complement pole bound

`rd:schur` has a valid mechanism for avoiding a loss proportional to the number of eliminated local blocks. If the block-diagonal augmentation `A` has inverse numerator matrix `C` with pole at most `h`, and `B=A+2E`, then `BC=1+2F`, with pole at most `h` in each entry of `F`. Modulo `2^M`,

`B^{-1} = C sum_{j=0}^{M-1}(-2F)^j`.

The term of index `j` has pole at most `(j+1)h`. Summing more matrix entries does not worsen a lower bound on Laurent exponents. Hence a bound `Mh` independent of the number of blocks follows **if** the actual arithmetic model has precisely the asserted block-diagonal augmentation and power-series entry lifts. This last arithmetic-model identification is a necessary hypothesis, not a consequence of abstract rank counting.

### 4. Binary transfer through a bounded clearing factor

I reconstructed `rd:binary-transfer` with its given assumptions. Testing the negative coefficients of `f_x` through degree zero modulo `2^M`, together with the constant coefficient of `d_x`, is sufficient. At the selected character, the constant coefficient of `f_x` has valuation `c`, so its DVR valuation is at most `c`; integrality of `d_x` bounds all coefficients of the power series `u_x` below by `-c`. Terms of negative degree in `f_x` therefore contribute to the constant-term convolution only in `2^{M-c} Z_2`. Division by `f_0(0)` loses another `c`, giving the stated `M-2c` congruence. No uniform negative-support bound on `d_x` is required.

Thus the large family does not invalidate this purely algebraic step. The relevant unresolved verification is whether the actual family admits the bounded `f` with nonzero bounded central value assumed by this lemma.

### 5. No simple falsification of the nonvanishing sieve

The source's use of a first moment for odd root number and a nonnegative first moment plus a lower sieve for even root number is appropriately separated. The factor-count bound can be absolute even though the size threshold depends on the curve and progression: an absolute error exponent and polynomial divisor exponent give an absolute level-of-distribution exponent, after which the sieve removes primes below a fixed power of `X`.

I checked the displayed approximate-functional-equation normalization, the prime-power Gauss-sum cases, the local density identity `beta_p=1/(1+p F_p^ev)`, and the transition from a polynomial `b`-error to a fixed sieve exponent. No concrete contradictory case was found. This is not a full independent reproduction of every analytic continuation and strip-bound input cited in that proof.

## Central arithmetic verification still outstanding

The following are exact verification gaps in **this audit**, not established false assertions in the manuscript. The manuscript supplies arguments for them; declaring them disproved merely because they are new would be unjustified.

1. **Weighted theta bridge (`co:theta-bridge`).** At an actual finite precision, the function obtained by reduced modular parametrization followed by `lambda_M` must transform under Brandt operators as stated; the proposed local Schwartz functions must count exactly the optimal embeddings giving the unaveraged genus-character Heegner sum. The coefficient comparison claims the single fixed multiplier `c_0 2^{omega(N)} L`, with no extra class-number or varying-prime denominator. I checked the individual nilpotent/residue-line weights, the treatment of the integral generator at 2, the root-character parity, and the orbit-stabilizer/orientation count for consistency. I did **not** independently construct the entire equivariant correspondence for arbitrary bad-level depth, including all 2-adic level cases. Its exact equation `co:weighted-comparison` is therefore unvalidated by this reviewer. It is essential for the subsequent odd unit bounds and cannot be replaced merely by modularity of a theta series.

2. **Simultaneous arithmetic assembly (`rd:assembly`, relying on `rd:derivative` and `rl:limit-evaluation-package`).** The proof needs actual finite target cochains, local Kummer lifts, boundary witnesses, duality maps and their nullhomotopies, preserved under the *same* inner ultrafilter and compatible with later switches and the outer quotient. I checked that the manuscript explicitly distinguishes these data from arbitrary quasi-isomorphic complexes and from limits of differential matrices alone. I have not reconstructed all these finite diagrams independently. The displayed determinant and ultrafilter arguments are conditional on that arithmetic interface; their algebraic validity does not independently certify the interface.

3. **Uniform bounded clearing (`rd:family-clearing`).** The proposed elimination needs the old complex as a subcomplex in the augmentation model, simultaneous local-block elimination over the group ring, and augmentation equal to the fixed old complex. The source claims to derive this from localization triangles and liftable disk cancellations. I have reconstructed the ensuing algebraic pole bound, but have not constructed the actual global arithmetic model with all these asserted properties. If that identification is false or loses a growing denominator, the missing-vertex implication is not established. I found no explicit counterexample to the identification.

4. **End-to-end downstream specialization.** Nothing in this pass proves finite Sha[2∞] for every required `E_l` independently of the companion. Nor does it verify the claimed pointwise theorem simply by checking its statement and a few lemmas. A full conclusion requires the other arithmetic audits plus independent verification of the outstanding interface above.

## Repair attempts and decision consequence

I tested whether the downstream 2-Selmer dimension and rational 2-torsion could bypass the converse. They do not: they bound the sum of Mordell–Weil rank and divisible Sha corank, and the missing alternative is exactly what the pointwise converse must exclude. I also tested whether an accumulated denominator is forced by matrix size, derivative count, unused-prime projectors or Laurent convolution. The displayed algebraic constructions explicitly cancel or bound those potential losses, and I found no valid counterexample to those cancellations under their stated hypotheses.

No repair is offered because this pass did not establish an actual mathematical error. The appropriate next step is an independent construction/check of the finite weighted theta correspondence and the simultaneous Selmer/Heegner diagrams, or a concrete falsification of one of their claims. It would be incorrect to promote this report into either a proof-failure theorem or a clean acceptance of the upstream breakthrough.

**Publication implication:** this report supplies some positive local evidence but does not discharge the arithmetic dependency. The unconditional geometric follow-on remains dependent on an end-to-end validation of family 004 and its pivotal arithmetic inputs. If the lead audit finds an actual upstream error elsewhere, that obstruction governs publication independently of the successful checks recorded here.
