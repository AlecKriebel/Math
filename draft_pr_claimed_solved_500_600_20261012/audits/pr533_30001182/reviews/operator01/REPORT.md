# Independent operator/state audit of PR #533

Problem 30001182 / OWR-3392-009. Frozen PR head: `135911efff1ad14314f0506b0d5f158ba986426f`. Reviewer scope: positivity, GNS, all-witness exclusion, pure folding, exact free-product state identity, and category/boundary assumptions. Historical priority is not assessed.

**Decision: PASS for the mathematical counterexample under the printed unrestricted positive-state definition.** The exact remaining mathematical gap within this scope is **none**. This is an independent AI-assisted audit, not formal certification or human peer review. The finite computation supplements the proof; it does not prove the infinite quantifiers.

## 1. Source and exact target

I independently obtained the report from the [publisher's PDF](https://ems.press/content/serial-article-files/46209?nt=1), reached from the [article page](https://ems.press/journals/owr/articles/3392). Printed p. 540 is PDF index 47. I read the complete extracted page, including the diagrams' map labels and item (1). Screenshot requests failed; no preexisting downloaded paper, text, or render was used.

The definition compares the entire two induced states on the **unital** free product of the subalgebras, using two distinct copies in the countably infinite ambient free product. It requests an extremal permutation-invariant state without prescribing a convex slice of full marginals. The contribution imposes no trace, faithfulness, distinctness, or trivial-tail condition. Item (1) specifically motivates the question by possible failure to lift extreme invariant states to a larger algebra. These observations support the convention used in the proof packet. Here “state” has the standard positive normalized meaning; the finite-dimensional example lies in unital *-algebras and C*-algebras.

The exact assertion tested is that a unital, state-preserving inclusion can change whether such a witness exists. The main example has distinct, proper coordinate subalgebras with scalar intersection. The independent polynomial check also addresses the more directional non-lifting concern in the algebraic category.

## 2. Independent downstairs proof, including every candidate witness

It is useful to prove the stronger one-parameter statement. Let

\[
A=\mathbb C^{\{00,01,10,11\}},\quad
p=(0,0,1,1),\quad q=(0,1,0,1),\quad
\varphi_t=(1-t)\delta_{00}+t\delta_{11},\quad 0<t<1.
\]

Set `B=span{1,p}` and `C=span{1,q}`. Both have dimension two, `A` has dimension four, and `span{1,p,q}` has dimension three. Thus the intersection is exactly the scalars. These are actual unital subalgebras, sharing the full identity; no compression to a support corner occurs.

Take **any** permutation-invariant positive normalized state `ω` on the algebraic free product of countably many copies of `A` satisfying the required full `B*C` state identity. Write `p_i=j_i(p)`, `q_i=j_i(q)`. The identity on just the relevant degree-one and degree-two words, followed by permutation invariance, implies

\[
\omega(p_i)=\omega(q_j)=t,
\qquad\omega(p_iq_j)=\omega(q_jp_i)=t\quad(i\ne j).
\]

These are necessary constraints on every possible witness, not assumptions about a selected natural witness.

### Positivity and the GNS domain

For the positive form `⟨x,y⟩=ω(x*y)`, Cauchy–Schwarz holds. If `ω(x*x)=0`, then Cauchy–Schwarz applied to `x` and `a*a x` gives

\[
\omega(x^*a^*ax)=0.
\]

Consequently the null space is a left ideal and left multiplication is well-defined on the GNS quotient. This derivation does not assume boundedness or faithfulness. Each generator is a self-adjoint idempotent there. It is also a contraction: the squared norms of its action and of its complementary projection sum to the original squared norm. Thus completion introduces no difficulty for these operators.

Let `P_i,Q_i` be the resulting projections and `Ω=[1]`. For distinct indices,

\[
\|(P_i-Q_j)\Omega\|^2
=\omega(p_i)+\omega(q_j)-\omega(p_iq_j)-\omega(q_jp_i)=0.
\]

For any `i,k`, choose `j` outside `{i,k}`. This gives `P_iΩ=Q_jΩ=P_kΩ`. Each `Q_jΩ` agrees with one of these by choosing `i≠j`. Hence all these vectors equal a common `v`.

For every generator `R`, idempotence gives `Rv=R²Ω=RΩ=v`. Starting at the rightmost letter now proves that **every nonempty finite generator word** sends `Ω` to `v`. Its moment is `⟨Ω,v⟩=t`.

There is no illegal inference that a null vector identity is an operator identity, and no use of a two-sided null ideal. The proof only multiplies well-defined GNS vectors on the left. In fact the cyclic space subsequently collapses to `span{Ω-v,v}`, on which every generator is the same projection. The vectors are orthogonal with squared norms `1-t` and `t`.

Because `1,p,q,pq` span each copy of `A`, the unit and these finite generator words span the algebraic free product. Evaluation at `00` in every copy defines a character `χ_00`, and evaluation at `11` in every copy defines `χ_11`. The moment result gives the full identity

\[
\boxed{\omega=(1-t)\chi_{00}+t\chi_{11}.}
\]

Both characters are positive normalized permutation-invariant states and they differ on `p_1`. The decomposition is nontrivial for `0<t<1`. This therefore excludes **all** extreme exchangeable witnesses downstairs. The unique admissible state does exist and is exactly the displayed mixture, so the exclusion is not a failure to construct a consistent joint law.

For the universal C*-free product, the same proof applies to the dense algebraic subalgebra, and equality of bounded states on that subalgebra implies equality everywhere. Alternatively the algebraic proof already excludes a larger class of states. No norm approximation or finite-word cutoff is used in this quantifier step.

## 3. Independent upstairs proof

Embed `A` as all diagonal matrices in `M4`, with the displayed point order, and use

\[
u_t=\sqrt{1-t}\,e_{00}+\sqrt t\,e_{11},
\qquad \psi_t(T)=u_t^*Tu_t.
\]

On a diagonal matrix this is exactly `φ_t`. The embedding sends `1_A` to `I4`, not to a rank-two support projection. The state support is smaller than the identity, which is permitted and explicitly distinguishes a nonfaithful state from a nonunital inclusion.

### Matrix purity and quotient pullback

A positive normalized functional on `Md` has a positive semidefinite density matrix with trace one: this follows directly by testing rank-one matrices. If its convex combination equals the vector-state density `u_t u_t*`, then each component has zero quadratic form on every vector perpendicular to `u_t`. Positivity eliminates the off-diagonal entries connecting that null space to its complement. Each component is consequently supported on `span{u_t}`, and trace one forces it to be exactly `u_t u_t*`. Thus `ψ_t` is pure. This is a statement about all positive algebraic states on `M4` as well as C*-states.

For any surjective unital *-map `Q:D→E`, suppose the pullback of a pure state `η` decomposes as `sη_1+(1-s)η_2`, with `0<s<1`. For `x∈ker Q`, its pulled-back `x*x` moment is zero, so positivity forces `η_k(x*x)=0`. Cauchy–Schwarz with the unit gives `η_k(x)=0`. Thus each component vanishes on the kernel and factors to a normalized linear functional `θ_k` on `E`. For any `a=Q(z)`,

\[
\theta_k(a^*a)=\eta_k(z^*z)\ge0.
\]

The factored functionals are states, and purity of `η` makes the decomposition trivial. This proof works for algebraic *-quotients without a closure or continuity assumption. In the C*-case the factored positive normalized functionals are automatically bounded states.

The folding map `Q:F(M4)→M4`, given by `Q(j_n(T))=T`, is a surjective unital *-map by the universal property; its range includes `Q(j_1(M4))=M4`. In the universal C*-category the same property gives a surjective C*-homomorphism. It obeys `Q∘α_σ=Q`, so

\[
\omega'_t=\psi_t\circ Q
\]

is permutation-invariant and pure among **all** states. Purity implies extremality within the exchangeable states. No de Finetti classification, tracial representation, or tail-algebra hypothesis is needed.

### The entire `B*C` law

Let `λ:B*C→F(M4)` put `B` in copy 1 and `C` in copy 2, let `m:B*C→A` multiply the original included letters, and let `ι:A→M4` be the diagonal inclusion. Both `Q∘λ` and `ι∘m` are unital *-maps and agree on every `B` and `C` letter. The universal property implies

\[
Q\circ\lambda=\iota\circ m.
\]

Consequently

\[
\omega'_t\circ\lambda
=\psi_t\circ\iota\circ m
=\varphi_t\circ m
\]

as full states on `B*C`, algebraically or universally in the C*-category. This covers arbitrary sums, affine letters, alternating words, orders, and lengths; it does not replace state equality with correlation agreement. In addition `ω'_t∘j_n=ψ_t` on the **entire** matrix algebra for every `n`.

An independently verified general consequence is that any pair of unital *-subalgebras of an ambient algebra with a pure state satisfies this definition, using pure folding. The example is an explicit instance of that general mechanism plus the downstairs exclusion.

## 4. Adversarial scope and boundary tests

| Attack or variant | Verified result |
|---|---|
| Another exchangeable downstairs witness with unusual higher moments | Impossible: the cyclic-vector collapse uniquely fixes every moment. |
| Algebraic GNS null-space/domain error | None: left-ideal proof above suffices; projection operators are contractions. |
| Pure state may lose purity under quotient pullback | False for surjective unital *-quotients; kernel-factorization proof covers both categories. |
| Off-diagonal matrix state fails to preserve the diagonal law | It preserves every diagonal value; coherence supplies purity upstairs. |
| Only degree-two equality upstairs | Full map identity proves every word at once. |
| A support corner was used as the ambient inclusion | False: the inclusion preserves the full identity `I4`. |
| Shared subalgebras or identical coordinate generators | Main example has distinct proper `B,C`, scalar intersection, and `p≠q`. Their equality in a nonfaithful GNS representation is a derived fact. |
| Require the witness's entire-copy marginal, but keep extremality among all exchangeable states | The upstairs witness still works and every downstairs candidate is still nonextreme. |
| Change extremality to the fixed-full-marginal slice | This example ceases to distinguish the ambients; see the proof below. |
| Require tracial witnesses | There is no upstairs tracial witness for this example; see below. The source has no trace restriction. |
| Require faithful ambient states | The rank-one matrix state and the four-point marginal are nonfaithful, as disclosed. No such variant is solved here. |
| Endpoints `t=0,1` | Downstairs character mixture degenerates to a pure character; the counterexample needs `0<t<1`. |
| Use only two copies | The third-index step fails, and an explicit extreme two-copy witness exists below. The printed product has infinitely many copies. |
| Demand a trivial tail or a particular normal W*-product convention | Not used or resolved. All matrix states are normal, but that does not specify a W*-free-product definition. |

### Fixed-marginal extremality really changes the example

Let `S_t` be the convex set of invariant states whose marginal on every full copy of `A` is `φ_t`. Put `μ_t=(1-t)χ_00+tχ_11`. Suppose `μ_t=sη_1+(1-s)η_2` inside `S_t`. For `i≠j`,

\[
\mu_t((p_i-q_j)^2)=0.
\]

Positivity forces each component to have the same zero-square identities. The fixed marginals give `η_k(p_i)=η_k(q_j)=t`; the GNS proof in Section 2 then gives `η_k=μ_t`. Hence `μ_t` **is extreme in the fixed-marginal slice** and satisfies the original joint law. Upstairs the pure witness is extreme in its fixed-marginal slice too. This proves the proof packet's caution about the convex set is essential and prevents misreading the added-marginal assertion.

### No tracial upstairs witness

Any tracial state on the free product of `M4` copies restricts to the normalized matrix trace on each copy. The required `B*C` identity and invariance would again force `p_iΩ=q_jΩ` for `i≠j`, and three indices would force `p_iΩ=q_iΩ`. Thus its expectation of `(p_i-q_i)^2` would be zero. But

\[
\frac14\operatorname{Tr}((p-q)^2)=\frac14\operatorname{Tr}(\operatorname{diag}(0,1,1,0))=\frac12.
\]

This is a contradiction, independent of full-marginal requirements. The actual vector state is nontracial: `ψ(E01 E10)=1/2`, while `ψ(E10 E01)=0`. Here matrix indices are `0,1,2,3`; point `01` is index 1.

### An explicit two-copy boundary witness

For just `F2(A)=A*A`, use two characters:

| Character | First copy evaluation | Second copy evaluation |
|---|---|---|
| `ξ_a` | `10` | `01` |
| `ξ_b` | `01` | `10` |

Their fair mixture is invariant under swapping the two copies. In both characters the first-copy `p` equals the second-copy `q`, taking values 1 and 0 respectively. Thus the complete `B*C` law is the fair perfectly correlated law. The mixture is extreme among swap-invariant states: the equivariant quotient onto `C²` with these two evaluations has a unique swap-invariant state, and any invariant decomposition of its pullback kills the quotient kernel by the same positivity argument as Section 3 and factors to that unique state. This explicitly shows why an argument considering only two copies would be insufficient. Its marginal is supported on `01,10`, and it does not extend to an admissible infinite exchangeable witness with the required law.

## 5. Separate algebraic non-lifting and C*-context checks

For `R=C[x]⊂S=C[x,x^{-1}]`, with both generators self-adjoint, evaluation at zero yields a character on `R` and hence a pure invariant character on `F(R)` by folding to `C`. A positive extension to `F(S)` would, in one copy, give self-adjoint `X,Y` with `XY=YX=1`, `η(X²)=0`. The positive Gram matrix on `{X,Y}` would be

\[
\begin{pmatrix}0&1\\1&\eta(Y^2)\end{pmatrix},
\]

whose determinant is `-1`. This is impossible. Equivalently Cauchy–Schwarz gives `1≤0`. The state has no positive extension at all. Both ambients admit the common probability-space marginal given by evaluation at 1; the nonextendible character is a different unrestricted invariant state. This does not pretend to be non-lifting of that chosen common marginal.

The contextual C*-extension statement is also correct with its explicit hypotheses. Given an equivariant **unital C*-inclusion** `D⊂E`, first extend the smaller invariant state positively. Average over each finite permutation group and use a weak-* cluster point (a subnet, if necessary) to obtain an invariant extension. The nonempty invariant-extension fiber is compact. When the smaller state is extreme among invariant states, the fiber is a face: restriction of any invariant convex decomposition must be the original smaller state in both components. An extreme point of the compact fiber is therefore extreme in the whole invariant-state space. No sequential-compactness assumption is needed. Thus the algebraic obstruction and C*-context are directionally distinct from the main restriction counterexample; the proof packet separates them correctly.

## 6. Exact checks and reproduction

`independent_verify.py` was written and run before the authored checker was read. It uses only the Python standard library and rational `Fraction` arithmetic. It checks the four-point algebra and coordinate intersection, rational rank-one coherent densities, state-preserving restrictions, projection saturation Gram matrices, arbitrary rational affine letters, matrix positivity, and exact boundary weights.

The run passed 12,282 binary-generator words through length 10, 23,436 alternating affine words through length 5, 42 principal minors, and 60 matrix positivity checks. Exact weights were `1/2`, `4/5`, `1/5`, `9/13`, `0`, and `1`. The graph of null-vector identifications is disconnected at two copies and connected for each tested count from three through nine. The report's proof, rather than these finite graph instances, covers all indices.

After the independent mathematical decision was logged, the authored `verify.py` was read, inspected for mutations, and run with its output redirected into this review folder. It only prints results and does not modify inputs. The replay passed all **14,944 assertions** and its JSON equals the frozen `checks.json` exactly. The output SHA-256 is `7d8106784864ab81d50511bb8deeeeec94de687fbd3bdfa57a6227fd30733d1e`.

The finite authored collapse model assumes the collapsed projections when executing its word loop, so it is not an independent check of the universal exclusion step. The written proof above supplies that step. The polynomial finite determinant loop similarly illustrates the exact Gram obstruction; the Cauchy–Schwarz proof supplies its universal parameter assertion.

## 7. Disposition within this review

No blocking mathematical error, hidden extra hypothesis, circularity, or overlooked eligible witness was found. The strongest verified claim is the full finite-dimensional ambient-dependence theorem for the unrestricted definition, with an all-witness uniqueness proof downstairs and a pure witness upstairs, valid in both requested free-product categories. The additional algebraic failure of positive lifting is independently verified.

No amendment is necessary to support that claim. A possible optional explanatory improvement would record explicitly that the downstairs mixture is extreme in the fixed-marginal slice, as proved here, but the existing warning is already accurate. The claimed result does not certify historical novelty, fixed-marginal extremality variants, faithful-only variants, tracial-only variants, or a normal W*-formulation. Those are not gaps in the theorem as stated. All original inputs were left unchanged; no commit, push, release, or outside communication was performed.
