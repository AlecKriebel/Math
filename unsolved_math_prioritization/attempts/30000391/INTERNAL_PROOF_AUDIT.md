# Internal audit of Farleys finite rank matching argument

Problem 30000391; audit date 2026-10-10 UTC.

## Verdict and boundary

The internal deductions in Farley's Lemma 1, Lemma 9, Proposition 10, and Theorem 11 check out relative to the geometric-lattice and transversal results cited in that paper. No unresolved internal gap was found. The audit below records the mathematical checks that matter, including finite generation at the limit step and the precise distinction between atoms below an element and hyperplanes above it.

This is not a recursive audit of all cited literature. The published theorem suffices for the applicability certificate regardless of how much of its proof is reproduced here. All general-theorem credit belongs to Farley and the earlier authors he cites; the checks below are verification, not a novelty claim.

Source: J. D. Farley, Australas. J. Combin. 82(3) (2022), 228-236, https://ajc.maths.uq.edu.au/pdf/82/ajc_v82_p228.pdf . Printed page numbers are used throughout.

## Notation and accepted dependencies

Write A for the atoms of a finite-rank geometric lattice L and H for its coatoms. To avoid the overbar/underbar ambiguity of PDF text extraction, put

    A_x = {a in A : a<=x},
    H_x = {h in H : x<=h}.

The audit accepts the standard rank properties of finite-rank geometric lattices: strict order increases rank; adjoining an atom not already below an element increases rank by one; intervals are geometric; every element is a finite join of atoms and a finite meet of coatoms; and rank is submodular.

Farley's numbered external inputs are:

- Theorem 2: a kappa-obstruction has deletion deficiency kappa.
- Theorem 3: a society with no matching covering its first side contains an obstruction.
- Theorem 4: the finite geometric-lattice matching theorem of Greene.
- Theorem 5: Björner's rank-three theorem and his cardinality-below-aleph_omega theorem.
- Lemma 6(a): if an atom a is not below a coatom h, then |A_h|<=|H_a|.
- Lemma 6(b): for an infinite finite-rank geometric lattice, its atoms, its coatoms, and its whole underlying set have equal cardinality.
- Theorem 7: Björner's regular-cardinality criterion when every rank-two lower interval has smaller cardinality.
- Theorem 8: the Milner-Shelah matching criterion, cited through Tverberg, comparing each incident second-side vertex degree with the first-side degree.

The first two inputs and their compatibility with Farley's obstruction definitions were checked directly against Aharoni, Nash-Williams and Shelah, *A General Criterion for the Existence of Transversals*, Proc. London Math. Soc. (3) 47 (1983), 43-68, https://doi.org/10.1112/plms/s3-47.1.43 ; author archive PDF https://shelah.logic.at/files/95295/194.pdf . The relevant statements are Section 4's obstruction definition, Lemma 4.2, Lemma 4.3, Corollary 4.9a and Theorem 5.1. Their complete 26-page proof was not independently re-proved. The other imported results were read as stated and cited in Farley; their original proof sources were not all retrieved.

## Modular complements and finite restrictions

In Lemma 1, choose a chain x=c_0<c_1<...<c_k=b of covers in an interval [a,b]. For each i, choose an atom u_i below c_i but not below c_(i-1). The cover property gives c_i=c_(i-1) join u_i. Put y=a join u_1 join ... join u_k. Then x join y=b and r(y)<=r(a)+k. Rank submodularity and x meet y>=a imply r(y)>=r(b)+r(a)-r(x)=r(a)+k. Equality follows, and the same inequality forces x meet y=a. Thus the rank equality that is compressed in the printed proof is justified.

For Lemma 9, let B be a subset of A and let L(B) be the elements of L that are finite joins of members of B, including the empty join. An arbitrary join of such elements is still a finite join from B: successive strict increases in a join can occur at most r(L) times. Thus L(B) is complete, with its own meet operation, and is not being assumed to be an ambient sublattice.

