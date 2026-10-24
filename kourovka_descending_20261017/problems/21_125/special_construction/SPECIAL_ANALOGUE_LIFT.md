# Attempt to lift through the established special Hydra analogues

October24,2026 UTC. This is an unsuccessful distinct algebraic mechanism, not a solution or proof that every lift is impossible.

Brady–Soroko's primary paper (author copy dated August28,2020), §5.1, defines the following groups for **m≥1 and 0≤k≤m**:
\[
B_{m,k}=\langle a_1,\ldots,a_{m+k+1}\mid
[a_i,a_{i+1}]=1\ (1\le i\le m),\quad
 a_{m+j+1}^{-1}a_j a_{m+j+1}=a_{m+j}\ (1\le j\le k)\rangle.
\]
The base B_(m,0) is the RAAG on a path, and successive displayed cyclic HNN extensions inject it by Britton's lemma. The paper supplies explicit finite special covers for its chosen analogues. These are different groups from the ordinary Hydra family.

There is an evident surjection onto the ordinary Hydra H_(k+1): send a_1,...,a_m to s, send a_(m+1) to u_1, and send a_(m+j+1) to u_(j+1). Every commuting base relation becomes trivial except [s,u_1], and the jth HNN relation becomes u_(j+1)^-1 s u_(j+1)=u_j. The images generate H_(k+1), proving surjectivity.

A surjection from a virtually special group provides no virtual-specialness conclusion for its quotient; even a free group surjects onto every finitely generated group. To obtain a useful mechanism here one needs a section (or an independent finite-index injection), which the quotient does not supply.

Two natural proposed generator lifts already fail exactly:

1. Lift s to a_1, u_1 to a_(m+1), and higher u's to their displayed stable letters. For m≥2, a_1 and a_(m+1) are nonadjacent vertices in the base path RAAG. Their commutator is nontrivial there, and stays nontrivial in B_(m,k) because the base injects through the HNN tower. Thus this lift fails the first Hydra relation.
2. For **m≥2 and 1≤k≤m**, lift s to a_m and u_1 to a_(m+1), which repairs the commuting base pair. Then the proposed u_2=a_(m+2) conjugates a_1, rather than a_m, to a_(m+1). For m≥2 the word a_(m+2)^-1 a_m a_(m+2) a_(m+1)^-1 is reduced in the first HNN extension: a_m is not in the associated cyclic subgroup <a_1>. Britton's lemma proves it nontrivial, and it remains so in later extensions. Thus the very next relation fails.

These computations refute only the obvious sections, not all possible word lifts. No nontrivial section candidate has survived even these initial relations. A section into a virtually special analogue would be a sufficient route-specific construction; no converse has been proved. No such section has been constructed here, so this proposed route remains blocked by an unsupported sufficient condition. Virtual specialness might instead be proved by an entirely different mechanism.
