# Independent adversarial audit: global analytic/action mechanism

## Decision and scope

**PASS for the global analytic/action family.** The authenticated proof establishes its finite-dimensional complex unimodular transverse-pair theorem using the stated classical Lie theory and topology. I found no missing analytic completeness assumption, unjustified passage from a local orbit to a global orbit, covering-space gap, or mismatch with the radical/topology argument. The post-Lie reduction, also read in full, is consistent with this theorem. No mathematical repair is required by this audit.

This is an independent validation of the original completed approach, not an additional proof-search turn. It makes no historical novelty or current literature-status judgment. Those are reserved for the parent after mathematical review. It does not endorse any old acceptance decision: no old audit, acceptance report, readiness report, or other new agent's conclusions were read.

The target is PID 30005737 / OWR-14298013-001: a perfect nonsemisimple finite-dimensional complex source and a semisimple target, on a common vector space, admit no post-Lie product. The proof actually establishes the stronger statement that a unimodular source admitting two homomorphisms to a complex semisimple target whose difference is invertible must be semisimple. The finite-dimensional complex scope is explicit in the authored proof. The complete native statement/background and empty native prior-report entry were read before the proof.

## Authentication and independence

The frozen head is `401f86e018e8cc5075e37a29bae9350eb9f89c36`, PR 894, original recorded effort 1/5. The external `SOURCE_MANIFEST.json` has SHA-256 `1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c`. All 18 source files, with no missing or additional files, passed byte length, SHA-256, and Git blob SHA-1 checks before their mathematical claims were used. The complete 3524-byte native canonical pair has SHA-256 `b27d5dbb0f92c0ab330bf44891ec4467f7d8c593cef610196cbd82d4cc6d5298`.

`INDEPENDENT_FREEZE.md` was saved at 2026-10-16T07:01:39.424036+00:00 before reading the proof or source notes. It records an independently chosen determinant/global-action route, its exact gaps, and boundary cases. The catalog desk note, encountered during the native inventory, mentioned a Levi route; it supplied no proof and was not evidence. The whole authenticated `source/authored/PROOF.md` and `source/authored/SOURCES.md` were then read. `INDEPENDENT_ASSESSMENT.md` records the resulting independent pass before any old or peer verdict. No such verdict was read afterward either.

The formal authentication run, primary retrieval, and adversarial computation each have their actual start/end UTC timestamps, return codes, raw stdout/stderr, and SHA-256 values persisted immediately. A shell ENOSPC failure occurred before its timestamp wrapper could execute. Its actual return code and raw error were preserved with an honest observation timestamp and null execution start/end fields. No synthetic execution time was invented. Only this audit's own downloaded scratch PDF was removed to recover space; its receipt and digest remain. The first exploratory inventory was a read operation, not an independently captured validated run. Its formal checks were subsequently run and captured in full.

## Step-by-step mathematical verification

### 1. Integration and action (proof lines 34-48)

Both homomorphisms integrate on the simply connected complex source group. They need not be injective, algebraic, or have closed image. For the resulting holomorphic homomorphisms, the formula

\[
A_h(p)=J_1(h)pJ_2(h)^{-1}
\]

is an action: composition places the right factors in precisely the reversed order produced by inversion of `J2(hh')`. It is defined for every group element and every point. Thus no theorem about integrating possibly incomplete arbitrary vector fields is being used.

For the derivative of `A_exp(tx)(p)`, left trivialization really gives

\[
B_p x=\operatorname{Ad}_{p^{-1}}j_1x-j_2x.
\]

The left contribution is `p^{-1}j1(x)p`; the right contribution is `-j2(x)`. At the identity this is the assumed invertible difference. The holomorphic inverse function theorem gives an open neighborhood in the identity orbit; translations by the action show that the whole orbit is open. No closedness of the immersed image in `N x N` is needed.

