# Independent sign-rotation audit of PR 1151 / problem 30003321

Audit family: `sign_rotation_01`. The audit was completed independently after the target and approach seal. This report concerns the exact bytes of `../../inputs/PROOF.md` recorded in `candidate_receipt.json`.

## Verdict and scope

**ACCEPT: the candidate proves the complete assigned statement, relative to its explicitly identified standard primary-source results.** I found no mathematical gap requiring repair. In particular, the sign rotation is valid for arbitrary set ordinals, including limits, and for initial exponent classes that are proper classes. Its crucial right-predecessor implication has the correct direction. The proof handles the trivial group separately and never assumes multiplicative closure or a simplicity-preserving group isomorphism.

This is an independent mathematical audit, not a proof-assistant certificate or a novelty/priority finding. I did not read an old audit, acceptance record, another family's output, or root conclusions. The candidate itself contains assertions about previous audits at lines 3, 7 and 93; these were encountered as part of reading the authorized file and supplied **no evidence** for this verdict. No priority search was performed. No git state was changed, and no outside person or sibling agent was contacted.

## Reconstructed original target and primary dependencies

The [OWR 60/2016 report](https://ems.press/content/serial-article-files/46663), Kaplan's contribution on joint work with Ehrlich, printed p. 3356 / PDF p. 44, asks: “Is every discrete initial subgroup of No isomorphic to an initial subgroup of Oz?” The same target is Question 9.1 on printed p. 15 of the [Ehrlich–Kaplan II author manuscript](https://elliotakaplan.github.io/Number_systems_with_simplicity_hierarchies_II.pdf).

The assigned claim makes the additive ordered-group meaning explicit and also includes `{0}`. Initiality means sign-prefix closure. The manuscript's introduction explicitly works in NBG with global choice and includes sets and proper classes. Neither the question nor the audited theorem requires a ring isomorphism or preservation of the original simplicity ordering.

I checked the following dependencies directly in the author manuscript:

- §2, printed pp. 2–3: the sign-sequence model, lexicographic order with `− < undefined < +`, proper-prefix simplicity, and the meaning of right predecessors.
- §3, printed pp. 4–6 and Proposition 3.3: ordinal-length normal forms and the canonical ordered-group correspondence with Hahn series.
- Lemma 5.1, printed p. 7: a nonzero initial real coefficient group either contains all dyadics or equals `2^(−n) Z`.
- Theorem 5.1, printed pp. 7–9, including the full displayed proof: initiality is characterized by truncation closure, cross sectionality, initial exponents, initial real coefficient groups, and dyadic inclusion at every right predecessor.
- §6.2, printed p. 11: the normal-form criterion for Oz used by the candidate.

The latter two are additive-group and membership results with exactly the hypotheses the candidate uses. The ring-only Theorem 6.2 is not used. These established results are accepted inputs; I did not recursively reprove every earlier theorem cited in their published proofs. Source bytes, hashes, retrieval times, selected-page renders, and precise reading scope are recorded separately. The source authenticated here is the designated author-hosted manuscript, not publisher-PDF bytes.

## Bottom-exponent lemma

Candidate lines 28–34 are correct. Let `g>0` be the least positive group element, with leading term `r ω^m`, `r>0`. If its tail `h` is nonzero, truncation closure and subtraction put `h` and `|h|` in the group. The support of `|h|` lies strictly below `m`. Therefore `g−|h|` still has leading coefficient `r>0` at exponent `m`, so `0<|h|<g`, irrespective of the sign of the original tail. This contradicts minimality. Thus `g=r ω^m`.

A smaller positive member of `R_m` would give a smaller positive group element, so `r` is the least positive real coefficient in `R_m`. A group containing all dyadics has no such least coefficient. The checked real-coefficient classification therefore gives `R_m=2^(−n)Z` and `r=2^(−n)`.

If an exponent `y<m` existed, cross sectionality would give `ω^y` in the group, and the leading-term ordering gives `0<ω^y<rω^m`, again impossible. Hence `m` is the minimum of the exponent class. If a sign of `m` were plus, its prefix immediately before that sign would be a smaller exponent in the initial class. Thus `m` has only minus signs, including the empty possibility: `m=−α` for an ordinal `α`.

This derivation does not assume finite support, finite birthday, a set-sized group, or that each coefficient appearing in a series belongs individually to its coefficient group without first using truncation closure and subtraction.

## Independent arbitrary-ordinal verification of the rotation

Write `a=(−)^α`, `e` for the empty sequence, and juxtaposition for ordinal concatenation. For clarity, the construction extends beyond the candidate's exponent class to the entire interval

`I_a={s : s≥a}`.

For `s>a`, exactly one of the following occurs:

1. **A0:** `s=(−)^β` with `β<α`.
2. **A1:** `s=(−)^β (+) u` with `β<α` and an arbitrary ordinal-length tail `u`.
3. **B:** `s=a (+) t` with an arbitrary ordinal-length tail `t`.

A0 and A1 together are candidate case A. This partition follows by comparing `s` with the all-minus word `a` at the first differing or terminating position. If `a` is a proper prefix, the next sign must be plus, since `s>a`. No predecessor of an ordinal is assumed to exist.

The candidate's map is

- `f(a)=e`;
- `f(s)=(+)s` in A0 or A1;
- `f(a(+)t)=(+)at` in B.

### Explicit inverse, including transfinite tails

For a nonzero nonnegative word `z`, write it uniquely as `z=(+)w`. Define

- `q(e)=a`;
- if `w=at`, set `q(z)=a(+)t`;
- if `a` is not a prefix of `w`, set `q(z)=w`.

In the final case `w>a`: a word below `a` would have to extend `a` to the minus side, and hence would have `a` as a prefix. In the middle case `q(z)>a` by its displayed plus. The two nonempty cases are disjoint. Direct substitution proves both `q(f(s))=s` and `f(q(z))=z`. Thus `f` is bijective from `I_a` to all nonnegative sign sequences, and its restriction to the candidate's `Gamma` is onto `Delta=f[Gamma]`.

This inverse uses the ordinal order type of a suffix, never integer subtraction from a limit length. For example, removing an initial plus from a word of length `ω` leaves a tail of order type `ω`, not a nonexistent ordinal `ω−1`. This fact does not obstruct decomposition: concatenation is the order sum of disjoint blocks. The suffix after a specified prefix has a unique ordinal order type.

### Order, collisions, and all cross-branch cases

Prepending or substituting a fixed common prefix preserves comparison of tails, including termination against a sign. It also preserves and reflects proper-prefix relations. This elementary statement holds at every ordinal length: the first differing tail position is carried by the unique order isomorphism of the tail block into the concatenation.

Consequently A/A comparisons reduce to the original source words, and B/B comparisons reduce to their tails. For the mixed cases:

- If `s` is in A0 and `v=a(+)t` is in B, `s` is a proper prefix of `v`, whose next sign is minus. Hence `s>v`. Likewise `(+)s` is a proper prefix of `(+)at`, with next sign minus, so `f(s)>f(v)`.
- If `s` is in A1 with first plus at `β<α` and `v` is in B, the first different signs are plus for `s` and minus for `v`. After the common prepended plus, exactly the same signs differ. Neither pair is prefix-comparable, and again `s>v` and `f(s)>f(v)`.
- The source minimum `a` maps to `e`, below every other image, all of which start with plus.

These cases exhaust every ordered pair, including the reverse mixed comparisons. They rule out every collision. They show strict order preservation on the full interval and preservation/reflection of the proper-prefix relation whenever both arguments differ from `a`. The inverse above additionally proves surjectivity explicitly.

### Complete prefix identity

For every `s>a`, the identity needed by the candidate is exactly

`Pref(f(s)) = {e} ∪ {f(v) : v∈Pref(s), v≠a}`,

where `Pref` denotes proper prefixes.

In A, a proper prefix of `(+)s` is either `e` or `(+)v` for a proper prefix `v` of `s`. Such a `v` cannot have `a` as a prefix, because then `s` would also have it. Hence `(+)v=f(v)`.

In B, `s=a(+)t`. A proper prefix of `(+)at` is exactly one of:

- `e=f(a)`;
- `(+) (−)^β=f((−)^β)` for `β<α`;
- `(+) a u=f(a(+)u)` for a proper prefix `u` of `t`.

The final family includes `(+)a` when `t` is nonempty and `u=e`. When `t=e`, `(+)a` is the whole image and is correctly excluded. Every boundary between blocks and every cutoff inside a block is covered by the ordinal order-sum decomposition. There is no missing limit prefix.

All preimages in this identity are actual source prefixes, except that the new empty prefix is the image of the existing minimum. Thus initiality of `Gamma` gives initiality of `Delta`. No closure of an initial class under taking an unforced limit completion is used.

### Right predecessors: exact direction matters

Suppose `f(y)` is a right proper prefix of `f(x)`. The child image cannot be empty because empty has no predecessors. The parent image cannot be empty because empty is the least element of `Delta`. Therefore `x,y≠a`. The preceding prefix equivalence gives that `y` is a proper prefix of `x`; order preservation gives `y>x`. This is precisely the source right-predecessor relation required by Theorem 5.1.

The rotation can **delete** old right predecessors of the source minimum. It does not preserve the right-predecessor relation on all source pairs. For instance, with `a=−`, source `e` is a right predecessor of `a`, but image `+` is not a predecessor of image `e`. This is harmless: the theorem only needs absence of newly created right predecessors. It is also why replacing the candidate's implication by a global equivalence would be incorrect. For children other than `a`, the relation is preserved in both directions.

The new prefix relation from the image `e=f(a)` to A images is always a left-predecessor relation. It creates no dyadic-coefficient requirement at the newly integral bottom coefficient.

## Boundary and falsification cases

- **`α=0`:** A is empty. Any positive source is `(+)t`, and B sends it to itself. The minimum remains empty. Thus `f` is the identity on the nonnegative interval.
- **Empty source word with `α>0`:** it is A0 with `β=0`, and maps to `+`. The only proper prefix of that image is empty, supplied by `a`.
- **A successor `α`:** the all-minus prefix of length `α−1` is handled by A0, not by assuming any uniform integer index for the removed plus. The B boundary word `a(+)` maps to `(+)a` and has exactly the prefixes described above.
- **`α=ω`:** `a` maps to empty; each finite all-minus word `(−)^n` maps to `(+) (−)^n`; and `a(+)`, if present, maps to `(+) (−)^ω`, a word of length `1+ω=ω`. That limit image's proper prefixes consist of empty and the finite displayed spine images. A descendant's prefix of length `ω` is present exactly when forced by the source prefix `a(+)`.
- **Missing limit node:** if `Gamma` consists only of `(−)^β` for `β≤ω`, its image is `{e} ∪ {(+) (−)^n:n<ω}`. It is initial although it omits `(+) (−)^ω`. The candidate correctly does not insert that unforced completion.
- **`α=ω+1`:** the source proper prefix `(−)^ω` maps to `(+) (−)^ω`. This is the limit prefix inside the image of `a(+)`, demonstrating that limit prefixes also occur within successor-length spines.
- **Arbitrary limit and uncountable `α`:** the general block-cut proof applies verbatim. It uses no countability, enumeration by natural numbers, immediate predecessor of `α`, or arithmetic cancellation of a final ordinal summand.
- **Singleton exponent class:** initiality forces `Gamma={0}`. The group is `2^(−n)Z`, and the coefficient rescaling gives `Z`.
- **Trivial group:** `{0}` is initial in No and contained in Oz; the identity supplies the separate case.

The finite diagnostics intentionally tested an overly strong right-relation equivalence before testing the exact candidate condition. Its failure and correction are preserved in `DIAGNOSTIC_HISTORY.md`. With the correct condition, the check passed for finite `α=0,…,8`, all sign words of length at most 8, 4,097 source nodes, and 1,923,413 ordered pairs. Exact rational dyadic values provided an independent finite comparison oracle. The checks cover inverse identities, order, complete proper-prefix identities, initiality of the image, the no-new-right-predecessor implication, and prefix equivalence away from the old minimum. These are diagnostics only. The arbitrary-ordinal proof is the block argument above.

## The group transformation and final hypotheses

Let `c_m=2^n` and `c_y=1` otherwise. Relabel each exponent by `f` and each coefficient at `y` by multiplication by `c_y`, exactly as in candidate lines 67–73. An increasing injective relabeling carries a set-sized reverse-well-ordered support to one of the same order type. It therefore defines a surreal normal form. This includes supports with limit order type and supports approaching the bottom exponent without containing it.

Coefficientwise addition and positive scaling show additivity and preservation of the sign of the first nonzero coefficient. Thus `T` is an injective ordered-group homomorphism. Its inverse on `H=T[G]` is explicitly

`U(Σ b_z ω^z)=Σ c_(q(z))^(−1) b_z ω^(q(z))`.

The same support argument makes this formula legitimate, and the two substitution identities give `UT=id_G` and `TU=id_H`.

For the canonical Hahn image of `H`, every hypothesis of the checked Theorem 5.1 holds:

1. Its exact exponent class is `Delta`, already proved initial and nonnegative.
2. A truncation corresponds to the same initial segment of the source support and hence lies in `H`.
3. For each nonbottom exponent, the source leader maps to the target leader; at zero the source least positive element maps to `1`. This proves cross sectionality even when `n>0`.
4. One-term images have one-term preimages, so the coefficient groups are exactly `Z` at zero and the unchanged `R_y` at other exponents. They are initial real subgroups.
5. Every target right predecessor comes from a source right predecessor at a nonbottom exponent. Its source coefficient group contains the dyadics and was not rescaled. Thus no required inclusion is lost by normalizing the bottom group to `Z`.

The theorem supplies initiality in **No**, a stronger property than the inherited initiality in Oz requested in the question. Nonnegative exponents and the integral zero coefficient give membership in Oz by the checked criterion. This proves the full desired model for the actual image of `G`; it never fills `G` out to a full Hahn group or assumes that arbitrary infinite sums belong to it.

As a concrete consistency calculation, the primary example `D+Z/ω` has exponents `{-1,0}`, bottom coefficient group `Z`, and `f(-1)=0`, `f(0)=1`. The construction gives `d+a/ω ↦ dω+a`, matching the advertised elementary example. For exponents `{-2,-1,0}`, the rotation gives `{-2,-1,0} ↦ {0,1/2,1}` in increasing order; the middle fractional positive exponent is permitted in Oz.

## Proper classes, remaining gaps, and optional exposition

`α` is a set ordinal because it is the sign length of one surreal. Concatenations and suffixes of each individual word are sets, however large the ambient class. The formulas for `f`, `q`, `T`, and `U` are elementary class definitions with set parameters and the supplied class `G`. NBG replacement sends each set support to a set. The image class `H` exists by elementary comprehension, and all algebra involves finitely many elements with set supports. No class-long sign string, non-set support, global enumeration of `G`, or stronger class-recursion principle is introduced.

**Unresolved mathematical gaps in the candidate, within the verified dependency scope: none found.** No rigorous repair was needed. The explicit inverse and expanded ordinal prefix proof above are independently checkable supplements to the candidate's shorter reasoning.

One optional wording improvement is available at candidate line 63: its limit example's empty proper prefix comes from `f(a)`, while its nonempty proper prefixes come from the nodes `(−)^β`, `β<α`. Equation (1) and the main initiality proof already include empty correctly, so this compressed explanatory sentence is not a gap in the theorem.

The remaining limitations are evidentiary scope: established literature inputs were checked in the author manuscript rather than rederived from foundational axioms, no formal verifier was used, and no priority conclusion was attempted.
