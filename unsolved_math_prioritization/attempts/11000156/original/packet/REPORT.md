# Boundary-twist factorizations: a scope-sensitive partial result

Problem 11000156 / AMR-109-0156, rank 1013. Research date: 2026-10-08.

## Result

The geometrically intended **untwisted** version has a published negative answer, credited to R. Inanc Baykur. The larger equivalence relation obtained by imposing only the printed commutation condition is **not resolved here**. Five approaches below leave a specific orientation-reversing gap. No new solution, novelty, human peer review, or formal certification is claimed.

## Recovered mathematical target

Use the boundary-pointwise mapping class group of a compact connected oriented surface Sigma_(g,n). Fix g and n, and let Delta be the product of one right-handed Dehn twist about each of its n boundary components. The question concerns two finite ordered positive factorizations F=(t_c1,...,t_cr) and G=(t_d1,...,t_ds) of this same Delta, with every c_i and d_j nonseparating. Their closed Lefschetz-fibration total spaces over S^2 are required to have equal Euler characteristic and signature. Must F and G be joined by the indicated moves?

The boundary components encode distinguished sections of square -1; n is not a number of punctures. The surrounding fibration correspondence assumes 2-2g-n<0. The question does not add a g>=3 hypothesis or assert a minimum number of boundary components. The pencil/section situation uses n>=1. Empty-boundary specializations should be labeled separately. Equality of Euler characteristic forces r=s, since chi=4-4g+r. Delta is a multitwist when n>1, not just one of its factors. [A06, book PDF pp. 139, 144-145; displayed page 138 for the question.]

We use the right Hurwitz convention

    (...,x,y,...) -> (...,y,y^-1 x y,...).

For a consecutive block B=(x_k,...,x_l) with product P, partial conjugation by t_a replaces B with (t_a x_k t_a^-1,...,t_a x_l t_a^-1), provided [P,t_a]=1. Inverses of these moves are included. Neither genus changes nor added factors are permitted. Each intermediate factor remains a positive twist on a nonseparating curve. Whole-word conjugations by twists are available because Delta is central; the operation permits k=1,l=r. They include ordinary global conjugation when the conjugator is written as a product of twists.

Three scopes must remain distinct:

1. U: P preserves the isotopy class of the **oriented** curve a. Its suspension is a torus.
2. T: only [P,t_a]=1 is required. This also allows P to reverse a, giving a Klein-bottle suspension.
3. C: conjugate B by any mapping class h centralizing P. This can exceed conjugations by commuting individual twists.

Thus U is contained in T, which is contained in C. Containment of move sets alone does not establish strict containment of the resulting orbit relations.

## Published result and its precise limit

Baykur's Theorem B supplies, for each N,n>=1, a sufficiently large genus and N factorizations of Delta with exclusively nonseparating factors and matching chi and sigma, pairwise inequivalent under Hurwitz moves and U-moves. In particular N=2 disproves the universal U-question. His proof uses exceptional-sphere intersection data. Remark 4.1 explicitly does not extend this argument to orientation-reversing T-moves; Remark 4.2 also warns against replacing centralizing mapping classes by commuting individual twists. [B16, Theorem B, Lemma 3.2, Remarks 4.1-4.2.]

This is a prior theorem, not an original counterexample. Its quantifiers are sufficient for a universal negative answer; this report does not claim an explicit smallest genus or examples in every genus above a threshold. The 2018/2019 rational/ruled-surface continuation uses differing numbers of reducible fibers, so it cannot supply the all-nonseparating pair needed here. [B19, Theorem 1 and its introduction.]

## Five substantive approaches

Source recovery and verification are not counted as proof turns. These are distinct attempts to settle the remaining T-question; none succeeds in doing so.

### Turn 1: extend the exceptional-sphere obstruction across the twisted move

The candidate is the multiset of fiber intersections of exceptional classes, or a parity reduction of that multiset. If every exceptional sphere could be moved off the surgery locus while preserving its homology class, surgery would leave its intersection with an unaffected regular fiber unchanged. Applying the inverse surgery would give equality of the multisets and therefore the desired obstruction.

