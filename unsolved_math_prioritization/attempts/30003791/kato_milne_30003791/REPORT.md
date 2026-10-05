# Linkage and vanishing in Kato–Milne cohomology

**Disposition:** no unrestricted resolution established. Both target implications remain unproved in this investigation for odd `p`. The literature search is bounded through 5 October 2026 and does not certify global openness. No novelty claim is made for the reductions or controls below.

## 1. Primary formulation and interpretation

The governing source is Adam Chapman's *Linkage in Kato-Milne Cohomology*, in the 2018 Oberwolfach report, printed pp. 1250–1251, especially Questions 4–5 ([primary PDF](https://ems.press/content/serial-article-files/46742), [DOI](https://doi.org/10.4171/OWR/2018/21)). Its two mathematical questions are:

\[
\text{Q4: }H_p^n(F)\text{ linked}\ \Longrightarrow\ H_p^{n+2}(F)=0\ ?
\]
\[
\text{Q5: }H_p^n(F)\text{ triple linked}\ \Longrightarrow\ H_p^{n+1}(F)=0\ ?
\]

Here `char(F)=p>0`, with `p` prime. The symbol degree `n` includes one additive slot and `n−1` logarithmic slots. The report refers to the analogous common-factor notion for symbols without supplying a full formal definition. This record uses the standard separable common-factor interpretation below, for `n≥2`; it does not manufacture an `n=1` convention. The report's general-p algebra display erroneously retains quadratic exponents. The correct general-p relations are `i^p−i=a`, `j^p=b`, `jij^−1=i+1`, as in its cited 2017 paper. Both primary pages were inspected visually.

### Exact common-factor convention

Use `H_p^{q+1}=coker(℘:Ω^q→Ω^q/dΩ^{q−1})`, and `ν_F(k)=ker ℘` in differential degree `k`. Logarithmic symbols in `ν_F(k)` act by exterior product on the Kato–Milne groups.

A family of symbols `s_i∈H_p^n(F)` is **separably (n−1)-linked** if there are one symbol `θ∈H_p^{n−1}(F)` and nonzero `c_i∈F` with `s_i=θ∧dlog c_i` for every `i`. Equivalently, presentations have the same additive entry and the same `n−2` logarithmic entries. The factor may depend on the family.

In this record, **linked** means this condition holds for every pair of symbols; **triple linked** means it holds for every triple. This is a universal quantifier over symbols over the given field, not a condition imposed on all extensions and not a single global factor shared by all symbols.

