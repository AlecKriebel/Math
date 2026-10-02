# Credited PVHH additive-cube resolution

Status: already_solved, 0/5 new author turns. The exact original fixed-point conjecture is Theorem18 of Cassaigne, Currie, Schaeffer and Shallit (2011 preprint; JACM2014). Independent AI-assisted source and reconstruction review passes; this is not a new discovery or human peer-review certification.

The morphism is0→03,1→43,3→1,4→01. Its fixed point beginning0 avoids three consecutive nonempty blocks with the same length and integer sum.

Read PRIOR_PROOF_AUDIT.md before using the computational evidence. The preprint's printed2.1758 rounds downward; the reconstruction rigorously uses2.176. Its printed503-vector count is not reproduced: directed interval arithmetic certifies497 vectors. The larger exact graph without the extra u+v filter has135572 reachable states and no acceptance, matching the printed reachability count; applying that safe filter gives78340. This does not establish what unavailable original code did. All distinctions are retained, and the original theorem and mechanism are fully credited.

The frozen source packet and separate review remain unchanged. The additive portable review wrapper uses SymPy; without raw source files it reports135593 assertions, or135598 with --source-dir pointing to the privately retained primary sources. Directed interval certification uses mpmath1.3.0. Raw PDFs, screenshots, imports and large state streams are excluded. The duplicate catalog30001564 receives no second result or PR.
