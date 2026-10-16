"""Strict payload, metadata and present-required external binding verifier."""
import sys
sys.dont_write_bytecode = True
import json
from common import ROOT, archive_bytes, digest, load, member, regular, require
from metadata_constants import EXPECTED_METADATA

def identity(path):
    raw = regular(path).read_bytes()
    return {'bytes':len(raw), 'sha256':digest(raw)}

def terminal_state():
    """Check current administration against exact dated review interfaces."""
    current = load(ROOT/'TERMINAL_STATUS.json')
    expected = {
        'schema_version':1, 'checkpoint_date_utc':'2026-10-16',
        'stage':'TERMINAL_ADMIN_COMPLETE_PENDING_ROOT_FINAL_INTEGRITY',
        'new_complete_whole_reviews_completed':2,
        'minimum_new_complete_whole_reviews_required':2,
        'latest_whole_review':'NEW_INDEPENDENT_COMPLETE_WHOLE_PACKAGE_02',
        'latest_review_complete':True,
        'latest_review_actionable_findings':{'P0':0,'P1':0,'P2':0,'P3':0},
        'latest_whole_review_ROOT_adopted':True,
        'further_whole_package_review_currently_required':False,
        'terminal_administrative_reconciliation_complete':True,
        'ROOT_final_terminal_integrity':'REQUIRED_UNADOPTED',
        'ROOT_final_terminal_integrity_adopted':False,
        'publication_ready':False, 'issues_resolved':False, 'published':False,
        'services_held_after_pr':1032,
        'full_result_physical_simple_oriented_realization_remaining_method_priority_worldwide_openness':'UNKNOWN',
        'exact_scope_math_adopted':True, 'evidence_root':'terminal/evidence',
        'historical_preparation_status':'STATUS.json'}
    for key, value in expected.items():
        require(type(current.get(key)) is type(value) and current[key] == value,
                'terminal current field: '+key)
    require(current['unchanged_paper'] == identity(ROOT/'paper.pdf'),
            'terminal unchanged paper identity')
    zero = {'P0':0,'P1':0,'P2':0,'P3':0}
    adoptions = []
    staged = load(ROOT/'terminal/REVIEW_STAGE_SELECTION.json')['entries']
    require(len(staged) == 55
            and len({(r['review'],r['path']) for r in staged}) == 55,
            '55 individual review-stage decisions')
    for number in (1,2):
        tag = str(number).zfill(2)
        prefix = ROOT/('terminal/evidence/package_'+tag)
        verdict = load(prefix/'VERDICT.json')
        seal = load(prefix/'OUTPUT_SEAL.json')
        pins = load(prefix/'OUTPUT_PINS.json')
        root = load(ROOT/('terminal/evidence/ROOT_WHOLE_PACKAGE_REVIEW_'+tag+'.json'))
        require(verdict['review'] == 'NEW_INDEPENDENT_COMPLETE_WHOLE_PACKAGE_'+tag,
                'whole-review identity '+tag)
        require(verdict['finding_counts'] == zero and verdict['findings'] == []
                and verdict['delegated_completion_percent'] == 100
                and verdict['new_complete_whole_reviews_contributed'] == 1
                and verdict['minimum_new_complete_whole_reviews_required'] == 2,
                'complete zero-actionable whole review '+tag)
        for obj in (verdict, seal, root):
            require(obj['publication_ready'] is False and obj['services_held_after_pr'] == 1032,
                    'dated review service hold '+tag)
        require(verdict['published'] is False and root['published'] is False
                and root['issues_resolved'] is False, 'dated review publication state '+tag)
        require(seal['findings'] == zero and seal['verdict'] == identity(prefix/'VERDICT.json'),
                'review seal verdict identity '+tag)
        require(seal['output_pins'] == identity(prefix/'OUTPUT_PINS.json')
                and root['output_pins_sha256'] == seal['output_pins']['sha256'],
                'ROOT adoption pin identity '+tag)
        require(root['whole_reviews_completed'] == number, 'ROOT adopted count '+tag)
        selected = ['VERDICT.json','REPORT.md'] + [
            'INDEPENDENT_DERIVATION_FROZEN.md' if number == 1 else 'INDEPENDENT_DERIVATION.md']
        require(seal['report'] == identity(prefix/'REPORT.md')
                and seal['independent_derivation'] == identity(prefix/selected[2]),
                'review seal authored interfaces '+tag)
        rows = pins['entries']
        require(len(rows) == (22 if number == 1 else 33), 'review output count '+tag)
        require(len({r['path'] for r in rows}) == len(rows), 'review unique output paths '+tag)
        for name in selected:
            matching = [r for r in rows if r['path'] == name]
            require(len(matching) == 1 and {k:matching[0][k] for k in ('bytes','sha256')}
                    == identity(prefix/name), 'review selected output pin '+tag+'/'+name)
        stage_rows = [r for r in staged if r['review'] == 'package_'+tag]
        require(len(stage_rows) == len(rows), 'complete review-stage partition '+tag)
        for row in rows:
            choices = [r for r in stage_rows if r['path'] == row['path']]
            require(len(choices) == 1 and all(choices[0][k] == row[k]
                    for k in ('bytes','sha256')), 'review-stage original identity '+tag)
            choice = choices[0]
            if row['path'] in selected:
                require(choice['disposition'] == 'EXACT_AUTHORED_COPY'
                        and choice['destination'] == 'terminal/evidence/package_'+tag+'/'+row['path']
                        and identity(member(choice['destination'])) == {k:row[k] for k in ('bytes','sha256')},
                        'review-stage selected copy '+tag)
            else:
                require(choice['disposition'] == 'OMITTED' and bool(choice['reason']),
                        'review-stage individual omission '+tag)
        adoptions.append(root)
    first, latest = adoptions
    require(first['status'] == 'ADOPT_COMPLETE_WHOLE01_ZERO_ACTIONABLE_SECOND_NEW_COMPLETE_WHOLE_REVIEW_REQUIRED'
            and first['minimum_new_complete_whole_reviews'] == 2
            and first['ROOT_full_REPORT_frozen_derivation_source_ledger_and_new_independent_code_read'] is True,
            'first dated ROOT adoption')
    require(latest['status'] == 'ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN'
            and latest['minimum_whole_reviews'] == 2 and latest['actionable_P0_P1_P2_P3'] == 0
            and latest['ROOT_full_REPORT_frozen_derivation_source_ledger_new_independent_controls_custody_checker_and_period_deletion_addendum_read'] is True
            and latest['terminal_administrative_reconciliation_and_root_final_integrity_required'] is True,
            'latest complete ROOT adoption')
    require(latest['complete_custody_closed_ZIP_and_metadata']['independent_closed_archive']['bytes']
            == current['reviewed_preterminal_support_archive']['bytes']
            and latest['complete_custody_closed_ZIP_and_metadata']['independent_closed_archive']['sha256']
            == current['reviewed_preterminal_support_archive']['sha256'], 'reviewed preterminal archive identity')
    require(latest['complete_custody_closed_ZIP_and_metadata']['paper'] == current['unchanged_paper'],
            'adopted unchanged paper identity')
    require(latest['review_actual_unmodified_external_commands'] == 116
            and latest['review_runtime_ROOT_or_ORIGINAL_modified'] is False,
            'latest actual execution scope')
    old = load(ROOT/'STATUS.json')
    require(old['new_complete_whole_reviews_completed'] == 0
            and old['minimum_new_complete_whole_reviews_required'] == 2
            and old['stage'] == 'PREPARATION_PENDING_TWO_NEW_COMPLETE_WHOLE_REVIEWS',
            'dated preparation checkpoint preserved')
    resolution = load(ROOT/'terminal/PREPARATION_PIN_RESOLUTION.json')['entries']
    require(len(resolution) == 123 and len({r['path'] for r in resolution}) == 123,
            '123 preparation pin resolutions')
    prep_pins = load(ROOT/'terminal/before/OUTPUT_PINS.json')
    prep_seal = load(ROOT/'terminal/before/PREPARATION_SEAL.json')
    require(len(prep_pins['entries']) == 123
            and prep_seal['output_pins_sha256'] == identity(ROOT/'terminal/before/OUTPUT_PINS.json')['sha256'],
            'dated preparation pin/seal identity')
    require([{k:r[k] for k in ('path','bytes','sha256')} for r in resolution]
            == prep_pins['entries'], 'preparation resolution exact original identities')
    old_manifest = load(ROOT/'terminal/before/MANIFEST.json')
    old_binding = load(ROOT/'terminal/before/DEPOSIT_BINDING.json')
    require(old_binding['artifacts']['pr1098_support_v1_0.zip'] == current['reviewed_preterminal_support_archive'],
            'before binding reviewed archive')
    omitted = []
    local_omissions = []
    old_portable = {r['path'] for r in old_manifest['entries']}
    for row in resolution:
        if row['disposition'] == 'KNOWN_OLD_ZIP_OMITTED':
            require(row['path'] == 'pr1098_support_v1_0.zip' and bool(row['reason'])
                    and {k:row[k] for k in ('bytes','sha256')}
                    == current['reviewed_preterminal_support_archive'], 'known omitted old ZIP identity')
            omitted.append(row['path'])
        elif row['disposition'] == 'UNCHANGED_LOCAL_PREPARATION_OUTPUT_OMITTED':
            require(row['path'] not in old_portable
                    and row['path'] not in ('paper.pdf','pr1098_support_v1_0.zip','MANIFEST.json','DEPOSIT_BINDING.json')
                    and bool(row['reason']) and 'resolved_path' not in row,
                    'individual local preparation omission')
            local_omissions.append(row['path'])
        else:
            require(row['disposition'] in ('EXACT_BEFORE_INTERFACE','UNCHANGED_CURRENT_BYTES'),
                    'preparation resolution disposition')
            require(identity(member(row['resolved_path'])) == {k:row[k] for k in ('bytes','sha256')},
                    'preparation before/current pin: '+row['path'])
    require(omitted == ['pr1098_support_v1_0.zip'], 'only obsolete archive omitted')
    require(len(local_omissions) == 18, '18 unchanged local preparation outputs omitted')
    require(old_manifest['schema_version'] == 1, 'dated before manifest schema')
    return {'whole_reviews_completed':2, 'minimum_whole_reviews':2,
            'latest_zero_actionable_ROOT_adopted':True,
            'ROOT_final_terminal_integrity':'REQUIRED_UNADOPTED',
            'publication_ready':False, 'issues_resolved':False, 'published':False,
            'services_held_after_pr':1032}

