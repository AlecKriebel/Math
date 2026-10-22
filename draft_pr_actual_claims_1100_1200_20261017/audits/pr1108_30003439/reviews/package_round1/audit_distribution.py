#!/usr/bin/env python3
"""Read-only frozen package audit; all outputs stay under this review folder."""
from pathlib import Path, PurePosixPath
from hashlib import sha256
from datetime import datetime, timezone
import json, zipfile, subprocess, sys
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
PUB=ROOT/'publication'
TMP=OUT/'tmp'
checks=[]
def check(ok,label):
    if not ok: raise RuntimeError(label)
    checks.append(label)
def desc(b):return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
receipt=json.loads((PUB/'PACKAGE_RECEIPT.json').read_text())
frozen={'output/pdf/negative-curvature-cone.pdf':'ad9864c08642737e4459673749c1db6d2e3dafb521f323fb1071f157f8110eb0','output/negative-curvature-cone-source-and-verification.zip':'d97ba7ed1057518e3bd499d88182c64767e912d589ed8574092c0ebc7a27c06e','output/zenodo-upload-kit.zip':'0f52fdfc42cc83e4739ca5de9cabda5120565c3d48cbb4457a0da9ab7ce1bd76'}
for name,h in frozen.items():check(desc((PUB/name).read_bytes())['sha256']==h,'Frozen '+name)
for name,d in receipt['files'].items():check(desc((PUB/name).read_bytes())==d,'Receipt '+name)
source=PUB/'output/negative-curvature-cone-source-and-verification.zip'
with zipfile.ZipFile(source) as z:
    names=z.namelist()
    expected_names={'LICENSE.txt','PROVENANCE.json','README.md','SOURCE_MANIFEST.json','main.tex','output/pdf/negative-curvature-cone.pdf','verification/check_geometry.py','verification/curvature_reproduction.py','verification/expected_results.json','audits/ROOT_MATHEMATICAL_CHECK.md','audits/ROOT_PRIORITY_CHECK.md','audits/curvature_01/ADVERSARIAL_REPORT.md','audits/curvature_01/execution.json','audits/curvature_01/results.json','audits/geometry_01/REPORT.md','audits/geometry_01/SOURCES.json','audits/geometry_01/results.json','audits/geometry_01/results_optimized.json','audits/priority_01/PRIORITY_AUDIT.md','audits/priority_01/SEARCH_LEDGER.md','audits/priority_01/SOURCE_LEDGER.json','audits/priority_01/SOURCE_LEDGER.md','audits/priority_01/additional_retrieval_metadata.json','audits/priority_01/remainder_check.txt','audits/priority_01/retrieval_metadata.json','audits/priority_01/supplemental_retrieval_metadata.json'}
    check(set(names)==expected_names,'Independent 26-member source allowlist')
    check(len(names)==len(set(names)),'No duplicate source members')
    check(all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names),'No unsafe source names')
    check(z.testzip() is None,'All source CRCs')
    members={n:z.read(n) for n in names}
    manifest=json.loads(members['SOURCE_MANIFEST.json'])
    check(set(names)==set(manifest)|{'SOURCE_MANIFEST.json'},'Exact source manifest membership')
    check(manifest==receipt['source_members'],'Receipt/source manifest agreement')
    for n,d in manifest.items():check(desc(members[n])==d,'Manifest '+n)
    for n in ['main.tex','README.md','LICENSE.txt','output/pdf/negative-curvature-cone.pdf','verification/check_geometry.py','verification/curvature_reproduction.py','verification/expected_results.json']:
        check(members[n]==(PUB/n).read_bytes(),'Working/package parity '+n)
    for n,raw in members.items():
        if n.startswith('audits/'):
            rel=n[len('audits/'):]
            local=ROOT/rel if rel.startswith('ROOT_') else ROOT/'reviews'/rel
            check(raw==local.read_bytes(),'Distributed audit binding '+n)
    provenance=json.loads(members['PROVENANCE.json'])
    check(provenance['source_head_sha']=='148130ab93ab46a3459d7bc98a11a1ca79052d65','Pinned PR head')
    check(provenance['source_head_sha']==json.loads((ROOT/'input/PR_SNAPSHOT.json').read_text())['head']['sha'],'Provenance matches frozen snapshot')
    check(provenance['source_proof_sha256']==desc((ROOT/'input/PROOF.md').read_bytes())['sha256'],'Pinned input proof')
    for n in names:
        target=TMP/'unpacked'/n
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(members[n])
with zipfile.ZipFile(PUB/'output/zenodo-upload-kit.zip') as z:
    names=z.namelist()
    check(len(names)==len(set(names)),'No duplicate kit members')
    check(set(names)=={'negative-curvature-cone.pdf',source.name,'README.md','zenodo-metadata.json','zenodo-deposit.json'},'Exact kit membership')
    check(z.testzip() is None,'All kit CRCs')
    check(z.read('negative-curvature-cone.pdf')==members['output/pdf/negative-curvature-cone.pdf'],'Kit PDF exact bytes')
    check(z.read(source.name)==source.read_bytes(),'Kit source ZIP exact bytes')
    check(z.read('README.md')==members['README.md'],'Kit README exact bytes')
    check(z.read('zenodo-metadata.json')==(PUB/'zenodo-metadata.json').read_bytes(),'Kit metadata exact bytes')
    kd=json.loads(z.read('zenodo-deposit.json'))
