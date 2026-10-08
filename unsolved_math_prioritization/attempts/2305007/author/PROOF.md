# Supporting mathematics and the imported theorem boundary

## 1. Exact question and conventions

Write Delta = {z in C : |z|<1} and let f(z)=sum_{n>=0} a_n z^n be holomorphic on Delta. No univalence, covering-map, or finite-valence assumption is imposed.

For any nonempty proper open set Omega in C, put

    rho_Omega(w) = dist(w, C \ Omega) if w is in Omega,
                   0 otherwise,
    d_Omega(r) = sup_{|w|=r} rho_Omega(w).

Equivalently d_Omega(r) is the supremum of radii of open Euclidean disks, centered on the circle of radius r, that are contained in Omega. Using a supremum accommodates the source's informal word “largest.” For a nonconstant f, let d_f=d_{f(Delta)}. A constant f already has all positive-index coefficients zero.

The suggested implication is

    d_f(r) -> 0 as r -> infinity  ==>  a_n -> 0 as n -> infinity.    (Q)

It is essential that r in the hypothesis is a radius in the value plane, not a radius tending to one in the input disk.

## 2. A completely proved positive omitted-value condition

**Proposition.** Suppose f(Delta) lies in a horizontal strip

    {w : |Im w-c| <= M}, with c real and M finite.

Then sum_{n>=1}|a_n|^2 <= 2M^2, in particular a_n -> 0.

**Proof.** Set g=f-ic and b_0=g(0). On every input circle |z|=t<1, the imaginary part v of g is bounded in absolute value by M. The uniformly convergent power series on that circle gives the Fourier expansion

    v(t e^{i theta}) = Im b_0
        + sum_{n>=1} [a_n t^n e^{in theta}
                      - conjugate(a_n) t^n e^{-in theta}]/(2i).

Orthogonality of distinct Fourier modes therefore gives

    (1/(2pi)) integral_0^{2pi} v(t e^{i theta})^2 dtheta
       = (Im b_0)^2 + (1/2) sum_{n>=1}|a_n|^2 t^{2n}
       <= M^2.

Let t increase to one and use monotone convergence for the nonnegative series. The result follows, and in fact the sharper bound is 2[M^2-(Im b_0)^2]. This condition constrains the omitted set to contain both complementary half-planes; it allows f to be unbounded. For example log((1+z)/(1-z)), with the logarithm on the right half-plane, has imaginary part in (-pi/2,pi/2) and is unbounded on the positive radius. The argument is elementary and classical, with no priority claim. QED.

## 3. The one non-elementary imported result

Use the following established result in precisely the form reported by Hayman and Lingham, Update 5.5, with its direct application in Update 5.40:

**Fernández capacity-zero obstruction (attributed, 1984).** If D is a planar domain and C\D has logarithmic capacity zero, there exists a holomorphic f:Delta -> D whose Taylor coefficients do not tend to zero.

Reference: J. L. Fernández, *On the growth and coefficients of analytic functions*, Annals of Mathematics (2) 120(3) (1984), 505-516, DOI https://doi.org/10.2307/1971085. The article's publisher record was checked. The actual theorem and proof in that article were unavailable in this investigation; reliance is on the explicit report in the original problem collection. Thus the consequence below is a deduction from an attributed classical theorem, not a self-contained independent proof of the analytic existence assertion.

## 4. An explicit domain satisfying the suggested geometry

For each integer m>=1 define

    E_m = {sqrt(m) exp(2pi i j/m) : j=0,...,m-1},
    E = union_{m>=1} E_m,
    D = C \ E.

**Lemma 1.** E is nonempty, countable, closed and locally finite; D is a domain and E has logarithmic capacity zero.

**Proof.** Each E_m is finite. A bounded disk of radius R meets only those E_m with m<=R^2, so it meets E in a finite set. This establishes local finiteness and closedness. D is open and nonempty.

To see path connectedness directly, join any two points of D by a line segment. That compact segment meets only finitely many points of E. Around those points choose sufficiently small disjoint disks containing no other E-points, avoiding both endpoints. Replace the portions of the segment inside these disks by arcs on the disk boundaries. The resulting path lies in D. Therefore D is connected.

Every compact subset K of E is finite by local finiteness. A nonempty finite set has zero logarithmic capacity: any probability measure supported on it has an atom, so its logarithmic energy has an infinite positive diagonal contribution. The kernel's negative part is bounded on K x K, so this contribution cannot be canceled. Thus its minimum logarithmic energy is +infinity and its logarithmic capacity is zero. The capacity of E, understood by compact exhaustion (equivalently polarity here), is consequently zero. QED.

**Lemma 2.** For every w with r=|w|>=1,

    dist(w,E) <= (1+pi)/r.

**Proof.** Take m=ceil(r^2), R=sqrt(m), and write w=r exp(i theta). Select a j modulo m whose angle 2pi j/m differs from theta, modulo 2pi, by at most pi/m. Set e=R exp(2pi i j/m) in E_m. The triangle inequality and |exp(i x)-exp(i y)|<=|x-y| give

    |w-e| <= (R-r)+R*pi/m.

Since R>=r and m-r^2<1 (or equals zero at an integer),

    0 <= R-r = (m-r^2)/(R+r) <= 1/r,
    R/m = 1/sqrt(m) <= 1/r.

Substitution proves the bound. The estimates also hold at the integer-square thresholds, where the radial difference is zero. QED.

**Corollary 3.** D is an unbounded Bloch domain, and d_D(r)->0.

**Proof.** Lemma 2 bounds d_D(r) by (1+pi)/r for r>=1. For |w|<=1, the E-point 1 gives dist(w,E)<=|w-1|<=2. Hence every disk contained in D has radius at most max{2,1+pi}. D is unbounded since deleting a locally finite point set cannot exhaust any open annulus. QED.

## 5. Consequence for the proposed implication

Apply the attributed Fernández theorem to the domain D in Lemma 1. It yields a holomorphic map f:Delta->D with coefficients not tending to zero; such an f is necessarily nonconstant. Write Omega=f(Delta), an open set by the open mapping theorem. Because Omega is contained in D, every disk contained in Omega is contained in D. Hence

    0 <= d_f(r) <= d_D(r) <= (1+pi)/r, r>=1.

Thus d_f(r)->0 although a_n does not tend to zero. This is the negative answer to (Q), conditional only on the precisely identified published theorem. The function f is existential here; no explicit formula or coefficient sequence for it is supplied.

This does not contradict a vanishing-coefficient theorem for the universal covering map of D. A statement about that particular covering function does not imply the same assertion for all holomorphic maps into D. Coefficientwise decay is not automatically inherited under arbitrary holomorphic subordination.

## 6. Why no common decay rate exists even in the bounded subclass

**Proposition.** For every sequence epsilon_n>0 tending to zero, there exists a holomorphic f with |f(z)|<=1 on Delta and coefficients a_n for which a_n/epsilon_n is unbounded.

**Proof.** Choose strictly increasing positive integers n_k with epsilon_{n_k}<=4^{-k}. Set

    f(z)=sum_{k>=1} 2^{-k} z^{n_k}.

The series converges uniformly on the closed unit disk by the Weierstrass test and has modulus at most sum 2^{-k}=1. Its n_k-th coefficient is 2^{-k}, so a_{n_k}/epsilon_{n_k}>=2^k. The other coefficients are zero. All coefficients still tend to zero. QED.

This proves failure of a single prescribed rate over the bounded unit ball. It does not assert that every possible omitted-value restriction is incapable of stronger conclusions; some restrictions can force constancy or other stronger behavior.
