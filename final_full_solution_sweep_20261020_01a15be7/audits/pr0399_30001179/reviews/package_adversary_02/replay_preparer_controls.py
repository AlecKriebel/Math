#!/usr/bin/env python3
"""Read-only source replay; redirect all HERE outputs/temporary fixtures to own private scope."""
import pathlib,subprocess,json,sys,hashlib
Q=pathlib.Path(__file__).resolve().parent;A=Q.parents[1];P=A.parents[1]/'private/pr0399_package_adversary_02/preparer_replay';P.mkdir(exist_ok=True)
results=[]
for n in ['offline_controls','candidate_controls','repair_controls']:
 source=A/'publication_operations_preparation'/(n+'.py')
 for optimized in [False,True]:
  out=P/(n+('_optimized'if optimized else'_normal'));out.mkdir(exist_ok=True)
  code='import importlib.util,pathlib,sys;sys.dont_write_bytecode=True;s=importlib.util.spec_from_file_location("scoped_controls",sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.HERE=pathlib.Path(sys.argv[2]);m.main()'
  r=subprocess.run([sys.executable,*(['-O']if optimized else[]),'-B','-c',code,str(source),str(out)],capture_output=True,text=True)
  (out/'stdout.txt').write_text(r.stdout);(out/'stderr.txt').write_text(r.stderr)
  results.append({'source':str(source.relative_to(A)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'optimized':optimized,'exit':r.returncode,'summary':json.loads(r.stdout)if r.returncode==0 else r.stderr})
(Q/'PREPARER_CONTROLS_REPLAY.json').write_text(json.dumps({'results':results,'scope':'Only HERE was redirected; test source and actual helper bodies unmodified. Canonical outputs/seals untouched; fixture boundary guards prohibit provider access.'},indent=2)+'\n');print(json.dumps([(r['source'],r['optimized'],r['exit'])for r in results]))
