# Five bounded approaches and their exact conclusions

This file proves the limited claims summarized in RESULT.md. It does not identify a canonical answer to Ohtsuki Problem 7.13. References [S1]–[S7] are defined in SOURCES.md. All mathematical arguments below are analytic or algebraic; no finite numerical test is used to prove an infinite statement.

## 0. Conventions and standard inputs

Fix an integer N>=3, q=exp(2 pi i/N), and q^a=exp(2 pi i a/N) for the rational powers used below. The actual SU(2) level is N-2. Set

  d_j = sin(pi j/N)/sin(pi/N),  1<=j<=N-1,
  theta_j = exp(pi i (j^2-1)/(2N)),
  D_N^2 = sum_j d_j^2 = N/[2 sin^2(pi/N)].

Use the unitary SU(2) theory, normalized to tau_N(S^3)=1. Its unnormalized invariant Z_N has Z_N(S^3)=D_N^(-1), Z_N(S^2 x S^1)=1, and tau_N=D_N Z_N. The modular matrix is S_ab=sqrt(2/N) sin(pi ab/N); all SU(2) labels are self-dual. Standard surgery gives, for positive even p surgery on the unknot,

  tau_N(M_p) = B_p/B_1,
  B_p = sum_{j=1}^{N-1} d_j^2 theta_j^p.

Here B_1 is the positive-blow-up Gauss sum for the chosen modular convention. Its absolute value is D_N. Indeed (S T S)_11 has absolute value S_11 by the modular relation, with T=diag(theta_j) and a modulus-one anomaly; also (S T S)_11=B_1/D_N^2 and S_11=1/D_N. A ribbon convention that inserts (-1)^(j-1) in each twist leaves the even-p numerator unchanged and only changes the explicitly normalized blow-up phase. None of the zero, modulus, or formal quadratic conclusions below depends on that phase. Positive surgery fixes our orientation convention; reversing orientation conjugates the invariant. Some sources denote the oppositely oriented surgery manifold by L(p,1).

These are standard SU(2) modular/surgery facts, used as inputs rather than re-proved as a new construction of the invariant. [S1, section 7.1; S3, sections 1 and 5.] In particular, the quantum dimensions are not normalized colored Jones polynomials equal to 1 on the unknot.

## 1. Polynomial upper bound does not calculate the target

### Proposition 1

If M has a genus-g Heegaard splitting, then |tau_N(M)|<=D_N^g.

### Proof

Let v be the handlebody vector. In the unitary theory the gluing map is unitary up to a scalar of absolute value 1. Therefore

  |Z_N(M)| = |<v,rho(f)v>| <= ||v||^2.

Doubling the handlebody gives #^g(S^2 x S^1). The connected-sum rule is Z_N(A#B)=D_N Z_N(A)Z_N(B), so its invariant is D_N^(g-1). This also gives D_N^(-1) for g=0. Hence ||v||^2=D_N^(g-1), and multiplication by D_N proves the claim. Finally D_N~N^(3/2)/(sqrt(2) pi).

Consequently limsup N^(-1)log|tau_N(M)|<=0 when zeros are assigned log|0|=-infinity. No lower bound follows. Even a nonzero sequence can be exponentially small while satisfying a polynomial upper bound. Nor does this estimate produce a complex Chern-Simons phase. The classical polynomial-bound argument already appears in the optimistic-limit motivation. [S2, introduction.] QED.

## 2. Explicit formal saddle candidates for an even lens surgery

This is a computation inside a specified formal rule, not an assertion that a saddle dominates the actual sum.

For p=8, the surgery numerator can be written exactly as

  B_8 = q^(-1)/(1-q)^2 sum_{j=1}^{N-1} q^(2j^2-j)(1-q^j)^2.

To check this, use d_j=q^((1-j)/2)(1-q^j)/(1-q) and theta_j^8=q^(2(j^2-1)). Their product is q^(2j^2-j-1)(1-q^j)^2/(1-q)^2. The factor outside the sum, including B_1^(-1) if working with tau_N, is retained as the standard surgery prefactor. We do not use an arbitrary exponentially winding logarithm of that prefactor.

The factor (1-q^j)^2 can also be expressed as two copies of (q)_j/(q)_(j-1). Its two positive and two negative dilogarithm contributions cancel under the leading formal rule, because j and j-1 have the same homogeneous linear part. The linear exponent -j enters the amplitude, not the quadratic action. Thus, writing z=q^j and choosing a local lift t=log z, the formal leading potential is

  V_tilde(t)=2t^2,
  exp[N V_tilde(t)/(2 pi i)].

This is exactly the quadratic part of Murakami's prescription, with its branch-correction rule. [S2, section 3.] The exponentiated critical equation is exp(4t)=1. Its lifts are

  t_m=pi i m/2,   m in Z.

Set c=-m and V_m(t)=2t^2+2 pi i c t. Then V_m'(t_m)=0 and V_m''(t_m)=4. Direct substitution yields

  V_m(t_m)=pi^2 m^2/2.

