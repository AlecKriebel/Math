# Arithmetic K pi 1 prior resolution audit

Problem 30000779, OWR-1586-003. Audit date: 8 October 2026.

## Finding and scope

The conjecture actually stated in Alexander Schmidt's Oberwolfach report is covered by prior work: Schmidt's marked-curve theorem covers odd primes, and its proof, with the mild pro-2 criterion of Labute and Mináč, covers the remaining source case of the prime 2 over totally imaginary number fields. The cyclotomic and class-number restrictions are unnecessary. The auxiliary primes can still be chosen inside an arbitrarily prescribed set of Dirichlet density one and away from the primes above p.

This is an audit of existing proofs and their application, not a new solution or a new proof-search attempt. It uses zero new substantive problem-solving turns. It does not settle or classify the broader p=2 real-number-field formulation produced by omitting the original report's real-place convention. That omission must be repaired before this finding is used to dispose of a literal catalogue statement. No residual open case is asserted.

The controlling English and German Schmidt proofs contain local indexing mistakes, including the local products in the duality proof and the cyclic-field subscripts in the roots-of-unity construction. The necessary corrections and auxiliary-size choices are made explicit below. Thus the conclusion is not based on treating every printed formula as correct. The corrections follow from the same source's stated cohomology and inertia calculations; they do not introduce a new arithmetic construction.

The proof is accepted relative to the standard imported results identified in the dependency ledger: arithmetic duality, class field theory, Chebotarev, the homotopy/cohomology characterization of K(pi,1), and the published mild-group algebra. This audit checks their interfaces and reads the controlling arguments, rather than claiming to reprove all of those foundations.

## Exact source statement

The source is Schmidt, “Rings of integers of type K(pi,1),” in Oberwolfach Report 30/2007, printed pp.1756–1758. The report's opening convention is that p is odd or k is totally imaginary. Its Theorem 1 imposes both mu_p not contained in k and p not dividing the ideal class number, and the following sentence conjectures removal of those two conditions.

Use D for the report's density-one set, to avoid confusing it with a marking set. The exact conjecture after removing the two restrictions is:

- k is a number field.
- p is a prime, with p odd or k totally imaginary.
- S is any finite set of nonarchimedean primes of k, with S intersect S_p empty.
- D is any set of nonarchimedean primes of Dirichlet density one.
- There is a finite D_1 contained in D such that Spec(O_k) minus (S union D_1) is a K(pi,1) for p.

The argument below gives the stronger choice D_1 disjoint from S union S_p. In particular, the final open arithmetic curve remains in the tame situation. No assumption that S is contained in D is required. S can be empty. The report's subsequent discussion of norm-congruent primes is not an additional hypothesis of its Theorem 1; it occurs after the conjecture.

The report uses the vanishing of higher homotopy groups of the p-completed étale homotopy type. Schmidt's marked-curve theorem uses cohomological comparison. With empty marking these are the same K(pi,1) property, by Proposition 2.1 of Schmidt's 2007 “Rings of integers” paper, pp.4–5 of the author/arXiv version. The regular connected scheme in the application is Spec(O_k) minus a finite set, so the stated scheme hypotheses hold.

Source: https://ems.press/content/serial-article-files/46117

## Controlling prior results and their status

1. Alexander Schmidt, “Über Pro-p-Fundamentalgruppen markierter arithmetischer Kurven,” Journal für die reine und angewandte Mathematik 640 (2010), 203–235. The author English translation is “On pro-p fundamental groups of marked arithmetic curves,” dated 16 January 2009, arXiv:0806.1863v2. The arXiv record labels it the final version and identifies it as an English translation of arXiv:0806.0772. The English author PDF and German v2 were inspected.

   https://www.mathi.uni-heidelberg.de/~schmidt/papers/marked.pdf
   https://arxiv.org/abs/0806.1863v2
   https://arxiv.org/abs/0806.0772v2

