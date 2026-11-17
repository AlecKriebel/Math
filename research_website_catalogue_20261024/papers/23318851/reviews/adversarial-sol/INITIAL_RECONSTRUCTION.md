# Row 194 — original-only adversarial reconstruction

2026-11-17T13:10:13Z. This is the INITIAL gate, not a final scientific or priority disposition. Only the controlling original TeX, all five actual PDF pages/text and native original metadata/Description have supplied mathematical content. Packaged audit opinions, README, support certificates/results, native program bodies, imported primary mathematics and current peer/root reports remain unread. No scientific program, source import, AST, compiler or test has run. The source-wide passive custody reader is separate from mathematical execution.

The target remains a hypothesis. I attempted to construct a single defining polynomial on a two-dimensional slice, to exploit a norm-ball/unit-sphere mismatch, to break the real realization, and to find exceptions in the exact zero-coordinate reduction. This produced a checkable conic-based reconstruction and several controls to false extensions, rather than a counterexample to the exact stated theorem. It is recorded below before any support/primary exposure. The earlier PRE_TEX_ATTACK.md preserves the conic route before the original proof was read, with the preceding Description/cover exposure expressly acknowledged.

## Exact claim, field, domain and exclusions

For a real binary tensor T in (R^2)^{tensor n}, M_i is the real two-row mode-i flattening, d_i=det(M_i M_i^T), and G_n is the image of the CLOSED Frobenius unit ball. Put C_n=[0,1/4]^n and H_n={d in C_n: d_i<=sum_{j!=i}d_j for every i}. For each integer n>=3, the claimed nonexistence is of ANY P in R[d_1,...,d_n] with G_n={d in C_n:P(d)>=0}, and separately with H_n instead of C_n. There is no degree bound, rational-coefficient restriction, or requirement that one P work simultaneously for different n. The coordinates are determinants themselves. Auxiliary existential variables, multiple inequalities and Boolean formulas are outside the claim.

Each Gram matrix is positive semidefinite of trace r=||T||_F^2<=1, so 0<=d_i<=r^2/4<=1/4. Real rank and real orthogonal diagonalization suffice throughout. No passage from complex existence to real existence is presumed. Native API and printed manuscript both say author version1.0.0, dated12October2026; the PDF container format1.5 is a different datum. The note is explicitly unrefereed.

For n=2 the two Gram determinants coincide by the shared singular values of a real2x2 matrix. Every common d in[0,1/4] occurs at norm1, e.g. diagonal Schmidt coefficients sqrt(lambda(d)),sqrt(1-lambda(d)). Thus -(d_1-d_2)^2>=0 defines G_2 in C_2, while the constant polynomial1 defines it in H_2 because H_2 is already the diagonal. For n=1 the Gram matrix of a two-vector has rank<=1 and G_1={0}; -d_1^2>=0 works. These are actual counterexamples to an unqualified all-n extension and test the stated n>=3 threshold. A zero-factor tuple, if defined, would be a point and is not the asserted setting.

The theorem is about the closed domain, including zero determinants. The stated proof for higher factors does NOT establish an all-positive-domain version. A different author's stronger positive-domain theorem is an original-author bibliographic assertion here, not an imported premise verified in INITIAL.

## Elementary marginal necessity independently reconstructed

Let r=||T||_F^2>0 and let mu_i be the smaller eigenvalue of its i-th Gram matrix. Fix factor1 and choose dominant eigenvectors u_j in every other factor. Let P_j be the corresponding rank-one orthogonal projectors and Q_j=I-P_j. Acting on the tensor product of the remaining factors, these projectors commute, and their simultaneous0/1 eigenvalues prove

sum_{j>=2}Q_j >= I-product_{j>=2}P_j.

The expectation in T gives sum_{j>=2}mu_j >= r-||contraction_{u_2,...,u_n}T||^2. The contraction is the flattening M_1 applied to a unit product vector, so its squared norm is at most the operator-norm square of M_1, namely r-mu_1. Hence mu_1<=sum_{j>=2}mu_j. Permute factors. This proof avoids relying on a complex marginal theorem or a statement-only citation. It also checks the original's recalled real Schmidt/Bessel argument by a distinct contraction formulation. Degenerate local eigenvalues allow any dominant eigenvector; zero T gives all zero determinants separately.

For fixed determinant d at trace r, the smaller eigenvalue is

