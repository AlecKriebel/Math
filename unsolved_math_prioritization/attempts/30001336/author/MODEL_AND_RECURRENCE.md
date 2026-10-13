# Exact model, operators, and coefficient recursion

## 1. Source and normalization

The source is Wulkenhaar's report with Grosse, *Progress in solving a noncommutative QFT in four dimensions*, in OWR 41/2009, DOI 10.4171/owr/2009/41. Its full derivation is Grosse–Wulkenhaar, arXiv:0909.1389v1, equations (18)–(19), (25), (29), (42)–(46). The MFO report PDF uses provisional printed page 538 for the conjecture; this is PDF page 50. Publisher pagination is 2318–2321 for the contribution. The question concerns each coefficient of a formal perturbation expansion, not existence, summability or uniqueness of an analytic nonperturbative function.

The action is the real quartic scalar model on four-dimensional Moyal space at the self-dual oscillator parameter Ω=1. The matrix kinetic term is Z(μ_bare²+|a|+|b|); the vertex is Z²λ. The original two-component matrix-index measure becomes ∫₀^Λ p dp, not the constant-density measure of the 2D model. The mass and wavefunction subtraction is

Γ_ab = Z μ_bare² − μ² + (Z−1)(|a|+|b|) + Γ_ab^ren,
Γ_00^ren=0, ∂Γ_00^ren=0.

There is no independent coupling counterterm in this source's self-dual prescription. Set |a|=μ²α/(1−α), |b|=μ²β/(1−β), with 0≤α,β<1. The dimensionless function here is normalized by

Γ_ab^ren = μ² (1−αβ)/((1−α)(1−β)) (1−1/G(α,β)).

It has G=1 at λ=0. This must not be confused with the unrescaled connected propagator, whose free value is 1/(μ²+|a|+|b|).

## Intended coefficient space and the source convention issue

The short OWR assertion asks whether every g_n is a polynomial with rational coefficients in a,b,A,B and the one-variable rooted-tree integrals evaluated at a and b. The full 2009 paper explicitly admits multiple-zeta constants and trees of at most n vertices. With the rooted kernel defined in ROOTED_KERNEL_PARTIALS.md, this leads to the candidate algebra Z_MZV[a,b,A,B,{I_t(a),I_t(b)}], where Z_MZV denotes the Q-algebra of multiple-zeta values. This is substantially smaller than allowing arbitrary rational functions in a,b or arbitrary operation-labelled tree integrals. The full paper's third-order footnote also singles out the removable divided integral (I(a)−a)/a; the convention issue is disclosed in APPROACHES_AND_GAPS.md and is not treated as a refutation. No unrestricted rational localization is assumed here.

## 2. The full source equation

Write a=α, b=β, D=1−ab, A=(1−a)/D, B=(1−b)/D, C=(1−a)(1−b)/D. For a coefficient function f define

L[f](a)=∫₀¹ (f(a,r)−f(0,r))/(1−r) dr,
M[f](a)=∫₀¹ a f(a,r)/(1−ar) dr,
N[f](a,b)=∫₀¹ (f(r,b)−f(a,b))/(r−a) dr,
y[f]=lim_(a→0) (M[f](a)−L[f](a))/a.

At r=a the divided difference is interpreted by its continuous limit. The subtraction inside L is essential; integrating its two summands separately need not make sense. Endpoint and limit interchanges must be justified for the particular coefficient under consideration.

The exact source equation is

G=1+λ{ A(M[G](b)−L[G](b)−b y[G])
       +B(M[G](a)−L[G](a)−a y[G])
       +B(G(a,b)/G(0,a)−1)(M[G](a)−L[G](a)+aN[G](a,0))
       −aB(L[G](b)+N[G](a,b)−N[G](a,0))
       +C(G(a,b)−1)y[G] }.

The formal quotient is legitimate because G(0,a) has constant coefficient 1. The equation was obtained using symmetry of the physical function; the arguments below do not prove symmetry for arbitrary formal solutions of the displayed equation.

