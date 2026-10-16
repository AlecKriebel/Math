# Candidate strengthening from homogenized braid signatures

This is a complete proposed proof, awaiting the final fresh adversarial and priority verdicts. It was developed during the PR938 priority audit and is counted as one additional substantive proof attempt. The immutable submitted proof and its observed1/5 accounting remain preserved; the known combined count is2/5. This document is a research artifact, not an accepted preprint or a historical-priority claim.

## Exact statement

Let P_m be the classical disk pure braid group, G^(0)=G and G^(k+1)=[G^(k),G^(k)]. Interpret braids as ordered smooth string links, and use Otto's ordinary integral smooth solvable filtration, defined by standard closures. For every m>=3 and every finite integer k>=1,

    P_m^(k) is not contained in F_1^m.

Consequently, for every m>=3 and integer n>=1,

    P_m^(n+2) is not contained in F_n^m.

The quantifiers are for each finite k there exists a braid; no single braid in the intersection of all derived terms is asserted. The result at all n is stronger than the submitted explicit n=1 witness. P_1 is trivial and P_2 is cyclic, so the m>=3 boundary is necessary.

## Group lemma

If a homogeneous real quasimorphism q on G is not a homomorphism, then q is nonzero on every finite positive derived term G^(k).

Suppose instead q vanishes identically on N=G^(k). It is normal. For g in G, n in N and positive integer r, write (gn)^r=g^r n_r with n_r in N. If D is the finite defect of q, homogeneity gives

    |r q(gn)-r q(g)| <= D,

since q(n_r)=0. Dividing by r and taking r to infinity proves q(gn)=q(g). Thus q descends to a well-defined homogeneous quasimorphism on G/N. This quotient is solvable and therefore amenable. Every homogeneous quasimorphism on an amenable group is a homomorphism, so q was a homomorphism on G, a contradiction.

The amenable-group fact is standard; see Calegari, *scl* (MSJ Memoirs20,2009), Proposition2.65, printed33; solvable amenability is recalled on printed27. One direct proof uses a left-invariant mean M: for a quasimorphism f define ell(g)=M_x(f(gx)-f(x)). The function of x is bounded, and left invariance yields ell(gt)=ell(g)+ell(t); also |ell(g)-f(g)|<=D(f). If f is homogeneous, applying this bound to powers forces ell=f. This uses an invariant mean only on a discrete amenable quotient, not amenability of the original braid group.

## A nonhomomorphic homogeneous quasimorphism on P_3

For a braid gamma in B_3 write s(gamma) for the ordinary signature of its standard oriented closure, with positive trefoil signature-2. Gambaudo–Ghys, *Braids and Signatures* (2005), TheoremA and Remark1, show that s is a quasimorphism on B_3. Their printed575 defines its homogenization

    q(gamma)=lim_(r->infinity) s(gamma^r)/r,

and establishes that q is a homogeneous quasimorphism. Their Remark3, printed545, gives s(sigma_1^ell)=1-ell for positive ell; adding a separate strand preserves signature. Put

    a=sigma_1^2, b=sigma_2^2,
    h=sigma_2 sigma_1^2 sigma_2^(-1),
    z=(sigma_1 sigma_2)^3=Delta_3^2.

All four are pure. Generator symmetry and conjugation of ordinary braid closures give q(a)=q(b)=q(h)=-2. The Artin relation proves z=a h b: after cancellation this product is sigma_1^2 sigma_2 sigma_1^2 sigma_2, and replacing its inner sigma_1 sigma_2 sigma_1 gives (sigma_1 sigma_2)^3.

For the three-strand specialization, Gambaudo–Ghys Lemma4.1, printed568–569, gives s(alpha Delta_3^4)=s(alpha)-8. Hence s(z^(2r))=-8r for every positive r, and q(z)=-4. A homomorphism on P_3 would instead give q(z)=q(a)+q(h)+q(b)=-6. Thus the restriction of q to P_3 is not a homomorphism. The group lemma now makes q nonzero on P_3^(k) for each finite k>=1.

All numerical values in this paragraph follow from published identities for every positive power; checking finitely many powers would not prove the limit or the group lemma. A simultaneous global signature-sign reversal preserves nonhomomorphism and the resulting obstruction.

## Transfer to solvability and to more strands

The separately reconstructed universal obstruction is: an algebraically split link admitting an integral smooth1-solution has ordinary signature0. For completeness, the solution's H1 isomorphism extends the all-meridian sign character. Signed integral cellular boundary matrices reduce mod2 to the ordinary ones, giving b2(W;Q_alpha)<=b2(W;F2)=rank H2(W;Z)=2r; integral UCT uses torsion-free H1. The2r framed solution surfaces have trivial restricted sign systems because both sets of surface groups lie in the commutator subgroup. Their local-coefficient fundamental cycles have hyperbolic pairings with off-diagonal units; they are independent and saturate the rank bound. Both ordinary and twisted signatures therefore vanish. Toffoli(1.1) and the one-colour surgery formula(4.21), with the zero framed linking matrix, identify the resulting zero rho defect with minus the ordinary signature at-1. Its pointwise domain has no Alexander-root exclusion. Full local-class, framing, radical and source checks are in the root/topology audit; no computed braid signature proves this universal lemma.

Fix k>=1 and choose v in P_3^(k) with q(v)!=0. By the definition of the limit, s(v^r) is nonzero for some positive integer r. The braid v^r remains in the same derived subgroup. Pairwise linking numbers are homomorphisms on pure braids and vanish on the first derived subgroup, so its closure is algebraically split. The signature obstruction proves v^r is outside F_1^3. In particular the argument never assumes q(v)!=0 implies s(v)!=0 for that exact representative; taking a power is essential.

Embed this braid in P_m by adding geometrically separate vertical strands. The embedding is a homomorphism, hence preserves derived membership, and its closure is a split union with unknots, which preserves signature. This proves the first statement for all m>=3. Finally F_n^m is contained in F_1^m for every integer n>=1, by the source's decreasing solvable filtration, proving the second statement. No signature homomorphism on the string-link concordance group and no new filtration model is used.

## Attribution and exact remaining verification

The homogenized signature, its values, amenable rigidity and1-solution obstruction are credited inputs. The connection to the source question is a newly assembled deduction in this audit; old ingredients alone do not establish that an earlier source already stated the complete answer. The classical priority family has also located a2025 published defect-restriction lemma that corroborates the group step; that broader theorem must receive credit in any promoted synthesis. No new general quasimorphism theorem or current-open/firstness claim is made here.

The original104-letter witness remains an independently certified explicit n=1 example in the supporting record. Its finite certificate is not a construction for every deeper derived term. Fresh adversarial verification of the complete stronger inference, a bounded primary priority audit, native attempt accounting, and sequential new whole-package reviews remain required before publication.
