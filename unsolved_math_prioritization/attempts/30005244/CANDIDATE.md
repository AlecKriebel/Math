# Spectral correctness of cubic DDA away from the static lattice interval

Numeric record **30005244 / OWR-11101924-008**. Full candidate for the source's off-interval spectral question, with the geometric consistency hypothesis made explicit. **Unreviewed.** One substantive author research turn. No novelty assertion.

## 1. Statement, normalization, and geometric hypothesis

Fix a bounded measurable set Ω in R³ and a frequency κ in C. All vector fields have three complex components. The most familiar admissible case is a bounded Lipschitz domain, or its closure; more generally, any bounded set with boundary of Lebesgue measure zero is admissible. We use ordinary volume measure, not a surface or point measure.

For every h>0 let the cubic lattice be x_m=a_h+hm, m in Z³, with arbitrary translation a_h. Put

    Q_m^h = x_m + h[-1/2,1/2)³,
    I_h = {m : x_m ∈ Ω},
    Ω_h = union_{m∈I_h} Q_m^h.

The precise geometric assumption is

    |Ω_h △ Ω| → 0.                                      (G)

Here △ is symmetric difference. All Ω_h lie in one bounded box for sufficiently small h. Condition (G) holds for every such translated cubic grid when |∂Ω|=0: a misclassified cell lies in a distance-√3 h neighborhood of the boundary. It is enough to assume (G) along the mesh sequence being considered. No boundary smoothness, convexity, or topology is otherwise used below.

Let r=|x|, e=x/r, and define for x≠0

    g_κ(x) = exp(iκr)/(4πr),
    K_κ(x) = -(D² + κ² I)g_κ(x),
    K_0(x) = (I-3eeᵀ)/(4πr³).

Transpose here is ordinary matrix transpose; operators and norms are those of complex Hilbert spaces. The source's diagonal-omitting DDA matrix is

    (T_κ^h)_{mn} = h³ K_κ(x_m-x_n), m≠n in I_h,
    (T_κ^h)_{mm} = 0.                                  (1)

The continuum comparison operator on L²(Ω;C³) is

    S_κ = p.v. ∫_Ω K_0(x-y)(·)(y)dy
          + ∫_Ω [K_κ-K_0](x-y)(·)(y)dy
        = A_κ - I/3,                                  (2)

where A_κ is the distributionally differentiated volume operator in the OWR report. The shift is essential. Equivalently, T_κ^h+I/3 approximates the spectrum of A_κ in the translated region. Neither the spectral variable z nor κ is sent to infinity as h→0.

Let T be the bounded selfadjoint lattice convolution operator on ℓ²(Z³;C³) with off-diagonal coefficients K_0(m-n) and zero diagonal. Define the **exact** interval

    I_lat = [Λ_-,Λ_+] = closure of the numerical range of T.

The boundedness of T and its interval bound are established inputs, credited to Costabel–Dauge–Nedaiasl [CDN, Proposition 3.15 and Sections 2.2, 2.4]. In particular [-1/3,2/3]⊂I_lat, so 0∈I_lat. This proof does not identify its endpoints with the numerical guesses -0.426024... and 0.770902... .

### Theorem

Under (G), for every fixed κ∈C:

1. Every compact subset of C\(I_lat ∪ σ(S_κ)) is eventually disjoint from σ(T_κ^h), with a uniform matrix-resolvent bound there.
2. The spectrum of S_κ outside I_lat consists of isolated eigenvalues of finite algebraic multiplicity. Every such eigenvalue is approximated by exactly that many eigenvalues of T_κ^h, counting algebraic multiplicity, inside any sufficiently small isolating circle; all of them converge to it.
3. After the cellwise embedding specified below, the corresponding Riesz projections converge in operator norm. Thus generalized eigenspaces are correctly approximated, including for defective eigenvalues.
4. No sequence of discrete eigenvalues can converge to a point outside I_lat that is not in σ(S_κ). In particular, every isolated nonreal continuum eigenvalue is spectrally approximated, and there is no nonreal spectral pollution away from the real interval.

This makes no claim of spectral correctness on I_lat, no quantitative convergence rate, and no density or distribution claim for eigenvalues accumulating inside that interval.

## 2. Common Hilbert space and static bounds

Work first in H=L²(R³;C³). Write M and M_h for multiplication by 1_Ω and 1_(Ω_h). Let E_h be the closed space of fields constant on each grid cell, and let P_h be orthogonal projection onto E_h, given by cell averages. The map J_h taking a sequence (u_m) to its cellwise constant field is an isometry from ℓ²(Z³;C³) with norm² h³∑|u_m|² onto E_h. Its adjoint is cell averaging. In particular, P_h=J_hJ_h*.