A cover u<v in L(B) is obtained by adjoining one atom b from a finite B-presentation of v. Since u<v is a cover, u join b=v. Semimodularity of L then makes this an ambient cover too. This proves cover preservation, and the same two-atom argument proves semimodularity inside L(B). Its atoms are precisely B and its rank equals the ambient rank of join B. When join B=1, its coatoms are ambient coatoms. For infinite B its cardinality equals |B|; for finite B it is finite. These facts justify all uses of the restriction in Proposition 10.

## Singular cardinal step

Let lambda be singular and assume the matching theorem for every smaller-cardinality geometric lattice of finite rank at least two. If L of size lambda were a counterexample, the obstruction theorem supplies a saturated obstruction Pi=(M,W,K). Its obstruction parameter kappa is positive and either finite or regular. Since its deficiency is kappa and |M|<=lambda, one has kappa<=lambda. Singularity of lambda gives kappa<lambda.

There is a set D contained in M of size kappa and an injective incident map E from M\D to W. Choose a finite set R of atoms spanning 1. Define

    B_0 = D union R,
    B_(n+1) = B_n union E^(-1)[H(L(B_n))],
    B = union_(n<omega) B_n.

Every B_n contains R, so its restriction has full rank and its coatoms are ambient coatoms. Set theta=max(kappa,aleph_0). Because lambda is singular, theta<lambda. Injectivity of E and the finite-join cardinality bound give |B_n|<=theta by induction, and hence |B|<=theta<lambda. This bound works even when cf(lambda)=omega: the construction is uniformly bounded by the single smaller cardinal theta, rather than merely taking an uncontrolled union of smaller cardinals.

The implicit limit justification is valid. If h is a coatom of L(B), h is a finite join of atoms of B. All those atoms occur in some B_n. Since R is also in B_n, the restriction has full rank and h is a coatom of L(B_n). Consequently

    E^(-1)[H(L(B))] subset B.

The smaller-cardinality hypothesis gives a matching G from B to H(L(B)). Retain E on M\B and use G on M intersect B. These two images are disjoint by the preceding inclusion. Saturation of Pi ensures that every hyperplane G(b), for b in M intersect B, lies in W: it is an ambient neighbor of a member of M. Thus the joined maps match all of M inside Pi, contradicting its positive deficiency. No surjectivity of E is needed.

This verifies Farley's new singular-cardinal step, including its key closure and saturation uses.

## Minimal counterexample reduction

Choose a counterexample of minimum cardinality and then minimum rank. The finite theorem, rank-three theorem and singular-cardinal step leave an infinite regular cardinal lambda and rank r>=4. The regular-cardinality criterion provides a rank-two element ell with |[0,ell]|=lambda; hence |A_ell|=lambda.

Every proper interval used below has cardinality at most lambda and smaller rank, so minimality gives it a matching. This is a lexicographic induction on cardinality and rank; the interval is not required to have strictly smaller cardinality.

If |H_p|=lambda for every atom p on ell, consider an atom q not on ell. Inside the rank-three lower interval [0,q join ell], Lemma 6(a) supplies at least lambda covers of q. Those covers are also atoms of [q,1], so that interval has cardinality lambda; Lemma 6(b) on [q,1] gives |H_q|=lambda. This spells out the passage behind the compressed equality on page 233. Every point then has lambda incident hyperplanes, while each hyperplane has at most lambda incident points. Theorem 8 supplies the matching, a contradiction.

It remains to consider q on ell with |H_q|<lambda.

## First geometric case

Suppose every rank-two flat through q other than ell has exactly two atoms. The map

    p -> p join q,   p not in A_ell,

is injective. A matching of [q,1] assigns distinct ambient hyperplanes to all covers of q. Use these assignments for the off-ell points, and assign q the hyperplane attached to ell. These choices all contain q and are pairwise distinct.

Choose an ambient hyperplane h_0 containing ell and a modular complement z of ell in [0,h_0]. Then r(z)=r-3 and ell meet z=0. For p on ell, put R_p=p join z. Its rank is r-2, so it is covered by h_0. If p and p' are distinct, their join is ell; consequently R_p=R_p' would force R_p=h_0, impossible by rank. Thus p -> R_p is injective.

