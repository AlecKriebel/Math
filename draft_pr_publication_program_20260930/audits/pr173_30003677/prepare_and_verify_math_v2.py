#!/usr/bin/env python3
from pathlib import Path
import ast,json,hashlib,subprocess,sys,datetime
A=Path(__file__).resolve().parent
def need(c,s):
 if not c:raise RuntimeError(s)
def ident(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
D=A/'repaired_candidate_v2';need(not D.exists(),'v2 already exists');D.mkdir()
for p in (A/'repaired_candidate_v1').rglob('*'):
 if p.is_file():
  to=D/p.relative_to(A/'repaired_candidate_v1');to.parent.mkdir(parents=True,exist_ok=True);to.write_bytes(p.read_bytes())
f=D/'CANDIDATE.md';s=f.read_text()
old='Every event mark is a finite degree, so all incident half-edges at reached vertices form a finite set almost surely. The fixed-length path likewise has only finitely many incident half-edges almost surely.'
new='Every event mark is a finite degree, so all incident half-edges at reached vertices form a finite set almost surely. In an immediate-partner revelation construction, also reveal each current frontier target and count its full incident degree in the cutoff. There are only finitely many current frontier edges, each such target has a finite degree almost surely, and hence this enlarged exposure remains finite almost surely. The fixed-length path likewise has only finitely many incident half-edges almost surely; any off-path targets revealed by that construction are included in the same cutoff. This argument needs no third moment. Counting only discovered vertices, or excluding already seen boundary targets from collision accounting, would not justify the uniform matching estimate.'
need(s.count(old)==1,'proof replacement target');s=s.replace(old,new);f.write_text(s);(D/'review/author_replay/CANDIDATE.md').write_text(s)
S=A/'root_explicit_support';need(not S.exists(),'support exists');S.mkdir()
src=A/'branching_local_adversary/public/controls.py';tree=ast.parse(src.read_text())
class Explicit(ast.NodeTransformer):
 def visit_Assert(self,node):
  return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError',ctx=ast.Load()),args=[ast.Constant(value='Finite control failed: '+ast.unparse(node.test))],keywords=[]),cause=None)],orelse=[]),node)
out=ast.unparse(ast.fix_missing_locations(Explicit().visit(tree)))+'\n';(S/'branching_controls_explicit.py').write_text(out)
negative=out.replace('labels[target] == 0','labels[target] == 1')
need(negative!=out,'mutant target');(S/'branching_controls_false_colour.py').write_text(negative)
runs=[]
def run(path,opt,expect,kind,cwd):
 cmd=[sys.executable,'-E','-S','-B','-P']+(['-O'] if opt else [])+[str(path)]
 r=subprocess.run(cmd,cwd=cwd,capture_output=True,timeout=120)
 need((r.returncode==0)==expect,'wrong outcome '+kind)
 stem=kind+('_optimized' if opt else '_ordinary')
 (S/(stem+'.stdout')).write_bytes(r.stdout);(S/(stem+'.stderr')).write_bytes(r.stderr)
 rec={'kind':kind,'optimized':opt,'exit_code':r.returncode,'code':ident(path),'stdout':ident(S/(stem+'.stdout')),'stderr':ident(S/(stem+'.stderr'))}
 if expect:rec['result']=json.loads(r.stdout)
 else:need(b'RuntimeError: Finite control failed:' in r.stderr,'unrelated negative failure')
 runs.append(rec);return rec
for opt in (False,True):
 for name,path in [('v2_author',D/'verify.py'),('v2_independent',D/'review/independent_checks.py')]:run(path,opt,True,name,D)
 b=run(S/'branching_controls_explicit.py',opt,True,'branching',S)
 need(b['result']==json.loads((A/'branching_local_adversary/public/control_results.json').read_text()),'branching exact result changed')
 run(S/'branching_controls_false_colour.py',opt,False,'branching_false_colour',S)
for kind in ('v2_author','v2_independent','branching'):
 rs=[r for r in runs if r['kind']==kind];need(rs[0]['result']==rs[1]['result'],'mode mismatch')
# Fresh independent actual executions of the already read, sealed standalone family export.
exp=A/'path_diagonal_adversary_public_support'
r=subprocess.run([sys.executable,'-E','-S','-B','-P',str(exp/'run_public_controls.py'),'--output',str(S/'PATH_PUBLIC_REPRODUCTION.json')],cwd=exp,capture_output=True,timeout=180)
need(r.returncode==0,'path controls driver failed')
pr=json.loads((S/'PATH_PUBLIC_REPRODUCTION.json').read_text());need(pr['summary']['run_count']==20 and pr['summary']['all_negative_runs_rejected'],'path summary')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'V2_PROOF_IDENTITIES_AND_EXPLICIT_INDEPENDENT_SUPPORT_REPRODUCED','v2_files':{str(p.relative_to(D)):ident(p) for p in D.rglob('*') if p.is_file()},'runs':runs,'path_export_driver':ident(exp/'run_public_controls.py'),'path_export_receipt':ident(S/'PATH_PUBLIC_REPRODUCTION.json'),'path_summary':pr['summary'],'original_branching_code_limitation':'Original family controls used assert. ROOT retains that historical code unchanged; this additive AST replacement enforces each identical predicate with RuntimeError under both execution modes. A false protected-colour variant rejects under both modes.','universal_stochastic_proof_certified_by_computation':False,'candidate_hypotheses_conclusion_unchanged':True,'prior_repaired_six_negative_variants':'The unchanged v1 verifier code already rejected all six false variants under both modes; v2 only expands the text and its artifact fingerprint.'}
(A/'ROOT_MATH_SUPPORT_REPRODUCTION.json').write_text(json.dumps(receipt,indent=2)+'\n')
for root in (D,S):
 for p in root.rglob('*'):
  if p.is_file():p.chmod(0o444)
(A/'ROOT_MATH_SUPPORT_REPRODUCTION.json').chmod(0o444)
print(json.dumps({'status':receipt['status'],'v2_baselines':4,'branching_baselines':2,'branching_negatives':2,'path_runs':20}))

