# A computer-assisted counterexample for the symmetric Sigma neighborhood

Problem 2306113 / AMR-022-6113, Hayman–Lingham Problem 6.113.
Date: 2026-10-08 UTC. Authored mathematical candidate; independent acceptance pending.

## Result and source qualification

With the explicitly defined symmetric neighborhood below, the proposed inclusion is **false**, already for x=0 and the positive parameter rho=1/1000. A polynomial g of degree 10 and an explicitly defined normalized univalent function F satisfy the neighborhood condition everywhere in the unit disk, while their Hadamard product vanishes at r=999/1000. In particular the center-case inclusion in Problem 6.112 is false under the same definition.

The source qualification matters. The inspected 2018 arXiv v2 HTML and PDF both have an unmatched vertical bar and parenthesis in the second summand defining Sigma in Problem 6.112. This report uses the symmetric repair

    |h'(z)-h(z)/z| + |h'(z)+h(z)/z| < 2 delta,
    h=g-f, for every z in D.

The 1989 Sheil-Small–Silvia article's publisher metadata was inspected, but its full text was not obtained. Thus this is a full proof for the displayed definition; identification of that definition with the proposers' original intended definition remains a separately stated source-verification dependency. The malformed expression is not silently treated as an independently verified correction.

The exact proof combines elementary holomorphic mapping arguments with a finite rational certificate and an explicit all-circle error bound. It is not merely a sampled numerical counterexample. It is not a formally verified theorem-prover certificate, and no novelty or current-literature completeness claim is made.

## 1. Definitions and exact claim

Let D={z in C: |z|<1}. Let A consist of analytic functions on D with f(0)=0 and f'(0)=1, and let S be its univalent subclass. For power series, the Hadamard product is coefficientwise multiplication. Here S* is the Hadamard dual

    S*={g in A : (g*F)(z) != 0 for every F in S and every 0<|z|<1}.

It is not notation for the class of starlike functions. Denote that latter class by St.

For a normalized difference h, necessarily h(0)=h'(0)=0, set

    P_h(z)=h'(z)+h(z)/z,
    M_h(z)=h'(z)-h(z)/z,
    s_h(z)=(|P_h(z)|+|M_h(z)|)/2.

The quotient at zero is its removable analytic extension. The symmetric neighborhood used in this report is

    Sigma_delta(f)={f+h in A : s_h(z)<delta for all z in D}.

This is a pointwise strict inequality on the open disk; it need not assert a strict inequality for the supremum at the boundary. Our witness satisfies the stronger strict uniform bound.

The coefficient neighborhood instead imposes sum_{n>=2} n|[z^n]h|<=delta. Those two conditions must not be interchanged.

Problem 6.113 asks whether, for every complex x and real rho with |x|<=rho<=1 and gamma=(1+rho)^(-2),

    Sigma_gamma(z/(1-xz)) is contained in S*.

We use the permitted pair x=0, rho=1/1000, so gamma=1000000/1002001.

## 2. An explicit member of S

For |u|=1, define

    K_u(z)=z/(1+u z)^2.

It is injective on D. Indeed K_u(z)=K_u(w) implies

    (z-w)(1-u^2 z w)=0,

and the second factor is nonzero on D x D. Its image is

    Omega_u=C \ {t/u : t>=1/4}.

Here is also a direct verification of the image description and inverse. For y in Omega_u, let s be the principal square root of 1-4u y. Then Re s>0, and

    J_u(y)=(1-s)/(u(1+s))

belongs to D and satisfies K_u(J_u(y))=y. Conversely, for z in D,

    1-4u K_u(z)=((1-u z)/(1+u z))^2,

where the fraction has positive real part. Thus the same square-root branch gives J_u(K_u(z))=z. These identities prove both assertions without importing a univalence theorem.

For a real 0<q<1, q Omega_u is contained in Omega_u: the excluded ray for q Omega_u begins at q/(4u), closer to zero. Therefore

    Phi_{q,u}(z)=J_u(q K_u(z))

is a holomorphic injective self-map of D, with Phi(0)=0 and Phi'(0)=q.

Use the exact constants

    q1=63/80,                 q2=2/25,
    u1=-1,
    u2=(-39951-2800 i)/40049,
    u3=(-621+100 i)/629.

All three u_j have modulus one, by integer arithmetic. Define

    F(z)=K_{u3}(Phi_{q2,u2}(Phi_{q1,u1}(z)))/(q1 q2).

The composition is holomorphic and injective on D. Its value at zero is zero, and its derivative there is q1 q2 divided by q1 q2. Consequently F belongs to S. This conclusion is global; no finite coefficient list is used to infer univalence.

