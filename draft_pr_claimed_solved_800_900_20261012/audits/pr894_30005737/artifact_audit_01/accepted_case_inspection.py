#!/usr/bin/env python3
"""Inspect each accepted false case, pin its actual mutated input, and rerun it.
Reuse only already reviewed harness function definitions, never its top-level run.
"""
import ast, base64, collections, copy, datetime, hashlib, importlib.util, io, json, os
from pathlib import Path
import shutil, struct, subprocess, sys, zipfile
BASE=Path(__file__).resolve().parent;PARENT=BASE.parent;TMP=BASE/'private_tmp';PACKET=TMP/'packet';RUNS=TMP/'runs'
PYTHON=sys.executable;ENV={'PATH':'/opt/homebrew/bin:/usr/bin:/bin','TMPDIR':str(TMP),'LC_ALL':'C','LANG':'C'}
RECEIPTS=[];OBS=[]
tree=ast.parse((BASE/'audit_runner.py').read_text())
# Function definitions are part of the public audit source, read in full before execution.
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'audit_runner_functions','exec'))
mb=(PARENT/'SOURCE_MANIFEST.json').read_bytes()
require(sha(mb)=='1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c','External manifest mismatch')
sm=json.loads(mb);ORIGINAL={e['path']:(PARENT/'source'/e['path']).read_bytes() for e in sm['files']}
for e in sm['files']:require(sha(ORIGINAL[e['path']])==e['sha256'],'Source mismatch')
ZINFOS=zipfile.ZipFile(io.BytesIO(ORIGINAL['AUTHOR_CANDIDATE.zip'])).infolist()
frozen=ORIGINAL['authored/CHECK_RESULTS.json']
INSPECT=[]

def inventory():
    rows=[]
    for f in sorted(PACKET.rglob('*')):
        name=str(f.relative_to(PACKET));s=f.lstat()
        if f.is_symlink():
            rows.append({'path':name,'type':'symlink','target':os.path.relpath(os.readlink(f),BASE),'target_exists':f.exists(),'read_bytes_sha256':sha(f.read_bytes()) if f.is_file() else None})
        elif f.is_file():rows.append({'path':name,'type':'regular','bytes':s.st_size,'sha256':sha(f.read_bytes())})
        else:rows.append({'path':name,'type':'directory'})
    return rows

def inspect_case(label,fn):
    reset();fn();before=inventory()
    changed=[r for r in before if r['path'] in ORIGINAL and r['type']=='regular' and r.get('sha256')!=sha(ORIGINAL[r['path']])]
    # Also capture unusual added files/symlinks and exact decoded semantics.
    row={'label':label,'input_inventory':before,'changed_original_files':changed,
         'publication_manifest_sha256':sha((PACKET/'PUBLICATION_MANIFEST.json').read_bytes())}
    if label=='wrong_metadata':
        m=json.loads((PACKET/'PUBLICATION_MANIFEST.json').read_bytes());row['inspected']={k:m[k] for k in ['problem_id','rank','status','turns','original_archive_contains_audits']}
    elif label=='duplicate_json_key':
        pairs=json.loads((PACKET/'PUBLICATION_MANIFEST.json').read_bytes(),object_pairs_hook=list)
        row['inspected']={'top_level_key_occurrences':dict(collections.Counter(k for k,v in pairs)),'first_files_value':pairs[0][1],'raw_prefix':(PACKET/'PUBLICATION_MANIFEST.json').read_text()[:80],'effective_problem_id':json.loads((PACKET/'PUBLICATION_MANIFEST.json').read_bytes())['problem_id']}
    elif label=='nonbytecode_cache_file':row['inspected']={'ignored_path':'__pycache__/not_bytecode.txt','content':(PACKET/'__pycache__/not_bytecode.txt').read_text()}
    elif label=='external_symlink':row['inspected']={'path':'authored/PROOF.md','is_symlink':(PACKET/'authored/PROOF.md').is_symlink(),'resolves_outside_packet':not (PACKET/'authored/PROOF.md').resolve().is_relative_to(PACKET),'bytes_match_original':(PACKET/'authored/PROOF.md').read_bytes()==ORIGINAL['authored/PROOF.md']}
    elif label=='dangling_symlink':row['inspected']={'path':'DANGLING','is_symlink':(PACKET/'DANGLING').is_symlink(),'exists':(PACKET/'DANGLING').exists()}
    elif label=='zip_symlink_metadata':
        z=zipfile.ZipFile(PACKET/'AUTHOR_CANDIDATE.zip');i=z.infolist()[0];row['inspected']={'member':i.filename,'Unix_mode_octal':oct(i.external_attr>>16),'payload_is_original_file_text':z.read(i)==ORIGINAL['authored/'+i.filename]}
    elif label=='zip_comment_trailer':
        z=zipfile.ZipFile(PACKET/'AUTHOR_CANDIDATE.zip');row['inspected']={'archive_comment':z.comment.decode(),'trailer':'nonzip trailing bytes','trailer_verified':(PACKET/'AUTHOR_CANDIDATE.zip').read_bytes().endswith(b'nonzip trailing bytes'),'member_payloads_all_original':all(z.read(i)==ORIGINAL['authored/'+i.filename] for i in z.infolist())}
    elif label=='original_manifest_duplicate':
        m=json.loads((PACKET/'authored/MANIFEST.json').read_bytes());names=[e['path'] for e in m['files']];row['inspected']={'entry_count':len(names),'unique_names':len(set(names)),'name_counts':dict(collections.Counter(names))}
    elif label=='original_manifest_traversal':
        m=json.loads((PACKET/'authored/MANIFEST.json').read_bytes());z=zipfile.ZipFile(PACKET/'AUTHOR_CANDIDATE.zip');n='../authored/PROOF.md';row['inspected']={'path':n,'listed_in_original_manifest':any(e['path']==n for e in m['files']),'listed_in_zip':n in z.namelist(),'read_bytes_original':(PACKET/'authored'/n).read_bytes()==ORIGINAL['authored/PROOF.md'],'zip_bytes_original':z.read(n)==ORIGINAL['authored/PROOF.md']}
    elif label=='false_proof_rehashed':row['inspected']={'false_proof_complete_text':(PACKET/'authored/PROOF.md').read_text(),'note':'Explicitly false: one-dimensional abelian complex Lie algebra is not semisimple.'}
    elif label=='checker_stub_rehashed':row['inspected']={'stub_complete_source':(PACKET/'authored/check_algebra.py').read_text(),'original_checker_unchanged':False,'checker_only_prints_frozen_bytes':True}
    elif label=='hostile_sitecustomize':row['inspected']={'all_original_files_byte_preserved':all((PACKET/n).read_bytes()==b for n,b in ORIGINAL.items()),'startup_hook_source':(TMP/'spoof_site/sitecustomize.py').read_text(),'child_exits_before_original_checker':True}
    journal(BASE/'ACCEPTED_CASE_INPUTS.jsonl',row)
    env={'PYTHONPATH':str(TMP/'spoof_site'),'PYTHONDONTWRITEBYTECODE':'1'} if label=='hostile_sitecustomize' else None
    p=run('inspect_accepted_'+label,['-I','-S','-B','verify_publication.py'],extra_env=env)
    observed=observe('inspect_accepted_'+label,p,'accept','Actual pre-run input inventory and explicit content inspection in ACCEPTED_CASE_INPUTS.jsonl')
    require(p.returncode==0 and p.stdout==expected_verifier,'Accepted input replay differs')
    after=inventory();require(before==after,'Verifier unexpectedly mutated test packet')
    row['returncode']=p.returncode;row['verifier_stdout_sha256']=sha(p.stdout);row['input_unchanged_after_verifier']=True;INSPECT.append(row)

