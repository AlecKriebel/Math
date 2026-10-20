# Direct KSL: exact subclasses and a conditional stiff-uniform PDE bound

Problem 30003094 / queue row 1829. Authored research, 20 October 2026.

## Scope and conventions

These results concern the **original direct K–S–L method applied to the full vector field**, with all three subflows solved exactly. They do not concern the modified linear/nonlinear splitting of Ostermann–Piazzola–Walach (2019). They establish a restricted affine subclass result, not a general solution of the original open question.

All matrices are real; replacing transposes by adjoints gives the complex version. The matrix norm is Frobenius unless marked operator norm. At each step the input is a rank-r factorization Y=USVᵀ with orthonormal U,V and nonsingular S. The K endpoint must have rank r; each returned matrix must have rank r to continue the fixed-rank iteration. These existence/rank assumptions are explicit. None of the bounds below contains an inverse retained singular value, but they do contain regularity assumptions that must be checked uniformly for a family of problems.

Write E_A(t)=exp(tA) and J_A(h)=∫₀ʰ exp(sA) ds. This definition does not require A to be invertible. For dissipative A, meaning A+Aᵀ≤0, both E_A(t) and E_{UᵀAU}(t) are contractions for t≥0. Indeed, differentiating the squared Euclidean norm of a solution gives a nonpositive derivative; applying this to matrix columns gives Frobenius contractivity.

## 1. Homogeneous separable stiffness is integrated exactly

**Proposition 1.** For F(Y)=AY+YB with constant square matrices A,B, one exact KSL step returns

Y⁺=exp(hA)Y exp(hB).

There is no dissipativity requirement and no commutation requirement between the compressed and full operators.

**Proof.** Set B₀=VᵀBV and let U₊Ŝ=K(h). The K equation gives

K(h)=exp(hA)US exp(hB₀).

The factors on the right that multiply U are invertible, so K(h) has rank r. Set A₊=U₊ᵀAU₊. The exact negative S flow is

S̃=exp(−hA₊)Ŝ exp(−hB₀).

Writing the L equation in transposed form gives

L(h)ᵀ=exp(hA₊)S̃ Vᵀ exp(hB).

Consequently

U₊L(h)ᵀ=U₊Ŝ exp(−hB₀)Vᵀ exp(hB)
             =exp(hA)USVᵀ exp(hB).

The final matrix also has rank r. Repetition proves exactness at every time step. ∎

This explains why homogeneous diffusion alone cannot provide the sought direct-method counterexample. The affine perturbation and the subspace selected during K are essential to the obstruction in RESEARCH_REPORT.md.

## 2. Fixed invariant column spaces give another exact subclass

**Proposition 2.** Consider F(Y)=AY+YB+C, with constant A,B,C. Let W be a fixed r-dimensional subspace such that AW⊂W, range(C)⊂W, and range(Y₀)=W. Whenever the K endpoints have rank r, direct exact KSL returns the exact affine-flow endpoint. The assertion continues for successive steps for as long as the required ranks persist.

**Proof.** The K equation is K′=AK+KB₀+CV. Its initial columns and right-hand side lie in W, so K(t) lies in W. A rank-r endpoint basis U₊ therefore spans W. Since W is invariant under A, Q(t)=U₊ᵀK(t) obeys the closed affine equation

Q′=A₊Q+QB₀+D,  D=U₊ᵀCV.

The S subflow is the exact inverse of this autonomous affine flow. It returns S̃=Q(0)=U₊ᵀUS. The L flow is the exact coordinate equation for the full affine evolution inside W:

(Lᵀ)′=A₊Lᵀ+LᵀB+U₊ᵀC,
L(0)ᵀ=U₊ᵀY₀.

Multiplication by U₊ recovers the exact full solution, which remains in W. ∎

For example, a fixed finite collection of left Fourier modes invariant under a left diffusion operator gives this exact subclass if the forcing and initial matrix use those columns. The claim does not require uniformly bounded ∥A∥ on the whole discretization space.

## 3. A cancellation identity for left-affine stiffness

Now let F(Y)=AY+C, with A,C constant. Let Y=USVᵀ be the input, U₊ the endpoint K basis, and

P=U₊U₊ᵀ,  Q=I−VVᵀ,  a=U₊ᵀAU₊.

**Lemma 3.** The exact direct KSL endpoint is

Ψ_h(Y)=K(h)Vᵀ+U₊J_a(h)U₊ᵀC Q,

where K(h)=exp(hA)US+J_A(h)CV.

**Proof.** The K formula is immediate. Set D=U₊ᵀCV. The S and transposed L subflows are

S′=−aS−D,  S(0)=Ŝ,
(Lᵀ)′=aLᵀ+U₊ᵀC,  L(0)ᵀ=S̃Vᵀ.

Integrating S and then multiplying its endpoint by exp(ha) yields

exp(ha)S̃=Ŝ−J_a(h)D.

Thus

L(h)ᵀ=ŜVᵀ−J_a(h)DVᵀ+J_a(h)U₊ᵀC
       =ŜVᵀ+J_a(h)U₊ᵀC Q.

