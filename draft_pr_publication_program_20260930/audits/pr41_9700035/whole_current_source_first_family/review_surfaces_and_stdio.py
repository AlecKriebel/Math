#!/usr/bin/env python3
"""Independent complete retained-stdio and surface-presentation inspection.
Reads frozen input only; executes/imports no submitted source.
"""
from pathlib import Path
import datetime,hashlib,json,math,os
R=Path(__file__).resolve().parent
C=R.parent/'reviewed_candidate'
PIN='3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa'
def H(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def check(x,s):
 if not x:raise ValueError(s)
def pairs(xs):
 d={}
 for k,v in xs:check(k not in d,'duplicate JSON key');d[k]=v
 return d
def constant(s):raise ValueError(s)
def floating(s):
 x=float(s);check(math.isfinite(x),'nonfinite JSON number');return x
def J(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=constant,parse_float=floating)
def leaves(x):
 if type(x) is dict:return 1+sum(leaves(v) for v in x.values())
 if type(x) is list:return 1+sum(leaves(v) for v in x)
 return 1
def main():
 started=now();check(H((C/'MANIFEST.json').read_bytes())==PIN,'current manifest pin')
 m=J((C/'MANIFEST.json').read_bytes());streams=[];errors=[];json_values=[];plain=[]
 for item in m['files']:
  p=C/item['path'];b=p.read_bytes()
  check(len(b)==item['bytes'] and H(b)==item['sha256'],'immutable complete file')
  n=p.name.lower()
  if 'stdout' not in n and 'stderr' not in n:continue
  t=b.decode('utf8');channel='stderr' if 'stderr' in n else 'stdout'
  row={'path':item['path'],'bytes':len(b),'sha256':H(b),'channel':channel,'complete_UTF8_read':True}
  if b.strip():
   try:
    value=J(b);row.update(content='whole_strict_JSON',typed_nodes=leaves(value));json_values.append({'path':item['path'],'value':value})
   except (ValueError,UnicodeError):
    row['content']='complete_plain_text';plain.append({'path':item['path'],'text':t})
  else:row['content']='empty'
  streams.append(row)
  if channel=='stderr' and b:errors.append({'path':item['path'],'bytes':len(b),'sha256':H(b),'complete_text':t})
 qualification=(C/'SOURCE_PROOF_QUALIFICATIONS.md').read_bytes()
 check(H(qualification)=='69196e84de0d627b31b6f2a20a3745ba33048969cb93efba92a886bfedf8bc7e','exact source qualification')
 targets=['README.md','SOURCE_AUDIT.md','review/REVIEW.md','pr_body.md']
 for name in targets:
  b=(C/name).read_bytes();check(b.endswith(qualification) and b.count(qualification)==1,'exact source note appended once: '+name)
 for name in ['SOURCE_AUDIT.md','review/REVIEW.md']:
  original=(C/'original_archive'/name).read_bytes();b=(C/name).read_bytes()
  check(b.count(original)==1 and b.index(original)<b.index(qualification),'complete original body preserved and qualified: '+name)
 for name in ['CURRENT_CONTEXT.md','CURRENT_AUDIT_SCOPE.md']:
  b=(C/name).read_bytes()
  check(b'full indexed target UNSOLVED' in b and b't^4 P(D>t)->0' in b and b'weak SIRSN' in b and b'PENDING' in b,'summary scoped limits')
 # The genuine completed root producers had empty stderr; historical negative
 # controls and the disclosed V1 closure failure are retained separately.
 check(all(not x['bytes'] for x in streams if x['channel']=='stderr' and x['path'].startswith('root_verification/')),'root successful channels empty stderr')
 check(all(not x['bytes'] for x in streams if x['channel']=='stderr' and x['path'].startswith('build/')),'successful builder/reconstruction channels empty stderr')
 result={'status':'PASS_OWN_FULL_STDIO_AND_CURRENT_PRESENTATION_CONTROLS','pid':os.getpid(),'started_utc':started,'finished_utc':now(),'current_manifest_sha256':PIN,'stream_files':len(streams),'complete_stream_bytes':sum(x['bytes'] for x in streams),'strict_JSON_stream_objects':len(json_values),'strict_JSON_stream_typed_nodes':sum(x.get('typed_nodes',0) for x in streams),'nonempty_stderr_files':len(errors),'plain_text_stream_files':len(plain),'exact_note_appended_once_to_all_four_current_targets':True,'original_source_review_complete_body_qualified':True,'candidate_helper_imports_or_execution':False,'shared_native_Git_remote_writes':False,'presentation_limitation':'CURRENT_CONTEXT and CURRENT_AUDIT_SCOPE summarize with inherited appended-below/follows wording although their summary bodies point elsewhere; the exact qualification/body is present and bound in the four actual current target surfaces.'}
 for filename,obj in [('WHOLE_CURRENT_STDIO_READ_LEDGER.json',streams),('WHOLE_CURRENT_STDIO_COMPLETE_JSON_VALUES.json',json_values),('WHOLE_CURRENT_STDIO_COMPLETE_PLAIN_VALUES.json',plain),('WHOLE_CURRENT_NONEMPTY_STDERR.json',errors),('CURRENT_PRESENTATION_STDIO_RESULT.json',result)]:
  (R/filename).write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 print(json.dumps(result,indent=2))
 print(json.dumps(errors,indent=2))
if __name__=='__main__':main()