**Sign attack:** positive-time fundamental fields for a left action use the opposite Lie-bracket convention to the `exp(-tx)` convention in the cited notes. The submitted proof never claims that its positive-time assignment is a homomorphism into vector fields. It only uses the direct derivative, rank, kernel, and group equivariance. These are correct with its chosen signs. There is no hidden sign-dependent bracket assertion.

### 2. The determinant continuation (proof lines 50-85)

The complex vector spaces have the same finite dimension. Fixed bases and the global left trivialization make `det Bp` a single-valued holomorphic scalar function on all of `N`. This is not a determinant section defined only near the initial orbit, and it does not require choosing a holomorphic logarithm or a global coordinate chart.

Writing `q=A_h(p)`, direct substitution gives

\[
q^{-1}=J_2(h)p^{-1}J_1(h)^{-1},\qquad
B_q=\operatorname{Ad}_{J_2(h)}B_p\operatorname{Ad}_{h^{-1}}.
\]

The last term follows because both integrated homomorphisms intertwine the adjoint representations. In particular, the second term `-j2` also transforms correctly; it cannot simply be discarded when checking this formula.

For any connected integration, `h -> det Ad_h` is a group character whose derivative at the identity is `x -> tr ad_x`. If that derivative vanishes, the character is locally constant, hence constant on the connected group, with value one. This reasoning works for complex determinants and for groups with discrete center. It does not require exponential surjectivity. The source satisfies the trace condition by hypothesis; the target does because semisimple Lie algebras are perfect. Consequently `f(A_h(p))=f(p)`.

The initial orbit is a nonempty open subset, and `f=f(e)` there. The identity theorem for holomorphic functions on a connected complex manifold then gives `f=f(e)` everywhere. One may justify this by continuation through overlapping coordinate balls; no compactness, algebraicity, density theorem, or finite diagnostic enters. Since `f(e)` is nonzero, there are no singular infinitesimal-action points anywhere.

Invertibility at each point separately gives an open neighborhood contained in that point's orbit. Thus every orbit is open. If there were more than one, any chosen orbit and the union of all the others would disconnect `N`. This proves transitivity. It is the decisive global step, and every needed assumption is present. Local transversality by itself would fail, as the dropped-hypothesis example below confirms.

### 3. Stabilizer and covering (proof lines 87-96)

The actual stabilizer of the identity is the inverse image of a point under the continuous orbit map, so it is closed. It is a Lie subgroup, with Lie algebra `ker Be=0`, hence discrete. It need not have been known to be central or finite. After transitivity, the induced map `G/H -> N` is a bijective local diffeomorphism, so it is a diffeomorphism (and locally holomorphic, giving the asserted complex-manifold identification).

For a closed discrete subgroup, the quotient map `G -> G/H` is a covering. Concretely, a sufficiently small neighborhood `V` of the identity satisfies `V^{-1}V intersect H={e}`; its right translates by distinct elements of `H` give the evenly covered sheets. The quotient theorem also supplies this local trivialization directly. Since the total space is connected and the base `N` is simply connected, the covering has a single sheet. This kills all of `H`, including a possible infinite discrete subgroup or ineffective kernel.

The proof therefore does not make the invalid general inference that an arbitrary surjective local diffeomorphism is a covering. The homogeneous quotient supplies the missing structure before the covering argument is used.

### 4. Interface with the radical/topology contradiction (proof lines 98-116)

Levi decomposition and simply connected integration identify `G`, as a manifold, with the product of the simply connected solvable radical integration and the simply connected semisimple Levi integration. There is no unsupported assumption that an arbitrary immersed Levi or radical subgroup is closed: the simply connected semidirect product is constructed first, then identified with `G` by uniqueness of integration.

The solvable induction is valid. A nonzero functional annihilating the derived algebra yields a codimension-one ideal. Any complementary one-dimensional subspace is a subalgebra. Its derivation action integrates on the simply connected kernel group, producing a semidirect product whose underlying manifold is `C` times that group. No assertion that every simply connected solvable group has a bijective exponential map is used. The inductive product is contractible and smoothly equivalent to a complex vector space.