Since U₊Ŝ=K(h), multiplication by U₊ proves the formula. ∎

The cancellation is algebraic. It must not be replaced by separately estimating the possibly expansive backward S subflow. This identity also displays why KSL is direction-sensitive: the right-affine identity is instead Ψ_h(Y)=P Φ_h(Y), as proved in the main report.

## 4. Conditional one-step consistency without ∥A∥

For F(Y)=AY+C the exact flow is Φ_h(Y)=exp(hA)Y+J_A(h)C. Subtracting Lemma 3 gives

Φ_h(Y)−Ψ_h(Y)=[J_A(h)−U₊J_a(h)U₊ᵀ] C Q.

Define the mixed-stage forcing defect and the endpoint-subspace leakage by

ε_h(Y)=∥(I−P)C Q∥,
γ_h(Y)=∥(I−P)AU₊∥₂.

The word “mixed” is important: P is formed from the **new** left basis U₊, while Q uses the **old** right basis V. This is not asserted to equal the normal defect at Y or at Ψ_h(Y).

**Theorem 4.** If A+Aᵀ≤0, then

∥Φ_h(Y)−Ψ_h(Y)∥ ≤ h ε_h(Y)+(h²/2)γ_h(Y)∥C Q∥.

In particular, ∥C Q∥≤∥C∥ may be used on the right.

**Proof.** Set R=AU₊−U₊a=(I−P)AU₊. Duhamel's formula gives

exp(sA)U₊−U₊exp(sa)
 =∫₀ˢ exp((s−z)A)R exp(za) dz.

For completeness, differentiating exp((s−z)A)U₊exp(za) in z gives −exp((s−z)A)R exp(za); integration from z=0 to z=s verifies the displayed formula.

Contractivity therefore yields

∥[exp(sA)U₊−U₊exp(sa)]U₊ᵀC Q∥
 ≤ s γ_h(Y)∥U₊ᵀC Q∥ ≤ s γ_h(Y)∥C Q∥.

Decompose C Q=P C Q+(I−P)C Q. It follows that

∥[exp(sA)−U₊exp(sa)U₊ᵀ]C Q∥
 ≤ ε_h(Y)+s γ_h(Y)∥C Q∥.

Integrating s from 0 to h proves the theorem. ∎

This is not a bare semigroup theorem. The leakage factor γ_h(Y) is a regularity/invariance requirement on a subspace selected by the **numerical method**. Without a uniform bound on it, Theorem 4 does not imply a stiffness-uniform order estimate.

## 5. A conditional global theorem

**Theorem 5.** Fix T>0. Consider any family of left-affine problems X′=AX+C, any dimensions and fixed ranks allowed for each member, and exact KSL iterates Y_j at times t_j with h_j=t_{j+1}−t_j>0 and h_max=max h_j. Suppose:

1. A+Aᵀ≤0 for every member.
2. The necessary rank-r K endpoints and rank-r returned matrices exist up to T.
3. ∥Y₀−X(0)∥≤δ.
4. For every actual numerical step, ε_{h_j}(Y_j)≤ε and γ_{h_j}(Y_j)∥C Q_j∥≤H, with δ,ε,H independent of the stiffness/discretization parameters.

Then for every t_n≤T,

∥Y_n−X(t_n)∥ ≤ δ+t_n ε+(H/2)∑_{j<n}h_j²
                  ≤ δ+Tε+(T h_max/2)H.

If γ_{h_j}(Y_j)≤Γ and ∥C∥≤M, one may take H=ΓM. No Lipschitz estimate for the numerical map and no inverse singular value is needed.

**Proof.** Differences under the exact affine flow satisfy

Φ_h(Z)−Φ_h(W)=exp(hA)(Z−W),

so the exact flow is nonexpansive. Apply Theorem 4 at the actual input Y_j and use the triangle inequality:

∥Y_{j+1}−X(t_{j+1})∥
 ≤∥Ψ_{h_j}(Y_j)−Φ_{h_j}(Y_j)∥
   +∥Φ_{h_j}(Y_j)−Φ_{h_j}(X(t_j))∥
 ≤h_jε+(h_j²/2)H+∥Y_j−X(t_j)∥.

Sum this recurrence and use ∑h_j=t_n and ∑h_j²≤h_max t_n. ∎

The theorem is a genuine global-in-time first-order temporal estimate for this specified class, conditional on the stated numerical-stage properties. It is not an unconditional nonlinear PDE theorem and does not show that target-solution smoothness alone implies those properties. Uniformity in rank is also not automatic: ε,Γ,M and rank-preserving existence must remain uniform if rank varies.

## 6. A periodic Fourier-Galerkin PDE corollary, including spatial error

Consider the autonomous equation on the two-dimensional periodic torus,

∂_t z=∂_x²z+f(x,y),   z(0)=z₀,

in the Hilbert norm L²((0,2π)²). There is diffusion in x only; no assertion about a fully two-sided parabolic operator is made here. Use orthonormal real Fourier bases in x and y, retaining all modes of frequency at most N in each variable. Let Π_N be this tensor-product L²-orthogonal projection. The coefficient matrix Z_N satisfies

Z_N′=A_N Z_N+C_N,

