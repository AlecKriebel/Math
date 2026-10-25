from pathlib import Path
import json
from datetime import datetime, timezone

B = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
spectral = {
  'title': 'Pure point Dirichlet spectrum on quasi-conical domains',
  'slug': 'pure-point-dirichlet-spectrum-quasi-conical-domains',
  'description': 'A connected quasi-conical domain with a complete Dirichlet eigenbasis and dense positive eigenvalues, addressing the Krejčířík–Lotoreichik spectral question.',
  'abstract': 'For every dimension at least two, we construct a connected open quasi-conical domain whose Dirichlet Laplacian has a complete orthonormal eigenbasis, although its spectrum and essential spectrum are the entire nonnegative half-line. Its positive eigenvalues are dense, zero is not an eigenvalue, and both continuous spectral subspaces vanish. We use the expanding-cube and shrinking-window geometry of Krejčířík and Lotoreichik, choosing both cube sizes and positive apertures inductively. The additional construction transports a growing family of complete finite spectral clusters with summable norm errors. A repeated dense test family proves completeness and excludes singular continuous spectrum. This answers the existential spectral-type question in their discussion and the corresponding Oberwolfach contribution.',
  'plain_language': [
    'Think of an infinite chain of increasingly large rooms, connected through increasingly small openings. Waves vanish on the walls. The rooms become large enough to contain balls of any radius, yet the whole connected space has a complete collection of square-integrable standing-wave modes.',
    'The surprising point is that these individual modes suffice to represent every square-integrable state, even though the spectrum fills the whole nonnegative half-line. The eigenvalues are dense: there are eigenvalues arbitrarily close to every positive energy. This does not mean that every energy is itself an eigenvalue.',
    'Krejčířík and Lotoreichik introduced this domain geometry and proved that it can retain an embedded eigenvalue while excluding the absolutely continuous part. Their remaining spectral-type question concerns the singular continuous part. This paper addresses that question by constructing a complete eigenbasis, choosing the room sizes as well as the openings.',
    'The additional ingredient is to preserve an expanding collection of whole finite-dimensional spectral clusters and repeatedly test it against a dense family of states. Keeping just one mode, or even many modes without proving completeness, would leave the central question unanswered.'
  ],
  'result': [
    'For every integer d ≥ 2 there is a connected open quasi-conical set Ω ⊂ Rᵈ whose Dirichlet Laplacian A has a complete orthonormal eigenbasis. The operator is defined by the closed energy form with domain H₀¹(Ω).',
    'The spectrum and essential spectrum are [0, ∞), which is also the closure of the point spectrum. All eigenvalues are positive, zero is not an eigenvalue, and both the absolutely continuous and singular continuous spectral subspaces vanish.',
    'The domain consists of expanding cubes joined through positive shrinking windows in their common faces. Both cube widths and window widths are chosen inductively. The result gives an existential construction within this geometric family.',
    'Pure point here describes spectral type and the existence of a complete eigenbasis. It does not mean an isolated sequence of eigenvalues or compact resolvent.'
  ],
  'limitations': [
    'The construction chooses future cube sizes to avoid finitely many protected eigenvalues. It does not prove the same conclusion for every prescribed sequence of cube sizes.',
    'The published proof uses windows in zero-thickness interface screens and does not establish a smooth-boundary or positive-length-passage version of the complete-eigenbasis result. Extensions of earlier embedded-eigenvalue results do not automatically give those stronger variants.',
    'The aperture choices are existential, without explicit numerical bounds that guarantee the infinite construction. The statement concerns the Dirichlet Laplacian, not arbitrary boundary conditions.',
    'The positive eigenvalues form a dense set whose closure is the half-line. The point spectrum itself is not asserted to equal the whole half-line.',
    'The geometry, shrinking-window perturbation theory and spectral-projection approach have substantial predecessors. The added claim is exhaustive cluster transport and completeness; the bounded literature comparison does not certify historical first priority.',
    'Finite diagnostic calculations in the archive cannot certify Mosco convergence, the infinite limiting operator or completeness. Those conclusions rely on the analytical argument.'
  ],
  'background': [
    {'title': 'Krejčířík and Lotoreichik, Quasi-conical domains with embedded eigenvalues', 'url': 'https://arxiv.org/abs/2205.08172v2', 'note': 'Introduces the expanding-cube and shrinking-window construction. Section 5 asks whether its singular continuous part can also be eliminated; Remarks 3.1 and 3.3 clarify spectral clusters and geometric variants.'},
    {'title': 'Lotoreichik, Quasi-conical domains with embedded eigenvalues, Oberwolfach Report 36/2023', 'url': 'https://ems.press/content/serial-article-files/47475', 'note': 'Printed pages 2077–2078 state the corresponding question of obtaining dense point spectrum with both continuous spectral parts absent.'},
    {'title': 'Krejčířík, Spectral geometry: old questions and new answers', 'url': 'https://arxiv.org/abs/2609.28602v1', 'note': 'Open Problem 1 on PDF page 16 repeats the spectral-type question. The present construction retains freedom to choose cube sizes as well as openings.'},
    {'title': 'Hempel, Seco and Simon, The Essential Spectrum of Neumann Laplacians on Some Bounded Singular Domains', 'url': 'https://math.caltech.edu/SimonPapers/217.pdf', 'note': 'An earlier rooms-and-passages construction in a different boundary-condition setting. Proposition 1.4 explicitly handles spectral projections and multiplicities; tracking whole clusters is not a new general principle.'}
  ],
  'why_it_works': [
    'At a finite stage, closing one window separates two bounded pieces. Shrinking-window convergence gives norm control of resolvents and of whole isolated finite spectral clusters, including their multiplicities.',
    'The next cube size avoids the finite set of protected spectral values. Its opening is then small enough that every previously protected projection changes by a summable amount.',
    'New finite spectral families capture successively larger portions of a countable dense collection of cube-supported states. Repeating this requirement prevents states from escaping the protected subspaces.',
    'At the infinite limit, each protected finite-dimensional subspace remains invariant under the resolvent and is spanned by eigenvectors. The dense test family proves that these subspaces together fill the Hilbert space, which removes both continuous spectral parts.',
    'The arbitrarily large cubes supply Weyl sequences throughout the nonnegative half-line. The zero-energy equation would require an L² constant on the connected infinite-volume domain, so zero is not an eigenvalue.'
  ],
  'collaboration': 'I welcome substantive collaboration on independent verification of the infinite spectral-projection argument, its relationship to domain-perturbation literature, and preparation for journal review. Expertise in spectral theory, quadratic forms or partial differential equations would be particularly useful.',
  'follow_up': None,
  'followup_rationale': 'No public follow-up is proposed. Prescribed cube widths, smoother boundaries and quantitative openings are plausible extensions, but this review establishes neither a sufficiently specific new mechanism nor a sufficiently compelling new conjecture to meet the high bar.',
  'publication_date': '2026-10-15', 'version': '1.0', 'doi': '10.5281/zenodo.23410944', 'author': 'Alec Kriebel',
  'pdf_filename': 'paper.pdf', 'supplement_filename': 'source-and-verification.zip', 'additional_assets': [],
  'status': 'Unrefereed preprint, version 1.0, developed with extensive AI assistance. No completed human peer review or formal verification is claimed.',
  'ai_disclosure': 'AI tools were used extensively in developing, reproducing, checking and adversarially reviewing the argument and preparing the note. Internal AI-assisted review is not external human peer review or proof-assistant certification.'
}
anti = {
  'title': 'Three anti-invariant classes on a nonintegrable four-manifold',
  'slug': 'three-anti-invariant-classes-nonintegrable-four-manifold',
  'description': 'A compact four-manifold with nonintegrable almost complex structures and three anti-invariant de Rham classes, addressing the Draghici–Li–Zhang conjecture.',
  'abstract': 'We construct smooth nonintegrable almost complex structures on the product of a genus-two curve and an elliptic curve with at least three independent real anti-invariant de Rham classes. The structures converge smoothly to the product complex structure and equal it outside one coordinate ball. The construction gives a negative answer to the unrestricted integrability conjecture of Draghici–Li–Zhang. The separate generic-vanishing statement is a prior theorem of Tan–Wang–Zhang–Zhu.',
  'plain_language': [
    'An almost complex structure tells a real even-dimensional space how multiplication by the imaginary unit should act on tangent directions. Integrability is the extra condition that makes this local rule come from actual complex coordinates.',
    'An influential conjecture proposed that, on a compact four-dimensional manifold, three independent anti-invariant cohomology classes would force integrability. These classes are global geometric data represented by closed differential forms with a particular symmetry under the almost complex structure.',
    'The paper constructs a small deformation of a product of two complex curves that preserves three such global classes but becomes nonintegrable. The deformation is confined to one coordinate ball and can be made arbitrarily small in the smooth topology.',
    'The key distinction is between global classes and pointwise forms. The three classes are independent globally, while their local representatives fit into a two-dimensional plane through a relation with varying coefficients. This leaves room to preserve all three classes while breaking integrability.'
  ],
  'result': [
    'Let Σ be the smooth compact completion of y² = z⁶ − 1, let E = C/(Z + iZ), and let J₀ be the product complex structure on M = Σ × E. Theorem 1 constructs ε₀ > 0 and a smooth family Jε for |ε| < ε₀.',
    'Every Jε agrees with J₀ outside one fixed coordinate ball and Jε → J₀ in C∞. Three fixed, linearly independent classes in H²_dR(M; R) have closed Jε-anti-invariant representatives.',
    'Every nonzero sufficiently small ε gives a nonintegrable structure. Consequently h⁻_Jε ≥ 3; the paper gives this lower bound, not an exact dimension.',
    'This is a counterexample to the unrestricted compact-four-manifold integrability conjecture of Draghici–Li–Zhang. The separate theorem that h⁻_J = 0 is open and dense among almost complex structures is prior work of Tan–Wang–Zhang–Zhu and is compatible with this exceptional family.'
  ],
  'limitations': [
    'The construction is on the specified genus-two-curve times elliptic-curve product. It does not assert that every compact four-manifold admits such a deformation.',
    'Three independent de Rham classes do not mean three pointwise independent anti-invariant forms. The local anti-invariant plane has real dimension two, and the third representative is a variable-coefficient combination of the other two.',
    'The theorem proves h⁻_J ≥ 3, without computing the exact value. It concerns smooth almost complex structures and does not impose compatibility with a fixed symplectic form.',
    'The deformation is not metric related to the original complex structure: there is no common positive compatible metric. Thus it lies outside the hypotheses of the earlier Draghici–Li–Zhang metric-related obstruction.',
    'Although the starting real pair is closed, variable normalization produces a complex two-form that is not closed. The established closed normalized-pair integrability criterion therefore does not apply.',
    'Earlier work includes compact nonintegrable examples with h⁻ = 2, higher-dimensional and noncompact examples, and nonintegrable structures on products of curves with many pluricanonical sections. Those sections are not automatically closed real anti-invariant de Rham classes. The bounded comparison does not certify exhaustive novelty or exclude further deductions from older examples.'
  ],
  'background': [
    {'title': 'Draghici, Li and Zhang, Symplectic forms and cohomology decomposition of almost complex four-manifolds', 'url': 'https://arxiv.org/abs/0812.3680v1', 'note': 'Question 3.27 asks for a compact nonintegrable four-dimensional example with h⁻_J ≥ 3.'},
    {'title': 'Draghici, Li and Zhang, On the J-anti-invariant cohomology of almost complex 4-manifolds', 'url': 'https://arxiv.org/abs/1104.2511v1', 'note': 'Conjecture 2.5 is the unrestricted integrability claim. Theorem 1.1 concerns the narrower class sharing a compatible metric with an integrable structure.'},
    {'title': 'Tan, Wang, Zhang and Zhu, On cohomology of almost complex 4-manifolds', 'url': 'https://arxiv.org/abs/1112.0768v3', 'note': 'Theorem 1.1 proves that h⁻_J = 0 is open and dense in the C∞ topology. This generic result is prior work, not contradicted by the exceptional family.'},
    {'title': 'Hind and Tomassini, On the anti-invariant cohomology of almost complex manifolds', 'url': 'https://arxiv.org/abs/1908.03016v3', 'note': 'Proposition 4.2 gives compact four-dimensional examples with h⁻ = 2. Their higher-dimensional and noncompact constructions have different scope.'},
    {'title': 'Donaldson, Two-forms on four-manifolds and elliptic equations', 'url': 'https://arxiv.org/abs/math/0607083v1', 'note': 'The positive oriented two-plane description is established background for the local realization of an almost complex structure.'},
    {'title': 'Bande and Kotschick, The geometry of recursion operators', 'url': 'https://arxiv.org/abs/math/0703348v2', 'note': 'Theorem 6 gives the closed-pair integrability criterion. The present normalized pair fails its closedness requirement.'},
    {'title': 'Chen and Zhang, Kodaira dimensions of almost complex manifolds I', 'url': 'https://wrap.warwick.ac.uk/id/eprint/164863/1/WRAP-Kodaira-dimensions-almost-complex-manifolds-I-Zhang-2022.pdf', 'note': 'Section 6.3 supplies earlier nonintegrable structures on T² × S with many pluricanonical sections. That is a different invariant from closed real anti-invariant cohomology.'},
    {'title': 'Chen and Zhang, Kodaira dimensions of almost complex manifolds II', 'url': 'https://wrap.warwick.ac.uk/id/eprint/163848/1/WRAP-Kodaira-dimensions-almost-complex-manifolds-II-Zhang-2022.pdf', 'note': 'Section 5.1 explicitly distinguishes the two invariants and asks for the anti-invariant cohomology of those earlier examples.'}
  ],
  'why_it_works': [
    'Two holomorphic one-forms on the genus-two curve, paired with the elliptic-curve differential, supply three closed real forms. Positivity of the square of a real holomorphic two-form and Stokes’ theorem establish independence of their de Rham classes.',
    'In one coordinate ball the forms satisfy γ = uα − vβ. A compactly supported perturbation changes β and γ by exact terms while preserving the corresponding identity γε = uα − vβε, so all three global classes stay fixed.',
    'For a sufficiently small parameter, α and βε span a positive two-plane. Normalizing this plane gives a decomposable complex two-form whose contraction kernel defines the new almost complex structure. The construction agrees smoothly with J₀ near the ball’s boundary.',
    'The local relation puts the third representative in the same anti-invariant plane. On the region where the cutoff is one, an explicit coframe has a nonzero integrability obstruction for every nonzero parameter, proving that the new structure is nonintegrable.'
  ],
  'collaboration': 'I welcome substantive collaboration on independent verification of the global class construction and local integrability obstruction, comparison with earlier almost complex examples, and preparation for journal review. Expertise in four-manifold geometry, differential forms or almost complex cohomology would be particularly useful.',
  'follow_up': None,
  'followup_rationale': 'No public follow-up is proposed. Computing the exact dimension, revisiting older product examples or changing the manifold would require further analysis before any direction could be presented as a sufficiently compelling and distinct research question. No conjecture is added merely to populate a section.',
  'publication_date': '2026-10-16', 'version': '1.0', 'doi': '10.5281/zenodo.23422055', 'author': 'Alec Kriebel',
  'pdf_filename': 'anti-invariant-four-manifold-v1.0.pdf', 'supplement_filename': 'anti-invariant-four-manifold-verification-v1.0.zip', 'additional_assets': [],
  'status': 'Unrefereed preprint, version 1.0, developed with extensive AI assistance. No completed human peer review or formal verification is claimed.',
  'ai_disclosure': 'AI tools were used extensively in the construction, drafting, literature checking and internal adversarial review. The note is unrefereed, and no independent human peer review or formal verification is claimed.'
}

