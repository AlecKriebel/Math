"""New six-labelled-subset reconstruction from the manuscript's atomic rules.
No deposited program, formula module, certificate or result file is imported.
"""
import json, sympy as s, sys, time

def need(ok,tag):
    if not ok:raise ValueError(tag)

def solve_triangle(weights,r,rule):
    degree=[sum(row) for row in weights];states=list(range(1,7));idx={a:i for i,a in enumerate(states)}
    A=s.zeros(6);b=s.zeros(6,1)
    for state in states:
        i=idx[state];fitness=[r if state>>u&1 else s.Integer(1) for u in range(3)]
        for v in range(3):
            mutant=bool(state>>v&1)
            if rule=='Bd':
                rate=sum(fitness[u]*weights[u][v]/degree[u] for u in range(3) if bool(state>>u&1)!=mutant)
            else:
                den=sum(fitness[u]*weights[u][v] for u in range(3))
                rate=sum(fitness[u]*weights[u][v] for u in range(3) if bool(state>>u&1)!=mutant)/den
            rate=s.cancel(rate);other=state^(1<<v);A[i,i]+=rate
            if other==7:b[i]+=rate
            elif other:A[i,idx[other]]-=rate
    h=A.inv(method='DM')*b;h=[s.cancel(x) for x in h]
    residual=A*s.Matrix(h)-b
    need(all(s.cancel(x)==0 for x in residual),rule+':six_harmonic_equations')
    return [h[idx[1<<v]] for v in range(3)]

def main():
    start=time.monotonic();r,d=s.symbols('r delta',positive=True);zero=s.Integer(0)
    weights=[[zero,d,s.Integer(1)],[d,zero,d],[s.Integer(1),d,zero]]
    D=9*r**2+d*(12*r**4+24*r**3+15*r**2+24*r+12)+d**2*(16*r**4+52*r**3+83*r**2+52*r+16)+d**3*(4*r**4+12*r**3+13*r**2+12*r+4)
    expected_B=r**2*(3+d*(12*r**2+12*r+5)+d**2*(16*r**2+36*r+21)+d**3*(4*r**2+8*r+3))/D
    expected_D=2*r*(r+1+d*(3*r**2+3*r+1)+d**2*(5*r+1))/(3*(r+1)*(2*r+d*(3*r**2+r+3)+6*d**2*r))
    expected_Y=3*(3*r**2+d*(5*r**2+12*r+12)+d**2*(21*r**2+36*r+16)+d**3*(3*r**2+8*r+4))/D
    expected_I=(2*r**2+3*r+1+d*(3*r**2+7*r+5)+d**2*(r**2+8*r))/((1+d)*(r+1)*(2*r+d*(3*r**2+r+3)+6*d**2*r))
    expected_forward=r*(r**2+3*r+2+d*(5*r**2+7*r+3)+d**2*(8*r+1))/((1+d)*(r+1)*(2*r+d*(3*r**2+r+3)+6*d**2*r))
    out={'independent_atomic_rule_reconstruction':True,'all_six_states_retained':True,'rules':{}}
    for rule in ['Bd','dB']:
        f=solve_triangle(weights,r,rule);beta=[s.cancel(x.subs(r,1/r)) for x in f];degree=[1+d,2*d,1+d]
        alpha=s.cancel(sum(f)/3);weighted=s.cancel(sum(f[v]/degree[v] for v in range(3)));invweighted=s.cancel(sum(beta[v]/degree[v] for v in range(3)))
        expected=expected_B if rule=='Bd' else expected_D
        need(s.cancel(alpha-expected)==0,rule+':displayed_alpha')
        need(s.limit(alpha,d,0)==s.Rational(1,3),rule+':singular_alpha')
        need(s.cancel(alpha.subs(r,1)-s.Rational(1,3))==0,rule+':neutral_uniform_control')
        if rule=='Bd':need(s.cancel(sum(beta)-expected_Y)==0,'Bd:resident_sum');need(s.limit(sum(f),d,0)==1,'Bd:forward_sum')
        else:need(s.cancel(invweighted-expected_I)==0,'dB:resident_inverse_degree');need(s.cancel(weighted-expected_forward)==0,'dB:forward_inverse_degree')
        wrong=expected+d/(r+1);need(s.cancel(alpha-wrong)!=0,rule+':altered_identity_rejected')
        out['rules'][rule]={'singleton_fixations':[str(x) for x in f],'uniform_fixation':str(alpha),'forward_inverse_degree_sum':str(weighted),'resident_inverse_degree_sum':str(invweighted),'singular_uniform_limit':'1/3','displayed_identities_match':True,'neutral_control':True,'altered_identity_rejected':True}
    rr=s.Rational(3,2);p=1-1/rr;I=s.limit(expected_I,d,0);C_B=(rr-1)/2;C_D=3*rr*(rr-1)/I
    need(C_B==s.Rational(1,4) and C_D==s.Rational(27,16),'endpoint_first_stage_constants')
    module_B=-p/C_B;module_D=-p/C_D;graph_D=module_D-p/3;baseline_D=-p/3
    need(module_B==-s.Rational(4,3) and graph_D-baseline_D==-s.Rational(16,81),'endpoint_differences')
    out['endpoint']={'first_stage_constants':[str(C_B),str(C_D)],'module_start_coefficients':[str(module_B),str(module_D)],'dB_graph_coefficient':str(graph_D),'dB_complete_coefficient':str(baseline_D),'dB_difference':str(graph_D-baseline_D)}
    out['elapsed_seconds']=round(time.monotonic()-start,3);print(json.dumps(out,indent=2))

if __name__=='__main__':main()
