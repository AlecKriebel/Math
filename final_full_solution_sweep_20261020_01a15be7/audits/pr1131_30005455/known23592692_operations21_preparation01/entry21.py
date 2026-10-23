"""SOURCE21 sole known23592692 recovery entry; separately adopted roles required.
No authority, runtime, state or service effect occurs on import or describe.
"""
import sys
if sys.flags.optimize!=0 or not __debug__ or not(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):raise RuntimeError('Require Python -I -S -B optimize0')
from pathlib import Path
import argparse,hashlib,re
P=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr1131_30005455')
E=Path(__file__).resolve().parent;SOURCE=E/'source21'
SOURCE21='c64fae35c2ea0ebd7213e0791559f3cb5eba9f87a5b6fa8a0fc2038af2da9670'
SOURCE20='2e434f85b085fcf9a5cc873a15a29e70623888b6d59194aa4c010124f5cc3455'
CENSUS20='0774d5637b1496bfe55497c68c394ad25053f1aabe77b9f572feec830c47eab6'
ENTRY19='126bc8ead8c2fa269d20fbc5e38d11a3a769ee4e28c52a93ed33d493bf927ef2'
AUTHORITY=P/'known23592692_operations21_authority01/ROOT_OPERATIONAL_CLEARANCE21.json'
COMPAT20=P/'known23592692_operations21_authority01/ROOT_OPERATIONAL_CLEARANCE20_COMPAT21.json'
HEAD='9601e1e768c94522bc8ad105db4dfae4770bad75'
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def checked(path,pin):
    need(path.is_file()and not any(q.is_symlink()for q in[path,*path.parents]),'exact regular no-symlink source path');raw=path.read_bytes();need(sha(raw)==pin,'complete source changed before compile');return raw
def execute(path,pin):
    raw=checked(path,pin);ns={'__file__':str(path),'__name__':'checked_source21_'+path.stem};exec(compile(raw,str(path),'exec',dont_inherit=True,optimize=0),ns);return ns
def components():
    import json
    raw=(SOURCE/'SOURCE_MANIFEST21.json').read_bytes();need(sha(raw)==SOURCE21,'complete SOURCE21 source manifest');mf=json.loads(raw)
    need(set(q.name for q in SOURCE.iterdir())==set(mf)|{'SOURCE_MANIFEST21.json'},'complete SOURCE21 namespace')
    for name,pin in mf.items():need(len(checked(SOURCE/name,pin['sha256']))==pin['bytes'],'complete source length')
    overlay=execute(SOURCE/'overlay21.py',mf['overlay21.py']['sha256']);overlay['sources'](SOURCE,SOURCE21)
    ns20=execute(P/'operations20/source/census20.py',CENSUS20);ns20['load_data'](ns20['sources'](P/'operations20/source',SOURCE20))
    entry19=execute(P/'ROOT_PRELAUNCH19.py',ENTRY19)
    return overlay,ns20,entry19
def prepare(argv):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['stage-known','publish','verify-public','ledger'])
    parser.add_argument('--expected-pr-head',required=True);parser.add_argument('--deposit-id',type=int,required=True)
    parser.add_argument('--clearance-sha256',required=True);parser.add_argument('--root21-clearance-sha256',required=True);parser.add_argument('--compat20-clearance-sha256',required=True)
    args=parser.parse_args(argv);need(args.expected_pr_head==HEAD and type(args.deposit_id)is int and args.deposit_id==23592692,'exact accepted known target/head')
    for value in[args.clearance_sha256,args.root21_clearance_sha256,args.compat20_clearance_sha256]:need(re.fullmatch('[a-f0-9]{64}',value or''),'exact external authority digest')
    overlay,ns20,entry19=components();action='resume-stage'if args.action=='stage-known'else args.action
    base=[action,'--expected-pr-head',HEAD,'--clearance-sha256',args.clearance_sha256]
    if action!='resume-stage':base+=['--deposit-id',str(args.deposit_id)]
    # Authenticated old entry's initial no-ID parser is used only for loading19.
    # The actual known-ID command surface is explicitly SOURCE21 below.
    m,_=entry19['prepare'](base);need(args.clearance_sha256=='55eb5e5e8a62553bd342ee690a753d1f66b8d63fd8f9cfe56d9b7c7f8f403e79','original ROOT19 identity')
    entry=Path(__file__).resolve();policy=overlay['KnownPolicy21'](m,SOURCE,SOURCE21,entry,sha(entry.read_bytes()),AUTHORITY,args.root21_clearance_sha256,COMPAT20,args.compat20_clearance_sha256,ns20)
    guard=ns20['Guard'](m,P/'operations20/source',SOURCE20,entry,sha(entry.read_bytes()),COMPAT20,args.compat20_clearance_sha256)
    policy.attach_guard(guard);policy.check()
    actual=[action,'--expected-pr-head',HEAD,'--deposit-id',str(args.deposit_id),'--clearance-sha256',args.clearance_sha256]
    return m,actual,policy,guard
def main(argv=None):
    m,args,policy,guard=prepare(sys.argv[1:]if argv is None else argv);return m.main(args)
if __name__=='__main__':main()
