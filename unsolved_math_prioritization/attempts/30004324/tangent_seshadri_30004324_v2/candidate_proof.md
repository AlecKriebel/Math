# A pointed minimal-rational-curve route to the tangent-Seshadri conjecture

Expanded author candidate v2, 2026-10-05. Two independent AI geometry audits of the original candidate found no essential gap. This version makes their four recommended justifications explicit and awaits a final delta audit. It is not a published or refereed resolution, and historical novelty is not established.

## Exact target

Let X be a smooth integral projective variety of dimension n >= 1 over an algebraically closed field k of arbitrary characteristic. Suppose that a closed point x in X satisfies epsilon(T_X;x) > 0, in the relative vector-bundle sense of Fulger--Murayama. The proposed conclusion is X isomorphic over k to P^n.

The conjecture is [FM21, Conjecture 4.9], corresponding to [FM19v2, Conjecture 5.9] and Fulger's contribution to OWR 53/2019, printed p. 3289. No Fano, nef-tangent, general-point, or characteristic-zero hypothesis is added.

## Definition and imported results

For a vector bundle E on X, use the quotient projective bundle rho:P(E)=Proj_X Sym(E)->X and its tautological class xi. The relative Seshadri constant is the infimum of xi.Gamma / mult_x(rho_*Gamma) over integral curves Gamma in P(E) whose image contains x and which are not contracted by rho. The multiplicity of the pushforward includes the full generic mapping degree. Global nefness of E is not required.

Equivalently, for normalizations nu:Ctilde->C of integral curves C through x,

epsilon(E;x) = inf_C mu_bar_min(nu^*E) / mult_x C.

Here mu_bar_min is the minimum quotient slope in characteristic zero. In characteristic p>0 it is the limit of p^(-e) mu_min(F^{e*}(nu^*E)). This normalization is essential on a general curve. On P^1 it is exactly the smallest splitting degree in every characteristic.

The following inputs are used with their stated hypotheses. The independent reports are supporting checks, not substitutes for these mathematical sources.

