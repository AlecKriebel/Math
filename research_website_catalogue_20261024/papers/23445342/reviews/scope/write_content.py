from pathlib import Path
from datetime import datetime, timezone
import json

root = Path(__file__).resolve().parents[4]
data = {
  '23445342': {
    'title': 'Coarse endpoint concentration at every diverging scale for one-dimensional space-time random walks',
    'slug': 'coarse-endpoint-concentration-random-walks',
    'description': 'One-dimensional random walks in iid space-time environments have sharply concentrated coarse endpoint laws at every deterministic diverging interval scale.',
    'abstract': "For a nearest-neighbor walk on Z in a fixed i.i.d. space-time environment with transition probabilities strictly between zero and one, we prove that its quenched and averaged endpoint laws agree, after coarse graining into deterministic intervals of any diverging length, outside an environment event of probability smaller than every inverse power of time. No uniform ellipticity or quantitative rate of divergence of the interval length is required. This is the affirmative one-dimensional assertion contrary to Conjecture 1 in Berger’s contribution to Oberwolfach Report 38/2009. The proof combines replica overlap estimates, environmental martingales, same-parity coalescence and concentration over a short final segment. Priority qualification: novelty and historical priority remain unresolved. A bounded literature audit established no exact full anticipation, but four relevant older original full texts could not be accessed. We make no claim of firstness, independent discovery or that the conjecture remained open until this work. Established late-layer and coalescing methods, including those of Dunlap–Gu and Barraquand–Rychnovsky, are explicitly credited.",
    'plain_language': [
      'Imagine a walker on the integers whose chance of stepping right is randomly chosen separately for every place and time. Once those chances are fixed, the walker still has its own randomness. The resulting endpoint distribution can be compared with the distribution obtained by averaging over all environments.',
      'The paper groups possible endpoints into intervals and compares the probability assigned to every interval. If the interval length tends to infinity, however slowly, the total discrepancy becomes small. For any fixed positive tolerance, the chance of an environment violating that tolerance eventually falls below every prescribed inverse power of time.',
      'The surprising feature is that no minimum growth rate for the intervals is required. The result also permits bias and transition probabilities arbitrarily close to zero or one, provided the environment law is fixed and neither endpoint occurs with positive probability.',
      'This establishes the affirmative one-dimensional statement opposed by a conjecture in Berger’s 2009 workshop contribution. The note is explicit that its historical novelty remains unresolved; earlier local-limit and fluctuation work must receive credit, and several older full texts remain unexamined.'
    ],
    'result': [
      'Let the right-step probabilities pₛ,ₓ be iid over space and time, with 0 < pₛ,ₓ < 1 almost surely. A nearest-neighbor walk on Z starts at zero. Write μ_N^ω for its endpoint law in the fixed environment and α_N = Eμ_N^ω for its averaged endpoint law.',
      'For every deterministic real sequence M_N > 0 tending to infinity, partition Z using the half-open intervals [b_N + jM_N, b_N + (j + 1)M_N), intersected with Z. For every ε, K > 0, the environmental probability that Σ_I |μ_N^ω(I) − α_N(I)| exceeds ε is at most C_{ε,K} N^(−K) for all sufficiently large N, uniformly in each deterministic alignment b_N.',
      'The discrepancy is full ℓ¹ distance, twice the usual total variation distance. Constants may depend on the fixed environment law; the eventual threshold may also depend on the chosen scale sequence. The scale may diverge nonmonotonically and arbitrarily slowly.',
      'The conclusion includes biased averaged walks, nearest-neighbor parity, and real interval lengths. It assumes neither uniform ellipticity nor inverse-moment bounds for the transition probabilities. All analytic estimates required by the proof are supplied in the note.'
    ],
    'limitations': [
      'The theorem concerns a fixed iid space-time environment law and nearest-neighbor jumps in one spatial dimension. It does not cover static or correlated environments, and its constants need not remain controlled as elliptic laws approach deterministic-arrow environments.',
      'The tolerance ε and inverse-power exponent K are fixed before taking large time. The theorem does not give a uniform convergence rate for every diverging scale sequence or a bound for a shrinking tolerance.',
      'The interval partition is deterministic. Uniformity in its deterministic alignment is not a simultaneous assertion for partitions selected after observing the environment.',
      'This is a statement about coarse endpoint probabilities, not a pointwise Gaussian local limit theorem or a claim that microscopic environmental fluctuations disappear. A qualitative central or local limit theorem alone does not supply the stated tail bound.',
      'Novelty and historical priority remain unresolved. The note could not inspect the complete original texts of Boldrighini–Minlos–Pellegrinotti (1999 and 2004), Boldrighini–Pellegrinotti (2001), or Bérard (2004); stronger estimates in those papers have not been excluded as antecedents. Firstness, independent discovery, a new method and present-day open status are not claimed.'
    ],
    'background': [
      {'title': 'Berger, Quenched Local Limit Theorem for Space-time Random Walk in Random Environment (2009)', 'url': 'https://ems.press/content/serial-article-files/46239', 'note': 'Printed pages 2151–2152 give the higher-dimensional coarse concentration theorem and Conjecture 1, which predicts failure in one transverse dimension.'},
      {'title': 'Dunlap and Gu, A quenched local limit theorem for stochastic flows', 'url': 'https://arxiv.org/abs/2105.07907', 'note': 'A prior continuum local-limit theorem with a stationary random corrector. Its short final-layer method is explicitly credited; its model and conclusion differ from the discrete coarse ℓ¹ concentration statement here.'},
      {'title': 'Barraquand and Rychnovsky, Random walk on nonnegative integers in beta distributed random environment', 'url': 'https://arxiv.org/abs/2201.07270v3', 'note': 'Proposition 1.13 concerns a full-space beta-environment local limit. Its discussion and proof use prior final-layer and ordered-coalescence ideas; these mechanisms are not claimed as new here.'},
      {'title': 'Boldrighini, Minlos and Pellegrinotti, Random walks in quenched iid space-time random environment are always a.s. diffusive (2004)', 'url': 'https://doi.org/10.1007/s00440-003-0331-x', 'note': 'An important earlier quenched central-limit result. Its complete original proof was not available for comparison, so it has not been ruled out as containing stronger relevant estimates.'},
      {'title': 'Boldrighini and Pellegrinotti, T⁻¹/⁴-noise for random walks in dynamic environment on Z (2001)', 'url': 'https://doi.org/10.17323/1609-4514-2001-1-3-365-380', 'note': 'Earlier work on environment-dependent fluctuation corrections. It is one of the full-text gaps that prevent a certified novelty claim.'},
      {'title': 'Bérard, The almost sure central limit theorem for one-dimensional nearest-neighbour random walks in a space-time random environment (2004)', 'url': 'https://doi.org/10.1239/jap/1077134669', 'note': 'Earlier nearest-neighbor quenched central-limit theory. The available abstract is not a substitute for checking all estimates in the original proof.'}
    ],
    'collaboration': 'I welcome substantive collaboration on an independent probability-theoretic review of the all-scale concentration argument, or on resolving the remaining primary-literature comparisons before a journal submission. Expertise in space-time random environments, quenched local limits, and concentration inequalities would be particularly useful.',
    'follow_up': None,
    'followup_rationale': 'No new follow-up meets the requested high bar. Correlated environments, shrinking tolerances and optimal rates would each need a precise supported mechanism rather than a generic extension question. The immediate literature task is checking antecedents, not advertising a new conjecture.',
    'publication_date': '2026-10-18', 'version': '1.0', 'doi': '10.5281/zenodo.23445342',
    'author': 'Alec Kriebel', 'pdf_filename': 'coarse_endpoint_concentration.pdf',
    'supplement_filename': 'coarse_endpoint_verification.zip', 'additional_assets': [],
    'why_it_works': [
      'Two walkers sharing the environment give a one-dimensional difference chain. Its return and occupation bounds control how much the endpoint law can depend on each newly exposed time layer.',
      'Environmental martingales first give sharp concentration at an auxiliary polynomial interval scale. A same-parity coalescing coupling then erases differences within those auxiliary cells over a shorter final time segment.',
      'The remaining environment is divided into independent moving strips. Before that segment, no relevant strip carries much starting mass; changing one strip therefore has small influence. Bounded differences concentrate the final coarse discrepancy around its conditional mean.',
      'The target interval length enters only through an expectation estimate that tends to zero whenever it diverges. It need not grow at the auxiliary polynomial rate. A controlled path-killing error allows the independent-strip argument to return to the unrestricted walk.'
    ],
    'status': 'Unrefereed research note, version 1.0, developed with extensive AI assistance. Novelty and historical priority remain unresolved.',
    'ai_disclosure': 'AI tools were used extensively in solving, drafting, and checking this work. The note has not undergone conventional human peer review. The author is responsible for the claims; finite checks supplement the analytic proof and do not certify novelty.'
  },
  '23387753': {
    'title': 'Finite-energy lattice percolation with internal critical probability one',
    'slug': 'finite-energy-percolation-critical-probability-one',
    'description': 'An invariant finite-energy percolation on every lattice Z^d, d ≥ 2, has a unique infinite cluster destroyed by every independent thinning below full retention.',
    'abstract': 'For every integer d ≥ 2 we construct a bond percolation on Zᵈ that is invariant under all lattice automorphisms, mixing under translations, and has ordinary finite energy. Almost surely it has a unique infinite component, yet every independent Bernoulli thinning with retention p < 1 destroys all infinite components. The construction perturbs a one-ended spanning tree, using the maximum finite-past size along each non-tree edge’s tree path to suppress every bypass of large tree cuts. This answers the historical ordinary-energy question of Benjamini, Häggström and Schramm. We also make explicit a planar threshold-one consequence of Häggström–Mester’s earlier construction. No first-priority claim is made.',
    'plain_language': [
      'Percolation studies which connections survive in a random network. This paper constructs a random network on the integer lattice that has one infinite connected component, yet is so fragile that independently deleting each edge with any fixed positive probability destroys every infinite component.',
      'The network has no preferred location or lattice direction. It also has ordinary finite energy: even after all other edges are revealed, any particular edge still has a positive conditional chance of being either present or absent. Those probabilities need not share a common bound away from zero and one.',
      'The construction leaves a sequence of bottlenecks on every route to infinity. Beyond a sufficiently large scale, each such boundary has exactly one surviving crossing edge. Independent thinning eventually breaks these indispensable connections, however close its retention probability is to one.',
      'The result works in every dimension at least two. It develops Häggström and Mester’s earlier one-ended-tree perturbation mechanism and makes a further threshold consequence of their planar example explicit. The note does not claim a verified first resolution of the historical question.'
    ],
    'result': [
      'For every integer d ≥ 2, there is a bond-percolation law on the nearest-neighbor edges of Zᵈ that is invariant under every graph automorphism and mixing under translations. For each edge e, its conditional probability of being open, given all other output edges, lies strictly between zero and one almost surely.',
      'Almost surely the realized graph X has a unique infinite component C, and p_c(X) = p_c(C) = 1 for independent internal bond thinning. The internal site thresholds of both graphs also equal one. These statements are quenched: X is fixed before the independent thinning is introduced.',
      'More generally, the perturbation applies to any countably infinite connected simple bounded-degree graph with a one-ended spanning tree T. If deleting a tree edge t leaves a finite side of size s_T(t), retain it with probability 1 − 2^(−s_T(t)). Insert a non-tree edge e with probability 2^(−M_T(e)), where M_T(e) is the maximum finite-side size along its connecting tree path. Conditional on T, these choices are independent.',
      'The all-dimensional lattice input comes from Timár’s established factor-of-iid one-ended spanning-tree theorem. The note also derives a planar threshold-one conclusion from the exact fixed-phase midpoint projection of Häggström–Mester’s older model, preserving its original flip rates.'
    ],
    'limitations': [
      'The energy condition is ordinary finite energy. The paper neither proves a uniform positive lower bound on the marginal conditional probabilities nor proves that every such uniform bound fails. Small probabilities conditional on the hidden tree do not alone decide the marginal question.',
      'Finite components are allowed. Existence of a unique infinite component does not say that every lattice vertex belongs to it. The external random process is a bond law; the additional site assertion concerns independent thinning inside its realized graph.',
      'The perturbation theorem requires a connected one-ended spanning tree and bounded ambient degree. A disconnected uniform spanning forest in higher dimensions cannot be substituted, since some non-tree edges would have no connecting tree path.',
      'The planar midpoint law is a coordinate marginal of a fixed-phase site construction, with all coarse vertices present. It is not the induced bond graph of the final open sites, and the old site/bond threshold comparison alone does not provide an external finite-energy bond law.',
      'The planar perturbation mechanism is due to Häggström and Mester. The note supplies an additional bounded-cutset deduction and a dimension-independent bypass rule with eventual singleton cuts. Neither first priority for the historical answer nor certified novelty of that rule is claimed. No finite coding radius or quantitative mixing rate is asserted.'
    ],
    'background': [
      {'title': 'Benjamini, Häggström and Schramm, On the effect of adding ε-Bernoulli percolation to everywhere percolating subgraphs of Zᵈ', 'url': 'https://arxiv.org/abs/math/9906002v1', 'note': 'Poses the historical ordinary-finite-energy bond question. Its separate sprinkling setting adds fixed-density noise to an everywhere-percolating graph.'},
      {'title': 'Benjamini and Tassion, Homogenization via sprinkling', 'url': 'https://arxiv.org/abs/1505.06069v1', 'note': 'Question 1 restates the exact existence problem and defines finite energy as insertion and deletion tolerance. The sprinkling theorem has different hypotheses from this tree-dependent perturbation.'},
      {'title': 'Häggström and Mester, Some two-dimensional finite energy percolation processes (2009)', 'url': 'https://doi.org/10.1214/ECP.v14-1446', 'note': 'Section 2 supplies the prior summable finite-past site-flip mechanism. The post-flip threshold-one deduction supplied in this note is not a theorem stated in the inspected antecedent; the original mechanism deserves explicit credit.'},
      {'title': 'Timár, One-ended spanning trees in amenable unimodular graphs', 'url': 'https://arxiv.org/abs/1805.10690v1', 'note': 'Theorem 1 provides the equivariant factor-of-iid connected one-ended spanning tree used on every Zᵈ with d ≥ 2.'},
      {'title': 'Pemantle, Choosing a spanning tree for the integer lattice uniformly', 'url': 'https://arxiv.org/abs/math/0404043v1', 'note': 'Provides the classical uniform spanning-tree alternative in dimensions two through four and the planar primal/dual input behind the earlier construction.'}
    ],
    'collaboration': 'I welcome substantive collaboration on an independent percolation-theoretic review of the bypass suppression and quenched threshold arguments, the exact relationship to the earlier planar construction, or preparation for journal submission. Expertise in invariant percolation and one-ended spanning trees would be especially useful.',
    'follow_up': None,
    'followup_rationale': 'No follow-up meets the requested high bar. Stronger uniform-energy assumptions, coding-radius estimates and quantitative mixing questions would require separate mechanisms and careful checks against existing results. They are not added merely as plausible extensions.',
    'publication_date': '2026-10-15', 'version': '1.0.0', 'doi': '10.5281/zenodo.23387753',
    'author': 'Alec Kriebel', 'pdf_filename': 'finite-energy-percolation-note.pdf',
    'supplement_filename': 'finite-energy-percolation-verification.zip', 'additional_assets': [],
    'why_it_works': [
      'In a one-ended tree, each edge on a ray separates off a finite set, and those sets grow to exhaust the graph. Any extra edge crossing one of these boundaries has a tree path that includes its separating tree edge.',
      'The insertion rule uses the largest finite-side size along that path. The probabilities of deleting the essential tree edge or adding any bypass have a summable total along the ray. Borel–Cantelli therefore leaves eventual singleton boundaries and retained infinite ray tails.',
      'The retained tails coalesce, yielding one infinite component. Once the graph is fixed, any infinite path must use infinitely many distinct bottleneck edges. Independent retention with p < 1 has probability at most pᵏ of preserving the first k of them, which tends to zero. The same argument uses their vertices for site thinning.',
      'Every conditional edge probability is strictly between zero and one even after the hidden tree is averaged out. Equivariance of the tree input and perturbation preserves all lattice symmetries, while their representation as a measurable factor of iid marks gives translation mixing.'
    ],
    'status': 'Unrefereed research note, version 1.0.0, developed with extensive AI assistance. No first-priority claim; independent specialist review welcome.',
    'ai_disclosure': 'OpenAI tools were used extensively in solving, proof development, drafting, coding, and adversarial verification. The author is responsible for the claims. No completed external human peer review or formal proof-assistant verification is claimed; package checks authenticate files rather than the infinite mathematical proof.'
  }
}

