import Bell.CircuitRealization
import Bell.FiniteLinearAlgebra

/-!
# Three-dimensional Lorentz compression and exact null splitting

A spatial unit normal orthogonal to both binary measurement spans defines a
positive compression that leaves their trace pairings unchanged. Each compressed
future vector splits into two future-null vectors in the same hyperplane.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder
namespace Bell.QubitGeometry
open Bell Lorentz

def dotLinear (n : V) : V →ₗ[ℝ] ℝ where
  toFun x := dotProduct n x
  map_add' := by intros; simp [dotProduct_add]
  map_smul' := by intros; simp [dotProduct_smul]

theorem dot_self_positive {x : V} (hx : x ≠ 0) : 0 < dotProduct x x := by
  have hn : 0 ≤ dotProduct x x := Finset.sum_nonneg (fun i _ => mul_self_nonneg (x i))
  exact lt_of_le_of_ne hn (fun h => hx (dotProduct_self_eq_zero.mp h.symm))

def normalizeVector (x : V) : V := (Real.sqrt (dotProduct x x))⁻¹ • x

theorem normalizeVector_unit {x : V} (hx : x ≠ 0) : dotProduct (normalizeVector x) (normalizeVector x)=1 := by
  have hp := dot_self_positive hx
  have hq := Real.sq_sqrt hp.le
  have hn := (Real.sqrt_pos.2 hp).ne'
  simp only [normalizeVector,smul_dotProduct,dotProduct_smul,smul_eq_mul]
  field_simp [hn]

theorem exists_unit_annihilator (H : Submodule ℝ V) (hH : Module.finrank ℝ H ≤ 3)
    (hu : timeUnit ∈ H) : ∃ n : V, n 0=0 ∧ dotProduct n n=1 ∧
      ∀ x ∈ H, dotProduct n x=0 := by
  classical
  have htop : H ≠ ⊤ := by
    intro h
    have hd := congrArg (fun S : Submodule ℝ V => Module.finrank ℝ S) h
    change Module.finrank ℝ H = Module.finrank ℝ (⊤ : Submodule ℝ V) at hd
    rw [finrank_top] at hd
    norm_num [V] at hd
    omega
  have hlt : H < (⊤ : Submodule ℝ V) := lt_top_iff_ne_top.mpr htop
  obtain ⟨x, _, hx⟩ := SetLike.exists_of_lt hlt
  obtain ⟨f,hfx,hfH⟩ := Submodule.exists_dual_map_eq_bot_of_nmem hx
    (inferInstance : Module.Free ℝ (V ⧸ H))
  let v : V := fun i => f (Pi.single i 1)
  have he : ∀ x, dotProduct v x=f x := fun x => (finite_functional_coordinates f x).symm
  have hfn : v ≠ 0 := by
    intro hz
    apply hfx
    rw [← he x,hz]
    simp [dotProduct]
  have hkill : ∀ y ∈ H, f y=0 := by
    intro y hy
    have hm : f y ∈ H.map f := ⟨y,hy,rfl⟩
    rw [hfH] at hm
    exact hm
  have hv0 : v 0=0 := by
    have ht := hkill timeUnit hu
    rw [← he] at ht
    simpa [timeUnit,dotProduct,Fin.sum_univ_succ] using ht
  refine ⟨normalizeVector v, ?_, normalizeVector_unit hfn, ?_⟩
  · simp [normalizeVector,hv0]
  · intro y hy
    simp [normalizeVector,smul_dotProduct,he,hkill y hy]

/-- Orthogonal compression onto the hyperplane normal to n. -/
def compress (n : V) : V →ₗ[ℝ] V where
  toFun x := x-dotProduct n x • n
  map_add' := by intros; simp [dotProduct_add,add_smul]; module
  map_smul' := by
    intro t x
    ext i
    simp [dotProduct_smul, Pi.smul_apply, smul_eq_mul]
    ring

theorem compress_time (n x : V) (hn0 : n 0=0) : compress n x 0=x 0 := by
  simp [compress,hn0]

theorem compress_orthogonal (n x : V) (hn : dotProduct n n=1) :
    dotProduct n (compress n x)=0 := by simp [compress,dotProduct_sub,dotProduct_smul,hn]

