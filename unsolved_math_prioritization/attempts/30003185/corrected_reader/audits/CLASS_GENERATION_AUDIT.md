**Integrated reader status.** Accepted replacement theorem and audited substitution. The old PS2011 documentary gate is bypassed, not retrospectively verified. See the [integrated theorem](../README.md) and [dependency map](../DEPENDENCIES.md).

# Independent acceptance of the replacement Bray class-generation theorem

13 October 2026. This is an independent audit of the replacement class-generation theorem.

## Verdict and accepted scope

**ACCEPTED.** The author's `CLASS_GENERATION.md`, SHA-256 `59e6ed7ac4d3fafbb2e11b2eea43c7681092984152bbdc2ef97e85d37d0b59ee`, proves a sufficient replacement for the formerly unverified class-generation input. No substantive correction to that candidate was required.

For odd q and all sufficiently large natural dimensions e, 192 independent representatives of any prescribed sequence of strong involution classes generate natural J=Sp_e(q) or Ω(V) with probability at least 1−q^(−e). Strong means both natural eigenspaces have dimensions in [e/3,2e/3]. Odd orthogonal dimensions and both even-dimensional form types are covered. The dimension threshold is absolute but is not numerically evaluated because a published absolute constant is not numerically specified.

The replacement is proved from inspected Burness and Liebeck–Pyber–Shalev theorems plus elementary subspace counting. It does not rely on the exact meaning of “classical group” in an unavailable source. The former PS2011 documentary gate is **bypassed as a dependency**, not retroactively verified. The earlier report about failure to retrieve that article remains accurate.

The replacement is exactly sufficient for the accepted generation bridge. Thus that bridge's conclusion is now unconditional relative to its stated, inspected standard published inputs: in the specified large-dimensional natural Sp/O/SO/Ω groups, retaining O(log n) Bray even-case outputs at any fixed confidence produces a subgroup containing C_G(t)''. The explicit variable-confidence statement remains O(log n·(1+log(1/δ))) samples.

## 1. Independently checked source statements

I read the actual Burness manuscript's Definitions 1–2, Theorem 1, Table 1, Corollary 1 and group conventions, and visually inspected pp.2–3. For the simple/projective groups used here and natural dimension e>10, its non-subspace fixed-point ratio is below |x^S|^(−1/2+1/e+ι), with ι≤1/(e−2). For q odd, its subspace-maximal alternative is the stabilizer of a totally singular or nondegenerate proper subspace. The theorem applies to prime-order elements, so the projected order-two elements qualify. Large dimensions avoid all exceptional minimal-module identifications. [Burness author manuscript](https://seis.bristol.ac.uk/~tb13602/docs/fpr1.pdf); [published article](https://doi.org/10.1016/j.jalgebra.2006.05.024).

I read and visually inspected Liebeck–Pyber–Shalev Theorem 1.1 on manuscript p.2. It bounds the **number of actual maximal subgroups**, not merely conjugacy classes, by C r^(−2/3)|S| for simple Lie-type S of rank r. The author's use of the weaker Cq^(e²) is valid. [Author manuscript](https://www.ma.imperial.ac.uk/~mwl/WALL.PDF).

For Burness's classification, take G=G₀=S and H=M maximal. Definition 1 then quantifies over just M itself. Consequently every maximal subgroup falls into the stated subspace case or the non-subspace case to which the fixed-point estimate applies. No unproved structural classification was inserted into the new argument.

These are theorem uses, not new proofs of those published theorems. Burness's paper explicitly places the full proof across its companion papers II–IV; the current argument invokes the stated result.

## 2. Independent derivation of the subspace bound

I supplied the separate, complete [subspace lemma](../proofs/SUBSPACE_LEMMA.md) and compared the author's incorporation against it.

For nondegenerate k-subspaces of any fixed occurring type, full-isometry orbit–stabilizer gives the bounds

(21/128)q^(k(e−k)) ≤ N(e,k,type) ≤ 2q^(k(e−k)).

The symplectic order-product correction lies in [7/8,1]; the positive-dimensional orthogonal correction lies in [7/6,8/3]. The zero-space factor is one. There are at most two orthogonal subspace types and only one permitted symplectic type.

For totally singular k-subspaces, counting ordered bases through successive perpendicular quotients gives

T(e,k)=∏_{j=0}^{k−1} N_(e−2j)/(q^(k−j)−1),

