"""Exclusive actual fsync journal with expected-byte history, not a projection."""
from pathlib import Path
import json,os,stat
from ops_core import require

class Journal:
    def __init__(self,path):
        self.path=Path(path);self.expected={}
        require(not self.path.exists(),'Existing actionCASE: GET-only reconciliation; never retry or alternate CASE')
        require(not self.path.parent.is_symlink(),'Action parent symlink')
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.path.mkdir(mode=0o700,exist_ok=False)
        self.sync(self.path.parent)

    def sync(self,path):
        fd=os.open(path,os.O_RDONLY)
        try:os.fsync(fd)
        finally:os.close(fd)

    def save(self,name,value):
        require(Path(name).name==name and name not in self.expected,'Invalid or repeated journal leaf')
        data=(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
        # Register intended bytes before any actual fsync callback can mutate it.
        self.expected[name]=data
        with (self.path/name).open('xb') as f:
            os.fchmod(f.fileno(),0o600);f.write(data);f.flush();os.fsync(f.fileno())
        self.sync(self.path)
        self.check()
        return data

    def check(self):
        require(self.path.is_dir() and not self.path.is_symlink(),'Journal directory replaced')
        require({p.name for p in self.path.iterdir()}==set(self.expected),'Unknown/missing durable history leaf')
        for name,data in self.expected.items():
            p=self.path/name
            require(p.is_file() and not p.is_symlink() and stat.S_IMODE(p.stat().st_mode)==0o600 and p.read_bytes()==data,'Durable exact history changed: '+name)
