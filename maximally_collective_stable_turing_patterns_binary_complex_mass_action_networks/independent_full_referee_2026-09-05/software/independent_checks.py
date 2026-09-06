"""Fresh symbolic checks and additional negative controls for the referee."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys
import sympy as s
import audit_driver as a

def exact_checks():
    sys.path.insert(0,str(a.SCRATCH/'full/independent_verifier'))
    import core, pareto_core as pc
    for m,L in ((3,s.Rational(2,3)),(7,s.Rational(3,5)),(11,s.Rational(1,2))):
        x=s.symbols('x:'+str(m+1))
        f=s.Matrix([1-x[0]*x[m-2]+x[m]**2-x[0]*x[m-1], -x[0]*x[1]+x[m-1]**2]+[x[0]*(x[i-1]-x[i]) for i in range(2,m-1)]+[2*x[0]*x[m-2]-2*x[m-1]**2+x[m]**2-x[0]*x[m-1], 2*x[0]*x[m-1]-2*x[m]**2])
        J=f.jacobian(x).subs(dict.fromkeys(x,s.Integer(1)))
        assert f.subs(dict.fromkeys(x,s.Integer(1)))==s.zeros(m+1,1)
        assert J==core.Avec(m)
        r,ds,ell=core.selected(m); D=s.diag(*ds)
        def hessian(u,v): return s.Matrix([(u.T*s.hessian(fi,x)*v)[0] for fi in f])
        assert hessian(r,r)==core.B(m,r,r)
        forcing=-hessian(r,r)/4
        cv=s.Matrix([0]+[4]*(m-2)+[2,1])
        augmented=J.col_join(cv.T)
        wzero=augmented.gauss_jordan_solve(forcing.col_join(s.Matrix([0])))[0]
        wtwo=(J-4*D).inv()*forcing
        assert wzero==core.w0(m)
        assert wtwo==core.w2(m)
        numerator=s.factor((ell.T*(hessian(r,wzero)+hessian(r,wtwo)/2))[0])
        assert numerator==core.N_formula(m,core.Hsum(m)) and numerator>0
        H=s.diag(*pc.Hlist(m,L)); rho=J.nullspace()[0]
        tau=s.factor(-(cv.T*H.inv()*wzero)[0]/(cv.T*H.inv()*rho)[0])
        scaledzero=wzero+tau*rho
        assert (cv.T*H.inv()*scaledzero)[0].simplify()==0
        assert J*scaledzero==forcing
        c=s.factor((ell.T*(hessian(r,scaledzero)+hessian(r,wtwo)/2))[0]/(ell.T*H.inv()*r)[0])
        expected=s.factor((pc.N0(m,pc.Hsum(m))+pc.tau_formula(m,pc.Hsum(m),L)*pc.Sterm(m,pc.Hsum(m)))/pc.den_formula(m,L))
        assert s.factor(c-expected)==0 and c<0
        print('DIRECT_POLYNOMIAL_JACOBIAN_HESSIAN_SOLVES_PASS',m,'L',L,'cubic_sign',s.sign(c))

def mutations():
    root=a.SCRATCH/'mutations'
    shutil.copytree(a.SOURCE/'public/repository',root,dirs_exist_ok=True)
    cases=[
        ('reaction_multiplicity','independent_verifier/common.py','vec({m-1:2})),','vec({m-1:3})),','verify_critical_profile.py'),
        ('diffusion_constant','independent_verifier/common.py','sp.Rational(23,63)','sp.Rational(24,63)','verify_critical_profile.py'),
        ('zero_mode_gauge','independent_verifier/common.py','sp.Rational(182448*m-373417,','sp.Rational(182448*m-373416,','verify_harmonic_corrections.py'),
        ('harmonic_recurrence','independent_verifier/verify_generic_cubic_recurrence.py','contraction0 + contraction2 / 2','contraction0 + contraction2 / 3','verify_generic_cubic_recurrence.py'),
        ('scaled_gauge','independent_verifier/pareto_core.py','return sp.factor(-top/bot)','return sp.factor(top/bot)','frontier_verify_normal_form.py'),
    ]
    for name,rel,old,new,entry in cases:
        p=root/rel; original=p.read_text(); assert old in original
        p.write_text(original.replace(old,new,1))
        try: assert a.run('mutation_'+name,['python',str(root/'independent_verifier'/entry),'3'] if entry=='frontier_verify_normal_form.py' else ['python',str(root/'independent_verifier'/entry)],root,expected=1)!=0
        finally: p.write_text(original)
    p=root/'independent_verifier/dd_verify_mode_isolation.py'; original=p.read_text()
    p.write_text("raise SystemExit(73)\n")
    try:
        assert a.run('mutation_wrapper_child_failure',['python','independent_verifier/verify_improved_profile.py'],root,expected=1)!=0
        assert 'IMPROVED_PROFILE_PASS' not in (a.LOGS/'mutation_wrapper_child_failure.log').read_text()
    finally: p.write_text(original)
    p=root/'data/current_profile_exact.json'; original=p.read_bytes(); payload=json.loads(original)
    payload['rows'][2]['eta']['exact']='1/10'; p.write_text(json.dumps(payload))
    try:
        assert a.run('mutation_numerical_source',['python','independent_verifier/verify_current_numerical_provenance.py'],root,expected=1)!=0
        # A fresh local self-hash must not repair a mismatching shipped baseline.
        (root/'verification_outputs/replay_self_consistency_manifest.txt').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  ./data/current_profile_exact.json\n')
        assert a.run('mutation_self_manifest',['sha256sum','-c','verification_outputs/replay_self_consistency_manifest.txt'],root)==0
        assert a.run('mutation_shipped_manifest',['sha256sum','-c','sha256_manifest.txt'],root,expected=1)!=0
    finally: p.write_bytes(original)
    print('INDEPENDENT_MUTATIONS_PASS')

def lock_controls():
    """Protocol-level shell tests only; stubs do not qualify an actual TeX build."""
    root=a.SCRATCH/'full'; base=(root/'environment/texlive-2022.04.lock.txt').read_text()
    fields=[line.split('|',1) for line in base.splitlines() if line and not line.startswith('#')]
    values=dict(fields)
    stub=a.SCRATCH/'lock_stubs'; stub.mkdir(exist_ok=True)
    engine='#!/bin/bash\nif [[ "${1:-}" == --version ]]; then printf "%s\\n" '+repr(values['ENGINE'])+'; else cp '+str(root/'environment/texlive-2022.04.lock.txt')+' "${1%.tex}.unused" 2>/dev/null || true; printf "%s\\n" '+repr('\n'.join(v for _,v in fields))+' > packages.log; cp packages.log standalone_probe.log; fi\n'
    # Last argument is the source filename; the checker needs only the two log files.
    for name,text in [('pdflatex',engine),('biber','#!/bin/bash\nprintf "%s\\n" '+repr(values['BIBER'])+'\n'),('kpsewhich','#!/bin/bash\nexit 0\n')]:
        p=stub/name;p.write_text(text);p.chmod(0o755)
    env=a.ENV.copy();env['PATH']=str(stub)+':'+env['PATH']
    assert a.run('lock_protocol_baseline',['bash','environment/check_toolchain.sh'],root,env=env)==0
    for name,value in fields:
        p=stub/'mutated.lock';p.write_text(base.replace(name+'|'+value,name+'|IMPOSSIBLE_REFEREE_VALUE',1));env['TOOLCHAIN_LOCK_FILE']=str(p)
        assert a.run('lock_protocol_mutation_'+name.replace('.','_'),['bash','environment/check_toolchain.sh','--quiet'],root,expected=2,env=env)!=0
    print('LOCK_PROTOCOL_ALL_FIELDS_REJECTED',len(fields),'ACTUAL_TEX_QUALIFICATION_NOT_CLAIMED')

if __name__=='__main__':
    {'exact':exact_checks,'mutations':mutations,'locks':lock_controls}[sys.argv[1]]()
