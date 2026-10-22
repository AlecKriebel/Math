from pathlib import Path
import hashlib,json,zipfile,re,ast,sys,subprocess,datetime,importlib.util,copy,tempfile
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'publication';M=R/'tmp/mirror'
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(n,x):(R/n).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
start=json.loads((R/'START_PINS.json').read_text());checks={}
checks['rebuilt_six']={n:pin(M/n)==v for n,v in start['publication'].items() if n!='PACKAGE_RECEIPT.json'}
checks['rebuilt_receipt_byte_equal']=(M/'PACKAGE_RECEIPT.json').read_bytes()==(P/'PACKAGE_RECEIPT.json').read_bytes()
source=json.loads((M/'SOURCE_MANIFEST.json').read_text());checks['source_manifest_exact_inventory']=set(source)=={str(p.relative_to(M)) for p in M.rglob('*') if p.is_file() and str(p.relative_to(M)) not in {'SOURCE_MANIFEST.json','PACKAGE_RECEIPT.json','output/zenodo-upload-kit.zip','output/random-lattice-counterexample-source-and-verification.zip'}}
checks['source_manifest_pins']=all(pin(M/n)==v for n,v in source.items())
checks['all_ten_input_bytes']=all((M/'audit/inputs'/n).read_bytes()==(A/'inputs'/n).read_bytes() for n in start['inputs'])
checks['input_nine_manifest_pins']=all(pin(M/'audit/inputs'/x['file'])=={'bytes':x['bytes'],'sha256':x['sha256']} for x in json.loads((M/'audit/inputs/MANIFEST.json').read_text())['entries'])
reviews={}
for d in sorted((M/'audit/reviews').iterdir()):
 rec=json.loads((d/'ARTIFACT_RECEIPT.json').read_text());rows=rec['files']
 reviews[d.name]={'count':len(rows),'pins_match':all(pin(d/x['path'])=={'bytes':x['bytes'],'sha256':x['sha256']} for x in rows)}
checks['review_authored_count']=sum(x['count'] for x in reviews.values());checks['review_manifests']=reviews
with zipfile.ZipFile(P/'output/zenodo-upload-kit.zip') as z:
 checks['kit_exact_members']=sorted(z.namelist())==sorted(['random-lattice-counterexample.pdf','random-lattice-counterexample-source-and-verification.zip','README.md','zenodo-metadata.json','zenodo-deposit.json'])
 checks['kit_pdf_identical']=z.read('random-lattice-counterexample.pdf')==(P/'output/pdf/random-lattice-counterexample.pdf').read_bytes()
 checks['kit_source_identical']=z.read('random-lattice-counterexample-source-and-verification.zip')==(P/'output/random-lattice-counterexample-source-and-verification.zip').read_bytes()
 checks['kit_metadata_identical']=z.read('zenodo-metadata.json')==(P/'zenodo-metadata.json').read_bytes()
 checks['kit_readme_identical']=z.read('README.md')==(P/'README.md').read_bytes()
 dep=json.loads(z.read('zenodo-deposit.json'));checks['kit_flat_files']=[x['path'] for x in dep['files']];checks['kit_metadata_structural_equality']=dep['metadata']==json.loads((P/'zenodo-metadata.json').read_text())
put('REBUILD_AND_INTEGRITY.json',checks)
# All text/code scanned, plus binary magic and extension inventory.
privacy=[];code=[];suffix={}
for n in source:
 p=M/n;b=p.read_bytes();suffix[p.suffix]=suffix.get(p.suffix,0)+1
 if p.suffix!='.pdf':
  t=b.decode(); hits=[]
  for key,pat in {'credential':r'(?i)(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{24,}|-----BEGIN .*PRIVATE KEY-----)','local_home':r'/Users/[^\s"<>]+','email':r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'}.items():
   found=sorted(set(re.findall(pat,t)))
   if found:hits.append({'kind':key,'matches':found})
  if hits:privacy.append({'file':n,'hits':hits})
 if p.suffix=='.py':
  tree=ast.parse(b);code.append({'file':n,'assert_count':sum(isinstance(x,ast.Assert) for x in ast.walk(tree)),'imports':sorted(set(x.module or '' for x in ast.walk(tree) if isinstance(x,ast.ImportFrom))|set(v.name for x in ast.walk(tree) if isinstance(x,ast.Import) for v in x.names))})
put('CONTENT_SCAN.json',{'extension_counts':suffix,'privacy_matches':privacy,'code':code,'forbidden_paths':[n for n in source if any(x in Path(n).parts for x in ['private','tmp','.git','__pycache__'])]})
# Pin references are indexed for manual current/historical classification.
known={n:pin(M/n) for n in source};mismatches=[];matched=0
for n in source:
 if not n.endswith('.json'):continue
 obj=json.loads((M/n).read_text())
 def visit(x,keys=[]):
  global matched
  if isinstance(x,dict):
   if 'sha256' in x:
    hints=[x[k] for k in ('path','file','name') if isinstance(x.get(k),str)]+keys[-1:]
    for hint in hints:
     candidates=[s for s in known if s==hint or s.endswith('/'+hint) or hint.endswith('/'+s) or hint.endswith('/'+s.removeprefix('audit/'))]
     if len(candidates)==1:
      target=candidates[0];matched+=1
      if x['sha256']!=known[target]['sha256'] or ('bytes' in x and x['bytes']!=known[target]['bytes']):mismatches.append({'file':n,'keys':keys,'hint':hint,'target':target,'recorded':x,'actual':known[target]})
      break
   for k,v in x.items():visit(v,keys+[k])
  elif isinstance(x,list):
   for i,v in enumerate(x):visit(v,keys+[str(i)])
 visit(obj)
put('PIN_REFERENCE_SCAN.json',{'resolved_references':matched,'mismatches_for_manual_history_review':mismatches})
print(json.dumps({'rebuild':checks,'privacy_match_files':len(privacy),'pin_reference_mismatches':len(mismatches)},indent=2))
