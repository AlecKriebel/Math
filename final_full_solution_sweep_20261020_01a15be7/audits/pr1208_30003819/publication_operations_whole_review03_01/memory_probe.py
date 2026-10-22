from pathlib import Path
import hashlib,sys,socket,http.client,urllib.request,subprocess,os,json,datetime
p=Path("/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr1208_30003819/publication_operations_preparation_03")
attempts=[]
def blocked(*a,**k):attempts.append("external transport");raise RuntimeError("External interfaces disabled")
socket.socket=blocked;socket.create_connection=blocked;socket.getaddrinfo=blocked
http.client.HTTPConnection=blocked;http.client.HTTPSConnection=blocked;urllib.request.urlopen=blocked;urllib.request.OpenerDirector.open=blocked;subprocess.run=blocked;subprocess.Popen=blocked;os.system=blocked;os.popen=blocked
raw=(p/"bootstrap.py").read_bytes()
if hashlib.sha256(raw).hexdigest()!="f1c9823ce373884b8f630e1ce405de3761eacb65f2ee480a710aeb0fe26bb2b0":raise RuntimeError("prehash")
ns={"__file__":str(p/"bootstrap.py"),"__name__":"independent_checked_bootstrap"};exec(compile(raw,str(p/"bootstrap.py"),"exec",dont_inherit=True,optimize=0),ns)
load,_=ns["load_verified"](p,"4403a056d8cbd39ab06cf225cd0d294daaaa81a8e4318b970c77367826f6bd02","f1c9823ce373884b8f630e1ce405de3761eacb65f2ee480a710aeb0fe26bb2b0");c=load("common");c.zenodo.token_for=blocked;M=load("models");runner=load("runner");fixture=M.inputs();base=M.World(fixture)
def call(w,a):return runner.main([a,"--expected-pr-head",w.git.head],provider=w,test_adoption=w.adoption,test_journal=w.j)
for action in ["integrate","describe","ready","merge","stage"]:call(base,action)
positive=base.clone();ans=call(positive,"publish");rows=[{"case":"positive_publish","accepted":True,"answer":ans,"POSTs":positive.native.calls.count("publish")}]
tests={
 "native_version_boolean":lambda l,n,f:n["versions"].__setitem__("index",True),
 "native_count_boolean":lambda l,n,f:n["media_files"].__setitem__("count",False),
 "parent_expiry_boolean":lambda l,n,f:n["parent"]["access"]["settings"].__setitem__("secret_link_expiration",False),
 "display_rights_contradiction":lambda l,n,f:n["ui"].__setitem__("rights",[{"id":"copyright-reserved","title":{"en":"All rights reserved"}}]),
 "display_creators_boolean":lambda l,n,f:n["ui"].__setitem__("creators",True),
 "native_self_wrong_record":lambda l,n,f:n["links"].__setitem__("self","https://zenodo.org/api/records/999/draft")
}
for name,fault in tests.items():
 w=base.clone();w.native.fault=fault
 try:ans=call(w,"publish");err=None
 except Exception as e:ans=None;err=type(e).__name__+": "+str(e)
 rows.append({"case":name,"accepted":ans is not None,"answer":ans,"error":err,"POSTs":w.native.calls.count("publish"),"PUBLISH_VERIFIED":w.j.exists("PUBLISH_VERIFIED")})
if attempts:raise RuntimeError("External attempt")
print(json.dumps({"at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"review_scope":"actual checked runner parser, MemoryJournal only; not production-fsynced evidence","results":rows,"external_attempts":attempts,"actual_filesystem_mutations":0},indent=2))
