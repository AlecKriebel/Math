# Independent elementary checks

For P=C[p,s,u,F,J], x=s²+u³+p²F and H=x²F−(1+2sx)J−p²J²−pu, the source's p-inverted coordinates give A[p⁻¹]=C[p,p⁻¹,x,y,z]. Hence Spec A is smooth on D(p), once those inverse substitutions are verified.

On the closed fiber p=0 set x₀=s²+u³. Since ∂x/∂F=p² and x is independent of J, the ambient partial derivatives reduce to

∂H/∂F mod p = x₀²,
∂H/∂J mod p = −(1+2sx₀).

The identity 4s²x₀²+(1−2sx₀)(1+2sx₀)=1 shows these two functions never vanish simultaneously. The hypersurface Jacobian criterion over C therefore proves smoothness at every closed point of V(p). Together the two opens/fiber cases cover Spec A. This establishes smoothness directly, without confusing a scheme retract with its algebra retraction or relying on regularity descent.

For algebra maps i:A→B and r:B→A, r∘i=id_A. On spectra, π=Spec(i):Spec B→Spec A and σ=Spec(r):Spec A→Spec B satisfy π∘σ=id_Spec A. The idempotent algebra endomorphism e=i∘r:B→B induces the idempotent scheme endomorphism σ∘π on Spec B. The image algebra is i(A), not a quotient that has been left unidentified.