mu_r(d)=(r-sqrt(r^2-4d))/2=2d/(r+sqrt(r^2-4d)).

One must NOT normalize a tensor and then pretend its determinants are unchanged: dividing T by sqrt(r) divides determinants by r^2. Instead use the ratio monotonicity. Set lambda(d)=mu_1(d). If lambda(d_i)>sum_{j!=i}lambda(d_j), then d_i is strictly larger than every other d_j and positive. For 0<d_j<d_i and r>2sqrt(d_i),

d/dr log(mu_r(d_j)/mu_r(d_i))
 =1/sqrt(r^2-4d_i)-1/sqrt(r^2-4d_j)>0.

Thus ratios at any permissible r<=1 are at most their trace-one values, whose sum is<1, contradicting the marginal necessity at trace r. Terms with d_j=0 are0. The lower endpoint follows by continuity. If d_i=1/4, r>=2sqrt(d_i)=1, so only r=1 is allowed and no derivative at a singular endpoint is needed. Consequently every point of G_n obeys lambda(d_i)<=sum_{j!=i}lambda(d_j).

## Exact real three-factor realization

For lambda_i in[0,1/2] satisfying all triangle inequalities, let

w_0=1-(lambda_1+lambda_2+lambda_3)/2,
w_1=(-lambda_1+lambda_2+lambda_3)/2,
w_2=(lambda_1-lambda_2+lambda_3)/2,
w_3=(lambda_1+lambda_2-lambda_3)/2.

All are nonnegative; their sum is1; w_0>=1/4. The real tensor with coefficients sqrt(w_0),sqrt(w_1),sqrt(w_2),sqrt(w_3) on000,011,101,110 has squared norm1. In each mode its two rows have disjoint support, so their inner product is0. The row-one squared norm is respectively w_2+w_3=lambda_1, w_1+w_3=lambda_2 and w_1+w_2=lambda_3. Its determinants are lambda_i(1-lambda_i). This proves sufficiency, including equality and zero weights, without a complex-to-real transfer. Combined with necessity and the norm-ball ratio argument, it establishes exactly the three-factor criterion used below.

This is mathematically prior construction credited by the original; no novelty is attributed to this reconstruction. INITIAL verifies the displayed linear-algebra argument, not the historical accuracy or exact scope of every cited antecedent.

## Independent determinant-plane/conic obstruction

Restrict a hypothetical defining polynomial to the symmetric plane d=(a,t,t), calling the restriction R(a,t). In the open square0<a,t<1/4, write b=lambda(t). The three triangle inequalities reduce to lambda(a)<=2b: the other two hold automatically and strictly when a>0. On the physical boundary for0<b<1/4,

t=b-b^2,   a=2b-4b^2.

The eliminated polynomial is

Q(a,t)=(a-4t)^2+2a-4t
      =a^2+(2-8t)a+16t^2-4t.

Its discriminant in a is4(1-4t), a nonsquare in R(t). Thus Q is irreducible in R[a,t] by Gauss' lemma. More explicitly, the function field map t->b-b^2 has degree2, while on Q the parameter is recovered by b=(4t-a)/2. The kernel of R[a,t]->R[b] given by this parametrization is exactly(Q). Therefore a polynomial that vanishes on any open b-interval of the curve is divisible by Q. This supplies the needed algebraic density; two isolated sample points would not suffice.

On0<b<1/4 this curve is a genuine separating boundary of the feasible set in the plane. The other determinant hull inequalities are strict: a<2t because2t-a=2b^2>0, and t<a+t because a>0. Cube bounds are strict. Both sides of the curve thus remain in either allowed ambient domain locally. The excluded point(a,t)=(17/100,9/100) is strictly inside the cube and H_3 plane (17/100<18/100), while lambda(a)>1/5=2lambda(9/100). It rejects the case R identically0.

Continuity of an exact nonnegativity description forces R to vanish on the separating arc. Write R=Q^m A with exact m>=1 and Q not dividing A. The parametrized restriction of A is a nonzero polynomial in b, so it is nonzero at some point of that physical arc. Since the feasible side has R>=0 and the infeasible side has R<0, the exact multiplicity m must be odd.

