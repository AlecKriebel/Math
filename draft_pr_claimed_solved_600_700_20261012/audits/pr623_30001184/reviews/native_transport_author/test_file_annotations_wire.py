"""F5 controls at the actual unchanged-kit HTTPSConnection wire boundary.

No native-client/kit method is replaced. Only the external connection is fake.
Every journal/state/source-copy write stays in the author's ignored tmp folder.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

import test_native_transport as baseline

nt, kit = baseline.nt, baseline.zenodo
TOKEN = 'offline-annotation-wire-token'
PDF, ZIP = 'gns_generation_counterexample.pdf', 'gns_verification.zip'


def expected_metadata(name):
    # Independent value controls: parent PDF geometry calibration and the ZIP's
    # raw EOCD central-directory offset field, not the adapter derivation method.
    if name == PDF:
        return {'width':612,'height':792}
    data = next(f['path'].read_bytes() for f in baseline.FILES if f['name']==ZIP)
    position = data.rfind(b'PK\x05\x06')
    offset = struct.unpack_from('<I',data,position+16)[0]
    if offset != 218946: raise RuntimeError('Independent ZIP EOCD mismatch')
    return {'zip_toc_position':offset}


def derived_links(name,draft):
    # Independent explicit templates from primary service config and deployed
    # published calibration. The draft namespace follows primary helpers.
    if name == PDF:
        namespace = 'draft' if draft else 'record'
        root = 'https://zenodo.org/api/iiif/'+namespace+':23356540'
        return {'iiif_canvas':root+'/canvas/'+name,'iiif_base':root+':'+name,
                'iiif_info':root+':'+name+'/info.json',
                'iiif_api':root+':'+name+'/full/full/0/default.png'}
    root = nt.DRAFT if draft else nt.REC
    return {'container':root+'/files/'+name+'/container'}


class Response:
    def __init__(self,status,data):
        self.status,self.data,self.position=status,data,0
    def read(self,size=-1):
        end=len(self.data) if size<0 else min(len(self.data),self.position+size)
        chunk=self.data[self.position:end];self.position=end
        return chunk


class AnnotationServer:
    def __init__(self):
        self.status,self.content={},{}
        self.published=False
        self.calls,self.uploads=[],[]
        self.loss=None
        self.list_mutator=None
        self.entry_mutator=None
        self.download_corrupt=False
        self.annotate=True
    def entry(self,name,draft=True):
        completed=self.status[name]=='completed'
        root=(nt.DRAFT if draft else nt.REC)+'/files/'+name
        entry={'key':name,'status':self.status[name],'metadata':None,
               'links':{'self':root,'content':root+'/content'}}
        if draft:entry['links']['commit']=root+'/commit'
        if self.annotate:entry['links'].update(derived_links(name,draft))
        if completed:
            data=self.content[name]
            entry.update(size=len(data),checksum='md5:'+hashlib.md5(data).hexdigest(),
                         mimetype='application/pdf' if name==PDF else 'application/zip',storage_class='L')
            if self.annotate:entry['metadata']=expected_metadata(name)
        if self.entry_mutator:self.entry_mutator(entry,draft)
        return entry
    def record(self,draft):
        result=deepcopy(baseline.FIXTURE)
        if not draft:
            result.update(is_draft=False,is_published=True,status='published')
            result['links'].update(self=nt.REC,files=nt.REC+'/files',self_html=nt.BASE+'/records/23356540')
            result['pids']={'doi':{'identifier':nt.DOI,'provider':'datacite','client':'datacite'},
                            'oai':{'identifier':nt.OAI,'provider':'oai'}}
        result['files'].update(count=len(self.status),entries={name:self.entry(name,draft) for name in self.status},
                              total_bytes=sum(len(self.content[name]) for name,state in self.status.items() if state=='completed'))
        return result
    def collection(self,draft):
        result={'enabled':True,'entries':[self.entry(name,draft) for name in self.status],
                'default_preview':None,'order':[],'links':{'self':(nt.DRAFT if draft else nt.REC)+'/files'}}
        if self.list_mutator:self.list_mutator(result,draft)
        return result
    def connection(self,host,timeout):
        if host!='zenodo.org':raise RuntimeError('Unexpected wire host')
        return Connection(self)
    def dispatch(self,method,target,headers,data):
        url=nt.BASE+target;self.calls.append((method,url))
        if headers.get('Authorization')!='Bearer '+TOKEN or headers.get('User-Agent')!=kit.USER_AGENT:
            raise RuntimeError('Incorrect offline authenticated identity')
        if method=='GET':
            if url==nt.DRAFT:
                return Response(404,b'{"message":"draft absent"}') if self.published else Response(200,json.dumps(self.record(True)).encode())
            if url==nt.REC:
                return Response(200,json.dumps(self.record(False)).encode()) if self.published else Response(404,b'{"message":"not published"}')
            if url in (nt.DRAFT+'/files',nt.REC+'/files'):
                return Response(200,json.dumps(self.collection(url==nt.DRAFT+'/files')).encode())
            if url.endswith('/content'):
                name=target.split('/')[-2]
                if headers['Accept']!='*/*':return Response(406,b'{"message":"not acceptable"}')
                if self.status.get(name)!='completed':return Response(404,b'pending unavailable')
                body=self.content[name]
                if self.download_corrupt:body=bytes([body[0]^1])+body[1:]
                return Response(200,body)
            raise RuntimeError('A preview/container/unexpected URL was requested')
        if method=='POST' and url==nt.DRAFT+'/files':
            payload=json.loads(data);name=payload[0]['key']
            if type(payload) is not list or len(payload)!=1 or name in self.status:raise RuntimeError('Repeated/invalid initialize')
            self.status[name]='pending';result=self.collection(True)
        elif method=='PUT' and url.endswith('/content'):
            name=target.split('/')[-2]
            if name in self.content or headers['Content-Type']!='application/octet-stream' or int(headers['Content-Length'])!=len(data):
                raise RuntimeError('Repeated/invalid payload transmission')
            self.content[name]=data
            self.uploads.append({'name':name,'size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'md5':hashlib.md5(data).hexdigest()})
            result=self.entry(name,True)
        elif method=='POST' and url.endswith('/commit'):
            name=target.split('/')[-2]
            if self.status[name]!='pending':raise RuntimeError('Repeated/invalid commit')
            self.status[name]='completed';result=self.entry(name,True)
        elif method=='POST' and url==nt.DRAFT+'/actions/publish':
            if self.published or set(self.status)!={PDF,ZIP} or any(value!='completed' for value in self.status.values()):
                raise RuntimeError('Repeated/incomplete publication')
            self.published=True;result=self.record(False)
        else:raise RuntimeError('Unexpected mutating route')
        if self.loss==(method,url):
            self.loss=None;raise OSError('Offline lost action response')
        return Response(200,json.dumps(result).encode())


class Connection:
    def __init__(self,server):self.server,self.headers,self.blocks=server,{},[]
    def putrequest(self,method,target):self.method,self.target=method,target
    def putheader(self,key,value):self.headers[key]=value
    def endheaders(self):pass
    def send(self,data):
        if type(data) is not bytes:raise RuntimeError('Non-byte kit transmission')
        self.blocks.append(data)
    def request(self,method,target,headers):self.method,self.target,self.headers=method,target,headers
    def getresponse(self):return self.server.dispatch(self.method,self.target,self.headers,b''.join(self.blocks))
    def close(self):pass


class AnnotationWireTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=nt.HERE/'tmp');self.folder=Path(self.temp.name)
        source=self.folder/'sources';source.mkdir()
        (source/'zenodo-deposit.json').write_bytes(baseline.CAPTURED.manifest.read_bytes())
        for entry in baseline.FILES:(source/entry['name']).write_bytes(entry['path'].read_bytes())
        self.captured=nt.capture_inputs(source/'zenodo-deposit.json')
        self.server=AnnotationServer()
        self.client=nt.NativeOwnDraftClient(TOKEN,self.captured.metadata,self.captured.files,allow_writes=True,journal_path=self.folder/'journal.json')
        self.patches=[patch.object(nt.http.client,'HTTPSConnection',side_effect=self.server.connection),
                      patch.object(kit,'STATE_DIR',self.folder/'kit-state'),patch.object(kit,'CHUNK',2047),
                      patch.object(kit,'doi_status',return_value={'status':'resolved','http_status':200,'url':'https://doi.org/'+nt.DOI})]
        for patcher in self.patches:patcher.start()
        self.place=kit.state_path(self.captured.manifest,'production')
        kit.save_state(self.place,{'id':nt.RECORD_ID,'manifest':str(self.captured.manifest),'environment':'production'})
    def tearDown(self):
        for patcher in reversed(self.patches):patcher.stop()
        self.temp.cleanup()
    def run_kit(self,command):
        return nt.run_captured_kit(argparse.Namespace(command=command,sandbox=False,confirm_id=nt.RECORD_ID,check_doi=True),self.captured,self.client)
    def writes(self):return [(method,url) for method,url in self.server.calls if method!='GET']
    def stage(self):self.assertEqual(self.run_kit('stage')['state'],'ready_to_publish')
    def assert_no_preview_reads(self):
        self.assertFalse(any('/iiif/' in url or url.endswith('/container') for _,url in self.server.calls))
    def test_full_deployed_shapes_stage_publish_inspect_and_real_kit_receipt(self):
        self.stage()
        self.assertEqual([method for method,_ in self.writes()],['POST','PUT','POST']*2)
        for upload in self.server.uploads:
            self.assertEqual((upload['size'],upload['sha256']),nt.FILE_PINS[upload['name']])
            self.assertEqual(upload['md5'],nt.FILE_MD5_PINS[upload['name']])
        receipt=self.run_kit('publish')
        self.assertEqual(receipt['state'],'published');self.assertTrue(receipt['receipt_saved'])
        self.assertEqual(kit.read_json(self.place)['publication'],receipt)
        before=self.writes();self.assertEqual(self.run_kit('inspect')['state'],'published')
        self.assertTrue(self.run_kit('publish')['already_published']);self.assertEqual(self.writes(),before)
        self.assert_no_preview_reads()
    def test_full_deployed_shapes_lost_publish_response_recovers_once(self):
        self.stage();self.server.loss=('POST',nt.DRAFT+'/actions/publish')
        receipt=self.run_kit('publish')
        self.assertTrue(receipt['recovered_after_publish_error']);self.assertTrue(receipt['receipt_saved'])
        self.assertEqual(kit.read_json(self.place)['publication'],receipt)
        before=self.writes();self.run_kit('inspect');self.run_kit('publish');self.assertEqual(self.writes(),before)
        self.assertEqual(sum(url.endswith('/actions/publish') for _,url in self.writes()),1)
        self.assert_no_preview_reads()
    def test_metadata_only_links_only_and_combined_shapes_draft_and_published(self):
        self.stage()
        for name in (PDF,ZIP):
            for variant in ('metadata','links','both'):
                def restrict(entry,draft,n=name,v=variant):
                    if entry['key']!=n:return
                    if v=='links':entry['metadata']=None
                    if v=='metadata':
                        entry['links']={key:value for key,value in entry['links'].items() if key in ('self','content','commit')}
                self.server.entry_mutator=restrict
                for published in (False,True):
                    with self.subTest(name=name,variant=variant,published=published):
                        self.server.published=published
                        result=self.run_kit('inspect');self.assertEqual(result['state'],'published' if published else 'ready_to_publish')
        self.assert_no_preview_reads()
    def test_derived_values_and_file_type_are_rejected_through_real_wire(self):
        self.stage();before=self.writes()
        cases=[(PDF,{'width':True,'height':792}),(PDF,{'width':612.0,'height':792}),
               (PDF,{'width':'612','height':792}),(PDF,{'width':611,'height':792}),
               (PDF,{'width':612,'height':0}),(PDF,{'width':612}),
               (PDF,{'width':612,'height':792,'author':'user'}),(PDF,{'zip_toc_position':218946}),
               (PDF,['width','height']),(ZIP,{'zip_toc_position':True}),
               (ZIP,{'zip_toc_position':218946.0}),(ZIP,{'zip_toc_position':'218946'}),
               (ZIP,{'zip_toc_position':200806}),(ZIP,{'zip_toc_position':-1}),
               (ZIP,{'zip_toc_position':218946,'author':'user'}),(ZIP,{'width':612,'height':792})]
        for name,metadata in cases:
            for published in (False,True):
                with self.subTest(name=name,metadata=metadata,published=published):
                    self.server.published=published
                    self.server.entry_mutator=lambda entry,draft,n=name,m=metadata:entry.update(metadata=m) if entry['key']==n else None
                    with self.assertRaises(kit.DepositError):self.run_kit('inspect' if published else 'publish')
                    self.assertEqual(self.writes(),before)
        for name,bad_mime in ((PDF,'application/zip'),(ZIP,'application/pdf'),(PDF,True),(ZIP,{})):
            self.server.published=False
            self.server.entry_mutator=lambda entry,draft,n=name,m=bad_mime:entry.update(mimetype=m) if entry['key']==n else None
            with self.assertRaises(kit.DepositError):self.run_kit('publish')
        self.assertEqual(self.writes(),before);self.assertNotIn('publication',kit.read_json(self.place))
    def test_unknown_partial_cross_type_and_wrong_state_links_rejected(self):
        self.stage();before=self.writes()
        changes=[
            lambda entry,draft:entry['links'].update(user='https://zenodo.org/user'),
            lambda entry,draft:entry['links'].pop('iiif_api') if entry['key']==PDF else None,
            lambda entry,draft:entry['links'].update(container=nt.DRAFT+'/files/'+PDF+'/container') if entry['key']==PDF else None,
            lambda entry,draft:entry['links'].update(iiif_base='https://zenodo.org/api/iiif/draft:23356540:'+ZIP) if entry['key']==ZIP else None,
            lambda entry,draft:entry['links'].update(derived_links(entry['key'],not draft)),
            lambda entry,draft:entry['links'].update(commit=nt.DRAFT+'/files/'+entry['key']+'/commit') if not draft else entry['links'].pop('commit'),
        ]
        for change in changes:
            for published in (False,True):
                with self.subTest(change=change,published=published):
                    self.server.published=published;self.server.entry_mutator=change
                    with self.assertRaises(kit.DepositError):self.run_kit('inspect' if published else 'publish')
                    self.assertEqual(self.writes(),before)
        self.assert_no_preview_reads()
    def test_every_derived_link_rejects_wrong_host_id_filename_query_fragment_state(self):
        self.stage();before=self.writes()
        for name in (PDF,ZIP):
            for published in (False,True):
                self.server.published=published
                for key,good in derived_links(name,not published).items():
                    variants=[good.replace('zenodo.org','evil.example'),good.replace('https:','http:'),
                              good.replace('23356540','23356541'),good.replace(name,'foreign.pdf'),
                              good+'?x=1',good+'#fragment',good+'?',good+'#',
                              good.replace('zenodo.org','token@zenodo.org'),good.replace('zenodo.org','zenodo.org:444')]
                    for bad in variants:
                        with self.subTest(name=name,key=key,url=bad,published=published):
                            self.server.entry_mutator=lambda entry,draft,n=name,k=key,u=bad:entry['links'].update({k:u}) if entry['key']==n else None
                            with self.assertRaises(kit.DepositError):self.run_kit('inspect' if published else 'publish')
                            self.assertEqual(self.writes(),before)
        self.assertNotIn('publication',kit.read_json(self.place));self.assert_no_preview_reads()
    def test_annotation_acceptance_does_not_weaken_content_sha_or_md5(self):
        self.stage();before=self.writes();self.server.download_corrupt=True
        with self.assertRaises(kit.DepositError):self.run_kit('publish')
        self.server.download_corrupt=False
        self.server.entry_mutator=lambda entry,draft:entry.update(checksum='md5:'+'0'*32) if entry['key']==PDF else None
        with self.assertRaises(kit.DepositError):self.run_kit('publish')
        self.assertEqual(self.writes(),before);self.assertFalse(self.server.published)
    def test_malformed_annotations_in_commit_ack_stop_after_reversible_commit(self):
        # Reject a hostile native acknowledgment through the actual kit request,
        # not by calling a validator directly. No publish follows the safe stop.
        self.server.entry_mutator=lambda entry,draft:entry.update(metadata={'width':False,'height':792}) if entry['key']==PDF and entry['status']=='completed' else None
        with self.assertRaises(kit.DepositError):self.run_kit('stage')
        self.assertEqual([method for method,_ in self.writes()],['POST','PUT','POST'])
        self.assertFalse(self.server.published);self.assert_no_preview_reads()
    def test_known_annotations_do_not_open_a_preview_request_route(self):
        for name in (PDF,ZIP):
            for url in derived_links(name,True).values():
                with self.assertRaises(kit.DepositError):self.client.request('GET',url)
        self.assertEqual(self.server.calls,[])


if __name__=='__main__':unittest.main(verbosity=2)
