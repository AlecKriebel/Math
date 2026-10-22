# Independent adversarial audit: PR1151 / Problem 30003321

Family: `hahn_image_01` — exact canonical Hahn image, coefficient groups, support transport, and simplicity obligations.

Verdict: **ACCEPT the complete mathematical claim relative to the explicitly cited established results of Ehrlich–Kaplan.** No mathematical correction or unresolved bridge was found in `inputs/PROOF.md`. This verdict covers nontrivial and trivial groups, sets and proper classes in NBG with global choice, an ordered additive-group isomorphism onto an initial subgroup of Oz, and arbitrary set-sized reverse-well-ordered supports. It does not assert priority, external peer review, or formal proof-assistant verification.

## Independence and target reconstruction

The independent approach was sealed at `2026-10-18T00:33:09.131181+00:00`, before reading the candidate. The seal's SHA-256 is `d88f88d0abcf9cf5d60ccd0653d50892726af7775cba58da4ff91d05362fd3b4`. Before that point I read only the supplied AGENTS.md and the two specified primary sources. I did not access the old AUDIT_REPORT, ACCEPTANCE, root verdict, sibling reports, or any historical audit material. The candidate itself contains historical-acceptance prose; that prose was not treated as mathematical evidence.

OWR60/2016, printed p.3356 (PDF p.44), asks whether each discrete initial additive subgroup of No has an ordered-group copy that is initial in Oz. The later manuscript repeats that target as Question 9.1, printed/PDF p.15. Its context explicitly distinguishes the group question from the theorem about initial subdomains. The manuscript's standing set theory is NBG with global choice, and its use of “class” includes sets and proper classes. The audit adds the zero-group convention specified in the candidate. No ring structure, simplicity-preserving isomorphism, or assertion that the original subgroup already lies in Oz is part of the target.

The precise success criterion is an explicit map T and subgroup H with T:G→H a bijective ordered additive-group homomorphism, H⊆Oz, and H initial in No (hence also initial with the induced simplicity order in Oz). A merely injective map, an initial exponent order embedding without coefficient checks, or a completion of G inside a larger Hahn group would not suffice.

## Primary dependencies and their exact role

The inspected author manuscript is the PDF at `https://elliotakaplan.github.io/Number_systems_with_simplicity_hierarchies_II.pdf`, SHA-256 `c6d91a1850514736d88c576cafe1f4cedf1e3dcb84a2a96418648cd4fc1a5160`, 351864 bytes. Source identity here is the exact public author-hosted byte stream; I did not authenticate a publisher PDF.

The normal-form preliminaries and Proposition 3.3 (pp.4–6) provide the canonical ordered-group identification of No with real Hahn series having set-sized decreasing supports. Lemma 5.1 (p.7) classifies nonzero initial real coefficient groups as dyadic cyclic groups or groups containing all dyadics. Theorem 5.1 (p.7; proof pp.7–9; reformulation p.9) characterizes the actual canonical image by truncation closure, cross-sectionality, initial exponent class, initial real coefficient groups, and the dyadic requirement at right simplicity predecessors. Section 6.2 (p.11) gives Oz's nonnegative-exponent/integer-constant-term description. These are imported results, not new conclusions of the candidate. Their manuscript hypotheses match their use in the proof.

The candidate's new bridge is Lemma 2: relocating the least exponent to zero while preserving all relevant right-predecessor implications. Lemma 1 and the transport/checking argument supply the remaining deductions from the imported results. The domain theorem (Theorem 6.2) is not used to settle the group question.

### Important theorem-hypothesis distinctions

- The exponent object in Theorem 5.1 is an **initial ordered subclass**, not necessarily an additive subgroup. The candidate needs only order preservation by f, and never assumes f additive.
- A canonical Hahn image is an actual truncation-closed subgroup. It need not be the unrestricted collection of every series with coefficients in its coefficient groups. The candidate correctly transports only source elements.
- The coefficient group at y is defined by **pure monomials**: R_y={r:rω^y∈G}. The target computation uses this exact definition.
- The dyadic condition is on the **right** simpler exponent y: y is a proper prefix of x with y>x. It is not an unconditional dyadic condition at all exponents.
- Left simpler exponents enter the monomial cut through integer multiples; cross-sectionality and addition supply those. No additional left-side dyadic hypothesis has been silently omitted.

## Full proof audit

### Lemma 1: bottom exponent and bottom coefficient group

Candidate lines 28–34 are valid. Let g be least positive and write g=rω^m+h with r>0 and all exponents of h below m. If h≠0, truncation closure and subtraction put h and |h| in G. Normal-form order gives |h|/ω^m infinitesimal, so |h|<rω^m/2 while g>rω^m/2. Thus 0<|h|<g, contradicting minimality. This works for tails of every set-sized support order type; no last term is required. Consequently g is a single monomial.

A positive coefficient smaller than r in R_m would give a smaller positive group element, so r is least positive in R_m. The initial-real-group classification then forces R_m=2^(−n)Z and r=2^(−n), with n≥0. A coefficient group containing D cannot have a least positive member.

