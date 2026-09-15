import Mathlib

/-! Limits of uniformly bounded complex families along genuine ultrafilters.
Compactness of closed complex balls proves convergence. Every subsequent law
uses that convergence and Hausdorff uniqueness, rather than a limit axiom.
The natural ultrafilter extends atTop, so ordinary convergent sequences retain
their limits. This is infrastructure for moment-limit / GNS reconstruction.
-/
noncomputable section
open scoped BigOperators Topology ComplexOrder
open Filter
namespace CyclicBell.General.Coverage

variable {ι J : Type*}

/-- An actual uniform norm bound, with no convergence premise. -/
def BoundedFamily (f : ι → ℂ) : Prop := ∃ M : ℝ, ∀ i, ‖f i‖≤M

namespace BoundedFamily

theorem const (z : ℂ) : BoundedFamily (fun _ : ι => z) := ⟨‖z‖,fun _ => le_rfl⟩

theorem add {f g : ι → ℂ} (hf : BoundedFamily f) (hg : BoundedFamily g) :
    BoundedFamily (fun i => f i+g i) := by
  obtain ⟨M,hM⟩ := hf
  obtain ⟨N,hN⟩ := hg
  exact ⟨M+N,fun i => (norm_add_le _ _).trans (add_le_add (hM i) (hN i))⟩

theorem neg {f : ι → ℂ} (hf : BoundedFamily f) : BoundedFamily (fun i => -f i) := by
  obtain ⟨M,hM⟩ := hf
  exact ⟨M,fun i => by simpa only [norm_neg] using hM i⟩

theorem sub {f g : ι → ℂ} (hf : BoundedFamily f) (hg : BoundedFamily g) :
    BoundedFamily (fun i => f i-g i) := by simpa only [sub_eq_add_neg] using hf.add hg.neg

theorem mul {f g : ι → ℂ} (hf : BoundedFamily f) (hg : BoundedFamily g) :
    BoundedFamily (fun i => f i*g i) := by
  obtain ⟨M,hM⟩ := hf
  obtain ⟨N,hN⟩ := hg
  refine ⟨M*N,fun i => ?_⟩
  rw [norm_mul]
  exact mul_le_mul (hM i) (hN i) (norm_nonneg _) ((norm_nonneg _).trans (hM i))

theorem smul (z : ℂ) {f : ι → ℂ} (hf : BoundedFamily f) :
    BoundedFamily (fun i => z*f i) := (const z).mul hf

theorem star {f : ι → ℂ} (hf : BoundedFamily f) : BoundedFamily (fun i => star (f i)) := by
  obtain ⟨M,hM⟩ := hf
  exact ⟨M,fun i => by simpa only [norm_star] using hM i⟩

theorem sum (s : Finset J) (f : J → ι → ℂ) (hf : ∀ j,BoundedFamily (f j)) :
    BoundedFamily (fun i => ∑ j ∈ s,f j i) := by
  classical
  choose M hM using hf
  refine ⟨∑ j ∈ s,M j,fun i => ?_⟩
  exact (norm_sum_le _ _).trans (Finset.sum_le_sum (fun j _ => hM j i))

end BoundedFamily

/-- This definition alone makes no claim for unbounded families. -/
def ultraLimit (U : Ultrafilter ι) (f : ι → ℂ) : ℂ := limUnder (U : Filter ι) f

/-- An ultrafilter whose image lies eventually in a compact ball converges. -/
theorem exists_ultra_tendsto_of_eventually_bounded (U : Ultrafilter ι) (f : ι → ℂ)
    (hf : ∃ M : ℝ, ∀ᶠ i in (U : Filter ι), ‖f i‖≤M) :
    ∃ z : ℂ,Tendsto f (U : Filter ι) (𝓝 z) := by
  obtain ⟨M,hM⟩ := hf
  have hmem : Metric.closedBall (0 : ℂ) M ∈ U.map f := by
    change ∀ᶠ i in (U : Filter ι), f i ∈ Metric.closedBall (0 : ℂ) M
    simpa only [Metric.mem_closedBall,dist_zero_right] using hM
  obtain ⟨z,_,hz⟩ := (isCompact_closedBall (0 : ℂ) M).ultrafilter_le_nhds' (U.map f) hmem
  exact ⟨z,hz⟩

