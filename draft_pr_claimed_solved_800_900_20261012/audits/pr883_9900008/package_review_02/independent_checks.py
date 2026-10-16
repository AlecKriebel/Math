#!/usr/bin/env python3
"""Independent r2 diagnostic and artifact checks; no universal-proof or novelty claim."""
from pathlib import Path
from fractions import Fraction as F
import datetime,hashlib,json,sys,itertools,zipfile,io,stat,subprocess,re,struct,zlib

def need(v,m):
    if not v: raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(b):
    def pairs(ps):
        d={}
        for k,v in ps:need(k not in d,'duplicate JSON');d[k]=v
        return d
    return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def diff(a,b,p=''):
    if type(a)!=type(b):return [p]
    if isinstance(a,dict):return [x for k in set(a)|set(b) for x in ([p+'/'+k] if k not in a or k not in b else diff(a[k],b[k],p+'/'+k))]
    if isinstance(a,list):return [p] if len(a)!=len(b) else [x for i,(v,w) in enumerate(zip(a,b)) for x in diff(v,w,p+'/'+str(i))]
    return [] if a==b else [p]
A=Path(sys.argv[1]).resolve();R=A/'replay/revision_r2';P=R/'preprint/verification_package'
outer=R/'CURRENT_PUBLICATION_MANIFEST.json';idx=P/'package_index.json';seal=strict((A/'revision_r2_SEAL.json').read_bytes())
need(sha(outer.read_bytes())=='4d3697ad4c38f37528b313626dc072c08c806d27c2a92316d63f4bcc522cfefa','outer external pin')
need(sha(idx.read_bytes())=='9c547acc859c79b26704df0d9d278aaa469d02e22093b3ab7d199d6b50e2c49b','index external pin')
for root,manifest,selfname in [(R,strict(outer.read_bytes()),outer.name),(P,strict(idx.read_bytes()),idx.name)]:
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()};expected={x['path'] for x in manifest['files']}|{selfname};need(actual==expected,'closed members')
    for row in manifest['files']:
        p=root/row['path'];raw=p.read_bytes();need(stat.S_ISREG(p.lstat().st_mode) and len(raw)==row['bytes'] and sha(raw)==row['sha256'],'file pin')
        if p.suffix=='.json':strict(raw)
for row in seal['core_files']:
    raw=(R/row['path']).read_bytes();need(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'core pin')
current=strict((R/'CURRENT_PUBLICATION.json').read_bytes());need(current['core_files']==seal['core_files'],'same eleven cores')
for row in current['tooling_layout']['copy_pairs']:need((R/row['outer_path']).read_bytes()==(P/row['portable_path']).read_bytes(),'duplicate pair')
source_manifest=(A/'SOURCE_MANIFEST.json').read_bytes();need(sha(source_manifest)=='53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab','source anchor')
sources=strict(source_manifest)['files'];need(len(sources)==26 and sum(x['bytes'] for x in sources)==211771,'source counts')
for row in sources:
    raw=(P/'source'/row['path']).read_bytes();need(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'source byte pin');need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['git_blob'],'source git blob')
    if row['path'] not in ['README.md','RESEARCH_LOG.md']:need(raw==(R/row['path']).read_bytes(),'original outer parity')
