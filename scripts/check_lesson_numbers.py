"""Independent arithmetic checks against the displayed lesson answers."""
import math
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tmp" / "lesson-review" / "numerical-checks.json"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

checks = []
def check(topic, name, value, shown, tolerance):
    checks.append(dict(topic=topic, name=name, calculated=value, displayed=shown,
                       passed=abs(value-shown) <= tolerance))

sin = lambda d: math.sin(math.radians(d))
cos = lambda d: math.cos(math.radians(d))
tan = lambda d: math.tan(math.radians(d))
sqrt = math.sqrt
G = 9.81  # m/s², the value used in every lesson and exercise

for name, value, shown, tol in [
    ('km/h',72/3.6,20,.05),
    ('Fx',20*cos(35),16.4,.05), ('Fy',20*sin(35),11.5,.05),
    ('asymmetric mean',sum([12.40,12.41,12.41,12.43,12.45])/5,12.42,.005),
    ('maximum deviation',max(abs(x-12.42) for x in [12.40,12.41,12.41,12.43,12.45]),.03,.005),
    ('interval lower endpoint',12.42-.03,12.39,.005),
    ('interval upper endpoint',12.42+.03,12.45,.005),
    ('endpoint midpoint',(12.40+12.45)/2,12.425,.0005),
    ('endpoint semirange',(12.45-12.40)/2,.025,.0005),
    ('ruler relative uncertainty',.03/12.42,.0024,.00005),
    ('speed',1.2/2.36,.508,.0005),
    ('speed uncertainty',(1.2/2.36)*(.01/1.2+.04/2.36),.013,.0005),
    ('integral',3*2+2**2,10,1e-10), ('signed area',2*3-1*2,4,1e-10),
    ('polar angle',math.degrees(math.atan2(3,4)),36.9,.05),
    ('polar x',5*cos(36.9),4,.005), ('polar y',5*sin(36.9),3,.005),
    ('tool v0x',10*cos(30),8.66,.005), ('tool v0y',10*sin(30),5,.005),
    ('tool unit x',3/5,.6,1e-10), ('tool unit y',4/5,.8,1e-10),
    ('unit modulus',math.hypot(6,-8),10,1e-10),
    ('unit x',6/10,.6,1e-10), ('unit y',-8/10,-.8,1e-10),
    ('unit check',.6**2+.8**2,1,1e-10),
    ('sum by components wrong unit modulus',math.hypot(6/-2,-8/-2),5,1e-10),
    ('vector sum x',4-1,3,0), ('vector sum y',3+2,5,0),
    ('dot product',4*-1+3*2,2,0),
    ('cross x',1*2-(-1)*3,5,0), ('cross y',-(2*2-(-1)*1),-5,0),
    ('cross z',2*3-1*1,5,0), ('cross check',2*5+1*-5+(-1)*5,0,0),
    ('missing minus check',2*5+1*5+(-1)*5,10,0),
    *[(f'secant [2;{b}]',(b*b/4-1)/(b-2),shown,1e-9) for b,shown in
      [(4,1.5),(3,1.25),(2.5,1.125),(2.25,1.0625),(2.1,1.025),(2.01,1.0025)]],
    ('tangent slope t/2 at 2',2/2,1,0),
    *[(f'rod x({t})',2*t**3-9*t**2+12*t,shown,0) for t,shown in [(0,0),(1,5),(2,4),(3,9)]],
    *[(f'rod v({t})',6*t**2-18*t+12,0,0) for t in (1,2)],
    ('rod secant [0,9;1]',(5-(2*.9**3-9*.9**2+12*.9))/.1,.32,1e-9),
    ('rod secant [1;1,1]',((2*1.1**3-9*1.1**2+12*1.1)-5)/.1,-.28,1e-9),
    ('extremum f(0)',0**3-3*0**2,0,0), ('extremum f(2)',2**3-3*2**2,-4,0),
    ('integral tool',2**2/2,2,0),
]: check('T0',name,value,shown,tol)

