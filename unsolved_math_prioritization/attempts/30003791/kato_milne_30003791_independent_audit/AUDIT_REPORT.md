# Independent audit: Kato–Milne linkage and vanishing

Problem 30003791 · rank 740 · OWR-16162-003  
Audit date: 5 October 2026

## Verdict

**PASS, strictly for the bounded research record and its elementary controls.**

All six elementary proof sections are valid under the stated definitions and ranges. The five approaches correctly stop at missing implications rather than asserting solutions. No proof or counterexample to either unrestricted odd-characteristic question is established. This is not a certification of global openness, novelty, the entire cited literature, or a successful fresh dataset-row comparison.

**Required mathematical corrections: none.** Three source/precision notes below should accompany reuse of the record. None invalidates its local results or its stated no-resolution disposition. The author freeze is unchanged.

### Frozen object

- Archive: `KATO_MILNE_30003791_SAFE_FREEZE.zip`
- Size: 20,996 bytes
- SHA-256: `6ab69c7efbb362416f44de1fb8c642eaa5ce0877aec1869b67859012f2f428e5`
- Exactly nine files, matching the authored directory byte for byte
- Eight listed file hashes verified; the ninth file is the self-excluded manifest
- No source PDFs, extracted source text, raw dataset records, private coordination material, or symlinks in the safe payload

## 1. Primary target and linkage convention

