# KP-5.16: equivalence of finite-generator DG algebras

**Target:** 3023 / KP-5.16, rank 1057.  
**Date:** 2026-10-08.  
**Disposition:** partial results; five substantive approaches exhausted; no complete solution of the graded-commutative branch.  
**Authorship:** independently written AI-assisted research for Alec Kriebel. Unrefereed. No novelty claim.

## 1. Exact scope and conclusion

The source asks three decision questions, separately for finite tensor DG algebras and finite-generator free graded-commutative DG algebras, over Z or a field. Generator degrees may be any integers. The relations to decide are stable tame isomorphism, quasi-isomorphism, and equivalence of the derived categories of DG modules as triangulated categories. The source is K3, Problem 5.16, printed pp. 313–315 [K3]. None of the three commutative questions is silently replaced here by an easier problem.

Manolescu–Rozenblyum [MR, Theorem 1] supplies the known negative answer for the tensor-algebra branch over every nonzero Turing-computable commutative coefficient ring. Their reductions already have generators in degrees 0 and 1. Their paper explicitly leaves the graded-commutative branch open. The inspected arXiv record displays version 1 with submission timestamp 2026-04-28 15:51:10 UTC, despite the 2605 identifier, and no journal reference. This date is transcribed from the record and also appears in its PDF/HTML stamp; it is not inferred from the identifier. Searches on 2026-10-08 located no later primary source resolving the commutative branch; this is a bounded literature finding, not a theorem about all literature. Section 3 reconstructs the DGA part of their first reduction and credits its origin.

The substantive outcomes for the remaining branch are:

1. An explicit unit-boundary criterion for every finite polynomial–exterior DGA, with arbitrary integer grading. Acyclicity is decidable over Z and effective fields in this convention. Thus a direct commutative version of the noncommutative zero-object reduction cannot prove the desired undecidability.
2. A precise integer-Diophantine encoding proving augmentation existence undecidable over Z, even for degree 0/1 polynomial–exterior DGAs. This does not decide the requested equivalence questions.
3. An exact reduction of quasi-isomorphism of complete-intersection Koszul models to isomorphism of their quotient rings, plus explicit syzygy obstructions to dropping regularity. No unproved ring-isomorphism undecidability is assumed.
4. A terminating strict-isomorphism algorithm for positive-generator DGAs over a finite field, and a positive semidecision procedure for stable tame equivalence in the full effective class. Neither is a general decision algorithm for the requested three relations.
5. A classified mixed-degree family with a nonzero triple Massey obstruction, showing concretely why mixed-degree quasi-isomorphism cannot simply be read from degree-zero quotient presentations or formal models.

These are partial theorems and blocked routes, not a solution of the full problem. The complete commutative decision questions remain unresolved by this work. Literature checks, convention audits, and code validation are not counted as substantive proof approaches.

## 2. Conventions that must be retained

We use homological grading: d has degree -1 and d(ab)=d(a)b+(-1)^|a| a d(b). All maps preserve the unit and the coefficient ring, unless an explicitly quoted source uses a different formulation.

A **polynomial–exterior** algebra means

    A = R[x_1,...,x_e] tensor Lambda(theta_1,...,theta_o),

where the x_i have even integer degrees and the theta_j have odd integer degrees. Odd squares are imposed to be zero, also over Z and in characteristic 2. This is often called strictly graded-commutative. It is not the same universal algebra as imposing only ab=(-1)^|a||b| ba over Z or in characteristic 2: the latter imposes 2 theta^2=0 over Z and imposes no odd-square relation over F_2. In characteristic different from 2 over a field the conventions coincide. A differential on a polynomial–exterior algebra must preserve these relations; our constructions do.

The source does not settle this distinction explicitly. It also does not specify an effective encoding of arbitrary fields. Algorithmic assertions here concern Z and fields with effective arithmetic and equality, such as Q and finite fields. No assertion about a Turing machine taking arbitrary exact real or complex coefficients is made.

### 2.1 A convention-dependent stabilization warning

Consider the polynomial–exterior DGA

    S_R=R[u] tensor Lambda(v),  |u|=2, |v|=1, du=v, dv=0.

