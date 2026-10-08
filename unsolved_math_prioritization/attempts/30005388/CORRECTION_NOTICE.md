# Current verifier correction and historical evidence

The published mathematical claim is limited to five partial route audits. The original authored report trio and INDEPENDENT_AUDIT.md are preserved byte-for-byte. Their mentions of verify.py, ORIGINAL_INPUT_INVENTORY.json, CORRECTION_VALIDATION.json, the original packet, and its 84-run validation describe the earlier audit stage. Those earlier full inputs and runner are intentionally not included here. The current reproduction instructions are in VERIFICATION.md.

The correct tensor involution is j⊗j+(Phi j)⊗(j Phi). The report’s literal inclusion and projection both have support ad,bc,cb,da,xx. Omitting the derivative correction makes the inclusion equivariance defect dd; the naive tensor square-axiom defect takes aa to bc+cb+dd.

The original verifier did not check the tensor matrix’s square axiom and used solver-selected substitute maps. Its historical naive-tensor runs returned PASS in all three Python optimization modes with different supports. This is a validation defect, not a counterexample to the report’s correct tensor certificates. HISTORICAL_FALSE_ACCEPTANCE.json preserves the exact recorded replacement supports and output hashes, clearly labeled as historical evidence.

verify_hardened.py adds grading, horizontal square-axiom and derivative-commutation checks and fixes the literal map supports before checking every matrix equation. independent_verify.py checks the literal maps through a separate vector-action implementation. Fresh mutation tests alter the actual code and reject both the naive tensor law and damaged literal maps.

CORRECTION.patch is a narrow authored contextual patch showing the historical change. Its original target is omitted, so patch application and original false-acceptance replay are NOT_RUN. HISTORICAL_PATCH_VALIDATION.json preserves the earlier exact patch-application observation without claiming current reproduction. The full flawed original verifier is not republished for provenance.

These corrections do not manufacture a knot involution, establish a new knot’s finite concordance order, or prove A=Arf on all smooth torsion. No sixth mathematical route was started.
