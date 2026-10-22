# Independent direct geometry audit

Status: exact independent proofs for all admitted least periods 3 and 4, plus a general elementary reduction and numerical star checks. The universal elementary route is **PARTIAL / BLOCKED at the scalar identity below**. It does not independently prove all eligible periods.

The mechanism was frozen before original PROOF, Root's proposed route, favorable reports, early author checkpoints, or prior203 target proofs. None of those mathematical arguments has been read for this report. A later Root message confirmed the signed-area positivity issue and requested the controls reported here; it supplied no universal target proof.

## Source and scope

Authenticated arXiv 2004.12497v11 pp.1-6 and journal DOI 10.1007/s40598-021-00174-y pp.343-346 were read in memory from the paths in PRIMARY_SOURCE_ACCESS_01.json. They specify a confocal ellipse pair, a>b>0, signed shoelace areas (Eq.1), and original-side pedal feet (Sec.3.3). Table 3 k203,b gives A A_m, N not congruent 2 modulo 4, M=O. It does not literally say least or primitive. The contract's least physical period interpretation is essential: the exact repeated-list counterexample below disproves an unrestricted list-length interpretation.

No novelty or priority claim is made. The triangular pedal-area identity used below is classical; its implication here is credited as such and also verified by an authored generic symbolic expansion. No target-paper result beyond definitions is imported.

Write E: x²/a²+y²/b²=1 and C: x²/(a²-lambda)+y²/(b²-lambda)=1, with 0<lambda<b². A physical positive orientation has outer eccentric parameters t_i with 0<t_(i+1)-t_i<pi. This follows because every tangent side leaves O strictly on the same side, and a tangent to a proper ellipse containing O cannot pass through O. Reversal negates both signed areas.

## General real support calculation

Put m_i=(t_i+t_(i+1))/2, d_i=(t_(i+1)-t_i)/2, and D_i=cos²(m_i)/a²+sin²(m_i)/b². The original complete chord line is

    (cos(m_i)/a)x+(sin(m_i)/b)y=cos(d_i).

Its tangency to C is exactly sin²(d_i)=lambda D_i. Its length is l_i=2ab sin²(d_i)/sqrt(lambda). The perpendicular foot from O onto that complete line is

    q_i=(cos(d_i)/D_i)(cos(m_i)/a,sin(m_i)/b).

Consequently

    A=ab sum_i sin(d_i)cos(d_i)=ab sum_i u_i/(1+u_i²),
    B=lambda²/(2ab) sum_i u_i u_(i+1)(u_i+u_(i+1)),  u_i=cot(d_i).

For the second formula, cross(q_i,q_(i+1)) equals cos(d_i)cos(d_(i+1)) sin(d_i+d_(i+1))/(ab D_iD_(i+1)); substitute D_i=sin²(d_i)/lambda and expand the sine. This is an algebraic derivation, not a conjectured billiard invariant.

All u_i>0 in this orientation, so A>0 and B>0, including primitive stars. No signed zero occurs in the proper admitted domain. Reversed lists give A<0 and B<0. Thus the absolute values of the signed shoelace areas have the same invariant product if the target theorem holds. An area of filled star regions is a separate geometric quantity and has not been assessed here. Degenerate caustics and repeated or padded lists are outside the least-period domain.

The precise remaining general identity is phase constancy of

    (lambda²/2) [sum_i u_i/(1+u_i²)]
                 [sum_i u_i u_(i+1)(u_i+u_(i+1))]

under the physical Poncelet correspondence when least N is odd or divisible by 4. No elementary telescoping or independent invariant establishing that statement for arbitrary N has been found. Assuming its constancy merely restates the central difficulty. This general route is blocked unless a materially new cancellation mechanism is supplied.

## Exact period 3 proof

Normalize E to the unit circle, set z_i=e^(it_i), r=sqrt(1-lambda/a²), s=sqrt(1-lambda/b²), k=r²-s², and c=2(1-r²-s²). Here 0<s<r<1 and 0<k<1. A chord between unit points z,w is tangent to the normalized caustic precisely when

    F(z,w)=z²+w²+c zw-k z²w²-k=0.                 (1)

