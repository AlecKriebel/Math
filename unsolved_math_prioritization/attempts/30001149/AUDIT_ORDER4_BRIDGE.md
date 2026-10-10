# Independent audit: the order-four weak-to-strong bridge

Date: 2026-10-10 UTC. Target: 30001149 / OWR-3388-008.

## Verdict

**Accept both exact candidates as mathematically proved under their stated hypotheses.** The maximal orbit degree eight is excluded by the elementary group argument. The remaining orbit degree four is excluded by the elliptic-quotient and tame-quotient argument. No blocking error or circular use of the desired bridge was found.

The accepted result is restricted to exact order four over an algebraically closed field of characteristic two. It removes the common-orbit-field hypothesis in that case. It does not resolve the original problem for higher powers of two or for odd characteristic. The resulting conjugacy class is already known; this audit is not a global novelty certificate, journal acceptance, or formal proof-assistant verification.

## 1. Distributed proof editions and accepted statement

The original proof arguments were read completely and accepted without a mandatory mathematical correction. The distributed editions below retain those arguments and update only status and novelty wording where needed:

- [ORDER4_R3_EXCLUSION.md](ORDER4_R3_EXCLUSION.md): 6,804 bytes; SHA-256 `f9676757a73ab41a5c8680ad8e2fbbb79879c2b1b761ba3ef1c9971ed91ad4c3`.
- [ORDER4_WEAK_BRIDGE.md](ORDER4_WEAK_BRIDGE.md): 11,335 bytes; SHA-256 `b2596a89e01e7d28dad57ff4fed82033522f114ac525491cf70bd0a6fd36e645`.

The dependency `ORBIT_TOWER_PARTIAL.md` was reread completely and its uses were checked against its stated ranges. The distributed edition is 6,714 bytes, SHA-256 `7426828fffb45642676a9848c235ce72f53b09c1a4bc7f217f211ce8e939eaa4`. It has the separate detailed acceptance audit in [AUDIT_RAMIFICATION_TOWER.md](AUDIT_RAMIFICATION_TOWER.md). The full mathematical content of all three proofs and both audits is retained. The ramification partial is not a dependency of this bridge.

**Precise accepted theorem.** Let k be algebraically closed of characteristic two. Let sigma be a k-algebra automorphism of k[[t]] of exact order four. Suppose that sigma(t) belongs to a degree-two Artin–Schreier extension E0/k(t) embedded in k((t)). Then

    k(t, sigma(t), sigma^2(t), sigma^3(t)) = k(t, sigma(t)) = E0,
    [k(t, sigma(t)):k(t)] = 2.

In particular E0 is sigma-stable. The known strong classification then implies that sigma belongs to its known single conjugacy class over algebraically closed k. No stability of E0 is assumed in proving the displayed statement.

## 2. Source and hypothesis boundary

The original setting is Ted Chinburg's contribution, *Katz-Gabber covers with extra automorphisms*, in *The Arithmetic of Fields*, Oberwolfach Report 05/2009, pp.325–327. Its ambient k is algebraically closed. Definition 1 on p.326 constrains the single image sigma(t); Theorem 2 on p.327 separately adds the common-field condition for all powers. The closing question drops that condition. These passages were checked in local text and the two relevant page images. [Publisher record](https://ems.press/journals/owr/articles/3388), [DOI](https://doi.org/10.4171/owr/2009/05).

The E0 formulation is equivalent to the normalized original one. Choose an Artin–Schreier generator beta of E0 with beta^2-beta=alpha in k(t), and subtract its finite nonpositive Laurent part h in k[t^-1]. The new beta'=beta-h belongs to tk[[t]], generates the same extension, and satisfies beta'^2-beta'=alpha-(h^2-h) in k(t) intersect tk[[t]]. Conversely, the original definition provides such a degree-two extension.

