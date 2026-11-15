"""Root-authorized exact sealed overlay installation; no rendering or source edits."""
from pathlib import Path
import datetime, hashlib, json, re, shutil, subprocess, xml.etree.ElementTree as ET

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O=Path(__file__).resolve().parent
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
PUB=W/'public'
E=P/'verification/local-banach-mtp2-stage-sol-20261025/resume'
A=P/'verification/banach-mtp2-independent-code-audit-sol-20261114'
PL=P/'verification/banach-mtp2-next-stage-plan-sol-20261025'
H=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def need(ok,message):
    if not ok: raise RuntimeError(message)
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(f): return json.loads(f.read_bytes())
def save(name,value): (O/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def bindings(rows,root=None):
    for r in rows:
        f=(root/r['path']) if root else Path(r['path'])
        need(f.is_file() and not f.is_symlink() and f.stat().st_size==r['bytes'] and H(f)==r['sha256'],'binding '+str(f))

need(not (O/'installation.json').exists(),'already installed; inspect receipt before continuing')
need(H(E/'SEAL.json')=='c697767fba940a0a36c38dd2aafa68097d0af34243953b04b213958ce2a57487','writer final seal')
need(H(A/'SEAL.json')=='ace00c06f5caeb3adbb3e4bad3d2d2c1657608f9f090849092e3371e900b680d','independent audit seal')
for d,m in [(E,'OWNED_MANIFEST.json'),(A,'MANIFEST.json'),(PL,'MANIFEST.json')]:
    s=read(d/'SEAL.json');need(H(d/m)==s['manifest_sha256'],'manifest seal '+str(d));bindings(read(d/m)['files'],d)
bindings(read(PL/'IMMUTABLE_INPUT_BINDINGS.json')['files'])
base=read(E.parent/'BASELINE_ACTUAL_524.json')
bindings(base['public_files']);bindings(base['actual_installed_core'])
need(len(base['public_files'])==524 and len(base['actual_installed_core'])==16,'baseline cardinalities')
need({str(f) for f in PUB.rglob('*') if f.is_file()}=={r['path'] for r in base['public_files']},'exact old public file set')
need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=W,text=True).strip()=='262f0f4f3eafd513e1bd549960020678307d6c67','website base HEAD')
need(subprocess.check_output(['git','branch','--show-current'],cwd=W,text=True).strip()=='master','website branch')
code=[('banach_mtp2_source.py',P/'scripts/banach_mtp2_source.py','2d6be6eb82dfc8bd81b057ad8bed23bdfa620f74af5292d1ebdaa4ebead138be'),('bm_body_contract.py',P/'scripts/bm_body_contract.py','d62fe7a698e95f65aaceb8a2b3a1c8e1861a4721a44f3f26905f2c344497f237'),('render_page.proposed.py',P/'scripts/render_page.py','9a344833d70bc840b5df125873e0db631ce81e55499e0d0279895e2b2f96be70'),('final-content-check.proposed.py',P/'verification/final-content-check.py','6eebcd5a0c8e9aa35afa7a9cdc1b9a6ccf3c47fbc162d374004169c3b0e2a6dc')]
for name,dest,pin in code: need(H(E/name)==pin,'exact approved code '+name)
need(all(not d.exists() for _,d,_ in code[:2]),'new helper destinations absent')
overlay=sorted(f for f in (E/'public').rglob('*') if f.is_file())
need(len(overlay)==10,'ten public overlay files')
old_index=(PUB/'research/index.html').read_text();new_index=(E/'public/research/index.html').read_text()
old_items=re.findall(r'<li\b[^>]*>.*?</li>',old_index,re.S)
new_items=re.findall(r'<li\b[^>]*>.*?</li>',new_index,re.S)
need(len(old_items)==70 and len(new_items)==72,'index list counts')
need([x for x in new_items if x in old_items]==old_items and all(new_items.count(x)==1 for x in old_items),'all70 full old index entries exactly preserved in order')
old_sitemap=ET.parse(PUB/'research/sitemap.xml').getroot();new_sitemap=ET.parse(E/'public/research/sitemap.xml').getroot()
old_nodes=[ET.tostring(x) for x in old_sitemap];new_nodes=[ET.tostring(x) for x in new_sitemap]
need(len(old_nodes)==71 and len(new_nodes)==73 and [x for x in new_nodes if x in old_nodes]==old_nodes,'all71 complete sitemap nodes preserved in order')
roots={}
for rid,pin in [('23217863','b8f379a432a6866d611b929b8c91a410312a36943b99051574edc135598b280a'),('23146753','9f03be990c7b547ebc341908662b241f84b77ffb9b26f9d834d72407d34b7860')]:
    f=P/('verification/root-clearance-'+rid+'-20261025.json');need(H(f)==pin,'original root science '+rid)
    ef=P/('verification/root-editorial-'+rid+'-20261025.json')
    roots[rid]={'science_sha256':H(f),'science_original':read(f),'editorial_sha256':H(ef),'editorial_original':read(ef)}