1. **Curve formula.** Fulger--Murayama, *Seshadri constants for vector bundles*, J. Pure Appl. Algebra 225 (2021), no.4, 106559, [DOI 10.1016/j.jpaa.2020.106559](https://doi.org/10.1016/j.jpaa.2020.106559), Example 3.20 and Corollary 3.21. The [public manuscript](https://par.nsf.gov/servlets/purl/10198624), pp.9--10, is the inspected final-numbering source. It applies to projective schemes over algebraically closed fields and does not assume the bundle globally nef.
2. **Existence at the specified point.** The same paper, Corollary 4.6 and its proof, p.16, deduces uniruledness and separable rational connectedness from the exact one-point hypothesis; its proof explicitly produces a rational curve through that point. Only that existence conclusion is needed here. We do not replace x by a general point.
3. **Stable maps in arbitrary characteristic.** Abramovich--Oort, *Stable maps and Hurwitz schemes in mixed characteristic*, [Theorem 2.8 and Section 2.5](https://arxiv.org/pdf/math/9808074), p.5: for a projective finite-presentation target embedded in projective space, fixed genus, number of marks, and embedding degree give a proper finite-presentation Artin stack with finite stabilizers and projective coarse moduli scheme. We take base Spec(k), genus zero, one mark, and embedding degree d. The entire stack need not be Deligne--Mumford in characteristic p.
4. **Inertia-free stacks and proper quasi-finite spaces.** [Stacks Project, Proposition 94.13.3, Tag 04SZ](https://stacks.math.columbia.edu/tag/04SZ) identifies an algebraic stack with trivial inertia as an algebraic space. [Proposition 67.50.2, Tag 03XX](https://stacks.math.columbia.edu/tag/03XX) makes a separated locally quasi-finite algebraic space over a scheme a scheme. [Lemma 37.44.1, Tag 02LS](https://stacks.math.columbia.edu/tag/02LS) then makes a proper quasi-finite morphism finite. These results are applied to the actual evaluation fiber, not to an assumed closed base change of a coarse-space construction.
5. **Pointed map deformations.** For a fixed smooth proper source curve and smooth target, the obstruction group for maps with prescribed values at a finite set of distinct source points is H^1 of the pulled-back tangent bundle tensored with the ideal of those points. Its vanishing gives the corresponding smooth Hom/evaluation morphism. The two-point evaluation calculation is given explicitly in [Gounelas, *Free Curves on Varieties*, Proposition 4.7 and proof](https://ems.press/content/serial-article-files/26314?nt=1), Documenta Math.21 (2016), printed p.299, citing Kollar II.3.5. Lemma 4 below supplies the fixed-value Cech lifting argument used here; it does not use characteristic-zero generic smoothness.
6. **Cohomology, base change, and descent.** [Stacks Project, Lemma 36.30.4, Tag 0B91](https://stacks.math.columbia.edu/tag/0B91) applies to a proper flat morphism of finite presentation and an invertible sheaf, making derived pushforward perfect and compatible with arbitrary base change. Fiber cohomology h^0=1, h^1=0 then gives the rank-one pushforward and adjunction isomorphism used below. Alternatively [Lemma 37.33.2, Tag 0EX7](https://stacks.math.columbia.edu/tag/0EX7) directly gives descent of a fiberwise-trivial bundle over a reduced base when the structure-sheaf pushforward is universally the structure sheaf; the latter hypothesis holds for this P^1-family, also by [Lemma 53.20.12, Tag 0GKA](https://stacks.math.columbia.edu/tag/0GKA).
7. **Numerical ampleness.** Nakai--Moishezon, in arbitrary characteristic, says that a Cartier divisor on a complete scheme is ample if its top intersections with every positive-dimensional integral subvariety are positive. A characteristic-free statement is [Fujino--Miyamoto, *Nakai--Moishezon ampleness criterion for real line bundles*, Theorem 1.3](https://www.math.kyoto-u.ac.jp/~fujino/Nakai-Moishezon3.pdf). Only the Cartier-divisor case is needed; positive tensor powers do not change ampleness.
8. **The established Fano case.** Fulger--Murayama, Proposition 4.8(1), p.16 of the cited public manuscript, states that a smooth projective Fano variety over an algebraically closed field of any characteristic with epsilon(T_X;x)>0 at some point is P^n. This clause invokes Mori's theorem as Kollar, *Rational Curves on Algebraic Varieties*, V.3.2; it does not invoke Conjecture 4.9. The separate characteristic-zero general-point clause 4.8(2) is unused. The full Kollar monograph is not claimed to have been independently inspected or re-proved; the exact imported proposition is directly inspected in FM21.

## Lemma 1: every rational curve through x is very free

Let C be an integral rational curve through x and let f:P^1 -> C -> X be its normalization. Put m=mult_x C. Write f^*T_X = direct_sum_i O(a_i). In positive characteristic, Frobenius multiplies every a_i by p, so the asymptotic normalized minimal slope is min_i a_i, just as in characteristic zero. The curve formula gives

min_i a_i >= m epsilon(T_X;x) > 0.

Thus every a_i is a positive integer and f is very free. In particular, -K_X.C=sum_i a_i>0. This uses normalizations of images, so no nonzero differential is being asserted for a purely inseparable multiple cover.

For a normalization, the differential is generically nonzero, hence a nonzero homomorphism O(2)->f^*T_X exists and some a_i>=2. Consequently -K_X.C>=n+1. The stronger bound is a useful control but is not needed for the Fano reduction below.

## Lemma 2: minimal ample degree eliminates every pointed boundary

Choose a very ample line bundle A on X. By dependency 2 there is an integral rational curve through x. Define

d=min{A.C : C is an integral rational curve through x}.

This is a positive integer and is attained.

The lower bound d persists after an algebraically closed field extension K/k. Indeed, a rational image of degree c<d through x_K would give its normalization map P^1_K->X_K of degree c. Reparametrize a preimage of x_K to 0. This is a K-point of the finite-type degree-c Hom scheme over k with evaluation at 0 equal to x. A nonempty finite-type scheme over the algebraically closed field k has a k-point. That k-map has a rational image through x of A-degree at most c, contradicting the minimum. This verifies the bound at all geometric residue fields of the stable-map stack without an uncountability assumption.

Consider any geometric stable map

(g:D -> X, p), with genus(D)=0, g(p)=x, deg(g^*A)=d.

The dual graph of D is a tree, and each component is P^1. Starting with the component carrying p, follow components contracted to x until reaching a nonconstant component D_v. Such a component exists since d>0. Its image C_v is an integral rational curve through x: the function field of a nonconstant image of P^1 is rational by Luroth's theorem, including in positive characteristic. If its mapping degree onto its image is e_v, then

d = sum_{w nonconstant} e_w(A.C_w) >= e_v(A.C_v) >= A.C_v >= d.

All summands are positive integers. Hence all inequalities are equalities: D_v is the unique nonconstant component, e_v=1, and A.C_v=d.

There cannot be any contracted component. Indeed each connected contracted subtree attaches to the sole nonconstant vertex by exactly one edge because the whole dual graph is a tree. If it has t>0 vertices and contains m marked points, then m<=1 and its total number of special points, counting incidences at nodes and marks, is

2(t-1)+1+m <= 2t.

Stability would require at least 3t special points. This is impossible. Thus D=P^1 is irreducible and smooth, and g is birational onto its image.

This argument includes a mark initially lying on a contracted component and includes possible inseparable covers. The latter have e_v>1 and are excluded by the degree equality.

## Lemma 3: a proper pointed family with universal P^1-curve exists

Let M_x be the fiber over x of the evaluation morphism from the proper stable-map stack in dependency 3, with genus zero, one mark, and A-degree d. It is proper and nonempty. Lemma 2 shows that every geometric object has smooth domain P^1 and is birational onto its image.

Such an object has trivial automorphism group scheme. An automorphism preserving g is the identity on the dense open set where g is an isomorphism onto its image. The only geometric automorphism is therefore the identity. To exclude a nonreduced stabilizer in positive characteristic as well, its tangent space consists of vector fields on P^1 vanishing at the mark and killed by dg. Because the birational normalization map is generically an isomorphism to a smooth curve in X, dg is generically injective. Such a vector field is zero. A finite group scheme with one geometric point and zero tangent space is the reduced identity group scheme, by Nakayama applied to its maximal ideal.

The finite inertia morphism restricted to M_x is consequently the identity. To check the possible nonreduced base, use its identity section to split the finite pushforward algebra into the structure sheaf and its augmentation ideal. That ideal has zero geometric residue fibers and hence is zero by Nakayama. Dependency 4 now identifies M_x with an algebraic space.

Let Q be the full projective coarse scheme of the one-marked degree-d stable-map stack. The natural morphism M_x->Q is proper: M_x is proper over k and Q is separated over k. It is quasi-finite because the coarse morphism identifies geometric points with isomorphism classes of stable maps, so every geometric fiber of this restricted morphism has at most one point. By Tag 03XX, M_x is a scheme; by Tag 02LS, M_x->Q is finite. A finite morphism is projective, so M_x is projective over k.

This argument does not assert that formation of a coarse space commutes with taking an arbitrary closed fiber in wild characteristic. It only uses the map from the inertia-free actual evaluation fiber to the full coarse scheme.

Choose a normalization f:P^1->X of a degree-d rational curve through x and a preimage 0 of x. Take the reduced irreducible component H of M_x through [f,0]; Lemma 4 justifies uniqueness of its local component at this point. H is an integral projective scheme. Restricting the universal curve of the stable-map stack to H gives an actual family

pi:U->H,

with marking section sigma:H->U and evaluation e:U->X, satisfying e composed with sigma identically x. The family is proper, flat, and finitely presented. All geometric fibers are smooth P^1 by Lemma 2, so pi is smooth.

The total space U is projective. A section of a smooth relative curve is an effective Cartier divisor; consequently O_U(sigma) has degree one on every fiber. Cohomology and base change give a locally free rank-two sheaf pi_*O_U(sigma), and the fiberwise surjective evaluation map presents U as its projective-line bundle. In particular pi is projective, and so is U because H is projective. This also verifies explicitly that the marking is available globally, not merely after an unidentified cover.

The total space is integral: smoothness over the reduced H gives reducedness, and flatness with geometrically integral fibers over the integral H gives irreducibility. The degree on fibers of every line bundle pulled back from X is locally constant in this proper flat family, hence constant on connected H. In particular the A-degree is always d.

## Lemma 4: the universal evaluation covers X

By Lemma 1, f^*T_X splits with all a_i>=1. Therefore

H^1(P^1, f^*T_X(-0-infinity))=direct_sum_i H^1(P^1,O(a_i-2))=0.

By dependency 5, evaluation at infinity on Hom(P^1,X;0 maps to x) is smooth at f. Explicitly, for a square-zero extension one lifts a map into the smooth target on an affine cover of P^1, prescribing the given values at 0 and infinity. Differences of local lifts form a Cech cocycle in f^*T_X(-0-infinity) tensored with the extension ideal. The displayed H^1 vanishes, so the cocycle can be corrected and the lifts glued. Finite presentation upgrades this infinitesimal lifting to smoothness near f. This is the relative lifting problem for the value at infinity while the value at 0 remains x. Also H^1(P^1,f^*T_X(-0))=0, so this pointed Hom scheme is smooth at f and has a unique local irreducible component there. Quotienting locally by Aut(P^1,0) maps that local component to the unique local component of M_x through [f,0], which is H. Equivalently, nearby pointed maps and the point infinity define points of U over H. The smooth evaluation supplies an open neighborhood of f(infinity) in the image of e.

Since H and U are proper, e(U) is closed in X. Since X is irreducible and the image contains a nonempty open subset, e(U)=X. This step uses smoothness at the chosen very free map, not generic smoothness of an arbitrary evaluation morphism.

## Lemma 5: the contracted section forces numerical Picard rank one

Let D be any Cartier divisor on X and let b=D.C, where C is the image of any fiber of U->H. Its value is constant by connectedness. Consider the line bundle

L=O_X(dD) tensor A^(-b).

It has degree zero on every fiber image. Thus e^*L restricts to O_{P^1} on every geometric fiber of pi. By dependency 6, e^*L=pi^*B for a line bundle B on H. Pull back by sigma. Because e composed with sigma is the constant map to x, sigma^*e^*L is a trivial line bundle. Hence B is trivial, and e^*L is trivial.

A line bundle whose pullback by a surjective proper morphism of projective varieties is numerically trivial is numerically trivial. Here is the curve argument without a separability or Bertini assumption. Let Gamma be any integral curve in X, including a curve avoiding x or of positive genus, and let eta be its generic point. Because e is surjective, the finite-type k(Gamma)-scheme U_eta is nonempty. Choose a closed point z of U_eta. Its residue field is a finite extension of k(Gamma), of total degree q>0. The reduced closure Gamma' of z in U is an integral proper curve dominating Gamma: it has function field k(z), which has transcendence degree one over k. Its generic degree over Gamma is q, including any inseparable degree.

The projection formula gives

0=deg(e^*L|Gamma')=q deg(L|Gamma).

These are integer intersection degrees, not elements of k. Thus even if the characteristic divides q, the positive integer q is nonzero in this equality, and deg(L|Gamma)=0. Thus

d[D] = b[A] in N^1(X)_R.

Every divisor class is proportional to [A], so rho(X)=1.

The argument uses an actual marking section. Merely having a proper unpointed family would not justify it.

## Fano reduction and conclusion

Apply Lemma 5 with D=-K_X. By Lemma 1, b=-K_X.C>0. Therefore

[-K_X]=(b/d)[A], where b/d>0.

For any positive-dimensional integral subvariety Z of dimension r, the numerical equality gives

(-K_X)^r.Z=(b/d)^r A^r.Z>0.

Since X is smooth, -K_X is Cartier. Nakai--Moishezon (dependency 7) shows it is ample. Thus X is Fano. Dependency 8, the established Fano clause for the original point x and the same field k, gives X isomorphic to P^n.

This completes the proposed argument for every n>=1 and every characteristic. For n=1 one can instead use epsilon(T_X;x)=deg(T_X)=2-2g, so positivity forces g=0. Dimension zero is harmless if included by convention: a smooth integral projective zero-fold over k is already P^0.

## Verification boundary and review status

The proposed argument retains smoothness, projectivity, an algebraically closed field of arbitrary characteristic, and positivity at the original arbitrary closed point. No global-nef, Fano, general-point, or characteristic-zero assumption has been added. No step relies on a finite computation.

Two uninvolved AI geometry audits of the original frozen candidate reported PASS and no essential gap. Their complete authored reports are preserved in review/first_geometry_audit.md and review/second_geometry_audit.md. This v2 makes explicit their geometric-field minimality, proper quasi-finite coarse-target argument, relative degree-one marking bundle, and generic-fiber numerical multisection. A final independent delta audit of this derivative is still required before publication.

The first audit also found a separate exact-file-set defect in the original integrity verifier. The historical REVISE_REQUIRED finding is preserved in review/original_integrity_finding.md; the strict replacement is authoritative in v2. This tooling correction has no mathematical role in the proof.

No internal geometric gap is currently identified. This remains an AI-assisted, independently checked candidate; neither the audits nor this revision establish historical novelty, external peer review, or acceptance by the mathematical community. The retrieved 2025 toric paper still frames the unrestricted assertion as conjectural. Specialist review and a thorough priority search remain appropriate before any claim that the conjecture has been settled.