2. John Labute and Ján Mináč, “Mild pro-2-groups and 2-extensions with restricted ramification,” Journal of Algebra 332 (2011), 136–158, DOI 10.1016/j.jalgebra.2011.01.019. The inspected manuscript title includes “of Q.” The author research page confirms the journal citation: https://www.math.mcgill.ca/labute/research.html . The author PDF is dated 13 October 2009; arXiv:0903.4383v2 was submitted 14 October 2009. Its introduction explicitly identifies its Theorem 1.1 as the missing ingredient for Schmidt's theorem at p=2 over totally imaginary number fields. The mathematical criterion and its proof, not just that sentence, are used here.

   https://www.math.mcgill.ca/labute/papers/Galram2.pdf
   https://arxiv.org/abs/0903.4383v2
   https://doi.org/10.1016/j.jalgebra.2011.01.019

The fresh author-PDF downloads of the OWR report, Schmidt translation, and Labute–Mináč paper match the earlier downloaded bytes exactly. The Labute–Mináč arXiv PDF has different bytes and font/text extraction behavior; it is tracked separately, not falsely reported as an identical file. The inspected theorem statements and controlling proof agree. This audit does not claim that either author manuscript was byte-compared to the publisher's typeset article.

## Exact theorem application for odd p

Schmidt's Theorem 1.1 takes a global field k, an odd prime p different from char(k), and pairwise disjoint sets S, T, M of nonarchimedean places, with S and T finite and M of Dirichlet density zero. Here T is the marking set: the maximal pro-p extension is unramified away from the subscript set and completely split at T.

It supplies a finite set A disjoint from S union T union M for which:

- G_{S union A}^T(k)(p) has cohomological dimension exactly 2 and its degree-one cup product surjects onto H^2.
- The extension realizes k_v(p) at every v in S union A.
- The decomposition groups belonging to S form the stated free pro-p product over the primes above S in k_A^{S union T}(p).
- Group cohomology agrees with marked étale cohomology in every degree for every discrete p-primary torsion module for that pro-p group.

For the OWR application set T empty and set

    M = ((all finite primes of k minus D) union S_p) minus S.

This M has density zero: the complement of D has density zero, S_p is finite, and deleting the finite set S does not change density. It is disjoint from S. Since S is tame, all of S_p remains excluded. Every prime of A, being outside both S and M, belongs to D and does not divide p. Thus D_1=A satisfies the report's conclusion. Empty marking is literally the ordinary étale site, not a further comparison theorem or a relaxation of the requested splitting conditions.

All number fields have characteristic zero, so the characteristic restriction is automatic. Neither the theorem nor this substitution imposes a class-number condition or excludes roots of unity. The assertion quantifies over every such k, p, S, and D before choosing A. It gives no uniform bound on the number or norm of the added primes, and none is claimed here.

## Cohomological preparation in the controlling proof

The complete route to Theorem 1.1 runs through Schmidt §§2–7. The later enlargement and duality-group results in §§8–9 are not needed for the OWR conclusion.

Write delta=1 if mu_p is contained in k, and delta_v=1 if mu_p is contained in k_v. For disjoint finite sets B and T the Kummer obstruction group is

    V_B^T = {a in k*/k*^p : a is a pth power at B,
             and has valuation divisible by p outside T}.

Schmidt's Lemma 3.5 identifies V_empty^T as an extension of the p-torsion T-class group by T-units modulo p. It is finite-dimensional. Adding a prime to B imposes another local pth-power condition. In particular, enlarging B can only shrink V_B^T. No class-number restriction has been assumed at this point.

Theorem 3.6, obtained using local duality, Artin–Verdier duality and the global generator formula, gives finite cohomology. In the tame situation with B nonempty and every v in B of norm 1 modulo p, the formulas needed below reduce to

    h^1(X minus B,T) = 1 + |B| - delta + dim V_B^T - r - |T|,
    h^2(X minus B,T) = |B| - delta + dim V_B^T,
    h^i(X minus B,T) = 0 for i >= 3,

