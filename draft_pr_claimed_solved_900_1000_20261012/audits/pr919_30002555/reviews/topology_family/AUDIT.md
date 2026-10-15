# Adversarial topology-family audit of PR919 / problem 30002555

Verdict: **PASS for the assigned mathematical topology/core family; no required repair identified.** Two optional clarifications are recorded below. This is not a novelty, priority, or current-openness certificate. It does not replace the separate full source-model, conformal, or computation audits.

Audit scope: the exact claimed-solved original packet at immutable head `704685791ec0053dc0a52590fdef49ed4aae61d9`, with original `public/PROOF.md` SHA-256 `78be2da0b8831461e0268eb230cf47273a629a81a9dc2db997234f9fb5036464`. The complete imported statement, parent charter, preflight, and snapshot were read first. `INITIAL_DERIVATION.md` was written before opening the submitted proof or any reviewer verdict. Afterwards the complete submitted proof and its bibliography were read. No original or fresh reviewer verdict was consulted, no other research shard was read, and no proof-search turn was added.

## 1. Exact claim and success criterion

The imported target asks whether every allowed pair (X,G), with X a closed Cantor subspace and G a countable prescribed subgroup of GL+(2,R) without contracting elements, occurs as the full matrix Veech group of a tame, connected, infinite-genus surface without planar ends and with end space X. The assigned pair is exactly

\[
X=\{0,2/3,1\},\qquad A=\frac15\begin{pmatrix}3&-4\\4&3\end{pmatrix},\qquad G=\langle A\rangle.
\]

