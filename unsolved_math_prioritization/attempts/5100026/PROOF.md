# The outer focal antipedal vertex centroid for even elliptic billiards

Problem 5100026 / AMR-050-0026, invariant k407. Full first-turn candidate, pending independent review. The proposed invariant is due to Reznik–Garcia–Koiller. Classical Jacobi parametrization and elliptic-function theory are credited below; no historical novelty claim is made.

## 1. Exact theorem and real domain

Let an ellipse E with semiaxes a>b>0 have a strict confocal elliptical caustic and a Poncelet billiard family of least even period N. Primitive star families are included. For a member P_0,...,P_(N-1), form the outer polygon whose vertices are the successive intersections of the tangents to E at P_i. Fix either focus M of **E**, rather than a focus of the outer-vertex locus.

Through each outer vertex R_i draw the line perpendicular to R_i-M. Let U_i be the intersection of this line with the corresponding line at R_(i+1). Then all these intersections are finite and unique, and

C(M) = (1/N) sum_i U_i

is independent of the orbit phase. It lies on the original focal axis, and the two focal centroids are negatives of one another. When N=4 it is the origin. This is the **vertex** centroid C0 prime star in both source Table 5 editions; a zero signed area does not make this arithmetic mean undefined.

Reversal and a repeated traversal of an even least-period orbit preserve the mean. Repeating an odd orbit does not create the even least-period hypothesis. Degenerate and hyperbolic caustics are outside the theorem. A circular billiard, if included as an additional limiting model, has the same assertion with M=O by antipodal symmetry, without taking a limit in the proof.

## 2. Canonical parameter and the actual outer vertices

