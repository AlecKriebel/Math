# Audit addendum and minor corrections

No mathematical correction is required for the frozen propositions, finite-cell proof, Boolean clauses, characteristic arithmetic or complete-region output.

1. **Box interface.** Theorem 3 advertises an explicit box among the algorithmic outputs. The proof gives that box, but `MonomialQuotient.regularity()` does not include it in its return dictionary. The separate `frontier_box.py` helper adds `minimal_element_box` and preserves every original result field. This is an interface completion, not a changed mathematical bound. The frozen source remains unchanged.

2. **Publication date clarification.** Independent access to the [EMS numeric landing page](https://ems.press/journals/owr/articles/10252925) succeeded during the audit. It records publication on 14 April 2023, for the 2022 volume. Thus the imported 2023 parenthetical is compatible with the publication date; the workshop itself was 27 March–2 April 2022. The author's historical failed access claim is not overwritten.

3. **Review-hash completion.** The author explicitly marked its review hash as not recomputed. The independent audit now recomputes it from the complete selected problem and normalized empty prior report, using the current upstream serialization rule, and confirms the catalogue match. This extends the verification record without changing the author receipt.

The correct overall status remains unresolved for the general finite-presentation module question. The unrestricted-sheaf finite-frontier interpretation fails; the monomial result is separately scoped and makes no priority claim.