where r=r_1+r_2. These formulas are valid for odd p, or at p=2 when k is totally imaginary. At finite extensions in the towers used later, the same real-place condition persists.

The duality statement Theorem 4.1 identifies the kernel of localization from H^2(X minus B,T) to the sum of local H^2(k_v), v in B, with the dual of V_B^T. Its proof chooses a finite auxiliary set containing the p-adic places, applies Poitou–Tate in the resulting invertible-coefficient situation, and compares the local conditions by excision. Consequently, when V_B^T=0, localization is injective. It is an isomorphism onto all local factors if delta=0; if delta=1, omitting any one factor makes it an isomorphism. This omitted factor is important in the roots-of-unity construction below. In the proof of Theorem 4.1, the first local product in each of its sequences (I) and (II) must be indexed by T, not S. The quotient diagram immediately above (I) already has T: the S factors have been divided out, the T factors remain in full, and the other factors are modulo unramified classes. Excision gives exactly the same local conditions. Both printed versions have this index slip; the corrected sequences prove the asserted duality without changing its hypotheses. Precise page locations and the corrected cokernel are recorded in the companion dependency ledger. At p-adic local factors the Kummer condition is explicitly the image of local units, dual to the unramified F_p-character subgroup by local reciprocity; it is not identified with ordinary Galois-unramified mu_p-cohomology.

Proposition 4.4 kills V_B^T by finitely many primes of norm 1 modulo p outside an arbitrary density-zero exceptional set. The input V_empty^T is finite-dimensional. The local-power map over all eligible primes is injective by the Kummer Hasse principle. In the relevant prime-exponent case there is no Grunwald–Wang special-case exception: that exception requires a 2-power exponent at least 8, whereas the module here is mu_p. Finite-dimensionality reduces injectivity to a finite subset of eligible primes.

Lemma 2.2 compares the universal pro-p cover with group cohomology. It gives an H^2 injection before asphericity is known. Vanishing on the universal pro-p cover is equivalent to comparison in all degrees and for all discrete p-primary modules. Corollary 3.7 then says, when the ramification set is nonempty, that surjectivity of H^2 comparison together with cd <= 2 is sufficient. The proof does not assume that the K(pi,1) property is already known merely from a cohomological-dimension bound.

## How the two arithmetic restrictions are removed

The new feature is temporary marking. Begin with a finite marking set T and a density-zero exclusion set M. Auxiliary markings T_0 can be chosen to remove the relevant class-group obstruction. Their later removal is proved to preserve the K(pi,1) property; they are not left as extra splitting requirements in the final OWR answer.

For precise bookkeeping, enlarge the marking set first and replace M by M minus the enlarged marking set whenever necessary. This does not loosen any final constraint: the new ramification primes are required to avoid the marking set anyway. Auxiliary markings may belong to the original M; no prime in M is thereby made a permitted new ramification prime.

The construction establishes Schmidt's Theorem 6.1: a nonempty finite tame ramification set A, disjoint from the prescribed markings and M, such that the marked curve is K(pi,1), every prime of A actually ramifies, V_A^{T union T_0}=0, and its cup product is onto. The two cases delta=0 and delta=1 require different independence arguments.

### The case without pth roots of unity

Choose auxiliary markings so that the T-class group has no p-torsion. Finitely many ideal classes have generators represented by primes, so this is possible without any hypothesis on the original class number. Choose a finite tame set P={p_1,...,p_m} such that V_{P minus {v}}^T=0 for every v in P. Two disjoint applications of Proposition 4.4 achieve the deletion property. Enlarge P further, if necessary, so that

    dim H^1(X minus P,T) = m+1-r-|T| >= 2.

The deletion property persists under this enlargement. This harmless size choice must be explicit: otherwise the source's later requirement of a Frobenius outside a given inertia line could have no solution. It also ensures nonemptiness.

