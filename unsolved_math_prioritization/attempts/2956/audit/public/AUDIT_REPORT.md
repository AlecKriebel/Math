# Independent audit: KP-4.80 / problem 2956

Assessment: 8 October 2026. Mathematical disposition: accept the report as a rigorous partial result, with both existence questions unresolved and five completed mathematical approaches. Executable disposition: accept only with the separate optimization-safe verifier correction supplied here. No mathematical theorem or proof in the frozen report needs changing on the evidence inspected.

## 1. Exact input and preservation

The input archive is `exotic_mapping_torsion_2956_sourcefree.zip`, 21,964 bytes, SHA-256 `cd72bc9863fb1cf4d99a22471ff712c7a59a3b2ed15d3323583204182865a570`. Its frozen report has SHA-256 `b8ffa82c80ed0c05807155ddb3c12d4154aea080a17a25be7c79677b3a65eab9`. Every archive member agrees byte-for-byte with the frozen directory; every manifest size and hash agrees. The original archive, receipt and frozen files were left intact. `INPUT_PINS.json` records the independently recomputed input pins.

Eleven public-source PDF byte counts and hashes, and both dataset byte counts and hashes, independently agree with the frozen source metadata. The exact numeric problem identifier occurs once with problem code KP-4.80. Neither claimed result key is present in the supplied results dataset. These are provenance checks, not a proof that no solution exists elsewhere. `SOURCE_PIN_RECHECK.json` contains metadata only.

The author manuscript's page 256 was checked visually and against extracted text. The target is existential higher finite cyclic torsion, or a finite subgroup of cardinality greater than two, in the smooth-to-topological mapping-class kernel of a closed simply connected smooth four-manifold. The exponent in its last proposed K3 example is n−1. The report faithfully retains this distinction and does not substitute a symplectic-to-smooth kernel or a group of periodic representatives. [Problem source](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).

## 2. Theorem 1: geometric relation and permutation action

The diagonal relation is valid. Here is an explicit check of the cutoff argument. Write the ambient circle action as R_t, with R_0=R_1=id, rotating exactly one oriented real two-plane. At each chosen fixed point of S² in S⁴, the derivative is the sum of that plane rotation and an identity two-plane. It is the generator of π₁SO(4), not a double rotation representing the trivial class.

Use invariant radial collars of the disjoint invariant balls. Choose a smooth collar function β that is one near the boundary and zero near the interior edge. On each collar put C_t(s,y)=(s,R_{−tβ(s)}y), and set C_t=id off the collars. Then F_t=C_tR_t is identity on a boundary neighborhood for every t. It starts at the identity; at t=1 the ambient rotation disappears and only the simultaneous collar twists remain. Thus F_t is an actual relative smooth isotopy proving the product of the n boundary twists trivial in P_n. Extension by the identity over the punctured summands proves the closed-manifold relation. Possible inverse conventions do not affect classes of exponent two.

The summand-permutation argument is also sufficient. Ordered configurations of finitely many disjoint small parametrized oriented balls can be moved by ambient isotopy, and terminal oriented frames can be adjusted through SO(4). Exchanging identical punctured summands then extends the ambient diffeomorphism to the connected sum. Consequently every permutation of the twist classes is realized by conjugation. It is unnecessary to choose these diffeomorphisms coherently as an S_n-action; the report correctly avoids that stronger claim.

Disjoint collar supports give commuting diffeomorphisms. A based nullhomotopy of the squared SO(4) loop gives the square isotopy. Mayer–Vietoris gives homology classes supported away from the collars, so the action on H₂ is trivial. Simply connectedness and the explicitly imported closed topological isotopy classification then identify these classes as exotic-kernel elements. Nothing in this argument proves a twist nonidentity. Exact order two requires that extra fact.

## 3. The module conclusion and the three-K3 gap

The elementary algebra is complete. Let R be the relation subspace of F₂ⁿ, and d the all-ones vector. The preceding geometry supplies d∈R and S_n-invariance. If R contains a vector other than 0,d, transposing unequal coordinates produces a weight-two vector. Its orbit spans the even-weight space A. Thus R is either ⟨d⟩ or contains A. For odd n, d∉A forces the latter case to be all F₂ⁿ; for even n, d∈A leaves exactly ⟨d⟩, A, F₂ⁿ. The stated quotient ranks follow, including the duplicated n=2 option.