As a complex its only nontrivial differentials are

    d(u^m)=m u^(m-1)v  (m>=1).

All u^m v are cycles, and each homogeneous component has the displayed unique monomial basis. Therefore over Z,

    H_0(S_Z)=Z, H_(2m)(S_Z)=0 for m>=1,
    H_(2m-1)(S_Z)=Z/m for m>=1.

Over F_p, u^p survives in H_(2p), and u^(p-1)v survives in H_(2p-1). Over Q the augmentation S_Q -> Q is a quasi-isomorphism.

Consequently, if one defines commutative stabilization by freely adjoining every degree-adjacent pair du=v, this operation does not preserve quasi-isomorphism over Z or F_p. R and S_R would be stable tame equivalent by construction but are not quasi-isomorphic in these coefficients. This is a counterexample to that imported implication under the stated convention, not a counterexample to undecidability or a correction of an unambiguously specified definition in the source. It is already unambiguous over odd-characteristic fields, where the two graded-commutativity conventions agree. In characteristic 2 this example uses the strict exterior convention only. Over sign-only Z the displayed polynomial–exterior algebra is not the free algebra requested by that alternative convention.

The opposite-parity pair |u| odd, |v| even, du=v, with u exterior, is contractible away from its unit by d(uv^m)=v^(m+1), without division. Restricted stabilizations, divided powers, or rational coefficients change the issue. We do not choose one of these repairs on the source's behalf. In particular we use the full implication chain only in the tensor case or, for polynomial–exterior stabilizations, over Q.

## 3. Reconstruction of the known tensor-algebra reduction

This section is attributed reconstruction of [MR, Section 3], not one of the five new approaches. Its undecidability input is the associative-algebra unit-ideal theorem stated as [MR, Theorem 2] and attributed there to Bokut [B]. We reconstruct the DGA reduction, not the underlying machine-theoretic theorem. [B]'s original Russian article was separately located; the full claimed coefficient-uniform computability theorem is retained as an external input rather than claimed independently re-proved.

Let f_1,...,f_m be words/polynomials in R<x_1,...,x_n>, with n,m>=1 (harmless padding ensures this). Define A by |x_i|=0, |r_j|=1, dx_i=0, dr_j=f_j. Let B have the same generators and dr_j=1. Since A has no negative degrees, H_0(A)=R<x>/(f), and 1 is a boundary precisely when 1 lies in the two-sided ideal (f). B has the explicit unit primitive r_1.

If dh=1, then for every cycle z, d(hz)=z, so A is acyclic. Conversely an acyclic unital DGA has a degree-one primitive of its unit. Every DG A-module M is acyclic in this case: multiplication by h gives a contraction, since d_M(hm)=m-hd_M(m). Thus its derived category is zero. Conversely, if D(A) is zero, the object A is zero there, so its underlying homology vanishes. In particular H_0(A)=0. This zero-category argument uses neither a linear enhancement nor Hochschild homology invariance under arbitrary triangulated equivalences.

Here is a direct tame normal-form argument for the special A above. It avoids extending a general filtered normal-form theorem outside its hypotheses. Choose h in A_1 with dh=1 and adjoin the stabilization a,b, |a|=1, |b|=2, da=0, db=a. In the successive free coordinate systems set

    a'=a+h,
    r'_j=r_j-a'f_j(x).

Then da'=1 and dr'_j=0. The changes are elementary: h contains no a or b, and f_j contains only x. Express D=db=a in the coordinates x,a',r'; it is independent of b and satisfies dD=0. Replace b by b'=b-a'D. Then db'=D-(D-a'dD)=0. We have obtained the free DGA in which a' has differential 1 and every other displayed generator is a cycle. Both A and B have the same degree counts, so the identical construction on B gives the same normal form. This works over every unital coefficient ring and is finite whenever h exists.

It follows for this constructed pair that

    1 in (f)  <=>  A and B stable tame isomorphic
              <=>  A and B quasi-isomorphic
              <=>  D(A) and D(B) equivalent.

