"""Fixed-path, externally pinned raw authority parsing. Import has no effects."""
from pathlib import Path
import stat,json,datetime
from ops_core import require,sha,canonical,strict_json,typed_equal

LEAVES={'activation':'ACTIVATION.json','root':'ROOT_ACTION_APPROVAL.json','independent':'INDEPENDENT_ACTION_REVIEW.json','gate':'REVIEWED_GATE.json'}
def no_symlinks(p):
    p=Path(p);require(p.is_absolute(),'Absolute fixed path required')
    for q in [p,*p.parents]:require(not q.is_symlink(),'Symlink in fixed path')
    return p
def exact_file(path,digest):
    p=no_symlinks(path);s=p.lstat();require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'Authority must be a regular single-link file')
    b=p.read_bytes();require(type(digest)is str and len(digest)==64 and sha(b)==digest,'Externally pinned authority/input bytes changed')
    return b
def semantic_keys(gate):
    return sorted(sha(canonical(x))for x in gate['semantic_decisions']+gate['intrabatch']+gate['cross_batch_eleven'])
class Authority:
    def __init__(self,config,pins,source_sha,plan_bytes,revision_sha,clock):
        require(set(pins)==set(LEAVES),'Four externally pinned authority roles required')
        self.paths={k:Path(config['authority_dir'])/v for k,v in LEAVES.items()};self.pins=pins;self.config=config;self.source_sha=source_sha;self.plan_bytes=plan_bytes;self.revision_sha=revision_sha;self.clock=clock;self.original=None
        self.check()
    def check(self):
        raw={k:exact_file(p,self.pins[k])for k,p in self.paths.items()}
        if self.original is not None:require(raw==self.original,'Original authority evidence changed')
        j={k:strict_json(v)for k,v in raw.items()};gate=j['gate'];a=j['activation'];keys=semantic_keys(gate)
        require(type(a)is dict and a.get('ready_for_execution')is True,'Activation is not affirmative literal true')
        require(a.get('source_manifest_sha256')==self.source_sha and a.get('plan_sha256')==sha(self.plan_bytes)and a.get('reviewed_gate_sha256')==self.pins['gate'],'Activation exact source/plan/gate binding')
        require(a.get('fixed_samecase')==self.config['case']and a.get('book')==self.config['book']and type(a.get('gid'))is int and a['gid']==self.config['gid'],'Activation fixed target/SAMECASE drift')
        require(a.get('root_approval_sha256')==self.pins['root']and a.get('independent_review_sha256')==self.pins['independent'],'Activation review byte pins')
        require(self.paths['root']!=self.paths['independent']and self.pins['root']!=self.pins['independent'],'Distinct root/independent raw evidence required')
        for role in ['root','independent']:
            e=j[role];require(type(e)is dict and e.get('role')==role and e.get('accepted')is True,'Exact independent/root action role absent')
            require(e.get('root_action_adoption')is(role=='root')and e.get('independent_whole_review')is(role=='independent'),'Wrong or conflated review role')
            require(e.get('source_manifest_sha256')==self.source_sha and e.get('plan_sha256')==sha(self.plan_bytes)and e.get('reviewed_gate_sha256')==self.pins['gate'],'Review exact source/plan/gate drift')
            require(e.get('literal1263_revision_sha256')==self.revision_sha and typed_equal(e.get('approved_semantic_keys'),keys),'Every exact semantic/literal decision must be adopted')
            require(e.get('fixed_samecase')==self.config['case'],'Review alternate CASE forbidden')
            for key,value in [('row_count',34),('new_publications',0),('native_write_attempt_limit',1)]:require(type(e.get(key))is int and e[key]==value,'Typed review action scope')
        for e in [a,j['root'],j['independent']]:
            require(type(e.get('valid_until_utc'))is str,'Explicit expiry required')
            deadline=datetime.datetime.fromisoformat(e['valid_until_utc']);require(deadline.tzinfo is not None and self.clock()<deadline.timestamp(),'Authority expired')
        require(gate.get('action_authority')is False and gate.get('root_action_adopted')is False,'Gate data cannot grant its own approval')
        require(gate.get('plan_sha256')==sha(self.plan_bytes),'Gate exact plan binding')
        if self.original is None:self.original=raw
        self.gate=gate
        return j
