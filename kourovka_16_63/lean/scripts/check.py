#!/usr/bin/env python3
"""Fail-closed offline runner for a mathematically incomplete formalization draft.

No command calls this the final group theorem. Default mode explicitly fails
because that theorem is absent. --milestones builds ALL current source; --module
is explicitly a smaller debugging run. --static-only and --prepare-audit do not
invoke Lean. Pin checkout does not reset an existing repository or lake update.
"""
from __future__ import annotations
import argparse,datetime,hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
from audit_support import AuditError,inventory,closure,write_inventory,write_queries,parse_axioms,scan_text
from build_serial import build as build_serial, run_process
ROOT=Path(__file__).resolve().parents[1]
CHECKER_REV='e11f65c651edd58d68ba260015d2bfde5102cd7f'

class Runner:
    def __init__(self,timeout:int):
        stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
        self.dir=ROOT/'logs/runs'/stamp;self.dir.mkdir(parents=True)
        self.timeout=timeout;self.index=0;self.commands=[]
    def run(self,args:list[str],label:str,cwd:Path=ROOT):
        self.index+=1;path=self.dir/f'{self.index:03d}_{label}.log';t=time.perf_counter()
        try:
            code,output,timed_out=run_process(args,cwd=cwd,timeout=self.timeout)
            if timed_out:output += '\nProcess-group timeout; child processes terminated.\n'
        except OSError as ex:
            output=str(ex);code=-1
        elapsed=time.perf_counter()-t
        path.write_text('$ '+' '.join(args)+'\n'+output+f'\nexit={code}\nmeasured_wall_seconds={elapsed}\n')
        self.commands.append({'argv':args,'cwd':str(cwd),'exit':code,'measured_wall_seconds':elapsed,
                              'log':path.relative_to(ROOT).as_posix()})
        if code:raise AuditError(f'{label} failed with exit {code}; inspect {path.relative_to(ROOT)}')
        return output
    def checkout(self,url,rev,dest):
        if dest.exists():
            actual=self.run(['git','rev-parse','HEAD'],'existing_pin_'+dest.name,dest).strip()
            if actual!=rev:raise AuditError(f'{dest} is at {actual}, expected {rev}; not resetting it')
            self.clean_dependency(dest)
            return
        dest.mkdir(parents=True)
        self.run(['git','init'],'init_'+dest.name,dest)
        self.run(['git','remote','add','origin',url],'remote_'+dest.name,dest)
        self.run(['git','fetch','--depth=1','origin',rev],'fetch_'+dest.name,dest)
        self.run(['git','checkout','--detach','FETCH_HEAD'],'checkout_'+dest.name,dest)
        actual=self.run(['git','rev-parse','HEAD'],'new_pin_'+dest.name,dest).strip()
        if actual!=rev:raise AuditError('fetched revision does not match '+rev)
        self.clean_dependency(dest)
    def clean_dependency(self,dest):
        changed=self.run(['git','status','--porcelain','--untracked-files=all'],'clean_'+dest.name,dest)
        if changed.strip():raise AuditError('tracked or untracked dependency changes at '+str(dest))
        # Include ignored Lean source too; normal Lake build/cache trees are allowed.
        untracked=self.run(['git','ls-files','--others','-z','--','*.lean'],
                           'source_shadow_'+dest.name,dest)
        shadows=[p for p in untracked.split('\0') if p and not p.startswith('.lake/')]
        if shadows:raise AuditError('untracked dependency Lean source at '+str(dest)+': '+repr(shadows[:12]))
    def dependencies(self,bootstrap:bool,recheck:bool):
        lock=json.loads((ROOT/'lake-manifest.json').read_text())
        for package in lock['packages']:
            dest=ROOT/'.lake/packages'/package['name']
            if not dest.exists() and not bootstrap:
                raise AuditError('missing pinned dependency '+package['name']+'; run --bootstrap')
            self.checkout(package['url'],package['rev'],dest)
        if recheck:
            dest=ROOT/'.tools/lean4checker'
            if not dest.exists() and not bootstrap:raise AuditError('checker missing; run --bootstrap --recheck')
            self.checkout('https://github.com/leanprover/lean4checker.git',CHECKER_REV,dest)
            if (dest/'lean-toolchain').read_text().strip()!=(ROOT/'lean-toolchain').read_text().strip():
                raise AuditError('checker/compiler toolchain mismatch')
            self.run(['lake','build','lean4checker'],'build_rechecker',dest)

