# Independent audit: genus-two real-multiplication Galois images

Problem 30001840 / OWR-11127-008. Audit date: 2026-10-07 UTC.

## Verdict

**Accept the five stated mathematical partial results, with their stated generic/base-field qualifications. Do not mark the broad original question solved.** No false mathematical conclusion was found in the frozen proof. Its most demanding steps, the split-prime product argument and integral lifting for every prime at least seven, survive independent checking. The accompanying proof expansion supplies details that were compressed in the original.

There is one concrete reproducibility defect: every acceptance check in the original `checks.py` is a Python assertion. Real optimized execution removes those checks. Nine deliberately false mathematical mutations are all accepted by the original program under `python -O`. The supplied corrected program retains its checks under optimization and rejects all nine. This defect does not invalidate the mathematical proof, which explicitly does not depend on the finite samples.

The original public directory has not been edited. `PROOF_CORRECTED.md`, `checks_corrected.py`, and `PROPOSED.patch` are reviewable derivative artifacts. The proof changes are expansions of valid arguments, not a retraction or weakening of the local-image theorems. The program changes repair the optimization defect. Applying the patch to a derivative packet requires regenerating that packet's manifest; the original freeze should remain intact.

## Freeze and inspection

- Original `PROOF.md`: SHA-256 `d352e5e64774e1b6afd50194a3bd0a1eafd2e0789abaf536f9dd082e34d7a627`.
- Original `MANIFEST.json`: SHA-256 `2b46f6cf67e9de36ca809237f1281d0fcc0288e03ab03c805a947a4cd5882d09`.
- All fourteen files listed in the original manifest match their recorded hashes and sizes.
- All eight scholarly PDFs match the source manifest's recorded hashes and sizes. These were supplied local copies; this audit does not represent them as new network retrievals.
- All five turn records, the complete consolidated proof, readme, author self-audit, source audit, manifests, ledger, and finite-check program were read.
- The entire Kohel contribution and its references were read in the official Oberwolfach report. The entire Darmon–Mestre article and Tautz–Top–Verberkmoes article were read. Takei's invariant definitions, proposition, and proof were read; the cited finite-group statements and contextual later results were inspected within their actual scopes. Key original-report, Darmon–Mestre, and Takei formula pages were also visually inspected.

The audit files contain authored analysis, code, public bibliographic metadata, hashes, sizes, and test results. They contain no third-party source documents, extracted source text, dataset contents, or private coordination material. No remote writes or publication were performed.

## Source question and the accepted scope

