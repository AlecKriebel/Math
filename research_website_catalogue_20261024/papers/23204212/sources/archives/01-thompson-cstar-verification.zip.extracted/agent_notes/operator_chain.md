# Independent reconstruction of the Thompson reduced C*-algebra chain

Checkpoint: 2026-10-07 05:15:50 UTC / 2026-10-06 22:15:50 America/Los_Angeles.

Completion estimate: **100% of this downstream literature-and-hypothesis audit**. The unconditional research target remains dependent on a proof of nonamenability of `F`; this audit supplies **0% new evidence for that upstream assertion**. No external communications or Git mutations were performed. This document was reconstructed from the primary sources below, without using the older triage.

## Exact result, hypotheses, and success criterion

Let `NA(F)` mean that the standard discrete Thompson group `F` is nonamenable. Let `CS(G)` mean that the **reduced** group C*-algebra `C*_r(G)` has no nonzero proper closed two-sided ideal. Let `UT(G)` mean that this reduced algebra has exactly one tracial state.

The verified downstream statement is

\[
\mathrm{NA}(F)\Longrightarrow
\bigwedge_{G\in\{F,T,\operatorname{Aut}(F),\operatorname{Comm}(F)\}}
\bigl(\mathrm{CS}(G)\land\mathrm{UT}(G)\bigr).
\]

The implication is established literature, not a new discovery. Conversely, each of the four simplicity assertions individually implies `NA(F)`. Thus proving the complete unconditional conjunction is equivalent to proving `NA(F)`. The trace assertion for `T` alone is already unconditional; it cannot replace simplicity in the converse.

Success for the original unconditional target therefore requires an independently checked upstream proof. Writing `NA(F)` as an input to an implication establishes only the conditional statement displayed above.

## Primary-source map