copies=[{'source':str(E/name),'destination':str(d),'bytes':(E/name).stat().st_size,'sha256':pin} for name,d,pin in code]
copies += [{'source':str(f),'destination':str(PUB/f.relative_to(E/'public')),'bytes':f.stat().st_size,'sha256':H(f)} for f in overlay]
need(len(copies)==14 and len({r['destination'] for r in copies})==14,'fourteen distinct destinations')
save('root-adoption.json',{'utc':now(),'status':'ROOT_APPROVED_EXACT_TWO_RECORD_14_PATH_INSTALLATION','records':['23217863','23146753'],'writer_seal_sha256':H(E/'SEAL.json'),'independent_auditor_seal_sha256':H(A/'SEAL.json'),'writer_verdict_original':read(E/'VERDICT.json'),'independent_auditor_verdict_original':read(A/'VERDICT.json'),'root_original_authorities':roots,'root_prior_full_read_confirmed':['source helper, body contract, renderer diff and checker diff','complete writer and independent auditor reports, literal custom verdicts and read-only verifiers','both complete actual rendered article bodies; qualifications, credit, license, status, collaboration and absent follow-ups','both root-adopted bounded negative legacy dispositions'],'actual_read_only_closure_runs_completed_before_install':True,'old_campaigns_not_repeated':True,'historical_private_flags_preserved':True,'whole_native_objects_preserved':True,'follow_up':None,'authorized_copies':copies,'later_live_browser_download_and_native_gates_pending':True,'canonical_tracker_write_authorized':False,'eligible_work_total':203,'all203_complete':False})
save('pre-installation.json',{'utc':now(),'public_baseline':base['public_files'],'core_baseline':base['actual_installed_core'],'website_head':base['website_commit_read_only_observed'],'copies':copies})
for r in copies:
    d=Path(r['destination']);d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(r['source'],d)
    need(d.stat().st_size==r['bytes'] and H(d)==r['sha256'],'installed bytes '+str(d))
public_dest={r['destination'] for r in copies if Path(r['destination']).is_relative_to(PUB)}
old_public={r['path'] for r in base['public_files']}
need(len(public_dest-old_public)==8,'eight new article files')
actual={str(f) for f in PUB.rglob('*') if f.is_file()}
need(actual==old_public|public_dest and len(actual)==532,'exact integrated public file set')
unchanged=[r for r in base['public_files'] if r['path'] not in public_dest];bindings(unchanged)
need(len(unchanged)==522,'522 unrelated public files exact')
core_dest={str(d) for _,d,_ in code}
unchanged_core=[r for r in base['actual_installed_core'] if r['path'] not in core_dest];bindings(unchanged_core)
need(len(unchanged_core)==14,'fourteen old core files exact')
receipt={'utc':now(),'status':'PASS_ROOT_EXACT14_SEALED_INSTALLATION','copies':copies,'new_public_files':8,'total_public_files':532,'all522_other_public_files_unchanged':True,'all14_other_old_core_files_unchanged':True,'all70_complete_old_index_entries_preserved_in_order':True,'all71_complete_old_sitemap_entries_preserved_in_order':True,'index_items':72,'sitemap_entries':73,'unrelated_public_homepage_sha256':H(PUB/'index.html'),'no_original_paper_or_review_config_edits':True,'all203_complete':False}
save('installation.json',receipt)
print(json.dumps({k:v for k,v in receipt.items() if k!='copies'},indent=2))
