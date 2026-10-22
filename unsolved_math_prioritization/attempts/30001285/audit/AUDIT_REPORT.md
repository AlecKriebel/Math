# Independent audit: motivic comparison problem 30001285

Queue rank 972; source problem OWR-3481-002. Audit date: 2026-10-07.

## Disposition

**Accepted as a source-free, unsolved partial-results packet after one minor definition-scope correction.** All five approaches have been examined in full. None settles the general comparison problem, and no sixth mathematical author approach is supplied by this audit. The author disposition remains **unsolved, five of five approaches used**.

The substantive conclusions survive review: the explicit projection obstruction, the distinct exponent-two comparison, the lifting and multiplier criteria, coprime descent, generic detection, and the conditional suspension comparison. The generic beta-minus-sigma class remains uncomputed. Product compatibility with one common normalization for those two particular families remains uncertified. The audit supplies no general injectivity theorem or equality classification.

The correction is confined to the definition of c_A in STATEMENT.md. Kahn's positive reduced étale-motivic generator construction in §10.A assumes deg(A)>2. For the division degrees 1 and 2, define the field-valued invariant to be zero instead. Wang's theorem justifies this over every extension because ind(A_L) divides d and is square-free. The attached patch makes that restriction explicit; it changes no positive-degree example or comparison result.

## 1. Objects examined and preservation

The complete frozen inventory comprised MANIFEST.json and 15 payload files. All 15 payload files were read, including STATEMENT.md, the five full approach files, coefficient and literature records, both scripts, and recorded control results. The externally supplied SHA-256 of the original manifest was verified:

    dfac54b9d1a507c2f3b4cfd6a13e2b627e3b1f85672723130254984183f16772

The original inventory, contents, and manifest remain unchanged. Correction and adversarial tests used separate copies. LOW_DEGREE_CORRECTION.patch contains the actual one-file textual correction. After applying it, only STATEMENT.md and its entry in a regenerated manifest differ. The corrected manifest SHA-256 is:

    f3cff9cedb5a6f8e912dffe81329ffc409ce80cd168401bb8fb4aa21e57f07e8

The corrected STATEMENT.md is 4,850 bytes, SHA-256:

    e1f917fc2f8ad6e0121a641127da9b980806b20172c14bb4423bdc4f3fe7c90e

This report and its associated files contain authored mathematics, verification metadata, and public citations. They contain no copied source documents, extracted source text, source inspection images, dataset contents, or private coordination records.

## 2. Source and hypothesis review

The relevant statements and complete directly used arguments were inspected in the supplied versions of:

- Kahn's 2009 Oberwolfach contribution, pp. 1754–1755, including the original problem and all displayed targets.
- Kahn's published 2010 article: introduction; §§7.B–7.D; §§10.A–10.B, including Theorem 10.7 and its proof, Remark 10.8 and Lemma 10.9; Proposition 10.11 and the completion in Corollary 11.12. The coefficient-warning discussion in §7.F was also checked.
- Kahn–Levine §6.9, including the construction of the maps, the extra d_3 issue, and the full proof of Proposition 6.9.1.
- Wouters arXiv:1003.1654v2, §§2.1–2.2 and §4.1, including both comparison arrows and Proposition 4.2's proof.
- Merkurjev's original author manuscript, *Invariants of algebraic groups*, June 1998: cycle-module conventions, Lemmas 2.1–2.2 and the complete proof of Theorem 2.3. The original theorem requires a smooth connected algebraic group and a cycle module annihilated by an integer prime to the characteristic. These conditions are met below. [Public author manuscript](https://www.math.ucla.edu/~merkurev/papers/last.pdf).

The five supplied PDFs match every recorded byte count and hash. Their ledger is reproduced as metadata in SOURCE_AUDIT.json. The additional Merkurjev author manuscript has 182,885 bytes and SHA-256 8f26266e6f1ce37db27718c4d9f89c347ea37bf00d9f274821ac0fe2c80ede5c. It is an author manuscript dated 1998, not a 2025 paper despite search-engine indexing dates. The journal reference is J. reine angew. Math. 508 (1999), 127–156. Only metadata is delivered.

The report page 1754, Kahn's printed p. 356, and Wouters's Proposition 4.2 page were also visually inspected. These confirm the integral Brauer degree, the different quotient/multiplier arrows, and the attribution of the negative projection answer.

### Hypotheses accepted

