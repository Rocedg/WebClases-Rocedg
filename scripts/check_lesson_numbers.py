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

for name, value, shown, tol in [
    ('km/h',72/3.6,20,.05), ('density',.675/(250*1e-6),2700,5),
    ('Fx',20*cos(35),16.4,.05), ('Fy',20*sin(35),11.5,.05),
    ('displacement',math.hypot(30,40),50,.05),
    ('angle',math.degrees(math.atan2(40,30)),53.1,.05),
    ('mean',sum([12.41,12.43,12.42,12.44,12.40])/5,12.42,.005),
    ('semirange',(12.44-12.4)/2,.02,.005),
    ('asymmetric mean',sum([12.40,12.41,12.41,12.43,12.45])/5,12.42,.005),
    ('maximum deviation',max(abs(x-12.42) for x in [12.40,12.41,12.41,12.43,12.45]),.03,.005),
    ('interval lower endpoint',12.42-.03,12.39,.005),
    ('interval upper endpoint',12.42+.03,12.45,.005),
    ('endpoint midpoint',(12.40+12.45)/2,12.425,.0005),
    ('endpoint semirange',(12.45-12.40)/2,.025,.0005),
    ('relative uncertainty',.02/12.42,.00161,.000005),
    ('speed',1.2/2.36,.508,.0005),
    ('speed uncertainty',(1.2/2.36)*(.01/1.2+.04/2.36),.013,.0005),
    ('secant',((2+3*3+3**2)-(2+3*1+1**2))/2,7,1e-10),
    ('integral',3*2+2**2,10,1e-10), ('signed area',2*3-1*2,4,1e-10),
]: check('T0',name,value,shown,tol)

for name, value, shown, tol in [
    ('mean velocity',(5-2)/6,.5,.0005), ('mean speed',(6+3)/6,1.5,.005),
    ('pass origin',12/5,2.4,.005), ('meeting',60/3,20,.05),
    ('meeting position',-20+2*20,20,.05), ('same direction meeting',60/(2-1),60,.05),
    ('no future meeting',60/(2-3),-60,.05),
    ('stop',12/3,4,.005), ('stop position',100+12*4-1.5*4**2,124,.5),
    ('return position',100+12*6-1.5*6**2,118,.5),
    ('maximum height',1.5+18**2/20,17.7,.05),
    ('ground time',(18+sqrt(18**2+30))/10,3.68,.005),
    ('impact speed',sqrt(18**2+30),18.8,.05),
    ('reaction distance',20*.8,16,.05), ('braking distance',20**2/10,40,.05),
    ('double speed distance',40*.8+40**2/10,192,.5),
    ('table acceleration',2*(12-10),4,.005), ('table prediction',10+2*4**2,42,.05),
]: check('T1',name,value,shown,tol)

vx,vy=12*cos(35),12*sin(35)
vyw=10*sin(20)
for name,value,shown,tol in [
    ('crossing',42/1.4,30,.05), ('drift',.6*42/1.4,18,.05),
    ('swimmer speed',math.hypot(.6,1.4),1.52,.005),
    ('horizontal time',sqrt(2*1.25/10),.5,.0005),
    ('horizontal range',3*sqrt(2*1.25/10),1.5,.005),
    ('impact speed',math.hypot(3,5),5.83,.005),
    ('impact angle',math.degrees(math.atan2(5,3)),59,.05),
    ('oblique vx',vx,9.83,.005), ('oblique vy',vy,6.88,.005),
    ('oblique time',2*vy/10,1.38,.005), ('oblique range',vx*2*vy/10,13.5,.05),
    ('oblique height',vy**2/20,2.37,.005),
    ('complementary range',400*sin(60)/10,34.6,.05),
    ('60 degrees time',4*sin(60),3.46,.005),
    ('60 degrees height',(20*sin(60))**2/20,15,.05),
    ('window impact',(vyw+sqrt(vyw**2+160))/10,1.65,.005),
    ('window negative root',(vyw-sqrt(vyw**2+160))/10,-.968,.0005),
    ('window range',10*cos(20)*(vyw+sqrt(vyw**2+160))/10,15.5,.05),
    ('window peak',8+vyw**2/20,8.58,.005),
    ('window ascending',(vyw-sqrt(vyw**2-8))/10,.150,.0005),
    ('window descending',(vyw+sqrt(vyw**2-8))/10,.534,.0005),
    ('window x1',cos(20)*(vyw-sqrt(vyw**2-8)),1.41,.005),
    ('window x2',cos(20)*(vyw+sqrt(vyw**2-8)),5.02,.005),
    ('wheel omega',8*math.pi,25.1,.05), ('wheel speed',.35*8*math.pi,8.8,.005),
    ('wheel normal acceleration',.35*(8*math.pi)**2,221,.5),
    ('half radius acceleration',.175*(8*math.pi)**2,111,.5),
    ('angular stop turns',50/(2*math.pi),7.96,.005),
    ('angular acceleration magnitude at 2s',math.hypot(.8,.2*12**2),28.8,.05),
]: check('T2',name,value,shown,tol)

