/- Exact left-inverse witness for thirty independent inner-derivation columns.
The data below are witnesses; their equation against the actual scaled bracket is proved by reduction. -/
import Kourovka.Certificates.DerivationMatrix
import Kourovka.Ambient.FastBasis
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.LinearAlgebra.Dimension.Constructions

set_option Elab.async false
set_option maxHeartbeats 50000000
set_option maxRecDepth 200000

namespace Kourovka.Certificates.InnerRank
open Kourovka.Linear Kourovka.Ambient Kourovka.Lattice
open scoped BigOperators

abbrev Param := Fin 30

def selectedRow : Param → Col := ![(0,1), (0,3), (1,1), (2,0), (2,1), (4,1), (5,1), (6,1), (7,1), (8,1), (10,0), (10,1), (11,1), (12,1), (13,1), (15,0), (15,1), (16,1), (17,1), (18,1), (19,1), (20,1), (22,0), (22,1), (22,2), (22,4), (22,5), (22,6), (22,7), (23,1)]

def inverseCoeff (i j : Param) : Rat :=
  match i.val,j.val with
  | 0, 2 => (1/2036162)
  | 1, 1 => (1/1036488922561)
  | 2, 3 => (-1/6108486)
  | 3, 0 => (-1/1036488922561)
  | 4, 4 => (-1/1027243729)
  | 5, 2 => (1/2072977845122)
  | 5, 3 => (1/2054487458)
  | 5, 5 => (-1/2036162)
  | 6, 0 => (-5/3109466767683)
  | 6, 4 => (5/3081731187)
  | 6, 6 => (-1/3054243)
  | 7, 2 => (-1/2072977845122)
  | 7, 3 => (-1/2054487458)
  | 7, 5 => (1/2036162)
  | 7, 7 => (-1/4072324)
  | 8, 0 => (1/1036488922561)
  | 8, 4 => (-1/1027243729)
  | 8, 6 => (1/5090405)
  | 8, 8 => (-1/5090405)
  | 9, 2 => (1/6218933535366)
  | 9, 3 => (1/6163462374)
  | 9, 5 => (-1/6108486)
  | 9, 7 => (1/12216972)
  | 9, 9 => (-1/6108486)
  | 10, 1 => (-1/2110459357539650882)
  | 10, 10 => (-1/4072324)
  | 11, 2 => (1/1036488922561)
  | 11, 11 => (-1/1018081)
  | 12, 0 => (-2/1036488922561)
  | 12, 1 => (1/1055229678769825441)
  | 12, 10 => (1/2036162)
  | 12, 12 => (-1/2036162)
  | 13, 2 => (-1/1036488922561)
  | 13, 11 => (1/1018081)
  | 13, 13 => (-1/3054243)
  | 14, 0 => (1/1036488922561)
  | 14, 1 => (-1/2110459357539650882)
  | 14, 10 => (-1/4072324)
  | 14, 12 => (1/4072324)
  | 14, 14 => (-1/4072324)
  | 15, 15 => (-1/6108486)
  | 16, 2 => (240/1036488922561)
  | 16, 3 => (240/1027243729)
  | 16, 5 => (-240/1018081)
  | 16, 16 => (-1/1018081)
  | 17, 0 => (-600/1036488922561)
  | 17, 4 => (600/1027243729)
  | 17, 6 => (-120/1018081)
  | 17, 15 => (1/2036162)
  | 17, 17 => (-1/2036162)
  | 18, 2 => (-400/1036488922561)
  | 18, 3 => (-400/1027243729)
  | 18, 5 => (400/1018081)
  | 18, 16 => (5/3054243)
  | 18, 18 => (-1/3054243)
  | 19, 8 => (120/1018081)
  | 19, 15 => (-1/2036162)
  | 19, 17 => (1/2036162)
  | 19, 19 => (-1/4072324)
  | 20, 7 => (-120/1018081)
  | 20, 9 => (240/1018081)
  | 20, 16 => (-1/1018081)
  | 20, 18 => (1/5090405)
  | 20, 20 => (-1/5090405)
  | 21, 8 => (-40/1018081)
  | 21, 15 => (1/6108486)
  | 21, 17 => (-1/6108486)
  | 21, 19 => (1/12216972)
  | 21, 21 => (-1/6108486)
  | 22, 22 => (-1/2036162)
  | 23, 0 => (-1728000/1036488922561)
  | 23, 2 => (216/1036488922561)
  | 23, 4 => (1728000/1027243729)
  | 23, 6 => (-345600/1018081)
  | 23, 7 => (-144/1018081)
  | 23, 11 => (-216/1018081)
  | 23, 13 => (48/1018081)
  | 23, 15 => (1440/1018081)
  | 23, 17 => (-1440/1018081)
  | 23, 23 => (-1/1018081)
  | 23, 25 => (1/1036488922561)
  | 23, 27 => (-1/6218933535366)
  | 24, 0 => (432/1036488922561)
  | 24, 1 => (144/1055229678769825441)
  | 24, 4 => (-720/1027243729)
  | 24, 6 => (144/1018081)
  | 24, 7 => (-5184000/1018081)
  | 24, 8 => (-288/1018081)
  | 24, 9 => (10368000/1018081)
  | 24, 10 => (72/1018081)
  | 24, 12 => (-72/1018081)
  | 24, 14 => (72/1018081)
  | 24, 16 => (-43200/1018081)
  | 24, 18 => (8640/1018081)
  | 24, 20 => (-8640/1018081)
  | 24, 22 => (1/2036162)
  | 24, 24 => (1/6163462374)
  | 24, 29 => (-1/2036162)
  | 25, 1 => (-1/2110459357539650882)
  | 25, 2 => (-12000/1036488922561)
  | 25, 3 => (-12000/1027243729)
  | 25, 5 => (12000/1018081)
  | 25, 10 => (1/4072324)
  | 25, 16 => (50/1018081)
  | 25, 28 => (-1/597017619395136)
  | 26, 0 => (24000/1036488922561)
  | 26, 2 => (-1/1036488922561)
  | 26, 4 => (-24000/1027243729)
  | 26, 6 => (4800/1018081)
  | 26, 11 => (1/1018081)
  | 26, 15 => (-20/1018081)
  | 26, 17 => (20/1018081)
  | 26, 27 => (1/447763214546352)
  | 27, 0 => (2/1036488922561)
  | 27, 1 => (-2/1055229678769825441)
  | 27, 2 => (12000/1036488922561)
  | 27, 3 => (12000/1027243729)
  | 27, 5 => (-12000/1018081)
  | 27, 10 => (-1/2036162)
  | 27, 12 => (1/2036162)
  | 27, 16 => (-50/1018081)
  | 27, 18 => (10/1018081)
  | 27, 26 => (-1/597017619395136)
  | 28, 2 => (1/1036488922561)
  | 28, 8 => (-2400/1018081)
  | 28, 11 => (-1/1018081)
  | 28, 13 => (1/3054243)
  | 28, 15 => (10/1018081)
  | 28, 17 => (-10/1018081)
  | 28, 19 => (5/1018081)
  | 28, 25 => (1/1492544048487840)
  | 29, 0 => (-1/1036488922561)
  | 29, 1 => (1/2110459357539650882)
  | 29, 7 => (1200/1018081)
  | 29, 9 => (-2400/1018081)
  | 29, 10 => (1/4072324)
  | 29, 12 => (-1/4072324)
  | 29, 14 => (1/4072324)
  | 29, 16 => (10/1018081)
  | 29, 18 => (-2/1018081)
  | 29, 20 => (2/1018081)
  | 29, 24 => (-1/8875385818560)
  | _,_ => 0

