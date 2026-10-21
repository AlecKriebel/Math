# Independent sufficient numerical witness

This is an audit computation, not a replay of Maple or a reconstruction of every printed Schubert coefficient. Run `python3 COMPUTATION.py`; the program uses only the Python standard library and emits `COMPUTATION_RESULT.json`. All arithmetic is exact. It independently verifies a sufficient nondivisibility input of the published Spin17 argument.

Let Y=IG(5,16) be the symplectic isotropic Grassmannian, T its rank-5 tautological bundle, and let x1,...,x5 be the roots of T. Write x=sum(xi); y1,y2,y3 are the remaining symplectic root coordinates. The published Appendix A polynomial is

    a = product_(s1,s2,s3 in {+1,-1}) (x+s1*y1+s2*y2+s3*y3).

It has degree 8 and equals 2^8*ztilde, since the eight factors defining ztilde are half these factors. The program does not enter the source's Schubert output.

The checkable integer obtained here is

    I = integral_Y a^3 c2(T)^9 c3(T)
      = -14668659594398531584
      = 2^22 * (-3497280977821).

The quotient is odd. If a^3 were divisible by 2^23 in the integral Chow ring, every pairing with an integral complementary class would be divisible by 2^23. This pairing disproves that divisibility. It establishes v2(a^3)<=22. It does not establish the reverse inequality for the class or the full printed expansion.

## Method 1: exact localization

The fixed points are signed 5-subsets of eight weights, hence C(8,5)*2^5=1792 points. At one fixed point, write the selected weights as xi and the three unselected positive weights as yj. The tangent Euler class is

    D_C = product_(i<=j)(-xi-xj)
          * product_(i,j,s=+1,-1)(s*yj-xi).

The tangent description is Sym^2(T*) plus Hom(T,T-perp/T); its rank is 15+30=45. Equivalently, Y is the regular zero locus of the alternating-form section of wedge^2(T*) on Gr(5,16). At every enumerated fixed point the program checks that the ordinary Grassmannian tangent Euler class divided by the normal Euler class equals D_C.

The integration formula is sum a^3*e2(x)^9*e3(x)/D_C. It is a homogeneous expression of degree zero, so the exact sum is constant. The program obtains I for weights (1,2,3,4,5,6,7,8), (1,3,5,7,11,13,17,19), and their listed doubled-weight control. None of the tangent denominators vanishes.

The standard localization theorem is a literature input, authenticated here in Edidin-Graham, arXiv:alg-geom/9508001v2, Corollary 1 and Proposition 5, printed p.9. It is not reproved by numerical agreement across weights. The integer I, rather than a modular residue obtained by division in a finite field, is computed before the valuation is taken.

## Method 2: integer Grassmannian multiplication

This calculation has no localization denominators. In ordinary Chow theory the trivial ambient symplectic bundle gives

    product_i(1-xi^2*t) * product_j(1-yj^2*t) = 1.

Let Hj=h_j(x1^2,...,x5^2). The elementary symmetric functions of the yj^2 become -H1,H2,-H3. Expanding the eight-factor product gives

    a = x^8 +4H1*x^6 +(6H1^2-8H2)*x^4
        +(4H1^3-16H1*H2+64H3)*x^2 +(H1^2-4H2)^2.

Newton identities express this as the 15-term integer polynomial in c1,...,c5 listed in the result JSON. Its coefficients and all subsequent products are computed, not transcribed from the paper.

Push Y into Gr(5,16). The normal Euler class is

    product_(i<j)(-xi-xj) = product_(i<j)(xi+xj)
                         = s_(4,3,2,1,0)(x).

The last identity follows directly from the ratio of the two alternant determinants with exponents (8,6,4,2,0) and (4,3,2,1,0). The ambient top degree is 55; the class a^3*c2^9*c3 has degree 45 and the normal class has degree 10. The program multiplies elementary symmetric functions by Schur functions using the vertical-strip Pieri rule, retaining only partitions inside the 5 by 11 rectangle. The coefficient of s_(11,11,11,11,11) is -I. The sign changes because the computation is in roots of T whereas the usual positive Schubert convention uses T*, and total degree 55 is odd. This integer method independently returns I.

The Grassmannian Chow interpretation of Schur classes, regular-zero-locus formula, and Pieri rule remain standard theorem inputs. The code does not prove them. It implements a different arithmetic mechanism from the fixed-point sum and from the source's divided-difference/Schubert package.

## Connecting only the necessary upper bound

The published Proposition 3.4 establishes that ztilde is a rational integral class on generic Spin17 OG5; tautological Chern classes are rational as well. That rationality argument remains a literature dependency, including its use of the K-theory theorem for strongly inner flags.

Odd-orthogonal OG(5,17) has the same fixed points. Its tangent weights replace the five long roots -2xi by -xi, so D_C=2^5*D_B. Thus the rational integral zero-cycle

    ztilde^3*c2(T)^9*c3(T)

has degree

    2^5 * I/2^24 = I/2^19
                 = -27978247822568
                 = 8*(-3497280977821).

The program also checks this directly by exact localization with D_B. Its 2-adic valuation is 3. The index of an orthogonal Grassmannian is a power of two, since the form splits over a multiquadratic extension. Consequently the generic Spin17 OG5 index divides 8. This verifies the sufficient upper-bound mechanism without computing the complete Chow image, the exact lower index bound, or all coefficients of a^3. Alternatively, Theorem 4.1 applies with n=8,m=5,l=3,j=3 and gives deficiency at least 24-22=2, hence the same bound.

Generic-index divisibility applies this bound to any Spin17 form. The flag map OG_(4,5)->OG5 has projective-space Grassmannian fibers and preserves index; its other projection to OG4 shows ind(OG4)|ind(OG5). A 17-dimensional subform of an 18-dimensional Clifford-trivial form gives an inclusion of fourth Grassmannians. These two steps yield the sufficient 18-dimensional fourth-Grassmannian bound. The published Spin18 result states the same bound directly.

## Controls and rejected arithmetic mutants

The localization implementation reproduces projective-space degree 1, LG(2,4) degree 2, IG(2,6) degree 14, and LG(3,6) degree 16. A target numerator of degree 43 integrates to zero on the 45-dimensional variety. The tangent description agrees with the ambient/normal description at every target fixed point. The two target methods agree exactly.

Omitting the normal Euler class in the ambient-Grassmannian method gives zero instead of I. Omitting the factor 2 in each long tangent root multiplies I by 32 and changes its valuation to 27; this is rejected by the independent Pieri value and the small projective-space controls. These are real executable mutations recorded in the result JSON, not hypothetical assurances.

No complete class-level valuation, independent Maple run, proof-assistant verification, or proof of all cited background theorems is claimed. No source-author code was downloaded or executed.

Root tooling feedback before sealing led to replacement of every validation assertion by an explicit exception guard. The mathematical mechanisms and pairing predated that feedback. TOOLING_VALIDATION.json records identical normal/-O/-OO outputs and live false-guard checks in all three modes.