where N_d counts nonzero singular vectors of the residual form. Their standard counts are q^d−1 in Sp, q^(d−1)−1 for odd orthogonal d, and (q^(m−1)+ε)(q^m−ε) for orthogonal d=2m. The residual even-dimensional sign is unchanged after removing hyperbolic planes. This yields

(1/2)q^Fσ(e,k) ≤ T(e,k) ≤ 8q^Fσ(e,k),
Fσ(e,k)=ke−(3k²+σk)/2,
σ=−1 in Sp and +1 in O.

The positive product correction is below four and the denominator correction is above one half. The even plus-type terminal hyperbolic plane is included, so both families of maximal singular subspaces are counted. Impossible dimensions give zero and are not used as positive denominators.

Now take x with eigenspaces A,B, of dimensions a,b≥e/3. Every x-invariant W decomposes into its intersections with A and B. If those dimensions are i,j and i+j=k≤e/2, the exponent loss for a nondegenerate W is

ib+ja−2ij ≥ ek/3−k²/2 ≥ ek/12.

For totally singular W, i≤a/2 and j≤b/2 imply ib+ja≥4ij, so its loss is

ib+ja−3ij ≥ (ib+ja)/4 ≥ ek/12.

The scalar linear terms in Fσ cancel. Summing possible dimensions and component types gives the valid common fixed-subspace probability bound

128(k+1)q^(−ek/12).

All relevant k-subspaces together number at most 12q^(ek). Degenerate invariant subspaces have invariant nonzero totally singular radicals; nondegenerate subspaces larger than e/2 can be replaced by perpendicular complements. Therefore this collection covers **every** reducible subgroup.

For e≥384, the author uses 128(k+1)≤256^k≤3^(8k)≤q^(ek/48). Raising the one-element bound to the 192nd power, and then counting subspaces, gives

P(reducible) ≤12Σ_{k≥1}q^(−11ek) <13q^(−11e)<(1/2)q^(−e).

Every inequality holds separately for every strong class. Arbitrary prescribed class sequences are therefore allowed; no averaging across classes, repeated-class assumption, or random-class law is used.

## 3. Orthogonal class transfer and subspace-orbit splitting

A strong involution x∈Ω(V) has large nondegenerate eigenspaces A,B. Its O-centralizer contains reflections of both spinor-norm classes supported inside A. Their determinant/spinor images generate O/Ω. Hence

O=ΩC_O(x), so x^O=x^Ω.

Thus a uniform Ω-class sample is a uniform full-O-class sample. For any fixed W, its stabilization probability equals the proportion of x-fixed points in the **full O-orbit** of W. This is true even if that orbit splits under Ω, including the familiar maximal-singular-space issue. The proof neither assumes subspace-orbit nonsplitting nor silently divides by the wrong orbit size. The same equality implies x^SO=x^Ω=x^O for the strong Ω involutions used here.

The argument is specific to these involutions. It is not a general assertion that all O-classes remain intact in Ω.

## 4. Projective passage, non-subspace bounds, and the lift back

Set S=J/Z(J). In these natural groups, |Z(J)|≤2. A strong involution x is noncentral, so its projective image has order exactly two. Projection maps x^J onto its S-class with equal fibers of size at most two. Independence and class-uniformity therefore survive projection without a probability loss. In particular, the possible conjugacy of x and −x is covered.

Natural class sizes give |x^J|≥(21/128)q^(ab), with ab≥2e²/9, hence

|x̄^S|≥(21/256)q^(2e²/9)≥q^(e²/5) for e≥16.

Since 1/e+1/(e−2)≤1/6, the inspected non-subspace estimate is at most q^(−e²/15). With 192 independent samples and at most Cq^(e²) actual maximal subgroups, the error is at most Cq^(−59e²/5).

The candidate's threshold

d₀=ceil(max{384, sqrt(log₃(2max{1,C}))})

indeed implies C≤q^(e²)/2. The non-subspace error is consequently at most (1/2)q^(−54e²/5)≤(1/2)q^(−e). Combining it with the reducibility bound proves projective generation with failure at most q^(−e).

Projective generation is sufficient upstairs for a specific reason: if KZ(J)=J, centrality and perfectness give J=(KZ(J))'=K'≤K. This rules out a missing-central-factor problem. No theorem about a projective involution with an order-four lift is needed or claimed.

## 5. The accepted Bray substitution

The new theorem has the closed strong balance range actually used in the previous bridge. It need not establish that bridge's broader provisional (1/4,3/4) hypothesis. Replace only that input and set c=192. The number of independent collection blocks is then 2c+1=385, and