Set

    D_h = J_h T J_h*,
    B_h = M_h D_h M_h.

Multiplication by M_h commutes with P_h. B_h is the finite static matrix T_0^h on its cellwise constant supported subspace, and is zero on its orthogonal complement. Compression of the quadratic form of T gives

    Λ_- I ≤ B_h ≤ Λ_+ I,
    ||(z-B_h)^(-1)|| ≤ dist(z,I_lat)^(-1),  z∉I_lat.     (3)

The extra zero eigenvalue in the common-space extension causes no problem because 0∈I_lat. Scalar multiplication of the sequence norm by h³ does not change the matrix operator norm.

Let D be whole-space convolution with p.v. K_0. The distribution identity

    -D²(1/(4π|x|)) = p.v. K_0 + (I/3)δ_0

follows, for example, by cubic symmetry and tracing the Hessian. Fourier transformation gives the symbol ξξᵀ/|ξ|²-I/3. Consequently D is bounded selfadjoint and -I/3≤D≤2I/3. Define B=MDM; its restriction to MH is S_0 and its complement is zero. Its spectrum also lies in I_lat.

## 3. Strong convergence of the static part

We prove D_h→D strongly, without asserting operator-norm convergence.

Take φ∈C_c^∞(R³;C³), and let φ_h be its sampled cellwise constant interpolant. Then ||φ_h-φ||₂→0, uniformly with respect to the grid translation. Since ||D_h||≤||T||, it suffices to compare D_hφ_h with Dφ.

Choose a smooth radial cutoff χ_δ, equal to one on |z|≤δ and zero on |z|≥2δ. For every h and δ,

    ∑_{j≠0} h³ K_0(hj) χ_δ(hj) = 0,
    p.v. ∫ K_0(z) χ_δ(z)dz = 0.                       (4)

The lattice sum is finite. Reflections cancel its off-diagonal entries; coordinate permutations make the diagonal entries equal; trace K_0=0 makes each zero. The same argument applies to the integral, or follows from spherical cancellation. Thus no shape-dependent self term is silently discarded.

At a cell center x_m, both the discrete near contribution and the continuum near contribution can be rewritten with φ(x_m-z)-φ(x_m). The Lipschitz bound gives

    |near discrete| ≤ C ||∇φ||∞ h³∑_{0<|hj|≤2δ}|hj|^(-2)
                    ≤ C' ||∇φ||∞ δ,
    |near continuous| ≤ C' ||∇φ||∞ δ.                (5)

The lattice estimate follows by shells of integer radius: the shell j≤|n|<j+1 has O((j+1)²) points, while the summand is O(j^-2). If the radius is below the first lattice shell, the sum is empty.

For fixed δ, the far kernel K_0(1-χ_δ) is smooth near its formerly singular point. On every fixed bounded set of center locations, the far sums are Riemann sums of a smooth function of z with uniformly bounded support and derivatives, and converge uniformly to the far integral. Hence

    sup_{|x_m|≤R}|(D_hφ_h)(x_m)-(Dφ)(x_m)| → 0

by first taking h→0 and then δ→0. Dφ is continuous (indeed smooth), so passing from the value at x_m to its cell's x does not change convergence on bounded sets.

For the tails, choose R larger than twice the support radius of φ. There is a constant independent of small h and lattice translation such that, on cells whose centers lie outside that ball,

    |(D_hφ_h)(x)| + |Dφ(x)| ≤ C(1+|x|)^(-3).

For the discrete term, sum |K_0(x_m-x_n)| |φ(x_n)|h³ over its bounded support; the sampled L¹ norm is uniformly bounded. The displayed tail is square-integrable and its L² mass tends to zero as R→∞. Combining local convergence and the tail proves ||D_hφ_h-Dφ||₂→0. Density and uniform boundedness prove D_h→D strongly on H.

Condition (G) implies M_h→M strongly by absolute continuity of integrals of |u|². Products of uniformly bounded strongly convergent operators therefore give

    B_h=M_hD_hM_h → MDM=B strongly.                  (6)

All B_h and B are selfadjoint. Their adjoints hence converge strongly too. No regularity of unknown eigenfunctions has been assumed.

## 4. Norm convergence of the dynamic part

Direct radial differentiation yields

 K_κ(x) = exp(iκr)/(4πr³)
          [(1-iκr-κ²r²)I + (κ²r²+3iκr-3)eeᵀ].       (7)

The constant and linear Taylor terms of K_κ-K_0 cancel appropriately, leaving

    R_κ(x):=K_κ(x)-K_0(x)
        = -κ²(I+eeᵀ)/(8πr) - iκ³I/(6π) + O(r).       (8)