for rid, content in data.items():
    p = root / 'papers' / rid
    if (p / 'reviews/scope/PUBLICATION_HOLD.json').exists():
        raise RuntimeError('Publication hold exists; do not regenerate promotional content.')
    receipt = json.loads((p / 'sources/receipt.json').read_text())
    record = json.loads((p / 'sources/record.json').read_text())
    byname = {f['name']: f for f in receipt['files']}
    content['source_binding'] = {
      'record_id': rid, 'concept_record_id': str(record['conceptrecid']),
      'record_url': 'https://zenodo.org/records/' + rid, 'doi': content['doi'],
      'version': content['version'], 'zenodo_publication_date': content['publication_date'],
      'manuscript_date': content['publication_date'],
      'printed_edition': ('18 October 2026; no version number printed on title page. Zenodo metadata and package README specify version 1.0.' if rid == '23445342' else 'October 15, 2026 — Version 1.0.0'),
      'source_retrieved_utc': receipt['retrieved_utc'],
      'pdf_sha256': byname[content['pdf_filename']]['sha256'],
      'supplement_sha256': byname[content['supplement_filename']]['sha256'],
      'files': receipt['files'],
      'reviewed_documents': [{'filename':content['pdf_filename'], 'pages':11 if rid == '23445342' else 5, 'read_scope':'all pages'}],
      'support_read_scope': ('Full original verification/submission/PROOF.md; the self-contained published paper incorporates its earlier analytic inputs. Package README and manifest structure reviewed after own scope conclusion.' if rid == '23445342' else 'Full original source/author/PROOF.md; package README and manifest structure after independent scope conclusion.'),
      'abstract_source': 'Complete published PDF page 1 abstract, cross-checked against ' + ('main.tex' if rid == '23445342' else 'note.tex') + '. Whitespace and mathematical typography normalized. Original priority qualification retained; no AI prose appended.',
      'archive_pdf_identity': ('The verification ZIP contains no PDF. The separately published main PDF is the only record PDF; no supplementary PDF exists.' if rid == '23445342' else 'The only PDF inside the ZIP is note.pdf, byte-identical to the published main PDF. No separate supplementary PDF exists.'),
      'review_boundary':'Independent scope and literature review only; separate analytic and adversarial mathematical gates required. No exhaustive priority certification.'
    }
    (p / 'reviews/scope/content.json').write_text(json.dumps(content, ensure_ascii=False, indent=2) + '\n')
    with (p / 'reviews/scope/RESEARCH_LOG.md').open('a') as f:
      f.write('\n' + datetime.now(timezone.utc).isoformat() + ' — 85% complete. Exact abstract and edition preserved in source-bound public content, with limitations and prior credit, separate AI status, and no speculative follow-up. Final integrity receipt and review summary remain.\n')
print('Wrote scope content for', ', '.join(data))
