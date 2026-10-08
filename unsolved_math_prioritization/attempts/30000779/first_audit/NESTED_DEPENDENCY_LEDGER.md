# Arithmetic K pi 1 dependency and correction ledger

Problem 30000779, OWR-1586-003. Audit date 8 October 2026.

This supplements PRIOR_RESOLUTION_AUDIT.md. It records an application audit of prior mathematics, with no new proof-search turn. The proposed mathematical acceptance concerns the exact OWR conjecture under its original convention that p is odd or k is totally imaginary. The catalogue's omission of that convention is a separate source-scope repair. No result or open-case classification for real number fields at p=2 is inferred.

## Inspection depth and citation convention

Page numbers below are the printed manuscript page numbers, which equal the one-based PDF page numbers for the Schmidt English and German manuscripts and for Labute–Mináč. They are not journal page numbers. The OWR report is identified by its printed pages 1756–1758.

The controlling arguments inspected are Schmidt marked curves §§2–7, including both arithmetic constructions and the complete proof of Proposition 7.1 and Theorem 1.1; Schmidt rings of integers Proposition 2.1 and §5; Labute–Mináč §§2–5 and §7; and Labute's mild-group elimination, reduction and relation-module proofs. The source pages carrying consequential indexing issues were also checked as images. The dependency boundary consists of explicitly stated standard imports below. This is not a claim to reprove étale homotopy theory, class field theory, arithmetic duality or PBW from first principles. Neither the real-field p=2 result nor the full profinite analogue is an imported conclusion.

Primary sources:

- Schmidt English: https://www.mathi.uni-heidelberg.de/~schmidt/papers/marked.pdf
- Schmidt German v2: https://arxiv.org/pdf/0806.0772v2
- Schmidt rings of integers v2: https://arxiv.org/pdf/0705.3372v2
- Labute–Mináč v2: https://arxiv.org/pdf/0903.4383v2
- Labute mild groups: https://www.math.mcgill.ca/labute/papers/Galram.pdf
- Labute addendum: https://www.math.mcgill.ca/labute/papers/Galram-Add.pdf
- NSW corrected edition 2.3: https://www.mathi.uni-heidelberg.de/~schmidt/NSW2e/NSW2.3.pdf
- Milne second edition: https://www.jmilne.org/math/Books/ADTnot.pdf
- Labute 1967 volume scan: https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0004/PPN356556735_0004.pdf

The 1967 scan used here is Labute, Algèbres de Lie et pro-p-groupes définis par une seule relation, Inventiones mathematicae 4 (1967), 142–158. It supplies the free graded Lie subalgebra input, Proposition 4 on pp.147–148, PDF pages 158–159 of the complete volume. It is not Labute's different 1967 paper Classification of Demuskin Groups. For the cup/relator interface the accessible source actually checked is NSW 3.9.13, together with Labute–Mináč §7.

## Exact correction locations in Schmidt

### Duality local products

In the proof of Theorem 4.1, replace the first local-product index S by T in precisely these displays:

- English p.10, sequence (I), between the first large diagram and the H^2 diagram.
- English p.10, sequence (II), immediately before the conclusion of the proof.
- German p.10, sequence (I), at the bottom of the page.
- German p.11, sequence (II), above the conclusion of the proof.

Only these products change. The S factors in the Kummer-condition sequence and the top row of the first diagram are correct and must remain S. The S factors in the H^2 localization diagram are also correct.

Here is the corrected cokernel calculation. Put J=Sigma minus (S union T). All cohomology in the following paragraph has F_p coefficients. Let

    W = product_{v in Sigma} H^1(k_v),
    B = product_{v in S} H^1(k_v) times product_{v in J} H^1_nr(k_v).

