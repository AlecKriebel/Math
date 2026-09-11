import Bell.Quantum

/-!
# Relabeling complete physical strategies

A relabeling is a bijection of the *declared* output alphabet for each input.
This includes unused (zero-projector) labels. It acts on a whole strategy at
once and preserves the same finite convex hull, without changing local dimension.

STATUS: uncompiled proof source.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace Bell

abbrev OutputRelabeling (A : Architecture) :=
  ((x : Fin A.aliceInputs) → Equiv.Perm (Fin (A.aliceOutputs x))) ×
  ((y : Fin A.bobInputs) → Equiv.Perm (Fin (A.bobOutputs y)))

def relabelPOVM {n : ℕ} (M : POVM n) (π : Equiv.Perm (Fin n)) : POVM n where
  effect := fun a => M.effect (π a)
  positive := fun a => M.positive (π a)
  normalized := by
    rw [Equiv.sum_comp π M.effect]
    exact M.normalized

def relabelPVM {n : ℕ} (M : PVM n) (π : Equiv.Perm (Fin n)) : PVM n where
  toPOVM := relabelPOVM M.toPOVM π
  idempotent := fun a => M.idempotent (π a)
  orthogonal := fun a b hab => M.orthogonal (π a) (π b) (fun h => hab (π.injective h))

def relabelBehavior {A : Architecture} (π : OutputRelabeling A) :
    Behavior A →ₗ[ℝ] Behavior A where
  toFun := fun p x y a b => p x y (π.1 x a) (π.2 y b)
  map_add' := by intros; rfl
  map_smul' := by intros; rfl

def relabelProjectiveStrategy {A : Architecture} (π : OutputRelabeling A)
    (s : ProjectiveStrategy A) : ProjectiveStrategy A where
  state := s.state
  alice := fun x => relabelPVM (s.alice x) (π.1 x)
  bob := fun y => relabelPVM (s.bob y) (π.2 y)

theorem relabelProjectiveStrategy_behavior {A : Architecture} (π : OutputRelabeling A)
    (s : ProjectiveStrategy A) :
    (relabelProjectiveStrategy π s).toStrategy.behavior =
      relabelBehavior π s.toStrategy.behavior := rfl

theorem relabel_mem_rawPVM {A : Architecture} (π : OutputRelabeling A)
    (p : Behavior A) (hp : p ∈ rawPVM A) : relabelBehavior π p ∈ rawPVM A := by
  obtain ⟨s,rfl⟩ := hp
  exact ⟨relabelProjectiveStrategy π s, relabelProjectiveStrategy_behavior π s⟩

/-- The proof uses the preimage of the actual convex hull, not an assumed
invariance of an abstract simulator set. -/
theorem relabel_mem_convexPVM {A : Architecture} (π : OutputRelabeling A)
    (p : Behavior A) (hp : p ∈ convexPVM A) : relabelBehavior π p ∈ convexPVM A := by
  have hc : Convex ℝ {p : Behavior A | relabelBehavior π p ∈ convexPVM A} := by
    intro p hp q hq a b ha hb hab
    change relabelBehavior π (a • p + b • q) ∈ convexPVM A
    rw [map_add, map_smul, map_smul]
    exact (convex_convexHull ℝ (rawPVM A)) hp hq ha hb hab
  have hs : rawPVM A ⊆ {p : Behavior A | relabelBehavior π p ∈ convexPVM A} := by
    intro p hp
    exact subset_convexHull ℝ (rawPVM A) (relabel_mem_rawPVM π p hp)
  exact (convexHull_min hs hc) hp

end Bell