L=ceil(κ^(−1)log n·log(385/η)), M=385L,

with κ=1/40000 in Sp and 1/10000000 in O/SO/Ω.

The previous orthogonal half-mass restriction, product-class law, first-success selection independence, exact C_G(t)'' identification, and extra-sample escape from a fixed subdirect graph remain the accepted second-pass arguments. The present proof does not discard the extra sample or mistake full projections for product containment.

At n≥max(49152,3d₀) in Sp, or max(98304,3d₀) in the orthogonal groups, the bridge's failure bound is

η+q^(−a)+q^(−b)+13q^(−2b²/9).

All substitutions and thresholds are correct. For η=1/20 it gives success above 0.9, and independent repetition supplies the stated arbitrary-confidence sample bound.

“High probability” should be accompanied by this precise confidence statement. A fixed constant times log n is proved sufficient for every **fixed** confidence, with a constant depending on that confidence. The current displayed bound does not itself prove 1−o(1) success as n grows with one fixed universal multiplier. For δ=n^(−A), the supplied amplification gives O((log n)²) samples. It is also a random-sample bound, not a full bit-operation, uniform-sampler, or exact-order-computation complexity result.

## 6. Why the old SO/generalized-Fitting wording was not repaired by assumption

I also inspected the Dixon–Praeger–Seress author manuscript, printed p.4. Its SO generation sentence cannot literally cover every strong SO-class. For an explicit infinite family, let V=H^(4m) be split of dimension 8m over any odd field and let A=H^(2m). Then x=−I_A⊕I_(A⊥) is strong and lies in Ω: its negative dimension is 4m and its spinor norm is (−1)^(2m)=1. Every conjugate in SO remains in the proper normal subgroup Ω, so no number of representatives from that class generates SO. This is an obstruction to that literal wording, not to the new Ω theorem. [Author manuscript](https://people.math.carleton.ca/~jdixon/Strong%20Involutions.pdf).

A central-factor variant shows why a literal generalized-Fitting target can also be unsafe. Over q=3, take V=H^(4m+1), of dimension 8m+2. The scalar −I has nontrivial spinor norm and lies in SO outside Ω, while a strong involution negative on H^(2m) lies in Ω. The central scalar belongs to the Fitting subgroup of SO, but cannot be generated by Ω-contained classes. The new proof invokes neither disputed wording.

The 2016 report's explicitly displayed sufficient Problem is a separate marginal probability assertion for a fixed t-eigenspace. The accepted first-pass natural-family marginal theorems already answered that narrower large-dimensional formulation independently of the generation input. The present pass now also establishes the generation conclusion in the stated natural scope. The database's broader one-line question should still not be silently enlarged to arbitrary similitudes, intermediate groups, non-natural representations, or arbitrary projective involutions. [Original report](https://ems.press/content/serial-article-files/46642).

## 7. Reproducible independent controls

The [stage certificate](../certificates/CLASS_GENERATION_STAGE.json) records exact arithmetic, exhaustive RREF subspace enumeration, and explicit-exception checks.

- 21 finite enumeration cases check symplectic spaces of dimensions 4 and 6 over F₃; both orthogonal signs in dimensions 4 and 6 over F₃; an odd orthogonal 5-space over F₃; and both orthogonal 4-space signs over F₅.
- For each case it checks total totally-singular subspace counts against the product formula, invariant singular counts against the eigenspace convolution, and invariant nondegenerate counts by discriminant against the same decomposition.
- It checks 2,255,650 integer exponent instances through e=120, respecting i+j=k and all relevant dimension constraints.
- Exact rational tests check constant absorption and the geometric tail comparisons.

Normal, -O, and -OO runs all passed with byte-identical JSON outputs (SHA-256 `8f93d4a94bb37e332a6a1d525d0b134efd4e2823719ed9ba489cb98739b13b89`). These finite controls guard against formula/implementation mistakes; they are not substitutes for the uniform proof above.

## 8. Publication boundary

Public authored artifacts are this audit, the independent subspace lemma, finite mathematical certificates, and the accepted mathematical proof. Programs are excluded from this reader. Third-party PDFs, source text extractions, response bodies, and page renders are private inspection evidence and are excluded. Public titles, source URLs, file sizes, hashes, and inspection status are recorded separately. Integrity hashes identify bytes, not mathematical truth.
