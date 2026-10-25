from pathlib import Path
from datetime import datetime, timezone
import json

B = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
upstream = 'https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Global-classical-solutions-of-the-three-dimensional-relativistic-Vlasov-Maxwell-system-September-23-2026'

contents = {
'23203334': {
 'title': 'Signed impulse estimates and global smooth solutions for finite multispecies relativistic Vlasov-Maxwell',
 'slug': 'multispecies-relativistic-vlasov-maxwell-signed-impulse',
 'description': 'A finite-species extension of the OpenAI signed-impulse argument for relativistic Vlasov–Maxwell, with distinct masses and charges and no neutrality assumption.',
 'abstract': 'We extend the signed-impulse proof of the one-species three-dimensional relativistic Vlasov–Maxwell theorem in OpenAI’s family 362 manuscript to a fixed finite collection of particle species. Mass normalization gives a common velocity law and constant species-dependent accelerations. The entire source–receiver cancellation has coefficient eₐe_b/mₐ; the source acceleration cancels before its sign is discarded. A positive mass-weighted energy controls a disjoint union of species label spaces, and the angular occupation and selected receiver coefficient use one simultaneous momentum bootstrap. We prove the resulting global classical theorem for nonnegative smooth compact phase data and compatible C_b^∞ ∩ L² Maxwell fields, without smallness, symmetry or neutrality. The universal geometric identity is inherited; the new estimates keep all source and receiver coefficients explicit and close the shared-field bootstrap.',
 'plain_language': [
  'The relativistic Vlasov–Maxwell equations describe a collisionless population of charged particles and the electromagnetic field they create. Several particle species share the same field, but their masses and charges make them respond differently. The question is whether initially smooth data can develop a singularity in finite time.',
  'This paper claims global smooth evolution for a fixed finite collection of species under its stated regularity assumptions, without requiring the particles to be dilute, symmetric or electrically neutral overall. It extends the signed-impulse argument in a specific OpenAI one-species manuscript; that upstream analytical argument is an essential dependency.',
  'The useful cancellation occurs before taking absolute values. Electric and magnetic contributions that look large separately can partly cancel in the accumulated change of a particle’s momentum. With several species, the signs and mass factors must stay attached to the correct source and receiving particle throughout that calculation.',
  'The added problem is a shared-field estimate when charge-to-mass ratios differ. Simply adding all species into one density does not generally produce a one-species equation. The paper instead combines their positive energies and controls every species in one momentum argument.'
 ],
 'result': [
  'Fix a finite number of species in three space dimensions, each with a positive mass and a real charge, including zero charge. Their initial phase densities are nonnegative smooth functions with compact support in position and momentum.',
  'The initial electric and magnetic fields lie in C_b^∞(R³) ∩ L²(R³): every spatial derivative is bounded, and the fields have finite L² norm. They satisfy the Maxwell divergence constraints for the initial charge density.',
  'Under these assumptions, the published theorem asserts a unique global classical solution that is smooth on every finite time interval, with compact phase support on each such interval and fields continuous in time with values in L². No smallness, symmetry or neutrality condition is imposed.',
  'Mass normalization gives all species the same velocity law u(v) = v/√(1 + |v|²), with acceleration coefficient eₐ/mₐ. The complete interaction between a receiver of species a and a source of species b carries eₐe_b/mₐ; positive mass-weighted energy controls all species together.',
  'The argument imports the geometric cancellation and analytical framework of the pinned OpenAI family 362 manuscript. Its claimed addition is the explicit coefficient bookkeeping and simultaneous closure needed for a fixed finite multispecies system.'
 ],
 'limitations': [
  'This is an extension of a specific upstream proof. Its conclusion depends on the analytical estimates in that proof; it is not an independent proof of the one-species theorem obtained from the headline existence statement alone.',
  'The data assumptions include compact phase support and bounded derivatives of all orders for the initial fields. The theorem does not cover arbitrary smooth finite-energy data, noncompact momentum tails, collisions or a different spacetime model.',
  'The number of species and their masses and charges are fixed. Constants may depend on these parameters, the initial data and the time horizon. No uniform infinite-species or zero-mass limit, or uniform-in-time momentum bound, is established.',
  'When all charged species have the same nonzero charge-to-mass ratio, a weighted reduction already gives a one-species problem. The substantive extension concerns differing ratios, including mixtures of opposite charges.',
  'Classical bounded-momentum continuation results, the retarded division identities and the upstream signed-impulse mechanism are prior inputs. This bounded literature review does not establish exhaustive historical priority.',
  'The finite algebraic and rational checks in the archive do not verify the full analytical theorem. No independently reproduced proof-assistant certificate or completed external human peer review is claimed.'
 ],
 'background': [
  {'title': 'OpenAI, Global classical solutions of the three-dimensional relativistic Vlasov–Maxwell system, pinned family 362 manuscript', 'url': upstream, 'note': 'The exact source dependency, pinned to commit adc7f1241b42e322a6451854ab7e4b4c146bf78a. The multispecies paper inherits its geometric cancellation and signed-impulse estimates and adapts their coefficient and bootstrap structure.'},
  {'title': 'Luk and Strain, A new continuation criterion for the relativistic Vlasov–Maxwell system', 'url': 'https://arxiv.org/abs/1406.0165v1', 'note': 'Reviews bounded-momentum continuation and explicitly notes the multispecies setting in Remark 1.2. Continuation once momentum stays bounded is a classical input, not the new step here.'},
  {'title': 'Bouchut, Golse and Pallard, Classical solutions and the Glassey–Strauss theorem for the 3D Vlasov–Maxwell system', 'url': 'https://arxiv.org/abs/math/0301175v1', 'note': 'Lemma 3.1 gives the division identities; the derivative estimates use their angular cancellation and a logarithmic bound. These support the continuation background.'},
  {'title': 'Mattingly, Pankavich and Ben-Artzi, Sharp time decay and scattering of small data solutions to the relativistic Vlasov–Maxwell system', 'url': 'https://arxiv.org/abs/2609.29013v1', 'note': 'A different result on small-data decay and scattering, with additional cancellation hypotheses for globally neutral systems. Those hypotheses and conclusions should not be conflated with arbitrary-size finite-time regularity.'}
 ],
 'why_it_works': [
  'Normalize momentum by each species’ mass. This produces a common relativistic velocity law while leaving the distinct charge-to-mass ratios explicit in the acceleration.',
  'Apply the inherited source–receiver identity to each pair of species before estimating magnitudes. The source acceleration cancels within the identity, leaving the correct receiver-dependent factor eₐe_b/mₐ.',
  'Combine the separate species label spaces using their positive mass-weighted energy. One common momentum bound then controls angular occupation across the shared field without pretending that the sum of the densities solves a scalar transport equation.',
  'The paper transfers the direct-force and selected-receiver estimates with this common bound. The selection gain offsets the angular loss, allowing the signed-impulse bootstrap to improve itself for every species simultaneously.',
  'The resulting momentum-growth control rules out finite-time momentum blowup. A local theory compatible with nonneutral fields and the bounded-momentum continuation criterion then give the asserted global solution.'
 ],
 'collaboration': 'I welcome substantive collaboration on independently checking the multispecies transfer and its upstream analytical dependencies, sharpening the comparison with earlier plasma results, and assessing journal suitability. Expertise in kinetic equations, hyperbolic partial differential equations or relativistic plasma dynamics would be especially useful.',
 'follow_up': None,
 'followup_rationale': 'No public follow-up is proposed. Removing compact phase support, lowering regularity or seeking uniform limits changes essential analytical inputs. This review has not established a concrete mechanism or a sufficiently compelling new conjecture for any such extension.',
 'publication_date': '2026-10-06',
 'version': '6 October 2026 manuscript; no numbered version',
 'doi': '10.5281/zenodo.23203334',
 'author': 'Alec Kriebel',
 'pdf_filename': 'paper.pdf',
 'supplement_filename': 'source-and-verification.zip',
 'additional_assets': [],
 'related_resources': [{'label': 'Original Zenodo README', 'url': 'https://zenodo.org/records/23203334/files/README.md?download=1'}],
 'status': 'Unrefereed preprint dated 6 October 2026, developed with extensive AI assistance. The Zenodo record does not supply a numbered version. No completed human peer review or formal verification is claimed.',
 'ai_disclosure': 'AI tools were used extensively in developing, checking and presenting the argument. Internal AI-assisted review and finite computational checks are not external human peer review or formal verification of the analytical theorem.'
},
'22013710': {
 'title': 'An exceptional four-dimensional unitary Hecke Yang–Baxter operator: a five-word Pauli–Clifford normal form',
 'slug': 'exceptional-four-dimensional-hecke-yang-baxter-operator',
 'description': 'An explicit four-dimensional local Yang–Baxter operator, its sparse Pauli form, minimal dimension and exact connection to the Galindo–Rowell construction.',
 'abstract': 'We give an explicit 16 × 16 unitary Yang–Baxter operator in the class [e^{iπ/3}, 1/2, 4]. On C⁴ ≅ C² ⊗ C², its reflection has a five-word real Pauli–Clifford expansion. Four words combine into an involution M, a fifth involution E anticommutes with M, and an explicit 18-word cubic certificate restricts the reflection circle αM + βE exactly to α² = 2/3, β² = 1/3. The spectral projection has both unnormalized partial traces 2I₄, so normalized matrix trace induces the η = 1/2 Markov trace and a faithful representation of Hₙ(3, 6) for every n. A direct dimension-three obstruction, together with the known dimension-two obstruction, proves that four is minimal. Galindo and Rowell independently obtained the same local solution through a quaternionic twisted-group-algebra construction. We identify the present matrix exactly with a local-unitary normal form of the opposite of their Family III operator and extend the comparison to all braid strands. Transporting known Family III results shows that the braid images are finite and Clifford in a fixed conjugated Pauli frame. A direct scalar enhancement and skein calculation identify the trace invariant as 2P_H(L; i, i); the Galindo–Rowell metric-family algorithm then gives exact deterministic polynomial-time evaluation.',
 'plain_language': [
  'A Yang–Baxter operator is a local rule for crossing neighboring strands that gives the same answer for two equivalent three-strand braids. Here the rule is unitary, so it preserves lengths in the associated state space. Each strand carries four states, and a crossing acts on a pair of strands through a 16 × 16 matrix.',
  'The paper writes an exceptional example using just five products of small Pauli matrices. That sparse form makes its identities explicit and supports a short exact certificate. Four states per strand are shown to be the smallest possible for this particular faithful localization of the Hecke quotient.',
  'Galindo and Rowell independently obtained the same local solution within a broader construction. This paper gives an exact change of basis and reversal of the local tensor factors relating the two presentations, then extends the comparison to any number of strands.',
  'That connection also explains the operator’s computational limits. Its braid images are finite and have Clifford structure in a fixed transformed basis. Its link invariant is a known special value of the HOMFLYPT polynomial, with an exact polynomial-time evaluation inherited from the Galindo–Rowell algorithm.'
 ],
 'result': [
  'For q = e^{iπ/3}, the paper gives an explicit 16 × 16 unitary operator R on C⁴ ⊗ C⁴ satisfying the braided Yang–Baxter equation and (R − qI)(R + I) = 0. The local state-space dimension is four.',
  'Its Hermitian reflection is a real linear combination of five Pauli–Clifford words. Within the specified circle H = αM + βE, the Yang–Baxter condition holds exactly at α² = 2/3 and β² = 1/3. This is a classification within that circle.',
  'The rank-eight spectral projection has both unnormalized partial traces equal to 2I₄. Normalized matrix trace then realizes the η = 1/2 Markov trace, with a faithful representation of the quotient Hₙ(3, 6) for every strand number n.',
  'A dimension-three obstruction, combined with the established dimension-two obstruction, proves minimal local dimension four for this faithful ordinary localization. Tensor amplification supplies local dimensions divisible by four.',
  'The operator is locally unitarily equivalent to the opposite of the Galindo–Rowell Family III operator. An all-strand intertwiner transfers the finite-image and conjugated Clifford-frame conclusions to this presentation.',
  'With the paper’s scalar enhancement, the link invariant is 2P_H(L; i, i), normalized to equal 2 on the unknot. The fixed metric-family algorithm of Galindo and Rowell gives exact deterministic polynomial-time evaluation in the strand number and braid-word length.'
 ],
 'limitations': [
  'The same local solution occurs in Galindo and Rowell’s independent construction. The public description credits that work and does not assert exclusive first priority. Historical public-release claims in the manuscript were not independently established in this review.',
  'The four reflection-circle solutions do not classify all Yang–Baxter operators in the exceptional class or prove uniqueness up to tensor equivalence. Minimal dimension four also does not classify every larger admissible local dimension.',
  'The comparison uses the opposite operator, which reverses the two local tensor factors, and an explicit basis change. Bare unitary similarity of matrices would not by itself identify their tensor-local braid representations.',
  'Clifford structure holds in a fixed conjugated Pauli frame. The paper does not claim that the displayed matrix is Clifford in the standard computational Pauli basis, or that its braids provide universal quantum computation.',
  'The faithful algebra is the braid-generated Hecke quotient inside the quaternionic tower. It is not the entire quaternionic algebra at every strand number.',
  'The HOMFLYPT evaluation and branched-cover formula are established invariants. Their identification with this normalization, and the transport of a known exact algorithm, do not constitute a new general algorithm for arbitrary quantum circuits or link-polynomial values.',
  'The final algebraic certificate is reproducible, but the initial numerical discovery search was not retained as a fully reproducible or exhaustive search. Finite computations supplement the all-strand argument; no completed external human peer review or proof-assistant certification is claimed.'
 ],
 'background': [
  {'title': 'Lechner, The classification problem for unitary R-matrices with two eigenvalues', 'url': 'https://arxiv.org/abs/2603.20158v1', 'note': 'Gives the Markov-trace classification framework and exceptional root-of-unity classes. The dimension and trace parameter are essential parts of the class under discussion.'},
  {'title': 'Galindo and Rowell, Unitary Yang–Baxter operators: towards a classification', 'url': 'https://arxiv.org/abs/2608.16865v1', 'note': 'Section 13 constructs the same exceptional local solution. Its Family III construction, trace comparison, finite-image and Clifford results, and metric-family algorithm supply the global conclusions transported here.'},
  {'title': 'Galindo, Hong and Rowell, Generalized and quasi-localizations of braid group representations', 'url': 'https://people.tamu.edu/~rowell/GHRarx1.pdf', 'note': 'Section 5.6 gives the earlier dimension-two obstruction for ordinary localization and distinguishes quasi-local and generalized realizations, which have different tensor placement rules.'},
  {'title': 'Rowell, A quaternionic braid representation', 'url': 'https://ems.press/content/serial-article-files/36758', 'note': 'Identifies the relevant Hecke quotient as a braid-generated subalgebra of the quaternionic tower and proves finite braid images. The whole quaternionic algebra must not be substituted for that subalgebra.'},
  {'title': 'Rowell and Wang, Localization of unitary braid group representations', 'url': 'https://arxiv.org/abs/1009.0241v2', 'note': 'Defines faithful localization of a whole sequence of braid representations and states the broader localization conjecture. A single exceptional example does not settle that general conjecture.'},
  {'title': 'Lickorish and Millett, Some evaluations of link polynomials', 'url': 'https://web.math.ucsb.edu/~millett/Papers/1986Millett6LickorishCommMathHelv.pdf', 'note': 'Theorem 2 evaluates P_H(L; i, i) using the mod-2 first homology of a cyclic triple branched cover. This prior topological evaluation underlies the formula identified in the paper.'}
 ],
 'why_it_works': [
  'Four Pauli words combine into one Hermitian involution, and a fifth involution anticommutes with it. Their linear combination is therefore a reflection when α² + β² = 1.',
  'Expanding the cubic braid relation in a linearly independent Pauli-word basis gives an exact finite certificate. On the chosen circle it forces α² = 2/3 and β² = 1/3.',
  'The two scalar partial traces identify the Markov trace. Positivity then identifies the representation kernel with its trace annihilator, proving faithfulness on the quotient for every n rather than only checking a few small matrices.',
  'An explicit local conjugacy to the opposite Galindo–Rowell operator extends through tensor-site reversal and a braid half twist. This makes the known Family III structure available on all strands.',
  'The quadratic relation and scalar enhancement give the HOMFLYPT skein relation with the stated unknot normalization. The exact trace comparison allows the established metric-family algorithm to evaluate the resulting invariant.'
 ],
 'collaboration': 'I welcome substantive collaboration on independent verification of the all-strand identifications, the relationship to localization and operator-classification results, and preparation for journal review. Expertise in braid representations, quantum algebra, tensor categories or link invariants would be particularly useful.',
 'follow_up': None,
 'followup_rationale': 'No public follow-up is proposed. Full uniqueness, additional local dimensions and a wider classification are natural questions, but this review supplies neither a new approach nor evidence strong enough to promote them as a focused conjecture. Much of the broader structure is already covered by the Galindo–Rowell work.',
 'publication_date': '2026-08-19',
 'version': '1.2.0',
 'doi': '10.5281/zenodo.22013710',
 'author': 'Alec Kriebel',
 'pdf_filename': 'exceptional-ybe-d4-v1.2.0.pdf',
 'supplement_filename': 'exceptional-ybe-d4-v1.2.0-source.zip',
 'additional_assets': [],
 'related_resources': [{'label': 'Original published SHA-256 checksums', 'url': 'https://zenodo.org/records/22013710/files/SHA256SUMS?download=1'}],
 'status': 'Unrefereed preprint, printed manuscript version 1.2.0 dated 19 August 2026, developed with extensive AI assistance. Zenodo omits a version field. No completed human peer review or formal verification is claimed.',
 'ai_disclosure': 'AI tools were used extensively in discovery, symbolic verification, software, drafting and internal review. The retained exact identities can be independently checked; internal AI review is not external human peer review or proof-assistant certification.'
}
}