Bleher–Chinburg–Poonen–Symonds, *Automorphisms of Harbater–Katz–Gabber curves*, Definition 1.1, uses the whole orbit field. Theorem 1.2 and Remark 1.4 give the strong classification and its single-class consequence. Definition 1.1 and Theorem 1.2 were visually checked on manuscript p.2; Remark 1.4 was checked in the author PDF text. Example 7.4, visually checked on p.17, is contextual corroboration for elliptic automorphisms and has HKG hypotheses. The present proof does not import those hypotheses or apply that example as an HKG theorem to its curves. [Author manuscript](https://math.mit.edu/~poonen/papers/AutK.pdf), [DOI](https://doi.org/10.1007/s00208-016-1490-2).

All geometric curves below mean smooth projective models of the stated one-variable function fields. Algebraic closure gives constant field k, rational closed points, and genus-zero curves isomorphic to P1. Quotients by finite groups are separable Galois covers; no purely inseparable degree is silently included in a Hurwitz computation.

## 3. Common orbit-field facts actually needed

Write t_i=sigma^i(t), with indices modulo four, and L=k(t_0,t_1,t_2,t_3). The orbit theorem supplies an integer 1<=r<=3, with [L:k(t_i)]=2^r, and Galoisness over every coordinate field and every consecutive interval field. An interval of ell<=r+1 coordinates has degree 2^(ell-1) over each coordinate it contains and index 2^(r-ell+1) in L. In particular every interval of r+1 coordinates generates L.

The first adjacent extension has degree exactly two, rather than merely at most two. If sigma(t) were rational in t, finite order would turn sigma(k(t)) subset k(t) into equality. Its restriction would still have order four, impossible in PGL2(k). A power fixing t acts identically on k[[t]], so the order cannot drop on k(t). Consequently k(t,sigma(t))=E0.

The embedding into k((t)) defines a point x with valuation group Z because v(t)=1. Its residue field is k, t is a uniformizer, and sigma preserves the valuation and fixes x. The action on L retains exact order four since it acts on t with that order. No assertion that X is an HKG curve follows or is needed here.

The cited whole-orbit genus bound specializes at p=2,r=2 to g_X<=5. It can also be rechecked immediately: an adjacent pair curve has two generating degree-two rational subfields, giving genus at most one; adding a third coordinate gives degrees two and four for the two generating subfields, so Castelnuovo–Severi gives g_X<=2*1+(2-1)(4-1)=5. All these maps are separable by the orbit Galois theorem. The perfect-field form and the common-factor condition are given in Khawaja–Siksek, *Primitive algebraic points on curves*, Theorem 14. [Published statement](https://link.springer.com/article/10.1007/s40993-024-00543-4).

## 4. Full audit of the orbit-degree-eight exclusion

Assume r=3. Here A_i fixes the triple field K_i=k(t_i,t_(i+1),t_(i+2)); this differs from the pair-field notation A_i used later when r=2. Keeping these two definitions separate is essential.

### 4.1 Distinctness, intersection, and neighboring commutation

Each K_i has index two in L. Two different triples together contain all four coordinates. Thus equality K_i=K_j would force their common field to be L, a contradiction. Since L/K_i is Galois, the corresponding order-two fixed groups A_i, and hence their nonidentity elements a_i, are all distinct.

For C_i=k(t_(i+1),t_(i+2)), both K_i/C_i and K_(i+1)/C_i have degree two. Their compositum is L and [L:C_i]=4. Their intersection must be C_i: otherwise the prime-degree argument would make the two fields equal. The group generated by A_i and A_(i+1) is finite because it fixes C_i and lies in Aut(L/C_i), whose order is at most four. Its fixed field is K_i intersect K_(i+1)=C_i. Artin's theorem therefore makes its order four. Two distinct involutions generate that group, so it is C2 x C2 and the generators commute.

This does not assume that the compositum of arbitrary normal towers is normal. The required normality of L/K_i was already established by the orbit theorem; Artin's fixed-field theorem is applied to an explicitly finite subgroup.

### 4.2 Generation of the order-eight coordinate groups

The three groups A_(j-2), A_(j-1), A_j fix t_j. The last two generate a subgroup of order four with fixed field k(t_j,t_(j+1)). If A_(j-2) were already in it, its fixed field K_(j-2) would contain that pair. K_(j-2) already contains the other three coordinates, so this would give K_(j-2)=L. Thus adjoining A_(j-2) strictly enlarges the order-four subgroup inside H_j=Gal(L/k(t_j)), which has order eight. The generated group is exactly H_j.

### 4.3 Elimination of the nonabelian possibility

For a_i,a_(i+1),a_(i+2), the middle generator is central in their order-eight generated group H_(i+2). The quotient by its order-two subgroup has order four and is abelian. Therefore the endpoint commutator lies in that middle subgroup. If the group is nonabelian the commutator is its nonidentity element; if the endpoints commuted, all three generators would commute.

Sigma conjugates all H_j transitively, so either all or none are nonabelian. In the nonabelian case the triples (a_0,a_1,a_2) and (a_2,a_3,a_0) give

    [a_0,a_2]=a_1,   [a_2,a_0]=a_3.

With the written commutator convention and involutory endpoints, the two commutators are inverse elements. Since a_1 has order two they are equal, contradicting a_1!=a_3. Hence each H_j is abelian and generated by involutions, so is elementary abelian of order eight.

### 4.4 The order-sixteen subgroup and restriction kernel

Every pair of the four a_i lies in one of these triples, so all commute. Their group P is elementary abelian, generated by four elements, and contains H_0. Its order is eight or sixteen. In the first case all H_i would be P, so all k(t_i) would be equal, contrary to the degree-two adjacent extension. Therefore |P|=16.

Let F=L^P. Then F subset k(t_0), [L:F]=16, and [k(t_0):F]=2. In particular F is nonconstant. Lüroth applies in this characteristic and makes F rational.

Sigma normalizes P by cyclically permuting A_i. But sigma^2 conjugates A_0 to the different A_2, whereas any element of the abelian P conjugates P trivially. Thus sigma^2 is not in P. Every nontrivial subgroup of <sigma> contains sigma^2, so <sigma> intersect P=1. Artin's theorem identifies Aut(L/F) with P, making this intersection exactly the restriction kernel. The induced automorphism of F has exact order four.

Finally, a projective 2-power torsion matrix in characteristic two has equal eigenvalues: the eigenvalue ratio is a 2-power root of unity, hence one. After scaling and conjugation it is scalar or a size-two unipotent block. Its square is the identity. Thus PGL2(k) has no element of order four. This is the required contradiction.

**Disposition of this candidate:** accept r!=3. Its own stated residual degree-four possibility is correctly not claimed solved by that file alone.

## 5. The orbit-degree-four setup and elliptic facts

Now assume r=2. Set H_i=Gal(L/k(t_i)) and A_i=H_i intersect H_(i+1). The orbit theorem gives |H_i|=4, |A_i|=2, and trivial intersections of three consecutive H_i.

Neighboring A_i cannot coincide, because that would give a nontrivial threefold intersection. They lie in H_(i+1), so they generate that order-four group, which is C2 x C2. This proves their commutation. If opposite groups A_0=A_2, conjugation by sigma also gives A_1=A_3. Then H_0=<A_3,A_0>=<A_0,A_1>=H_1, contrary to the adjacent degree-two extension. The other opposite equality is equivalent by conjugation. Thus all four a_i are distinct and

    H_i=<a_(i-1),a_i> is C2 x C2.

Let E_i=L^{A_i}=k(t_i,t_(i+1)). Sigma permutes them, so their genera have a common value e<=1. The inequality uses the two generating coordinate fields, not an action of sigma on any one E_i.

### 5.1 Why the Weierstrass substitutions exhaust the possibilities

On an elliptic curve with origin O, the standard Riemann–Roch spaces for 2O and 3O show that an origin-preserving automorphism has the form

    x -> u^2 x+r,    y -> u^3 y+v x+w,    u!=0.

Indeed x has pole order two and y pole order three at O; the leading coefficients satisfy B^2=A^3 and can be written A=u^2, B=u^3. This is a statement about the chosen elliptic origin, without an HKG condition.

Over algebraically closed characteristic-two k the ordinary and supersingular normal forms in the candidate are valid. They can be obtained directly from a nonsingular general Weierstrass equation. If a_1!=0, scaling and translations remove a_3 and a_4 and give y^2+xy=x^3+c x^2+d, with nonsingularity forcing d!=0. If a_1=0, nonsingularity forces a_3!=0; scale a_3 to one. Starting with y^2+y=x^3+a_2x^2+a_4x+a_6, use x=X+r and y=Y+sX+w. Choose s=a_4+r^2 and solve r^4+r+a_4^2+a_2=0; then choose w from its Artin–Schreier equation to remove the constant. Algebraic closure supplies these choices, giving Y^2+Y=X^3. This also supplies the model reduction without invoking a classification of HKG curves.

### 5.2 Ordinary calculation

For y^2+xy=x^3+c x^2+d, substitution and reduction by the original equation give coefficient of xy equal to u^6+u^5 and coefficient of y equal to r u^3. These force u=1 and r=0. The remaining difference is

    (v^2+v)x^2 + w x + w^2.

It vanishes exactly when w=0 and v^2+v=0. Hence the only origin-preserving automorphisms are identity and (x,y)->(x,y+x), the negation map. There is no origin-preserving element of order four on an ordinary curve.

### 5.3 Supersingular calculation and the full automorphism group

For y^2+y=x^3, coefficient comparison gives

    u^6+u^3=0,   v^2=u^4 r,   v=u^2 r^2,   w^2+w=r^3.

Since u!=0, these are equivalently u^3=1, r^4=r, v=u^2r^2, and w^2+w=r^3, exactly as in the candidate. If the substitution is an involution, its square on x has linear coefficient u^4=1, which together with u^3=1 forces u=1. Its square on y is y+r^3. It follows that r=0, v=0, and w is zero or one. Thus the unique nonidentity origin-preserving involution is (x,y)->(x,y+1), namely negation.

Negation has no affine fixed point on this model and fixes O, so E(k)[2]={O}. This concerns rational torsion points, not the length of the 2-torsion group scheme. Every curve automorphism is uniquely T_Q followed by an origin-preserving group automorphism. The linear part of an involution has square one. If the linear part were identity, a nontrivial involution would be a nonzero rational 2-torsion translation, impossible. Hence every nonidentity involution is T_Q[-1]. Two distinct such elements multiply to the nonzero translation T_(Q-R). If they commuted this product would have order two, again impossible. The full automorphism group, including translations, therefore contains no C2 x C2.

### 5.4 Rational quotients of elliptic involutions

An involution with genus-zero quotient must have a fixed point. Otherwise the degree-two quotient cover is unramified and Hurwitz would give 0=2*(-2), a contradiction. Choosing a fixed point as origin makes the involution the unique nonidentity origin-preserving involution computed above. Relative to any other origin it is T_Q[-1]. The product of two such involutions is a translation. This argument works in the wild characteristic because the hypothetical fixed-point-free cover has zero different; it does not use the tame formula for a ramified degree-two cover.

### 5.5 Consequences for X and E_i

If g_X=0, sigma would give an order-four element of PGL2(k). If g_X=1, take its fixed point x as origin. The ordinary calculation rules out an ordinary curve, while the supersingular calculation rules out the subgroup H_i=C2 x C2. Therefore 2<=g_X<=5, and Aut_k(X) is finite, as for every smooth projective curve of genus at least two.

If e=0, E_0 and E_1 are rational, have index two in L, and generate L because three consecutive coordinates do. Castelnuovo–Severi would give g_X<=1. Hence e=1. In particular every subsequent appeal to elliptic automorphisms is now justified.

## 6. The commuting dihedral groups and the even-order obstruction

Put B=<a_0,a_2> and C=<a_1,a_3>. Each generator of one commutes with both generators of the other, including the neighboring pair across the cyclic index boundary. Therefore B and C commute elementwise, BC=P is a subgroup, and conjugation by any element bc of P restricts on B to conjugation by b. At this point B intersect C need not yet be trivial; the proof correctly does not assume it.

Their rotation elements r_B=a_0a_2 and r_C=a_1a_3 have the same finite order d>=2. Finiteness follows from g_X>=2; equality of orders follows from sigma conjugation. A group generated by two distinct involutions whose product has order d is dihedral of order 2d. Alternating words give the rotation and reflection normal forms; the two cosets are distinct. If a generating involution were a power of the rotation, the generated group would be cyclic, which has at most one involution, contradicting the distinct generators. This includes d=2, where the group is C2 x C2.

Conjugation by sigma sends r_B to r_C and r_C to r_B^-1 and exchanges B and C. It therefore normalizes P. Since P contains H_0, F=L^P is contained in k(t_0). F has transcendence degree one because [L:F]=|P| is finite. Lüroth makes F rational.

For even d, the two generating reflections a_0 and a_2 have distinct images in the abelianization B/[B,B]=C2 x C2. An inner automorphism cannot interchange them. But sigma^2 does interchange them. If sigma^2 were in P, its conjugation on B would be inner by the preceding elementwise commutation. Thus sigma^2 is not in P, and <sigma> intersect P=1. Artin identifies P=Aut(L/F), giving a faithful order-four action on the rational F, impossible.

This proves that d is odd before any faithful action of C on E_0 is claimed. That order of argument is important: for even d, a central intersection could invalidate such faithfulness.

## 7. Odd order, faithful elliptic descent, and free translations

For odd d, the center of a dihedral group of order 2d is trivial. Since B and C commute, an element of B intersect C is central in both. Thus B intersect C=1 and P=B x C.

C normalizes A_0, in fact centralizes it, so preserves E_0=L^{A_0}. The kernel of its restriction is

    C intersect Aut(L/E_0) = C intersect A_0 = 1.

The first equality uses Artin for the actual fixed field E_0, and the final equality uses A_0 subset B and B intersect C=1. Hence the descended C-action is faithful, with the orders of all its elements preserved.

The fixed fields of the descended involutions are

    (E_0)^{a_1}=L^{<A_0,A_1>}=k(t_1),
    (E_0)^{a_3}=L^{<A_0,A_3>}=k(t_0).

Thus both involutions have rational quotient. Their product r_C is a translation on E_0, of exact order d. Every nonidentity power is a nonzero translation, so fixes no point of E_0. A point of X fixed by such a power would map to a fixed point on the quotient curve of E_0, impossible. Thus the entire cyclic group R_C=<r_C> acts freely on X, not merely its chosen generator.

The quotient map by R_C is consequently unramified and separable. Riemann–Hurwitz yields

    g_X-1 = d(g_(X/R_C)-1).

Here g_X-1 is a positive integer at most four. Thus g_(X/R_C)-1 is positive, and d divides g_X-1. As d is odd and at least three, the only possibility is d=3 and g_X=4 (with g_(X/R_C)=2).

Consequently P=S3 x S3 and R=<r_B,r_C>=C3 x C3. R is characteristic in P, for example as its commutator subgroup, and is also directly normalized by sigma through the displayed conjugation equations. No assumption that R acts freely is made. The argument proves that R_C is free, and sigma-conjugacy gives the same conclusion for R_B; this does not establish freeness for the other cyclic subgroups of R.

## 8. The tame quotient and the one-branch obstruction

Let Y=X/R, h=g_Y. Because |R|=9 is prime to characteristic two, all inertia is tame. A tame inertia subgroup at a smooth point embeds by its tangent action in k^*, so is cyclic. One way to see the required injectivity is that the kernel lies in the first ramification group, which is a 2-group, while the group here has odd order. Since R has exponent three, nontrivial inertia has order exactly three, never nine.

Over algebraically closed k the decomposition and inertia groups coincide. Each branch point on Y therefore has 9/3=3 points above it, each with different exponent 3-1=2. If s is the number of branch points on Y, their total different contribution is 6s. The tame Hurwitz formula gives

    6 = 2g_X-2 = 9(2h-2)+6s,
    s=4-3h.

The only nonnegative possibilities are (h,s)=(0,4) and (1,1).

Suppose (h,s)=(1,1), and call its sole branch point Q. The inertia subgroup I has order three. As R is a two-dimensional vector space over F3, there is a homomorphism chi:R->C3 nonzero on I. For H=ker chi, the intermediate cover X/H -> Y is cyclic of degree three. Inertia in that quotient is the image of I, so Q remains ramified; no new branch point appears in an intermediate cover.

Kummer theory applies because characteristic two is coprime to three and k contains a primitive cube root of unity. Thus the cyclic intermediate extension is k(Y)(w) with w^3=f in k(Y)^*. This precise Kummer converse is stated in [Stacks Project, Lemma 9.24.1](https://stacks.math.columbia.edu/tag/09I6).

For completeness the valuation criterion used here can be verified in the completed local field k((z)). Write f=z^m u with u in k[[z]]^*. Every such unit has a cube root: its nonzero constant has a cube root in k and Hensel's lemma applies since the derivative of X^3-u at that root is nonzero. Therefore the local extension is generated by a cube root of z^m. It is unramified (indeed locally split) if 3 divides m and totally ramified of degree three otherwise. Consequently v_Q(f) is not divisible by three while every other v_T(f) is divisible by three.

All closed points have degree one over k. The principal-divisor identity

    sum_T v_T(f)=0

is now impossible modulo three. This proves that a single branch point cannot occur. No characteristic-zero topological fundamental-group assertion, or false genus-one unramified-cover obstruction, is being used. Hence Y has genus zero and is rational.

## 9. The final exact-order kernel check

Let c_sigma denote conjugation by sigma. We have

    c_sigma(r_B)=r_C,    c_sigma(r_C)=r_B^-1.

Applying this twice gives inversion of both generators of R. This is nontrivial because they have order three. Since R is abelian, conjugation by any element of R is trivial on R. Therefore sigma^2 is not in R. Equivalently, its order already distinguishes it from the odd-order R, but the written conjugation argument is independently valid.

It follows that <sigma> intersect R=1. Sigma normalizes R, so acts on L^R=k(Y), and Artin's theorem gives Aut(L/L^R)=R. The kernel of this restriction is exactly the trivial intersection. Thus its action on rational k(Y) has exact order four, contradicting the PGL2 fact once more.

This excludes r=2. Together with the separate r=3 exclusion and the original 1<=r<=3, it forces r=1. At this point, and only at this point, the whole-orbit hypothesis of the known strong classification is established.

## 10. Disposition, novelty, and remaining limits

- Accept the exact two candidates and their combination as a restricted theorem. No corrective patch is required.
- The proof uses the accepted orbit tower, elementary finite-group and fixed-field arguments, Lüroth, Castelnuovo–Severi, elementary elliptic automorphisms, Riemann–Hurwitz, and tame Kummer theory. It does not require an HKG assertion for the pair field or the enlarged orbit field.
- The known conjugacy class, its formulas, and the strong classification remain credited to the literature. The possible contribution represented by these candidates is specifically the removal of the common-field assumption for order four.
- Bounded searches for weak almost-rational order-four classification and quadratic finite-order Nottingham elements did not establish whether this bridge has previously appeared elsewhere. Search non-detection is not evidence sufficient to call the result new. A separate literature and novelty assessment remains necessary before claiming priority.
- The original all-primes, all-orders problem remains unresolved by these files. Orders 2^n with n>=3 and odd-characteristic orders p^n with n>=2 are outside the theorem. In particular this audit does not justify changing the overall problem to solved.
- The field and group symbols A_i refer to different subgroups in the r=3 and r=2 proofs. A combined presentation should keep that distinction explicit. This is an editorial caution, not a mathematical defect.
- An optional exposition improvement is to include the explicit Weierstrass coefficient comparison and the local Kummer unit argument from this audit. Their omission from the candidates does not leave an unproved special-case claim: the stated standard hypotheses are satisfied.

## 11. Inspection and verification record

Input bytes and hashes were checked before the proof review, frozen without changes, and checked again after the review. The audit is a complete mathematical argument check, including intersections, generated-group orders, all quotient restriction kernels, curve genera, both elliptic substitutions, freeness of every nonidentity rotation in R_C, tame inertia, and the one-branch obstruction. No finite computation or truncated power-series experiment is substituted for a proof.

Previously retained public PDFs were independently rehashed during this audit:

- Oberwolfach Report 05/2009: 644,177 bytes; SHA-256 `0fa8b21258df304ffac28c381a7035b1af3ec550edc046209b38d52a87e5b1ee`.
- BCPS author manuscript: 453,738 bytes; SHA-256 `69b1152c83d139e56d5b0a96b1ad67b271388e58cb2d77adfc4668c96a7aed05`.

The latter is an author-manuscript identity, not a journal-PDF identity claim. Existing rendered images of OWR pp.326–327 and BCPS pp.2 and 17 were inspected. The current public author PDF was also opened through the web text tool; that retrieval was not treated as a new byte-identical local download. The current published Castelnuovo–Severi statement and Stacks Kummer converse were checked through their public pages. No copied third-party source files are part of this authored audit package.
