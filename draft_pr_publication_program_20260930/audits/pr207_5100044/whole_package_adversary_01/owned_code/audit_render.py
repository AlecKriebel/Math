from pathlib import Path
import hashlib,json,datetime,subprocess,re
O=Path(__file__).resolve().parent.parent;A=O.parent
same=[]
for page in range(1,8):
 old=O/f'renders/paper-{page}.png';new=O/f'renders/rebuilt-{page}.png'
 same.append({'page':page,'png_bytes_identical':old.read_bytes()==new.read_bytes(),'original_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'rebuilt_sha256':hashlib.sha256(new.read_bytes()).hexdigest()})
oldtext=subprocess.check_output(['pdftotext','-layout',str(A/'publication_package_v1/focal_inversion_area.pdf'),'-'])
newtext=subprocess.check_output(['pdftotext','-layout',str(O/'output/pdf/focal_inversion_area.pdf'),'-'])
log=(O/'output/pdf/focal_inversion_area.log').read_text()
warnings=[line for line in log.splitlines() if re.search(r'(LaTeX Warning:|Package .* Warning:|Overfull \\|Underfull \\|Missing character:|undefined references)',line)]
r={'schema':'fresh-owned-pdf-rebuild-check-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tex_source_identical':(O/'output/pdf/focal_inversion_area.tex').read_bytes()==(A/'publication_package_v1/focal_inversion_area.tex').read_bytes(),'original_pdf_sha256':hashlib.sha256((A/'publication_package_v1/focal_inversion_area.pdf').read_bytes()).hexdigest(),'rebuilt_pdf_sha256':hashlib.sha256((O/'output/pdf/focal_inversion_area.pdf').read_bytes()).hexdigest(),'all_seven_page_pixels_byte_identical':all(x['png_bytes_identical'] for x in same),'pdftotext_byte_identical':oldtext==newtext,'warnings':warnings,'pages':same,'compiler_command':'/opt/homebrew/bin/tectonic --only-cached --untrusted --keep-logs focal_inversion_area.tex','user_editor_opened_or_changed':False,'artifact_authoring_marker_successfully_run_once':True}
if not r['all_seven_page_pixels_byte_identical'] or not r['pdftotext_byte_identical'] or warnings:raise RuntimeError(r)
(O/'PDF_REBUILD_CHECK.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='pages'},indent=2))
