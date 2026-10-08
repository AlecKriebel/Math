#!/usr/bin/env python3
"""Reproduce UID-1000, read-only and optimization/mutation audit in a fresh temp tree.
Usage: python3 -B run_readonly_audit.py /path/to/frozen/public > EXECUTION_AUDIT.json
The original packet is read only. Temporary specimens are chmod 0444/0555.
"""
import ast
import errno
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ORIGINAL=Path(sys.argv[1]).resolve()

def need(condition,message):
    if not condition:
        raise RuntimeError(message)

need(os.getuid()==1000 and os.geteuid()==1000,'Must run as genuine UID/EUID 1000')
freeze=(ORIGINAL/'EDITION_MANIFEST.json').read_bytes()
need(hashlib.sha256(freeze).hexdigest()=='00949c87a3adfa815c55af7b95df7e72da00ca64f382f401c0ca97f3ba0c7f19','Frozen manifest pin')
for entry in json.loads(freeze)['files']:
    data=(ORIGINAL/entry['path']).read_bytes()
    need(len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'],'Frozen leaf pin')
expected=json.loads((ORIGINAL/'VERIFICATION_RESULTS.json').read_text())
old=(ORIGINAL/'verify_exact.py').read_text()
new=(HERE/'verify_exact_corrected.py').read_text()
mutations=[
    ('graph_predicate_false','return covered == (1 << len(adj)) - 1','return False'),
    ('cycle_lift_connected','if i % n not in {1, 2}','if True'),
    ('word_not_cyclically_reduced',"target = 'AdBDaCAdbDac'","target = 'AdBDaCAdbDacaA'"),
    ('schottky_identity','base = ((34, 21), (21, 13))','base = ((1, 0), (0, 1))'),
    ('c5_false_clique','for k in cliques:','for k in cliques + [(1 << n) - 1]:'),
]
workspace=Path(tempfile.mkdtemp(prefix='raag-audit-'))
records=[]

def specimen(edition,mutation,source):
    directory=workspace/(edition+'_'+mutation)
    directory.mkdir()
    p=directory/'verify_exact.py'
    p.write_text(source)
    p.chmod(0o444)
    # Include an already existing read-only output file, exactly as in a freeze.
    (directory/'VERIFICATION_RESULTS.json').write_text(json.dumps(expected))
    (directory/'VERIFICATION_RESULTS.json').chmod(0o444)
    directory.chmod(0o555)
    for target,flags in [(p,os.O_WRONLY),(directory/'probe',os.O_WRONLY|os.O_CREAT|os.O_EXCL)]:
        try:
            fd=os.open(target,flags,0o600)
        except PermissionError as exc:
            need(exc.errno==errno.EACCES,'Expected EACCES')
        else:
            os.close(fd)
            raise RuntimeError('Read-only probe was writable')
    return p


def run(p,optimization,kind,extra=()):
    flags=['-B']+(['-'+('O'*optimization)] if optimization else [])
    command=[sys.executable,*flags]
    if kind=='core':
        command += [str(HERE/'readonly_core_runner.py'),str(p)]
    else:
        command += [str(p),*extra]
    process=subprocess.run(command,cwd=p.parent,capture_output=True,text=True,
                           env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},timeout=60)
    parsed=None
    if process.returncode==0:
        parsed=json.loads(process.stdout)
    record={'specimen':p.parent.name,'mode':['normal','-O','-OO'][optimization],
            'execution':kind,'uid':os.getuid(),'euid':os.geteuid(),
            'input_mode':oct(p.stat().st_mode & 0o777),'cwd_mode':oct(p.parent.stat().st_mode & 0o777),
            'input_write_denied':True,'cwd_create_denied':True,
            'exit_code':process.returncode,'stdout_sha256':hashlib.sha256(process.stdout.encode()).hexdigest(),
            'stderr_last_line':process.stderr.strip().splitlines()[-1] if process.stderr.strip() else None}
    if parsed is not None:
        result=parsed['results'] if kind=='core' else parsed
        record['reported_all_checks_passed']=result.get('all_checks_passed')
        if kind!='cli_external':
            record['results_match_frozen']=result==expected
        if kind=='core':
            need(parsed['uid']==1000 and parsed['euid']==1000,'Subprocess identity')
            need(parsed['input_write_denied'] and parsed['cwd_create_denied'],'Subprocess permissions')
        record['returned_minimum_trace']=result.get('explicit_free_embedding',{}).get('minimum_absolute_trace')
    records.append(record)
    return process,record

