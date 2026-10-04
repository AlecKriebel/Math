# Turn 3: exact uniform-quarter-flux spectrum and complete holonomy optimization

This turn solves the two remaining loop-phase variables inside the uniform-pi/2 flux class on every L by L torus with L divisible by4. It supplies its thermodynamic energy and explicit error bounds. Arbitrary nonuniform flux patterns are still not compared, so the source problem remains unresolved.

## 1. A four-dimensional magnetic fiber

Write L=4n. Use horizontal phase e^(ia/L) and vertical phase i^x e^(ib/L), where a,b are the two loop holonomies. Every plaquette has flux pi/2. After Fourier decomposition, take

    k_x=(2pi j+a)/L,  0<=j<n,
    k_y=(2pi l+b)/L,  0<=l<L.

Each fiber is the four-site Harper cycle. Its diagonal entries are2cos(k_y+pi x/2), x=0,1,2,3, its three interior off-diagonal hoppings are1, and its closing hoppings are w and conjugate(w), where w=e^(4ik_x). These are the standard magnetic-translation/Harper variables; the characteristic identity below is proved directly rather than imported.

Set A=2cos(k_y), B=−2sin(k_y), so the diagonal is(A,B,−A,−B). Expanding the determinant gives

    det(EI−H)=E⁴−(A²+B²+4)E²+A²B²+2−w−w^(-1)
              =E⁴−8E²+4−2cos(4k_y)−2cos(4k_x).           (1.1)

The supplied Laurent-polynomial determinant checker verifies every coefficient over the Gaussian integers. Let

    f(t)=sqrt(4+sqrt(12+2t)),  −2<=t<=2.

The four eigenvalues are

    ±sqrt(4+sqrt(12+2t)),  ±sqrt(4−sqrt(12+2t)),
    t=cos(4k_x)+cos(4k_y).

The outer negative band is separated from the inner bands by a positive gap: its magnitudes are at least sqrt(4+2sqrt2), whereas the inner magnitudes are at most sqrt(4−2sqrt2). There is exactly one outer-negative eigenvalue per fiber, and exactly N/4 fibers. Thus the quarter-filled sum consists of that entire band, with no sorting ambiguity at the Fermi level.

Since cos(4k_y) repeats four times as l varies, the exact energy density is

    e_n(a,b)=−(1/(4n²)) sum_(j,k=0)^(n−1)
        f(cos((2pi j+a)/n)+cos((2pi k+b)/n)).              (1.2)

## 2. Alternating derivative signs of the band function

For every integer m>=1 and t>−6,

    sign f^(m)(t)=(−1)^(m−1).                             (2.1)

Here the outer square root is evaluated at a positive argument. To prove(2.1), write f=g composed with h, where g(x)=sqrt(4+x), h(t)=sqrt(12+2t). The kth derivative of either square root has sign(−1)^(k−1), with strictly positive magnitude. Repeated differentiation of the composition gives a sum with positive integer coefficients of terms

    g^(k)(h(t)) product_(i=1)^k h^(m_i)(t),
    m_i>=1,  sum_i m_i=m.

This form follows by induction using the product and chain rules. Each term has sign(−1)^(k−1+sum_i(m_i−1))=(−1)^(m−1), so no cancellation occurs. In particular f is strictly increasing and strictly concave, and all higher derivative signs are controlled.

## 3. A Chebyshev divided-difference lemma

Let g be C^n on[−1,1] with g^(n) of one strict sign. Define

    S_n(a)=sum_(j=0)^(n−1) g(cos((2pi j+a)/n)).

This depends only on c=cos(a), because its n arguments, including multiplicity, are the roots of T_n(x)−c. For−1<c<1 the roots x_1,...,x_n are distinct. The leading coefficient of T_n is A_n=2^(n−1) for n>=1 (also1 when n=1). Implicit differentiation gives

    dS_n/dc =sum_i g'(x_i)/T_n'(x_i)
              =g'[x_1,...,x_n]/A_n.                     (3.1)

