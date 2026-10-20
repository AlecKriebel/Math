# Independent audit: signed quadratic-pencil radius bound

Date: 2026-10-20 UTC.

Audited `ATTEMPT_2.md`, SHA-256 `b1bcd3696822d2dbf959eb33d3f1b27b870114d7243080fe9715fc1f0f911689`, against the exact model and scope in the source/status gate.

## Verdict

**PASS for all stated proved results.** The exact quadrant operator identity, the conjectured lower bound on the radius for -1<=a<0, the polynomial-times-exponential coefficient estimate, the bulk endpoint noninvertibility, and the finite one-sided Abel limit are justified. I found no required correction.

The argument does **not** prove the matching radius upper bound. Its distinction between bulk noninvertibility and singularity of the particular corner matrix element is essential and correct. The finite Abel limit is not a claim of ordinary convergence of the signed series at the boundary or of analyticity there.

## 1. Exact contraction and boundary realization

NW and ES occurrences cannot overlap: their terminal letters W,S are disjoint from their initial letters N,E. The expansion by selected corners therefore defines disjoint two-letter marked blocks.

Contracting NW to (-1,+1) and ES to (+1,-1) preserves validity in the quadrant in both directions. For NW, validity of the final point forces the initial x-coordinate to be at least one; the intermediate N-step is then automatically allowed. For ES, validity of the final point forces the initial y-coordinate to be at least one; the intermediate E-step is automatically allowed. No additional boundary projection or correction is needed.

Macrostep sequences are in bijection with original words together with chosen corners. Other corners created across macrostep boundaries are simply unselected; this does not impair the bijection. Both diagonals have degree two in the individual-step variable. Hence the exact resolvent is I-tA+(1-a)t^2 B, with the sign and length convention stated in the attempt.

## 2. Full-plane form minimum and transition point

Zero extension realizes the quadrant forms as compressions of the full-plane forms. The symbol has the stated cross term 2br^2 cos(theta-phi). After writing the half-sum and half-difference angles, its minimum is the minimum on c in [0,1] of

    1-4rc+4br^2 c^2-2br^2.

The minimizer is c=1 up to r=1/(2b), and c=1/(2br) afterward. This proves both branches of m(r). The smaller zero is on the first branch exactly when b<=3/2. Rationalizing that root yields 1/(2+sqrt(4-2b)); on the second branch the zero is sqrt((b-1)/(2b^2)). Squaring and substituting b=1-a gives exactly the two recovered radius formulas.

The constants used later are valid throughout 1<b<=2: t0<=1/sqrt(8)<1/2, and t0<1/sqrt(2b). At the transition b=3/2 the two formulas agree at t0=1/3. The parity unitary changes the sign of A but not B, so negative real arguments have the same coercivity.

## 3. Complex disk and genuine bounded invertibility

For every unit vector, alpha and beta in the scalar quadratic are real. Real zeros are excluded inside the target interval by real coercivity and parity. If z=x+iy is a nonreal zero, division of the imaginary part by y gives alpha=2b beta x. Substitution into the real part then gives b beta |z|^2=1. Thus beta>0 and |z|>=1/sqrt(2b)>t0. There is no omitted case when beta=0: a linear real polynomial has no nonreal zero.

Factoring the scalar polynomial with constant term 1 gives the claimed lower bound (1-r/t0)^2, uniformly over all unit vectors and |z|<=r<t0. Constant and linear polynomials also satisfy that weaker quadratic bound.

Cauchy–Schwarz converts it to a uniform lower bound on ||K(z)f||. The same argument applies to K(z)^*=K(conjugate(z)), so closed range and a trivial adjoint kernel imply surjectivity. This is the necessary infinite-dimensional step; injectivity alone would not have sufficed. The inverse norm estimate and holomorphy are consequently justified throughout the entire complex disk, not only on the real axis.

The parity identity makes the corner function even. Passing from t to u=t^2 therefore yields the radius bound with the correct half-length normalization. Cauchy's estimate at r=t0 n/(n+1) gives

    |Q_n(a)| <= (n+1)^2(1+1/n)^(2n) rho_*(a)^(-n)
              <= e^2(n+1)^2 rho_*(a)^(-n).

This is a bound on the signed coefficient itself. No coefficient positivity has entered.

## 4. Endpoint Weyl sequence

The listed frequencies attain the symbol minimum zero. A normalized plane wave on an N-by-N square has pointwise size 1/N. The finite-range operator annihilates the wave except within bounded distance of the boundary of that square, leaving O(N) sites of size O(1/N), hence norm error O(N^(-1/2)). The supporting squares can escape both axes, ensuring weak convergence to zero.

This is a valid Weyl sequence for the self-adjoint quadrant operator. It establishes endpoint essential spectrum and noninvertibility. Because the supports escape the corner, it does not establish a singularity of the corner matrix element, exactly as the attempt warns.

## 5. Rank-one estimate and Abel limit

The unilateral-shift identities are exact:

    R*R=2I+B,  RR*=2I+B-P,
    H^2+L^2=2I+B-P/2.

Here P has diagonal value two at the origin, one on the other axis sites, and zero elsewhere; hence P>=2|delta><delta|. Functional calculus for H, whose spectrum lies in [-2,2], reproduces the same scalar minimum m(r). Thus the rank-one domination of K(r) is correct. Inversion reverses the positive-operator order and yields the stated corner bound.

At r=t0, the regularized corner resolvents increase as epsilon decreases and are bounded by 1/(bt0^2+epsilon), hence have a finite limit. The exact identity

    K(st0)=s^2 K0+(1-s)[(1+s)I-st0 A]

gives the two scalar regularization bounds. The lower scalar epsilon is positive because 1+s-4st0 >= min(1,2-4t0)>0. After inversion, the bounding corner elements are s^(-2)G(epsilon_+/s^2) and s^(-2)G(epsilon_-/s^2); both tend to the same finite limit. This proves the asserted Abel limit, without any monotonicity assumption on Q(a,r^2).

## 6. Final factorization and remaining scope

Expanding br^2(R-1/(br)I)^*(R-1/(br)I) and using R*R=2I+B yields exactly the displayed factorization. On the lower branch its scalar remainder vanishes at t0. The multiplier parameter is alpha=sqrt(2/(b-1)), ranging from 2 to sqrt(2), as stated. The Hardy-space identification is the usual coefficient-space unitary identification, so this is a quadrant identity rather than a heuristic Fourier replacement.

No conclusion about nonanalyticity of the corner element follows just from this factorization. The remaining task is correctly identified as a threshold-coupling/nonanalyticity argument for the varying pencil. A claim that the full negative-parameter radius conjecture is solved would exceed the audited result.

