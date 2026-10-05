from review_tools import *
import zipfile, stat, ast
def verify(entries,root):
    checked=[]
    for e in entries:
        p=root/e['file']
        if not p.is_file()or sha(p)!=e['sha256']or p.stat().st_size!=e['bytes']:raise RuntimeError('integrity mismatch '+str(p))
        checked.append(e['file'])
    return checked
prep=json.loads((Q/'PREPARATION_MANIFEST.json').read_text())
freeze=json.loads((Q/'private_notes/FROZEN_CANDIDATE_MANIFEST.json').read_text())
payload=json.loads((Q/'publicfiles/PAYLOAD_MANIFEST.json').read_text())
report={'UTC':utc(),'preparation_files_verified':len(verify(prep['files'],Q)), 'frozen_public_files_verified':len(verify(freeze['public_files'],Q)), 'payload_members_verified':len(verify(payload['files'],Q/'publicfiles')),'hashes':{str(p.relative_to(Q)):sha(p)for p in [Q/'PREPARATION_MANIFEST.json',Q/'private_notes/FROZEN_CANDIDATE_MANIFEST.json',Q/'publicfiles/pr95_note.pdf',Q/'publicfiles/pr95_support.zip']}}
regular=[];links=[]
for root,dirs,files in os.walk(Q,followlinks=False):
    for name in dirs+files:
        p=Path(root)/name
        if p.is_symlink():links.append({'file':str(p.relative_to(Q)),'target':os.readlink(p)})
    for name in files:
        p=Path(root)/name
        if not p.is_symlink():regular.append({'file':str(p.relative_to(Q)),'bytes':p.stat().st_size,'sha256':sha(p)})
dump(A/'Q_BASELINE.json',{'UTC':utc(),'files':regular,'symlinks':links})
report['all_regular_file_count']=len(regular);report['intentional_symlink_count']=len(links);report['preparation_coverage_omissions']=sorted(set(e['file']for e in regular)-set(e['file']for e in prep['files']))
with zipfile.ZipFile(Q/'publicfiles/pr95_support.zip')as z:
    infos=z.infolist();names=[i.filename for i in infos]
    if len(set(names))!=len(names):raise RuntimeError('duplicate archive entry')
    for i in infos:
        p=Path(i.filename)
        if p.is_absolute()or'..'in p.parts or stat.S_ISLNK(i.external_attr>>16):raise RuntimeError('unsafe archive entry')
        if z.read(i.filename)!=(Q/'publicfiles'/i.filename).read_bytes():raise RuntimeError('archive content mismatch')
    if set(names)!=set(e['file']for e in payload['files'])|{'PAYLOAD_MANIFEST.json'}:raise RuntimeError('archive coverage mismatch')
    report['archive_members_byte_compared']=len(names)
for line in (Q/'publicfiles/SHA256SUMS.txt').read_text().splitlines():
    digest,name=line.split(maxsplit=1)
    if digest!=sha(Q/'publicfiles'/name):raise RuntimeError('external digest mismatch')
report['external_digests_verified']=True
report['zero_ast_asserts']={p.name:not any(isinstance(n,ast.Assert)for n in ast.walk(ast.parse(p.read_text())))for p in (Q/'publicfiles/verification').glob('*.py')}
if not all(report['zero_ast_asserts'].values()):raise RuntimeError('removable asserts')
current=[];all_receipts=[]
for p in Q.rglob('process.json'):
    d=json.loads(p.read_text());wd=p.parent
    if 'inputs'in d and 'exit_code'in d and 'pid'in d:
        for e in d['inputs']:
            if 'snapshot'in e:
                f=wd/e['snapshot']
                if sha(f)!=e['sha256']or f.stat().st_size!=e['bytes']:raise RuntimeError('receipt snapshot mismatch '+str(p))
        for name in ['stdout.bin','stderr.bin']:
            if name in d:
                f=wd/name
                if sha(f)!=d[name]['sha256']or f.stat().st_size!=d[name]['bytes']:raise RuntimeError('receipt stream mismatch '+str(p))
        all_receipts.append(str(p.relative_to(Q)))
        if str(p.relative_to(Q)).startswith('publicfiles/verification/recorded_processes/'):
            current.append({'label':d['label'],'pid':d['pid'],'recorder_pid':d['recorder_pid'],'argv':d['argv'],'started_utc':d['started_utc'],'ended_utc':d['ended_utc'],'exit_code':d['exit_code'],'source_sha256':d['inputs'][0]['sha256'],'runner_sha256':d['inputs'][3]['sha256'],'invocation_manifest_sha256':d['inputs'][4]['sha256'],'stdout_bytes':d['stdout.bin']['bytes'],'stderr_bytes':d['stderr.bin']['bytes']})
report['structurally_verified_receipts_count']=len(all_receipts)
report['public_current_assembly_receipts']=current
for r in json.loads((Q/'publicfiles/verification/recorded_results.json').read_text())['runs']:
    f=Q/'publicfiles/verification/recorded_processes'/r['label']
    for k,name in [('process_sha256','process.json'),('stdout_sha256','stdout.bin'),('stderr_sha256','stderr.bin')]:
        if sha(f/name)!=r[k]:raise RuntimeError('summary receipt linkage mismatch')
report['current_summary_links_verified']=True
for e in json.loads((Q/'private_notes/INPUTS.json').read_text())['files']:
    p=Q.parent/e['file']
    if sha(p)!=e['sha256']or p.stat().st_size!=e['bytes']:raise RuntimeError('prep sibling input mismatch')
report['preparation_sibling_inputs_verified']=True
dump(A/'INTEGRITY.json',report)
print(json.dumps({k:v for k,v in report.items()if k not in ['public_current_assembly_receipts','hashes']}))
