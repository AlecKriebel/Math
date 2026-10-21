"""Root one-time stable program lock installation; no views, native APIs or phases."""
import sys
if not (sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):
    raise RuntimeError('Ordinary Python -E -S -B -P required before dependencies')
from pathlib import Path
import argparse,datetime,fcntl,hashlib,json,os,stat,tempfile
D=Path(__file__).absolute().parent
A=D.parent
P=A.parent.parent
LOCK=P/'ROOT_GLOBAL_FIVE_WRITER.lock'
PAYLOAD=b'PR publication program: stable Root cooperating global-five writer lock v1\nNever unlink or replace this inode; every existing-view writer must flock it.\n'
EXPECTED={'bytes':153,'sha256':'61404e167a3dedccc0fd17a1a1823fd772bc12a9144a4f012ab26d5e2a26fc0a'}
def need(ok,msg):
    if type(ok) is not bool or not ok:raise RuntimeError(msg)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def syncdir(p):
    fd=os.open(p,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
def read(p,wanted):
    need(p.resolve(strict=True)==p and p.is_relative_to(P),'Canonical program input')
    before=p.lstat();need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode)==0o444 and before.st_size<=2000000,'Regular readonly input before open')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC|os.O_NONBLOCK)
    try:
        s=os.fstat(fd);need(stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o444 and s.st_size<=2000000,'Regular readonly bounded input')
        raw=os.read(fd,2000001)
    finally:os.close(fd)
    need(pin(raw)==wanted,'Exact Root-adopted input');return raw
def durable(path,raw):
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
    try:
        with os.fdopen(fd,'wb',closefd=False) as f:need(f.write(raw)==len(raw),'Short durable write');f.flush();os.fsync(fd)
    finally:os.close(fd)
    syncdir(path.parent)
class SafeParser(argparse.ArgumentParser):
    def error(self,message):raise RuntimeError('Invalid command arguments')
def main():
    ap=SafeParser();ap.add_argument('--adoption-bytes',type=int,required=True);ap.add_argument('--adoption-sha256',required=True);args=ap.parse_args()
    wanted={'bytes':args.adoption_bytes,'sha256':args.adoption_sha256}
    a=json.loads(read(A/'ROOT_LIFECYCLE_SOURCE_ADOPTION_01.json',wanted))
    need(a.get('schema')=='pr206-root-lifecycle-source-adoption-v1' and a.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and a.get('PR')==206 and a.get('accepted_preparation_only') is True,'Actual Root source adoption')
    read(Path(__file__).absolute(),a['program_lock_installer_pin'])
    protocol=a['program_view_writer_protocol']
    need(protocol=={'schema':'pr206-program-view-writer-protocol-v1','lock_path':'draft_pr_publication_program_20260930/ROOT_GLOBAL_FIVE_WRITER.lock','lock_payload':EXPECTED,'every_existing_view_writer_must_hold_same_stable_inode':True,'never_unlink_or_replace_lock_inode':True,'Root_alone_operates_existing_views':True,'uncooperative_same_UID_content_CAS_guaranteed':False},'Exact global cooperative writer protocol')
    need(pin(PAYLOAD)==EXPECTED and LOCK.resolve(strict=False)==LOCK,'Exact lock payload/canonical path')
    for p in (D,A,P):need(p.is_dir() and not p.is_symlink() and p.resolve(strict=True)==p,'Canonical owned/program directory')
    begin={'schema':'pr206-root-program-lock-installation-attempt-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'adoption_pin':wanted,'views_or_phase_actions':False}
    durable(D/'INSTALL_ATTEMPT.json',(json.dumps(begin,sort_keys=True,indent=2)+'\n').encode())
    created=False
    if not os.path.lexists(LOCK):
        fd,name=tempfile.mkstemp(prefix='stable_program_lock_staged_',dir=D)
        with os.fdopen(fd,'wb') as f:need(f.write(PAYLOAD)==len(PAYLOAD),'Short staged lock');f.flush();os.fchmod(f.fileno(),0o444);os.fsync(f.fileno())
        staged=Path(name);syncdir(D)
        try:os.link(staged,LOCK,follow_symlinks=False);syncdir(P);created=True
        except FileExistsError:pass
    read(LOCK,EXPECTED)
    fd=os.open(LOCK,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC|os.O_NONBLOCK)
    try:
        fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        opened=os.fstat(fd);current=LOCK.lstat()
        need(stat.S_ISREG(current.st_mode) and (opened.st_dev,opened.st_ino)==(current.st_dev,current.st_ino),'Stable installed descriptor/path inode')
        read(LOCK,EXPECTED)
        result={'schema':'pr206-root-program-lock-installation-receipt-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':206,'accepted':True,'created_now':created,'reused_existing_without_chmod_unlink_replace':not created,'lock_relative_path':protocol['lock_path'],'payload_pin':EXPECTED,'device':opened.st_dev,'inode':opened.st_ino,'actual_source_adoption_pin':wanted,'all_future_Root_existing_view_writers_required_to_obey_same_stable_inode':True,'uncooperative_same_UID_content_CAS_guaranteed':False,'actual_global_views_native_services_or_phase_actions':False}
        raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode();durable(D/'ROOT_PROGRAM_LOCK_INSTALLATION_RECEIPT.json',raw)
        last=LOCK.lstat();need((last.st_dev,last.st_ino)==(opened.st_dev,opened.st_ino),'Stable inode through receipt')
    finally:
        try:fcntl.flock(fd,fcntl.LOCK_UN)
        finally:os.close(fd)
    print(json.dumps({'status':'PASS','receipt_pin':pin(raw),'created_now':created,'views_or_phase_actions':False},sort_keys=True))
def entry():
    try:main()
    except BaseException as error:
        if isinstance(error,SystemExit) and (error.code is None or (type(error.code) is int and error.code==0)):return
        sys.stderr.write('Root PR206 installer failed: '+type(error).__name__+'\n')
        raise SystemExit(1) from None
if __name__=='__main__':entry()

