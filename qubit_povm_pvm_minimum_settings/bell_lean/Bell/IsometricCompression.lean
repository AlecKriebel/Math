import Bell.Quantum
import Mathlib.Data.Matrix.Kronecker

/-! Isometric embeddings into a fixed finite carrier, with the orthogonal
complement assigned to one declared outcome. No Hilbert-space dimension or
measurement assumption is hidden in the embedding. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace Bell.IsometricCompression

variable {m n : Type*} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]

def embed (V : Matrix m n ℂ) (A : Matrix n n ℂ) : Matrix m m ℂ := V * A * V.conjTranspose

def complement (V : Matrix m n ℂ) : Matrix m m ℂ := 1 - V * V.conjTranspose

variable (V : Matrix m n ℂ) (hV : V.conjTranspose * V = 1)

 theorem embed_positive {A : Matrix n n ℂ} (hA : A.PosSemidef) :
    (embed V A).PosSemidef := hA.mul_mul_conjTranspose_same V

include hV in
theorem embed_trace (A : Matrix n n ℂ) : (embed V A).trace = A.trace := by
  unfold embed
  rw [Matrix.trace_mul_cycle, hV, Matrix.one_mul]

include hV in
theorem embed_mul (A B : Matrix n n ℂ) : embed V A * embed V B = embed V (A * B) := by
  unfold embed
  calc
    V * A * V.conjTranspose * (V * B * V.conjTranspose) =
      V * A * (V.conjTranspose * V) * B * V.conjTranspose := by simp only [Matrix.mul_assoc]
    _ = V * (A * B) * V.conjTranspose := by rw [hV, Matrix.mul_one]; simp only [Matrix.mul_assoc]

include hV in
theorem support_idempotent : (V * V.conjTranspose) * (V * V.conjTranspose) =
    V * V.conjTranspose := by
  calc
    _ = V * (V.conjTranspose * V) * V.conjTranspose := by simp only [Matrix.mul_assoc]
    _ = _ := by rw [hV, Matrix.mul_one]

 theorem complement_hermitian : (complement V).conjTranspose = complement V := by
  simp [complement, Matrix.conjTranspose_mul]

include hV in
theorem complement_idempotent : complement V * complement V = complement V := by
  unfold complement
  have hs := support_idempotent V hV
  noncomm_ring [hs]

include hV in
theorem complement_positive : (complement V).PosSemidef := by
  have hp := Matrix.posSemidef_conjTranspose_mul_self (complement V)
  rwa [complement_hermitian, complement_idempotent V hV] at hp

include hV in
theorem complement_mul_embed (A : Matrix n n ℂ) : complement V * embed V A = 0 := by
  unfold complement embed
  rw [Matrix.sub_mul, Matrix.one_mul]
  have he : V * V.conjTranspose * (V * A * V.conjTranspose) = V * A * V.conjTranspose := by
    calc
      _ = V * (V.conjTranspose * V) * A * V.conjTranspose := by simp only [Matrix.mul_assoc]
      _ = _ := by rw [hV, Matrix.mul_one]
  rw [he, sub_self]

include hV in
theorem embed_mul_complement (A : Matrix n n ℂ) : embed V A * complement V = 0 := by
  unfold complement embed
  rw [Matrix.mul_sub, Matrix.mul_one]
  have he : V * A * V.conjTranspose * (V * V.conjTranspose) = V * A * V.conjTranspose := by
    calc
      _ = V * A * (V.conjTranspose * V) * V.conjTranspose := by simp only [Matrix.mul_assoc]
      _ = _ := by rw [hV, Matrix.mul_one]
  rw [he, sub_self]

 theorem embed_zero : embed V 0 = 0 := by simp [embed]

 theorem embed_one_add_complement : embed V 1 + complement V = 1 := by
  simp [embed, complement]

variable {α : Type*} [Fintype α] [DecidableEq α]

def paddedEffect (E : α → Matrix n n ℂ) (selected a : α) : Matrix m m ℂ :=
  embed V (E a) + if a = selected then complement V else 0

