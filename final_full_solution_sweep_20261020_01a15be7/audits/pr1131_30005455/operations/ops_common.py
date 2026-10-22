#!/usr/bin/env python3
"""PR1131 fixed identities, read-only custody, private durable receipts; no service writes."""
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import zipfile

OPS=Path(__file__).resolve().parent
AUDIT=OPS.parent
REPO=AUDIT.parents[2]
PUBLICATION=AUDIT/'publication'
PRIVATE=OPS/'private'
RUNTIME=OPS/'runtime'
ORIGINAL='bacae693a1f2a33c89565b0bd716620885831289'
BRANCH='codex/30005455-finite-warm-thresholds'
PROBLEM='unsolved_math_prioritization/attempts/30005455'
QUEUE='unsolved_math_prioritization/QUEUE.md'
REPOSITORY='AlecKriebel/Math'
SHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
HEADERS=['Original Problem','Solution Chat URL','DOI','Notes']
TITLE='A sharp forest bound and an improved whisker bound for finite WARM graphs'
SCIENCE_SHA='8bc7d6ce77fe4457d87c653decbc16be735a657fcd1a0d54b9571919ec71a2dd'
FREEZE_SHA='6adff8209ea170a6d0847a7aa1efd720dab937a14010e7298398a8fcd1984551'
SOURCE_SHA='e3db5fb166e0823ebacb4048f8330c398e80c0c237bfc02c897f0891026508ba'
ORIGINALS={'ACCEPTANCE.json','MANIFEST.json','MATHEMATICAL_AUDIT.md','PROOF.md','README.md','SOURCE_METADATA.json','SOURCE_REVIEW.md','STATUS.json'}
FLAT={'finite-warm-thresholds.pdf','finite-warm-thresholds-source-and-verification.zip','README.md','zenodo-metadata.json','zenodo-deposit.json'}
PATTERN=re.compile(r'30005455|12697708|/pull/1131\b|\bPR\s*#?1131\b|warm|whisker|reinforced.{0,10}graph|forest.{0,12}(?:bound|threshold)',re.I)
sys.path.insert(0,str(REPO/'zenodo_deposit_tool'))
import zenodo

def need(condition,message):
    if not condition:raise RuntimeError(message)