Take m=1 and m=2. Their points are z=i and z=-1, their amplitudes z^(-1)(1-z)^2 are respectively -2 and -4, and neither is zero. Both lie over interior values j/N=1/4 and 1/2. The corresponding critical values are pi^2/2 and 2 pi^2. Their difference is 3 pi^2/2, not an element of 4 pi^2 Z.

Even logarithm-lift ambiguity at a fixed point does not collapse these two classes: replacing m by m+4k changes V_m by 4 pi^2 m k+8 pi^2 k^2, a multiple of 4 pi^2. Thus the two classes remain distinct under this natural period quotient. After division by 2 pi i, the displayed representatives become -i pi/4 and -i pi.

The calculation proves only that the formal critical-point rule for this fixed expression admits these distinct regular outputs. It does not prove both lie on an admissible integration cycle, that either is selected by the source's intended meaning, or that this potential/candidate set is invariant under changing surgery presentation. In particular, it does not prove that the original problem has no possible rigorous formulation. The calculation pinpoints missing selection data even in an elementary Seifert subcase.

## 3. A genuine Seifert zero-subsequence obstruction

### Proposition 2

For M_2, the +2 surgery on the unknot (RP^3 up to orientation),

  tau_N(M_2)=0                         for odd N,
  |tau_N(M_2)|=1/[sqrt(2) cos(pi/(2N))] for even N.

Therefore the ordinary all-level logarithm of tau_N(M_2) does not exist as a sequence of finite complex values. For the extended-real logarithm of its absolute value,

  liminf_N log|tau_N(M_2)|/N=-infinity,
  limsup_N log|tau_N(M_2)|/N=0.

This is a classical calculation, not a new example. [S3, equation (5.12) and its following paragraph.] Here is an elementary verification of the cancellation and modulus.

### Odd N

The summands of B_2 pair under j -> N-j. Quantum dimensions are equal in a pair, and

  theta_(N-j)^2/theta_j^2
    = exp[pi i ((N-j)^2-j^2)/N]
    = exp(pi i N) exp(-2 pi i j)
    = (-1)^N.

For odd N no index is fixed by this involution, so every pair cancels. Since B_1 is nonzero, tau_N=0. Notice that no asymptotic approximation appears here.

### Even N

Put f(j)=exp(pi i j^2/N) and G=sum_{j=0}^{N-1} f(j). Now f is N-periodic. Define

  F=sum_{j=0}^{N-1} sin^2(pi j/N) f(j).

The j=0 term is zero, so F is the numerator sum of interest apart from nonzero scalars. The identity sin^2 x=1/2-(e^(2ix)+e^(-2ix))/4 and completion of the square give

  sum_j f(j)e^(+2 pi i j/N)=e^(-pi i/N)G,
  sum_j f(j)e^(-2 pi i j/N)=e^(-pi i/N)G,
  F=(1-e^(-pi i/N))G/2.

Periodicity justifies both index shifts. Also

  |G|^2=sum_{d=0}^{N-1} exp(pi i d^2/N)
                     sum_{k=0}^{N-1} exp(2 pi i k d/N)=N,

because the inner sum is zero unless d=0. Hence |F|=sqrt(N) sin(pi/(2N)). Since

  B_2=e^(-pi i/N)F/sin^2(pi/N),
  |B_1|=sqrt(N/2)/sin(pi/N),

we obtain

  |tau_N|=sqrt(2) sin(pi/(2N))/sin(pi/N)
         =1/[sqrt(2) cos(pi/(2N))].

This tends to 1/sqrt(2). The two liminf/limsup assertions follow. In Kirby–Melvin's convention tau_N itself, rather than just its absolute value, equals the displayed positive number at even N. We do not need that stronger phase convention for the obstruction. QED.

A logarithm branch cannot repair a zero. Passing to even levels is a different, explicitly restricted question. Multiplication by any nonzero normalization factor preserves the odd-level zero obstruction.

## 4. Exactly what rational-phase expansions imply

### Proposition 3: conditional residue-class logarithmic rate

Suppose a complex sequence has a full finite-phase Poincare expansion

  a_N ~ sum_{s in F} exp(2 pi i N s) sum_{r>=0} c_(s,r) N^(d_s-r/h),

where F is a finite subset of Q/Z, h is a positive integer, and d_s are real. Let L be a common denominator of all s. For a residue a modulo L, combine terms of each power with coefficients exp(2 pi i a s)c_(s,r). If at least one combined coefficient is nonzero, let b N^lambda be the highest surviving power on that class. Then

  a_N=b N^lambda(1+O(N^(-delta)))

on that class for some delta>0, and consequently

  log|a_N|/N -> 0,
  Log(a_N)/N -> 0

there, where Log has argument in any fixed bounded interval of length 2 pi.

### Proof