For each p_i choose its valuation class s_i. Valuations make the s_i independent modulo T-units. Over L=k(mu_p), their Kummer extension and the T-unit Kummer extension have cyclotomic character, whereas the marked elementary abelian p-extension has trivial character. Since delta=0 and [L:k] divides p-1, these character spaces are distinct and the extensions are linearly disjoint. This is Lemma 6.4; it is the place where the old proof's cyclotomic restriction used to be essential, not a condition imposed on the other case.

Chebotarev now supplies q_a with prescribed nonzero valuation-Kummer behavior at s_a, trivial behavior at the other s_b, splitting in the T-unit field, and Frobenius outside the p_a-inertia line in the old marked elementary extension. It can also impose splitting in the fields introduced at earlier stages. The construction avoids M and every finite set of previously used primes. For the number-field application, take primes of L of absolute residue degree one; their complement has density zero. Then q_a splits in L and has norm 1 modulo p. This makes explicit a residue-degree step suppressed in the English text and present in the German construction.

Lemma 5.2 gives a cyclic degree-p character eta_a ramified at q_a and unramified elsewhere outside the markings. Set V=span(eta_1,...,eta_m) and U=H^1(X minus P,T). Independent inertia at the new primes gives H^1=U direct-sum V. The imposed splitting and local cup-product calculation yield V cup V=0. Here self-cups vanish because p is odd.

For every a choose chi_a in U which is nonzero on p_a-inertia and zero on Frob(q_a). The Frobenius is outside that inertia line, so such a character exists. Choose psi_a in U nonzero on Frob(q_a). Localization identifies H^2 with the 2m coordinates at the p_i and q_i. The classes chi_a cup eta_a have a nonzero diagonal in the p_i block and zero q_i block. The classes psi_a cup eta_a have a nonzero diagonal in the q_i block. The resulting block triangular matrix is invertible. Hence U cup V surjects onto H^2.

The English PDF p.15 and German PDF p.16 print Frob(p_a) in the condition on psi_a. The q_a coordinate of the asserted matrix requires Frob(q_a). The correction above is guaranteed by the preceding Frobenius choice. At a ramified p_a a Frobenius lift is not even canonical for an arbitrary character in U. This is a genuine indexing correction, not an assumption to hide.

### The case containing pth roots of unity

Enlarge the temporary marking set T so that it contains S_p and V_T^empty=0. Choose it large enough that n=|T|+r >= 3. Proposition 4.4 and subsequent finite enlargement give this, regardless of the class number. Here k is totally imaginary, automatically for odd p and by hypothesis when p=2.

Lemma 6.5 yields p-torsion-free Cl_T(k) and

    L = k_T^el = k(pth roots of all T-units),
    dim Gal(L/k) = n.

For every nonzero vector g of Gal(L/k), choose one eligible prime p_g with Frobenius g. Denote the resulting set by P={p_0,...,p_m}, so m+1=p^n-1. Then V_P^T=0 and the elementary marked group E=Gal(k_P^{T,el}/k) has dimension m+1-n. Removing any one prime leaves the Frobenius vectors spanning Gal(L/k), so each prime of P has nonzero inertia in E.

For each a=1,...,m choose an index set I_a, disjoint from {0,a}, of size n-1 such that adjoining Frob(p_0), or instead Frob(p_a), to {Frob(p_i):i in I_a} gives a basis of Gal(L/k). This exists by elementary linear algebra: for independent Frob(p_0),Frob(p_a), use their sum and complete a basis; for dependent vectors, use a complement. The construction of P contains every required nonzero vector.

Define

    R_a = {p_0,p_a} union {p_i : i in I_a},
    F_a = k_{R_a}^{T,el}.

The source's inertia calculation proves that F_a/k is cyclic of order p and ramifies at both p_0 and p_a. More explicitly, the inertia groups with indices outside {0,a} union I_a form an independent set of m-n elements in E, and either adding the inertia at p_0 or at p_a gives a basis. Their fixed field is F_a, whose degree is p. Equivalently, |R_a|=n+1 and the Frobenius vectors at R_a have rank n, so the cohomology formula gives h^1(X minus R_a,T)=1; deleting p_0 or p_a leaves a basis and makes h^1 zero.

