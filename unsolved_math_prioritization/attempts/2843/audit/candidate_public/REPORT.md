# Support genus: five approaches and the remaining genus-one obstruction

**Problem:** K3 Problem 3.45; catalogue identifier 2843.  
**Date:** 2026-10-08.  
**Status:** rigorous partial analysis; neither part of the problem is solved.  
**Novelty:** no claim of a new contact-topological theorem. The elementary calculations below are supplied with proofs, including known mechanisms recovered during the investigation. Source searches, source normalization, and numerical checks are not counted as mathematical approaches.

## 1. The precise target

Work with closed, connected, oriented three-manifolds and positive cooriented contact structures. An abstract open book has a compact connected oriented page S with nonempty boundary and monodromy fixing a neighborhood of the boundary pointwise. Its page genus is minimized over **all** open books supporting the specified contact structure:

sg(Y, xi) = min {genus(S) : (S, phi) supports (Y, xi)}.

There is no bound on the number of boundary components in this definition. In particular, restricting to a fixed binding, connected binding, a prescribed Reeb vector field, or Milnor open books changes the optimization problem.

The two targets are:

- (a) existence of a pair (Y, xi) with sg(Y, xi) >= 2;
- (b) unboundedness of the set of support genera.

Part (b) implies part (a); the converse is not established here. The source is [K3], printed/PDF page 163, Problem 3.45, proposed and scribed by J. Baldwin. The page was checked both as extracted text and visually. The generic AIM workshop report is not used as the exact problem source.

### Current-literature correction

The July 2026 preprint [OS26, Theorem 1.1] establishes