theorem compress_square (n x : V) (hn0 : n 0=0) (hn : dotProduct n n=1) :
    lorentzSquare (compress n x)=lorentzSquare x+(dotProduct n x)^2 := by
  have hn' := hn
  simp [dotProduct,Fin.sum_univ_succ,hn0] at hn'
  change lorentzSquare (x - dotProduct n x • n) = _
  simp [lorentzSquare, dotProduct, Fin.sum_univ_succ, hn0]
  linear_combination -(n 1*x 1+n 2*x 2+n 3*x 3)^2 * hn'

theorem compress_future (n : V) (hn0 : n 0=0) (hn : dotProduct n n=1)
    {x : V} (hx : Future x) : Future (compress n x) := by
  refine ⟨by simpa [compress_time n x hn0] using hx.1, ?_⟩
  rw [compress_square n x hn0 hn]
  exact add_nonneg hx.2 (sq_nonneg _)

theorem compress_pairing (n x y : V) (hny : dotProduct n y=0) :
    dotProduct y (compress n x)=dotProduct y x := by
  have hyn : dotProduct y n=0 := by simpa [dotProduct_comm] using hny
  simp [compress,dotProduct_sub,dotProduct_smul,hyn]

theorem normalHyperplane_dim_le_three (n : V) (hn : dotProduct n n=1) :
    Module.finrank ℝ (LinearMap.ker (dotLinear n)) ≤ 3 := by
  have hproper : LinearMap.ker (dotLinear n) ≠ ⊤ := by
    intro htop
    have hnmem : n ∈ LinearMap.ker (dotLinear n) := by rw [htop]; trivial
    change dotProduct n n=0 at hnmem
    linarith
  have hd := Submodule.finrank_lt hproper
  have hd' : Module.finrank ℝ (LinearMap.ker (dotLinear n)) < 4 := by simpa [V] using hd
  omega

