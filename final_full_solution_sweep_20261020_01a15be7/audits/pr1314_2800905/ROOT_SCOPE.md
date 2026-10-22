# Root provisional original-scope receipt: PR1314 /2800905

The exact original problem is the unspiked positive-PCA relaxation for symmetric Gaussian W with all independent upper-triangular entries of variance1/n: compare p(W)=max{x^T W x:x>=0,||x||_2=1} with s(W)=max{Tr(WX):X positive semidefinite, entrywise nonnegative,Tr(X)=1}. The complete claimed negative resolution is s(W)->2 in probability and expectation while p(W)<=sqrt(2)+o(1) with high probability, excluding every rank-one SDP optimizer with high probability.

Root previously read the full pinned PR description, ACCEPTANCE.md, PROOF.md and VERDICT.json, and the complete cached original. The proof uses Sudakov-Fernique comparison plus concentration for the true optimum, a small-rank Haar spectral projector corrected by the all-ones matrix for SDP feasibility, global semicircle limits with the order of parameters explicit, and an expectation lower bound using Tr(G)/n. The original equal-diagonal-variance model is handled by a vanishing diagonal operator-norm perturbation from invariant GOE. Published reversed variance conventions are diagnosed but are not an author-confirmed erratum.

The full true-optimum limit sqrt(2) is attributed to Montanari-Richard and is not required or independently reproved here. No planted positive-PCA threshold question is substituted for this original unspiked problem. Claimed scope is complete provisionally; correctness, exact standard-result hypotheses and fresh publication identity need independent review. The explicit prior lead is Bandeira-Kunisky-Wein, PMLR145 theorem4 and arXiv2012.02243v1 theorem3. No novelty, readiness, publication or spreadsheet-write authority follows from this receipt.

Progress: overall80%; this candidate is provisional, not scientifically final.
