# Independent mathematical audit: ordinary GE tensorization

Date: 2026-10-09. Problem: 30004587 / OWR-4990370-005.

## Verdict

**ACCEPT the counterexample to same-constant tensorization in the stated, not necessarily ergodic, tracial setting.**

The qubit depolarizing semigroup has ordinary logarithmic-mean GE(1,∞), including for arbitrary complex observables. The identity semigroup on a second qubit also has GE(1,∞). Their tensor product violates GE(1,∞) at the positive definite rational density and rational self-adjoint observable stated below. The violation is exact, takes place at a positive time, and is evaluated in the full tensor-product differential calculus.

No blocking mathematical gap was found. The certificate for the audited file, source hashes, and executed checker is recorded separately in `AUDIT_MANIFEST.json`.

## 1. Scope and source checks

1. Wirth's contribution to **Oberwolfach Report 2/2021**, printed pp. 78–79, defines the class using a normal faithful trace and a symmetric weak-star continuous UCP semigroup; it does not require ergodicity. The discussion on p. 79 expressly includes nonergodic semigroups before posing the tensorization question. Both pages were visually inspected. The identity factor is therefore within this question's stated class. The displayed GE formula on p. 78 lacks the curvature exponential; the precise convention must be taken from the next source. [Public PDF](https://publications.mfo.de/bitstream/handle/mfo/3838/OWR_2021_02.pdf)

2. Wirth–Zhang, **Complete gradient estimates of quantum Markov semigroups**, arXiv:2007.13506v2, Definition 2.5, requires

   q_ρ(P_t A) ≤ e^(−2Kt) q_{P_tρ}(A).

   It tests all observables in the form domain and all trace-normalized densities. No ergodicity assumption occurs. In finite dimension there are no domain, normality, or Γ-regularity obstructions. Their complete estimate additionally requires all identity amplifications, and their Theorem 4.1 concerns that stronger condition. [Primary manuscript](https://arxiv.org/abs/2007.13506v2)

3. Münch–Wirth–Zhang, **Intertwining Curvature Bounds for Graphs and Quantum Markov Semigroups**, arXiv:2401.05179v1, §3.3 uses generator A−τ_n(A)I and normalized trace. Theorem 3.23 gives GE_Λ(1/2+1/n,∞), hence GE(1,∞) for n=2. Although its initial convention tests self-adjoint observables, Remark 3.24 extends the theorem to arbitrary complex observables for symmetric means. The logarithmic mean qualifies. The theorem and remark were visually inspected on pp. 26 and 28. The arXiv record inspected on the audit date lists v1 of 10 January 2024; no publication or novelty conclusion is inferred from that record. [Primary manuscript](https://arxiv.org/abs/2401.05179v1)

The authored proof also establishes the needed qubit estimate independently, so its acceptance does not rest on a convention mismatch or an unproved invocation of the 2024 result.

## 2. Factor estimate independently checked

Let σ₁,σ₂,σ₃ be the usual Pauli matrices and let δ_j A=[σ_j,A]/√8. Direct matrix algebra gives

Σ_j δ_j*δ_j(A)=A−τ₂(A)I₂.

Here the star on δ_j denotes Hilbert-space adjoint with respect to τ₂. Thus the factor 1/√8 is correct for the positive generator, and the logarithmic weighted norm is

q_ρ(A)=(1/8)Σ_j τ₂([σ_j,A]* Λ_ρ([σ_j,A])),

where Λ_ρ(B)=∫₀¹ρ^αBρ^(1−α)dα.

After unitarily diagonalizing ρ=diag(r,s), write A=[[u,v],[w,z]]. Independent expansion gives

q_ρ(A)=θ(r,s)|u−z|²/4
       +(r+s+2θ(r,s))(|v|²+|w|²)/8.

The executed exact checker verifies the entire Hermitian Gram matrix on the four complex matrix units, including all cross terms. This establishes the formula for arbitrary complex A, rather than only for Hermitian A.

Conjugating the Pauli basis acts by an orthogonal transformation on the real space of traceless Hermitian matrices, so the summed norm is unitarily covariant. Under depolarization, r+s remains fixed and θ(r,s) cannot decrease. The proof's joint-concavity argument is valid: each scalar function r^αs^(1−α) is jointly concave for 0≤α≤1, and its integral is bounded above by the arithmetic mean. All nonnegative boundary cases follow by continuity. Since δP_t=e^(−t)δ, this proves the required GE(1,∞) for every density, observable, and time.

The identity factor has zero derivation; its GE(1,∞) is the equality 0≤0. It is nonergodic, which is allowed here.

## 3. Full tensor calculus, not merely generator restriction

On M₄ use U_j=σ_j⊗I₂, Δ_j A=[U_j,A]/√8, and τ₄=Tr/4. Exact checking on all sixteen matrix units verifies

Σ_j Δ_j*Δ_j(A)=A−I₂⊗(τ₂⊗id)(A).

This is the positive generator of T_t=P_t⊗id. Its logarithmic norm uses ordinary left/right multiplication by the full M₄ density, not separate marginal densities.

For the four Bell projectors p_i, the three U_j give the three perfect matchings of four points. Each unordered pair supplies two matrix entries of modulus |a_i−a_k|. Consequently the full ambient norm, for Bell-diagonal ρ and A, is

q^T_ρ(A)=(1/16)Σ_{i<k}θ(r_i,r_k)|a_i−a_k|².

The coefficient is exactly (1/8)·(1/4)·2. This directly verifies the inherited logarithmic weights. Merely knowing that the Bell algebra is invariant under the generator would not have been enough; the proof correctly performs this additional calculation.

An independent shorter check uses p=|Φ⁺⟩⟨Φ⁺| and q=I₄−p. For ρ=rp+sq,

Λ_ρ(B)=rpBp+sqBq+θ(r,s)(pBq+qBp).

Substituting each full commutator [U_j,p] gives q^T_ρ(p)=3θ(r,s)/16 exactly. The checker verifies this symbolic identity without assuming a classical restriction principle.

## 4. Exact witness and strict violation

The observable and density are

p=(1/2)[[1,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,1]],

ρ=(2/3)I₄+(4/3)p.

The density eigenvalues are 2,2/3,2/3,2/3, so ρ>0 and τ₄(ρ)=1. The observable p is self-adjoint and rank one, not positive definite.

Because the first-factor conditional expectation sends p to I₄/4, it sends ρ to I₄. At t=log 2,

T_tρ=(3/2)p+(5/6)(I₄−p),
T_tp=p/2+I₄/8.

Therefore

q^T_ρ(p)=1/(4 log 3),
q^T_{T_tρ}(p)=1/(8 log(9/5)).

The purported GE(1,∞) has

LHS=1/(16 log 3),
RHS=1/(32 log(9/5)).

Both logarithms are positive, and LHS>RHS is equivalent to

(9/5)²>3,

which follows from the exact rational difference 6/25>0. The numerical gap is approximately 0.00372440391361056208914, supplied only as a diagnostic; the sign proof does not use floating point.

The independent infinitesimal calculation also agrees:

(d/dt)|₀ q^T_{T_tρ}(p)=(1−log 3)/(4(log 3)²)<0.

For example, log 3=2∫₀^(1/2)(1−u²)^(−1)du>1. This second check is consistent with the positive-time witness and the exponential convention.

## 5. Acceptance boundaries

- This disproves preservation of the same curvature lower bound under arbitrary tensor products in the stated class; it also exhibits ordinary GE(1,∞) without CGE(1,∞).
- The example includes an identity factor. It does not prove failure when both factors are required to be ergodic.
- It does not contradict the complete-GE tensorization theorem.
- It does not settle preservation of a fixed nonpositive K, nor quantify an optimal weaker tensor bound.
- Rescaling the first generator and time transports the same counterexample to each prescribed K>0; its weighted norm gains a common positive scale factor, which cancels in the comparison.
- This is a correctness and source-scope audit, not a claim of global literature novelty.

## Reproducibility

Run `python verify_pauli_witness.py` with SymPy. The script checks the qubit and tensor generator identities on full matrix-unit bases, the general complex-observable weighted Gram matrix, the full ambient Bell-projector norm, all rational matrix/eigenvalue identities, the finite-time energy values, and the time-zero derivative. The successful output is saved as `symbolic_results.json`.

Source PDF renderings are inspection evidence only, not authored mathematical material.