metadata=json.loads((PUB/'zenodo-metadata.json').read_text())
deposit=json.loads((PUB/'zenodo-deposit.json').read_text())
check(metadata==deposit['metadata']==kd['metadata'],'Three metadata copies equal')
check(deposit['files']==[{'path':'output/pdf/negative-curvature-cone.pdf'},{'path':'output/'+source.name}],'Repository deposit paths')
check(kd['files']==[{'path':'negative-curvature-cone.pdf'},{'path':source.name}],'Portable deposit paths')
for field,value in {'upload_type':'publication','publication_type':'preprint','version':'1.0.0','license':'cc-by-4.0','publication_date':'2026-10-17'}.items():check(metadata[field]==value,'Metadata '+field)
check(metadata['creators'][0]['orcid']=='0009-0001-9320-500X','Author ORCID')
expected=json.loads(members['verification/expected_results.json'])
runs=[]
for name,opt in [('check_geometry.py',False),('check_geometry.py',True),('curvature_reproduction.py',False),('curvature_reproduction.py',True)]:
    args=[sys.executable,'-B']+(['-O'] if opt else [])+[str(TMP/'unpacked/verification'/name)]
    p=subprocess.run(args,text=True,capture_output=True)
    suffix=name.removesuffix('.py')+('_optimized' if opt else '')
    (OUT/(suffix+'.stdout.json' if p.returncode==0 else suffix+'.stderr.txt')).write_text(p.stdout if p.returncode==0 else p.stderr)
    runs.append({'name':name,'optimized':opt,'returncode':p.returncode})
    if name=='curvature_reproduction.py' and opt:
        check(p.returncode!=0 and 'requires enabled assertions' in p.stderr,'Curvature -O explicitly rejects')
    else:
        check(p.returncode==0,'Run '+suffix)
        value=json.loads(p.stdout)
        if name=='check_geometry.py':
            stable={k:v for k,v in value.items() if k not in {'checked_at_utc','python_version','optimization_mode'}}
            check(value['checks_passed']==791 and value['negative_controls_rejected']==8,'All 791 geometry checks and 8 controls '+suffix)
            check(stable==expected['geometry'],'Stable expectation '+suffix)
        else:
            check({k:v for k,v in value.items() if k!='python'}==expected['curvature'],'Stable curvature expectations')
# Mutations target actual distributed code, not merely independent shadow formulas.
mutants=[('check_geometry.py','B[0][0]=2*(t-1)**2*(t+2)','B[0][0]=3*(t-1)**2*(t+2)','geometry_matrix_corruption'),('check_geometry.py','+2*t**3\nB[1][2]','+3*t**3\nB[1][2]','geometry_second_diagonal_corruption'),('curvature_reproduction.py','nc13=6*(t-1)','nc13=5*(t-1)','curvature_matrix_corruption'),('curvature_reproduction.py','3*(t-1)**3*(8*t**2+13*t+3)','3*(t-1)**3*(8*t**2+13*t+4)','curvature_square_corruption')]
mutations=[]
for name,old,new,label in mutants:
    raw=members['verification/'+name].decode()
    check(raw.count(old)==1,'Unique mutation target '+label)
    target=TMP/(label+'.py');target.write_text(raw.replace(old,new))
    opts=[False,True] if name=='check_geometry.py' else [False]
    for opt in opts:
        p=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(target)],text=True,capture_output=True)
        check(p.returncode!=0,'Mutation rejected '+label+str(opt))
        mutations.append({'label':label,'optimized':opt,'returncode':p.returncode,'diagnostic':p.stderr.splitlines()[-1]})
repacked=[]
for original in [source,PUB/'output/zenodo-upload-kit.zip']:
    target=TMP/('repacked-'+original.name)
    with zipfile.ZipFile(original) as a,zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as b:
        for n in sorted(a.namelist()):
            i=zipfile.ZipInfo(n,date_time=(2026,10,17,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o644<<16
            b.writestr(i,a.read(n))
    check(original.read_bytes()==target.read_bytes(),'Independent deterministic repack '+original.name)
    repacked.append({'name':original.name,**desc(target.read_bytes()),'byte_identical':True})
result={'repacked_archives':repacked,'status':'PASS','checked_at_utc':datetime.now(timezone.utc).isoformat(),'checks_passed':len(checks),'checks':checks,'runs':runs,'mutations':mutations,'frozen_hashes':frozen,'source_members':len(members),'kit_members':5,'unpacked_path':str(TMP/'unpacked')}
(OUT/'distribution_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'checks','mutations'}},indent=2))
