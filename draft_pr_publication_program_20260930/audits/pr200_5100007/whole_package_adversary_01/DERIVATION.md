# Independent derivation before supplied reports

Checkpoint UTC: 2026-10-16 05:06:00 UTC. Completion estimate 35%.

I have now read only the current manuscript, theorem contract, executable checkers/requirements, metadata, package index/seal, and direct Stachel/Ferudun primary PDF extracts. No supplied supporting derivation, historical proof, priority report or audit conclusion has yet been read. The following reasoning is mine, reconstructed to challenge the current proof.

## Exact hypothesis and published scope

The assertion concerns a>b>0, proper nested confocal axes alpha>beta>0 with 0<lambda<b², and least billiard period N>=3. Each focus is an original common focus, each outer vertex is the intersection of the *boundary* tangents at consecutive impacts, and the product consists of ordinary positive distances over one primitive orbit. The family parameter changes with axes and winding fixed. The assertion is each one-focus product is constant iff 4 divides N; repeats preserve this criterion. Circle/degenerate/hyperbolic/separatrix/N=2 exclusions are material.

Stachel's published Theorem 4.3 and (4.9), read directly from the supplied source PDF, give modulus c/alpha (his letter m denotes modulus), P(u)=(-a sn u,b cn u), cn v=beta/b and a=alpha dn v/cn v, v=2tau K/N; the impact step is 2v. The source includes arbitrary coprime turning numbers and initial parameter. Its preceding displayed dn(u+2kK)=(-1)^k dn(u) is contradicted by standard dn real-period data, but is not necessary for this theorem's parameter relation. DLMF 22.4, read directly online, has dn(u+2K)=dn(u), dn(u+2iK')=-dn(u), and the correct shifts. Thus squaring gives the manuscript's lattice, while treating dn itself as 2iK'-periodic would fail.

## Geometry independently reconstructed

Write s=sn u,z=cn u,d=dn u,h=sn v,C=cn v,D=dn v and Delta=1-k²s²h². Since 0<v<K, all h,C,D,d,Delta are positive for real u. Addition formulas give sn(u±v)=(sCD±hzd)/Delta and cn(u±v)=(zC∓shdD)/Delta. Substitution shows Q=(-aDs/C,bz/C) solves both tangents. Their coefficient determinant has magnitude 2hCd/(ab Delta)>0. Also Qx²/a²+Qy²/b²-1=h²d²/C²>0, so the vertex is outside E and cannot be either interior focus. These facts are independent of N or winding. The chord through the two impacts has equation -x s/alpha+y z/beta=1: substitution gives (D s sn(u±v)+z cn(u±v))/C=1. This supplies a direct compatibility check on the canonical half-step and caustic.

## Algebra independently reconstructed

Use kappa=k²,t=sn²v,q=1-t, S=sn²u. Then the outer semiaxes are Ao=alpha(1-kappa t)/q and Bo=alpha sqrt(1-kappa)/q, while c²=alpha²kappa. With U=1-2kappa t+kappa t² and V=1-2t+kappa t², direct distance multiplication gives

H=[(Bo²+c²)+(Ao²-Bo²)S]²-4c²Ao²S
 =alpha⁴/q⁴[(U+kappa V S)²-4kappa(1-kappa t)²q²S]
 =alpha⁴/q⁴(1-kappa S)(U²-kappa V²S).

Here U+V=2q(1-kappa t), and double angle gives dn delta=U/W, cn delta=V/W with W=1-kappa t²>0. Thus H=Cv dn²u [dn²delta-k²cn²delta sn²u], Cv=alpha⁴W²/q⁴>0. This is a squared *paired* ordinary distance, not a one-focus square. Each squared distance also factors as alpha²W/q²(1±k sn u)(dn delta±k cn delta sn u); all real factors are positive because dn²delta-k²cn²delta=1-k²>0.

## Lattice, orders, and exceptional case

On T=C/(2K Z+2iK' Z), sn² is a degree-two meromorphic function with one double pole p=iK'; dn²=1-k²sn² has a double zero at p+K and double pole p. DLMF's shift sn(z+K+iK')=dn z/(k cn z) implies that B(u)=dn²delta-k²cn²delta sn²u vanishes at p+K±delta. For 0<delta<2K, cn delta vanishes only at delta=K. Otherwise B retains a double pole at p and is nonconstant. Its two listed zeros cannot coincide unless 2delta is in the real lattice 2K Z, giving delta=K. Neither zero is p or p+K. Their distinctness and degree two prove each has order one; no derivative assumption is needed. Therefore div H=2[p+K]+[p+K+delta]+[p+K-delta]-4[p]. If delta=K, B=k'² and div H=2[p+K]-2[p]. Closure forces N=4,tau=1 in this exception. This reasoning covers every k in (0,1); no hidden special modulus can change the degree.

## Universal subgroup proof and ordinary products

Modulo T, delta/(2K)=2tau/N has additive order L=N/gcd(N,2), because gcd(tau,N)=1. For F=product_(j=0)^(L-1) H(u+jdelta), translating the complete divisor (including repeated zeros between factors) gives 4O_(p+K)-4O_p in the nonexceptional case. The two cosets are either equal or disjoint. They coincide iff the real cyclic subgroup of order L contains its unique order-two point K, iff L is even, iff 4 divides N. At N=4 the coefficient is two and the same cancellation occurs. A zero divisor on the compact connected torus makes F constant; its real value is positive. Otherwise the nonzero divisor prevents constancy.

For every N, Q(u+2K)=-Q(u), hence Rminus(u)=Rplus(u+2K), independently of whether -Q lies in the same orbit. Also Rplus² Rminus²=F^(N/L). Thus constancy of either one-focus product forces both constant and forces F^(N/L) constant on a real interval free of poles. Its meromorphic identity extension on the connected torus would contradict the nonzero divisor when 4 does not divide N. This establishes necessity for odd N without illicit antipodal orbit pairing. For 4|N, N/2 steps add 2K tau and tau is odd, so actual orbit antipodal pairing gives Rplus=Rminus and Rplus²=F. Positivity allows the unique ordinary square root. Coprime star generators all produce the same subgroup; reversing direction only permutes lengths. Repeating r times produces R±^r and cannot change constancy on positive reals.

## Current result and remaining challenge

No analytic gap or counterexample has been found in the universal criterion. This is a checkable derivation, not a reliance on sampled output. Remaining work: independent computations, explicit guards and expected-output replay, all payload text/source/timeline consistency, ZIP and seal verification, and PDF layout. Historical novelty is not concluded. The direct competing PDF's Theorem 1 indeed states the same positive theorem for every coprime winding and supplies a closely overlapping factor/divisor method; manuscript attribution is necessary and substantively appropriate.
