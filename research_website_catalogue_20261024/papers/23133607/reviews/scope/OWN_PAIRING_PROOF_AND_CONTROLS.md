# Own actual uniform proof and hand-worked controls

Frozen after INITIAL92959fdf… and before supplied scientific code/output, archived/current reviewer opinion or any new foreign scientific body. This is actual written symbolic reasoning, not a claimed computational run. No scientific programme has been executed. Root140 gate is CLOSED. The mechanism is a perfect-pairing/common-kernel obstruction and exact structural witnesses, distinct from native finite-field replay.

## Universal pairing obstruction, without choosing a dual matrix

Let k be a perfect field of characteristic p, σ its Frobenius, and let T carry σ-semilinear F and σ^-1-semilinear V. Under the target's duality convention, an isomorphism α:T→T_D would define a nondegenerate k-bilinear pairing b(x,y)=α(x)(y) satisfying

b(Fx,y)=σ(b(x,Vy)), b(Vx,y)=σ^-1(b(x,Fy)).

Iterating gives b(F²x,y)=σ²(b(x,V²y)) and b(V²x,y)=σ^-2(b(x,F²y)). These are identities of scalar functions, not ordinary k-linear adjoint identities without twists.

For the actual M, F²e0=e2 and V²e0=e4, and both second kernels are K=span(e1,e2,e3,e4,e5). Therefore, for every y∈K,

b(e2,y)=σ²(b(e0,0))=0, b(e4,y)=σ^-2(b(e0,0))=0.

The two functionals b(e2,−),b(e4,−) lie in the one-dimensional annihilator K⊥. They must be dependent. But the independent vectors e2,e4 would have independent images under the injective map x↦b(x,−). Contradiction. This rules out any compatible perfect bilinear form, without requiring symmetry, antisymmetry, alternation, a polarization, or a preferred pairing on elliptic factors.

In coordinates, all entries in row2 and row4 of a hypothetical pairing matrix B vanish except possibly column0. Write B20=a,B40=c. If a=c=0 then row2 is zero. Otherwise the nonzero row combination c·row2−a·row4 vanishes, since its column0 coefficient is ca−ac=0 and all other coefficients are already0. Thus B is singular over every commutative field, with no division and no exceptional scalar case. This is an explicit universal algebraic singularity certificate. It does not solve an intertwiner by a finite prime-field search.

The annihilator interpretation independently yields the paper's numeric invariant: im(F_D²)=(kerV²)⊥ and im(V_D²)=(kerF²)⊥, so their intersection has dimension6−dim(K+K)=1. The primal second images ke2,ke4 are distinct, so their intersection has dimension0. Surjectivity of the dual-twist construction follows by defining φ on imV² through φ(V²t)=σ^-2ψ(t) for ψ vanishing on kerV², then extending linearly. Well-definedness and k-linearity use perfectness explicitly. Thus this route retains the semilinearity instead of hiding it in transpose notation.

## Extension to every n and arbitrary cross-block pairings

For M_n=M⊕I^(n−3), F²,V² vanish on each I, so both second kernels are K_n=K⊕I^(n−3), of dimension2n−1. The vectors e2,e4 remain independent second images from e0. Any putative perfect pairing on M_n, including arbitrary mixed pairings between old and added blocks, would again send those two vectors into the one-dimensional K_n⊥. The same singularity certificate applies. No cancellation/Krull–Schmidt theorem or block-diagonal assumption for the hypothetical isomorphism is used.

The rest of the local uniform construction is fully reconstructed in INITIAL_DERIVATIONS Families1–10. The explicit unimodular basis identifies the three I module factors; exact contravariance reverses their order; L=span(e0,e3,e5) complements imF and V is injective there. Each I has the analogous complement kx. These are formal Honda hypotheses for all original p>3,n≥3. Actual group-scheme realization still depends on the exact categorical primary statements and is not retroactively asserted verified by this proof freeze.

## Twelve actual hand-worked controls

1. **Mixed compositions and second kernels.** F has chains e0→e1→e2, e3→e4, with e5 isolated; V has e0→e5→e4, e3→e2, with e1 isolated. Every image under either is killed by the other. Both second maps kill exactly the span of all basis vectors except e0. No unlisted length-two source exists.

2. **Singularity certificate including zero cases.** Pairing compatibility forces B2j=B4j=0 for j=1,…,5. If(a,c)=(0,0), a row is zero. If(a,c)≠(0,0), c·row2−a·row4 is a nontrivial zero combination. This covers both one-zero cases and characteristic2 without a division; the group theorem's p>3 range is nevertheless retained.

