# Independent acceptance audit: arithmetic K(pi,1)

Problem 30000779 / OWR-1586-003. Review date: 8 October 2026.

## 1. Verdict

**Accept as a credited prior resolution of the exact Oberwolfach conjecture.** Schmidt's marked-curve construction, with the explicit corrections under review, proves the odd-prime case. The same arithmetic construction over totally imaginary number fields satisfies the characteristic-two mildness criterion proved by Labute and Minac. No unresolved compatibility condition remains in this application.

Acceptance includes the explicit integral Kummer local-condition correction in the companion `LOCAL_CONDITION_CLARIFICATION.md`. This makes precise a correction already substantively present in the proposed ledger; it is not an additional arithmetic hypothesis. The other linked index corrections and the auxiliary-size choices are necessary parts of the accepted reconstruction.

The accepted statement is:

- For every number field k and every prime p such that p is odd or k is totally imaginary;
- for every finite set S of finite primes disjoint from S_p;
- and for every prescribed set D of finite primes of Dirichlet density one;
- there exists a finite A contained in D minus (S union S_p) such that Spec(O_k) minus (S union A) is a K(pi,1) for p.

There is no class-number or cyclotomic exclusion. S may be empty and need not be contained in D. A depends on k, p, S and D; no uniform size or norm bound is claimed.

The original report expressly adopts the convention p odd or k totally imaginary before stating its theorem and conjecture. A catalogue sentence omitting that convention is not disposed of literally by this finding. Repair that source-scope omission before attaching the accepted resolution to the catalogue statement. This review makes no theorem or residual-open-case classification for p=2 over real number fields.

This is an independent audit of prior proofs and their application, with **zero new substantive proof-search turns**. It makes no novelty claim. It does not claim to have reproved arithmetic duality, class field theory, profinite group cohomology, PBW or etale homotopy theory from their foundations.

## 2. Review basis and integrity

The review read the proposed `PRIOR_RESOLUTION_AUDIT.md`, `NESTED_DEPENDENCY_LEDGER.md`, `SOURCE_VERIFICATION_METADATA.json` and `AUTHORED_PACKET_MANIFEST.json`. Every declared authored-file byte count and SHA-256 matched a fresh computation. All ten locally available source PDFs also matched the byte counts and SHA-256 values in the source metadata. The input files have been preserved.

The argument was checked against Schmidt's English manuscript, its German v2 counterpart, the original OWR contribution, Schmidt's earlier homotopy comparison and cup criterion, Labute's elimination/reduction and relation-module arguments, Labute-Minac's mixed/quadratic algebra and mildness proofs, the cited NSW interfaces, and Milne's comparison/duality statements. The consequential Schmidt corrections were checked in rendered source pages, not just extracted text.

The source-verification file accompanying this report distinguishes fresh local integrity checks from historical retrieval claims. It does not claim a new network download for every PDF, a publisher-PDF byte comparison, or independent verification of every earlier retrieval timestamp. Milne was inspected through the public PDF reader; no local-file hash for that book is asserted.

## 3. Source statement and theorem substitution

