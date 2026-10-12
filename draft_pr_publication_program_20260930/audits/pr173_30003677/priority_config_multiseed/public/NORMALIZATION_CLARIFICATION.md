# Additive jump-mark normalization clarification

UTC: 2026-10-12T15:06:56.306604+00:00. Audit completion estimate: 100% of the bounded priority audit; this adds a representation repair. All previously sealed files and hashes are preserved.

This clarification accompanies `COROLLARY_DERIVATION.md`. Its displayed bare-lambda functions are the actual Markov transition intensities, denoted q_j here. To embed these exactly into Ganguly–Ramanan's original v1 Poisson SDE, choose jump set J={1,2} and the probability measure sigma(1)=sigma(2)=1/2. For susceptible v,

q_j(v,x)=lambda_j sum_(u~v) m_uv 1{x_u=j},

r_j(v,t,x)=2 1{x_v(t-)=0} lambda_j sum_(u~v) m_uv 1{x_u(t-)=j}, j=1,2.

Here r_j is the SDE acceptance threshold, while q_j is the physical generator intensity (and includes the susceptible indicator when evaluated on arbitrary states). The accepted j-mark points have intensity sigma(j) r_j=q_j because the driving intensity is ds dr sigma(dj). The accepted jump adds j to state 0. Rates vanish for states 1 and 2, so the state space {0,1,2} is preserved and recoloring is impossible. Left-limit evaluations give predictability. This specifies exactly the candidate's rates lambda_j per infectious edge channel.

With multiplicity capped at two and closure cardinality k, the SDE thresholds obey the uniform bound C_k=4 max(lambda1,lambda2)(k-1)+1. The same discrete-mark regularity, weak continuity, finite-dissociability, capped-multigraph equivalence, marked limit, limiting ray bound and diagonal apply. Neither the physical process nor any conclusion changes. Bare q_j used as SDE thresholds with this probability measure would instead represent half the intended rates; `normalization_checks.py` explicitly verifies this semantic negative.

The normalization was prompted by a parent representation question after the substantive first seal. I independently checked the already retained primary v1 section 3.1 (p.8), equation (3.3) and Definition 3.3 (p.9). The parent's derivation and other family verdicts were not consumed. This is additive source checking, not independent confirmation from a parent conclusion.

The operative delivery package is now `SAFE_PUBLIC_ALLOWLIST_V2.json`, `FINAL_MANIFEST_V2.json` with its detached checksum, and `FINAL_INVENTORY_V2.json`. The original manifest, receipts, inventory, allowlist and verifier are preserved historical checkpoint artifacts; the original verifier correctly passed before this additive package existed. The V2 verifier checks the complete present recursive inventory and every 0444 mode. The exact-corollary priority obstruction and bounded uncertainty stated in `REPORT.md` remain the final substantive assessment.
