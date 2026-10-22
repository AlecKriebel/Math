"""Fresh real binary-child and interrupted-HTTP evidence preservation checks."""
from pathlib import Path
import http.client, json, subprocess, sys, urllib.request
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import release_binding as rb
import append_verified_tracker as a
import verify_published_readonly as v
import publish_preprint as p
CASE=HERE/'minimal_synthetic_case'
R,PUB=CASE/'preprint',CASE/'publication'
CTX=rb.context(R)
Z=rb.publication(R,PUB,CTX)
ROOT=HERE/'stream_fixture'
ROOT.mkdir(exist_ok=False)
stdout=b'output\x00\xffbinary'
stderr=b'error\x00\xfebinary'
actual_run=subprocess.run
observed=[]

def binary_child(*args,**kwargs):
    # Only this actual local Python child executes. The proposed gh/GWS/tool
    # arguments supplied by the candidates never execute or contact a provider.
    assert kwargs.get('text') is False
    source='import os;os.write(1,'+repr(stdout)+');os.write(2,'+repr(stderr)+')'
    return actual_run([sys.executable,'-B','-c',source],capture_output=True,text=False)

subprocess.run=binary_child
try:
    f=ROOT/'append';f.mkdir()
    try:a.reader(f)('binary',['not-executed'])
    except UnicodeDecodeError:pass
    else:raise AssertionError('Expected actual decode failure')
    assert (f/'binary-stdout.json').read_bytes()==stdout and (f/'binary-stderr.txt').read_bytes()==stderr
    observed.append('append reader preserves actual binary child streams')
    f=ROOT/'inspect';f.mkdir()
    try:v.inspect_existing(R,CTX,Z['id'],f)
    except UnicodeDecodeError:pass
    else:raise AssertionError('Expected actual decode failure')
    assert (f/'inspect-stdout.json').read_bytes()==stdout and (f/'inspect-stderr.txt').read_bytes()==stderr
    observed.append('publication inspect preserves actual binary child streams')
    f=ROOT/'fresh_publish';f.mkdir()
    try:p.publish_once(R,f,ROOT=CASE)
    except UnicodeDecodeError:pass
    else:raise AssertionError('Expected actual decode failure')
    outputs=list(f.rglob('PR-head-preflight-stdout.json'));errors=list(f.rglob('PR-head-preflight-stderr.txt'))
    assert len(outputs)==len(errors)==1 and outputs[0].read_bytes()==stdout and errors[0].read_bytes()==stderr
    assert not (f/'STAGE_ATTEMPT.json').exists() and not (f/'PUBLISH_ATTEMPT.json').exists()
    observed.append('publication preflight preserves actual binary streams and performs no stage')
finally:subprocess.run=actual_run

class Interrupted:
    def __init__(self):self.step=0
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self,n):
        self.step+=1
        if self.step==1:return b'ab'
        if self.step==2:return b'cd'
        raise http.client.IncompleteRead(b'\x00\xfftail',999)

f=ROOT/'http';f.mkdir()
actual_open=urllib.request.urlopen
urllib.request.urlopen=lambda *args,**kwargs:Interrupted()
try:
    try:v.public_bytes(R,CTX,Z,f)
    except http.client.IncompleteRead:pass
    else:raise AssertionError('Expected actual HTTP IncompleteRead')
finally:urllib.request.urlopen=actual_open
body=(f/CTX['expected_files'][0]['name']).read_bytes()
assert body==b'abcd\x00\xfftail'
failure=json.loads((f/(CTX['expected_files'][0]['name']+'-READ_FAILURE.json')).read_text())
assert failure['retained_bytes']==10 and failure['exception_partial_bytes']==6 and failure['error_type']=='IncompleteRead'
observed.append('HTTP preserves two earlier chunks plus actual IncompleteRead.partial')
(HERE/'STREAM_RESULTS.json').write_text(json.dumps(dict(groups=4,all_expected_observations=True,observations=observed,actual_child_processes=3,no_provider_command_executed=True),indent=2)+'\n')
print(json.dumps(dict(groups=4,all_expected_observations=True,observations=observed)))
