# New mechanism ledger (separate from immutable submission accounting)

- Original submission stays author 1/5.
- Classical priority review developed **one materially new positive mechanism**, first signalled to root before the initial ledger checkpoint below (the message carries its own transport time; not reconstructed here). This is a new deduction made during this review, not a claim that a prior publication states the deduction. Do not label the whole classical work “audit 0 positive turns.” Root decides program accounting and independently falsifies this mechanism before promotion.
- Status: internally proved below using checked classical sources plus the parent-accepted universal F1 signature obstruction; fresh independent review is still required. This ledger does not amend the submitted n=1 theorem or author a paper.

## A. Classical signature quasimorphism with explicit normalization

Write s(g)=signature of the standard oriented closure at -1, with positive trefoil -2. Gambaudo–Ghys (2005), Theorem A and Remark 1, printed pp.544–545, give a bounded defect on B3. Their printed p.575 defines q(g)=lim_{r->infinity}s(g^r)/r, states q is a homogeneous quasimorphism, and |q-s|<=6. In particular its restriction to P3 is one as well.

Let a=sigma1^2, b=sigma2^2, h=sigma2 sigma1^2 sigma2^-1, z=(sigma1 sigma2)^3=Delta3^2. They are pure: a,b have trivial permutation, h is a conjugate of a, z is a full twist. q is conjugacy invariant (proof in B below), so q(a)=q(b)=q(h)=-2. Indeed GG Remark 3, p.545 gives s(sigma1^ell)=1-ell for positive ell. Adding a separate third trivial strand gives a split unknot, which does not change the Seifert-form signature. Taking ell=2r gives q(a)=-2. sigma1 and sigma2 are conjugate in B3, giving q(b)=-2, and h is a conjugate of a.

The braid relation gives z=a h b exactly: sigma1² sigma2 sigma1² sigma2 = sigma1 (sigma1 sigma2 sigma1) sigma1 sigma2 = sigma1 (sigma2 sigma1 sigma2) sigma1 sigma2 = (sigma1 sigma2)^3. GG Lemma 4.1 at n=3, pp.568–569, gives s(alpha Delta3^4)=s(alpha)-8. Starting at identity, s(Delta3^(4r))=-8r, hence q(z²)=-8 and q(z)=-4 by homogeneity. Equivalently GG Proposition 5.2 at theta=1/2, n=3, ell=2 gives q(sigma1 sigma2)=-4/3, hence q(z)=-4.

If q|P3 were a homomorphism, z=a h b would imply -4=-6. Thus q|P3 is not a homomorphism. This is a check of the pure subgroup specifically, not an inference from global nonhomomorphism on B3.

## B. Normal descent and all finite derived terms

Let q:G->R be homogeneous with finite defect D. Its conjugacy invariance follows from |q(x g^r x^-1)-q(g^r)|<=2D and division by r. For any normal subgroup N on which q vanishes identically, and any g in G,n in N, write (gn)^r=g^r n_r with n_r in N (normality). Then

|r q(gn)-r q(g)| = |q(g^r n_r)-q(g^r)-q(n_r)| <= D.

Taking r to infinity gives q(gn)=q(g). Thus q descends *exactly* to a homogeneous quasimorphism on G/N, with no bounded-section or representative gap. It is homogeneous since (gN)^r=g^r N and has defect <=D by choosing lifts.

Calegari, scl (MSJ Memoirs 20, 2009), Proposition 2.65, printed p.33, states and proves that every homogeneous quasimorphism on an amenable group is a homomorphism. Printed p.27 lists solvable groups among amenable examples. A direct proof useful here is: for a left invariant mean m and bounded F_g(x)=q(gx)-q(x), define H(g)=m_x F_g(x). Left invariance and F_{gh}(x)=F_g(hx)+F_h(x) imply H(gh)=H(g)+H(h); the defect inequality gives |H(g)-q(g)|<=D. Homogeneity of both makes them equal by applying the bound to g^r and dividing by r. Solvability gives amenability through induction on derived length (abelian groups are amenable; extensions of amenable groups are amenable).

Set G=P3. Every ordinary D^k G is normal, and G/D^k G is solvable of derived length at most k. If q vanished on D^k G, exact descent and Proposition 2.65 would make q a homomorphism on G, contradicting A. Therefore for **each finite k>=1**, there is x_k in D^k P3 with q(x_k) nonzero. No claim says a single element belongs to the intersection of all derived terms, and no nonzero-on-a-group inheritance is assumed without proof.

## C. Pointwise obstruction and exact quantifiers

For such x_k, homogeneity gives q(x_k^r)=r q(x_k). Since |q-s|<=6 on B3, choose a positive integer r with r |q(x_k)|>6. Then s(x_k^r) is nonzero, and x_k^r stays in D^k P3. Every member of D^k P3 for k>=1 has zero pairwise linking numbers, since pairwise linking is a homomorphism. Each closure component of a pure braid is an unknot after deleting the others.

Use the parent-accepted lemma: an algebraically split integral smooth 1-solvable link has pointwise s=0 at -1. This is an imported topological premise here, whose original direct proof and primary formulas have already passed the mathematical gate. It follows x_k^r is outside F1^3. Equivalently, if D^k P3 were contained in F1^3 then every positive power of every member would have s=0, so q would vanish there, contradiction. The latter argument needs only containment and subgroup power closure, not signature additivity or any homomorphism on string links.

