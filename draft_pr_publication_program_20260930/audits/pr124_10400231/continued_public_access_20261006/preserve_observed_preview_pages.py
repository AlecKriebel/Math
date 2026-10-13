"""Copy unmodified licensed preview images exported by the browser pageAssets tool."""
from pathlib import Path
import datetime,hashlib,json,os,re,urllib.parse
D=Path(__file__).resolve().parent;S=D/'private_sources';S.mkdir(exist_ok=True)
roots=[Path('/var/folders/cp/bbqcpp814bjd_6mfhk6lxf7r0000gn/T/browser-use/assets/d2b3d786-72a9-4da8-aaf5-e8daf74554b0'),Path('/var/folders/cp/bbqcpp814bjd_6mfhk6lxf7r0000gn/T/browser-use/assets/c9183a9f-db64-4a3e-b886-7386dc7a9e95')]
out=D/'ACTUAL_PREVIEW_PAGES_01.json'
if out.exists():raise RuntimeError('Preserved actual page set already exists')
events=[]
for root in roots:
 m=root/'manifest.json';raw=m.read_bytes();x=json.loads(raw)
 (S/('bundle_'+root.name+'_manifest.json')).write_bytes(raw)
 assets=x.get('assets')
 if not isinstance(assets,list):raise RuntimeError('Actual manifest schema not expected')
 for item in assets:
  url=item['url'];q=urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
  if q.get('id')!=['83ZJs9Z9BY0C']:raise RuntimeError('Wrong observed book')
  page=q['pg'][0]
  if page not in ['PA22','PA23','PA45','PA46']:raise RuntimeError('Unexpected observed page')
  src=Path(item['path']);b=src.read_bytes()
  if not b.startswith(b'\x89PNG\r\n\x1a\n'):raise RuntimeError('Non-image preview response')
  dest=S/('turaev2002_'+page+'.png')
  if dest.exists():raise RuntimeError('Prior source image exists')
  dest.write_bytes(b)
  events.append({'printed_page':int(page[2:]),'source_book_id':'83ZJs9Z9BY0C','source_asset_id':item['id'],'source_export_path':str(src),'unmodified_local_path':str(dest),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'public_permalink':'https://books.google.com/books?id=83ZJs9Z9BY0C&pg='+page,'bundle_manifest_bytes':len(raw),'bundle_manifest_sha256':hashlib.sha256(raw).hexdigest(),'copied_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()})
receipt={'schema':'pr124-observed-public-preview-page-preservation/v1','actual_operator_PID':os.getpid(),'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'events':events,'full_pixels_read_by_root_before_copy':[22,23,45,46],'copied_images_unmodified':True,'no_access_control_bypass':True,'only_browser_exported_observed_assets':True,'publisher_permission_banner_observed':True,'copyrighted_images_kept_private':True,'entire_book_obtained':False,'shared_tracked_or_service_mutations':False,'priority_or_publication_clearance':False}
out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(json.dumps({'PID':os.getpid(),'UTC':receipt['UTC'],'pages':[x['printed_page'] for x in events],'copied_images_unmodified':True}))
