#!/usr/bin/env python3
"""Replay exact-byte packet checks. This program does not validate mathematics."""
import copy, hashlib, json, pathlib, shutil, stat, subprocess, sys, tempfile, zipfile
EXPECTED={'PROOF.md','README.md','REPORT.md','research_log.json','sources.json','status.json','verification_metadata.json','verify_packet.py'}
PINS={
 'author':('QUADRATIC_TWO_TYPE_2931_AUTHOR_SAFE_FREEZE.zip',14117,'a7feb177dbc27c56674e4333675303fa91cfbf2bfb61905273361934b8cca368','QUADRATIC_TWO_TYPE_2931_AUTHOR_EXTERNAL_MANIFEST.json','30bd1af52d976b711cc52a6c30abca55f0832ef9e767702232dc38b6e9051a20'),
 'corrected':('QUADRATIC_TWO_TYPE_2931_CORRECTED_SAFE.zip',14294,'ef24b757bb91a0854f13b40892fac78e7ca5a714ff4af14c4b5df4bcdf889c64','QUADRATIC_TWO_TYPE_2931_CORRECTED_EXTERNAL_MANIFEST.json','e2b2d992b3e4be35c8c2302b27f390cc1899b409cc2205a882b63e57aa61ceee')}
def check(c,m):
 if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 check(__debug__,'Replay must not run with -O or -OO')
 check(len(sys.argv) in (2,3),'Usage: replay_audit.py INPUT_DIRECTORY [OUTPUT_JSON]')
 root=pathlib.Path(sys.argv[1]).resolve();results=[];member_checks={}
 for label,(zn,size,zh,mn,mh) in PINS.items():
  z=root/zn;m=root/mn;blob=z.read_bytes();mb=m.read_bytes()
  check(len(blob)==size and sha(blob)==zh,'Untrusted archive: '+label);check(sha(mb)==mh,'Untrusted external manifest: '+label)
  manifest=json.loads(mb);entries={e['path']:e for e in manifest['files']};check(set(entries)==EXPECTED,'Wrong member set')
  with tempfile.TemporaryDirectory(prefix='quadratic-audit-') as td:
   t=pathlib.Path(td);packet=t/'packet';packet.mkdir();rows=[]
   with zipfile.ZipFile(z) as archive:
    info=archive.infolist();check(len(info)==8 and {x.filename for x in info}==EXPECTED,'Unsafe ZIP member inventory')
    for inf in info:
     check(not inf.is_dir() and stat.S_ISREG(inf.external_attr>>16),'Nonregular ZIP member')
     b=archive.read(inf);e=entries[inf.filename];check(len(b)==e['bytes'] and sha(b)==e['sha256'],'Member mismatch')
     (packet/inf.filename).write_bytes(b);rows.append(e)
   member_checks[label]=sorted(rows,key=lambda e:e['path']);verifier=packet/'verify_packet.py'
   def run(test,target,mp=m,flags=(),expected=2):
    p=subprocess.run([sys.executable,*flags,str(verifier),str(target),str(mp)],cwd=t,text=True,capture_output=True)
    row={'packet':label,'test':test,'expected_exit':expected,'exit_code':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()};results.append(row)
    check(p.returncode==expected,label+': '+test+' returned unexpected exit')
   run('directory_normal',packet,expected=0);run('zip_normal',z,expected=0)
   run('optimized_explicit_rejection',packet,flags=('-O',));run('doubly_optimized_explicit_rejection',packet,flags=('-OO',))
   bad=t/'bad';shutil.copytree(packet,bad);(bad/'PROOF.md').write_bytes((bad/'PROOF.md').read_bytes()+b'changed\n');run('tampered_member',bad);shutil.rmtree(bad)
   shutil.copytree(packet,bad);(bad/'unexpected.txt').write_text('extra');run('unexpected_member',bad);shutil.rmtree(bad)
   badm=t/'bad_manifest.json';mm=copy.deepcopy(manifest);mm['problem_id']=2932;badm.write_text(json.dumps(mm));run('wrong_problem',packet,badm)
   badm.write_text('{"problem_id":2931,"problem_id":2931}');run('duplicate_json_key',packet,badm)
   badz=t/'bad.zip';badz.write_bytes(blob+b'x');run('tampered_zip',badz)
   relocated=t/'relocated space';relocated.mkdir();rz=relocated/'packet.zip';rm=relocated/'manifest.json';rz.write_bytes(blob);rm.write_bytes(mb);run('relocated_zip_and_manifest',rz,rm,expected=0)
   shutil.copytree(packet,bad);old=(bad/'PROOF.md').read_bytes();(bad/'PROOF.md').write_bytes(bytes([old[0]^1])+old[1:]);run('same_size_member_mutation',bad);shutil.rmtree(bad)
   shutil.copytree(packet,bad);(bad/'PROOF.md').unlink();run('missing_member',bad);shutil.rmtree(bad)
   link=t/'packet_link';link.symlink_to(packet,target_is_directory=True);run('symlink_target',link)
   ml=t/'manifest_link';ml.symlink_to(m);run('symlink_manifest',packet,ml)
   shutil.copytree(packet,bad);(bad/'PROOF.md').unlink();(bad/'PROOF.md').symlink_to(packet/'PROOF.md');run('symlink_member',bad);shutil.rmtree(bad)
   mm=copy.deepcopy(manifest);mm['schema_version']=float('nan');badm.write_text(json.dumps(mm));run('nonfinite_manifest',packet,badm)
   mm=copy.deepcopy(manifest);mm['files'][0]['bytes']=True;badm.write_text(json.dumps(mm));run('boolean_byte_count',packet,badm)
   mm=copy.deepcopy(manifest);mm['files'][0]['sha256']='0'*64;badm.write_text(json.dumps(mm));run('wrong_member_digest',packet,badm)
 report={'problem_id':2931,'tests':results,'test_count':len(results),'all_expected_outcomes':True,'member_checks':member_checks,'mathematical_validation':False,'optimization_note':'-O and -OO are intentionally rejected with exit 2; these are rejection tests, never mathematical passes.'}
 out=json.dumps(report,indent=2)+'\n'
 if len(sys.argv)==3:pathlib.Path(sys.argv[2]).write_text(out)
 else:print(out,end='')
if __name__=='__main__':main()