The governing report is *Explicit Methods in Number Theory*, Report 35/2011, DOI [10.4171/OWR/2011/35](https://doi.org/10.4171/OWR/2011/35). Kohel's contribution, printed pp. 1998–2000, uses the curve with the coefficient **minus** five on the cubic term. It distinguishes the moduli image, exceptional finite levels, and a Tate-module image. Its displayed arithmetic representation is of the absolute Galois group of the rationals, with no chosen rational parameter. The subsequent discussion also averages over a family. There is no justification for silently replacing a fiber representation by generic geometric monodromy.

The audit therefore accepts the following precise statements, not a parameter-uniform arithmetic solution:

1. For transcendental t, the image on J_t[2] is AGL_1(F_5), of order 20, over Q(t); it is D_5, of order 10, geometrically and over Q(sqrt(5))(t).
2. At three the generic geometric **linear** image has order 120, the full central inverse image of projective A_5 in SL_2(F_9).
3. For every rational prime ell at least seven, the generic geometric integral image is SL_2(O_K tensor Z_ell).
4. At the same primes, the arithmetic image over K(t) is the R-linear group of scalar R-determinant, and the arithmetic image over Q(t) is the full RM normalizer in the polarized symplectic-similitude group.
5. The coarse geometric moduli image has rational parameter t squared. The smooth fiber t=0 has arithmetic mod-two image C_4 and one nonzero rational two-torsion class, disproving uniform assignment of the generic image to every rational fiber.

The historical turn files remain useful provenance. Their conclusions agree with the consolidated proof. This acceptance is an independent mathematical audit of the stated packet, not peer review, a novelty certificate, or a global literature-status theorem.

## Approach 1: two-torsion

### Chebyshev identity and splitting field

The identity f(u+u^-1)=u^5+u^-5 is exact. The independent program verifies it symbolically in a Laurent-polynomial ring rather than by sampled substitution. The rational function t=-(u^5+u^-5) has degree ten, and adjoining fifth roots of unity gives a degree-forty Galois extension of Q(t). The forty substitutions stated in the proof are distinct and fix t.

On the five roots, the action is indeed i -> ea i+eb. Its kernel consists of the identity and simultaneous inversion of the root of unity and u. Thus the splitting field is the indicated fixed field and has affine group of order twenty. The constant field of the larger rational-function field is Q(zeta_5); intersecting its constants with the fixed field gives the real quadratic field. Passing to K(t) or to algebraically closed constants leaves the dihedral order-ten subgroup.

### Passage to J[2]

For the six branch points, including infinity, the usual even-subset construction gives a four-dimensional F_2-space. The five finite-branch divisor classes have their sole relation equal to their sum. A permutation of the five finite roots acts faithfully on that quotient, so no additional kernel changes the division field. The order-five subgroup has no nonzero fixed vectors on the quotient. Independent enumeration confirms faithfulness of the entire S_5 action and a zero-dimensional fixed space for the five-cycle; these finite confirmations are not needed for the argument.

The discriminant is 3125(t^2-4)^2. It agrees with an independent exact symbolic product of squared branch differences. Thus the stated characteristic-zero singular parameters are exactly plus and minus two. The rational Weierstrass section supplies no nonzero generic two-torsion class. This does not deny other level or theta-characteristic structures.

**Accepted without mathematical correction.**

## Approach 2: projective and linear residual images

The family identification is C_1(s), with s=-t/2, in Darmon–Mestre, not the sextic C_2. Their construction parameter r is five, while their torsion prime p becomes the varying ell. The standing exclusions are therefore ell different from two and five. Proposition 2.1 supplies the RM action over K and its nontrivial Galois descent. Proposition 3.1(1) explicitly supplies the exceptional projective A_5 at ell=3 and the stated full projective groups at the other covered prime ideals. No result about the twisted C_2 construction in Section 4 is needed.

The central-lift argument is valid in odd characteristic. A lift h of a nonidentity projective involution has h squared scalar. Since h has determinant one, that scalar is plus or minus one. If it were plus one, h would be diagonalizable with eigenvalues in {1,-1}; determinant one then makes it scalar. Hence h squared is minus the identity. The subgroup contains the full scalar kernel and equals the inverse image of its projective image. The exceptional group has order 120, whereas SL_2(F_9) has order 720. Confusing its order with sixty would incorrectly discard the center.

Independent multiplication and enumeration confirm the stated order fingerprint. The ring at five is nonreduced, not F_25. Neither those matrices nor the residual theorem alone identify a full integral Jacobian lattice at the exceptional primes.

**Accepted without mathematical correction.**

## Approach 3: integral geometric images

### The integral RM module

Darmon–Mestre, printed p. 308, first identifies rational Betti homology as a two-dimensional K-vector space. Comparison with etale cohomology is compatible with algebraic endomorphisms. Hence the rational ell-adic module has rank two over K tensor Q_ell. For ell at least seven, R=O_K tensor Z_ell is a product of unramified discrete valuation rings. Each integral factor is finitely generated and torsion-free over its DVR and has fraction-field rank two. Therefore each factor is free of rank two, and so is the R-module.

The RM correspondence is symmetric under transposition: transposition inverts the fifth-root automorphism, and the quotient construction identifies this inverse correspondence with the original one. It is therefore self-adjoint for the canonical principal polarization. Thus the perfect alternating Weil form is R-balanced. In an R-basis, balancedness and alternation show that it is phi(det(v,w)) for one Z_ell-linear functional phi on R. Perfectness of the unramified trace pairing gives phi(c)=Tr(beta c), for beta in R. Perfectness of the polarization forces beta to be a unit in every factor. This proves the exact determinant-one target, not merely a rational algebraic-group containment.

The corrected proof records these details explicitly. It does not rely on an identification between the displayed abstract U,V group and a global integral lattice.

### Split primes and Goursat

Separate prime-ideal surjectivity is insufficient. In a proper subdirect product of two SL_2(F_ell) factors, Goursat gives a common nontrivial quotient. Simplicity of PSL_2 and perfectness of SL_2 leave an SL_2 graph or a PSL_2 graph. Both identify the projectivized representations. There is no residual determinant or abelian quotient left to impose a different central entanglement.

For a prime field, every automorphism of PSL_2 is induced by PGL_2; the cited Kucharczyk propositions support exactly this statement. Such automorphisms preserve squared trace. The infinity element used in the comparison is genuinely common to both factors: the source fixes its K-valued trace on rational Betti homology **before** prime-ideal reduction. Its traces in the two embeddings are minus w and minus w prime. Their squares differ by minus sqrt(5), which is nonzero at every split prime under consideration. Thus both graph possibilities are impossible.

The independent mod-eleven control has two projections of order 1320 and joint order 1320 squared. The two squared traces are nine and five. This is a concrete check of the obstruction, not a proof for all split primes; the all-primes argument is the Goursat/trace argument above.

### Arbitrary-lift powering

The proof correctly handles an arbitrary lift, rather than presuming a unipotent lift actually lies in H. For u=I+E_12 and h=u+pA, the first-order expansion is

h^p = u^p + p sum u^j A u^(p-1-j) modulo p squared.

After reduction modulo p, every entry in the sum is a polynomial in j of degree at most two. Sums of 1, j, and j squared vanish for p at least five, including in every residue-field extension. Hence the result is I+pE_12. In other product factors an element reducing to the identity has p-th power equal to the identity modulo p squared. Full joint residual surjectivity supplies this individually supported lift in each factor.

The first layer is an F_p-vector space stable under the full residue group. Diagonal conjugation gives square multiples of E_12; every field element is a difference of two squares in odd characteristic. Weyl and lower-unipotent conjugations then give both off-diagonal directions and the diagonal direction, with all residue-field coefficients. Factor support is preserved, so there is no diagonal Lie-subspace obstruction. Higher layers follow by p-th powers, induction, and closedness.

The bound matters. Modulo nine, the determinant-one matrix [[1,1],[3,4]] reduces to I+E_12, but its cube is [[1,6],[0,1]], not I+3E_12. The exact lifting lemma is therefore not silently applicable at three. Exhaustive checks of all p-cubed determinant-one lifts at p=5 and p=7 pass; at p=3, eighteen of twenty-seven lifts violate the claimed larger-prime congruence.

**Accepted. The expanded proof removes compressed lattice, product, and lifting details; no theorem is weakened.**

## Approach 4: arithmetic reconstruction

The trace-form argument identifies the centralizer in GSp exactly with the R-linear matrices whose R-determinant is a diagonal Z_ell unit. This determinant equals the polarization multiplier, hence the cyclotomic character.

For ell different from five, K cannot be contained in the ell-power cyclotomic extension: K is ramified at five and the latter extension is unramified there. Since K is quadratic, the intersection is Q. The cyclotomic image of G_K is therefore all Z_ell units. The constants exact sequence transfers this to K(t). Containing the geometric determinant kernel and surjecting onto its determinant quotient gives the entire stated centralizer group.

Arithmetic over Q(t) normalizes R. The kernel of its action on R is exactly the same centralizer. The Z_ell-algebra R has only two automorphisms: the unramified quadratic involution in the inert case, or factor exchange in the split case. RM descent gives an actual arithmetic element inducing the nonidentity automorphism. A subgroup containing the full kernel and one nontrivial coset is the whole normalizer. There is no missing coset-size or multiplier argument at these primes.

The reasoning is local at one rational prime. It neither establishes independence across primes nor describes the arithmetic image of a chosen rational specialization. In particular, the cyclotomic disjointness argument is not transferable to ell=5.

**Accepted without mathematical correction.**

## Approach 5: moduli and specialization

Takei's parameter is s with the constant term 2-4s; substituting t=2-4s gives exactly the four displayed invariants. The audit independently recomputes their defining root-difference sums in Z[zeta_5][u,u^-1], with the five Chebyshev roots and the branch point at infinity. The fifteen, ten, and sixty term sums give the claimed A, B, and C, and the squared-difference product gives D. Thus the formulas are checked as identities, not inferred from a finite list of rational parameters.

With weights 2,4,6,10, equality of the nonzero constant A forces the square of the scaling parameter to equal one. Its sixth power also equals one, so equality of C forces equal t squared. Conversely, (x,y) -> (-x,iy) gives an isomorphism from C_t to C_-t. The degree-two assertion and the rational image coordinate follow. This only describes the coarse curve image; it does not classify every RM or level marking or characterize a Shimura subvariety.

At t=0 the quartic x^4-5x^2+5 is Eisenstein at five. The formulas for alpha and beta put all four roots in Q(alpha), so this field is the degree-four splitting field. Sending alpha to beta negates sqrt(5), consequently sends beta to minus alpha, and gives an element of order four. Thus the group is C_4, not the Klein four group. The two-torsion action remains faithful when one finite root is rational. Its fixed subspace has dimension one. The specialization is smooth because its discriminant is nonzero.

**Accepted without mathematical correction.**

## Finite controls and adversarial testing

The original finite output was reproduced byte-for-byte. Both the original and corrected scripts produce the frozen output in ordinary and actual optimized child processes. The mutation harness records both `sys.flags.optimize` and `__debug__`, so optimization is not simulated.

Nine isolated mutations alter: the Chebyshev sign; an affine slope; the second generator; its branch coefficient; the coefficient-ring relation; the product-power relation; the linear-versus-projective cardinality; the element-order fingerprint; and the determinant target.

- Original program, ordinary Python: rejects 9/9.
- Original program, `python -O`: rejects 0/9.
- Corrected program, ordinary Python: rejects 9/9.
- Corrected program, `python -O`: rejects 9/9.

The independent implementation uses precomputed ring operations and sparse right-generator multiplication rather than the original generic matrix multiplication. It checks every determinant in 1,962,930 enumerated matrices. Moduli 2,3,4,5,7,9,11 give orders 10,120,320,15000,117600,87480,1742400. The extra powers of two and three agree with the abstract Hecke-group indices in the inspected later source, but no actual Jacobian image is inferred merely from this agreement. Its full output is byte-identical with and without optimization.

The scripts use only the Python standard library. Finite enumeration does not replace the residual theorem, the common-inertia source input, comparison theory, or an argument identifying a particular integral monodromy lattice.

## Remaining scope and the later literature

The frozen packet does not prove complete integral images at 2,3,5; the full adelic image; or a parameter-dependent classification of rational-fiber arithmetic images. Nor does it fully characterize every level structure or the geometric specialness of its curve inside the RM surface. Those are correctly labeled **packet gaps**, not globally open problems.

Lang–Lang's inspected arXiv v3 gives congruence indices for its explicitly specified integral Hecke group, including prime powers of two and three and multiplicativity across coprime ideals. It is stronger than a prime-ideal-only theorem. The abstract matrix group tested here is highly relevant to that theorem. A separate algebraic bridge note records a concrete way to pursue an integral identification; this does not retroactively make the missing argument part of the original five-turn proof.

Cadoret–Moonen's Theorem A assumes the Mumford–Tate conjecture and, for its adelic conclusion, Hodge-maximality, after the setup's connected-image adjustment. It gives openness, not an exact subgroup or a uniform arithmetic-fiber answer. Takei's published triangle-group theorem concerns specified congruence quotients. None of these should be represented as automatically resolving the broad arithmetic question.

No exhaustive present-day literature search was performed in this audit. The verdict does not certify historical novelty or current global openness.

## Deliverables and reproduction

- `PROOF_CORRECTED.md`: full source-free proof with the integral-module, common-inertia, Goursat, and arbitrary-lift details expanded.
- `checks_corrected.py`: optimization-safe replacement retaining the original output format.
- `PROPOSED.patch`: exact patch against the frozen `PROOF.md` and `checks.py`.
- `independent_checks.py` and `INDEPENDENT_CONTROLS.json`: exact symbolic and independent matrix checks.
- `mutation_checks.py` and `MUTATION_RESULTS.json`: genuine optimized subprocess baselines and mathematical mutants.
- `SOURCE_VERIFICATION.json`: public source metadata, byte verification, and actual inspection scope.
- `corrected_public/`: full derivative public packet, with its own regenerated manifest; historical turn records and the frozen original remain unchanged.
- `PATCH_VERIFICATION.json`: successful isolated patch application, byte comparison, and both manifest checks.
- `AUDIT_MANIFEST.json`: hashes and sizes of the audit deliverables, excluding itself.

Run `python mutation_checks.py` from this directory, and `python -O independent_checks.py --split`. The mutation runner expects the untouched sibling `public` directory for the original comparison. Run `python -O checks_corrected.py` to reproduce the original finite output with active checks.
