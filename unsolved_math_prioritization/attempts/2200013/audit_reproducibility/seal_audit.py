#!/usr/bin/env python3
"""Seal authored audit outputs; does not change the original or corrected slice."""
import hashlib
import json
import re
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(path,data):
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')


def need(condition,label):
    if not condition:
        raise RuntimeError(label)


root=Path(__file__).resolve().parent
report=json.loads((root/'CONTROL_REPORT.json').read_text())
pins=json.loads((root/'EXTERNAL_PINS.json').read_text())
need(report['all_passed'] and report['control_count']==report['passed_count']==687,'complete controls required')
need(report['original_preserved'] and report['proof_bytes_unchanged'],'freeze preservation required')
need(report['uid']!=0 and report['euid']!=0,'actual nonroot evidence required')
for path,entry in pins['corrected'].items():
    data=(root/'corrected'/path).read_bytes()
    need(len(data)==entry['bytes'] and digest(data)==entry['sha256'],'corrected external pin mismatch')
manifest=json.loads((root/'corrected/verification/MANIFEST.json').read_text())
for entry in manifest['files']:
    data=(root/'corrected/public'/entry['path']).read_bytes()
    need(len(data)==entry['bytes'] and digest(data)==entry['sha256'],'corrected public manifest mismatch')
acceptance={'schema':'independent-tropical-acceptance-v1','audit_date_utc':'2026-10-08',
            'problem_id':2200013,'problem_number':'AMR-021-0013','rank':1031,
            'mathematical_verdict':'ACCEPTED','corrected_verifier_verdict':'ACCEPTED',
            'classification':'LITERATURE_DERIVED_NEGATIVE_RESOLUTION_WITH_EXPLICIT_RECONSTRUCTION',
            'original_frozen_certificate_mathematically_valid':True,
            'original_standalone_parser_had_exact_type_weakness':True,
            'original_preserved':True,'proof_bytes_unchanged':True,
            'corrected_public_files_changed':['verify_math.py'],
            'control_count':687,'passed_count':687,'modes':['normal','O','OO'],
            'controls_per_mode':229,'overflow_literal_rejection_controls':78,
            'actual_uid':report['uid'],'actual_euid':report['euid'],
            'distinct_negative_roots_at_least':4,'distinct_binomial_weighted_corners':3,
            'all_coefficients_strictly_positive':True,'actual_degree':'200000000000000000100',
            'independent_integer_reconstruction':True,'direct_binomial_ratio_checks':99,
            'direct_power_form_chord_checks':17,'conventional_slope_multiplicity_target':False,
            'novelty_claim':False,'minimal_degree_claim':False,'exact_total_root_claim':False,
            'third_party_sources_or_dataset_contents_in_release':False,
            'publication_performed':False,'queue_changes_performed':False,
            'external_pins':pins}
write(root/'ACCEPTANCE.json',acceptance)
base={'AUDIT.md','ACCEPTANCE.json','CONTROL_REPORT.json','EXTERNAL_PINS.json','INDEPENDENT_MATH.json',
      'PARSER_HARDENING.patch','SOURCE_METADATA.json','independent_math.py','run_audit.py','seal_audit.py',
      'RELEASE_ALLOWLIST.json','AUDIT_MANIFEST.json'}
base.update('corrected/public/'+entry['path'] for entry in manifest['files'])
base.update({'corrected/verification/MANIFEST.json','corrected/verification/bootstrap.py'})
write(root/'RELEASE_ALLOWLIST.json',{'schema':'source-free-audit-allowlist-v1','paths':sorted(base)})
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
need(actual-{'AUDIT_MANIFEST.json'}==base-{'AUDIT_MANIFEST.json'},'unexpected or missing audit files')
for path in sorted(base-{'AUDIT_MANIFEST.json'}):
    data=(root/path).read_bytes()
    private_path = re.search(rb'(?:/(?:workspace|root)/|private_sources/|codex://|sediment://)[A-Za-z0-9_]',data)
    need(private_path is None,'private-location marker in '+path)
entries=[{'path':path,'bytes':len((root/path).read_bytes()),'sha256':digest((root/path).read_bytes())}
         for path in sorted(base-{'AUDIT_MANIFEST.json'})]
write(root/'AUDIT_MANIFEST.json',{'schema':'independent-source-free-audit-manifest-v1',
                                 'self_excluded_for_external_pinning':True,'file_count':len(entries),'files':entries})
print(json.dumps({'status':'PASS','allowlist_file_count':len(base),'sealed_file_count':len(entries),
                  'audit_manifest_sha256':digest((root/'AUDIT_MANIFEST.json').read_bytes()),
                  'audit_manifest_bytes':(root/'AUDIT_MANIFEST.json').stat().st_size,
                  'audit_sha256':digest((root/'AUDIT.md').read_bytes()),
                  'controls_sha256':digest((root/'CONTROL_REPORT.json').read_bytes()),
                  'acceptance_sha256':digest((root/'ACCEPTANCE.json').read_bytes())},sort_keys=True))
