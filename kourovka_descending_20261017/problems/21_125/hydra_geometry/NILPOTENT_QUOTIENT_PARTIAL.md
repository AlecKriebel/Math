# A certified finite quotient cover for rank5, and its explicit failure of specialness

**Author-verified partial result; fresh independent adversarial review pending.** No full or original resolution of Kourovka21.125 is claimed. The elementary finite Lie/group computations are preserved to make the route reproducible.

## Exact outcome

There is a finite quotient of the ordinary Hydra group G_5 for which the induced regular cover of the published canonical CAT(0) square complex has no hyperplane self-intersections. The quotient is realized inside a group of order101^195. The same cover **has inter-osculating hyperplanes and is not special**. Thus this is a concrete unsuccessful construction, not evidence of virtual specialness or its failure for G_5.

The cover degree is the order of the image of G_5, at most101^195. Surjectivity onto the full ambient finite group is unnecessary and is not assumed.

## 1. Finite associative algebra and exponential groups

Let N be the nonunital associative algebra over F_101 on two noncommuting variables x,y, truncated by all words of degree11. Thus N^11=0. For a in N set

    exp(a)=sum_(k=0)^10 a^k/k!,
    log(1+a)=sum_(k=1)^10 (-1)^(k+1) a^k/k.

The denominators are invertible in F_101. The finite polynomials exp and log are inverse bijections N<->1+N, by the usual formal one-variable identities truncated to degree10. The group1+N uses actual associative multiplication. Every unit has exponent dividing101, since (1+a)^101=1+a^101=1.

We use one established input: the finite-degree Baker–Campbell–Hausdorff identity says log(exp(a)exp(b)) is a Lie polynomial in a,b when all terms above degree10 are discarded, with denominators whose prime divisors are at most10. It is therefore valid in this characteristic. In particular, for any Lie subalgebra R of N, exp(R) is a group. For a Lie ideal I of R, exp(I) is a normal subgroup of exp(R): closure follows from BCH, and conjugation follows from the finite identity exp(a)exp(b)exp(-a)=exp(exp(ad(a))(b)). This is the standard class-less-than-characteristic exponential construction, also within Lazard's1954 correspondence; **the computation does not assume arbitrary subgroup/Lie-subalgebra correspondence**.

The computational certificate supplies explicit polynomial bases R,I,W with dimensions226,31,88 respectively. The verifier proves directly that R is Lie closed, I is an ideal of R, W is Lie closed, and I<=W<=R. Consequently

    Q=exp(R)/exp(I)

is a finite group of order101^(226-31)=101^195, and exp(W)/exp(I) is a subgroup. No group enumeration or floating-point arithmetic is involved.

## 2. Exact Hydra homomorphism and the separating certificate

Set s=exp(x), alpha_5=exp(y), and recursively set

    alpha_(i-1)=alpha_i^-1 s alpha_i  (i=5,4,3,2)

in1+N. The remaining relator is r=s^-1 alpha_1^-1 s alpha_1. Its logarithm belongs to I; the verifier reconstructs that logarithm from the actual unit multiplication and checks membership. Therefore the displayed assignment defines a homomorphism G_5->Q.

Every generator of the canonical hyperplane stabilizer

    L_5=<alpha_1, alpha_i s alpha_i^-1 (i=2,3,4,5)>

has logarithm in W, checked directly. Hence q(L_5) is contained in exp(W)/exp(I).

For each j=2,3,4,5, the certificate supplies a linear functional f_j on N that vanishes on W and satisfies f_j(log(alpha_j))=1 in F_101. Since I<=W, this proves q(alpha_j) is not in exp(W)/exp(I), and therefore not in q(L_5). Indeed, if exp(log(alpha_j)) exp(-w) belonged to exp(I) for some w in W, then alpha_j would belong to the group exp(W), giving log(alpha_j) in W, a contradiction.

The regular-cover filter proved in CANONICAL_COVER_MECHANISM.md now establishes the asserted absence of hyperplane self-intersections. This filter says nothing by itself about specialness.