Cross-sectionality puts ω^y in G for every exponent y. If y<m, ω^y is infinitesimal relative to ω^m and hence smaller than 2^(−n)ω^m; thus no such y exists. The leading exponent m is therefore the minimum of the entire exponent class, not merely the support of g.

If a sign of m were plus, the proper prefix immediately before that plus would be smaller than m and belong to the initial exponent class, a contradiction. Thus m is the all-minus sequence −α for a set ordinal α. This reasoning covers α=0 and limit α. It also agrees with the independently inspected Proposition 5.2 (p.10), although that proposition is not needed by the candidate.

### Lemma 2: independent structural verification

Let a be the all-minus sequence of length α and e the empty sequence. For s>a there are exactly two possibilities:

1. A: s does not extend a. It is either an all-minus proper prefix of a, or it first diverges from a by a plus at an index β<α.
2. B: s=a·(+)·t, uniquely. A minus immediately after a would instead make s<a.

The candidate sets f(a)=e, f(s)=(+)·s in A, and f(s)=(+)·a·t in B. All operations are concatenations of well-ordered sequences. They are not subtraction or arithmetic shifting of ordinal positions.

Within A, prefixing the same sign preserves order and prefix relations. Within B, replacing a common prefix by another common prefix does the same. Across A/B, an A-node that is an all-minus proper prefix of a is a right prefix of each B-node; its image is likewise a right prefix of the corresponding image. Otherwise an A-node first differs from every B-node by a plus versus a minus, and the images have the same first difference after their common initial plus. This verifies strict order, injectivity, and both directions of proper-prefix equivalence on Γ\{a}. There is no A-node below any B-node; this cross-case order is consistent with the construction.

For every s>a the exact proper-prefix identity is

    Pref(f(s)) = {e} ∪ { f(v) : v∈Pref(s), v≠a }.

In A this is immediate by stripping the initial plus. In B, the prefixes of (+)·a·t fall into the empty prefix, (+)·(−)^β for β<α, and (+)·a·u for proper prefixes u of t. Their preimages are respectively a, (−)^β, and a·(+)·u. This is exhaustive for arbitrary ordinal α and arbitrary ordinal-length t: a prefix of a concatenation cuts either inside the fixed prefix or inside the tail. No cardinality, successor-length, or eventual-constancy assumption is used. Since Γ is initial, every listed preimage belongs to Γ, so Δ=f[Γ] is initial.

Every nonempty image starts with plus, so Δ has minimum zero and is nonnegative. If f(y) is a right prefix of f(x), neither x nor y is a: f(a)=0 is least, and zero has no proper prefix. Prefix equivalence away from a plus monotonicity gives y∈R_s(x). Thus the needed implication has the correct direction. Relations with a can be lost; no new right relation is created. A new left prefix at zero is harmless because H will contain the integer multiples of 1.

Boundary checks: α=0 makes the construction the identity on nonnegative sign sequences. If α is a nonzero limit, the image of a·(+) is the actual set-length sequence (+)·(−)^α. Its prefixes come from the already-present shorter all-minus source nodes. This introduces no assumed limit completion in Γ. If Γ={a}, initiality forces a=e, so this degenerate exponent case is also covered. For finite all-minus chains, the map converts the chain above its minimum into a descending positive chain above zero, with the source minimum alone sent to zero.

The finite diagnostic separately enumerates all sign sequences of length ≤12 above each minimum −α, α=0,…,12. Injectivity, order, the exact prefix identity, initiality, and all right-predecessor implications passed. These tests are diagnostic only. The preceding sequence-concatenation proof is what covers limit lengths.

### Transport: exact source image, arbitrary supports, and group structure

Candidate lines 67–73 define fixed positive scalars c_m=2^n and c_y=1 otherwise, then replace each term r_yω^y by c_y r_y ω^{f(y)}. Because f is increasing and injective, a decreasing support indexed by any set ordinal retains precisely its support order type. Each image support is a set by NBG class replacement; hence the output is an actual surreal normal form. No new infinite series is admitted just because its coefficients look allowable.

For two source series, addition is coefficientwise on the union of their supports. Relabeling introduces no collisions and each coordinate uses the same scalar in every element, so T(g+h)=T(g)+T(h). Nonzero coefficients remain nonzero. The first nonzero coefficient in a difference retains its sign, proving injectivity and strict order preservation. H=T[G] is closed under addition and inverses, and T is onto H by its definition. In particular the argument proves an isomorphism onto its target subgroup; it does not merely exhibit a map into Oz.

### Complete Theorem 5.1 application to H

