# Independent reconstruction of the candidate mathematics

Only candidate `TURN_1.md` has been opened at this stage. Its opening and closing scope sentences are part of that proof file; no program, check output, state/final result, source gate, prior-resolution file, or earlier review has been read. The source-first baseline seal is already recorded. The reconstruction below uses the independently retrieved primary-source definitions and direct equations, not the claimed check results.

## Construction and actual AF hypotheses

Take χ∈C∞([0,∞)), 0≤χ≤1, χ=0 for r≤2, χ=1 for r≥3. Define u=1−χ(r)/r with χ/r=0 near zero; g=u⁴δ on R³. It is globally smooth because the origin has u=1 and the transition functions are smooth. For r≥2, u≥1−1/r≥1/2; for r≤2, u=1. Consequently `(1/16)δ≤g≤δ` and length is bounded below by one fourth of Euclidean length. Every g-Cauchy sequence is Euclidean Cauchy and g is complete. R³ gives connectedness, orientability, one end, and no boundary.

For r≥3, u=1−1/r. Thus g−δ=O(r⁻¹), ∂g=O(r⁻²), ∂²g=O(r⁻³), and every higher derivative has the corresponding decay. The scalar curvature is `R_g=−8u⁻⁵Δδu`. It vanishes for r≤2 and r≥3, hence is smooth and integrable with respect to dV_g. It must be negative somewhere: `∫R³ Δu dx=lim_{r→∞}4πr²u'(r)=4π>0`, while Δu has compact support. This last observation explicitly separates the counterexample from the R≥0 class.

For g_ij=u⁴δ_ij, summation gives `∂i gij−∂j gii=−2∂j(u⁴)=−8u³∂j u`. ADM flux at radius r is `(1/(16π))4πr²(−8u³u')=−2r²u³u'`. Since u'=1/r² on the end, m_ADM=−2. The hypotheses of the original one-ended smooth O₂ AF definition and finite ADM mass are met; the hypothesis R≥0 is not met.

## Exhaustion and the harmonic exterior

Let a_R=(R/2)e₁ and K_R={|x−a_R|≤R}, R≥6. If |x|≤R/2 then |x−a_R|≤R, so K_R contains the full core and a centered radius-R/2 ball. If S≥R, then `|a_S−a_R|+R=(S+R)/2≤S`, proving nesting. The spheres are smooth and bounded; K_R exhausts R³ as R→∞. Every exterior point has r≥R/2≥3, exactly the region where u=1−1/r is positive and Euclidean harmonic. No unsupported inclusion about the transition annulus is used.

## Metric capacity, not Euclidean replacement

For g=u⁴δ in3 dimensions, `g^ij=u⁻⁴δ^ij`, `dV_g=u⁶dx`, and `|∇φ|²_gdV_g=u²|∇φ|²δdx`. Also `Δ_gφ=u⁻⁶divδ(u²∇φ)`.

The Euclidean exterior sphere potential is f_R=1−R/|x−a_R|, zero on the sphere and1 at infinity. Because both u and f_R are harmonic on the entire exterior, `div(u²∇(f_R/u))=uΔf_R−f_RΔu=0`. Thus ψ_R=f_R/u is g-harmonic, has the correct boundary values, and finite energy. Uniform ellipticity and the exterior maximum principle give uniqueness of the potential. At infinity for each fixed R, `f_R=1−R/r+O_R(r⁻²)` and `1/u=1+1/r+O(r⁻²)`, hence `ψ_R=1−(R−1)/r+O_R(r⁻²)`. The normalized metric flux across a far coordinate sphere has factor u² times the Euclidean radial derivative, so its limit is R−1. Therefore `cap_g(K_R)=R−1` exactly. Sending the flux radius to infinity first at each fixed R is legitimate; uniformity of the O_R coefficient in the later exhaustion parameter is unnecessary.

This is precisely the m=−2 case of Jauregui2020 equation(41), printed p.22. The source proves the capacity transformation before imposing nonnegative mass for its volume rearrangement. It is therefore applicable to this example despite its appearance within the proof of Theorem7, whose final upper bound is expressly restricted to m≥0. Using that identity as if its subsequent volume estimate also held for m<0 would be false; the candidate does not do so.