Scale the major semiaxis of the caustic to one. Its minor semiaxis is k'=sqrt(1-k²), with 0<k<1. All quantities below use this common Euclidean scaling. Let K=K(k), K'=K(k'), p=iK'. The Jacobi functions sn, cn, dn have modulus k. Set

v=2K tau/N, delta=2v, 0<tau<N/2, gcd(tau,N)=1,
s=sn(v), c=cn(v), d=dn(v),
a=d/c, b=k'/c.

Here 0<v<K, s,c,d>0, a>1, and a²-b²=k². Stachel's Theorem 4.3 and equation (4.9) give all the source families, including their turning number tau, by

P(w)=(-a sn(w), b cn(w)),  P_i=P(w+i delta).

The foci are (±k,0). Since N is even, tau is odd, and shifting N/2 indices adds 2K tau. Thus both original and outer vertices are antipodally paired.

The intersection of the tangents at P(u-v) and P(u+v) is

R(u)=(-A sn(u), B cn(u)),  A=a d/c=d²/c², B=b/c=k'/c².       (1)

This is the actual outer polygon, not an independently chosen confocal billiard. For a direct verification put S=sn(u), C=cn(u), D=dn(u), D0=1-k²s²S². The addition formulas are

sn(u±v)=(S c d ± s C D)/D0,
cn(u±v)=(C c ∓ S s D d)/D0.                                (2)

The tangent at P(t) has equation -sn(t)x/a+cn(t)y/b=1. Substituting (1) into the two tangent equations and using C²=1-S² and D²=1-k²S² verifies each. Equivalently, solving the sum and difference gives -R_x/a=S d/c and R_y/b=C/c. Consecutive outer vertices R(u-v),R(u+v) therefore lie on the tangent at the original vertex P(u).

Take M=(k,0). Write q_±=R(u±v)-M. The antipedal intersection U(u) is given by

q_± dot (U-M)=q_± dot q_±.                                  (3)

All complex continuations use the bilinear extension x_1 y_1+x_2 y_2, never a Hermitian norm. Equations (1)–(2) give

Delta_M(u):=det(q_-,q_+)
 = 2B s d D (a+kS)/D0.                                     (4)

Indeed det(R(u-v),R(u+v))=2AB s c D/D0, while subtracting M adds 2kB S s D d/D0, and A c=a d. For real u, D>0, D0>0, and a+kS>=a-k>0. Hence (4) never vanishes. The negative focus follows by the central symmetry. This proves the entire real construction is finite for every phase, including stars. No signed-area denominator occurs.

## 3. Local singularities of one antipedal vertex

We first assume N>=6. Standard Jacobi identities give a common period lattice 4K Z+4p Z for sn and cn. They have common simple poles at p+2mK+2np. The simple zeros of dn are K+p+2mK+2np. Useful shift identities are

sn(u+2K)=-sn(u), cn(u+2K)=-cn(u), dn(u+2K)=dn(u),
sn(u+2p)=sn(u), cn(u+2p)=-cn(u), dn(u+2p)=-dn(u).           (5)

We use these standard identities directly (DLMF 22.4), with dn having real period 2K. Every coordinate of (3), by Cramer's rule, is a meromorphic function on this common torus. Away from an endpoint pole, its only possible singularities are zeros of (4). We now inspect all possibilities; the inspection also controls apparent singularities in (4) itself.

### 3a. Zeros of dn

At u=K+p and its translates, S=±1/k and D=0. Equation (2) gives equal finite endpoints R(u-v)=R(u+v), since D0=c²!=0. The factor a+kS is a±1, which is nonzero because a>1. Thus Delta_M has a simple zero. At coincident endpoints the two equations (3) coincide, so both Cramer numerators vanish. A holomorphic numerator vanishing at a simple denominator zero has a removable quotient. Thus U is holomorphic here, even though the direct complex line construction is singular.

### 3b. Common poles of sn, cn and dn

At u=p and its translates, the endpoint arguments u±v are regular. In (4), D and S each have a simple pole and D0 has a double pole. The leading coefficient of D(a+kS)/D0 is nonzero, since k,s are nonzero and each Jacobi residue is nonzero. Hence Delta_M has a finite nonzero limit. The regular endpoints and Cramer numerators show U is regular.

### 3c. The focal roots a+k sn(u)=0

Such a root has S=-a/k. It is simple: sn'=cn dn, while cn²=1-a²/k² and dn²=1-a² are both nonzero. It does not coincide with a zero or pole already considered.

The common original tangent at P(u) has normal n=(-S/a,C/b) and equation n dot X=1. At S=-a/k it passes through M. Moreover C²=1-a²/k²=-b²/k², so n dot n=0. Over the complex plane its one-dimensional direction is isotropic. Both q_±, being on this line through M, therefore satisfy q_± dot q_±=0. Both right sides in (3) vanish, so both Cramer numerators vanish.

For N>=6 these endpoints are finite and Delta_M has a simple zero. Here is the exact exceptional-case check. The overlap with D0=0 would require s²a²=1, or s d=c. Squaring with x=s² gives

k²x²-2x+1=0.

Its only root in (0,1) is x=1/(1+k'). The real Jacobi half-period values identify precisely v=K/2. Since v=2K tau/N and gcd(tau,N)=1, this means N=4, tau=1. It is absent for N>=6. Thus the focal-root singularities of U are removable by simple-zero cancellation. This isotropic cancellation is why using the original foci is essential; a generic fixed point would leave extra poles.

### 3d. Endpoint poles

The only possibilities left are u±v=p+2mK+2np. Exactly one endpoint is singular: two would require 2v to be a real Jacobi pole separation, hence 0 or 2K, whereas 0<2v<2K. These points are the simple zeros of D0. Their dn and sn values are finite and nonzero. By the preceding overlap calculation the factor a+kS is nonzero for N>=6. Formula (4) has a simple pole. An endpoint has a simple pole, so the right side of (3) has order at most two; its Cramer numerator consequently has order at most two, because the other endpoint is regular. Thus U has at most a simple pole.

These four cases exhaust the torus: away from Jacobi poles, the determinant is the explicit product/quotient (4), and the zeros of D0 are exactly its endpoint-pole locations, as also follows from sn(p+t)=1/(k sn t) and the degree-two sn map on its own period torus. No unlisted finite determinant zero is discarded.

## 4. Cancellation in the complete cyclic sum

Use outer-vertex phase w and set R_i(w)=R(w+i delta). Let I_M(X,Y) denote the intersection of the antipedal lines through X and Y, which is symmetric in X,Y. The sum whose constancy is required is

F_M(w)=sum_(i=0)^(N-1) I_M(R_i(w),R_(i+1)(w)).             (6)

It is meromorphic on the compact torus with periods 4K,4p. By Section 3 it has at most simple poles where some R_j has a pole. Fix such a point w0. In the real delta orbit there are precisely two endpoint poles: j and j+N/2. This follows from gcd(tau,N)=1, N even and the two real pole classes separated by 2K. At the first,

R_j(w0+z)=L/z+O(1),

with nonzero vector L, and R_(j+N/2)=-R_j. The two neighbors are finite and opposite, say Q,-Q. To see the latter, (5) and ordinary sn oddness/cn evenness imply R(p+t)=-R(p-t); translating the pole by 2K or 2p preserves that statement. The neighbors at the opposite vertex are correspondingly -Q,Q.

For completeness, the residue of I_M(L/z+O(1),Q+O(z)) is the vector V(M,Q) characterized by the leading two equations in (3):

L dot V=L dot L,  (Q-M) dot V=0.

The determinant det(L,Q-M) is nonzero: it is the leading coefficient of the simple pole in Section 3d. Thus, for J(x,y)=(-y,x),

V(M,Q)=-(L dot L) J(Q-M)/det(L,Q-M).                       (7)

This formula is valid even if its numerator happens to vanish. At the opposite endpoint pole the leading vector is -L, so its incident residue is -V(-M,-Q) or -V(-M,Q), respectively. The total residue in (6) is

V(M,Q)+V(M,-Q)-V(-M,Q)-V(-M,-Q)=0,                         (8)

because V(M,-Q)=V(-M,Q) and V(M,Q)=V(-M,-Q), directly from (7). For N>=6 the four incident edge indices j-1,j,j+N/2-1,j+N/2 are distinct. This avoids double counting. There are no higher Laurent terms to cancel, by Section 3d.

Every possible pole in (6) is therefore removable. A holomorphic function on this compact complex torus is constant, separately in each coordinate. Dividing by N proves the required vertex-centroid invariance for all N>=6 in the theorem. No value formula is needed for the source's invariant, whose value column is unspecified; (3) at any single phase is a finite explicit expression for that constant.

Reflection in the focal axis sends R(u) to R(2K-u) and fixes M. It permutes the full family with reversed cyclic order; I_M is symmetric in its two inputs. Hence the phase-independent constant is fixed by that reflection and lies on the focal axis. Central symmetry sends the positive-focus construction to the negative-focus construction and negates the centroid. The constant is not asserted to be O for N>=6.

## 5. The exceptional least period four

When v=K/2, the half-period identities give d²=k' and c²=k'/(1+k'). Consequently A=B=1+k'. The four outer vertices are antipodally paired on this circle, so the outer quadrilateral is a rectangle circumscribed about E.

Choose its orthonormal side axes and write its vertices as (±h,±l), with h,l>0. Let the original focus have coordinates (m,n). The ellipse support identity h_E(e)²=b²+(M dot e)² for each unit direction e gives

h²-m²=l²-n²=b²>0.                                         (9)

A direct solution of the four antipedal line pairs yields their mean

( m/2 [(l²-n²)/(h²-m²)-1],
  n/2 [(h²-m²)/(l²-n²)-1] ).                              (10)

For example, subtracting the two line equations at the top edge gives x=-m, and substitution gives y=l+(h²-m²)/(l-n). The bottom, right and left edges give the analogous formulas; their mean is (10). Alternatively, Cramer's rule verifies (10) directly; the exact checker does so with unrestricted h,l,m,n. Equations (9) make both entries zero. The real determinant check of Section 2 remains valid at N=4, so none of these intersections is undefined. This direct treatment does not pass through a singular complex limiting argument.

For a circular original ellipse the two foci are O. An even primitive orbit and its outer polygon are centrally symmetric, their consecutive real antipedal normals are independent, and antipedal intersections occur in opposite pairs. The vertex centroid is O.

## 6. Credit, source alignment, and checks

The source is Reznik–Garcia–Koiller, arXiv2004.12497v11 Section3.5/Table5 and the final *Fifty New Invariants*, printed pp.347–348. Both call the requested quantity the outer-antipedal vertex centroid, for even N and the original foci. The proofs of other area or original-polygon invariants are not substituted. In particular, the generally different foci of the outer locus are never used.

Stachel, *On the motion of billiards in ellipses*, Theorem4.3 and equation(4.9), supplies the classical parametrization. The elementary Jacobi addition, shift and pole facts are those of DLMF22.2,22.4,22.8. The meromorphic-removal method is related to earlier campaign treatments of other elliptic invariants; all formulas needed here are derived above. Neither a new parametrization nor historical priority is claimed.

The accompanying exact checker verifies tangent equations, the determinant identity, isotropic focal cancellation, the N4 overlap equation, residue identities and the unrestricted rectangle formula. An integer checker covers orbit/pole-index bookkeeping for many primitive even periods. Separately labeled high-precision tests use actual tangent and antipedal intersections, both foci, primitive stars and critical complex neighborhoods. They corroborate the proof, but they do not replace its all-period singularity classification. This is one substantive author turn; independent source and proof review is required before publication as a claimed result.