def self_test():
    scan_text('theorem sample : True := True.intro /- nested /- comment -/ -/')
    rejected=0
    for bad in ['theorem bad : False := by sorry','axiom bad : False',
                'theorem bad : True := by native_decide','set_option debug.skipKernelTC true']:
        try:scan_text(bad)
        except AuditError:rejected+=1
    if rejected!=4:raise AuditError('source rejection self-test failed')
    if parse_axioms("'T' depends on axioms: [propext, Classical.choice]",['T'])!={'T':['propext','Classical.choice']}:
        raise AuditError('positive parser control failed')
    badtexts=["'T' depends on axioms: [sorryAx]",'',"'T' does not depend on any axioms\n'T' does not depend on any axioms",
              "'U' does not depend on any axioms"]
    for text in badtexts:
        try:parse_axioms(text,['T'])
        except AuditError:continue
        raise AuditError('axiom-output rejection self-test failed')
    print(json.dumps({'status':'PYTHON_RUNNER_CONTROLS_PASSED','lean_invoked':False,
                      'source_rejection_controls':4,'axiom_output_rejection_controls':4},indent=2))

def protected_hashes():
    files=list((ROOT/'Kourovka').rglob('*.lean'))+[ROOT/'Kourovka.lean',ROOT/'lean-toolchain',
      ROOT/'lakefile.toml',ROOT/'lake-manifest.json',ROOT/'reference/source_inventory.json']
    files+=list((ROOT/'data').glob('*'))
    files+=list((ROOT/'scripts').glob('*.py'))+list((ROOT/'validation').glob('*.lean'))
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file()}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--milestones',action='store_true',help='compile/audit all CURRENT source; not the absent group theorem')
    ap.add_argument('--module',help='compile/audit just this module and imports; a debugging run only')
    ap.add_argument('--bootstrap',action='store_true',help='fetch missing exact dependency commits')
    ap.add_argument('--cache',action='store_true',help='fetch pinned mathlib cache; not a from-source dependency rebuild')
    ap.add_argument('--fresh',action='store_true',help='legacy full dependency rebuild request; unsupported by this bounded runner')
    ap.add_argument('--fresh-project',action='store_true',help='explicit fresh project compilation (the default); preserves pinned dependency objects')
    ap.add_argument('--recheck',action='store_true',help='run pinned lean4checker --fresh on the chosen module')
    ap.add_argument('--prepare-audit',action='store_true',help='refresh STATIC inventory and queries after intentional source edits; no Lean')
    ap.add_argument('--static-only',action='store_true',help='scan recursive source, imports and inventory; no Lean')
    ap.add_argument('--self-test',action='store_true',help='Python runner regression tests only; no Lean')
    ap.add_argument('--timeout',type=int,default=3600,help='timeout for each module or other command; kills its whole process group')
    args=ap.parse_args()
    if args.self_test:self_test();return 0
    if args.module and args.milestones:ap.error('use --module OR --milestones')
    if args.fresh:ap.error('--fresh previously requested a full dependency-source rebuild. This bounded runner does not implement that mode. Use --fresh-project for a fresh project-source check; pinned dependency objects are preserved.')
    if args.timeout<=0:ap.error('--timeout must be positive')
    runner=Runner(args.timeout)
    result={'complete_formalization':False,'final_group_theorem_present':False,
       'lean_build_started':False,'lean_build_succeeded':False,'axiom_audit_succeeded':False,
       'fresh_recheck_succeeded':False,'elaborated_statement_inspection_ran':False,'commands':runner.commands}
    try:
        inv=write_inventory(ROOT) if args.prepare_audit else inventory(ROOT)
        expected=json.loads((ROOT/'reference/source_inventory.json').read_text())
        if inv!=expected:raise AuditError('source inventory drift: inspect edits, then run --prepare-audit')
        result['static_scan']={'modules':len(inv['imports']),'named_query_roots':len(inv['named_declarations']),
          'all_modules_imported':True,'status':'STATIC_ONLY_NOT_PROOF'}
        if args.prepare_audit or args.static_only:
            result['status']='STATIC_ONLY_NOT_A_PROOF';return 0
        if not (args.module or args.milestones):
            result['status']='INCOMPLETE_FINAL_GROUP_THEOREM_ABSENT'
            raise AuditError('The unconditional group construction and theorem are absent. '
                             '--milestones checks all current draft source, not a final result.')
        mod=args.module or 'Kourovka'; selected=closure(inv,mod)
        result['selected_module']=mod;result['modules_in_selected_closure']=len(selected)
        for exe in ('lean','lake'):
            if shutil.which(exe) is None:
                result['status']='BLOCKED_NO_LEAN_TOOLCHAIN'
                raise AuditError(exe+' not on PATH; install Lean/Lake 4.19.0 offline')
        version=runner.run(['lean','--version'],'lean_version')
        if not re.search(r'\bversion 4\.19\.0\b',version):raise AuditError('wrong Lean version '+version.strip())
        runner.run(['lake','--version'],'lake_version')
        binary=Path(shutil.which('lean')).resolve()
        result['invoked_lean_path']=str(binary)
        result['invoked_lean_file_sha256']=hashlib.sha256(binary.read_bytes()).hexdigest()
        result['compiler_hash_note']='The PATH executable may be an elan shim; this is not independent compiler validation.'
        runner.dependencies(args.bootstrap,args.recheck)
        if args.cache:
            runner.run(['lake','exe','cache','get'],'pinned_mathlib_cache')
            result['used_mathlib_cache']=True
        result['source_dependency_rebuild_requested']=False
        result['fresh_project_compilation']=True
        before=protected_hashes()
        names=[d['name'] for d in inv['named_declarations'] if d['module'] in selected]
        queries=runner.dir/'queries';write_queries(queries,mod,names)
        result['lean_build_started']=True
        serial=build_serial(ROOT,mod,args.timeout)
        result['serial_build']=serial
        if not serial['all_selected_modules_passed']:
            raise AuditError('serial project build failed; inspect '+serial['log_directory'])
        if set(serial['selected_modules'])!=selected:
            raise AuditError('serial build closure differs from audited selection')
        result['lean_build_succeeded']=True
        output=runner.run(['lake','env','lean','-j1',str(queries/'AxiomAudit.lean')],'actual_axioms')
        result['actual_axiom_dependencies']=parse_axioms(output,names);result['axiom_audit_succeeded']=True
        runner.run(['lake','env','lean','-j1',str(queries/'Statements.lean')],'actual_elaborated_statements')
        result['elaborated_statement_inspection_ran']=True
        result['human_statement_fidelity_review']='still required; query output does not decide semantic agreement'
        if args.recheck:
            binary=ROOT/'.tools/lean4checker/.lake/build/bin/lean4checker'
            if not binary.exists():raise AuditError('missing built pinned rechecker')
            runner.run(['lake','env',str(binary),'--fresh',mod],'fresh_kernel_recheck')
            result['fresh_recheck_succeeded']=True
        if protected_hashes()!=before:raise AuditError('protected inputs changed during validation')
        # Recheck pins even if a dependency build script touched its checkout.
        runner.dependencies(False,False)
        result['status']='DRAFT_SOURCE_VALIDATION_PASSED_NOT_FINAL_GROUP_THEOREM'
        return 0
    except (AuditError,OSError,ValueError) as ex:
        result.setdefault('status','CHECK_FAILED');result['error']=str(ex);return 2
    finally:
        result['run_directory']=runner.dir.relative_to(ROOT).as_posix()
        text=json.dumps(result,indent=2)+'\n'
        (runner.dir/'result.json').write_text(text)
        (ROOT/'logs/latest_source_check.json').write_text(text)
        print(text)
if __name__=='__main__':sys.exit(main())
