# Independent normalized-coefficient curve proof and actual hand controls

This actual work follows INITIAL34ee9916 and precedes scientific README/support/code/results, archived scientific opinion, current peer/root findings, and foreign bodies. No scientific programme runs. The mechanism directly follows the unit-diagonal tensor coefficient along a curve and identifies its second-order weighted variance; it is not a supplied bilinear-slice/Cauchy–Schwarz proof or native finite replay.

## Universal deduction, including every scale and coordinate convention

Let p be the original positive definite real homogeneous form of degree d in m>=1 variables. Positive degree and p(-x)=(-1)^d p(x)>0 force even d>=2. Write A for its unique symmetric d-linear polarization. Compactness gives a unit v minimizing p on the sphere, with c=p(v)>0. Set P=p/c and B=A/c, so P(x)>=||x||^d and P(v)=1. For u perpendicular to v, comparison of P(v+tu) with (1+t^2||u||^2)^(d/2) at0 gives

    B(v^(d-1),u)=0,
    Q(u,u):=B(v^(d-2),u,u)>=||u||^2/(d-1).

Indeed the first derivative difference is dB(v^(d-1),u) and the second is d(d-1)Q(u,u)-d||u||^2. All constants are explicit. This only uses a local Hessian property at a minimizing direction, not global convexity.

Choose orthonormal w1,...,w_(m-1) in v-perp and wm=0. Put xi=v+epsilon wi. In the ordered orthonormal basis(w1,...,w_(m-1),v), X has determinant epsilon^(m-1). Hence xi are independent for every epsilon!=0, and all m tangents wi are distinct. In m1 the determinant has exponent0 and there are no mixed tuples.

Use the *original* unit-diagonal columns

    zi(epsilon)=xi/p(xi)^(1/d)
               =c^(-1/d) (v+epsilon wi) P(v+epsilon wi)^(-1/d).

These are defined with the positive real root; P(xi)>0 since xi has radial component1. Each p(zi)=1 exactly, and

    det Z=epsilon^(m-1) c^(-m/d) product_i P(xi)^(-1/d)

in the displayed orthonormal orientation, so it is nonzero for every epsilon!=0. This is no conditioning estimate.

For a tuple J of lengthd, let ar=wjr. Directly evaluate its actual *original* normalized ordered coefficient:

    C_J(epsilon)=A(zj1,...,zjd)
       = B(v+epsilon a1,...,v+epsilon ad)
          / product_r P(v+epsilon ar)^(1/d).

The numerator's original factorc cancels exactly the d column factors c^(-1/d). No factorc^m belongs in this coefficient ratio (it belongs in the determinant only). Every numerator is1 at0, so by continuity and the finite number of tuples it is positive in one common neighborhood; logs, if used below, are justified there independently of the inequality to be proved.

The diagonal expansion is

    P(v+epsilon ar)=1+binom(d,2)Q(ar,ar) epsilon^2+O(epsilon^3),
    P(v+epsilon ar)^(-1/d)
       =1-(d-1)Q(ar,ar)epsilon^2/2+O(epsilon^3).

Thus the normalized column has second-order radial correction

    c^(1/d) zi = v+epsilon wi
                 -(d-1)Q(wi,wi)epsilon^2 v/2+O(epsilon^3).

Evaluating B on all d corrected columns yields

    C_J=1+epsilon^2[sum_(r<s)Q(ar,as)
                         -(d-1)sum_r Q(ar,ar)/2]+O(epsilon^3)
       =1-epsilon^2 S_J/2+O(epsilon^3),
    S_J=sum_(r<s)Q(ar-as,ar-as).

Each diagonal term appears d-1 times in S_J, and the off-diagonal contribution is-2sum Q(ar,as). Equivalently log C_J=-epsilon^2 S_J/2+O(epsilon^3); no extra d remains in the normalized deficit. The source's polynomial gap has quadratic coefficient dS_J/2, which is a different quantity.

