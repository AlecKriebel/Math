from pathlib import Path
import json,hashlib,zipfile,io,stat,subprocess
R=Path(__file__).resolve().parents[2]
W=Path(__file__).resolve().parent
P=R/'preprint_v1_0'
def require(c,m):
    if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def check_rows(rows,root):
    for x in rows:
        p=root/x['path'];b=p.read_bytes()
        require(len(b)==x['bytes'] and sha(b)==x['sha256'],'pin mismatch '+str(p))
    return len(rows)
counts={}
counts['current_outputs']=check_rows(load(P/'CURRENT_OUTPUT_PINS.json')['entries'],P)
counts['current_all_files']=check_rows(load(R/'repairs/package01/FINAL_CURRENT_PINS.json')['records'],P)
counts['original_preparation_inputs']=check_rows(load(P/'INPUT_PINS.json')['records'],R)
counts['repair_outputs']=check_rows(load(R/'repairs/package01/OUTPUT_PINS.json')['entries'],R/'repairs/package01')
counts['whole01_outputs']=check_rows(load(R/'reviews/package_01/OUTPUT_PINS.json')['entries'],R/'reviews/package_01')
copies=load(P/'COPY_MAP.json')['copies'];counts['copies']=len(copies)
require(copies==load(P/'SAFE_INPUT_PINS.json')['records'],'copy/input-pin equality')
require(copies[:72]==load(R/'repairs/package01/before/preprint_v1_0/COPY_MAP.json')['copies'],'old72 copy records altered')
for x in copies:
    source=R/x['source_path'];dest=P/x['package_path'];b=source.read_bytes()
    require(b==dest.read_bytes() and len(b)==x['bytes'] and sha(b)==x['sha256'],'source copy mismatch '+x['package_path'])
require(sum(x['source_path'].startswith('submitted/') for x in copies)==9,'nine originals not covered')
current=load(P/'CURRENT_STATUS.json');status=load(P/'STATUS.json')
require(current['publication_ready'] is False and current['issues_updated'] is False and current['whole_package_reviews_completed']==1,'current stage altered')
require(status['publication_ready'] is False and status['whole_package_reviews_completed']==0,'old stage altered')
meta=load(P/'metadata.json')
require(meta==load(P/'publication/zenodo.json')['metadata']==load(P/'publication/release_metadata.json')['metadata'],'metadata normalization')
binding=load(P/'publication/DEPOSIT_BINDING.json')
for k,name in [('paper_pdf','paper.pdf'),('support_archive','support.zip')]:
    b=(P/name).read_bytes();require(binding[k]=={'path':name,'bytes':len(b),'sha256':sha(b)},'external binding '+k)
allow=load(P/'SUPPORT_ALLOWLIST.json')['members'];entries=load(P/'SUPPORT_MANIFEST.json')['entries']
require(allow==sorted(set(allow)),'allowlist sorted unique')
require([x['path'] for x in entries]==[x for x in allow if x!='SUPPORT_MANIFEST.json'],'manifest exact coverage')
check_rows(entries,P)
for name in allow:
    f=P/name;require(stat.S_ISREG(f.lstat().st_mode) and not f.is_symlink(),'nonregular '+name)
    if name!='paper.pdf':f.read_bytes().decode('utf-8')
with zipfile.ZipFile(P/'support.zip') as z:
    require(z.namelist()==allow,'ZIP member order')
    for i in z.infolist():
        require(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==(0o100644<<16),'ZIP header mismatch '+i.filename)
        require(i.compress_type==zipfile.ZIP_DEFLATED and not(i.flag_bits&1),'ZIP compression/encryption')
        require(z.read(i)==(P/i.filename).read_bytes(),'ZIP byte mismatch '+i.filename)
    require(z.testzip() is None,'ZIP CRC failure')
    counts['zip_members']=len(allow)
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
    for name in allow:
        i=zipfile.ZipInfo(name,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_DEFLATED;i.internal_attr=0
        z.writestr(i,(P/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
require(buf.getvalue()==(P/'support.zip').read_bytes(),'independent closed ZIP differs')
q=subprocess.run(['python3','-I','-B','resolve_preparation_stage.py'],cwd=R/'repairs/package01',capture_output=True,text=True)
require(q.returncode==0,'103-stage resolver failed')
resolution=json.loads(q.stdout);require(resolution['original_output_records']==103,'old103 resolution count')
for x in resolution['records']:
    b=(R/x['resolved_path']).read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'old103 resolved bytes differ')
counts['historical_preparation_output_records']=103
(W/'HISTORICAL_103_PIN_RESOLUTION.json').write_text(json.dumps(resolution,indent=2)+'\n')
summary={'pass':True,'counts':counts,'independent_closed_zip_byte_identical':True,'pdf_sha256':sha((P/'paper.pdf').read_bytes()),'archive_sha256':sha((P/'support.zip').read_bytes()),'all_source_equal_copies':True,'metadata_objects_identical':True,'dated_old_stages_preserved':True,'new_separate_pending_stage':True}
(W/'DISTRIBUTION_INTEGRITY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