The English pp.18–19 and German pp.18–19 instead omit I_a in three linked places: the cyclic-field assertion, the field defining the Frobenius kernel in condition (C_a), and the H^1 space from which chi_a is selected. The general dimension identity h^1(X minus R,T)=|R|-rank(Frob_R) shows that the literal two-prime field is trivial for an independent pair. Such pairs occur here, so the printed assertion cannot be used literally. The same omission occurs in the selection of chi_a and the relevant Frobenius kernel. Replace all three occurrences consistently by F_a or R_a as above. The source itself only claims chi_a unramified outside {0,a} union I_a, which confirms the required index set.

Lemma 6.5 provides the linear disjointness needed to choose q_a such that it splits in L, splits in the pth-root fields for indices in I_a, is nontrivial in the pth-root field for s_a, and has a nonzero Frobenius in Gal(k_P^{T,el}/F_a). This last vector space has dimension m-n=p^n-2-n, which is positive with our choice n>=3. Thus the nonzero condition is possible at p=2 as well. The q_a can further split in each earlier k_{q_b}^{T,el}; those fields are independent of the old composite because each has its own newly ramified prime q_b.

Let eta_a be the degree-p character from q_a, chi_a a nonzero character of F_a, and psi_a any character of E nonzero on Frob(q_a). In particular psi_a can and should be chosen in the old space U=H^1(X minus P,T), although the source prints the larger ambient H^1 space. Let V be the span of the eta_a. As before H^1=U direct-sum V.

Localization now omits the p_0 factor, as required by delta=1. Its remaining 2m factors are p_1,...,p_m,q_1,...,q_m. For chi_a cup eta_a:

- The p_a coordinate is nonzero.
- At indices in I_a, eta_a has trivial local unramified character because q_a splits the corresponding Kummer field.
- At the other p_i outside R_a, chi_a is unramified.
- At q_a the product is zero because Frob(q_a) lies in ker(chi_a).
- At q_b with b different from a, both characters are unramified.

Thus the first block is again diagonal. The psi_a cup eta_a classes give a diagonal nonzero q-block, with unrestricted old-prime coordinates. The same invertible block matrix proves U cup V onto H^2. This works over F_2; it does not require a sign distinction.

## The prime 2 interface

For p=2 one always has delta=1. The preceding roots-of-unity branch is therefore the only branch required. All of Schmidt §§3–5 and Proposition 7.1 already have the standing hypothesis p odd or k totally imaginary, rather than p odd alone.

One must separately check V cup V=0; graded commutativity does not imply zero self-cups in characteristic 2. The check is as follows.

Each q_a splits in L=k(square roots of T-units). Since -1 is a T-unit, L contains k(i); hence -1 is a square in k_{q_a}. Also q_a does not lie above 2. The local degree-one cup pairing over k_{q_a} is alternating. For example, using the tame local presentation and the cup/relator coefficient formula, the inertia power in its relator has exponent N(q_a)-1 divisible by 4, so no generator-square coefficient remains in degree two. Therefore eta_a cup eta_a vanishes at q_a. At every other prime of the final ramification set, eta_a is unramified, and the unramified local group is procyclic of cohomological dimension 1, so its self-cup vanishes there too. Injective H^2 localization gives global eta_a cup eta_a=0.

For b<a, the construction requires q_a to split in K_b=k_{ {q_b} }^{T,el}. Hence eta_b restricts to zero at q_a, killing the q_a coordinate of eta_a cup eta_b. For the opposite direction, q_a also splits in L. Lemma 5.2 gives L K_b=L(root_p s_{q_b}), so q_a splits in that compositum. The same lemma, now applied to q=q_a and its test prime q_b, says that q_b splits in K_a=k_{ {q_a} }^{T,el}. Thus eta_a restricts to zero at q_b, killing the q_b coordinate. The lemma applies because both primes are outside T union S_p, are distinct, and have norm 1 modulo p, and Cl_T(k)(p)=0. At every remaining ramification prime both characters are unramified, so the local cup is zero. This verifies both directions; a one-sided successive-splitting assertion alone would not suffice. Injective localization now gives eta_a cup eta_b=0. Together with the diagonal calculation, V cup V=0 in full.

