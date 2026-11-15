# Independent analytic proof and falsification controls

This is a personal reconstruction, made before supplied scientific code/results and peer opinions. The substantial initial version is sealed separately. The exact rational controls were frozen at 2026-11-15T06:29:42.603868+00:00 before reading the original author proof. Neither a source programme nor an optimization solver was run by this lane.

Let S=R[x,y,z], let ΣS² mean a finite sum of squares of real polynomials, and let I_R(L) be the entire ideal of real polynomials vanishing on the real zero set of L. The target is the literal published universal statement for both J_R=(yR_x−xR_y,zR_x−xR_z,zR_y−yR_z) and K_R=(yR_x,xR_y,zR_x,xR_z,zR_y,yR_z): for every real ε≥0, R+ε is not in ΣS²+I_R(L). This implies the advertised ordinary-radical and original-ideal conclusions because L⊂sqrt(L)⊂I_R(L). No reverse inclusion is assumed.

## Universal proof

1. Write R=F(x²,y²,z²), where F=a³+b³+c³−a²b−ab²−a²c−ac²−b²c−bc²+3abc. The exact identity F=(a−b)²(a+b−c)+c(a−c)(b−c), together with symmetry and the ordering a≥b≥c≥0, proves R≥0. It also classifies the nonzero zero directions: a=b and c=0 or c=a, followed by coordinate permutations.

2. The ten representatives are (1,s,t), (1,s,0), (1,0,t), (0,1,t), with every indicated sign independently ±1. All entire real lines through these representatives consist of global minima. Consequently ∇R=0 there and all J and K generators vanish there. Direct whole-line polynomial identities independently verify this fact; sampling alone was not used.

3. A homogeneous cubic vanishing at the six representatives with a zero coordinate has the form A x(x²−y²−z²)+B y(y²−x²−z²)+C z(z²−x²−y²)+Dxyz. At (1,s,t) its value is −A−Bs−Ct+Dst. The four sign characters 1,s,t,st are independent, so A=B=C=D=0. If a homogeneous polynomial of degree d≤3 vanishes at all ten representatives, multiplication by x^(3−d) reduces to the cubic case; the polynomial ring is an integral domain. Thus that polynomial is zero. The exact evaluation ranks are 1,3,6,10 for d=0,1,2,3. The cubic determinant in the independent order is −128. A separate post-freeze calculation verifies −128 in the exact order printed in original_packet/author/PROOF.md; see SOURCE_ORDER_DETERMINANT.json.

4. The x-axis lies in both real varieties: ∇R(u,0,0)=(6u⁵,0,0), all six cross products vanish, and R(u,0,0)=u⁶.

5. Suppose R+ε=Σ_j q_j²+h, h∈I_R(L), with finitely many polynomial q_j of any finite degrees. On each zero line, ε=Σ_j q_j(uv)² for every real u. Every q_j(uv) is bounded on the whole real line, hence constant. Equivalently, the highest-degree nonzero leading terms of finitely many real polynomial squares cannot cancel. Expanding q_j into homogeneous parts shows that each positive-degree homogeneous part vanishes at the ten representatives. In particular, its parts of degrees 1,2,3 vanish identically by step3. Constants are retained for ε>0.

6. On the x-axis, u⁶+ε=Σ_j q_j(u,0,0)². If any restricted polynomial has degree D>3, choose the maximal such D. The coefficient of u^(2D) is a nonempty sum of positive squares of nonzero real leading coefficients, impossible on the degree-six left side. Thus all restrictions have degree≤3. Their degree1–3 parts are already zero, so they are constants. A constant right side cannot equal u⁶+ε. The case of zero summands also contradicts this identity. This proves the full claim for ε=0 and every ε>0 simultaneously. No global bound on deg(q_j), finite-variety assumption, radicality assumption, generic-position assumption or SDP calculation occurs.

## Other statements and category boundaries

For every real polynomial f in n≥1 variables, nonnegativity on all R^n is equivalent to nonnegativity on V_R(J_f). If a negative point is the origin, all minors vanish there. Otherwise minimize f on the compact sphere with that point's radius. Its minimizer remains negative and satisfies ∇f=λx by the regular sphere multiplier condition. This argument covers unbounded-below polynomials and nonattaining global infima; it is not a genericity claim.