A is a fixed central division algebra of degree d prime to char(F). For extensions L/F, its index can drop but always divides d. Morita invariance is applicable to SK_i, but does not replace a degree-dependent generalized Severi–Brauer variety by an unidentified variety. The packet explicitly keeps this distinction.

All coefficient claims are restricted to the prime-to-characteristic part. All uses of the report's SK_2 constructions keep the algebraically closed-subfield hypothesis. Later sources sometimes require only a separably closed subfield; the stronger retained hypothesis is valid. The characteristic-zero field Q_5((x))((y)) does not satisfy that extra subfield hypothesis and is used only for SK_1.

The SL_1 construction specified by the report and Kahn §10 is a field-valued SK_1 invariant. There is no displayed third SK_2 construction to compare. The report's r=d label refers to the absence of the Brauer denominator, whereas the geometric map sigma_d is zero. Those maps are not identified in the packet.

### Correction rechecked

For d=1 or 2 and every L/F, SK_1(A_L)=0 by the split case or Wang's square-free-index theorem. Therefore there is exactly one homomorphism from this source to B_1(L), namely zero, and these zero maps form a natural invariant. This establishes the patched low-degree definition. It neither asserts that a positive generator exists in degree 2 nor extends Kahn's generator calculation beyond its stated range. For d>2 the original definition is unchanged.

## 3. Coefficient and target audit

Write j=i+2. The connecting isomorphism is

    H^(j+1)(F,Q/Z(j)) = H_et^(j+2)(F,Z(j)).

Thus the SK_1 groups have degrees 4 and 5 respectively, while the SK_2 groups have degrees 5 and 6. The Brauer class has Galois degree 2, twist 1, and integral étale-motivic degree 3. Cup product with K_(i+1)^M gives the exact degrees and twists in the packet. No degree-zero interpretation of the connecting map is used in the accepted product argument.

For N invertible in F, the coefficient map H^(j+1)(F,Z/N(j)) into B_i is injective under the norm-residue theorem. To check the kernel, use the coefficient long exact sequence: it is the quotient of H^j(F,Q/Z(j)) by N. This group identifies with K_j^M(F) tensor Q/Z on the relevant prime-to-characteristic part and is divisible, so that quotient is zero. Exactness also identifies the image with B_i[N].

For r dividing d and N=d/r, r[A] is N-torsion. Norm-residue identifies the finite denominator with r[A] cup K_(i+1)^M(F). Since that entire denominator lies in B_i[N], the finite quotient B_i[N]/D_(i,r) injects into B_i/D_(i,r). This is the finite refinement in Kahn Corollary 7.4. No assertion that beta has this particular finite refinement follows from source torsion alone. The packet correctly gives B=Q/Z, D=B[2], N=4 as a counterexample to confusing (B/D)[N] with B[N]/D.

When s divides r, D_(i,r) is contained in D_(i,s), giving the stated quotient projection. If e annihilates D, multiplication defines mu_e:B/D→B, with both composites equal to multiplication by e and kernel B[e]/D. It is not the quotient map or an inverse in general.

The reduction Z/4(j)→Z/2(j), followed by its standard coefficient inclusion back into Z/4(j), is multiplication by 2. This uses the compatible Tate-twist coefficient system. Tensoring three separate inclusions of groups of roots of unity would give the wrong morphism and is correctly excluded.

## 4. Approach 1: extension lifting and the Q_5 example

### Algebraic lemma

The displayed pullback E_f is an abelian group and yields an exact extension of S by D. A section is exactly a lift s↦(s,g(s)). For an element s annihilated by n, replacing a representative b by b+d changes nb by nd; hence theta_n is well-defined in D/nD. A homomorphic lift forces theta_n=0. For S cyclic of order n the converse follows by replacing b with b-d when nb=nd. Direct sums of cyclic groups can then be treated generator by generator. No claim of sufficiency for an arbitrary torsion group or of automatic field-naturality has been added.

### Independent reconstruction of the local calculation

The residue classes 1 and 4 are the nonzero squares modulo 5. Thus 2 is a nonsquare unit and Q_5(sqrt(2))/Q_5 is unramified quadratic. The extension Q_5(sqrt(5))/Q_5 is ramified quadratic. They are distinct and linearly disjoint. These satisfy the exact hypotheses of the Platonov construction quoted in Wouters §2.2(b); its conclusion is index 4 and SK_1(A)=Z/2 for A=(2,x)_2 tensor (5,y)_2. The exponent is exactly 2: it divides 2 because both factors are quaternions, and it is not 1 because the algebra is division of index 4.