def verify():
    for path in ('metadata.json', 'zenodo-api.json', 'publication/zenodo-deposit.json'):
        j = load(ROOT/path)
        obj = j if path == 'metadata.json' else j['metadata']
        require(obj == EXPECTED_METADATA, 'native metadata mismatch: '+path)
    native = load(ROOT/'publication/zenodo-deposit.json')
    require(set(native) == {'metadata','files'}, 'native upload root fields')
    require(native['files'] == [
        {'path':'../paper.pdf','name':'paper.pdf'},
        {'path':'../pr1098_support_v1_0.zip','name':'pr1098_support_v1_0.zip'}],
        'native exact file selections')
    require(set(load(ROOT/'zenodo-api.json')) == {'metadata'}, 'API metadata wrapper')
    manifest = load(ROOT/'MANIFEST.json')
    require(manifest['schema_version'] == 1, 'manifest schema')
    archive = archive_bytes()
    bindings = load(ROOT/'ARTIFACT_BINDINGS.json')  # Required, even in an extraction.
    require(set(bindings) == {'paper.pdf'}, 'external PDF binding names')
    for name, expected in bindings.items():
        raw = regular(ROOT/name).read_bytes()
        require(expected == {'bytes':len(raw),'sha256':digest(raw)}, 'artifact binding: '+name)
    require(archive == regular(ROOT/'pr1098_support_v1_0.zip').read_bytes(),
            'current archive does not equal closed deterministic reconstruction')
    require(regular(ROOT/'paper.pdf').read_bytes().startswith(b'%PDF-'), 'PDF header')
    current = terminal_state()
    return {'status':'PASS','payload_members':len(manifest['entries']),
            'strict_present_required_bindings':True,'metadata_objects_exact':True,
            'archive_bytes':len(archive),'archive_sha256':digest(archive),
            'terminal_workflow':current}

if __name__ == '__main__':
    require(not sys.argv[1:], 'stdout verifier accepts no output argument')
    print(json.dumps(verify(), sort_keys=True, indent=2))