For the source's common-source formulation, if A and B are acyclic, the unital direct-product DGA A times B is acyclic and its two projections are quasi-isomorphisms. The common source is not required to be finite free. The standard tensor stabilization has a contraction on words with a distinguished stabilization letter; its augmentation is a quasi-isomorphism. Thus the stable-tame implication used here is valid in the tensor-algebra case without imposing a new commutative convention.

Applying the external unit-ideal undecidability input gives the known noncommutative conclusion. The group-based second proof in [MR] is useful corroboration, but this report does not rely on transporting Hochschild homology through an arbitrary non-enhanced triangulated equivalence.

## 4. Approach 1: unit-boundary certificates and the zero-object route

### Theorem 4.1 (polynomial–exterior acyclicity criterion)

Let A be a finite polynomial–exterior DGA over a commutative ring R, with arbitrary integer generator degrees and a degree -1 differential. Write P=R[x_1,...,x_e], J=(theta_1,...,theta_o), and

    q_j = d(theta_j) modulo J, in P.

Then the following are equivalent:

(a) A is acyclic; (b) 1 is a boundary; (c) the ideal (q_1,...,q_o) in P contains 1.

If (c) holds, a degree-one primitive of 1 can be built from a polynomial ideal certificate.

**Proof.** Acyclicity implies (b), since d1=0. If dh=1, left multiplication by h contracts the underlying complex, proving (a). To compare (b) and (c), first note that the even generators have odd differential, hence dx_i belongs to J. Any homogeneous element of degree one is a sum of terms with an odd number of theta factors. Modulo J, its differential can only come from terms with exactly one theta factor. Consequently dh mod J belongs to (q_j), and (b) implies (c).

Conversely take a finite identity 1=sum a_j q_j in P. Every q_j is homogeneous of degree |theta_j|-1. Although degrees of even variables may be zero or negative, each polynomial has finite support. Extract from each a_j its homogeneous component of degree 1-|theta_j|. Taking the total-degree-zero component of the identity preserves 1 and gives a certificate with these homogeneous coefficients. This is a finite extraction, not an appeal to finite-dimensional graded pieces.

Set w=sum a_j theta_j, so |w|=1. Let c=1-dw. The certificate gives c in J, while dc=0. Because J^(o+1)=0, c^(o+1)=0. Therefore

    h = w (1+c+...+c^o)

has degree one, and

    dh = (1-c)(1+c+...+c^o)=1-c^(o+1)=1.

No inverse integer is used. This proves the theorem. If there are no odd generators, the ideal is zero and acyclicity occurs only for the zero coefficient ring, excluded in our decision applications. QED.

For example, let |x|=0, |a|=|b|=1, |c|=-1, dx=c, da=1+bc, db=dc=0. Then h=a(1-bc) is an explicit degree-one primitive of 1. The even-variable differential is nonzero; the theorem is not limited to Koszul complexes.

**Algorithmic corollary.** Unit-ideal membership is decidable in a polynomial ring over an effective field, and over Z by effective strong Gröbner/standard-basis algorithms. Compute the q_j and test the ideal. Thus acyclicity, and equivalence to the zero derived category, is decidable throughout this polynomial–exterior class. The same test is valid for finite fields of odd characteristic, where graded-commutative automatically means polynomial–exterior. No assertion is made here for sign-only free algebras over Z.

In the sign-only characteristic-2 convention the algebra is an ordinary polynomial algebra with a graded derivation. There is a separate elementary criterion: A is acyclic iff 1 belongs to the ordinary ideal generated by all d(generator). Necessity follows from the derivation rule. If 1=sum a_j d b_j, squaring in characteristic 2 gives 1=sum a_j^2 (d b_j)^2. Since every square is a cycle and d^2 b_j=0,

    1 = d(sum a_j^2 b_j d b_j).

Extracting the degree-one component gives a homogeneous primitive. Hence this convention also has a decidable acyclicity problem over an effective characteristic-2 field. This is not an identification of the two characteristic-2 categories.

