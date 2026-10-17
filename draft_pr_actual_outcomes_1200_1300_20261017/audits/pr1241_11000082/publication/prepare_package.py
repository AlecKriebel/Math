#!/usr/bin/env python3
"""Prepare an explicitly approved edition and portable authored evidence only."""
from pathlib import Path, PurePosixPath
import hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
EDITION=AUDIT/'current_edition'
PACKAGE=ROOT/'verification'
NAMES=['ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json']
PR=1241
PROBLEM=11000082
ORIGINAL='493a764dec034b7b645be76a284c4e6edc0583eb'
TITLE='Equal dilatations deep in the Johnson filtration: a convex-core proof'
MATCHING_DOI='10.5281/zenodo.23301731'
MINIMUM_FREEZES={
 'reviews/analytic_adversary/FINAL_AUTHORED_FREEZE.json':('reviews/analytic_adversary','entries','file'),
 'reviews/source_question_family/FREEZE_MANIFEST.json':('reviews/source_question_family','authored_files','path'),
 'reviews/convex_core_adversary/FREEZE_MANIFEST.json':('reviews/convex_core_adversary','authored_files','path'),
 'priority/independent/FREEZE_MANIFEST.json':('priority/independent','all_authored_content_files','path_relative_to_authored_root'),
 'priority/adversary/FREEZE_MANIFEST.json':('priority/adversary','authored_files','path'),
}
def need(c,m):
 if not c:raise RuntimeError(m)
