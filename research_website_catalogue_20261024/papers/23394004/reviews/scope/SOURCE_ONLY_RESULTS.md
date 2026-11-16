# Exact source-only hand controls — 23394004

2026-11-16T12:01:03Z. All calculations below are written exact arithmetic; no scientific program, archived result or foreign body used.

1. The middle factorization identity reduces to d²−mqt=U, q−d²t=V and U+V=2qd². Therefore d²(V²−U²t)+q(U²−mV²t)=UV(U+V), giving the required coefficient exactly. This tests the actual factorization, not just a sampled value. The translated determinant and two distance products leave q⁴, dimensionally inverse length² per edge.

2. Critical triangle:3v=2K implies v=2K/3 and τ/N=1/3, so primitivity givesN=3,τ=1. Here the second linear factor is Z(1−k snu), with its degree-two zero atK+p. dnu vanishes simply there and the first factor is nonzero (d+C), so the resulting pole is at most simple. Omitting this case would exclude the smallest claimed period. L1=0 instead requires N=6τ, which is excluded by oddness; it must not silently be covered by the common-Jacobi-pole order count.

3. Cartesian triangle family check. Put a=√21,b=4,c=√5,α=3a/5,β=8/5. Then inner axes²189/25,64/25 differ by5, and caustic parameter336/25 gives the stated strict confocal ellipse. PhaseA original vertices (a,0),(-3a/5,16/5),(-3a/5,-16/5). The latter two share vertical tangent-to-caustic chord x=-α; the other side normals (2/a,±1) give caustic support²4α²/a²+β²=4. Incoming/outgoing unit vectors at the upper-left vertex differ by(-a/5,7/5), seven times its outer-ellipse normal(-a/35,1/5); thus reflection is exact. The outer tangent intersections are (a,8),(-5a/3,0),(a,-8).

For a focus f=(f,0), f²=5, the symmetric outer pair has x=a−f, squared distance D=(a−f)²+64=2(45−af), and the middle inverse coordinate is1/(-5a/3−f). Direct three-edge shoelace simplification gives B_f=8/[15(7a+f)]. Hence B_+B_-=64/[225(49a²−c²)]=64/(225·1024)=1/3600. Inverting the ORIGINAL triangle instead gives B_f^orig=16/[9(7a+f)], product1/324. This explicitly distinguishes the target from k903,a.

4. A second exact phase in the same family is (0,4),(-21/5,-8/5),(21/5,-8/5). Its oblique chords have normals(±4,3), support12 and caustic support²16α²+9β²=144. At the lower-right vertex, incoming/outgoing unit vectors differ by(8/5,-4/5), eight times its outer normal(1/5,-1/10), so reflection holds. Outer tangent intersections are(-7,4),(0,-10),(7,4).

Relative to a focus f²=5, their squared distances are D_A=14(5+f),D_B=105,D_C=14(5−f). The successive relative determinants are D_A,D_C,56. Thus B_f=(1/2)[2/105+56/(D_AD_C)]=(1/2)[2/105+1/70]=1/60, so the product is1/3600 again. For the original vertices, distances are21,(42/5)(3+f),(42/5)(3−f); relative edge determinants are(28/5)(3+f),336/25,(28/5)(3−f). Shoelace gives B_f^orig=(1/2)[4/63+1/21]=1/18, product1/324. Individual focus areas differ between phases, while their product agrees; the universal proof is still required beyond these controls.

5. Focus/scale controls: (A²−B²)−c²=−α²m(1−m)t²/q²<0, so replacing the original foci with outer-locus foci changes the construction. Unit inversion under a whole similarity s changes translated inverse vectors by1/s, hence the product by s^(−4). Common radiusρ gives product factorρ⁸. For a unit-circle triangle θ=2π/3, outer radius2, each central inverse area3√3/16 and product27/256; this matches the direct circular formula.

Source-only result: full internal analytic argument coherent with exact hand controls; no internal defect located. Exact remaining gap is primary target/canonical/Jacobi interface validation, CLOSED pending per-paper GO. Completion45%, follow_up:null. No firstness/current-openness conclusion or scientific code execution.
