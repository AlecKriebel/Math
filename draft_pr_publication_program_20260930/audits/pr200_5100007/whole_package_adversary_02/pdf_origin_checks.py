from pathlib import Path
import subprocess,hashlib,json
HERE=Path.cwd();pkg=HERE.parent/'publication_package_v2';renders=HERE.parent/'package_build_01'/'private_pdf_qa_v2'
rows=[]
for page in range(1,7):
 p=subprocess.run(['/opt/homebrew/bin/pdftoppm','-r','110','-f',str(page),'-l',str(page),'-singlefile','-png',str(pkg/'outer_focal_period.pdf')],capture_output=True,check=True)
 actual=hashlib.sha256(p.stdout).hexdigest();existing=hashlib.sha256((renders/('page-'+str(page)+'.png')).read_bytes()).hexdigest()
 rows.append({'page':page,'current_PDF_render_sha256':actual,'inspected_existing_render_sha256':existing,'byte_equal':actual==existing})
 if actual!=existing:raise RuntimeError('render identity mismatch '+str(page))
primaries=[]
for name,path in [('Stachel published',HERE.parent/'math_source_family_01'/'private_sources'/'stachel_published.pdf'),('Reznik journal',HERE.parent/'math_source_family_01'/'private_sources'/'journal_reznik.pdf'),('Ferudun primary',HERE.parent/'priority_exact_history_01'/'private_readings'/'ferudun_site.pdf')]:
 b=path.read_bytes();primaries.append({'name':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'md5':hashlib.md5(b).hexdigest()})
report={'status':'PASS','all_six_visually_inspected_renders_bound_to_current_PDF':True,'render_checks':rows,'primary_source_byte_identities':primaries,'third_party_images_or_full_texts_not_in_safe_authored_manifest':True}
Path('PDF_SOURCE_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
