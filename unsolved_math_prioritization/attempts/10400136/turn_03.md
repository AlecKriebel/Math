# Attempt 3: charge/flattening algebra and symmetry-factor cancellation

## Mechanism and conventions

We tested whether the scalar symmetrization factor itself isolates all of the desired phase. We use the explicit quantum-shape convention in Baseilhac–Benedetti, *Non ambiguous structures*, §8, equation (8), [primary preprint](https://arxiv.org/abs/1506.01174). Fix an odd N=2m+1, ζ=exp(2πi/N), an oriented branched tetrahedron with sign ε in {−1,1}, shape parameters w_k, integer flattenings f_k and charges c_k. They satisfy w_(k+1)=(1−w_k)^(-1), Σf_k corrected by the principal log branches so that Σ(log(w_k)+πif_k)=0, and Σc_k=1. Define

    u_k = exp((log(w_k)+πi(N+1)(f_k−εc_k))/N),
    α(f,c) = (u_0^(−c_1) u_1^(c_0))^m.

All exponents on u_k in α are integers, so no further power branch is implicit.

## Exact calculation

Writing L_k=log(w_k), substitution gives

    α(f,c) = exp{(m/N)[−c_1 L_0+c_0 L_1
                       +πi(N+1)(c_0 f_1−c_1 f_0)]}.        (1)

The apparent quadratic terms in the charges cancel exactly:

    ε c_1 c_0 − ε c_0 c_1 = 0.

For a charge increment d=(d_0,d_1,d_2) with Σd_k=0, recomputing the quantum roots for the new charge and applying (1) yields

    α(f,c+d)/α(f,c)
      = exp{(m/N)[−d_1L_0+d_0L_1
                    +πi(N+1)(d_0f_1−d_1f_0)]}.          (2)

This is an exact local identity, not a statement that the modified charge extends to a global triangulation.

For an even flattening increment f→f+2a with Σa_k=0, one has

    u_k(f+2a,c)/u_k(f,c) = ζ^(a_k),
    α(f+2a,c)/α(f,c) = ζ^[m(c_0a_1−c_1a_0)].            (3)

Indeed exp(2πi(N+1)a_k/N)=ζ^(a_k). Thus even changes, invisible to flattening parity, may change the local symmetry phase. For c=(1,0,0) and a=(0,1,−1), the phase is ζ^m. Since gcd(m,N)=1, this is primitive. This local example does not prove a nontrivial phase for a closed state sum: the global edge and weight constraints may force compensating contributions.

There is also a local non-phase obstruction to interpreting α as merely the root-of-unity ambiguity. Take (w_0,w_1,w_2)=(2,−1,1/2), f=(0,−1,0), c=(1,0,0), and d=(0,1,−1). These satisfy the tetrahedral constraints. Equation (2) gives

    |α(f,c+d)/α(f,c)| = 2^(−m/N) ≠ 1.

Therefore the symmetry factor contains more than unit-modulus phase data at the tetrahedral level. Dividing by it is a significant change to the state sum, whose invariance needs its own theorem.

## A concrete global test left unsupplied

For a fixed triangulation, all signed edge-sum and fixed boundary-log requirements on an even flattening increment are integer linear equations Ca=0, with the tetrahedral equations included. Any permitted a in this kernel changes the product of local factors by

    ζ^[m Σ_Δ(c_(Δ,0)a_(Δ,1)−c_(Δ,1)a_(Δ,0))].           (4)

Thus a proposed invariance of that product under every such change requires the displayed linear functional to vanish modulo N on the allowed integer kernel. This is a finite lattice calculation once C and the charge system are actually supplied. No synthetic matrix is substituted for a genuine triangulation here, and the reduced tensor contraction may still compensate the factor in (4).

## Scope and outcome

The published non-ambiguous refinements are relevant partial progress, but retain root ambiguities. More decisively for the original closed pairs, their normalized defect is trivial modulo μ_4 (Proposition 1.13 and §8.7). That fact defeats the proposed direct use of this particular defect as a nontrivial closed-triple phase selector; it does not prohibit other geometric refinements.

**Result:** exact local phase/charge formulas and a specified global lattice test. No complete global anomaly cancellation and no new invariant are established.