For the Kummer coefficients, the local condition at v in J is explicitly O_v^× k_v^{×p}/k_v^{×p}. Local reciprocity says that its annihilator under local Tate duality is H^1_nr(k_v,F_p): an unramified character evaluates through the valuation, so it kills precisely the unit condition. At v dividing p this unit subgroup must not be silently identified with the generally smaller Galois-unramified subgroup of H^1(k_v,mu_p). The source's “nr” abbreviation in the Kummer-coefficient display is read using this explicit integral Kummer condition. Thus the argument does not assume p invertible at those local rings.

The quotient W/B is

    Q = product_{v in T} H^1(k_v) times product_{v in J} (H^1(k_v)/H^1_nr(k_v)).

Poitou–Tate, and the choice killing Sha^2(k,Sigma), identify coker(H^1(X minus Sigma) -> Q) with (V_S^T)^dual. Excision and Proposition 3.1 identify exactly that same cokernel with ker(H^2(X minus S,T) -> H^2(X minus Sigma)). Localization injectivity on X minus Sigma identifies this kernel with Sha^2(k,S,T). Thus Theorem 4.1 follows with T in both displays. This correction is already forced by the correctly indexed quotient in each source's large diagram.

### The odd-prime branch

English p.15, the displayed condition defining chi_a and psi_a, and German p.16, its first displayed condition, put the nonvanishing condition on psi_a at the old prime p_a. It must be at the new prime q_a. Proposition 5.3 then gives the needed nonzero q_a cup coordinate. Choose psi_a in the old H^1 space, so its Frobenius at q_a is well-defined. The preceding choice Frob(q_a) outside the p_a-inertia line both makes this Frobenius nonzero and allows chi_a to vanish on it while being nonzero on inertia.

Explicitly enlarge the old prime set until its H^1 dimension is at least two. This preserves every deletion-vanishing condition on V. It ensures the Frobenius-outside-line choice exists. For the number-field construction one may discard all primes of absolute residue degree greater than one in k(mu_p); this discarded set has density zero and the remaining primes descend to primes split in k(mu_p)/k. The German version explicitly includes degree-one primes. No effective Chebotarev estimate is required.

### The roots-of-unity cyclic field

Set n=|T|+r, choose n>=3, and let P={p_0,...,p_m} contain one prime for every nonzero vector in Gal(L/k), where L=k_T^el and m+1=p^n-1. For each a let I_a be the n-1 auxiliary indices chosen in the source, and define

    R_a = {p_0,p_a} union {p_i : i in I_a},
    F_a = k_{R_a}^{T,el}.

There are three linked omitted-I_a occurrences in each version:

1. The field declared cyclic of degree p after the inertia-subspace calculation. English p.18, paragraph immediately above condition (C_a); German p.18, final paragraph. Replace the two-prime field by F_a.
2. The fixed field in the final bullet of condition (C_a). English p.18 and German p.19. Require the E-component of Frobenius to be in Gal(k_P^{T,el}/F_a) minus {0}, where E=Gal(k_P^{T,el}/k).
3. The H^1 space from which a generator chi_a is chosen. English p.19, first paragraph after the cup-surjectivity goal; German p.19, final proof paragraph beginning the choice of chi_a. Use H^1(X minus R_a,T), equivalently the character space of F_a/k.

In that same third paragraph both versions choose psi_a from the whole final H^1 space. The argument needs and permits the stronger choice psi_a in H^1(X minus P,T). Make this explicit. Then psi_a is unramified at every q_b, its q_a Frobenius value is canonical, and the off-diagonal q_b coordinates of psi_a cup eta_a vanish.

These are author-audit corrections; they are not presented as a publisher's or author's issued erratum. Their necessity and sufficiency can be checked without a new arithmetic idea:

