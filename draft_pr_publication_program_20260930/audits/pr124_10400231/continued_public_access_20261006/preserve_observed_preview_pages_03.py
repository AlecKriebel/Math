"""Preserve observed page20; record page19 as a failed placeholder, never as source text."""
from pathlib import Path
import datetime,hashlib,json,os
D=Path(__file__).resolve().parent;S=D/'private_sources'
root=Path('/var/folders/cp/bbqcpp814bjd_6mfhk6lxf7r0000gn/T/browser-use/assets/e5ec260a-d66f-4a83-ba71-076d4aaebcbf')
out=D/'ACTUAL_PREVIEW_PAGES_03.json'
if out.exists():raise RuntimeError('Prior actual receipt exists')
raw=(root/'manifest.json').read_bytes();m=json.loads(raw)
md=S/('bundle_'+root.name+'_manifest.json')
if md.exists():raise RuntimeError('Prior bundle manifest exists')
md.write_bytes(raw);events=[]
for x in m['assets']:
 b=Path(x['path']).read_bytes()
 if x['id']=='edf5e0bfe04e44f6':
  dest=S/'turaev2002_PA20.png';valid=True;page=20
 elif x['id']=='416209bfe7658592':
  dest=S/'turaev2002_PA19_UNAVAILABLE_PLACEHOLDER.png';valid=False;page=19
 else:raise RuntimeError('Unexpected observed asset')
 if dest.exists():raise RuntimeError('Prior source exists')
 dest.write_bytes(b)
 events.append({'printed_page_requested':page,'valid_primary_page_pixels':valid,'root_full_pixels_read':True,'source_asset_id':x['id'],'source_export_path':x['path'],'private_local_path':str(dest),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'public_permalink':'https://books.google.com/books?id=83ZJs9Z9BY0C&pg=PA'+str(page),'bundle_manifest_sha256':hashlib.sha256(raw).hexdigest()})
r={'schema':'pr124-observed-public-preview-page-preservation/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'events':events,'available_primary_pages':[20],'unavailable_primary_pages':[19],'UI_limit_message':'You have either reached a page that is unavailable for viewing or reached your viewing limit for this book.','page19_image_text':'image not available','navigation_stopped_after_limit_observed':True,'no_access_control_bypass':True,'copyrighted_images_kept_private':True,'shared_tracked_or_service_mutations':False,'priority_or_publication_clearance':False}
out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print(json.dumps({'PID':os.getpid(),'UTC':r['UTC'],'valid_primary_page20':True,'page19_unavailable_placeholder':True}))

