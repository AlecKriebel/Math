# Unrestricted correlation-model degrees: rigorous partial results

Problem 30005309 / OWR-11695865-008. Authored 11 October 2026 UTC.
No exact all-n degree formula is claimed.

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. Novelty and priority are unestablished; no exhaustive current-openness claim is made.

## 1. Scope and conclusions

Work over C. Let X_n be the open set of invertible symmetric n by n matrices Sigma with every diagonal entry equal to 1. Put m=n(n-1)/2, N=n(n+1)/2, K=Sigma^{-1}, and W=S^{-1}, where S is generic symmetric invertible data. The three critical systems are, for i<j,

* ML: (K-KSK)_{ij}=0;
* dual ML: (K-W)_{ij}=0;
* SSL: (KSK-W)_{ij}=0.

Degrees mean generic complex critical-scheme lengths, with multiplicity, on this invertible open set. No positive-real restriction, optimizer count, or equicorrelation restriction is used.

Here are partial results, not recurrences for the exact three requested degree sequences:

1. Define A_0=1 and
   A_n=sum_{k=1}^n binom(n-1,k-1) a_k A_{n-k},
   where a_1=1, a_2=2, and a_k=2^k for k>=3.
   Then MLdeg(n)>=A_n. The exponential generating function is
   sum A_n x^n/n! = exp(e^{2x}-1-x-x^2).
   For n=1,...,8, A_n is 1,3,15,73,433,3067,23775,202321.

2. Define B_0=1 and
   B_n=sum_{k=1}^n binom(n-1,k-1) b_k B_{n-k},
   where b_1=1, b_2=0, and b_k=2^{k-1} for k>=3.
   Then SSLdeg(n)>=B_n under the target's usual finite-generic-degree convention. More intrinsically, every n has a nonempty open set of data with at least B_n distinct simple invertible SSL critical points. Its generating function is
   sum B_n x^n/n! = exp((e^{2x}-1)/2-x^2).
   For n=1,...,8, B_n is 1,1,5,25,97,489,3285,22481.

3. Dual ML has a scheme-exact n-variable saturated determinant reduction. It gives dualMLdeg(n)<=n!, and dualMLdeg(a+b)>=dualMLdeg(a)dualMLdeg(b). In particular dualMLdeg(n)>=2^{floor(n/2)}. The proof below also independently recovers dualMLdeg(3)=5, improving the elementary lower bound to 5^{floor(n/3)} times 2 when n is 2 modulo 3, and times 1 otherwise. None of these statements is an exact all-n recurrence.

4. There are elementary upper bounds
   MLdeg(n)<=min((2n-1)^m, 2^m binom(N,n)),
   and SSLdeg(n)<=(2n)^m under the finite-generic-degree convention. The latter Bezout bound also bounds total isolated critical-scheme length whenever the specialized critical scheme is not finite.

5. A precise obstruction to naive diagonal specialization is proved: for generic diagonal data, the ML critical locus already has a one-dimensional connected-block locus at n=4, and SSL has a two-dimensional connected-block locus at n=5. Thus the displayed lower-bound families cannot simply be declared exhaustive. These loci remain in the invertible domain; they are not determinant-zero artifacts.

The all-n proof is algebraic and independent of the finite computational checks. The checks corroborate identities and catch scope errors; they do not certify novelty or prove the missing exact formulas.

## 2. Scheme convention and elementary upper bounds

Write Sigma=I+(x_{ij})_{i<j}, Delta=det(Sigma), C=adj(Sigma). Over the rational function field F=C(s_{ij}), the exact ideals in F[x_{ij}] are

I_ML=(Delta C_{ij}-(CSC)_{ij}:i<j):Delta^infinity,
I_dual=(C_{ij}-W_{ij}Delta:i<j):Delta^infinity,
I_SSL=((CSC)_{ij}-W_{ij}Delta^2:i<j):Delta^infinity.

Equivalently work directly in F[x,Delta^{-1}], or adjoin t with t Delta-1. Multiplication by Delta or Delta^2 is by a unit there, so it preserves local schemes and multiplicities. W is the inverse of the same S, not independent data.

