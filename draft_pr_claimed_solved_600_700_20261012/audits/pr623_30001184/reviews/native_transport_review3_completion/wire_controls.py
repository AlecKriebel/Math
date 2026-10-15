"""Independent review3 server at HTTPSConnection boundary, no real network.

No adapter or kit HTTP/lifecycle/verifier method is replaced. Small private
TemporaryDirectory inputs and state are cleaned after each case.
"""
import argparse
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,struct,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import run_supplied as loaded

nt,kit=loaded.nt,loaded.nt.zenodo
HERE=Path(__file__).resolve().parent
PDF='gns_generation_counterexample.pdf'
ZIP='gns_verification.zip'
TOKEN='review3-offline-placeholder'
BASE='https://zenodo.org'
REC=BASE+'/api/records/23356540'
DRAFT=REC+'/draft'
FIXTURE=json.loads((loaded.SNAP/'native_shape.json').read_bytes())
PAYLOADS={f['name']:f['path'].read_bytes() for f in loaded.original.FILES}
EOCD=PAYLOADS[ZIP].rfind(b'PK\x05\x06')
OFFSET=struct.unpack_from('<I',PAYLOADS[ZIP],EOCD+16)[0]
if OFFSET!=218946 or PAYLOADS[ZIP][OFFSET:OFFSET+4]!=b'PK\x01\x02':raise RuntimeError('Independent EOCD mismatch')
GEOMETRY=subprocess.run(['pdfinfo','-f','1','-l','5','-box',str(nt.MANIFEST.parent/PDF)],capture_output=True,check=True).stdout.decode()
for page in range(1,6):
    if 'Page'+str(page) in GEOMETRY:raise RuntimeError('Unexpected pdfinfo output format')
    line=next(v for v in GEOMETRY.splitlines() if v.startswith('Page') and v.split()[1]==str(page) and 'size:' in v)
    if '612 x 792 pts' not in line:raise RuntimeError('Independent PDF dimension mismatch')
ANNOTATIONS={PDF:{'width':612,'height':792},ZIP:{'zip_toc_position':OFFSET}}

def previews(name,draft):
    if name==ZIP:return {'container':(DRAFT if draft else REC)+'/files/'+name+'/container'}
    namespace='draft' if draft else 'record'
    root=BASE+'/api/iiif/'+namespace+':23356540'
    file=root+':'+name
    return {'iiif_canvas':root+'/canvas/'+name,'iiif_base':file,'iiif_info':file+'/info.json','iiif_api':file+'/full/full/0/default.png'}

class Reply:
    def __init__(self,status,body):self.status,self.body,self.pos=status,body,0
    def read(self,size=-1):
        end=len(self.body) if size<0 else min(len(self.body),self.pos+size)
        block=self.body[self.pos:end];self.pos=end;return block

