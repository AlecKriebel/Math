# Third homology and pre-Bloch groups: scoped partial investigation

Problem **30003264 / OWR-15173-001**, rank **733**. **Unsolved, 5/5 approaches used.** Independent audit: **PASS strictly for the statement repair and bounded partial investigation**. No full solution, primary disproof, novelty or priority claim is made.

## What is established

The imported formula uses the kernel of localization from S-integer homology to field homology. The [primary report](https://ems.press/content/serial-article-files/46655?nt=1), printed p. 2959, instead uses the kernel of the composite to indecomposable K3. This is a substantive statement repair. The zero specialization on the imported kernel, including the explicit P(F5)[1/2] = Z/3 obstruction, does not disprove the primary question.

The five bounded approaches are:

1. The wrong-kernel obstruction and an exact five-term residue calculation.
2. The credited known Q, S={infinity,2} case with the actual maps; it does not prove eventuality.
3. The rational reduction ker(pi_S) = ker(j_S), with infinity and 2,3,5,7 in S, coefficients Z[1/2], and s_p = -2 Delta_p on N_Q. The primary's eventual surjectivity is an imported input. The DVR sequence is not asserted to be left-injective.
4. Elementwise and finitely generated-submodule eventual killing, with an abstract countermodel showing that a field-colimit isomorphism does not imply finite-stage injectivity.
5. The complete finite-squareclass-character criterion and an abstract mixed-character obstruction to checking only target-supported components.

Neither abstract countermodel is an arithmetic counterexample. The remaining finite-stage arithmetic kernel is unresolved. Imported theorems are credited; their full foundations have not been independently re-proved.

- [Proofs and exact remaining gaps](author/PROOF.md)
- [Independent audit](audit/AUDIT.md)
- [Mandatory interpretation boundaries](audit/MANDATORY_CORRECTIONS.md)
- [Current disposition](release_status.json)

Both frozen directories and both ZIP archives are unchanged. Statements inside those freezes about pending review or no remote writes describe their historical preparation stage. The separate audit and this wrapper provide the current disposition without rewriting either freeze. This remains unrefereed AI-assisted work.

## Reproduce

From any working directory, run Python 3.10 or newer on `verify_release.py`, then repeat with `-O`. Only the standard library is needed; there are no network requests. The verifier checks the exact publication inventory, frozen manifests and archive membership, current disposition, byte-identical normal/optimized author and independent replays, and integrity. The embedded independent replay exercises author damage controls, archive corruption, package corruption and arithmetic mutations. These checks concern integrity and finite controls, not a formal proof of general S-arithmetic homology.

The public manifest hashes every publication file except itself. Its external SHA-256 is recorded in the draft PR. A self-modifiable manifest or verifier alone is not an authenticity anchor.

Only authored proof/code/audit and public verification metadata are included. Source PDFs, extracted source text, raw corpora, selected source records and private coordination files are excluded. The existing queue is preserved except for this row's Status and Turns; Findings, Chat, DOI and the stale embedded header are unchanged. No dataset edit, merge, release or outreach is part of this publication.
