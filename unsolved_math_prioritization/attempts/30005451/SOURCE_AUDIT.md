# Source, model and prior-work audit

Checked 2026-09-30. The runtime is gpt-6-astra at xhigh, not ultra.

## Exact source and required record repair

The unsolvedmath page was requested first and was unavailable. The complete pinned record is preserved in `source_record.json`; no imported report existed for its exact problem number. The official EMS report was retrieved in full. Maria Deijfen and Remco van der Hofstad's complete contribution “Recent developments in preferential attachment models,” printed pp. 646–651, was read, including the initial graph, edge normalization, local-in-probability definition and all three open-problem paragraphs. Printed p. 650 was visually checked.

The dataset's clean statement is not a faithful target: it asks for equality between a **fixed-outdegree** model and the Bernoulli model. The primary source instead proposes replacing that fixed outdegree by an **i.i.d. Poisson outdegree**, and replacing total-degree attachment by indegree-only attachment. Its question (b) asks for the relation between these local limits. The primary source's paragraph (c) separately discusses nonlinear functions and fixed outdegree. Neither the source nor the candidate asserts that a total-degree theorem with random outdegrees already applies after this modification.

The report's standard fixed-outdegree graph starts with one self-loop, and it describes both self-loop and no-self-loop conventions in its discussion. The candidate does not silently use that graph as the Bernoulli seed. The Bernoulli graph starts with a single isolated vertex, exactly as prescribed on p. 650. The candidate explicitly defines two no-new-self-loop Poisson adaptations: frozen weights and sequentially updated weights. These correspond to the independent and sequential conventions in the cited local-limit paper. A written finite-seed argument covers either Poisson graph's alternative fixed initial graph, including a finite multigraph.

Distances are undirected, and the root is uniform among all vertices; local convergence is empirical convergence in probability of rooted finite-radius neighborhoods, as on p. 648. The coupling additionally preserves orientations, multiplicities and identical age marks. It does not claim a limit in a stronger topology requiring global or component-size agreement.

The abbreviated report omits the condition f(0)<=1 needed for its initial Bernoulli probability to be valid. The full Dereich–Mörters source supplies this condition. For the affine rule f(k)=ak+b, the candidate therefore uses 0<=a<1 and 0<b<=1. It does not extend the one-vertex Bernoulli construction to b>1 by silently clipping probabilities. It also does not assert an affine a=1 endpoint excluded by the source's strict increment bound.

## Primary literature actually read

### Dereich–Mörters: the Bernoulli model and its limit

The full arXiv:1007.0899v2 PDF, dated 5 February 2013, was retrieved. Its front matter identifies the Annals of Probability paper, 41(1), 329–384, DOI 10.1214/11-AOP697. The downloaded file uses its own reprint pagination, which the candidate states explicitly.

Read the complete model definition on reprint pp. 3–4, the idealized branching-random-walk/neighborhood-tree construction in Section 1.3, and the explicit weak-local-limit identification on p. 9 (also visually checked). Sections 5–6 were inspected for the neighborhood-exploration couplings and their stopping events. These couplings retain the explored graph structure; their displayed Propositions 5.1 and 6.1 summarize a truncated-component-size consequence, so the candidate does not misquote those displayed formulas as a formal local-convergence theorem. The explicit local-limit statement and its construction are credited dependencies, not a claim that this campaign re-proved the entire 56-page paper.

The source says that incoming columns are independent because an edge's attachment probability depends only on its receiving vertex's current indegree. The candidate uses this exact property in a separate concentration proof, rather than assuming that annealed local convergence automatically implies the report's empirical convergence in probability.

The earlier arXiv:0807.4904 degree-evolution paper was also retrieved in full; its model and Theorem 1.1 were read. It gives limiting indegree frequencies and asymptotically Poisson outgoing counts. It is corroboration, not a replacement for the actual giant-component/local-neighborhood paper cited as [15] in the report. The candidate derives its matching affine mean and moment bounds directly.

### Garavaglia–Hazra–van der Hofstad–Ray: current version and limitation

The full arXiv:2212.05551v4 PDF, revised 2 March 2026, was retrieved. The arXiv version history and current “Updated proofs” metadata were independently checked. Read the model definitions, root/mark conventions, Theorem 1.5 and the literature/open-problem discussion. Printed p. 13 was visually checked.

The current paper treats total-degree attachment. It identifies local limits for models (A), (B), (D), and (E), and still lists the Dereich–Mörters conditionally independent-edge model as an extension. It now leaves model (F), sampling without replacement, open. Older indexed material can state a broader list; the candidate uses the current v4 scope. No claim about a journal publication or the correctness of an older broader statement is made. The candidate's proof does not rely on any of these total-degree convergence theorems.

## Prior-attempt and duplicate gates

The current queue row was rank 132, queued, 0/5. The exact numeric all-state GitHub PR search returned no match. An all-state preferential-attachment keyword PR search returned no match. The dedicated remote branch was absent before work began; selected-path history was empty. Campaign state, assessment history and related-target groups had no entry for this ID. Corpus comparison identified no duplicate local-limit statement. No previous Alec or campaign work was overwritten. The imported August 2026 literature triage is retained as background, with its stronger fixed-outdegree formulation explicitly corrected.

The repository instructions and policy were read. The user-authorized isolated branch and parent-maintained queue workflow applies; no generator or shared queue was edited. There has been one substantive approach: affine Poisson row coupling plus local stability. The earlier checkpoint is preserved and superseded by the complete candidate.

## What is and is not resolved by the candidate

The written theorem establishes the complete local-limit comparison for the two explicitly defined **affine**, indegree-based, Poisson-outdegree adaptations. It includes zero outdegrees, sequential reinforcement, fixed seed changes, and empirical convergence in probability. It gives the common affine Gamma–Poisson neighborhood tree by reformulating the known Dereich–Mörters tree, and it diagnoses the fixed-outdegree extraction error through a positive isolated-root probability.

It does not claim the analogous comparison for every nonlinear concave f. The key normalization identity S_n=a T_n+b n is specifically affine. Nor does it cover an arbitrary interpretation of the unspecified adaptation or a simple-graph convention forbidding parallel edges. If the original open-ended paragraph (b) is read as asking for a result for all nonlinear functions, that larger request remains unresolved. This scope distinction should survive review, queue classification and publication.

Bounded current-literature searches did not locate this exact affine comparison in another source. This is not a priority certificate. The result remains an unrefereed candidate pending separate adversarial AI review; all old limit and branching-process results are credited.