This gives the newly derived stronger conclusion D^k P3 not subset F1^3 for every finite k>=1. Taking k=n+2 and F_n^3 subset F1^3 yields, for every n>=1, D^(n+2) P3 not subset F_n^3. Split trivial strands preserve derived membership, signature, and zero linking, so this noncontainment extends to every m>=3. This conclusion is **not** silently substituted for the submitted n=1 theorem. It is new work in this review and remains subject to independent falsification. For m=1,2 all positive derived terms are trivial.

## D. Historical claim boundary

GG2005 supplies q and the values; Calegari2009 supplies the amenable quotient fact; the elementary normal-descent calculation is standard and appears in general quasimorphism literature. These old ingredients do not, merely by being combined now, prove an earlier author stated or knew the exact negative answer. The actual prior-publication search and pre-2017 solvability-to-pointwise-signature bridge remain separate audit questions. No firstness, exhaustive-absence, or current-openness assertion is made.

File checkpoint UTC: 2026-10-15T08:45:14.846564+00:00

## E. Independently completed pre-2017 solvability bridge

The topological premise in C can also be obtained entirely from primary pre-2017 ingredients, without importing Toffoli2022. This is part of the same mechanism, not a second positive turn.

1. Otto2014 Definition2.3, pp.2631–2632 gives a smooth integral 1-solution W with H1(M_L;Z)=Z^m and embedded framed L_i,D_i whose fundamental groups lie in pi1(W)'. Lift them to the abelian cover. Their group-ring intersection pairings are zero on L_i,L_j and unit dual on L_i,D_j after whisker adjustment: the actual embedded surfaces have only their single transverse dual intersection, so no other translate contributes. These are precisely the n=1 Lagrangian/dual data in Cha2010 §8, p.599. The rank equality 2r=b2(W) is Otto's basis condition. Cha's Remark8.1 explicitly removes dependence on spin and the self-intersection condition, so a spin mismatch creates no gap. H1(M_L) is 2-torsion free.
2. Cha2010 Theorem8.2(2), n=1,p=2,d=2, has a tower of height n-1=0: M0=M_L. For chi sending all meridians to -1, the theorem says lambda(M_L,chi)=0 in L0(Q(zeta2))=L0(Q). His Definition2.2, p.566, is [twisted intersection form] minus the image of the ordinary signature, with boundary normalization 1/r. Evaluating the signature under Q(zeta2)->C therefore gives twisted signature minus ordinary signature zero. This is exactly the Casson–Gordon convention in Cimasoni–Florens §6.4, p.1257. Since the actual H1 inclusion is an integral isomorphism, the order-two character extends over W itself and one can use boundary normalization r=1. No averaged knot signature from Cha's earlier §7 enters.
3. Cimasoni–Florens, Generalized Seifert surfaces and signatures of colored links, TransAMS360(2008),1223–1264, electronically published23October2007, Theorem6.7 p.1257: for surgery matrix Lambda=0 all three matrix correction terms vanish and sigma_CG(M_L,chi)=sigma_L(-1,...,-1), with one color per component. Its hypothesis is n_i coprime to q, satisfied by q=2,n_i=1. It has no Alexander-root exclusion.
4. Their Proposition2.5 p.1232 merges two colors with correction minus the linking number of the two sublinks. Repeating merges makes the ordinary one-colored Levine–Tristram signature sigma_L(-1) equal to the all-distinct-colored value when all pairwise linking numbers are zero. Hence s(L)=0 for every algebraically split integral 1-solvable L. Formula pixels and the entire relevant definition/theorem/proof text were inspected; Theorem6.7 proof continues pp.1258–1259, and Proposition2.5's proof was read.

Thus GG2005 + elementary normal descent + amenable-quasimorphism theory (available in Calegari2009) + Cha2010 + Cimasoni–Florens2007/2008 + Otto2014 give a complete checkable implication for the stronger noncontainment derived in C. This exhibits an elementary classical-corollary route now; it does not document that the corollary itself appeared before the present review.

## F. Additional explicit published inheritance theorem

Kawasaki–Kimura–Maruyama–Matsushita–Mimura, The space of nonextendable quasimorphisms, AGT25:2(2025),1169–1226, published16May2025, Lemma7.12 p.1207, gives the stronger equality D_G(f)=D_N(f|N) when G/N is solvable. Taking N=D^k(P3), it gives a second published route from q's nonhomomorphism on P3 to nonzero restriction on every D^k. The source's proof uses Lemma7.10 and the equality of homogeneous defect with the supremum of absolute commutator values, then iterates through the derived series. This theorem is post-question but pre-submission. It does not state a pure-braid solvable-filtration answer, and its inclusion here does not turn our newly assembled application into an earlier published complete answer.

## G. Root accounting update

At 2026-10-15T08:55:20.464187+00:00, root reported that its independent reconstruction was saved separately and that genuine unmodified queue.py CLI accounting in an isolated private selected-record slice records the newly strengthened candidate as **2/5**, with this mechanism **one additional positive turn**. This family did not run that CLI or inspect the new candidate. The original immutable package remains1/5. This is parent-reported accounting, not a claimed mutation of the global native state. Fresh independent falsification remains pending. The2025 Lemma7.12 attribution and now-derived-versus-earlier-published distinction above are retained.