**Attribution and mechanism.** Rizell [R, Proposition 1.3] gives a related characteristic-algebra/acyclicity criterion in supercommutative settings. The argument here explicitly records finite odd-ideal nilpotence and the integer-degree extraction needed in this target. It claims no novelty over that literature.

**Exact remaining gap.** The theorem decides only equivalence to the zero object. General pairwise equivalence is not reduced to this test. A uniform construction converting arbitrary pairwise quasi-isomorphism or derived equivalence into acyclicity in this same finite polynomial–exterior class would now give an algorithm, but no such construction is supplied. For stable tame equivalence, even the homology-preserving stabilization convention must first be fixed. This route is blocked as a direct transfer of [MR]'s zero-object undecidability reduction.

## 5. Approach 2: Diophantine augmentations and attempted rigidification

For an integer polynomial f in Z[x_1,...,x_n], define

    K_f=Z[x_1,...,x_n] tensor Lambda(e), |x_i|=0, |e|=1,
    dx_i=0, de=f.

An augmentation K_f -> Z sends x_i to an integer a_i and e to zero. It is a chain map exactly when f(a_1,...,a_n)=0. This is a bijection, not merely an implication. The construction is effective and d^2=0. The Davis–Putnam–Robinson–Matiyasevich theorem therefore implies that augmentation existence for these finite polynomial–exterior DGAs is undecidable. Over any effective field k the same construction identifies augmentation existence with rational-point existence over k; over F_q it is decidable by checking the q^n tuples. No undecidability over Q is inferred from the integer result.

Augmentation existence is invariant under any elementary DGA isomorphism and under the literal canceling-pair stabilization: an old augmentation extends by setting both new generators to zero, and restriction gives an old augmentation. This observation alone cannot prove equivalence undecidable. A decidable equivalence relation can have an undecidable union of equivalence classes; equality of integer encodings versus a halting subset is a simple abstract example.

We attempted to rigidify augmentation existence by comparing K_f with a fixed target representing a root. The simplest such comparison already fails. For f=x^2-1, integer roots exist, but K_f is not quasi-isomorphic to Z: after rationalization H_0 is Q[x]/(x^2-1), which is Q times Q, not Q. Thus a root does not collapse all components or all homology. Conversely f=x^2+1 has no integer augmentation but its unit ideal is proper and K_f is not acyclic. The predicates 'a root exists' and 'the unit is a boundary' are genuinely different.

Nor does merely adjoining a variable that selects an augmentation solve the problem: it constructs an existential parameter space, whereas the equivalence question compares two fixed finitely encoded DGAs. A useful reduction would need a uniform pair (A_f,B_f) for which an unspecified integer root produces a tame/quasi/derived equivalence and every such equivalence recovers a root, while preserving finite freeness. No such rigidity theorem or gadget has been proved here.

**Strongest result:** the exact augmentation-undecidability reduction above.  
**Gap:** an equivalence-versus-root biconditional, with both directions and no unbounded extra generators.  
**Disposition:** blocked; this is a different arithmetic mechanism from unit-ideal membership.

## 6. Approach 3: complete intersections and finite resolutions

Let P=R[x_1,...,x_n] with all x_i of degree zero. For a sequence f=(f_1,...,f_m), form the Koszul DGA

    K_P(f)=P tensor Lambda(e_1,...,e_m), |e_j|=1, de_j=f_j.

### Proposition 6.1

If f is a regular sequence, the augmentation K_P(f) -> P/(f) is a quasi-isomorphism. Consequently for regular-sequence presentations S=P/(f) and T=Q/(g),

    K_P(f) quasi-isomorphic to K_Q(g)  <=>  S isomorphic to T

as coefficient algebras.

**Proof.** For m=1, the Koszul complex is P --f_1--> P, and injectivity follows from the non-zero-divisor hypothesis. Inductively, adjoining e_m forms the mapping cone of multiplication by f_m on the previous Koszul complex. The long exact homology sequence and regularity of f_m modulo the earlier f_i imply zero positive homology and degree-zero homology P/(f). This also covers m=0. The forward implication of the biconditional follows by applying H_0 to a quasi-isomorphism zigzag. For the converse use the quasi-isomorphisms to S and T and the ring isomorphism. In the source's common-source language, identify S with T and take the degreewise fiber product K_P(f) times_S K_Q(g). Both projections are surjective quasi-isomorphisms because their kernels are the acyclic kernels of the opposite augmentations. Thus the precise common-source formulation is met, without requiring that the common source have finitely many free generators. QED.

