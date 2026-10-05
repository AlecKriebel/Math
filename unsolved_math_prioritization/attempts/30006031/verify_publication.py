#!/usr/bin/env python3
"""Mandatory strict audit guard and byte-exact replay; Python standard library only."""
import argparse, hashlib, importlib.util, json, os, stat, subprocess, sys, tempfile, zipfile
from pathlib import Path, PurePosixPath
ROOT=Path(__file__).absolute().parent
FROZEN={'OPERADIC_CENTER_30006031_AUTHOR_PACKET.zip': {'bytes': 25495, 'sha256': '80e41bf9af68cbd1197495c188ba3ea956b541238ea33ab0ea4cbadfeabecb60'}, 'OPERADIC_CENTER_30006031_INDEPENDENT_AUDIT.zip': {'bytes': 48563, 'sha256': 'fa00b34d9b275451bb751fa489a541471cd15d71e29807c8e5b61f253ca33020'}, 'audit/AUDIT_MANIFEST.json': {'bytes': 2921, 'sha256': 'ef3b6fa42a354e507161350342610839017dc6757ef0cc9d6f1ac5e3b2e693ba'}, 'audit/AUDIT_REPORT.md': {'bytes': 12825, 'sha256': '09e92ffac549e9aa76c34587652822f169dc5b2a69fef4b2cb09bee6dff3b765'}, 'audit/AUDIT_RESULTS.json': {'bytes': 2575, 'sha256': '5572b338ce5e34dfbd778cc328acf597922b55bfe0772719a1f4e0ccde4a3de0'}, 'audit/CORRECTIONS.md': {'bytes': 2485, 'sha256': '4dd83b1add7609a19359ec931cefb66e5aa775a2505ab57ad91ec3d5a7d7f199'}, 'audit/EXTERNAL_AUDIT_RESULTS.json': {'bytes': 5811, 'sha256': '1634d83f5594a80e101ea5ecaa5bfd1e905d7a137cea43fdecdddc9b01683579'}, 'audit/PACKAGE_CHECKS.json': {'bytes': 1614, 'sha256': 'ee9b838ba6e13042ed011e6eaddd1ed3a66f48527073763da8b354b53424327f'}, 'audit/README.md': {'bytes': 1537, 'sha256': 'ba356c5ef0e5028a77bdd6bdca736e631fd0cb4c9b5b539c2b4d516b9ab77907'}, 'audit/SOURCE_AUDIT.json': {'bytes': 10045, 'sha256': '69080ee43fa83bca5c7d5a7351f7e8063ab70c6e847d7e0e6d525478cd05a7fa'}, 'audit/author/APPROACH_LOG.json': {'bytes': 4804, 'sha256': 'f0a912f4bd7297335fc06dd03b6ee36b9a0c8fb74587aa2646479efd8822769b'}, 'audit/author/EXTERNAL_REPLAY.json': {'bytes': 3206, 'sha256': 'eb036f9fb3114690e2a9b4056e58e2dd7d5c6f3e10fbfca5189fa4b93e2ac96c'}, 'audit/author/MANIFEST.json': {'bytes': 1513, 'sha256': '64feb895b04279f97b88a9f624d5d75d9937b14d3b10981badf790e5dc2bb619'}, 'audit/author/PROOF.md': {'bytes': 15974, 'sha256': 'dac45b750f2bae44384b01bdac42a66ed5a46114e4418427ce0335450a00e3eb'}, 'audit/author/README.md': {'bytes': 2803, 'sha256': '35313c59a67d41db15acf571b09b01481def9075f4ef32cf9aea25ca06684002'}, 'audit/author/RESULTS.json': {'bytes': 2965, 'sha256': 'dbd21f46f9ba0d939bef93e5025edf1443929541c5df9104652dbb20b04031c0'}, 'audit/author/SOURCE_GATE.md': {'bytes': 8852, 'sha256': '34aa224917bf42a2314a1f7d444d283e4d3d2592aa7e9af4eaa4d56c1c6b5ab1'}, 'audit/author/SOURCE_VERIFICATION.json': {'bytes': 8942, 'sha256': '73ce2013442cbd5efcaea2795fddcd8094d0429776bbd48bcc8094e94ed44715'}, 'audit/author/VALIDATION.md': {'bytes': 2807, 'sha256': '59f3a38aab77b81fb837fc63358db77b78032fdc78b4ad1fbc53631abb718fac'}, 'audit/author/verify.py': {'bytes': 11297, 'sha256': 'd80e5505ab864490304576017d0eb4b314bb291ca385e86f977e5a1888022c7c'}, 'audit/verify_audit.py': {'bytes': 15573, 'sha256': '7c9c9955edadec7b2bfe7d2d59e32c490cf61f53dfa6a2d02241b31f88cb5068'}}
SCOPE={'author_guard_dangling_symlink_bug_preserved': True, 'formal_verification': False, 'free_E2_scope': 'The specified free E2 action cannot extend along E2 to E3; no target counterexample and no obstruction to an unrelated E3 action.', 'general_problem_solved': False, 'historical_labels': 'The unchanged author audit-pending and audit no-remote-writes labels describe their freeze checkpoints.', 'human_peer_review': False, 'independent_audit': 'ACCEPT_SCOPED_ARGUMENTS_WITH_PACKAGING_GUARD_CORRECTION', 'indexing_scope': 'The printed K_m convention and E2 claim disagree in arity two; normalizing levels is not an E3 theorem.', 'novelty_certified': False, 'problem_id': 30006031, 'problem_number': 'OWR-14298590-001', 'rank': 792, 'remaining_gap': 'Intended derived-center definition/model hypotheses and the coherent E3 construction and comparison remain unrecovered.', 'review_sha256': '5576c84aff240284caeb8d3ea655c4be9c82ed64d9a7c4737888242b70cb9487', 'statement_sha256': '9c4f90cf2e091ef4dc8f2336fcac77d255b9acf432b0c9ea645596fd62b5a33c', 'status': 'unsolved', 'strict_audit_guard_mandatory': True, 'strict_center_scope': 'The explicitly defined strict unary center is a commutative monoid with Com and hence little-disks actions; no identification with the intended derived center.', 'target_counterexample': False, 'turns': '5/5'}
AUDIT_DIGEST='ef3b6fa42a354e507161350342610839017dc6757ef0cc9d6f1ac5e3b2e693ba'
AUTHOR_DIGEST='64feb895b04279f97b88a9f624d5d75d9937b14d3b10981badf790e5dc2bb619'
ARCHIVES=[('OPERADIC_CENTER_30006031_AUTHOR_PACKET.zip','audit/author','MANIFEST.json'),('OPERADIC_CENTER_30006031_INDEPENDENT_AUDIT.zip','audit','AUDIT_MANIFEST.json')]
def need(ok,label):
 if not ok: raise RuntimeError('FAIL: '+label)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def guard(root):
 need(stat.S_ISDIR(root.lstat().st_mode),'regular packet root directory')
 p=root/'audit/verify_audit.py';need(stat.S_ISDIR(p.parent.lstat().st_mode),'audit directory')
 need(stat.S_ISREG(p.lstat().st_mode),'regular audit verifier')
 need(pin(p.read_bytes())==FROZEN['audit/verify_audit.py'],'trusted audit verifier bytes before import')
 spec=importlib.util.spec_from_file_location('operadic_strict_audit',p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def integrity(root,expected):
 audit=guard(root)
 result=audit.verify_manifest(root/'PUBLICATION_MANIFEST.json',expected)
 audit.verify_manifest(root/'audit/AUDIT_MANIFEST.json',AUDIT_DIGEST)
 audit.verify_manifest(root/'audit/author/MANIFEST.json',AUTHOR_DIGEST)
 for n,h in FROZEN.items():need(pin((root/n).read_bytes())==h,'immutable '+n)
 need(json.loads((root/'PUBLICATION.json').read_bytes())==SCOPE,'scope metadata')
 for name,folder,mname in ARCHIVES:
  d=root/folder;manifest=json.loads((d/mname).read_bytes());members={r['path'] for r in manifest['files']}|{mname}
  with zipfile.ZipFile(root/name) as z:
   infos=z.infolist();need(len(infos)==len(members) and {i.filename for i in infos}==members,'exact ZIP inventory')
   need(z.testzip() is None,'ZIP CRC')
   for i in infos:
    p=PurePosixPath(i.filename);mode=i.external_attr>>16;ft=stat.S_IFMT(mode)
    need(not p.is_absolute() and '..' not in p.parts and str(p)==i.filename and '\\' not in i.filename,'safe ZIP path')
    need(not i.is_dir() and ft in (0,stat.S_IFREG) and not i.flag_bits&1,'regular unencrypted ZIP member')
    need(z.read(i)==(d/i.filename).read_bytes(),'exact ZIP member bytes')
 return result['files']+1

def run(script,*args):
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 with tempfile.TemporaryDirectory(prefix='operadic-replay-') as tmp:
  # Starting a new normal interpreter keeps checks active even under an optimized parent.
  check=subprocess.run([sys.executable,'-B','-c','import sys; print(__debug__, sys.flags.optimize)'],env=env,cwd=tmp,capture_output=True,check=True)
  need(check.stdout==b'True 0\n','child assertions active')
  r=subprocess.run([sys.executable,'-B',str(script),*map(str,args)],env=env,cwd=tmp,capture_output=True,timeout=300)
 need(r.returncode==0 and not r.stderr,'normal replay '+script.name)
 return r.stdout

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--expected-manifest',required=True,help='Externally trusted SHA-256 of PUBLICATION_MANIFEST.json')
 for n in ['catalog','problems','research','source-dir']:ap.add_argument('--'+n,type=Path)
 args=ap.parse_args();count=integrity(ROOT,args.expected_manifest)
 for s,e,n in [('audit/author/verify.py','audit/author/RESULTS.json',900),('audit/verify_audit.py','audit/AUDIT_RESULTS.json',19322)]:
  b=run(ROOT/s);need(b==(ROOT/e).read_bytes(),'byte-identical default '+s);need(json.loads(b)['assertions_passed']==n,'default exact count')
 b=run(ROOT/'audit/verify_audit.py','--author-dir',ROOT/'audit/author','--manifest',ROOT/'audit/AUDIT_MANIFEST.json','--expected-manifest',AUDIT_DIGEST);r=json.loads(b)
 need(r['assertions_passed']==19327,'author replay audit count')
 need(r['author_replay']['author_dangling_symlink_blind_spot_reproduced'] is True,'original bug reproduced')
 need(r['author_replay']['audit_guard_rejected_it'] is True,'strict guard rejects original bug')
 external='NOT_RUN_EXTERNAL_INPUTS_REQUIRED';given=[args.catalog,args.problems,args.research,args.source_dir]
 if any(given):
  need(all(given),'all four external inputs required')
  need(all(p.is_file() for p in given[:3]) and args.source_dir.is_dir(),'external paths exist')
  opts=['--author-dir',ROOT/'audit/author','--source-metadata',ROOT/'audit/author/SOURCE_VERIFICATION.json']
  for flag,p in zip(['catalog','problems','research','source-dir'],given):opts+=['--'+flag,p.absolute()]
  b=run(ROOT/'audit/verify_audit.py',*opts);need(b==(ROOT/'audit/EXTERNAL_AUDIT_RESULTS.json').read_bytes(),'byte-identical full external replay')
  need(json.loads(b)['assertions_passed']==19359,'external exact count');external='PASS_19359_CHECKS_BYTE_IDENTICAL'
 out={'status':'PASS_WITH_DOCUMENTED_AUTHOR_GUARD_CORRECTION','problem_id':30006031,'disposition':'UNSOLVED 5/5','packet_files':count,'frozen_files_and_archives':len(FROZEN),'author_default_assertions':900,'audit_default_assertions':19322,'audit_author_replay_assertions':19327,'author_default_replay':'byte-identical','audit_default_replay':'byte-identical','strict_guard':'mandatory; trusted digests; lstat; exact recursive files and directories','author_guard_regression':'Original dangling-symlink bug reproduced; strict audit guard rejects it','replay_children':'normal Python; PYTHONOPTIMIZE removed; assertions active','external_evidence_replay':external,'general_problem_solved':False,'target_counterexample':False}
 b=(json.dumps(out,indent=2,sort_keys=True)+'\n').encode()
 if external=='NOT_RUN_EXTERNAL_INPUTS_REQUIRED':need(b==(ROOT/'VERIFICATION_RESULTS.json').read_bytes(),'exact publication result')
 sys.stdout.buffer.write(b)
if __name__=='__main__':main()