The final expression is the divided difference of g' of order n−1. Its mean-value formula is g^(n)(xi)/(n−1)! for some xi between the nodes, so(3.1) has the sign of g^(n). The formula for n=1 simply reads g'. Continuity of the multiset of roots extends the monotonicity to c=±1, where some roots coalesce. This proves a global endpoint optimum rather than only a stationary-point test.

For fixed second-coordinate cosine in(1.2), use g(x)=f(x+d). Its nth derivative has sign(−1)^(n−1). Therefore the positive sum of band magnitudes is maximized by

    cos(a)=1 if n is odd;  cos(a)=−1 if n is even.

The same argument then optimizes b, independently of the value already chosen for a. Since energy is the negative of this sum, the **global holonomy minimizers within the uniform-pi/2 class** are

    a=b=0 mod2pi, if n is odd,
    a=b=pi mod2pi, if n is even.                           (3.2)

Strictness gives these loop values as the only ones modulo2pi in this class. Gauge and time-reversal equivalents do not change the spectrum. The result says nothing about flux configurations outside the uniform class.

## 4. Exact small sizes and the Jensen benchmark

For n=1, (3.2) gives the4 by4 optimum from Turn1. For n=2, a=b=pi makes every sampled cosine zero, so every outer negative eigenvalue is−f(0)=−(1+sqrt3). Hence the best uniform-pi/2 density on the8 by8 torus is exactly

    e_2(pi,pi)=−(1+sqrt3)/4.                              (4.1)

For every n>=2 the average of each sampled cosine is0 regardless of a,b. Strict concavity gives e_n(a,b)>=−f(0)/4. Equality requires every sampled cosine in both coordinates to be constant0. This happens at n=2 with the twists above, but is impossible for n>=3 because at least three distinct equally spaced angles cannot all have zero cosine. Thus the Jensen bound is strict for n>=3.

This is a uniform-flux benchmark, not a proof of global8 by8 optimality among nonuniform fields.

## 5. Thermodynamic density and a uniform twist error bound

The limit, independent of a,b, is

    e_* =−1/[4(2pi)²] integral_0^(2pi) integral_0^(2pi)
                 f(cos x+cos y) dx dy.                    (5.1)

Let

    K=1/[2sqrt8 sqrt(4+sqrt8)].

Since f'(t)=1/[2 f(t) sqrt(12+2t)], its derivative is at most K on[−2,2]. Each angular partial derivative of f(cos x+cos y) is therefore bounded by K. Center a square integration cell of side2pi/n at every sample point of the shifted grid in(1.2), using the periodic domain. The mean absolute displacement in one coordinate is pi/(2n), so the difference between the sampled mean and the integral mean is at most K pi/n. Consequently, uniformly in a,b,

    |e_n(a,b)−e_*| <= K pi/(4n)=K pi/L.                   (5.2)

This proves the thermodynamic limit and quantifies why the loop phases cannot change its bulk density, while retaining their finite-volume effect.

Concavity also gives an elementary analytic enclosure. The chord between−2 and2 lies below f, while Jensen bounds the mean above by f(0). Since the mean of cos x+cos y is0,

    −(1+sqrt3)/4 <= e_*
      <=−[sqrt(4+2sqrt2)+2sqrt2]/8.                        (5.3)

Both inequalities are strict for the continuum integral, because the argument is not almost surely constant or supported only at the endpoints. The non-strict version is a convenient certified enclosure. No numerical quadrature or rounded eigenvalue comparison is needed for these statements.

## 6. Verification and remaining gap

verify_turn3.py checks the complete Laurent-polynomial characteristic identity, the Chebyshev substitution identity through degree20, and the divided-difference derivative formula using exact rational nodes and dual-number matrix powers. These finite algebraic checks supplement the all-degree derivative and monotonicity proofs.

We now have a fully specified and holonomy-optimized uniform candidate and a controlled bulk energy. What remains is to prove that no nonuniform phase pattern lowers the actual quarter-filled sorted sum, or to construct and rigorously verify such a competitor. The polynomial-defect minimizer of Turn2 cannot be substituted for that comparison.
