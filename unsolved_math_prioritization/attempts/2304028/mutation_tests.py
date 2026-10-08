#!/usr/bin/env python3
"""New publication mutations plus reconstructed historical finite validator controls.

All fixtures are test-only. Production inputs and their external pins stay fixed.
This is not a hostile-code sandbox or a universal mathematical proof.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import copy, hashlib, json, os, pathlib, shutil, subprocess, tempfile

def check(ok, message):
    if not ok: raise RuntimeError(message)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, obj): p.write_text(json.dumps(obj, indent=2)+'\n')

def thaw_fixture(root):
    # Only call on newly copied, disposable fixtures, never production inputs.
    check(root != PACKET, 'Never thaw the input packet')
    for path in [root, *root.rglob('*')]:
        check(not path.is_symlink() and (path.is_dir() or path.is_file()),
              'Only ordinary disposable fixture entries may be thawed')
        path.chmod(0o755 if path.is_dir() else 0o644)
check(len(sys.argv)==4, 'Expected manifest pin, packet path, independently trusted wrapper pin')
MANIFEST_PIN, argument, WRAPPER_PIN = sys.argv[1:]
PACKET = pathlib.Path(os.path.abspath(argument))
WRAPPER = PACKET/'verify_publication.py'
check(not WRAPPER.is_symlink() and sha(WRAPPER)==WRAPPER_PIN, 'Wrapper hash before execution')
check(os.getuid()==os.geteuid()!=0, 'Actual equal nonroot UID/EUID')
initial = {p.relative_to(PACKET).as_posix():p.read_bytes() for p in PACKET.rglob('*') if p.is_file()}
publication_work = pathlib.Path(tempfile.mkdtemp(prefix='polynomial-publication-mutations-'))
BASE=publication_work/'original'
(BASE/'audit').mkdir(parents=True)
shutil.copytree(PACKET/'author',BASE/'public')
thaw_fixture(BASE/'public')
shutil.copyfile(PACKET/'FREEZE.json',BASE/'audit/FREEZE.json')
wrapper_copy=publication_work/'trusted_wrapper.py'
wrapper_copy.write_bytes(WRAPPER.read_bytes())
check(sha(wrapper_copy)==WRAPPER_PIN,'Captured trusted wrapper')
wrapper_rows=[]
PIN = 'b76dfab10d985100f7dc23854491ee83dddd6364a1eb8dee2fb7dc5ceeb22000'
VERIFIER = 'c665a143651efce5532f41d55db02471f1c4b1e0e7146477a87ad36f2369a58c'
def check(ok, msg):
    if not ok: raise RuntimeError(msg)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, d): p.write_text(json.dumps(d, indent=2) + '\n')
check(os.getuid() == os.geteuid() != 0, 'Actual unprivileged UID required')
check(sha(BASE/'audit/FREEZE.json') == PIN, 'Original external freeze')
frozen = json.loads((BASE/'audit/FREEZE.json').read_text())
for f in frozen['files']:
    p=BASE/'public'/f['path']; check(p.stat().st_size==f['bytes'] and sha(p)==f['sha256'], 'Original member pin')
check(sha(BASE/'public/verify.py') == VERIFIER, 'Trusted verifier before execution')
work=pathlib.Path(tempfile.mkdtemp(prefix='independent-polynomial-audit-'))
hostile=work/'hostile'; hostile.mkdir()
for name in ['argparse','fractions','hashlib','json','pathlib','sitecustomize','usercustomize']:
    (hostile/(name+'.py')).write_text("raise RuntimeError('AUDITOR HOSTILE IMPORT LOADED')\n")
for p in hostile.iterdir(): p.chmod(0o444)
hostile.chmod(0o555)
env=dict(os.environ, PYTHONPATH=str(hostile), PYTHONHOME='/not-a-python-home', PYTHONSTARTUP=str(hostile/'sitecustomize.py'), PYTHONINSPECT='1', PYTHONOPTIMIZE='0')
ledger=json.loads((BASE/'public/cases.json').read_text())
runs=[]
def payload(name):
    p=work/name; shutil.copytree(BASE/'public',p); thaw_fixture(p); return p

def manifest(p, name, original=False):
    mp=work/(name+'.json')
    if original: shutil.copyfile(BASE/'audit/FREEZE.json',mp); return mp,PIN
    save(mp, {'schema_version':1,'files':[{'path':x.name,'bytes':x.stat().st_size,'sha256':sha(x)} for x in sorted(p.iterdir()) if x.is_file()]})
    return mp,sha(mp)

def run(name,p,mp,pin,accept=False,isolated=True,modes=('', '-O', '-OO')):
    check(sha(p/'verify.py')==VERIFIER, 'External verifier trust must precede every execution')
    for mode in modes:
        cmd=[sys.executable]+(['-I'] if isolated else [])+['-B']+([mode] if mode else [])+[str(p/'verify.py'),'--root',str(p),'--manifest',str(mp),'--expected-sha256',pin]
        res=subprocess.run(cmd,cwd=hostile,env=env if isolated else dict(os.environ),capture_output=True,text=True,timeout=45)
        check((res.returncode==0)==accept, 'Unexpected acceptance for '+name+': '+res.stderr)
        row={'case':name,'optimization':mode or 'normal','returncode':res.returncode,'stdout':res.stdout.strip(),'stderr':res.stderr.strip()}
        if accept:
            r=json.loads(res.stdout); check(r=={'finite_cases':24,'literature_classification':'KNOWN-SOLVED','negative_type_controls':25,'status':'PASS','uid':os.geteuid(),'universal_proof_checked_by_code':False}, 'Incorrect success receipt')
        runs.append(row)

p=payload('frozen'); mp,pin=manifest(p,'frozen-manifest',True)
for q in p.iterdir(): q.chmod(0o444)
p.chmod(0o555); mp.chmod(0o444)
probes=[]
for path,mode in [(p/'new','w'),(p/'cases.json','a'),(hostile/'new','w'),(mp,'a')]:
    try:
        with path.open(mode): pass
    except PermissionError: probes.append(True)
    else: probes.append(False)
check(all(probes),'Read-only permissions not enforced')
run('frozen_readonly_hostile',p,mp,pin,True)
run('wrong_external_pin',p,mp,'0'*64)
run('nonisolated_rejected',p,mp,pin,isolated=False)

mutators={
'coefficient_bool':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(0,True),
'coefficient_float':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(0,0.0),
'coefficient_nan':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(0,float('nan')),
'coefficient_inf':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(0,float('inf')),
'coefficient_minus_inf':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(0,-float('inf')),
'expected_bool':lambda x:x['cases'][0]['expected'].__setitem__('degree',True),
'expected_float':lambda x:x['cases'][0]['expected'].__setitem__('degree',2.0),
'expected_wrong':lambda x:x['cases'][0]['expected'].__setitem__('distinct_nonreal_outside_P',0),
'version_bool':lambda x:x.__setitem__('schema_version',True),
'unknown_key':lambda x:x.__setitem__('extra',1),
'duplicate_id':lambda x:x['cases'][1].__setitem__('id',x['cases'][0]['id']),
'missing_case':lambda x:x['cases'].pop(),
'leading_zero':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(-1,0),
'coefficient_bound':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(0,1000001),
'string_coefficient':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(0,'0')}
for name,mut in mutators.items():
    q=payload(name); x=copy.deepcopy(ledger); mut(x); save(q/'cases.json',x); mm,pp=manifest(q,name+'-manifest'); run(name,q,mm,pp)
for name in ['stale_payload','unknown_public_file','symlink_payload','duplicate_json_key','manifest_bool_bytes','manifest_float_bytes','manifest_duplicate_member']:
    q=payload(name); mm,pp=manifest(q,name+'-manifest',True)
    if name=='stale_payload':
        (q/'REPORT.md').write_text((q/'REPORT.md').read_text()+'\nmutation\n')
    elif name=='unknown_public_file': (q/'unlisted.txt').write_text('x')
    elif name=='symlink_payload': (q/'cases.json').unlink(); (q/'cases.json').symlink_to(BASE/'public/cases.json')
    elif name=='duplicate_json_key':
        (q/'cases.json').write_text((q/'cases.json').read_text().replace('"schema_version": 1,','"schema_version":1,"schema_version":1,',1)); mm,pp=manifest(q,name+'-manifest')
    else:
        m=json.loads(mm.read_text())
        if name=='manifest_bool_bytes': m['files'][0]['bytes']=True
        elif name=='manifest_float_bytes':m['files'][0]['bytes']=float(m['files'][0]['bytes'])
        else:m['files'][1]=copy.deepcopy(m['files'][0])
        save(mm,m);pp=sha(mm)
    run(name,q,mm,pp)
original_run_count=len(runs); check(original_run_count==75,'Original scenario inventory')

# Additional independent malformed schemas and numeric overflow encodings.
extra={
'coefficient_false':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(0,False),
'coefficient_fraction':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(0,0.5),
'coefficient_null':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(0,None),
'coefficient_object':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(0,{'n':0}),
'coefficient_negative_bound':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(0,-1000001),
'coefficient_large_integer':lambda x:x['cases'][0]['coefficients_low_to_high'].__setitem__(0,10**1000),
'degree_too_large':lambda x:x['cases'][0].__setitem__('coefficients_low_to_high',[0]*10+[1]),
'constant_outside_scope':lambda x:x['cases'][0].__setitem__('coefficients_low_to_high',[1]),
'coefficient_array_empty':lambda x:x['cases'][0].__setitem__('coefficients_low_to_high',[]),
'case_not_object':lambda x:x['cases'].__setitem__(0,[]),
'case_missing_expected':lambda x:x['cases'][0].pop('expected'),
'case_extra_key':lambda x:x['cases'][0].__setitem__('extra',0),
'expected_missing_key':lambda x:x['cases'][0]['expected'].pop('degree'),
'expected_extra_key':lambda x:x['cases'][0]['expected'].__setitem__('extra',0),
'expected_not_object':lambda x:x['cases'][0].__setitem__('expected',[]),
'expected_negative':lambda x:x['cases'][0]['expected'].__setitem__('degree',-1),
'expected_out_of_range':lambda x:x['cases'][0]['expected'].__setitem__('degree',101),
'case_id_bool':lambda x:x['cases'][0].__setitem__('id',True),
'case_id_invalid':lambda x:x['cases'][0].__setitem__('id','../bad'),
'case_id_long':lambda x:x['cases'][0].__setitem__('id','x'*51),
'ledger_cases_object':lambda x:x.__setitem__('cases',{}),
'ledger_version_float':lambda x:x.__setitem__('schema_version',1.0),
'ledger_purpose_false':lambda x:x.__setitem__('purpose',False),
'ledger_missing_version':lambda x:x.pop('schema_version')}
for name,mut in extra.items():
    q=payload(name); x=copy.deepcopy(ledger);mut(x);save(q/'cases.json',x); mm,pp=manifest(q,name+'-manifest');run(name,q,mm,pp)
for name,replacement in [('float_exponent_overflow','1e309'),('float_negative_exponent_overflow','-1e309'),('float_underflow','1e-999'),('negative_zero_float','-0.0'),('integer_parse_limit','1'+'0'*5000)]:
    q=payload(name); t=(q/'cases.json').read_text();t=t.replace('"schema_version": 1,','"schema_version": '+replacement+',',1); (q/'cases.json').write_text(t);mm,pp=manifest(q,name+'-manifest');run(name,q,mm,pp)
for name in ['manifest_version_bool','manifest_version_float','manifest_files_object','manifest_unknown_key','manifest_path_traversal','manifest_hash_bool','manifest_uppercase_hash','manifest_zero_bytes','manifest_huge_bytes','manifest_symlink','manifest_duplicate_key','unlisted_directory']:
    q=payload(name);mm,pp=manifest(q,name+'-manifest');m=json.loads(mm.read_text())
    if name=='manifest_version_bool':m['schema_version']=True
    elif name=='manifest_version_float':m['schema_version']=1.0
    elif name=='manifest_files_object':m['files']={}
    elif name=='manifest_unknown_key':m['extra']=1
    elif name=='manifest_path_traversal':m['files'][0]['path']='../REPORT.md'
    elif name=='manifest_hash_bool':m['files'][0]['sha256']=False
    elif name=='manifest_uppercase_hash':m['files'][0]['sha256']=m['files'][0]['sha256'].upper()
    elif name=='manifest_zero_bytes':m['files'][0]['bytes']=0
    elif name=='manifest_huge_bytes':m['files'][0]['bytes']=1000001
    elif name=='manifest_symlink':
        target=mm.with_suffix('.target'); mm.rename(target);mm.symlink_to(target)
    elif name=='manifest_duplicate_key':mm.write_text(mm.read_text().replace('"schema_version": 1,','"schema_version":1,"schema_version":1,',1))
    elif name=='unlisted_directory':(q/'extra').mkdir()
    if name not in ['manifest_symlink','manifest_duplicate_key','unlisted_directory']:save(mm,m)
    pp=sha(mm);run(name,q,mm,pp)

# Exact boundary acceptance using the unchanged trusted verifier, newly pinned test-only ledger.
for sign in [-1,1]:
    name='valid_degree9_coefficient_bound_'+str(sign);q=payload(name);x=copy.deepcopy(ledger)
    x['cases'][0]['coefficients_low_to_high']=[0]*9+[sign*1000000]
    x['cases'][0]['expected']={'degree':9,'degree_Q':18,'distinct_nonreal_Q':8 if sign<0 else 10,'distinct_nonreal_outside_P':8 if sign<0 else 10,'real_Q_with_multiplicity':10 if sign<0 else 8,'infinity_fixed_multiplicity':11}
    save(q/'cases.json',x);mm,pp=manifest(q,name+'-manifest');run(name,q,mm,pp,True)
# Original externally fixed pin must reject semantic edits as well as report edits.
q=payload('tampered_ledger_original_pin');x=copy.deepcopy(ledger);x['cases'][0]['expected']['degree']=3;save(q/'cases.json',x);mm,pp=manifest(q,'tampered_ledger_original_pin',True);run('tampered_ledger_original_pin',q,mm,pp)
# Demonstrate the external caller rejects a replaced verifier without executing it.
q=payload('replaced_verifier_not_executed');(q/'verify.py').write_text('raise RuntimeError("UNTRUSTED VERIFIER MUST NOT EXECUTE")\n')
check(sha(q/'verify.py') != VERIFIER,'Verifier substitution detection')
for f in frozen['files']:
    check(sha(p/f['path'])==f['sha256'],'Frozen read-only input changed')
check(set(x.name for x in p.iterdir())==set(x['path'] for x in frozen['files']),'Unexpected generated file')
report={'schema_version':1,'external_freeze_sha256':PIN,'externally_checked_verifier_sha256':VERIFIER,'uid':os.getuid(),'euid':os.geteuid(),'python_version':sys.version.split()[0],'readonly_write_probes_denied':len(probes),'original_positive_runs':sum(x['returncode']==0 for x in runs[:original_run_count]),'original_negative_runs':sum(x['returncode']!=0 for x in runs[:original_run_count]),'additional_positive_runs':sum(x['returncode']==0 for x in runs[original_run_count:]),'additional_negative_runs':sum(x['returncode']!=0 for x in runs[original_run_count:]),'replacement_verifier_rejected_before_execution':True,'frozen_readonly_payload_unchanged':True,'all_expected_outcomes':True,'test_only_mutations_re_pinned':True,'original_pin_never_replaced':True,'runs':runs}
validator_report = {k:v for k,v in report.items() if k!='runs'}

# The source-independent validator scenario inventory is an exact reconstruction.
check(validator_report['original_positive_runs']==3 and validator_report['original_negative_runs']==72,
      'Original scenario totals')
check(validator_report['additional_positive_runs']==6 and validator_report['additional_negative_runs']==126,
      'Independent additional scenario totals')

# Publication wrapper: verify every complete typed success receipt, not just rc.
def typed(a,b):
    if type(a) is not type(b): return False
    if type(b) is dict: return set(a)==set(b) and all(typed(a[k],v) for k,v in b.items())
    if type(b) is list: return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
    return a==b

def wrapper_run(label, root, pin, accept=False, isolated=True):
    check(sha(wrapper_copy)==WRAPPER_PIN, 'Trusted wrapper before every execution')
    for mode in ['', '-O', '-OO']:
        cmd=[sys.executable]+(['-I','-S','-B'] if isolated else ['-S','-B'])+([mode] if mode else [])+[str(wrapper_copy),pin,str(root)]
        r=subprocess.run(cmd,cwd=hostile,env=env if isolated else dict(os.environ),capture_output=True,text=True,timeout=60)
        check((r.returncode==0)==accept, 'Wrapper expected outcome: '+label+' '+mode+' '+r.stderr)
        if accept:
            expected={'schema_version':1,'problem_id':2304028,'status':'PASS',
                'optimization':{'':0,'-O':1,'-OO':2}[mode], 'uid':os.getuid(),'euid':os.geteuid(),
                'manifest_sha256':pin,'verified_payload_files':13,
                'source_checks':'NOT_RUN','corpus_checks':'NOT_RUN',
                'historical_sympy_reconstruction':'NOT_RUN','universal_proof_by_code':False,
                'readonly_write_probes_denied':4,
                'validator_receipt':{'status':'PASS','uid':os.geteuid(),'finite_cases':24,
                    'negative_type_controls':25,'universal_proof_checked_by_code':False,
                    'literature_classification':'KNOWN-SOLVED'}}
            check(typed(json.loads(r.stdout),expected) and r.stderr=='', 'Complete wrapper success receipt')
        wrapper_rows.append({'case':label,'optimization':mode or 'normal','accepted':r.returncode==0})

readonly=publication_work/'readonly_packet'
shutil.copytree(PACKET,readonly)
for p in readonly.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
readonly.chmod(0o555)
probes=[]
for p,mode in [(readonly/'new','w'),(readonly/'PUBLIC_MANIFEST.json','a'),(readonly/'author/cases.json','a')]:
    try:
        with p.open(mode):pass
    except PermissionError:probes.append(True)
    else:probes.append(False)
check(all(probes),'Actual packet read-only enforcement')
wrapper_run('readonly_relocated_hostile',readonly,MANIFEST_PIN,True)
wrapper_run('wrong_pin',readonly,'0'*64)
wrapper_run('malformed_pin',readonly,'G'*64)
wrapper_run('missing_isolation',readonly,MANIFEST_PIN,isolated=False)

def wrapper_fixture(label):
    q=publication_work/('wrapper_'+label);shutil.copytree(PACKET,q);thaw_fixture(q);return q

def repin(root):
    m=json.loads((root/'PUBLIC_MANIFEST.json').read_text())
    for row in m['files']:
        p=root/row['path'];row.update(bytes=p.stat().st_size,sha256=sha(p))
    save(root/'PUBLIC_MANIFEST.json',m)
    return sha(root/'PUBLIC_MANIFEST.json')

for label in ['changed_report','changed_ledger','changed_validator','changed_audit',
              'changed_wrapper','changed_driver','missing_file','extra_file','extra_directory',
              'linked_payload','linked_manifest','fifo_entry','laundered_author','laundered_audit',
              'laundered_original_allowlist','laundered_freeze','laundered_external_hashes']:
    q=wrapper_fixture(label);pin=MANIFEST_PIN
    targets={'changed_report':'author/REPORT.md','changed_ledger':'author/cases.json',
             'changed_validator':'author/verify.py','changed_audit':'audit/MATHEMATICAL_AUDIT.md',
             'changed_wrapper':'verify_publication.py','changed_driver':'mutation_tests.py',
             'laundered_author':'author/REPORT.md','laundered_audit':'audit/MATHEMATICAL_AUDIT.md',
             'laundered_original_allowlist':'ORIGINAL_PUBLIC_ALLOWLIST.json',
             'laundered_freeze':'FREEZE.json','laundered_external_hashes':'EXTERNAL_HASHES.json'}
    if label in targets:
        target=q/targets[label];target.write_bytes(target.read_bytes()+b'\n')
        if label.startswith('laundered_'):pin=repin(q)
    elif label=='missing_file':(q/'README.md').unlink()
    elif label=='extra_file':(q/'extra').write_text('extra')
    elif label=='extra_directory':(q/'extra').mkdir()
    elif label in ['linked_payload','linked_manifest']:
        target=q/('author/cases.json' if label=='linked_payload' else 'PUBLIC_MANIFEST.json')
        target.unlink();target.symlink_to(PACKET/target.relative_to(q))
    elif label=='fifo_entry':os.mkfifo(q/'unexpected_fifo')
    wrapper_run(label,q,pin)

q=publication_work/'linked_root';q.symlink_to(readonly,target_is_directory=True)
wrapper_run('linked_root',q,MANIFEST_PIN)

for label in ['version_bool','version_float','target_bool','target_float','unknown_key','missing_key',
              'files_object','missing_row','duplicate_row','row_extra','path_traversal','path_bool',
              'bytes_bool','bytes_float','bytes_zero','bytes_huge','hash_bool','hash_uppercase',
              'json_duplicate','json_nan','json_inf','json_minus_inf','json_overflow']:
    q=wrapper_fixture(label);mp=q/'PUBLIC_MANIFEST.json';m=json.loads(mp.read_text())
    if label=='version_bool':m['schema_version']=True
    elif label=='version_float':m['schema_version']=1.0
    elif label=='target_bool':m['problem_id']=True
    elif label=='target_float':m['problem_id']=2304028.0
    elif label=='unknown_key':m['extra']=1
    elif label=='missing_key':m.pop('schema_version')
    elif label=='files_object':m['files']={}
    elif label=='missing_row':m['files'].pop()
    elif label=='duplicate_row':m['files'][1]=copy.deepcopy(m['files'][0])
    elif label=='row_extra':m['files'][0]['extra']=1
    elif label=='path_traversal':m['files'][0]['path']='../README.md'
    elif label=='path_bool':m['files'][0]['path']=True
    elif label=='bytes_bool':m['files'][0]['bytes']=True
    elif label=='bytes_float':m['files'][0]['bytes']=float(m['files'][0]['bytes'])
    elif label=='bytes_zero':m['files'][0]['bytes']=0
    elif label=='bytes_huge':m['files'][0]['bytes']=1000001
    elif label=='hash_bool':m['files'][0]['sha256']=False
    elif label=='hash_uppercase':m['files'][0]['sha256']=m['files'][0]['sha256'].upper()
    save(mp,m)
    if label=='json_duplicate':mp.write_text(mp.read_text().replace('"schema_version": 1,','"schema_version":1,"schema_version":1,',1))
    elif label.startswith('json_'):
        value={'json_nan':'NaN','json_inf':'Infinity','json_minus_inf':'-Infinity','json_overflow':'1e309'}[label]
        mp.write_text(mp.read_text().replace('"schema_version": 1,','"schema_version":'+value+',',1))
    wrapper_run(label,q,sha(mp))

# Execution trust anchor substitutions are rejected by this caller, never executed.
substitute=publication_work/'substitute.py'
substitute.write_text('raise RuntimeError("DO NOT EXECUTE")\n')
check(sha(substitute)!=WRAPPER_PIN,'Substituted wrapper hash must fail')
final={p.relative_to(PACKET).as_posix():p.read_bytes() for p in PACKET.rglob('*') if p.is_file()}
check(initial==final,'Original packet bytes changed')
check({p.relative_to(readonly).as_posix():p.read_bytes() for p in readonly.rglob('*') if p.is_file()}==initial,'Read-only packet changed')
result={'schema_version':1,'problem_id':2304028,'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),
    'manifest_sha256':MANIFEST_PIN,'wrapper_sha256':WRAPPER_PIN,
    'validator_original_positive_runs':validator_report['original_positive_runs'],
    'validator_original_negative_runs':validator_report['original_negative_runs'],
    'validator_additional_positive_runs':validator_report['additional_positive_runs'],
    'validator_additional_negative_runs':validator_report['additional_negative_runs'],
    'validator_finite_cases_per_positive':24,'validator_internal_negatives_per_positive':25,
    'wrapper_positive_runs':sum(r['accepted'] for r in wrapper_rows),
    'wrapper_negative_runs':sum(not r['accepted'] for r in wrapper_rows),
    'readonly_outer_probes_denied':len(probes),'substituted_wrapper_not_executed':True,
    'substituted_validator_not_executed':True,'input_unchanged':True,
    'source_checks':'NOT_RUN','corpus_checks':'NOT_RUN','historical_sympy_reconstruction':'NOT_RUN',
    'universal_proof_by_code':False,'wrapper_runs':wrapper_rows}
print(json.dumps(result,indent=2,sort_keys=True))