3. **Actual scalar twists.** F²(λe0)=σ²(λ)e2 and V²(λe0)=σ^-2(λ)e4. Under the dual formula, F_Dφ is linear in t because σ(φ(V(λt)))=λσ(φ(Vt)), and is σ-semilinear in φ. Omitting the outerσ would fail linearity for a non-Frobenius-fixedλ. No finite field was chosen where σ² could accidentally become identity.

4. **Positive self-dual rank-two comparison.** On I with Fx=Vx=y, the pairing b(x,x)=b(y,y)=0,b(x,y)=b(y,x)=1 is nondegenerate. The four basis-pair identities for F are1=σ1,0=σ0,0=σ0,0=σ0; for V they are the same withσ^-1. Bilinearity plus semilinearity extends them to all coefficients. Thus the obstruction does not reject I; both second images are0 and the annihilator expression is0. No alternating form is required for self-duality.

5. **Padding with all cross terms allowed.** At n=4, dimM_n=8 and dimK_n=7. The same two pairing rows can be nonzero only in the e0 column, including their entries against both added I vectors, because those vectors lie in K_n. The singularity argument survives arbitrary mixed blocks. For general n the codimension remains1, proving the universal extension rather than testing a list of n.

6. **Integral inverse basis identities.** Substituting e0=a,e1=b,e2=z,e3=w−2b,e4=v−z,e5=u−w+b into u=e1+e3+e5 returns u; into v=e2+e4 returns v; into w=2e1+e3 returns w. The remaining a,b,z identities are immediate. The inverse contains no denominator, so reduction does not lose rank at an allowed prime.

7. **Three actual quotient actions and order.** On M1, Fu=Vu=v. On M2/M1, Fw=v+z becomes z and Vw=z. On M/M2, Fa=b and Va=u−w+b becomes b. The second vector is killed in each quotient. Under exact contravariance the group factors occur in the reverse order(a,b),(w,z),(u,v), not as same-direction module subobjects.

8. **Honda injectivity on arbitrary coefficients.** For l=ae0+be3+ce5, V(l)=σ^-1(a)e5+σ^-1(b)e2+σ^-1(c)e4. Independence forces all three twisted coefficients0, hence a=b=c=0. L and imF have disjoint displayed bases spanning allM, so L/pL→M/imF is an isomorphism. This is a uniform semilinear proof, not an ordinary determinant silently ignoringσ.

9. **Wrong complement negative witness.** L_bad=imF has V|L_bad=0 and maps to0 in M/imF, a3-dimensional quotient. It fails both required conditions despite having the expected dimension3. An argument using any arbitrarily selected half-dimensional subspace is invalid; the actual chosen L passes separately.

10. **Nilpotence is not quasi-supersingularity.** A6-dimensional module with F=V=0 is nilpotent but every subquotient also has zeroF,V, so it cannot have a factor isomorphic to I with nonzeroF. Moreover kerV is allM while imF=0; it fails the proposed deformability identity, and the complement condition would force L=M with noninjectiveV. This rejects two incorrect shortcuts at once without treating this object as the source's example.

11. **Base-change direction.** In a finite free W-basis of a Hopf algebra A, the dual basis of A^∨ reduces to the dual basis of A⊗k. The natural pairing commutes with multiplication/comultiplication, giving (A^∨⊗k)≅(A⊗k)^∨ as Hopf algebras. Therefore a W-Cartier self-duality would yield a special-fibre one. The converse is not used and is not established by this control.

12. **Categorical gap and forbidden extrapolations retained.** A module/word/integral lattice for a group over k is not itself a W-group realization. Actual finite Honda anti-equivalence and reduction/p-multiplication compatibility remain required. Likewise n≤2 minimality requires Takao's actual proposition, and the I elliptic identification uses algebraic closedness. Local formulas working at p=2 or3 do not extend the source's theorem to those primes. These are explicit unresolved interfaces, not silently assumed positive cases.

## Evidence limits at this freeze

All twelve controls were actually developed by symbolic hand reasoning after the initial, before any scientific output/code or foreign-body exposure. There is no claimed machine execution, formal certificate replay, finite-field experiment or native checker result. The checkable artifacts are the displayed identities, singularity certificate, positive pairing and countermechanisms. The local conclusion is a uniform module/Honda-condition proof conditional on the exact cited category and duality interfaces. Root140 remains CLOSED; no findings are shared.

Follow-up is null. No new scientific programme or first-priority claim is inferred from a classical module or the pairing reformulation. Primary acquisition may proceed only after the opposite initial/own-results freezes and explicit neutral root GO; old authenticated bodies are to be bound by reference rather than duplicated.
