# Independent conic-geometry derivation

This derivation was developed from RGK arXiv:2004.12497v11 before reading the submitted proof; its mechanism and partial results were frozen in the two accompanying freeze records. It does not establish the full noncircular all-period product theorem by itself.

## 1. Exact objects and signed areas

Let a>b>0, 0<lambda<b², E:x²/a²+y²/b²=1, C:x²/(a²−lambda)+y²/(b²−lambda)=1. Work in the positive orientation; reversing it negates both areas and preserves their product. Write

p_i=(a cos t_i,b sin t_i), D=diag(a⁻²,b⁻²), n_i=Dp_i, k_i=|n_i|, u_i=n_i/k_i, h_i=1/k_i.

The tangent L_i has equation n_i·X=1. Its intersection with L_(i+1) is

T_i=((n_(i+1),y−n_i,y),(n_i,x−n_(i+1),x))/det(n_i,n_(i+1)).

The foot from any fixed M onto L_i is

q_i=M+[(1−n_i·M)/|n_i|²]n_i.

For a cyclic list z_i, area means (1/2) sum det(z_i,z_(i+1)); it remains defined for self-intersections, repetitions and zero signed area. This is explicitly the primary source's equation (1), not an interpretive repair.

The denominator of the projection is positive for real boundary points. Consecutive tangents are parallel only when their contact points are antipodal; their chord would pass through O, hence could not be tangent to the strictly interior C. Consecutive coincident contacts are excluded by lambda>0. Thus all real T_i and q_i are finite under the stated hypotheses.

## 2. Elementary conic relation and central symmetry

Put P=a²b², c²=a²−b². For consecutive boundary parameters t,s, write u=(t+s)/2 and v=(s−t)/2. Their chord is

(cos u/a)x+(sin u/b)y=cos v.

The dual tangency equation for C gives

sin²v=lambda*(b² cos²u+a² sin²u)/P.                         (1)

Equivalently, with alpha=P−lambda c², beta=P+lambda c², gamma=P−lambda(a²+b²),

alpha cos t cos s+beta sin t sin s=gamma.                  (2)

Implicit differentiation gives

(ds/dt)²=D(s)/D(t),
D(t)=alpha² cos²t+beta² sin²t−gamma²
    =4lambda P*(b²−lambda+c² sin²t).

The forward chosen tangency branch preserves orientation, so the positive square root applies. Therefore

dt/sqrt(b²−lambda+c² sin²t)                               (3)

is an invariant measure for the billiard step. Its density is strictly positive and pi-periodic. In its cumulative coordinate U, the billiard step is a translation: derivative of U(F(t))−U(t) is zero. Translation by t→t+pi equals half the full U-period.

For primitive period n=2m, the translation number is w/n with gcd(w,n)=1. In particular w is odd, so F^m advances U by an odd half-period. Thus

p_(i+m)=−p_i.                                             (4)

This proof includes all admissible primitive star winding numbers. It uses a conic relation and differentiation, without importing the submitted elliptic-curve pole mechanism.

## 3. Arbitrary M reduces to two scalar products

Let theta_i be the unit normal angle and Delta_i=theta_(i+1)−theta_i, considered modulo2pi inside trigonometric functions. Translation invariance of signed shoelace area gives

B_M=area(q_i)=1/2 sum (h_i−M·u_i)(h_(i+1)−M·u_(i+1)) sin Delta_i.       (5)

By (4), the terms linear in M cancel in opposite pairs. For M=r(cos psi,sin psi), rotate all normal angles by −psi. The identity

cos x cos y sin(y−x)=[sin(2(y−x))+sin2y−sin2x]/4

shows that anisotropic quadratic terms telescope around the cycle. Consequently every primitive even confocal family satisfies the exact identity

B_M=B_0+(|M|²/8) S,       S=sum sin(2Delta_i).              (6)

Equation (6) is also valid for any centrally paired list of tangent lines, independently of a billiard condition. It shows that all points on the same circle centered at O have the same signed pedal area, for each fixed orbit phase.

Thus the target's full arbitrary-M claim is equivalent to two scalar statements:

A'B_0 is phase-invariant; A'S is phase-invariant.           (7)

One implication follows from (6). Conversely set M=0 and any |M|=1. This route does not establish (7); moving the difficulty to (7) is a reduction, not a proof.

## 4. Outer-area formula and outer-vertex locus

From the two tangent equations,

T_i=(a cos u,b sin u)/cos v.

After affinely normalizing E to a unit circle, the oriented side portion between neighboring tangent intersections has signed length tan v_(i−1)+tan v_i. Summing the oriented triangles from O yields

A'=ab sum tan((t_(i+1)−t_i)/2).                           (8)

This formula uses a coherent lift of successive angles and extends to stars by signed summation. All needed denominators are nonzero as discussed above. Equation (1) also gives the locus

T_x²*(a²−lambda)/a⁴+T_y²*(b²−lambda)/b⁴=1.                (9)

Equations (5), (8), and (9) offer direct conic quantities against which a proposed general proof can be checked.

## 5. Circle: a rigorous complete all-period boundary theorem

For a=b=R, every fixed-caustic orbit has constant parameter increment delta=2pi w/n. Exclude coincident or antipodal consecutive contacts, and require least period at least3. A cyclic regular or star list then has

A'=n R² tan(delta/2),
B_M=(n R²/2)sin delta+(n |M|²/8)sin2delta.                  (10)

The linear terms vanish because the first harmonic sums to zero; the quadratic formula follows from the telescoping identity above. Both expressions are independent of the initial phase, for every winding and every repetition. In particular the product theorem extends to this circular boundary, although the candidate deliberately excludes it. For a star with cos delta<0, B_M vanishes when |M|²=−2R²/cos delta. Zero signed pedal area therefore cannot be discarded by division.

## 6. Exact six-period control and remaining gap

For a=2,b=1,lambda=4/9, a six-period orbit is

(2,0),(4/3,sqrt5/3),(−4/3,sqrt5/3),(−2,0),(−4/3,−sqrt5/3),(4/3,−sqrt5/3).

Every point lies on E, every chord satisfies the confocal dual tangency equation, and every outgoing unit chord has n_i·v_i=−1/3. This equal Joachimsthal value plus opposite signs for incoming/outgoing normal components verifies reflection. Direct exact projection gives

A'=16sqrt5/5,
B_(u,v)=5sqrt5*(u²+v²+9)/18,
A'B_(u,v)=40*(u²+v²+9)/9.                                (11)

This is a whole arbitrary-M identity at one orbit phase. It does not prove phase invariance. Numerical direct collision checks at other phases and primitive periods 6,10,14 corroborate (7), including star orbits, but are not proofs or interval certificates.

The exact remaining gap of this independent direct route is the noncircular general-period proof of (7). The submitted candidate addresses that gap by a materially different meromorphic-function argument. It would be circular to call the present geometric reduction a separate full proof of its conclusion.