The standard regular-sequence input is also recorded in [Stacks, Tag 062F]. An isomorphism of S and T is sufficient for derived Morita equivalence of these DGAs through the quasi-isomorphisms. We do not use an unproved converse for the source's most general triangulated-category formulation.

### Why arbitrary presentations do not give the same reduction

Take P=Q[x,y], f_1=x^2, f_2=xy. In K_P(f),

    z=y e_1-x e_2

is a cycle. Every degree-two element is a multiple of e_1e_2, and

    d(e_1e_2)=x^2 e_2-xy e_1=-x z.

Thus z is not a boundary: equality z=-p x z would force 1=-px in the domain P by comparing the e_2 coefficient. Adjoining a generator to kill z raises a new resolution problem and need not terminate with finitely many generators. Even more simply, K_Q[x](x) and K_Q[x](x,0) have the same H_0=Q but the latter has a nonzero H_1 class from the redundant relation. Equality of presentation quotient rings is not enough for arbitrary Koszul models.

A concrete solved subfamily is K_Q[x](x^n), n>=1. Its H_0=Q[x]/(x^n) has Q-dimension n, so two such DGAs are quasi-isomorphic exactly when their n agree.

**Exact remaining gap.** General isomorphism of finitely generated commutative algebras is not known here to be undecidable, and restricting to complete intersections is an additional unsupported step. Poonen [P, Section 13.1] explicitly recorded the open status of the general ring-isomorphism problem in his dated survey; we have not found a current primary theorem justifying the needed stronger assertion. Therefore the proposition is a faithful reduction to a difficult algebraic classification problem, not a completed undecidability proof. This route must not be promoted using an unattributed claim that affine-scheme isomorphism is 'famously undecidable.'

## 7. Approach 4: effective map spaces and certificate enumeration

### Proposition 7.1 (finite-field positive-degree strict isomorphism)

Fix a finite field. For finite-generator polynomial–exterior DGAs all of whose generators have strictly positive homological degrees, strict DGA isomorphism is decidable.

**Proof.** In either target algebra, each homogeneous component of any specified degree is finite-dimensional: the exponent of a positive-degree generator in a monomial is bounded by that degree divided by the generator degree, and odd exponents are at most one. The component is consequently a finite set over the finite field. Enumerate all degree-preserving choices of images for the finitely many generators of A and B. They extend to graded algebra maps, with the strict relations checked when required. Keep only choices commuting with d on generators. For each pair f:A->B and g:B->A, test gf and fg on generators. All checks are finite polynomial identities. Existence of an inverse pair is equivalent to strict DGA isomorphism, and all choices are finite, proving termination with both YES and NO. QED.

This is an isomorphism algorithm, not a quasi-isomorphism algorithm. No unproved assertion that quasi-isomorphic finite positive-generator objects must be strictly isomorphic is made. Minimal-model arguments require their own characteristic, connectivity, and differential conventions; the source's brief Sullivan remark is not applied wholesale over Z or finite fields.

For infinite fields the same bounded-degree parametrization produces finitely many polynomial equations in coefficients for inverse maps. Whether they have solutions is a field-specific arithmetic question, not automatically decidable over Q. For zero-degree generators or mixed positive/negative even generators, homogeneous components need not be finite-dimensional at all: every x^m has degree zero if |x|=0, and every x^m y^m has degree zero for |x|=2, |y|=-2. Thus the proof does not extend by retaining the same finite enumeration.

### Proposition 7.2 (positive semidecision for stable tame equivalence)

Over Z or an effectively presented countable field, the literal stable tame equivalence relation is recursively enumerable, under either effectively specified free graded-commutative convention.

