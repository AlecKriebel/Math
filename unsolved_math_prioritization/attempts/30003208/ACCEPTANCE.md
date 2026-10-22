# Independent analytic acceptance: tail generation by ordinary shifted moments

## Reader edition note

The report below is reproduced in full. Its exact reviewed object is the original proof hash stated in the verdict. The present [proof edition](PROOF.md) adds material-method attribution and updates its final status sentence, without changing the mathematics. References below to accompanying programs and result files describe the original private audit record; programs are not included in this public reader. A compact [verification certificate](VERIFICATION.json) records both the original controls and additional independently implemented controls. Finite checks supplement the analytic proof and do not prove its infinite-dimensional conclusion.

## Verdict and exact object reviewed

**ACCEPT.** The argument in *Tail generation by ordinary shifted moments* proves the stated general-symmetric theorem. No mathematical correction is required to the reviewed text.

- Reviewed proof SHA256: `45ee9fd0e214340b1a0c0caf1e3e8fc776e6727189031ca3ee140d3fcf705f98`
- Reviewed proof size: 7,729 bytes
- Review date: 13 October 2026 UTC
- Conclusion accepted: for every unital C*-algebra A and symmetric state on its countable universal unital free product, the canonical expectation satisfies
  `closure_WOT F(π(𝔄)) = T`, and every `t ∈ T` has approximants `F(x_λ) → t` with `x_λ ∈ π(𝔄)` and `||x_λ|| ≤ ||t||`. Consequently `D'' = T` in the original GNS representation.

This is an analytic audit against the cited published-source construction and standard operator-algebra theorems, not a formal proof-assistant certificate, a novelty certificate, or evidence of journal acceptance. The numerical controls below are supplementary only.

## 1. Source-premise verification