for name,value,shown,tol in [
    ('opposed forces',(3-1)/.25,8,.005),
    ('normal upward',20-10*sin(30),15,.05), ('normal downward',20+10*sin(30),25,.05),
    ('incline stop time',2.6/(10*sin(20)),.760,.0005),
    ('incline distance',2.6**2/(20*sin(20)),.988,.0005),
    ('incline height',2.6**2/20,.338,.0005),
    ('descent time',sqrt(2*.6/5),.490,.0005), ('descent speed',sqrt(2*5*.6),2.45,.005),
    ('pulley acceleration',.2*10/(.1+.2),6.67,.005),
    ('pulley tension',.1*.2*10/(.1+.2),.667,.0005),
    ('conical tension',.2*10/cos(30),2.31,.005),
    ('conical speed',sqrt(.5*10*tan(30)),1.7,.005),
]: check('T3',name,value,shown,tol)

for name,value,shown,tol in [
    ('static threshold',.4*2*10,8,.005), ('kinetic acceleration',(7-.3*20)/2,.5,.0005),
    ('stop distance',3**2/(2*3),1.5,.005),
    ('incline weight parallel',3*sin(25),1.27,.005),
    ('incline normal',3*cos(25),2.72,.005),
    ('incline static max',.5*3*cos(25),1.36,.005),
    ('incline kinetic friction',.35*3*cos(25),.952,.0005),
    ('incline downhill acceleration',10*(sin(25)-.35*cos(25)),1.05,.005),
    ('incline uphill acceleration',10*(sin(25)+.35*cos(25)),7.4,.005),
    ('critical angle',math.degrees(math.atan(.5)),26.6,.05),
    ('flat curve',sqrt(.8*10*30),15.5,.05), ('banked curve',sqrt(30*10*tan(10)),7.27,.005),
    ('wet curve',sqrt(.5*10*30),12.2,.05),
    ('spring equilibrium',.2*10/100,.02,.00005), ('spring acceleration',(2-100*.03)/.2,-5,.005),
    ('pendulum fit',4*math.pi**2/4.015,9.83,.005),
    ('spring fit',4*math.pi**2/11.7,3.37,.005), ('effective mass',.0664/11.7,.00568,.000005),
    ('squared period',.983**2,.966,.0005),
]: check('T4',name,value,shown,tol)

wf=8*6*cos(30)
for name,value,shown,tol in [
    ('applied work',wf,41.6,.05), ('pushing friction work',-.3*(10+8*sin(30))*6,-25.2,.05),
    ('pushing speed',sqrt(2*(4.5+wf-25.2)),6.46,.005),
    ('pulling speed',sqrt(2*(4.5+wf-10.8)),8.4,.005),
    ('variable force max kinetic',6*3-3**2,9,.005),
    ('variable force final speed',sqrt(6*4-4**2),2.83,.005),
    ('elevator useful power',50*10*.4,200,.5), ('elevator input energy',50*10*4/.8,2500,5),
    ('throw kinetic',.5*.5*12**2,36,.05), ('throw speed at 5m',sqrt(2*(36-25)/.5),6.63,.005),
    ('throw peak',36/(.5*10),7.2,.005),
    ('resistance at 4m',100-2*(10-4)-40,48,.05),
    ('free fall final speed',sqrt(200),14.1,.05), ('resisted final speed',sqrt(160),12.6,.05),
    ('spring energy',.5*100*.2**2,2,.005), ('spring speed',sqrt(2*2/.5),2.83,.005),
    ('ramp height',2/(.5*10),.4,.0005), ('ramp 30 distance',.4/sin(30),.8,.0005),
    ('ramp 60 distance',.4/sin(60),.462,.0005),
    ('rough approach loss',.2*.5*10*.5,.5,.0005), ('rough approach height',1.5/5,.3,.0005),
    ('system balance',4+18-12,10,.05), ('lifting work',2*10*3,60,.05),
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
    ('plasticine stopping distance',(10/3)**2/(2*.2*10),2.78,.005),
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
