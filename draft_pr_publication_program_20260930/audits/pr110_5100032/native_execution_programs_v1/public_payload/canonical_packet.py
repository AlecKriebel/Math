"""Local canonical packet construction only; never creates evidence/clearance or executes."""
import argparse,pathlib
import native_worker as w
import native_runner as r
import protocol as p
FIELDS={'schema','template_only','identity','main_parent','workspace_parent','program_files','native_baseline','input_files',
 'original','package','publication_receipt','sheet_receipt','service_process_contracts','preflight_receipt','runtime','source_cache','raw_source_pins',
 'resources','parent_policy','assessment_overlay','campaign_note','import_UTC','attempt_offer_sources','checked_artifacts'}
def build_packet(obj):
    r.need(set(obj)==FIELDS and obj['schema']=='pr110-concrete-native-inputs/v1' and obj['template_only'] is False,'Complete actual-input document; no template becomes a packet')
    r.need(set(obj['program_files'])==r.PROGRAMS,'Reviewed four-file family')
    for name,spec in obj['program_files'].items():
        r.need(r.audit_path(spec)==r.D/name,'Exact reviewed program location');w.read_file(r.D/name,128*1024,spec)
    specs=obj['input_files'];r.need(isinstance(specs,list) and 1<=len(specs)<=256,'Bounded registry')
    for spec in specs:r.audit_path(spec)
    r.need(len({x['path'] for x in specs})==len(specs) and sum(x['bytes'] for x in specs)<=32*1024*1024,'Unique bounded registry')
    for spec in specs:w.read_file(r.audit_path(spec),8*1024*1024,spec,retain=False)
    w.limits_policy(obj['resources']);r.process_policy(obj['parent_policy']);p.stamp(obj['import_UTC'])
    r.need(set(obj['native_baseline'])==set(p.NATIVE) and obj['workspace_parent']==str(r.D/'workspaces'),'Exact baseline/private parent')
    body=w.canonical(obj);r.need(len(body)<=512*1024,'Packet cap');return body
def build_config(obj):
    r.need(set(obj)=={'schema','template_only','packet','adversary','commission'} and obj['schema']=='pr110-concrete-native-config/v1' and obj['template_only'] is False,'Exact non-template config')
    for role in ['packet','adversary','commission']:w.read_file(r.audit_path(obj[role]),512*1024 if role=='packet' else 128*1024,obj[role])
    return w.canonical(obj)
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--kind',choices=['packet','config'],required=True);a.add_argument('--draft',required=True);a.add_argument('--output',required=True);args=a.parse_args()
    destination=pathlib.Path(args.output);r.need(destination.parent.is_relative_to(r.D),'Construction output stays in dedicated new folder')
    draft=w.loads(w.read_file(pathlib.Path(args.draft),512*1024));body=build_packet(draft) if args.kind=='packet' else build_config(draft)
    w.atomic_write(destination.parent,destination.name,body,512*1024);print(w.canonical({'schema':'pr110-local-canonical-construction/v1','UTC':w.now(),
      'output':str(destination),'pin':w.pin(body),'construction_only':True,'service_authentication_provided':False,'execution_authorization_provided':False}).decode(),end='')