theorem exists_spatial_unit_perpendicular (n : V) :
    ∃ d : V, d 0=0 ∧ dotProduct d d=1 ∧ dotProduct n d=0 := by
  let f : V →ₗ[ℝ] (Fin 2 → ℝ) :=
    { toFun x := ![x 0,dotProduct n x]
      map_add' := by intros; ext i; fin_cases i <;> simp [dotProduct_add]
      map_smul' := by intros; ext i; fin_cases i <;> simp [dotProduct_smul] }
  have hk : LinearMap.ker f ≠ ⊥ := LinearMap.ker_ne_bot_of_finrank_lt (by simp [V])
  obtain ⟨x,hx,hxn⟩ := (Submodule.ne_bot_iff _).mp hk
  have h0 := congrFun hx 0
  have h1 := congrFun hx 1
  change x 0=0 at h0
  change dotProduct n x=0 at h1
  refine ⟨normalizeVector x, by simp [normalizeVector,h0],normalizeVector_unit hxn, ?_⟩
  simp [normalizeVector,dotProduct_smul,h1]

def spatial (x : V) : V := ![0,x 1,x 2,x 3]
def radius (x : V) : ℝ := Real.sqrt (x 1^2+x 2^2+x 3^2)

theorem radius_nonnegative (x : V) : 0 ≤ radius x := Real.sqrt_nonneg _
theorem radius_square (x : V) : radius x^2=x 1^2+x 2^2+x 3^2 :=
  Real.sq_sqrt (by positivity)

theorem radius_le_time {x : V} (hx : Future x) : radius x ≤ x 0 := by
  have hr := radius_square x
  have hn := radius_nonnegative x
  have hq := hx.2
  unfold lorentzSquare at hq
  nlinarith [hx.1]

def splitDirection (d x : V) : V := if radius x=0 then d else (radius x)⁻¹ • spatial x

def nullPiece (d x : V) (k : Fin 2) : V :=
  ((x 0+ConeCircuits.sign k*radius x)/2) • (timeUnit+ConeCircuits.sign k • splitDirection d x)

theorem splitDirection_time (d x : V) (hd0 : d 0=0) : splitDirection d x 0=0 := by
  unfold splitDirection
  split_ifs <;> simp [spatial,hd0]

theorem splitDirection_unit (d x : V) (hdu : dotProduct d d=1) :
    dotProduct (splitDirection d x) (splitDirection d x)=1 := by
  unfold splitDirection
  split_ifs with hr
  · exact hdu
  · have hsq := radius_square x
    simp [Matrix.cons_val, smul_dotProduct,dotProduct_smul,smul_eq_mul,spatial,dotProduct,Fin.sum_univ_succ]
    field_simp [hr]
    nlinarith

theorem radius_direction (d x : V) : radius x • splitDirection d x=spatial x := by
  by_cases hr : radius x=0
  · have hsq := radius_square x
    rw [hr] at hsq
    have h1 : x 1=0 := by nlinarith [sq_nonneg (x 2),sq_nonneg (x 3)]
    have h2 : x 2=0 := by nlinarith [sq_nonneg (x 1),sq_nonneg (x 3)]
    have h3 : x 3=0 := by nlinarith [sq_nonneg (x 1),sq_nonneg (x 2)]
    ext i
    fin_cases i <;> simp [Matrix.cons_val, hr,spatial,h1,h2,h3]
  · simp [splitDirection,hr,smul_smul]

theorem nullPiece_sum (d x : V) : (∑ k : Fin 2, nullPiece d x k)=x := by
  have hd := radius_direction d x
  calc
    (∑ k : Fin 2, nullPiece d x k) =
        ((x 0+radius x)/2) • (timeUnit+splitDirection d x)+
        ((x 0-radius x)/2) • (timeUnit-splitDirection d x) := by
      simp [Fin.sum_univ_two, nullPiece, ConeCircuits.sign, sub_eq_add_neg]
    _ = x 0 • timeUnit+radius x • splitDirection d x := by module
    _ = x := by
      rw [hd]
      ext i
      fin_cases i <;> simp [Matrix.cons_val, timeUnit,spatial]

theorem nullPiece_null_or_zero (d : V) (hd0 : d 0=0) (hdu : dotProduct d d=1)
    {x : V} (hx : Future x) (k : Fin 2) : nullPiece d x k=0 ∨ FutureNull (nullPiece d x k) := by
  let u := splitDirection d x
  have hu0 : u 0 = 0 := splitDirection_time d x hd0
  have huu : dotProduct u u = 1 := splitDirection_unit d x hdu
  have hq : ∀ k : Fin 2, lorentzSquare (timeUnit+ConeCircuits.sign k • u)=0 := by
    intro k
    have he := huu
    simp [dotProduct,Fin.sum_univ_succ,hu0] at he
    fin_cases k <;>
      simp [Matrix.cons_val, hu0,lorentzSquare,timeUnit,ConeCircuits.sign] <;> nlinarith [he]
  let t := (x 0+ConeCircuits.sign k*radius x)/2
  have ht : 0 ≤ t := by
    have hr := radius_le_time hx
    have hn := radius_nonnegative x
    fin_cases k <;> simp [t,ConeCircuits.sign] <;> linarith [hx.1]
  by_cases ht0 : t=0
  · exact Or.inl (by change t • _ = 0; rw [ht0, zero_smul])
  · right
    refine ⟨?_, ?_⟩
    · have htp : 0<t := lt_of_le_of_ne ht (Ne.symm ht0)
      change 0 < (t • (timeUnit + ConeCircuits.sign k • u)) 0
      simpa only [Pi.smul_apply, Pi.add_apply, smul_eq_mul, hu0, mul_zero, add_zero, timeUnit, Matrix.cons_val_zero, mul_one] using htp
    · have he := hq k
      change lorentzSquare (t • (timeUnit+ConeCircuits.sign k • u))=0
      have hs : ∀ y : V, lorentzSquare (t • y)=t^2*lorentzSquare y := by
        intro y; simp [lorentzSquare,mul_pow]; ring
      rw [hs,he,mul_zero]

theorem nullPiece_in_plane (n d x : V) (hn0 : n 0=0)
    (hnd : dotProduct n d=0) (hnx : dotProduct n x=0) (k : Fin 2) :
    dotProduct n (nullPiece d x k)=0 := by
  have hs : dotProduct n (spatial x)=0 := by
    simpa [spatial,dotProduct,Fin.sum_univ_succ,hn0] using hnx
  have hu : dotProduct n (splitDirection d x)=0 := by
    unfold splitDirection
    split_ifs <;> simp [hnd,dotProduct_smul,hs]
  have htime : dotProduct n timeUnit = 0 := by simp [Matrix.cons_val, timeUnit,dotProduct,Fin.sum_univ_succ,hn0]
  simp only [nullPiece,dotProduct_smul,dotProduct_add,hu,htime,smul_eq_mul,mul_zero,add_zero]

end Bell.QubitGeometry