At finite coefficients, apply the complete discretely valued cohomology decomposition first for y and then for x. The surviving group is H^2(Q_5,Z/N(1)); the other terms vanish by cd(Q_5)=2. Passing through the compatible coefficient system gives

    H^4(Q_5((x))((y)),Q/Z(3)) = Br(Q_5) = Q/Z.

Every element of D=[A] cup K_2^M(F) is killed by 2. Its nonzero element can be detected without a general claim about arbitrary local parameters. Multiply [A] by {5,y}. The mixed term from (2,x) has iterated residue (2,5), up to a sign that is irrelevant for 2-torsion. The contribution from (5,y) has a repeated symbol and is zero because -1 is a square in Q_5. The quaternion (2,5) is nonsplit: norms from the unramified quadratic extension have even valuation, whereas v_5(5)=1. Therefore D is the unique nonzero order-two subgroup {0,1/2} of Q/Z.

Kahn §7.C identifies sigma_1 with Suslin's injective degree-four invariant. Since the source is Z/2 and (Q/Z)/D has exactly one nonzero element of order 2, sigma_1(s)=1/4+D. Its obstruction is theta_2=1/2 in D/2D, which is nonzero. Equivalently, every homomorphism Z/2→Q/Z lands in D and therefore projects to zero.

This establishes the claimed impossibility of a homomorphic lift even over this one field. It is the known Wouters obstruction with explicit local parameters, not a new disproof of the open-ended comparison request. Neither beta_1(s) nor beta_1=sigma_1 is determined.

## 5. Approach 2: multiplier and universal invariant

The multiplier lemma and the exact sequence

    0 → B[e]/D → (B/D)[e] → D intersection eB → 0

are correct. The last map sends b+D to eb. Its image, kernel, and representative independence follow directly from eD=0. The noncyclic example B=(Z/2)^2, D generated by (1,0), exhibits a genuine residual kernel: different quotient-valued homomorphisms may have equal multiplier transforms.

For the motivic denominator, e=exp(A)/gcd(exp(A),r) annihilates r[A]. Keeping this integer fixed after extension makes multiplication natural even when the exponent drops. Consequently mu_e composed with sigma_r, and mu_exp(A) composed with beta_1, are field-natural SK_1 homomorphisms with unquotiented target B_1.

Precomposition by SL_1(A_L)→SK_1(A_L) places each in the group covered by Kahn Theorem 10.7. Its cyclic universal generator is the fixed-base c_A. The scalar-multiple conclusions are therefore justified. In low degrees the patched zero-source convention makes the assertion vacuous. In higher degree the theorem's hypotheses are met. This does not determine the scalar and, even after determining it, does not remove the kernel B[e]/D.

For the explicit algebra, Kahn Theorem E identifies c_A with sigma_2, since exp(A)=2<ind(A). The denominator for r=2 vanishes. Rost injectivity identifies the nonzero value with 1/2 in Q/Z. Thus mu_2(sigma_1(s))=c_A(s), while q_1(c_A(s))=0. Here mu_2 is an isomorphism because Q/Z is divisible and B[2]=D. These statements are mutually consistent and require their named coefficient arrows.

The distinction between fixed-base c_A evaluated over L and the newly normalized c_(A_L) is also essential. Kahn Remark 10.8 warns against replacing one by the other indiscriminately; Lemma 10.9 supplies the asserted compatibility when the exponent is unchanged.

## 6. Approach 3: transfer and the source annihilator

Restriction preserves the denominator, and corestriction does so by the projection formula with the Milnor K-theory transfer. Therefore corestriction after restriction is multiplication by [L:F] on the quotient target. Only finite separable extensions are used in this argument.

The source annihilator d=ind(A) is valid for both SK_1 and SK_2. Here is an independent reconstruction of the introductory transfer argument. Choose a maximal separable splitting subfield L of the division representative, of degree d. Over L the reduced norm is the split Morita isomorphism; its kernel is zero. Thus restriction sends an SK_i element to zero. Restriction of scalars after scalar extension on K_i(A) is multiplication by d, because the composite exact functor is a direct sum of d copies. Hence d kills the original element. Reduced norm naturality and the established reduced norm for K_2 are the imported K-theoretic inputs. This proof does not use an undefined reduced norm in higher K-degrees.

