# Second independent audit: Kirby Problem 4.115(a)

Date: 2026-10-08

## Verdict

**Pass.** The argument in `PART_A_PROOF.md` gives a mathematically complete affirmative answer to part (a) of Problem 4.115 as formulated in the inspected 2026 K3 problem list. I found no missing mathematical hypothesis or invalid inference. The example is a closed oriented smooth 4-manifold with fundamental group C8 and two orientation-preservingly diffeomorphic, non-isotopic balanced (3,1)-trisections. The non-isotopy proof remains valid when every permutation of the sectors is allowed. The genus-minimality claim is also correct.

This verdict concerns proof validity and exact problem scope. It is not a claim of novelty, publication, or external peer review. Part (b) remains unresolved by this construction.

Audited proof SHA-256: `90be5ae3ab394227e9b22db5db3c49e1798714f70a7c554eed4fadb539ee820b`.

The proof was read and checked independently against primary sources; no first-audit document was consulted. The proof itself was not edited.

## 1. Exact source scope and equivalence relation

I inspected the problem and its surrounding remarks in the [2026 K3 preliminary author PDF, printed page 286](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf#page=286), including the rendered page. Part (a) requests a diffeomorphic/non-isotopic pair on the same 4-manifold. Part (b), separately, adds the closed simply connected condition and asks for balanced, equal-genus trisections that are non-diffeomorphic. The simply connected qualifier does not govern part (a).

The first remark explicitly discusses orientation-preserving diffeomorphisms, their isotopy classes, and the possibility that a nontrivial diffeomorphism could preserve the initial sectors setwise. The present homology obstruction addresses precisely that loophole; merely observing that F acts nontrivially on homology would not suffice.

For the formal convention, [Islambouli, Section 4.2 and Proposition 4.5](https://arxiv.org/html/1804.06978v2) uses ambient isotopy starting at the identity and carrying corresponding sectors to corresponding sectors. The draft proves the stronger assertion with arbitrary final sector permutations. Thus it satisfies both the labeled convention and the weaker unordered equivalence convention. Possible additional orientation constraints on sector permutations only reduce the allowed maps and cannot invalidate the obstruction.

## 2. The lens-space map and orientation

Take the quotient specified in the proof, rather than relying on a naming convention for lens spaces. The deck generator is

    d(z1,z2) = (zeta z1, zeta^3 z2), with zeta^8 = 1 primitive.

The action is free: a fixed point has a nonzero coordinate, and either 8 divides the exponent or 8 divides three times the exponent. Since 3 is invertible modulo 8, either condition forces the deck transformation to be the identity. Therefore the quotient has universal cover S3 and fundamental group C8.

For s(z1,z2)=(z2,z1), direct multiplication gives s d s^-1=d^3. This is an actual self-map of the specified quotient. The real determinant of the swap on C2=R4 is positive: swapping two real 2-planes has determinant (-1)^4=1. It preserves the unit ball and the outward normal, so its restriction to the sphere and the descended map preserve orientation.

If a lifted loop ends at d x, the image lifted loop ends at d^3 s(x). Consequently the induced automorphism is multiplication by 3. A basepoint change can introduce only an inner automorphism, which is trivial here; alternatively one can work entirely in H1. No classification theorem for lens-space mapping classes is needed.

## 3. Fixing a ball is legitimate

The represented diagonal point is genuinely fixed by s. On the tangent 3-space, the plus eigenspace is one-dimensional and the minus eigenspace two-dimensional. Thus the derivative is a rotation by pi, not an orientation reversal. The descended map is an isometry for the quotient round metric. The equivariance of exponential coordinates at a fixed point therefore identifies it exactly with this linear rotation throughout a sufficiently small normal ball.

The radial correction b(v)=R_{-pi chi(|v|)}v preserves the radius. Its explicit inverse has the opposite rotation at the same radius, so it is a diffeomorphism, not merely a local formula. It is smooth at the center because chi is constant there, and extends smoothly across the outside of the chart because chi vanishes near the outer boundary. The same construction with angle multiplied by t supplies an isotopy from the identity to b.

On a smaller ball where chi=1, b composed with s is the identity. One can choose the closed ball B strictly inside that region, obtaining identity on a whole neighborhood of B. This stronger collar statement is exactly what the spin construction needs. Since b is isotopic to the identity, composing with it leaves the H1 action equal to multiplication by 3. There is no unsupported use of a general ball-fixing theorem.

## 4. The spun map and its homology action

The displayed spin agrees with [Meier's definition, Section 2.1](https://arxiv.org/html/1708.01214v1): glue the punctured 3-manifold times S1 to S2 times D2 along their product boundary. The map f times the identity on the first piece equals the identity near the entire gluing boundary. It therefore glues smoothly to the identity on the cap. Smoothing corners causes no problem because both maps agree on a collar. It preserves the natural spin orientation.

Van Kampen on M=M-circ union B gives pi1(M-circ)=C8, because the intersection sphere is simply connected. For the spin, the first piece has group C8 times Z, the cap is simply connected, and the boundary group Z maps to exactly the S1 factor. The pushout is therefore C8, not C8 times another cyclic factor.

The inclusion of a fixed M-circ slice supplies the identification, and F composed with this inclusion equals the inclusion composed with f. Hence F induces multiplication by 3 on H1 of the spin. This explicitly proves the required naturality. No claim that a particular spun trisection construction is equivariant under f is needed or used.

## 5. Existence of the trisection

The two invariant solid tori on S3 descend to solid tori in the quotient. One can additionally check this without the mapping-torus description: on the first torus, in the proof's coordinates (w,u), the invariant coordinates (w u^6,u^8) identify its quotient with D2 times S1. On the second torus, with w=z2/z1 and u=z1/|z1|, use (w u^-2,u^8). These maps have exactly the deck orbits as fibers. The common boundary is a torus. Thus the quotient has a genus-one Heegaard splitting.

[Meier, Theorem 1.2](https://arxiv.org/html/1708.01214v1), states that a genus-k Heegaard splitting of a closed connected orientable 3-manifold yields a (3k,k)-trisection of its spin and twisted spin. Its k=1 case applies with no extra restriction. In particular, the extra diagram hypothesis in the separate Theorem 1.4 is not an assumption of Theorem 1.2.

Choose any such trisection T on X and define the second trisection as its actual image F(T). This supplies the diffeomorphism between the two with the required sector correspondence. One does not have to identify F(T) with a second output of Meier's construction, specify the three sector classes in advance, or choose B compatibly with the displayed genus-one splitting.

## 6. Sector surjectivity

The draft's van Kampen argument is correct and applies to unbalanced trisections as well.

For any sector Xj, either handlebody in the Heegaard splitting of its boundary surjects onto pi1(boundary Xj): one obtains the boundary by attaching only 2- and 3-handles to that handlebody. The inclusion of the boundary of a 4-dimensional 1-handlebody induces an isomorphism on fundamental groups. Hence pi1(Hij) surjects onto pi1(Xj).

In the pushout for Xi union Xj, all generators from Xj can consequently be represented by loops already in Xi. Thus Xi surjects onto the fundamental group of the union. The intersection of this union with the last sector Xk is Hki union Hkj, namely the entire boundary of Xk; that boundary again surjects onto pi1(Xk). The second pushout creates no new generators. Collar neighborhoods justify ordinary open-cover van Kampen if desired.

This proves that each sector surjects onto pi1(X). It agrees with the handle-decomposition explanation immediately before [Islambouli's Proposition 4.5](https://arxiv.org/html/1804.06978v2), where any chosen sector supplies the 0- and 1-handles. The proof does not rely on identifying the abstract sector group with the ambient group.

## 7. The invariant and every permutation caveat

For a sector Xi diffeomorphic to S1 times B3, the image of a generator of H1(Xi;Z) is a generator of C8. The only choices of a generator of the infinite cyclic domain differ by sign. Therefore the unordered set of these two possible images is intrinsic to the embedded sector. The possible values are A={1,7} and B={3,5}.

If h is ambiently isotopic to the identity and takes Xi to a sector Y, the naturality square for inclusion maps commutes. The ambient H1 map is the identity, while the sector H1 map is multiplication by plus or minus one. Thus the class of Xi equals that of Y. This explains why quotienting by the full automorphism group of C8 would be incorrect for this isotopy problem: that would discard the fixed ambient identification which isotopy preserves.

There is no arbitrary-marking defect. Choosing another isomorphism H1(X)=C8 multiplies all images by the same unit, which merely exchanges or preserves the names A and B. Multiplication by 3 still interchanges them because C8 is abelian and these scalar automorphisms commute.

F sends each sector class to the other class. If T has a sectors of class A, F(T) has 3-a such sectors. Equality after any permutation would require a=3-a, which has no integral solution. This excludes all six permutations, even with independent sign changes in the three sector generators.

As an independent algebraic cross-check, any permutation on three letters has an odd-length cycle. Along such a cycle, the equations r_i=epsilon_i 3 r_sigma(i) combine to r_i=epsilon 3^ell r_i with ell odd. Since 3^2=1 modulo 8, this requires 1=plus or minus 3 modulo 8 after cancelling the unit r_i, which is impossible. This reaches the same conclusion without counting A and B.

In particular, the argument excludes the possibility mentioned in the problem's first remark: there cannot be a trisection-preserving diffeomorphism whose H1 action cancels that of F so as to make F(T) isotopic to T. Nontrivial homology action alone would leave that possibility open; the sector invariant closes it.

## 8. Genus and stabilization

The spin has Euler characteristic 2: the product with S1 and the gluing boundary have Euler characteristic zero, while S2 times D2 has Euler characteristic two. For a (g;k1,k2,k3)-trisection, inclusion-exclusion yields chi(X)=2+g-k1-k2-k3. Sector surjectivity and pi1(X)=C8 force each ki to be at least one. Consequently g=k1+k2+k3 is at least three, including for unbalanced trisections. The exhibited pair is therefore minimal-genus.

[Gay and Kirby, Theorem 11, published page 3101](https://msp.org/gt/2016/20-6/gt-v20-n6-p02-p.pdf#page=5), establishes ambient isotopy after sufficiently many stabilizations. There is no contradiction: this proof is rank-one and makes no stabilization-persistence claim. It also makes no non-diffeomorphism claim, since F explicitly supplies a diffeomorphism.

## 9. Prior-work and novelty check

The appropriate conceptual credit is Islambouli's Nielsen-class framework. In rank one, the present obstruction reduces to the elementary plus-or-minus ambiguity of an infinite cyclic generator, so a classification of higher-rank Nielsen classes is unnecessary.

I checked the cited Meier and Islambouli primary texts, their relevant theorem statements, and targeted searches for the exact diffeomorphic/non-isotopic phrase, L(8,3), lens-space spins, and Nielsen-based examples. I did not locate an earlier explicit statement of this precise pair or a primary-source result already asserted as an answer to 4.115(a). That negative search result is limited evidence and does not establish novelty.

Two potentially misleading adjacent hits were checked. The [2025 Kyushu seminar announcement](https://www.math.kyushu-u.ac.jp/activities/13100/) identifies its examples as a survey of Islambouli's 2021 work, not a new construction. [Aranda and Zupan's 2025 paper](https://arxiv.org/html/2503.04607v1), especially its introduction and Section 8, concerns weak reducibility and the diffeomorphism classification of genus-three trisections/manifolds; the inspected statements do not provide this ambient-isotopy distinction or contradict it.

The published DOI endpoints were not accessible through the research tool during this audit. The key existence theorem, spin definition, and Nielsen-invariant statements were directly verified in the authors' arXiv texts. This access limit does not leave a mathematical dependency unchecked, but the audit does not claim a page-by-page comparison with both final journal versions.

## Final assessment

No correction is required for the mathematics of the audited proof. The defensible conclusion is: **part (a) has an affirmative example by the displayed construction; part (b) is not answered; novelty is not established by this audit.** A public-facing conclusion should retain all three distinctions.
