# Independent internal AI audit of the relative ends partial theorem

This AI-assisted manuscript and its independent internal AI audit are unrefereed. “Accepted” refers only to the stated internal partial-theorem assessment; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The full spectrum for g >= 2 remains unresolved by this work, and no novelty or global-openness claim is made.

The theorem hash below identifies the originally audited text. The distributed proof preserves that entire text with only the publication-status paragraph added; ACCEPTANCE.json also identifies the distributed edition.

## Decision and accepted scope

**ACCEPT AS A PARTIAL THEOREM.** The submitted deductions are mathematically sound. No correction to their conclusions, genus restrictions, or generator bounds is required. The explanatory additions below make several implicit steps explicit; they are not conditions that invalidate the original proof.

The exact target is Farb's Question 2.1, problem 11000008 / AMR-109-0008: the relative ends of finitely generated subgroups of the orientation-preserving mapping class group of a closed oriented genus-g surface. The audited theorem has SHA256 `1d413a42ca84931d6d44051bb5dd7a6f971804f201e6754d09250731a85b182c` and 19025 bytes.

The accepted claims are:

1. Zero relative ends occurs exactly for finite-index subgroups.
2. For g >= 2, an infinite-index subgroup H with vcd(H) <= 4g-7 has one relative end. Consequently any witness with at least two relative ends has vcd(H) in {4g-6,4g-5}.
3. In genus two, 0, 1, 2, and continuum many ends are realized by finitely generated subgroups. The two-ended witness needs at most ten generators; the continuum-ended witness needs at most eight.
4. The separate genus-zero and genus-one conclusions are correct: their spectra are respectively {0} and {0, continuum}, with finitely generated subgroups understood.

No full genus-g spectrum for g >= 2 has been established. The four genus-two realizations are not an exhaustive classification. The audit neither proves global openness nor claims novelty.

## Exact invariant and finite index arguments

Farb defines the invariant using the quotient of a proper connected cocompact geometric model by H; his subsequent observation about covers of moduli space is not a solution of the question. A finite-generator Cayley graph, with its unit-edge length metric, is itself an admissible model. Thus the submitted proof can choose that model directly. It need not assert a quasi-isometry theorem for arbitrary non-length metrics. See [Farb, Question 2.1, printed page 15](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf).

With right multiplication edges and the left G-action, the quotient vertices are left H-orbits Hg. Its graph metric agrees, on vertices, with the quotient word metric. It is connected and locally finite. A finite coset set gives a finite graph and no ends; an infinite coset set gives a locally finite infinite connected graph and therefore a ray. This proves the zero-ends assertion, including finite-index subgroups that are not normal.

For H <= K <= G and [G:K] finite, the inclusion of word-metric spaces K into G is H-equivariant and a quasi-isometry. For x,y in K,

    d(Hx,Hy) = inf over h in H of d(x,hy).

Applying the two word-metric inequalities before taking the infimum proves the corresponding inequalities on the quotient vertex sets. Writing G=KT with T finite makes the quotient map coarsely onto, since kt lies within uniformly bounded G-distance of k. Connected locally finite graph quasi-isometries preserve ends. This proves the candidate's Lemma 1 for the same subgroup H in both ambient groups. It does not assume normality of K or H, and it does not replace H by an intersection at this step.

The second finite-index operation is different. For H0 normal of finite index in H, H/H0 acts by graph automorphisms on H0\Cay(G), and the orbit graph is H\Cay(G). Finite sets lift to finite sets. For clarity, the inverse image of any connected downstairs component has at most |H/H0| components: lift paths from a chosen downstairs vertex, using one starting vertex in each finite fiber. Consequently an infinite downstairs component contains the image of an infinite upstairs component. If upstairs is one-ended there can be only one such downstairs component, and finite fibers ensure that downstairs remains infinite.

