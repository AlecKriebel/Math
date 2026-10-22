"""Read-only postseal PR788 classical-priority crosscheck custody."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,re,stat,subprocess,sys
OLD_MANIFEST='59ee3141dd73732c4494594e561feeda54ce6fa55304a5a41974945b74e7a3a2'
OLD_CHECKER='81fb18e7d6c59aa95c1d2131d9a5778e9bceb745bba0814f79be3ecbd75c1b46'
PEER='1cd07885ed60a5d9ebde4d5cda65f205a2622a9ffccf1765ffc2534e0b6490ac'
HEAD='3412d5a074c3f3a03f75735a9ccf1755e172204a'
EXCEPTION={'MANIFEST.json':'Only self-hash exception; caller-held external SHA256 required.'}
def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def valid(v):return isinstance(v,str)and re.fullmatch('[0-9a-f]{64}',v)is not None
def unique(ps):
 d={}
 for k,v in ps:need(k not in d,'Duplicate JSON key');d[k]=v
 return d
def constant(x):raise ValueError('Nonfinite JSON constant')
def parse(b):return json.loads(b,object_pairs_hook=unique,parse_constant=constant)
def safe(n):
 need(isinstance(n,str)and n and'\\'not in n and not PurePosixPath(n).is_absolute()and all(x not in('','.','..')for x in n.split('/')),'Unsafe relative path')
 return n
def regular(p):
 need(stat.S_ISREG(p.lstat().st_mode),'Nonregular input')
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 with os.fdopen(fd,'rb')as f:
  need(stat.S_ISREG(os.fstat(f.fileno()).st_mode),'Nonregular descriptor');return f.read()
def relative(t,n):
 safe(n);p=t
 for part in n.split('/'):p=p/part;need(not p.is_symlink(),'Symlink path component')
 return regular(p)
def check(b,r):
 need(type(r.get('bytes'))is int and r['bytes']>=0 and valid(r.get('sha256')),'Invalid byte/hash row')
 need(len(b)==r['bytes']and sha(b)==r['sha256'],'Byte/hash mismatch')
def main(a):
 w=Path(a.packet).absolute();t=Path(a.case_root).absolute()
 need(w.is_dir()and not w.is_symlink()and t.is_dir()and not t.is_symlink(),'Bad root')
 need(Path(__file__).absolute()==w/'custody_check.py','Wrong checker path')
 need(valid(a.expected_manifest_sha)and valid(a.expected_checker_sha),'Caller-held pins required')
 need(sha(regular(w/'custody_check.py'))==a.expected_checker_sha,'External checker pin')
 files={}
 for p in w.iterdir():files[p.name]=regular(p)
 need(sha(files['MANIFEST.json'])==a.expected_manifest_sha,'External manifest pin')
 m=parse(files['MANIFEST.json']);need(m['schema']=='pr788-priority-classical-crosscheck/v1'and m['head']==HEAD,'Wrong target')
 need(m['exceptions']==EXCEPTION,'Widened exception')
 rows=m['files'];need(set(files)==set(rows)|{'MANIFEST.json'}and'MANIFEST.json'not in rows,'Strict flat closure')
 required={'CHECKPOINT.json','INPUT_BINDINGS.json','REPORT.md','VERDICT.json','SOURCE_LEDGER.json','PRIMARY_FETCH_RECEIPTS.json','LIVE_VOR_VERSION_CHECK.json','OLD_SEAL_REPLAY.json','RESEARCH_LOG.md','custody_check.py','test_custody.py','CUSTODY_RECIPE.md'}
 need(required<=set(rows),'Missing required artifact')
 for n,r in rows.items():need('/'not in safe(n),'Nonflat authored name');check(files[n],r)
 b=parse(files['INPUT_BINDINGS.json']);need(b['head']==HEAD and b['bound_file_count']==64 and len(b['files'])==64,'Input scope')
 actual={}
 for n,r in b['files'].items():actual[n]=relative(t,n);check(actual[n],r)
 need(sha(actual['priority_question/REPORT.md'])==PEER,'Released peer report pin')
 need(sha(actual['priority_classical/MANIFEST.json'])==OLD_MANIFEST and sha(actual['priority_classical/custody_check.py'])==OLD_CHECKER,'Old immutable pins')
 critical={'priority_question_scratch/mundet_discrete2021v1.pdf':'025e8393073f144f2b91555300b9d05225cfdabb5786ad054298e80e5e38d5b4',
 'priority_question_scratch/mundet_discrete_vor.pdf':'cc0a420e104cc661dcf4b4000228832d1663543fd26f2243055923ccd6bae2fa',
 'priority_question_scratch/cwy2013v3.pdf':'27e694c2d2cb3bf19103eb1f419332e99bcf5a27bd2f1acbf14c2839715cefa3',
 'priority_classical_crosscheck_scratch/Mundet_current_VOR.pdf':'1fb4d6373049df6d904c83e3a06f5c4ec3b06af0d061d1ff8a50b15f305127c3'}
 for n,h in critical.items():need(sha(actual[n])==h and actual[n].startswith(b'%PDF'),'Primary PDF pin')
 ledger=parse(files['SOURCE_LEDGER.json'])
 need(len(ledger['sources'])==4 and len(ledger['visuals'])==4 and len(ledger['limitations'])>=5,'Evidence/read-scope ledger')
 for r in ledger['sources']:check(actual[r['file']],r);need(r['scope']and r['locator'],'Lost source read scope')
 fetch=parse(files['PRIMARY_FETCH_RECEIPTS.json']);need(len(fetch)==3,'Primary fetch scope')
 need(all(r['pdf_magic']is True and r['status']==200 for r in fetch),'Primary retrieval failure')
 version=parse(files['LIVE_VOR_VERSION_CHECK.json'])
 need(version['theorem11_normalized_equal']is True and version['section13_normalized_equal']is True,'Unresolved VOR comparison')
 need(version['old_section13_normalized_sha256']==version['live_section13_normalized_sha256']=='6f632d5cac1cf1c9d9b3c110100b53aeb4a5f3b6a3c8642a6cdec8b674e076d9','VOR section pin')
 v=parse(files['VERDICT.json']);need(v['head']==HEAD and v['status']=='C1_SUPPORTED_REQUIRED_PUBLICATION_CONTEXT'and v['new_substantive_proof_turns']==0,'Verdict scope')
 for k in ['actual_free_cyclic_every_odd_prime','fixed_manifold_quantifier_verified','no_continuous_circle','nonabelian_pi1_exclusion_verified','new_public_context_required','parent_agreement_and_peer_report_seen']:
  need(v.get(k)is True,'Required C1/exposure flag: '+k)
 for k in ['depends_on_hyperbolic_factor_dimension','effective_only_dismissal_valid','counterexample_to_verified_Wu_theorem','full_matching_Hanke_predecessor_verified','firstness_certified','absence_certified','worldwide_openness_certified','old_seal_modified','historical48_files_modified','source_or_git_mutations','publication_or_contact']:
  need(v.get(k)is False,'Inflated outcome flag: '+k)
 need(v['priority_status']=='UNRESOLVED'and len(v['required_publication_context'])==3,'Priority/context requirement')
 args=[sys.executable,'-B']+(['-O']if sys.flags.optimize else[])+[str(t/'priority_classical/custody_check.py'),'--packet',str(t/'priority_classical'),'--input-root',str(t/'intake'),'--expected-manifest-sha',OLD_MANIFEST,'--expected-checker-sha',OLD_CHECKER,'--source-root',str(t/'priority_classical_scratch')]
 child=subprocess.run(args,capture_output=True,timeout=15)
 need(child.returncode==0,'Old seal replay failure: '+child.stderr.decode())
 d=parse(child.stdout);need(d['status']=='PASS'and d['original_git_blobs']==48 and d['bound_source_inputs']==51 and d['external_scratch_files_checked']==31,'Old complete-custody scope')
 return {'status':'PASS','optimization':sys.flags.optimize,'manifest_sha256':a.expected_manifest_sha,'checker_sha256':a.expected_checker_sha,
 'authored_files':len(rows),'direct_external_bindings':64,'primary_pdf_artifacts':4,'viewed_renders':4,'old_original_git_blobs':48,'old_source_inputs':51,'old_external_files':31,'old_seal_unchanged':True,'scope':'Exact custody and bounded crosscheck consistency, not proof/novelty certification.'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['packet','case-root','expected-manifest-sha','expected-checker-sha']:p.add_argument('--'+n,required=True)
 try:print(json.dumps(main(p.parse_args()),indent=2,sort_keys=True))
 except Exception as e:print('CUSTODY_FAIL: '+str(e),file=sys.stderr);sys.exit(1)