For p different from q on ell, q is not below R_p and q join R_p=h_0. Therefore h_0 is the unique hyperplane containing both R_p and q. Since R_p is a meet of coatoms and has rank r-2, at least one hyperplane other than h_0 contains it. Choose such a hyperplane for p. It does not contain q, so it cannot collide with any previous assignment. Two such new assignments could coincide only if that hyperplane contained R_p join R_p'=ell join z=h_0, forcing it to be h_0, also impossible. Incidence and injectivity both follow.

## Second geometric case

Otherwise there is a line ell_1 through q, different from ell, containing two further distinct atoms p_1 and p_2. The two lines meet exactly in q. Choose a hyperplane h_0 containing ell and avoiding p_1; modular complementarity in [ell,1] gives one. It also avoids p_2, since containing q and p_2 would force it to contain ell_1 and hence p_1.

Let C be the elements covered by h_0. A matching of [0,h_0] gives an injection g:A_(h_0)->C with p<=g(p). Divide C according to the number of ambient hyperplanes above its members:

    C_2 = {c in C : |H_c|=2},
    C_3 = C\C_2.

Every c in C has rank r-2 and at least two coatom extensions, so membership in C_3 means at least three, not merely 'not equal to two'. The bars in the source count hyperplanes above c, not points below c.

Put y=join(A\A_(h_0)); then q<=p_1 join p_2<=y. For c in C_2 there is a unique hyperplane h different from h_0 above c. Every atom w outside h_0 makes w join c a hyperplane different from h_0, so w join c=h. Therefore y<=h and c=h_0 meet h. Distinct c's give distinct h's. It follows that

    |C_2| <= |H_y| <= |H_q| < lambda.

This one direction of the printed equivalence suffices. Its reverse is also valid: if c=h_0 meet h and y<=h, a third hyperplane h' above c would contain an atom a outside c. Such an atom cannot lie in h_0, since otherwise a join c=h_0=h'. Thus a<=y<=h, so a lies in h meet h'=c, a contradiction.

Because [0,h_0] contains [0,ell], it has cardinality lambda. Lemma 6(b) therefore gives |C|=lambda and then |C_3|=lambda. Choose an injection b from the off-h_0 atoms into C_3, and assign

    f(p)=p join b(p)   for p outside h_0.

This is an ambient hyperplane and is different from h_0. For each p on h_0, select a hyperplane above g(p), excluding h_0, and also excluding f(p') if b(p')=g(p) for an outside point p'. There is at most one such p' because b is injective, and when it exists g(p) is in C_3, so at least three hyperplanes are available.

The collision check uses a simple rank fact: if c,c' are distinct members of C, their join is h_0. Hence no hyperplane other than h_0 can contain both.

- Two off-h_0 images cannot coincide because their distinct b-values would force the common image to be h_0.
- Two on-h_0 images cannot coincide because their distinct g-values would force the same outcome.
- A mixed collision forces the g-value and the b-value to agree, and precisely that image was excluded when choosing the on-h_0 assignment.

All images contain their assigned point. This finishes the internal matching construction.

## Issues checked and limits retained

The restriction lattice need not preserve ambient meets; no argument above requires that. Finite generation ensures that no new coatom first appears only at the countable union stage. Saturation puts the replacement matching back inside the obstruction. Uniform cardinal bounds handle singular cofinality omega. The two possible rank-two configurations through q exhaust the cases because every line has at least two atoms. The least-cardinality/least-rank choice justifies both interval matchings. The main theorem is about covering the atom side; it does not claim a bijection or maximal chains through all points.

These checks reveal explanatory compressions, but no missing hypothesis or unfilled mathematical step in the inspected argument. Original proofs of the finite theorem, Björner's imported results and the Milner-Shelah/Tverberg criterion remain outside this audit's acceptance boundary.