A common-target difference is consequently d-torsion. If its restriction vanishes after degree n, it is also n-torsion, and Bezout proves vanishing when gcd(d,n)=1. Several degrees work exactly when their joint gcd with d is 1. The primary-component formulation is also correct.

A splitting extension has degree divisible by d. Its restriction–corestriction relation yields no new annihilator coprime to d; a maximal subfield recovers precisely the already known d-annihilation. The explicit projection counterexample shows that agreement after splitting cannot imply agreement before splitting. No sufficient family of prime-to-index comparison computations is supplied.

## 7. Approach 4: quotient cycle module and generic evaluation

The quotient in this approach is a legitimate cycle-module target, not merely an isolated quotient abelian group. One may write its complete graded version as follows. Let

    M_n(L)=H^n(L,Q/Z(n-1)),
    N_n(L)=r[A_L] cup K_(n-2)^M(L),
    Q_n(L)=M_n(L)/N_n(L),

with negative cohomological degrees zero and N_n zero for n<2. Work throughout with the prime-to-characteristic coefficients. The class r[A] is fixed over the base field and is unramified at valuations trivial on that field. Restriction, transfer, Milnor K-action, and residue therefore preserve N: restriction is natural, transfer uses the projection formula, multiplication uses associativity, and residue passes the fixed unramified Brauer class through to the residue field. The Brauer degree is even, so possible ordering conventions do not alter the subgroup. Equivalently N is the image of the corresponding degree-shifted Milnor cycle-module map. Quotients carry the inherited cycle-module operations and identities.

The bounded-torsion passage is valid **on the full graded module**. Define T=ker(d:Q→Q), not just a torsion subgroup in degree four with no other degrees specified. All operations commute with multiplication by d and therefore restrict to T; the cycle-module relations and finite-support property are inherited. Thus T is a cycle module of exponent dividing d, prime to char(F).

Each field-valued difference from SK_1(A_L) lands in T_4(L), because ind(A_L) divides d. The group SL_1(A) is smooth, affine, and geometrically connected. The theorem verified in Merkurjev's original manuscript therefore applies to its invariant with values in T_4. It identifies generic evaluation with the multiplicative unramified class; in particular the evaluation map is injective. Surjectivity of SL_1(A_L)→SK_1(A_L) then shows that the difference on SK_1 vanishes everywhere exactly when its value on the generic element vanishes. In degree d=1 the conclusion is simply the zero-source case.

This argument does not replace T_4 by B_1[d]/D. Those groups can differ, as the packet's finite-refinement negative example demonstrates. It also does not use unrestricted unbounded-exponent generic evaluation without checking the torsion condition.

### Spectral-sequence indexing and the remaining obstruction

At (p,q)=(2,-3), p-q=5, -q=3 and -p-q=1. The incoming d_2 has source (0,-2), identifying the SK_1 denominator with [A] cup K_2^M. For SK_2 the target is (2,-4), the incoming d_2 source is (0,-3), and a d_3 can arise from (-1,-2), namely H_et^1(F,Z(2)). The retained field hypothesis kills this extra image as in Kahn–Levine §6.9. The proof of Proposition 6.9.1 identifies the underlying Brauer differential, including its stated normalization.

These statements fix the target; they do not calculate the image of the generic SK_1 element. The filtered-comparison criterion in the packet is a valid sufficient criterion: a suitably normalized filtration-preserving morphism induces commuting maps of spectral sequences and edge assignments. No such morphism is constructed. Equality of a target or of one differential is not a replacement for it.

The generic class omega_A=beta_1([eta])-sigma_1([eta]) remains the precise unevaluated obstruction. The warning about the flag-variety comparison and finite coefficient reduction is appropriate; this audit supplies no corrected general flag theorem.

## 8. Approach 5: suspension, residue, and signs

The direct-summand assertion is unconditional within the stated K-theoretic framework. The module product sends SK_1×K_1(F) to SK_2 by reduced norm compatibility. For the chosen normalization, localization gives partial_K({t}·x)=x. The graded interchange rule gives x·{t}=-{t}·x, so right suspension has residue -x and left inverse -partial_K. This proves injectivity and an actual splitting. The rational function field retains the field and index hypotheses needed for the constructions being discussed.

The subsequent lemma is conditional exactly as stated. If both invariant families satisfy the displayed right-product identity (H), their difference satisfies it. The cohomological residue at t descends to the quotient because A is unramified and residues take [A] cup K_3^M into [A] cup K_2^M. For a base-field class b of Galois degree 4,

    partial_H(b cup {t}) = b.

