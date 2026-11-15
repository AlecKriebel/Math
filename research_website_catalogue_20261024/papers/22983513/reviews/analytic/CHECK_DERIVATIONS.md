# Checkable independent interval enclosures

This calculation was designed from the sealed interval reconstruction, without importing the native verifier or its outputs. The shared coordinate-commutator proof is analytic; this separate check tests an actual infinite spectral remainder in a fully known model.

For Ω=(0,π), uⱼ=√(2/π)sin(jx), Eⱼ=j². The identity 2sin(jx)sin(kx)=cos((j−k)x)−cos((j+k)x), followed by integration of xcos(mx), gives aⱼⱼ=π/2; aⱼₖ=0 for unequal equal parity; and aⱼₖ=−8jk/[π(j²−k²)²] otherwise. Thus every state has infinitely many nonzero coordinate coefficients.

Let p be the largest integer with p²<z and choose K≥2p with K²>z. The exact scalar left remainder is

    F(z)=∑_{j²<z}[4(z−j²)j²−(z−j²)²].

The partial spectral right remainder is the sum, for j²<z, k≤K, k²>z and opposite parity, of

    64j²(z−j²)k²(k²−z) / [π²(k²−j²)³].

All terms are positive. For k>K, let ρ=1−p²/(K+1)². Then k²−j²≥ρk² and k²−z≤k². Dropping parity restrictions gives a rigorous upper tail bound

    T ≤ 64∑_{j²<z}j²(z−j²) / [π²ρ³K],

using ∑_{k>K}k⁻²≤∫_K^∞x⁻²dx=1/K. A lower bound for π gives an upper bound for the partial sum and T; an upper bound for π gives a lower partial sum. Every stored exact enclosure contains the rational F(z). The finite partial sums remain strictly below F(z), as infinite support predicts.

For π use the alternating arctangent series at1/5 and1/239. The true value lies between its24-term sum and that sum plus the next term. Machin’s identity π=16atan(1/5)−4atan(1/239) follows from tan(4atan(1/5))=120/119, the tangent subtraction formula giving1 after subtracting atan(1/239), and the angle being between0 andπ/2. This provides rational lower/upper bounds differing by less than10⁻³⁴. There is no floating-point tolerance in any acceptance predicate.

The seven tested thresholds and exact F values are3/2→7/4,4→3,9/2→19/2,9→23,10→50,25→230,65/4→395/4. For example the first enclosure is approximately[1.74684,1.75318] around7/4; the stored fractions, not those rounded figures, are the evidence. All use K=512.

Separately, ∑ⱼ₌₁ᴶj²=J(J+1)(2J+1)/6 and ∑ⱼ₌₁ᴶj⁴=J(J+1)(2J+1)(3J²+3J−1)/30 imply

    D=(J+1)(2J+1)(3J+5)/12,
    D−(Eⱼ₊₁−Eⱼ)²/4=(2J+1)(3J²+2J+2)/12>0, j=J.

The program compares these to independently accumulated exact finite moments for J=1,…,128. It tests wrong sign and missing coefficient64 against the enclosures, rejects treating a finite partial sum as the full remainder, retains equality at z=E₁, and checks the zero finite trace that obstructs imposing every Dirichlet first-moment row rule on a finite symmetric matrix. These are semantic controls, not a claim to have exhaustively mutation-tested the program.