## 3. Exact triangular recursion and its limitation

Put G=Σ_(n≥0) λⁿg_n, g_0=1. Abbreviate L_n=L[g_n], M_n=M[g_n], N_n=N[g_n], y_n=y[g_n], and h_n(a)=g_n(0,a).

Let d_0=1 and d_n=−Σ_(j=1)^n h_j d_(n−j). For n≥1 set q_n=Σ_(j=0)^n g_j(a,b)d_(n−j)(a); set q_0=0. Thus Σλⁿq_n=G(a,b)/G(0,a)−1.

Define S_n(a)=M_n(a)−L_n(a)+aN_n(a,0), and

F_n(a,b)=A(M_n(b)−L_n(b)−b y_n)
         +B(M_n(a)−L_n(a)−a y_n)
         −aB(L_n(b)+N_n(a,b)−N_n(a,0)).

Then

g_(n+1)=F_n+B Σ_(k=1)^n q_k S_(n−k)+C Σ_(k=1)^n g_k y_(n−k).

**Proof.** Formal inverse multiplication gives the recurrence for d. Each source operator is linear when defined coefficientwise. Cauchy products of the two nonlinear terms give the two finite sums. Every term on the right uses only g_0,…,g_n. This proves uniqueness and construction in any coefficient class where these operations actually exist and remain in that class. It does not prove that the desired class is such a class. In particular, it does not establish endpoint convergence, the rooted-tree polynomial assertion, or a nonperturbative fixed point.

At a=0 this gives

h_(n+1)(b)=M_n(b)−L_n(b)−b y_n+(1−b)Σ_(k=1)^n h_k(b)y_(n−k).

Provided the limits and derivatives in this identity exist, induction proves h_n(0)=h_n'(0)=0 for n≥1: the first difference has zero value and zero first derivative by the definition of y_n, and the earlier h_k have both zero. Physical symmetry supplies the corresponding other-variable normalization; it has not been silently inferred from finite tests.

## 4. First nontrivial coefficients, derived using the actual kernels

Let I(a)=−log(1−a), J(a)=K I(a)=Li₂(a)+I(a)²/2, where Kf(a)=∫₀¹ a f(r)/(1−ar)dr. Let z₂=ζ(2). At order zero,

L_0=N_0=0, M_0=I, y_0=1,
g_1=A(I(b)−b)+B(I(a)−a).

Direct integration gives

L_1(a)=(I(a)²+I(a))/a−I(a)−1−J(a),
M_1(a)=(I(a)²+I(a))/a−2I(a)+a−1,
y_1=1,
N_1(a,b)=B[J(a)+J(b)+z₂+I(b)−(I(b)²+I(b))/b],
N_1(a,0)=J(a)+z₂−1.

All expressions at zero mean removable limits. For example,

g_1(a,r)−g_1(0,r)=(1−r)/(1−ar)[I(a)−a−a(I(r)−r)],

which directly justifies convergence of L_1. Integrating this identity gives L_1. For M_1 use (Kf)'(a)=∫f(r)/(1−ar)² dr, J'=I/[a(1−a)], and K(r)=(I−a)/a. Partial fractions in N_1 together with the proved identity D I=J+ζ(2) in ROOTED_KERNEL_PARTIALS.md give its stated formula.

Substitution in the exact recurrence yields

g_2=AB[J(a)−a+J(b)−b+(I(a)−a)(I(b)−b)+ab(z₂+1)]
    +A[bJ(b)−bI(b)]−aAB[I(b)²−2bI(b)+I(b)]
    +B[aJ(a)−aI(a)]−bAB[I(a)²−2aI(a)+I(a)].

This is the previously published second-order answer, not a new resolution. Its boundary is h_2(b)=J(b)−bI(b)−b+b². The verifier checks the rational identity with independent symbols for I,J,z₂, symmetry, endpoint cancellation and the kernel identities. It does not extrapolate from these checks to all orders.