This follows by squaring cos²(d)=r²cos²(m)+s²sin²(m) and multiplying by 4e^(2im). All calculations encode real unit-circle points; no complex billiard chart or pole cancellation is assumed.

For three distinct vertices x,y,z, subtract F(x,y)-F(x,z). Dividing by y-z yields (y+z)(1-kx²)+cx=0. If sigma_j are the elementary symmetric sums, every vertex solves

    k x³-k sigma_1 x²+(c-1)x+sigma_1=0.

Comparison with the monic root polynomial gives sigma_2=(c-1)/k and sigma_1=-k sigma_3. Since the roots have unit modulus, sigma_2=sigma_3 conjugate(sigma_1)=-k. Hence 1-2r²-2s²+k²=0. Factorization gives

    ((r+s)²-1)(1-(r-s)²)=0,

and the proper-domain bounds force r+s=1. In particular k=r-s.

Let the physical circumcircle have equation x²+y²-2C_x x-2C_y y+w_0=0. Substituting x=a(z+z^-1)/2 and y=b(z-z^-1)/(2i), then multiplying by z², gives a quartic with leading and constant coefficients (a²-b²)/4 and z² coefficient (a²+b²)/2+w_0. The triangle cubic is

    P(z)=z³+k sigma_3 z²-kz-sigma_3.

The fourth quartic root is 1/sigma_3 by its constant term. Therefore its z² coefficient is -(a²-b²)k/2 and

    w_0=-(a²+b²+(a²-b²)k)/2=-(a²r+b²s).

Confocality together with r+s=1 gives a²r+b²s=delta, where delta=sqrt(a⁴-a²b²+b⁴). Thus the power of O with respect to every such circumcircle is -delta.

For a triangle let Delta=A>0 and R be its circumradius. The chord-length formula and d_1+d_2+d_3=pi give Delta=2ab product_i sin(d_i), product_i l_i=2ab Delta²/lambda^(3/2), and R=ab Delta/(2lambda^(3/2)). The classical signed pedal-triangle identity is B=-w_0 Delta/(4R²). It follows that

    A B = delta lambda³/(a²b²).                  (2)

Every proper physical triangle is covered by the pairwise tangency argument. Reversal preserves the product. No unproved phase-invariant factor remains in (2).

## Exact period 4 proof

Use the same F. With four distinct vertices z_1,z_2,z_3,z_4, the two neighbors of z_2 are the roots of F(z_2,w), so

    z_1 z_3=(z_2²-k)/(1-kz_2²).

The same product is (z_4²-k)/(1-kz_4²). The Mobius function here is injective because 1-k²>0 and has no denominator zero on the unit circle. Hence z_2²=z_4²; distinctness forces z_4=-z_2. Similarly z_3=-z_1. The quadratic neighbor sum is zero, forcing c=0. Thus every least-period 4 orbit is centrally symmetric and r²+s²=1, equivalently lambda=a²b²/(a²+b²). This establishes the needed coverage without importing a central-symmetry theorem.

Write the physical quadrilateral P,Q,-P,-Q, let h=cross(P,Q)>0, l_1=|Q-P|, l_2=|P+Q|. Then A=2h. The corresponding first two feet satisfy cross(q_1,q_2)=2h³/(l_1²l_2²), and the other feet are their negatives. Thus B=4h³/(l_1²l_2²). The two chord half angles are d and pi/2-d; the general length formula gives h²=lambda l_1l_2. Therefore

    A B = 8 lambda².                            (3)

The only primitive winding for N=4 is 1 or its reversal, so this is full least-period 4 coverage.

## Checkable artifacts and controls

verify_direct_geometry_01.py uses explicit RuntimeError guards, never removable assertions. Both ordinary and optimized Python runs pass. The optimized result records optimized_mode=true and intentionally rejects an actual false rational identity. No package installation was performed. All subsequent execution uses -B and sets sys.dont_write_bytecode before nonstandard imports.