Now take1/4<b<1/2 in the SAME parametrization. We still have0<a,t<1/4, but lambda(a)=1-2b, rather than2b, because the quadratic map has crossed its maximum. All three triangles are strict:1-2b<2b, and b<(1-2b)+b. Thus the conic arc is now in a full open feasible neighborhood of the plane. Its determinant hull inequalities remain strict by the same formulas. Also partial_a Q=2-4b>0, so the curve is smooth and has a transverse sign crossing. Choose a point where A does not vanish, possible by the same polynomial-in-b argument. R>=0 on both sides of that interior crossing requires m even. Contradiction.

For orientation, the boundary point b=1/10 gives(a,t)=(4/25,9/100); the interior point b=2/5 gives(a,t)=(4/25,6/25). These samples locate open arcs but are not used in place of the generic residual argument. The route uses a determinant-coordinate irreducible conic on a plane and its physical/interior arcs. The original proof instead pulls back to three eigenvalue variables and uses global reflection of linear factors. Both are boundary/interior parity mechanisms; the conic calculations were saved before reading that proof, after the explicitly disclosed abstract/Description cues.

## Adversarial check of the original reflection argument

The substitution F(t)=P(t_i(1-t_i)) is a polynomial globally invariant under each t_i->1-t_i. The reflection need NOT preserve the small-eigenvalue domain(0,1/2)^3 or feasibility. Its role is the global polynomial automorphism carrying the factor L=t_1-t_2-t_3 to -(t_1+t_2+t_3-1). Polynomial vanishing on a relatively open plane patch gives divisibility by L. Exact multiplicity transfers under the automorphism; nonzero residual restrictions cannot vanish on either entire relatively open patch. This closes the potential hidden domain-invariance mistake.

At the physical patch t=(b+c,b,c), b,c>0,b+c<1/2, all three hull slacks are positive:2bc,2c(1-b-c),2b(1-b-c). At the interior patch t_1+t_2+t_3=1 inside(0,1/2)^3 they are2t_jt_k>0. Therefore neither parity crossing escapes H_3. The original strict-H_3 excluded point (55,28,28)/256 has smaller eigenvalues(5/16,1/8,1/8) and first hull slack(28+28-55)/256=1/256>0; it is indeed infeasible. Constant or identically zero polynomials cannot evade the contradiction.

No numerical sampling of polynomial degrees is a substitute for exact finite multiplicity in the polynomial ring. Allowing all real coefficients, including transcendental coefficients, does not alter these algebraic arguments.

## Exact zero-coordinate slices and scaling checks

If a real mode flattening has Gram determinant0, its rank is<=1. For a nonzero tensor it factors as S tensor u in that factor. Rescale u to norm1 and absorb its length into S. For every other mode, the flattening Gram is multiplied by ||u||^2=1, and the Frobenius norm is unchanged. The next zero-determinant condition consequently remains zero on S. Repeat. If the tensor is0, all assertions are immediate. Conversely tensor any three-factor witness with unit vectors in the added factors.

This proves exactly G_n intersect{d_4=...=d_n=0}=G_3 x{0}^{n-3}. The C_n face is C_3 and the H_n face is H_3: inequalities for added indices read0<=sum d_j, and the first three are the original three. Restricting a hypothetical P_n to this face gives an exact forbidden description in dimension3. If that restriction is identically0 it accepts the entire face, already contradicted by the explicit excluded three-factor point. No continuity approximation from strictly positive factors is used.

This step depends essentially on the allowed closed zero-determinant faces. It cannot establish the higher-factor all-positive-domain theorem attributed to Ferudun. The original explicitly says so; treating that attribution as this note's own theorem would overstate its result.

## Positive four-factor witness: exact hand arithmetic

For the DISPLAYED polynomials in the original, take d=(2401,1296,1296,1)/10000. Every coordinate is strictly between0 and1/4. The hull slacks, with the same denominator10000, are192,2402,2402,4992, all strictly positive.

Thus Q_1=192*2402^2*4992/10^16. Factoring gives2^15*3^2*13*1201^2 divided by2^16*5^16, hence

Q_1=168760917/(2*5^16)=168760917/305175781250.

For Q_2 the square roots are(49,36,36,1)/100. Pair each sign vector with its global negative. There are8 pairs, so no overall minus sign. Representatives with first sign positive have numerators122,120,50,48,50,48,-22,-24. Their product is2^18*3^4*5^5*11*61. After squaring and the factor1/2,

Q_2=2^3*3^8*11^2*61^2/5^22
   =23632249608/2384185791015625.

With common denominator2*5^22, the difference numerator is

168760917*15625 -2*23632249608
=2636889328125-47264499216
=2589624828909>0,

