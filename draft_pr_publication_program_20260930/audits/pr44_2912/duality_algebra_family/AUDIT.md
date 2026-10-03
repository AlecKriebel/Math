# PR44 / Kirby 4.36 — independent duality and algebra adversarial audit

Verdict: the mathematical deductions in OBSTRUCTION.md Sections 2–3 pass this scoped independent audit. No mandatory mathematical correction was found in those deductions. The work remains UNSOLVED: it proves neither general completeness of the full unmarked homotopy 2-type nor a same-full-2-type counterexample among actual 2-knot complements. This is an AI audit with checkable derivations and finite arithmetic controls, not human peer review or formal verification.

Original immutable inputs: head c772dc5b851ec91da9d46d534577609e5d3ca389; base 01358d66fc67d1c462bddf31c0d4ee5b120e6737; snapshot_manifest_v2.json SHA256 75f21617c7bdc192a0a64b76de4c1deec7ecc04d35bb93cf885ec11deb542b1d; full 19-path diff 75046 bytes, SHA256 e5f892ccda9e0202e97a98c045481c92b04d2291d5ae3c5a21d05e7e3c417f3b. All 18 original snapshot file bodies and the full diff were read. The mathematical artifact is literally OBSTRUCTION.md, SHA256 69a3ffb7b6c2ba3bf1a4df8d7d83960d66095db9d175d78cfe49e2324aac1a71. No candidate or historical review helper was imported, compiled or executed by this family.

## Independence and exact target

EARLY_DERIVATION.md was sealed at actual UTC 2026-10-03T00:36:12.243649+00:00 before opening any candidate mathematical argument, result, review, or helper body. Its SHA256 is d9df5d8bc2de015a268a160473f5f9aba5a8e73a9ec4a89265a6e8e00ee2d4d1; the literal source_record.json had SHA256 44162e54c0f08a328332fc98980ff7e3fa50c96b9dade7583a53c480baf5eb30. Subsequent exposure to all candidate/historical bodies is disclosed in SOURCE_READ_RECEIPT.json. The mechanism retained here is compact-support duality and explicit crossed-homomorphism algebra, with independent coefficient coordinates and normal forms.

The target is the homotopy type of the entire complement of an actual smooth or locally flat PL embedded S^2 in S^4. The compact exterior X has the same homotopy type. The invariant is the full triple (G, A, k), with G=pi_1(X), A=pi_2(X) as a G-module, and k in H^3(G;A), modulo compatible group/module isomorphisms carrying k. The input does not specify a meridian, boundary identification, boundary sphere, or relative fundamental class. A marked-pair classification or arbitrary-CW counterexample would not answer the question.

## 1. Duality kernel, including module sides and support

Let R=ZG, and give C_*(tilde X) its left deck action. The cochain complex Hom_R(C_*(tilde X),R) has a commuting right R-action by multiplication in the target. Since X has a finite cell model, its R-valued cochains correspond to finite-support cellular cochains upstairs: there are finitely many orbit representatives, and every R-valued coordinate has finite support. Thus these are compactly supported cochains on the cover. They are not arbitrary ordinary cochains on tilde X.

For an oriented exterior, equivariant Poincare-Lefschetz duality gives the left-module isomorphism

  H_3(tilde X;Z) = overline[H^1(X,boundary X;R)].

The overline makes a right module M into a left module by g·m=m·g^(-1). The orientation character is trivial here. Equivalently, duality on the noncompact cover uses H_c^1(tilde X,boundary tilde X), or compact-support cohomology of its interior. The boundary collar provides the relative/interior identification. Simply replacing this by ordinary H^1 of the cover would be invalid. The basic limiting control is the oriented line: H_c^1(R;Z)=Z whereas ordinary H^1(R;Z)=0.

A meridian mu generates H_1(X;Z)=Z, so it has infinite order. The boundary map Z=pi_1(S^2 x S^1) -> G is injective with image H=<mu>. If r in R is fixed by an infinite subgroup, coefficients are constant on its infinite left orbits; finite support forces all coefficients to vanish. Hence H^0(X;R)=H^0(boundary X;R)=0.