The numerator degrees are at most 2n-1, n, and 2n, respectively. Affine Bezout bounds the sum of multiplicities of isolated roots by the product of these degree bounds. For ML there is a smaller alternative: introduce a diagonal D and use

S=Sigma-Sigma D Sigma. (2.1)

This is equivalent to ML because D=K-KSK is uniquely recovered. With Sigma coordinates in P^m and D coordinates in P^n, all N equations have bidegree at most (2,1). The coefficient of H^m E^n in (2H+E)^N is 2^m binom(N,n).

ML generic finiteness and reducedness can also be seen directly: (Sigma,D) -> Sigma-Sigma D Sigma maps the irreducible N-dimensional open set X_n times C^n to Sym_n. At (I,0) its derivative sends a zero-diagonal H and diagonal E to H-E, an isomorphism. It is therefore dominant and generically finite, and characteristic zero gives an open set of finite reduced fibers. This argument is not being asserted as a proof of generic finiteness for SSL; the SSL lower-bound theorem below has its explicit intrinsic simple-branch formulation even without that extra assertion.

## 3. The dual determinant reduction, its base locus, and product bound

Let A have zero diagonal and generic off-diagonal entries A_{ij}=W_{ij}. Put M(z)=A+diag(z_1,...,z_n) and f(z)=det M(z). The exact dual critical scheme is

J=(partial_i f-f:1<=i<=n):f^infinity. (3.1)

Indeed the dual equations force K=M(z). Since (M^{-1})_{ii}=partial_i f/f, the correlation diagonal constraints are exactly partial_i f=f. Conversely every invertible M satisfying these equations yields Sigma=M^{-1} in X_n. These constructions are inverse morphisms on the localized coordinate rings, so multiplicity is preserved. The diagonal entries of W do not enter (3.1); generic invertible S gives generic off-diagonal W.

Every equation in (3.1) is multiaffine in z. Compactify in (P^1)^n. Each has divisor class H_1+...+H_n. The coefficient of H_1...H_n in their product is n!, giving the isolated-root bound and thus dualMLdeg(n)<=n!.

The unsaturated base locus has a concrete description:

f=partial_1 f=...=partial_n f=0 iff rank M<=n-2. (3.2)

The reverse implication is immediate from the cofactors. If rank M=n-1, its nonzero symmetric adjugate has the form c vv^T. Its diagonal entries cannot all vanish over C, since that would imply every v_i^2=0. This proves (3.2).

For generic off-diagonal A and n>=3 this base locus has dimension n-3. To see dominance and the fiber dimension, choose an invertible (n-3)-square principal block freely on a dense open subset of its diagonal-coordinate space. Its Schur complement is symmetric 3 by 3 with fixed generically nonzero off-diagonal entries a,b,c. There is a unique rank-one completion, with diagonal (ab/c, ac/b, bc/a). Thus the rank<=n-2 locus maps dominantly to the off-diagonal coordinates. The symmetric corank>=2 variety has codimension 3: its rank n-2 stratum is parametrized by an (n-2)-subspace and a nondegenerate symmetric form there, giving dimension N-3. Generic fiber dimension is consequently n-3. This also shows why unsaturated Bezout counting does not directly give the desired degree.

For the product bound, take block-diagonal W with blocks of sizes a,b in their respective finite, simple generic loci. Every pair of block critical matrices gives a critical matrix of size a+b. The derivative of K_{ij}-W_{ij} in a cross-block zero-diagonal variation H is -K_a H K_b, an invertible linear map because both K blocks are invertible. The within-block Jacobians are invertible by the simple-fiber choice. Hence all products are simple in the full unrestricted model and persist under generic perturbation. This proves supermultiplicativity. Generic finiteness of the dual map offdiag(Sigma^{-1}) follows from its invertible derivative at I.

For completeness, the n=3 reduction at A_{12}=1,A_{13}=2,A_{23}=3 has
f=z_1 z_2 z_3-9z_1-4z_2-z_3+12.
After adjoining t f-1, an exact lexicographic Groebner basis is