The fixed certificate hash is

    SHA256 7bfdf7d30b708866c271499003af3844e24905e6995eb5ca728f72af49044b56

for rank5_lie_certificate.json. The finite-dimensional closure checks cover all potentially nonzero basis brackets:455 for R,46 for the ideal condition,117 for W. Brackets omitted by the degree test are identically zero because their minimum total degree exceeds10. Dual supports have sizes26,6,2,1. These numbers describe this certificate, not a general-rank theorem.

## 3. Actual group-word proof of q(s) in q(L_5)

A Lie-span observation alone is not used to infer group membership. Instead, rank5_s_membership_slp.json gives a192-node straight-line **group word**. Its initial units are exponentials of the L-generator logarithms and exponentials of ideal-basis vectors. All operations are multiplication and integer powers0..100 in1+N. A single final seed is s=exp(x).

The read-only verifier evaluates powers by repeated squaring in the associative ring, independently of the collector's exp/log power implementation. It proves the final unit is exactly1. It also checks the formal shape of the expression is

    h*s=1,

where h uses only L-generator seeds and exp(I) seeds. There is exactly one s seed, and every operation involving it is left multiplication by an h-expression. Thus no implicit equation solving or subgroup/Lie correspondence is needed. Modulo exp(I), all ideal seeds vanish, and the identity proves q(s) belongs to q(L_5).

The SLP hash is

    SHA256 d6f43db01906e8f3fd96acebec1ab55a8103712e2a2da010a8c0637e2640a6d4

The machine-readable verifier receipt confirms this hash.

## 4. Explicit inter-osculation

Here is a general geometric criterion that explains this failure. Let m>=3 and q:G_m->Q be a quotient with q(alpha_m) not in q(L_m), but q(s) in q(L_m). In the regular kernel cover, at the identity vertex consider the positive alpha_(m-2) and positive alpha_(m-1) germs. They never bound a square: every square corner containing two distinct positive labels includes s.

The hyperplanes of those germs are respectively

    H_1=q(alpha_(m-1))^-1 H,
    H_2=q(alpha_m)^-1 H.

The standard crossing pair from square m-1 is (H,q(alpha_m)^-1 H). Translate that pair by q(alpha_(m-1))^-1. The first member becomes H_1. The second equals H_2, because

    alpha_m alpha_(m-1)^-1 alpha_m^-1=s^-1

and q(s) stabilizes H. Thus H_1,H_2 cross somewhere, even though the displayed germs osculate at the identity. They are distinct: equality would give q(alpha_m^-1 s) in q(L_m), and q(s) in q(L_m) would force q(alpha_m) in q(L_m), contrary to the hypothesis.

For m=5 the germs are alpha_3+ and alpha_4+. The dual certificate supplies q(alpha_5) not in q(L_5), and the exact192-node group word supplies q(s) in q(L_5). Hence this cover inter-osculates and is not special. This is an explicit fatal obstruction to this particular finite quotient construction.

## 5. Reproduction and limits

Run in this directory using Python3 standard library:

    python3 verify_rank5_lie_certificate.py
    python3 verify_rank5_s_membership.py

The checks take seconds and read the fixed certificates. Rebuilding the Lie certificate is optional:

    python3 build_rank5_lie_certificate.py

Rebuilding the group SLP is also optional:

    python3 rank5_group_sifting.py

The latter is an exact ring-unit collection search; its correctness is not needed once the short final identity is verified.

Exploratory calculations on classes below10 explain why shallower quotient attempts fail: for rank5 alpha_2 remains in the computed Lie span through class9. Rank3 first separates all alpha_j at class3, rank4 at class6, rank5 at class10. The triangular pattern is **not proved for general rank** and is not used as evidence that any general construction works. Larger finite cases do not repair the need to remove inter-osculation. No claim of originality, full virtual specialness, or complete negative resolution follows.

Established input reference: Michel Lazard, *Sur les groupes nilpotents et les anneaux de Lie*, Ann. Sci. ENS(3)71(1954),101–190, DOI10.24033/asens.1021. The proof here uses only the standard finite-degree BCH closure and normal-ideal consequences explained above, not an unchecked special case from that paper.
