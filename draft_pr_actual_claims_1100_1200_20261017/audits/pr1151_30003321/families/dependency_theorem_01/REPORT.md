# Focused independent dependency audit: Ehrlich–Kaplan Theorem 5.1

## Result

The specified manuscript's characterization supports the full set/proper-class scope in the sealed claim, including arbitrary set supports and discrete pure coefficient groups. Its printed sufficiency proof has two genuine invalid intermediate assertions. They are repairable without changing any theorem hypothesis. `INDEPENDENT_PROOF.md` gives the complete replacement construction and independently proves the needed initial-additive-subgroup extension principle from recursive surreal addition. No equivalent form of the downstream discrete-group-to-Oz question is used.

This audit concerns the imported characterization only. I did not read or validate the downstream candidate, old acceptance reports, or root/sibling verdict reports; I did not search for priority or communicate externally. No git/index/PR mutation was made. All authored files are confined to this assigned family directory; third-party PDF/text bodies are under ignored `private/`.

## Exact imported object and scope

Object: Philip Ehrlich and Elliot Kaplan, *Number Systems with Simplicity Hierarchies: A Generalization of Conway's Theory of Surreal Numbers II*, author PDF at <https://elliotakaplan.github.io/Number_systems_with_simplicity_hierarchies_II.pdf>. Main theorem and proof: PDF pp.7–9; supporting definitions and lemmas: pp.2–7. The retrieved file is 351864 bytes, SHA-256 `c6d91a1850514736d88c576cafe1f4cedf1e3dcb84a2a96418648cd4fc1a5160`. Machine-readable retrieval and reading scopes appear in `source_receipt.json`.

The exact hypotheses and success criteria were sealed in `sealed_claim.md`: canonical normal-form image, truncation closure, cross sectionality, initial exponent subclass, initial real coefficient groups, and dyadic closure at right-predecessor exponents. The additive coefficient groups can be Z, 2^{-m}Z, or groups containing D; the proof does not assume divisibility. The exponent class may be proper, but all supports are sets. The canonical qualification is essential: this is not an assertion about arbitrary order embeddings of exponents.

## Literal source failure 1: bounded exponent stages do not exhaust

Define q_n to have sign sequence + followed by n minuses, for n<ω. Thus q_n=2^{-n}. Define p_n=q_n followed by one plus. The sequence (p_n) is strictly decreasing: p_n and p_{n+1} first differ at the sign immediately after q_n, which is plus in p_n and minus in p_{n+1}. Its terms are pairwise prefix-incomparable. Put

    Γ = {0} ∪ {q_n:n<ω} ∪ {p_n:n<ω},
    R_0=Z,    R_{q_n}=D,    R_{p_n}=Z.

Let G be all reverse-well-ordered series over Γ having coordinate coefficients in these respective groups. These algebraic/tree hypotheses are checked without using the theorem conclusion:

* Γ is initial: the prefixes of q_n and p_n are 0 and the earlier q_j, and these are included.
* G is a subgroup, truncation closed and cross sectional, by its coordinate definition; each indicated coefficient group is initial in R.
* No p_n is a proper prefix of any exponent in Γ. All nonzero right simplicity predecessors in Γ are among the q_j, whose groups contain D. The exponent 0 is below every other Γ-element, so is never a right predecessor here.

Every birthday level of Γ is finite and every Γ-element has finite birthday. Any birthday-respecting enumeration therefore has order type ω and each bounded initial segment is finite. Nevertheless b=Σ_{n<ω}ω^{p_n} belongs to the canonical image A. Its support is not contained in any such finite stage. Thus the source's equality A=⋃_{α<β}A_α, with A_α defined by support in {a_δ:δ≤α}, fails for this legal set example. A chain union is initial; the invalid step is claiming it contains these omitted series.

## Literal source failure 2: dyadic cut options need not be in G

The same example witnesses failure of automatic membership of the source's limit-series cut options. Its b has leading coefficient 1, support length ω, and leading exponent p_0=2. At μ=0,n=1 the lower standard cut option is (1/2)ω^{p_0}. It is not in A because R_{p_0}=Z. Indeed every perturbation 1±2^{-n}, n>0, at any leaf p_μ is nonintegral and hence excluded. It therefore cannot lie in any previous subgroup contained in A.

These dyadic options are legitimate options for the normal-form cut, but need not be predecessors of b. Their absence does not falsify initiality. To place such b literally in one of the source's Z_α stages, one can additionally include the exponent q_ω with sign sequence + followed by ω minuses, retaining D on all its required q_n right predecessors. Then b lies in A_ω but not in ⋃_{n<ω}A_n, and the same absent dyadic options remain absent globally. The point does not depend on choosing this augmentation: the claimed option-membership mechanism is already invalid for b in the original group.

`counterexample_check.py` checks finite instances of the prefix, leaf and order claims with exact arithmetic. It passes. The quantified infinite argument is the sign-sequence proof above, not an extrapolation from this computation.

## Complete repair and why its central steps close

The independent repair first constructs the group of all finite pure-monomial sums, processing exponents by birthday and coefficients by real birthday. Every canonical cut option for each new pure term lies in an earlier group: the leader's right options use exactly the theorem's dyadic condition, and all other pure-term cuts use earlier coefficient predecessors and earlier left exponent predecessors. Chain unions suffice in this phase because the claimed output is only the finite-support group.