theorem ultraLimit_tendsto (U : Ultrafilter ι) (f : ι → ℂ) (hf : BoundedFamily f) :
    Tendsto f (U : Filter ι) (𝓝 (ultraLimit U f)) := by
  obtain ⟨M,hM⟩ := hf
  exact tendsto_nhds_limUnder (exists_ultra_tendsto_of_eventually_bounded U f
    ⟨M,Eventually.of_forall hM⟩)

theorem ultraLimit_eq_of_tendsto (U : Ultrafilter ι) (f : ι → ℂ) {z : ℂ}
    (hf : Tendsto f (U : Filter ι) (𝓝 z)) : ultraLimit U f=z := hf.limUnder_eq

@[simp] theorem ultraLimit_const (U : Ultrafilter ι) (z : ℂ) :
    ultraLimit U (fun _ => z)=z := ultraLimit_eq_of_tendsto U _ tendsto_const_nhds

theorem ultraLimit_congr (U : Ultrafilter ι) (f g : ι → ℂ) (hf : BoundedFamily f)
    (hfg : f =ᶠ[U] g) : ultraLimit U f=ultraLimit U g := by
  symm
  exact ultraLimit_eq_of_tendsto U g ((ultraLimit_tendsto U f hf).congr' hfg)

theorem ultraLimit_add (U : Ultrafilter ι) (f g : ι → ℂ)
    (hf : BoundedFamily f) (hg : BoundedFamily g) :
    ultraLimit U (fun i => f i+g i)=ultraLimit U f+ultraLimit U g :=
  ultraLimit_eq_of_tendsto U _ ((ultraLimit_tendsto U f hf).add (ultraLimit_tendsto U g hg))

theorem ultraLimit_neg (U : Ultrafilter ι) (f : ι → ℂ) (hf : BoundedFamily f) :
    ultraLimit U (fun i => -f i) = -ultraLimit U f :=
  ultraLimit_eq_of_tendsto U _ (ultraLimit_tendsto U f hf).neg

theorem ultraLimit_sub (U : Ultrafilter ι) (f g : ι → ℂ)
    (hf : BoundedFamily f) (hg : BoundedFamily g) :
    ultraLimit U (fun i => f i-g i)=ultraLimit U f-ultraLimit U g :=
  ultraLimit_eq_of_tendsto U _ ((ultraLimit_tendsto U f hf).sub (ultraLimit_tendsto U g hg))

theorem ultraLimit_mul (U : Ultrafilter ι) (f g : ι → ℂ)
    (hf : BoundedFamily f) (hg : BoundedFamily g) :
    ultraLimit U (fun i => f i*g i)=ultraLimit U f*ultraLimit U g :=
  ultraLimit_eq_of_tendsto U _ ((ultraLimit_tendsto U f hf).mul (ultraLimit_tendsto U g hg))

theorem ultraLimit_smul (U : Ultrafilter ι) (z : ℂ) (f : ι → ℂ) (hf : BoundedFamily f) :
    ultraLimit U (fun i => z*f i)=z*ultraLimit U f := by
  rw [ultraLimit_mul U (fun _ => z) f (BoundedFamily.const z) hf,ultraLimit_const]

theorem ultraLimit_star (U : Ultrafilter ι) (f : ι → ℂ) (hf : BoundedFamily f) :
    ultraLimit U (fun i => star (f i))=star (ultraLimit U f) :=
  ultraLimit_eq_of_tendsto U _ (continuous_star.continuousAt.tendsto.comp (ultraLimit_tendsto U f hf))

theorem ultraLimit_sum (U : Ultrafilter ι) (s : Finset J) (f : J → ι → ℂ)
    (hf : ∀ j ∈ s,BoundedFamily (f j)) :
    ultraLimit U (fun i => ∑ j ∈ s,f j i)=∑ j ∈ s,ultraLimit U (f j) := by
  apply ultraLimit_eq_of_tendsto
  exact tendsto_finset_sum s (fun j hj => ultraLimit_tendsto U (f j) (hf j hj))

theorem ultraLimit_norm_le (U : Ultrafilter ι) (f : ι → ℂ) (M : ℝ)
    (hf : BoundedFamily f) (hM : ∀ᶠ i in (U : Filter ι),‖f i‖≤M) : ‖ultraLimit U f‖≤M :=
  le_of_tendsto (ultraLimit_tendsto U f hf).norm hM

theorem ultraLimit_re_nonneg (U : Ultrafilter ι) (f : ι → ℂ) (hf : BoundedFamily f)
    (hpos : ∀ᶠ i in (U : Filter ι),0≤(f i).re) : 0≤(ultraLimit U f).re :=
  ge_of_tendsto (Complex.continuous_re.continuousAt.tendsto.comp (ultraLimit_tendsto U f hf)) hpos

theorem ultraLimit_nonneg (U : Ultrafilter ι) (f : ι → ℂ) (hf : BoundedFamily f)
    (hpos : ∀ᶠ i in (U : Filter ι),0≤f i) : 0≤ultraLimit U f :=
  ge_of_tendsto (ultraLimit_tendsto U f hf) hpos

/-- Positive semidefiniteness survives a pointwise ultralimit of bounded kernels.
The hypothesis is finite Gram positivity of the original kernels; no Hilbert
space realization or positivity of the limiting kernel is assumed. -/
theorem ultraLimit_gram_nonneg (U : Ultrafilter ι) (K : ι → J → J → ℂ)
    (hK : ∀ j k, BoundedFamily (fun i => K i j k))
    (s : Finset J) (c : J → ℂ)
    (hpos : ∀ᶠ i in (U : Filter ι),
      0 ≤ ∑ j ∈ s, ∑ k ∈ s, star (c j) * K i j k * c k) :
    0 ≤ ∑ j ∈ s, ∑ k ∈ s, star (c j) * ultraLimit U (fun i => K i j k) * c k := by
  apply ge_of_tendsto _ hpos
  exact tendsto_finset_sum s (fun j _ => tendsto_finset_sum s (fun k _ =>
    ((ultraLimit_tendsto U (fun i => K i j k) (hK j k)).const_mul (star (c j))).mul_const (c k)))

/-- The real-part version used by pre-inner-product-space constructors. -/
theorem ultraLimit_gram_re_nonneg (U : Ultrafilter ι) (K : ι → J → J → ℂ)
    (hK : ∀ j k, BoundedFamily (fun i => K i j k))
    (s : Finset J) (c : J → ℂ)
    (hpos : ∀ᶠ i in (U : Filter ι),
      0 ≤ (∑ j ∈ s, ∑ k ∈ s, star (c j) * K i j k * c k).re) :
    0 ≤ (∑ j ∈ s, ∑ k ∈ s, star (c j) * ultraLimit U (fun i => K i j k) * c k).re := by
  apply ge_of_tendsto _ hpos
  exact Complex.continuous_re.continuousAt.tendsto.comp
    (tendsto_finset_sum s (fun j _ => tendsto_finset_sum s (fun k _ =>
      ((ultraLimit_tendsto U (fun i => K i j k) (hK j k)).const_mul (star (c j))).mul_const (c k))))

/-- Hermitian symmetry survives the same pointwise limit. -/
theorem ultraLimit_kernel_star (U : Ultrafilter ι) (K : ι → J → J → ℂ)
    (hK : ∀ j k, BoundedFamily (fun i => K i j k))
    (hstar : ∀ i j k, star (K i j k) = K i k j) (j k : J) :
    star (ultraLimit U (fun i => K i j k)) = ultraLimit U (fun i => K i k j) := by
  rw [← ultraLimit_star U (fun i => K i j k) (hK j k)]
  congr 1
  funext i
  exact hstar i j k

/-- A genuine ultrafilter extension of atTop, chosen using Mathlib's theorem. -/
def naturalUltrafilter : Ultrafilter ℕ := Ultrafilter.of Filter.atTop

theorem naturalUltrafilter_le_atTop : (naturalUltrafilter : Filter ℕ)≤Filter.atTop :=
  Ultrafilter.of_le Filter.atTop

theorem ultraLimit_natural_of_tendsto (f : ℕ → ℂ) {z : ℂ}
    (hf : Tendsto f Filter.atTop (𝓝 z)) : ultraLimit naturalUltrafilter f=z :=
  ultraLimit_eq_of_tendsto _ _ (hf.mono_left naturalUltrafilter_le_atTop)

end CyclicBell.General.Coverage
