"""Independent lifecycle tests at the stdlib HTTPSConnection boundary.

No method of the native client or unchanged kit is replaced. Only the external
connection is substituted. Mutable paths, locks, journals and receipts are own.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib, json, os, stat, sys, tempfile, types, unittest
from pathlib import Path
from unittest.mock import patch
import run_supplied as captured_modules

HERE = Path(__file__).resolve().parent
nt = captured_modules.nt
kit = nt.zenodo
TOKEN = 'offline-review-token-only'
fixture = json.loads((captured_modules.SNAP/'native_shape.json').read_bytes())

class Response:
    def __init__(self, status, data):
        self.status, self.data, self.pos = status, data, 0
    def read(self, size=-1):
        end = len(self.data) if size < 0 else min(len(self.data),self.pos+size)
        data = self.data[self.pos:end]
        self.pos = end
        return data

class Server:
    def __init__(self):
        self.entries, self.content = {}, {}
        self.published = False
        self.calls, self.uploads = [], []
        self.fault = None
        self.pending_get = False
        self.binary_status = 200
        self.record_mutator = self.list_mutator = None
        self.fake_md5 = False
        self.corrupt_download = False
        self.on_send = None
        self.mutation_ack = None
    def entry(self,name,draft=True):
        root = (nt.DRAFT if draft else nt.REC)+'/files/'+name
        done = self.entries[name] == 'completed'
        result = {'key':name,'status':'completed' if done else 'pending','metadata':None,
                  'links':{'self':root,'content':root+'/content'}}
        if draft: result['links']['commit'] = root+'/commit'
        if done:
            data = self.content[name]
            result.update(size=len(data),checksum='md5:'+hashlib.md5(data).hexdigest())
            if self.fake_md5: result['checksum'] = 'md5:'+nt.FILE_MD5_PINS[name]
        return result
    def record(self,draft):
        r=deepcopy(fixture)
        if not draft:
            r.update(is_draft=False,is_published=True,status='published')
            r['links'].update(self=nt.REC,files=nt.REC+'/files',self_html=nt.BASE+'/records/'+str(nt.RECORD_ID))
            r['pids']={'doi':{'identifier':nt.DOI,'provider':'datacite','client':'datacite'},
                       'oai':{'identifier':nt.OAI,'provider':'oai'}}
        r['files'].update(count=len(self.entries),entries={n:self.entry(n,draft) for n in self.entries},
                          total_bytes=sum(len(self.content[n]) for n,s in self.entries.items() if s=='completed'))
        if self.record_mutator: self.record_mutator(r)
        return r
    def collection(self,draft):
        result={'enabled':True,'entries':[self.entry(n,draft) for n in self.entries],
                'order':[],'default_preview':None,'links':{'self':(nt.DRAFT if draft else nt.REC)+'/files'}}
        if self.list_mutator: self.list_mutator(result)
        return result
    def connection(self,host,timeout):
        if host != 'zenodo.org': raise AssertionError('Wrong host reached wire')
        return Connection(self)
    def dispatch(self,method,target,headers,data):
        url=nt.BASE+target
        self.calls.append((method,url))
        if headers.get('Authorization') != 'Bearer '+TOKEN: raise AssertionError('Missing own token')
        if headers.get('User-Agent') != kit.USER_AGENT: raise AssertionError('Wrong user agent')
        if self.fault == (method,url,'before'):
            self.fault=None
            raise OSError('modeled connection lost before action')
        status=200
        if method=='GET':
            if url == nt.DRAFT:
                status,result=(404,{'message':'draft absent'}) if self.published else (200,self.record(True))
                if headers['Accept'] != nt.NATIVE_ACCEPT: raise AssertionError('Native draft negotiation')
            elif url == nt.REC:
                status,result=(200,self.record(False)) if self.published else (404,{'message':'not published'})
            elif url in [nt.DRAFT+'/files',nt.REC+'/files']:
                result=self.collection(url.startswith(nt.DRAFT))
            elif target.endswith('/content'):
                name=target.split('/')[-2]
                if headers['Accept'] != '*/*': return Response(406,b'{"message":"Not acceptable"}')
                if self.binary_status!=200: return Response(self.binary_status,b'blocked')
                if self.entries.get(name)=='pending' and not self.pending_get: return Response(404,b'pending unavailable')
                body=self.content.get(name,b'')
                if self.corrupt_download and body: body=bytes([body[0]^1])+body[1:]
                return Response(200,body)
            else: raise AssertionError((method,target))
        elif method=='POST' and url==nt.DRAFT+'/files':
            payload=json.loads(data)
            if type(payload) is not list or len(payload)!=1 or set(payload[0])!={'key'}: raise AssertionError('Initialization shape')
            name=payload[0]['key']
            if name in self.entries: raise AssertionError('Repeated initialize')
            self.entries[name]='pending'
            result=self.collection(True)
        elif method=='PUT' and target.endswith('/content'):
            name=target.split('/')[-2]
            if name in self.content: raise AssertionError('Repeated PUT')
            if headers['Content-Type']!='application/octet-stream': raise AssertionError('Upload type')
            if int(headers['Content-Length'])!=len(data): raise AssertionError('Upload length')
            self.content[name]=data
            self.uploads.append({'name':name,'size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'md5':hashlib.md5(data).hexdigest()})
            result=self.entry(name)
        elif method=='POST' and target.endswith('/commit'):
            name=target.split('/')[-2]
            if self.entries[name]=='completed': raise AssertionError('Repeated commit')
            self.entries[name]='completed'
            result=self.entry(name)
        elif method=='POST' and url==nt.DRAFT+'/actions/publish':
            if self.published: raise AssertionError('Repeated publication')
            if set(self.entries)!=set(nt.FILE_PINS) or any(s!='completed' for s in self.entries.values()): raise AssertionError('Incomplete publication')
            self.published=True
            result=self.record(False)
        else: raise AssertionError((method,target))
        if method!='GET' and self.mutation_ack: result=self.mutation_ack(method,url,result)
        if self.fault == (method,url,'after'):
            self.fault=None
            raise OSError('modeled response lost after action')
        return Response(status,json.dumps(result).encode())

class Connection:
    def __init__(self,server):
        self.server,self.headers,self.blocks=server,{},[]
        self.closed=False
    def putrequest(self,method,target): self.method,self.target=method,target
    def putheader(self,key,value): self.headers[key]=value
    def endheaders(self): pass
    def send(self,data):
        if type(data) is not bytes: raise AssertionError('Non-byte transmission')
        self.blocks.append(data)
        if self.method=='PUT' and self.server.on_send: self.server.on_send(self,len(self.blocks))
    def request(self,method,target,headers):
        self.method,self.target,self.headers=method,target,headers
    def getresponse(self): return self.server.dispatch(self.method,self.target,self.headers,b''.join(self.blocks))
    def close(self): self.closed=True

class WireTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=HERE/'tmp')
        self.folder=Path(self.temp.name)
        source=self.folder/'sources';source.mkdir()
        (source/'zenodo-deposit.json').write_bytes(captured_modules.original.CAPTURED.manifest.read_bytes())
        for f in captured_modules.original.FILES:
            (source/f['name']).write_bytes(f['path'].read_bytes())
        self.captured=nt.capture_inputs(source/'zenodo-deposit.json')
        self.server=Server()
        self.client=nt.NativeOwnDraftClient(TOKEN,self.captured.metadata,self.captured.files,allow_writes=True,journal_path=self.folder/'journal.json')
        self.patches=[patch.object(nt.http.client,'HTTPSConnection',side_effect=self.server.connection),
                      patch.object(kit,'STATE_DIR',self.folder/'kit-state'),patch.object(kit,'CHUNK',2047),
                      patch.object(kit,'doi_status',return_value={'status':'resolved','http_status':200,'url':'https://doi.org/'+nt.DOI,'resolved_url':nt.BASE+'/records/'+str(nt.RECORD_ID)})]
        for p in self.patches:p.start()
        self.place=kit.state_path(self.captured.manifest,'production')
        kit.save_state(self.place,{'id':nt.RECORD_ID,'environment':'production','manifest':str(self.captured.manifest)})
    def tearDown(self):
        for p in reversed(self.patches):p.stop()
        self.temp.cleanup()
    def run_kit(self,command,client=None):
        args=argparse.Namespace(command=command,sandbox=False,confirm_id=nt.RECORD_ID,check_doi=True)
        return nt.run_captured_kit(args,self.captured,client=client or self.client)
    def writes(self):return [x for x in self.server.calls if x[0]!='GET']
    def restart(self):
        return nt.NativeOwnDraftClient(TOKEN,self.captured.metadata,self.captured.files,allow_writes=True,journal_path=self.folder/'journal.json')
    def stage(self):self.assertEqual(self.run_kit('stage')['state'],'ready_to_publish')
    def test_full_actual_wire_lifecycle_and_receipt(self):
        self.stage()
        self.assertEqual([m for m,u in self.writes()],['POST','PUT','POST']*2)
        for upload in self.server.uploads:
            self.assertEqual((upload['size'],upload['sha256']),nt.FILE_PINS[upload['name']])
            self.assertEqual(upload['md5'],nt.FILE_MD5_PINS[upload['name']])
        receipt=self.run_kit('publish')
        self.assertEqual(receipt['state'],'published')
        self.assertTrue(receipt['receipt_saved'])
        self.assertEqual(kit.read_json(self.place)['publication'],receipt)
        before=self.writes()
        self.assertTrue(self.run_kit('publish',self.restart())['already_published'])
        self.assertEqual(self.run_kit('inspect',self.restart())['state'],'published')
        self.assertEqual(before,self.writes())
    def test_manifest_and_both_payloads_replaced_during_actual_stream(self):
        changed=set()
        def race(conn,block):
            name=conn.target.split('/')[-2]
            p=self.folder/'sources'/name
            if block==1:
                replacement=self.folder/('changed-'+name)
                replacement.write_bytes(b'changed pathname')
                os.replace(replacement,p)
                (self.folder/'sources/zenodo-deposit.json').write_bytes(b'bad manifest')
                changed.add(name)
            else:
                with p.open('ab') as s:s.write(b'changed inode')
        self.server.on_send=race
        self.stage()
        self.assertEqual(changed,set(nt.FILE_PINS))
        for n,data in self.server.content.items():
            self.assertEqual((len(data),hashlib.sha256(data).hexdigest()),nt.FILE_PINS[n])
            self.assertEqual(hashlib.md5(data).hexdigest(),nt.FILE_MD5_PINS[n])
        self.assertEqual(self.run_kit('publish')['state'],'published')
    def test_lost_initialize_no_repeat_across_restart(self):
        self.server.fault=('POST',nt.DRAFT+'/files','before')
        with self.assertRaises(kit.DepositError):self.run_kit('stage')
        before=self.writes()
        for i in range(3):
            with self.assertRaises(kit.DepositError):self.run_kit('stage',self.restart())
        self.assertEqual(before,self.writes())
    def test_lost_initialize_after_registration_recovers(self):
        self.server.fault=('POST',nt.DRAFT+'/files','after')
        self.stage()
        self.assertEqual(len(self.writes()),6)
    def test_lost_content_unreadable_no_repeat_across_restart(self):
        name=self.captured.files[0]['name']
        self.server.fault=('PUT',nt.DRAFT+'/files/'+name+'/content','after')
        with self.assertRaises(kit.DepositError):self.run_kit('stage')
        before=self.writes()
        for i in range(3):
            with self.assertRaises(kit.DepositError):self.run_kit('stage',self.restart())
        self.assertEqual(before,self.writes())
        self.assertEqual(len(before),2)
    def test_lost_content_readable_exact_sha_recovers(self):
        name=self.captured.files[0]['name']
        self.server.pending_get=True
        self.server.fault=('PUT',nt.DRAFT+'/files/'+name+'/content','after')
        self.stage()
        self.assertEqual(len(self.writes()),6)
    def test_lost_content_readable_corrupt_sha_no_commit(self):
        name=self.captured.files[0]['name']
        self.server.pending_get=True;self.server.corrupt_download=True
        self.server.fault=('PUT',nt.DRAFT+'/files/'+name+'/content','after')
        with self.assertRaises(kit.DepositError):self.run_kit('stage')
        before=self.writes()
        with self.assertRaises(kit.DepositError):self.run_kit('stage',self.restart())
        self.assertEqual(before,self.writes());self.assertEqual(len(before),2)
    def test_lost_commit_before_action_no_repeat(self):
        name=self.captured.files[0]['name']
        self.server.fault=('POST',nt.DRAFT+'/files/'+name+'/commit','before')
        with self.assertRaises(kit.DepositError):self.run_kit('stage')
        before=self.writes()
        for i in range(3):
            with self.assertRaises(kit.DepositError):self.run_kit('stage',self.restart())
        self.assertEqual(before,self.writes())
    def test_lost_commit_after_action_readback_recovers(self):
        name=self.captured.files[0]['name']
        self.server.fault=('POST',nt.DRAFT+'/files/'+name+'/commit','after')
        self.stage();self.assertEqual(len(self.writes()),6)
    def test_lost_publish_before_action_no_repeat(self):
        self.stage();self.server.fault=('POST',nt.DRAFT+'/actions/publish','before')
        with self.assertRaises(kit.DepositError):self.run_kit('publish')
        before=self.writes()
        for i in range(3):
            with self.assertRaises(kit.DepositError):self.run_kit('publish',self.restart())
        self.assertEqual(before,self.writes())
        self.assertNotIn('publication',kit.read_json(self.place))
    def test_lost_publish_after_action_genuine_receipt_recovers(self):
        self.stage();self.server.fault=('POST',nt.DRAFT+'/actions/publish','after')
        receipt=self.run_kit('publish')
        self.assertTrue(receipt['recovered_after_publish_error']);self.assertTrue(receipt['receipt_saved'])
        self.assertEqual(kit.read_json(self.place)['publication'],receipt)
        before=self.writes();self.run_kit('publish',self.restart());self.assertEqual(before,self.writes())
    def test_receipt_save_failure_preserves_publication_and_recovers_readonly(self):
        self.stage()
        with patch.object(kit,'save_state',side_effect=OSError('receipt disk failure')):
            receipt=self.run_kit('publish')
        self.assertTrue(self.server.published);self.assertFalse(receipt['receipt_saved'])
        self.assertEqual(receipt['state'],'published');self.assertNotIn('publication',kit.read_json(self.place))
        before=self.writes()
        recovered=self.run_kit('inspect',self.restart())
        self.assertTrue(recovered['receipt_saved']);self.assertEqual(before,self.writes())
    def test_binary_negotiation_and_406_fail_closed(self):
        self.stage();before=self.writes();self.server.binary_status=406
        with self.assertRaises(kit.DepositError):self.run_kit('publish')
        self.assertEqual(before,self.writes());self.assertFalse(self.server.published)
        self.server.binary_status=200
        self.assertEqual(self.run_kit('inspect')['state'],'ready_to_publish')
    def test_remote_sha_checked_independently_of_advertised_md5(self):
        self.stage();before=self.writes();self.server.corrupt_download=True
        with self.assertRaises(kit.DepositError):self.run_kit('publish')
        self.assertEqual(before,self.writes());self.assertFalse(self.server.published)
    def test_strict_full_record_hostile_shape_matrix(self):
        edits=[lambda r:r.update(id='23356541'),lambda r:r.update(id=True),lambda r:r.update(is_draft=1),
               lambda r:r.update(is_published=0),lambda r:r.update(is_draft=False,is_published=True,status='published'),
               lambda r:r['metadata'].update(additional_titles=[]),lambda r:r['metadata']['creators'][0].update(role={'id':'author'}),
               lambda r:r['metadata']['creators'][0]['person_or_org']['identifiers'].append({'scheme':'gnd','identifier':'x'}),
               lambda r:r['metadata']['rights'][0].update(icon='changed'),lambda r:r['metadata']['subjects'].append({'subject':'extra'}),
               lambda r:r['metadata']['related_identifiers'][0]['relation_type'].update(title={'en':'changed'}),
               lambda r:r['access']['embargo'].update(active=0),lambda r:r['access'].update(files='restricted'),
               lambda r:r.update(custom_fields={'rich':'unreviewed'}),lambda r:r['links'].update(publish=nt.REC+'/draft/actions/other'),
               lambda r:r['links'].update(self=nt.BASE+'/api/records/23356541/draft'),lambda r:r['links'].update(files=nt.DRAFT+'/files/'),
               lambda r:r['links'].update(self_html=nt.BASE+'/uploads/23356541'),lambda r:r['files'].update(count=True),
               lambda r:r['files'].update(entries={'other.pdf':{}}),lambda r:r['pids'].update(doi={'identifier':nt.DOI,'provider':'external'}),
               lambda r:r['pids'].update(oai={'identifier':'oai:zenodo.org:23356541','provider':'oai'})]
        for change in edits:
            with self.subTest(change=change):
                self.server.record_mutator=change
                with self.assertRaises(kit.DepositError):self.run_kit('stage')
                self.assertEqual(self.writes(),[])
    def test_hostile_published_pids_no_receipt(self):
        self.stage();self.server.published=True
        exact=self.server.record(False)['pids']
        for bad in [{}, {'doi':exact['doi']},{'oai':exact['oai']},{**exact,'ark':{}},
                    {**exact,'doi':{'identifier':nt.DOI,'provider':'datacite','client':None}},
                    {**exact,'doi':{'identifier':nt.DOI,'provider':'datacite','client':'wrong'}},
                    {**exact,'oai':{'identifier':nt.OAI,'provider':'external'}},
                    {**exact,'oai':{'identifier':nt.OAI,'provider':'oai','client':'oai'}}]:
            self.server.record_mutator=lambda r,b=bad:r.update(pids=b)
            with self.subTest(bad=bad),self.assertRaises(kit.DepositError):self.run_kit('inspect')
            self.assertNotIn('publication',kit.read_json(self.place))
        self.assertEqual(len(self.writes()),6)
    def test_unknown_same_host_record_url_and_routing_matrix(self):
        cases=[('GET',nt.BASE+'/api/user/records'),('GET',nt.BASE+'/api/records/23356541'),
               ('PUT',nt.DRAFT),('DELETE',nt.DRAFT),('POST',nt.REC+'/versions'),
               ('GET',nt.DRAFT+'?x=1'),('GET',nt.DRAFT+'#x'),('GET',nt.DRAFT.replace('https:','http:')),
               ('GET',nt.DRAFT.replace('zenodo.org','zenodo.org:443')),('GET',nt.DRAFT.replace('zenodo.org','user@zenodo.org')),
               ('GET',nt.DRAFT.replace('zenodo.org','ZENODO.ORG')),('GET',nt.DRAFT+'/files/../files')]
        before=list(self.server.calls)
        for method,url in cases:
            with self.subTest(url=url),self.assertRaises(kit.DepositError):self.client.request(method,url)
        self.assertEqual(before,self.server.calls)
    def test_real_sync_failure_sticky_even_after_read_and_restart_no_blind_retry(self):
        fsync=nt.os.fsync;counter=0
        def fail(fd):
            nonlocal counter
            counter+=1
            if counter==2:raise OSError('directory fsync failed')
            return fsync(fd)
        with patch.object(nt.os,'fsync',side_effect=fail):
            with self.assertRaises(kit.DepositError):self.run_kit('stage')
        self.assertTrue(self.client._storage_failed);self.assertEqual(self.writes(),[])
        self.assertFalse(self.client.get(nt.RECORD_ID)['submitted'])
        with self.assertRaises(kit.DepositError):self.run_kit('stage')
        with self.assertRaises(kit.DepositError):self.run_kit('stage',self.restart())
        self.assertEqual(self.writes(),[])
    def test_process_lock_rejects_parallel_process_and_releases(self):
        import subprocess
        lock=self.folder/'lock'
        code='import fcntl,sys; f=open(sys.argv[1],"a+b"); fcntl.flock(f.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)'
        with nt.runner_lock(lock):
            result=subprocess.run([sys.executable,'-B','-c',code,str(lock)],capture_output=True)
            self.assertNotEqual(result.returncode,0)
        result=subprocess.run([sys.executable,'-B','-c',code,str(lock)],capture_output=True)
        self.assertEqual(result.returncode,0);self.assertEqual(stat.S_IMODE(lock.stat().st_mode),0o600)
    def test_privacy_connection_errors_redact_token(self):
        with patch.object(nt.http.client,'HTTPSConnection',side_effect=OSError('wire '+TOKEN)):
            # Constructor itself is outside the kit's try; this exception is not
            # printed by normal code, so exercise the protected connection send.
            pass
        class Bad(Connection):
            def getresponse(self):raise OSError('wire '+TOKEN)
        with patch.object(nt.http.client,'HTTPSConnection',side_effect=lambda *a,**k:Bad(self.server)):
            with self.assertRaises(kit.DepositError) as caught:self.client.get(nt.RECORD_ID)
        self.assertNotIn(TOKEN,str(caught.exception))

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(WireTests))
    record={'checked_utc':datetime.now(timezone.utc).isoformat(),'optimization':sys.flags.optimize,'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'real_network_calls':0,'scope':'actual native client and unchanged kit; substituted stdlib HTTPS connection only'}
    (HERE/('WIRE_OPTIMIZED.json' if sys.flags.optimize else 'WIRE_NORMAL.json')).write_text(json.dumps(record,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
