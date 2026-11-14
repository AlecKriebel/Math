"""Resume only inside the private stage; preserve predecessor artifacts."""
from pathlib import Path
import datetime, hashlib, json, re, shutil, subprocess, difflib
E=Path(__file__).resolve().parent; OLD=E.parent; P=OLD.parents[1]
if (E/'RESUME_BASELINE.json').exists():raise RuntimeError('historical one-time preparation already completed; preserve final proposals')
LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
H=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def put(n,x): (E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
base=json.loads((OLD/'BASELINE_ACTUAL_524.json').read_bytes()); frozen=json.loads((OLD/'FROZEN_INPUT_SET.json').read_bytes())
head=subprocess.check_output(['git','-C',str(LIVE.parent),'rev-parse','HEAD'],text=True).strip()
if head!=base['website_commit_read_only_observed']:raise ValueError('production HEAD changed')
actual={str(f):{'bytes':f.stat().st_size,'sha256':H(f)} for f in sorted(LIVE.rglob('*')) if f.is_file()}
expected={r['path']:{'bytes':r['bytes'],'sha256':r['sha256']} for r in base['public_files']}
if actual!=expected:raise ValueError('production public baseline changed')
for r in base['actual_installed_core']:
 f=Path(r['path'])
 if H(f)!=r['sha256'] or f.stat().st_size!=r['bytes']:raise ValueError('installed core changed '+str(f))
put('RESUME_BASELINE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'HEAD':head,'public_files_revalidated':len(actual),'core_files_revalidated':len(base['actual_installed_core']),'selected_path_bytes_unchanged':True,'frozen_input_set_sha256':H(OLD/'FROZEN_INPUT_SET.json'),'predecessor_failure_preserved':H(OLD/'initial-render-103.stderr'),'python':subprocess.check_output(['which','python3'],text=True).strip(),'bundled_python':__import__('sys').executable})
for n in ['banach_mtp2_source.py','bm_body_contract.py']:shutil.copyfile(OLD/n,E/n)
s=(OLD/'render_page.proposed.py').read_text()
# Exact root-relative reader links required by the accepted MTP2 reader packet.
s=s.replace("if paper.name in BM_IDS:\n    sections+=f'<section id=\"paper\"", "if paper.name in BM_IDS:\n    bm_prefix='/research/'+slug+'/' if paper.name=='23146753' else ''\n    sections+=f'<section id=\"paper\"")
s=s.replace('href="{h(c["pdf_filename"])}">Open PDF</a>','href="{h(bm_prefix+c["pdf_filename"])}">Open PDF</a>')
s=s.replace('href="{h(c["pdf_filename"])}" download>Download PDF</a> · <a href="{h(original_pdf_url)}" download>Download original PDF from Zenodo','href="{h(bm_prefix+c["pdf_filename"])}" download>Download PDF</a> · <a href="{h(original_pdf_url)}" download>Download original PDF from Zenodo')
s=s.replace('href="{h(c["supplement_filename"])}" download>Download complete ZIP','href="{h(bm_prefix+c["supplement_filename"])}" download>Download complete ZIP')
s=s.replace("bibtex_download=' download' if paper.name in BM_IDS else ''", "bibtex_download=' download' if paper.name in BM_IDS else ''\nbibtex_href='/research/'+slug+'/citation.bib' if paper.name=='23146753' else 'citation.bib'")
s=s.replace('<a href="citation.bib"{bibtex_download}>','<a href="{bibtex_href}"{bibtex_download}>')
(E/'render_page.proposed.py').write_text(s)
r=s.replace('ROOT = Path(__file__).resolve().parents[1]',f'ROOT = Path({str(P)!r})').replace("SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",f'SITE = Path({str(E/"public/research")!r})')
(E/'render_page.stage.py').write_text(r)
for n in ['index.html','sitemap.xml']:
 (E/'public/research').mkdir(parents=True,exist_ok=True);shutil.copyfile(LIVE/'research'/n,E/'public/research'/n)
checker=(OLD/'inputs/final-content-check.py').read_text()
checker=checker.replace('parser=argparse.ArgumentParser', 'from banach_mtp2_source import BM_IDS\nfrom bm_body_contract import check_bm_page\nparser=argparse.ArgumentParser',1)
needle="for rid in args.record_ids:\n p=R/'papers'/rid;"
replacement="""for rid in args.record_ids:
 if rid in BM_IDS:
  item=check_bm_page(R,S,rid,index,sitemap)
  result['papers'][rid]=item
  result['issues'] += [rid+': '+key for key,value in item['checks'].items() if not value]
  continue
 p=R/'papers'/rid;"""
if checker.count(needle)!=1:raise ValueError('checker insertion count')
checker=checker.replace(needle,replacement)
(E/'final-content-check.proposed.py').write_text(checker)
checker=checker.replace("R=Path(__file__).resolve().parents[1]",f'R=Path({str(P)!r})').replace("if not args.output_dir.resolve().is_relative_to(R/'verification'):","if not args.output_dir.resolve().is_relative_to(Path("+repr(str(P/'verification'))+")):")
(E/'final-content-check.stage.py').write_text(checker)
for name,orig in [('render_page',OLD/'inputs/render_page.py'),('final-content-check',OLD/'inputs/final-content-check.py')]:
 (E/(name+'.diff')).write_text(''.join(difflib.unified_diff(orig.read_text().splitlines(True),(E/(name+'.proposed.py')).read_text().splitlines(True),fromfile='installed/'+name+'.py',tofile='proposed/'+name+'.py')))
print('fresh baseline authenticated; resume code and ten-file overlay namespace prepared')