for ident, c in contents.items():
    p = B/ident
    record = json.loads((p/'sources/record.json').read_text())
    receipt = json.loads((p/'sources/receipt.json').read_text())
    by_name = {f['name']:f for f in receipt['files']}
    is_vm = ident == '23203334'
    c['source_binding'] = dict(
        record_id=ident, concept_record_id=str(record['conceptrecid']),
        record_url=f'https://zenodo.org/records/{ident}', doi=c['doi'],
        zenodo_version=record['metadata'].get('version'),
        manuscript_version=None if is_vm else '1.2.0',
        manuscript_date='6 October 2026' if is_vm else '19 August 2026',
        publication_date=record['metadata']['publication_date'],
        archive_version_label=None if is_vm else 'v1.2.0',
        version_source=('Zenodo has no version metadata and the printed PDF gives a date without a numbered version. The page uses a descriptive manuscript-date label, not an invented version number.' if is_vm else 'Zenodo has no version metadata. Version 1.2.0 is printed on the PDF and present in the original PDF/ZIP filenames; the raw record is preserved unchanged.'),
        source_retrieved_utc=receipt['retrieved_utc'],
        pdf_sha256=by_name[c['pdf_filename']]['sha256'],
        supplement_sha256=by_name[c['supplement_filename']]['sha256'],
        files=receipt['files'],
        reviewed_documents=[dict(filename=c['pdf_filename'], pages=10 if is_vm else 20, read_scope='all pages')],
        support_read_scope=('All five published mathematical Markdown supplements read in full: pair identity, transfer lemma, uniform lemma chain, local theory and occupation audit. The occupation supplement includes historical independent review assessments, encountered before the scope checkpoint; exposure is disclosed and those assessments are not used as validation. No current sibling mathematical verdict consulted.' if is_vm else 'Full main manuscript and exact verification source verify_tensor_words.py and verify_concurrent_equivalence.py read. Dedicated archived audit/adjudication opinions were not consulted. Historical status and chronology assertions in the manuscript were encountered but not adopted as proof or independently verified priority.'),
        abstract_source='Complete original page 1 abstract, visually checked and cross-checked against TeX. Only mathematical typography and whitespace normalized. AI/status prose is separate.',
        archive_pdf_identity=('No PDF or nested ZIP occurs in the source-and-verification archive; the separate ten-page PDF is the complete reader manuscript.' if is_vm else 'The only archive PDF is output/pdf/exceptional_ybe_d4.pdf, byte-identical to the separately published twenty-page main PDF. No additional supplement PDF or nested ZIP is present.'),
        review_boundary=('Publication scope and bounded primary-literature review with explicitly disclosed archived-opinion exposure; not an independent mathematical gate, exhaustive novelty certificate or human peer review.' if is_vm else 'Independent publication scope and bounded primary-literature review; not an independent mathematical gate, exhaustive novelty certificate or human peer review.')
    )
    (p/'reviews/scope/content.json').write_text(json.dumps(c, indent=2, ensure_ascii=False)+'\n')
    with (p/'reviews/scope/RESEARCH_LOG.md').open('a') as f:
        f.write('\n## '+datetime.now(timezone.utc).isoformat()+' — 85%\n\nCandidate content drafted with complete original abstract, exact metadata boundaries, primary-source credit and follow_up:null. All published files and archive manifest entries pass byte integrity checks. Final report and disposition remain.\n')
    print(ident, len(json.dumps(c, ensure_ascii=False)))