The checked primary source is Kenneth J. Dykema, Claus Köstler and John D. Williams, *Quantum symmetric states on free product C*-algebras*, [arXiv:1305.7293v3](https://arxiv.org/pdf/1305.7293v3).

The following source locations were directly checked against the PDF and its extracted text:

- p.8, §5 opening and Definitions 5.1.1–5.1.2: general symmetric-state scope, GNS tail, permutation unitaries.
- pp.9–10, Lemmas 5.1.5–5.1.9: isometric shift; the domain contains the represented free product and preserves Q.
- pp.11–12, Theorem 5.1.10, equation (10), part (iv): WOT iterates define G on R; its restriction F has domain Q, range T and norm one.
- pp.12–13, Example 5.2.1: Liu's nonnormality example.
- p.16, Definition 5.3.1 and Question 5.3.5: exact recursive D and generation question.
- p.26, Theorem 7.3/Table 1: credited quantum-symmetric case.

The PDF checked has SHA256 `c7349b4d3b185ec25bbf6c67e57fee504e7f94c624754ff44972ea2703992e72` and 465,298 bytes. The [arXiv record](https://arxiv.org/abs/1305.7293v3) dates v3 to September 2014; the current PDF rendering has August 2021 running headers/metadata. No historical-byte authentication is asserted.

The complete §5.1 proof establishing the needed expectation was read; §§5.2–5.3 were read for the stated domain, nonnormality, and definition boundaries. Rendered pages 8, 10, 11, 12, 13, 16 and 26 were visually inspected. There is no unnoticed faithfulness, trace, separability, or quantum-symmetry premise in the facts used by the candidate.

## 2. Independent reconstruction of the critical lemma

Use the candidate's concrete GNS notation `(π,H,ξ)`. Put

`B_N = C*(π_j(A): 1 ≤ j ≤ N)`,
`C_N = C*(π_j(A): j > N)`,
`H_N = closure(B_N ξ)`, and let `P_N` project onto `H_N`.

Take a finite-copy polynomial x whose entire index support is a finite set `S ⊂ {N+1,N+2,...}`. For any integer `k ≥ 1`, prescribe `σ(i)=i+k` on S. With `U=S∪(S+k)`, this is a bijection from S onto S+k. Complete it by a bijection `U\S → U\(S+k)` and set σ equal to the identity outside U. This is a finite permutation fixing every index at most N.

This extension is valid even if S and S+k overlap. The prescribed images already occupy exactly S+k; the complementary assignment has disjoint image and precisely the needed remaining domain. An index that occurs repeatedly in a word is a single member of S and receives the same image at every occurrence. No disjoint-support assumption between S and S+k, and no distinct-index assumption within a word, is used.

The concrete covariance gives `β̂_σ(x)=α^k(x)`. Because σ fixes the first N copies, it fixes B_N pointwise. Since its implementing unitary fixes ξ, for every `y,z∈B_N`:

`⟨α^k(x)yξ,zξ⟩ = ⟨xyξ,zξ⟩`.

In particular, the matrix coefficient agrees with its k=0 value for *every* k, not only eventually. The source's WOT shift-limit formula therefore gives

`⟨F(x)yξ,zξ⟩ = ⟨xyξ,zξ⟩`.

Finite-copy polynomials in the indices greater than N are norm dense in C_N. The norm-one bound for F extends this equality to all `x∈C_N`. Density of `B_Nξ` then extends it to all pairs of vectors in H_N. Thus the candidate's identity is correct:

`P_N F(x) P_N = P_N x P_N`, for every `x∈C_N`.

The projection P_N need not belong to M, commute with T, or reduce C_N. None of those assertions occurs in the proof or is needed for this compression identity.

## 3. Independent bounded-density argument

The spaces H_N increase and have dense union. Indeed, every finite copyword involves some finite initial segment, and their linear span applied to the cyclic GNS vector is dense. This proves `P_N→I` strongly without assuming H or A is separable. Each H_N can itself be nonseparable; an increasing *sequence of subspaces* is not a claimed countable dense set of vectors.

Let `t∈T`, let `r=||t||`, and take finitely many arbitrary pairs `(η_j,ζ_j)` in H and a tolerance `ε>0`. The case r=0 uses x=0. For r>0 choose N so that, for every j,

`2r (||η_j−P_Nη_j|| ||ζ_j|| + ||P_Nη_j|| ||ζ_j−P_Nζ_j||) < ε/2`.

By definition of T, `t∈C_N''`. Kaplansky density for the concrete unital C*-algebra C_N supplies an `x∈C_N`, `||x||≤r`, satisfying

`|⟨(x−t)P_Nη_j,P_Nζ_j⟩| < ε/2`

for every j. The same x handles the whole finite list.

Set `d=F(x)`. The compression lemma identifies the last display with `|⟨(d−t)P_Nη_j,P_Nζ_j⟩|`. Since `||d−t||≤2r`, the exact decomposition

`⟨(d−t)η,ζ⟩ = ⟨(d−t)(η−P_Nη),ζ⟩ + ⟨(d−t)P_Nη,ζ−P_Nζ⟩ + ⟨(d−t)P_Nη,P_Nζ⟩`

bounds each original coefficient by less than ε. This proves WOT approximation on arbitrary vectors, not merely on the cyclic vector or on an unspecified dense domain.

The element x belongs to π(𝔄), because a C*-homomorphism has norm-closed image and π(𝔄) contains all copies. More explicitly, π factors through the C*-quotient `𝔄/kerπ`; its induced injection is isometric, so its image is complete and hence closed. This works even when π is noninjective.

Direct the WOT neighborhoods of t by reverse inclusion and choose such an x in each neighborhood. This gives the promised net, with the input bound `||x_λ||≤r` and output bound `||F(x_λ)||≤r`. No abstract lift of x to an element of 𝔄 with an exactly attained quotient norm is needed: the norm claim concerns the concrete represented element x.

Conversely F has values in the WOT-closed algebra T. Thus the claimed WOT closure equality follows. The neighborhood proof is also a proof that the image under F of the radius-r ball of π(𝔄) is WOT dense in the radius-r ball of T.

## 4. Exact-radius Kaplansky, including nonselfadjoint t

The candidate uses the full norm-ball form of Kaplansky, which is valid; it does not inadvertently apply a selfadjoint-only statement to arbitrary t.

To see the nonselfadjoint reduction explicitly, form the selfadjoint operator

`S = [[0,t],[t*,0]] ∈ M_2(C_N'')`, with `||S||=||t||`.

Entrywise strong density identifies the strong closure of `M_2(C_N)` with `M_2(C_N'')`. Selfadjoint Kaplansky supplies selfadjoint matrices `S_λ∈M_2(C_N)` with `||S_λ||≤r` and `S_λ→S` strongly. Their upper-right corners `x_λ` lie in C_N, satisfy `||x_λ||≤r`, and converge strongly to t. Hence they provide the finite WOT approximations needed above.

This standard reduction is independently documented in [Kaplansky density notes, §3.4, Theorem 3.4.6, pp.42–43](https://users.math.msu.edu/users/banelson/conferences/GOALS/notes/7-6_vNa_notes.pdf). The review checked both the theorem and its 2×2 argument. No separability assumption is needed; the approximants are nets.

## 5. D containment and the bicommutant conclusion

D is unital. Setting all internal D entries in its defining operations equal to 1 therefore shows that F of every ordinary finite copyword belongs to D, including words with repeated indices. F(1)=1 handles the empty word. Linearity handles polynomial combinations. Norm density of those polynomials in π(𝔄), boundedness of F, and norm closedness of D then yield

`F(π(𝔄)) ⊂ D ⊂ T`.

This does not redefine D as a set of first moments or discard the recursive definition. It shows only that the first-stage polynomial moments already suffice for the von Neumann generation conclusion. Taking WOT closures gives `T⊂D''`, while `D⊂T` gives `D''⊂T` by the bicommutant theorem for unital *-algebras. Thus `D''=T` on H.

The argument makes no assertion that D equals the first-stage C*-algebra, that `D⊂π(𝔄)` in the general symmetric case, or that the finite-permutation fixed-point algebra equals T.

## 6. Nonfaithfulness and nonnormality attacks

### Nonfaithful state and quotient relations

The permutation implementation is legitimate on a nonfaithful GNS space: ψ invariance makes `[a]↦[β_σ(a)]` preserve the GNS seminorm, so it descends to the quotient and extends to a unitary, with inverse furnished by σ inverse. It fixes ξ and intertwines π on a dense set, hence on H. Thus every quotient relation among concrete copy images is preserved. This prevents a hidden assumption that formal words retain their universal norms or are linearly independent after applying π.

The proof uses ξ as a cyclic vector, never as a separating vector. Equality of operators is inferred from coefficients on the increasing dense family H_N, not from equality on ξ alone. Faithfulness of ψ̂, its restriction to T, or their GNS representations is not invoked.

### No illicit passage of a WOT limit through F

For a fixed N the compression of F restricted to C_N is explicitly identified with compression of the input. Kaplansky applies before F is used. The proof selects one approximant for each finite test and uses only the norm bound on F afterward. It never writes `F(WOT-lim x_λ)=WOT-lim F(x_λ)` and never extends F to M.

### Liu's example is a successful negative control

In the indicated compact-plus-scalar representation, `π_n(a)^2=e_00+e_nn`, so the stated expectation sends it to e_00. Together with F(1)=1, these outputs already span the two-dimensional T. The canonical expectation is nevertheless nonnormal: finite-rank projections `q_m=Σ_{j=0}^m e_jj` converge strongly upward to I, whereas `F(q_m)=e_00` for every m.

This confirms that the accepted density conclusion and failure of normality coexist. It also tests a genuine weakness that would invalidate a different proof: using only scalar or linear one-letter moments would miss e_00 here, while the permitted ordinary quadratic word recovers it. The candidate correctly allows all finite words.

The fixed-point enlargement in the source's separate Example 5.1.4 is not a counterexample either. The proof crucially uses `t∈C_N''` for every N; a fixed point outside the tail does not satisfy that premise.

## 7. Additional independently executed controls

The accompanying `check_controls.py` and `CONTROL_RESULTS.json` record:

- 5,760 partial-bijection completion cases over all subsets of seven consecutive tail indices, five cutoffs and nine positive shifts.
- 2,135 of these cases have overlapping original and shifted supports.
- 5,715 nonempty-support cases also verify whole repeated-index word transport.
- 350 exact integer-matrix instances in finite corners of Liu's representation check whole-word permutation covariance, shift compression and expectation compression. Compact and scalar parts are kept distinct so the character is not incorrectly replaced by a finite-dimensional trace.
- Negative controls distinguish the zero linear moment from the nonzero quadratic moment and reproduce the finite-rank-projection obstruction to normality, with the infinite-dimensional limiting assertion justified analytically.

All controls passed. They do not prove the universal operator-algebra result; the arguments in §§2–6 do.

## 8. Scope, credit, and remaining limits

The substantive accepted conclusion answers the general-symmetric generation question. The already established quantum-symmetric case remains credited to Dykema–Köstler–Williams. The proof uses their canonical expectation and standard Kaplansky/bicommutant theory.

**Method credit is material.** Dykema–Köstler–Williams Lemma 5.1.8, Theorem 5.1.10's proof, and Remark 5.1.11 already contain finite-word coefficient stabilization and its bounded-vector extension. The compression idea must not be presented as unprecedented. The added deduction in the reviewed argument is to approximate a chosen tail operator inside the future algebra for each finite family of initial-copy test vectors, retaining the exact norm bound, and thereby obtain the WOT density of ordinary F-moments.

A closely related explicit past/future coefficient identity appears in Weihua Liu, *Extended de Finetti theorems for boolean independence and monotone independence*, [arXiv:1505.02215v1](https://arxiv.org/pdf/1505.02215v1), §6.2, Lemma 6.8, printed p.33. Its setting is a bilateral spreadable sequence of bounded variables in a W*-probability space with a non-degenerated normal state and the stated nonunital-generation condition. Its shift is a normal bilateral automorphism. The lemma treats algebraic past test vectors and a future von Neumann-algebra operator, using bounded Kaplansky approximation. Lemma 6.9 and Proposition 6.10 then address shift expectations; Remark 6.11 records an extension limitation. The audit directly read this surrounding setup and visually inspected p.33. This establishes relevant technique prior art; the inspected passages do not state the exact Dykema–Köstler–Williams D-generation theorem. No full-paper audit or claim of a new general-symmetric theorem already appearing there is made.

These attribution qualifications should accompany any presentation of the accepted proof. They do not change its mathematical verdict or the frozen proof's byte identity.

The review does not certify historical priority, worldwide openness, or absence of another proof. It does not resolve the separate inclusion question `D⊂π(𝔄)`. It does not turn a nonnormal expectation into a normal one. It also does not authenticate a historical arXiv binary merely from the version label.

No source document, source text, dataset contents, private communication, or coordination record is reproduced in this acceptance report. No remote publication or external mutation was performed during this review.

**Final disposition:** accept the exact proof bytes identified above, without a mathematical amendment. All claimed universal scope and bounded-preimage strength are supported by the proof as written.
