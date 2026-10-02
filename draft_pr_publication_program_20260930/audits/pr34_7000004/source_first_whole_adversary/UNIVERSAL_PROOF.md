# Independent universal proof and adversarial reconstruction

Written before reading older family/root reports or supplementary candidate certificates. Inputs read: literal original Ghomi printed p6, candidate RESULT.md, and Ni–Zhang–Zhang v1 primary PDF (actual printed pp2–3). This is independent verification of the exposed candidate, not a new search turn or blind rediscovery.

## Candidate

For the parameter circle set c=cos t, s=sin t, g=(c,s,(c²−s²)/4), w=(−c³,s³,1), r=√(1+c⁶+s⁶), b=w/r. These functions are smooth and periodic, with no seam defect. The xy projection g_xy=(c,s) is an embedded regular circle. Equality of g values forces equality modulo 2π, and |g'|≥1. Thus g is embedded and regular.

Direct differentiation gives g'=(-s,c,-cs), g''=(-c,-s,-(c²−s²)), and g'''=(s,-c,4cs). The cross product x component is c[-(c²−s²)]−(-cs)(-s)=-c³; its y component is (-cs)(-c)−(-s)[-(c²−s²)]=s³; its z component is s²+c²=1. Therefore g'×g''=w never vanishes, curvature is positive, and b is precisely the unit Frenet binormal with a smooth osculating plane. Equality of b values gives equality of c³ and s³ by ratios to b_z=1/r>0. Real cubing is injective, and the pair (c,s) determines the parameter-circle point. This proves global injectivity, including cardinals and antipodes.