The cohomology long exact sequence of the pair then identifies its degree-one relative term with the kernel of H^1(X;R) -> H^1(boundary X;R). In degree one, a simply connected universal cover makes the chain complex a resolution through degree one, so H^1(X;R)=H^1(G;R). The same statement for boundary X is valid despite the boundary's nonzero pi_2; only degree one is used. Boundary restriction is exactly group restriction to H. Therefore

  H_3(tilde X;Z) = overline[ker(H^1(G;R) -> H^1(H;R))].

This validates candidate formula (2). It is a formula for the group with its specified meridional inclusion. It does not prove that the unmarked full 2-type determines that inclusion, the kernel, or a map realizing an isomorphism of the kernels.

For H=<mu>, the cyclic resolution yields H^1(H;R)=R/(mu-1)R as a right R-module. The subgroup image (mu-1)R is a right ideal. A left-module version requires the displayed involution or a consistent alternative convention. The candidate's cohomology/homology convention is consistent.

For one-ended finitely generated G, H^1(G;ZG)=0, so the kernel vanishes. Infinite ends alone say nothing sufficient about the restriction kernel. Normal generation cannot repair this: for a crossed homomorphism d and d(mu)=0,

  d(a mu a^(-1)) = (1-a mu a^(-1))d(a),

which need not vanish. The candidate does not make either erroneous implication.

## 2. Sufficient degree-one pair-map criterion

Let f:(X,boundary X)->(Y,boundary Y) be a relative degree-one map of oriented exteriors inducing isomorphisms on pi_1 and pi_2. Naturality of the homology boundary homomorphism gives boundary degree one. On S^2 x S^1, the induced integers alpha on H^1 and beta on H^2 satisfy alpha beta=1, because their cup product generates H^3. Thus alpha and beta are units, and f on boundary pi_1 is an isomorphism.

The fundamental-group isomorphism transports the coefficient group ring. In degree one, f^* is an isomorphism on both absolute group cohomology and boundary group cohomology, and the restriction square commutes. The relative degree-one cohomology kernels are consequently isomorphic under f^*.

Naturality of cap product gives, with transported local coefficients,

  f_*([X,boundary X] cap f^*u) = f_*[X,boundary X] cap u
                                = [Y,boundary Y] cap u.

Combining this identity with duality proves that the actual lifted map on H_3 of universal covers is an isomorphism. H_0 and H_1 of the simply connected covers are already isomorphic; H_2 is isomorphic by Hurewicz and the pi_2 hypothesis. A compact smooth/PL 4-manifold with nonempty boundary has a CW model of dimension at most 3, so the covers have no homology above degree 3. The lifted map is a homology equivalence of simply connected CW spaces, hence a homotopy equivalence by the homological Whitehead theorem. With the pi_1 isomorphism this makes f a homotopy equivalence.

This validates the candidate's sufficient criterion. It does not provide the assumed pair map. A full 2-type isomorphism can be realized by an absolute map of 3-dimensional models (the first lifting obstruction from P_2Y to Y lies in degree 4). That obstruction argument supplies no boundary map or degree-one relative class. Thus the candidate's exact realization gap is real, and it is a gap in this attempted route rather than a theorem that no other route can work.

## 3. Amalgam kernel by crossed homomorphisms

The displayed group is G=A*_C B with A=C_7 semidirect C_3, C=C_3, and B=C_3 semidirect_{-1} Z. The inclusions of C in both factors are injective; the amalgam presentation is exactly the candidate's presentation. The redundant relation b^7=1 follows from a^3=1 and a b a^(-1)=b^2: iterate conjugation to get b=b^8. The finite factor has normal forms b^j a^i, and multiplication

  (j,i)(k,l)=(j+2^i k mod 7, i+l mod 3).

The infinite factor can instead use t^n a^i, with multiplication

  (n,i)(m,j)=(n+m, (-1)^m i+j mod 3).

Here t is of infinite order and normally generates G: killing t forces a=a^2, hence a=1, and then b=b^2, hence b=1. This group-theoretic weight calculation does not identify t as the geometric meridian of a particular exterior. That condition remains explicit in the candidate.

The low-degree exact sequence can be checked directly rather than assumed from a Mayer-Vietoris citation. For a finite group F, every crossed homomorphism d:F->ZF is principal. Write u_x as the coefficient of 1 in d(x^(-1)). The cocycle identity shows that the coefficient of x in d(f) equals u_(f^(-1)x)-u_x, exactly the coefficient of x in (f-1)u. For R restricted to F, apply this on each regular F-block. Only finitely many blocks occur because F and the supports of d(f) are finite. Thus H^1(A;R)=H^1(C;R)=0.