864t+z_3^4-2z_3^3-37z_3^2+38z_3+181,
60z_1+z_3^4-8z_3^3-20z_3^2+153z_3-70,
60z_2-z_3^4+8z_3^3+30z_3^2-223z_3-120,
z_3^5-8z_3^4-25z_3^3+188z_3^2+25z_3-150.

The last polynomial is squarefree, so these are five simple invertible roots. For generic a,b,c the single rank-one base point is itself a simple root of the unsaturated three equations: their Jacobian there is Hess(f), whose determinant is 2z_1z_2z_3, nonzero. The multiaffine bound 6 therefore leaves at most 5 invertible roots, and the five simple specialized roots give the reverse inequality by persistence. Thus dualMLdeg(3)=5, a reproof of a value already in the primary table.

## 4. Diagonal-data ML classification

Fix S=diag(s_1,...,s_n), with the s_i generic and nonzero. A connected block means a connected component of the graph of nonzero off-diagonal entries of Sigma. Equation (2.1) respects that decomposition. Within a block of size k, D is invertible for generic data. Here is a direct justification. The matrix D Sigma commutes with DS because
DS=D Sigma-(D Sigma)^2.
If an edge joined a nonzero d_i to a zero d_j, the commutator in that entry would force s_i d_i=0, impossible. Hence D is either everywhere nonzero on a connected block or everywhere zero. In the latter case Sigma=S on the block, which forces a singleton with s_i=1; generic data excludes this.

The same commutator now shows s_i d_i=c throughout a connected block. Set

T=sum_{i in block} 1/s_i, d_i=c/s_i,
B=D^{1/2} Sigma D^{1/2}.

Then B^2-B+cI=0 and diag B=(c/s_i). Exclude the proper discriminant c=1/4 and write c=lambda(1-lambda). B has the form

B=(1-lambda)I+(2lambda-1)P,
P=P^T=P^2, rank P=r.

Taking traces gives

T lambda(1-lambda)=(k-r)+(2r-k)lambda. (4.1)

All square-root choices for the diagonal congruence merely reparametrize sign choices; they do not change the count of Sigma matrices.

For r=1, write P=uu^T with u^T u=1. Equation (4.1) becomes

T lambda^2-(T+k-2)lambda+k-1=0. (4.2)

For generic data it has two distinct roots; lambda,1-lambda,2lambda-1 are nonzero. For each root the prescribed squares are

u_i^2=[lambda(1-lambda)/s_i-(1-lambda)]/(2lambda-1). (4.3)

They sum to 1 and are all nonzero generically. They yield 2^{k-1} different matrices uu^T, all with complete off-diagonal support, and therefore 2^{k-1} different Sigma matrices.

For k>=3 the two roots of (4.2) give different c: their sum is 1+(k-2)/T, not 1. Since D is recovered uniquely from (Sigma,S), the families cannot overlap. There are 2^k such matrices. For k=2 the two roots are complementary, and P versus I-P describes the same family; directly the equation is rho^2=1-s_1-s_2, giving exactly two nonzero invertible points generically. For k=1 there is just Sigma=[1]. These are the weights a_k.

### Simplicity within one block

This must be checked in the full zero-diagonal tangent space, not just along an equicorrelation line. Suppose H=delta Sigma has zero diagonal and is in the ML critical Jacobian kernel at one of the constructed points. Differentiate (2.1), allowing a uniquely determined diagonal delta D. Differentiating the commutation relation, using s_i d_i=c and complete off-diagonal support, forces s_i delta d_i=delta c independent of i.

For a first-order deformation, the trace of B is T c. On its lambda and 1-lambda eigenspaces, differentiating B^2-B+cI=0 gives eigenvalue derivatives -delta c/(2lambda-1) and +delta c/(2lambda-1). Thus

[T-(k-2r)/(2lambda-1)] delta c=0.

