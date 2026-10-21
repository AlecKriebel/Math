from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,stat,subprocess,datetime,os
W=Path(__file__).resolve().parent;R=W.parent.parent;REPO=R.parent;out=[]
def git(*a):return subprocess.check_output(['git','-C',str(REPO),*a])
def h(b):return hashlib.sha256(b).hexdigest()
for n in [906,908,909,919]:
 p=W/'private'/f'public{n:04}';d=json.loads((W/f'private/inputs/PR{n:04}_DISPOSITION.json').read_text());e=json.loads((W/f'private/inputs/eligibility/pr{n:04}.json').read_text());zpath=next(p.glob('*.zip'));pdf=next(p.glob('*.pdf'));z=zipfile.ZipFile(zpath);infos=z.infolist();names=[x.filename for x in infos];m=json.loads(z.read('PACKAGE_MANIFEST.json'));payload=m['files'];errors=[]
 for x in infos:
  path=PurePosixPath(x.filename);mode=(x.external_attr>>16)&0o177777
  if path.is_absolute() or '..' in path.parts or '\\' in x.filename or str(path)!=x.filename or x.is_dir() or (stat.S_IFMT(mode) not in [0,stat.S_IFREG]):errors.append('unsafe/nonregular '+x.filename)
 if len(set(names))!=len(names):errors.append('duplicate names')
 if z.testzip() is not None:errors.append('CRC')
 if set(names)!=set(payload)|{'PACKAGE_MANIFEST.json'}:errors.append('manifest closure')
 for name,pin in payload.items():
  b=z.read(name)
  if len(b)!=pin['bytes'] or h(b)!=pin['sha256']:errors.append('payload '+name)
 if z.read('note.pdf')!=pdf.read_bytes():errors.append('external PDF mismatch')
 if m['original_pr_head']!=d['inventory_head_sha']:errors.append('head mismatch')
 # All original tree blobs, not merely root claims or manifest subset.
 roots=[os.path.commonpath([f for f in e['changed_paths'] if '/attempts/' in f])]
 original=[]
 for root in roots:
  for entry in git('ls-tree','-r','-z',d['inventory_head_sha'],'--',root).split(b'\0'):
   if not entry:continue
   obj,pathname=entry.split(b'\t',1);mode,typ,blob=obj.decode().split();full=pathname.decode();relative=full[len(root)+1:];member='original_packet/'+relative;b=git('cat-file','blob',blob)
   ok=member in names and z.read(member)==b
   original.append({'path':full,'blob':blob,'bytes':len(b),'sha256':h(b),'member':member,'equal':ok})
   if not ok:errors.append('original '+full)
 originalnames={x['member'] for x in original};archived={x for x in names if x.startswith('original_packet/')}
 if originalnames!=archived:errors.append('original tree closure')
 (p/'note.tex').write_bytes(z.read('note.tex'));subprocess.run(['pdftotext','-layout',str(pdf),str(p/'note.txt')],check=True)
 (p/'package_identity.json').write_bytes(z.read('ORIGINAL_SNAPSHOT.json'))
 if 'BIBLIOGRAPHIC_IDENTITIES.json' in names:(p/'bibliographic_identities.json').write_bytes(z.read('BIBLIOGRAPHIC_IDENTITIES.json'))
 for name in ['README.md','note.tex','TARGET_IDENTITY_PREFLIGHT.json','PR_DESCRIPTION_CORRECTED.md']:
  if name in names:(p/('package_'+name.replace('/','_'))).write_bytes(z.read(name))
 # Find immutable original provenance text without executing anything.
 for x in original:
  if any(k in x['path'].upper() for k in ['SOURCE','FORMULATION','PROOF','README']):
   f=p/'original_text'/x['member'];f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(z.read(x['member']))
 out.append({'pr':n,'record':int(d['doi'].split('.')[-1]),'members':len(names),'manifest_payloads':len(payload),'safe_unique_regular_crc_closed':not errors,'manifest_sha256':h(z.read('PACKAGE_MANIFEST.json')),'archive_sha256':h(zpath.read_bytes()),'pdf_sha256':h(pdf.read_bytes()),'external_embedded_pdf_equal':z.read('note.pdf')==pdf.read_bytes(),'original_tree_count':len(original),'original_tree_archive_closed':originalnames==archived,'all_original_blobs_exact':all(x['equal'] for x in original),'originals':original,'errors':errors})
(W/'PACKAGE_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps([{k:v for k,v in x.items() if k!='originals'} for x in out],indent=2))