The middle-thirds Cantor set contains all three points (ternary representatives 0.000..., 0.200..., and 0.222...). A finite subset is closed. Thus the candidate does not depend on the empty-space edge case or on interpreting “Cantor subspace” as requiring perfection. The source quantifier is over closed subspaces, not only spaces homeomorphic to the whole Cantor set. The exact question and matrix-derivative convention occur in the [Oberwolfach report, printed pp. 886–887](https://ems.press/content/serial-article-files/46504).

The mathematical success criterion for this family is a connected compact K in every eligible three-ended surface such that h(K) intersects K for every self-homeomorphism h, together with the valid implication from compact-set properness of the full rotational affine preimage to finite rotational derivative image. A single counterexample pair is sufficient to negate the target's universal existence claim. Abstract isomorphism of groups is weaker and does not suffice.

## 2. Independent end-space proof

Let S be any connected second-countable surface without boundary, with exactly n finite ambient ends, n>=3. No genus assumption is needed for the following lemma.

Choose an exhaustion by compact connected subsurfaces. For every pair of distinct ends, some stage separates that pair. Since there are finitely many pairs, one stage separates all of them at once. The stage has finitely many boundary components and hence finitely many complementary components. Fill the relatively compact complementary components. Every remaining component has a nonempty ambient-end set: its closure is a noncompact bordered surface with compact boundary, and a proper exhaustion inside it supplies an escaping end. Two such components cannot carry the same ambient end. Thus there is a connected compact subsurface K for which S\K has exactly n components U_i and the ambient end sets U_i^* are the distinct singleton sets {e_i}.

Here, for an open component U of the complement of a compact set, define

\[
U^*=\{e\in\operatorname{Ends}(S):\text{a sufficiently far representative of }e\text{ lies in }U\}.
\]

This is an ambient-end definition. It is **not** an assertion that the generally nonproper inclusion U->S induces an intrinsic end-space map. An open collar near a deleted compact boundary can contribute an intrinsic end of U which escapes no compact subset of S.

Now assume h(K)∩K is empty for a homeomorphism h:S->S. Connectedness of h(K) puts it in a single U_i. Connectedness of K puts K in one component W of S\h(K). For each j!=i the connected closure cl_S(U_j) is disjoint from h(K) and meets K along nonempty boundary; hence cl_S(U_j) lies in W. Therefore

\[
\{e_j:j\ne i\}\subset W^*,\quad |W^*|\ge n-1\ge2.
\]

A homeomorphism is proper: the inverse image of a compact set is compact. It therefore induces a bijection h_* of the ambient end space by applying h to escaping representatives. Its complementary components are h(U_k), and

\[
h(U_k)^*=h_*(U_k^*)=\{h_*(e_k)\}.
\]

Every component of S\h(K), including W, consequently has exactly one ambient end, a contradiction. End permutations, orientation reversal, moving handles, infinite support, and nonaffine homeomorphisms are all included. The proof contains no assumption that h fixes an end, has finite order, or belongs to a subgroup acting properly.

This argument constructs the separator directly from ends and does not transfer the main difficulty to classification, group realization, or an unsupported nondisplaceability assertion.

## 3. Comparison with submitted Lemma 2

The submitted proof takes B_n to be an n-holed sphere capped at each boundary by a one-ended infinite-genus tail with one boundary circle. Such a tail exists by removing a disk from a ray of handles. The finite gluing produces an orientable, connected, second-countable surface without boundary. Its genus is infinite, its end space has exactly n points, and all those points are accumulated by genus. The central n-holed sphere is a compact connected subsurface.

The classification hypotheses match precisely: the source works with orientable surfaces without boundary, and classification uses genus together with the nested pair of all ends and nonplanar ends. For both S and B_n these invariants are infinite genus and the nested pair (X,X) with |X|=n. Thus a homeomorphism exists and transports the core. See [Ramírez Maluendas–Valdez, Section 1.1, Theorem 1.2, printed pp. 533–534](https://msp.org/agt/2017/17-1/agt-v17-n1-p15-s.pdf). The direct exhaustion proof above supplies a second route and also shows that nonplanarity is unnecessary for this topological step.

The submitted connected-set argument at original proof lines 167–173 is valid: K together with every other tail is connected because each tail closure meets K. Its assertion that a complementary component “carries” one end is correct when read in the ambient sense fixed in the proof's definition of Ends(S). If read instead as a claim that the open U_i intrinsically has one end, it would be false: deleting the cuff adds a collar end. That alternative reading is not needed anywhere in the proof. Optional clarification O1 makes this explicit.

No circular classification use occurs: B_n's invariants can be checked before classification, classification identifies only the surface type, and nondisplaceability is then established by the independent finite-end count.

## 4. Surface, cone, boundary, and closure conventions

The end count uses the exact underlying topological S named in the target. Finite cone points included in S are ordinary topological disk points, so they do not alter its topological end space. The local complex structure extends at angle 2*pi*m with a coordinate w for which the developing coordinate is proportional to w^m. The local affine map is holomorphic away from such a point and extends by the removable-singularity theorem; continuity bounds the target coordinate near the image point, and the same argument applies to the inverse.

If a convention omits finite cone points, do not fill them during the argument. The exact omitted-point surface already has translation charts and a complex structure, so use its own stated genus and ends. Removing a closed discrete included finite-cone set can add isolated planar puncture ends and is not an operation preserving the original target. It is unnecessary here.

Infinite-angle completion points are not ordinary manifold points. They must remain outside the surface unless a different topological object has explicitly been specified. This audit does not identify the ends of the metric completion with Ends(S), and does not infer that every missing infinite-angle point creates an isolated planar ambient end. Such a cone has noncompact cuffs, so the simple puncture inference would be unjustified.

“Without boundary” means no actual topological boundary. A finite or infinite conical metric completion is a separate object. The central core's own boundary circles are retained as part of K, and its open complement and the closed tails S\int(K) are not conflated. The source topology convention is explicit in [RMV, Section 1.1](https://msp.org/agt/2017/17-1/agt-v17-n1-p15-s.pdf); its tame metric definition and derivative Veech definition appear in Section 1.4. These observations agree with submitted proof lines 34–58. No extra compact-boundary hypothesis on S has been silently added.

## 5. Independent audit of the finiteness bridge

Let H be a group of self-homeomorphisms acting compact-set properly on S: for every compact C, the transporter {h:h(C)∩C is nonempty} is finite. Applying this definition to the nondisplaceable K shows that H itself is finite. No free action, finite area, proper flat metric, or global lower bound on displacement is required.

For the translation surface define H=D^{-1}(SO(2)) inside the full orientation-preserving affine group. Its members are locally z->lambda*z+b with |lambda|=1 and therefore holomorphic, including the finite-cone extensions just described. This proves H<=Aut_hol(S). By definition of derivative image,

\[
D(H)=\Gamma(S)\cap SO(2).
\]

This identity neither identifies H with its derivative image nor assumes a trivial translation kernel. Any nontrivial kernel makes H larger; it does not weaken the finiteness contradiction. No splitting of D is invoked.

The submitted Lemma 1's uniformization-normalizer proof was checked as a dependency, independently of its cited isometry theorem. Infinite genus implies nonabelian fundamental group. One way to see this precisely is to choose an embedded positive-genus compact core with essential boundary; its fundamental group injects into the ambient surface, by the standard incompressibility of such a subsurface. A freely acting plane deck group consists of translations and is abelian; a sphere deck group is trivial. Therefore the universal conformal cover is H, with nonabelian discrete deck group Lambda.

If N=N_PSL(2,R)(Lambda) were nondiscrete, a sequence of nonidentity elements approaching 1 would eventually centralize two fixed noncommuting elements of Lambda. A nonidentity real Möbius transformation has abelian centralizer, so this is impossible. N is a discrete subgroup, hence closed; it meets compact transporters in finitely many points. The proper action of PSL(2,R) on H follows from the compact point stabilizer. A finite union L of compact lifted coordinate neighborhoods covers any prescribed compact C downstairs. Every coset whose C-image meets C has a representative whose L-image meets L, after multiplying by a deck transformation. Hence Aut_hol(S)=N/Lambda acts compact-set properly.

The proof uses the complete uniformizing metric only as an auxiliary conformal object, and assumes no completeness of the given flat metric. Torsion in N creates at most finite stabilizers and causes no difficulty. This checks the specific bridge needed here; the separate conformal family remains responsible for its complete dedicated audit.

The already-published-source cross-check is [Artigiani et al., Theorem 1.8 and Corollary 2.19, arXiv:2311.00158v2](https://arxiv.org/pdf/2311.00158v2). They give finite isometry groups in the nondisplaceable case and proper discontinuity for infinite-type translation surfaces; Section 3.1 uses the rotational affine preimage. This is corroboration, not the proof of the end lemma and not a priority search.

Thus every translation structure on an infinite-genus surface with finitely many n>=3 ambient ends has finite D^{-1}(SO(2)) and finite Gamma(S)∩SO(2), independently of whether some of those finitely many ends are planar. The submitted all-nonplanar specialization follows immediately.

## 6. Exact witness and conjugacy controls

A^T A=I and det(A)=1, so every positive, zero, or negative power preserves the norm of every vector. Strict contraction is therefore excluded without relying on the determinant as a test for contraction.

An independent infinite-order check uses the complex eigenvalue alpha=(3+4i)/5. If A^k=I for k!=0, replacing k by |k| gives that alpha is a root of unity. Both alpha and alpha^{-1} are algebraic integers; hence alpha+alpha^{-1}=6/5 is an algebraic integer. A rational algebraic integer must be an integer, which 6/5 is not. Thus A^k!=I for every nonzero integer k. In particular G is countably infinite. This is a universal argument, not a bounded-power computation or an irrational-angle approximation. The original mod-5 trace induction is also valid.

If Gamma(S) contains A, it contains all of G, contradicting the finiteness of Gamma(S)∩SO(2). This disproves realization of the exact pair.

The optional conjugacy statement is also consistent. If the prescribed group is PGP^{-1}, change charts by P^{-1}, or directly give the translation charts the constant positive-definite quadratic form invariant under that group. In the changed charts those affine maps are conformal for a complex structure on the same topological surface, and the same compact core applies. Finite conical coordinates still extend. For the assertion that tameness survives chart change, a cyclic covering over a punctured disk becomes a cyclic covering over a punctured ellipse; restricting to a smaller round disk gives the appropriate cyclic conical neighborhood in the changed metric, for finite and infinite covering degree. Bilipschitz equivalence alone would be insufficient to prove that exact local model, but the submitted proof supplies this additional argument. The exact embedded witness needs no conjugacy step.

## 7. Falsification attempts and boundary outcomes

| Attempt / boundary | Outcome and exact reason |
| --- | --- |
| Arbitrary permutation of the n ends | Does not evade the contradiction: h_* sends singleton ambient-end sets to singleton sets. |
| h(K) snakes across several tails | Impossible when disjoint from K, since h(K) is connected and the tails are distinct components. |
| h(K) lies deep inside one nonplanar tail | The component containing K still contains all other n-1 tails, contradicting singleton ambient-end sets. |
| Artificial intrinsic collar ends | They expose a wording ambiguity only; the corrected ambient-end proof never counts them. |
| n=1 | No numerical contradiction. A one-ended ray-of-handles surface permits moving a compact central block further into its only tail. No nonexistence claim follows. |
| n=2 | The count yields one other tail, compatible with singleton end sets. The bi-infinite chain of handles admits a shift displacing finite block cores. No negative conclusion about Jacob's ladder or its lattice question follows. |
| Infinite end spaces | A compact separator cannot in general isolate all infinitely many ends. This finite-end proof does not apply to the blooming Cantor tree or classify other infinite spaces. |
| Extra finite planar or isolated ends | With finitely many total ends >=3 the topology lemma still works. All ends of a finite Hausdorff end space are isolated; isolated does not mean planar. |
| Included finite cones | Ordinary topological disk points; complex structure and maps extend. |
| Omitted finite cones | Use the given punctured surface and its actual end space. Filling points would change the problem and is not used. |
| Infinite-angle completion points | Do not adjoin them as manifold points or use completion ends. No completeness assumption enters. |
| Finite rotation groups | Compatible with the proved finiteness. The counterexample requires the proven infinite order of A. |
| Nontrivial affine translation kernel | Included in the full preimage H; its possible size cannot invalidate the inference. |
| Abstract cyclic realization | An infinite cyclic group generated by a nonrotational matrix is outside this obstruction. |
| Source/editorial contraction typo | Not adjudicated by this topology-family audit; rotations preserve every norm under any strict-shortening interpretation. Exact source family must own source-transcription conclusions. |

## 8. Issues and strongest verified conclusion

**Required issues: none.** The end-core proof and its use in rotational finiteness are valid under the exact underlying-surface convention stated in the submitted proof.

**O1, optional exposition:** at original proof lines 161 and 170–173, write “carrying exactly one ambient end of S” and/or introduce U_i^*. This prevents an incorrect intrinsic-end reading of the open complements. It does not change a mathematical hypothesis or result.

**O2, optional exposition:** at original proof lines 168–170, explicitly note that each cl_S(U_j) is connected, meets K, and is disjoint from h(K). This makes connectedness of K union the other tails immediate to a reader. The supplied model already guarantees it.

Strongest verified mathematical conclusion: for every infinite-genus Riemann/translation surface with finitely many n>=3 ambient ends, any compact-set proper homeomorphism group is finite; in particular the full rotational affine preimage and its derivative image are finite. For X={0,2/3,1}, the exact infinite noncontracting rotational matrix group G=<A> cannot even be a subgroup of the Veech group. The submitted all-nonplanar tame case is a specialization.

Exact remaining mathematical gap in this family: **none found**. The whole package still needs the parent synthesis of independent source-model/conformal/computation reviews and the explicitly later priority/framing audit. No novelty/current-openness claim follows from this verdict. No external human input was sought, drafted, or initiated.

## 9. Reproducibility and preservation

The audit's checkable mathematical artifacts are this proof and `INITIAL_DERIVATION.md`. `VERIFY_AUDIT.py` uses only the standard library to check all 27 immutable original hashes, the expected original head recorded in the snapshot, the exact proof hash, and the self-excluding curated allowlist manifest when present. `VERIFICATION.json` records the original-integrity result; no bounded numerical test is presented as evidence for a universal topological assertion.

All created files are confined to this reviewer folder. No original file, Git index/branch, PR, tracker, release, Zenodo object, other audit folder, or environment was modified. Retrieved third-party bodies were read through the web tool and were not saved into the public packet. The manifest explicitly lists the public allowlist with size and SHA-256, and excludes itself by design.