**Proof.** Enumerate finite lists of stabilization degrees on the two sides, finite elementary transformations and permissible generator permutations, and coefficient expressions. For unit scalings enumerate a coefficient together with an inverse and check their product is one; no oracle for recognizing units in a more general computable ring is necessary. Differential preservation and equality of finite generator images are finite syntactic algebra checks. An accepted word is a genuine certificate of stable tame equivalence. If an equivalence exists by definition, one finite certificate eventually appears. If none exists, this procedure may run forever. QED.

There is no established recursive bound here on stabilization number, stabilization degree, elementary-word length, or polynomial degree. Failing to find a certificate up to a finite bound cannot be reported as inequivalence. Combining a YES semidecision procedure with an infinite collection of obstructions is not a decision algorithm unless every NO instance is guaranteed to trigger one effectively.

The checker exhausts a small complete finite-field example: over F_3, with a,b in degree 1 and c in degree 3, compare dc=ab with dc=k ab. The full enumeration gives 48 strict isomorphisms for k=1 or 2, and none for k=0. It is exhaustive only for this finite map space, not evidence for a universal bound.

**Exact remaining gap:** a complete effective negative certificate or a proven bound on the required equivalence data. This route is algorithm construction and semidecision, distinct from the preceding arithmetic and ring-presentation reductions.

## 8. Approach 5: mixed degrees, derivations, and Massey obstructions

Work over Q. For n>=1 define the finite polynomial–exterior DGA

    A_n=Q[x,z] tensor Lambda(y), |x|=|z|=0, |y|=-1,
    dx=dy=0, dz=x^n y.

The derivation squares to zero: d^2 vanishes on generators, and the graded derivation calculation gives d^2=0 on the algebra. Explicitly,

    d(p(x,z))=x^n (partial p/partial z)y,   d(p(x,z)y)=0.

Since Q[x,z] is a domain and partial/partial z is surjective as a Q[x]-linear map,

    H_0(A_n)=Q[x],
    H_(-1)(A_n)=(Q[x,z]/(x^n)) y,
    H_i(A_n)=0 otherwise.

The H_0-action on H_(-1) has annihilator exactly (x^n): inclusion in the annihilator is immediate; testing against the class of y gives the converse. Therefore

    dim_Q(H_0/Ann(H_(-1)))=n.

Any graded homology-algebra isomorphism preserves this number. Consequently A_n and A_m are quasi-isomorphic if and only if n=m. The reverse implication is the identity. Over Q, where the literal polynomial–exterior stabilizations are quasi-isomorphisms, the same classification holds for stable tame equivalence: different n are obstructed by homology, and equal n are identical. No classification of their derived categories as arbitrary triangulated categories is asserted.

### Proposition 8.1 (nonformality)

Every A_n is nonformal: it is not quasi-isomorphic to its own homology algebra equipped with zero differential.

**Proof.** Take homology classes represented by a=y, b=x^n, c=y. Their adjacent products are boundaries, both equal to dz. In homological convention, if ab=du and bc=dv, a triple Massey representative is

    a v + (-1)^(|a|+1) u c.

Here |a|=-1 and we choose u=v=z, obtaining 2zy in degree -1. Its full indeterminacy is

    [y]H_0(A_n)+H_0(A_n)[y]=Q[x]y

inside (Q[x,z]/(x^n))y. The class of 2zy does not lie in that submodule: reduction modulo x^n leaves a nonzero z term over Q. Thus this triple Massey product does not contain zero. In the zero-differential homology algebra the same adjacent products vanish as actual products, so primitives u=v=0 are allowed and the corresponding triple contains zero. Triple Massey products, including whether zero belongs to the full coset with its indeterminacy, are preserved by quasi-isomorphisms. This follows by applying a chain map to a defining system, and for a quasi-isomorphism lifting cycles and correcting boundary differences; the changes are exactly the stated indeterminacy. Therefore no quasi-isomorphism zigzag can identify A_n with its homology algebra. QED.

This route generalizes as follows. Any polynomial derivation delta on P=Q[x_1,...,x_s] gives a DGA P tensor Lambda(y_-1), d(p)=delta(p)y, dy=0. Its H_0 is ker(delta), and H_(-1) is coker(delta) times y, with the induced ker(delta)-module structure. This directly embeds differential-invariant computations into the mixed-degree target. The construction is finite; the kernel and cokernel need not come with a finite effective classification. We do not replace that missing classification by a Hilbert-series guess or assume that homology is finitely generated.