1. **Adrien Le Boudec and Nicolás Matte Bon**, *Subgroup dynamics and C*-simplicity of groups of homeomorphisms*, Annales scientifiques de l'École Normale Supérieure, Série 4, **51** (2018), no. 3, 557–602, DOI [10.24033/asens.2361](https://numdam.org/articles/10.24033/asens.2361/). Inspected both [arXiv:1605.01651v3](https://arxiv.org/html/1605.01651) (23 December 2016) and the [published PDF](https://numdam.org/item/10.24033/asens.2361.pdf). Theorem 3.7 occurs on printed p. 576; Theorem 4.1 and Corollary 4.2 on p. 581; Theorem 4.3 and Corollary 4.4 on p. 582. Numbering agrees across these versions.
2. **Matthew G. Brin**, *The chameleon groups of Richard J. Thompson: automorphisms and dynamics*, Publications mathématiques de l'IHÉS **84** (1996), 5–33, DOI [10.1007/BF02698834](https://www.numdam.org/articles/10.1007/BF02698834/); [published PDF](https://www.numdam.org/item/PMIHES_1996__84__5_0.pdf). Inspected §1.1 / Theorem 1, printed pp. 8–9, and the normalizer computation on p. 22.
3. **José Burillo, Sean Cleary, Claas E. Röver**, *Commensurations and subgroups of finite index of Thompson's group F*, Geometry & Topology **12** (2008), 1701–1709, DOI [10.2140/gt.2008.12.1701](https://geodesic.mathdoc.fr/articles/10.2140/gt.2008.12.1701/); [author-hosted PDF](https://web.mat.upc.edu/pep.burillo/Papers/comF.pdf); [arXiv:0711.0919](https://arxiv.org/abs/0711.0919). Inspected §1, Proposition 2.1, and Theorem 3.1 with its realization proof. **0711.1014 is a different paper**, by Bleak and Wassink.
4. **The same authors**, *Addendum to “Commensurations and subgroups of finite index of Thompson's group F”*, Geometry & Topology **17** (2013), 1199–1203, DOI [10.2140/gt.2013.17.1199](https://doi.org/10.2140/gt.2013.17.1199); [author-hosted PDF](https://web.mat.upc.edu/pep.burillo/Papers/simple.pdf); [arXiv:1301.0616](https://arxiv.org/abs/1301.0616). Inspected Theorem 1 and its exact sequences.
5. **Uffe Haagerup and Kristian Knudsen Olesen**, *Non-inner amenability of the Thompson groups T and V*, Journal of Functional Analysis **272** (2017), 4838–4852, DOI [10.1016/j.jfa.2017.02.003](https://doi.org/10.1016/j.jfa.2017.02.003); [arXiv text](https://arxiv.org/html/1609.05086). Inspected Proposition 4.1, Theorem 4.5, Remark 4.6, and Proposition 2.4.
6. **Emmanuel Breuillard, Mehrdad Kalantar, Matthew Kennedy, Narutaka Ozawa**, *C*-simplicity and the unique trace property for discrete groups*, Publications mathématiques de l'IHÉS **126** (2017), 35–71, DOI [10.1007/s10240-017-0091-2](https://doi.org/10.1007/s10240-017-0091-2); [arXiv:1410.2518v3](https://arxiv.org/html/1410.2518v3). Theorem 1.3 / Corollary 4.3 and the radical proofs were independently inspected in [unique_trace_audit.md](./unique_trace_audit.md).

Historical reference: J. W. Cannon, W. J. Floyd, W. R. Parry, *Introductory notes on Richard Thompson's groups*, L'Enseignement Mathématique (2) **42** (1996), 215–256, DOI [10.5169/seals-87877](https://doi.org/10.5169/seals-87877). The referenced Binghamton PDF did not load in this audit. No claim below is presented as a fresh inspection of that PDF: elementary local-copy arguments are written out instead, and the necessary structural facts were checked in Brin and Burillo–Cleary–Röver.

## Precisely what the numbered results assert

The following mathematical paraphrase records the source statements, rather than claiming to resolve their input.

| LBM result | Input and conclusion |
|---|---|
| Theorem 4.1 | `NA(F)` implies `CS(G)` for every countable `G≤Homeo(S¹)` containing the standard circle copy of `F`. |
| Corollary 4.2 | `NA(F) ⇔ CS(F) ⇔ CS(T)`. |
| Theorem 4.3 | `NA(F)` implies `CS(G)` for every countable `G≤Homeo(R)` containing the specified line copy of `F`. |
| Corollary 4.4 | `NA(F) ⇔ CS(Aut(F)) ⇔ CS(Comm(F))`, with **abstract** commensurator. |

Their common forward mechanism is Theorem 3.7: for a countable faithful group of homeomorphisms of a Hausdorff space, nonamenability of every nonempty-open-set rigid stabilizer suffices for reduced simplicity. The proof passes through nonamenability of nontrivial uniformly recurrent subgroups and Kennedy's criterion.

## Definitions and action-level reconstruction

Put `D=Z[1/2]`. The interval group `F` consists of increasing PL homeomorphisms of `[0,1]`, with finitely many breakpoints in `D` and slopes in `2^Z`. The endpoints are fixed. Identifying the endpoints gives its faithful standard action on `S¹=R/Z`.

The circle group `T` consists of orientation-preserving PL circle homeomorphisms with finitely many dyadic breakpoints, slopes in `2^Z`, and preservation of `D/Z`. This last requirement matters. Without it, all irrational rotations would satisfy the truncated slope/breakpoint condition, and the purported family would be uncountable and would not be closed under composition with dyadic-breakpoint elements. Brin's primary definition explicitly includes preservation of dyadic points.

Use `P_+` for increasing locally PL homeomorphisms of `R` with locally finite dyadic breakpoints, positive slopes in `2^Z`, and preservation of `D`. Use `P=P_+⋊⟨r⟩`, where `r(x)=-x`, for the extension allowing reversal; equivalently absolute slopes lie in `2^Z`. These definitions avoid ambiguity about slope signs.

The line copy is

\[
F_{\mathbb R}=\{g\in P_+:\exists M>0,\ l,r\in\mathbb Z,
\quad g(x)=x+l\ (x<-M),\quad g(x)=x+r\ (x>M)\}.
\]

Brin §1.1 gives its conjugacy with the standard interval action; BCR §1 gives the same eventual-translation model. Its derived subgroup `F'` is the bounded-support subgroup of `P_+`.

For `G≤Homeo(X)` and open `U⊂X`, define the rigid stabilizer

\[
G_U=\{g\in G:g(x)=x\text{ for every }x\in X\setminus U\}.
\]

This is a pointwise-complement stabilizer, not merely a setwise stabilizer or a point stabilizer.

### Explicit local-copy lemma

Every nonempty open `U` of `R` contains a closed elementary dyadic interval `I=[a,a+2^{-n}]` with `a∈D`. On the circle, choose such an interval in the open chart `(0,1)` inside `U`; even when `U` contains the endpoint class `0`, it also contains a subinterval away from `0`.

For `f∈F`, define

\[
\iota_I(f)(x)=
\begin{cases}
a+2^{-n}f(2^n(x-a)),&x\in I,\\
x,&x\notin I.
\end{cases}
\]

Continuity follows because `f(0)=0` and `f(1)=1`. Composition on `I` is affine conjugation, so `iota_I` is a homomorphism; restriction proves injectivity. A breakpoint `b∈D` goes to `a+2^{-n}b∈D`. Slopes are unchanged under the affine conjugation, and the extension adds at most the two dyadic endpoints. The map preserves `D`.

Thus the circle construction belongs to the standard circle copy of `F`; the line construction has bounded support and belongs to `F'≤F_R`. In both cases its support is contained in `I⊂U`. Consequently `F_U` contains an isomorphic copy of `F`.

Under `NA(F)`, subgroup closure of amenability forces `F_U` to be nonamenable. If `F≤G≤Homeo(X)`, then `F_U≤G_U`. The same obstruction holds for every open `U`, so Theorem 3.7 applies. This checks the forward implications for both `G=F` and `G=T`, and for the line overgroups below.

### Hypotheses that must not be silently substituted

- **Faithful realization:** an abstract subgroup isomorphic to `F` is insufficient for this argument unless its image has the local-support property. Theorems 4.1 and 4.3 use the standard copies just specified. A nonfaithful action with kernel cannot be treated as `G≤Homeo(X)`.
- **Countability:** it is verified below for all four targets. The argument does not infer it from membership in the PL ambient group.
- **Space:** `R` and `S¹` are Hausdorff. Compactness is not required by Theorem 3.7.
- **All open sets:** the explicit dyadic interval construction covers disconnected open sets and neighborhoods of `0`; checking only whole-space stabilizers would not suffice.
- **Reversal:** Theorem 4.3 uses full `Homeo(R)`, so reversing elements of full automorphism and commensurator groups are permitted.
- **No minimality prerequisite:** standard `F` on the circle fixes `0` and is not minimal. The stronger extreme-boundary criterion of Corollary 3.14 is not needed here. The local-stabilizer criterion remains applicable.

## Full automorphism and abstract commensurator groups

`Aut(F)` means all abstract automorphisms, including those induced by reflection in the line model. Brin Theorem 1 identifies it through conjugation with `N_Homeo(R)(F_R)≤P`. The increasing subgroup is `Aut^+(F)`, of index two; its elements satisfy `h(x+1)=h(x)+1` near both ends. The normalizer is an overgroup of `F_R` and so satisfies the local-copy hypotheses.

The abstract group `Comm(F)` consists of equivalence classes of isomorphisms `phi:H→K`, where `H,K≤F` have finite index. Two representatives are equivalent when they coincide on some finite-index subgroup of `F` contained in both domains. For `phi:H→K` and `psi:L→M`, the composition is defined on `phi^{-1}(K∩L)`; its image lies in `M`. Restriction provides the well-defined equivalence-class product, and inverse representatives provide inverses.

This must be distinguished from a relative commensurator in a prespecified ambient group. BCR Theorem 3.1 supplies the substantive identification of this **abstract** group with a faithful subgroup of `P≤Homeo(R)`: maps satisfying, on the two tails separately,

\[
h(x+p_+)=h(x)+q_+\quad(x\gg0),\qquad
h(x+p_-)=h(x)+q_-\quad(x\ll0),
\]

for nonzero integers `p_±,q_±`. The signs allow reversal. It contains `F_R`, whose tail translations satisfy such conditions. Thus Theorem 4.3 applies to the full commensurator as well.

### Center and centralizers, checked directly

If a nonidentity `h∈Homeo(R)` moves `x`, continuity gives a small interval `J` with `J∩h(J)=∅`. Choose a dyadic `I⊂J` and nonidentity `f∈iota_I(F)≤F'`. Then `f` and `hfh^{-1}` have disjoint nonempty supports and cannot coincide. Hence

\[
C_{\operatorname{Homeo}(\mathbb R)}(F')=
C_{\operatorname{Homeo}(\mathbb R)}(F_R)=\{e\}.
\]

In particular `Z(F)=1`, and `F≅Inn(F)◁Aut(F)`.

BCR Proposition 2.1 gives `H'=F'` for every finite-index `H≤F`; each commensuration therefore restricts to an automorphism of `F'`. In the faithful line model, conjugation by any element of `P` preserves bounded support and the local dyadic PL conditions. Thus `F'` is normal in the **full** commensurator. This is a direct argument, not an inference that normality is transitive along a subnormal chain. It also proves injection of the natural inner-commensuration copy of `F`: an element in its kernel centralizes `F'`, which the preceding lemma rules out.

## Countability proofs

`F` and `T` have finite PL descriptions using only dyadic coordinates and integer slope exponents (for `T` include the dyadic image of a chosen basepoint). A countable union of finite products of countable sets is countable. Thus both are countable. Haagerup–Olesen's introduction also records the two-generator presentation of `F`; BCR uses its finite generation in Proposition 2.1.

If `F=⟨x_0,x_1⟩`, an automorphism is determined by `(alpha(x_0),alpha(x_1))∈F²`. Hence `Aut(F)` is countable.

More generally a finitely generated countable group `Gamma` has only finitely many index-`n` subgroups: a subgroup yields an action on `n` cosets, and a homomorphism to the finite symmetric group is determined by the finite generating tuple. Taking the union over `n` gives countably many finite-index subgroups. Each is finitely generated by Schreier's lemma. For fixed finite-index `H,K`, an isomorphism `H→K` is determined by the images in countable `K` of finitely many generators of `H`, so there are at most countably many. The countable union over pairs `(H,K)`, followed by passage to equivalence classes, remains countable. Apply this to `Gamma=F` to obtain countability of `Comm(F)`.

The ambient `P_+` is **uncountable**: choose nonidentity dyadic bumps in pairwise disjoint intervals `[n+1/4,n+3/4]` for positive integers `n`. Every binary sequence selects which bumps to apply. The resulting map has locally finite dyadic breakpoints and satisfies all ambient conditions; distinct sequences give distinct maps. Therefore the countability step could not validly be skipped by calling the PL ambient group countable.

## Reverse implications: no missing amenability shortcut

For a nontrivial amenable group `G`, the trivial representation extends to a character on `C*_r(G)`; its kernel is nonzero because `lambda_g-1≠0` for `g≠e`. Thus `CS(F)⇒NA(F)`.

For `T`, the following checkable reconstruction of Haagerup–Olesen Theorem 4.5 avoids confusing subgroup amenability with amenability of the whole overgroup. Suppose `F` were amenable. On `D/Z`, the point stabilizers in `T` are conjugate to `F` (dyadic rotations establish transitivity). The permutation representation `pi` is then weakly contained in the regular representation by HO Proposition 4.1, and factors through a nonzero homomorphism from `C*_r(T)`.

Choose nonidentity `a,b∈F` with disjoint supports. They commute, and for every dyadic point `d`, at most one moves `d`. It follows that

\[
\pi(a+b-ab-e)\delta_d=0.
\]

But `e,a,b,ab` are distinct, so `a+b-ab-e≠0` in `C T`; regular representation is injective on the group algebra. The factor map has a nonzero proper kernel. Consequently `CS(T)⇒NA(F)`.

For `Aut(F)`, amenability of `F` would give the nontrivial amenable normal subgroup `Inn(F)`. For `Comm(F)`, it would give the nontrivial amenable normal subgroup `F'` by the direct normality proof above. Reduced C*-simple groups have trivial amenable radical, so neither simplicity assertion can coexist with amenability of `F`. The published Corollary 4.4 instead obtains the commensurator converse from the BCR addendum's subnormal chain and BKKO inheritance of C*-simplicity by normal subgroups; both approaches validate the same implication.

## Unique trace and reduced/full boundaries

The independent primary-source audit [unique_trace_audit.md](./unique_trace_audit.md) verifies BKKO Theorem 1.3 / Corollary 4.3:

\[
\mathrm{UT}(G)\Longleftrightarrow R_a(G)=\{e\},\qquad
\mathrm{CS}(G)\Longrightarrow\mathrm{UT}(G).
\]

The canonical normalized trace is `tau(lambda_g)=delta_{g,e}`. With the forward simplicity statements proved conditionally, unique trace follows for all four targets under the same assumption.

`T` is simple as an abstract group and nonamenable unconditionally: HO Proposition 2.4 exhibits `C2*C3` inside it. Its amenable radical is therefore trivial and `UT(T)` already holds. The companion audit gives direct radical and centralizer proofs that `UT(F)`, `UT(Aut(F))`, and `UT(Comm(F))` are each equivalent to `NA(F)`.

For every nontrivial group, the **full** group algebra `C*(G)` has the augmentation character `epsilon(u_g)=1` and the regular trace `tau(u_g)=delta_{g,e}`. They differ on every nonidentity group element. The augmentation kernel is also nonzero and proper. Thus full simplicity and full unique trace fail for all four targets; a reduced result cannot be relabeled as a full result.

Abstract group simplicity is distinct as well. `F/F'≅Z²` shows `F` is not simple. Full `Aut(F)` and full `Comm(F)` have proper orientation-preserving index-two subgroups. The abstract simplicity of `T` establishes its radical claim, but does not establish reduced C*-simplicity.

## Source defects and validation record

**Left-tail typo, visually verified:** published LBM p. 582 (PDF page index 27) literally prints `x≤A` and `x≥A` for the two translations, with `A>0`; the arXiv HTML repeats it. The former must read `x≤-A`. Otherwise continuity at `A` forces equal translations and the description collapses to integer translations, contradicting the stated faithful `F` model. Brin p. 8 and BCR §1 explicitly give the negative left-tail threshold. The published page was downloaded and rendered locally to distinguish a true printed typo from text-extraction loss; temporary whole-paper and page-image files were removed after inspection.

**Orientation notation:** LBM defines its `PL_2(R)` with positive slopes, then places the full automorphism and commensurator groups inside it. Read literally, that ambient identification misses reflection. Brin separates `PL_2` from its index-two extension, and BCR explicitly permits reflection. The corrected faithful embeddings into full `Homeo(R)` supply exactly the hypotheses of LBM Theorem 4.3, so this notation issue does not defeat Corollary 4.4.

**Falsifiable checks applied:** tested neighborhoods of the circle fixed point; disconnected opens; boundary continuity of local copies; slope and dyadic preservation; full versus increasing automorphism/commensurator groups; countability despite an uncountable ambient group; proper kernels under the amenable branch; and nontransitivity of normality. The unique-trace arguments received a separate adversarial subagent check. No claim of new nonamenability evidence, new operator-algebra theorem, or proof of the original unconditional target is made.

**Strongest verified conclusion:** the original four-group reduced simplicity-plus-unique-trace package is a valid conditional consequence, and its unresolved mathematical input is precisely `NA(F)`. Any route that merely restates one of these equivalent assertions without independently proving it transfers the central difficulty and is blocked as a discovery route.
