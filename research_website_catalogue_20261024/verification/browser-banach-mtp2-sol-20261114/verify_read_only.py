"""Read-only custody and measured-observation verifier; no browser actions."""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)
seal=json.loads((E/'SEAL.json').read_bytes());require(H(E/'MANIFEST.json')==seal['manifest_sha256'],'manifest seal')
manifest=json.loads((E/'MANIFEST.json').read_bytes())
for r in manifest['files']:
    p=E/r['path'];require(p.resolve().is_relative_to(E) and p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'] and H(p)==r['sha256'],'binding '+r['path'])
require({str(p.relative_to(E)) for p in E.rglob('*') if p.is_file()}-{'SEAL.json','MANIFEST.json'}=={r['path'] for r in manifest['files']},'owned file set')
v=json.loads((E/'VERDICT.json').read_bytes());require(len(v['targets'])==2 and v['screenshots_native_JPEG_count']==13,'scope')
saved=[]
for x in v['targets']:
    m=x['mobile_viewport'];require(m['innerWidth']==m['clientWidth']==m['scrollWidth']==390 and m['innerHeight']==844 and m['iframeRect'][0]['width']==374 and m['overflowX']=='visible','mobile measurements')
    require(x['desktop_viewport']['scrollWidth']==x['desktop_viewport']['clientWidth'] and len(x['iframe'])==1,'desktop/frame')
    require(x['native_reader_total_pages_personally_visible']==({'23217863':7,'23146753':5}[x['record_id']]),'native reader count')
    saved.extend(z['nativeSavedPath'] for z in x['native_local_downloads'])
require(len(saved)==len(set(saved))==4 and all(Path(p).is_absolute() for p in saved),'native saved path receipts')
require(all(p.read_bytes().startswith(b'\xff\xd8\xff') for p in E.glob('*.jpg')) and len(list(E.glob('*.jpg')))==13,'actual JPEG bytes')
index=v['actual_index_click_destinations'];require(index['viewportOverrideReset'] and index['indexBmDestination']==v['targets'][0]['canonical_url'] and index['indexMtpDestination']==v['targets'][1]['canonical_url'],'actual index clicks/reset')
print(json.dumps({'status':'PASS_BROWSER_EVIDENCE_CUSTODY','owned_bindings':len(manifest['files']),'native_JPEG_screenshots':13,'measured_mobile_width':390,'native_PDF_total_pages':[7,5],'actual_native_download_path_receipts':saved,'downloaded_byteidentity_comparison':'Pending root-owned closure; not performed by this verifier.','browser_lane_released':True},indent=2))