- Lemma 6.5 gives V_{R_a}^T=0 because the Frobenius vectors span an n-dimensional space.
- Theorem 3.6 gives dim H^1(X minus R_a,T)=|R_a|-n=1.
- Deleting p_0 or p_a leaves a Frobenius basis, so the corresponding H^1 dimension is zero. The unique character of F_a therefore ramifies at both p_0 and p_a.
- The inertia lines outside {0,a} union I_a span an (m-n)-dimensional subspace of E, whose dimension is m+1-n. Its fixed field is exactly F_a.
- Lemma 6.5(b), with independent Frobenius indices {a} union I_a, makes L, k_P^{T,el}, and k(root_p s_a, root_p s_i for i in I_a) linearly disjoint. The prescribed root behavior and any chosen nonzero element of ker(E -> Gal(F_a/k)) can therefore be imposed simultaneously.
- That kernel has dimension m-n=p^n-2-n>0 for n>=3, including p=2. This additional explicit size choice avoids a zero-kernel edge case.
- Each earlier one-prime cyclic field K_b is ramified at its own q_b and unramified at the other new primes and in the old compositum. Independence of the corresponding inertia coordinates makes simultaneous splitting in all earlier K_b compatible with the old conditions.

The literal two-prime field cannot substitute for F_a: for an independent pair of its Frobenius vectors, the dimension formula |R|-rank(Frob_R) makes the two-prime H^1 group zero. The corrected construction instead always has dimension one.

## Full characteristic-two cup check

For p=2, delta=1, so only the roots-of-unity branch is needed. Temporary T includes S_2, has trivial 2-primary class group, and has n>=3. Let K_a=k_{ {q_a} }^{T,el} and let eta_a be its nonzero character. All q_a are distinct and avoid T, M and P. They split in L=k(square roots of T-units).

For b<a, successive splitting gives q_a split in K_b. Thus eta_b is the zero local character at q_a and the cup eta_a cup eta_b vanishes there. Since q_a splits in both L and K_b, it splits in L K_b. Lemma 5.2 identifies this field with L(square root of s_{q_b}). Apply the final equivalence of that lemma with its ramified prime q=q_a and its test prime p=q_b. It says that q_b splits in K_a. Hence eta_a is the zero local character at q_b, so the opposite cup coordinate is also zero. This is the reciprocity step required to turn the one-sided recursive choice into vanishing in both directions.

The hypotheses of this second use of Lemma 5.2 hold: Cl_T(k)(2)=0; q_a is outside T union S_2 and split in the T-unit field; q_b is outside T union {q_a} and has odd norm, hence norm 1 modulo 2. Every other prime of the final ramification set sees both characters unramified, so their cup factors through the procyclic unramified quotient and is zero. Localization is injective, giving global off-diagonal vanishing.

For the diagonal, -1 is a T-unit, so L contains k(i). Splitting q_a in L makes -1 a square in k_{q_a}. Since q_a does not divide 2, N(q_a)=1 modulo 4. The tame local pro-2 presentation is generated by Frobenius sigma and inertia tau, with relation sigma tau sigma^{-1}=tau^{N(q_a)}. Modulo the third lower 2-central subgroup its relation has a nonzero cross-commutator coefficient and no generator-square coefficients: N(q_a)-1 is divisible by 4. NSW 3.9.13 identifies those square coefficients with the two diagonal cup values. Both diagonal values are zero, so the entire local pairing is alternating. In particular eta_a cup eta_a is zero at q_a. It is zero at every other prime because eta_a is unramified there. Again localization gives global zero. No odd-characteristic anticommutativity argument is used at 2.

Finally, the arithmetic block matrix proves the étale cross-cup product surjective. H^1(group) equals H^1(marked curve), and H^2(group) injects into H^2(marked curve) by Lemma 2.2. Functoriality of cup products therefore proves that injection surjective before any mildness assertion is used. Thus group H^2 has dimension exactly 2m>0, the group is finitely generated and finitely presented, and its decomposition satisfies Labute–Mináč Theorem 1.1 with the two summands interchanged. This order of implications avoids assuming asphericity in order to prove it.

## Imported arithmetic interfaces

### Homotopy and pro-cover comparison

