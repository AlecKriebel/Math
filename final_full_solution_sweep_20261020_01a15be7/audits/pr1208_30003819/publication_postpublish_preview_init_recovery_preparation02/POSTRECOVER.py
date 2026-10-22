"""Externally prehashed exact record23578142 postpublish recovery; no bundled authority."""
from pathlib import Path
import argparse,hashlib,json,sys
P=Path(__file__).resolve().parent
MODULES=['POSTRECOVER.py','preview_policy.py','postpublish_adapter.py','postpublish_guard.py','INPUT_BINDINGS.json']
def need(v,m):
 if not v:raise RuntimeError(m)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def parser():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['check-preparation','reconcile','verify-public','ledger']);p.add_argument('--source-sha256',required=True);p.add_argument('--authorization-sha256');p.add_argument('--execute-one',action='store_true');return p
def main(argv=None):
 need(sys.flags.isolated and sys.flags.no_site and sys.flags.optimize==0 and __debug__,'Use CPython -I -S -B optimize0 before loading project code');a=parser().parse_args(argv)
 raw=(P/'SOURCE_MANIFEST.json').read_bytes();need(pin(raw)['sha256']==a.source_sha256,'Externally pinned source differs');m=json.loads(raw);need(set(m['files'])==set(MODULES),'Exact new source modules required');buffers={k:(P/k).read_bytes() for k in MODULES}
 for name,body in buffers.items():need(pin(body)==m['files'][name],'New checked module changed')
 def source_check():
  need((P/'SOURCE_MANIFEST.json').read_bytes()==raw,'New source manifest changed')
  for k,b in buffers.items():need((P/k).read_bytes()==b,'New source changed: '+k)
 def execute(name,body,path):
  ns={'__name__':name,'__file__':str(path)};exec(compile(body,str(path),'exec',dont_inherit=True),ns);return ns
 g=execute('postpublish_guard',buffers['postpublish_guard.py'],P/'postpublish_guard.py');policy=execute('preview_policy',buffers['preview_policy.py'],P/'preview_policy.py');adapter=execute('postpublish_adapter',buffers['postpublish_adapter.py'],P/'postpublish_adapter.py');b=g['strict'](buffers['INPUT_BINDINGS.json']);old=P.parent/'publication_samecase_recovery_preparation01'
 oldmodules={}
 for name in ['recovery_guard.py','recovery_adapter.py']:
  path=old/name;body=g['readpin'](path,b['refs'][str(path)]);oldmodules[name]=execute(name[:-3],body,path)
 og=oldmodules['recovery_guard.py'];oa=oldmodules['recovery_adapter.py'];c=g['contract'](P,a.source_sha256,og);g['preserved'](c);pairs=oa['capture_namespace'](c['case']/'reads',g['strict'])[0]
 if a.action=='check-preparation':
  need(not a.execute_one and a.authorization_sha256 is None,'Check never authorizes action');proposed=g['strict']((P/'PROPOSED_AUTHORIZATION.json').read_bytes());need(proposed['template_only'] is True and proposed['ready_for_execution'] is False,'No self-generated authority');print(json.dumps({'status':'PREPARED_NOT_ADOPTED','record':23578142,'capture_pairs':pairs,'original_successful_POST_retained':True,'readiness':False}));return
 auth=g['verify_authorization'](c,a.authorization_sha256,a.action,source_check);og['packet_check'](P,auth['packet_manifest_sha256']);og['packet_check'](old,g['strict']((c['old']['new']).read_bytes())['recovery_packet_manifest_sha256'])
 core=P.parent/'publication_operations_preparation_07';body=(core/'bootstrap.py').read_bytes();need(pin(body)['sha256']==g['BOOT07'],'Original bootstrap changed');boot=execute('checked_original_bootstrap07',body,core/'bootstrap.py');load,_=boot['load_verified'](core,g['SOURCE07'],g['BOOT07']);common=load('common');common.authority(c['old']['old'],g['OLD_SHA'] if 'OLD_SHA' in g else og['OLD_SHA'],a.action)
 if not a.execute_one:print(json.dumps({'status':'AUTHORITY_VALIDATED_NO_ACTION','service_calls':0,'CASE_changed':False,'action':a.action}));return
 providers=load('providers');life=load('lifecycle');native=load('native_policy');runner=load('runner');original=(core/'native_policy.py').read_bytes();source07=g['strict']((core/'SOURCE_MANIFEST.json').read_bytes());policy['install'](native,life,original,source07['files']['native_policy.py'])
 Provider=adapter['provider_class'](oa['provider_class'](providers,c['case']/'reads'))
 def checker(e):
  g['verify_authorization'](c,a.authorization_sha256,a.action,source_check);e.p.verify_captures()
 binding={k:b[k] for k in ['original_publish_response','original_publish_intent','original_publish_phase_intent']};binding['additive_authorization']={'path':str(c['new']),'sha256':a.authorization_sha256,'source_sha256':a.source_sha256}
 runner.RealProvider=Provider;runner.Engine=adapter['engine_class'](life,checker,binding)
 return runner.main([a.action,'--expected-pr-head',b['head'],'--adoption',str(c['old']['old']),'--adoption-sha256',b['original_authority_sha256']])
if __name__=='__main__':main()
