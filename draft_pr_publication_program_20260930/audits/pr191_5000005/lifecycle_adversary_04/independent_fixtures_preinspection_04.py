"""Independent fixtures sealed before author harness/results or implementation inspection.
No network, subprocess, repository, or production imports. Python standard library only.
"""
from dataclasses import dataclass, field
import copy
import hashlib
import json

ORIGINAL_HEAD = "a2791bdd3f7ecd5694aeeeb5dffb21964a5639fe"
ORIGINALS = {f"original/{i:02d}": f"original immutable {i}\n".encode() for i in range(16)}
PROTECTED_CLASSES = ("science-json", "science-text", "science-log", "paper", "case-proof", "support", "review", "gate", "control")
TRUSTED_BYTES = {f"protected/{kind}.txt": f"trusted approved gate {kind}\n".encode() for kind in PROTECTED_CLASSES}
PRIVATE_SENTINEL = "PR191_ADVERSARY04_PRIVATE_FOREIGN_ROW_SENTINEL_DO_NOT_PUBLISH"

def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(value):
    return (json.dumps(value,sort_keys=True,indent=2)+"\n").encode()

def object_id(kind,raw):
    return hashlib.sha1(kind.encode()+b" "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def blob(raw):
    return {"type":"blob", "raw":raw, "oid":object_id("blob",raw)}

def tree(entries):
    # Independent native tree serializer. Input entries: (mode, basename, object).
    raw=b"".join(str(mode).encode()+b" "+name.encode()+b"\0"+bytes.fromhex(obj["oid"]) for mode,name,obj in sorted(entries,key=lambda e:e[1]+("/" if e[0]==40000 else "")))
    return {"type":"tree", "raw":raw,"oid":object_id("tree",raw),"entries":list(entries)}

def flat_tree(files):
    nested={}
    for path,raw in files.items():
        node=nested
        parts=path.split("/")
        for part in parts[:-1]: node=node.setdefault(part,{})
        node[parts[-1]]=raw
    def build(node):
        return tree([(40000,name,build(value)) if isinstance(value,dict) else (100644,name,blob(value)) for name,value in node.items()])
    return build(nested)

def commit(files, parents, message="PR191 approved message\n"):
    t=flat_tree(files)
    raw=("tree "+t["oid"]+"\n"+"".join("parent "+p+"\n" for p in parents)+"author Independent Fixture <offline@invalid> 1792044000 +0000\ncommitter Independent Fixture <offline@invalid> 1792044000 +0000\n\n"+message).encode()
    return {"type":"commit","raw":raw,"oid":object_id("commit",raw),"tree":t,"parents":list(parents),"files":copy.deepcopy(files),"message":message}

@dataclass
class Calls:
    calls:list=field(default_factory=list)
    def record(self, entrypoint, **kwargs):
        self.calls.append({"entrypoint":entrypoint,**copy.deepcopy(kwargs)})
    def count(self, entrypoint):
        return sum(c["entrypoint"]==entrypoint for c in self.calls)

@dataclass
class PublicationFixture:
    calls:Calls=field(default_factory=Calls)
    stage_files:dict=field(default_factory=dict)
    stage_metadata:dict=field(default_factory=dict)
    inspected:bool=False
    production:dict|None=None
    generation:int=0
    uncertainty:str|None=None
    def stage(self,files,metadata):
        self.calls.record("kit.stage",files=files,metadata=metadata)
        self.stage_files=copy.deepcopy(files); self.stage_metadata=copy.deepcopy(metadata)
    def inspect(self):
        self.calls.record("kit.inspect")
        self.inspected=True
        return {"files":copy.deepcopy(self.stage_files),"metadata":copy.deepcopy(self.stage_metadata)}
    def publish(self, timeout_after=False):
        self.calls.record("kit.publish")
        if not self.inspected: raise AssertionError("publication without inspect")
        if self.production is not None: raise AssertionError("duplicate publication")
        self.production={"id":5000005,"doi":"10.5281/zenodo.5000005","production":True,"files":copy.deepcopy(self.stage_files),"metadata":copy.deepcopy(self.stage_metadata)}
        if timeout_after:
            self.uncertainty="unknown outcome"
            raise TimeoutError("write committed; outcome unknown")
        return copy.deepcopy(self.production)
    def observe(self):
        self.calls.record("production.read")
        self.generation+=1
        return {"generation":self.generation,"record":copy.deepcopy(self.production)}

@dataclass
class TrackerFixture:
    calls:Calls=field(default_factory=Calls)
    own:list=field(default_factory=list)
    foreign:list=field(default_factory=lambda:[[PRIVATE_SENTINEL,"private baseline"]])
    generation:int=0
    def append(self, target, gid, header, cells, mode="RAW", timeout_after=False):
        self.calls.record("tracker.append",target=target,gid=gid,header=header,cells=cells,mode=mode)
        if mode!="RAW" or len(cells)!=4: raise AssertionError("wrong append shape or mode")
        if self.own: raise AssertionError("blind duplicate append")
        self.own=list(cells)
        if timeout_after: raise TimeoutError("append committed; outcome unknown")
        return {"range":"A2:D2"}
    def read_own(self):
        self.generation+=1; self.calls.record("tracker.read_own",generation=self.generation)
        return {"generation":self.generation,"cells":copy.deepcopy(self.own)}
    def read_full(self):
        self.generation+=1; self.calls.record("tracker.read_full",generation=self.generation)
        return {"generation":self.generation,"rows":[copy.deepcopy(self.own),*copy.deepcopy(self.foreign)]}

QUALIFICATIONS=("bare A0/signed conjunction false for every n >= 5", "parity-selected K_PS signed law and existence for every n >= 3", "Ferudun exact same theorem and mechanisms credited", "no novelty/firstness/history/independence/current-openness certification", "extensive AI assistance; unrefereed")
def factual_state(stage,actual_publication=False,actual_tracker=False,actual_merge=False,actual_current_main=False,actual_receipt=False):
    if stage not in ("pending","95","100"): raise ValueError(stage)
    if stage=="95" and not (actual_publication and actual_tracker): raise ValueError("95 requires observations")
    if stage=="100" and not (actual_publication and actual_tracker and actual_merge and actual_current_main and actual_receipt): raise ValueError("100 requires actual factual acceptance and receipt")
    return {"stage":stage,"completed":40 if stage=="100" else 39,"published":24 if stage=="100" else 23,"cursor":192 if actual_receipt else 191,"claimed_solved":"2/5","scientific_qualifications":list(QUALIFICATIONS)}

def self_test():
    assert len(ORIGINALS)==16 and len(TRUSTED_BYTES)==9
    a=commit(TRUSTED_BYTES,[ORIGINAL_HEAD]); b=commit({**TRUSTED_BYTES,"unexpected":b"x"},[ORIGINAL_HEAD])
    assert a["oid"]!=b["oid"] and a["tree"]["oid"]!=b["tree"]["oid"]
    p=PublicationFixture(); p.stage({"paper.pdf":b"approved"},{"title":"qualified result"});p.inspect()
    try: p.publish(timeout_after=True)
    except TimeoutError: pass
    assert p.observe()["record"]["doi"].startswith("10.5281/") and p.calls.count("kit.publish")==1
    t=TrackerFixture()
    try:t.append("exact-target","gid-0",["a","b","c","d"],["own",1,"10.5281/zenodo.5000005","approved"],timeout_after=True)
    except TimeoutError:pass
    assert t.read_own()["cells"]==t.read_own()["cells"] and t.read_full()["rows"][1][0]==PRIVATE_SENTINEL
    assert t.calls.count("tracker.append")==1
    assert factual_state("pending")["cursor"]==191
    try:factual_state("100")
    except ValueError:pass
    else:raise AssertionError("early 100 fixture accepted")
    return {"fixture_self_checks":12,"status":"PASS","production_imports":False,"external_calls":False}
if __name__=="__main__": print(json.dumps(self_test(),sort_keys=True))