The argument is valid conditional on that disjointness statement, but no such statement is available for the Klein-bottle suspension. Algebraic intersection already shows what is needed: a nonzero mod-2 intersection of an exceptional class with the Klein bottle prevents disjoint representatives. Passing to the orientable double cover does not remove that obstruction in the original manifold. In particular, an upstairs isotopy need not descend equivariantly. Replacing the multiset by parity loses its distinguishing power unless one first proves a surgery transformation rule. This route stops at a missing preservation theorem, rather than at a missing arithmetic calculation.

As a check on the numerical mechanism only, the script reproduces the recurrence for partial doubling and checks the kernel direction (-1,3,-2): both its sum and its scalar product with (4,2,1) vanish. The changed last exceptional-data entry shows why there is information beyond chi and sigma. This recurrence audit does not repair the geometric gap. [B16, Sections 3-4.]

### Turn 2: replace orientation-reversing moves by untwisted ones

One might hope that a positive block commuting with a twist automatically preserves its curve's orientation. That hope fails even inside a genuine positive boundary-twist factorization.

Let a,b intersect once on a one-holed torus, and write a,b also for their positive twists. The braid relation is aba=bab. Put z=(ab)^3=(aba)^2. Conjugation by aba interchanges a and b, so z is central. The two-chain relation gives z^2=(ab)^6=Delta. Thus z is a positive six-factor block of a positive factorization of Delta and commutes with a.

On integral homology take

    A = [[1,1],[0,1]], B = [[1,0],[-1,1]].

Direct multiplication gives (AB)^3=-I. Therefore z reverses the orientation of a. Curve classes on the one-holed torus are primitive homology slopes up to sign; z fixes the underlying unoriented curve. This exhibits an actual T-admissible block that is not U-admissible. It is not a counterexample to the main question: conjugating this particular block by a is redundant under Hurwitz moves, since a is among its factors and z is central in their group.

A second reduction would factor any centralizing h into twists each centralizing the block. Already in SL(2,Z), a matrix M=[[p,q],[r,s]] commutes with A only when r=0 and s=p; det M=1 then forces p=s=+1 or -1. Hence C(A)={+/- A^k:k in Z}. Twists on the same torus commuting with a project to powers of A, whereas z projects to -I. A product of the former cannot produce the latter. This defeats a centralizer-generation shortcut; it does not prove inequivalence of any pair of boundary factorizations. [Two-chain relation: A06 book PDF p. 132, relation (3); the obstruction is consistent with B16 Remark 4.2.]

### Turn 3: use stable classification and cancel the stabilizer

Auroux's stable classification identifies two fibrations after enough fiber sums with a universal fibration, under matching chi, sigma, section square, and reducible-fiber counts. Our nonseparating hypothesis matches the last condition. After retaining a single distinguished section, the theorem gives a stable comparison. It does not automatically retain every marked section when n>1. [A05, Theorem 2.]

Even for n=1, the algebraic conclusion has form F U^k ~ G U^k, with new factors present. The desired conclusion is F ~ G using a fixed-length relation. A cancellation theorem for the positive-factorization quotient would suffice, but it is not supplied by stable classification. Such cancellation is not a formal property of monoids: in the union monoid of subsets of {1,2}, distinct {1} and {2} become equal after adding {1,2}. This example is only a logical warning, not a claim about the Lefschetz-factorization monoid.

The exact gap is injectivity of stabilization on the relevant T-orbits (and, for n>1, control of the extra marked sections). Applying stable classification again does not address either gap.

### Turn 4: construct a quadratic-refinement obstruction

Let V be a symplectic vector space over F_2 with form omega. A quadratic refinement obeys q(x+y)=q(x)+q(y)+omega(x,y). For the transvection T_a(x)=x+omega(x,a)a, expansion yields

    q(T_a x)=q(x)+omega(x,a)(q(a)+1).

Thus q is preserved by T_a exactly when q(a)=1 for nonzero a. A proposed invariant asking for one quadratic refinement with value 1 on every vanishing vector needs to survive every admissible partial conjugation. Commutation of a block product with T_a by itself imposes no q(a)=1 requirement.

