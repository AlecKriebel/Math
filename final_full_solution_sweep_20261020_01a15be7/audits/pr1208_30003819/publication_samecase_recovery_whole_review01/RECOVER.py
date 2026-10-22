"""External prehashed additive same-CASE adapter launcher. No bundled recovery authority."""
from pathlib import Path
import argparse,hashlib,json,sys
P=Path(__file__).resolve().parent
MODULES=['RECOVER.py','recovery_adapter.py','recovery_guard.py','INPUT_BINDINGS.json']
def need(v,m):
 if not v:raise RuntimeError(m)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def main(argv=None):
 need(sys.flags.isolated and sys.flags.no_site and sys.flags.optimize==0 and __debug__,'Use CPython-I-S-B optimize0 before loading project code')
 p=argparse.ArgumentParser();p.add_argument('action',choices=['check-preparation','integrate','describe','ready','merge','stage','publish','verify-public','ledger','reconcile']);p.add_argument('--adapter-source-sha256',required=True);p.add_argument('--recovery-authorization-sha256');p.add_argument('--execute-one',action='store_true');a=p.parse_args(argv)
 raw=(P/'SOURCE_MANIFEST.json').read_bytes();need(pin(raw)['sha256']==a.adapter_source_sha256,'External adapter-source anchor differs');m=json.loads(raw);need(set(m['files'])==set(MODULES),'Exact adapter modules required');buffers={name:(P/name).read_bytes() for name in MODULES}
 for name,body in buffers.items():need(pin(body)==m['files'][name],'Adapter source changed')
 def source_check():
  need(pin((P/'SOURCE_MANIFEST.json').read_bytes())['sha256']==a.adapter_source_sha256,'Adapter manifest changed')
  for name,body in buffers.items():need((P/name).read_bytes()==body,'Expected adapter bytes changed')
 modules={}
 for name in ['recovery_guard.py','recovery_adapter.py']:
  ns={'__name__':name[:-3],'__file__':str(P/name)};exec(compile(buffers[name],str(P/name),'exec',dont_inherit=True),ns);modules[name]=ns
 g=modules['recovery_guard.py'];adapter=modules['recovery_adapter.py'];c=g['contract'](P,a.adapter_source_sha256);g['preserved'](c);capture_pairs=adapter['capture_namespace'](c['case']/'reads',g['strict'])[0]
 if a.action=='check-preparation':
  need(not a.execute_one and a.recovery_authorization_sha256 is None,'Preparation inspection never authorizes effects');d=g['strict']((P/'PROPOSED_RECOVERY_AUTHORIZATION.json').read_bytes());need(d['ready_for_execution'] is False and d['template_only'] is True,'No self-generated recovery authority');print(json.dumps({'status':'PREPARED_RECOVERY_NOT_ADOPTED','original_prefix_preserved':True,'capture_pairs':capture_pairs,'ready_for_execution':False}));return
 authorization=g['verify_authorization'](c,a.recovery_authorization_sha256,a.action,source_check);g['packet_check'](P,authorization['recovery_packet_manifest_sha256'])
 core=P.parent/'publication_operations_preparation_07';body=(core/'bootstrap.py').read_bytes();need(pin(body)['sha256']==g['BOOT07'],'Original bootstrap differs');ns={'__name__':'externally_checked_original07','__file__':str(core/'bootstrap.py')};exec(compile(body,str(core/'bootstrap.py'),'exec',dont_inherit=True),ns);load,_=ns['load_verified'](core,g['SOURCE07'],g['BOOT07']);common=load('common');common.authority(c['old'],g['OLD_SHA'],a.action)
 if not a.execute_one:print(json.dumps({'status':'RECOVERY_AUTHORITY_VALIDATED_NO_ACTION','action':a.action,'service_calls':0,'CASE_changed':False}));return
 g['action_precheck'](c,a.action);providers=load('providers');lifecycle=load('lifecycle');runner=load('runner');Provider=adapter['provider_class'](providers,c['case']/'reads')
 def checker(engine):
  g['verify_authorization'](c,a.recovery_authorization_sha256,a.action,source_check);engine.p.verify_captures()
 binding={'recovery_authorization_path':str(c['new']),'recovery_authorization_sha256':a.recovery_authorization_sha256,'adapter_source_sha256':a.adapter_source_sha256,'original_authority_sha256':g['OLD_SHA']};Engine=adapter['engine_class'](lifecycle,checker,c['phase_pin'],binding);runner.RealProvider=Provider;runner.Engine=Engine
 return runner.main([a.action,'--expected-pr-head',g['head_for'](c,a.action),'--adoption',str(c['old']),'--adoption-sha256',g['OLD_SHA']])
if __name__=='__main__':main()
