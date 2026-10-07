from pathlib import Path
import subprocess,hashlib,json,re,datetime,argparse
ap=argparse.ArgumentParser(description='Export exact selected Lean dependency closure from read-only upstream Git objects. Does not certify compilation.')
ap.add_argument('--upstream',type=Path,required=True)
ap.add_argument('--output',type=Path,required=True)
a=ap.parse_args(); root=a.upstream.resolve(); dest=a.output.resolve(); dest.mkdir(parents=True,exist_ok=True); harness=dest/'pinned_build'; pin='adc7f1241b42e322a6451854ab7e4b4c146bf78a'
mods=set(); extern=set(); pending=['OAI.InformationTheory.PhotonNumber.Inequality']
while pending:
 m=pending.pop()
 if m in mods: continue
 p='lean/'+m.replace('.','/')+'.lean'; raw=subprocess.check_output(['git','-C',str(root),'show',pin+':'+p]); mods.add(m)
 q=harness/Path(p).relative_to('lean');q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
 for imp in re.findall(r'^import ([A-Za-z0-9_.]+)',raw.decode(),re.M):
  if imp.startswith('OAI.'): pending.append(imp)
  else: extern.add(imp)
records=[]
for m in sorted(mods):
 p='lean/'+m.replace('.','/')+'.lean'; raw=(harness/Path(p).relative_to('lean')).read_bytes()
 records.append({'module':m,'path':p,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'git_blob':subprocess.check_output(['git','-C',str(root),'rev-parse',pin+':'+p]).decode().strip(),'imports':re.findall(r'^import ([A-Za-z0-9_.]+)',raw.decode(),re.M),'source_red_flags':re.findall(r'\b(?:sorry|axiom|admit|unsafe)\b',raw.decode())})
for p in ['lean-toolchain','lakefile.lean','lake-manifest.json','README.md','docs/273.md','ComparatorChallenges/README.md','ComparatorChallenges/EntropyPhotonNumber.lean','ComparatorChallenges/EntropyPhotonNumber.json']:
 raw=subprocess.check_output(['git','-C',str(root),'show',pin+':lean/'+p]);q=dest/'upstream_config'/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
(harness/'LICENSE').write_bytes(subprocess.check_output(['git','-C',str(root),'show',pin+':LICENSE']))
(harness/'lean-toolchain').write_text('leanprover/lean4:v4.34.1\n')
(harness/'lakefile.lean').write_text('import Lake\nopen Lake DSL\npackage OAI where\n  version := v!"0.1.0"\n  fixedToolchain := true\n  leanOptions := #[⟨`autoImplicit, false⟩]\nrequire mathlib from ".lake/packages/mathlib"\nlean_lib OAI where\n  globs := #[`OAI.+]\n')
(harness/'CheckAxioms.lean').write_text('import OAI.InformationTheory.PhotonNumber.Inequality\n#print axioms OAI.EntropyPhotonNumber.entropy_photon_number_inequality\n#check OAI.EntropyPhotonNumber.entropy_photon_number_inequality\n#check OAI.EntropyPhotonNumber.epni_entropy_closed\n#check OAI.EntropyPhotonNumber.entropy_tangent_finiteEnergy\n')
(dest/'source_manifest.json').write_text(json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'upstream_pin':pin,'modules':records,'external_imports':sorted(extern),'mathlib_pin':'d13f23b723b8a846827a245b89c10fc7d3f11612'},indent=2)+'\n')
print('Copied',len(mods),'modules;',sum(x['bytes'] for x in records),'bytes; external imports',sorted(extern));print('Red flags',[(x['module'],x['source_red_flags']) for x in records if x['source_red_flags']])