def binding(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def safe(raw):
 need(isinstance(raw,str) and bool(raw),'Invalid relative path')
 rel=PurePosixPath(raw);need(not rel.is_absolute() and '..' not in rel.parts and str(rel)==raw and raw!='.','Unsafe relative path '+raw)
 return raw
def within(root,raw):
 p=root/safe(raw);need(not p.is_symlink(),'Symlink forbidden '+raw)
 try:p.resolve().relative_to(root.resolve())
 except ValueError:raise RuntimeError('Path escaped authored root '+raw)
 return p
def copy(src,rel):
 dst=PACKAGE/safe(rel);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
def authored(folder):
 candidates=[p for p in folder.rglob('*') if p.is_file() and not p.is_symlink()]
 if not candidates:return []
 run=subprocess.run(['git','check-ignore','--no-index','-z','--stdin'],input=b'\0'.join(str(p).encode() for p in candidates)+b'\0',capture_output=True)
 need(run.returncode in (0,1),run.stderr.decode());ignored=set(run.stdout.decode().split('\0'))
 return [p for p in candidates if str(p) not in ignored and (p.suffix in {'.md','.json','.jsonl','.py','.sha256'} or p.name in {'.gitignore','SHA256SUMS'})]
def load_context():
 context=json.loads((AUDIT/'CURRENT_PR1241_CONTEXT.json').read_text())
 need(context.get('schema')=='math-pr1241-current-context-v1','Missing explicit current context schema')
 need(context.get('pr')==PR and context.get('problem_id')==PROBLEM and context.get('original_head')==ORIGINAL and context.get('title')==TITLE,'Current context identity differs')
 priority=json.loads((AUDIT/'PRIORITY_ADJUDICATION.json').read_text())
 for key in ['novelty_clearance','firstness_claim','current_openness_claim','new_existence_claim']:
  need(priority.get(key) is False,'Priority record must explicitly disclaim '+key)
 need(priority.get('matching_publication_doi')==MATCHING_DOI,'Positive matching printed theorem must be credited explicitly')
 math_gate=json.loads((AUDIT/'MATH_GATE.json').read_text())
 need(math_gate.get('pr')==PR and math_gate.get('problem_id')==PROBLEM and math_gate.get('original_head')==ORIGINAL and isinstance(math_gate.get('status'),str) and math_gate['status'].startswith('PASS'),'Current mathematical gate must pass for this exact original target')
 texts=context.get('edition_text',{})
 need(set(texts)=={'PROOF.md','AUDIT.md','README.md','ACCEPTANCE.md'},'Exactly four explicit current prose records required')
 for name,text in texts.items():need(isinstance(text,str) and bool(text.strip()),'Empty current edition '+name)
 for key in ['acceptance','sources','verification']:need(isinstance(context.get(key),dict) and bool(context[key]),'Explicit structured current record required: '+key)
 registry=context.get('authored_freezes');need(isinstance(registry,list) and bool(registry),'Explicit complete authored freeze registry required')
 seen=set()
 for entry in registry:
  need(set(entry)=={'path','base','entries_key','path_key','sha256'},'Unexpected authored freeze registry schema')
  path=safe(entry['path']);safe(entry['base']);need(path not in seen,'Duplicate authored freeze');seen.add(path)
  need(path.startswith(('reviews/','priority/')),'Freeze outside own review/priority trees')
  need(entry['entries_key'] in {'entries','files','authored_files','all_authored_content_files','new_authored_files'} and entry['path_key'] in {'file','path','path_relative_to_authored_root','path_relative_to_family_root'},'Unsupported explicit freeze schema')
  need(binding(within(AUDIT,path))['sha256']==entry['sha256'],'Authored freeze differs from outside anchor '+path)
 for path,shape in MINIMUM_FREEZES.items():
  found=next((e for e in registry if e['path']==path),None)
  need(found is not None and tuple(found[k] for k in ['base','entries_key','path_key'])==shape,'Missing/wrong required freeze '+path)
 need(any(e['path'].startswith('priority/adversary/') for e in registry),'Independent general-theory priority freeze required')
 return context,priority

def main():
 context,priority=load_context()
 # Authenticate every frozen authored member before writing any edition/package.
 frozen_members=[]
 for reg in context['authored_freezes']:
  manifest=within(AUDIT,reg['path']);obj=json.loads(manifest.read_text());entries=obj.get(reg['entries_key'])
  need(isinstance(entries,list) and bool(entries),'Empty/invalid authored freeze '+reg['path'])
  base=within(AUDIT,reg['base']);seen=set()
  frozen_members.append((manifest,reg['path']))
  for entry in entries:
   name=safe(entry.get(reg['path_key']));need(name not in seen,'Duplicate frozen member');seen.add(name)
   p=within(base,name);need(binding(p)=={'bytes':entry['bytes'],'sha256':entry['sha256']},'Frozen member changed '+str(p))
   frozen_members.append((p,reg['base']+'/'+name))
 EDITION.mkdir(exist_ok=True);PACKAGE.mkdir(exist_ok=True)
 for name,text in context['edition_text'].items():(EDITION/name).write_text(text)
 save(EDITION/'SOURCES.json',{'schema':'johnson-multiplicity-current-sources-v1','problem_id':PROBLEM,'explicit_current_record':context['sources'],'priority_adjudication':priority,'historical_submitted_record':json.loads((AUDIT/'submitted/SOURCES.json').read_text()),'distribution':'Authored source receipts only; omitted third-party bodies and raw inventories are receipt-only, not portable evidence manifests.'})
 save(EDITION/'VERIFICATION.json',{'schema':'johnson-multiplicity-current-verification-v1','problem_id':PROBLEM,'explicit_current_record':context['verification'],'current_math_gate':json.loads((AUDIT/'MATH_GATE.json').read_text()),'historical_submitted_record':json.loads((AUDIT/'submitted/VERIFICATION.json').read_text()),'portable_replay':'All authored byte bindings and original Git identities; finite root diagnostics in normal/-O/-OO; source-question and convex-core assertion-based diagnostics in normal mode on temporary copies only. Infinite and ambient claims rest on written proofs. No omitted historical program replay or third-party body reauthentication is claimed.'})
 save(EDITION/'ACCEPTANCE.json',{'schema':'johnson-multiplicity-current-acceptance-v1','problem_id':PROBLEM,'original_head':ORIGINAL,'explicit_current_record':context['acceptance'],'priority_clearance':False,'matching_publication_doi':MATCHING_DOI,'firstness_claim':False,'new_existence_claim':False,'current_openness_claim':False,'current_document_bindings':{n:binding(EDITION/n) for n in ['PROOF.md','AUDIT.md','ACCEPTANCE.md']},'publication_gate':'Separate exact PDF/archive and sequential fresh whole-package review and publication receipts; none implied by preparing this edition.'})
 save(EDITION/'MANIFEST.json',{'schema':'johnson-multiplicity-current-edition-manifest-v1','members':NAMES,'entries':[{'file':n,**binding(EDITION/n)} for n in NAMES if n!='MANIFEST.json'],'self_hash_excluded':'MANIFEST.json'})
 # Rebuild only package-owned copies; retain its authored verifier.
 for name in ['current_edition','original_submitted','provenance','reviews','priority','manuscript','diagnostics']:
  p=PACKAGE/name
  if p.exists():need(p.is_dir() and not p.is_symlink(),'Unexpected package child');shutil.rmtree(p)
 for n in NAMES:copy(EDITION/n,'current_edition/'+n);copy(AUDIT/'submitted'/n,'original_submitted/'+n)
 for p in sorted(AUDIT.iterdir()):
  if p.is_file() and not p.is_symlink() and p.suffix in {'.md','.json'} and p.name!='RESEARCH_LOG.md':copy(p,'provenance/'+p.name)
 for family in ['analytic_adversary','source_question_family','convex_core_adversary']:
  folder=AUDIT/'reviews'/family
  for p in authored(folder):copy(p,'reviews/'+family+'/'+p.relative_to(folder).as_posix())
 for p in authored(AUDIT/'priority'):copy(p,'priority/'+p.relative_to(AUDIT/'priority').as_posix())
 # Explicit registry members are included even when a newly written child would
 # otherwise match a global scratch-directory ignore rule.
 for p,rel in frozen_members:copy(p,rel)
 for name in ['root_horowitz_checks.py','ROOT_EXACT_DIAGNOSTICS.json','ROOT_REPLAY_RECEIPT.json']:copy(AUDIT/name,'diagnostics/'+name)
 copy(ROOT/'manuscript/main.tex','manuscript/main.tex');copy(ROOT/'BIBLIOGRAPHY_QA.json','provenance/BIBLIOGRAPHY_QA.json')
 print(json.dumps({'current_edition_files':8,'portable_files':sum(p.is_file() for p in PACKAGE.rglob('*')),'scope':'Explicit current context plus authored proofs, reviews, finite diagnostics and receipts; external source bodies omitted.'}))
if __name__=='__main__':main()