There are finitely many exponent ladders d_s-r/h. Their union is bounded above and locally finite, so the highest surviving exponent exists. Take the full expansion beyond that exponent and at least one lower step; the Poincare remainder and the discrete gap give the stated relative error. For large N the parenthesized term is nonzero. Then log|a_N|=lambda log N+log|b|+o(1); dividing by N gives zero. The chosen argument is bounded, giving the complex assertion. QED.

If every combined coefficient on a residue class vanishes, a full asymptotic expansion alone supplies no nonvanishing or lower bound there. The sequence might vanish identically on that class, or it might contain nonzero exponentially small terms invisible to all orders. For example 1+(-1)^N is zero on the odd class, while 1+(-1)^N+exp(-N) is exponentially small there and has the same all-orders power expansion. These are abstract sequence controls, not additional WRT examples. Proposition 2 gives an actual WRT zero class.

### Proposition 4: logarithm-lift freedom

Let a_N be any eventually nonzero sequence with Log(a_N)/N -> 0. For any real alpha, set

  ell_N=Log(a_N)+2 pi i floor(alpha N).

Then exp(ell_N)=a_N and ell_N/N -> 2 pi i alpha. Thus an unspecified logarithm for each integer N does not determine a complex limiting rate. If one additionally imposes a particular analytic interpolation and a continuous logarithm, the admissible choices are more restricted; no such interpolation is inferred here.

For an individual phase exp(2 pi i N s) with a polynomial-size nonvanishing amplitude, the phase-unwrapped logarithm naturally suggests 2 pi i s, whereas the principal logarithm divided by N tends to zero. A sum of such phases can cancel. Therefore knowing all terms of a genuine asymptotic expansion is not the same task as specifying one canonical formal critical value.

## 5. A constructive nonvanishing family from identity mapping tori

The source suggests the mapping-torus trace route. For the identity map of a closed genus-g oriented surface Sigma_g, this gives a clean ordinary-limit calculation, without the phase cancellations seen above.

### Proposition 5

For each fixed g>=0, in the normalization tau_N(S^3)=1,

  tau_N(Sigma_g x S^1)=D_N v_g(N)>0,
  log(tau_N(Sigma_g x S^1))/N -> 0.

Here v_0(N)=1, v_1(N)=N-1, and for g>=2,

  v_g(N)=(N/2)^(g-1) sum_{j=1}^{N-1} sin(pi j/N)^(2-2g).

For g>=2 this dimension is Theta_g(N^(3g-3)); accordingly tau_N is Theta_g(N^(3g-3/2)). For g=0 and g=1 the orders of tau_N are respectively N^(3/2) and N^(5/2).

### Proof

The mapping-torus axiom identifies Z_N(Sigma_g x S^1) with the trace of the identity on its state space, hence its dimension v_g(N). There is no projective-map choice for the identity cobordism with the product structure. The displayed formula is the standard SU(2) Verlinde dimension formula, obtained from sum_j S_(1j)^(2-2g); see [S7], equations (1.1)–(1.2) and Theorem 1.4, for a primary proof of the corresponding genus>=2 dimensions. The prefactor is derived from the S-matrix in those equations; the apparent inconsistent exponent in its display (1.5) is not used. The sphere and torus dimensions follow directly from the modular-functor state spaces and also from that sum.

All summands are positive. Set a=2g-2>=2. The j=1 term and sin(pi/N)<=pi/N give

  v_g(N)>=(N/2)^(g-1)(N/pi)^(2g-2).

For m=min(j,N-j), concavity of sin on [0,pi/2] gives sin(pi j/N)>=2m/N. Each m appears at most twice, so

  v_g(N)<=2 (N/2)^(g-1)(N/2)^(2g-2) sum_{m=1}^infinity m^(-(2g-2)).

The series converges, proving the two-sided order. The assertions for tau_N follow from tau_N=D_N Z_N and D_N~N^(3/2)/(sqrt(2)pi). Since these are positive real quantities bounded above and below by fixed powers of N, their ordinary logarithms divided by N tend to zero. QED.

These manifolds are Seifert fibered trivial circle bundles. This is a genuine positive subclass calculation of the ordinary limit, using classical formulas with credit; it is not a theorem selecting the formal optimistic branch for arbitrary Seifert manifolds. Passing from the identity to a general monodromy replaces a positive dimension by a possibly cancelling trace, so this argument does not extend automatically.

## 6. Why no full solution is inferred

Proposition 1 controls growth from above. Proposition 2 blocks the literal all-level logarithm in a real Seifert example. The formal calculation of section 2 exhibits explicit candidate multiplicity. Proposition 5 supplies a positive ordinary-limit subclass. Propositions 3–4 explain precisely why current asymptotic-expansion theorems do not on their own remove the remaining ambiguity. None provides a presentation-independent critical-point selection, an integration-cycle theorem, or an all-Seifert formal invariant. The original target is therefore left unresolved by this packet.
