from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,io,subprocess,datetime,re,ast,stat
R=Path(__file__).resolve().parent; A=R.parent.parent; P=A/'publication'; X=R/'extracted/grassmann_calibrations_v1'
sha=lambda b:hashlib.sha256(b).hexdigest()
def req(c,m):
 if not c: raise RuntimeError(m)
d={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
man=json.loads((P/'PACKAGE_MANIFEST.json').read_text());records=man['files']
req(len({s['path'] for s in records})==len(records),'manifest duplicate')
for s in records:
 b=(P/s['path']).read_bytes(); req(len(b)==s['bytes'] and sha(b)==s['sha256'],'manifest '+s['path'])
d['manifest_nonself_entries']=len(records)
names=sorted([s['path'] for s in records]+['PACKAGE_MANIFEST.json'])
with zipfile.ZipFile(P/'grassmann_calibrations_source_verification_v1.zip') as z:
 req(z.testzip() is None,'CRC')
 actual=z.namelist();expected=['grassmann_calibrations_v1/'+n for n in names]
 req(actual==expected,'archive set/order')
 req(len(set(n.casefold() for n in actual))==len(actual),'casefold names')
 for n in names:
  req(z.read('grassmann_calibrations_v1/'+n)==(P/n).read_bytes()==(X/n).read_bytes(),'ZIP or extracted '+n)
 for t in z.infolist():
  req(not t.filename.startswith('/') and '..' not in PurePosixPath(t.filename).parts and '\\' not in t.filename,'unsafe name')
  req(t.filename.isascii() and t.date_time==(2026,10,12,0,0,0) and t.create_system==3 and t.external_attr==0o100644<<16 and t.compress_type==zipfile.ZIP_DEFLATED,'ZIP attribute '+t.filename)
 d['zip_entries']=len(actual);d['zip_crc_safe_sorted_regular_ascii']=True
out=io.BytesIO()
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in names:
  t=zipfile.ZipInfo('grassmann_calibrations_v1/'+n,date_time=(2026,10,12,0,0,0));t.create_system=3;t.external_attr=0o100644<<16;t.compress_type=zipfile.ZIP_DEFLATED;z.writestr(t,(P/n).read_bytes())
req(out.getvalue()==(P/'grassmann_calibrations_source_verification_v1.zip').read_bytes(),'deterministic ZIP')
d['independent_rebuilt_zip_identical']=True;d['zip_sha256']=sha(out.getvalue())
pins=json.loads((A/'SUBMITTED_PINS.json').read_text());head=pins['head_commit'];prefix='unsolved_math_prioritization/attempts/30002816/'
tree=subprocess.check_output(['git','ls-tree','-r','--name-only',head,'--',prefix],cwd=Path("/Users/alec/Documents/Math")).decode().splitlines()
req(set(tree)=={r['repository_path'] for r in pins['files']},'original full tree')
rows=[]
for r in pins['files']:
 b=subprocess.check_output(['git','show',head+':'+r['repository_path']],cwd=Path("/Users/alec/Documents/Math"))
 req(b==(A/'submitted'/r['relative']).read_bytes()==(P/'evidence/submitted'/r['relative']).read_bytes(),'original '+r['relative'])
 req(len(b)==r['bytes'] and sha(b)==r['sha256'],'original pin '+r['relative'])
 rows.append({'relative':r['relative'],'bytes':len(b),'sha256':sha(b),'git_show_identical':True})
d['original_head']=head;d['original_full_tree_count']=len(tree);d['original_all_git_show']=rows
req((P/'evidence/SUBMITTED_PINS.json').read_bytes()==(A/'SUBMITTED_PINS.json').read_bytes(),'pins copy')
for k in ('01','02'):
 c=json.loads((P/('evidence/PACKAGE_REVIEW_'+k+'_COPY.json')).read_text());rows=[]
 for r in c['files']:
  b=(P/r['path']).read_bytes();req(len(b)==r['bytes'] and sha(b)==r['sha256'],'copy pin '+r['path'])
  suffix=r['path'].split('evidence/package_review_'+k+'/')[1]
  req(b==(A/('reviews/package_'+k)/suffix).read_bytes(),'actual authored copy '+r['path'])
  rows.append(r['path'])
 actualset={p.relative_to(P).as_posix() for p in (P/('evidence/package_review_'+k)).rglob('*') if p.is_file()}
 req(actualset==set(rows),'copy set '+k)
 d['review_'+k+'_exact_copied_authored_records']=len(rows)
mdlinks=[]
for n in ('README.md','SUPPLEMENT.md','evidence/INDEX.md'):
 p=P/n
 for label,url in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',p.read_text()):
  if '://' in url or url.startswith('#'):continue
  target=(p.parent/url.split('#')[0]).resolve();req(target.exists(),'link '+n+' '+url);mdlinks.append({'from':n,'to':url})
d['current_relative_links']=mdlinks
jsons=[];python=[]
for n in names:
 p=P/n
 if p.suffix=='.json':json.loads(p.read_text());jsons.append(n)
 if p.suffix=='.py':ast.parse(p.read_text());python.append(n)
d['all_delivered_JSON_parse_count']=len(jsons);d['all_delivered_Python_AST_parse_count']=len(python)
meta=json.loads((P/'metadata.json').read_text());wrap=json.loads((P/'zenodo-deposit.json').read_text());req(meta==wrap['metadata'],'metadata wrapper')
req(meta['title']=='An application of separable-state nonrepresentability to Grassmann orbitopes and calibrations','title');req(meta['version']=='1.0' and meta['license']=='cc-by-4.0' and meta['creators'][0]['orcid']=='0009-0001-9320-500X','metadata exact')
d['metadata_wrapper_equal']=True
d['current_state']=json.loads((P/'evidence/CURRENT_REVIEW_STATE.json').read_text())
req(d['current_state']['preprint_ready_for_immutable_publication'] is False and d['current_state']['published'] is False,'state')
no_raw=[n for n in names if '/raw/' in n or n.endswith(('.pyc','.png','.jpg','.jpeg')) or '__pycache__' in n]
req(not no_raw,'raw/caches '+str(no_raw));d['raw_third_party_cache_image_paths']=no_raw
d['local_not_in_archive']=sorted(p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file() and p.relative_to(P).as_posix() not in names)
(R/'INVENTORY.json').write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps({k:v for k,v in d.items() if k not in ['original_all_git_show','current_relative_links']},indent=2))
