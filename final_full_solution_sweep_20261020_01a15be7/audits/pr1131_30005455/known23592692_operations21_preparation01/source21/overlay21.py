"""Explicit SOURCE21 known-ID recovery overlay; import performs no effects.

Frozen19/20 remain authenticated base code. This module is additional executed
policy, not covered by the old19 source identity or old20 entry approval.
"""
from pathlib import Path
import argparse,ast,copy,datetime,hashlib,json,re,stat
P=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr1131_30005455')
ID=23592692
HOLD='CONSUMED_RESPONSE18_HOLD_ac0b45e76fc14c80b31553d32261db57.json'
FAILURE='RESUME_STAGE_FAILURE.json'
def need(v,m):
    if not v:raise RuntimeError('SOURCE21: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def strict(b):
    def unique(pairs):
        out={}
        for key,value in pairs:need(key not in out,'duplicate JSON key');out[key]=value
        return out
    return json.loads(b,object_pairs_hook=unique,parse_constant=lambda s:need(False,'nonfinite JSON'))
def plain(p):
    p=Path(p);need(p.is_absolute()and not any(q.is_symlink()for q in[p,*p.parents]),'absolute nonsymlink path');return p
def pinned(spec):
    p=plain(spec['path']);raw=p.read_bytes();need(type(spec['bytes'])is int and len(raw)==spec['bytes']and sha(raw)==spec['sha256'],'entire pinned buffer '+str(p));return raw
def sources(root,pin):
    root=plain(root);raw=(root/'SOURCE_MANIFEST21.json').read_bytes();need(sha(raw)==pin,'externally pinned overlay source manifest')
    manifest=strict(raw);need(set(q.name for q in root.iterdir())==set(manifest)|{'SOURCE_MANIFEST21.json'},'complete finite overlay source namespace')
    out={}
    for name,value in manifest.items():
        need(Path(name).name==name and name not in{'','.','..'},'source basename')
        path=plain(root/name);need(stat.S_ISREG(path.lstat().st_mode),'regular source');raw=path.read_bytes();need(value=={'bytes':len(raw),'sha256':sha(raw)},'complete overlay source drift');out[name]=raw
    return out
def utc(value):
    need(type(value)is str,'UTC time type');t=datetime.datetime.fromisoformat(value.replace('Z','+00:00'));need(t.tzinfo is not None and t.utcoffset()==datetime.timedelta(0),'aware UTC');return t
def callable_record21(fn):
    f=getattr(fn,'__func__',fn)
    return (f.__code__,canonical(f.__defaults__),canonical(f.__kwdefaults__),
            tuple(id(cell.cell_contents)for cell in(f.__closure__ or ())))
class KnownPolicy21:
    def __init__(self,m,source_root,source_pin,entry_path,entry_pin,authority_path,authority_pin,compat_path,compat_pin,ns20):
        self.m=m;self.source_root=Path(source_root);self.source_pin=source_pin;self.entry_path=Path(entry_path);self.entry_pin=entry_pin
        self.authority_path=Path(authority_path);self.authority_pin=authority_pin;self.compat_path=Path(compat_path);self.compat_pin=compat_pin
        self.ns20=ns20;self.guard=None;buffers=sources(self.source_root,self.source_pin);self.data=strict(buffers['DATA_CONTRACT21.json']);self.recipe=strict(buffers['SOURCE19_OVERLAY_REPLACEMENTS.json'])
        need(self.data['id']==ID and len(self.data['historical_runtime'])==6,'exact knownID and six historical runtime files')
        self.initial_legacy=m.CUSTODY.loads(pinned(self.data['first_response']))['response']
        need(self.initial_legacy['id']==ID and self.initial_legacy['submitted']is False and self.initial_legacy['files']==[],'first full returned empty known draft')
        self.bucket=self.initial_legacy['links']['bucket']
        self.required_ui_fields=frozenset(m.NATIVE_POLICY.UI_POLICY.FIELDS)
        self.runtime_names()
        self.metadata,self.uploads=m.c.zenodo.load_manifest(m.pl.MANIFEST)
        self.original_context=m.local_context;self.original_certify=m.certify;self.original_resume=m.resume_stage;self.original_verify_public=m.verify_public18
        self.ui=m.NATIVE_POLICY.UI_POLICY;self.original_ui=self.ui.validate
        self.sdk=m.c.zenodo.ZenodoClient;need(type(self.sdk)is type,'SDK class must remain a typed class')
        self.original_request=self.sdk.request;self.original_create=self.sdk.create
        self.guard_class=m.pl.GuardedClient;self.original_guard_create=self.guard_class.create;self.original_edge_create=m.EdgeDelegate.create
        self.initial_write_intents=frozenset(q.name for q in m.RUNTIME.glob('WRITE_*_INTENT.json'));self.used_write_intents=set();self.active_write=None
        check_function=type(self).check;integrity_function=type(self).verify_callable_integrity
        def dispatch21():
            if type(self).check is not check_function or type(self).verify_callable_integrity is not integrity_function:raise RuntimeError('SOURCE21 class checker detached')
            integrity_function(self)
            return check_function(self)
        self.dispatch_wrapper=dispatch21
        self.history_wrapper=lambda kind:(dispatch21(),self.history(kind))[1]
        m.__dict__['_SOURCE21_HISTORY_CHECK']=self.history_wrapper
        # Compile ONLY the exact already-returned, full authenticated buffers.
        # No check followed by a second unverified read of either function file.
        manifest_raw=(m.CONTEXT['source_root']/'SOURCE_MANIFEST.json').read_bytes();need(sha(manifest_raw)==self.data['source19_sha256'],'full externally pinned base19 source manifest')
        manifest=strict(manifest_raw);checked19=m.CONTEXT['check_sources']()
        for name in ['lifecycle19.py','ui19.py']:
            need(type(checked19)is dict and name in checked19 and type(checked19[name])is bytes and manifest[name]=={'bytes':len(checked19[name]),'sha256':sha(checked19[name])},'exact same authenticated base19 function buffer')
        text=checked19['lifecycle19.py'].decode('utf-8',errors='strict');tree=ast.parse(text)
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='local_context');context=ast.get_source_segment(text,node)
        for old,new in self.recipe['local_context']:
            need(context.count(old)==1,'exact authenticated19 context replacement');context=context.replace(old,new,1)
        exec(compile(context,str(self.source_root/'overlay21.py')+'::authenticated19_context','exec',dont_inherit=True,optimize=0),m.__dict__)
        self.context21=m.local_context
        ui_text=checked19['ui19.py'].decode('utf-8',errors='strict');ui_node=next(n for n in ast.parse(ui_text).body if isinstance(n,ast.FunctionDef)and n.name=='validate');ui_code=ast.get_source_segment(ui_text,ui_node)
        for old,new in self.recipe['ui_validate']:
            need(ui_code.count(old)==1,'exact authenticated19 UI replacement');ui_code=ui_code.replace(old,new,1)
        ui_globals=dict(self.ui.__dict__);ui_globals['_SOURCE21_FIELDS']=self.language_fields
        exec(compile(ui_code,str(self.source_root/'overlay21.py')+'::authenticated19_UI','exec',dont_inherit=True,optimize=0),ui_globals)
        self.ui_wrapper=ui_globals['validate'];self.ui.validate=self.ui_wrapper
        edge_class=next(n for n in tree.body if isinstance(n,ast.ClassDef)and n.name=='EdgeDelegate');edge_node=next(n for n in edge_class.body if isinstance(n,ast.FunctionDef)and n.name=='mutation');edge_code=ast.get_source_segment(text,edge_node)
        for old,new in self.recipe['edge_mutation']:
            need(edge_code.count(old)==1,'exact authenticated immediate delegate-site replacement');edge_code=edge_code.replace(old,new,1)
        self.delegate_write_wrapper=lambda edge,kind,args:(dispatch21(),self.delegate_write(edge,kind,args))[1]
        m.__dict__['_SOURCE21_DELEGATE_WRITE']=self.delegate_write_wrapper
        exec(compile(edge_code,str(self.source_root/'overlay21.py')+'::authenticated19_immediate_delegate','exec',dont_inherit=True,optimize=0),m.__dict__)
        self.edge_mutation21=m.__dict__['mutation'];m.EdgeDelegate.mutation=self.edge_mutation21
        def disabled_create(*a,**k):raise RuntimeError('SOURCE21: create permanently disabled; only known23592692 may be recovered')
        self.disabled_create=disabled_create
        self.sdk.create=self.guard_class.create=m.EdgeDelegate.create=disabled_create
        def request21(client,method,url,payload=None,file=None,accept='application/json'):
            dispatch21()
            need(type(method)is str and type(url)is str,'typed SDK HTTP edge')
            base='https://zenodo.org';dep=base+'/api/deposit/depositions/'+str(ID);rec=base+'/api/records/'+str(ID)
            if method=='GET':need(url in{dep,rec,rec+'/draft',rec+'/files',rec+'/draft/files'}and payload is None and file is None,'only known-record SDK GET routes')
            elif method=='PUT':
                self.authorize_wire(client,'stage',method,url,payload,file)
                if url==dep:need(file is None and type(payload)is dict and set(payload)=={'metadata'}and m.SHEET_POLICY.typed_equal(payload['metadata'],self.metadata),'exact known metadata PUT')
                else:
                    from urllib.parse import quote
                    entries={self.bucket.rstrip('/')+'/'+quote(e['name']):e for e in self.uploads}
                    need(url in entries and payload is None and file==entries[url]['path'],'exact known bucket/filename/source upload PUT')
            else:
                need(method=='POST'and url==dep+'/actions/publish'and payload is None and file is None,'POST create and every other mutation are permanently forbidden')
                self.authorize_wire(client,'publish',method,url,payload,file)
            return self.original_request(client,method,url,payload,file,accept)
        self.request_wrapper=request21;self.sdk.request=request21
        def certify21(args,action,name,value,facts):
            dispatch21();value={**value,'additional_source21_policy':self.provenance()};return self.original_certify(args,action,name,value,facts)
        self.certify_wrapper=certify21;m.certify=certify21
        def verify_public21(args):
            dispatch21();return {**self.original_verify_public(args),'additional_source21_policy':self.provenance()}
        self.verify_public_wrapper=verify_public21;m.verify_public18=verify_public21
        self.resume_wrapper=lambda args:(dispatch21(),self.resume_known_stage(args))[1];m.resume_stage=self.resume_wrapper
        self.language_helper=ui_globals['_SOURCE21_FIELDS']
        self.base_sources=m.CONTEXT['check_sources'];self.record_code=callable_record21.__code__
        # Seal the new policy's code/defaults/closures and fixed helper globals.
        selected=[self.dispatch_wrapper,self.context21,self.ui_wrapper,self.edge_mutation21,self.history_wrapper,self.delegate_write_wrapper,self.disabled_create,self.request_wrapper,self.certify_wrapper,self.verify_public_wrapper,self.resume_wrapper,self.language_helper,self.original_request]
        method_names=['__init__','check','history','language_fields','resume_known_stage','provenance','delegate_write','authorize_wire','runtime_names','verify_callable_integrity','attach_guard']
        self.class_method_seals=tuple((name,getattr(type(self),name))for name in method_names)
        selected += [fn for name,fn in self.class_method_seals]
        selected += [self.original_context,self.original_certify,self.original_resume,self.original_verify_public,self.base_sources]
        selected += [self.ui.expected,self.ui.date,self.ui.vocabulary,self.ui.need]
        selected += [need,sha,canonical,strict,plain,pinned,sources,utc,callable_record21]
        self.callable_seals=tuple((fn,callable_record21(fn))for fn in selected)
        self.ui_constants=(canonical(self.ui.LABELS),self.ui.MONTHS,self.ui.LICENSE_DESCRIPTION)
        # Only immutable helpers/selectors are sealed here. Base19 mutable action,
        # state and runtime globals retain their existing dedicated exact guards.
        self.global_seals=[]
        for fn in selected:
            f=getattr(fn,'__func__',fn);names=set(f.__code__.co_names)
            if f.__globals__ is m.__dict__:names &= {'_SOURCE21_HISTORY_CHECK','_SOURCE21_DELEGATE_WRITE'}
            for name in names:
                if name in f.__globals__:self.global_seals.append((f.__globals__,name,f.__globals__[name]))
        self.global_seals=tuple(self.global_seals)
        integrity_code=type(self).verify_callable_integrity.__code__
        def checked_sources21():
            if type(self).verify_callable_integrity.__code__ is not integrity_code:raise RuntimeError('SOURCE21 integrity checker code changed')
            integrity_function(self);return self.base_sources()
        self.sources_wrapper=checked_sources21;m.CONTEXT['check_sources']=checked_sources21
        self.callable_seals+=((checked_sources21,callable_record21(checked_sources21)),)
        callback_names=['dispatch_wrapper','original_request','original_context','original_certify','original_resume','original_verify_public','base_sources','context21','ui_wrapper','history_wrapper','delegate_write_wrapper','disabled_create','request_wrapper','certify_wrapper','verify_public_wrapper','resume_wrapper','language_helper','sources_wrapper']
        self.callback_attribute_seals=tuple((name,getattr(self,name))for name in callback_names)
    def runtime_names(self):
        names={q.name for q in self.m.RUNTIME.iterdir()};initial=set(self.data['historical_runtime'])
        if 'RESUME_KNOWN_STAGE21_INTENT.json'not in names:
            need(names==initial,'exact original six-file namespace required before first new21 intention')
            return
        fixed={'RESUME_KNOWN_STAGE21_INTENT.json','CANONICAL_STATE_INSTALLED.json','STAGE_SERVICE_OUTCOME.json','RESUME_STAGE_VERIFIED.json','ZENODO_STAGE_VERIFIED.json','ZENODO_PUBLISH_INTENT.json','PUBLISH_RETURNED_SERVICE_FACT.json','PUBLISH_SERVICE_OUTCOME.json','ZENODO_PUBLISH_VERIFIED.json','LEDGER_APPEND_INTENT.json','LEDGER_APPEND_RESPONSE.json','LEDGER_APPEND_ACKNOWLEDGED.json','LEDGER_VERIFIED.json'}
        pattern=r'(?:RESPONSE_CHECK_[a-f0-9]{32}|PRIVATE_PUBLICATION_STATE_[0-9]{2}|WRITE_stage_upload_[a-f0-9]{64}_INTENT|WRITE_stage_update_INTENT|WRITE_publish_publish_INTENT)\.json'
        need(all(n in initial or n in fixed or re.fullmatch(pattern,n)is not None for n in names),'unknown/orphan runtime filename is not an adopted21 action artifact')
    def verify_callable_integrity(self):
        forbidden={'check','history','language_fields','resume_known_stage','provenance','delegate_write','authorize_wire','runtime_names','verify_callable_integrity','attach_guard'}
        if forbidden.intersection(self.__dict__):raise RuntimeError('SOURCE21 per-instance policy-method shadow')
        for name,fn in self.class_method_seals:
            if type(self).__dict__.get(name)is not fn:raise RuntimeError('SOURCE21 class method binding changed: '+name)
        for name,fn in self.callback_attribute_seals:
            if self.__dict__.get(name)is not fn:raise RuntimeError('SOURCE21 callback attribute binding changed: '+name)
        if callable_record21.__code__ is not self.record_code:raise RuntimeError('SOURCE21 callable-record checker changed')
        for fn,expected in self.callable_seals:
            current=callable_record21(fn)
            if current[0] is not expected[0] or current[1:]!=expected[1:]:raise RuntimeError('SOURCE21 callable code/defaults/closure changed')
        for namespace,name,value in self.global_seals:
            if namespace.get(name)is not value:raise RuntimeError('SOURCE21 fixed helper/global binding changed: '+name)
        if (type(self.ui.FIELDS)is not set or frozenset(self.ui.FIELDS)!=self.required_ui_fields
                or canonical(self.ui.LABELS)!=self.ui_constants[0]or self.ui.MONTHS!=self.ui_constants[1]
                or self.ui.LICENSE_DESCRIPTION!=self.ui_constants[2]
                or self.ui_wrapper.__globals__.get('_SOURCE21_FIELDS')is not self.language_helper
                or self.ui_wrapper.__globals__.get('FIELDS')is not self.ui.FIELDS):
            raise RuntimeError('SOURCE21 UI required constants/helper changed')
        if self.m.CONTEXT.get('check_sources')is not self.sources_wrapper:raise RuntimeError('SOURCE21 source/integrity wrapper detached')
    def provenance(self):
        return {'source21_sha256':self.source_pin,'entry21_sha256':self.entry_pin,'ROOT21_sha256':self.authority_pin,'compatibility20_authority_sha256':self.compat_pin,'base_source19_sha256':self.data['source19_sha256'],'base_source20_sha256':self.data['source20_sha256'],'known_id':ID,'first_return_sha256':self.data['first_response']['sha256'],'execution_policy_modified_from19':True}
    def check(self):
        type(self).verify_callable_integrity(self);m=self.m;buffers=sources(self.source_root,self.source_pin);need(canonical(strict(buffers['DATA_CONTRACT21.json']))==canonical(self.data),'in-memory fixed contract drift')
        need(sha(plain(self.entry_path).read_bytes())==self.entry_pin,'sole entry21 drift')
        pinned(self.data['ROOT_preparation_input_adoption'])
        need(m.__dict__.get('_SOURCE21_HISTORY_CHECK')is self.history_wrapper and m.__dict__.get('_SOURCE21_DELEGATE_WRITE')is self.delegate_write_wrapper and m.EdgeDelegate.mutation is self.edge_mutation21 and m.resume_stage is self.resume_wrapper and m.certify is self.certify_wrapper and m.verify_public18 is self.verify_public_wrapper,'new21 lifecycle aliases detached')
        need(self.ui.validate is self.ui_wrapper and m.NATIVE_POLICY.UI_POLICY is self.ui,'new21 UI alias detached')
        need(m.pl.GuardedClient is self.guard_class and self.guard_class.create is self.disabled_create and m.EdgeDelegate.create is self.disabled_create,'GuardedClient/edge create blocker detached')
        need(m.c.zenodo.ZenodoClient is self.sdk and self.sdk.create is self.disabled_create and self.sdk.request is self.request_wrapper,'SDK create/HTTP blockers detached')
        if self.guard is not None:
            self.guard.aliases();need(self.guard.context_original is self.context21,'actual20 guard must wrap reviewed21 context')
        raw=plain(self.authority_path).read_bytes();need(sha(raw)==self.authority_pin,'ROOT21 authority changed/revoked');ad=strict(raw)
        exact={'schema':'ROOT-known23592692-source21-authority-1','id':ID,'concept':self.data['concept'],'owner':self.data['owner'],'source21_sha256':self.source_pin,'entry21_sha256':self.entry_pin,'base_source19_sha256':self.data['source19_sha256'],'base_source20_sha256':self.data['source20_sha256'],'ROOT19_sha256':self.data['ROOT19_sha256'],'compatibility20_authority_sha256':self.compat_pin,'first_return_sha256':self.data['first_response']['sha256'],'known_create_only':True,'create_permanently_forbidden':True,'whole21_review_adopted':True,'publication_ready':True,'unresolved_findings':[]}
        need(all(k in ad and canonical(ad[k])==canonical(v)for k,v in exact.items()),'ROOT21 exact source/known recovery authority')
        need(type(ad.get('whole21_review_sha256'))is str and re.fullmatch('[a-f0-9]{64}',ad['whole21_review_sha256'])and ad['whole21_review_sha256']!='0'*64,'new independent whole21 review pin')
        need(type(ad.get('allowed_actions'))is list and len(ad['allowed_actions'])==len(set(ad['allowed_actions']))and set(ad['allowed_actions'])<={'stage-known','publish','verify-public','ledger'},'ROOT21 exact action roles')
        now=datetime.datetime.now(datetime.timezone.utc);start=utc(ad['not_before']);end=utc(ad['expires_at']);need(start<=now<end and end-start<=datetime.timedelta(hours=2),'new short ROOT21 validity')
        compat_raw=plain(self.compat_path).read_bytes();need(sha(compat_raw)==self.compat_pin,'new compatibility20 authority changed/revoked');compat=strict(compat_raw)
        need(compat.get('whole20_review_sha256')==ad['whole21_review_sha256']and compat.get('entry20_sha256')==self.entry_pin,'legacy compatibility20 field names must bind actual21 entry and SAME new whole21 review')
        need(sha((m.RUNTIME/'ROOT_OPERATIONAL_CLEARANCE19.json').read_bytes())==self.data['ROOT19_sha256'],'original ROOT19 authority preserved')
        if m.ACTION_ARGS is not None:
            action='stage-known'if m.ACTION_ARGS.action=='resume-stage'else m.ACTION_ARGS.action
            need(action in ad['allowed_actions']and m.ACTION_ARGS.deposit_id==ID and type(m.ACTION_ARGS.deposit_id)is int,'ROOT21 action/known target not permitted')
        return ad
    def delegate_write(self,edge,kind,args):
        """Grant exactly one matching SDK request at the original immediate site."""
        m=self.m;self.check();need(self.active_write is None,'no nested delegated mutation capability')
        need(type(edge)is m.EdgeDelegate and edge.args is m.ACTION_ARGS and edge.action==m.ACTION and edge.guard.delegate is edge and edge.guard.identifier==ID and edge.known_id==ID,'actual bound known EdgeDelegate/GuardedClient')
        need(kind in{'upload','update'}and m.ACTION=='stage'and m.ACTION_ARGS.action=='resume-stage' or kind=='publish'and m.ACTION=='publish'and m.ACTION_ARGS.action=='publish','mutation kind must match current parsed phase')
        need(edge.guard.pending_transition==kind and edge.guard.edge_used is True and edge.guard.edge_gate is not None and edge.guard.snapshot is not None,'original fresh per-write guard state')
        key=kind+('_'+sha(args[1]['name'].encode())if kind=='upload'else'');intent='WRITE_'+m.ACTION+'_'+key+'_INTENT.json'
        need(intent not in self.initial_write_intents and intent not in self.used_write_intents and intent in m.OWN_RUNTIME,'only this newly consumed per-write intention may grant capability')
        m.runtime_exact();value=m.c.strict_json(m.pinned(m.RUNTIME/intent,m.OWN_RUNTIME[intent]))
        need(value['action']==m.ACTION and value['kind']==kind and value['known_id']==ID and value['clearance_sha256']==m.ACTION_ARGS.clearance_sha256,'exact newly bound per-write intention')
        m.state_exact(ID);m.c.fresh(edge.guard.edge_gate['at_start']);m.c.fresh(edge.guard.snapshot['observed_at'],seconds=30)
        self.used_write_intents.add(intent);cap={'client':edge.delegate,'edge':edge,'kind':kind,'args':args,'intent':intent,'unused':True};self.active_write=cap
        try:
            result=getattr(edge.delegate,kind)(*args);need(cap['unused']is False,'delegate returned without the one reviewed SDK request');return result
        finally:self.active_write=None
    def authorize_wire(self,client,action,method,url,payload,file):
        m=self.m;cap=self.active_write;need(cap is not None and cap['unused']is True and cap['client']is client and m.ACTION==action,'SDK mutation lacks current one-use phase capability')
        kind=cap['kind'];args=cap['args'];dep='https://zenodo.org/api/deposit/depositions/'+str(ID)
        if kind=='upload':
            from urllib.parse import quote
            need(action=='stage'and method=='PUT'and url==args[0].rstrip('/')+'/'+quote(args[1]['name'])and payload is None and file==args[1]['path'],'upload wire must match exact fresh grant')
        elif kind=='update':need(action=='stage'and method=='PUT'and url==dep and args[0]==ID and type(payload)is dict and set(payload)=={'metadata'}and m.SHEET_POLICY.typed_equal(payload['metadata'],args[1])and file is None,'metadata wire must match exact fresh grant')
        else:need(kind=='publish'and action=='publish'and method=='POST'and url==dep+'/actions/publish'and args==(ID,)and payload is None and file is None,'publish wire must match exact fresh grant')
        m.local_context(m.ACTION_ARGS,m.ACTION);m.runtime_exact();m.state_exact(ID)
        edge=cap['edge'];need(edge.guard.pending_transition==kind,'active transition changed at HTTP edge');m.c.fresh(edge.guard.edge_gate['at_start']);m.c.fresh(edge.guard.snapshot['observed_at'],seconds=30)
        cap['unused']=False  # Consumed BEFORE entering original transport, even on loss.
    def history(self,kind):
        self.check();m=self.m;self.runtime_names()
        for name,pin in self.data['historical_runtime'].items():
            need((m.RUNTIME/name).read_bytes()==pinned(pin),'one of six exact historical runtime files changed')
        pinned(self.data['first_response'])
        holds={name for name in m.OWN_RUNTIME if 'HOLD' in name}
        failures={name for name in m.OWN_RUNTIME if 'FAILURE' in name}
        need(holds=={HOLD}and failures=={FAILURE},'any future/additional HOLD or failure blocks this actor')
        if self.guard is not None:need(self.guard.known(ID)==ID,'full tagged original known-create proof')
        need(kind in{'hold','failure'},'exact historical predicate role')
    def language_fields(self,native):
        ui=native.get('ui');need(type(ui)is dict,'native UI object')
        if 'languages'in ui:return self.ui.FIELDS
        md=native.get('metadata');need(type(md)is dict,'native metadata object')
        need(type(native.get('id'))in{str,int}and str(native['id'])==str(ID),'missing-language policy restricted to exact known record')
        need('languages'not in md,'missing UI language requires canonical languages ABSENT, including no empty-list extension')
        return self.ui.FIELDS-{'languages'}
    def resume_known_stage(self,args):
        m=self.m;self.check();need(type(args.deposit_id)is int and args.deposit_id==ID,'only exact known draft recovery')
        need(not any((m.RUNTIME/n).exists()for n in['RESUME_KNOWN_STAGE21_INTENT.json','ZENODO_STAGE_VERIFIED.json','RESUME_STAGE_VERIFIED.json']),'known stage already consumed; no retry')
        m.require_action(args,'stage');m.verify_merged_payload();m.local_context(args,'stage');need(self.guard.known(ID)==ID,'full known first receipt required')
        m.state_exact(ID,absent=True)
        m.record(m.RUNTIME/'RESUME_KNOWN_STAGE21_INTENT.json',{'at':m.c.stamp(),'id':ID,'canonical_manifest':str(m.pl.MANIFEST.resolve()),'additional_source21_policy':self.provenance(),'rule':'Known already-created empty draft only; no create; any failure consumes this stage-known attempt.'})
        client=m.pl.GuardedClient(args,'stage',ID)
        try:
            ad=m.require_action(args,'stage');gate,_,_=m.pl.collect('before_stage',args.expected_pr_head,ID,cleared=ad)
            _,snapshot=client.observation(False,set());m.local_context(args,'stage');m.family(gate,snapshot)
            need(snapshot['record']==ID and snapshot['concept']==self.data['concept']and snapshot['owner']==self.data['owner']and snapshot['files']=={}and snapshot['bucket']==self.bucket,'fresh full exact known draft identity/owner/concept/empty files/bucket')
            m.c.fresh(gate['at_start']);m.c.fresh(snapshot['observed_at'],seconds=30)
            identity={'manifest':str(m.pl.MANIFEST.resolve()),'environment':'production','id':ID}
            m.guarded_save_state(m.state_place(),identity);m.state_exact(ID)
            result=m.c.zenodo.run(argparse.Namespace(command='stage',manifest=m.pl.MANIFEST,sandbox=False,confirm_id=ID,check_doi=True),client=client)
            need(result.get('state')=='ready_to_publish'and type(result.get('id'))is int and result['id']==ID,'known stage uploads/metadata outcome unconfirmed')
            m.state_exact(ID);m.record(m.RUNTIME/'STAGE_SERVICE_OUTCOME.json',result)
            facts=m.final_facts(args,'stage',ID,False)
            m.certify(args,'stage','RESUME_STAGE_VERIFIED.json',{'at':m.c.stamp(),'id':ID,'known_recovery21':True},facts)
            m.certify(args,'stage','ZENODO_STAGE_VERIFIED.json',result,facts)
        except BaseException as exc:
            m.record(m.RUNTIME/'RESUME_KNOWN_STAGE21_FAILURE.json',{'at':m.c.stamp(),'id':ID,'exception_type':type(exc).__name__,'additional_source21_policy':self.provenance(),'no_retry_or_new_create':True,'GET_only_reconciliation_required':True});raise
        return {k:result.get(k)for k in['id','state','doi','doi_url','record_url']}
    def attach_guard(self,guard):
        need(self.guard is None,'one unchanged20 guard only');self.guard=guard;need(guard.context_original is self.context21,'guard must bind21 context, not old19');return self