Schmidt rings of integers Proposition 2.1, manuscript pp.4–5, equates vanishing of higher homotopy of the p-completed étale homotopy type, all-degree comparison with pro-p fundamental group cohomology for all discrete p-primary modules, and F_p cohomological acyclicity of the universal pro-p cover. Its homotopy import is Artin–Mazur 4.3–4.4. The application scheme is connected, locally noetherian and regular. Marked-curve Lemma 2.2 proves the cohomological analogue, including H^2 injectivity before K(pi,1) is known; its proof was read. The final marking set is empty, so the two notions coincide directly. Artin–Mazur's foundational proof is an import, not independently reproved here.

### Local duality and tame groups

NSW 7.2.6 gives the perfect local pairing H^i(k_v,F_p) against H^{2-i}(k_v,mu_p) and identifies H^2(k_v,F_p) with mu_p(k_v)^dual. NSW 7.3.9 supplies h^1=1+delta_v+[k_v:Q_p], with the last term zero away from p. Here k_v is always nonarchimedean of characteristic zero, and the new primes have residue characteristic different from p. These statements imply marked-curve Proposition 3.1 and the nonzero mixed local cup in Proposition 5.3. No alternation is assumed at 2 without the separate check above.

NSW 7.5.2–7.5.3 gives the tame semidirect presentation; 7.5.8 gives inflation isomorphisms from the maximal pro-p quotient for p-primary coefficients; 7.5.9 gives cd=2 when the tame local field contains mu_p. The auxiliary primes all have norm 1 modulo p. For a finite-cd quotient of this local group, inertia has either zero image or an injective Z_p image, since nontrivial finite p-torsion is excluded. In the latter case an element of the kernel projecting nontrivially to Frobenius would force N(v)^a=1 for a nonzero a in Z_p. The positive integer N(v)>1 has infinite p-adic order, also at p=2. Therefore the kernel is zero. Actual ramification at an auxiliary prime forces full local realization; its cd=2 forces exact global cd=2 after the global upper bound is known.

### Arithmetic cohomology and the real-place convention

Milne II.2.9 applies to a locally constant constructible sheaf on an affine arithmetic open, with p invertible there, and identifies its p-primary étale cohomology with that of the unramified-outside-the-boundary Galois group. Milne II.2.13 supplies the finite Euler characteristic. These are used after removing S_p in Schmidt Proposition 3.2 and Proposition 3.3. Excision restores the desired tame open afterward; p is not asserted invertible on the final scheme.

Milne II.3.1 and Corollary II.3.2 give the perfect pairing of Ext^r(F,G_m) with degree 3-r compact-support cohomology, and the ordinary-cohomology form except for 2-primary coefficients over real number fields. With F=F_p, U=X and the source convention, this yields H^3(X,F_p)^dual=mu_p(k). Finite-prime boundary maps are dual to inclusions of roots of unity. This accounts for the single omitted local H^2 factor when delta=1. The theorem interfaces and real-place exception were checked; their entire duality proofs are standard imports.

NSW 10.7.10 is the global H^1 generator formula used by Schmidt Theorem 3.6. It permits arbitrary finite ramification and marking sets, with the relevant Kummer obstruction term. Include archimedean primes in the Galois set and use p odd or total imaginarity to remove the unwanted real p-terms. The resulting h^1, h^2 and h^3 formulas in the main audit do not impose a class-number assumption. The finite extensions used in universal pro-p covers retain the same real-place convention.

NSW 10.4.8 identifies p-primary cohomology after passing to a maximal pro-p quotient when the ramification set contains all p-adic primes (and the stated archimedean places). This is the Neumann comparison used at Schmidt Proposition 3.2. Its containing-S_p hypothesis is checked at that intermediate stage only.

### Duality and local conditions

