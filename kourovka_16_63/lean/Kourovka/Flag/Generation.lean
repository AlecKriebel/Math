/- Generated uncompiled proof source. Every DAG node carries an explicit proof attempt.
The source generator supplies values but is not a mathematical assumption.
Only ordinary reduction and preceding proved equalities are used. -/
import Kourovka.Flag.Concrete
namespace Kourovka.Flag.Generation
open Kourovka.Linear Kourovka.Ambient

set_option Elab.async false
set_option maxRecDepth 100000
set_option maxHeartbeats 20000000

def n0 : E := x
theorem value_0 : n0 = ![1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  decide +kernel

theorem fixed_0 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n0 = n0 := by
  unfold Preserves at hQ
  exact hx

theorem zero_0 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n0 = 0 := by
  unfold IsDerivation at hD
  exact hx

def n1 : E := y
theorem value_1 : n1 = ![0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0] := by
  decide +kernel

theorem fixed_1 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n1 = n1 := by
  unfold Preserves at hQ
  exact hy

theorem zero_1 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n1 = 0 := by
  unfold IsDerivation at hD
  exact hy

def n2 : E := B n0 n1
theorem value_2 : n2 = ![0, 2, 1007, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n2, value_0, value_1]
  decide +kernel

theorem fixed_2 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n2 = n2 := by
  unfold Preserves at hQ
  simp only [n2, hQ, fixed_0 Q hQ hx hy, fixed_1 Q hQ hx hy]

theorem zero_2 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n2 = 0 := by
  unfold IsDerivation at hD
  simp only [n2, hD, zero_0 D hD hx hy, zero_1 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n3 : E := B n0 n2
theorem value_3 : n3 = ![0, 4, 4, 0, 16, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n3, value_0, value_2]
  decide +kernel

theorem fixed_3 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n3 = n3 := by
  unfold Preserves at hQ
  simp only [n3, hQ, fixed_0 Q hQ hx hy, fixed_2 Q hQ hx hy]

theorem zero_3 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n3 = 0 := by
  unfold IsDerivation at hD
  simp only [n3, hD, zero_0 D hD hx hy, zero_2 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n4 : E := B n0 n3
theorem value_4 : n4 = ![0, 8, 1001, 0, 64, 0, 0, 0, 0, 0, 64, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n4, value_0, value_3]
  decide +kernel

theorem fixed_4 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n4 = n4 := by
  unfold Preserves at hQ
  simp only [n4, hQ, fixed_0 Q hQ hx hy, fixed_3 Q hQ hx hy]

theorem zero_4 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n4 = 0 := by
  unfold IsDerivation at hD
  simp only [n4, hD, zero_0 D hD hx hy, zero_3 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n5 : E := ((0 : k) / (1 : k)) • n0
theorem value_5 : n5 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n5, value_0]
  have hs : ((0 : k) / (1 : k)) = (0 : k) := by
    apply (div_eq_iff (by decide +kernel : (1 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_5 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n5 = n5 := by
  unfold Preserves at hQ
  simp only [n5, map_smul, fixed_0 Q hQ hx hy]

theorem zero_5 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n5 = 0 := by
  unfold IsDerivation at hD
  simp only [n5, map_smul, zero_0 D hD hx hy, smul_zero]

def n6 : E := ((-1 : k) / (16 : k)) • n4
theorem value_6 : n6 = ![0, 504, 505, 0, 1005, 0, 0, 0, 0, 0, 1005, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n6, value_4]
  have hs : ((-1 : k) / (16 : k)) = (63 : k) := by
    apply (div_eq_iff (by decide +kernel : (16 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_6 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n6 = n6 := by
  unfold Preserves at hQ
  simp only [n6, map_smul, fixed_4 Q hQ hx hy]

theorem zero_6 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n6 = 0 := by
  unfold IsDerivation at hD
  simp only [n6, map_smul, zero_4 D hD hx hy, smul_zero]

def n7 : E := n5 + n6
theorem value_7 : n7 = ![0, 504, 505, 0, 1005, 0, 0, 0, 0, 0, 1005, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n7, value_5, value_6]
  decide +kernel

theorem fixed_7 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n7 = n7 := by
  unfold Preserves at hQ
  simp only [n7, map_add, fixed_5 Q hQ hx hy, fixed_6 Q hQ hx hy]

theorem zero_7 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n7 = 0 := by
  unfold IsDerivation at hD
  simp only [n7, map_add, zero_5 D hD hx hy, zero_6 D hD hx hy, add_zero]

def n8 : E := ((1 : k) / (8 : k)) • n3
theorem value_8 : n8 = ![0, 505, 505, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n8, value_3]
  have hs : ((1 : k) / (8 : k)) = (883 : k) := by
    apply (div_eq_iff (by decide +kernel : (8 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_8 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n8 = n8 := by
  unfold Preserves at hQ
  simp only [n8, map_smul, fixed_3 Q hQ hx hy]

theorem zero_8 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n8 = 0 := by
  unfold IsDerivation at hD
  simp only [n8, map_smul, zero_3 D hD hx hy, smul_zero]

def n9 : E := n7 + n8
theorem value_9 : n9 = ![0, 0, 1, 0, 1007, 0, 0, 0, 0, 0, 1007, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n9, value_7, value_8]
  decide +kernel

theorem fixed_9 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n9 = n9 := by
  unfold Preserves at hQ
  simp only [n9, map_add, fixed_7 Q hQ hx hy, fixed_8 Q hQ hx hy]

theorem zero_9 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n9 = 0 := by
  unfold IsDerivation at hD
  simp only [n9, map_add, zero_7 D hD hx hy, zero_8 D hD hx hy, add_zero]

def n10 : E := ((1 : k) / (2 : k)) • n2
theorem value_10 : n10 = ![0, 1, 1008, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n10, value_2]
  have hs : ((1 : k) / (2 : k)) = (505 : k) := by
    apply (div_eq_iff (by decide +kernel : (2 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_10 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n10 = n10 := by
  unfold Preserves at hQ
  simp only [n10, map_smul, fixed_2 Q hQ hx hy]

theorem zero_10 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n10 = 0 := by
  unfold IsDerivation at hD
  simp only [n10, map_smul, zero_2 D hD hx hy, smul_zero]

def n11 : E := n9 + n10
theorem value_11 : n11 = ![0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n11, value_9, value_10]
  decide +kernel

theorem fixed_11 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n11 = n11 := by
  unfold Preserves at hQ
  simp only [n11, map_add, fixed_9 Q hQ hx hy, fixed_10 Q hQ hx hy]

theorem zero_11 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n11 = 0 := by
  unfold IsDerivation at hD
  simp only [n11, map_add, zero_9 D hD hx hy, zero_10 D hD hx hy, add_zero]

def n12 : E := ((0 : k) / (1 : k)) • n0
theorem value_12 : n12 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n12, value_0]
  have hs : ((0 : k) / (1 : k)) = (0 : k) := by
    apply (div_eq_iff (by decide +kernel : (1 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_12 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n12 = n12 := by
  unfold Preserves at hQ
  simp only [n12, map_smul, fixed_0 Q hQ hx hy]

theorem zero_12 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n12 = 0 := by
  unfold IsDerivation at hD
  simp only [n12, map_smul, zero_0 D hD hx hy, smul_zero]

def n13 : E := ((-1 : k) / (48 : k)) • n4
theorem value_13 : n13 = ![0, 168, 841, 0, 335, 0, 0, 0, 0, 0, 335, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n13, value_4]
  have hs : ((-1 : k) / (48 : k)) = (21 : k) := by
    apply (div_eq_iff (by decide +kernel : (48 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_13 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n13 = n13 := by
  unfold Preserves at hQ
  simp only [n13, map_smul, fixed_4 Q hQ hx hy]

theorem zero_13 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n13 = 0 := by
  unfold IsDerivation at hD
  simp only [n13, map_smul, zero_4 D hD hx hy, smul_zero]

def n14 : E := n12 + n13
theorem value_14 : n14 = ![0, 168, 841, 0, 335, 0, 0, 0, 0, 0, 335, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n14, value_12, value_13]
  decide +kernel

theorem fixed_14 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n14 = n14 := by
  unfold Preserves at hQ
  simp only [n14, map_add, fixed_12 Q hQ hx hy, fixed_13 Q hQ hx hy]

theorem zero_14 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n14 = 0 := by
  unfold IsDerivation at hD
  simp only [n14, map_add, zero_12 D hD hx hy, zero_13 D hD hx hy, add_zero]

def n15 : E := ((1 : k) / (8 : k)) • n3
theorem value_15 : n15 = ![0, 505, 505, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n15, value_3]
  have hs : ((1 : k) / (8 : k)) = (883 : k) := by
    apply (div_eq_iff (by decide +kernel : (8 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_15 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n15 = n15 := by
  unfold Preserves at hQ
  simp only [n15, map_smul, fixed_3 Q hQ hx hy]

theorem zero_15 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n15 = 0 := by
  unfold IsDerivation at hD
  simp only [n15, map_smul, zero_3 D hD hx hy, smul_zero]

def n16 : E := n14 + n15
theorem value_16 : n16 = ![0, 673, 337, 0, 337, 0, 0, 0, 0, 0, 337, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n16, value_14, value_15]
  decide +kernel

theorem fixed_16 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n16 = n16 := by
  unfold Preserves at hQ
  simp only [n16, map_add, fixed_14 Q hQ hx hy, fixed_15 Q hQ hx hy]

theorem zero_16 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n16 = 0 := by
  unfold IsDerivation at hD
  simp only [n16, map_add, zero_14 D hD hx hy, zero_15 D hD hx hy, add_zero]

def n17 : E := ((-1 : k) / (6 : k)) • n2
theorem value_17 : n17 = ![0, 336, 673, 0, 672, 0, 0, 0, 0, 0, 672, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n17, value_2]
  have hs : ((-1 : k) / (6 : k)) = (168 : k) := by
    apply (div_eq_iff (by decide +kernel : (6 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_17 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n17 = n17 := by
  unfold Preserves at hQ
  simp only [n17, map_smul, fixed_2 Q hQ hx hy]

theorem zero_17 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n17 = 0 := by
  unfold IsDerivation at hD
  simp only [n17, map_smul, zero_2 D hD hx hy, smul_zero]

def n18 : E := n16 + n17
theorem value_18 : n18 = ![0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n18, value_16, value_17]
  decide +kernel

theorem fixed_18 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n18 = n18 := by
  unfold Preserves at hQ
  simp only [n18, map_add, fixed_16 Q hQ hx hy, fixed_17 Q hQ hx hy]

theorem zero_18 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n18 = 0 := by
  unfold IsDerivation at hD
  simp only [n18, map_add, zero_16 D hD hx hy, zero_17 D hD hx hy, add_zero]

def n19 : E := ((0 : k) / (1 : k)) • n0
theorem value_19 : n19 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n19, value_0]
  have hs : ((0 : k) / (1 : k)) = (0 : k) := by
    apply (div_eq_iff (by decide +kernel : (1 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_19 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n19 = n19 := by
  unfold Preserves at hQ
  simp only [n19, map_smul, fixed_0 Q hQ hx hy]

theorem zero_19 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n19 = 0 := by
  unfold IsDerivation at hD
  simp only [n19, map_smul, zero_0 D hD hx hy, smul_zero]

def n20 : E := ((1 : k) / (48 : k)) • n4
theorem value_20 : n20 = ![0, 841, 168, 0, 674, 0, 0, 0, 0, 0, 674, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n20, value_4]
  have hs : ((1 : k) / (48 : k)) = (988 : k) := by
    apply (div_eq_iff (by decide +kernel : (48 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_20 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n20 = n20 := by
  unfold Preserves at hQ
  simp only [n20, map_smul, fixed_4 Q hQ hx hy]

theorem zero_20 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n20 = 0 := by
  unfold IsDerivation at hD
  simp only [n20, map_smul, zero_4 D hD hx hy, smul_zero]

def n21 : E := n19 + n20
theorem value_21 : n21 = ![0, 841, 168, 0, 674, 0, 0, 0, 0, 0, 674, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n21, value_19, value_20]
  decide +kernel

theorem fixed_21 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n21 = n21 := by
  unfold Preserves at hQ
  simp only [n21, map_add, fixed_19 Q hQ hx hy, fixed_20 Q hQ hx hy]

theorem zero_21 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n21 = 0 := by
  unfold IsDerivation at hD
  simp only [n21, map_add, zero_19 D hD hx hy, zero_20 D hD hx hy, add_zero]

def n22 : E := ((-1 : k) / (12 : k)) • n2
theorem value_22 : n22 = ![0, 168, 841, 0, 336, 0, 0, 0, 0, 0, 336, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n22, value_2]
  have hs : ((-1 : k) / (12 : k)) = (84 : k) := by
    apply (div_eq_iff (by decide +kernel : (12 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_22 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n22 = n22 := by
  unfold Preserves at hQ
  simp only [n22, map_smul, fixed_2 Q hQ hx hy]

theorem zero_22 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n22 = 0 := by
  unfold IsDerivation at hD
  simp only [n22, map_smul, zero_2 D hD hx hy, smul_zero]

def n23 : E := n21 + n22
theorem value_23 : n23 = ![0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n23, value_21, value_22]
  decide +kernel

theorem fixed_23 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n23 = n23 := by
  unfold Preserves at hQ
  simp only [n23, map_add, fixed_21 Q hQ hx hy, fixed_22 Q hQ hx hy]

theorem zero_23 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n23 = 0 := by
  unfold IsDerivation at hD
  simp only [n23, map_add, zero_21 D hD hx hy, zero_22 D hD hx hy, add_zero]

def n24 : E := ((0 : k) / (1 : k)) • n0
theorem value_24 : n24 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n24, value_0]
  have hs : ((0 : k) / (1 : k)) = (0 : k) := by
    apply (div_eq_iff (by decide +kernel : (1 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_24 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n24 = n24 := by
  unfold Preserves at hQ
  simp only [n24, map_smul, fixed_0 Q hQ hx hy]

theorem zero_24 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n24 = 0 := by
  unfold IsDerivation at hD
  simp only [n24, map_smul, zero_0 D hD hx hy, smul_zero]

def n25 : E := ((1 : k) / (16 : k)) • n4
theorem value_25 : n25 = ![0, 505, 504, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n25, value_4]
  have hs : ((1 : k) / (16 : k)) = (946 : k) := by
    apply (div_eq_iff (by decide +kernel : (16 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_25 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n25 = n25 := by
  unfold Preserves at hQ
  simp only [n25, map_smul, fixed_4 Q hQ hx hy]

theorem zero_25 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n25 = 0 := by
  unfold IsDerivation at hD
  simp only [n25, map_smul, zero_4 D hD hx hy, smul_zero]

def n26 : E := n24 + n25
theorem value_26 : n26 = ![0, 505, 504, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n26, value_24, value_25]
  decide +kernel

theorem fixed_26 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n26 = n26 := by
  unfold Preserves at hQ
  simp only [n26, map_add, fixed_24 Q hQ hx hy, fixed_25 Q hQ hx hy]

theorem zero_26 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n26 = 0 := by
  unfold IsDerivation at hD
  simp only [n26, map_add, zero_24 D hD hx hy, zero_25 D hD hx hy, add_zero]

def n27 : E := ((-1 : k) / (4 : k)) • n3
theorem value_27 : n27 = ![0, 1008, 1008, 0, 1005, 0, 0, 0, 0, 0, 1005, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n27, value_3]
  have hs : ((-1 : k) / (4 : k)) = (252 : k) := by
    apply (div_eq_iff (by decide +kernel : (4 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_27 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n27 = n27 := by
  unfold Preserves at hQ
  simp only [n27, map_smul, fixed_3 Q hQ hx hy]

theorem zero_27 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n27 = 0 := by
  unfold IsDerivation at hD
  simp only [n27, map_smul, zero_3 D hD hx hy, smul_zero]

def n28 : E := n26 + n27
theorem value_28 : n28 = ![0, 504, 503, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n28, value_26, value_27]
  decide +kernel

theorem fixed_28 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n28 = n28 := by
  unfold Preserves at hQ
  simp only [n28, map_add, fixed_26 Q hQ hx hy, fixed_27 Q hQ hx hy]

theorem zero_28 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n28 = 0 := by
  unfold IsDerivation at hD
  simp only [n28, map_add, zero_26 D hD hx hy, zero_27 D hD hx hy, add_zero]

def n29 : E := ((-1 : k) / (4 : k)) • n2
theorem value_29 : n29 = ![0, 504, 505, 0, 1008, 0, 0, 0, 0, 0, 1008, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n29, value_2]
  have hs : ((-1 : k) / (4 : k)) = (252 : k) := by
    apply (div_eq_iff (by decide +kernel : (4 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_29 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n29 = n29 := by
  unfold Preserves at hQ
  simp only [n29, map_smul, fixed_2 Q hQ hx hy]

theorem zero_29 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n29 = 0 := by
  unfold IsDerivation at hD
  simp only [n29, map_smul, zero_2 D hD hx hy, smul_zero]

def n30 : E := n28 + n29
theorem value_30 : n30 = ![0, 1008, 1008, 0, 1008, 0, 0, 0, 0, 0, 1008, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n30, value_28, value_29]
  decide +kernel

theorem fixed_30 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n30 = n30 := by
  unfold Preserves at hQ
  simp only [n30, map_add, fixed_28 Q hQ hx hy, fixed_29 Q hQ hx hy]

theorem zero_30 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n30 = 0 := by
  unfold IsDerivation at hD
  simp only [n30, map_add, zero_28 D hD hx hy, zero_29 D hD hx hy, add_zero]

def n31 : E := ((1 : k) / (1 : k)) • n1
theorem value_31 : n31 = ![0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0] := by
  rw [n31, value_1]
  have hs : ((1 : k) / (1 : k)) = (1 : k) := by
    apply (div_eq_iff (by decide +kernel : (1 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_31 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n31 = n31 := by
  unfold Preserves at hQ
  simp only [n31, map_smul, fixed_1 Q hQ hx hy]

theorem zero_31 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n31 = 0 := by
  unfold IsDerivation at hD
  simp only [n31, map_smul, zero_1 D hD hx hy, smul_zero]

def n32 : E := n30 + n31
theorem value_32 : n32 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0] := by
  rw [n32, value_30, value_31]
  decide +kernel

theorem fixed_32 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n32 = n32 := by
  unfold Preserves at hQ
  simp only [n32, map_add, fixed_30 Q hQ hx hy, fixed_31 Q hQ hx hy]

theorem zero_32 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n32 = 0 := by
  unfold IsDerivation at hD
  simp only [n32, map_add, zero_30 D hD hx hy, zero_31 D hD hx hy, add_zero]

def n33 : E := B n11 n23
theorem value_33 : n33 = ![0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n33, value_11, value_23]
  decide +kernel

theorem fixed_33 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n33 = n33 := by
  unfold Preserves at hQ
  simp only [n33, hQ, fixed_11 Q hQ hx hy, fixed_23 Q hQ hx hy]

theorem zero_33 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n33 = 0 := by
  unfold IsDerivation at hD
  simp only [n33, hD, zero_11 D hD hx hy, zero_23 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n34 : E := B n18 n33
theorem value_34 : n34 = ![0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n34, value_18, value_33]
  decide +kernel

theorem fixed_34 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n34 = n34 := by
  unfold Preserves at hQ
  simp only [n34, hQ, fixed_18 Q hQ hx hy, fixed_33 Q hQ hx hy]

theorem zero_34 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n34 = 0 := by
  unfold IsDerivation at hD
  simp only [n34, hD, zero_18 D hD hx hy, zero_33 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n35 : E := ((1 : k) / (6 : k)) • n34
theorem value_35 : n35 = ![0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n35, value_34]
  have hs : ((1 : k) / (6 : k)) = (841 : k) := by
    apply (div_eq_iff (by decide +kernel : (6 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_35 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n35 = n35 := by
  unfold Preserves at hQ
  simp only [n35, map_smul, fixed_34 Q hQ hx hy]

theorem zero_35 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n35 = 0 := by
  unfold IsDerivation at hD
  simp only [n35, map_smul, zero_34 D hD hx hy, smul_zero]

def n36 : E := B n18 n35
theorem value_36 : n36 = ![0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n36, value_18, value_35]
  decide +kernel

theorem fixed_36 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n36 = n36 := by
  unfold Preserves at hQ
  simp only [n36, hQ, fixed_18 Q hQ hx hy, fixed_35 Q hQ hx hy]

theorem zero_36 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n36 = 0 := by
  unfold IsDerivation at hD
  simp only [n36, hD, zero_18 D hD hx hy, zero_35 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n37 : E := ((1 : k) / (5 : k)) • n36
theorem value_37 : n37 = ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n37, value_36]
  have hs : ((1 : k) / (5 : k)) = (202 : k) := by
    apply (div_eq_iff (by decide +kernel : (5 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_37 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n37 = n37 := by
  unfold Preserves at hQ
  simp only [n37, map_smul, fixed_36 Q hQ hx hy]

theorem zero_37 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n37 = 0 := by
  unfold IsDerivation at hD
  simp only [n37, map_smul, zero_36 D hD hx hy, smul_zero]

def n38 : E := B n18 n37
theorem value_38 : n38 = ![0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n38, value_18, value_37]
  decide +kernel

theorem fixed_38 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n38 = n38 := by
  unfold Preserves at hQ
  simp only [n38, hQ, fixed_18 Q hQ hx hy, fixed_37 Q hQ hx hy]

theorem zero_38 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n38 = 0 := by
  unfold IsDerivation at hD
  simp only [n38, hD, zero_18 D hD hx hy, zero_37 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n39 : E := ((1 : k) / (4 : k)) • n38
theorem value_39 : n39 = ![0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n39, value_38]
  have hs : ((1 : k) / (4 : k)) = (757 : k) := by
    apply (div_eq_iff (by decide +kernel : (4 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_39 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n39 = n39 := by
  unfold Preserves at hQ
  simp only [n39, map_smul, fixed_38 Q hQ hx hy]

theorem zero_39 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n39 = 0 := by
  unfold IsDerivation at hD
  simp only [n39, map_smul, zero_38 D hD hx hy, smul_zero]

def n40 : E := B n18 n39
theorem value_40 : n40 = ![0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n40, value_18, value_39]
  decide +kernel

theorem fixed_40 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n40 = n40 := by
  unfold Preserves at hQ
  simp only [n40, hQ, fixed_18 Q hQ hx hy, fixed_39 Q hQ hx hy]

theorem zero_40 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n40 = 0 := by
  unfold IsDerivation at hD
  simp only [n40, hD, zero_18 D hD hx hy, zero_39 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n41 : E := ((1 : k) / (3 : k)) • n40
theorem value_41 : n41 = ![0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n41, value_40]
  have hs : ((1 : k) / (3 : k)) = (673 : k) := by
    apply (div_eq_iff (by decide +kernel : (3 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_41 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n41 = n41 := by
  unfold Preserves at hQ
  simp only [n41, map_smul, fixed_40 Q hQ hx hy]

theorem zero_41 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n41 = 0 := by
  unfold IsDerivation at hD
  simp only [n41, map_smul, zero_40 D hD hx hy, smul_zero]

def n42 : E := B n18 n41
theorem value_42 : n42 = ![0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n42, value_18, value_41]
  decide +kernel

theorem fixed_42 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n42 = n42 := by
  unfold Preserves at hQ
  simp only [n42, hQ, fixed_18 Q hQ hx hy, fixed_41 Q hQ hx hy]

theorem zero_42 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n42 = 0 := by
  unfold IsDerivation at hD
  simp only [n42, hD, zero_18 D hD hx hy, zero_41 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n43 : E := ((1 : k) / (2 : k)) • n42
theorem value_43 : n43 = ![0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n43, value_42]
  have hs : ((1 : k) / (2 : k)) = (505 : k) := by
    apply (div_eq_iff (by decide +kernel : (2 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_43 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n43 = n43 := by
  unfold Preserves at hQ
  simp only [n43, map_smul, fixed_42 Q hQ hx hy]

theorem zero_43 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n43 = 0 := by
  unfold IsDerivation at hD
  simp only [n43, map_smul, zero_42 D hD hx hy, smul_zero]

def n44 : E := B n18 n43
theorem value_44 : n44 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n44, value_18, value_43]
  decide +kernel

theorem fixed_44 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n44 = n44 := by
  unfold Preserves at hQ
  simp only [n44, hQ, fixed_18 Q hQ hx hy, fixed_43 Q hQ hx hy]

theorem zero_44 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n44 = 0 := by
  unfold IsDerivation at hD
  simp only [n44, hD, zero_18 D hD hx hy, zero_43 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n45 : E := ((1 : k) / (1 : k)) • n44
theorem value_45 : n45 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n45, value_44]
  have hs : ((1 : k) / (1 : k)) = (1 : k) := by
    apply (div_eq_iff (by decide +kernel : (1 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_45 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n45 = n45 := by
  unfold Preserves at hQ
  simp only [n45, map_smul, fixed_44 Q hQ hx hy]

theorem zero_45 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n45 = 0 := by
  unfold IsDerivation at hD
  simp only [n45, map_smul, zero_44 D hD hx hy, smul_zero]

def n46 : E := ((-1 : k) / (1 : k)) • n35
theorem value_46 : n46 = ![0, 0, 0, 0, 1008, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n46, value_35]
  have hs : ((-1 : k) / (1 : k)) = (1008 : k) := by
    apply (div_eq_iff (by decide +kernel : (1 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_46 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n46 = n46 := by
  unfold Preserves at hQ
  simp only [n46, map_smul, fixed_35 Q hQ hx hy]

theorem zero_46 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n46 = 0 := by
  unfold IsDerivation at hD
  simp only [n46, map_smul, zero_35 D hD hx hy, smul_zero]

def n47 : E := n23 + n46
theorem value_47 : n47 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n47, value_23, value_46]
  decide +kernel

theorem fixed_47 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n47 = n47 := by
  unfold Preserves at hQ
  simp only [n47, map_add, fixed_23 Q hQ hx hy, fixed_46 Q hQ hx hy]

theorem zero_47 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n47 = 0 := by
  unfold IsDerivation at hD
  simp only [n47, map_add, zero_23 D hD hx hy, zero_46 D hD hx hy, add_zero]

def n48 : E := B n18 n47
theorem value_48 : n48 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n48, value_18, value_47]
  decide +kernel

theorem fixed_48 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n48 = n48 := by
  unfold Preserves at hQ
  simp only [n48, hQ, fixed_18 Q hQ hx hy, fixed_47 Q hQ hx hy]

theorem zero_48 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n48 = 0 := by
  unfold IsDerivation at hD
  simp only [n48, hD, zero_18 D hD hx hy, zero_47 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n49 : E := ((1 : k) / (4 : k)) • n48
theorem value_49 : n49 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n49, value_48]
  have hs : ((1 : k) / (4 : k)) = (757 : k) := by
    apply (div_eq_iff (by decide +kernel : (4 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_49 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n49 = n49 := by
  unfold Preserves at hQ
  simp only [n49, map_smul, fixed_48 Q hQ hx hy]

theorem zero_49 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n49 = 0 := by
  unfold IsDerivation at hD
  simp only [n49, map_smul, zero_48 D hD hx hy, smul_zero]

def n50 : E := B n18 n49
theorem value_50 : n50 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n50, value_18, value_49]
  decide +kernel

theorem fixed_50 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n50 = n50 := by
  unfold Preserves at hQ
  simp only [n50, hQ, fixed_18 Q hQ hx hy, fixed_49 Q hQ hx hy]

theorem zero_50 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n50 = 0 := by
  unfold IsDerivation at hD
  simp only [n50, hD, zero_18 D hD hx hy, zero_49 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n51 : E := ((1 : k) / (3 : k)) • n50
theorem value_51 : n51 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n51, value_50]
  have hs : ((1 : k) / (3 : k)) = (673 : k) := by
    apply (div_eq_iff (by decide +kernel : (3 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_51 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n51 = n51 := by
  unfold Preserves at hQ
  simp only [n51, map_smul, fixed_50 Q hQ hx hy]

theorem zero_51 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n51 = 0 := by
  unfold IsDerivation at hD
  simp only [n51, map_smul, zero_50 D hD hx hy, smul_zero]

def n52 : E := B n18 n51
theorem value_52 : n52 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n52, value_18, value_51]
  decide +kernel

theorem fixed_52 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n52 = n52 := by
  unfold Preserves at hQ
  simp only [n52, hQ, fixed_18 Q hQ hx hy, fixed_51 Q hQ hx hy]

theorem zero_52 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n52 = 0 := by
  unfold IsDerivation at hD
  simp only [n52, hD, zero_18 D hD hx hy, zero_51 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n53 : E := ((1 : k) / (2 : k)) • n52
theorem value_53 : n53 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n53, value_52]
  have hs : ((1 : k) / (2 : k)) = (505 : k) := by
    apply (div_eq_iff (by decide +kernel : (2 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_53 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n53 = n53 := by
  unfold Preserves at hQ
  simp only [n53, map_smul, fixed_52 Q hQ hx hy]

theorem zero_53 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n53 = 0 := by
  unfold IsDerivation at hD
  simp only [n53, map_smul, zero_52 D hD hx hy, smul_zero]

def n54 : E := B n18 n53
theorem value_54 : n54 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n54, value_18, value_53]
  decide +kernel

theorem fixed_54 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n54 = n54 := by
  unfold Preserves at hQ
  simp only [n54, hQ, fixed_18 Q hQ hx hy, fixed_53 Q hQ hx hy]

theorem zero_54 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n54 = 0 := by
  unfold IsDerivation at hD
  simp only [n54, hD, zero_18 D hD hx hy, zero_53 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n55 : E := ((1 : k) / (1 : k)) • n54
theorem value_55 : n55 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n55, value_54]
  have hs : ((1 : k) / (1 : k)) = (1 : k) := by
    apply (div_eq_iff (by decide +kernel : (1 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_55 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n55 = n55 := by
  unfold Preserves at hQ
  simp only [n55, map_smul, fixed_54 Q hQ hx hy]

theorem zero_55 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n55 = 0 := by
  unfold IsDerivation at hD
  simp only [n55, map_smul, zero_54 D hD hx hy, smul_zero]

def n56 : E := B n11 n32
theorem value_56 : n56 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0] := by
  rw [n56, value_11, value_32]
  decide +kernel

theorem fixed_56 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n56 = n56 := by
  unfold Preserves at hQ
  simp only [n56, hQ, fixed_11 Q hQ hx hy, fixed_32 Q hQ hx hy]

theorem zero_56 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n56 = 0 := by
  unfold IsDerivation at hD
  simp only [n56, hD, zero_11 D hD hx hy, zero_32 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n57 : E := B n11 n56
theorem value_57 : n57 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0] := by
  rw [n57, value_11, value_56]
  decide +kernel

theorem fixed_57 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n57 = n57 := by
  unfold Preserves at hQ
  simp only [n57, hQ, fixed_11 Q hQ hx hy, fixed_56 Q hQ hx hy]

theorem zero_57 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n57 = 0 := by
  unfold IsDerivation at hD
  simp only [n57, hD, zero_11 D hD hx hy, zero_56 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n58 : E := ((1 : k) / (2 : k)) • n57
theorem value_58 : n58 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0] := by
  rw [n58, value_57]
  have hs : ((1 : k) / (2 : k)) = (505 : k) := by
    apply (div_eq_iff (by decide +kernel : (2 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_58 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n58 = n58 := by
  unfold Preserves at hQ
  simp only [n58, map_smul, fixed_57 Q hQ hx hy]

theorem zero_58 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n58 = 0 := by
  unfold IsDerivation at hD
  simp only [n58, map_smul, zero_57 D hD hx hy, smul_zero]

def n59 : E := B n18 n58
theorem value_59 : n59 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0] := by
  rw [n59, value_18, value_58]
  decide +kernel

theorem fixed_59 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n59 = n59 := by
  unfold Preserves at hQ
  simp only [n59, hQ, fixed_18 Q hQ hx hy, fixed_58 Q hQ hx hy]

theorem zero_59 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n59 = 0 := by
  unfold IsDerivation at hD
  simp only [n59, hD, zero_18 D hD hx hy, zero_58 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n60 : E := ((1 : k) / (4 : k)) • n59
theorem value_60 : n60 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0] := by
  rw [n60, value_59]
  have hs : ((1 : k) / (4 : k)) = (757 : k) := by
    apply (div_eq_iff (by decide +kernel : (4 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_60 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n60 = n60 := by
  unfold Preserves at hQ
  simp only [n60, map_smul, fixed_59 Q hQ hx hy]

theorem zero_60 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n60 = 0 := by
  unfold IsDerivation at hD
  simp only [n60, map_smul, zero_59 D hD hx hy, smul_zero]

def n61 : E := B n18 n60
theorem value_61 : n61 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0] := by
  rw [n61, value_18, value_60]
  decide +kernel

theorem fixed_61 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n61 = n61 := by
  unfold Preserves at hQ
  simp only [n61, hQ, fixed_18 Q hQ hx hy, fixed_60 Q hQ hx hy]

theorem zero_61 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n61 = 0 := by
  unfold IsDerivation at hD
  simp only [n61, hD, zero_18 D hD hx hy, zero_60 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n62 : E := ((1 : k) / (3 : k)) • n61
theorem value_62 : n62 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0] := by
  rw [n62, value_61]
  have hs : ((1 : k) / (3 : k)) = (673 : k) := by
    apply (div_eq_iff (by decide +kernel : (3 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_62 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n62 = n62 := by
  unfold Preserves at hQ
  simp only [n62, map_smul, fixed_61 Q hQ hx hy]

theorem zero_62 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n62 = 0 := by
  unfold IsDerivation at hD
  simp only [n62, map_smul, zero_61 D hD hx hy, smul_zero]

def n63 : E := B n18 n62
theorem value_63 : n63 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0] := by
  rw [n63, value_18, value_62]
  decide +kernel

theorem fixed_63 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n63 = n63 := by
  unfold Preserves at hQ
  simp only [n63, hQ, fixed_18 Q hQ hx hy, fixed_62 Q hQ hx hy]

theorem zero_63 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n63 = 0 := by
  unfold IsDerivation at hD
  simp only [n63, hD, zero_18 D hD hx hy, zero_62 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n64 : E := ((1 : k) / (2 : k)) • n63
theorem value_64 : n64 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0] := by
  rw [n64, value_63]
  have hs : ((1 : k) / (2 : k)) = (505 : k) := by
    apply (div_eq_iff (by decide +kernel : (2 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_64 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n64 = n64 := by
  unfold Preserves at hQ
  simp only [n64, map_smul, fixed_63 Q hQ hx hy]

theorem zero_64 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n64 = 0 := by
  unfold IsDerivation at hD
  simp only [n64, map_smul, zero_63 D hD hx hy, smul_zero]

def n65 : E := B n18 n64
theorem value_65 : n65 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0] := by
  rw [n65, value_18, value_64]
  decide +kernel

theorem fixed_65 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n65 = n65 := by
  unfold Preserves at hQ
  simp only [n65, hQ, fixed_18 Q hQ hx hy, fixed_64 Q hQ hx hy]

theorem zero_65 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n65 = 0 := by
  unfold IsDerivation at hD
  simp only [n65, hD, zero_18 D hD hx hy, zero_64 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n66 : E := ((1 : k) / (1 : k)) • n65
theorem value_66 : n66 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0] := by
  rw [n66, value_65]
  have hs : ((1 : k) / (1 : k)) = (1 : k) := by
    apply (div_eq_iff (by decide +kernel : (1 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_66 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n66 = n66 := by
  unfold Preserves at hQ
  simp only [n66, map_smul, fixed_65 Q hQ hx hy]

theorem zero_66 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n66 = 0 := by
  unfold IsDerivation at hD
  simp only [n66, map_smul, zero_65 D hD hx hy, smul_zero]

def n67 : E := B n33 n39
theorem value_67 : n67 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 720, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n67, value_33, value_39]
  decide +kernel

theorem fixed_67 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n67 = n67 := by
  unfold Preserves at hQ
  simp only [n67, hQ, fixed_33 Q hQ hx hy, fixed_39 Q hQ hx hy]

theorem zero_67 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n67 = 0 := by
  unfold IsDerivation at hD
  simp only [n67, hD, zero_33 D hD hx hy, zero_39 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n68 : E := ((1 : k) / (720 : k)) • n67
theorem value_68 : n68 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n68, value_67]
  have hs : ((1 : k) / (720 : k)) = (604 : k) := by
    apply (div_eq_iff (by decide +kernel : (720 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_68 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n68 = n68 := by
  unfold Preserves at hQ
  simp only [n68, map_smul, fixed_67 Q hQ hx hy]

theorem zero_68 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n68 = 0 := by
  unfold IsDerivation at hD
  simp only [n68, map_smul, zero_67 D hD hx hy, smul_zero]

def n69 : E := B n18 n68
theorem value_69 : n69 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n69, value_18, value_68]
  decide +kernel

theorem fixed_69 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n69 = n69 := by
  unfold Preserves at hQ
  simp only [n69, hQ, fixed_18 Q hQ hx hy, fixed_68 Q hQ hx hy]

theorem zero_69 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n69 = 0 := by
  unfold IsDerivation at hD
  simp only [n69, hD, zero_18 D hD hx hy, zero_68 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n70 : E := ((1 : k) / (6 : k)) • n69
theorem value_70 : n70 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n70, value_69]
  have hs : ((1 : k) / (6 : k)) = (841 : k) := by
    apply (div_eq_iff (by decide +kernel : (6 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_70 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n70 = n70 := by
  unfold Preserves at hQ
  simp only [n70, map_smul, fixed_69 Q hQ hx hy]

theorem zero_70 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n70 = 0 := by
  unfold IsDerivation at hD
  simp only [n70, map_smul, zero_69 D hD hx hy, smul_zero]

def n71 : E := B n18 n70
theorem value_71 : n71 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n71, value_18, value_70]
  decide +kernel

theorem fixed_71 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n71 = n71 := by
  unfold Preserves at hQ
  simp only [n71, hQ, fixed_18 Q hQ hx hy, fixed_70 Q hQ hx hy]

theorem zero_71 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n71 = 0 := by
  unfold IsDerivation at hD
  simp only [n71, hD, zero_18 D hD hx hy, zero_70 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n72 : E := ((1 : k) / (5 : k)) • n71
theorem value_72 : n72 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n72, value_71]
  have hs : ((1 : k) / (5 : k)) = (202 : k) := by
    apply (div_eq_iff (by decide +kernel : (5 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_72 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n72 = n72 := by
  unfold Preserves at hQ
  simp only [n72, map_smul, fixed_71 Q hQ hx hy]

theorem zero_72 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n72 = 0 := by
  unfold IsDerivation at hD
  simp only [n72, map_smul, zero_71 D hD hx hy, smul_zero]

def n73 : E := B n18 n72
theorem value_73 : n73 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n73, value_18, value_72]
  decide +kernel

theorem fixed_73 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n73 = n73 := by
  unfold Preserves at hQ
  simp only [n73, hQ, fixed_18 Q hQ hx hy, fixed_72 Q hQ hx hy]

theorem zero_73 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n73 = 0 := by
  unfold IsDerivation at hD
  simp only [n73, hD, zero_18 D hD hx hy, zero_72 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n74 : E := ((1 : k) / (4 : k)) • n73
theorem value_74 : n74 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n74, value_73]
  have hs : ((1 : k) / (4 : k)) = (757 : k) := by
    apply (div_eq_iff (by decide +kernel : (4 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_74 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n74 = n74 := by
  unfold Preserves at hQ
  simp only [n74, map_smul, fixed_73 Q hQ hx hy]

theorem zero_74 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n74 = 0 := by
  unfold IsDerivation at hD
  simp only [n74, map_smul, zero_73 D hD hx hy, smul_zero]

def n75 : E := B n18 n74
theorem value_75 : n75 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n75, value_18, value_74]
  decide +kernel

theorem fixed_75 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n75 = n75 := by
  unfold Preserves at hQ
  simp only [n75, hQ, fixed_18 Q hQ hx hy, fixed_74 Q hQ hx hy]

theorem zero_75 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n75 = 0 := by
  unfold IsDerivation at hD
  simp only [n75, hD, zero_18 D hD hx hy, zero_74 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n76 : E := ((1 : k) / (3 : k)) • n75
theorem value_76 : n76 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n76, value_75]
  have hs : ((1 : k) / (3 : k)) = (673 : k) := by
    apply (div_eq_iff (by decide +kernel : (3 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_76 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n76 = n76 := by
  unfold Preserves at hQ
  simp only [n76, map_smul, fixed_75 Q hQ hx hy]

theorem zero_76 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n76 = 0 := by
  unfold IsDerivation at hD
  simp only [n76, map_smul, zero_75 D hD hx hy, smul_zero]

def n77 : E := B n18 n76
theorem value_77 : n77 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n77, value_18, value_76]
  decide +kernel

theorem fixed_77 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n77 = n77 := by
  unfold Preserves at hQ
  simp only [n77, hQ, fixed_18 Q hQ hx hy, fixed_76 Q hQ hx hy]

theorem zero_77 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n77 = 0 := by
  unfold IsDerivation at hD
  simp only [n77, hD, zero_18 D hD hx hy, zero_76 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n78 : E := ((1 : k) / (2 : k)) • n77
theorem value_78 : n78 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n78, value_77]
  have hs : ((1 : k) / (2 : k)) = (505 : k) := by
    apply (div_eq_iff (by decide +kernel : (2 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_78 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n78 = n78 := by
  unfold Preserves at hQ
  simp only [n78, map_smul, fixed_77 Q hQ hx hy]

theorem zero_78 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n78 = 0 := by
  unfold IsDerivation at hD
  simp only [n78, map_smul, zero_77 D hD hx hy, smul_zero]

def n79 : E := B n18 n78
theorem value_79 : n79 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n79, value_18, value_78]
  decide +kernel

theorem fixed_79 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n79 = n79 := by
  unfold Preserves at hQ
  simp only [n79, hQ, fixed_18 Q hQ hx hy, fixed_78 Q hQ hx hy]

theorem zero_79 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n79 = 0 := by
  unfold IsDerivation at hD
  simp only [n79, hD, zero_18 D hD hx hy, zero_78 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n80 : E := ((1 : k) / (1 : k)) • n79
theorem value_80 : n80 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n80, value_79]
  have hs : ((1 : k) / (1 : k)) = (1 : k) := by
    apply (div_eq_iff (by decide +kernel : (1 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_80 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n80 = n80 := by
  unfold Preserves at hQ
  simp only [n80, map_smul, fixed_79 Q hQ hx hy]

theorem zero_80 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n80 = 0 := by
  unfold IsDerivation at hD
  simp only [n80, map_smul, zero_79 D hD hx hy, smul_zero]

def n81 : E := B n33 n55
theorem value_81 : n81 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 568, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n81, value_33, value_55]
  decide +kernel

theorem fixed_81 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n81 = n81 := by
  unfold Preserves at hQ
  simp only [n81, hQ, fixed_33 Q hQ hx hy, fixed_55 Q hQ hx hy]

theorem zero_81 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n81 = 0 := by
  unfold IsDerivation at hD
  simp only [n81, hD, zero_33 D hD hx hy, zero_55 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n82 : E := ((1 : k) / (8640 : k)) • n81
theorem value_82 : n82 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n82, value_81]
  have hs : ((1 : k) / (8640 : k)) = (723 : k) := by
    apply (div_eq_iff (by decide +kernel : (8640 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_82 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n82 = n82 := by
  unfold Preserves at hQ
  simp only [n82, map_smul, fixed_81 Q hQ hx hy]

theorem zero_82 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n82 = 0 := by
  unfold IsDerivation at hD
  simp only [n82, map_smul, zero_81 D hD hx hy, smul_zero]

def n83 : E := B n18 n82
theorem value_83 : n83 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n83, value_18, value_82]
  decide +kernel

theorem fixed_83 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n83 = n83 := by
  unfold Preserves at hQ
  simp only [n83, hQ, fixed_18 Q hQ hx hy, fixed_82 Q hQ hx hy]

theorem zero_83 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n83 = 0 := by
  unfold IsDerivation at hD
  simp only [n83, hD, zero_18 D hD hx hy, zero_82 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n84 : E := ((1 : k) / (2 : k)) • n83
theorem value_84 : n84 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0] := by
  rw [n84, value_83]
  have hs : ((1 : k) / (2 : k)) = (505 : k) := by
    apply (div_eq_iff (by decide +kernel : (2 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_84 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n84 = n84 := by
  unfold Preserves at hQ
  simp only [n84, map_smul, fixed_83 Q hQ hx hy]

theorem zero_84 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n84 = 0 := by
  unfold IsDerivation at hD
  simp only [n84, map_smul, zero_83 D hD hx hy, smul_zero]

def n85 : E := B n18 n84
theorem value_85 : n85 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0] := by
  rw [n85, value_18, value_84]
  decide +kernel

theorem fixed_85 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n85 = n85 := by
  unfold Preserves at hQ
  simp only [n85, hQ, fixed_18 Q hQ hx hy, fixed_84 Q hQ hx hy]

theorem zero_85 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n85 = 0 := by
  unfold IsDerivation at hD
  simp only [n85, hD, zero_18 D hD hx hy, zero_84 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n86 : E := B n47 n66
theorem value_86 : n86 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 576] := by
  rw [n86, value_47, value_66]
  decide +kernel

theorem fixed_86 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n86 = n86 := by
  unfold Preserves at hQ
  simp only [n86, hQ, fixed_47 Q hQ hx hy, fixed_66 Q hQ hx hy]

theorem zero_86 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n86 = 0 := by
  unfold IsDerivation at hD
  simp only [n86, hD, zero_47 D hD hx hy, zero_66 D hD hx hy, map_zero, LinearMap.zero_apply, add_zero]

def n87 : E := ((1 : k) / (576 : k)) • n86
theorem value_87 : n87 = ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] := by
  rw [n87, value_86]
  have hs : ((1 : k) / (576 : k)) = (755 : k) := by
    apply (div_eq_iff (by decide +kernel : (576 : k) ≠ 0)).2
    decide +kernel
  rw [hs]
  decide +kernel

theorem fixed_87 (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) : Q n87 = n87 := by
  unfold Preserves at hQ
  simp only [n87, map_smul, fixed_86 Q hQ hx hy]

theorem zero_87 (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) : D n87 = 0 := by
  unfold IsDerivation at hD
  simp only [n87, map_smul, zero_86 D hD hx hy, smul_zero]

theorem target_0 : n0 = (unitVec 0 : E) := by
  rw [value_0]
  decide +kernel

theorem target_1 : n11 = (unitVec 1 : E) := by
  rw [value_11]
  decide +kernel

theorem target_2 : n18 = (unitVec 2 : E) := by
  rw [value_18]
  decide +kernel

theorem target_3 : n33 = (unitVec 3 : E) := by
  rw [value_33]
  decide +kernel

theorem target_4 : n35 = (unitVec 4 : E) := by
  rw [value_35]
  decide +kernel

theorem target_5 : n37 = (unitVec 5 : E) := by
  rw [value_37]
  decide +kernel

theorem target_6 : n39 = (unitVec 6 : E) := by
  rw [value_39]
  decide +kernel

theorem target_7 : n41 = (unitVec 7 : E) := by
  rw [value_41]
  decide +kernel

theorem target_8 : n43 = (unitVec 8 : E) := by
  rw [value_43]
  decide +kernel

theorem target_9 : n45 = (unitVec 9 : E) := by
  rw [value_45]
  decide +kernel

theorem target_10 : n47 = (unitVec 10 : E) := by
  rw [value_47]
  decide +kernel

theorem target_11 : n49 = (unitVec 11 : E) := by
  rw [value_49]
  decide +kernel

theorem target_12 : n51 = (unitVec 12 : E) := by
  rw [value_51]
  decide +kernel

theorem target_13 : n53 = (unitVec 13 : E) := by
  rw [value_53]
  decide +kernel

theorem target_14 : n55 = (unitVec 14 : E) := by
  rw [value_55]
  decide +kernel

theorem target_15 : n68 = (unitVec 15 : E) := by
  rw [value_68]
  decide +kernel

theorem target_16 : n70 = (unitVec 16 : E) := by
  rw [value_70]
  decide +kernel

theorem target_17 : n72 = (unitVec 17 : E) := by
  rw [value_72]
  decide +kernel

theorem target_18 : n74 = (unitVec 18 : E) := by
  rw [value_74]
  decide +kernel

theorem target_19 : n76 = (unitVec 19 : E) := by
  rw [value_76]
  decide +kernel

theorem target_20 : n78 = (unitVec 20 : E) := by
  rw [value_78]
  decide +kernel

theorem target_21 : n80 = (unitVec 21 : E) := by
  rw [value_80]
  decide +kernel

theorem target_22 : n82 = (unitVec 22 : E) := by
  rw [value_82]
  decide +kernel

theorem target_23 : n84 = (unitVec 23 : E) := by
  rw [value_84]
  decide +kernel

theorem target_24 : n85 = (unitVec 24 : E) := by
  rw [value_85]
  decide +kernel

theorem target_25 : n58 = (unitVec 25 : E) := by
  rw [value_58]
  decide +kernel

theorem target_26 : n60 = (unitVec 26 : E) := by
  rw [value_60]
  decide +kernel

theorem target_27 : n62 = (unitVec 27 : E) := by
  rw [value_62]
  decide +kernel

theorem target_28 : n64 = (unitVec 28 : E) := by
  rw [value_64]
  decide +kernel

theorem target_29 : n66 = (unitVec 29 : E) := by
  rw [value_66]
  decide +kernel

theorem target_30 : n87 = (unitVec 30 : E) := by
  rw [value_87]
  decide +kernel

theorem fixed_basis (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) (i : I) : Q (unitVec i) = unitVec i := by
  fin_cases i
  · simpa only [target_0] using fixed_0 Q hQ hx hy
  · simpa only [target_1] using fixed_11 Q hQ hx hy
  · simpa only [target_2] using fixed_18 Q hQ hx hy
  · simpa only [target_3] using fixed_33 Q hQ hx hy
  · simpa only [target_4] using fixed_35 Q hQ hx hy
  · simpa only [target_5] using fixed_37 Q hQ hx hy
  · simpa only [target_6] using fixed_39 Q hQ hx hy
  · simpa only [target_7] using fixed_41 Q hQ hx hy
  · simpa only [target_8] using fixed_43 Q hQ hx hy
  · simpa only [target_9] using fixed_45 Q hQ hx hy
  · simpa only [target_10] using fixed_47 Q hQ hx hy
  · simpa only [target_11] using fixed_49 Q hQ hx hy
  · simpa only [target_12] using fixed_51 Q hQ hx hy
  · simpa only [target_13] using fixed_53 Q hQ hx hy
  · simpa only [target_14] using fixed_55 Q hQ hx hy
  · simpa only [target_15] using fixed_68 Q hQ hx hy
  · simpa only [target_16] using fixed_70 Q hQ hx hy
  · simpa only [target_17] using fixed_72 Q hQ hx hy
  · simpa only [target_18] using fixed_74 Q hQ hx hy
  · simpa only [target_19] using fixed_76 Q hQ hx hy
  · simpa only [target_20] using fixed_78 Q hQ hx hy
  · simpa only [target_21] using fixed_80 Q hQ hx hy
  · simpa only [target_22] using fixed_82 Q hQ hx hy
  · simpa only [target_23] using fixed_84 Q hQ hx hy
  · simpa only [target_24] using fixed_85 Q hQ hx hy
  · simpa only [target_25] using fixed_58 Q hQ hx hy
  · simpa only [target_26] using fixed_60 Q hQ hx hy
  · simpa only [target_27] using fixed_62 Q hQ hx hy
  · simpa only [target_28] using fixed_64 Q hQ hx hy
  · simpa only [target_29] using fixed_66 Q hQ hx hy
  · simpa only [target_30] using fixed_87 Q hQ hx hy

theorem zero_basis (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) (i : I) : D (unitVec i) = 0 := by
  fin_cases i
  · simpa only [target_0] using zero_0 D hD hx hy
  · simpa only [target_1] using zero_11 D hD hx hy
  · simpa only [target_2] using zero_18 D hD hx hy
  · simpa only [target_3] using zero_33 D hD hx hy
  · simpa only [target_4] using zero_35 D hD hx hy
  · simpa only [target_5] using zero_37 D hD hx hy
  · simpa only [target_6] using zero_39 D hD hx hy
  · simpa only [target_7] using zero_41 D hD hx hy
  · simpa only [target_8] using zero_43 D hD hx hy
  · simpa only [target_9] using zero_45 D hD hx hy
  · simpa only [target_10] using zero_47 D hD hx hy
  · simpa only [target_11] using zero_49 D hD hx hy
  · simpa only [target_12] using zero_51 D hD hx hy
  · simpa only [target_13] using zero_53 D hD hx hy
  · simpa only [target_14] using zero_55 D hD hx hy
  · simpa only [target_15] using zero_68 D hD hx hy
  · simpa only [target_16] using zero_70 D hD hx hy
  · simpa only [target_17] using zero_72 D hD hx hy
  · simpa only [target_18] using zero_74 D hD hx hy
  · simpa only [target_19] using zero_76 D hD hx hy
  · simpa only [target_20] using zero_78 D hD hx hy
  · simpa only [target_21] using zero_80 D hD hx hy
  · simpa only [target_22] using zero_82 D hD hx hy
  · simpa only [target_23] using zero_84 D hD hx hy
  · simpa only [target_24] using zero_85 D hD hx hy
  · simpa only [target_25] using zero_58 D hD hx hy
  · simpa only [target_26] using zero_60 D hD hx hy
  · simpa only [target_27] using zero_62 D hD hx hy
  · simpa only [target_28] using zero_64 D hD hx hy
  · simpa only [target_29] using zero_66 D hD hx hy
  · simpa only [target_30] using zero_87 D hD hx hy

/-- Every linear bracket-preserving map is determined by x,y; no bijectivity needed. -/
theorem fixed_all (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (hy : Q y = y) (a : E) : Q a = a := by
  rw [linear_apply Q a]
  simp only [fixed_basis Q hQ hx hy]
  exact (decompose a).symm

/-- Every derivation killing x,y vanishes. -/
theorem zero_all (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (hy : D y = 0) (a : E) : D a = 0 := by
  rw [linear_apply D a]
  simp only [zero_basis D hD hx hy, smul_zero, Finset.sum_const_zero]

end Kourovka.Flag.Generation