Let `d=dim_C n=dim_C g` and `s=dim_C` of the Levi factor. The compact real form of `N` is a compact connected orientable real `d`-manifold; its top ordinary singular homology is `Z`. Thus `H_d(N;Z)=Z`. The compact real form of the Levi integration has real dimension `s`, and the radical is contractible, so `H_d(G;Z)=0` when `s<d`. This contradicts the manifold identification obtained above. The homology degree is `d`, not the real dimension `2d` of the noncompact complex group. Orientability follows, for example, from a left-invariant real volume form on a Lie group. Nothing depends on a classification of simple factors or equality of cohomology rings beyond this degree obstruction.

### 5. Post-Lie passage (proof lines 118-155)

The last post-Lie identity makes each left multiplication a derivation of the semisimple target. Its zero center and inner derivations give the unique linear `R`. The middle identity makes `R` a homomorphism. The first identity gives the cross terms which, on expanding the target bracket, make `R+I` a second homomorphism. Their difference is the identity. The trace functional vanishes on brackets, so perfectness makes the source unimodular. Thus the hypotheses used in the analytic argument match the native source/target roles exactly. No brackets were exchanged.

## Adversarial checks and boundary cases

An exact, independently constructed dropped-unimodularity example tests the most dangerous inference. In `sl2(C)` use the standard basis `H,E,F` with `[H,E]=2E`. Let the source be the direct sum of the upper Borel algebra on `H,E` and a central line on `Z`. Define `j1(H,E,Z)=(H,E,0)` and `j2(H,E,Z)=(0,0,F)`. Both are homomorphisms and their difference is invertible. The source is nonunimodular because `tr ad_H=2`.

For `p=[[a,b],[c,d]]` in `SL2(C)`, the determinant in the proof is exactly

\[
\det B_p=-d^2(ad-bc)=-d^2.
\]

It is `-1` at the identity and zero at the Weyl matrix with entries `(0,-1,1,0)`. Thus this is a genuine locally transverse example with a singular locus away from the initial orbit once unimodularity is removed. The executable check verifies the polynomial identity over an exact rational polynomial ring and every basis-pair homomorphism equation. It is neither a finite search used as proof of the target nor a counterexample under the target's assumptions. It independently confirms that the character factor in the submitted global argument is indispensable.

Other boundary attacks were resolved as follows:

- Zero dimension gives zero source and target, with the empty determinant equal to one. It cannot satisfy nonsemisimplicity. The strengthened theorem remains valid.
- A direct sum of semisimple target factors causes no change: perfectness, inner derivations, simply connected integration and compact real forms apply to the full semisimple algebra.
- Nontrivial finite centers, universal covers, and nonclosed homomorphism images do not obstruct the construction or determinant identity. The action is built on the source and target integrations themselves.
- A solvable or nilpotent source is a permitted test of the stronger theorem. Its Levi dimension is zero, so a positive-dimensional semisimple target has incompatible positive-degree top homology after transitivity.
- A reductive target with center falls outside the theorem. Its contractible central directions invalidate the compact-form dimension comparison, and its derivations need not all be inner. No extension to that case is justified here.
- The proof makes no arbitrary-real-form claim. The final homology degree comparison uses the complex field. It also makes no positive-characteristic or infinite-dimensional claim.
- The resulting manifold diffeomorphism is not itself claimed to be a group or Lie-algebra isomorphism. Semisimplicity is all the target contradiction requires.

No hidden compactness/properness assumption, limiting argument, physical model assumption, or finite numerical approximation is used. The route does not transfer the central problem to an equivalent unsupported conjecture.

## Imported inputs and exact source validation

