"""Resume the stopped operator path repair without rerunning completed mutations."""
from pathlib import Path
import hashlib,json,subprocess
A=Path(__file__).resolve().parent;C=A.parents[2]
source=(A/'prepare_native_acceptance.py').read_text()
prefix=source[:source.index("ready=load(A/'ROOT_READY_FOR_PUBLICATION.json')")]
prefix=prefix.replace("D.mkdir(exist_ok=False);records=[]","records=json.loads((D/'PROCESS_JOURNAL.json').read_text())['records']")
ns={'__file__':str(A/'prepare_native_acceptance.py')};exec(compile(prefix,str(A/'prepare_native_acceptance.py'),'exec'),ns)
load=ns['load'];require=ns['require'];git=ns['git'];sha=ns['sha'];records=ns['records']
ready=load(A/'ROOT_READY_FOR_PUBLICATION.json');pub=load(A/'actual_operations/zenodo_publish/stdout.bin')
public=load(A/'ROOT_PUBLIC_DEPOSIT_VERIFICATION.json');tracker=load(A/'ROOT_TRACKER_RECORD.json')
pr=load(A/'actual_operations/pr95_merged_readback/stdout.bin')
require(ready['publication_clearance'] and ready['whole_package_rounds']==2 and not ready['priority_clearance'],'review gate')
require(pub['state']=='published' and public['verified'] and tracker['unique_verified'] and tracker['DOI']==pub['doi'],'service gates')
require(pr['state']=='MERGED' and pr['headRefOid']==ns['HEAD'],'merge gate')
merge=pr['mergeCommit']['oid'];base=records[-1]['argv'][-1]
require(records[-1]['argv'][:4]==['/usr/bin/git','reset','--mixed','--quiet'] and records[-1]['exit_code']==0,'initial termination point')
rev=[x for x in records if x['argv']==['/usr/bin/git','rev-parse','HEAD']];require(len(rev)==1,'old head receipt')
old=(ns['D']/rev[0]['stdout_file']).read_text().strip()
require(git('rev-parse','HEAD').strip().decode()==base,'partial base changed')
require(not git('diff','--cached','--name-only','-z'),'foreign staged')
old_queue=git('show',old+':unsolved_math_prioritization/QUEUE.md')
queue=C/'unsolved_math_prioritization/QUEUE.md';require(queue.read_bytes()==old_queue,'unknown queue worktree edits')
orig=load(A/'original_source_authentication_20261005/ORIGINAL_BLOB_MANIFEST.json')
require(len(orig['files'])==17,'incoming inventory')
author_source=A/'repaired_certificate_sources_20261005/verify.py'
require(sha(author_source)=='1294068a5202c9f05ededf864887b7ce7bcb979319bd8f32827df5c88191a6e8','repaired author pin')
for e in orig['files']:
    require(sha(Path(e['preserved_path']))==e['sha256'],'incoming archive')
    b=git('show',base+':'+e['path']);require(hashlib.sha256(b).hexdigest()==e['sha256'],'merged original')
    f=C/e['path'];expected=author_source.read_bytes() if e['relative_path'] in ['verify.py','independent_review/author_replay/verify.py'] else b
    require(not f.is_symlink() and f.read_bytes()==expected,'unexpected partial native body')
qb=git('show',base+':unsolved_math_prioritization/QUEUE.md').decode();lines=qb.splitlines()
indices=[i for i,s in enumerate(lines) if '| 10400120 / AMR-103-0120 |' in s];require(len(indices)==1,'queue unique')
i=indices[0];cells=lines[i].split('|');require(cells[8].strip()=='claimed_solved' and cells[9].strip()=='2/5','status effort')
ns.update({'ready':ready,'pub':pub,'public':public,'tracker':tracker,'pr':pr,'merge':merge,'base':base,'old':old,'doi':pub['doi'],'url':pub['doi_url'],'queue':queue,'qb':qb,'lines':lines,'i':i,'cells':cells,'N':C/'unsolved_math_prioritization/attempts/10400120'})
start=source.index("source=A/'repaired_certificate_sources_20261005/independent_review/independent_checks.py'")
exec(compile(source[start:],str(A/'prepare_native_acceptance.py'),'exec'),ns)