More generally, finite group orbits account exactly for the identification of ends. Exhaust by invariant finite sets. Ends with the same image have components related at each stage by a group element; finiteness supplies one element working along a cofinal subsequence, hence identifying the two ends. Lifting an escaping ray establishes surjectivity. Therefore continuum many ends remain continuum after a finite quotient. This is the only higher-cardinality subgroup-index transfer needed in the genus-one argument. An unrestricted claim that every finite-index change of H preserves its precise end count would be unjustified; the candidate does not make that claim.

For N normal in K the coset graph is the Cayley graph of K/N, up to redundant edges and loops. The two genus-two constructions use this fact only inside their finite-index ambient subgroup Gamma, and then apply the equivariant ambient-index argument. No ordinary end count of N is substituted.

## Finite support cohomology and the dimension bound

Coset inversion Hg -> g^{-1}H identifies the right Schreier graph with the graph on left cosets G/H using left multiplication generators, after inverting the symmetric generating set. The left permutation action on all functions on G/H is available even though arbitrary permutations from G need not preserve the chosen graph's edges.

If an infinite Schreier graph has two distinct ends, some finite vertex set separates two infinite components. The characteristic function f of one such component has finite edge boundary. For every generator s, sf-f has finite support. For products, the cocycle identity extends this to every group element. Thus b(g)=gf-f is a cocycle in the direct-sum module Z[G/H], not merely in the product of all copies of Z.

If H^1(G,Z[G/H]) vanishes, then b(g)=gm-m for a finitely supported m. The function f-m is invariant under a transitive permutation action, hence constant. Away from the finite support of m this would make f constant, contradicting its infinite support and infinite complement. The graph must therefore have one end. This implication is all that is required; no unproved equality between end cardinality and a cohomology dimension is used.

Now take a duality group K of dimension d and its actual right dualizing module D. The pertinent identity is

    H^1(K,M) = H_{d-1}(K,D tensor_Z M).

