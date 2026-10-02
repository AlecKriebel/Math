#!/usr/bin/env python3
"""Read-only Git binding and private exact replay/mutation audit for PR36."""
from pathlib import Path
from datetime import datetime, timezone
import difflib
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent
REPO = ROOT.parents[3]
HEAD = '35be7fe58a2832c4d7012cf69c973810fb4c42f8'
BASE = '01358d66fc67d1c462bddf31c0d4ee5b120e6737'
PREFIX = 'unsolved_math_prioritization/attempts/20001424/'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def main():
    manifest = json.loads((AUDIT/'snapshot_manifest.json').read_text())
    metadata = json.loads((AUDIT/'pr_input/metadata.json').read_text())
    checks = []
    file_records = []
    for entry in manifest['files']:
        rel = entry['path']
        data = (AUDIT/'source_snapshot'/rel).read_bytes()
        obj = git('rev-parse', f'{HEAD}:{PREFIX}{rel}').decode().strip()
        exact = git('cat-file', 'blob', obj)
        same = data == exact and obj == entry['git_blob'] and sha(data) == entry['sha256'] and len(data) == entry['size']
        if not same:
            raise AssertionError(f'Git binding failed: {rel}')
        checks.append(same)
        file_records.append({'path':rel,'git_blob':obj,'sha256':sha(data),'size':len(data),'exact_git_equal':same})
    changed = git('diff','--name-only',BASE,HEAD).decode().splitlines()
    if changed != manifest['changed_paths'] or changed != [x['path'] for x in metadata['files']]:
        raise AssertionError('17-path inventory differs')
    if metadata['headRefOid'] != HEAD or manifest['head'] != HEAD or manifest['base'] != BASE:
        raise AssertionError('Head/base identity differs')
    diff = (AUDIT/'pr_input/diff.patch').read_bytes()
    generated = git('diff','--no-ext-diff','--no-color','--abbrev=9',BASE,HEAD)
    # GitHub adds a final LF and may vary headers. Parse complete per-file payload
    # and compare actual Git hunks; preserve the exact comparison outcome.
    diff_equal = diff == generated
    def hunks(data):
        out={}
        path=None
        for line in data.decode().splitlines():
            if line.startswith('diff --git '):
                path=line.split(' b/',1)[1];out[path]=[]
            elif path is not None and (line.startswith(('+','-',' ','@@')) and not line.startswith(('+++ ','--- '))):
                out[path].append(line)
        return out
    if hunks(diff) != hunks(generated):
        raise AssertionError('Complete exact diff hunks differ from actual Git')
    if sha(diff) != manifest['diff_sha256'] or len(diff) != manifest['diff_bytes']:
        raise AssertionError('Diff digest binding failed')
    queue_rows = {}
    for key, commit in [('base',BASE),('head',HEAD)]:
        text=git('show',f'{commit}:unsolved_math_prioritization/QUEUE.md').decode()
        queue_rows[key]=[line for line in text.splitlines() if '20001424 /' in line]
    binding = {'at_utc':datetime.now(timezone.utc).isoformat(),'head':HEAD,'base':BASE,
               'branch_at_check':git('branch','--show-current').decode().strip(),
               'numeric_files_verified':len(file_records),'changed_paths_verified':len(changed),
               'files':file_records,'diff_sha256':sha(diff),'actual_git_diff_sha256':sha(generated),
               'diff_byte_equal':diff_equal,'full_hunks_equal':True,'queue_rows':queue_rows,
               'scope':'Read-only object binding; no branch, queue, history or remote mutation.'}
    (ROOT/'git_binding_results.json').write_text(json.dumps(binding,indent=2)+'\n')

    private=ROOT/'original_replay'
    result=ROOT/'results'
    mutations=ROOT/'mutations'
    for directory in (private,result,mutations):
        directory.mkdir(exist_ok=True)
    author=private/'verify_graph.py'
    reviewer=private/'independent_checks.py'
    for src,dst in [(AUDIT/'source_snapshot/verify_graph.py',author),(AUDIT/'source_snapshot/review/independent_checks.py',reviewer)]:
        shutil.copy2(src,dst)
        if src.read_bytes()!=dst.read_bytes():
            raise AssertionError('Private input copy changed')
    runs=[]
    def run(name,file,expected,receipt=None,extra=()):
        cp=subprocess.run([sys.executable,*extra,str(file)],cwd=private,capture_output=True)
        (result/(name+'.stdout')).write_bytes(cp.stdout)
        (result/(name+'.stderr')).write_bytes(cp.stderr)
        equal=cp.stdout==receipt if receipt is not None else None
        outcome='rejected' if cp.returncode else 'accepted'
        if expected=='rejected' and cp.returncode==0:
            raise AssertionError(f'Mutation unexpectedly accepted: {name}')
        if expected=='accepted' and cp.returncode!=0:
            raise AssertionError(f'Control unexpectedly rejected: {name}')
        if receipt is not None and expected=='receipt_match' and not equal:
            raise AssertionError(f'Unchanged replay receipt differs: {name}')
        runs.append({'name':name,'command':[sys.executable,*extra,str(file)],'returncode':cp.returncode,
                     'outcome':outcome,'expected':expected,'receipt_equal':equal,
                     'stdout_sha256':sha(cp.stdout),'stderr_sha256':sha(cp.stderr),
                     'stderr_tail':cp.stderr.decode(errors='replace')[-1000:]})
        return cp
    ar=(AUDIT/'source_snapshot/graph_verification.json').read_bytes()
    rr=(AUDIT/'source_snapshot/review/independent_results.json').read_bytes()
    run('author_unchanged',author,'receipt_match',ar)
    run('reviewer_unchanged',reviewer,'receipt_match',rr)
    algebra=ROOT/'exact_algebra_controls.py'
    run('algebra_positive_and_negative',algebra,'accepted')

    specs=[
        ('author_all_inside',author,'[prev,next_,pend] if i<2 else [prev,pend,next_]','[prev,next_,pend]','rejected',ar),
        ('author_degree_output_corrupt',author,"'candidate_degree':11","'candidate_degree':12",'accepted',ar),
        ('reviewer_pendant_coordinate_corrupt',reviewer,'(-2,0),(0,-2)','(-Q(1,2),0),(0,-2)','rejected',rr),
        ('reviewer_reflection_matrix_corrupt',reviewer,'A=((0,-1),(1,0))','A=((1,0),(0,1))','rejected',rr),
        ('algebra_resultant_guard_removed',algebra,'args.omit_resultant or br != 0','True','rejected',None),
        ('algebra_insufficient_exponent',algebra,'type=int, default=20','type=int, default=1','rejected',None),
    ]
    mutation_records=[]
    for name,src,old,new,expected,receipt in specs:
        text=src.read_text()
        if text.count(old)!=1:
            raise AssertionError(f'Mutation anchor mismatch: {name}')
        altered=text.replace(old,new)
        file=mutations/(name+'.py');file.write_text(altered)
        patch=''.join(difflib.unified_diff(text.splitlines(True),altered.splitlines(True),fromfile=src.name,tofile=file.name))
        (mutations/(name+'.patch')).write_text(patch)
        cp=run(name,file,expected,receipt)
        if name=='author_degree_output_corrupt' and cp.stdout==receipt:
            raise AssertionError('Receipt equality failed to detect output corruption')
        mutation_records.append({'name':name,'source':str(src.relative_to(ROOT)),'file':str(file.relative_to(ROOT)),
                                 'source_sha256':sha(src.read_bytes()),'mutation_sha256':sha(file.read_bytes()),
                                 'patch_sha256':sha(patch.encode()),'old':old,'new':new})
    # Historical checkers use assert; -O removes their guards. Retain this
    # limitation, but do not mistake optimized success for a proof failure.
    cp=run('author_all_inside_optimized',mutations/'author_all_inside.py','accepted',ar,('-O',))
    if cp.stdout==ar:
        raise AssertionError('Optimized corrupt receipt should differ')
    report={'at_utc':datetime.now(timezone.utc).isoformat(),'pass':True,'runs':runs,'mutations':mutation_records,
            'unchanged_private_input_sha256':{'author':sha(author.read_bytes()),'reviewer':sha(reviewer.read_bytes())},
            'scope':'Normal unchanged replays match historical receipts; actual mutated programs test guards. Optimized historical assert-based programs are not valid verification. No rational-map coefficients constructed.'}
    (ROOT/'replay_mutation_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'git_numeric_files':len(file_records),'changed_paths':len(changed),'full_hunks_equal':True,
                      'diff_byte_equal':diff_equal,'runs':len(runs),'pass':True},indent=2))


if __name__=='__main__':
    main()