For r=1 this coefficient is nonzero precisely away from the discriminant of (4.2). Thus delta c=0 and delta D=0. Put X=D^{1/2} H D^{1/2}. The remaining linear equation is
BX+XB=X, with diag X=0.
Because r=1 and lambda differs from 1-lambda, every symmetric solution has the form X=uv^T+vu^T with u^T v=0. Its diagonal is 2u_i v_i; all u_i are nonzero, so X=0, hence H=0. The k=2 argument is included, or follows directly by differentiating rho^2=1-s_1-s_2. A singleton has no within-block tangent variables.

### Simplicity across blocks and the lower bound

For two different blocks, the cross-block linearization of (2.1) is
H-(Sigma_a D_a)H-H(D_b Sigma_b)=0.
The spectra of Sigma_a D_a are lambda_a and 1-lambda_a; for a singleton its only eigenvalue is 1-s_i. A sum of an eigenvalue from each block can equal 1 only if their constants c_a and c_b agree, because z and 1-z have the same product z(1-z). Here a singleton has c_i=s_i(1-s_i).

All block constants are nonconstant algebraic functions of that block's own diagonal data. For k>=2 this follows already from (4.1): a constant nonzero c would give only constant lambda values but a varying T, a contradiction. For disjoint blocks the parameter sets are independent. Consequently c_a=c_b is a proper algebraic condition, also after allowing the two possible roots in a block. There are finitely many partitions and block choices for fixed n, so one can simultaneously avoid all these conditions, all discriminants, zero coordinates, and determinant-zero conditions on one nonempty Zariski open subset of diagonal data.

For such data every product of the constructed connected-block points is a distinct simple point of the full critical scheme. Distinct partitions have distinct support components. Counting the block containing label 1 gives exactly the recurrence for A_n. The implicit function theorem, or etale persistence of simple roots, preserves all these points under general nearby symmetric-data perturbation. Every nonempty complex analytic neighborhood intersects the generic Zariski open locus. Hence MLdeg(n)>=A_n.

## 5. Diagonal-data SSL classification and lower bound

With diagonal S, W is diagonal, so the SSL condition is that T_0=KSK be diagonal. T_0 is automatically invertible. It is equivalent to

Sigma T_0 Sigma=S. (5.1)

On a connected block, B=T_0^{1/2} Sigma T_0^{1/2} satisfies B^2=ST_0. Commutation and connectedness force s_i (T_0)_{ii}=c. Write T=sum 1/s_i, beta^2=c and

B=beta(2P-I), P=P^T=P^2, rank P=r.

The diagonal constraint and trace give

beta=(2r-k)/T, P_{ii}=(1+beta/s_i)/2. (5.2)

For generic diagonal data T is nonzero. The case 2r=k is impossible because beta cannot vanish. For r=1 and k>=3, beta=(2-k)/T is nonzero. The prescribed diagonal entries in (5.2) sum to 1 and are generically nonzero, giving 2^{k-1} rank-one projectors uu^T and hence 2^{k-1} distinct connected critical matrices. Replacing (r,beta,P) by (k-r,-beta,I-P) is the same B, not a new family. There is no connected k=2 solution at generic diagonal data, while a singleton always gives Sigma=[1]. These are exactly the weights b_k.

For completeness, the constructed points are simple. A zero-diagonal kernel variation H of (5.1), with diagonal delta T_0, first forces s_i delta(T_0)_{ii}=delta c. Since trace B=T c, differentiating B^2=cI gives

T delta c=(2r-k)delta c/(2beta)=(T/2)delta c.

Thus delta c=0, delta T_0=0. The remaining equation is BX+XB=0 for X=T_0^{1/2} H T_0^{1/2}. At rank one its solutions are uv^T+vu^T with u^T v=0. The zero diagonal and nonzero u_i force X=0.

Across blocks, the linearization is
(Sigma_a T_{0,a})H+H(T_{0,b} Sigma_b)=0.
The eigenvalues in a connected nonsingleton block are beta and -beta. A singleton has eigenvalue s_i and constant c_i=s_i^2. Distinct block constants c again prevent opposite eigenvalues. Constants from disjoint blocks are nonconstant functions of independent diagonal parameters: c=(k-2)^2/T^2 for nonsingletons. Avoiding finitely many proper conditions makes every constructed block product simple simultaneously. The partition recurrence and persistence argument now prove the stated B_n bound and its intrinsic simple-branch version.