| Required hypothesis | Verification |
| --- | --- |
| Actual exponent class equals Δ | No transformed term leaves f[Γ]; conversely every f(y) has its pure unit monomial in H by the cross-section check below. |
| Δ initial in No | Exact prefix identity proved above. |
| Truncation closure | The same ordinal-index initial segment before and after relabeling gives trunc(T(g))=T(trunc(g)). This includes limit-index truncations. |
| Cross-sectionality | For y≠m, ω^y maps to ω^{f(y)}. At f(m)=0, the least positive source monomial 2^(−n)ω^m maps to 1. Mapping ω^m itself to 2^n does not cause a failure because the smaller source monomial exists. |
| Exact initial coefficient groups | A one-term image can come only from a one-term source, since f is injective and nonzero coefficients stay nonzero. Thus the group at zero is exactly 2^n R_m=Z, and at f(y), y≠m, it is exactly R_y. All are initial in R. There is no unproved assertion that an arbitrary coefficient appearing deep inside a source support belongs to R_y. |
| Right simpler dyadics | Any right pair in Δ pulls back to a source right pair. Its upper/right endpoint cannot be m, whose image is minimum zero. Its coefficient group is therefore unchanged and contains D by the source theorem. |
| Left simpler cut options | Cross-sectionality supplies every unit monomial, and subgroup closure supplies integer multiples. The new zero left prefix is supplied by 1∈H. The theorem requires no further left dyadic condition. |

All hypotheses apply to the actual canonical Hahn image of H, so Theorem 5.1 proves H initial in No. All its exponents are ≥0 and its zero coefficient is an integer, so the imported Oz description gives H⊆Oz. Initiality in No implies initiality with the induced simplicity order in Oz. The zero group is separately initial and maps to itself. This closes the entire stated claim.

### Proper-class bookkeeping

The least positive element, α, n, and each individual sign sequence/support are sets. The surgery and scaling formulas define class functions with set parameters. Elementary class comprehension defines H, and class replacement sends each individual support to a set. Group operations involve two source elements at a time. There is no class-length series, no set enumeration of a proper class, and no new class recursion. The bridge thus works unchanged for proper-class Γ and G under the stated foundational setting. Its use of Theorem 5.1 is within that theorem's explicit class convention.

## Adversarial failed alternatives and attempted counterexamples

These are deductions using the same published characterization, not counterexamples to the candidate.

1. **Arbitrary initial order relocation can fail.** Let Γ={−1,0,1} with coefficient groups (Z,D,Z), respectively, and take their finite direct sum of monomials. The source meets Theorem 5.1 and is discrete. The increasing relocation −1↦0, 0↦1/2, 1↦1 has initial target exponent set {0,1/2,1}, but 1 is a new right prefix of 1/2. The target coefficient group at 1 is Z, so the target fails the required D condition. The candidate's stronger right-predecessor implication excludes this obstruction.
2. **Uniform division by the least positive element can fail.** Use Γ={−1,0,1} with groups (1/4 Z,D,Z). Uniform multiplication by 4ω sends them to coefficient groups (Z,D,4Z) at exponents (0,1,2). The last group is not initial in R: it contains 4 but not the simpler 1. The candidate scales only the bottom coordinate, leaving all other initial coefficient groups intact.
3. **Completing the Hahn image changes the problem.** Let Γ={0}∪{2^(−n):n≥0}; let R_0=Z and the other coefficient groups equal D. The finite-support direct sum is a countable discrete initial subgroup by Theorem 5.1. Adjoining every permissible series also admits ∑_{n<ω}ω^{2^(−n)} and continuum many binary coefficient variants. That full group cannot be a copy of the original countable group. The candidate never makes this completion step.
4. **Limit-node and ordinal-index attacks.** I checked separately α=0, finite α, nonzero limit α, successor α above a limit, empty t, and limit-length t. The surgery uses the actual concatenated segment a, not an integer-offset deletion. The proper-prefix identity covers the transition node (+)·a exactly when its corresponding source node a·(+) is present. No counterexample resulted.
5. **Tail/cancellation attacks.** A nonzero tail of a least positive element directly contradicts minimality regardless of its sign or support order type. In T, distinct source exponents stay distinct, so no cancellation creates a falsely pure target monomial or a larger coefficient group. Cancellations in addition are shared coordinatewise by T.

No repair is needed. The strongest verified conclusion is the entire target, conditional only on the cited established inputs. No central difficulty has been transferred to an unsupported claim. The imported characterization is substantial, but the new exponent-surgery bridge is explicitly proved rather than assumed.

## Evidence and limitations

All third-party PDF bodies and their extracts are confined to this family's ignored `.private/` directory. Retrieval byte counts, SHA-256 identifiers, URLs, exact inspected pages, evidence-file hashes, authored-artifact hashes, and scope are recorded in `RECEIPT.json`; `RECEIPT.sha256` pins that receipt. No old/root/sibling audit was read, no substantive priority search was performed, no git or PR mutation was made, and no external individual was contacted. Findings were sent only to the assigning parent research agent.

The theorem dependency was checked directly against the specified author manuscript, including the proof of Theorem 5.1; this is not a fresh independent derivation of all foundational surreal results in its bibliography. The finite diagnostic does not certify transfinite supports or replace the general proof. Completion toward this assigned mathematical audit: **100%**; no mathematical gap remains within its stated scope.