Any cocycle on G can be adjusted by a principal cocycle to vanish on A. Its restriction to B then vanishes on C. Conversely, a cocycle on B can be adjusted to vanish on C and combined with the zero cocycle on A, giving a cocycle on the amalgam. Hence restriction H^1(G;R)->H^1(B;R) is surjective.

A class in its kernel has a representative d vanishing on A with d(h)=(h-1)v for h in B. Compatibility on C forces v in R^C. Two such representatives differ by a global principal cocycle precisely when their v's differ by R^A plus R^B. Since B is infinite, R^B=0. The resulting exact sequence is

  0 -> R^A -> R^C -> H^1(G;R) -> H^1(B;R) -> 0.

All these maps respect the commuting right R-action. This independently validates candidate formula (4) and its orientation of the module maps.

## 4. Restriction B -> <t>, without infinite formal sums

Adjust a cocycle on B to have d(a)=0. Differentiating t a t^(-1)=a^(-1) shows that d(t) lies in R^C. Conversely every v in R^C supplies such a cocycle. The remaining principal changes come from u in R^C and change v by (t-1)u. Therefore

  H^1(B;R)=R^C/(t-1)R^C.

On one regular B-block ZB g, write N_C=1+a+a^2. The invariant vectors N_C t^n g form a Laurent basis, and t shifts n by one. For any finite Laurent polynomial p=sum c_n t^n, its class modulo t-1 is the integer sum c_n. This holds for every finite support, not only tested windows: if sum c_n=0, the finitely supported sequence u_n=-sum_(j<=n)c_j satisfies c_n=u_(n-1)-u_n. The telescoping sum is finite. If the total is nonzero, augmentation rules out such a primitive.

As a module restricted to T=<t>, the same B-block has three regular T-orbits represented by 1,a,a^2 (using t^n a^i). The class represented by N_C restricts to (1,1,1) in Z^3. Thus each B-block contributes the injection Z->Z^3, n->(n,n,n). Direct sums of these injections remain injective; there is no completion or infinite series involved. This also verifies the candidate transfer argument, whose multiplication-by-three composite and torsion-free source are consistent with this explicit calculation.

Consequently the kernel of restriction G->T is exactly R^C/R^A, validating candidate formula (5). Since t-1 has augmentation zero, it cannot be a unit in ZG. Any attempted inverse using an infinite geometric series would leave the integral group ring and invalidate the calculation. No such inverse is used in the candidate.

## 5. Integral finite blocks and global module scope

On a right A-coset Ag, the seven C-invariant norm vectors N_C xg, for Cx in C\A, form a Z-basis. The A-invariant vector N_Ag is their sum. The quotient block is Q=Z^7/Z(1,...,1). The diagonal vector is primitive: subtracting its coordinate at zero gives the explicit integral quotient map

  (v_0,...,v_6) -> (v_1-v_0,...,v_6-v_0),

with diagonal kernel and surjective image Z^6. Thus each block is free rank six without torsion. The direct sum over A\G is nonzero and free as an abelian group.

The identity block is a right A-module on C\A. Inversion sends Cx to x^(-1)C. Right multiplication by g^(-1), which defines the conjugate left action, becomes left multiplication by g on A/C. Taking b^jC as representatives gives a:j->2j and b:j->j+1. This proves the candidate's involution/coset convention exactly. The finite checker verifies an A-block; the global G-action, including movement between blocks by t, is supplied by the right R-module quotient R^C/R^A, not by a six-dimensional matrix for all of G.

The diagonal quotient must not be replaced integrally by the augmentation lattice I=ker(sum:Z^7->Z). Their A-coinvariants differ. In Q all coset generators become equal, and the diagonal relation is 7e=0, so Q_A=Z/7. In I, cyclic b-coinvariants are Z/7 generated by e_1-e_0, and a doubles that generator; imposing a-coinvariants kills it, so I_A=0. The two lattices are therefore not isomorphic as A-modules, despite their equal ranks and rational isomorphism. The candidate uses the correct quotient throughout.

In the alternate coordinate-zero basis, the exact control gives det(b-1)=7 and det(a)=det(b)=1. The determinant-seven statement is an additional falsifier of treating b-1 as an integral unit on Q. Cramer's rule confirms that all a-1 columns lie in the b-1 lattice. These are exact integer checks, not floating-point rank estimates.