Independently, w'=(3c²s,3s²c,0). If b'=0, differentiating w=rb and its constant z component forces r'=0 and w'=0. Conversely w'=0 forces r'=0 and b'=0. Hence b'=0 exactly at cs=0, four points. Torsion is (w·g''')/r²=3cs/r², with genuine sign changes. Smooth injectivity does not imply regularity of the spherical binormal.

## Every claimed push-off

Let q_e=g+eb for 0<e<1/3. Extend b to F(x,y)=(-x³,y³,1)/√(1+x⁶+y⁶) on the closed unit disk. Normalization v↦v/|v| has derivative (I−vvᵀ/|v|²)/|v| of norm ≤1 since |v|≥1. The derivative of v=(-x³,y³,1) has norm 3 max(x²,y²)≤3. Thus |DF|≤3. The disk is convex, so integrating along a segment yields |F_xy(p)−F_xy(p')|≤3|p−p'|. The reverse triangle inequality gives

|p+eF_xy(p)−p'−eF_xy(p')|≥(1−3e)|p−p'|>0.

Also |(I+eDF_xy)v|≥(1−3e)|v|. Restricting to the circle gives an injective regular projected push-off, so the full smooth push-off is an injective immersion of a compact circle and therefore an embedding. This proof needs the strict e<1/3 interval; it claims nothing at the endpoint.

Use the global shear h(x,y,z)=(x,y,z−(x²−y²)/4). Its inverse adds the same polynomial, and det Dh=1. It sends g to the planar unit circle bounding the unit disk D. Substitution yields

h_z(q_e)=e/r+e(c⁴+s⁴)/(2r)−e²(c⁶−s⁶)/(4r²).

Since r≥1, c⁴+s⁴≥0 and |c⁶−s⁶|≤1, this is at least (e/r)(1−e/(4r))≥(e/r)(1−e/4)>0. The sheared push-off misses the whole disk and its boundary. The two embedded curves are disjoint. Linking equals algebraic intersection with a spanning disk; the intersection is empty, so linking is zero. The orientation-preserving shear preserves linking. Consequently Lk(g,q_e)=0 for every 0<e<1/3. This is an exact all-parameter proof; sampling, crossing counts, writhe integration and diagrams are unnecessary. Orientation reversal can only change a sign, leaving zero intact.

This refutes the literal universal question with a unit, nonzero, smooth field and embedded curve/push-offs, without exploiting normalization or immersed-linking ambiguity.

## Exact earlier printed construction and priority limit

I viewed actual printed pp2–3 of arXiv:2606.29231v1. Section 2 prints v(x,y)=(x,y,x⁴−y⁴), n=(-4x³,4y³,1)/√(1+16x⁶+16y⁶), and γ_a=(ac,as,a⁴(c⁴−s⁴)) for every a>0. These are operative printed equations, not an abstract linking theorem. Since c⁴−s⁴=c²−s², direct differentiation gives γ'_a×γ''_a=a²(-4a³c³,4a³s³,1). Its normal is therefore its Frenet binormal, globally injective by the cubic-ratio proof and with positive curvature.

For a=4^(−1/3), the positive homothety X↦X/a sends γ_a to g because a³=1/4, and its unit binormal agrees with b since 4a³=1. It sends γ_a+δn to g+(δ/a)b. Positive homotheties preserve linking; the proved result gives embedded disjoint zero-linking push-offs for every 0<δ<a/3. This is a verified elementary consequence of an earlier dated printed construction. It does not assert that the paper prints the linking conclusion, identifies Ghomi’s question, establishes earliest worldwide priority, or provides external referee certification.

There is a second independent consequence on the a=1 graph. For x²+y²=1 let α=e/√(1+16x⁶+16y⁶)>0. The push-off is (x−4αx³,y+4αy³,x⁴−y⁴+α). For 0<e<1/4 we have 0<α<1/4, giving |x−4αx³|≤|x| and |y+4αy³|≥|y|. Its vertical gap above the graph at the new xy coordinates equals

α+[x⁴−(x−4αx³)⁴]+[(y+4αy³)⁴−y⁴]≥α>0.

It misses the entire graph disk. The tubular-neighborhood theorem ensures embedded disjoint push-offs for sufficiently small e. This proves zero linking on a sufficiently small interval; it does not prove embedding for all e<1/4.

The Hessian of x⁴−y⁴ is diag(12x²,−12y²); graph curvature is K=−144x²y²/(1+16x⁶+16y⁶)², zero on both axes. Every printed γ_a meets them at four points. This is not a strictly negative-curvature example.

## Conditional claims derived independently

For an arclength curve with T=g' and a C² compatible unit B, set N=B×T. Differentiating frame orthogonality gives T'=kN, B'=−τN and N'=−kT+τB without dividing by k. In a positive-speed parameter the right sides all acquire v. The twist density T·(B×B') is τ.

If B is regular, |τ|>0 and its sign σ is constant. Its spherical unit tangent is U=−σN and dℓ=|τ|ds. Therefore dU/dℓ=(k/τ)T−B. With outward sphere normal B, the left conormal is B×U=σT, so kg=(dU/dℓ)·(B×U)=k/|τ| and kg dℓ=k ds. A regular injective spherical loop is Jordan. Gauss–Bonnet on its chosen disk gives ∫kg dℓ=2π−A with 0<A<4π, hence |∫k ds|<2π. If signed k has one sign, |∫k ds|=∫|T'|ds≥2π by Fenchel, contradiction. Our candidate has positive k but τ=0 four times, outside the regular-B hypothesis. Nonzero twist alone need not force linking because writhe can compensate.

For X(s,u)=g(s)+uN(s), at u=0 the first form is E=G=1,F=0 with normal B; the second coefficients are 0,τ,0. Thus K=−τ². For any smooth surface with K<0, its shape operator is invertible; the normal derivative along a regular curve is −S(T)≠0. The candidate’s stationary B cannot be that surface normal. A local ruled strip or nonpositive graph does not settle the global annulus/boundary rigidity question. A negative answer to original Problem 1.4 does not settle the later negative-curvature question.

## Review boundary

No unsupported mathematical gap is found in the exposed RESULT argument. This seal does not yet certify source versions, history, code, queue, metadata or procedure, all of which remain to be inspected and attacked. The universal argument above is the mathematical certificate; computation is supplemental. Completion estimate: 25%.
