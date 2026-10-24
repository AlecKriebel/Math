# Finite free-factor HNN extensions: sparse finite-action certificates

Recorded 2026-10-24. Alec Kriebel, ORCID <https://orcid.org/0009-0001-9320-500X>.

**Status.** The zero-virtual-second-Betti remainder is not solved. This approach produces an explicit mechanism valid for arbitrary associated-subgroup rank when a finite-action certificate exists, and constructs such certificates and unbounded connected covers for a concrete family. One member has zero second Betti number in every finite abelian cover but unbounded second Betti numbers in finite covers. The examples belong to the already understood cyclic-edge subclass, so these derivations do not establish a new case of Kourovka 21.139. No literature-wide novelty claim is made. Estimated completion toward the general free-factor-HNN detection goal: **15%**. The construction and verification subsystem below is complete.

## 1. Exact target and structural input

The conditional target supplied to this independent approach is:

> If a hyperbolic compact special group of rational cohomological dimension at most two has H_2(H;Q)=0 for every finite-index subgroup H, must it be free?

For this approach the reduction to a finitely generated free-by-Z group is treated as prior input, not reproved. The free kernel is allowed to have infinite rank.

The relevant precise primary reference is Marco Linton, *Embedding finitely generated free-by-cyclic groups in {finitely generated free}-by-cyclic groups*, [arXiv:2510.10178v2](https://arxiv.org/html/2510.10178v2), revised 22 April 2026; published as [IMRN 2026, rnag020](https://doi.org/10.1093/imrn/rnag020). The introduction and Theorem 4.1 support a finite-rank free-base HNN description in which both associated subgroups are free factors. Theorem 4.1 is formulated using minimal bi-invariant graph triples; its antecedents include injectivity of the displayed graph map. Its Euler-characteristic conclusion is chi(G)=rank(A)-rank(F). This is stronger than the one-sided free-factor formulation attributed there to Feighn–Handel. Corollary 1.5 supplies virtual compact specialness for hyperbolic free-by-cyclic groups. None of these statements supplies positive virtual H_2.

Write the resulting presentation abstractly as

    G = < F, t | t^-1 a_i t = w_i, 1<=i<=s >,
    F = A*C, A=<a_1,...,a_s>, B=<w_1,...,w_s>.

A and B are free factors, and the indicated map A->B is an isomorphism. The presentation complex is the aspherical graph of graphs for this HNN extension. Its finite covering complexes therefore compute group homology. A tree of copies of F glued along these free factors has free fundamental group; the increasing finite intervals can be enlarged by free products. This also directly shows the height kernel is free, without claiming it is finitely generated.

Both-free-factor status does not imply that the HNN group is free. Surface examples already rule out that shortcut. Completing the partial isomorphism to an automorphism of F and imposing its omitted stable-letter relations gives a quotient; it does not give an embedding of G in that mapping torus.

## 2. Cover and Fox conventions, checked directly

Permutation matrices use column vectors: P(p)e_j=e_{p(j)}. The algebraic matrices below describe a **left** representation rho. The actual cellular covering graph has **right generator actions rho(x)^-1**. If D_x is the evaluated Fox derivative of a relator with respect to x, its cellular boundary block is D_x^T under this convention.

This is checked by walking the relator from every face-sheet: a positive letter contributes its starting oriented edge; a negative letter first moves backwards along that generator and contributes minus that edge. The implementation checks equality between this direct edge-walk matrix and the transposed Fox matrix, as well as d_1 d_2=0. Consequently the claims are not based on exchanging the kernel of a matrix and the kernel of its transpose. All reported ranks use exact rational arithmetic.

## 3. A general sparse-certificate amplification lemma

**Proposition 1.** Let the finite free-base HNN presentation above be given. Suppose:

1. rho:F->Sym(Omega) is a finite transitive left permutation action killing A and B;
2. T_0 is any permutation of Omega, used for the left image of t;
3. the resulting second-boundary kernel contains a nonzero tuple v=(v_1,...,v_s), with each v_i in Q^Omega;
4. there is omega in Omega with v_i(omega)=0 for every i.

Then for every n>=1 there is a connected degree n|Omega| cover of G with b_2>=n. In particular vb_2(G)=infinity.

**Proof.** Since rho kills A and B, every choice of T satisfies the HNN relations. On n disjoint copies of Omega, retain the base action and retain T_0 except for

    T(omega,j) = (T_0(omega), j+1 mod n).

This is a permutation: the removed targets and new targets are exactly the same n points. The base action connects every copy internally, and the modified stable-letter edges connect all copies.

At this representation the stable-letter Fox blocks vanish because rho(a_i)=1. In the other blocks the dependence on T in the transposed boundary is exactly T v_i in the a_i component; all other terms are evaluated words in F. Changing T on the source omega does not change any T v_i because all those source coefficients are zero. The n disjointly supported copies of v therefore remain in ker d_2. They are linearly independent. Asphericity makes them independent group H_2 classes. QED.

This works for arbitrary s. It is an actual construction once the finite certificate is supplied. It does not assert that every nonfree HNN group has such a certificate. The hypotheses are substantially stronger than b_2>0: the base action must already be transitive after killing both associated free factors, and the homology tuple must have a common zero.

## 4. An explicit telescoping family

For p,k>=1 and epsilon in {+1,-1}, put q=kp+epsilon>=2 and

    w=(a b^k)^p b^epsilon,
    G_{p,k,epsilon}=<a,b,t | t^-1 a t=w>.

The word w is primitive in F(a,b): take the basis u=a b^k,b, then w=u^p b^epsilon is a basis element after Nielsen transformations. Thus both associated cyclic subgroups are free factors. Their abelianization vectors are (1,0) and (p,q), so no nonzero powers are conjugate. Each is maximal cyclic and malnormal in the free base, and neither meets a conjugate of the other nontrivially. [Kapovich, arXiv:math/9704203, Proposition 4.11](https://arxiv.org/abs/math/9704203) therefore gives hyperbolicity. These groups are torsion-free by their Bass–Serre action. The free height-kernel argument in section 1 and Linton's corollary give virtual compact specialness. They have a finite two-dimensional classifying space and chi=-1.

Let P rotate Omega=Z/q and take rho(a)=I, rho(b)=P. Then rho(w)=P^q=I, so the image T of t is unrestricted. Write J=I+P+...+P^{q-1}. For r=t^-1 a t w^-1, direct Fox calculation gives

    D_a = T^-1 - sum_{j=0}^{p-1} P^{jk},
    D_b = -J,
    D_t = 0.

These formulas also hold when epsilon=-1; the last inverse b cancels the end of the last b-run, leaving total exponent q.

Set

    x=e_0-e_{-k}.

Since gcd(k,q)=1, x is nonzero. The transposed boundary conditions are

    J x=0,
    T x=sum_{j=0}^{p-1} P^{-jk}x.

The second right-hand side telescopes to e_0-e_{-pk}. Since -pk=epsilon mod q, the two target points are distinct. Choose T fixing 0 and sending -k to -pk. It extends to a permutation, and x is a nonzero H_2 class. Equivalently one may choose T(i)=p i mod q, because gcd(p,q)=1. This latter choice yields a finite metacyclic monodromy quotient; a nonsolvable quotient is not necessary.

For q>=3, x has a zero coordinate. Proposition 1 applies and gives connected covers of degrees nq with b_2>=n for every n. There is also an explicit completion: in each block prescribe T(0)=0 and T(-k)=-pk, reserve one unused source and target for a cyclic link to the next block, and match all remaining unused slots internally. These are the permutations generated by the verification script.

All canonical cyclic height covers, of every degree, have b_2=0: there a=b=I and D_b=-qI is invertible. Thus a single selected tower cannot test the zero-virtual-b_2 hypothesis.

The q=2 boundary is important. The vector x then uses both sheets, so Proposition 1 has no unused source with which to connect copies. The group G_{1,1,+1}=<a,b,t | t^-1 a t=a b^2> is the closed nonorientable genus-three surface group (a commutator times a square). Its orientable double cover has b_2=1, and every finite cover has b_2<=1. No unbounded conclusion is asserted at q=2.

## 5. Every abelian cover can miss the homology

**Proposition 2.** In the family above, every finite abelian cover has b_2=0 if and only if

    gcd(q,k-1)=gcd(q,k+1)=1.

**Proof.** Over C a finite abelian covering module decomposes into finite-order one-dimensional characters. Let their values on a,b,t be A,B,T. A nonzero second-boundary kernel in a character summand requires all Fox derivatives to vanish. The stable-letter derivative T^-1(A-1) forces A=1. The relation then forces B^q=1.

If B=1, D_b=-q is nonzero. If B!=1, then D_b=0, and the remaining condition is

    T^-1 = S(B),
    S(B) = sum_{j=0}^{p-1}B^{jk}
         = (1-B^{-epsilon})/(1-B^k).

The denominator is nonzero because gcd(k,q)=1. Since |T|=1, we need |S(B)|=1. Comparing chord lengths on the unit circle gives

    B^k = B^{epsilon} or B^{-epsilon}.

Equivalently a nontrivial B has order dividing q and one of k-1,k+1. If such a B exists, S(B) is either 1 or -B^{-epsilon}, itself a root of unity. We may then choose the required finite-order T, producing a finite cyclic character with H_2!=0. If neither gcd exceeds one there is no such character. Character decomposition proves the assertion for all finite abelian covers, and scalar extension from Q to C preserves the second Betti number. QED.

The simplest worked example is

    E=G_{2,2,+1}=<a,b,t | t^-1 a t=a b^2 a b^3>.

Here q=5 and gcd(5,1)=gcd(5,3)=1. Consequently every finite abelian cover of E has zero rational H_2. Nevertheless E has connected degree-5n covers with b_2=n, as follows.

Use sheets (i,j) in Z/5 x Z/n. Define left matrices by

    P(i,j)=(i+1,j),
    T(0,j)=(0,j), T(1,j)=(1,j),
    T(2,j)=(3,j+1), T(3,j)=(4,j), T(4,j)=(2,j).

Again the actual right generator actions are a=I, b=P^-1, t=T^-1. The action is transitive: P connects each block and T connects consecutive blocks. Here

    d_2 has blocks T-I-P^-2, -J, 0.

The first block equation forces

    z_{0,j}=z_{2,j}=z_{3,j}=0,
    z_{4,j}=-z_{1,j}.

Conversely those vectors satisfy both blocks. Thus the full kernel has basis e_{1,j}-e_{4,j}, of dimension n. Since the cover's Euler characteristic is -5n, b_1=6n+1. In particular the first cover has degree 5, b_1=7, b_2=1. For n=1 one can write the left permutations b=(1 2 3 4 5), t=(3 4 5), and use their inverses as the right covering permutations.

This is a rigorous countercontrol to any strategy that replaces all finite covers by all finite abelian covers or by roots-of-unity Alexander tests. It is not a counterexample to 21.139.

### 5.1 Every finite p-group monodromy can also miss it

The parent researcher supplied the following additional diagnostic, independently checked here.

**Proposition 3.** For every prime l and every finite cover of E whose entire monodromy group is an l-group, b_2 over F_l and over Q are both zero. More generally the same assertion holds, for each prime separately, for an aspherical one-relator presentation whose exponent-sum vector is primitive.

**Proof.** The a-exponent sum of E's relator is -1. Its evaluated a-Fox block in F_l[P], for a finite l-group P, therefore has augmentation -1. The augmentation ideal of F_l[P] is nilpotent, so this block is a unit. For completeness, choose a central element z of order l. Modulo (z-1), induction on |P| makes the augmentation ideal nilpotent. Thus a sufficiently large power of the original ideal lies in (z-1); a further l-th power vanishes because (z-1)^l=0 and z is central. An element of nonzero augmentation is then inverted by a finite geometric series.

Consequently the a-block acts invertibly on every finite permutation module, including the cover module, and d_2 is injective over F_l. A full-rank minor modulo l is a nonzero integral minor, so d_2 is injective over Q as well. For a primitive exponent-sum vector, for each prime choose some coordinate nonzero modulo that prime and apply the same argument. QED.

The monodromy qualification is essential: degree being prime or a prime power does not make the monodromy a prime-power group. E's degree-five positive witness may instead use left permutations P(i)=i+1 and T(i)=2i modulo 5, generating C_5 semidirect C_4 of order 20. This is a solvable monodromy group, with b_2=1, and its inverse right action is a connected covering certificate. Thus neither all finite abelian covers nor all finite prime-power-group covers suffice to test the problem, and the prime-power argument does not extend to all finite solvable monodromy. No assertion is made about all mixed-prime nilpotent monodromy.

## 6. A higher-rank boundary case

Consider F=F(a,b,c), A=<a,b>, B=<bc,ca>, with a->bc and b->ca. Both A and B are free factors: (bc,ca,c) is a free basis. The quotient F/<<A,B>> is trivial. Therefore the base-transitive hypothesis of Proposition 1 can only have one sheet, where a nonzero tuple cannot have a common zero.

Yet this does not imply freeness or virtual H_2 vanishing. In the canonical cyclic height covers, the Fourier matrix from edge H_1 to vertex H_1 is

    [ z^-1   -1   ]
    [ -1     z^-1 ]
    [ -1     -1   ].

Its kernel is nonzero exactly at z=-1, with vector (1,-1). Hence the degree-two height cover has b_2=1; more generally height degree n gives b_2=1 for even n and 0 for odd n. This is a concrete reason not to assert that triviality of the quotient obtained by killing both associated factors forces freeness. It also shows that such killed-edge actions cannot be the only detection mechanism.

## 7. Exact remaining gap and route disposition

The general HNN route remains incomplete. The strongest proved general statement here is Proposition 1, conditional on a sparse finite-action certificate. We have not shown that an arbitrary nonfree hyperbolic HNN extension with free-factor associated subgroups admits such a certificate, or even any finite cover with nonzero H_2. For groups where F/<<A,B>> is trivial, this particular amplification mechanism has no nontrivial base-transitive action at all; the higher-rank example above needs a different certificate.

An assertion that every nonfree such HNN contains a nonfree cyclic-edge sub-HNN with the needed intersection properties would transfer the central difficulty to an unsupported subgroup-existence claim. That proposed universal reduction is therefore **blocked** unless a new construction proves those intersection and nonfreeness requirements. The unrestricted claim that all nonfree free-factor HNN groups have a finite H_2 witness is likewise not promoted as a lemma.

Possible productive next work is to search higher-rank Fox matrices for finite nonabelian actions with local kernel vectors, while retaining an independent route for trivial killed-edge quotients. The E example provides a mandatory benchmark: an implementation confined to abelian actions must fail on it. Outside input might be useful for a priority audit of these explicit certificate constructions, but no outreach has been prepared or initiated.

## 8. Artifacts and validation

All files are inside `source_20261024_hnn/`:

- `search_covers.py`: exact Fraction row reduction; transposed Fox boundary; independent direct right-action relator-edge walks; chain identity and connectivity checks.
- `cover_results.json`: all labeled transitive actions in degrees 1 through 4 for G_{2,1,+1}; first positive witness degree 3.
- `verify_telescoping.py` and `telescoping_results.json`: 24 parameter/copy cases, degrees up to 20, including epsilon=-1 and p=1 boundaries. Each contains explicit permutations, direct-edge-walk equality, n independent kernel certificates, and exact b_1,b_2.
- `verify_exact_e.py` and `exact_e_results.json`: the exact b_2=n family for E, plus the higher-rank two-sheet boundary certificate.
- `abelian_blind_results.json`: auxiliary enumeration of all 120 choices of T with b a 5-cycle and a=I for E; 35 have b_2=1 and 85 have b_2=0. Both left-representation matrices and their inverse right covering actions are explicitly recorded.
- `manifest.json`: primary source URLs, retrieval timestamp, hashes, and artifact checksums.

The independent adversarial subagent verified the dihedral boundary control, the telescoping identities, the gcd criterion including p=1 and q=2 boundaries, the exact E kernel, and the connected-copy amplification. A parent audit identified the importance of explicitly distinguishing left Fox representations from right cellular actions; direct edge-walk equality checks were then added and passed. No floating-point rank calculation enters any certificate.