Next it adjoins all actual infinite-limit-support members of A, in order of support length. A series of length α=λ+n, with λ zero or limit and n finite, is a limit-length prefix plus finitely many pure monomials. This proves exhaustion, and also proves that every proper prefix of the next limit series is present. For x=Σ_{μ<λ}r_μω^{y_μ}, use the two options

    s_{μ+1} − ω^{y_μ},    s_{μ+1} + ω^{y_μ}.

They lie in the earlier group using integer closure alone. For every original dyadic option at index μ, choose a later index ν<λ; the unit options at ν lie closer to x by leading-term comparison. Consequently x is the simplest separator of the unit options. This provides the exact cut, with no fractional coefficient assumption.

For any x in the class case, the union of its support with all predecessor exponents is an actual set-sized initial exponent set E⊆Γ. The **existing** subgroup A_E of A with supports in E inherits every hypothesis and exactly the same coefficient groups at E-exponents. Apply the set theorem to A_E. It contains x and every predecessor of x; these predecessors are consequently in A. No new supported series, class cuts, or class-length recursions are needed.

## Initial-module extension dependency: independently closed for Z

The source's Lemma 4.1 cites predecessor [15], Theorem 6 without proof. Two author-hosted predecessor URLs returned 404; two primary publisher PDF URLs returned non-PDF challenge documents. Their retrieval outcomes are recorded in `predecessor_retrieval_receipt.json`; no predecessor text was obtained or claimed read.

Rather than treating that pointer as an established independent proof, `INDEPENDENT_PROOF.md`, §1 rederives precisely the Z-module specialization needed here:

1. The sum of two initial subclasses is initial. Induct on the natural sum of operand birthdays in the recursive surreal addition formula; a predecessor of the sum must be that sum's option or a predecessor of an option on its side. The option has a smaller operand-birthday measure. This avoids any invalid induction on the birthday of the resulting arithmetic value.
2. Negation preserves initiality; finite sums and their union therefore make the additive subgroup generated by an initial class initial.
3. If an initial subgroup contains every option of a known b-cut, each predecessor of b is already in the subgroup. Thus adjoining b makes an initial set and its generated subgroup is initial.

For a cut-partition formulation, when b∉M, partition all of the set M as {m:m<b} and {m:b<m}. The known option cut is included on the correct sides, so every partition realizer realizes the option cut. Since b realizes both and is simplest for the option cut, it is simplest for the partition. If b∈M the stage is skipped. This verifies every partition-cut hypothesis required to use source Lemma 4.1, and the independent argument supplies the conclusion without importing the general K-module claim.

The general s-hierarchical K-module extension lemma is not proved or needed in this audit. Standard normal-form facts in the pinned paper and their cited antecedents remain identified imports, not independently reconstructed sign-expansion theory. There is no circular reliance on Theorem 5.1 or on the downstream target question.

## Adversarial comparison with the specifically requested new repair

My exact claim was sealed before receiving any candidate proof. I independently discovered the finite-monomial/limit-length/unit-perturbation/local-set-restriction mechanism and the Z-extension proof before receiving the parent message about the sibling mechanism. The parent message then disclosed that the fresh sibling reformulation had the same four structural features and requested adversarial inspection. After that disclosure but **before reading any sibling file**, I sealed the complete `INDEPENDENT_PROOF.md` at 2026-10-18T00:40:27.654505Z (SHA-256 `03862bbbebdc1444d42d17e44557c9b94ceb0dc4573d41f23275fb4290fc9117`). This limits any claim of complete blind independence of the final write-up, but not of the already reconstructed mechanism, which was logged and messaged to the parent before access.

I then read only the expressly named fresh sibling `class_boundaries_01/DEPENDENCY_REFORMULATION.md`, in full. The access receipt records SHA-256 `995758a4ea1d04fcdbbf567717c398ba67cfdc1d893915fea44476f9fbac06c7`, 12208 bytes. I found no gap in its proof after checking:

* Its smaller family of normalized leading-coefficient-1 limit generators exhausts A: subtracting the pure term (r_0−1)ω^{y_0} preserves the limit length and makes the leading coefficient exactly 1; it never cancels the first term.
* Every proper prefix at a limit-support adjunction is earlier. A successor-length prefix is a shorter limit prefix plus finitely many pure terms; a limit-length prefix is an earlier normalized generator. Same-length ordering cannot introduce a dependency cycle.
* Its unit options lie in the current group, including coefficients r_μ±1=0; cancellation is harmless.
* Its full partition is truly all of M, both sides are sets, b is omitted before partitioning, and b is the simplest partition realizer.
* Its chain limits, generator exhaustion, and actual A_I restrictions preserve group operations, truncation, cross sectionality, coefficient equality, and the inherited right-predecessor condition.

Its reliance on source Lemma 4.1 is sufficient as a named source import; the independent Z-extension derivation above additionally supplies that omitted dependency proof. Thus no remaining theorem/class-size gap was found in the fresh repair. This conclusion is confined to the imported theorem characterization, and is not an endorsement of uninspected downstream reasoning or publication status.
