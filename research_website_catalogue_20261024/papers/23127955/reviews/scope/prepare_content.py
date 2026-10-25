"""Prepare unpromoted, source-bound page content; never writes publication or source files."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[1]
SOURCE = PAPER / 'sources'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

receipt = json.loads((SOURCE / 'receipt.json').read_text())
record = json.loads((SOURCE / 'record.json').read_text())
metadata = record['metadata']
tex_path = SOURCE / 'published-source/paper.tex'
tex = tex_path.read_text()
abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1).strip()
abstract = abstract.replace('$\\R^3$', 'ℝ³').replace('$2$', '2').replace('~', ' ')
abstract = ' '.join(abstract.split())
assert '\\' not in abstract and '$' not in abstract
abstract = abstract.replace(' For compact sets,', '\n\nFor compact sets,')
abstract = abstract.replace(' This proves the measure-zero', '\n\nThis proves the measure-zero')
files = {item['name']: item for item in receipt['files']}
content = {
    'title': metadata['title'],
    'slug': 'common-tangents-three-convex-sets-null',
    'description': 'Common supporting tangent lines to three disjoint convex sets in three-dimensional space occupy zero volume, even for nonsmooth or nonclosed sets.',
    'abstract': abstract,
    'plain_language': [
        'Take three convex sets in three-dimensional space, with no point belonging to more than one set. A convex set contains the straight segment between any two of its points. Here a tangent line must actually meet the set and lie in a supporting plane: a plane with the entire set on one side.',
        'Now collect every line tangent to all three sets and extend each line infinitely in both directions. The paper proves that the whole collection occupies zero three-dimensional volume. This remains true for unbounded sets, sets missing some boundary points, nonsmooth shapes, and even sets lying in a plane or a line.',
        'The striking point is the change from two sets to three. Common tangents to two disjoint rectangles can fill a region of positive volume. A third disjoint convex set imposes an additional contact condition that forces the volume swept out by the common tangents to vanish. Zero volume does not mean there are only finitely many lines.'
    ],
    'result': [
        'For every three pairwise disjoint convex subsets K₁, K₂ and K₃ of ℝ³, the union of all complete affine lines tangent to each set has three-dimensional Lebesgue outer measure zero. Equivalently, this union is contained in a Lebesgue-measurable null set. If any set is empty, the union is empty.',
        'Tangency requires actual intersection with the set and containment of the line in a supporting plane. Contacts and supporting planes need not be unique, and a contact may be an entire segment. The sets need not be closed, bounded, full dimensional, strictly convex or smooth; their closures may intersect.',
        'This is the measure-zero statement of Xavier Goaoc’s Conjecture 4 in Oberwolfach Report 44/2008, section 13, page 2552. The paper does not establish the separate countable-union-of-2-manifolds statement in Conjecture 3.'
    ],
    'why_it_works': [
        'The proof first localizes actual contacts to countably many disjoint compact caps. For two compact convex sets it constructs countably many Lipschitz families of lines, each described by two parameters. The construction uses support inequalities and a contraction argument, so it does not require smooth boundaries or differentiable support functions.',
        'At almost every parameter corresponding to a common tangent, each contact forces a transverse derivative to have rank at most one. The determinant that measures the volume swept out along the line is a polynomial of degree at most two in the height coordinate. The three distinct contacts give it three distinct roots, so it vanishes identically. The area formula then gives zero volume. Separate cases handle points, segments and planar sets.'
    ],
    'limitations': [
        'Nullness is a statement about ordinary three-dimensional volume. The paper does not prove containment in countably many 2-manifolds, a Hausdorff-dimension bound of two, or a description by smooth surfaces.',
        'Pairwise disjointness and supporting tangency are essential to the stated theorem. Lines that merely pass through the interiors of the sets are not covered. Contact with a closure alone is not enough when the original set omits that contact point.',
        'For nonclosed inputs the union of tangent lines need not itself be closed. The outer-measure conclusion avoids assuming either input measurability or closedness of that union.',
        'This is a geometric existence theorem, not an algorithm for enumerating tangents, a bound on their number, or a theorem in arbitrary ambient dimensions. The source package’s exact finite checks support algebraic and rational steps; they do not replace the proof for arbitrary convex sets.',
        'The attribution to the 2008 conjecture identifies the historical question answered by the stated theorem. It is not a certification of first priority, an exhaustive literature search, or a claim that the question remained unresolved until this preprint.'
    ],
    'background': [
        {
            'title': 'Xavier Goaoc, Union of lines tangent to three convex sets in ℝ³ (2008)',
            'url': 'https://ems.press/content/serial-article-files/46191',
            'note': 'Oberwolfach Report 44/2008, section 13, page 2552. Gives the supporting-tangency convention and distinguishes the measure-zero conjecture from the 2-manifold conjecture.'
        },
        {
            'title': 'Demouth and Goaoc, Topological changes in the apparent contour of convex sets',
            'url': 'https://web.archive.org/web/20110401122240id_/http://www.loria.fr/~goaoc/papers/TopVE.pdf',
            'note': 'The historical author-hosted manuscript asks the compact-convex measure-zero question in section 7, printed page 11. The 1 April 2011 archive capture does not establish the manuscript’s publication date or identity with the version cited in 2008.'
        },
        {
            'title': 'Leon Simon, Introduction to Geometric Measure Theory',
            'url': 'https://math.stanford.edu/~lms/ntu-gmt-text.pdf',
            'note': 'The standard density theorem, Rademacher’s theorem and area formula supply the analytic inputs; chapter 1, Corollary 3.10, and chapter 2, Theorems 1.4 and 3.3.'
        },
        {
            'title': 'Cheong, Goaoc and Holmsen, Some New Results on Geometric Transversals (2024)',
            'url': 'https://doi.org/10.1007/s00454-023-00573-2',
            'note': 'Related work on the topology and existence of meeting transversals. These are different questions from the spatial volume of supporting tangent lines.'
        },
        {
            'title': 'Cheong, Goaoc and Holmsen, The Topology of the set of line Transversals (author preprint)',
            'url': 'https://arxiv.org/abs/2205.14681v2',
            'note': 'Accessible author preprint for the line-transversal component of the published article; its stated theorem concerns acyclicity for disjoint open convex sets.'
        }
    ],
    'collaboration': 'I welcome independent scrutiny from researchers in convex geometry, geometric measure theory and geometric transversals, especially a close reading of the compact-cap localization, the Lipschitz parametrizations and the treatment of degenerate contacts. Substantive improvements to the proof or its presentation could support a joint journal submission.',
    'follow_up': None,
    'followup_rationale': 'The stronger 2-manifold statement is a substantial existing problem, but this review establishes no concrete new route from the null-Jacobian argument to the required regularity. No speculative follow-up is added merely to populate a section.',
    'publication_date': metadata['publication_date'],
    'version': metadata['version'],
    'doi': record['doi'],
    'author': 'Alec Kriebel',
    'pdf_filename': 'common_tangent_nullness.pdf',
    'supplement_filename': 'common_tangents_null_locus_v1.zip',
    'supplement_label': 'Source and exact finite controls (ZIP)',
    'additional_assets': [],
    'status': 'Unrefereed preprint',
    'ai_disclosure': 'This is an unrefereed preprint. Extensive AI assistance was used in solving, drafting and internal verification, including adversarial mathematical examinations. It has not undergone conventional external human peer review; internal AI examinations do not constitute such review.',
    'source_binding': {
        'record_id': '23127955',
        'concept_record_id': str(record['conceptrecid']),
        'record_url': 'https://zenodo.org/records/23127955',
        'doi': record['doi'],
        'metadata_version': metadata['version'],
        'zenodo_version': metadata['version'],
        'manuscript_version': None,
        'manuscript_date': '3 October 2026',
        'publication_date': metadata['publication_date'],
        'source_receipt_sha256': sha(SOURCE / 'receipt.json'),
        'record_metadata_sha256': sha(SOURCE / 'record.json'),
        'pdf_sha256': files['common_tangent_nullness.pdf']['sha256'],
        'supplement_sha256': files['common_tangents_null_locus_v1.zip']['sha256'],
        'files': receipt['files'],
        'primary_tex_path': 'sources/published-source/paper.tex',
        'primary_tex_sha256': sha(tex_path),
        'mathematical_support_path': 'sources/published-source/source/CANDIDATE.md',
        'mathematical_support_sha256': sha(SOURCE / 'published-source/source/CANDIDATE.md'),
        'abstract_source': 'Complete sole abstract in published paper.tex, lines 25–27; only TeX-to-Unicode normalization and paragraph breaks.',
        'main_pdf_pages': 8,
        'unique_reader_pdf_count': 1,
        'additional_reader_pdfs': [],
        'archive_pdf_copy': 'sources/published-source/common_tangent_nullness.pdf',
        'archive_pdf_byte_identical': True,
        'metadata_related_identifiers': metadata.get('related_identifiers', []),
        'review_boundary': 'Acquisition, source/claim scope and editorial candidate only. No mathematical promotion, no fresh scientific-code execution, no conventional peer review or novelty certification.'
    }
}
(HERE / 'content.json').write_text(json.dumps(content, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status':'DRAFT_SCOPE_CONTENT_ONLY','abstract_words':len(abstract.split()),'description_characters':len(content['description']),'files':len(files),'follow_up':None}))
