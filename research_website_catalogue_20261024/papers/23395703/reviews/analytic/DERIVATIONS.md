# Independent analytic reconstruction

## The exact source question

For the homogeneous Jacobian ideal of a characteristic-zero central arrangement, use degree reverse lexicographic order with x1>x2>x3>x4. The conjectural threshold is the least p with x2^p in the generic initial ideal. The authentic BPT notation uses d0=p−1, whereas OWR/PT use the unshifted exponent. The current claim is p=8 together with a minimal generator of degree7 supported in the first three variables and involvingx3.

## 1. Scalar polar system, including its converse

Put f_j=(∂Q/∂j)|_C. Because the ambient factor rowsa_i are constant, differentiation before substitution gives

    Σu_j f_j = Σ_i(a_i·u)∏_(h≠i)L_h.

For a zero linear relation, reduce moduloL_i. The quotient is a domain and every otherL_h has nonzero image by pairwise nonproportionality. Thus L_i dividesa_i·u, so a_i·u=λ_iL_i. Substitution back proves the converse precisely whenΣλ_i=0. This uses no generic-rank sample. For a constant relation, divisibility forcesa_i·u=0; the coordinate factors giveu=0. Thus all four degree6 generators remain independent.

Independence ofX,Y equates the scalars ofX,Y,X−Y,X−2Y. With their common valuea and remaining valuesb,c,d, all relations are exactly

    u=(aX,aY,bZ,cW),
    (a−d)X+(b−d)Z+(c−d)W=0,
    4a+b+c+d=0.

In three variablesX,Z,W are independent; hencea=b=c=d and7a=0. There are no linear relations, giving H3(5,6,7)=(21,24,24).

In two variables the seven pairwise distinct nonzero forms makeX,Z,W span dimension2. Its relation space has dimension1; letρ denote a nonzero relation. Set(a,b,c)=(d,d,d)+tρ. The trace equation7d+t(4ρ_x+ρ_z+ρ_w)=0 has rank1. The map to u is injective: u=0 impliesa=b=c=0 and then d(X+Z+W)=0, whenced=0 andt=0. Thus there is exactly one independent linear binary syzygy.

## 2. Binary colength and shifts

At a projective common zero of all four binary polars, restricted Euler forcesQ|_C=0 because7 is invertible. Exactly oneL_i vanishes. The gradient vector there is the nonzero ambient rowa_i times the product of the other nonzero factors. Contradiction. This holds over an algebraic closure and descends by faithful field extension. ThusI2 has height2 and finite colength.

The four minimal degree6 generators have a graded Hilbert–Burch resolution with three syzygy shifts6+e_i,e_i≥1. The finite-colength Hilbert numerator1−4t^6+Σt^(6+e_i) has a double zero at1; its derivative givesΣe_i=6. Exactly one linear syzygy means exactly onee_i=1; the others are≥2. Therefore the shifts are(1,2,3), and H2(6,7,8)=(3,1,0).

## 3. Compatible open flags over every field in scope

The explicit binary rows are(1,0),(0,1),(1,−1),(1,−2),(2,3),(7,11),(10,14). All21pair determinants are nonzero integers. C0 has determinant1, and its first three columns span the ternary plane w=x+2y+3z. The ternary coordinate XZW determinant is nonzero. All these are polynomial nonvanishing conditions, defining a nonempty open subset ofGL4 overQ and hence over every characteristic-zeroK. The calculations above hold throughout it. Intersecting the generic-initial open set gives the desired generic sections. Infinite-field rational-point density applies to the finite intersection of K-defined opens; no algebraic-closedness assumption onK is needed.

A second independent check of the needed generic dimensions bypasses the shift classification. At the displayed binary flag the degree8 multiplication matrix has a9×9minor equal to40555206945792000000. As a polynomial in the flag entries, this minor is not identically zero over any characteristic-zero field. Its nonvanishing defines an additional nonempty open set on which the rank is the maximum9. The scalar argument already fixes binary degree6/7 ranks4/7 and ternary ranks4/12 on the original open. Intersect these opens and the gin open. This proves the same required five Hilbert values. An exact rank at a single point **combined with this polynomial-open argument and the scalar rank bounds** is a universal generic proof; an unsupported sampled initial ideal would not be.

## 4. Monomial conclusion, with full-ring minimality

Conca's revlex section identity gives H_r(k)=dim(K[x1,…,xr]/B_r)_k, B_r=B∩K[x1,…,xr]. Characteristic-zero generic initial ideals are strongly stable. Ifx2^7 belonged toB, repeated moves towardx1 would put all binary degree7 monomials inB, contradictingH2(7)=1. H2(8)=0 givesx2^8∈B. Earlier pure powers would implyx2^7∈B by ideal closure. Hencep=8.

For A3=K[x1,x2,x3]/B3, quotienting byx3 identifies its multiplication cokernel with the binary quotient. Therefore

    dim ker(x3:(A3)_(k−1)→(A3)_k)=H3(k−1)−H3(k)+H2(k).

This is0 atk6 and1 atk7. There are no elements ofB below degree6. A degree6 generator divisible byx3 would give a killed degree5 standard monomial, so none exists. The degree7 kernel supplies a standard degree6 monomialm withx3m∈B3. Any minimal divisorv ofx3m inB3 must containx3, or it would dividem. Its degree is consequently7. The samev is minimal inB because a divisor of a first-three-variable monomial cannot involvex4. This is a counterexample to the actual conjecture; no full gin or particular exponent vector is needed.

## 5. Own exact certificate and boundary controls

Own multiplication matrices have ranks4,12,4,7,9 at(r,k)=(3,6),(3,7),(2,6),(2,7),(2,8). Nonzero minors, selected row/column indices and complete left-kernel checks are reproducible in independent_algebra.py and its output. An independently recovered minimal binary syzygy matrix has columns

    (11s, 11t, −146s−219t, 175s+275t),
    (−12s²−17st, −12st−17t², 82s²+235st+168t², 0),
    (−3268s³−4275s²t+4200st²,
     −6068s²t+4125st²−1400t³,
     26998s³+40497s²t, 0).

With sign convention(−1)^i on the deleted rowi=0,…,3, all four maximal minors are exactly70000 times the four binary ambient polars. The displayed paper syzygy follows independently fromρ=(1,−11,3) and(d,t)=(4,7).

RestrictingQ first and differentiating afterward gives only2binary or3ternary independent degree6 polars, rather than4. This confirms that the three-dimensional arrangement theorem concerns a different ideal. In characteristic7 the ternary degree7 rank drops from12 to11, reflecting the Euler relation. Characteristic2 already merges factors. Bad primes of the chosen flag determinants include2,3,5,7,11,17; this is only a flag warning, not a classification of positive-characteristic counterexamples. The manuscript makes no extension to those characteristics.
