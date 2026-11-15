#!/usr/bin/env python3
"""Read-only analytic118 closure; no network, source replay or file writes."""
from pathlib import Path, PurePosixPath
from hashlib import sha256, md5
from datetime import datetime, timezone
import json
import stat
import sys
import zipfile
import zlib

P=Path(__file__).resolve().parent
B=P.parents[1]
READY='398351e05ac4ddc92510ea191c109dd22a48a177869872a8008ff2f8328581e5'
INITIAL='ac63cdfcc9d13624dca31210346884feb55b9fee5ca1c1edfe76da5256d59c57'
EXCLUDE={'OWNED_MANIFEST.json','CLOSURE.json','SEAL.json'}


def need(ok,label):
    if not ok:raise ValueError(label)


def h(body):return sha256(body).hexdigest()


def read(path):return json.loads(path.read_bytes())


def blob(body,size,expected):
    need(len(body)==size and h(body)==expected,'whole byte count/SHA256')


def safe_names(names):
    seen=set()
    for name in names:
        q=PurePosixPath(name)
        need(not q.is_absolute() and '..' not in q.parts and '\\' not in name
             and ':' not in name and q.parts,'unsafe archive path')
        need(name.casefold() not in seen,'duplicate archive name')
        seen.add(name.casefold())


def execution(rec):
    need(rec['exit_code']==0,'execution failed')
    need(rec['command'][1:3]==['-E','-B'],'execution isolation flags')
    need(rec['timeout_seconds']==30,'execution bound')


def reject(label,function):
    try:function()
    except ValueError:return label
    raise ValueError('negative custody control escaped: '+label)


