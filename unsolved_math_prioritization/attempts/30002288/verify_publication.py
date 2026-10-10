"""Exact authenticated replays; finite tests do not prove continuum theorems."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('REJECT: require -I -S -B')
import argparse,hashlib,json,pathlib,shlex,shutil,subprocess,tempfile

def need(b,m):
 if not b:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--expected-manifest',required=True);a=ap.parse_args();root=pathlib.Path(__file__).absolute().parent
 need(sha((root/'PUBLICATION_MANIFEST.json').read_bytes())==a.expected_manifest,'publication pin')
 meta=json.loads((root/'PUBLICATION_METADATA.json').read_bytes());acc=json.loads((root/'audit/ACCEPTANCE.json').read_bytes());acc2=json.loads((root/'review2/SEPARATE_ACCEPTANCE.json').read_bytes())
 need(meta['canonical_status']=='unsolved' and meta['turns']=='5/5' and meta['compound_outcome']=='PARTIAL','canonical scope')
 need(acc['representation_question']=='ACCEPTED_NEGATIVE_ANSWER' and acc['general_finite_p_selection']=='UNRESOLVED_BY_THIS_WORK','first acceptance')
 need(acc2['compound_outcome']=='PARTIAL' and acc2['decisions']['corrected_core']['decision']=='ACCEPT' and acc2['decisions']['supplement_v2']['decision']=='ACCEPT_SEPARATELY_FOR_ROOT_LEVEL_ASYMPTOTICS_AND_ADMISSIBILITY','separate acceptance')
 anchors={r['role']:r for r in meta['archives']};runs=[]
 with tempfile.TemporaryDirectory(prefix='fractional verified replay ') as td:
  t=pathlib.Path(td);shim=t/'python-with-bytecode-disabled'
  # Reject deliberately omitted isolation flags before interpreter startup.
  # Valid nested checkers retain -I -S and receive -B.
  shell='#!/bin/sh\nflags=""\nhas_i=0\nhas_s=0\nwhile [ "$#" -gt 0 ]; do\n case "$1" in\n -I) has_i=1; flags="$flags $1"; shift ;;\n -S) has_s=1; flags="$flags $1"; shift ;;\n -O|-B) flags="$flags $1"; shift ;;\n -*) echo "unsupported interpreter option" >&2; exit 2 ;;\n *) break ;;\n esac\ndone\nif [ "$has_i" != 1 ] || [ "$has_s" != 1 ]; then echo "Use python -I -S" >&2; exit 2; fi\nexec '+shlex.quote(sys.executable)+' -B $flags '+shlex.quote(str(root/'isolated_runner.py'))+' "$0" "$@"\n'
  shim.write_text(shell);shim.chmod(0o700)
  def run(label,script,args,expected=None):
   p=subprocess.run([str(shim),'-I','-S','-B',*(['-O'] if sys.flags.optimize else []),str(script),*map(str,args)],cwd=t,capture_output=True,timeout=900)
   need(p.returncode==0 and not p.stderr,label+': '+p.stderr.decode())
   if expected is not None:need(p.stdout==expected,label+' output bytes mismatch')
   result=json.loads(p.stdout);need(result.get('status')=='PASS',label+' status')
   runs.append({'name':label,'output_sha256':sha(p.stdout),'status':'PASS','case_count':result.get('case_count')})
  for role,r in anchors.items():
   if 'bootstrap' not in r:continue
   expected=root/role/({'original':'RESULTS.json','corrected':'RESULTS.json','audit':'INDEPENDENT_DIAGNOSTICS_RESULTS.json','review2':'DIAGNOSTIC_RESULTS.json'}[role])
   args=[root/role,root/'archives'/r['archive']['filename'],root/'manifests'/r['manifest']['filename']]+(['--optimized'] if sys.flags.optimize else [])
   run(role+' frozen bootstrap',root/'historical_bootstraps'/r['bootstrap']['filename'],args,expected.read_bytes())
  for role,script,expected in [('original','replay_author.py','AUTHOR_REPLAY_RESULTS.json'),('corrected','replay_corrected.py','CORRECTED_REPLAY_RESULTS.json')]:
   r=anchors[role];args=[root/'archives'/r['archive']['filename'],root/'manifests'/r['manifest']['filename'],root/'historical_bootstraps'/r['bootstrap']['filename']]
   run(role+' exact archived 36-control suite',root/'audit'/script,args,(root/'audit'/expected).read_bytes())
  # Actually apply the unchanged unified patch, then compare all corrected bytes.
  fresh=t/'fresh original';shutil.copytree(root/'original',fresh)
  p=subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(root/'audit/VISCOSITY_TEST_CLASS.patch')],cwd=fresh,capture_output=True)
  need(p.returncode==0 and b'fuzz' not in (p.stdout+p.stderr).lower() and b'offset' not in (p.stdout+p.stderr).lower(),'zero-fuzz exact patch')
  need(set(x.name for x in fresh.iterdir())==set(anchors['corrected']['members']),'patched inventory')
  changed=[]
  for f in fresh.iterdir():
   need(f.read_bytes()==(root/'corrected'/f.name).read_bytes(),'patch reconstruction bytes')
   if f.read_bytes()!=(root/'original'/f.name).read_bytes():changed.append(f.name)
  need(changed==['PROOF.md'],'correction beyond proof paragraph')
  need((root/'audit/VISCOSITY_TEST_CLASS.patch').read_bytes()==(root/'review2/VISCOSITY_TEST_CLASS.patch').read_bytes(),'patch disagreement')
  run('independent packet mutation controls',root/'test_packets.py',['--package',root])
 print(json.dumps({'status':'PASS','problem_id':30002288,'optimized':bool(sys.flags.optimize),'archives_preserved':5,'archive_members':36,'actual_zero_fuzz_reconstruction':True,'changed_core_files':['PROOF.md'],'separate_v2_acceptance_verified':True,'canonical_status':'unsolved','turns':'5/5','compound_outcome':'PARTIAL','general_finite_p_selection':'UNRESOLVED_BY_THIS_WORK','all_valid_checker_executions_isolated_no_site_no_bytecode':True,'runs':runs},sort_keys=True,indent=2))
if __name__=='__main__':main()