There is a concrete quotient-level failure. In dimension four with symplectic basis e1,f1,e2,f2, start with paired transvections on f1, then on each of the four basis vectors. Every pair squares to identity over F_2; the full word has length ten and product I. There is exactly one q taking value 1 on all its vanishing vectors, namely

    q(x1,y1,x2,y2)=x1*y1+x2*y2+x1+y1+x2+y2.

Take a=e1+e2, for which q(a)=0. Conjugating the first pair by T_a is admissible in Sp(4,F_2), and changes f1 to f1+e1+e2, on which q is 0. The unchanged basis vectors still force the same q, so no common refinement exists afterward.

This eliminates the naive quotient invariant. It is deliberately not promoted to an actual Lefschetz example: squares of positive Dehn twists are not identity in the mapping class group, and the finite-word product condition does not prove a boundary-multitwist lift. The missing lift and signature control remain essential.

### Turn 5: finite symplectic-image orbit obstruction

In Sp(2,F_2)=S_3 the nonzero transvections are its three transpositions. Exhaustively checking the modest 3^6=729 ordered length-six words gives 243 with product I. Hurwitz moves alone split these into component sizes 1,1,1,240. Adding partial conjugations by transpositions commuting with the selected block product connects all 243.

The collapse has a transparent mechanism. From (s,s,s,s,s,s), conjugate the first pair by a different transposition t. Its product s^2=I commutes with t, and the result is (u,u,s,s,s,s), where u=tst differs from s. The generated subgroup changes from order two to S_3. Therefore generated-subgroup order is not an invariant of this finite move system.

The script independently checks product preservation for every generated edge and computes the components. This is a small quotient experiment, not an exhaustive search in a mapping class group. It supplies neither a positive proof nor a lifted counterexample: reduction can identify inequivalent geometric factorizations, and no Euler/signature data is encoded. The search offers no residual finite obstruction at this size.

## Remaining gap and accepted status

A complete negative result for the commutation-only T-reading needs a pair of genuine positive nonseparating factorizations of the same Delta with matching chi and sigma, together with an invariant valid also when a block reverses the conjugating curve. A positive result would require a constructive T-move connectivity theorem for all such pairs. Neither is established here. The general-centralizer C-reading would require still more.

Accepted status: unsolved for the broader literal algebraic reading; credited prior negative resolution for the untwisted geometric reading; five approaches exhausted. No claim that the broader question is globally open as of today follows merely from this bounded literature search.

## Reproducibility limits

The packet contains authored analysis, small exact algebra/combinatorial checks, and public bibliographic/hash metadata. It contains no copied PDFs, extracts, or dataset records. The checker verifies those finite statements and packet integrity; it does not verify Seiberg-Witten theory, pencil existence, surgery theorems, general mapping-class equality, or the main problem. External manifest and bootstrap hashes identify one frozen packet. They are integrity pins, not signatures or a proof certificate.

## Sources

- A06: Denis Auroux, Mapping class group factorizations and symplectic 4-manifolds: some open problems, 2006. https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf ; author chapter https://people.math.harvard.edu/~auroux/papers/mcg-farb.pdf . Book Question 2.5 is numbered Question 5 in the author chapter.
- B16: R. Inanc Baykur, Inequivalent Lefschetz fibrations and surgery equivalence of symplectic 4-manifolds, J. Symplectic Geometry 14 (2016), 671-686. https://arxiv.org/abs/1408.4869 ; DOI https://doi.org/10.4310/JSG.2016.v14.n3.a2 . Inspected arXiv v3 dated 2015-10-14, including the corrected Theorem B.
- A05: Denis Auroux, A stable classification of Lefschetz fibrations, Geometry & Topology 9 (2005), 203-217. https://arxiv.org/abs/math/0412120 ; https://doi.org/10.2140/gt.2005.9.203 .
- B19: R. Inanc Baykur, Inequivalent Lefschetz fibrations on rational and ruled surfaces, 2019. https://arxiv.org/abs/1806.00375 ; https://doi.org/10.1090/pspum/102/02 .
