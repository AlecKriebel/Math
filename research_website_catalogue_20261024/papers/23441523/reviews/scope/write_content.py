from pathlib import Path
from datetime import datetime, timezone
import json

root = Path(__file__).resolve().parents[4]
data = {
    '23441523': {
        'title': 'A polynomial versus superpolynomial gap in vertex-distribution-free graph testing',
        'slug': 'vertex-distribution-free-graph-testing-gap',
        'description': 'A fixed graph property has polynomial testing cost under uniform vertex sampling but superpolynomial cost with arbitrary vertex weights.',
        'abstract': 'We give a negative answer to the comparison question of Gishboliner and Shapira in Oberwolfach Report 19/2019, Problem 5, and their later Problem 5.6. The fixed property consisting of K₄-free graphs that become 3-colorable after deleting at most one vertex has a polynomial classical canonical tester, for every input size. In the vertex-distribution-free model, every adaptive two-sided tester has superpolynomial total sample-plus-adjacency cost as the proximity parameter tends to zero. The lower bound follows by an elementary tripartite-cover and heavy-apex reduction from the established two-sided triangle-testing lower bound. All distances allow arbitrary edge additions and deletions. The reduction remains valid when the tester is given the vertex set, its size, the full positive rational distribution, and the heavy vertex. A self-contained classical sampling argument and exact finite verification materials accompany the note.',
        'plain_language': [
            'Graph property testing asks whether a large network has a specified feature, or is far from having it, while inspecting only a small part of the network. Usually every vertex receives equal weight. The vertex-distribution-free model allows vertices to have very different weights, which affect both sampling and the cost of changing edges.',
            'This paper constructs one fixed feature that is relatively cheap to test with uniform samples but much more expensive with arbitrary vertex weights. The feature has two conditions: no four vertices form a complete clique, and deleting at most one vertex makes the graph colorable with three colors.',
            'The key example gives a single vertex half of the sampling weight. Its connections force the rest of the graph to obey a difficult triangle-free condition. That one vertex has little influence under uniform sampling in a large graph, yet it is expensive to disconnect under the weighted distance.',
            'The separation persists even if the tester is told every vertex name and the entire distribution. The obstruction is therefore not just ignorance of the sampling weights. The result measures how many samples and adjacency questions are required; it makes no claim of a polynomial running-time algorithm.'
        ],
        'result': [
            'Fix the property P of finite simple undirected K₄-free graphs that become 3-colorable after deleting at most one vertex. It is hereditary, closed under edge deletion, and extendable by adding an isolated vertex.',
            'For every nonempty input size, a one-sided classical canonical tester uses O(ε⁻⁶ log(1/ε)) independent uniform samples and O(ε⁻¹² log²(1/ε)) adjacency queries. It does not need to know the number of vertices.',
            'Along a sequence of positive rational ε tending to zero, every randomized adaptive two-sided vertex-distribution-free tester has worst-case total sample-plus-adjacency cost exp(Ω(log²(1/ε))). This remains true with the full vertex set, its size, the complete positive rational weight vector, and the distinguished heavy vertex supplied.',
            'The distance is the sum of D(u)D(v) over unordered changed vertex pairs, minimized over graphs with the property on the same vertex set; additions and deletions are both allowed. For uniform D this is the number of changed edges divided by n². Testers accept members and reject ε-far inputs with probability at least 2/3.',
            'Consequently no fixed polynomial in classical canonical complexity and 1/ε can bound the VDF complexity for every extendable hereditary property, even after a fixed positive constant rescaling of the classical proximity parameter. This addresses the comparison question in Gishboliner–Shapira Problem 5.6 and the earlier Oberwolfach problem.'
        ],
        'limitations': [
            'This is a separation for one fixed property. It does not classify which other properties have a gap, or settle every question about forbidding one fixed subgraph.',
            'The lower bound counts samples and adjacency queries together. It is not a sample-only bound when unlimited arbitrary-name adjacency queries are free. Its displayed quantitative bound is stated along a sequence of proximity parameters.',
            'The classical tester can use exhaustive membership checking on the sampled graph. Polynomial oracle complexity does not imply polynomial running time.',
            'The proof imports the established two-sided triangle-testing lower bound of Alon and Shapira. The contribution is the property and the reduction that place known triangle hardness against a polynomial classical tester, not a new triangle lower bound.',
            'The literature comparison is bounded. No claim of exhaustive priority certification, independent human peer review, or formal proof verification is made. The finite programs supplement the written proof and its cited theorem.'
        ],
        'background': [
            {'title': 'Gishboliner and Shapira, Testing Graphs against an Unknown Distribution', 'url': 'https://arxiv.org/abs/1905.09903v5', 'note': 'Defines the VDF framework and states the uniform-versus-VDF comparison as Problem 5.6. Its positive result for blowup-avoidable properties does not cover every extendable hereditary property.'},
            {'title': 'Gishboliner, joint work with Shapira, Oberwolfach Report 19/2019', 'url': 'https://ems.press/content/serial-article-files/46798', 'note': 'The original comparison appears as Problem 5 on printed page 1139. The model counts vertex samples and edge queries.'},
            {'title': 'Alon and Shapira (2004), Testing subgraphs in directed graphs', 'url': 'https://doi.org/10.1016/j.jcss.2004.04.008', 'note': 'Theorem 4(ii) and its two-sided lower-bound argument supply the classical triangle-testing hardness used by the reduction.'},
            {'title': 'Alon and Krivelevich (2002), Testing k-colorability', 'url': 'https://doi.org/10.1137/S0895480199358655', 'note': 'Part of the established polynomial colorability-testing theory. The note includes a conservative sampling proof that explicitly handles every input size.'},
            {'title': 'Fei (2026), Testing Properties of Edge Distributions', 'url': 'https://arxiv.org/abs/2603.22702v2', 'note': 'Studies distributions on edges with a different default sampling oracle and arbitrary edge weights. Those results should not be conflated with vertex-product distance and counted adjacency access here.'}
        ],
        'collaboration': 'I welcome substantive collaboration on an independent review of the testing models, the all-size classical bound, and the adaptive lower-bound reduction, or on preparing the result for journal submission. Expertise in graph property testing and removal lemmas would be particularly useful.',
        'follow_up': None,
        'followup_rationale': 'No new follow-up meets the requested high bar. Classifying other separating properties, improving quantitative bounds, or restricting distributions are broad existing directions. This review establishes neither a new precise conjecture with evidence nor an exceptional reason to advertise one on this page.',
        'publication_date': '2026-10-17', 'version': '1.0.0',
        'doi': '10.5281/zenodo.23441523', 'author': 'Alec Kriebel',
        'pdf_filename': 'vdf-testing-gap.pdf',
        'supplement_filename': 'vdf-testing-gap-source-and-verification.zip',
        'additional_assets': [],
        'why_it_works': [
            'The classical tester looks for two disjoint subgraphs that each fail 3-colorability. Deleting one vertex cannot remove both obstructions. A color-list sampling argument finds these witnesses in large inputs; sufficiently many samples collect every vertex of a small input.',
            'For the lower bound, a tripartite cover makes any graph 3-colorable while preserving triangle-freeness and retaining a constant fraction of its distance from that property. Adding a universal vertex with weight 1/2 converts the tail’s triangle-free distance exactly into one quarter of the new graph’s distance from P.',
            'The composition loses only a factor of 36 in proximity. Sampling the constructed graph needs no access to the original edges, and each adjacency query costs at most one original adjacency query. The established adaptive two-sided triangle lower bound therefore transfers to the weighted testing problem.'
        ],
        'status': 'Unrefereed research note, version 1.0.0, developed with extensive AI assistance. Independent specialist review welcome.',
        'ai_disclosure': 'AI tools were used extensively in development, verification, literature review, and writing. The author is responsible for the claims. AI-assisted reviews and finite verification programs are not independent human peer review or formal proof certification.'
    },
    '23356680': {
        'title': 'A smooth Reshetnyak-harmonic sphere with unbounded distortion',
        'slug': 'reshetnyak-harmonic-sphere-unbounded-distortion',
        'description': 'A smooth sphere homeomorphism locally minimizes Reshetnyak energy while its infinitesimal distortion has no finite bound.',
        'abstract': 'We construct a compact smooth Riemannian sphere and a smooth homeomorphism from the round sphere which locally minimizes Reshetnyak energy against every same-trace Sobolev competitor, but has essentially unbounded infinitesimal distortion. This gives a negative answer for the Reshetnyak member of the general-energy harmonic-sphere question posed in the inspected 2025 texts of Meier–Vikman–Wenger. Scalar calibration on a flat belt and an exact two-form calibration on conformal caps prove the full local comparison. The map does not minimize energy in its homotopy class and is not Korevaar–Schoen harmonic. Separately, an angular-stress argument gives the nonsharp bound 4 + √17 for locally Korevaar–Schoen-minimizing spheres into complete metric spaces; the sharper classical SL(2)-minimal bound also applies. Classical ingredients are credited; first priority is not claimed.',
        'plain_language': [
            'An energy-minimizing map can be thought of as a way of placing one surface onto another that cannot be improved by changing a small patch while keeping its boundary fixed. Whether that condition prevents severe stretching depends on which energy is being minimized.',
            'The paper constructs a smooth map from the round sphere onto a smooth Riemannian sphere. It is a homeomorphism: it is one-to-one, onto, and has a continuous inverse. It locally minimizes Reshetnyak energy, which measures the square of the greatest infinitesimal stretch, yet its stretching can be arbitrarily unequal in different directions.',
            'Near the equator, one direction is compressed by a factor proportional to the square of the distance from the equator while the other is left unchanged. The ratio of the two stretches exceeds every finite bound on a region of positive area. This is a distortion phenomenon, even though the map and both surfaces are smooth.',
            'The choice of energy matters. The example does not minimize the usual Dirichlet, or Korevaar–Schoen, energy and does not minimize energy globally within its homotopy class. A separate argument in the paper establishes bounded infinitesimal distortion for locally Korevaar–Schoen-minimizing spheres into complete metric spaces.'
        ],
        'result': [
            'There is a compact smooth Riemannian surface X diffeomorphic to S² and a smooth homeomorphism u from the round S² to X that locally minimizes Reshetnyak energy E₊² but has essentially unbounded infinitesimal distortion.',
            'Local minimization has the full fixed-trace meaning: each source point has a neighborhood U such that, for every Lipschitz domain Ω compactly contained in U, u has no larger energy than any W¹,²(Ω, X) competitor with the same boundary trace. Competitors need not be continuous, remain in the chosen image patch, or share a prescribed homotopy class.',
            'The target is geodesic, satisfies a local quadratic isoperimetric inequality, and every sufficiently small-diameter continuous sphere in it is null-homotopic. Thus the counterexample satisfies the target assumptions of the general-energy harmonic-sphere question in the inspected Meier–Vikman–Wenger arXiv v1 and Oberwolfach texts.',
            'On a punctured equatorial band the ratio of largest to smallest infinitesimal stretch is 1/t² in cylindrical coordinates. Every proposed finite distortion bound fails on a set of positive area. The inverse homeomorphism need not be smooth.',
            'Separately, for a complete metric target in the standard metric-Sobolev framework, a locally Korevaar–Schoen-minimizing W¹,² map from S² has infinitesimal distortion at most 4 + √17. The stress argument also gives SL(2)-minimality, so the sharper established Lytchak–Wenger bound 2√2 + √6 applies. The displayed elementary constant is not claimed as an improvement or an optimum.'
        ],
        'limitations': [
            'The counterexample uses Reshetnyak energy, the integral of the squared operator norm. It is not Korevaar–Schoen harmonic, where the smooth-target energy instead sums the squares of both singular values. Comparable energies can have different minimizers.',
            'The map is a local fixed-trace minimizer, not a global minimizer in its homotopy class. A conformal homeomorphism in the same class has strictly lower total energy, so the example does not contradict the established theory of global homotopy minimizers.',
            'The negative answer is tied to the Reshetnyak member of the general-energy question in the inspected 2025 arXiv version and workshop contribution. The revised journal body was not available for comparison, and neither unchanged final wording nor continued open status is asserted.',
            'The positive Korevaar–Schoen statement gives bounded distortion in general metric targets, not conformality of every tangent seminorm. The smooth Riemannian-target conformality phenomenon and the sharper SL(2)-minimal bound are classical ingredients.',
            'First priority and optimal constants are not claimed. Finite algebra checks and numerical diagnostics support the construction but do not certify the universal Sobolev comparison or the global stress argument.'
        ],
        'background': [
            {'title': 'Meier, Vikman and Wenger, Energy minimizing harmonic 2-spheres in metric spaces', 'url': 'https://arxiv.org/abs/2503.08553v1', 'note': 'Question 1.9 asks about infinitesimal quasiconformality of harmonic spheres. Definition 6.1 supplies the local fixed-trace condition; the allowed energies include Reshetnyak and Korevaar–Schoen energy.'},
            {'title': 'Meier, joint work with Vikman and Wenger, Oberwolfach Report 30/2025', 'url': 'https://ems.press/content/serial-article-files/52249', 'note': 'Question 1 on printed page 1625 asks the corresponding question after fixing an admissible energy. The preceding global homotopy-minimizer result has a stronger hypothesis.'},
            {'title': 'Lytchak and Wenger, Energy and area minimizers in metric spaces', 'url': 'https://arxiv.org/abs/1507.02670v2', 'note': 'Provides the established energy/area and SL(2)-minimal seminorm framework. Section 3.3 records the sharper Korevaar–Schoen quasiconformality constant 2√2 + √6.'},
            {'title': 'Korevaar and Schoen (1993), Sobolev spaces and harmonic maps for metric space targets', 'url': 'https://doi.org/10.4310/CAG.1993.v1.n4.a4', 'note': 'Foundational metric-Sobolev and harmonic-map theory used by the separate Korevaar–Schoen statement. The paper does not identify this energy with Reshetnyak energy.'},
            {'title': 'Sacks and Uhlenbeck (1981), The existence of minimal immersions of 2-spheres', 'url': 'https://doi.org/10.2307/1971131', 'note': 'Classical harmonic-sphere theory provides the smooth-target background for the holomorphic quadratic-differential argument. That classical conformality mechanism is credited, not presented as new.'}
        ],
        'collaboration': 'I welcome substantive collaboration on an independent geometric-analysis review, especially the unrestricted Sobolev competitor comparison and the metric angular-stress argument, or on developing a journal submission. Expertise in metric Sobolev maps, energy minimization, and quasiconformality would be especially useful.',
        'follow_up': None,
        'followup_rationale': 'No follow-up meets the requested high bar. Optimal KS distortion is already an established question in Lytchak–Wenger, and broad questions about other energies would require a new classification mechanism or a precisely supported conjecture. This review supplies neither, so no speculative prompt is added.',
        'publication_date': '2026-10-13', 'version': '1.0',
        'doi': '10.5281/zenodo.23356680', 'author': 'Alec Kriebel',
        'pdf_filename': 'harmonic-sphere-energy-v1.0.pdf',
        'supplement_filename': 'harmonic-sphere-source-verification-v1.0.zip',
        'additional_assets': [],
        'why_it_works': [
            'The target sphere has a flat cylindrical belt and smooth conformal caps. The map compresses one belt coordinate by h(t), with h′(t) = t² near the equator, while preserving the angular coordinate. It becomes conformal away from the compressed region.',
            'On the belt, a globally 1-Lipschitz extension of the angular coordinate turns every competitor into a scalar Sobolev function with the same boundary data. Its Dirichlet energy gives a lower bound attained by the constructed map. This comparison still works when a competitor leaves the local image patch.',
            'On the caps, an exact two-form with comass at most one agrees with the area form near the image. Pullback and trace-gluing identities make its integral depend only on the fixed boundary trace, giving the required lower bound for arbitrary Sobolev competitors.',
            'For the separate KS result, inner variations yield an angular stress tensor. On the sphere it defines a holomorphic quadratic differential and therefore vanishes. The resulting balance of the infinitesimal seminorm bounds distortion; the established SL(2)-minimal theory gives the sharper constant.'
        ],
        'status': 'Unrefereed research note, version 1.0, developed with extensive AI assistance. Independent specialist review welcome.',
        'ai_disclosure': 'AI tools were used extensively in development, verification, adversarial review, and writing. The author is responsible for the claims. AI-assisted reviews are not independent human or journal peer review, and the accompanying checks are not formal proof certification.'
    }
}
for rid, content in data.items():
    folder = root / 'papers' / rid
    if (folder / 'reviews/scope/PUBLICATION_HOLD.json').exists():
        raise RuntimeError('Publication hold exists; do not regenerate promotional content.')
    receipt = json.loads((folder / 'sources/receipt.json').read_text())
    record = json.loads((folder / 'sources/record.json').read_text())
    byname = {f['name']: f for f in receipt['files']}
    pages = 5 if rid == '23441523' else 6
    tex = 'main.tex' if rid == '23441523' else 'note.tex'
    duplicate = 'output/pdf/vdf-testing-gap.pdf' if rid == '23441523' else 'note.pdf'
    content['source_binding'] = {
        'record_id': rid,
        'concept_record_id': str(record.get('conceptrecid')),
        'record_url': 'https://zenodo.org/records/' + rid,
        'doi': content['doi'],
        'version': content['version'],
        'zenodo_publication_date': content['publication_date'],
        'manuscript_date': content['publication_date'],
        'printed_edition': ('17 October 2026 · Version 1.0.0' if rid == '23441523' else '13 October 2026 · Version 1.0 · Unrefereed research note'),
        'source_retrieved_utc': receipt['retrieved_utc'],
        'pdf_sha256': byname[content['pdf_filename']]['sha256'],
        'supplement_sha256': byname[content['supplement_filename']]['sha256'],
        'files': receipt['files'],
        'reviewed_documents': [{'filename': content['pdf_filename'], 'pages': pages, 'read_scope': 'all pages'}],
        'support_read_scope': (['Complete original authored audit/inputs/PROOF.md, including the direct rational hard-family construction.', 'Package README and manifest structure; archived review verdicts not used to form scope conclusion.'] if rid == '23441523' else ['Complete original_packet/author/PROOF.md and KOREVAAR_SCHOEN.md mathematical arguments.', 'Package README and manifest structure; archived review verdicts not used to form scope conclusion.']),
        'abstract_source': 'Full published PDF page 1 abstract, cross-checked against published-source/' + tex + '; whitespace and mathematical typography normalized, no editorial disclosure appended.',
        'archive_pdf_identity': 'Uploaded PDF is byte-identical to ' + duplicate + ' inside the published ZIP. The archive has no other PDF and the record has no separately published supplementary PDF.',
        'review_boundary': 'Independent publication scope and literature review only. Mathematical promotion requires the separately assigned analytic and adversarial gates. No exhaustive novelty certification.'
    }
    (folder / 'reviews/scope/content.json').write_text(json.dumps(content, ensure_ascii=False, indent=2) + '\n')
    with (folder / 'reviews/scope/RESEARCH_LOG.md').open('a') as f:
        f.write('\n' + datetime.now(timezone.utc).isoformat() + ' — 85% complete. Source-bound page draft written with full original abstract, exact edition, separate AI status, precise scope/credit boundaries, no speculative follow-up, and all published downloads. Final integrity and consistency review remain.\n')
print('Wrote independent scope content for', ', '.join(data))
