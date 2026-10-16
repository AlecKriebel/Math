# Package06 early independent checkpoint

UTC: 2026-10-15T03:50:23.999000+00:00. Estimated review completion: 15%.

This checkpoint predates reading any prior review conclusions. Inputs examined: current TeX in full; Hayman–Lingham printed p.143/PDF p.144; Duren 1981 printed pp.352–355. Publication input inventory and hashes are frozen in INPUT_FREEZE.json. The three requested frozen payload hashes agree.

## Exact claim and independent reconstruction

For epsilon=10^-24 every global maximizer of Re[a2+i epsilon(a4-3a3)] exists by compactness of S, is a genuine support point since identity and Koebe give 0 and 2, and omits one analytic arc with increasing modulus. The published Duren trajectory convention directly agrees with the manuscript. It is crucial that the proof starts with actual global maximizers: a positive trajectory alone does not establish support extremality.

The comparison with Koebe and |an|<=n gives Re a2>=2-13 epsilon and |a2-2|<8 eta, eta=10^-12. Odd-root area theorem controls a3 uniformly and controls the H=sqrt(z/f) tail. Thus A=2a3+a2^2-6a2=-2+O(eta), B=3a2-3=3+O(eta), with manuscript constants 106 and 24. Extraction of f^2,f^3,f^4 at degrees <=4 gives Q=-a/w^3-b/w^4-c/w^5, a=1+i epsilon A,b=i epsilon B,c=i epsilon. Pullback w=-v^-2 gives exactly 4(a-bv^2+cv^4)dv^2. The polynomial is uniformly near 1 on |v|<=3, so the positive-real-root coordinate G is locally invertible and has a unique inverse for |t|<2 by Rouche. Infinity has only one projected positive trajectory because the two real G rays are identified by v to -v.

## Distinct tip mechanism constants

Recompute the actual-tip estimate at z=-3/4, rather than the manuscript's -2/3. Here H0=7/4, k=-12/49 and k'=16/343. The same area tail gives |H-H0|<5 eta and |H'-H0'|<12 eta, since r^4/[3(1-r^2)]=27/112 and (1-r^2)^-2-1=207/49. On 1.7<|H|<1.8, the algebraic identities give |f-k|<2 eta and |f'-k'|<6 eta. The inverse-disk Schwarz estimate then gives actual tip radius <13/49+5 eta<0.27. The constructed W for 0<t<=7/4 has radius >25/81>0.30. Therefore a genuine finite tip cannot interrupt continuation. At every other intersection Q is regular/nonzero, so horizontal natural-coordinate uniqueness makes the coincidence set both open and closed. This excludes the key possible failure of mistaking a nearby trajectory for the actual slit.

## Distinct sign-reversal mechanism

An alternative expansion avoids differentiating the inverse: write Z=G(v)/(v p(v)) with v=V(t). Since p=1+(i epsilon/2)P0+O(epsilon eta), G/v=1+(i epsilon/2)average(P0)+O(epsilon eta). The coefficient difference is (average(P0)-P0)/2=v^2-(2/5)v^4. Thus Z=1+i epsilon q(v)+O(epsilon eta), and |v-t|<=333 epsilon replaces q(v) by q(t) at only O(epsilon^2) cost. This directly verifies q(1)=3/5 and q(7/4)=-441/640 with margins much larger than the remainder. Re Z>0 fixes outward orientation. Argument derivative changes sign. Signed outward radial angle tends to zero at infinity and has both signs; its absolute value has an interior zero between positive endpoint values. Both monotonic directions fail for signed and unsigned conventions. At epsilon=0 the mechanism vanishes, consistent with Koebe. All coefficient estimates apply to every maximizer, with no uniqueness or selection dependence.

No mathematical flaw found in this independent first pass. Remaining work: check numerical constants with independent exact controls; inspect full actual package, all runner and producer behavior, clean offline jobs, byte rebuilds, visual PDF, provenance and priority/source claims under the user's expressly accepted limits.
