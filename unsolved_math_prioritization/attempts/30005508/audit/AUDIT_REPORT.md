# Independent audit: projective characters and square roots in real blocks

**Problem:** 30005508 / OWR-13750328-013  
**Date:** 3 October 2026  
**Verdict:** **PASS — scoped partial results; the general problem remains unresolved.**

The five-approach record is mathematically coherent within its stated scope. I found no blocking error in the central-quotient reduction, the all-defect-pair model calculation, the direct-product theorem, or the nonnilpotent order-864 example. None proves the universal conjecture. The exact outstanding statement is the involution-orbit formula for arbitrary real nonprincipal blocks with one simple module. Keep the record unresolved, with five approaches completed, and make no general-solution or novelty claim.

The frozen author files were not edited. Their exact checker was rerun and its JSON output agrees with the recorded output. The additional independently written program in this directory does not import that checker or its results.

## 1. Source and scope checks

The original statement is Conjecture 4 in Benjamin Sambale's contribution to [Oberwolfach Report 19/2023](https://doi.org/10.4171/owr/2023/19), printed page 1056. The adjacent Theorem 3 concerns Conjecture 2, a different assertion about nilpotent-block indicators. It does not settle Conjecture 4.

The published [dihedral-block paper](https://doi.org/10.1017/S0004972723000436), Section 3, labels the involution-orbit statement Conjecture 3.2. Theorem 3.3 deduces the scalar indicator identity from it. Lemma 4.1 treats the entire square-root permutation module; Proposition 4.2 proves an aggregate identity under nilpotent abelian local-defect hypotheses. The following paragraph states a local orbit formula, without a proof. The report correctly distinguishes these levels and the different numbering in the author's preprint.

Theorem 13 of [Real characters in nilpotent blocks](https://doi.org/10.1007/s10013-023-00623-5) uses the quotient defect-pair assertion. I also checked its underlying source directly: John Murray, [Real subpairs and Frobenius–Schur indicators of characters in 2-blocks](https://archive.maths.nuim.ie/staff/jmurray/Preprints/jmurrayRealSubpairs.pdf), Lemma 1.7 and the remark immediately following its proof. The lemma provides a real dominated quotient block with the image defect pair. The following uniqueness condition applies here because the factored subgroup is central.

A targeted current source search found no general resolution. This is a limited negative search, not a proof that no resolution exists.

## 2. The central-quotient reduction survives adversarial checks

Use the notation of Approach 2: H=C_G(x), Z=〈x〉, C=C_H(y), and K the inverse image of C_(H/Z)(yZ), where y²=x. Assume first that the local block b is real.

### Block and projective issues

- Z is a central 2-subgroup contained in P=C_D(x). Central 2-subgroup quotient correspondence gives a unique dominated block, preserves simple modules by inflation, and preserves the principal block. Thus the quotient block is real, nonprincipal, and has one simple module.
- Murray's quotient result gives its actual defect pair (P/Z,Q/Z). This is not an assertion about abstractly isomorphic defect groups in unrelated ambient groups.
- The ordinary projective character upstairs must not be identified with an inflated projective character downstairs. The author's argument makes no such identification.
- There is also a valid modular deflation statement: if U is the projective cover of S, then k(H/Z)⊗_(kH)U is projective and has exactly the same simple head downstairs. Projectivity follows by applying tensor product to a splitting of U from a free kH-module; the head multiplicities follow from the Hom adjunction. It is the quotient projective cover. Its degree generally differs from U's.

### Stabilizer and index issues

Since h∈K fixes x and sends y to yx^j, the equation (yx^j)²=x gives x^(2j)=1. Hence there are at most two possible images of y. The homomorphism from K to automorphisms of 〈y〉 has kernel C. Therefore C is normal in K and t=[K:C] is 1 or 2. This holds also when x=1, when t=1.

Crucially, C/Z need not be the full quotient centralizer. It is normal in K/Z=C_(H/Z)(yZ), with quotient K/C. The proof retains this enlargement throughout.

As an H/Z-set, y^H is (H/Z)/(C/Z). Inducing in two stages through K/Z produces an inner permutation module inflated from the regular module of the 2-group K/C. Its composition factors are exactly t trivial factors. Exactness of induction gives the Grothendieck-group identity

[k[y^H]] = t[k[(yZ)^(H/Z)]].

Taking the appropriate simple-module coefficient proves the stated restricted-projective multiplicity identity. This is a composition-factor identity, not an assertion that the two permutation modules split into isomorphic direct summands.

### Orbit intersections and converse

Every fiber of y^H→(yZ)^(H/Z) has size t. Because Z≤P≤Q, membership in Q\P is constant across all lifts of a quotient point. Consequently the right-hand intersection count also scales by t. No normalizer, centralizer, or fusion index has been omitted.

For x≠1, yZ has order exactly 2. For x=1 the statement is already the involution-orbit conjecture, with y=1 handled separately. If b is nonreal, the stated local-pair hypothesis makes Q=P, and the square-root-module vanishing argument applies. A principal local block could not induce the stipulated nonprincipal global block, by Brauer's third main theorem.

Thus the two universal assertions really are equivalent: the involution formula on all real nonprincipal one-simple blocks implies every local square-root formula; specialization to x=1 gives the converse. This equivalence is a valid reduction, not a solution.

## 3. Other proved partial results

### Orbit-module and zero-case argument

Projective/Brauer duality turns the character inner product into a composition multiplicity in the orbit permutation module. The nonnegativity argument correctly descends vanishing of the whole root module to each orbit. The identity-root case and the nonreal local-block case are valid. For a root central in H, one may also note directly that a central 2-element lies in every defect group of H.

An aggregate scalar cannot recover its individual nonnegative summands. The packet never promotes that scalar to the desired orbitwise identity.

### The C3⋊E family

For every index-two pair D<E of 2-groups, the central idempotent attached to the two nontrivial C3 characters supports precisely the two-dimensional simple module. The real defect class {a,a⁻¹} yields the actual pair (D,E). For x∈D, the local group is C3⋊C_E(x); its local block is real exactly when C_E(x)>C_D(x), otherwise the two choices are nonreal conjugate blocks.

Inducing a nontrivial C3 character gives a projective with simple head of multiplicity one, so it is the claimed projective indecomposable. If a root lies in D, its centralizer contains C3 and the character average is zero. If it lies outside D, C3-conjugation reduces to a root e∈E\D, its centralizer is C_E(e), and both quantities are |C_E(x):C_E(e)|. These statements do not assume a split extension or an abelian D.

This proves every admissible subsection in these models. It does not transfer to arbitrary blocks having the same abstract pair.

### Direct products with 2-groups

The product defect pair, subsection block, and centralizers all split as stated. The projective factor contributed by C_T(z) is its regular character. Restriction contributes the index [C_T(z):C_T(w)], while the orbit-intersection side acquires the same index. It is positive, so equivalence follows in both directions. No compatibility with an arbitrary Morita equivalence is assumed or needed.

## 4. The order-864 example: block identification independently certified

The original script correctly evaluates a supplied class function, but that alone would not establish that it is the unique projective character of an actual block. The proof in Approach 5 supplies the missing representation-theoretic identification. The independent controls strengthen this by checking an explicit block certificate.

### Group and representation certificate

The control program constructs Q, H=Q⋊C2, and the action on V=F2^4 independently. It checks every associativity triple in H and every pair of action operators on every vector. These exact checks certify the semidirect-product construction of G=V⋊H, of order 864.

Over F4, with a primitive cube root w, it builds the degree-three matrices

ρ(a,b,c)e_j = w^(c+aj)e_(j+b), with indices modulo 3.

All Q multiplication relations are verified, and the matrices span the full nine-dimensional matrix algebra. The induced six-dimensional representation of H is then verified on every pair of elements; its matrices span the full 36-dimensional matrix algebra. These span identities remain true after extending the field, so the representations are absolutely irreducible.

The element e=z+z² is verified to be a central idempotent. Its regular-action rank on kH is 36 and it acts as the identity on the six-dimensional representation. Hence e kH maps onto a 36-dimensional full matrix algebra and is itself that algebra. In particular, it has exactly one simple module.

Every simple kG-module is trivial on the normal 2-subgroup V. Therefore e supports exactly one simple module in kG as well; it is a primitive central block idempotent. It is fixed by inversion and acts as zero on the trivial module, certifying reality and nonprincipality. This avoids the false general inference that an arbitrary normal-2-subgroup quotient automatically gives a bijection of all blocks.

### Actual defect pair and nonnilpotence

The class {z,z²} is the support of e, and its class sum acts as the identity on the simple module. Thus it is a real defect class. Its centralizer has order 432; its extended centralizer is G. The exhibited 2-subgroups D and E have orders 16 and 32 respectively and are Sylow in those two centralizers. This certifies the actual defect pair.

The program verifies C_G(D)=D×〈z〉, of order 48, and explicitly constructs the primitive central idempotent over a nontrivial character of 〈z〉. Its stabilizer has order 432. Thus the inertial quotient has order 9 (and is Q/〈z〉≅C3×C3), establishing nonnilpotence.

### Actual projective character and six orbit tests

Induction from the odd-order subgroup Q is projective. Its restriction/Hom calculation gives the sole simple module once in its head, so Ind_Q^G ρ is the unique projective indecomposable. The independent program recomputes this induced ordinary character for every element using exact pairs of integers in Z[ζ3], rather than assuming the values in the author's checker. It obtains degree 96, value −48 on z and z², and zero elsewhere.

The complete orbit results are:

| Class size | Centralizer order | Multiplicity | Intersection with E\D |
|---:|---:|---:|---:|
| 1 | 864 | 0 | 0 |
| 3 | 288 | 0 | 0 |
| 3 | 288 | 0 | 0 |
| 9 | 96 | 0 | 0 |
| 18 | 48 | 2 | 2 |
| 54 | 16 | 6 | 6 |

The 88 elements comprise all elements whose square is 1, including the identity. These checks establish the x=1 assertion for this block. They do not enumerate every local subsection of this group.

## 5. Additional independent controls and limitations

Run `python3 independent_controls.py`. It uses only the standard library and exact finite-field, integer, and rational arithmetic.

In addition to the block certificate above, it checks all index-two subgroups of E=C2,C4,C8,D8,Q8 in the C3⋊E construction: nine pairs, 31 element-indexed subsections, and 124 individual root tests. These include nonreal local blocks and nonsplit extensions.

There are 66 positive actual-block quotient tests. Cyclic models give t=1. Dihedral and quaternion models give t=2, with original multiplicity/intersection 2 and quotient multiplicity/intersection 1. Thus the nontrivial multiplier is tested inside genuine nonprincipal blocks, not only in bare 2-groups. The program additionally compares the two permutation characters on all odd-order elements, independently checking the relevant Grothendieck identity in these examples.

These tests supplement the proofs; they are not exhaustive over finite groups. Neither a finite search nor the source-status search supplies a general proof. There is no claim of a new theorem's priority, a new example's priority, or identification with a particular SmallGroup library entry.

## 6. Final disposition

**Accept the packet as an audited unresolved research record with valid scoped partial results.** No mathematical correction is required for that scope. Do not label the original problem solved, do not replace the involution-orbit conjecture by a scalar result, and do not treat this audit's stronger finite certificates as a proof of the universal statement.
