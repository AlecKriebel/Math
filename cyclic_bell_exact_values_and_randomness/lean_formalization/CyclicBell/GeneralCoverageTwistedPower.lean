import CyclicBell.GeneralCoveragePolarAlgebra
import CyclicBell.GeneralFunctionalCalculus

/-! Ordered products for a noncommutative twisted power. No commutativity of
the factors is assumed; the application identifies them through actual CFC. -/
noncomputable section
namespace CyclicBell.General.Coverage
variable {A : Type*} [Monoid A]

def orderedProduct (f : ℕ → A) (n : ℕ) : A := ((List.range n).map f).prod

@[simp] theorem orderedProduct_zero (f : ℕ → A) : orderedProduct f 0=1 := rfl

theorem orderedProduct_succ (f : ℕ → A) (n : ℕ) :
    orderedProduct f (n+1)=orderedProduct f n*f n := by
  simp [orderedProduct,List.range_succ]

theorem shift_power (b : A) (f : ℕ → A)
    (hshift : ∀ k,b*f k=f (k+1)*b) (n k : ℕ) :
    b^n*f k=f (k+n)*b^n := by
  induction n with
  | zero => simp
  | succ n ih =>
    calc
      b^(n+1)*f k = b*(b^n*f k) := by rw [pow_succ']; simp only [mul_assoc]
      _ = b*(f (k+n)*b^n) := by rw [ih]
      _ = f (k+n+1)*(b*b^n) := by rw [← mul_assoc,hshift,mul_assoc]
      _ = f (k+(n+1))*b^(n+1) := by rw [pow_succ']; simp only [Nat.add_assoc]

theorem twisted_power_ordered (b : A) (f : ℕ → A)
    (hshift : ∀ k,b*f k=f (k+1)*b) (n : ℕ) :
    (f 0*b)^n=orderedProduct f n*b^n := by
  induction n with
  | zero => simp
  | succ n ih =>
    calc
      (f 0*b)^(n+1)=orderedProduct f n*(b^n*f 0)*b := by
        rw [pow_succ,ih]
        simp only [mul_assoc]
      _ = orderedProduct f n*(f n*b^n)*b := by
        rw [shift_power b f hshift n 0,Nat.zero_add]
      _ = orderedProduct f (n+1)*b^(n+1) := by
        rw [orderedProduct_succ,pow_succ]
        simp only [mul_assoc]

theorem conjugate_twisted_power [Star A] (a b : A) (hb : StarUnitary b) (n : ℕ) :
    (a*b)^n=orderedProduct (fun j => b^j*a*(star b)^j) n*b^n := by
  have hshift (j : ℕ) :
      b*(b^j*a*(star b)^j)=(b^(j+1)*a*(star b)^(j+1))*b := by
    have hc : (star b)^(j+1)*b=(star b)^j := by
      rw [pow_succ,mul_assoc,hb.1,mul_one]
    calc
      b*(b^j*a*(star b)^j)=(b^(j+1)*a)*(star b)^j := by
        rw [pow_succ']; simp only [mul_assoc]
      _ = (b^(j+1)*a)*((star b)^(j+1)*b) := by rw [hc]
      _ = _ := by simp only [mul_assoc]
  simpa only [pow_zero,one_mul,mul_one] using
    twisted_power_ordered b (fun j => b^j*a*(star b)^j) hshift n

end CyclicBell.General.Coverage
