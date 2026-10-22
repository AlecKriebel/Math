from pathlib import Path
import json,hashlib,sys
P=Path(__file__).resolve().parent;S=P/'source'
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
body=(S/'bootstrap17.py').read_bytes();BS='5a60e8743ab5dd72e113a75f9af370974a0895bdabd8e68321d58701c947ae94';MS='623a85eca963527260367dd192bb0373f6a81972179633fa6f219c72a6237803'
need(sha(body)==BS,'Own bootstrap changed')
ns={'__file__':str(S/'bootstrap17.py'),'__name__':'source_parameter_probe'}
exec(compile(body,str(S/'bootstrap17.py'),'exec',dont_inherit=True,optimize=0),ns)
rows=[]
for label,ms,bs in [('wrong_source','0'*64,BS),('wrong_bootstrap',MS,'0'*64)]:
 reads=[];prior=Path.read_bytes
 def guarded(p):
  reads.append(str(p))
  need(p==S or S in p.parents,'Project dependency read before parameter rejection')
  return prior(p)
 Path.read_bytes=guarded
 try:
  try:ns['load_verified'](S,ms,bs)
  except RuntimeError as e:error=str(e)
  else:raise RuntimeError('Bad source parameter accepted')
 finally:Path.read_bytes=prior
 need(error in {'Operations17 source seal changed','Operations17 bootstrap changed'},'Unexpected source-parameter failure: '+error)
 rows.append({'case':label,'status':'PASS_REJECTED_BEFORE_DEPENDENCY_LOAD','error':error,'source_reads':reads,'outside_source_reads':0})
out={'cases':rows,'source_manifest_sha256':MS,'bootstrap_sha256':BS,'actual_effects':0,'project_dependency_loads':0,'publication_ready':False}
(P/'private/SOURCE_PARAMETER_REJECTIONS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