Thus on any bounded difference set and for fixed κ,

    ||R_κ(x)||_F ≤ C_κ/|x|, x≠0.                     (9)

Here ||·||_F denotes Frobenius norm. The formula also covers κ=0, with R_0=0. The growth of exp(iκr) at infinity is immaterial: only a bounded difference set will be used.

Let C be the integral operator on H with kernel

    c(x,y)=1_Ω(x) R_κ(x-y) 1_Ω(y).

It is Hilbert–Schmidt, because |x-y|^-2 is locally integrable in three dimensions. Let C_h have cellwise kernel

    c_h(x,y)=1_(Ω_h)(x)1_(Ω_h)(y) R_κ(x_m-x_n)

when x∈Q_m^h, y∈Q_n^h, m≠n, and zero when m=n. Then B_h+C_h is exactly the embedded finite matrix T_κ^h, including its omitted diagonal.

We claim

    ||C_h-C||_HS → 0.                               (10)

Here are near-diagonal estimates that justify the claim despite point sampling. If |x-y|<δ, then |x_m-x_n|<δ+√3h. By (9), boundedness of the number of occupied cells times h³, and the same lattice-shell estimate as above,

 ∫∫_{|x-y|<δ} ||c_h(x,y)||_F² dxdy
   ≤ C h⁶ (#I_h) ∑_{0<|hj|<δ+√3h}|hj|^-2
   ≤ C'(δ+h).                                      (11)

The corresponding continuum integral is ≤C'δ. On a fixed complement of this diagonal neighborhood, R_κ is uniformly continuous; center-to-point differences tend uniformly to zero. The two masks also converge in measure by (G); the product masks converge in L² on their common bounded support. Therefore the far kernels converge in L². Taking h→0 and then δ→0 proves (10). Equivalently one can use a smooth cutoff to avoid the boundary |x-y|=δ.

In particular C_h→C in operator norm, and C is compact. This compactness concerns only the difference K_κ-K_0, not the strongly singular original operator.

## 5. Compact resolvent factorization

Set

    S=B+C,   S_h=B_h+C_h,
    R(z)=(z-B)^(-1),   R_h(z)=(z-B_h)^(-1),  z∉I_lat.

On MH, S is precisely S_κ; on its complement it is zero. On the finite supported cellwise space S_h is T_κ^h; on its complement it is zero. Thus their nonzero spectral data outside I_lat are the desired data.

For every compact G⊂C\I_lat, (3), (6), and the resolvent identity imply R_h(z)→R(z) strongly, uniformly in z∈G on each fixed vector. Pointwise convergence follows from

    R_h(z)-R(z)=R_h(z)(B_h-B)R(z).

Uniformity follows from uniform resolvent bounds and equicontinuity on G (or a finite net). Since R_h(z)*=R_h(conjugate z), the adjoints also converge strongly, uniformly on compact sets on each vector.

We use the elementary compact-multiplication fact: if X_h→X strongly with uniformly bounded norms and K is compact, then ||(X_h-X)K||→0. Approximate K in norm by finite-rank operators to prove it. If the adjoints also converge strongly, then ||K(X_h-X)||→0 as well. Uniform versions hold on compact parameter sets, by finite-net approximation of a norm-continuous compact-operator family.

It follows from (10) that

    F_h(z):=R_h(z)C_h → F(z):=R(z)C

in operator norm, uniformly on compact subsets of C\I_lat. F and each F_h are analytic compact-operator families. Moreover

    z-S_h = (z-B_h)(I-F_h(z)),
    z-S   = (z-B)(I-F(z)).                           (12)

The analytic Fredholm alternative applies on the connected set C\I_lat; invertibility at sufficiently large |z| follows from boundedness of S. Therefore every spectral point of S in that set is isolated, with finite algebraic multiplicity. This is a standard compact analytic-operator principle: locally split off a finite-dimensional subspace so the complementary block of I-F stays invertible; its finite-dimensional Schur complement is analytic. Its determinant has isolated zeros, and the inverse has finite-rank principal Laurent coefficients. Invertibility somewhere and connectedness exclude the identically singular alternative.

If G is a compact subset of C\(I_lat∪σ(S)), then (I-F(z))^-1 is uniformly bounded there. Uniform norm convergence of F_h and a Neumann series show that (I-F_h(z))^-1 exists and is uniformly bounded on G for all small h. Equation (12) proves conclusion 1 and the no-pollution assertion.

## 6. Norm convergence of Riesz projections, including multiplicities

Choose a positively oriented isolating circle Γ around an eigenvalue λ of S outside I_lat, small enough that its closed interior misses I_lat and all other eigenvalues. On Γ define

    G_h(z)=(I-F_h(z))^-1 F_h(z),
    G(z)  =(I-F(z))^-1 F(z).

Then G_h→G in norm uniformly on Γ, and G(z) is compact and norm-continuous. Resolvent factorization gives

    (z-S_h)^(-1) = R_h(z) + G_h(z)R_h(z),
    (z-S)^(-1)   = R(z)   + G(z)R(z).                (13)

The first terms are analytic inside Γ and integrate to zero. For the second terms,

 ||G_hR_h-GR|| ≤ ||G_h-G|| ||R_h|| + ||G(R_h-R)|| →0

uniformly on Γ. The last term uses compactness of G and **strong adjoint convergence** of R_h. Omitting the adjoint argument here would leave a real gap; ordinary strong convergence alone would not justify right multiplication by a compact factor.

Consequently the Riesz projections

    P_h=(2πi)^(-1)∮_Γ (z-S_h)^(-1)dz,
    P  =(2πi)^(-1)∮_Γ (z-S)^(-1)dz

satisfy ||P_h-P||→0. For small h their difference has norm below one. Restrictions of P_h to ran P and P to ran P_h are then injective: otherwise a nonzero vector is moved by P_h-P by its full norm. Thus their finite ranks are equal. These ranks are precisely the algebraic multiplicity of λ and the total algebraic multiplicities of the discrete eigenvalues inside Γ.

For arbitrarily smaller isolating circles the same argument applies; no-pollution on compact annuli forces all of these discrete eigenvalues to approach λ. Norm convergence of the finite-rank projections also yields the two-sided approximation of their generalized eigenspaces. This proves conclusions 2 and 3. Any putative polluted limit outside I_lat has a small compact neighborhood in the continuum resolvent set, contradicting conclusion 1; this proves conclusion 4.

Finally, ||S_h|| is uniformly bounded by ||T||+sup_h||C_h||, so no discrete eigenvalue escapes to infinity for fixed κ and bounded Ω. All arguments work for real positive κ as well as complex κ: no boundedness of the nonzero-frequency infinite-lattice Toeplitz operator has been assumed.

## 7. Source scope, credit, and limitations

The OWR discussion gives the cubic point-sampling matrix and the shift by I/3, then asks for correct spectral behavior off the static interval. The present theorem supplies that behavior for geometrically consistent particle discretizations, including every bounded Lipschitz particle and every bounded Jordan-measurable particle. The report does not state a boundary regularity hypothesis, and this packet must not be represented as a theorem about every pathological measurable support regardless of how the grid sees it.

Condition (G) is an explicit sufficient geometric condition, not an asserted necessary-and-sufficient criterion for spectral convergence. Without any such control, point sampling can fail even to approximate the underlying volume measure. For example, a countable union of chosen rational grids can be covered by an open subset of a box of arbitrarily small volume; its compact complement has positive volume but contains no grid points. For that set the chosen DDA systems are empty. This illustrates the missing geometric issue; it is not being presented as an exact nonreal-eigenvalue counterexample.

The essential established input is the static lattice operator theorem of Costabel–Dauge–Nedaiasl, not a numerical estimate of Λ_±. The underlying compact-operator and Riesz-projection arguments are standard functional analysis. The proposed contribution is their rigorously justified application to this diagonal-omitting DDA scheme, especially static strong consistency, Hilbert–Schmidt convergence of the dynamic correction, and handling changing particle grids. Independent review and a broader novelty check remain required.

### References

[OWR] M. Costabel, joint work with M. Dauge and K. Nedaiasl, “Stability analysis of the DDA for Dielectric Scattering,” Oberwolfach Report 43/2022, pp. 2580–2582; target Section 4, p. 2582. [DOI](https://doi.org/10.4171/owr/2022/43), [full report](https://publications.mfo.de/bitstream/handle/mfo/3995/OWR_2022_43.pdf?sequence=4).

[CDN] M. Costabel, M. Dauge, K. Nedaiasl, “Stability Analysis of a Simple Discretization Method for a Class of Strongly Singular Integral Equations,” Integral Equations and Operator Theory 95, article 29 (2023), [DOI](https://doi.org/10.1007/s00020-023-02750-7). Full author manuscript inspected: [arXiv:2302.13159v3](https://arxiv.org/abs/2302.13159v3). The numbering cited above is from that v3 manuscript: Sections 1.2 and 1.6, equations (3.38)–(3.42), Lemma 3.14, Proposition 3.15. The publisher metadata/abstract was accessible; its full typeset article was not accessed.
