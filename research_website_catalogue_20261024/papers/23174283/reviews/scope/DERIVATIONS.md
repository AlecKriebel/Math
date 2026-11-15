# Independent derivations and source-interface checks

Record 23174283, scope/source family. These deductions were reconstructed from the target and then checked against actual primary bodies. The initial six-family reconstruction was sealed before foreign bodies, supplied code/results, or opinions. Finite diagnostics below supplement these deductions.

## Exact all-integer arithmetic route

Let n≥3, q=F_n, p=F_{n−1}, 1≤m<q and ℓ∈Z. The repeated Fibonacci value 1 causes no ambiguity after requiring j≥2: exactly one j has F_j≤m<F_{j+1}. Put h=n−j≥1. The adjacent vectors (F_j,F_{j−1}) and (F_{j+1},F_j) have determinant (−1)^{j−1}, hence give integral coordinates S,T for (m,ℓ). S=0 is impossible, as it would make positive m<F_{j+1} an integral multiple of F_{j+1}. If T≠0 then S,T must have opposite signs; if T=0 then S>0. The two recurrence identities are

    p F_j − q F_{j−1} = (−1)^{j−1} F_h,
    p F_{j+1} − q F_j = (−1)^j F_{h−1}.

Consequently |mp−ℓq|=|S F_h−T F_{h−1}|≥F_h. Opposite signs prevent cancellation; the T=0 case uses S≥1. This remains valid at h=1 because F_0=0. Finally

    q = F_j F_{h+1}+F_{j−1}F_h ≤ 3F_jF_h ≤ 3m|mp−ℓq|.

This establishes the needed bound for every ℓ, rather than merely for one selected nearest residue. It requires no estimate imported from the literature. The exact stronger index credited to Zaremba and SCN is therefore an attribution/interface check, not a missing premise of the target proof.

## Global geometry and equality

For 0≤a<b≤1, d=b−a and longitude cosine c, set U=2(a+b−2ab), V=4√[a(1−a)b(1−b)]. Direct scalar products give D²=2(U−cV), U−2d=4a(1−b)≥0 and V²=U²−4d². If c≤0 then D²≥4d. For 0<c<1, U>V≥0 because d>0. Thus U−cV>0, and

    (U−cV)²−4d²(1−c²)=(V−cU)²≥0

can be square-rooted without a sign ambiguity, giving D²≥4d√(1−c²). This is a global inequality including poles; it does not assume that the Lambert map preserves planar distances.

For any target pair i<j, m=j−i and d=m/q. Consecutive Fibonacci coprimality makes the nearest residue r=mp−ℓq nonzero, with |r|≤q/2. In particular c=1 cannot occur. When c>0, |r|<q/4, so the sine lower chord on [0,π/2] gives

    D² ≥ (4m/q)sin(2π|r|/q) ≥ 16m|r|/q² ≥ 16/(3q) > 4/q.

For c≤0, D²≥4m/q≥4/q. The north-pole pair {0,1} has squared chord 4/q. Equality in the latter chain requires m=1 and U=2d. Since j<q, b<1, and 4a(1−b)=0 then forces a=0. Thus the unique unordered pair is exactly {z_0,z_1}. No exceptional numerical treatment of q=2,3,5 is necessary. On the unit sphere geodesic distance is 2arcsin(D/2), a strictly increasing function of chord D, yielding the stated geodesic minimum.

## Exact source dictionary

Write Φ(α,t)=(2√[t(1−t)]cos(2πα), 2√[t(1−t)]sin(2πα),1−2t). The target is T(k)=Φ(pk/q,k/q), 0≤k<q.

* Brauchart printed p.2438 displays precisely this formula and range, and explicitly identifies the pole/next-point chord as the conjectured minimum. Its next set notation instead uses indices 1,…,q. Define R(x,y,z)=(x,−y,−z). Since p is integral, T(q−j)=R T(j) for 1≤j≤q. Therefore these two q-point endpoint conventions are isometric, with closest pair indexed {q−1,q} under the latter convention. Including both endpoints gives q+1 points and two pole-adjacent minimizing pairs; it cannot inherit the target uniqueness claim.
* ABD's actual 2012 Section 5.2 starts with f_j=(j/q,{pj/q}), then applies the same Φ. Its point A(j)=Φ(j/q,{pj/q}) has height parameter k/q for k=pj mod q. Cassini gives p²≡(−1)^n (mod q), so the target longitude at k is (−1)^n j/q modulo 1. Therefore A(j)=(T_x(k),(−1)^n T_y(k),T_z(k)). Multiplication by p permutes residues; the unordered sets are exactly isometric. Odd n requires the y reflection. No arbitrary rational multiplier has this self-inverse-up-to-sign property.
* The dual lattice condition in SCN is h_1+p h_2≡0 (mod q). The vector (−r,m) lies in it. Both components are nonzero, so its max-factor product is m|r|. SCN Theorem 2.2 explicitly states the exact index F_{n−2}, for n≥3, using F_1=F_2=1. Zaremba's printed p.186 gives the same index and generator (1,F_{n−1}) at modulus F_n. The bound F_{n−2}≥q/3 follows from q=2F_{n−2}+F_{n−3} when n≥4; n=3 is immediate. These agree with the target's credits.

## Checkable diagnostics and falsifiers

`independent_verifier.py` reads no supplied results and writes no files. It uses explicit runtime guards, integer arithmetic and rational fractions, so optimization cannot disable its checks. Its normal and optimized outputs agree. It checks Cassini/coprimality for all 198 indices 3…200; 2,581 exact reversed-coordinate residues; 1,274 endpoint identities; 1,323 unit-norm height identities; 1,539 rational geometric pairs; and all 1,581 nonzero offsets through q=610 against the product bound and exact index. These are finite diagnostics, not the universal argument above.

Four exact negative controls reject substitutions: p=3,q=5 needs the odd reflection; p=3,q=7 is not its own inverse; midpoint heights have no index-zero pole; Φ(0,0) and Φ(0,1/2) have squared chord 2 while their planar squared distance is 1/4. They identify genuine convention failures without alleging them in the target.

The supplied, independently inspected package additionally passed all four positive routes and all five intentionally false mathematical controls. The rational direct-chord route derives π intervals by Machin's identity and alternating series, then uses a cosine upper Taylor bound and rational inequalities. Its branch/sign conditions are explicit. The conventions program includes floating coordinate checks, which remain convention diagnostics, while modular identities are exact. No supplied finite route establishes the infinite theorem or priority.