The freshly retrieved primary PDF, including visual inspection of printed pages 1250–1251, confirms the two different target degrees: pair linkage in degree n asks about degree n+2; triple linkage asks about degree n+1. The record correctly restricts its precise convention to n ≥ 2. The primary contribution supplies the symbol-linkage analogy rather than a full separate formal definition. Its general-p algebra display does retain quadratic exponents, as the author reports. [Primary report](https://ems.press/content/serial-article-files/46742)

The stated interpretation is justified by the explicit common-factor definitions in Chapman–McKinnie §1.4 and Chapman–Dolphin §2.2. A common symbol in H_p^(n−1) is separable linkage: one additive slot and n−2 logarithmic slots can be held fixed. A common element of ν_F(n−1) is the different, inseparable condition. Equality of complete sets of factors is stronger still. The record preserves all three distinctions. [Definitions](https://arxiv.org/pdf/1705.09553v2), [factor and total-linkage definitions](https://arxiv.org/abs/1806.03603)

The universal quantifier is over all pairs or triples of degree-n symbols over one field. It is neither a quantifier over all extensions nor a single factor required to work for the entire group. No conclusion in this audit identifies a selected family with a universally linked field.

## 2. Line-by-line proof audit

### Section 1: appending logarithmic factors — PASS

The operation is additive and well defined on the quotient. Since d(dlog c)=0, appending dlog c sends an exact form dη to d(η∧dlog c). It also sends each representative of an Artin–Schreier relation to the same kind of relation one degree higher. This checks the whole relation subgroup, because forms and the Artin–Schreier map are additive. It does not require an unsupported product of two arbitrary Kato–Milne classes.

The argument applies to every characteristic-p field, including p=2, imperfect fields, fields of infinite p-rank, and the degree-one domain needed when n=2. For degree zero differential forms, the conventional negative-degree differential space is zero.

### Section 2: symbol compression — PASS

The induction is legitimate: the sum of two linked symbols is a symbol with the same common factor and multiplicative slot xy. Both x and y are nonzero, and xy=1 merely gives the zero symbol. Thus the induction remains inside the hypothesis. General differential forms are finite sums of decomposable forms, and a nonzero entry db becomes b dlog b. Entries equal to zero contribute zero. This establishes generation and completes the proof, without any finite-generation assumption on the field.

The result is symbol length at most one in degree n only. No degree-raising vanishing claim is inferred.

### Section 3: finite p-basis vanishing — PASS

The p-basis expansion is finite even when the field itself is infinite. The stated quotient over F^p maps isomorphically to F by the basis hypothesis, and its defining relations have zero derivative. Hence the formal partial derivations exist and test linear independence of the dt_i. Exterior powers above r vanish, giving the precise cohomological cutoff m>r+1. The two displayed sufficient bounds on r are correctly indexed.

The perfect-field case r=0 is consistent. This theorem is conditional on finite p-rank and is not asserted for arbitrary infinite-p-rank fields. No linkage-to-p-rank implication has been proved.

### Section 4: prescribed logarithmic factor transfer — PASS

The additional hypothesis explicitly transfers the particular factor dlog c of the second symbol to the first. The quotient-level append operation then produces a repeated exterior factor, which is zero in all characteristics; characteristic two does not invalidate alternation in the exterior algebra.

Every degree-(n+1) generating symbol has the required decomposition with a degree-(n−1) symbol and two appended slots. The case n=2 uses H_p^1 and works identically. Nothing in the proof silently replaces arbitrary separable triple linkage by the stronger factor-transfer property.

### Section 5.1: Laurent p-basis — PASS

At each Laurent-series stage, sorting exponents modulo p produces finitely many residue classes. Each resulting series still has its outer exponents bounded below; dividing those exponents by p gives another Laurent series. Applying the coefficient-field p-basis decomposition produces p^r spanning monomials, and uniqueness follows recursively from coefficient comparison. No uniform lower bound on every inner exponent is required in an iterated Laurent field.

### Section 5.2: exact-form and Artin–Schreier detector — PASS

The fully iterated coefficient extraction is additive, with values in the prime field. Frobenius multiplies every exponent by p and raises coefficients to pth powers, so its fully constant coefficient is unchanged. In top degree there is one logarithmic basis form Λ_r; the Artin–Schreier image of fΛ_r is represented by (f^p−f)Λ_r modulo exact forms. The detector kills these representatives.

The delicate point is algebraic, rather than continuous, differentials. The author's finite p-basis expansion resolves it correctly. Algebraic differentiation of Σ_e h_e^p t^e gives Σ_e h_e^p d(t^e). Therefore the Euler derivation multiplies each exponent by its residue modulo p. A zero exponent contributes zero and no exponent is shifted. This proves annihilation of every exact top form without exchanging an arbitrary derivation with an infinite sum.

Consequently the detector descends to H_p^(r+1) and takes value 1 on [1;t_1,…,t_r]. This is a valid all-prime, all-finite-r proof for the specified Laurent fields over F_p. It is not claimed for an arbitrary coefficient field with the same scalar-valued detector.

### Section 5.3: selected-family controls — PASS

The common factor contains n−2 logarithmic slots; adjoining one slot gives degree n. Adjoining two or three total new slots gives degrees n+1 or n+2, respectively. These match the two constructions. The n=2 empty-string convention is explicit. Appending complementary slots to any allegedly zero selected member would kill the nonzero top class, proving that all displayed members and their common factor are nonzero.

These examples refute only local selected-family implications. In particular, the displayed pair with a nonzero degree-(n+1) append does not refute Q4, whose conclusion is degree n+2; the displayed triple is not a universally triple-linked field. The record says so plainly.

### Section 6: presentation sign — PASS

The generator substitution is valid in every characteristic: j is invertible because j^p=b≠0; setting I=−i and J=j^−1 gives the new additive parameter −a and multiplicative parameter b^−1, with the same conjugation convention. Recovering the old generators proves an algebra isomorphism, not merely equality of Brauer classes.

Applying the substitution to both algebras introduces three minus signs in the appended differential class. Over the stated two-variable Laurent field, the detector distinguishes 1 from −1 exactly when p is odd. This disproves presentation invariance of the element, while leaving zero versus nonzero unchanged under this substitution. The record does not claim that this particular calculation proves or disproves invariance of vanishing under every possible presentation change.

## 3. Literature hypotheses and stops

Each listed source statement was checked against the identified version. Fresh byte-level evidence and exact inspection scopes are in `verification/fresh_source_retrieval.json`.

1. The 2017 Albert-form route assumes isotropy of every relevant form. Its reverse linkage-to-isotropy assertion is restricted to p=2, and the pure-part condition for degree-three vanishing has its own quantifiers. The record does not extend either converse to odd primes. [2017 source](https://backoffice.biblio.ugent.be/download/8619328/8619329)
2. The characteristic-two triple theorem covers n≥3 in Theorem 3.3 and n=2 in Theorem 4.4. Its hypotheses are met by universal separable linkage. The higher-degree pair result is also explicitly attributed in the common-slots paper's introduction. [Triple linkage](https://arxiv.org/pdf/1706.04929v2), [common slots](https://doi.org/10.1017/S0004972718000229)
3. The 2019 Corollary 3.3 requires total separable one-linkage, in addition to the displayed shared factor. Proposition 3.2 needs a specified Artin–Schreier factor. Their use as stronger sufficient conditions, rather than solutions of universal triple linkage, is accurate. The elementary logarithmic-factor argument agrees with Remark 3.7. [2019 source](https://arxiv.org/abs/1806.03603)
4. The degree-three algebra results are specifically in characteristic 3, for division algebras with a common additive slot. Vanishing is the premise; the extension has degree at most two, and quadratic closedness removes that extension. [Degree-three source](https://arxiv.org/pdf/1901.00358v3)
5. The 2023 Theorem 4.7 has an infinite-field hypothesis, equal degree p^m, and a prescribed common simple purely inseparable splitting field. The parametrized version chooses F_p-independent r_i. Corollary 4.8 permits a much larger cyclic splitting degree. Neither supplies the missing target implication. [2023 source](https://arxiv.org/pdf/2012.07496v3)
6. The 2024 Theorem 3.3 goes from an already vanishing degree-three class to inseparable linkage after prime-to-p extension. Corollary 3.5 adds p-specialness and H_p^3=0. Reversing this reasoning would be invalid. The source's sign observation is correctly reproduced. See the source typo note below. [2024 source](https://arxiv.org/pdf/2403.11154v1)
7. The finite-family nonlinkage theorem, the quaternion linkage-number meeting questions, and exponent-lowering symbol-length bounds do not establish the universal target assumptions with a surviving target class. Their limited roles in the record are correct. [Finite families](https://arxiv.org/pdf/2104.08349v1), [meeting notes](https://math.haifa.ac.il/ufirst/Events/BGM_problems.pdf), [lower exponent](https://arxiv.org/abs/2409.16447)

As an additional adversarial literature check, the 2024 preprint published in 2025 as *Invariant for sets of Pfister forms* concerns quadratic Pfister forms and 2-primary invariants. Its inspected definitions and Sections 3–5 do not resolve the odd-p questions here. [Additional source](https://arxiv.org/html/2404.00121v1)

The author's institutional bibliography corroborates the cited journal years, including the 2026 lower-exponent publication. It is bibliographic evidence, not exhaustive status certification. [Publication list](https://www.cs.mta.ac.il/staff/Adam_Chapman/publications)

## 4. Source and precision notes

### S1. Secondary-source typo, not an error in the frozen proof

The 2024 PDF's Theorem 3.2 displays n homogeneous equations in n−1 variables. That statement is false as written: two equations x=0 and x=0 in one variable have no nonzero common solution over any extension, although their degrees are prime to every p. Visual inspection confirms that this is not an extraction error. The proof of Theorem 3.3 instead uses p−1 equations in p variables, the expected dimensional pattern. The frozen record does not invoke the erroneous displayed count, and explicitly excludes independent validation of imported homogeneous-system results. Retain that limitation. No correction to its elementary proofs is needed. [Source location](https://arxiv.org/pdf/2403.11154v1)

### S2. Make source hypotheses explicit when expanding the summaries

If revising the literature prose, add “in characteristic 3, with the displayed common additive slot” to the degree-three paragraph, and “over an infinite field, for equal-degree p^m algebras” to the 2023 paragraph. The former is already documented in the source metadata; the latter is explicit in the source theorem. These are clarifications to summaries, not repaired proof gaps. The record uses neither theorem to deduce a target conclusion.

### S3. Frozen historical audit status

The author's files correctly record that audit was pending when frozen. Preserve those historical bytes. Attach this separate audit, or create a newly hashed revision if changing that status. An audit PASS must never be promoted to “problem solved,” “globally open,” or “novel theorem.”

## 5. Independent computation and provenance

The author's complete program was read and replayed from a temporary unrelated working directory. Its output matches the frozen JSON byte for byte. Its count of 10,140 monomial Artin–Schreier controls and 38,090 exact-form controls also matches independent combinatorial counting. The sparse crossed-product reduction, negative powers of the central b, and all generator identities are internally consistent.

The independently authored verifier uses a different representation: p×p matrices over F_p[u,v,v^−1], with a diagonal additive generator and a weighted cyclic shift. It checks ten identities for each of p=2,3,5,7,11,13. It separately checks 600 p-basis decompositions, 1,800 derivation comparisons, 600 Artin–Schreier residues, 600 exact residues, 600 d² tests, and 46 pair/triple degree cases. Incorrect nonconstant detectors and the odd-prime incomplete sign change are rejected. These are finite corroboration and negative controls; the preceding proof review carries the infinite-field claims.

All ten public scholarly PDFs were freshly retrieved, and every size and SHA-256 matched the author's metadata. The primary pages were rendered from the freshly retrieved PDF and visually checked. Failed web screenshot and DOI-reader attempts supplied no evidence; successful public PDF retrievals and the verified publisher link supplied the checks instead. No restricted registry route was retried.

The locally supplied catalog's 21,735,099 bytes, SHA-256 and Git blob SHA-1 were recomputed. The ID/rank/source association and retained record-hash metadata match. The raw statement and review bodies were not supplied by that catalog, so their hashes were not freshly recomputed. No current remote corpus or dataset-row match is asserted. Only match booleans and public verification metadata appear in this audit.

Read-only GitHub checks at main commit `83f42b8d239702e55c976b033c6dd919232c6526` found 62 attempt-directory entries and no target match. Exact-ID PR, commit, branch and default-branch code searches, plus the Kato Milne PR search, returned no matches. These bounded checks cannot exclude deleted or unindexed work. There were no remote writes or communications to outside individuals.

## 6. Reproduction and stopping condition

Run `python3 -B code/independent_verify.py` from this audit directory, with the author directory and named freeze archive present as siblings. Or pass `--author-root` and `--archive` explicitly. Output must match `verification/independent_controls.json`. No external package or network access is required.

Run `python3 -B code/verify_audit_manifest.py` to verify this audit's file set and hashes. This audit is complete for the requested scope. The two unrestricted odd-prime targets remain unresolved by the audited investigation, with exactly the missing bridges stated in the original report.
