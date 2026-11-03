# Independent acceptance audit: Farb Problem 3.10

Problem ID: 11000031. Queue row: 1886. Audit date: 2026-10-21.

## Decision and exact scope

ACCEPT as already solved by Noel Brady, Matt Clay, and Pallavi Dani, *Morse theory and conjugacy classes of finite subgroups*, Geometriae Dedicata 135 (2008), 15–22. Workflow disposition: `already_solved`; workflow Turns: `1`. These are administrative workflow values, not a claim to one new mathematical proof attempt. No novelty is claimed.

Farb's original Problem 3.10 is existential: find a finitely presented subgroup of a closed orientable surface mapping class group with infinitely many conjugacy classes of finite subgroups, conjugating inside that subgroup. Genus 5 suffices. This audit does not settle minimal genus or assert the property for every genus. The corpus's appended isomorphism-problem discussion is not part of the requested problem.

The decisive published result is Brady–Clay–Dani Theorem 3.1: for g ≥ 3, a subgroup of type F_(g−3) with infinitely many involution conjugacy classes. Its finite-presentation consequence is g ≥ 5. [Author manuscript, p. 8](https://www.math.lsu.edu/~pdani/research/conj-classes.pdf). The author's [publication list](https://www.math.lsu.edu/~pdani/research.html) confirms the 2008 journal publication. The [original question](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf) is at PDF page 34, printed page 27.

## Independent logical audit of the construction

The following checks make explicit the mathematical steps between the credited inputs and the desired conclusion. They are verification, not a new result.

Set n = g−2 and G = product_(i=1)^n F(a_i,b_i). Let alpha simultaneously exchange a_i and b_i in every free factor, and let E = G semidirect <s>, where s has order 2 and acts by alpha. Define chi:E→Z by assigning 1 to every a_i and b_i, and 0 to s. The defining relations preserve these assignments, so chi is well-defined and surjective. Write K = ker(chi|G) and H = ker chi = K semidirect <s>.

### Embedding audit

The geometric input is the curve system and orientation-preserving involution of Figure 4 in the author manuscript. It supplies n pairs of curves, each pair intersecting twice and all cross-pair intersections zero; the involution exchanges the two members of every pair. The free-group assertion for each twist pair is the cited Dehn-twist theorem. These geometric and foundational claims remain credited inputs, rather than a claimed reconstruction of all surface-topology arguments here.

Given those inputs, the product embedding is not merely an inference from commutativity. Let G_i be the free rank-two subgroup from the i-th pair. Disjoint supports give commuting G_i and G_j for i ≠ j. If x_1 ... x_n = 1 with x_i in G_i, then x_i is the inverse of a product of elements commuting with every element of G_i. Thus x_i is central in G_i. A nonabelian free group has trivial center, so each x_i = 1. This proves that the multiplication map from the direct product is injective.

Conjugation of a positive Dehn twist by an orientation-preserving mapping class is the positive twist about the image curve. Therefore the geometric involution induces exactly alpha, with no inversion of generators. The product G is torsion-free. The geometric involution is nontrivial, since its conjugation exchanges distinct free generators; consequently its order is exactly 2, and it is not in G. The natural homomorphism E→Mod_g is therefore injective: a kernel element g s^epsilon with epsilon = 0 forces g = 1; epsilon = 1 would put s in G, impossible. Restricting an injective homomorphism to H remains injective. No quotient of H is being substituted, so torsion and internal conjugacy are preserved.

### Kernel finiteness audit

This is finiteness of a classifying-space skeleton, not finiteness of the kernel as a set. The needed credited product-kernel theorem says that K is of type F_(n−1). One way to see its applicability is the standard cubical model: the universal cover of the product of n two-petal roses is a product of n trees, and the sum-height map sends every positively oriented generator edge upward by 1. Its ascending and descending links are each the join of n two-point sets, hence S^(n−1), which is (n−2)-connected. The applicable Morse-theoretic finiteness theorem yields type F_(n−1). This use of the foundational Morse theorem is an explicit external dependency, not a full independent proof of that theorem.

K has index 2 in H. Type F_m is invariant under passage between a group and a finite-index subgroup, so H is of type F_(n−1) = F_(g−3). In particular g = 5 gives n = 3 and type F_2, which is equivalent to finite presentability. The argument needs no assertion that H is type F_infinity, no torsion-free claim for H, and no finite-dimensional classifying space. Torsion is compatible with a finite 2-skeleton.

### Independent algebraic check of conjugacy separation

Here one can avoid the CAT(0) fixed-point argument altogether. The automorphism exchanging the two basis letters of a rank-two free group has no nonidentity fixed element: a nonempty reduced word remains reduced after the letter exchange, and its first letter changes. Uniqueness of reduced words prevents equality. Applying this factor by factor gives Fix_G(alpha) = {1}.

An element g s^epsilon of E centralizes s exactly when alpha(g) = g. Thus C_E(s) = <s>, and chi vanishes on this centralizer.

Choose t = a_1, so chi(t) = 1. For every integer j let u_j = t^j s t^(−j). Each u_j lies in H and has order exactly 2. If h in H satisfied h u_j h^(−1) = u_k, then t^(−k) h t^j would centralize s. Its chi-value is j−k, whereas every element of C_E(s) has chi-value zero. Hence j = k. The u_j therefore represent infinitely many H-conjugacy classes. They are all conjugate in E, which is harmless: the problem asks about conjugacy in H, not in Mod_g or E.

For an involution u, the subgroup <u> has exactly one nonidentity element. Consequently h<u_j>h^(−1) = <u_k> if and only if h u_j h^(−1) = u_k. The preceding separation therefore proves infinitely many conjugacy classes of finite subgroups, already of order 2.

## Evidence boundaries and edition control

I read the locally recovered author manuscript's complete text, including Proposition 1.1, Example 1.2, Theorem 3.1, and references, and visually inspected the supplied page-8 rendering including Figure 4. I also checked the author-hosted manuscript and publication listing through web retrieval. Local PDF byte counts and SHA-256 hashes were recomputed and agree with the recovery metadata. The 233,371-byte author PDF is dated April 2, 2008. Its reference numbers [1], [13], [14] are local to that edition; they must not be silently carried over to the arXiv edition. No arXiv byte-equivalence claim is made.

The embedding's geometric realization and the foundational free-twist and Morse finiteness theorems remain source-dependent. The normal-form embedding completion, semidirect-product kernel checks, algebraic conjugacy separation, genus threshold, and involution-to-subgroup implication were independently checked above. This is not formal proof-assistant certification or external human peer review. No copied source document, dataset contents, or private coordination material is included in this authored acceptance report.

## Required metadata correction

The inspected recovery gate and metadata use `0/5`. For the requested standard workflow, supersede that administrative value with `already_solved/1`, while retaining the clear statement that there is no new proof or novelty claim. This audit itself does not edit the recovery files, QUEUE, repository branches, or remote publication state.