NSW 8.6.7 is the perfect pairing Sha^1(A') times Sha^2(A) -> Q/Z; NSW 8.6.10 is the nine-term local-global sequence for a finite G_S module with order invertible outside S. Take A=F_p and A'=mu_p. The auxiliary Sigma includes S_p and all relevant finite sets; add the archimedean places in the Galois notation. Enlarge Sigma so the class group over k(mu_p) has no p-primary part. Restriction across the degree-prime-to-p cyclotomic extension is injective, so this also kills the needed original-field kernels. The corrected local-condition cokernel above is the precise interface used to obtain Schmidt Theorem 4.1.

NSW 8.6.3 identifies Sha^1(G_T,Z/pZ) with Hom(Cl_T(k),Z/pZ) when p is invertible outside T. In Lemma 6.5, T contains S_p, delta=1, and V_T^empty=0. Poitou–Tate then kills Sha^1, and finiteness of Cl_T makes its p-primary part zero. NSW 8.3.5 is the T-idèle exact sequence. With that class-group obstruction absent, reduction modulo p and the reciprocity map identify the valuation element s_i with the inverse Frobenius at p_i. Linear independence of these Frobenius vectors is therefore exactly the linear-disjointness condition of Lemma 6.5(b). The proofs of Lemma 6.5 and its Kummer dimension statements were read in full.

### Hasse principle and prime selection

NSW 9.1.9(ii) gives injective localization for mu_p if the tested primes split in k(mu_p) with density strictly larger than 1/(p[k(mu_p):k]), except for the Grunwald–Wang special case. Here eligible split primes have density 1/[k(mu_p):k]. Removing any density-zero set and finitely many primes preserves this strict inequality. The special case requires a 2-power exponent at least 8; our exponent is the prime p, including exponent 2, so it cannot occur. Finite-dimensional V_empty^T then makes a finite set of local tests sufficient, as in Schmidt Proposition 4.4.

Chebotarev is used on finite Galois composita. The source's Lemmas 6.4 and 6.5 and the independently ramified new cyclic fields verify every compatibility requirement. Each prescribed nonempty Frobenius class has positive density. A density-zero set remains density zero upon finite base extension: the prime sum upstairs is bounded by the extension degree times the prime sum downstairs, up to the harmless higher-residue-degree terms. Thus all exclusions survive prime selection. No claim of effective bounds or bounded cardinality is needed.

## Imported algebra and reconstruction interfaces

### Cup coefficients and minimal presentation

NSW 3.9.13, checked statement and cochain proof, expresses the cup pairing against a minimal relator through its quadratic commutator and power coefficients. In characteristic two the diagonal coefficient is retained; for exponent q=2 its binomial factor is nonzero. This supplies both the local self-cup calculation and the coefficient identification in Labute–Mináč §7. Finite H^1 gives a finite generating set; finite H^2 gives a finite minimal relation set. The nonzero H^2 condition is established by the already-surjective arithmetic cross-cup before mildness.

### Odd-prime mildness

Schmidt rings of integers Theorem 5.5, pp.17–18, deduces mildness from the isotropic-summand and full-rank cross-cup conditions. It uses Labute Theorem 3.3, an elimination-based strongly-free criterion over a field, and Theorem 3.10, reduction from the graded polynomial ring F_p[pi] to F_p. The relevant proofs were inspected. Independent cross brackets form a free family over the enveloping algebra of the complementary free Lie algebra: in the free associative word basis, their final generator and the eliminated generator distinguish their summands. Labute Theorem 4.1 then gives a free completed relation module and cd=2.

### Characteristic-two mildness

Labute–Mináč Theorem 2.2 identifies the graded algebra of a weighted free pro-2 group with the free mixed Lie algebra. Theorem 2.3 and Corollary 2.4 identify the positive-degree-above-one part as an ordinary free Lie algebra over F_2[pi], and give the corresponding reduced quadratic structure. Theorem 4.5 proves elimination for the quadratic algebra by inverse semidirect-product maps; Theorem 4.7 proves strong freeness from independent projected relations; Theorem 4.4 lifts that result to the mixed algebra by a relation-module exact sequence and Hilbert-series comparison. These controlling proofs and Theorem 1.1's proof in §7 were read.

The distinction between the mixed square P(x)=pi*x+x^2 and its reduced quadratic image x^2 is essential. In §7 the tensor-space argument is the reduced quadratic calculation; Theorem 4.4 supplies the mixed lift. Vanishing of one summand's entire self-cup pairing removes its internal quadratic terms, and surjectivity of its cross-cup makes the projected relation forms independent. All relation degrees are two and their number is positive. The conclusion is mildness, then cd=2 by Theorem 5.3(c).

### Relation module and free Lie subalgebra

Labute–Mináč Theorem 5.3 explicitly imports the proof of Labute Theorem 4.1 with one modification. Labute's full induction, manuscript pp.17–19, was inspected: the graded relation ideal equals the graded normal subgroup, its abelianization matches the graded completed relation module, and graded freeness lifts to freeness over Z_p[[G]]. The modified input at 2 is that the relation ideal is contained in L_mix^+, which is free as an ordinary Lie algebra, with torsion-free quotient over F_2[pi].

The nested free-subalgebra theorem is Labute 1967 Proposition 4: a homogeneous subalgebra of a graded free Lie algebra over a one-variable polynomial ring over a field is free when its quotient is free over that ring. Proposition 3 identifies torsion-free positively graded modules over that polynomial ring with graded-free modules. These statements and proofs on pp.147–148 were inspected in the volume scan. Apply them with the homogeneous relation ideal, and use strong freeness plus the mixed PBW injection to obtain its torsion-free quotient. The exact completed resolution is

    0 -> R/[R,R] -> Z_p[[G]]^d -> Z_p[[G]] -> Z_p -> 0.

Its first term is free on the finitely many minimal relators. It yields cd<=2, and nonzero H^2 yields equality. The 2006 addendum's example and dimension-formula corrections do not alter this proof.

Ordinary PBW, mixed PBW (Lazard II.1.2.8), the free-associative Magnus realization of a free pro-p group, the standard relation-module exact sequence, and the free-pro-p criterion H^2(G,F_p)=0 are foundational algebra/group-cohomology imports. Their module, grading and finite-presentation hypotheses are satisfied above; their original foundational proofs are not claimed independently audited here.

### Removing markings and realizing local groups

Schmidt Proposition 7.1, English pp.19–20, is read as a complete proof, not as an unexplained monotonicity assertion. Corollary 3.4 on the original marked universal pro-p cover identifies exactly the new unramified H^1 classes at the unmarked primes and gives H^i=0 for i>=2. Lemma 2.2 injects the new kernel group's H^2 into zero, so it is free pro-p. Nontrivial torsion-free procyclic decomposition groups give full unramified Z_p towers. The next excision step after removing the prescribed S identifies the additional ramified classes over these towers; the higher local cohomology vanishes, giving another free kernel and the K(pi,1) comparison.

NSW 1.6.15 is the recognition theorem: a pro-p homomorphism is an isomorphism if its induced H^1 map is an isomorphism and its H^2 map is injective, with trivial F_p coefficients. In the first use both groups are free, so the H^2 condition is automatic; it is not an H^1-only recognition claim for arbitrary groups. NSW 4.3.14 identifies cohomology of a free pro-p product over a profinite bundle with the continuous generalized local sums. This verifies the second use and the local free-product assertion. The sums are the direct limits over finite subextensions defined at the start of Schmidt §7, rather than an unrestricted discrete sum over infinitely many primes.

## Outcome and limits

No unverified arithmetic hypothesis is being substituted for the cyclotomic or class-number restrictions. Temporary markings remove the obstruction, and Proposition 7.1 removes those markings again. For the actual OWR application the final marking is empty and the forbidden set is ((all finite primes minus D) union S_p) minus S. Every added prime belongs to D, avoids S and S_p, and every prescribed S prime is retained. S need not lie in D and may be empty.

The mathematical recommendation is acceptance as a credited prior resolution of the exact source conjecture, subject to independent review of this authored correction/application packet. Keep the broader literal catalogue statement on a source-scope hold until its missing real-place convention is repaired; do not invent a residual open question. No copied source body, source image, private coordination file, dataset content, or queue record belongs in the public authored packet.
