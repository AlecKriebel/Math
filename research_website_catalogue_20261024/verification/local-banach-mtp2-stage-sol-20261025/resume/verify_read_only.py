"""Verify sealed private payload/custody/current production; performs no writes."""
from pathlib import Path
import hashlib, json, re, subprocess, sys
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;OLD=E.parent;P=OLD.parents[1];PL=P/'verification/banach-mtp2-next-stage-plan-sol-20261025';LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
H=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)
def bindings(rows,root=None):
    for row in rows:
        f=(root/row['path']) if root else Path(row['path'])
        require(f.is_file() and not f.is_symlink() and f.stat().st_size==row['bytes'] and H(f)==row['sha256'],'binding changed '+str(f))
seal=json.loads((E/'SEAL.json').read_bytes());require(H(E/'OWNED_MANIFEST.json')==seal['manifest_sha256'],'owned manifest seal')
manifest=json.loads((E/'OWNED_MANIFEST.json').read_bytes());bindings(manifest['files'],E)
owned={str(p.relative_to(E)) for p in E.rglob('*') if p.is_file()}-{'OWNED_MANIFEST.json','SEAL.json'}
require(owned=={x['path'] for x in manifest['files']},'exact owned file set')
preserved=json.loads((E/'PRESERVED_PREDECESSOR.json').read_bytes());bindings(preserved['files'])
ps=json.loads((PL/'SEAL.json').read_bytes());require(H(PL/'MANIFEST.json')==ps['manifest_sha256'],'planning seal');pm=json.loads((PL/'MANIFEST.json').read_bytes());bindings(pm['files'],PL)
immutable=json.loads((PL/'IMMUTABLE_INPUT_BINDINGS.json').read_bytes());bindings(immutable['files'])
base=json.loads((OLD/'BASELINE_ACTUAL_524.json').read_bytes());bindings(base['public_files']);bindings(base['actual_installed_core'])
actual={str(p) for p in LIVE.rglob('*') if p.is_file()};require(actual=={r['path'] for r in base['public_files']},'production file set changed')
require(subprocess.check_output(['git','-C',str(LIVE.parent),'rev-parse','HEAD'],text=True).strip()==base['website_commit_read_only_observed'],'website HEAD changed')
overlay=E/'public';files=[p for p in overlay.rglob('*') if p.is_file()];require(len(files)==10,'overlay ten files')
index=(overlay/'research/index.html').read_text();sitemap=(overlay/'research/sitemap.xml').read_text();require(len(re.findall(r'<li><a href="/research/[^"/]+/">',index))==72,'index72');require(sitemap.count('<loc>')==73,'sitemap73')
for mode in ['normal','optimized']:
    fault=json.loads((E/('FAULTS_'+mode+'.json')).read_bytes());require(fault['status']=='PASS' and fault['case_count']==fault['passed']==204,'fault suite '+mode)
    require(all(H(E/name)==pin for name,pin in fault['code_bindings'].items()),'fault code bindings '+mode)
    target=json.loads((E/('target-final-'+mode+'.json')).read_bytes());require(target['status']=='PASS' and set(target['papers'])=={'23217863','23146753'},'target positive '+mode)
compat=json.loads((E/'COMPATIBILITY.json').read_bytes());require(compat['status']=='PASS' and compat['old_content_suite_runs']==1 and compat['paired_renderer_processes']==138 and len(compat['renderer_comparisons'])==69 and all(x['full_output_bytes_equal'] for x in compat['renderer_comparisons']),'bounded compatibility')
require(not (E/'compatibility-scratch').exists(),'no retained legacy tree')
print(json.dumps({'status':'PASS_PRIVATE_STAGE_SEALED_PRODUCTION_UNCHANGED','owned_bindings':len(manifest['files']),'plan_owned_bindings':len(pm['files']),'immutable_input_bindings':len(immutable['files']),'production_public_files':len(actual),'core_bindings':len(base['actual_installed_core']),'private_overlay_files':10,'hypothetical_integrated_files':532,'index_items':72,'sitemap_entries':73,'production_adoption':False,'browser_mobile_PDF_download_native_sheet_live_gates':False},indent=2))