J_R⊂K_R⊂G_R=(R_x,R_y,R_z). Euler's identity 6R=xR_x+yR_y+zR_z proves R∈G_R; therefore R+ε has the evident SOS-plus-gradient-ideal certificate ε+R. The note does not refute the gradient-ideal theorem. The point (2,2,1) has R=9 and ∇R=(12,12,6); J_R vanishes and yR_x=24. This independently rules out conflation of J and K. In fact, V_R(K_R) is exactly the ten zero lines plus the three axes: at least two nonzero coordinates force every derivative to vanish, whence Euler forces R=0; with one nonzero coordinate the point is on an axis. No classification of V_R(J_R) is required.

For Q=(1−xy)²+y²−1/2, the literal product ideal has generators 2y²(xy−1) and 2x[x(xy−1)+y]. Their real common zero set is {0}: the first forces y=0 or xy=1; the second becomes −2x² in the first case and 2 in the second. Q(0)=1/2 and Q(2,1/2)=−1/4. Its infimum −1/2 is approached along (1/u,u) but is never attained, since equality would require y=0 and xy=1. This is a separate product-ideal diagnostic. It is not a counterexample to the minor-variety nonnegativity equivalence.

## Materially distinct adversarial controls

| Attack | Checkable outcome | Meaning and exact limit |
|---|---|---|
| Positive ε permits constants | Constants explicitly retained in steps5–6; bound on the axis eliminates positive degrees, not constants | Avoids an invalid zero-constant inference |
| Arbitrarily high degrees might cancel | Maximal axis degree has strictly positive leading square coefficient | Universal for finite real-polynomial sums, not a fixed search bound |
| Ten projective points mistaken for ten affine samples | Entire lines are substituted as polynomials in u | Finite evaluations alone do not establish the theorem |
| Delete one zero direction | Remove (1,1,1). With p=x(x²−y²−z²)+y(y²−x²−z²)+z(z²−x²−y²)−xyz, h=R−p² vanishes on the other nine lines and the x-axis | The weakened spine admits R+ε=p²+(sqrt ε)²+h. On the missing line h=−16u⁶, so this is not an actual certificate. Rank falls to9 |
| Product and minor categories confused | Exact point (2,2,1) distinguishes J_R from K_R | Main theorem covers both separately |
| Q diagnostic transferred to J_Q | At x=3s,y=s,s²=5/24: ∇Q=−(x,y)/4, Q=−29/192, J_Q=0 and yQ_x=−5/32 | Exact real quadratic-field control exhibits a negative point on V_R(J_Q), as the sphere argument demands |
| Gradient ideal included accidentally | Euler identity supplies a positive certificate for G_R | The obstruction is to the stated ideal-only certificates |
| Real field replaced by C | Every f=((f+1)/2)²+((f−1)/(2i))² over C | Real coefficients and positivity are essential; this is outside the claim |
| Approximate or inequality-multiplier certificates included | The primary positive results contain an additional inequality with an SOS multiplier | Those certificates are not ruled out |

INDEPENDENT_ALGEBRA.json gives exact sparse polynomials, evaluation matrices, ranks, the nine-line control, quadratic-field values and Euler identity. Its small 343-point integer grid is explicitly only a diagnostic; all universal assertions above have independent proofs. Infinite sums, analytic summands, rational-function squares, complex coefficients, and a restriction to the origin's sphere are not substituted for the actual category.

## Assessment

The entire original mathematical claim and auxiliary diagnostics are supported. No substantive proof gap or counterexample to that claim was found. The classical Robinson form and cubic-zero argument are prior mathematics; the note's specific application is the line/axis obstruction for both proposed ideal-only formulations. Neither first priority nor continuing open status through2026 has been established. Complete original Hà–Pham2008/2009 bodies are not claimed read; their relevant certificate distinction is independently checked in actual later primary statements. This is a bounded bibliographic limitation, not an unsupported import in the self-contained proof. No repaired or narrower theorem is proposed.
