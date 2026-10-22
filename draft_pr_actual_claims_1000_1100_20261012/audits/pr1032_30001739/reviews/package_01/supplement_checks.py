from pathlib import Path
import hashlib,json,subprocess,sys,datetime,re,shutil
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'preprint_v1_0';K=P/'kit';h=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
def req(v,m):
 if not v:raise RuntimeError(m)
def run(name,args,cwd=R):
 p=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
 (R/'receipts'/f'{name}.stdout').write_bytes(p.stdout);(R/'receipts'/f'{name}.stderr').write_bytes(p.stderr)
 rows.append({'name':name,'argv':list(map(str,args)),'cwd':str(cwd),'exit':p.returncode,'stdout_sha256':h(p.stdout),'stderr_sha256':h(p.stderr),'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr)})
 req(p.returncode==0,'supplement command '+name);return p.stdout
own=json.loads((R/'independent.normal.json').read_text())
analytic=json.loads(run('direct_analytic',[sys.executable,'-I','-B',str(K/'scripts/check_analytic_independent.py')]))
key=lambda r:(tuple(s.replace('E','T') for s in r['pair']),r['q'],r.get('zeta',r.get('character_sign')))
fresh={key(x):x for x in own['germs']}
for x in analytic['scalar_checks']:
 y=fresh[key(x)]
 req(all(x[k]==y[k] for k in ['P','Q','order']),'germ data disagreement')
 req(x['leading_in_t_minus_1']==y['leading'],'leading coefficient disagreement')
# Paper table vs own full graphs, not the packaged graph implementation.
graphs={}
for x in own['partitions']:
 graphs[(''.join(x['m']),''.join(x['n']))]=x['forward'];graphs[(''.join(x['n']),''.join(x['m']))]=x['reverse']
table=[]
for line in (P/'paper.tex').read_text().splitlines():
 if re.match(r'^\$[ABCDT]+/[ABCDT]+\$ &',line):
  parts=line.split(' & ');dirs=re.findall(r'[ABCDT]+',parts[1]);G=graphs[tuple(dirs)]
  witness=tuple(re.findall(r'\(([ABCDT]),([ABCDT])\)',parts[2])[0]);Y=[list(t) for t in re.findall(r'\(([ABCDT]),([ABCDT])\)',parts[3])]
  req(list(witness) in G['isolated'],'own graph table witness')
  req(sorted(Y)==sorted(G['Y']),'own graph table full Y')
  table.append({'direction':dirs,'witness':witness,'Y':Y})
req(len(table)==15,'table15')
# Run builder itself under both optimization flags in separate untouched copies.
for mode in ['O','OO']:
 d=R/'scratch'/('builder_inside_'+mode);shutil.copytree(K,d)
 run('inside_builder_'+mode,[sys.executable,'-I','-B','-'+mode,str(d/'scripts/build_archive.py'),'inside.zip'],cwd=d)
 req((d/'inside.zip').is_file(),'builder optimized output')
# Existing input preservation, archived old preparation pins and seals.
checks=[]
for name,base,data in [('review_input_freeze',A,json.loads((R/'INPUT_FREEZE.json').read_text())['files']),('original_preparation_pins',A,json.loads((A/'preparation/unknown_priority_20261016/ORIGINAL_INPUT_PINS.json').read_text())['files']),('preparation_seal',P,json.loads((P/'PREPARATION_SEAL.json').read_text())['files'])]:
 bad=[]
 for row in data:
  p=base/row['path']
  if not p.is_file() or p.stat().st_size!=row['bytes'] or h(p.read_bytes())!=row['sha256']:bad.append(row['path'])
 req(not bad,name+' old changed');checks.append({'name':name,'entries':len(data),'mismatches':bad})
binding=json.loads((P/'DEPOSIT_BINDING.json').read_text())
req(binding['metadata_sha256']==h((P/'.zenodo.json').read_bytes()),'metadata binding')
for row in binding['files']:
 b=(P/row['path']).read_bytes();req(len(b)==row['bytes'] and h(b)==row['sha256'],'binding exact file')
for r in [binding['native_metadata'],json.loads((P/'PREPARATION_SEAL.json').read_text())['native_manifest']]:
 b=(A/r['path']).read_bytes();req(len(b)==r['bytes'] and h(b)==r['sha256'],'native sealed file')
(R/'SUPPLEMENT_RESULTS.json').write_text(json.dumps({'scalar_rows_agree':40,'manuscript_table_agrees_with_new_independent_graphs':table,'preservation_checks':checks,'original_pdf_pinned':True,'original_archive_pinned':True,'binding_valid':True,'optimized_builder_inside_also_succeeds':['O','OO'],'commands':rows},indent=2)+'\n')
print(json.dumps({'scalar_rows':40,'table_rows':15,'preserved':checks,'optimized_builder_defect_reproduced':True},indent=2))
