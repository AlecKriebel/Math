"""Controls run only on owned scratch copies and outputs; no sealed input changes."""
from pathlib import Path
import subprocess,shutil,json,sys,hashlib,os
W=Path(__file__).absolute().parent;S=W.parent/'preprint/source';P=W.parent/'preprint/output/pdf/paper.pdf';D=W.parent/'whole_preprint_round01_scratch/controls';D.mkdir(parents=True,exist_ok=True)
PIN='6287da0dabdad505f3d312dfeefc9e75f34caaeccb267fada3f9119502cfa6be'
rows=[]
def run(name,cmd,expected):
 p=subprocess.run([sys.executable,'-I','-B']+cmd,cwd='/',capture_output=True,text=True,timeout=120)
 ok=(p.returncode==0)==expected
 rows.append({'name':name,'expected_accept':expected,'returncode':p.returncode,'matched_expectation':ok,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()})
 if not ok:raise ValueError('unexpected control result: '+name)
def vf(s,pin=PIN):return [str(s/'verify_source.py'),'--expected-manifest-sha256',pin,'--pdf',str(P)]
def bf(s,out,pdf=P):return [str(s/'build_package.py'),'--expected-manifest-sha256',PIN,'--pdf',str(pdf),'--output-dir',str(out)]
def copy(name):
 dst=D/name
 if dst.exists():shutil.rmtree(dst)
 shutil.copytree(S,dst);return dst
run('baseline_source_core_zero_bodies',vf(S),True)
run('wrong_external_manifest_pin',vf(S,'0'*64),False)
for name,mutation in [('changed_source',lambda s:(s/'README.md').write_bytes((s/'README.md').read_bytes()+b'changed')),('unexpected_source_file',lambda s:(s/'extra').write_text('extra')),('missing_source_file',lambda s:(s/'LICENSE.txt').unlink()),('empty_source_directory',lambda s:(s/'empty').mkdir()),('source_leaf_symlink',lambda s:((s/'LICENSE.txt').unlink(),(s/'LICENSE.txt').symlink_to(S/'LICENSE.txt'))),('source_subdirectory_symlink',lambda s:(shutil.rmtree(s/'audit/math_quotient_algebra'),(s/'audit/math_quotient_algebra').symlink_to(S/'audit/math_quotient_algebra',target_is_directory=True)))]:
 s=copy(name);mutation(s);run(name,vf(s),False)
s=copy('relocated');run('relocated_core_zero_bodies',vf(s),True)
run('build_inside_source',bf(S,S/'forbidden-output'),False)
wrong=D/'wrong.pdf';wrong.write_bytes(P.read_bytes()+b'changed');run('wrong_pdf',bf(S,D/'wrong_pdf_out',wrong),False)
out=D/'linked_out';out.mkdir(exist_ok=True);(out/'main.tex').symlink_to(S/'main.tex');run('symlink_output_file',bf(S,out),False)
out=D/'hardlink_out';out.mkdir(exist_ok=True);donor=D/'disposable_hardlink_target';donor.write_bytes((S/'main.tex').read_bytes());os.link(donor,out/'main.tex');run('hardlinked_output_file',bf(S,out),False);(out/'main.tex').unlink()
out=D/'ancestor_out';out.symlink_to(D/'real_out',target_is_directory=True);run('symlink_output_ancestor',bf(S,out/'child'),False)
# Historical direct author invocation resolves a verifier symlink; operative wrapper rejects it.
orig=S/'audit/intake/original/unsolved_math_prioritization/attempts/30001478';alias=D/'historical_verify.py';alias.symlink_to(orig/'author/verify.py');run('historical_author_self_symlink_caveat', [str(alias)],True)
legacy=copy('wrapper_guard')/'audit/intake/original/unsolved_math_prioritization/attempts/30001478';f=legacy/'author/verify.py';data=f.read_bytes();replacement=D/'replacement_verify.py';replacement.write_bytes(data);f.unlink();f.symlink_to(replacement);run('operative_original_wrapper_rejects_child_symlink',[str(legacy/'verify_publication.py'),'--expected-manifest','f1aab7f750c4c2aba55ba52addbfdd211de3b47edb6fa898387b2720b713e58d','--integrity-only'],False)
run('source_rechecked_after_controls',vf(S),True)
(W/'CONTROL_RESULTS.json').write_text(json.dumps({'result':'PASS','controls':rows,'count':len(rows),'scope':'No hostile concurrent filesystem actor tested. Historical self-symlink acceptance is reproduced and bounded by operative wrapper protection.'},indent=2)+'\n')
print('PASS',len(rows))