where A_N is symmetric negative semidefinite, C_N contains the coefficients of Π_N f, and the coefficient Frobenius norm is exactly the represented function's L² norm. Its full-field norm ∥A_N∥₂ grows like N², but the contraction constant is one.

Let the reference Galerkin solution start at Π_N z₀. Let the numerical rank-r initializer have coefficient error at most δ_N relative to Π_N z₀. Assume all required ranks persist and the numerical stages satisfy

∥(I−P_{j+1})C_N(I−V_jV_jᵀ)∥≤ε,
∥(I−P_{j+1})A_NU_{j+1}∥₂≤Γ,

with ε,Γ independent of N and the time steps. Then the function z_{N,j}^{KSL} represented by Y_j obeys

∥z_{N,j}^{KSL}−z(t_j)∥_{L²}
 ≤δ_N+Tε+(T h_max/2)Γ∥f∥_{L²}
   +∥(I−Π_N)z₀∥_{L²}+T∥(I−Π_N)f∥_{L²},

for t_j≤T.

**Proof.** The temporal/rank part follows from Theorem 5 and ∥C_N∥≤∥f∥_{L²}. The exact PDE mild solution is

z(t)=exp(t∂_x²)z₀+∫₀ᵗ exp(s∂_x²)f ds.

The Fourier projection commutes with this semigroup. Hence the exact Galerkin solution is Π_Nz(t), and semigroup contraction gives

∥z(t)−Π_Nz(t)∥_{L²}
 ≤∥(I−Π_N)z₀∥_{L²}+t∥(I−Π_N)f∥_{L²}.

Add the two errors. ∎

If z₀,f∈H^s of the torus, s≥0, define the H^s norm by weights (1+k²+ℓ²)^s on the orthonormal complex Fourier coefficients, equivalently the corresponding real-basis norm. Every discarded mode has max(|k|,|ℓ|)≥N+1, so the last two terms are bounded by

[1+(N+1)²]^(−s/2)(∥z₀∥_{H^s}+T∥f∥_{H^s}).

Thus this corollary specifies the PDE, boundary condition, space discretization, norm, exact subflows, rank condition, numerical-stage assumptions, temporal order and spatial tail. No unweighted grid sample norm is substituted for L².

### What can make the stage hypotheses meaningful?

- A sufficient condition for Γ is the explicit uniform basis bound
  ∑_{i=1}^r∥∂_x²u_{j+1,i}∥_{L²_x}²≤Γ²,
  where u_{j+1,i} are the orthonormal left spatial basis functions. Indeed, this bounds ∥A_NU_{j+1}∥₂, hence its projected leakage. The bound concerns the numerical basis, not just the exact solution.
- The mixed forcing defect vanishes when the forcing columns lie in the new left subspace, or the forcing rows lie in the old right subspace. More generally its displayed uniform estimate must be established for the chosen problem and iteration.
- If all columns stay in a fixed invariant Fourier subspace containing the forcing columns, Proposition 2 gives exact temporal evolution, under the rank condition. This is a concrete nonempty case of the hypotheses, but not evidence that they hold generically.

## 7. A weaker right-affine graph-norm estimate

For comparison, suppose F(Y)=YB+C, B+Bᵀ≤0. The main report proves Ψ_h(Y)=P Φ_h(Y), where P is the K endpoint column projector. For one step,

∥Φ_h(Y)−Ψ_h(Y)∥≤h(∥YB∥+2∥C∥).

**Proof.** Put K₀=US and B₀=VᵀBV. Since B₀ is dissipative,

K(h)−K₀=∫₀ʰ K₀B₀ exp(sB₀)ds+∫₀ʰ CV exp(sB₀)ds,

and K₀B₀=YBV. Thus ∥K(h)−K₀∥≤h(∥YB∥+∥C∥). As (I−P)K(h)=0,

∥(I−P)Y∥=∥(I−P)K₀∥≤h(∥YB∥+∥C∥).

Use Φ_h(Y)=Yexp(hB)+∫₀ʰ Cexp(sB)ds and contraction of exp(hB) to obtain the result. ∎

This is **only an O(h) one-step estimate**, not an O(h²) local consistency estimate. Summing it over T/h steps need not yield a vanishing bound. We do not turn it into an unsupported global first-order theorem. It merely exhibits a graph-norm quantity that the negative families fail to control: in the smoother-target example of the main report, ∥Y₀B∥ diverges despite ∥Y₀−X₀∥→0.

## 8. Reproducibility and remaining gap

The checker check_subclass_identities.py tests the three endpoint identities and Theorem 4's local inequality on 24 seeded rank-two matrices. The positive theorem rests on the proofs above, not these tests. In particular, those tests do not certify any numerical-stage regularity for a PDE family.

What remains unresolved is a substantially broader direct-method result deriving mesh-uniform stage control from natural PDE data and initialization assumptions, especially for two-sided or nonlinear operators. The negative constructions show why assumptions consisting only of contractive analytic semigroup bounds, bounded forcing, a small normal remainder and small Hilbert-norm initialization error cannot suffice. They do not exclude useful positive theorems under additional spatial regularity or restricted initialization.
