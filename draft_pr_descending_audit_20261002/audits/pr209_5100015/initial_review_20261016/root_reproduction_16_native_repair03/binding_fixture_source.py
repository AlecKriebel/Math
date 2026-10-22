"""Controlled exact-source repair probes. All external providers are in-memory stubs.
Synthetic clearances are confined to this owned folder and grant no real authority.
"""
from pathlib import Path
from datetime import datetime,timezone
import base64,builtins,copy,hashlib,json,sys,types,traceback

HERE=Path(__file__).resolve().parent
PUB=HERE.parent
NAMES=['append_verified_tracker.py','integrate_reviewed_pr.py','publish_preprint.py','release_binding.py','verify_and_merge.py','verify_published_readonly.py']
SOURCE={n:(PUB/n).read_bytes() for n in NAMES}
SNAP=HERE/'source_snapshot_01'
RUNS=HERE/'probe_runs_01'
RESULTS=[]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def pin(p,base):return dict(path=p.relative_to(base).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
def reject(fn):
    try:fn()
    except Exception as e:return {'type':type(e).__name__,'error':str(e)}
    raise AssertionError('Expected rejection was accepted')

class Fixture:
    def __init__(self,label,version='1.0',date='2026-10-16'):
        self.base=RUNS/label
        if self.base.exists():raise RuntimeError('Preserve earlier outputs; use a new run directory')
        self.c=self.base/'case';self.r=self.c/'preprint';self.pub=self.c/'publication'
        self.r.mkdir(parents=True);self.pub.mkdir(parents=True)
        for n,raw in SOURCE.items():(self.pub/n).write_bytes(raw)
        self.modules={};self.calls=[];self.appends=0;self.publishes=0;self.stages=0
        self.sheet=[['Original Problem','Solution Chat URL','DOI','Notes']]
        self.duplicate=False;self.lose_append=False;self.lose_publish=False;self.bad_public=False
        self.rb=self.module('release_binding.py')
        (self.r/'manuscript.pdf').write_bytes(b'%PDF synthetic exact-source probe\n')
        (self.r/'manuscript.tex').write_text('Synthetic fixture, no mathematical authority.\n')
        (self.r/'data.txt').write_text('Synthetic input.\n')
        (self.r/'k303b-source-verification.zip').write_bytes(b'Synthetic ZIP byte payload; no scientific claims.')
        self.metadata={'title':'The outer center-pedal area product in elliptic billiards','version':version,'publication_date':date}
        dump(self.r/'metadata.json',self.metadata)
        dump(self.r/'SOURCE_MANIFEST.json',{'files':[pin(self.r/n,self.r) for n in ['data.txt','manuscript.tex','manuscript.pdf','metadata.json']]})
        self.maps=self.rb.EXPECTED_DEPOSIT_FILES
        dump(self.r/'deposit.json',{'metadata':self.metadata,'files':self.maps})
        p={'submission_files':[pin(self.r/x['path'],self.r) for x in self.maps],
           'source_manifest':pin(self.r/'SOURCE_MANIFEST.json',self.r),
           'manuscript_source':pin(self.r/'manuscript.tex',self.r),'metadata':pin(self.r/'metadata.json',self.r)}
        dump(self.r/'PACKAGE_MANIFEST.json',p)
        self.helpers=[pin(self.pub/n,self.pub) for n in NAMES]
        self.core=self.rb.current_core(self.r)
        whole=self.reviews('whole',self.core)
        helper=self.reviews('helper',self.helpers)
        public=[pin(self.r/n,self.c) for n in self.rb.CORE]+[pin(self.pub/n,self.c) for n in NAMES]
        dump(self.pub/'PUBLIC_EXPORT_MANIFEST.json',{'schema':'pr209-public-export-manifest-v1','files':public})
        self.clear={'release_cleared':True,'fresh_manuscript_reviews':2,'final_frozen_clean_reviews':1,
            'unresolved_mandatory_findings':[],'unresolved_optional_findings':[],
            'original_native_head':self.rb.ORIGINAL_HEAD,'release_helpers':self.helpers,
            'submission_files':p['submission_files'],'source_manifest':p['source_manifest'],'manuscript_source':p['manuscript_source'],
            'publication_metadata':self.metadata,'publication_metadata_sha256':sha((self.r/'metadata.json').read_bytes()),
            'package_manifest_sha256':sha((self.r/'PACKAGE_MANIFEST.json').read_bytes()),
            'deposit_manifest_sha256':sha((self.r/'deposit.json').read_bytes()),
            'whole_package_reviews':whole,'release_helper_reviews':helper,
            'public_export_manifest':pin(self.pub/'PUBLIC_EXPORT_MANIFEST.json',self.c)}
        self.save_clear()
        self.ctx=self.rb.context(self.r)
    def save_clear(self):dump(self.r/'FINAL_CLEARANCE.json',self.clear)
    def reviews(self,kind,expected):
        entries=[]
        for i in [1,2]:
            folder=self.c/(kind+str(i));folder.mkdir()
            freeze_time='2020-01-01T'+('00' if i==1 else '03')+':00:00+00:00'
            complete_time='2020-01-01T'+('01' if i==1 else '04')+':00:00+00:00'
            (folder/'REPORT.md').write_text('SYNTHETIC '+kind+' review '+str(i)+'; no real authority.\n')
            findings=[{'id':'M1','status':'open'}] if i==1 else []
            if kind=='whole':
                freeze={'frozen_utc':freeze_time,'core':[dict(path=n,**v) for n,v in expected.items()]}
                dump(folder/'FROZEN_BYTES.json',freeze)
                a={'schema':'pr209-whole-package-assessment-v1','review_id':kind+str(i),'review_completed':True,
                   'frozen_utc':freeze_time,'completed_utc':complete_time,'frozen_bindings':expected,
                   'evidence':{'report':pin(folder/'REPORT.md',folder),'freeze':pin(folder/'FROZEN_BYTES.json',folder)}}
            else:
                for n,raw in SOURCE.items():(folder/n).write_bytes(raw)
                dump(folder/'FROZEN_SOURCES.json',{'frozen_utc':freeze_time,'rows':expected})
                a={'schema':'pr209-release-helper-assessment-v1','reviewer':kind+str(i),'completed_utc':complete_time,'frozen_sources':expected}
            a.update(verdict='REPAIRS_REQUIRED' if i==1 else 'CLEAN',mandatory_findings=findings,optional_findings=[])
            dump(folder/'ASSESSMENT.json',a)
            dump(folder/'AUTHORED_MANIFEST.json',{'files':[pin(p,folder) for p in sorted(folder.iterdir()) if p.is_file()]})
            entry={'assessment':pin(folder/'ASSESSMENT.json',self.c),'authored_manifest':pin(folder/'AUTHORED_MANIFEST.json',self.c),'supplements':[]}
            if kind=='helper':entry['source_freeze']=pin(folder/'FROZEN_SOURCES.json',self.c)
            if i==1:
                r={'review_id':kind+str(i),'utc':'2020-01-01T02:00:00+00:00',
                   'review_assessment_sha256':entry['assessment']['sha256'],'review_manifest_sha256':entry['authored_manifest']['sha256'],
                   'resolved_findings':[{'id':'M1','status':'resolved'}],
                   'unresolved_mandatory_findings':[],'unresolved_optional_findings':[],
                   ('package_bindings' if kind=='whole' else 'source_bindings'):expected}
                dump(folder/'ROOT_RESOLUTION.json',r);entry['resolution']=pin(folder/'ROOT_RESOLUTION.json',self.c)
            entries.append(entry)
        return entries
    def imp(self,name,globals=None,locals=None,fromlist=(),level=0):
        if name=='release_binding':return self.rb
        if name=='subprocess':return types.SimpleNamespace(run=self.run)
        if name=='urllib.request':return types.SimpleNamespace(request=types.SimpleNamespace(Request=lambda *a,**k:a[0],urlopen=self.urlopen))
        if name=='verify_published_readonly':return self.module(name+'.py')
        return builtins.__import__(name,globals,locals,fromlist,level)
    def module(self,name):
        if name in self.modules:return self.modules[name]
        m=types.ModuleType(name[:-3]);m.__file__=str(self.pub/name)
        m.__dict__['__builtins__']={**vars(builtins),'__import__':self.imp}
        exec(compile(SOURCE[name],str(SNAP/name),'exec'),m.__dict__)
        self.modules[name]=m
        return m
    def v(self,state='published'):
        return {'environment':'production','title':self.metadata['title'],'files':self.ctx['expected_files'],
            'id':12345,'state':state,'doi':'10.5281/zenodo.12345','doi_url':'https://doi.org/10.5281/zenodo.12345',
            'record_url':'https://zenodo.org/records/12345','doi_resolution':{
                'status':'resolved','http_status':200,'url':'https://doi.org/10.5281/zenodo.12345',
                'resolved_url':'https://zenodo.org/records/12345'}}
    def run(self,args,**kw):
        self.calls.append({'args':args,'text':kw.get('text')})
        if args[0].endswith('/gws'):
            params=json.loads(args[args.index('--params')+1])
            if args[1:4]==['sheets','spreadsheets','get']:
                result={'spreadsheetId':self.rb.SHEET,'sheets':[{'properties':{'sheetId':self.rb.SHEET_ID,'title':'Math Puzzles'}}]}
            elif args[4]=='append':
                self.appends+=1;row=json.loads(args[args.index('--json')+1])['values'][0];self.sheet.append(row)
                if self.duplicate:self.sheet.append(row[:])
                result={'updates':{'updatedRows':1,'updatedCells':4,'updatedRange':"'Math Puzzles'!A2:D2",'updatedData':{'values':[row]}}}
                if self.lose_append:raise TimeoutError('Synthetic lost append outcome after one actual stub append')
            else:
                target=params['range']
                result={'range':target,'values':copy.deepcopy(self.sheet if target==self.rb.FULL_RANGE else [self.sheet[1]])}
        elif 'gh' in Path(args[0]).name:
            if args[2].endswith('pulls/209'):
                result={'number':209,'state':'open','draft':True,
                    'head':{'sha':self.rb.ORIGINAL_HEAD,'ref':'dot/math-5100015','repo':{'full_name':'AlecKriebel/Math'}},
                    'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}
            else:result={'content':base64.b64encode(b'| 222 | 5100015 / AMR-050-0015 | title | a | b | c | 2021 | claimed_solved | 1/5 |\n').decode()}
        else:
            op=args[3]
            if op=='check':result={k:v for k,v in self.v().items() if k in ['environment','title','files']}
            elif op=='stage':self.stages+=1;result=self.v('ready_to_publish')
            elif op=='publish':
                self.publishes+=1;result=self.v()
                if self.lose_publish:raise TimeoutError('Synthetic lost publish outcome after stub publication')
            elif op=='inspect':result=self.v('published' if (self.pub/'PUBLISH_ATTEMPT.json').exists() else 'ready_to_publish')
            else:raise RuntimeError('No unapproved provider operation '+repr(args))
        return types.SimpleNamespace(returncode=0,stdout=json.dumps(result),stderr='')
    def urlopen(self,url,**kw):
        self.calls.append({'public_url':url})
        name=url.split('/files/')[1].split('?')[0];mapping=next(m for m in self.maps if m['name']==name)
        raw=b'Corrupt public bytes' if self.bad_public else (self.r/mapping['path']).read_bytes()
        class Response:
            def __enter__(self):return self
            def __exit__(self,*args):return None
            def read(self):return raw
        return Response()
    def publish(self):return self.module('publish_preprint.py').publish_once(self.r,self.pub,self.base)
    def append(self):return self.module('append_verified_tracker.py').append_once(self.r,self.pub)
    def trace(self):dump(self.base/'PROVIDER_TRACE.json',{'calls':self.calls,'stages':self.stages,'publishes':self.publishes,'appends':self.appends,'sheet':self.sheet})

def test(label,fn):
    try:detail=fn();r={'label':label,'status':'PASS','detail':detail}
    except Exception as e:r={'label':label,'status':'FAIL','error':repr(e),'traceback':traceback.format_exc()}
    RESULTS.append(r);dump(HERE/'PROBE_RESULTS_01.json',RESULTS);print(json.dumps(r),flush=True)

def baseline():
    f=Fixture('baseline');z=f.publish();t=f.append()
    zhash=f.rb.digest(f.pub/'ZENODO_VERIFIED_PUBLICATION.json');thash=f.rb.digest(f.pub/'TRACKER_VERIFIED_APPEND.json')
    p=f.module('verify_published_readonly.py').verify_publication_live(f.r,f.pub,f.ctx)
    v=f.module('append_verified_tracker.py').verify_tracker_live(f.r,f.pub,f.ctx,z)
    assert zhash==f.rb.digest(f.pub/'ZENODO_VERIFIED_PUBLICATION.json') and thash==f.rb.digest(f.pub/'TRACKER_VERIFIED_APPEND.json')
    assert f.stages==f.publishes==f.appends==1 and t['append_count']==1 and v['values']==t['values']
    f.trace();return {'stages':1,'publishes':1,'appends':1,'immutable_receipts_unchanged_by_live_checks':True,'publication_ancestors':list(z['lineage'])}

def counter_only():
    f=Fixture('counter_only');f.clear.pop('whole_package_reviews');f.clear.pop('release_helper_reviews');f.save_clear()
    return reject(lambda:f.rb.context(f.r))

def finding_and_chronology():
    out={}
    for label,edit in [('unresolved_finding',lambda x:x['resolved_findings'][0].update(status='unresolved')),
                       ('late_resolution',lambda x:x.update(utc='2020-01-01T03:30:00+00:00'))]:
        f=Fixture(label);entry=f.clear['whole_package_reviews'][0];path=f.c/entry['resolution']['path'];r=json.loads(path.read_text());edit(r);dump(path,r);entry['resolution']=pin(path,f.c);f.save_clear()
        out[label]=reject(lambda:f.rb.context(f.r))
    return out

def stale_source():
    f=Fixture('stale_source');(f.r/'data.txt').write_text('Changed after review')
    return reject(lambda:f.rb.context(f.r))

def missing_lineage():
    f=Fixture('missing_lineage');f.publish();(f.pub/'STAGE_ATTEMPT.json').unlink()
    before=len(f.calls);a=reject(lambda:f.rb.publication(f.r,f.pub,f.ctx));b=reject(lambda:f.module('verify_published_readonly.py').verify_existing(f.r,f.pub,f.ctx))
    assert len(f.calls)==before;f.trace();return {'pure':a,'readonly':b,'provider_reads_after_missing_ancestry':0}

def tracker_corruption():
    out={}
    for label,field,value in [('append_count','append_count',9),('range','updated_range','Other sheet!Z999'),('notes','values',None),('reconcile','reconciled_existing_attempt',True)]:
        f=Fixture('tracker_'+label);f.publish();t=f.append()
        if field=='values':value=t['values'][:];value[3]='False theorem or stale metadata'
        t[field]=value;dump(f.pub/'TRACKER_VERIFIED_APPEND.json',t)
        out[label]=reject(lambda:f.rb.tracker(f.r,f.pub,f.ctx))
        f.trace()
    return out

def duplicate_race():
    f=Fixture('duplicate_race');f.publish();f.duplicate=True
    first=reject(f.append);second=reject(f.append)
    assert f.appends==1 and not (f.pub/'TRACKER_VERIFIED_APPEND.json').exists()
    assert list((f.pub/'private_transport/tracker_runs').rglob('PENDING.json'))
    f.trace();return {'first':first,'second':second,'actual_stub_appends':f.appends,'final_problem_rows':len(f.sheet)-1,'no_verified_receipt':True}

def unknown_append():
    f=Fixture('unknown_append');f.publish();f.lose_append=True;first=reject(f.append);f.lose_append=False;t=f.append()
    assert f.appends==1 and t['append_count']==0 and t['reconciled_existing_attempt']
    f.trace();return {'first':first,'actual_stub_appends':1,'recovered_invocation_append_count':0}

def unknown_publish():
    f=Fixture('unknown_publish');f.lose_publish=True;first=reject(f.publish);before=len(f.calls);second=reject(f.publish);assert len(f.calls)==before
    f.lose_publish=False;z=f.module('verify_published_readonly.py').verify_existing(f.r,f.pub,f.ctx)
    assert f.stages==f.publishes==1 and json.loads((f.pub/'ZENODO_TOOL_PUBLICATION_RECEIPT.json').read_text())['source']=='read-only-recovery'
    f.trace();return {'first':first,'blocked_retry':second,'actual_stub_stage':1,'actual_stub_publish':1,'read_only_recovery':z['submitted']}

def public_failure():
    f=Fixture('public_failure');f.bad_public=True;first=reject(f.publish)
    assert not (f.pub/'ZENODO_VERIFIED_PUBLICATION.json').exists() and (f.pub/'PUBLICATION_VERIFICATION_PENDING.json').exists()
    failed=list((f.pub/'private_transport/zenodo_verification').rglob('k303b-outer-center-pedal-areas.pdf'));assert failed and failed[0].read_bytes()==b'Corrupt public bytes'
    f.bad_public=False;z=f.module('verify_published_readonly.py').verify_existing(f.r,f.pub,f.ctx);f.trace()
    return {'first':first,'failed_public_payload_retained_losslessly':True,'recovery':z['submitted'],'publish_calls':f.publishes}

def version_date():
    f=Fixture('version_date','1.1','2026-10-17');f.publish();t=f.append()
    assert 'v1.1,2026-10-17' in t['values'][3] and 'v1.0,2026-10-16' not in t['values'][3]
    f.trace();return {'derived_version':'1.1','derived_date':'2026-10-17','exact_payload_validated':True}

def exports():
    out={}
    for label,path in [('unreviewed', 'preprint/UNREVIEWED.txt'),('env','publication/.env')]:
        f=Fixture('export_'+label);(f.c/path).write_text('Synthetic private/unreviewed marker')
        out[label]=reject(lambda:f.rb.public_exports(f.r,f.pub,f.ctx))
    f=Fixture('export_traversal');m=json.loads((f.pub/'PUBLIC_EXPORT_MANIFEST.json').read_text());m['files'][0]['path']='../elsewhere'
    dump(f.pub/'PUBLIC_EXPORT_MANIFEST.json',m);f.clear['public_export_manifest']=pin(f.pub/'PUBLIC_EXPORT_MANIFEST.json',f.c);f.save_clear()
    out['traversal']=reject(lambda:f.rb.context(f.r))
    return out

def optimized():
    out={}
    for name in NAMES:
        try:exec(compile(SOURCE[name],str(SNAP/name),'exec',optimize=2),{'__name__':'synthetic_optimized','__file__':str(SNAP/name)})
        except RuntimeError as e:out[name]=str(e)
        else:raise AssertionError('Optimized source accepted '+name)
    return out

if __name__=='__main__':
    SNAP.mkdir(exist_ok=False)
    for n,raw in SOURCE.items():(SNAP/n).write_bytes(raw)
    dump(HERE/'EXACT_SOURCE_INPUTS_01.json',{'utc':datetime.now(timezone.utc).isoformat(),'case_completion_percent':55,'files':[pin(SNAP/n,HERE) for n in NAMES]})
    for label,fn in [('baseline',baseline),('counter_only',counter_only),('finding_and_chronology',finding_and_chronology),
                     ('stale_source',stale_source),('missing_lineage',missing_lineage),('tracker_corruption',tracker_corruption),
                     ('duplicate_race',duplicate_race),('unknown_append',unknown_append),('unknown_publish',unknown_publish),
                     ('public_failure',public_failure),('version_date',version_date),('exports',exports),('optimized',optimized)]:
        test(label,fn)
    raise SystemExit(0 if all(r['status']=='PASS' for r in RESULTS) else 1)
