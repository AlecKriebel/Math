# Author turn 2: a general lifted-intersection criterion, and failed power repairs

**Outcome:** scoped partial; the original closed-surface pseudo-Anosov construction remains unresolved. The current source claim is neither accepted from its abstract nor declared false. Turn1's three-chain finding concerns its displayed route only.

## 1. A reusable positive criterion

Retain the source's canonical based automorphism lifts A,B,C,D,E. Let G1=<A,B,C,D> and G2=<B,C,D,E> inside the based automorphism group, not merely the mapping class group. Write b=b1, z=b3 and a=a1 a4^(-1) for based loops. The explicit square action fixes a and b under C,D, and fixes b,z under E. It sends a to a z^(-1) under E.

The source's lifted chain identity is

 Q=(ABC)^4 = Ad_(z^(-1)) E².

The directly recorded coordinate maps allow this identity to be checked on based generators, rather than deduced by comparing only one test loop. Since Q and E fix z, for each integer k,

 E^(2k) = Ad_(z^k) Q^k.

Let h be any based word. Suppose:

 (i) W belongs to G1∩G2;
 (ii) W fixes the based word E^(2k)(h z^k), exactly, not merely its conjugacy class;
 (iii) V belongs to G1∩G2 and fixes h exactly.

Then

 U=Ad_(z^k) E^(-2k) W E^(2k) Ad_(z^(-k))

belongs to G1 ∩ Ad_(h^(-1)) G2 Ad_h, and so does VU.

**Proof.** The chain identity simplifies U to Q^(-k)WQ^k, proving G1 membership. Put P=E^(-2k) W E^(2k). Hypothesis(ii) says P fixes s=h z^k. Therefore

 Ad_h U Ad_(h^(-1)) = Ad_s P Ad_(s^(-1)) = P,

which belongs to G2. Hypothesis(iii) gives the corresponding membership for V, and intersections are subgroups. This is a sufficient construction criterion, with an explicit word-fixing gate; it is not a theorem that every projected lifted intersection contains pseudo-Anosovs. □

For h=b and k=1, the criterion recovers the source's choice W=(CD)^(-1)B(CD), which fixes bz. For k>1 the required word is different; replacing E² by E^(2k) is not automatically allowed.

## 2. Character invariant associated with the criterion

On the four-square representation groupoid, let δ=A2−A3. Away from the degeneracies, the two projective vectors

 v1=A4δ, v2=A1δ

are respectively G1- and G2-invariant. Here “invariant” refers to the projective line, not a fixed normalized vector. One can verify the generic mechanism directly: the two orthogonal operators B2·X·B1^(-1)−X and B4·X·B3^(-1)−X have rank2 and their two image planes meet in the line spanned by δ. The square equations place δ in both images. Distinctness of the planes and δ≠0 hold at the explicit irreducible witnesses in Turn1. A,C preserve the B data and A4, while B,D preserve the A data; this gives G1 invariance. C,E preserve the B data and A1, giving the symmetric G2 argument. Exceptional central/rank-zero cases are excluded from the generic argument, not treated as rank2.

For H=ρ(h), put

 w_h=Ad_(H^(-1))(v2),
 F_h= <v1,w_h>²/(|v1|² |w_h|²).

An automorphism in Ad_(h^(-1))G2 Ad_h fixes the projective line of w_h. This follows by precomposing the G2-invariant function with Ad_(h^(-1)); it correctly includes the fact that H itself varies with ρ. Thus F_h is invariant under the intersection in Section1, and it descends to the character quotient because both vectors transform by the same overall quaternion conjugation.

This is a conditional invariant construction. To conclude nonergodicity for a chosen projected element, one must still verify nonconstancy, an invariant conull domain and the pseudo-Anosov condition. The original h=b nonconstancy has already been certified by exact irreducible witnesses. The connected smooth full-measure character locus from Goldman–Xia supplies the setting for the usual rational-identity extension and positive-measure open-set argument. None of this turns a reducible mapping class into a pseudo-Anosov.

## 3. Why the simplest higher-power repair does not pass the gate

A natural attempt is

 R_(2k)=E^(-2k)(CD)^(-1)B(CD)E^(2k).

Increasing the power changes the curve intersections, so it could remove the three-chain degeneracy. But retaining h=b would require W to fix b z^k; changing the conjugating word to h=b^k would require it to fix b^k z^k. The known equality W(bz)=bz implies neither assertion in a nonabelian surface group.

There is an exact countercontrol on a valid irreducible representation. Set

 A1=(3+4j)/5, A2=(1+i+j+k)/2,
 A3=j A2 j^(-1), A4=1,
 B3=B4=j, B1=A1 A2 j, B2=A1^(-1)B1 A1.

For the original function F_b the starting value is1/100. The source's R_2 preserves it, whereas R_4 gives16/25. For the modified function F_(b²), the starting value is22801/62500 and R_4 gives47089/62500. Hence neither the unchanged angle nor the naive squared-conjugator angle is invariant under this proposed repair. These are exact rational values, not approximate numerics.

This rules out these specified function/element pairs. It does not rule out another invariant of R_4, another word h, another W, or a different construction. Finite tests at other powers are controls only and do not justify a universal absence claim.

## 4. A second compatible family is still reducible

Take h=a and arbitrary integer k. Since E^(2k)(a z^k)=a z^(-k), any W in <B,C> fixes the required word: B,C fix both a and z. Any V in <C,D> fixes a. The sufficient criterion therefore applies.

However, E is disjoint from both B and C in the standard chain, so E^(-2k)W E^(2k)=W as a mapping class. The projected elements obtained this way lie in <B,C,D>. Those three twists form another three-curve chain and preserve its essential boundary multicurve. This whole compatible subfamily is reducible. It is a method obstruction, not an obstruction intrinsic to the full invariant stabilizer.

The lesson is precise: changing powers can improve an intersection picture while violating the based-word condition; preserving that condition in the two simplest subfamilies leaves a reducible projected subgroup.

## Remaining gap

Find h,k,W,V satisfying the exact lifted-intersection criterion whose projected subgroup genuinely contains a closed genus2 pseudo-Anosov, or produce a materially different invariant/construction. The original source problem remains unresolved2/5. No publication status correction is justified by the current preprint audit. The next author research turn must address this genuine pseudo-Anosov existence step; an independent review of another problem intervenes as scheduled.