Every summand is nonnegative since differences are tangent. For a mixed tuple some ar-as is nonzero, so S_J>0. For each mixed J the expansion makes C_J<1 for all sufficiently small nonzero epsilon. The independently obtained numerator positivity gives C_J>0. A minimum of the finitely many positive epsilon bounds works for every mixed tuple simultaneously. A pure tuple gives C_J=p(zi)=1 identically, rather than only through Taylor order. This proves the entire strict original theorem and its exact pure-equality statement at all m,d; no finite cases stand in for those quantifiers.

The multiplicity form makes the normalization audit explicit. For alpha_i counts of indexi, sum alpha_i=d,

    S_alpha=d sum_i alpha_i Q(wi,wi)
                -Q(sum_i alpha_i wi,sum_i alpha_i wi).

This is a weighted variance, not a sum over distinct variables alone. At the chosen orthonormal/zero tangents,

    S_alpha >= [alpha_m sum_(i<m)alpha_i
                         +2sum_(i<j<m)alpha_i alpha_j]/(d-1)>0

for every mixed alpha. The scalar numerator on the right counts all occurrence pairs and is positive. Higher Taylor terms still depend on p; this does not assert a uniform epsilon across all forms or a conditioning bound.

Let S have the zi as columns. The coordinate relation is old x=S t; therefore p'(t)=p(S t) and A'(ej1,...,ejd)=A(zj1,...,zjd). For alpha, the ordinary monomial coefficient is multinomial(d;alpha)C_alpha. The theorem bounds C_alpha, not that ordinary coefficient by1. Absolute-value bounds follow because all chosen ordered coefficients are positive and the diagonal is1.

Strict inequalities, numerator positivity, positive p(xi) and det X!=0 are open conditions on the raw matrix columns, for finitely many tuples. Density of rational matrices gives rational *unnormalized* columns with the same inequalities, even with irrational coefficients of p. Their individual nonlinear unit-diagonal scalings need not be rational. None of these arguments asserts semidefinite, integral-unimodular or orthogonally constrained versions.

## Twelve actual hand-worked controls

1. Degree and one-variable boundary: if p=a x^d with a>0 and even d, z=a^(-1/d) gives p(z)=1 and the mixed condition is vacuous. Odd degree cannot meet positivity at bothx and-x. m0 and degree0 are outside the statement.

2. Exact quadratic clustered basis: p=x^2+y^2,v=(1,0),w1=(0,1),w2=0,epsilon1/2 gives z1=(2/sqrt5,1/sqrt5),z2=(1,0). Both diagonal values are1; A(z1,z2)=2/sqrt5 is strictly in(0,1), and detS=-1/sqrt5 is nonzero. This checks determinant order and a nontrivial strict mixed entry exactly.

3. Multinomial mutant: the transformed polynomial in case2 is t1^2+t2^2+(4/sqrt5)t1t2. The ordinary mixed coefficient4/sqrt5>1, while the ordered coefficient2/sqrt5<1. Their factor is binom(2;1,1)=2. Dropping the factor would falsely reject this valid coefficient normalization; it is not a counterexample to the stated ordered theorem.

4. Common scale: replace the quadratic by9(x^2+y^2). The correct columns are case2's columns divided by3. Their p-diagonals remain1 and the ordered mixed value remains2/sqrt5, since9*(1/3)^2=1. Using the P-normalized columns without restoringc gives diagonal9. For16(x^2+y^2)^2 the required common column factor is1/2, since16*(1/2)^4=1; an erroneous square-root factor1/4 instead yields diagonal1/16. This checks the degree root and common coefficient scale separately from determinant scaling.

5. Exact tangent constant: for P=(x^2+y^2)^2 atv=(1,0), P(v+tu)=1+2t^2+t^4 foru=(0,1). Its second derivative4 equals d(d-1)Q=12Q, so Q=1/3=1/(d-1). The lower-bound constant is attained and cannot be replaced in this calculation by1 or1/d.

6. All binary mixed quartic multiplicities: for the same radial quartic, take x1=(1,epsilon),x2=v and t=epsilon^2. For k copies ofx1 and4-k copies ofx2, N1=1,N2=1+t/3,N3=1+t,N4=(1+t)^2; denominators are(1+t)^(k/2). Thus C1=C3=1/sqrt(1+t), C2=(1+t/3)/(1+t), C0=C4=1. At epsilon1/2, the mixed values are2/sqrt5,13/15,2/sqrt5, all strictly between0 and1. This covers every mixed ordered tuple for this fixed m2,d4 example by symmetry, not all p/d in lieu of the proof.