The independently fetched primary source is [Pavel Etingof, MIT Lie Groups and Lie Algebras notes](https://ocw.mit.edu/courses/18-755-lie-groups-and-lie-algebras-ii-spring-2024/mit18_755_s24_lec_full.pdf). The retrieved 4,247,073-byte PDF has SHA-256 `ffb09776bafa3fa50dfc2bc83ee36b89058f98b7f80ff6fa90e2e34962cc9046`; the receipt records URL, HTTP status, actual timestamps and permitted response metadata. The extracted private text digest is also preserved in the captured run. The relevant hypotheses, rather than only theorem labels, were read.

The conditional input list is:

| Input | Exact source location | Audit status |
|---|---|---|
| Existence, uniqueness and homomorphism integration for finite-dimensional complex Lie algebras and simply connected groups | Theorems 9.12-9.13, Corollary 9.14, printed p.55 | Verified applicable |
| Closed stabilizers, quotient manifold and local trivialization | Theorem 4.1, printed p.28; Proposition 4.12, Corollaries 4.13 and 4.16, printed p.31 | Verified applicable |
| Levi splitting and simply connected product topology | Theorem 48.9, printed p.264; Theorem 49.1, p.265; Corollary 49.6, p.266 | Verified applicable; submitted solvable induction independently checked |
| Compact real form and polar decomposition, including covering groups | Corollary 43.5, pp.231-232; Theorem 43.7 and Corollary 43.8 plus following covering discussion, p.233 | Verified applicable |

The holomorphic inverse/identity theorems, elementary connected-covering classification, and top homology of compact orientable manifolds are classical imported foundations, not novel results of this proof. Their hypotheses are explicitly checked above. The algebraic inner-derivation fact and trace-of-commutator identity are likewise classical. There is no unverified theorem input equivalent to the target claim. This audit did not attempt to reprove the classical foundations or conduct a broad priority search.

## Check records, failure preservation and repairs

`AUTHENTICATION_RUN.json`: return code 0, 2026-10-16T07:01:39.389816+00:00 to 2026-10-16T07:01:39.423362+00:00. All 18 source files and complete native pair passed.

`PRIMARY_FETCH_RUN.json`: return code 0, 2026-10-16T07:02:21.914444+00:00 to 2026-10-16T07:02:23.034046+00:00. HTTP 200; PDF conversion also returned 0. The raw copyrighted source body and extracted corpus stay in private scratch and are excluded from the public-safe package; the downloaded PDF was subsequently removed after ENOSPC.

`ENOSPC_01_RUN.json`: actual shell return code 1, observed at 2026-10-16T07:04:51.934577+00:00. The shell could not create its here-document temporary file, so none of that attempted Python checkpoint/diagnostic wrapper ran. The error and empty stdout are retained with hashes. The initial attempted assessment write therefore was not claimed to have succeeded. The assessment was successfully written afterward. No mathematics or external result failed in this event.

`DROPPED_UNIMODULARITY_RUN.json`: return code 0, 2026-10-16T07:05:47.752967+00:00 to 2026-10-16T07:05:47.780744+00:00. Exact polynomial and homomorphism diagnostics passed. Raw stdout/stderr and their hashes accompany every captured run. No failed mathematical check was discarded or silently repaired.

The only source-inventory path correction was locating `ROOT_NATIVE_RECEIPT.json` at the parent audit root after an exploratory lookup under `private_native` showed it absent there. This was not evidence of a missing receipt and did not affect authentication of the independently pinned canonical pair.

## Strongest result and exact remaining gap

The strongest verified result in this family is the full global-action and topology contradiction for the stated unimodular transverse-pair theorem, hence compatibility of that mechanism with the perfect-source post-Lie target. There is **no unresolved mathematical gap identified here** and no required mathematical repair. Scope limitations are finite dimension, characteristic zero, and the complex field as explicitly stated by the author. Overall acceptance remains the parent's responsibility after combining independent families and conducting any separate provenance/priority work.

Audit completion: 100% once the final public-safe manifest verification recorded in the research log succeeds. This percentage measures completion of the assigned validation, not a probabilistic claim of correctness or the research program's overall discovery completion.