## 6. Primary sources and limits of source certification

[Lomonaco's published scan](https://userpages.cs.umbc.edu/lomonaco/5knots/Lomonaco-Pacific-Journal-Math.pdf), printed pp.373–375, was read in extracted text and inspected as rendered pixels. Its Theorems 10.1–10.2 apply when both covers have H_3=0. Theorem 10.3 retains a finite proper amalgam splitting with the meridional subgroup in a vertex factor. Theorem 10.4 lists the cited quasi-aspherical subclasses. The proof of 10.1 was read; its geometric-realization step is an absolute-map statement. It supplies no unmarked-to-degree-one-pair realization.

[Hillman's author manuscript v3](https://arxiv.org/pdf/math/0212142v3), §§14.6–14.7, printed pp.276–278, was read as text and pixels. It identifies the displayed group as an infinite-ended 2-knot group and as a satellite group; it also treats geometric weight orbits. This verifies the group citation, without proving the proposed letter t is a particular exterior's meridian. Its §1.7 was additionally checked for ends and free-coefficient conventions. Both downloaded PDF hashes match the original source_manifest.json; retrieval and rendering access receipts record actual children.

[Brown's author-hosted lectures](https://pi.math.cornell.edu/~kbrown/papers/cohomology_hangzhou.pdf), Proposition 3.3 and the proof of (3.12), were read through the web tool. They verify finite-group regular-coefficient vanishing and the general transfer composite. [Sun's local-coefficient duality paper](https://arxiv.org/pdf/1709.00569), Theorem 1 and surrounding cap-product/proof passages, was checked for compact support and the proof mechanism. These supporting lookups are not claims to have read either entire paper.

This family did not read the full 1983 Gonzalez-Acuna–Montesinos paper and does not certify its inaccessible proof. Nor does this family independently certify the recent preprints in candidate Section 4; their source-level checking belongs to the separately assigned literature family. The logical exclusions are valid conditional on the quoted hypotheses: inequivalent first k-invariants fail the same-full-2-type premise, and surjectivity from boundary pi_1=Z forces a cyclic exterior group, which must be Z by abelianization. Bounded searches cannot certify absence of later literature.

## 7. Actual computations, negative controls, and disposition

Own code own_exact_controls.py was completely read before each launch together with capture_operator.py. The launch records preserve their exact prelaunch bytes, UTC clocks, operator and child PIDs, argv, cwd, standard streams, exit status, and before/after hashes. The initial normal run passed 30,185 controls (PID 83658, actual 00:42:30.802717–00:42:30.962630 UTC); the final source run also passed 30,185 (PID 87633, actual 00:47:39.927381–00:47:40.068679 UTC). Both normal outputs are byte-identical. The controls cover finite normal-form laws, coset and quotient representations, primitive diagonal, exact determinants/coinvariants, explicit B cocycles, T-orbit labels, and finite Laurent primitives. The written proofs above address all finite supports; the bounded computations are supporting arithmetic.

The deliberate diagonal/augmentation false assertion exited 1 (PID 83930). The first deliberately failing unit control used the literal augmentation contradiction 0=1 and is retained as an alarm-only initial version (PID 83929). It was strengthened to compute the finite-support product (t-1)u before asserting its augmentation equals 1; the strengthened version also exited 1 (PID 87632). All failed-control source bytes and stderr remain. The universal nonunit proof is augmentation multiplicativity, not a claim inferred from these deliberate failures.

The historical author/review PASS labels, claimed model/reasoning profiles, 507 and 29,933 counts, and dated search statements remain historical input claims. This family has not retroactively authenticated those executions or profiles; root is reproducing the two original helpers separately. My 30,185 count refers only to my own arithmetic source and captured runs.

The strongest verified result is the conditional duality-kernel/pair-map criterion and exact R^C/R^A block description. A positive answer still requires a mechanism obtaining the relevant homotopy equivalence from the full unmarked 2-type, with no added degree-one-pair premise. A negative answer still requires two actual exteriors with matching full triples and a verified higher-homotopy difference. Neither exists in this package. The original two routes remain blocked at their stated realization gaps. Original attempts remain 2/5; new substantive attempts 0; this is an audit, not another research attempt. Original discovery completion remains 0%; this scoped mathematical audit is complete at 100%.
