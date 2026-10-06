"""Preserve only unmodified, already observed publisher-permitted preview images."""
from pathlib import Path
import datetime,hashlib,json,os,urllib.parse
D=Path(__file__).resolve().parent;S=D/'private_sources'
roots=[Path('/var/folders/cp/bbqcpp814bjd_6mfhk6lxf7r0000gn/T/browser-use/assets/e192974c-0339-4885-8fab-b50405df2a71'),Path('/var/folders/cp/bbqcpp814bjd_6mfhk6lxf7r0000gn/T/browser-use/assets/cca8b517-ede0-475b-a390-82fe2d55ee6b')]
out=D/'ACTUAL_PREVIEW_PAGES_02.json'
if out.exists():raise RuntimeError('Prior actual receipt exists')
events=[]
for root in roots:
 raw=(root/'manifest.json').read_bytes(); x=json.loads(raw)
 manifest_dest=S/('bundle_'+root.name+'_manifest.json')
 if manifest_dest.exists():raise RuntimeError('Prior bundle manifest exists')
 manifest_dest.write_bytes(raw)
 for item in x['assets']:
  q=urllib.parse.parse_qs(urllib.parse.urlparse(item['url']).query)
  if q.get('id')!=['83ZJs9Z9BY0C']:raise RuntimeError('Wrong observed book')
  page=q['pg'][0]
  if page not in ['PA26','PA27','PA28','PA114','PA118']:raise RuntimeError('Unexpected observed page')
  src=Path(item['path']); b=src.read_bytes()
  if not b.startswith(b'\x89PNG\r\n\x1a\n'):raise RuntimeError('Non-PNG response')
  dest=S/('turaev2002_'+page+'.png')
  if dest.exists():raise RuntimeError('Prior source exists')
  dest.write_bytes(b)
  events.append({'printed_page':int(page[2:]),'source_book_id':'83ZJs9Z9BY0C','source_asset_id':item['id'],'source_export_path':str(src),'unmodified_local_path':str(dest),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'public_permalink':'https://books.google.com/books?id=83ZJs9Z9BY0C&pg='+page,'bundle_manifest_bytes':len(raw),'bundle_manifest_sha256':hashlib.sha256(raw).hexdigest(),'copied_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()})
receipt={'schema':'pr124-observed-public-preview-page-preservation/v1','actual_operator_PID':os.getpid(),'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'events':events,'full_pixels_read_by_root_before_copy':[26,27,28,114,118],'explicit_preview_omissions_observed':[{'printed_pages':[24,25],'UI_text':'Pages 24 to 25 are not shown in this preview.'},{'printed_pages':[115,116,117],'UI_text':'Pages 115 to 117 are not shown in this preview.'}],'copied_images_unmodified':True,'no_access_control_bypass':True,'only_browser_exported_observed_assets':True,'publisher_permission_banner_observed':True,'copyrighted_images_kept_private':True,'entire_book_obtained':False,'shared_tracked_or_service_mutations':False,'priority_or_publication_clearance':False}
out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'PID':os.getpid(),'UTC':receipt['UTC'],'pages':[x['printed_page'] for x in events]}))