for name, value, shown, tol in [
    ('mean velocity',(5-2)/6,.5,.0005), ('mean speed',(6+3)/6,1.5,.005),
    ('pass origin',12/5,2.4,.005), ('meeting',60/3,20,.05),
    ('meeting position',-20+2*20,20,.05), ('same direction meeting',60/(2-1),60,.05),
    ('no future meeting',60/(2-3),-60,.05),
    ('stop',12/3,4,.005), ('stop position',100+12*4-1.5*4**2,124,.5),
    ('return position',100+12*6-1.5*6**2,118,.5),
    ('read santo grial turn',8/4,2,1e-10), ('read santo grial position',4+8*2-2*2**2,12,1e-10),
    ('maximum height time',18/G,1.83,.005),
    ('maximum height',1.5+18*(18/G)-G/2*(18/G)**2,18.0,.05),
    ('ground time',(-18-sqrt(18**2+6*G/2))/-G,3.75,.005),
    ('ground negative root',(-18+sqrt(18**2+6*G/2))/-G,-.0815,.00005),
    ('impact velocity',18-G*(18+sqrt(18**2+6*G/2))/G,-18.8,.05),
    ('return to hand',36/G,3.67,.005),
    ('reaction distance',20*.8,16,.05), ('braking distance',20*4-2.5*4**2,40,.05),
    ('total stop position',16+20*4-2.5*4**2,56,.05), ('total stop time',.8+20/5,4.8,.005),
    ('double speed distance',40*.8+40**2/10,192,.5),
    ('table acceleration',2*(12-10),4,.005), ('table prediction',10+2*4**2,42,.05),
]: check('T1',name,value,shown,tol)

vx,vy=12*cos(35),12*sin(35)
vyw=10*sin(20)
th=sqrt(2*1.25/G)
for name,value,shown,tol in [
    ('crossing',42/1.4,30,.05), ('drift',.6*42/1.4,18,.05),
    ('swimmer speed',math.hypot(.6,1.4),1.52,.005),
    ('horizontal time',th,.505,.0005),
    ('horizontal range',3*th,1.51,.005),
    ('impact speed',math.hypot(3,G*th),5.79,.005),
    ('impact angle',math.degrees(math.atan2(G*th,3)),58.8,.05),
    ('oblique vx',vx,9.83,.005), ('oblique vy',vy,6.88,.005),
    ('oblique time',2*vy/G,1.40,.005), ('oblique range',vx*2*vy/G,13.8,.05),
    ('oblique height',vy**2/(2*G),2.41,.005),
    ('complementary range',400*sin(60)/G,35.3,.05),
    ('30 degrees time',2*20*sin(30)/G,2.04,.005),
    ('30 degrees height',(20*sin(30))**2/(2*G),5.10,.005),
    ('60 degrees time',2*20*sin(60)/G,3.53,.005),
    ('60 degrees height',(20*sin(60))**2/(2*G),15.3,.05),
    ('window impact',(vyw+sqrt(vyw**2+4*G/2*8))/G,1.67,.005),
    ('window negative root',(vyw-sqrt(vyw**2+4*G/2*8))/G,-.975,.0005),
    ('window range',10*cos(20)*(vyw+sqrt(vyw**2+4*G/2*8))/G,15.7,.05),
    ('window peak',8+vyw**2/(2*G),8.60,.005),
    ('window ascending',(vyw-sqrt(vyw**2-4*G/2*.4))/G,.149,.0005),
    ('window descending',(vyw+sqrt(vyw**2-4*G/2*.4))/G,.549,.0005),
    ('window x1',10*cos(20)*(vyw-sqrt(vyw**2-4*G/2*.4))/G,1.40,.005),
    ('window x2',10*cos(20)*(vyw+sqrt(vyw**2-4*G/2*.4))/G,5.16,.005),
    ('wheel omega',8*math.pi,25.1,.05), ('wheel speed',.35*8*math.pi,8.8,.005),
    ('wheel normal acceleration',.35*(8*math.pi)**2,221,.5),
    ('half radius acceleration',.175*(8*math.pi)**2,111,.5),
    ('angular stop turns',50/(2*math.pi),7.96,.005),
    ('angular acceleration magnitude at 2s',math.hypot(.8,.2*12**2),28.8,.05),
]: check('T2',name,value,shown,tol)