**Strongest result:** explicit full quasi-isomorphism and rational stable-tame classification of the A_n subfamily, together with an explicit nonformality obstruction.  
**Exact remaining gap:** no complete invariant or undecidability reduction for arbitrary polynomial derivations, and no route from these homological invariants to the full derived-Morita question. This constitutes genuine mixed-degree proof work, but only on a separately labeled subfamily.

## 9. What was tested, and what was not

The accompanying standard-library checker uses exact rational arithmetic and exact modular arithmetic. All correctness guards are explicit exceptions or conditional checks, not Python assertions. It checks algebra signs, Leibniz identities, d^2, a noncommutative normal-form automorphism and its two-sided inverse, the unit-primitive correction, the Koszul syzygy, the stabilization boundary coefficients, finite-field augmentation examples, a complete finite map-space enumeration, and the A_n derivative and Massey formulas. Tests include deliberately invalid differentials/certificates to ensure rejection paths actually run.

Runs in normal, -O and -OO modes use actual UID 1000, read-only packet/source inputs, denied append/create probes, and output files outside the frozen input directories. The validation receipt records the actual results and optimization-invariance comparison. The frozen packet is content-addressed by SHA-256; read-only permissions prevent ordinary writes during tests. This is a reproducibility snapshot, not a claim of privileged filesystem immutability against its owner.

Finite identities and finite examples corroborate implementations. The universal statements are supported by the written proofs, not extrapolation from tests. Source hash checks establish bytes inspected, not mathematical correctness or peer review. Missing source files are explicitly NOT_RUN, never PASS. No copied primary-source body, private corpus body, or private coordination material is in this packet.

## 10. Final accounting and boundary

Exactly five substantive approaches are recorded in APPROACHES.json. The known noncommutative theorem reconstruction, literature triage, convention audit and tests count zero. All five approaches produced proved intermediate statements but left the general graded-commutative stable-tame, quasi-isomorphism and derived-Morita decision problems unsettled. The appropriate queue outcome is **exhausted, 5/5**, with the known noncommutative resolution credited and the commutative remainder explicit. No candidate full solution is proposed.

## References

[K3] R. I. Baykur, R. C. Kirby, D. Ruberman (eds.), *K3: A New Problem List in Low-Dimensional Topology*, AMS Mathematical Surveys and Monographs 295 (2026), Problem 5.16, printed pp. 313–315. Author's preliminary version: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

[MR] C. Manolescu and N. Rozenblyum, *Undecidability problems for semifree DG algebras*, arXiv:2605.08122v1 (2026). https://arxiv.org/abs/2605.08122 ; author's PDF https://web.stanford.edu/~cm5/dgas.pdf . Known result, not a result of this packet.

[R] G. Dimitroglou Rizell, *Nontriviality results for the characteristic algebra of a DGA*, Math. Proc. Cambridge Philos. Soc. 162 (2017), 419–433. https://arxiv.org/abs/1512.03570 ; https://doi.org/10.1017/S0305004116000645 . Proposition 1.3 and Section 2 are relevant; their stated grading/field/filtration hypotheses should not be discarded.

[B] L. A. Bokut', *Unsolvability of certain algorithmic problems in a class of associative rings*, Algebra i Logika 9:2 (1970), 137–144. https://www.mathnet.ru/eng/al1237 . Russian original; foundational undecidability input, not independently reconstructed here.

[P] B. Poonen, *Undecidable problems: a sampler*, in *Interpreting Gödel* (2014), 211–241, especially Sections 2 and 13. https://math.mit.edu/~poonen/papers/sampler.pdf . A dated survey, not evidence that no subsequent theorem exists.

[Stacks] The Stacks Project, Lemma 15.31.2, Tag 062F, regular sequences are Koszul-regular. https://stacks.math.columbia.edu/tag/062F . The elementary induction used here is supplied in Section 6.