include hV in
theorem paddedEffect_positive (E : α → Matrix n n ℂ) (selected a : α)
    (hE : ∀ a, (E a).PosSemidef) : (paddedEffect V E selected a).PosSemidef := by
  unfold paddedEffect
  apply (embed_positive V (hE a)).add
  split_ifs
  · exact complement_positive V hV
  · exact Matrix.PosSemidef.zero

 theorem paddedEffect_sum (E : α → Matrix n n ℂ) (selected : α)
    (hE : ∑ a, E a = 1) : ∑ a, paddedEffect V E selected a = 1 := by
  simp only [paddedEffect, Finset.sum_add_distrib, embed, ← Matrix.sum_mul,
    ← Matrix.mul_sum]
  rw [hE]
  simpa [embed] using embed_one_add_complement V

include hV in
theorem paddedEffect_idempotent (E : α → Matrix n n ℂ) (selected a : α)
    (hE : E a * E a = E a) :
    paddedEffect V E selected a * paddedEffect V E selected a = paddedEffect V E selected a := by
  unfold paddedEffect
  by_cases ha : a = selected
  · simp only [if_pos ha, Matrix.add_mul, Matrix.mul_add, embed_mul V hV,
      complement_mul_embed V hV, embed_mul_complement V hV, complement_idempotent V hV,
      hE, add_zero, zero_add]
  · simp only [if_neg ha, add_zero, embed_mul V hV, hE]

include hV in
theorem paddedEffect_orthogonal (E : α → Matrix n n ℂ) (selected a b : α)
    (hab : a ≠ b) (hE : E a * E b = 0) :
    paddedEffect V E selected a * paddedEffect V E selected b = 0 := by
  unfold paddedEffect
  by_cases ha : a = selected <;> by_cases hb : b = selected
  · exact (hab (ha.trans hb.symm)).elim
  · simp only [if_pos ha, if_neg hb, add_zero, Matrix.add_mul,
      embed_mul V hV, complement_mul_embed V hV, hE, embed_zero, zero_add]
  · simp only [if_neg ha, if_pos hb, add_zero, Matrix.mul_add,
      embed_mul V hV, embed_mul_complement V hV, hE, embed_zero, zero_add]
  · simp only [if_neg ha, if_neg hb, add_zero, embed_mul V hV, hE, embed_zero]

include hV in
theorem compress_paddedEffect (E : α → Matrix n n ℂ) (selected a : α) :
    V.conjTranspose * paddedEffect V E selected a * V = E a := by
  have hc : complement V * V = 0 := by
    simp only [complement, Matrix.sub_mul, Matrix.one_mul, Matrix.mul_assoc, hV, Matrix.mul_one, sub_self]
  have he (A : Matrix n n ℂ) : V.conjTranspose * embed V A * V = A := by
    simp only [embed, ← Matrix.mul_assoc, hV, Matrix.one_mul]
    rw [Matrix.mul_assoc, hV, Matrix.mul_one]
  unfold paddedEffect
  split_ifs
  · rw [Matrix.mul_add, Matrix.add_mul, he, Matrix.mul_assoc, hc, Matrix.mul_zero, add_zero]
  · simp only [add_zero, he]

end Bell.IsometricCompression

namespace Bell.IsometricCompression
open scoped Kronecker

variable {m n p q : Type*} [Fintype m] [Fintype n] [Fintype p] [Fintype q]
  [DecidableEq m] [DecidableEq n] [DecidableEq p] [DecidableEq q]

theorem kronecker_conjTranspose (V : Matrix m n ℂ) (W : Matrix p q ℂ) :
    (V ⊗ₖ W).conjTranspose = V.conjTranspose ⊗ₖ W.conjTranspose := by
  ext i j
  simp [Matrix.conjTranspose_apply, Matrix.kronecker_apply, mul_comm]

theorem tensor_isometry (V : Matrix m n ℂ) (W : Matrix p q ℂ)
    (hV : V.conjTranspose * V = 1) (hW : W.conjTranspose * W = 1) :
    (V ⊗ₖ W).conjTranspose * (V ⊗ₖ W) = 1 := by
  rw [kronecker_conjTranspose, ← Matrix.mul_kronecker_mul, hV, hW,
    Matrix.one_kronecker_one]