## 6. Positive-dimensional diagonal fibers: the missing contribution

The variety of symmetric idempotents P of rank r is an open homogeneous realization of the Grassmannian and has dimension r(k-r). Its diagonal map lands in the affine hyperplane sum p_i=r. This map is dominant and generically has fiber dimension

r(k-r)-(k-1)=(r-1)(k-r-1). (6.1)

Here is a differential proof of dominance. Tangent variations are [A,P], A skew-symmetric. Varying A_{ij} gives a diagonal variation proportional to P_{ij}(e_i-e_j). At a projector whose off-diagonal support is connected these span the full trace-zero diagonal hyperplane. Such projectors exist: the rank-r idempotent variety is irreducible (it is the open set of nondegenerate r-subspaces of the ordinary Grassmannian), and each off-diagonal coordinate is nonzero at some point for 1<=r<k, so a generic point has every off-diagonal entry nonzero. Generic smoothness gives (6.1).

The prescribed diagonals in Sections 4 and 5 are generic points of this trace hyperplane for generic diagonal S on the indicated eigenvalue branch. This is not an assumption: for ML choose generic lambda and p_i with sum p_i=r, set c=lambda(1-lambda), d_i=(1-lambda)+(2lambda-1)p_i, s_i=c/d_i. The trace relation holds, and the resulting parameter map is generically finite over s because lambda satisfies the nonconstant quadratic (4.1). It is dominant. For SSL choose generic nonzero beta and p_i of trace r, set s_i=beta/(2p_i-1); when 2r!=k these recover (5.2) and give a dominant parametrization of diagonal data.

For ML, k=4,r=2 gives dimension 1, with generic c=2/T and lambda distinct from 1-lambda. For SSL, k=5,r=2 gives dimension 2, with beta=-1/T. On a dense open subset all entries needed for connectedness and invertibility remain nonzero. This proves the stated obstruction on the actual critical open set. The omitted positive-dimensional strata can contribute additional isolated branches after a generic nondiagonal perturbation. Calculating those contributions, along with possible limiting behavior at the determinant boundary and infinity, remains unresolved here.

## 7. Small-degree controls and claim boundary

For n=2, write Sigma=[[1,rho],[rho,1]], S=[[a,b],[b,c]], d=ac-b^2. The three exact generic polynomials, up to nonzero scalar, are

ML: rho^3-b rho^2+(a+c-1)rho-b;
dual: W_12 rho^2-rho-W_12;
SSL: b rho^4+b(d-2)rho^2-d(a+c)rho+b(d+1).

For S=[[2,1],[1,3]], they are squarefree, have degrees 3,2,4, and have no root at rho=+1 or -1. Their degree and resultant conditions are Zariski open, proving the usual n=2 degrees. At n=1 all three degrees equal 1.

The finite exact tests independently evaluate the original matrix critical equations and their full off-diagonal Jacobians for rational examples of the block constructions; compare analytic Jacobians against direct symbolic differentiation in n=2; verify the n=3 saturated dual Groebner certificate; and reject singular, wrong-diagonal, and altered-equation controls. Full rational Jacobian nonsingularity in the larger examples is certified by exact Gaussian elimination modulo prime 1000003, after checking denominator invertibility; a nonzero modular determinant proves the rational determinant is nonzero. Separate integrity controls reject a changed manifest pin, changed member bytes, an omitted member, a duplicate path, and an unlisted inventory file, with explicit exceptions rather than Python assert statements. These checks are run in normal, -O, and -OO modes.

No claim is made that A_n or B_n is an exact degree sequence. In particular A_4=73 is strictly below the source's ML degree 109, and B_2=1 is below the SSL degree 4. No interpolation from the primary numerical table enters any proof above. The exact requested all-n recurrences for all three degrees remain unresolved in this attempt. The claims are rigorous partial bounds and reductions, with no exhaustive novelty claim.
