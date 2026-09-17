import CyclicBell.GeneralSecondWitness

/-! Explicit state-vector annihilation of every second-family SOS factor.
The proof uses the literal Fourier compression and unitary invariance of Phi_d,
not scalar attainment or any maximality assumption. The aligned extra factor
I - A_0 tensor B_none also annihilates the same state. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

/-- The vector identity fixes entrywise conjugation, rather than an adjoint,
in the second tensor factor. It is valid in every nonzero dimension. -/
theorem phi_unitary_conjugate_invariance (A : Mat (Ix d)) (hA : UnitaryRel A) :
    applyOp (kron A (entryConjugate A)) (maximallyEntangled d) =
      maximallyEntangled d := by
  funext i
  rcases i with ⟨i,k⟩
  rw [phi_apply]
  change (invSqrtDim d : ℂ) * (A * A.conjTranspose) i k = _
  rw [hA.2]
  by_cases hik : i=k <;> simp [maximallyEntangled,Matrix.one_apply,hik]

/-- Every literal residual P_l = d lambda_l I - A_l tensor Bhat_l from
manuscript eq:second-sos kills Phi_d for the actual permutation strategy. -/
theorem secondPermutation_residual_zero (hd : 2≤d) (κ : Equiv.Perm (Ix d)) (l : Ix d) :
    applyOp (((d : ℂ)*generalLambda l) • (1 : Mat (Ix d × Ix d)) -
      kron (encoded ((secondPermutationStrategy hd κ).alice l))
        (secondFourier (fun y => encoded ((secondPermutationStrategy hd κ).bob (some y))) l))
      (maximallyEntangled d) = 0 := by
  change applyOp (((d : ℂ)*generalLambda l) • (1 : Mat (Ix d × Ix d)) -
    kron (encoded (secondAlice hd κ l))
      (secondFourier (fun y => encoded (permutationBob κ (some y))) l))
    (maximallyEntangled d) = 0
  have hinv := phi_unitary_conjugate_invariance (encoded (secondAlice hd κ l))
    (encoded_unitary (secondAlice hd κ l))
  rw [secondAlice_encoding] at hinv
  have hconj : entryConjugate (entryConjugate (weightedCycle (secondWeight l ∘ κ))) =
      weightedCycle (secondWeight l ∘ κ) := by
    ext i j
    simp only [entryConjugate,star_star]
  rw [hconj] at hinv
  rw [secondPermutation_compression hd κ,secondAlice_encoding,kron_smul_right]
  funext i
  have hv := congrFun hinv i
  simp only [applyOp] at hv
  simp only [applyOp,Matrix.sub_apply,Matrix.smul_apply,smul_eq_mul,
    sub_mul,Finset.sum_sub_distrib,mul_assoc,← Finset.mul_sum]
  simp only [Matrix.one_apply,ite_mul,zero_mul,Finset.sum_ite_eq',Finset.mem_univ,
    Finset.sum_ite_eq,if_true,one_mul,hv,sub_self,Pi.zero_apply]

/-- The extra aligned term has residual I - A_0 tensor B_none, with the
manuscript's B_none = X and A_0 = X. This also vanishes as a vector. -/
theorem secondPermutation_aligned_residual_zero (hd : 2≤d) (κ : Equiv.Perm (Ix d)) :
    applyOp ((1 : Mat (Ix d × Ix d)) -
      kron (encoded ((secondPermutationStrategy hd κ).alice 0))
        (encoded ((secondPermutationStrategy hd κ).bob none)))
      (maximallyEntangled d) = 0 := by
  change applyOp ((1 : Mat (Ix d × Ix d)) -
    kron (encoded (secondAlice hd κ 0)) (encoded (permutationBob κ none)))
    (maximallyEntangled d) = 0
  have hinv := phi_unitary_conjugate_invariance (encoded (secondAlice hd κ 0))
    (encoded_unitary (secondAlice hd κ 0))
  rw [secondAlice_zero] at hinv
  have hconj : entryConjugate (cyclicShift d)=cyclicShift d := by
    rw [cyclicShift,weighted_entry_conjugate]
    simp only [star_one]
  rw [hconj] at hinv
  rw [secondAlice_zero,permutationBob_none]
  funext i
  have hv := congrFun hinv i
  simp only [applyOp] at hv
  simp only [applyOp,Matrix.sub_apply,sub_mul,Finset.sum_sub_distrib]
  simp only [Matrix.one_apply,ite_mul,zero_mul,Finset.sum_ite_eq',Finset.mem_univ,
    Finset.sum_ite_eq,if_true,one_mul,hv,sub_self,Pi.zero_apply]

end CyclicBell.General

#print axioms CyclicBell.General.phi_unitary_conjugate_invariance
#print axioms CyclicBell.General.secondPermutation_residual_zero
#print axioms CyclicBell.General.secondPermutation_aligned_residual_zero