for name,value,shown,tol in [
    ('opposed forces',(3-1)/.25,8,.005),
    ('normal upward',2*G-10*sin(30),14.6,.05), ('normal downward',2*G+10*sin(30),24.6,.05),
    ('incline acceleration',G*sin(20),3.355,.0005),
    ('incline stop time',2.6/(G*sin(20)),.775,.0005),
    ('incline distance',2.6**2/(2*G*sin(20)),1.01,.005),
    ('incline height',2.6**2/(2*G),.345,.0005),
    ('descent acceleration',G*sin(30),4.91,.0051),
    ('descent time',sqrt(2*.6/(G*sin(30))),.495,.0005), ('descent speed',sqrt(2*G*sin(30)*.6),2.43,.005),
    ('pulley acceleration',.2*G/(.1+.2),6.54,.005),
    ('pulley tension',.1*.2*G/(.1+.2),.654,.0005),
    ('pulley normal',.1*G,.981,.0005),
    ('equal masses acceleration',.1*G/.2,4.91,.0051), ('equal masses tension',.1*.1*G/.2,.491,.0005),
    ('conical tension',.2*G/cos(30),2.27,.005),
    ('conical speed',sqrt(.5*G*tan(30)),1.68,.005),
]: check('T3',name,value,shown,tol)

for name,value,shown,tol in [
    ('normal',2*G,19.6,.05),
    ('static threshold',.4*2*G,7.85,.005), ('kinetic friction',.3*2*G,5.89,.005),
    ('kinetic acceleration',(7-.3*2*G)/2,.557,.0005),
    ('free deceleration',.3*G,2.94,.005), ('stop time',3/(.3*G),1.02,.005),
    ('stop distance',3**2/(2*.3*G),1.53,.005),
    ('incline weight parallel',.3*G*sin(25),1.24,.005),
    ('incline normal',.3*G*cos(25),2.67,.005),
    ('incline static max',.5*.3*G*cos(25),1.33,.005),
    ('incline kinetic friction',.35*.3*G*cos(25),.934,.0005),
    ('incline downhill acceleration',G*(sin(25)-.35*cos(25)),1.03,.005),
    ('incline uphill acceleration',G*(sin(25)+.35*cos(25)),7.26,.005),
    ('critical angle',math.degrees(math.atan(.5)),26.6,.05),
    ('flat curve',sqrt(.8*G*30),15.3,.05), ('banked curve',sqrt(30*G*tan(10)),7.20,.005),
    ('wet curve',sqrt(.5*G*30),12.1,.05),
    ('spring equilibrium',.2*G/100,.0196,.00005), ('spring acceleration',(.2*G-100*(.2*G/100+.01))/.2,-5,.005),
    ('pendulum fit',4*math.pi**2/4.015,9.83,.005),
    ('pendulum discrepancy',4*math.pi**2/4.015-G,.02,.005),
    ('spring fit',4*math.pi**2/11.7,3.37,.005), ('effective mass',.0664/11.7,.00568,.000005),
    ('squared period',.983**2,.966,.0005),
]: check('T4',name,value,shown,tol)