It holds for all left ZK-modules M in the definition of integral duality. In particular it applies to M=Z[K/L], whose underlying abelian group is free even when the coset set is infinite. There is no finite-rank coefficient assumption. The mapping class group input is virtual duality, not Poincare duality, so replacing D by Z would be an error. [Harer, Corollary 4.2, printed pages 176-177](https://imag.umontpellier.fr/~calaque/GdT-CGEMC-Harer.pdf) provides the integral duality and closed-surface dimension. [Ivanov and Ji, Theorem 1.1 and equation (3)](https://arxiv.org/pdf/0707.4322) explicitly confirms both the finite-index torsion-free hypotheses and the all-coefficients formulation.

For the right action (d0 tensor m)k=d0 k tensor k^{-1}m, the candidate's tensor-induction isomorphism is correct:

    d0 tensor gL  ->  d0 g tensor g^{-1},
    D tensor_Z Z[K/L]  ->  Res_L(D) tensor_ZL ZK.

Replacing g by gl, l in L, changes the image to d0 gl tensor l^{-1}g^{-1}, which equals the original balanced tensor. Right equivariance follows because the image of d0 k tensor k^{-1}gL is d0 g tensor g^{-1}k. The inverse sends a tensor u to a u tensor u^{-1}L. It respects (a l) tensor u = a tensor lu and composes to the identity in both directions. This checks the module sides and all inverses independently.

Homological Shapiro then yields H_{d-1}(L,Res_L D). A free left ZK-resolution of Z restricts to a free left ZL-resolution, and tensor associativity gives the stated identification of complexes. To prove the vanishing, replace that resolution with a projective ZL-resolution of length at most d-2, which exists by the integral cohomological dimension hypothesis. This kills the homology in degree d-1 for the actual right coefficient module, without requiring L or D to have any additional finiteness property. In particular, finite generation of H is not being used as a substitute for type FP or finite presentation.

A finite-index subgroup of a duality group has the same finite cohomological dimension. Hence cd(L)<=d-2 also ensures that L has infinite index. In the surface application, choose a torsion-free normal finite-index K in G_g and let L=H intersect K. Normality can be arranged by taking the finite-index core; torsion-freeness survives this operation. The dimension is d=4g-5, and cd_Z(L)=vcd(H). First obtain e(K,L)=1, then e(G_g,L)=1, and finally e(G_g,H)=1 using the finite orbit quotient. As a subgroup of K, L has cd(L)<=d. Integral dimensions and the contrapositive therefore leave precisely d-1 and d for a subgroup with at least two relative ends. All inequalities and the g=2 boundary case check correctly.

## The unit weight kernel argument

The elementary lemma does not depend on a BNS characterization. Let chi(y_i)=1 for a finite generating set with connected commuting graph. Put t=y_0, k_i=y_i t^{-1}, and alpha(x)=txt^{-1}. A commuting pair y_i,y_j yields

    alpha(k_j) = k_i^{-1} k_j alpha(k_i),
    alpha^{-1}(k_j) = alpha^{-1}(k_i) k_j k_i^{-1}.

Both identities are needed. Root a spanning tree at k_0=1. Induction along it puts both conjugates of every k_i in N=<k_i>. Thus tNt^{-1}=N, and P=<N,t> makes N normal. The quotient P/N is cyclic on tN; its map to Z sends tN to 1, so it is infinite cyclic and N=ker chi. There is no appeal to a kernel of F_2 -> Z, which would be infinitely generated for an epimorphism. The claimed nine-generator kernel is established directly.

For the ten pure braid swings on a convex pentagon, the five sides form a connected commuting cycle and every diagonal commutes with the disjoint opposite side displayed in the candidate. The independent exact-coordinate check finds exactly ten disjoint-chord edges, equal to the ten listed edges, and verifies connectivity. Inversion of a diagonal swing preserves commutation and changes its character value from -1 to +1. The full twist has one unit of pairwise winding for every unordered pair; relative to the swing basis its abelianization is the sum of the ten pair classes. Five positive and five negative weights therefore kill it. The character is onto Z because a side has value 1. The swing generation, abelianization, and disjoint-support commutation facts agree with [Koban, McCammond and Meier, Definition 2.4, Lemma 2.5 and Remark 2.6](https://web.math.ucsb.edu/~mccammon/papers/sigma-pure-braids.pdf).

## Sphere quotient and hyperelliptic lift

The normalization map on ordered configurations is a genuine homeomorphism:

    (z1,...,z5) -> (z1, z2-z1, (z3-z1)/(z2-z1), ..., (z5-z1)/(z2-z1)).

Its inverse reconstructs each z_i from the translation, nonzero scale, and normalized points. The last three points avoid 0,1 and each other. Rotating the nonzero scale through a full turn gives the central full twist, with either global orientation convention generating the same central cyclic subgroup. The remaining factor parametrizes six ordered sphere points modulo Mobius transformations with three of them at 0,1,infinity. Its Teichmuller cover is contractible and the pure mapping class action is free: an automorphism fixing three distinct marked points on a sphere is the identity. Consequently its fundamental group is PMod(S_0,6), and the exact quotient is P_5/<z>. This avoids confusing the pure group with the full sphere group or leaving a boundary twist unaccounted for.

The genus-two hyperelliptic double cover has six branch points; each has ramification index two upstairs, and the total Euler characteristic is -2. Thus Winarski's finite-cover, negative-Euler-characteristic, and no-unramified-preimage hypotheses all hold. The branch points are marked downstairs, while their preimages are not extra marked points upstairs. Her theorem gives the Birman-Hilden property. The further identifications SMod(S_2)=Mod(S_2) and LMod(S_0,6)=Mod(S_0,6) use genus-two symmetric twist generators and lifts of sphere half twists. These are exactly the distinctions made in [Winarski, Theorem 1.1 and section 4.2](https://arxiv.org/pdf/1309.3650) and [Margalit and Winarski, introduction and section 4](https://arxiv.org/pdf/1703.03448).

The resulting surjection Theta:G_2 -> Mod(S_0,6) has kernel <iota> of order two. The preimage Gamma of the pure group has index 6!=720, since permutations of the six points are all realized by orientation-preserving sphere mapping classes.

The descended character on Q=PMod(S_0,6) has kernel generated by at most nine images of the braid-kernel generators. Its preimage H_2 in Gamma is generated by lifts of those nine and iota: after matching the image of any element by a word in the lifts, the residual element lies in the finite kernel. Gamma/H_2 is exactly Z, so e(G_2,H_2)=2. The proof requires normality only in Gamma. Neither normality in G_2 nor invariance of the character under all six-point permutations is asserted.

## Continuum witness and low genus

Forgetting two marked points Q -> PMod(S_0,4) has quotient F_2. The successive kernels have ranks four and three, because a sphere with five, respectively four, points removed has those free fundamental groups. Thus the combined kernel is an extension of F_3 by F_4 and has at most seven generators; its hyperelliptic preimage has at most eight.

The same conclusion can be checked directly in normalized configurations. Projection Conf_3(C minus {0,1}) -> C minus {0,1}, keeping one normalized moving point, has fiber Conf_2(C minus {0,1,x}). Its base has zero pi_2, so the fundamental group of the fiber injects as the kernel and the quotient is F_2. Projecting that two-point configuration onto its first point has base group F_3 and fiber group F_4, again with vanishing pi_2 of the base. These are within the dimension-two, connected-manifold and n>1 hypotheses of [Fadell and Neuwirth, Theorem 1, printed pages 111-112](https://doi.org/10.7146/math.scand.a-10517). The forgetful exact sequences also match Harer's ordered-point convention and sequence S1 on printed page 144.

A nonabelian finite-rank free group's Cayley tree has a Cantor end space, of cardinality continuum. Applying the normal quotient lemma inside Gamma and ambient finite-index passage gives exactly that relative-end cardinality for H_infty in G_2. The witnesses H=G_2 and H={1} supply 0 and 1.

In genus zero the orientation-preserving mapping class group is trivial. In genus one it is SL(2,Z), and the standard quotient by its center is C_2*C_3. This latter presentation can also be checked directly: the transformations S(x)=-1/x and R(x)=-1/(x+1) have orders two and three in PSL(2,Z). S sends negative reals to positive reals; each of R and R^2 sends positive reals to negative reals. The free-product ping-pong lemma therefore supplies C_2*C_3, and the Euclidean algorithm supplies generation since T(x)=x+1=S^{-1}R. The kernel of the map of this free product onto C_2 x C_3 has index six and acts freely on its tree. The quotient graph has six edges and five vertices, so its rank is two. Lifting its free basis splits the central C_2 extension. Taking the normal core of a free direct factor gives a normal finite-index nonabelian free group F inside SL(2,Z).

If H is finitely generated and infinite index, L=H intersect F is finitely generated, normal of finite index in H, and infinite index in F. Its rose covering has a finite core, since finitely many generating loops carry the entire fundamental group. After removing a finite connected enlargement of that core, the remaining components are attached trees. A finite core cannot account for the infinite covering, and beyond an attachment every vertex has forward degree 2 rank(F)-1 >= 3. Such a tree has continuum many rays and ends. A countable locally finite graph has at most continuum many rays, so the exact count is continuum. Ambient passage and the finite orbit quotient preserve this cardinality, as established earlier. Finite generation is important here; dropping it would invalidate the finite-core argument.

## Corrections and acceptance limits

No blocking mathematical correction was found. The following clarifications are supplied in this audit without editing the candidate:

- Choose the Cayley graph directly as the geometric model, avoiding unnecessary claims about arbitrary connected metrics.
- In the finite quotient argument, use path lifting and the finite fiber to justify that an infinite component downstairs receives an infinite component upstairs.
- State explicitly that the induced module can have infinite rank, the dualizing module is retained, and no FP hypothesis on L is used.
- Use pairwise winding to make the full-twist abelianization calculation explicit.
- When using the configuration fibration on fundamental groups, mention the vanishing pi_2 of the punctured-plane base.

The low-genus modular-group identifications are standard background rather than a novel classification. The main accepted result remains partial. No restriction of arbitrary relative ends to the ordinary finitely generated group list 0/1/2/infinity is used. Other genus-two values and the higher-genus high-dimensional cases are not decided. This audit does not establish current literature exhaustiveness or mathematical novelty.