The extra direct trial-energy bound is independently correct. Put ρ=|x−a_R|. For ρ≥R, the angular mean of1/|a_R+ρω| equals1/ρ because ρ>|a_R|. Thus `(1/(4π))∫ρ≥R R²ρ⁻⁴ dx=R`, and `(1/(4π))∫ρ≥R (−2/r)R²ρ⁻⁴dx=−1`. Since r≥ρ−R/2≥ρ/2, the positive r⁻² term is at most `4R²∫R∞ρ⁻⁴dρ=4/(3R)`. The actual weighted metric energy of the Euclidean trial function f_R is in `[R−1,R−1+4/(3R)]`, consistently above the minimizing value R−1. This trial bound is not used to claim an exact capacity.

## Volume with all omitted errors controlled

For r≥3, `u⁶=(1−1/r)⁶=1−6/r+15/r²−20/r³+15/r⁴−6/r⁵+1/r⁶`; the remainder after1−6/r is bounded by C/r². Replacing the true smooth u⁶ by1−6/r on the fixed core changes the volume integral by a finite, R-independent constant (1/r is locally integrable). K_R⊂B(0,3R/2), so `∫K_R r⁻²dx≤4π(3R/2)=6πR`. Thus `V_R=(4π/3)R³−6∫K_Rr⁻¹dx+O(R)` with a constant independent of R.

For d=|a|<R, shell integration about a gives

`∫B(a,R)r⁻¹dx = 4π[∫₀ᵈ ρ²/d dρ + ∫dᴿρdρ] = 2π(R²−d²/3)`.

At d=R/2 this is (11π/6)R², hence `V_R=(4π/3)R³−11πR²+O(R)`. Taking the normalized cube root gives `r_V=R[1−(33/4)/R+O(R⁻²)]^(1/3)=R−11/4+O(R⁻¹)`. Compact-fill volume cannot contribute a constant to r_V: its contribution is O(R⁻²), and higher conformal terms contribute O(R⁻¹). Dimensional constants and the sign of the mass term agree with the independently derived general family.

## What the supremum proves, and what it does not prove

This exact admissible exhaustion has `r_V(K_R)−cap_g(K_R)→−11/4+1=−7/4`. Therefore `m_CV≥−7/4>−2=m_ADM`. The gap is1/4, and strict inequality remains true if m_CV=+∞. The argument needs neither an upper bound for m_CV nor optimality/minimization of the shifted balls. In particular, it does not determine the exact value of m_CV.

For a general negative-mass end u=1+m/(2r) and fixed0≤λ<1, the same computations give cap=R+m/2, `V=(4π/3)R³+6πm(1−λ²/3)R²+O(R)`, `r_V=R+(3m/2)−mλ²/2+O(R⁻¹)`, and the deficit limit `m(1−λ²/2)`. At λ=0 it equals m; at m=0 all shifted Euclidean balls give0; if m>0, the shifted limit is≤m. Thus the displaced negative-mass effect is consistent with the standard positive-mass equality and directly exhibits why centered-ball computations cannot suffice.

A separate limiting exhaustion can take centers approaching tangency while keeping the core inside (L_j=j³, D_j=L_j−j). It improves the lower bound to m_CV≥m/2=−1. This is an optional strengthened control; it does not invalidate the candidate's weaker sufficient bound or imply the exact mass. The candidate's fixedλ construction is simpler and sufficient.

## Independent mathematical verdict before software/status/review access

**PASS for the stated explicit counterexample; PASS for the mathematical distinction of scopes.** The original intended R≥0/empty-minimal-boundary equality is already a literature result, with BFM2023 providing the key upper bound. The proof in TURN_1 correctly disproves only a literal unrestricted all-AF reading. All central steps have been reconstructed above; no missing hypothesis, hidden singularity, capacity normalization error, exhaustion defect, circularity, or insufficient-error-order step was found. The text properly leaves exact m_CV and historical novelty unestablished.

No mathematical fix is mandatory on the inspected proof. This verdict does not yet endorse the unexamined packet's final/state/source/priority statements or software reproducibility. Those are the next audit phase.
