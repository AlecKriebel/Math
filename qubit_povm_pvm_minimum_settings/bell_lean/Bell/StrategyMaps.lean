import Bell.SteeringRepresentation

/-! # Physical maps of complete strategies

Input selection/permutation and arbitrary deterministic output postprocessing
act linearly on behaviors and preserve both actual quantum strategy classes.
Outcome maps need not be bijections: merging and zero-padding are included.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder
namespace Bell

def coarsenPOVM {n m : ℕ} (N : POVM n) (f : Fin n → Fin m) : POVM m where
  effect b := ∑ a, if f a=b then N.effect a else 0
  positive b := positive_sum _ fun a => by
    split_ifs
    · exact N.positive a
    · exact Matrix.PosSemidef.zero
  normalized := by
    rw [Finset.sum_comm]
    simpa using N.normalized

private theorem coarsen_product {n m : ℕ} (N : PVM n) (f : Fin n → Fin m) (b c : Fin m) :
    (coarsenPOVM N.toPOVM f).effect b * (coarsenPOVM N.toPOVM f).effect c =
      if b=c then (coarsenPOVM N.toPOVM f).effect b else 0 := by
  classical
  change (∑ a, if f a=b then N.effect a else 0) *
      (∑ a, if f a=c then N.effect a else 0) = _
  rw [Matrix.sum_mul]
  have hi (a : Fin n) :
      (if f a=b then N.effect a else 0) * (∑ a', if f a'=c then N.effect a' else 0) =
        if f a=b ∧ f a=c then N.effect a else 0 := by
    rw [Matrix.mul_sum]
    rw [Finset.sum_eq_single a]
    · by_cases hb : f a=b <;> by_cases hc : f a=c <;>
        simp [hb,hc,N.idempotent a]
    · intro a' _ hne
      by_cases hb : f a=b <;> by_cases hc : f a'=c <;>
        simp [hb,hc,N.orthogonal a a' (Ne.symm hne)]
    · simp
  simp_rw [hi]
  by_cases hbc : b=c
  · subst c
    simp [coarsenPOVM]
  · simp [hbc, show ∀ a, ¬(f a=b ∧ f a=c) from fun a h => hbc (h.1.symm.trans h.2)]

def coarsenPVM {n m : ℕ} (N : PVM n) (f : Fin n → Fin m) : PVM m where
  toPOVM := coarsenPOVM N.toPOVM f
  idempotent b := by simpa using coarsen_product N f b b
  orthogonal b c hbc := by simpa [hbc] using coarsen_product N f b c

structure StrategyMap (A B : Architecture) where
  aliceInput : Fin B.aliceInputs → Fin A.aliceInputs
  bobInput : Fin B.bobInputs → Fin A.bobInputs
  aliceOutput : (x : Fin B.aliceInputs) → Fin (A.aliceOutputs (aliceInput x)) → Fin (B.aliceOutputs x)
  bobOutput : (y : Fin B.bobInputs) → Fin (A.bobOutputs (bobInput y)) → Fin (B.bobOutputs y)

namespace StrategyMap
variable {A B : Architecture} (T : StrategyMap A B)

def behavior : Behavior A →ₗ[ℝ] Behavior B where
  toFun p x y a b := ∑ c, ∑ d,
    if T.aliceOutput x c=a ∧ T.bobOutput y d=b then p (T.aliceInput x) (T.bobInput y) c d else 0
  map_add' := by
    intro p q
    funext x y a b
    simp only [Pi.add_apply, Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro c _
    apply Finset.sum_congr rfl
    intro d _
    split_ifs <;> simp
  map_smul' := by
    intro t p
    funext x y a b
    simp only [Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro c _
    apply Finset.sum_congr rfl
    intro d _
    split_ifs <;> simp

def strategy (s : Strategy A) : Strategy B where
  state := s.state
  alice x := coarsenPOVM (s.alice (T.aliceInput x)) (T.aliceOutput x)
  bob y := coarsenPOVM (s.bob (T.bobInput y)) (T.bobOutput y)

def projectiveStrategy (s : ProjectiveStrategy A) : ProjectiveStrategy B where
  state := s.state
  alice x := coarsenPVM (s.alice (T.aliceInput x)) (T.aliceOutput x)
  bob y := coarsenPVM (s.bob (T.bobInput y)) (T.bobOutput y)

theorem strategy_behavior (s : Strategy A) : (T.strategy s).behavior = T.behavior s.behavior := by
  funext x y a b
  simp only [strategy, Strategy.behavior, coarsenPOVM, born,
    tensor_sum_left, tensor_sum_right, Matrix.mul_sum, Matrix.trace_sum, Complex.re_sum]
  change (∑ c, ∑ d, born s.state.density
    (if T.aliceOutput x c=a then (s.alice (T.aliceInput x)).effect c else 0)
    (if T.bobOutput y d=b then (s.bob (T.bobInput y)).effect d else 0)) = _
  apply Finset.sum_congr rfl
  intro c _
  apply Finset.sum_congr rfl
  intro d _
  by_cases hc : T.aliceOutput x c=a <;> by_cases hd : T.bobOutput y d=b <;>
    simp [hc,hd,behavior,Strategy.behavior,born,tensor_zero_left,tensor_zero_right]

theorem mem_rawPOVM {p : Behavior A} (hp : p ∈ rawPOVM A) : T.behavior p ∈ rawPOVM B := by
  obtain ⟨s,rfl⟩ := hp
  exact ⟨T.strategy s,T.strategy_behavior s⟩

theorem mem_rawPVM {p : Behavior A} (hp : p ∈ rawPVM A) : T.behavior p ∈ rawPVM B := by
  obtain ⟨s,rfl⟩ := hp
  exact ⟨T.projectiveStrategy s,T.strategy_behavior s.toStrategy⟩

theorem mem_convexPVM {p : Behavior A} (hp : p ∈ convexPVM A) : T.behavior p ∈ convexPVM B := by
  have hc : Convex ℝ {p | T.behavior p ∈ convexPVM B} := by
    intro p hp q hq a b ha hb hab
    change T.behavior (a • p+b • q) ∈ convexPVM B
    rw [map_add,map_smul,map_smul]
    exact (convex_convexHull ℝ (rawPVM B)) hp hq ha hb hab
  exact (convexHull_min (fun p hp => subset_convexHull ℝ (rawPVM B) (T.mem_rawPVM hp)) hc) hp

end StrategyMap

def swappedArchitecture (A : Architecture) : Architecture :=
  ⟨A.bobInputs,A.aliceInputs,A.bobOutputs,A.aliceOutputs⟩

def swapBehavior (A : Architecture) : Behavior A →ₗ[ℝ] Behavior (swappedArchitecture A) where
  toFun p x y a b := p y x b a
  map_add' := by intros; rfl
  map_smul' := by intros; rfl

def swapState (ρ : State) : State where
  density := ρ.density.submatrix Prod.swap Prod.swap
  positive := ρ.positive.submatrix Prod.swap
  normalized := by
    change (∑ i : Joint, ρ.density i.swap i.swap) = 1
    rw [Equiv.sum_comp (Equiv.prodComm Qubit Qubit) (fun i => ρ.density i i)]
    exact ρ.normalized

def swapStrategy {A : Architecture} (s : Strategy A) : Strategy (swappedArchitecture A) where
  state := swapState s.state
  alice := s.bob
  bob := s.alice

theorem swap_born (ρ : JointOperator) (M N : Operator) :
    born (ρ.submatrix Prod.swap Prod.swap) N M = born ρ M N := by
  simp [born,tensor,Matrix.trace,Matrix.mul_apply,Fintype.sum_prod_type,
    Fin.sum_univ_succ,Matrix.submatrix_apply]
  ring

theorem swapStrategy_behavior {A : Architecture} (s : Strategy A) :
    (swapStrategy s).behavior = swapBehavior A s.behavior := by
  funext x y a b
  exact swap_born _ _ _

def swapProjectiveStrategy {A : Architecture} (s : ProjectiveStrategy A) :
    ProjectiveStrategy (swappedArchitecture A) where
  state := swapState s.state
  alice := s.bob
  bob := s.alice

theorem swap_mem_convexPVM {A : Architecture} {p : Behavior A} (hp : p ∈ convexPVM A) :
    swapBehavior A p ∈ convexPVM (swappedArchitecture A) := by
  have hs : rawPVM A ⊆ {p | swapBehavior A p ∈ convexPVM (swappedArchitecture A)} := by
    rintro p ⟨s,rfl⟩
    exact subset_convexHull ℝ _ ⟨swapProjectiveStrategy s,swapStrategy_behavior s.toStrategy⟩
  apply (convexHull_min hs ?_) hp
  intro p hp q hq a b ha hb hab
  change swapBehavior A (a • p+b • q) ∈ _
  rw [map_add,map_smul,map_smul]
  exact (convex_convexHull ℝ _) hp hq ha hb hab

theorem swap_mem_convexPOVM {A : Architecture} {p : Behavior A} (hp : p ∈ convexPOVM A) :
    swapBehavior A p ∈ convexPOVM (swappedArchitecture A) := by
  have hs : rawPOVM A ⊆ {p | swapBehavior A p ∈ convexPOVM (swappedArchitecture A)} := by
    rintro p ⟨s,rfl⟩
    exact subset_convexHull ℝ _ ⟨swapStrategy s,swapStrategy_behavior s⟩
  apply (convexHull_min hs ?_) hp
  intro p hp q hq a b ha hb hab
  change swapBehavior A (a • p+b • q) ∈ _
  rw [map_add,map_smul,map_smul]
  exact (convex_convexHull ℝ _) hp hq ha hb hab

theorem swap_extreme {A : Architecture} {p : Behavior A}
    (hp : p ∈ Set.extremePoints ℝ (convexPOVM A)) :
    swapBehavior A p ∈ Set.extremePoints ℝ (convexPOVM (swappedArchitecture A)) := by
  refine ⟨swap_mem_convexPOVM hp.1, ?_⟩
  intro q hq r hr hseg
  obtain ⟨a,b,ha,hb,hab,he⟩ := hseg
  have hs := hp.2 (swap_mem_convexPOVM hq) (swap_mem_convexPOVM hr)
    ⟨a,b,ha,hb,hab,by
      have h := congrArg (swapBehavior (swappedArchitecture A)) he
      simpa only [map_add,map_smul,swapBehavior] using h⟩
  constructor
  · funext x y u v
    exact congrFun (congrFun (congrFun (congrFun hs.1 y) x) v) u
  · funext x y u v
    exact congrFun (congrFun (congrFun (congrFun hs.2 y) x) v) u

def FullPureStrategy.swap {A : Architecture} (s : FullPureStrategy A) :
    FullPureStrategy (swappedArchitecture A) where
  coefficient := s.coefficient.transpose
  coefficient_invertible := by simpa using s.coefficient_invertible
  normalized := by
    rw [← pureDensity_trace]
    have he : pureDensity s.coefficient.transpose =
        (pureDensity s.coefficient).submatrix Prod.swap Prod.swap := rfl
    rw [he]
    exact (swapState (pureState s.coefficient s.normalized)).normalized
  alice := s.bob
  bob := s.alice

theorem FullPureStrategy.swap_behavior {A : Architecture} (s : FullPureStrategy A) :
    s.swap.behavior = swapBehavior A s.behavior := swapStrategy_behavior s.toStrategy

end Bell