Labute–Mináč Theorem 1.1 applies to a finitely generated pro-p group with H^2 nonzero and a decomposition H^1=U_LM direct-sum V_LM such that U_LM cup U_LM=0 and U_LM cup V_LM surjects onto H^2. In the present construction take U_LM=V and V_LM=U. The order reversal makes no difference to surjectivity. The group is finitely generated because H^1 is finite-dimensional; it is finitely presented because H^2 injects into finite-dimensional étale H^2. Here H^2 has dimension 2m>0.

Theorem 1.1 makes this group mild, and Labute–Mináč Theorem 5.3(c) gives cd=2. The rest of the arithmetic argument is unchanged after these explicit checks. The claim for p=2 therefore uses an inspected theorem and verified inputs, not an extrapolation from odd primes or from a result about Q.

In particular, Labute–Mináč's separate theorem about extensions of Q unramified at infinity is not used to infer a K(pi,1) result for schemes over real number fields. The scheme's étale fundamental group and an extension required to remain unramified at real places need not coincide at p=2. The original OWR convention avoids precisely that issue.

## Mild group proof audit

For odd p the cup criterion is Schmidt 2007 Theorem 5.5, restated as Theorem 6.2 of the marked-curve paper. Its proof writes a minimal presentation, reads the quadratic relator coefficients from cup products, reduces the free F_p[pi]-Lie algebra modulo pi, and applies the strongly-free-sequence criterion. Surjectivity of the cross-cup map is exactly linear independence of the relator images in the cross-bracket space. The isotropic summand eliminates its internal brackets. Labute's reduction theorem lifts strong freeness back to F_p[pi], and his relation-module theorem gives cd=2.

At p=2 ordinary Lie brackets are not enough. Labute–Mináč §§2–4 retain the square operator in a mixed Lie algebra and pass to its reduced quadratic Lie algebra. Their Theorem 2.3 supplies the free ordinary Lie algebra in degrees greater than one. Theorem 4.5 proves the relevant elimination theorem by constructing inverse maps of semidirect products; Theorem 4.7 proves the independence criterion for strongly free sequences. Cross brackets are independent over the enveloping algebra because their words have distinct final generator letters in the eliminated part. Theorem 4.4 lifts strong freeness from the reduced quadratic algebra to the mixed algebra using the relation-module exact sequence and matching Hilbert series.

Theorem 1.1 is proved in §7, pp.19–21. With a minimal presentation, transgression identifies H^2 dual with minimal relations. The dual of the cup product sends those relations to their quadratic initial forms, including the square terms. Vanishing on U_LM cup U_LM puts them in the ideal generated by the other basis variables. Surjectivity on U_LM cup V_LM makes their cross-bracket projections linearly independent. Theorems 4.7 and 4.4 give strong freeness. The source's tensor description is read in the reduced quadratic algebra, where the square symbols are represented by xi_i^2; the mixed-algebra lifts are recovered by Theorem 4.4.

Labute–Mináč Theorem 5.3 imports the induction of Labute 2006 Theorem 4.1 for its relation-module and dimension assertions. That complete induction, author-version pp.17–19, was inspected. It compares the relation ideal with the associated graded normal subgroup, proves injectivity and surjectivity one degree at a time, and lifts graded freeness to the completed relation module. The modification needed at 2 is exactly that the relation ideal, lying in degrees at least two, sits in the free Lie algebra supplied by Labute–Mináč Theorem 2.3 and has torsion-free quotient. The resulting exact resolution is

    0 -> R/[R,R] -> Z_p[[G]]^d -> Z_p[[G]] -> Z_p -> 0,