The degree is even, hence moving the uniformizer to the first position introduces no sign. This proves the three claimed implications under (H): equality on decomposables from SK_1 equality, descent from SK_2 equality over F(t), and detection of a nonzero suspended difference.

There is no contradiction with partial_K(x·{t})=-x: an unsigned residue square for both cohomological degrees has not been asserted. In the coefficient triangle, the connecting morphism has degree one. Its usual left multiplication by a degree-one integral class contributes a minus sign, whereas right multiplication has the displayed unsigned formula. The packet correctly refuses to claim that the two separately constructed invariant families share the necessary edge/product convention merely from the word “multiplicative.”

Kahn Propositions 7.7–7.8 and the Kahn–Levine module spectral sequence are valid structural inputs. Their precise common normalization is an outstanding comparison task. Even once that is supplied, the argument covers the subgroup generated by products, not all SK_2. The statement about the Calmès symbol is used only to reject an unjustified generation argument; no nonzero beta-versus-sigma value is extracted from it.

## 9. Executable validation and limits

The author's checks.py uses explicit conditional failures, so optimization does not disable the checks. Normal and optimized isolated runs each reproduced CHECK_RESULTS.json exactly, with 114,419 assertions. The author manifest verifier passed both modes from a foreign working directory, confirming its relative-file resolution. The corrected packet also passed both modes and all independent checks.

The separate independent_controls.py reconstructs finite abelian groups by tuples, enumerates all their subgroups, forms quotient cosets, and checks lifts and multipliers without reusing the author's cyclic-residue representation. Its 17 models include all cyclic groups of orders 1 through 12 and five noncyclic products, including (Z/4)^2. It checks lift existence, representative independence, actual homomorphism relations for the constructed lifts, multiplier kernels, the torsion exact-sequence image, coprime annihilator logic, and explicit negative examples. Separate parity and local quadratic-unit controls check only the claimed formal arithmetic, not the motivic theory.

There are 13,525 independent controls per run. The independent script was itself run normally and under optimization with identical results. It invokes both modes of the author scripts. A deliberately false check fails in each mode. In disposable copies, the verifier rejected each of the following in both modes: a wrong external digest, altered payload, extra file, missing file, payload symlink, manifest symlink, unsafe manifest filename, and directory in place of a payload. The unsafe-name fixture is rejected already by inventory validation; this does not claim a separate traversal was performed. No concurrent hostile-filesystem/TOCTOU hardening is claimed.

The two supplied corpus byte counts and SHA-256 hashes were independently rechecked. The problems corpus contains one record with id 30001285. The research-results object contains neither the exact problem-number key nor an exact-title substring match. These are provenance checks, not mathematical evidence. Dataset contents are excluded from the deliverables.

No finite test establishes Platonov's SK_1 computation, Suslin/Rost injectivity, the norm-residue theorem, reduced norm construction, Rost's cycle-module theory, or the cited motivic spectral sequences. These remain explicit literature dependencies. The relevant source hypotheses and directly used arguments have been checked; this is not a reproof or proof-assistant formalization of that entire literature.

## 10. Acceptance boundaries and deliverables

Accepted after the attached correction:

1. The source-level formulation and all displayed coefficient targets, with low-degree c_A defined as above.
2. The elementary lifting, multiplier, and descent lemmas.
3. The explicit known projection obstruction over Q_5((x))((y)).
4. The distinct, previously established exponent-two comparison c_A=sigma_2.
5. Generic detection using the complete quotient cycle module and its bounded-torsion kernel.
6. The K-theory direct summand and the conditional comparison lemma under (H).
7. Vacuous equality for square-free index, with the appropriate SK_2 construction hypotheses retained.

Not established: beta_1=sigma_1 in general; beta_1's explicit value in the local example; generic omega_A=0; a normalized filtered comparison; the common hypothesis (H) for beta and sigma; all-SK_2 generation by products; classification of equality cases; general injectivity; or any third SL_1-based SK_2 invariant.

A bounded current primary-source search found no theorem superseding this disposition. That absence is not a proof of worldwide literature completeness. The journal full text of Wouters's later publication was not separately inspected; the exact v2 numbering and source version have been retained.

The public audit deliverables are this report, the actual correction patch, independent controls and their results, corrected-copy results, source metadata, an acceptance record, and a hash manifest. The external hash of that audit manifest must be supplied separately. This audit authorizes no claim that the problem is solved or that the imported results are new.