For n=3 the standard leaf-neck subgroup is therefore trivial or a Klein four-group. In the latter case its three specified generators are the three distinct nonzero elements. The two end-summand necks in the linear picture are independent. This is a valid reduction to one nontriviality statement, not an establishment of that statement. Stabilization by another K3 need not preserve the known two-K3 class.

Corollary 3 correctly requires conjugation-invariance of the proposed scalar homomorphism: equal generator values, exponent two and an odd number of factors force zero. It makes no unsupported universal claim about gauge-theoretic invariants.

## 4. Nonequivariant Bauer–Furuta scope

KM Definition 3.2 requires a closed oriented spin fiber, b₁=0, a spin lift with trivial homological monodromy and the bounding stable framing of the base circle. The K3 connected-sum neck families meet these conditions. KM Proposition 5.1 distinguishes the spin lift according to which side carries the spin-deck twist; its signature test is precisely 16 modulo 32. The report preserves both lifts. For n K3 summands the nonequivariant fiber invariant is ηⁿ; family degree is n+1, also recovered from d=−(2χ+3σ)/4+1=n. Both two-K3 spin-family values are the nonzero order-two class η³. [KM](https://arxiv.org/pdf/2001.08771v2).

IWX Table 1 has zero in every component of the fourth stable stem. Hence η⁴=0 and every larger power vanishes. The report's n≥3 conclusion is correct only for this specified nonequivariant framed invariant. It neither trivializes the closed neck nor kills an equivariant refinement. The distinction between a nonzero invariant for one structured spin family and an obstruction for the underlying smooth family is explicitly retained. [Stable stems](https://arxiv.org/pdf/2001.04247v1).

## 5. Remaining mathematical routes and hypotheses

- Capping: Baraglia Proposition 7.1 gives the spin alternatives for the boundary-twist kernel, and Theorem 7.2 supplies the zero frame-evaluation map for a manifold homeomorphic to K3. All these classes disappear on ordinary ball capping. The report does not identify a several-boundary relative topological kernel with the closed homological kernel. For one puncture, the central order-two extension gives precisely orders m or 2m upstairs. Theorem 7.7 applies to manifolds homeomorphic to K3; its extension class is pulled back from the intersection-lattice action. Restriction to its kernel is zero, so the abstract product splitting is valid. It is not a diffeomorphism-group splitting or an action. [Baraglia](https://arxiv.org/pdf/2310.18819v1).
- Sphere twists: smooth square triviality and the Picard–Lefschetz reflection hold for the standard local two-sphere twist. Exact order two follows from its nonidentity homology action on a −2 class. The report restricts braid relations to standard Lagrangian A_r configurations. Their negative Cartan matrix is nonsingular, their rational root classes are independent, and the standard S_{r+1} representation on the sum-zero subspace is faithful. Therefore the smooth twist subgroup is S_{r+1} and meets the exotic kernel trivially. Equal reflections have equal negative eigenspaces and hence roots differing by sign; their intersection has absolute value two, precluding the proposed one-intersection repair. [Seidel](https://arxiv.org/pdf/math/0309012v3), [Arabadji–Baykur](https://arxiv.org/pdf/2304.10399v3).
- Periodic maps: averaging a metric and uniqueness of an isometry from its first-order data prove the support lemma. The homologically trivial orientation-preserving Lefschetz number is 2+b₂>0. Cauchy's theorem combined with the Matumoto–Ruberman involution statement gives the odd-order restriction on finite actual diffeomorphism groups for simply connected closed spin manifolds of nonzero signature. Konno's Proposition 7.1 explicitly states and applies exactly these hypotheses. The original Ruberman proof was not independently retrieved here; an AMS PDF attempt failed. The report already discloses this imported-theorem boundary. [Konno](https://arxiv.org/pdf/2203.11631v4).
- Symplectic rigidity: Chen–Kwasik Corollary A concerns finite symplectic symmetries of the canonical-orientation K3 surface. Theorem A's conditions are trivial rational canonical class, nonzero signature and b⁺≥2. The report does not apply this to arbitrary smooth representatives or connected sums. [Chen–Kwasik](https://arxiv.org/abs/0709.1708).

## 6. Current-source scope check

The current-source statements were checked against their actual domains, not inferred from titles. Tilton Theorem 1.2 is a punctured boundary result. Lindblad Theorem 1.1 concerns relative commutators for the specified complete-intersection families, and Section 4.5 carefully separates full-group from Torelli abelianization. Lin–Sha Theorem 1.6 assumes that the neck mapping class already generates an order-two subgroup; Corollary 1.7 adds simple connectivity, spin and nonzero signature for non-kinetic realizability. None supplies the missing three-K3 nontriviality proof. [Tilton](https://arxiv.org/abs/2511.16804), [Lindblad](https://arxiv.org/abs/2604.13194), [Lin–Sha](https://arxiv.org/abs/2606.24482).

Jianfeng Lin's result is one S²×S² stabilization. Baraglia–Tomlin Theorem 1.1 gives an infinite free abelian quotient for 2CP²#n(−CP²), n≥10, and therefore gives no finite torsion conclusion. The official publisher confirms 7 September 2026 publication. The audit found no contradiction of the report's bounded unresolved status. This is not a comprehensive literature-exhaustion certificate. [Lin](https://arxiv.org/abs/2003.03925), [Baraglia–Tomlin](https://academic.oup.com/qjmath/advance-article/doi/10.1093/qmath/haag031/8786456).

Bibliographic update only: Baraglia's arXiv record now also lists publication in Algebraic & Geometric Topology 26 (2026), 1635–1653. The frozen packet accurately identifies the inspected v1 manuscript; no change to the proof dependencies is required.

## 7. Verifier defect, minimal correction and genuine readonly controls

The frozen verifier contains ten Python assert statements. Under −O or −OO they are removed, while the unconditional success field remains true. This is a real false-PASS risk even though all three unmutated runs match the frozen JSON.

The separate correction changes only those ten statements to explicit calls of require, whose body raises AssertionError on false conditions. It preserves algorithms, output schema and exact output bytes. The supplied unified patch is against the pinned original. There are zero ast.Assert nodes in the corrected script. The frozen report, mathematical status and original expected JSON are unchanged.

`READONLY_MUTATION_RESULTS.json` records genuine real/effective UID 1000 runs. Each input script was mode 0444, its working directory 0555. Actual file-append and directory-create probes both raised PermissionError. Test JSON was captured on stdout, so inability to write to the input directory is never counted as rejection. Readonly source hashes were unchanged afterward. These are normal filesystem-permission checks, not a claim of an immutable mount.

Results:

- Six unmutated runs, original and corrected in normal/−O/−OO modes, matched EXACT_CHECKS.json byte-for-byte.
- Five distinct semantic mutants: allow a false odd-n rank-one case; drop the scalar diagonal condition; use a wrong triple diagonal; drop a reflection generator; omit Coxeter multiplication.
- All five original normal-mode mutants rejected by AssertionError.
- All ten original optimized mutants falsely returned success.
- All fifteen corrected mutant runs rejected by an explicit semantic AssertionError, in all three modes.

## 8. Independent exact verification

`independent_exact.py` never imports the candidate verifier. It enumerates every binary subspace in canonical reduced row-echelon form and then tests diagonal containment and adjacent-transposition stability. Total subspaces inspected for n=2,…,8 are 5, 16, 67, 374, 2,825, 29,212 and 417,199. The resulting relation dimensions, quotient ranks and invariant scalar-character counts agree with the packet.

Separately, all permutations of r+1 letters, r=1,…,5, are converted directly to integer matrices on the sum-zero representation. These independently recover the reflection matrices, faithful group orders, form preservation and Coxeter orders; element-order histograms are included. An explicit two-bit quotient checks the three-neck addition table. Signature-modulo-32 arithmetic and formal nilpotence independently check both spin-lift records, while connected-sum Euler arithmetic checks the K3 totals. No finite program computes a gauge invariant from geometric data.

Three readonly UID 1000 baseline runs recomputed the entire independent enumeration in normal/−O/−OO modes. Eight additional data mutants were rejected in every mode: false odd-n rank one, repeated triple generator, wrong A₂ order, false η⁴ nonvanishing, a missing two-K3 lift value, wrong connected-sum Euler characteristic, and truncated module/root coverage. This adds 24 semantic rejections, including checks outside the minimal verifier patch. Results and runnable harnesses accompany this report.

## 9. Final acceptance boundary

Accept the authored mathematical partial reductions. Adopt the separately pinned optimization-safe verifier for future validation. Preserve the original freeze as the input under audit. Keep KP-4.80 unresolved with five mathematical approaches; neither the original finite cyclic torsion assertion nor the larger finite subgroup assertion is solved. No source bodies, dataset contents or private coordination material are included in this audit packet.