with the first term free of positive finite rank. It gives cd<=2, and nonzero H^2 gives equality. The 2006 author's addendum was inspected: its corrections concern examples and a dimension formula, not this relation-module proof or the strongly-free cup criterion used here.

## Removing temporary markings and restoring the prescribed ramification

Apply the auxiliary construction with marking set S union T, where S is the finite set of primes that the final theorem is required to allow to ramify. It gives a nonempty tame A and extra markings T_0 such that (X minus A,S union T union T_0) is K(pi,1).

Proposition 7.1 is not an unsupported assertion of monotonicity under deleting primes. Its proof first removes markings. Over the universal marked pro-p cover, Corollary 3.4 shows that removing T_0 leaves H^i=0 for i>=2 and creates only the expected unramified H^1 classes at those points. H^2 of the corresponding kernel group injects into zero, so that kernel is a free pro-p group. Lemma 2.2 and Corollary 3.7 recover the K(pi,1) property after passing to its universal pro-p cover. Its nontrivial local decomposition groups are torsion-free procyclic groups, hence Z_p, giving the full unramified p-extension at the newly unmarked points.

Repeating this for the markings S gives (X minus A,T) K(pi,1) and realizes the maximal unramified p-extension at all primes in S. Excision after removing S from the scheme identifies the new cohomology with the local ramified cohomology above those unramified towers. It vanishes in degree at least two. The new kernel is again free; its local H^1 maps identify it with the expected free pro-p local groups. The pro-p isomorphism criterion using H^1 and H^2 and the cohomology theorem for free products then give full local realization at S and the stated free-product result. The K(pi,1) comparison for (X minus (S union A),T) follows at the same time.

This proves cd<=2. For each v in A, its local field has residue characteristic different from p and contains mu_p. The full local pro-p group has the tame presentation with Frobenius action tau -> tau^{N(v)}. Its quotients of finite cohomological dimension are the full group, the unramified Z_p quotient, and the trivial group. To check the point used here: finite cohomological dimension excludes nontrivial p-torsion, so a nontrivial inertia image must be Z_p; a nonzero kernel projecting to the Frobenius factor would impose N(v)^a=1 on that infinite inertia for a nonzero a in Z_p, impossible because N(v)>1 is not a p-adic root of unity. This applies at p=2 as well. The auxiliary construction ensured actual ramification at every v in A, so the decomposition group is full. It has cd=2, proving exact global cd=2 and local realization at A.

Finally, V_A^{S union T union T_0}=0 implies the smaller obstruction groups used after unmarking also vanish. The localization sequences for H^1 and H^2, the inherited surjective cup product at A, and the surjective local cup products at S give the final surjective global cup product. Empty final T now gives precisely the ordinary curve asked for in the report.

## Import ledger and checked hypotheses

The following are imports, not claims of foundational reproving.