for id, c, pages, date, support, identity in [
    ('23410944', spectral, 6, '15 October 2026',
     'Complete published paper and manuscript source, plus complete historical_candidate/author/PROOF.md. Historical author status assertions were encountered but not adopted as validation. No dedicated archived or sibling mathematical audit opinions read.',
     'No PDFs occur in the source-and-verification ZIP or any of its three nested archives. The separate six-page PDF is the reader manuscript.'),
    ('23422055', anti, 5, 'October 16, 2026',
     'Complete published paper and manuscript source, plus complete original/unsolved_math_prioritization/attempts/30004549/author/R3_counterexample_candidate.md. Historical author status assertions were encountered but not adopted as validation. No dedicated archived or sibling mathematical audit opinions read.',
     'The sole archive PDF, paper/note.pdf, is byte-identical to the separately published five-page reader manuscript. The nested author packet contains no additional PDF.'),
]:
    p = B/id
    record = json.loads((p/'sources/record.json').read_text())
    receipt = json.loads((p/'sources/receipt.json').read_text())
    byname = {f['name']:f for f in receipt['files']}
    c['source_binding'] = dict(record_id=id, concept_record_id=str(record['conceptrecid']), record_url='https://zenodo.org/records/'+id,
       doi=c['doi'], zenodo_version=record['metadata']['version'], manuscript_version='1.0', manuscript_date=date,
       publication_date=record['metadata']['publication_date'], archive_version_label='1.0',
       version_source='Zenodo metadata and printed manuscript date/version agree.',
       source_retrieved_utc=receipt['retrieved_utc'], pdf_sha256=byname[c['pdf_filename']]['sha256'],
       supplement_sha256=byname[c['supplement_filename']]['sha256'], files=receipt['files'],
       reviewed_documents=[dict(filename=c['pdf_filename'], pages=pages, read_scope='all pages')],
       support_read_scope=support,
       abstract_source='Complete published page 1 abstract, visually checked and cross-checked against the manuscript TeX. Only whitespace and mathematical typography normalized; AI/editorial prose kept separate.',
       archive_pdf_identity=identity,
       review_boundary='Independent scope and bounded primary-literature review; not a separate mathematical gate, exhaustive novelty certificate or human peer review.')
    (p/'reviews/scope/content.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    with (p/'reviews/scope/RESEARCH_LOG.md').open('a') as f:
        f.write('\n## '+datetime.now(timezone.utc).isoformat()+' — 85%\n\nFull-abstract source-bound candidate content prepared; primary comparison and plain-language boundaries included. Public files, ZIP CRCs, complete manifest and nested ZIP CRCs verified. No additional reader supplement PDFs. Public follow-up omitted under the high bar. Final report and content consistency checks remain.\n')
    print(id, 'content written')
