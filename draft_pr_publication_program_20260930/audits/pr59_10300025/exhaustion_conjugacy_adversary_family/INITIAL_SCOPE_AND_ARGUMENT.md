# Independent start — before candidate or inherited review

2026-10-03 16:32 UTC. Family: nested interval exhaustion / endpoint barriers. Original head supplied by ROOT: bdee508c676c98cb96dbc1a2e5aef2fe9cd1c744. Read only root AGENTS and the literal original source_record.json at this point; its SHA256 is 3219f4c402af980ad96bd00e9f86733fd9e39e27cd33726c5f6b72e3f296fd48. No candidate proof, author program, historical review, known-result prose, prior verdict, or other new reviewer argument has been read.

Literal target: for the leaf-space action rho_H of pi_1(M) of an R-covered foliation of an atoroidal 3-manifold, find one topological conjugacy after which

    | d(rho_H(alpha)(p), rho_H(alpha)(q)) - d(p,q) | <= C(alpha)

for every alpha,p,q, with finite positive C(alpha) allowed to depend on alpha. The raw source record labels the historical literature triage open/unverified. This label is not adopted as a present priority conclusion. Success requires a universal proof, not finite samples. Independently checking whether the primary question imposes additional geometric conditions remains necessary.

Independent proposed universal argument: let g_1,g_2,... enumerate an arbitrary countable image in Homeo(R), permitting both orientations. Put I_0={0}. Recursively choose I_n=[l_n,r_n] with strict nesting, l_n<-n, r_n>n, containing each g_j(I_(n-1)) and g_j^(-1)(I_(n-1)) for j<=n in its interior. This is possible because there are finitely many compact image intervals. Define increasing h by h(0)=0, h(l_n)=-n, h(r_n)=n and affine interpolation on each interval between successive marked points. These points exhaust both ends, so h is an increasing homeomorphism.

For n>=i, forward containment g_i(I_n) subset I_(n+1) supplies an outer image barrier. Inverse containment g_i^(-1)(I_(n-1)) subset I_n supplies an inner barrier at each appropriate end, with monotonicity determining which endpoint is used. Consequently, for orientation sign epsilon_i, g_i(r_n) has h-coordinate in [n-1,n+1] when epsilon_i=+1 and [-n-1,-n+1] when epsilon_i=-1. The analogous statement holds at l_n. For |t|>=i, affine h and monotonicity imply |h g_i h^(-1)(t)-epsilon_i t|<=2. On [-i,i], forward containment bounds the image in [-i-1,i+1], giving a global bound K_i=2i+1. The reverse triangle inequality then gives global additive distance distortion at most 2K_i=4i+2.

This mechanism uses no invariant measure, countable summable weights, orbit enumeration within a dense orbit, differentiability, faithfulness, or geometric foliation data. Inverses and both endpoint directions are essential. Group-wide uniform C is not claimed. For a finite image, repeat identity in the enumeration. For a nonfaithful action choose an index of each image map. The usual second-countable 3-manifold fundamental group is countable; the exact primary context still needs checking. This is an initial independent argument to adversarially verify, not yet an accepted result or priority claim.

Checkpoint: mathematical validation estimate 45%; independent proof candidate obtained, edge-case audit and primary/candidate comparison pending. All work remains private to this family; no Git, native queue, production, remote, or publication mutation.