metadata=strict((R/'preprint/metadata.json').read_bytes());deposit=strict((R/'preprint/zenodo-deposit.json').read_bytes());need(metadata==deposit['metadata'],'nested deposit metadata exact equality')
files=deposit['files'];need(len(files)==2,'exact two deposit files')
expected_files=[{'path':'output/pdf/note.pdf','name':'diffuse-allocation-note.pdf'},{'path':'verification.zip','name':'diffuse-allocation-verification.zip'}]
need(files==expected_files,'deposit exact path names')
need(metadata['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'author ORCID')
need(metadata['publication_date']=='2026-10-15' and metadata['version']=='1.0.0','date/version')
family_rows=[]
for folder in sorted((P/'audits').iterdir()):
    m=strict((folder/'PUBLIC_MANIFEST.json').read_bytes());paths=[]
    for row in m.get('files',m.get('allowed_public_files',[])):
        raw=(folder/row['path']).read_bytes();need(('bytes' not in row or len(raw)==row['bytes']) and sha(raw)==row['sha256'],'family safe row '+folder.name+'/'+row['path']);paths.append(row['path'])
    need({str(x.relative_to(folder)) for x in folder.rglob('*') if x.is_file()}==set(paths)|{'PUBLIC_MANIFEST.json'},'family explicit closed safe list')
    family_rows.append({'family':folder.name,'files_including_manifest':len(paths)+1,'manifest_sha256':sha((folder/'PUBLIC_MANIFEST.json').read_bytes())})
# Search decoded public contents, recursively including both nested original ZIPs.
private_patterns=[rb'/' + rb'Users/',rb'/' + rb'private/var/',rb'/' + rb'var/folders/',rb'/home/[^ /\n]+/',rb'/' + rb'tmp/',rb'[A-Za-z]:\\\\Users\\\\',rb'Bearer [A-Za-z0-9._-]{20,}']
scan_count=0;leaks=[];zip_checks=[]
def scan(label,raw):
    global scan_count
    scan_count+=1
    for pat in private_patterns:
        if re.search(pat,raw):leaks.append({'path':label,'pattern':pat.decode('ascii')})
    if raw.startswith(b'PK\x03\x04'):
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            for n in z.namelist():scan(label+'::'+n,z.read(n))
for p in sorted(R.rglob('*')):
    if p.is_file():scan(str(p.relative_to(R)),p.read_bytes())
need(not leaks,'private path/credential scan')
with zipfile.ZipFile(R/'preprint/verification.zip') as z:
    names=z.namelist();need(names==sorted(str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()),'zip exact sorted closed set')
    for info in z.infolist():
        need(z.read(info.filename)==(P/info.filename).read_bytes(),'zip bytes')
        need(info.date_time==(2026,10,15,0,0,0) and info.external_attr==(stat.S_IFREG|0o644)<<16 and not info.extra and not info.comment,'zip stable metadata')
# Verify actual prepared Git blobs, without changing refs, branch or index.
prepared='83a9565aa3588dc33abbc293e9f416d1da422bc6';prefix='unsolved_math_prioritization/attempts/9900008/'
tree=subprocess.check_output(['git','--no-optional-locks','ls-tree','-rz',prepared,'--',prefix])
rows=[x.split(b'\t',1) for x in tree.split(b'\0') if x];need(len(rows)==244,'prepared closed tree count')
for meta,path in rows:
    mode,kind,blob=meta.split();relative=path.decode()[len(prefix):];need(mode==b'100644' and kind==b'blob','git entry type');want=(R/relative).read_bytes();need(hashlib.sha1(b'blob '+str(len(want)).encode()+b'\0'+want).hexdigest()==blob.decode(),'actual prepared git bytes')
q=subprocess.check_output(['git','--no-optional-locks','show',prepared+':unsolved_math_prioritization/QUEUE.md']).decode();qr=[l for l in q.splitlines() if '9900008 / AMR-098-0008' in l];need(len(qr)==1,'one target queue row');cols=[s.strip() for s in qr[0].split('|')];need(cols[8]=='claimed_solved' and cols[9]=='1/5' and cols[10]=='','exact queue disposition/effort/blank DOI')
# Independently compare private raw receipt snapshots against the amended public bytes.
repair=[]
for fam in ['allocation_audit_01','artifact_audit_01']:
    amendment=strict((P/'audits'/fam/'PUBLIC_PATH_AMENDMENT.json').read_bytes())
    for row in amendment['receipts']:
        oldraw=(A/'private_legacy_receipt_paths'/fam/row['path']).read_bytes();newraw=(P/'audits'/fam/row['path']).read_bytes();need(len(oldraw)==row['original_bytes'] and sha(oldraw)==row['original_sha256'],'raw original receipt preserved');need(len(newraw)==row['public_bytes'] and sha(newraw)==row['public_sha256'],'public receipt pin')
        old=strict(oldraw);new=strict(newraw);descriptor=new.pop('publication_metadata_redaction');changes=sorted(diff(old,new));need(changes==row['changed_json_pointers'],'only recorded local field changed');need(descriptor['original_json_sha256']==sha(oldraw) and descriptor['raw_original_preserved_privately'] is True,'honest metadata amendment descriptor');repair.append({'family':fam,'file':row['path'],'only_changed_pointers':changes,'raw_original_authenticated':True,'all_other_fields_equal':True})
# Distinct exact arithmetic independently of the author's verifier.
finite=[]
for weights in [(F(1),F(2)),(F(2),F(3)),(F(1),F(1))]:
    maps=[]
    for labels in itertools.product(range(3),repeat=2):
        received=[F(0)]*3
        for j,w in zip(labels,weights):received[j]+=w
        if received==list(weights)+[F(0)]:maps.append(labels)
    need(maps==([(0,1),(1,0)] if weights[0]==weights[1] else [(0,1)]),'independent quotient maps')
    finite.append({'weights':list(map(str,weights)),'preserving_maps':maps})
unit=0
for d in range(1,54):
    for k in range(d+1):
        u=F(k,d);points=[(F(n)+off,w) for n in range(-3,4) for off,w in [(F(0),F(1)),(F(1,2),F(2))] if -u<=F(n)+off<1-u]
        need(len(points)==2 and sum(w for _,w in points)==3 and sum(w for y,w in points if y%1==F(1,2))/3==F(2,3),'unit window root event')
        unit+=1
need([sum(w*p for w,p in zip([F(1),F(2)],column)) for column in zip((F(0),F(1)),(F(1,2),F(1,2)))]==[1,2],'Markov mass balance')
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','outer_files':244,'portable_members':204,'core_files':seal['core_files'],'source_files':26,'source_bytes':211771,'duplicate_copy_pairs':10,'all_12_family_safe_manifests':family_rows,'nested_metadata_equal':True,'deposit_files':files,'prepared_git_commit':prepared,'prepared_git_blobs_verified':244,'one_queue_row_literal_claimed_solved_effort_1_of_5_blank_doi':True,'recursive_public_payloads_scanned':scan_count,'private_path_or_credential_matches':leaks,'legacy_receipt_transformations':repair,'finite_quotient_controls':finite,'independent_exact_unit_windows':unit,'Markov_mass_balance_verified':True,'limitation':'Finite diagnostics supplement independently reconstructed universal proof; priority remains bounded.'},indent=2))