Write F(z)=z+sum_{n>=2} a_n z^n.

## 3. The exact polynomial perturbation and scalar

Let h(z)=sum_{n=2}^{10} c_n z^n. The following integer pairs specify c_n as (A_n+i B_n)/1000000:

| n | A_n | B_n |
|---|---:|---:|
| 2 | 154786 | 220683 |
| 3 | 33016 | -51407 |
| 4 | 11233 | -46494 |
| 5 | 9231 | -29408 |
| 6 | 12204 | -19762 |
| 7 | 10737 | -12877 |
| 8 | 12351 | -7915 |
| 9 | 15523 | -15643 |
| 10 | 10090 | 33865 |

Set

    r=999/1000,
    L=sum_{n=2}^{10} c_n a_n r^(n-1),
    g(z)=z-h(z)/L.

This defines L as a complex number, not its real part or modulus. Every coefficient a_n required here is Gaussian rational, as shown in Section 4. In particular L and all coefficients of g are exact Gaussian rationals. The certificate proves

    Re L > 2517/2500 = 1.0068.                         (1)

For orientation only, Re L is approximately 1.006803223324637 and Im L approximately -0.000314035248335046. Decimal values are not used in any certificate comparison.

Section 5 proves

    sup_{|z|<=1} s_h(z)
       <= 513446291949/512000000000
       < 251/250 = 1.004.                             (2)

Since |L|>=Re L, equations (1) and (2) imply

    s_{-h/L}(z) < (251/250)/(2517/2500)
                 = 2510/2517
                 < 1000000/1002001 = gamma.

The last inequality is an integer comparison. Thus g belongs to Sigma_gamma(z), and also to Sigma_1(z).

On the other hand, coefficientwise multiplication gives exactly

    (g*F)(r)=r-(h*F)(r)/L
            =r-rL/L=0.

As F belongs to S and 0<r<1, g does not belong to S*. This disproves the parameterized inclusion for the displayed symmetric definition. QED, subject to the exact certificate proved and verified below.

## 4. Exact coefficient calculation

All power-series calculations in this section may be performed modulo z^11, because later terms cannot affect earlier coefficients in compositions whose inner series has zero constant term.

The expansions used are

    K_u(z)=sum_{n>=1} n(-u)^(n-1) z^n,
    J_u(y)=sum_{n>=1} C_n u^(n-1) y^n,
    C_n=(1/(n+1)) binom(2n,n).

The inverse-series formula follows either by expanding the square root in Section 2 or by solving the quadratic equation K_u(J_u(y))=y and choosing J_u(0)=0, J_u'(0)=1. Consequently

    Phi_{q,u}=J_u composed with (q K_u),
    F=(q1 q2)^(-1) K_{u3} composed with Phi_{q2,u2}
                                       composed with Phi_{q1,u1}

are obtained by finite sums and products of rational pairs. The supplied verifier uses Fraction for both real and imaginary parts. In addition to constructing each inverse composition, it independently checks, through degree 10,

    K_u composed with Phi_{q,u}=q K_u.

The verifier calculates L from the nine coefficients of h, the exact ten coefficients of F, and the rational r. Its exact real part is N/D, where

    N=405060549603285758485667422940782591483247763782798484017289213787330309559159416000967760687419806896501225537,
    D=402323453301734918728627923217998774858332677743835558400000000000000000000000000000000000000000000000000000000.

The integer inequality 2500 N > 2517 D proves (1). No truncation error appears in L: h is a degree-10 polynomial, so only these coefficients enter its Hadamard product with F.

## 5. Exact all-circle certificate

This section supplies the analytic justification that turns finite rational checks into the universal inequality (2).

For real theta, P(theta)=P_h(exp(i theta)) and M(theta)=M_h(exp(i theta)). Their polynomial expansions are

    P(theta)=sum_{n=2}^{10}(n+1)c_n exp(i(n-1)theta),
    M(theta)=sum_{n=2}^{10}(n-1)c_n exp(i(n-1)theta).

The reverse triangle inequality and differentiation imply that s_h(exp(i theta)) is Lipschitz in angular distance, with constant at most

    B0=sum_{n=2}^{10}n(n-1)|c_n|
       <= sum_{n=2}^{10}n(n-1)(|Re c_n|+|Im c_n|)
       = 6004273/500000.                                (3)

Take N0=8192 and the rational unit-circle points

    v_j=((1-t_j^2)+2i t_j)/(1+t_j^2),
    t_j=j/N0,  -N0<=j<=N0,

