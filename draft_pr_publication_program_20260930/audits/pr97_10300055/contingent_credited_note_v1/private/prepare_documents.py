"""Prepare safe metadata and a bounded source-read ledger; no publication calls."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil

D = Path(__file__).absolute().parent.parent
A = D.parent
P = D/'publicfiles'
C = A/'primary_source_cache_20261005'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

sources = []
def source(key, title, path, url, scope, mode, limits):
    sources.append(dict(id=key, title=title, source_url=url,
        source_sha256=sha(path), research_source_reference=str(path.relative_to(A)),
        preparation_read_scope=scope, read_mode=mode, limits=limits))

source('C', 'Calegari 2002 Version 0.78', C/'calegari2002.pdf',
       'https://arxiv.org/pdf/math/0209081v1',
       'Printed/PDF pp.1 and 29: date/version, tautness definition, entire Questions 13.1/13.2 and nearby remarks',
       'Actual cached primary PDF text; p.29 newly rendered and visually inspected',
       'Final AMS 2003 chapter body unread. Ordinary fundamental-class closed/oriented interpretation is explicit, not a quoted source-wide convention.')
source('V11', 'Vogel 2011 Rigidity versus flexibility for tight confoliations', C/'vogel2011.pdf',
       'https://msp.org/gt/2011/15-1/gt-v15-n1-p03-p.pdf',
       'Printed pp.42–43 (PDF pp.2–3): exact ET every-sufficiently-C0-close tightness statement and disk criterion',
       'Actual cached primary PDF text; p.42 newly rendered and visually inspected',
       'Full ET book unread; imported global theorem not reproved.')
source('V16', 'Vogel 2016 On the uniqueness of the contact structure approximating a foliation', C/'vogel2016.pdf',
       'https://msp.org/gt/2016/20-5/gt-v20-n5-p01-p.pdf',
       'Printed p.2451 (PDF p.13): entire smooth Gray Theorem 2.9 and surrounding relative/parameter discussion',
       'Actual cached primary PDF text and new visual inspection of statement page',
       'Smooth theorem only; no C1 Gray assertion.')
source('DR', 'Dathe–Rukimbira 2008 author preprint', C/'dathe_rukimbira2008.pdf',
       'https://arxiv.org/pdf/0812.3389v1',
       'PDF p.5: tightness definition and Propositions 3.3–3.4 with proof',
       'Actual cached primary PDF text and new visual inspection of statement page',
       'Proposition 3.4 assumes closed defining form. Final published 2011 body unread.')
source('DK', 'Dathe–Khoule 2012 original article',
       A/'priority_covering_interpretation_adversary_20261006/private_dk2012_body_reconstruction.txt',
       'https://www.researchgate.net/publication/258228980_Sur_les_deformations_d%27un_feuilletage_de_codimension_1_en_structures_de_contact',
       'Printed pp.102–103: actual original Definition 2.1, coefficient conditions, Theorem 2.2, full expansion/proof, original reconstructed lines L491–679',
       'Primary author-uploaded transcription reconstructed by the prior audit; actual supporting statement text independently read, not inferred from a report',
       'Original PDF pixels not obtained. Earlier audits read all 1166 original body/reference lines L43–1208 (pp.100–107). This preparation reread actual statement/proof pages, not the complete article. No literal exact tightness/Question 13.2 answer located in the complete transcription; bounded absence is not firstness proof. Printed theorem does not explicitly name a C1 threshold.')
source('KMNW', 'Khoule–Manso–Ndiaye–War 2025 arXiv:2503.00454v1',
       A/'priority_linear_contact_mechanism_20261006/khoule_manso_ndiaye_war2025.pdf',
       'https://arxiv.org/pdf/2503.00454v1',
       'Section 6, PDF/printed pp.32–33: Definition 6.1, historical C1 attribution, Theorem 6.2 and equations (59)–(63)',
       'Actual cached primary PDF extraction read independently',
       'Normalized equality drops nonnegative mixed term in general; valid in zero-Q case. Unrelated main results not audited.')

ledger = dict(schema='pr97-source-read-scope/v1',
    recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    preparation_scope='Short smooth-omega classical corollary; no fresh central proof search',
    sources=sources,
    unread_material_gaps=[
        dict(title='Final Calegari 2003 AMS chapter', doi='10.1090/pspum/071/2024640',
             gap='Bibliographic identity authenticated; actual body unread; no equality with 2002 inferred'),
        dict(title='Eliashberg–Thurston Confoliations',
             gap='Full body unread; exact neighborhood statement verified through V11/DR'),
        dict(title='Final Dathe–Rukimbira 2011 article', doi='10.1515/advgeom.2010.043',
             gap='Full published body unread; 2008 version inspected'),
        dict(title='Khoule–Ndiaye–Wade 2025 affine-pairs article', doi='10.1007/s00022-025-00742-z',
             gap='Full body unread'),
        dict(title='Named Mitsumatsu Warsaw/Japanese materials and complete citation coverage',
             gap='Not read; no speculative secondary routes used')],
    third_party_redistribution=False, priority_clearance=False, publication_authorized=False)
(P/'PRIMARY_SOURCE_READ_SCOPE.json').write_text(json.dumps(ledger, indent=2, ensure_ascii=False)+'\n')

input_refs = [
    'credited_verification_candidate_v2/CANDIDATE.md',
    'credited_verification_candidate_v2/verify.py',
    'credited_verification_candidate_v2/review/independent_checks.py',
    'ROOT_MATHEMATICAL_GATE_20261005.json',
    'ROOT_CREDITED_CANDIDATE_PREPARATION_20261006.json',
    'ROOT_PRIORITY_ADJUDICATION_20261006.json',
    'priority_question_history_20261006/REPORT.md',
    'priority_linear_contact_mechanism_20261006/REPORT.md',
    'priority_covering_interpretation_adversary_20261006/REPORT.md']
(D/'private/INPUT_BINDINGS.json').write_text(json.dumps(dict(
    schema='pr97-preparation-inputs/v1',
    inputs=[dict(reference=rel, sha256=sha(A/rel), bytes=(A/rel).stat().st_size)
            for rel in input_refs]), indent=2)+'\n')

preset = Path('/Users/alec/Documents/Math/zenodo_deposit_tool/deposit.example.json')
previous = A.parent/'pr95_10400120/qualified_publication_package_v2/zenodo-deposit.json'
proto = json.loads(preset.read_text())['metadata']
old = json.loads(previous.read_text())['metadata']
meta = {key: proto[key] for key in ['upload_type', 'publication_type', 'access_right', 'license', 'creators']}
description = [
    'A short classical argument proves ordinary tightness of a smooth contact form omega satisfying d alpha = alpha wedge omega, when a global nowhere-zero C1 alpha defines a cooriented taut C2 foliation without spherical leaves on a closed oriented smooth three-manifold. The proof uses the known Dathe–Khoule 2012 general affine criterion, a finite contact path, the Eliashberg–Thurston tightness neighborhood and smooth Gray stability, with finite-interval smoothing of alpha. It addresses the conditional tightness implication in Calegari’s actual 2002 Version 0.78 Question 13.2 under the smooth contact-form interpretation; it does not produce a contact connection form or settle the separate existence Question 13.1.',
    'Historical priority remains unresolved. The general contact-pencil mechanism is prior work, and ordinary smooth tightness is our standard corollary of prior affine/ET/Gray results. No first solution, exhaustive novelty clearance, present-day open status or newly discovered historical resolution is claimed. The final AMS 2003 Calegari chapter, DOI 10.1090/pspum/071/2024640, and full Confoliations remain unread; equality with the 2002 source is not assumed. Bounded actual-source comparisons and unread boundaries are documented. The longer supporting candidate separately retains accurately qualified C1-contact/C2-disk extras whose novelty is also unestablished.',
    'AI tools were used extensively in analysis, drafting, literature comparison, reproduction and adversarial verification. No conventional human peer review or refereeing has occurred; independent AI audits are not human peer review. Exact finite symbolic/rational programs check local differential-form identities, boundary corrections and contact-margin arithmetic, not imported global ET/Gray proofs or priority. The package comprises PDF, LaTeX source, exact support programs/current candidate, actual-run receipts, a safe closed manifest, qualification, read-scope ledger and instructions. No third-party paper bodies/images are included.']
meta.update(title='Tightness of contact Godbillon–Vey forms: a classical argument for Calegari’s conditional question',
    version='1.0', publication_date='2026-10-05',
    keywords=['Godbillon–Vey', 'taut foliation', 'tight contact structure',
              'affine contact deformation', 'Calegari Question 13.2'],
    description=''.join('<p>'+paragraph+'</p>' for paragraph in description),
    related_identifiers=[dict(identifier=value, relation='references', scheme=scheme)
        for value, scheme in [
            ('https://arxiv.org/abs/math/0209081v1', 'url'),
            ('https://www.researchgate.net/publication/258228980_Sur_les_deformations_d%27un_feuilletage_de_codimension_1_en_structures_de_contact', 'url'),
            ('10.2140/gt.2011.15.41', 'doi'), ('10.2140/gt.2016.20.2439', 'doi'),
            ('https://arxiv.org/abs/0812.3389v1', 'url'),
            ('https://arxiv.org/abs/2503.00454v1', 'url')]])
(P/'zenodo_metadata.proposed.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False)+'\n')
(D/'private/METADATA_PROVENANCE.json').write_text(json.dumps(dict(
    preset_path=str(preset), preset_sha256=sha(preset),
    pr95_pattern_path=str(previous), pr95_pattern_sha256=sha(previous),
    fields_preserved_from_preset=['creators','upload_type','publication_type','access_right','license'],
    pattern_adapted_from_pr95=['HTML paragraph scope, priority and AI disclosure',
                             'keywords','related_identifiers','publication_date','version'],
    creator_preset_equals_pr95=(meta['creators']==old['creators']),
    no_pr95_authorization_inherited=True, proposed_metadata_only=True,
    publication_authorized=False), indent=2)+'\n')
print('Source ledger and proposed metadata prepared')