matching the printed fraction2589624828909/4768371582031250. This is a finite exact arithmetic derivation, not a native program run.

The inverse x->lambda(x) is increasing. d_1>6/25=f(2/5); d_2=d_3=81/625<5/36=f(1/6); d_4=1/10000<99/10000=f(1/100). Hence lambda(d_1)>2/5 and the other three sum to<1/6+1/6+1/100=103/300<2/5. Necessity for the BALL, already derived above, rules out every allowed norm, rather than only normalized tensors. This checks the displayed witness and displayed sign condition internally. Whether the displayed polynomials and direction are exactly Seigal's original Conjecture1.5 is a separate primary-source attribution interface not yet read.

The full sign product is a polynomial in d: flipping one square root permutes its factors, so it is separately even in each square-root variable. At the real GHZ tensor(d_i=1/4 for three factors), the displayed formulas give Q_1=(1/4)^3=1/64 and Q_2=(1/2)*(3/16)^2=9/512. The claimed external secondary pair expression is not defined fully in this note; judging the precise printed external theorem/direction requires the actual Seigal primary after resume. It is not an input to the theorem here.

## Optional hull-containment and convexity stress test

The proof of nondefinability only needs the explicitly defined domain H_n and local strict slacks. It does not require an imported theorem identifying that domain with a convex hull. Nevertheless containment can be checked from the marginal necessity: write lambda_i<=1/2. If s=sum_{j!=i}lambda_j<=1/2, monotonicity of f(x)=x-x^2 gives d_i<=f(s)<=sum_{j!=i}f(lambda_j). If s>=1/2, each f(lambda_j)>=lambda_j/2 gives sum_{j!=i}d_j>=1/4>=d_i. Thus G_n lies in H_n.

A vertex argument also suggests the full hull equality without a primary citation. A non-cube vertex of H_n must have an active polygon equality. If two distinct polygon equalities are active, all other coordinates vanish and the two surviving coordinates agree; absent endpoint cube bounds this is an edge, not a vertex. If exactly one is active, a vertex needs n-1 coordinate bounds, and the remaining coordinate is an integer multiple of1/4, hence an endpoint. So all vertices are cube vertices with either0 or at least2 coordinates equal1/4. The all-zero vertex is a product tensor; every other such vertex is a GHZ tensor on its active subset tensored with unit vectors elsewhere. This supplies checkable supporting reasoning but is not used to replace the requested later provenance comparison with Seigal's actual theorem.

## Original-only gaps, imported interfaces and stopping point

The exact central mathematical argument has been reconstructed from elementary real linear algebra and polynomial factorization, including the closed-ball normalization and exact higher-factor slice. No code/certificate is needed for that deduction. No counterexample to the exact core statement was produced in these initial attacks. This is an INITIAL observation, not an authorization to promote the result or a claim of full scientific/priority review.

The strongest citation-dependent conditional conclusion is: IF the original displayed Q_1,Q_2 and sign direction are the original Seigal conjecture, THEN the independently checked positive tuple refutes that conjecture at n=4; the universal original nondefinability argument addresses each n>=3 in its explicitly defined C_n/H_n domains. Exact primary interfaces still to inspect after explicit resume are Seigal Theorem1.3 and Conjecture1.5, the precise secondary display in Theorem1.4, the cited HSS/Bravyi/DSL statements and proof scope, and Sinn's earlier obstruction scope. These are attribution/antecedent interfaces; the displayed elementary proof has been checked without presuming their truth from citations.

The original's claims about PR170, byte identity, timestamps, visibility, Ferudun's creation time/theorem/mechanism and comparative strength are exposed AUTHOR ASSERTIONS only at this gate. No Git, network, support archive priority evidence or other author's primary text has been inspected. Literal simultaneity, mutual independence, exclusive firstness and complete historical novelty remain unverified and are expressly not certified by the original either. Native publication date12October2026 is distinct from claimed earlier GitHub disclosure and author-controlled commit dates.

Support/runtime/negative-control correspondence is wholly unassessed in INITIAL. No native program has been read or run. No source, old packet, repository/index/ref/config, website, Sheet, redirect, release or Zenodo record has been modified. No person has been contacted and no outreach prepared. Freeze this entire INITIAL namespace and stop; continuation requires a separate sibling after root's source gate and explicit RESUME. Follow-up defaults to null at this gate.