def main():
    args=sys.argv[1:]
    need(args in ([],['--preseal'],['--inputs-only']),'unsupported arguments')
    source=B/'sources'
    need(h((source/'SOURCE_READY.json').read_bytes())==READY,'frozen SOURCE_READY')
    ready=read(source/'SOURCE_READY.json')
    need(ready['record_id']==23385145 and ready['version']=='1.0' and
         ready['publication_date']=='2026-10-14' and
         ready['created'].startswith('2026-10-15'),'native target/date/version')
    need(ready['target_manuscript_scientifically_read'] is False and
         ready['source_programs_executed_or_scientifically_read'] is False,
         'historical acquisition flags normalized')
    frozen=read(P/'INPUT_MANIFEST.json')['all_original_source_files'];paths=set()
    for entry in frozen:
        q=B/entry['path'];need(q.is_file() and not q.is_symlink(),'source regular file')
        blob(q.read_bytes(),entry['bytes'],entry['SHA256']);paths.add(entry['path'])
    need(paths=={str(q.relative_to(B)) for q in source.rglob('*') if q.is_file()}
         and len(paths)==124,'whole original source membership')
    assets=ready['all_assets_in_original_order']
    need([x['original_api_file_object']['key'] for x in assets]==
         ['weighted_centers.pdf','verification_package.zip'],'native asset order')
    for asset in assets:
        body=Path(asset['path']).read_bytes();blob(body,asset['bytes'],asset['sha256'])
        need('md5:'+md5(body).hexdigest()==asset['original_api_file_object']['checksum'],
             'native asset MD5')
    archive=read(Path(ready['whole_archive_custody_path']))
    stored=archive['all_safe_regular_occurrences'];total=0
    with zipfile.ZipFile(Path(assets[1]['path'])) as z:
        members=z.infolist();safe_names([m.filename for m in members])
        need(len(members)==len(stored)==93,'whole ZIP inventory')
        for ordinal,(m,entry) in enumerate(zip(members,stored)):
            need(not m.is_dir() and not m.flag_bits&1 and
                 stat.S_IFMT(m.external_attr>>16) in (0,stat.S_IFREG),'ZIP regular body')
            body=z.read(m)
            blob(body,entry['bytes'],entry['SHA256'])
            need(m.filename==entry['original_member_name'] and
                 ordinal==entry['ordinal_zero_based'] and
                 zlib.crc32(body)&0xffffffff==m.CRC and
                 '%08x'%m.CRC==entry['CRC32'],'native ZIP ordinal/name/CRC')
            need(Path(entry['extracted_path']).read_bytes()==body,'complete extraction identity')
            total+=len(body)
    need(total==705178 and archive['nested_archives']==0,'whole expanded package')
    need(h((P/'INITIAL_SEAL.json').read_bytes())==INITIAL,'early initial seal changed')
    initial=read(P/'INITIAL_SEAL.json')
    need(h((P/'INITIAL_MANIFEST.json').read_bytes())==initial['INITIAL_MANIFEST_SHA256'],
         'early manifest')
    initial_files=read(P/'INITIAL_MANIFEST.json')['files']
    for entry in initial_files:
        q=Path(entry['path']);need(q.is_relative_to(P),'initial payload outside lane')
        blob(q.read_bytes(),entry['bytes'],entry['SHA256'])
    need(len(initial_files)==10 and initial['acquisition_exposure_honestly_recorded'] is True
         and initial['before_foreign_code_results_triage_archived_current_peer_findings'] is True,
         'early exposure/independence contract')
    primary_count=pdf_count=0
    for name in ['PRIMARY_FETCH_01.json','PRIMARY_FETCH_02.json']:
        for rec in read(P/name):
            q=Path(rec['path']);need(q.is_relative_to(P),'primary outside lane')
            body=q.read_bytes();blob(body,rec['bytes'],rec['SHA256'])
            need(isinstance(rec['headers_in_received_order'],list),'ordered primary headers')
            if rec['PDF_magic']:
                need(body.startswith(b'%PDF-') and rec['HTTP_status']==200,'actual primary PDF')
                pdf_count+=1
            else:need(rec['HTTP_status'] in (200,403),'primary HTML transport status')
            primary_count+=1
    need(primary_count==9 and pdf_count==6,'whole primary bodies')
    pixels=read(P/'PRIMARY_RENDER_RECEIPTS.json')
    for rec in pixels:
        need(rec['exit_code']==0 and h(Path(rec['image_path']).read_bytes())==
             rec['image_SHA256'],'actual primary image binding')
    need(len(pixels)==10,'primary selected image count')
    calls=read(P/'EXACT_RUN_RECEIPTS.json')
    need([r['name'] for r in calls['executions']]==['own-exact','native-subset'],
         'bounded execution identities')
    for rec in calls['executions']:
        execution(rec);script=Path(rec['command'][-1])
        need(script.is_relative_to(P) and h(script.read_bytes())==rec['script_SHA256'],
             'actual script binding')
        for stream in ['stdout','stderr']:
            q=Path(rec[stream+'_path']);need(q.is_relative_to(P),'stream outside lane')
            need(h(q.read_bytes())==rec[stream+'_SHA256'],'actual stream binding')
        need(Path(rec['stderr_path']).read_bytes()==b'','unexpected stderr')
    native=calls['native_byte_identity']
    need(Path(native['original_path']).read_bytes()==Path(native['isolated_copy_path']).read_bytes()
         and h(Path(native['isolated_copy_path']).read_bytes())==native['SHA256'],
         'isolated native byte identity')
    own=read(P/'own-exact.stdout.json');bounded=read(P/'native-subset.stdout.json')
    need(own['verdict']=='PASS' and own['exact_counts']['exact_profiles']==10004 and
         own['exact_counts']['search_progress_invariants']==33394 and
         own['exact_counts']['exact_recursion_parameter_cases']==4103 and
         own['source_imports']==[] and own['writes']==[],'own exact result contract')
    need(own['compressed_exact_countermodel']['duplicated_slice_volume']==1022147483646
         and own['compressed_exact_countermodel']['corrected_algorithm_refuted'] is False,
         'countermodel affects literal source estimate, not target')
    need(bounded['verdict']=='PASS' and bounded['functions_called']==
         ['source_branch_controls','log_base_counterexample'] and
         bounded['source_branch_controls']['explicit_profiles']==17 and
         bounded['exact_counts']['morse_calls']==105 and
         bounded['not_called']==['all_small','main','run_all.py'],'bounded native subset')
    verdict=read(P/'VERDICT.json')
    need(verdict['literal_verdict']=='SUPPORTED_FULL_ORIGINAL_THEOREM' and
         verdict['full_original_quantified_claim_supported'] is True and
         verdict['narrowed_or_repaired_target_theorem_substituted'] is False and
         verdict['remaining_in_scope_mathematical_gap'] is None,'full theorem disposition')
    need(verdict['scientific_findings_sent_to_root'] is False and
         verdict['publication_authorized'] is False,'historical delivery/authority')
    negative=[reject('corrupt SHA',lambda:blob(b'x',1,h(b'y'))),
      reject('wrong size',lambda:blob(b'x',2,h(b'x'))),
      reject('archive traversal',lambda:safe_names(['../x'])),
      reject('archive case collision',lambda:safe_names(['A','a'])),
      reject('false successful run',lambda:execution({'exit_code':1,'command':['py','-E','-B'],'timeout_seconds':30})),
      reject('missing isolation flags',lambda:execution({'exit_code':0,'command':['py','-O'],'timeout_seconds':30}))]
    owned_count=None
    if args!=['--inputs-only']:
        manifest=read(P/'OWNED_MANIFEST.json');owned=set()
        for rec in manifest['files']:
            q=P/rec['path'];need(q.is_relative_to(P) and not q.is_symlink(),'owned regular path')
            blob(q.read_bytes(),rec['bytes'],rec['SHA256']);owned.add(rec['path'])
        actual={str(q.relative_to(P)) for q in P.rglob('*') if q.is_file()
                and str(q.relative_to(P)) not in EXCLUDE}
        need(actual==owned,'unmanifested/missing owned artifact');owned_count=len(owned)
    if not args:
        seal=read(P/'SEAL.json')
        for name,field in [('OWNED_MANIFEST.json','OWNED_MANIFEST_SHA256'),
          ('CLOSURE.json','CLOSURE_SHA256'),('REPORT.md','REPORT_SHA256'),
          ('VERDICT.json','VERDICT_SHA256'),('DERIVATION.md','DERIVATION_SHA256')]:
            need(h((P/name).read_bytes())==seal[field],'terminal binding '+name)
        need(seal['INITIAL_SEAL_SHA256']==INITIAL and seal['SOURCE_READY_SHA256']==READY
             and seal['completion_estimate_percent_bounded_review']==100,'terminal provenance')
        closure=read(P/'CLOSURE.json')
        need(closure['exit_code']==0 and closure['result']['verdict']=='PASS' and
             closure['verifier_SHA256']==h(Path(__file__).read_bytes()) and
             closure['stdout_SHA256']==h(closure['stdout'].encode()) and
             closure['stderr']=='' and json.loads(closure['stdout'])==closure['result'],
             'captured actual preseal closure')
    print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'verdict':'PASS',
      'mode':args[0] if args else 'terminal-read-only','original_source_files':len(frozen),
      'whole_ZIP_payloads':len(stored),'whole_ZIP_expanded_bytes':total,
      'initial_payloads':len(initial_files),'whole_primary_PDFs':pdf_count,
      'whole_primary_transports':primary_count,'selected_primary_rasters':len(pixels),
      'owned_manifest_payloads':owned_count,'custody_negative_controls_rejected':negative,
      'programs_replayed':[],'network_requests':[],'writes':[]},indent=2))


if __name__=='__main__':main()