class Remote:
    def __init__(self):
        self.states,self.bytes={},{}
        self.published=False;self.calls=[];self.sent=[]
        self.annotation_mode='exact';self.preview_mode=True
        self.change_item=None;self.change_record=None;self.change_collection=None
        self.loss=None;self.binary_mode='exact';self.pending_readable=False
        self.bad_ack=None;self.on_chunk=None
    def item(self,name,draft):
        done=self.states[name]=='completed'
        root=(DRAFT if draft else REC)+'/files/'+name
        r={'key':name,'status':self.states[name],'metadata':None,
           'links':{'self':root,'content':root+'/content'},
           'access':{'hidden':False},'storage_class':'L','transfer':{'type':'L'},
           'created':'2026-10-14T00:00:00Z','updated':'2026-10-14T00:00:00Z'}
        if draft:r['links']['commit']=root+'/commit'
        if self.preview_mode:r['links'].update(previews(name,draft))
        if done:
            content=self.bytes[name]
            r.update(size=len(content),checksum='md5:'+hashlib.md5(content).hexdigest(),
                     mimetype='application/pdf' if name==PDF else 'application/zip')
            if self.annotation_mode=='exact':r['metadata']=deepcopy(ANNOTATIONS[name])
            elif self.annotation_mode=='empty':r['metadata']={}
        if self.change_item:self.change_item(r,draft)
        return r
    def record(self,draft):
        r=deepcopy(FIXTURE)
        if not draft:
            r.update(is_draft=False,is_published=True,status='published')
            r['links'].update(self=REC,files=REC+'/files',self_html=BASE+'/records/23356540')
            r['pids']={'doi':{'identifier':'10.5281/zenodo.23356540','provider':'datacite','client':'datacite'},
                       'oai':{'identifier':'oai:zenodo.org:23356540','provider':'oai'}}
            r['access']['status']='open'
        r['files'].update(enabled=True,count=len(self.states),entries={n:self.item(n,draft) for n in self.states},
                          total_bytes=sum(len(self.bytes[n]) for n,s in self.states.items() if s=='completed'))
        if self.change_record:self.change_record(r)
        return r
    def collection(self,draft):
        r={'enabled':True,'entries':[self.item(n,draft) for n in self.states],
           'order':[],'default_preview':None,'links':{'self':(DRAFT if draft else REC)+'/files'}}
        if self.change_collection:self.change_collection(r,draft)
        return r
    def connect(self,host,timeout):
        if host!='zenodo.org':raise RuntimeError('Host escaped own endpoint')
        return Wire(self)
    def dispatch(self,method,path,headers,data):
        url=BASE+path;self.calls.append((method,url))
        if headers.get('Authorization')!='Bearer '+TOKEN:raise RuntimeError('Offline credential mismatch')
        if headers.get('User-Agent')!=kit.USER_AGENT:raise RuntimeError('Kit transport bypass')
        if self.loss==(method,url,'before'):
            self.loss=None;raise OSError('Review3 before-response interruption')
        if method=='GET':
            if url==DRAFT:
                if headers.get('Accept')!=nt.NATIVE_ACCEPT:raise RuntimeError('Native negotiation bypass')
                return Reply(404,b'{"message":"not found"}') if self.published else Reply(200,json.dumps(self.record(True)).encode())
            if url==REC:
                return Reply(200,json.dumps(self.record(False)).encode()) if self.published else Reply(404,b'{"message":"not found"}')
            if url in (DRAFT+'/files',REC+'/files'):return Reply(200,json.dumps(self.collection(url==DRAFT+'/files')).encode())
            if url.endswith('/content'):
                if headers.get('Accept')!='*/*':return Reply(406,b'wrong accept')
                name=path.split('/')[-2]
                if self.states[name]=='pending' and not self.pending_readable:return Reply(404,b'pending unreadable')
                b=self.bytes.get(name,b'')
                if self.binary_mode=='corrupt':b=bytes([b[0]^1])+b[1:]
                elif self.binary_mode=='short':b=b[:-1]
                elif self.binary_mode=='long':b=b+b'X'
                elif self.binary_mode=='406':return Reply(406,b'not acceptable')
                return Reply(200,b)
            raise RuntimeError('Inert/unknown route followed: '+path)
        name=None
        if method=='POST' and url==DRAFT+'/files':
            parsed=json.loads(data)
            if len(parsed)!=1 or set(parsed[0])!={'key'}:raise RuntimeError('Unexpected initialize body')
            name=parsed[0]['key']
            if name in self.states:raise RuntimeError('Repeated initialize')
            self.states[name]='pending';result=self.collection(True)
        elif method=='PUT' and url.endswith('/content'):
            name=path.split('/')[-2]
            if name in self.bytes or headers.get('Content-Type')!='application/octet-stream' or int(headers.get('Content-Length','-1'))!=len(data):raise RuntimeError('Repeated/invalid PUT')
            self.bytes[name]=data;self.sent.append({'name':name,'size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'md5':hashlib.md5(data).hexdigest()})
            result=self.item(name,True)
        elif method=='POST' and url.endswith('/commit'):
            name=path.split('/')[-2]
            if self.states[name]!='pending':raise RuntimeError('Repeated commit')
            self.states[name]='completed';result=self.item(name,True)
        elif method=='POST' and url==DRAFT+'/actions/publish':
            if self.published or self.states!={PDF:'completed',ZIP:'completed'}:raise RuntimeError('Repeated/invalid publish')
            self.published=True;result=self.record(False)
        else:raise RuntimeError('Unapproved mutating endpoint')
        if self.bad_ack:self.bad_ack(method,url,result)
        if self.loss==(method,url,'after'):
            self.loss=None;raise OSError('Review3 after-response interruption')
        return Reply(201,json.dumps(result).encode())

class Wire:
    def __init__(self,remote):self.remote,self.headers,self.blocks=remote,{},[]
    def putrequest(self,method,path):self.method,self.path=method,path
    def putheader(self,key,value):self.headers[key]=value
    def endheaders(self):pass
    def send(self,block):
        if type(block)is not bytes:raise RuntimeError('Not captured bytes')
        self.blocks.append(block)
        if self.remote.on_chunk:self.remote.on_chunk(self,len(self.blocks))
    def request(self,method,path,headers):self.method,self.path,self.headers=method,path,headers
    def getresponse(self):return self.remote.dispatch(self.method,self.path,self.headers,b''.join(self.blocks))
    def close(self):pass

COUNTS={'hostile_annotation_cases':0,'hostile_link_cases':0,'positive_representation_cases':0}
class Review3WireTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=HERE/'tmp');self.folder=Path(self.temp.name)
        self.sources=self.folder/'sources';self.sources.mkdir()
        (self.sources/'zenodo-deposit.json').write_bytes(loaded.original.CAPTURED.manifest.read_bytes())
        for name,b in PAYLOADS.items():(self.sources/name).write_bytes(b)
        self.captured=nt.capture_inputs(self.sources/'zenodo-deposit.json')
        self.remote=Remote();self.client=self.restart()
        self.patches=[patch.object(nt.http.client,'HTTPSConnection',side_effect=self.remote.connect),
                      patch.object(kit,'STATE_DIR',self.folder/'kit-state'),patch.object(kit,'CHUNK',733),
                      patch.object(kit,'doi_status',return_value={'status':'resolved','http_status':200,'resolved_url':BASE+'/records/23356540','url':'https://doi.org/10.5281/zenodo.23356540'})]
        for p in self.patches:p.start()
        self.place=kit.state_path(self.captured.manifest,'production')
        kit.save_state(self.place,{'id':23356540,'manifest':str(self.captured.manifest),'environment':'production'})
    def tearDown(self):
        for p in reversed(self.patches):p.stop()
        self.temp.cleanup()
    def restart(self):return nt.NativeOwnDraftClient(TOKEN,self.captured.metadata,self.captured.files,allow_writes=True,journal_path=self.folder/'native-journal.json')
    def run_kit(self,command,client=None):return nt.run_captured_kit(argparse.Namespace(command=command,sandbox=False,confirm_id=23356540,check_doi=True),self.captured,client or self.client)
    def writes(self):return [(m,u)for m,u in self.remote.calls if m!='GET']
    def stage(self):self.assertEqual(self.run_kit('stage')['state'],'ready_to_publish')
    def clean_routes(self):self.assertFalse(any('/iiif/'in u or u.endswith('/container')for _,u in self.remote.calls))
    def test_complete_deployed_lifecycle_and_genuine_unchanged_receipt(self):
        self.stage();self.assertEqual(len(self.writes()),6)
        for sent in self.remote.sent:
            self.assertEqual((sent['size'],sent['sha256']),nt.FILE_PINS[sent['name']]);self.assertEqual(sent['md5'],nt.FILE_MD5_PINS[sent['name']])
        receipt=self.run_kit('publish');self.assertTrue(receipt['receipt_saved']);self.assertEqual(receipt['metadata_normalizations'],[])
        self.assertEqual(receipt['doi'],'10.5281/zenodo.23356540');self.assertEqual(receipt['state'],'published')
        self.assertEqual(kit.read_json(self.place)['publication'],receipt)
        before=self.writes();self.run_kit('inspect',self.restart());self.run_kit('publish',self.restart());self.assertEqual(self.writes(),before);self.clean_routes()
    def test_asynchronous_absent_empty_exact_annotations_all_states(self):
        self.remote.annotation_mode='none';self.stage()
        for mode in ('none','empty','exact'):
            for show in (False,True):
                for published in (False,True):
                    with self.subTest(mode=mode,links=show,published=published):
                        self.remote.annotation_mode=mode;self.remote.preview_mode=show;self.remote.published=published
                        self.assertEqual(self.run_kit('inspect')['state'],'published' if published else 'ready_to_publish')
                        COUNTS['positive_representation_cases']+=1
        self.assertEqual(len(self.writes()),6);self.clean_routes()
    def test_lost_publication_full_annotations_readback_then_restart(self):
        self.stage();self.remote.loss=('POST',DRAFT+'/actions/publish','after')
        r=self.run_kit('publish');self.assertTrue(r['recovered_after_publish_error']);self.assertTrue(r['receipt_saved'])
        self.assertEqual(kit.read_json(self.place)['publication'],r)
        before=self.writes();self.run_kit('publish',self.restart());self.assertEqual(before,self.writes());self.assertEqual(len(before),7);self.clean_routes()
    def test_lost_publish_bad_final_annotation_withholds_receipt_until_exact_readonly_recovery(self):
        self.stage();self.remote.loss=('POST',DRAFT+'/actions/publish','after')
        self.remote.change_item=lambda item,draft:item['links'].update(iiif_info=BASE+'/api/iiif/record:23356541:'+PDF+'/info.json')if not draft and item['key']==PDF else None
        with self.assertRaises(kit.DepositError):self.run_kit('publish')
        self.assertTrue(self.remote.published);before=self.writes();self.assertEqual(len(before),7)
        self.assertNotIn('publication',kit.read_json(self.place))
        with self.assertRaises(kit.DepositError):self.run_kit('inspect',self.restart())
        self.assertEqual(before,self.writes())
        self.remote.change_item=None;r=self.run_kit('inspect',self.restart());self.assertTrue(r['receipt_saved'])
        self.assertEqual(kit.read_json(self.place)['publication'],r);self.assertEqual(before,self.writes());self.clean_routes()
    def test_lost_publish_before_action_no_duplicate_across_restarts(self):
        self.stage();self.remote.loss=('POST',DRAFT+'/actions/publish','before')
        with self.assertRaises(kit.DepositError):self.run_kit('publish')
        before=self.writes()
        for _ in range(2):
            with self.assertRaises(kit.DepositError):self.run_kit('publish',self.restart())
        self.assertEqual(before,self.writes());self.assertFalse(self.remote.published);self.assertNotIn('publication',kit.read_json(self.place))
    def test_receipt_storage_failure_then_read_only_recovery_with_annotations(self):
        self.stage()
        with patch.object(kit,'save_state',side_effect=OSError('Offline kit receipt storage failure')):r=self.run_kit('publish')
        self.assertTrue(self.remote.published);self.assertEqual(r['state'],'published');self.assertFalse(r['receipt_saved'])
        before=self.writes();r=self.run_kit('inspect',self.restart());self.assertTrue(r['receipt_saved'])
        self.assertEqual(kit.read_json(self.place)['publication'],r);self.assertEqual(before,self.writes());self.clean_routes()
    def test_bad_derived_types_values_unknown_fields_and_mimes(self):
        self.stage();before=self.writes()
        cases=[(PDF,v)for v in [False,[],{'width':612}, {'width':True,'height':792},{'width':612.0,'height':792},{'width':612,'height':'792'},
                              {'width':612,'height':793},{'width':0,'height':792},{'width':612,'height':792,'extra':None},{'zip_toc_position':OFFSET}]]
        cases +=[(ZIP,v)for v in [False,[],{'zip_toc_position':True},{'zip_toc_position':float(OFFSET)},{'zip_toc_position':str(OFFSET)},
                                 {'zip_toc_position':200806},{'zip_toc_position':-1},{'zip_toc_position':OFFSET,'extra':{}},{'width':612,'height':792}]]
        for name,metadata in cases:
            for published in (False,True):
                with self.subTest(name=name,metadata=metadata,published=published):
                    self.remote.published=published
                    self.remote.change_item=lambda item,draft,n=name,m=metadata:item.update(metadata=m)if item['key']==n else None
                    with self.assertRaises(kit.DepositError):self.run_kit('inspect'if published else'publish')
                    self.assertEqual(before,self.writes());COUNTS['hostile_annotation_cases']+=1
        for name in (PDF,ZIP):
            for wrong in ('text/plain',True,123,{},'application/zip'if name==PDF else'application/pdf'):
                self.remote.published=False
                self.remote.change_item=lambda item,draft,n=name,m=wrong:item.update(mimetype=m)if item['key']==n else None
                with self.assertRaises(kit.DepositError):self.run_kit('publish')
                self.assertEqual(before,self.writes());COUNTS['hostile_annotation_cases']+=1
    def test_every_scoped_link_wrong_host_id_name_state_parameters_and_group(self):
        self.stage();before=self.writes()
        for name in (PDF,ZIP):
            for published in (False,True):
                self.remote.published=published
                for key,url in previews(name,not published).items():
                    bads=[url.replace('zenodo.org','bad.example'),url.replace('zenodo.org','zenodo.org.evil'),url.replace('https:','http:'),
                          url.replace('23356540','23356541'),url.replace(name,'other.zip'),url+'?a=1',url+'#x',url+'?',url+'#',
                          url.replace('zenodo.org','u@zenodo.org'),url.replace('zenodo.org','zenodo.org:443'),url.replace('/api/','/api/../api/'),
                          url.replace('zenodo.org','ZENODO.ORG'),url+'/',None,123]
                    if name==PDF:bads.append(url.replace('draft:','record:')if not published else url.replace('record:','draft:'))
                    else:bads.append(url.replace('/draft/','/')if not published else url.replace('/files/','/draft/files/'))
                    for bad in bads:
                        with self.subTest(key=key,bad=bad,published=published):
                            self.remote.change_item=lambda item,draft,n=name,k=key,b=bad:item['links'].update({k:b})if item['key']==n else None
                            with self.assertRaises(kit.DepositError):self.run_kit('inspect'if published else'publish')
                            self.assertEqual(before,self.writes());COUNTS['hostile_link_cases']+=1
        changes=[lambda item,draft:item['links'].update(unknown=BASE+'/unknown'),
                 lambda item,draft:item['links'].pop('iiif_canvas')if item['key']==PDF else None,
                 lambda item,draft:item['links'].pop('iiif_info')if item['key']==PDF else None,
                 lambda item,draft:item['links'].pop('iiif_base')if item['key']==PDF else None,
                 lambda item,draft:item['links'].update(container=DRAFT+'/files/'+PDF+'/container')if item['key']==PDF else None,
                 lambda item,draft:item['links'].update(iiif_info=BASE+'/api/iiif/draft:23356540:'+ZIP+'/info.json')if item['key']==ZIP else None,
                 lambda item,draft:item['links'].pop('self'),lambda item,draft:item['links'].pop('content'),
                 lambda item,draft:item['links'].pop('commit')if draft else item['links'].update(commit=REC+'/files/'+item['key']+'/commit')]
        for change in changes:
            for published in (False,True):
                self.remote.published=published;self.remote.change_item=change
                with self.assertRaises(kit.DepositError):self.run_kit('inspect'if published else'publish')
                self.assertEqual(before,self.writes());COUNTS['hostile_link_cases']+=1
        self.clean_routes()
    def test_correct_annotations_preserve_md5_downloaded_sha_size_and_http(self):
        self.stage();before=self.writes()
        for mode in ('corrupt','short','long','406'):
            self.remote.binary_mode=mode
            with self.assertRaises(kit.DepositError):self.run_kit('publish')
            self.assertEqual(before,self.writes())
        self.remote.binary_mode='exact'
        self.remote.change_item=lambda item,draft:item.update(checksum='md5:'+'0'*32)if item['key']==ZIP else None
        with self.assertRaises(kit.DepositError):self.run_kit('publish')
        self.assertEqual(before,self.writes());self.assertFalse(self.remote.published)
    def test_mutated_private_paths_during_actual_kit_stream_preserve_snapshots(self):
        touched=set()
        def race(conn,count):
            if conn.method!='PUT':return
            name=conn.path.split('/')[-2]
            if count==1:
                (self.sources/name).write_bytes(b'wrong source bytes');(self.sources/'zenodo-deposit.json').write_bytes(b'{}');touched.add(name)
            else:
                with (self.sources/name).open('ab')as s:s.write(b'X')
        self.remote.on_chunk=race;self.stage();self.assertEqual(touched,{PDF,ZIP})
        for name,b in self.remote.bytes.items():self.assertEqual(b,PAYLOADS[name])
        self.assertEqual(self.run_kit('publish')['state'],'published');self.clean_routes()
    def test_bad_completed_ack_stops_before_publish_but_reconciles_exact_readback(self):
        def malformed(method,url,response):
            if url.endswith('/commit')and response['key']==PDF:response['metadata']['width']=False
        self.remote.bad_ack=malformed
        # A malformed acknowledgment is not trusted. Correct independent
        # readback can nevertheless reconcile that reversible commit.
        self.stage();self.assertFalse(self.remote.published);self.assertEqual(len(self.writes()),6)
        self.remote.bad_ack=None;self.assertEqual(self.run_kit('publish')['state'],'published')
    def test_persistent_bad_annotation_after_commit_fails_closed(self):
        self.remote.change_item=lambda item,draft:item.update(metadata={'width':False,'height':792})if item['key']==PDF and item['status']=='completed'else None
        with self.assertRaises(kit.DepositError):self.run_kit('stage')
        self.assertEqual(len(self.writes()),3);before=self.writes()
        with self.assertRaises(kit.DepositError):self.run_kit('stage',self.restart())
        self.assertEqual(before,self.writes());self.assertFalse(self.remote.published)
    def test_pending_preview_links_without_extracted_metadata_valid_but_premature_values_reject(self):
        self.remote.change_item=lambda item,draft:item.update(metadata=deepcopy(ANNOTATIONS[item['key']]))if item['status']=='pending'else None
        with self.assertRaises(kit.DepositError):self.run_kit('stage')
        self.assertEqual(len(self.writes()),1);self.assertFalse(self.remote.published)
    def test_lost_content_pending_exact_bytes_uses_no_second_put(self):
        self.remote.pending_readable=True;self.remote.loss=('PUT',DRAFT+'/files/'+PDF+'/content','after')
        self.stage();self.assertEqual(len(self.writes()),6);self.assertEqual(sum(m=='PUT'and PDF in u for m,u in self.writes()),1)
        self.assertEqual(self.run_kit('publish')['state'],'published')
    def test_preview_annotations_never_enable_a_request_route(self):
        for name in (PDF,ZIP):
            for draft in (False,True):
                for url in previews(name,draft).values():
                    with self.assertRaises(kit.DepositError):self.client.request('GET',url)
        self.assertEqual(self.remote.calls,[])
    def test_write_intents_are_synced_before_each_actual_kit_dispatch(self):
        syncs=[];real=nt.os.fsync
        def record(fd):syncs.append(fd);return real(fd)
        original_dispatch=self.remote.dispatch
        observed=[]
        def guarded(method,path,headers,data):
            if method!='GET':
                journal=kit.read_json(self.client.journal_path)
                key='publish'if path.endswith('/actions/publish')else ('initialize:'+json.loads(data)[0]['key']if path==DRAFT[len(BASE):]+'/files'else ('content:'if method=='PUT'else'commit:')+path.split('/')[-2])
                self.assertEqual(journal['operations'][key]['phase'],'attempted')
                self.assertGreaterEqual(len(syncs),3);observed.append(key);syncs.clear()
            return original_dispatch(method,path,headers,data)
        self.remote.dispatch=guarded
        with patch.object(nt.os,'fsync',side_effect=record):self.stage();self.run_kit('publish')
        self.assertEqual(len(observed),7);self.assertEqual(len(set(observed)),7)

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Review3WireTests))
    report={'checked_utc':datetime.now(timezone.utc).isoformat(),'optimization':sys.flags.optimize,'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'case_counts':COUNTS,'network_calls':0,'scope':'Actual captured adapter and unchanged kit, only stdlib HTTPSConnection replaced; DOI resolver result is modeled, not live-verified'}
    (HERE/('WIRE_OPTIMIZED.json'if sys.flags.optimize else'WIRE_NORMAL.json')).write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
