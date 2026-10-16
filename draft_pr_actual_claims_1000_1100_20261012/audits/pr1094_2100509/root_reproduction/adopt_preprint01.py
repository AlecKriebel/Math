from pathlib import Path
import json, hashlib, io, zipfile, tempfile, subprocess, os, datetime
A=Path(__file__).resolve().parents[1];P=A/'preprint_v1_0';K=P/'kit'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();require(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p));return b
seal=load(P/'PREPARATION_SEAL.json')
require(sha((P/'OUTPUT_PINS.json').read_bytes())==seal['output_pins_sha256'],'seal mismatch')
outputs=load(P/'OUTPUT_PINS.json')['records']
for r in outputs:check(P/r['path'],r)
baseline=load(P/'FROZEN_INPUT_PINS.json')['records']
for r in baseline:check(A/r['path'],r)
custody=load(K/'CUSTODY_MAP.json');copies=custody['copies'];exclusions=custody['exclusions']
require({r['path'] for r in baseline}=={r['original_path'] for r in copies}|{r['path'] for r in exclusions},'custody not exact partition')
require(len(copies)+len(exclusions)==len(baseline),'duplicate custody row')
for r in copies:require(check(K/r['copy_path'],r)==check(A/r['original_path'],r),'copy differs')
metadata=load(K/'metadata.json');native=load(P/'zenodo-deposit.json')
require(metadata==load(K/'.zenodo.json')==load(K/'metadata_api.json')['metadata']==native['metadata'],'metadata differs')
manifest=load(K/'MANIFEST.json');names=sorted(['MANIFEST.json']+[r['path'] for r in manifest['records']])
for r in manifest['records']:check(K/r['path'],r)
archive=P/'pr1094_supportkit_v1.0.zip'
with zipfile.ZipFile(archive) as z:
    require(z.namelist()==names and z.testzip() is None,'ZIP inventory/CRC')
    for n in names:
        i=z.getinfo(n);require(z.read(n)==(K/n).read_bytes() and i.date_time==(1980,1,1,0,0,0) and i.create_system==3 and i.external_attr==0o100644<<16 and i.compress_type==zipfile.ZIP_STORED,'ZIP bytes/header')
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
    for n in names:
        i=zipfile.ZipInfo(n,(1980,1,1,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_STORED;z.writestr(i,(K/n).read_bytes())
require(buf.getvalue()==archive.read_bytes(),'independent CLOSED ZIP differs')
commands=[];mode_results=[]
with tempfile.TemporaryDirectory(prefix='root-preprint-',dir=Path(__file__).parent) as td:
    td=Path(td).resolve();clean=td/'clean'
    with zipfile.ZipFile(archive) as z:z.extractall(clean)
    protected={n:sha((clean/n).read_bytes()) for n in names}
    def run(flags,args,success=True,cwd=clean):
        argv=['python3','-B',*flags,*args];p=subprocess.run(argv,cwd=cwd,capture_output=True)
        require((p.returncode==0)==success,str(argv)+p.stderr.decode(errors='replace'))
        commands.append({'argv':argv,'exit_code':p.returncode,'expected_success':success,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)})
        return p
    for flags,mode in [([], 'normal'),(['-O'],'optimized')]:
        run(flags,['scripts/verify_kit.py'])
        result=td/('checks-'+mode+'.json');run(flags,['scripts/run_checks.py','--out',str(result)]);mode_results.append(load(result))
        rebuilt=td/(mode+'.zip');run(flags,['scripts/build_support.py','--out',str(rebuilt)])
        require(rebuilt.read_bytes()==archive.read_bytes(),'documented ZIP rebuild differs')
        pdf=td/('pdf-'+mode);run(flags,['scripts/build_pdf.py','--out-dir',str(pdf)])
        require((pdf/'paper.pdf').read_bytes()==(P/'paper.pdf').read_bytes(),'PDF rebuild differs')
        run(flags,['scripts/verify_kit.py','--binding',str(P/'DEPOSIT_BINDING.json'),'--require-binding'])
        run(flags,['scripts/verify_kit.py','--binding',str(td/'absent.json'),'--require-binding'],False)
        alias=td/('paper-hardlink-'+mode);os.link(clean/'paper.tex',alias)
        run(flags,['scripts/build_support.py','--out',str(alias)],False)
        run(flags,['scripts/build_pdf.py','--out-dir',str(clean/'new-pdf'),'--tectonic','absent-root-compiler'],False)
    require(mode_results[0]==mode_results[1],'normal/optimized complete check JSON differs')
    for n,h in protected.items():require(sha((clean/n).read_bytes())==h,'protected extraction changed')
    run([], [str(A.parents[2]/'zenodo_deposit_tool/zenodo.py'),'check',str(P/'zenodo-deposit.json')],cwd=A.parents[2])
pages=[]
for p in sorted(Path(__file__).parent.glob('paper_page-*.png')):
    pages.append({'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'root_actual_view':True})
require(len(pages)==5,'five actual page views required')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
record={'utc':utc,'status':'ROOT_ADOPT_COMPLETE_PREPRINT_PENDING_TWO_NEW_FULL_WHOLE_REVIEWS','pr':1094,'head':'954dd70b49458026e29b8dae63243391249008d8','full_preparation_report_paper_current_scripts_and_native_metadata_read':True,'outputs_rehashed':len(outputs),'prior_inputs_rehashed_unchanged':len(baseline),'exact_copy_pairs':len(copies),'individual_exclusions':len(exclusions),'independent_closed_zip_members':len(names),'normal_optimized_math_full_json_equal':True,'commands':commands,'paper_actual_page_views':pages,'proof_scope':'Complete real-spectrum compact-support classification in commuting local frame, all n>=1; credited prior nonreal obstruction, semisimple/2D, local point and regular-layer interfaces; full-result/method priority UNKNOWN.','new_whole_reviews_completed':0,'minimum_new_whole_reviews':2,'publication_ready':False,'published':False,'services_held_after_pr':1032,'output_pins_sha256':sha((P/'OUTPUT_PINS.json').read_bytes()),'preparation_seal_sha256':sha((P/'PREPARATION_SEAL.json').read_bytes()),'pdf_sha256':sha((P/'paper.pdf').read_bytes()),'zip_sha256':sha(archive.read_bytes())}
(A/'ROOT_PREPRINT_REVIEW_01.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS','utc':utc,'outputs':len(outputs),'prior_inputs':len(baseline),'copies':len(copies),'zip_members':len(names),'commands':len(commands),'pdf_sha256':record['pdf_sha256']}))