wf=8*6*cos(30)
wpush=-.3*(G+8*sin(30))*6
wpull=-.3*(G-8*sin(30))*6
for name,value,shown,tol in [
    ('applied work',wf,41.6,.05), ('pushing normal',G+8*sin(30),13.8,.05),
    ('pushing friction work',wpush,-24.9,.05),
    ('pushing speed',sqrt(2*(4.5+wf+wpush)),6.51,.005),
    ('pulling normal',G-8*sin(30),5.81,.005), ('pulling friction work',wpull,-10.5,.05),
    ('pulling speed',sqrt(2*(4.5+wf+wpull)),8.44,.005),
    ('variable force max kinetic',6*3-3**2,9,.005),
    ('variable force final speed',sqrt(6*4-4**2),2.83,.005),
    ('elevator useful power',50*G*.4,196,.5), ('elevator input energy',50*G*4/.8,2450,5),
    ('elevator useful energy',50*G*4,1960,5),
    ('throw kinetic',.5*.5*12**2,36,.05), ('throw potential at 5m',.5*G*5,24.5,.05),
    ('throw speed at 5m',sqrt(2*(36-.5*G*5)/.5),6.77,.005),
    ('throw peak',36/(.5*G),7.34,.005), ('reference shift',.5*G*2,9.81,.005),
    ('fall initial energy',1*G*10,98.1,.05),
    ('free fall kinetic at 4m',G*10-G*4,58.9,.05),
    ('resistance at 4m',G*10-2*(10-4)-G*4,46.9,.05),
    ('free fall final speed',sqrt(2*G*10),14.0,.05), ('resisted final speed',sqrt(2*(G*10-20)),12.5,.05),
    ('spring energy',.5*100*.2**2,2,.005), ('spring speed',sqrt(2*2/.5),2.83,.005),
    ('ramp height',2/(.5*G),.408,.0005), ('ramp 30 distance',2/(.5*G)/sin(30),.815,.0005),
    ('ramp 60 distance',2/(.5*G)/sin(60),.471,.0005),
    ('rough approach loss',.2*.5*G*.5,.491,.0005), ('rough approach height',(2-.2*.5*G*.5)/(.5*G),.308,.0005),
    ('system balance',4+18-12,10,.05), ('lifting work',2*G*3,58.9,.05),
]: check('T5',name,value,shown,tol)

def collision(m1,m2,u1,u2,e):
    p=m1*u1+m2*u2
    v1=(p-m2*e*(u1-u2))/(m1+m2)
    v2=v1+e*(u1-u2)
    return v1,v2,.5*m1*v1**2+.5*m2*v2**2
v1,v2,k=collision(.5,.3,4,-6,.4)
for name,value,shown,tol in [
    ('rebound impulse',.2*(5-(-10)),3,.005), ('short pulse average',3/.02,150,.5),
    ('long pulse average',3/.1,30,.05), ('short triangle area',.5*.02*300,3,.005),
    ('long triangle area',.5*.1*60,3,.005),
    ('plasticine kinetic final',.5*.75*(10/3)**2,4.17,.005),
    ('plasticine loss',12.5-.5*.75*(10/3)**2,8.33,.005),
    ('plasticine deceleration',.2*G,1.96,.005),
    ('plasticine stopping distance',(10/3)**2/(2*.2*G),2.83,.005),
    ('external impulse percentage',1.5*.01/2.5*100,.6,.0005),
    ('skater velocity',-60*2/40,-3,.005), ('skater energy',.5*60*2**2+.5*40*3**2,300,.5),
    ('collision v1',v1,-1.25,.005), ('collision v2',v2,2.75,.005),
    ('collision kinetic',k,1.525,.0005), ('collision loss',9.4-k,7.88,.0050001),
    ('adhesion speed',(.5*4+.3*-6)/.8,.25,.0005),
    ('adhesion energy',.5*.8*.25**2,.025,.00005),
]: check('T6',name,value,shown,tol)
for e, answers in [(0,(8,8,64)),(.5,(7,9,65)),(1,(6,10,68))]:
    for name,value,shown in zip(['v1','v2','energy'],collision(1,1,10,6,e),answers):
        check('T6',f'e={e} {name}',value,shown,1e-10)
for name,value,shown in zip(['v1','v2'],collision(1,4,10,6,1)[:2],(3.6,7.6)):
    check('T6','unequal elastic '+name,value,shown,1e-10)

OUTPUT.write_text(json.dumps(checks,indent=2),encoding='utf8')
failed=[c for c in checks if not c['passed']]
print(f'{len(checks)} numerical checks; {len(failed)} failures')
for item in failed: print(item)
assert not failed