try:
    baseline={edition:specimen(edition,'baseline',source) for edition,source in [('original',old),('corrected',new)]}
    for optimization in range(3):
        _,r=run(baseline['original'],optimization,'cli')
        need(r['exit_code']!=0 and 'PermissionError' in r['stderr_last_line'],'Original CLI must fail read-only output write')
        _,r=run(baseline['original'],optimization,'core')
        need(r['exit_code']==0 and r['results_match_frozen'],'Original core reproduction')
        process,r=run(baseline['corrected'],optimization,'cli')
        need(r['exit_code']==0 and r['results_match_frozen'],'Corrected CLI reproduction')
        need(process.stdout.encode()==(ORIGINAL/'VERIFICATION_RESULTS.json').read_bytes(),'Byte-identical corrected stdout')
        external=workspace/('external_'+str(optimization)+'.json')
        _,r=run(baseline['corrected'],optimization,'cli_external',('--output',str(external)))
        need(r['exit_code']==0 and external.read_bytes()==(ORIGINAL/'VERIFICATION_RESULTS.json').read_bytes(),'External output reproduction')
        r['external_file_matches_frozen']=True
        r['external_file_sha256']=hashlib.sha256(external.read_bytes()).hexdigest()
    for name,before,after in mutations:
        for edition,source in [('original',old),('corrected',new)]:
            need(source.count(before)==1,'Unique mutation target '+name)
            p=specimen(edition,name,source.replace(before,after,1))
            for optimization in range(3):
                _,r=run(p,optimization,'core' if edition=='original' else 'cli')
                expected_accept=edition=='original' and optimization>0
                if expected_accept:
                    need(r['exit_code']==0 and r['reported_all_checks_passed'] is True,'Reproduce optimized false pass')
                else:
                    need(r['exit_code']!=0 and 'AssertionError' in r['stderr_last_line'],'Mutation must be rejected')
    independent=[]
    # Run the independent algorithm in the same read-only working directory.
    ip=workspace/'independent'
    ip.mkdir()
    script=ip/'independent_exact_check.py'
    script.write_bytes((HERE/'independent_exact_check.py').read_bytes())
    script.chmod(0o444)
    ip.chmod(0o555)
    for optimization in range(3):
        flags=['-B']+(['-'+('O'*optimization)] if optimization else [])
        process=subprocess.run([sys.executable,*flags,str(script)],cwd=ip,capture_output=True,text=True,timeout=60)
        need(process.returncode==0,'Independent implementation')
        data=json.loads(process.stdout)
        need(data==json.loads((HERE/'INDEPENDENT_EXACT_RESULTS.json').read_text()),'Independent result pin')
        independent.append({'mode':['normal','-O','-OO'][optimization],'uid':os.getuid(),'euid':os.geteuid(),
                            'input_mode':'0o444','cwd_mode':'0o555','exit_code':process.returncode,
                            'matches_independent_results':True,'stdout_sha256':hashlib.sha256(process.stdout.encode()).hexdigest()})
    need((ORIGINAL/'EDITION_MANIFEST.json').read_bytes()==freeze,'Original manifest unchanged')
    for entry in json.loads(freeze)['files']:
        data=(ORIGINAL/entry['path']).read_bytes()
        need(len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'],'Original leaf unchanged')
    result={'python_version':sys.version,'uid':os.getuid(),'euid':os.geteuid(),
            'original_assert_nodes':sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(old))),
            'corrected_assert_nodes':sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(new))),
            'original_optimized_false_passes':sum(r['specimen'].startswith('original_') and r['specimen']!='original_baseline' and r['exit_code']==0 for r in records),
            'corrected_mutations_rejected':sum(r['specimen'].startswith('corrected_') and r['specimen']!='corrected_baseline' and r['exit_code']!=0 for r in records),
            'original_freeze_unchanged':True,'records':records,'independent_runs':independent}
    print(json.dumps(result,indent=2))
finally:
    for folder,dirs,files in os.walk(workspace):
        Path(folder).chmod(0o755)
        for name in files:
            (Path(folder)/name).chmod(0o644)
    shutil.rmtree(workspace)