together with their negatives. There are 32770 listed points, including harmless repetitions at the endpoints. The v_j cover the right semicircle with angular parameter theta(t)=2 arctan(t). Since |theta'(t)|<=2, every point of that semicircle is within angular distance 1/N0 of a listed v_j. Their negatives give the same coverage of the other semicircle. This is a proved covering statement, not an empirical spacing check.

At each listed point, P_h and M_h are evaluated by exact Gaussian-rational Horner arithmetic. For a nonnegative rational X, the code constructs a rational upper bound for sqrt(X) by choosing the smallest nonnegative integer k such that

    k^2 >= 10^18 X,

and using k/10^9. It implements this with integer square roots and then checks the defining squared inequality. Applying this separately to |P_h| and |M_h| and taking half their sum yields, at every listed point, an exact upper bound no larger than

    500679451/500000000.                                (4)

Combining (3), (4), and the angular covering,

    s_h(exp(i theta))
      <= 500679451/500000000
          + (6004273/500000)/8192
       = 513446291949/512000000000
       < 251/250.

This proves the bound on the entire unit circle, not just on the grid.

Finally the bound holds on the closed disk. One way to see this without a separate subharmonic theorem is to use

    |P_h(z)|+|M_h(z)|
       = max_{|alpha|=|beta|=1}|alpha P_h(z)+beta M_h(z)|.

For each alpha,beta the expression inside the modulus is an analytic polynomial. The maximum-modulus principle applies, and taking the maximum over alpha,beta proves the disk bound (2).

## 6. Exact reduction relating Problems 6.112 and 6.113

This reduction is independent of the particular counterexample. Under the symmetric definition, the full parameterized assertion is equivalent to Sigma_1(z) subset S*.

The forward direction follows by x=rho=0. For the converse, assume the center inclusion. If h obeys s_h<1 and F belongs to S, put H(w)=(h*F)(w)/w, extended at zero by zero. If |H(w0)|>1, the scalar lambda=-1/H(w0) has |lambda|<1. Then z+lambda h belongs to Sigma_1(z) but its Hadamard product with F vanishes at w0, contradiction. Thus |H|<=1, and Schwarz's lemma gives |H(w)|<=|w|.

For g=f_x+h in Sigma_gamma(f_x), apply the preceding argument to h/gamma. The classical normalized-univalent growth lower bound gives, for w!=0,

    |(f_x*F)(w)/w|=|F(xw)/(xw)|
       >= (1+|xw|)^(-2),

with the value 1 when x=0. Meanwhile |(h*F)(w)/w|<=gamma|w|<gamma and gamma<=(1+|xw|)^(-2). Hence g*F cannot vanish. The converse uses this classical growth theorem as an imported dependency; the explicit counterexample in Sections 2–5 does not use it.

## 7. Scope, dependencies, and remaining acceptance work

The mathematical counterexample relies only on the elementary mapping and power-series calculations in Sections 2–5, integer/rational arithmetic, and the maximum-modulus principle. It does not import de Branges' theorem, a characterization of a convex hull, a Loewner existence theorem, numerical ODE accuracy, or optimizer success. Those tools or theorems were useful in exploratory routes but are unnecessary for validating this witness.

Remaining acceptance tasks are independent mathematical/reproducibility review and primary-source reconciliation of the malformed neighborhood definition. They are not gaps in the proof of the explicitly displayed symmetric statement. This main proof makes no claim about alternative repairs. The separately proved ALTERNATIVE_REPAIR.md supplement certifies the same witness for the particular inner-absolute-value repair stated there; neither document claims to exhaust possible source interpretations.

### Primary references

- W. K. Hayman and E. F. Lingham, Research Problems in Function Theory (New Edition), arXiv:1809.07200v2, Problems and Updates 6.111–6.113, printed pages 156–157: https://arxiv.org/html/1809.07200v2 . The inspected update reports no solution known to its editors at that time; this is not a 2026 open-status certification.
- T. Sheil-Small and E. M. Silvia, Neighborhoods of analytic functions, Journal d'Analyse Mathématique 52 (1989), 210–240, DOI https://doi.org/10.1007/BF02820479 . Publisher metadata inspected; full text not obtained. No theorem or corrected formula is attributed to an uninspected page.
- D. J. Hallenbeck, Convex hulls and extreme points of families of starlike and close-to-convex mappings, Pacific Journal of Mathematics 57 (1975), 167–179, Theorem 8: https://msp.org/pjm/1975/57-1/pjm-v57-n1-p18-s.pdf . Relevant to a discarded convex-hull route, not a dependency of the counterexample.
- L. de Branges, A proof of the Bieberbach conjecture, Acta Mathematica 154 (1985), 137–152, DOI https://doi.org/10.1007/BF02392821 . Relevant to the auxiliary coefficient route, not a dependency of the counterexample.