OWR Report 30/2007, printed pp.1756-1758, first fixes the real-place convention. Its Theorem 1 assumes mu_p is not contained in k and p does not divide the ideal class number, and the following conjecture asks to remove those two assumptions. The subsequent restriction to norm-congruent primes belongs to later discussion, not to that conjecture. [Original OWR report](https://ems.press/content/serial-article-files/46117).

Schmidt's Theorem 1.1 permits pairwise disjoint finite S,T and a density-zero exceptional set M, with p odd. Set the final marking T to empty and set

    M = ((all finite primes minus D) union S_p) minus S.

This set is disjoint from S and has density zero. Since S is tame, it still contains every p-adic prime. The added primes, being outside S and M, lie in D and avoid p. The theorem's all-degree group/marked-etale comparison with empty marking is the ordinary etale comparison. Schmidt's earlier Proposition 2.1 identifies that comparison with the p-completed homotopy formulation used in the report. The arithmetic open is connected, regular and noetherian, as required. [Marked-curve manuscript](https://www.mathi.uni-heidelberg.de/~schmidt/papers/marked.pdf), Theorem 1.1; [rings-of-integers paper](https://arxiv.org/pdf/0705.3372v2), Proposition 2.1.

For p=2 the theorem is not applied by ignoring its odd-prime hypothesis. Sections 3-5 and the unmarking argument have the standing odd-prime-or-total-imaginarity convention. The construction in the roots-of-unity branch is checked below with the extra diagonal-cup check; the missing group-theoretic implication is then supplied by Labute-Minac Theorem 1.1.

## 4. Arithmetic preparation and corrected duality

The group V_B^T consists of classes locally pth powers at B and with valuations divisible by p outside T. The exact sequence in Lemma 3.5 makes V_empty^T finite-dimensional and identifies its unit and p-class-group contributions. Adding a local test only shrinks V. Thus no class-number hypothesis has been assumed before the obstruction is killed.

Theorem 3.6 follows from the global H^1 generator formula, the Euler characteristic and the degree-three boundary map. For a nonempty tame B whose norms are 1 modulo p, the formulas used here are

    h^1(X minus B,T) = 1 + |B| - delta + dim V_B^T - r - |T|,
    h^2(X minus B,T) = |B| - delta + dim V_B^T,
    h^i(X minus B,T) = 0 for i >= 3,

where r=r_1+r_2 and delta indicates mu_p contained in k. The finite extensions in the towers still satisfy the real-place convention.

I independently reconstructed Theorem 4.1 using the local unit subgroup C_v in Kummer cohomology. Its annihilator is the unramified F_p-character subgroup, including at p-adic v. This gives the quotient Q with full H^1 factors at T and ramified-quotient factors at Sigma minus (S union T). Poitou-Tate and excision give the same cokernel. Thus the first product in both printed sequences (I) and (II) must be T-indexed. The full calculation and the separate p-adic Kummer-denominator replacement are in the companion clarification. Both English and German sources contain the printed index errors.

Consequently V_B^T=0 gives injective H^2 localization. It is onto all local factors when delta=0. When delta=1, the global roots-of-unity term imposes one relation whose coefficient at every local factor is nonzero; omitting any one factor therefore makes localization an isomorphism. The construction must, and does, omit the p_0 coordinate.

Proposition 4.4 is legitimate for p=2 as well: localization of mu_p at the eligible split primes is injective by the prime-exponent Hasse principle. Their density is 1/[k(mu_p):k], strictly greater than its required 1/(p[k(mu_p):k]); finite and density-zero exclusions do not change it. The Grunwald-Wang exceptional case does not occur for exponent p. Finite-dimensionality reduces the local tests to finitely many primes.

## 5. Temporary markings and the delta=0 branch

Temporary markings remove the obstruction without constraining the final answer. In the delta=0 branch choose enough markings to kill the p-part of the marking-class group. Finitely many prime ideal classes suffice. If the enlarged marking meets the original exceptional set, remove that intersection from the exceptional set during the auxiliary argument: every new ramification prime is separately required to avoid the marking, so this does not admit a forbidden final prime.

Two disjoint finite applications of Proposition 4.4 give P such that V_(P minus {v})^T=0 for every v in P. Enlarge P using further eligible primes until

    dim H^1(X minus P,T) = |P| + 1 - r - |T| >= 2.

Deletion-vanishing persists. Every old inertia line is nonzero by the H^1 dimension difference after deleting its prime. The displayed size condition is genuinely useful: a Frobenius outside that line exists in the elementary old Galois group only when the latter has dimension at least two.

The valuation classes s_i are independent modulo T-units. Over k(mu_p), the valuation-root and unit-root fields have cyclotomic action, while the elementary marked extension has trivial action. The cyclotomic extension has nontrivial degree prime to p in this branch, so the two character types are distinct. Lemma 6.4 therefore gives the required linear disjointness.

For q_a impose the source's nonzero s_a root coordinate, zero other old root coordinates, zero unit-root coordinate and an elementary old Frobenius outside the p_a inertia line. At successive stages also impose splitting in both each earlier one-prime cyclic field and its valuation-root field. The enlarged form of Lemma 6.4 proves simultaneous compatibility. Exclude all old/new primes and the exceptional set. In the number-field application choose primes upstairs of absolute residue degree one; the omitted higher-degree primes have density zero. Their descendants split in k(mu_p)/k. This descent detail is explicit in the German proof.

Let U be the old H^1 and V the span of the new one-prime characters eta_a. Their distinct inertia coordinates give independence and U intersect V=0; the dimension formula gives H^1=U direct-sum V. Successive splitting in the two types of earlier fields gives both off-diagonal local cup vanishings; odd characteristic gives diagonal vanishing.

Choose chi_a in U nonzero on p_a inertia and zero on Frob(q_a), and choose psi_a in U nonzero on Frob(q_a). The former choice follows from Frobenius being outside the inertia line; the latter from its nonzero value. The printed psi_a condition at Frob(p_a) must be corrected to Frob(q_a), in English p.15 and German p.16. A Frobenius at the ramified old prime would not establish the required new-prime coordinate.

The chi_a cup eta_a products give a nonzero diagonal old-prime block and zero new-prime block. The psi_a cup eta_a products give a nonzero diagonal new-prime block. Local Proposition 5.3 verifies these entries. Hence the block-triangular matrix is invertible and U cup V spans H^2.

## 6. The delta=1 branch and the three linked repairs

Enlarge T to contain S_p, kill V_T^empty, and ensure n=|T|+r>=3. Adding local tests preserves V_T^empty=0. Lemma 6.5, using the now-corrected duality and Poitou-Tate, gives Cl_T(k)(p)=0 and

    L = k_T^el = k(pth roots of T-units),  dim Gal(L/k)=n.

This applies to odd p with mu_p in k, and to p=2 over totally imaginary k. Select one prime for each nonzero vector of Gal(L/k), obtaining P={p_0,...,p_m}, with m+1=p^n-1. Chebotarev allows all exclusions. The Frobenius vectors span even after deleting any one prime; hence V_P^T and all one-deletion obstruction groups vanish. If E=Gal(k_P^(T,el)/k), then dim E=m+1-n and every old prime has nonzero inertia.

For a=1,...,m choose n-1 indices I_a, avoiding 0 and a, such that adjoining either Frob(p_0) or Frob(p_a) gives a basis of Gal(L/k). This follows explicitly by using a complement for a dependent pair, or using their sum and completing a basis for an independent pair. All needed nonzero vectors occur in P.

Set

    R_a = {p_0,p_a} union {p_i : i in I_a},
    F_a = k_(R_a)^(T,el).

The Frobenius rank on R_a is n, so V_(R_a)^T=0 and the cohomology formula gives h^1(X minus R_a,T)=1. Deleting p_0 or p_a leaves a Frobenius basis and gives h^1=0. Thus F_a/k is cyclic of order p and ramifies at both distinguished primes. Equivalently, the inertia lines outside R_a are an independent family of m-n vectors in E, and their fixed field is F_a.

This establishes, rather than assumes, the three linked source corrections:

1. Replace the two-prime field asserted cyclic by F_a.
2. In condition (C_a), require the old Frobenius to be a nonzero vector in Gal(k_P^(T,el)/F_a).
3. Choose chi_a from H^1(X minus R_a,T), not the printed two-prime H^1 space.

They occur in English pp.18-19 and German pp.18-19. The literal two-prime field is trivial when its two Frobenius vectors are independent: its H^1 dimension is two minus two. Such pairs occur in this construction. This is a consequential omission, not a harmless alternate notation.

There is no hidden compatibility introduced by the repair. Lemma 6.5(b), applied to the independent indices {a} union I_a, makes L, k_P^(T,el) and k(root_p s_a, root_p s_i for i in I_a) jointly linearly disjoint. Thus the zero L coordinate, the specified root coordinates and any vector in the corrected nonzero Frobenius kernel can be prescribed independently. Its dimension is

    dim Gal(k_P^(T,el)/F_a) = m-n = p^n-2-n > 0.

The inequality follows from n>=3, including p=2. It prevents a real edge-case failure: at p=2,n=2 that kernel would be zero.

The earlier cyclic fields K_b, ramified at q_b alone outside T, are jointly independent from this old compositum and from one another. Indeed, each q_b is unramified in the old compositum and in every K_c with c different from b; its inertia maps nontrivially only to its own cyclic factor. No nontrivial linear combination of these factors can become an old-compositum character. Hence requiring q_a to split in every earlier K_b is compatible with all old prescriptions. All choices can exclude every earlier prime.

Let eta_a generate H^1 of K_a/k, and let chi_a be the character of F_a/k. Choose psi_a in the old space U=H^1(X minus P,T), nonzero on the selected nonzero Frob(q_a). This strengthens the source's larger ambient-space choice and is available. It makes every new-prime Frobenius evaluation canonical.

Localization omitting p_0 has the 2m coordinates p_1,...,p_m,q_1,...,q_m. For chi_a cup eta_a, the p_a entry is nonzero. At I_a, eta_a is locally zero by the root splitting and Lemma 5.2; outside R_a, chi_a is unramified and both characters are unramified. At q_a the product is zero because the Frobenius lies in ker chi_a; at other q_b both are unramified. Thus the first block is diagonal. The psi_a cup eta_a products have nonzero diagonal q_a entries and zero other new-prime entries. The block matrix is invertible over every F_p, including F_2.

## 7. Characteristic two: the full isotropic-summand check

For p=2 one has delta=1, so only the preceding branch is needed. Merely invoking anticommutativity would be invalid; both off-diagonal and diagonal products have been checked.

If b<a, q_a splits in K_b, so eta_b restricts to zero at q_a. It also splits in L. Lemma 5.2 identifies L K_b with L(root_p s_(q_b)); therefore q_a splits in that root compositum. Apply the final equivalence of the same lemma with its ramified prime q=q_a and its test prime q_b. It implies q_b splits in K_a. Thus eta_a restricts to zero at q_b as well. The lemma's hypotheses hold: Cl_T(k)(2)=0, both primes are distinct and outside T union S_2, q_a splits in the unit-root field, and q_b has norm 1 modulo 2. All other local cup coordinates involve two unramified characters and are zero. Injective localization proves off-diagonal vanishing globally.

For the diagonal, -1 is a T-unit, so L contains k(i). A new q_a splitting in L has -1 square locally, hence N(q_a)=1 modulo 4 since q_a is not above 2. In the tame local pro-2 presentation, the relator has a cross-commutator term, while its inertia-power exponent N(q_a)-1 is divisible by 4. Modulo the third lower 2-central group there are no generator-square terms. NSW 3.9.13 therefore gives zero diagonal cup coefficients. The local pairing is alternating, and eta_a cup eta_a vanishes at q_a. At other primes eta_a is unramified, so its self-cup factors through a procyclic group of cohomological dimension one and vanishes. Localization gives global diagonal vanishing.

Bilinearity now gives V cup V=0, with U cup V onto H^2 by the verified matrix. This check works without imposing that k itself contain i: splitting the auxiliary primes in k(i) suffices.

## 8. Group cohomology, mildness and the nested algebra

The ordering of implications is sound. Lemma 2.2 identifies H^1 of the group and curve and injects group H^2 into curve H^2 before asphericity is known. Naturality of cups and the arithmetic cross-cup surjectivity show that this injection is onto. Consequently group H^2 has dimension 2m>0. H^1 is finite and H^2 is finite, giving a finitely generated, finitely presented pro-p group. No K(pi,1) comparison in degree two has been presumed in order to prove itself.

For odd p, Schmidt's earlier Theorem 5.5 converts the cup conditions to independent quadratic cross-brackets in a minimal presentation. Labute's Theorem 3.3 gives strong freeness after reduction modulo pi, and Theorem 3.10 lifts it over F_p[pi]. The p-power linear terms disappear only in this reduction; they are not incorrectly inferred from odd-characteristic cups.

For p=2, use Labute-Minac Theorem 1.1 with its U equal to the arithmetic V and its V equal to the arithmetic U. The cup order reversal does not alter surjectivity. In the proof, the mixed operator is P(x)=pi*x+x^2; the tensor-square coefficient computation takes place in the reduced quadratic algebra, where its image is x^2. The square terms inside the isotropic summand disappear because the entire restricted cup pairing is zero, not merely its off-diagonal part.

I checked the elimination argument in Theorem 4.5, the independence criterion in Theorem 4.7 and the lift in Theorem 4.4. Elimination identifies the ideal generated by the complementary variables with a free quadratic algebra on iterated adjoints. The cross-brackets are independent over the complementary free associative algebra: distinct final complementary-generator indices and preceding generator letters distinguish the words. Full rank of the cross-cup makes the projected relators independent in that free module.

For clarity in the lifting proof, write M=r/[r,r]. The correct reduction map is U/ pi U = U tensor_(F_2[pi]) F_2. There are surjections from the free reduced relation module onto M/pi M and then onto the reduced ideal's abelianization; their composite is an isomorphism under reduced strong freeness. The relation-module exact sequence and the two Hilbert-series bounds force equality, torsion-freeness of U over F_2[pi], and freeness of M over U. This explicit reading avoids relying on typographical tensor/reduction ambiguities in the manuscript.

Theorem 5.3 imports the relation-module induction from Labute 2006 Theorem 4.1. The induction compares the initial relation ideal with the graded closed normal subgroup; it then compares graded abelianizations, and lifts graded freeness to the completed relation module. At 2 the relation ideal lies in degrees at least two inside L_mix^+, which is a free ordinary Lie algebra by Theorem 2.3. Mixed PBW and strong freeness give a torsion-free quotient over F_2[pi]. Labute 1967 Propositions 3-4 supply graded freeness and the homogeneous-subalgebra implication under precisely that quotient hypothesis. Thus the modified induction is applicable.

The resulting completed relation-module resolution is

    0 -> R/[R,R] -> Z_p[[G]]^d -> Z_p[[G]] -> Z_p -> 0,

with the first module free on the minimal relations. It gives cd G<=2; nonzero H^2 gives equality. The inspected 2006 addendum changes examples and a dimension formula, not the elimination, reduction or relation-module implication used here. No result about extensions of Q unramified at infinity is used to infer a real-field scheme statement.

Sources: [Schmidt 2007](https://arxiv.org/pdf/0705.3372v2), section 5; [Labute 2006 author manuscript](https://www.math.mcgill.ca/labute/papers/Galram.pdf), Theorems 3.3, 3.10, 4.1; [addendum](https://www.math.mcgill.ca/labute/papers/Galram-Add.pdf); [Labute-Minac v2](https://arxiv.org/pdf/0903.4383v2), sections 2-5 and 7; [Labute 1967 volume scan](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0004/PPN356556735_0004.pdf), printed pp.147-148.

## 9. Universal covers, unmarking, excision and final comparison

The auxiliary construction gives a nonempty A with marked curve (X minus A,S union T union T_0) of type K(pi,1), vanishing obstruction and actual ramification at every prime of A. Corollary 3.7 applies after the mildness calculation because H^2 comparison is already surjective, cd<=2, and A is nonempty.

Proposition 7.1 does not use an unjustified monotonicity principle. Over the original marked universal pro-p cover, Corollary 3.4 shows that unmarking T_0 introduces exactly the local unramified degree-one classes and leaves higher cohomology zero. The new kernel's H^2 injects into zero, so it is free pro-p. Applying the degree-two comparison criterion over this cover and then its universal pro-p cover gives the unmarked K(pi,1) property. Each new local decomposition group is nontrivial, torsion-free and procyclic, hence Z_p. This realizes the full unramified local tower.

Repeat for S. Excision after deleting S then computes new cohomology from the local ramified parts over those full unramified towers. Their H^i for i>=2 is zero. Another free kernel results. Its degree-one restriction maps furnish the full local degree-one spaces; local decomposition groups are free subgroups of that free kernel. The local pro-p maps are isomorphisms by the H^1-isomorphism/H^2-injection criterion, with both H^2 groups zero. Thus local realization at S is proved, not assumed. The same comparison yields the K(pi,1) property of (X minus (S union A),T).

The free-product assertion uses the continuous generalized sums, defined as limits over finite subextensions. NSW 4.3.14 computes the corresponding free-product cohomology; NSW 1.6.15 then recognizes the isomorphism. An arbitrary discrete sum over infinitely many primes and an H^1-only recognition theorem for arbitrary pro-p groups would be insufficient; neither is being used.

The final curve has no higher etale cohomology and comparison gives cd<=2. At each auxiliary prime v, the tame local pro-p group has inertia Z_p and Frobenius action by N(v). Any finite-cd quotient is torsion-free. If its inertia image is nonzero, it is an injective image of Z_p. A kernel element with nonzero Frobenius projection a would then force N(v)^a=1 on that inertia, impossible: the positive integer N(v)>1 has infinite p-adic order. A kernel with zero Frobenius projection lies in the already-injective inertia. Hence a ramified finite-cd quotient is the full local group. Actual auxiliary ramification gives full local realization at A and exact global cd=2. This remains valid at p=2.

Finally the obstruction groups shrink under unmarking and the relevant enlargements. The two final localization sequences in Schmidt p.21 are therefore exact; in degree one the kernel is the more strongly marked space, and dimension comparison gives surjectivity onto the local H^1 factors. The old surjective cup spans the kernel of H^2 localization; local perfect pairings, lifted through the H^1 surjection, span its quotient. Thus the claimed final cup surjectivity also follows. Empty final T is precisely the unmarked arithmetic curve in the conjecture.

## 10. Imported interfaces and checked hypotheses

The following remain standard imports; the review checked their statements and the indicated application hypotheses rather than claiming foundational reproving.

- **Homotopy comparison:** Schmidt 2007 Proposition 2.1 uses Artin-Mazur 4.3-4.4. Here the scheme is connected and locally noetherian; empty marking ensures its applicability to the original homotopy formulation. The marked cohomological comparison proof in Lemma 2.2 was checked separately.
- **Local duality and dimension:** NSW 7.2.6 and 7.3.9 concern finite modules over nonarchimedean local fields. F_p and its dual mu_p meet the characteristic hypotheses. Newly selected primes are away from p; the only potentially p-adic conditions are treated explicitly as integral Kummer conditions or in the intermediate wild open.
- **Arithmetic etale comparison and duality:** Milne II.2.9 requires the coefficient prime invertible on the affine open used for comparison; Sigma contains S_p. II.2.13 supplies the Euler characteristic there. II.3.1 and II.3.2 give the required finite pairing and ordinary-cohomology version under the real-place convention. The boundary is compatible with local invariants. Excision restores the tame curve; p is not assumed invertible on that final curve. [Milne, Arithmetic Duality Theorems](https://www.jmilne.org/math/Books/ADTnot.pdf).
- **Poitou-Tate and class groups:** NSW 8.6.7 and 8.6.10 are applied with a finite module whose order is invertible outside Sigma and with the archimedean places included. The real terms contribute no relevant p-primary correction in this scope. NSW 8.6.3 identifies the required degree-one kernel with class-group characters. NSW 8.3.5 gives the idele-class interface in Lemma 6.5; reciprocity sends a valuation representative to inverse Frobenius, so the linear independence used there has the required arithmetic meaning.
- **Generator formula and pro-p comparison:** NSW 10.7.10 supplies the H^1 formula with the Kummer obstruction. The archimedean convention reconciles its Galois notation with the marked scheme. NSW 10.4.8 requires S_p and the archimedean places; it is used only at the intermediate stage where those hypotheses hold.
- **Hasse principle and Chebotarev:** NSW 9.1.9(ii) has the density and exponent conditions checked in section 4. Every Chebotarev prescription above is nonempty in a finite Galois compositum by the specified joint linear disjointness. Lifting a density-zero exceptional set to a finite extension preserves density zero; higher residue-degree contributions have bounded prime sums. This justifies the exclusions and the degree-one choice.
- **Local groups and recognition:** NSW 7.5.2-3, 7.5.8-9 give the tame presentation, local maximal-pro-p inflation and local cd=2 where mu_p is present. NSW 1.6.15 requires H^1 isomorphism and H^2 injection, both verified. NSW 4.3.14 is used for profinite bundles and continuous generalized sums. Freeness from H^2=0 and the subgroup theorem for free pro-p groups are standard imports.
- **Algebra foundations:** Ordinary and mixed PBW, Magnus realization, finite-presentation/cohomology criteria, and the completed relation-module resolution are imports. The relevant modules are finite-dimensional where finite presentation is invoked, relation degrees are two, the number of relations is positive, and the polynomial-ring quotients needed by the graded free-subalgebra theorem are torsion-free. The controlling reduction/elimination and completed-induction arguments were inspected as described in section 8.

NSW source: [Cohomology of Number Fields, corrected online edition 2.3](https://www.mathi.uni-heidelberg.de/~schmidt/NSW2e/NSW2.3.pdf).

## 11. Attribution and disposition boundary

The English marked-curve manuscript is dated 16 January 2009 and its arXiv v2 record calls it the final English translation. The German paper is listed by Schmidt as J. reine angew. Math. 640 (2010), 203-235. Labute's author page lists the Labute-Minac result as J. Algebra 332 (2011), 136-158, with the journal title omitting “of Q.” These publication attributions are independently supported by the public author/record pages. [Schmidt arXiv record](https://arxiv.org/abs/0806.1863v2), [Schmidt publication list](https://www.mathi.uni-heidelberg.de/~schmidt/publ_de.html), [Labute publication list](https://www.math.mcgill.ca/labute/research.html).

The accepted resolution is credited to that prior mathematics, with an authored application/correction audit. Its mathematical acceptance does not authenticate every literal printed formula, extend the source convention, or license publication of source bodies. The review's authored report, local-condition clarification and public verification metadata contain no copied source pages, datasets or private coordination material.

No GitHub, queue, branch or publication action was taken in this independent review. The mathematical work requested for this review is complete; the source-scope catalogue repair is the stated disposition boundary.