Exact checks at a²=8,b²=5 cover two distinct phases each for N=3 and N=4, exact membership in E, all side tangencies, every physical reflection, distinct vertices, and reversal. Products are 11200/729 for N=3 (lambda=40/9) and 12800/169 for N=4 (lambda=40/13). A generic symbolic expansion independently verifies the classical pedal-area identity for arbitrary triangle (0,0),(x,0),(u,v) and pedal point (h,j).

An exact counterexample to repeated-list interpretation uses a=2,b=1,lambda=4/9 and two least-period six orbits:

    (2,0),(4/3,sqrt(5)/3),(-4/3,sqrt(5)/3),
    (-2,0),(-4/3,-sqrt(5)/3),(4/3,-sqrt(5)/3);

    (0,1),(-4sqrt(2)/3,1/3),(-4sqrt(2)/3,-1/3),
    (0,-1),(4sqrt(2)/3,-1/3),(4sqrt(2)/3,1/3).

Both have six distinct vertices and satisfy every exact billiard reflection. Their products are 14000/729 and 14336/729. Repeating each list twice labels it N=12 and produces products 56000/729 and 57344/729, differing by 448/243. Thus list length divisible by 4 cannot replace least period.

75-decimal-digit diagnostics independently solve the physical step and closure for (N,w)=(3,1),(4,1),(5,1),(5,2),(7,2),(8,1),(8,3),(9,4),(12,5),(20,1), plus excluded (6,1). The step comes from the positive quadratic root for v=tan(d): if D=cos²(t)/a²+sin²(t)/b² and H=(1/b²-1/a²)sin(t)cos(t), then v=lambda D/[sqrt(lambda(D-lambda/(a²b²)))-lambda H]. They test five phases each, physical reflections, closure, distinct vertices, scalar reduction, and reversal. All eligible product spreads are below 8e-72. These finite noninterval computations are diagnostic only and do not prove the general theorem.

For least (20,1), replacing complete-line feet by clipped-segment feet gives a product spread about 0.0673555963 and disagreement from the full-line product about 3.69590510. For a nonconfocal control, affine regular triangles in a²=8,b²=5 with caustic axes a/2,b/2 have product spread about 0.0980707280. These controls support the exact scope restrictions without extending them to every possible unsigned or nonconfocal construction.

## Custody incident and limits

Initial Python ordinary/optimized imports omitted -B and wrote shared-runtime bytecode caches outside this agent's assigned folder. This violated the read-only runtime boundary. The agent reported it promptly, stopped cache-writing imports, and made no deletions. RUNTIME_CACHE_INCIDENT_01.json inventories 945 regular .pyc files (30,634,652 bytes), with SHA256, inode and modification times at or after the first observed import second 2026-10-16T09:54:11Z. There was no before-state inventory; regenerated versus newly created individual cache status is therefore not claimed. No source file or other extension is included. Root independently validated the inventory and matching retained .py sources, then removed exactly those 945 regenerable cache files at 2026-10-16T09:57:15Z (A204/PRIVATE_REGENERABLE_RUNTIME_CLEANUP_01.json; inventory SHA256 a68a3f8b1fa83bc1a40818dc61f0ca3deb6bc45e8927a565085dc9b1d3aa7a5b). All source and other files were retained. A subsequent read-only check found zero .pyc files in this runtime after final -B ordinary and optimized runs. The operational incident is resolved by bounded cleanup; it is not concealed as mathematical evidence.

No original/native/foreign mathematical files, Git state, branches, refs, tracker, UI, publication, or external-person communication were edited or initiated by this agent. The unintended runtime bytecode writes are the explicit exception to the assigned-path write restriction.

Bounded direct-family audit completion: 100%. Final ordinary and optimized outputs are identical apart from the recorded optimization-mode field. Universal elementary discovery completion: 25%; exact N3/N4 and the general reduction are established, while the arbitrary-N scalar cancellation remains unproved here. Mathematical clearance of the full target and priority clearance require the independent work of the wider audit.