sg(xi # eta) <= max(sg(xi), sg(eta)).

Consequently, iterated contact connected sums of genus-one examples do not produce support genus above one. This removes one suggestion in the April K3 text. It does not settle either question. The inspected arXiv record lists v1, submitted 2026-07-22, and no journal publication or later version. Its theorem and proof, including the polygonal construction, were inspected. This report imports that theorem rather than claiming to prove it anew.

The same preprint treats the existence question as unresolved. A targeted search on 2026-10-08 found no verified later resolution. This is a bounded literature assessment, not a proof of the absence of a resolution.

## 2. Approach I: fundamental groups, binding complexity, and boundary twists

### Candidate and attempted inference

Let S_g be a genus-g surface with one boundary component, g >= 1. Write delta for a curve parallel to that boundary and set

O(g,n) = (S_g, t_delta^n), n >= 1.

Let (Y(g,n), xi(g,n)) be the contact manifold it supports. The proposed inference was that the visible genus g is forced by the large rank of the underlying three-manifold. The computation below establishes a sharp statement with connected binding, and identifies exactly why it does not establish sg = g.

### Proposition 2.1: exact elementary invariants

For g,n >= 1:

1. H_1(Y(g,n); Z) is free of rank 2g.
2. The minimum page genus among supporting open books with connected binding is g.
3. The support norm, defined here by sn(xi) = min(-chi(S)), is 2g-1.
4. Every supporting page of genus h with b boundary components satisfies
   2h+b-1 >= 2g.
   Thus, if sg(xi(g,n)) <= 1, any genus-one supporting page has b >= 2g-1, and any planar one has b >= 2g+1.

**Proof.** Put a basepoint on the boundary and choose free generators a_1,b_1,...,a_g,b_g of pi_1(S_g). Write w for the product of their commutators. Depending on the convention for the oriented boundary loop, a right boundary twist acts on this based free group by conjugation by w or by w^(-1). The sign will have no effect on the following presentation. Van Kampen for the mapping torus, followed by filling the binding torus, kills the mapping-torus generator and gives

pi_1(Y(g,n)) = <a_1,b_1,...,a_g,b_g | [w^n,a_i]=[w^n,b_i]=1, 1<=i<=g>.

Indeed, the relations identify x with phi_*(x); the meridian of the attached solid torus is the circle in the mapping-torus direction, not the page-boundary longitude. Every displayed relator is a commutator. Abelianization therefore introduces no relation among the 2g generators. This proves (1).

For an arbitrary open book with page S of type (h,b), pi_1 of the filled manifold is a quotient of pi_1(S): kill the mapping-torus generator using any one binding torus; other binding tori can add relations but cannot add generators. Equivalently, the usual two-page Heegaard splitting has genus 2h+b-1. It follows that

b_1(Y) <= 2h+b-1.

For b=1 this gives h >= g. The displayed candidate has genus g and connected binding, proving (2). Also -chi(S)=2h+b-2 >= 2g-1, while O(g,n) realizes equality. This proves (3) and (4). QED.

**Caution on the homology calculation.** The formula H_1(Y)=coker(phi_*-I) on absolute page homology is valid in the connected-binding calculation above. It is not a formula for all multi-boundary open books: relative arcs contribute extra relations. An annular n-fold twist is a control example; its filled manifold has H_1 = Z/n for nonzero n, although the action on the annulus's absolute H_1 is the identity.

### Consequences and the precise gap

If s=sg(xi(g,n)) and beta is its binding number at minimal genus, then

beta >= 2g+1-2s.

In particular, support norm can grow linearly while a genus-one possibility survives by increasing binding number. The integer constraints already permit h=1,b=2g-1 for g>=2; they do not assert that such a supporting open book exists. A page with h=g,b=1 and a putative page with h=1,b=2g-1 have exactly the same Euler characteristic.

There is also no upper bound on the number of boundary components of *all* supporting books obtained from this argument. A positive stabilization along an arc with both endpoints on the same boundary component changes (h,b) to (h,b+1) and preserves the contact structure. A bound on the minimal binding number would be a different, substantive theorem.

This approach proves exact connected-binding genus and exact norm, but supplies no obstruction to the multi-binding alternatives. Large first Betti number, large fundamental-group rank, or large support norm must not be relabeled as large support genus.

## 3. Approach II: horizontal pages and changing the Reeb field

### Candidate and geometry

Consider the n=1 member, realized as the circle bundle pi:Y_g -> Sigma_g with Euler number -1 and its canonical Boothby-Wang contact structure xi_g. A connection contact form alpha has Reeb field R equal to the circle-action generator. The section over a once-punctured base gives O(g,1); this identification is described in [M12, Section 3].

A tempting strategy is to use the projection to the base to force the genus of every supporting page. The following argument works with an additional, very specific hypothesis.

### Proposition 3.1: the horizontal lower bound

Suppose an ordinary open book has b binding components that are fibers of pi and its page interiors are positively transverse to the fixed circle fibers. Assume pi on a page interior is the resulting finite covering of the base with those b points removed. If the covering has degree d >= 1 and the page genus is h, then

2-2h-b = d(2-2g-b),

h = 1+d(g-1)+(d-1)b/2,

h-g = (d-1)(g-1+b/2) >= 0.

**Proof.** Remove small binding neighborhoods and corresponding disks in the base. The page is a compact surface with b boundary circles. Its projection is an unbranched degree-d cover of a genus-g surface with b boundary circles. Euler characteristic multiplies by d under a finite covering. Substitution of chi=2-2 genus-number of boundary circles gives the three identities. Since g>=1, b>=1, d>=1, the last expression is nonnegative. QED.

The standard section has d=1 and genus g, so it realizes the minimum in this restricted horizontal class. The displayed numerical conditions are necessary only; the report does not assert the existence of covers or open books for every triple (g,b,d) satisfying parity and Euler-characteristic conditions.

### Why a supporting open book need not lie in that class

The contact structure specifies a conformal class of positive contact forms, not this single Reeb field. If f:Y_g -> R_{>0} and beta=f alpha, write

R_beta = R_alpha/f + Z, with Z in xi_g.

For v in xi_g, the equation d beta(R_beta,v)=0 yields

d alpha(Z,v) = df(v)/f^2.

The restriction of d alpha to xi_g is nondegenerate. Hence a function with df|xi_g nonzero produces Z nonzero. Such a Reeb field is not tangent to the original circle fibers. Giroux support can therefore select an adapted Reeb field without preserving the Boothby-Wang projection. This calculation prevents an unjustified transfer of Proposition 3.1 to all supporting open books.

**Remaining step.** One would need a theorem putting a genus-minimizing supporting open book into the fixed horizontal class, or a genus estimate valid without that hypothesis. Neither is proved or imported here. The restricted result is consistent with sg(xi_g)=1 for arbitrarily large g.

## 4. Approach III: formal plane fields and an explicit characteristic-number test

The next strategy was to detect increasing genus through Euler classes or the three-dimensional plane-field invariant. On the same circle-bundle candidates, both can be computed explicitly.

### Proposition 4.1: characteristic numbers of the candidate

For the canonical structure xi_g on the Euler-number -1 bundle, c_1(xi_g)=0. With the convention d_3(xi_std on S^3)=-1/2,

d_3(xi_g) = -g^2+2g-1/2.

**Proof.** The horizontal oriented two-plane bundle is isomorphic to pi^*T Sigma_g. In the Gysin sequence, cup product with the Euler class -1 maps H^0(Sigma_g;Z) onto H^2(Sigma_g;Z). Thus pi^*:H^2(Sigma_g;Z)->H^2(Y_g;Z) is zero, proving c_1(xi_g)=0.

Let X_g be the oriented disk bundle of degree -1. It is the standard symplectic filling of the Boothby-Wang boundary; choose an almost complex structure compatible with the symplectic form and the boundary contact structure. Its zero section has tangent Chern number 2-2g and normal Chern number -1. Therefore c_1(X_g) evaluates to 1-2g on the generator of H_2(X_g). Its intersection matrix is [-1], so

c_1(X_g)^2 = -(1-2g)^2, chi(X_g)=2-2g, sigma(X_g)=-1.

Using the almost-complex-boundary formula

d_3 = (c_1^2-2chi-3sigma)/4

now gives the assertion. The rational square is well-defined because the boundary first Chern class is torsion (in fact zero). The formula's normalization agrees at g=0 with -1/2. QED.

The characteristic-number formula is an imported standard plane-field formula; see [EO08, Section 3.3] for the normalization and contact-surgery version. The calculation is not a claim that X_g is Stein: its positive-genus symplectic zero section is important, and the filling used here is symplectic.

### What the computation can and cannot prove

Eliashberg's realization theorem [E89] gives an overtwisted representative in each homotopy class of positive oriented plane fields; Etnyre's theorem [E04] makes each such representative planar. Consequently a numerical lower bound that depends only on the homotopy class of the plane field and is required to hold for *all* contact structures cannot be positive anywhere: evaluate it on the overtwisted representative of the same class. This includes c_1 and d_3, even taken together. Restrictions to fillable or tight structures would change that logical statement and require additional input.

There is a valid, but only genus-zero, conclusion for these candidates. [GGP20, Theorem 1.7] excludes planarity when a symplectic filling contains a positive-genus symplectic surface. The zero section of X_g supplies that surface for g>=1. Thus

1 <= sg(xi_g) <= g.

In particular sg(xi_1)=1; no conclusion sg(xi_g)>1 for g>=2 follows. The rank-one intersection form [-1] does not become more restrictive as g grows. The varying d_3 calculation does not repair that gap.

## 5. Approach IV: Floer U-depth and the missing genus-one inequality

The Floer strategy was to turn increasingly deep U-divisibility of a contact class into increasing support genus. The available planar obstruction [OSS05, Theorem 1.2] says that for a planar structure its class c^+ belongs to U^d HF^+(-Y) for every d>=0. Its contrapositive can exclude genus zero. It supplies no stated numerical inequality for genus one.

Here is an exact algebraic diagnostic of the attempted extrapolation. Work over a field F and let

T^+ = F[U,U^{-1}]/U F[U],

M_m = T^+ direct-sum F[U]/(U^{m+1}),

c_m = (0,U^m), m>=0.

Then U c_m=0, c_m is nonzero, and

max {d>=0 : c_m is in U^d M_m} = m.

Indeed, U^{m-d} maps to U^m for 0<=d<=m. For d>=m+1 the finite summand has zero image, while the first summand cannot contribute to the nonzero second coordinate. By contrast the element (1,0) is killed by U and lies in every U^d M_m, since U^{-d} maps to 1 in the tower.

These computations separate three notions often conflated in a putative argument: being killed by U; having finite U-depth; and having infinite U-depth. Arbitrarily large finite depth is fully compatible with the elementary module axioms. This is an algebraic test, not a claim that every M_m with this distinguished class is realized by the present contact candidates.

For the torsion-c_1 candidate in Section 4, the usual absolute grading of a nonzero contact element would be

grade(c^+(xi_g)) = -d_3(xi_g)-1/2 = g^2-2g.

Knowing this grade does not locate the class in an infinite U-tower versus a finite summand. This investigation does not compute HF^+(-Y_g), identify the actual contact class, or assert a U-depth for it.

[K14] gives genuine contact U-depth calculations and uses them to distinguish Stein-cobordism behavior; its discussion explicitly separates that invariant from a higher-genus obstruction. Those results do not supply the needed implication here.

**Remaining step.** A theorem restricting the *actual* Floer module together with its contact class for every genus-one supporting open book, uniformly over the number of binding components, is required. Inserting a guessed relation such as sg >= 1+depth or sg >= -sigma is not justified by the planar theorem. The module test diagnoses the missing premise rather than disproving every possible refined Floer approach.

## 6. Approach V: positive factorizations, capping vectors, and filling growth

This route aims to rule out genus one using unbounded Euler characteristics of Stein fillings. It yields a concrete fixed-open-book bound. The general low-genus finiteness principle is already [BMV17, Proposition 1]; the explicit weighted constraint system below records exactly what is controlled and what is not.

Let S be a genus-one surface with b>=1 labeled boundary components. Mapping classes fix each boundary pointwise. For every i, cap all boundaries except i to obtain a homomorphism

q_i: Mod(S) -> Mod(S_{1,1}).

Use the abelianization e:Mod(S_{1,1})->Z normalized by e(t_a)=1 for a nonseparating curve. The two-chain relation t_boundary=(t_a t_b)^6 gives e(t_boundary)=12. Set e_i=e(q_i(phi)) and E=sum_i e_i.

An allowable positive factorization uses only homologically nonzero simple closed curves. Let N be its number of nonseparating factors. Every separating allowable curve cuts off a genus-zero side containing a nonempty proper subset A of the b boundary labels. Let s_A count factors of that topological boundary type. If b=1 there are no such subsets and no allowable separating curves.

### Proposition 6.1: capping constraints

Every allowable positive factorization satisfies, for each i,

e_i = N + 12 sum_{A containing i} s_A,

where N and all s_A are nonnegative integers and A ranges over nonempty proper subsets. Its length is

ell = N+sum_A s_A.

In particular:

- all e_i are nonnegative and congruent to N modulo 12;
- N <= min_i e_i;
- E = bN+12 sum_A |A|s_A;
- ell <= E/min(b,12).

**Proof.** A nonseparating curve remains nonseparating after each capping and contributes 1 to each e_i. A separating curve of type A becomes boundary-parallel if i is in A, contributing 12, and bounds a disk if i is outside A, contributing zero. Allowability excludes A empty and A equal to all boundary components: in the latter case the curve represents the sum of all boundary classes, which is zero. Summing factor contributions proves the first identity, and the rest follow. Each nonseparating factor contributes b to E; each separating one contributes at least 12. QED.

A sharper necessary upper bound is obtained by maximizing

N+(E-bN)/12

over the finite set of integers 0<=N<=min e_i with N congruent to every e_i modulo 12. If that set is empty, no allowable positive factorization exists. This is only an upper bound: the linear constraints forget geometric intersections, ordering, and the mapping-class-group product equation.

For example, when b>=2, for a boundary multitwist with each exponent one, e_i=12 for all i. The constraints permit N=0 or N=12. In the latter case no separating factors occur and ell=12. In the former case the subsets appearing with positive multiplicity form a partition of the boundary labels into nonempty proper blocks. The constraint system's feasibility does not establish an actual factorization with each such partition.

### Corollary 6.2: the exact filling bound covered by this argument

Suppose a compact four-manifold X is the total space of an allowable Lefschetz fibration over the disk with this *fixed* boundary open book (S,phi). Its handle description has one 0-handle, b+1 1-handles, and ell 2-handles. Hence

chi(X)=ell-b <= E/min(b,12)-b.

Also b_2(X)<=ell. Thus a fixed genus-one open book cannot be filled by such Lefschetz fibrations with unbounded Euler characteristic.

### The attempted jump and why it remains a gap

A Stein filling yields an allowable Lefschetz fibration with some supporting open book, but that book need not be the chosen minimal-genus book. Stabilization equivalence of supporting books does not identify the sets of their positive factorizations or their fillings. In particular, the argument above does not imply a uniform bound for all Stein fillings of an arbitrary contact structure of support genus one.

Precisely, if a particular genus-one book O had the extra property that **every** Stein filling of its boundary were realized by an allowable Lefschetz fibration with exactly O, then its contact boundary could not have Stein fillings with unbounded Euler characteristic. This conditional statement follows immediately from Corollary 6.2. The required universal genus-one filling property has not been proved here and is not imported. [BVM18] explains the corresponding distinction; its examples also show that infinitely many Stein fillings need not mean unbounded size.

This is the surviving concrete route to the original target: a sufficiently strong genus-one filling theorem, or a substitute uniform bound invariant under changes of supporting book, would turn suitable unbounded-filling families into examples for part (a). None is established in this report.

## 7. Conclusion and nonclaims

The completed calculations establish exact invariants for a standard boundary-twist family, a horizontal-page restriction, a characteristic-number formula, an algebraic diagnosis of a Floer extrapolation, and quantitative fixed-genus-one-book factorization bounds. Several recover familiar mechanisms; they are not advertised as new discoveries.

The outstanding quantifiers are essential:

- every supporting open book, rather than every one with connected binding;
- every adapted Reeb field, rather than the circle-action field;
- contact geometry, rather than the formal homotopy class alone;
- a genuine genus-one Floer restriction, rather than a planar criterion;
- every filling, rather than the fillings of one chosen open book.

No genus-two support example, no unbounded-support-genus family, and no universal genus-one upper bound is proved. The appropriate outcome for both parts of K3 Problem 3.45 is **unresolved after five distinct approaches**. The July 2026 connected-sum theorem is a relevant literature correction, not a solution or an extra research turn.

## References

- [K3] R. Inanc Baykur, R. C. Kirby, D. Ruberman (eds.), *K3: A New Problem List in Low-Dimensional Topology*, Mathematical Surveys and Monographs 295, AMS, 2026, Problem 3.45, p.163. [Author-hosted preliminary version](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf).
- [OS26] M. Orbegozo Rodriguez, E. Stenhede, *The support genus does not increase under contact connected sum*, arXiv:2607.19892v1, 2026. [Primary record](https://arxiv.org/abs/2607.19892).
- [EO08] J. B. Etnyre, B. Ozbagci, *Invariants of contact structures from open books*, Trans. Amer. Math. Soc. 360 (2008), 3133-3151. [DOI](https://doi.org/10.1090/S0002-9947-08-04459-0); [preprint](https://arxiv.org/abs/math/0605441).
- [M12] P. Massot, *Two remarks on the support genus question*, October 2012, unpublished manuscript. [Author PDF](https://www.imo.universite-paris-saclay.fr/~patrick.massot/files/exposition/genus.pdf).
- [E89] Y. Eliashberg, *Classification of overtwisted contact structures on 3-manifolds*, Invent. Math. 98 (1989), 623-637. [Publisher](https://doi.org/10.1007/BF01393840).
- [E04] J. B. Etnyre, *Planar open book decompositions and contact structures*, IMRN 2004, 4255-4267. [Author PDF](https://etnyre.math.gatech.edu/preprints/papers/planar.pdf); [arXiv](https://arxiv.org/abs/math/0404267).
- [GGP20] P. Ghiggini, M. Golla, O. Plamenevskaya, *Surface singularities and planar contact structures*, Ann. Inst. Fourier 70 (2020), 1791-1823. [arXiv:1708.04108v4](https://arxiv.org/abs/1708.04108).
- [OSS05] P. Ozsvath, A. Stipsicz, Z. Szabo, *Planar open books and Floer homology*, IMRN 2005, 3385-3401. [DOI](https://doi.org/10.1155/IMRN.2005.3385); [arXiv](https://arxiv.org/abs/math/0504403).
- [K14] C. Karakurt, *Contact structures on plumbed 3-manifolds*, Kyoto J. Math. 54 (2014), 271-294. [arXiv](https://arxiv.org/abs/0910.3965); [DOI](https://doi.org/10.1215/21562261-2642395).
- [BMV17] R. I. Baykur, N. Monden, J. Van Horn-Morris, *Positive factorizations of mapping classes*, Algebr. Geom. Topol. 17 (2017), 1527-1555. [Publisher PDF](https://msp.org/agt/2017/17-3/agt-v17-n3-p06-s.pdf); [arXiv](https://arxiv.org/abs/1412.0352).
- [BVM18] R. I. Baykur, J. Van Horn-Morris, *Fillings of genus-1 open books and 4-braids*, IMRN 2018, 1329-1346. [DOI](https://doi.org/10.1093/imrn/rnw281); [arXiv](https://arxiv.org/abs/1604.02945).