7. Distinguish the two gap constants: in case6 with k2, S=2*2*(1/3)=4/3. The actual normalized deficit coefficient is S/2=2/3, while product P-N^4 has coefficient dS/2=8/3. Directly,(1+t)^4-(1+t/3)^4 starts with(8/3)t, and C2=1-(2/3)t+O(t^2). This rejects an extra d in the normalized-coefficient curve.

8. Three-variable weighted cross-pairs: P=(x1^2+x2^2+x3^2)^2,v=e1,w1=e2,w2=e3,w3=0. For multiplicities(1,1,2), the Euclidean pair-difference sum is2+2+2=6, hence S=6/3=2. The explicit radial polarization B(a,b,c,d)=[(a.b)(c.d)+(a.c)(b.d)+(a.d)(b.c)]/3 gives N=B(v+epsilon e2,v+epsilon e3,v,v)=1. Its normalized coefficient is1/(1+epsilon^2), with quadratic deficit1=S/2. At epsilon1/2 it is4/5. This checks different nonzero tangent directions and repeated zero tangents simultaneously.

9. A genuinely nonconvex positive form, exact mixed checks: take p=x^4+8x^2y^2+y^4. On the unit circle p=1+6x^2y^2>=1, so v=e1 is a global minimum andc1. At(1,1) the Hessian is[[28,32],[32,28]], with negative eigenvalue-4, so global convexity fails. For epsilon1/10, P0=p(1,epsilon)=10801/10000>27/25. The three mixed numerators are N1=1,N2=76/75,N3=26/25. For k1, P0>1. For k2, N2^2<27/25<P0 since76^2=5776<6075=27*225. For k3, N3^4<(27/25)^3<P0^3 since26^4=456976<492075=27^3*25. These imply Ck<1 for k1,2,3 with positive numerators and cover every mixed binary quartic tuple. No approximate floating point or native dataset was used.

10. Pure identity and semidefinite boundary: a pure tuple always has N=p(xi), so its polynomial gap is identicallyzero and unit-normalized coefficient exactly1. For the excluded semidefinite p=x1^d in m2, any unit-diagonal columns have first coordinates of absolute value1, so every ordered mixed coefficient has absolute value1. The strict mixed theorem cannot simply be extended to semidefinite forms.

11. Rational and orthogonality exclusions: for m1,p=2x^2, unit normalization requires z=plus/minus1/sqrt2, not a rational basis; the raw column1 is rational. For the isotropic quadratic, any orthogonal change keeps mixed coefficients0, contradicting a hypothetical strict-positive orthogonal version. These checks preserve the actual GL(R), rational-raw-only and unrestricted-conditioning scope rather than narrowing the original theorem.

12. Coordinate inverse mutant, computed exactly: case2's S=[[2/sqrt5,1],[1/sqrt5,0]] has inverse[[0,sqrt5],[1,-2]]. The intended p(S t) has unit diagonals and positive ordered mixed2/sqrt5. The wrong p(S^-1 t) is t1^2-4t1t2+9t2^2, whose second diagonal is9 and ordered mixed is-2. This falsifies an inverted substitution convention without numerical tolerance.

These are actual symbolic/hand-worked controls with no scientific execution. They target normalization, multiplicity factors, coordinate orientation, arbitrary dimension, local-versus-global positivity and scope boundaries; the universal proof carries the unbounded claim.

## Frozen limits before later exposure

The full original mathematical basis-existence and strict coefficient statement is now deduced internally, with exact constants and checkable controls. The actual classical problem's ordered coefficient convention and GL scope, Brandes2015's precise antecedent, native rights/edition/support and bounded priority history remain unverified. No primary body, support README, supplied code/output, archived opinion or current peer/root finding has yet been read, and no GET or scientific programme has run. This is not a final disposition; default followupnull and publication/canonical/AA authority absent. Root143 remains CLOSED.