/-- Actual inner derivation column, directly in the ell-basis. -/
def innerColumn {R : Type*} [CommRing R] (i : Param) : V R →ₗ[R] V R :=
  LB (unitVec (Fin.castLE (by decide : 30 ≤ 31) i))

/-- Compute the actual rational inner-column entry through the proved integer evaluator. -/
theorem inner_entry_fast (j : Param) (c : Col) :
    toEntries (innerColumn (R:=Rat) j) c =
      (FastBasis.coeff scaledTerms (Fin.castLE (by decide : 30 ≤ 31) j) c.2 c.1 : Int) := by
  exact FastBasis.cast_fromTerms_sound scaledTerms _ _ _

def innerMap {R : Type*} [CommRing R] : (Param → R) →ₗ[R] (V R →ₗ[R] V R) where
  toFun a := ∑ i, a i • innerColumn i
  map_add' := by intro a b; simp [add_smul,Finset.sum_add_distrib]
  map_smul' := by intro c a; simp [Pi.smul_apply,smul_smul,smul_eq_mul,Finset.smul_sum]

@[simp] theorem innerMap_unit {R : Type*} [CommRing R] (j : Param) :
    innerMap (unitVec j : Param → R) = innerColumn j := by
  simp [innerMap, unitVec]

/-- The extractor is only used over Rat, where its explicit nonzero denominators are legitimate. -/
def extractor : (V Rat →ₗ[Rat] V Rat) →ₗ[Rat] (Param → Rat) where
  toFun D := fun i => ∑ j, inverseCoeff i j * toEntries D (selectedRow j)
  map_add' := by
    intro D E; funext i
    simp [mul_add,Finset.sum_add_distrib]
  map_smul' := by
    intro c D; funext i
    simp only [map_smul,Pi.smul_apply,smul_eq_mul,Finset.mul_sum,RingHom.id_apply]
    apply Finset.sum_congr rfl
    intro j hj
    ring

def LeftInverseCheck (i : Param) : Prop :=
  ∀ j : Param, (∑ t : Param, inverseCoeff i t *
    (toEntries (innerColumn (R:=Rat) j)) (selectedRow t)) = if i=j then 1 else 0

instance (i : Param) : Decidable (LeftInverseCheck i) := by
  unfold LeftInverseCheck
  infer_instance

end Kourovka.Certificates.InnerRank