def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def digest(value):return sha(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
def pin(data):return {'bytes':len(data),'sha256':sha(data)}
def strict_json(data):
    def pairs(items):
        out={}
        for k,v in items:
            need(k not in out,'Duplicate JSON key');out[k]=v
        return out
    return json.loads(data,object_pairs_hook=pairs)

def safe(root,name):
    need(isinstance(name,str) and name and '\\' not in name and ':' not in name and '\0' not in name,'Unsafe path')
    p=PurePosixPath(name)
    need(not p.is_absolute() and p.as_posix()==name and all(c not in {'','.','..'} for c in name.split('/')),'Unsafe path')
    need(not root.is_symlink() and not any(root.joinpath(*p.parts[:i]).is_symlink() for i in range(1,len(p.parts)+1)),'Symlink rejected')
    return root/name

def read_pinned(path,expected):
    data=path.read_bytes();need(pin(data)==expected,'Artifact changed: '+str(path));return data

def durable(path,value):
    """O_EXCL intent/receipt: preserve even partial writes and fsync directory."""
    need(path.parent in {RUNTIME,PRIVATE} or PRIVATE in path.parents,'Receipt outside assigned private/runtime directory')
    need(not any(p.is_symlink() for p in [OPS,RUNTIME,PRIVATE,path.parent]),'Receipt symlink rejected')
    path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'wb') as f:
        f.write((json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode());f.flush();os.fsync(f.fileno())
    fd=os.open(path.parent,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)

def fresh(timestamp,seconds=180):
    t=dt.datetime.fromisoformat(timestamp);need(t.tzinfo is not None,'Missing timezone')
    need(-5<=(dt.datetime.now(dt.timezone.utc)-t).total_seconds()<=seconds,'Expired/future observation')

def package():
    dependencies=strict_json((OPS/'DEPENDENCY_PINS.json').read_bytes())
    need(set(dependencies)=={'zenodo_deposit_tool/zenodo.py'},'Unexpected operational code dependency')
    for name,p in dependencies.items():read_pinned(safe(REPO,name),p)
    freeze=read_pinned(AUDIT/'PACKAGE_FREEZE_01.json',{'bytes':(AUDIT/'PACKAGE_FREEZE_01.json').stat().st_size,'sha256':FREEZE_SHA})
    frozen=strict_json(freeze);need(frozen['pr']==1131 and frozen['head']==ORIGINAL,'Wrong freeze identity')
    need(len(frozen['frozen_six'])==6,'Six release pins required')
    for name,p in frozen['frozen_six'].items():read_pinned(safe(PUBLICATION,name),p)
    source=(PUBLICATION/'SOURCE_MANIFEST.json').read_bytes();need(sha(source)==SOURCE_SHA,'Source manifest changed')
    declared=strict_json(source);need(len(declared)==44,'Expected 44 source payloads')
    payload={name:read_pinned(safe(PUBLICATION,name),p) for name,p in declared.items()}
    zdata=payload.get('output/pdf/finite-warm-thresholds.pdf');need(zdata is not None,'PDF absent from source')
    with zipfile.ZipFile(PUBLICATION/'output/finite-warm-thresholds-source-and-verification.zip') as z:
        names=z.namelist();need(len(names)==45 and len(set(names))==45 and z.testzip() is None,'Source ZIP closure/CRC')
        need(set(names)==set(declared)|{'SOURCE_MANIFEST.json'},'Source ZIP inventory mismatch')
        for name in names:
            safe(Path('/synthetic'),name);info=z.getinfo(name)
            need(not info.is_dir() and (info.external_attr>>16 & 0o170000)!=0o120000,'Unsafe archive member')
            need(z.read(name)==(source if name=='SOURCE_MANIFEST.json' else payload[name]),'Source ZIP bytes changed')
    native=strict_json(payload['zenodo-deposit.json']);metadata=strict_json(payload['zenodo-metadata.json'])
    need(native['metadata']==metadata and metadata['title']==TITLE and metadata['version']=='1.0.0','Metadata identity mismatch')
    need(native['files']==[{'path':'output/pdf/finite-warm-thresholds.pdf'},{'path':'output/finite-warm-thresholds-source-and-verification.zip'}],'Two exact uploads required')
    with zipfile.ZipFile(PUBLICATION/'output/zenodo-upload-kit.zip') as kit:
        need(len(kit.namelist())==5 and set(kit.namelist())==FLAT and kit.testzip() is None,'Kit closure/CRC')
        flat={name:kit.read(name) for name in kit.namelist()}
    need(flat['README.md']==payload['README.md'] and flat['zenodo-metadata.json']==payload['zenodo-metadata.json'],'Kit prose/metadata changed')
    need(flat['finite-warm-thresholds.pdf']==zdata and flat['finite-warm-thresholds-source-and-verification.zip']==(PUBLICATION/'output/finite-warm-thresholds-source-and-verification.zip').read_bytes(),'Kit upload bytes changed')
    flatnative=strict_json(flat['zenodo-deposit.json'])
    need(flatnative=={'metadata':metadata,'files':[{'path':'finite-warm-thresholds.pdf'},{'path':'finite-warm-thresholds-source-and-verification.zip'}]},'Kit flat deposit differs')
    science=(AUDIT/'ROOT_SCIENTIFIC_CLEARANCE.json').read_bytes();need(sha(science)==SCIENCE_SHA,'Root scientific clearance changed')
    s=strict_json(science)
    need(s['pr']==1131 and s['head']==ORIGINAL and s['scientific_package_accepted'] is True and s['unresolved_substantive_package_issues']==[] and s['frozen_six']==frozen['frozen_six'],'Root scientific acceptance incomplete')
    for name,p in s['root_acceptance_pins'].items():read_pinned(safe(AUDIT,name),p)
    need(sha((AUDIT/'reviews/package01/FINAL_REVIEW_MANIFEST.json').read_bytes())==s['review01_manifest_sha256'],'Review01 manifest changed')
    need(sha((AUDIT/'reviews/package02/MANIFEST.json').read_bytes())==s['review02_manifest_sha256'],'Review02 manifest changed')
    return {'freeze':frozen,'source':payload,'flat':flat,'metadata':metadata}

def proposal():
    data=strict_json((OPS/'INTEGRATION_PROPOSAL.json').read_bytes())
    need(data['pr']==1131 and data['original_head']==ORIGINAL and data['queue_change'] is False,'Wrong integration proposal')
    result={}
    need(len(data['files'])==8,'Exactly current framing3 plus flat preprint5 required')
    for e in data['files']:
        body=read_pinned(safe(OPS,e['proposal_path']),e['after'])
        need(e['repository_path'].startswith(PROBLEM+'/') and e['repository_path'] not in result,'Proposal path outside attempt/duplicate')
        result[e['repository_path']]=body
    need(set(result)=={PROBLEM+'/'+n for n in ['README.md','STATUS.json','MANIFEST.json']}|{PROBLEM+'/preprint/'+n for n in FLAT},'Unexpected exact overlay')
    pkg=package()
    for e in data['files']:
        n=e['repository_path'][len(PROBLEM)+1:]
        need(e['before']==(None if n.startswith('preprint/') else pin(pkg['source']['original/'+n])),'Proposal before pin differs from immutable original')
    for n,b in pkg['flat'].items():need(result[PROBLEM+'/preprint/'+n]==b,'Proposed preprint differs from frozen kit')
    return data,result

def clearance(clearance_sha,operations_sha):
    """Caller supplies both external SHA anchors; this code cannot author clearance."""
    need(re.fullmatch('[a-f0-9]{64}',clearance_sha or '') and re.fullmatch('[a-f0-9]{64}',operations_sha or ''),'Root SHA anchors required')
    manifest=(OPS/'OPERATIONS_MANIFEST.json').read_bytes();need(sha(manifest)==operations_sha,'Operations seal changed')
    m=strict_json(manifest)
    need(m['excluded']==['OPERATIONS_MANIFEST.json','private/','runtime/','__pycache__/'],'Unexpected manifest exclusion policy')
    actual={p.relative_to(OPS).as_posix() for p in OPS.rglob('*') if p.is_file() and not any(x in {'private','runtime','__pycache__'} for x in p.relative_to(OPS).parts) and p.relative_to(OPS).as_posix()!='OPERATIONS_MANIFEST.json'}
    need(actual==set(m['files']),'Unsealed operations file or missing file')
    for n,p in m['files'].items():read_pinned(safe(OPS,n),p)
    cpath=RUNTIME/'ROOT_OPERATIONAL_CLEARANCE.json';raw=cpath.read_bytes();need(sha(raw)==clearance_sha,'Root operational clearance changed')
    c=strict_json(raw)
    need(c['pr']==1131 and c['original_head']==ORIGINAL and c['operations_manifest_sha256']==operations_sha and c['scientific_clearance_sha256']==SCIENCE_SHA and c['freeze_sha256']==FREEZE_SHA and c['publication_ready'] is True and c['unresolved_operational_findings']==[] and c['root_complete_reports_read_and_all_seals_verified'] is True,'Root final operational clearance incomplete')
    need(c['integration_proposal_sha256']==sha((OPS/'INTEGRATION_PROPOSAL.json').read_bytes()),'Proposal not cleared')
    need(set(c['allowed_actions'])<={'integrate','pr-description','ready','merge','stage','publish','ledger'},'Unknown allowed action')
    package();proposal();return c

def command(argv,body=None):
    run=subprocess.run(argv,input=None if body is None else json.dumps(body,ensure_ascii=False).encode(),cwd=REPO,capture_output=True,timeout=60)
    need(run.returncode==0,'Provider operation failed; preserve intent and reconcile; no automatic retry')
    return strict_json(run.stdout)

def gh(endpoint):return command(['gh','api','--hostname','github.com','repos/'+REPOSITORY+'/'+endpoint])
def gws_read():
    v=command(['gws','sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':SHEET,'range':"'Math Puzzles'!A:AQ",'valueRenderOption':'FORMATTED_VALUE'})])
    need(v.get('majorDimension')=='ROWS' and re.fullmatch(r"'Math Puzzles'!A1:AQ[1-9][0-9]*",v.get('range','')) is not None,'Full A:AQ response schema/range changed')
    rows=v.get('values');need(isinstance(rows,list) and rows and rows[0]==HEADERS,'Ledger four-column header changed')
    need(all(isinstance(r,list) and len(r)<=4 and all(isinstance(x,str) for x in r) for r in rows),'Ledger outside exact four-cell schema')
    return v,rows

def validate_pr(pr,head,merged):
    need(re.fullmatch('[a-f0-9]{40}',head or '') and pr['number']==1131 and pr['head']['sha']==head and pr['head']['ref']==BRANCH and pr['head']['repo']['full_name']==REPOSITORY and pr['base']['repo']['full_name']==REPOSITORY and pr['base']['ref']=='main','PR identity/head/base changed')
    need(pr['merged'] is merged and pr['state']==('closed' if merged else 'open'),'Wrong PR merge state')