theorem tensor_compression (V : Matrix m n ℂ) (W : Matrix p q ℂ)
    (A : Matrix m m ℂ) (B : Matrix p p ℂ) :
    (V ⊗ₖ W).conjTranspose * (A ⊗ₖ B) * (V ⊗ₖ W) =
      (V.conjTranspose * A * V) ⊗ₖ (W.conjTranspose * B * W) := by
  rw [kronecker_conjTranspose, ← Matrix.mul_kronecker_mul, ← Matrix.mul_kronecker_mul]

theorem trace_embed_pairing (V : Matrix m n ℂ) (A : Matrix n n ℂ) (B : Matrix m m ℂ) :
    (embed V A * B).trace = (A * (V.conjTranspose * B * V)).trace := by
  unfold embed
  calc
    (V * A * V.conjTranspose * B).trace = ((V * A) * (V.conjTranspose * B)).trace := by
      rw [Matrix.mul_assoc]
    _ = ((V.conjTranspose * B) * (V * A)).trace := Matrix.trace_mul_comm _ _
    _ = (A * ((V.conjTranspose * B) * V)).trace := by
      rw [← Matrix.mul_assoc, Matrix.trace_mul_comm]
    _ = _ := by simp only [Matrix.mul_assoc]

variable {k : ℕ}

def povm (V : Matrix Qubit n ℂ) (hV : V.conjTranspose * V = 1)
    (E : Fin k → Matrix n n ℂ) (selected : Fin k)
    (hE : ∀ a, (E a).PosSemidef) (hsum : ∑ a, E a = 1) : POVM k where
  effect := paddedEffect V E selected
  positive := fun a => paddedEffect_positive V hV E selected a hE
  normalized := paddedEffect_sum V E selected hsum

def pvm (V : Matrix Qubit n ℂ) (hV : V.conjTranspose * V = 1)
    (E : Fin k → Matrix n n ℂ) (selected : Fin k)
    (hE : ∀ a, (E a).PosSemidef) (hsum : ∑ a, E a = 1)
    (hidem : ∀ a, E a * E a = E a)
    (horth : ∀ a b, a ≠ b → E a * E b = 0) : PVM k where
  toPOVM := povm V hV E selected hE hsum
  idempotent := fun a => paddedEffect_idempotent V hV E selected a (hidem a)
  orthogonal := fun a b hab => paddedEffect_orthogonal V hV E selected a b hab (horth a b hab)

def state (V : Matrix Qubit n ℂ) (W : Matrix Qubit q ℂ)
    (hV : V.conjTranspose * V = 1) (hW : W.conjTranspose * W = 1)
    (ρ : Matrix (n × q) (n × q) ℂ) (hρ : ρ.PosSemidef) (htrace : ρ.trace = 1) : State where
  density := embed (V ⊗ₖ W) ρ
  positive := embed_positive _ hρ
  normalized := (embed_trace _ (tensor_isometry V W hV hW) ρ).trans htrace

theorem born_padded (V : Matrix Qubit n ℂ) (W : Matrix Qubit q ℂ)
    (hV : V.conjTranspose * V = 1) (hW : W.conjTranspose * W = 1)
    {k l : ℕ} (E : Fin k → Matrix n n ℂ) (F : Fin l → Matrix q q ℂ)
    (selectedA a : Fin k) (selectedB b : Fin l)
    (ρ : Matrix (n × q) (n × q) ℂ) :
    born (embed (V ⊗ₖ W) ρ) (paddedEffect V E selectedA a) (paddedEffect W F selectedB b) =
      (ρ * (E a ⊗ₖ F b)).trace.re := by
  change (embed (V ⊗ₖ W) ρ *
    (paddedEffect V E selectedA a ⊗ₖ paddedEffect W F selectedB b)).trace.re = _
  rw [trace_embed_pairing, tensor_compression, compress_paddedEffect V hV,
    compress_paddedEffect W hW]

def canonicalEmbedding {d : ℕ} (hd : d ≤ 2) : Matrix Qubit (Fin d) ℂ :=
  fun i j => if i = Fin.castLE hd j then 1 else 0

theorem canonicalEmbedding_isometry {d : ℕ} (hd : d ≤ 2) :
    (canonicalEmbedding hd).conjTranspose * canonicalEmbedding hd = 1 := by
  ext i j
  simp [Matrix.mul_apply, Matrix.conjTranspose_apply, canonicalEmbedding,
    Matrix.one_apply, apply_ite, eq_comm]

end Bell.IsometricCompression