expected_verifier=(RUNS/'verifier_normal.stdout').read_bytes()
for label,fn in [('wrong_metadata',pub_metadata),('duplicate_json_key',duplicate_json_key),('nonbytecode_cache_file',cache_payload),('external_symlink',symlink_proof),('dangling_symlink',dangling_symlink),('zip_symlink_metadata',zip_symlink_mode),('zip_comment_trailer',zip_extra_metadata),('original_manifest_duplicate',original_duplicate),('original_manifest_traversal',original_traversal),('false_proof_rehashed',false_proof),('checker_stub_rehashed',checker_stub),('hostile_sitecustomize',lambda:None)]:
    inspect_case(label,fn)

# Unresolved layer coverage: distinguish original-freeze, parser, and literal-boolean checks.
def original_freeze_mismatch():hash_tamper();publication_refresh()
def original_count_bad():
    m=json.loads((PACKET/'authored/MANIFEST.json').read_bytes());m['files'].pop();write_json(PACKET/'authored/MANIFEST.json',m);publication_refresh()
def original_bad_json(): (PACKET/'authored/MANIFEST.json').write_bytes(b'{bad');publication_refresh()
def stub_control_value(value):
    report=json.loads(frozen);report['invalid_R_identity_detected']=value;b=(json.dumps(report,indent=2,sort_keys=True)+'\n').encode();(PACKET/'authored/CHECK_RESULTS.json').write_bytes(b);(PACKET/'authored/check_algebra.py').write_bytes(b'import sys\nsys.stdout.buffer.write('+repr(b).encode()+b')\n');author_refresh()
for label,fn in [('original_freeze_mismatch',original_freeze_mismatch),('original_unique_count_bad',original_count_bad),('original_manifest_bad_json',original_bad_json),('stub_control_false',lambda:stub_control_value(False)),('stub_control_integer_one',lambda:stub_control_value(1))]:
    case('layer_'+label,fn,'reject','Exercises a previously unisolated validation layer')
reset()
write_json(BASE/'ACCEPTED_CASE_INSPECTION.json',{'timestamp_utc':now(),'all_12_accepted_cases_explicitly_inspected_and_reexecuted':len(INSPECT)==12,'cases':[{'label':x['label'],'inspected':x['inspected'],'returncode':x['returncode'],'verifier_stdout_sha256':x['verifier_stdout_sha256'],'input_unchanged_after_verifier':x['input_unchanged_after_verifier']} for x in INSPECT],'supplemental_processes':len(RECEIPTS),'original_source_preserved':all((PARENT/'source'/n).read_bytes()==b for n,b in ORIGINAL.items())})
log('Explicitly inspected and pinned actual inputs for all 12 accepted false cases, reran each, and verified no verifier-induced input mutation. Added five isolated original-freeze/parser/boolean controls; all rejected. Final private packet restored exactly.',95)
print(json.dumps({'inspected_accepted_cases':len(INSPECT),'supplemental_processes':len(RECEIPTS)},sort_keys=True))