For comparison, **inseparable (n−1)-linkage** means a common logarithmic symbol in `ν_F(n−1)`, with the additive entry allowed to vary. **Total separable one-linkage** of two symbols means their entire sets of factors in `H_p^1(F)` agree. Neither should silently replace the target hypothesis. Precise definitions are in Chapman–McKinnie §1.4 and Chapman–Dolphin §2.2 ([2018 paper](https://arxiv.org/abs/1705.09553), [2019 paper](https://arxiv.org/abs/1806.03603)).

## 2. Established literature and what it does not settle

1. **Characteristic two.** The linked-field implication and its higher-Pfister analogues are established prior results. Chapman–Dolphin's Theorem 4.3 gives `H_p^4=0` assuming isotropy of every Albert p-form; for `p=2`, their Remark 4.1 identifies the required isotropy with linkage. Their Question 4.6 explicitly isolates the odd-prime issue in degree two. The higher-degree characteristic-two linked result is recorded in the 2018 primary report and discussed in *Common slots of bilinear and quadratic Pfister forms*. Chapman–Dolphin–Leep Theorem 3.3 (`n≥3`) and Theorem 4.4 (`n=2`) establish the characteristic-two triple-linkage vanishing. These known results are not claimed as new proofs here. [2017 paper](https://arxiv.org/abs/1701.01367), [2018 triple-linkage paper](https://arxiv.org/abs/1706.04929), [common-slots paper](https://doi.org/10.1017/S0004972718000229)

2. **Total linkage, 2019 publication.** Chapman–Dolphin Corollary 3.3 proves that for `π=θ∧dlog b` and `ω=θ∧dlog c`, total separable one-linkage makes `θ∧dlog b∧dlog c` zero, for every prime characteristic. Its Proposition 3.2 gives a specific sufficient common Artin–Schreier factor. This requires transfer of specified factors, not merely existence of some common factor for every triple. The paper appeared in *Journal of Number Theory* 199 (2019), 352–362; the inspected manuscript is arXiv v3 of November 2018. [paper](https://arxiv.org/abs/1806.03603)

3. **Degree three, 2020 publication.** Chapman's Theorems 4.3–4.4 show that vanishing of the appended class for a pair of degree-three division symbol algebras yields inseparable linkage after an extension of degree at most two, and over the original field when it is quadratically closed. This is a conclusion about a pair under an already-assumed vanishing condition. It is not a proof of either universal vanishing implication. [paper](https://arxiv.org/abs/1901.00358)

4. **Common splitting fields, 2023 publication.** Chapman–Florence–McKinnie Theorem 4.7 and its proof produce common cyclic presentations for finite families of `p^m`-symbol algebras with a prescribed common simple purely inseparable splitting field. Corollary 4.8 permits larger common cyclic splitting fields. No reduction from universal separable linkage of `H_p^n` to the required inseparable hypothesis is supplied by those statements. Enlarging the splitting degree from `p` to a power of `p` is not the degree-p linkage required here. [paper](https://arxiv.org/abs/2012.07496)

5. **Prime-to-p extensions, 2024.** Chapman's Theorem 3.3 extends the vanishing-to-inseparable-linkage direction to all primes, allowing a finite extension of degree prime to `p`. Corollary 3.5 specializes this to p-special fields with `H_p^3=0`. Remark 3.6 explicitly notes presentation dependence of the appended `H_p^3` element for odd primes. None reverses the implication needed for Q4/Q5. The inspected PDF is arXiv v1; the author's publication list records the journal article in *Rendiconti del Circolo Matematico di Palermo* 73 (2024), 2527–2531. [paper](https://arxiv.org/abs/2403.11154)

6. **Other later work checked.** *Linkage of sets of cyclic algebras* constructs finite families lacking a common maximal subfield; it does not establish universal linkage of a field with a surviving target class. *Classes in H_{p^m}^{n+1}(F) of lower exponent* concerns symbol-length bounds when decreasing the exponent, a different hypothesis. The latter's abstract and 2026 publication metadata were checked; its full proof was not audited. June 2022 Brauer Group Meeting notes discuss higher linkage numbers for quaternion algebras, rather than settling the present odd-prime cohomological implications. [sets](https://arxiv.org/abs/2104.08349), [lower exponent](https://arxiv.org/abs/2409.16447), [2022 meeting notes](https://math.haifa.ac.il/ufirst/Events/BGM_problems.pdf)

Publication dates were cross-checked against the [author's institutional publication list](https://www.cs.mta.ac.il/staff/Adam_Chapman/publications). Source dates were read from the papers rather than treating search-engine crawl dates as publication dates. No unpublished manuscript or restricted source was relied upon.

## 3. Five substantive approaches and exact stops

### Approach 1: common-factor compression

Separable pair linkage makes the sum of two degree-n symbols a symbol, via `θ∧dlog x+θ∧dlog y=θ∧dlog(xy)`. Induction therefore proves symbol length at most one in `H_p^n`. This is fully proved in `proofs/elementary_controls.md`, §2.

**Stop:** symbol compression concerns addition in degree `n`. Appending new logarithmic factors raises the degree, and there is no demonstrated argument forcing the resulting class to vanish. We do not assume an arbitrary product of two Kato–Milne classes is defined.

### Approach 2: p-bases and exterior degree

A finite p-basis of size `r` gives `dim_F Ω^1=r`, so `H_p^m=0` for `m>r+1`. Thus Q4's conclusion holds whenever `r≤n`, and Q5's whenever `r≤n−1`, without needing linkage. Full proof: §3.

**Stop:** neither target assumption has been shown to imply the respective p-rank bound. Replacing the arbitrary field by a small-p-rank field would change the problem. The iterated-Laurent construction in §5 proves the bound is sharp as a statement depending only on p-rank: `H_p^{r+1}(K_r)≠0`.

### Approach 3: Albert p-forms and norm identities

In degree two, the 2017 Theorem 4.3 reduces vanishing of `H_p^4` to isotropy of all Albert p-forms. Theorem 4.4 gives a related sufficient pure-part isotropy hypothesis for `H_p^3`. Their proofs use norm-preserving symbol changes and exact differential identities; those portions were inspected.

**Stop:** the general implication from separable linkage to isotropy of the relevant Albert p-form is only supplied there for `p=2`. In odd characteristic, the reverse direction of their Remark 4.1 cannot simply be used. No substitute linking the universal triple hypothesis to the required pure-part isotropy was obtained. This is an identified missing implication, not a claim that the implication is false.

### Approach 4: forcing an already chosen factor

The 2019 total-separable-linkage result would settle Q5 under a stronger total-factor hypothesis. An even more elementary sufficient condition is total inseparable one-factor sharing for each pair `θ∧dlog b, θ∧dlog c`: rewrite the first with factor `dlog c`, then append that same factor and use alternation. This restricted implication has a complete proof in §4.

**Stop:** triple linkage gives existence of a common factor depending on the triple. It does not explicitly promise preservation of the particular factor needed in this argument. No valid construction of a third symbol forcing that specified factor was found. The elementary sufficient condition is not reported as an equivalent reformulation of Q5.

### Approach 5: descent, valuation controls, and presentation consistency

The 2024 prime-to-p result starts with vanishing and concludes linkage after extension. Attempting to use it in reverse leaves its central hypothesis unproved. Restriction–corestriction can descend a vanishing class across a finite prime-to-p extension, but cannot manufacture vanishing or show universal linkage persists with the needed strength after extension.

Two exact controls rule out tempting shortcuts:

- Over `K_n=F_p((t_1))...((t_n))`, a displayed linked pair of degree-n symbols has a nonzero appended degree-`n+1` class. Over `K_{n+1}`, a displayed linked triple has a nonzero appended degree-`n+2` class. A constant-coefficient functional is proved to annihilate both exact forms and Artin–Schreier images and takes value one on each top class. These fields are not asserted universally linked.
- The algebra isomorphism `[a,b)≅[-a,b^{-1})`, applied to both members of a pair, changes the appended class to its negative. For odd `p`, the Laurent detector makes the difference explicit. This reproduces the 2024 sign obstruction. Zero/nonzero is unchanged by negation, so the control does not itself refute a vanishing criterion.

Complete proofs: §§5–6. Exact sparse crossed-product and Laurent-polynomial checks are in `code/check_controls.py`. They are consistency tests, not finite tests of the universal field hypotheses.

## 4. Remaining mathematical work

A full affirmative solution must establish, for **every** characteristic-p field under the exact universal hypothesis, vanishing of every generating symbol in the claimed higher degree. In the approaches above, the missing bridges are:

- Q4: upgrade common-factor linkage to a usable higher-degree norm/isotropy identity, without importing a characteristic-two converse;
- Q5: use universal triple linkage to force the prescribed common factor or another identity killing every appended symbol, rather than merely locating some factor for a selected triple.

A negative solution must instead supply an actual field satisfying the entire universal pair/triple linkage hypothesis and a nonzero class in the specified target group. Our selected-family controls do not do that.

## 5. Prior-work and verification limits

A current main-branch attempts listing was checked, and exact-ID PR, commit, branch and code searches returned no target match. Topic searches found no matching Kato–Milne attempt. Available prior-conversation retrieval yielded unrelated problems and no usable exact-target research. These checks are stronger than reading a queued catalog label, but cannot exclude deleted branches, unindexed work or inaccessible private artifacts.

The numeric registry page could not be read: the web reader failed and a direct request returned HTTP 403. No alternate route to that restricted page was attempted afterward. A separate public dataset filter returned HTTP 500. Therefore no successful current dataset-row comparison is claimed; the exact mathematical target is anchored to the independently retrieved primary report, while the ID-to-title/source association comes from the supplied public catalog descriptor. Full corpus hashes, if mentioned in source metadata, are not portrayed as newly verified corpus downloads.

The supplied control program passed and was replayed from a different working directory. A fresh uninvolved audit remains a prerequisite to publication. No push, PR, queue update or other remote write was performed in this investigation.