- Homotopy comparison: Schmidt 2007 Proposition 2.1, pp.4–5, with its Artin–Mazur comparison input. The scheme is connected and locally noetherian. Empty marking is essential to the direct application to the report's homotopy wording.
- Tate local duality and local H^1 dimensions: Neukirch–Schmidt–Wingberg, second edition, 7.2.6 and 7.3.9. All local fields used for these calculations are nonarchimedean; coefficients are F_p or their Cartier dual mu_p; p differs from the characteristic of the field. Residue characteristic may equal p only at already specified or temporarily marked primes, never at the newly selected tame primes.
- Artin–Verdier duality: Milne, Arithmetic Duality Theorems, II.3.1–3.2. For F_p on X=Spec(O_k), it identifies H^3(X,F_p) dual with mu_p(k). The ordinary/compact-support comparison has no relevant real correction for odd p, and none at all over a totally imaginary field. The boundary maps to local H^2 are dual to the inclusions of roots of unity, justifying omission of exactly one local factor when delta=1.
- Invertible-coefficient comparison and Euler characteristic: Milne II.2.9 and II.2.13, together with NSW 10.4.8. These are applied after deleting all p-adic primes, so p is invertible on that intermediate affine curve. Excision restores the desired tame scheme afterward. The argument does not incorrectly assume p invertible on the final tame scheme.
- Poitou–Tate: NSW 8.6.7 and 8.6.10, for finite coefficient modules of order invertible outside the auxiliary finite set, which contains S_p and the archimedean places. With the real-place convention the unwanted real p-primary terms vanish. The relevant dual module is mu_p. The class-group identification used in Lemma 6.5 is NSW 8.6.3; the T-idèle exact sequence is NSW 8.3.5, applied with finite Cl_T and no p-primary part.
- Kummer Hasse principle: NSW 9.1.9(ii). The eligible splitting-prime set has density 1/[k(mu_p):k], strictly above 1/(p[k(mu_p):k]); removing a density-zero set and finitely many primes preserves the inequality. Exponent p avoids the exceptional exponent-2^r case with r>=3. Passing a density-zero set to a finite extension again has density zero.
- Chebotarev: used only in finite Galois composita with explicitly compatible Frobenius prescriptions. Linear disjointness in Lemma 6.4 or 6.5 makes those prescriptions compatible. Nonempty Frobenius classes have positive density and survive exclusion of M and finite sets. No GRH, effective Chebotarev bound, or density conjecture is needed.
- Cup/relator coefficients: NSW 3.9.13 and Labute–Mináč §7. Presentations are minimal and finitely generated; characteristic-2 square coefficients are retained. Surjective cross-cup products force the needed independent nonzero quadratic relation forms.
- Mildness and cd=2: Schmidt 2007 Theorem 5.5, Labute 2006 Theorems 3.3, 3.10 and 4.1, and Labute–Mináč Theorems 4.4, 4.7 and 5.3. Their graded hypotheses, nonzero relation count, and finite presentation hypotheses were checked in the constructions above. PBW, elimination, and the free-Lie-subalgebra input are used with the stated graded free or torsion-free modules; they are algebraic imports, not additional number-field restrictions.
- Pro-p recognition: NSW 1.6.15. The maps are maps of pro-p groups, H^1 is an isomorphism, and H^2 is injective, with trivial F_p coefficients. No assertion that H^1 alone detects a general pro-p isomorphism is used.
- Free-product cohomology: NSW 4.3.14, for the bundle of pro-p local decomposition groups over the profinite set of primes in the relevant Galois extension. The direct sums are the continuous generalized sums used in Schmidt §7, not unqualified sums over an infinite discrete set.
- Local maximal-pro-p comparison and dimension: NSW 7.5.2–7.5.3, 7.5.8 and 7.5.9. The newly selected primes are tame and contain mu_p; full local groups have cd=2, and inflation from their maximal pro-p quotients preserves the p-primary cohomology used in the proof.

The companion NESTED_DEPENDENCY_LEDGER.md gives exact statements, inspection depth, the marked local-condition correction, and every corrected cyclic-field occurrence. NSW references were checked in the author's corrected online edition 2.3 (May 2020), using the numbered results rather than assuming page-number identity with the 2008 edition. Milne's second edition preserves the relevant theorem numbering. Its full PDF was available to the public web reader; a separate direct file request returned HTTP 406, so no local byte hash is claimed for that source.

## Acceptance boundary

Accept the prior-resolution finding for the exact OWR conjecture under its original real-place convention, with the explicit local proof corrections and auxiliary choices recorded above. Credit Schmidt and Labute–Mináč. Do not call the audit a new solution. Do not assert that an arbitrary further finite enlargement preserves K(pi,1); Schmidt's separate enlargement theorem has a nonsplitting hypothesis and is unnecessary here. Do not infer full profinite, characteristic-p, or p=2 real-field coverage from a pro-p theorem with different hypotheses.

No original proof-search, dataset modification, queue modification, GitHub mutation, or publication was performed in this audit. The accompanying verification metadata contains only public bibliographic and byte-integrity information. Downloaded source bodies and inspection images are excluded from the authored deliverables.
