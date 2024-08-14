from math import sqrt, ceil
from Crypto.Util.number import long_to_bytes

def baby_step_giant_step(a, b, p):
    k = (1<<50 -1)
    m = ceil(sqrt(k))
    
    babies = {}
    bs = 1

    for i in range(m): 
        print("bs: ", bs)
        babies[bs] = i
        bs = (bs*a) % p

    gs = b
    giant_step = pow(a,-m,p)

    for j in range(m):
        print("gs: ", gs)
        if gs in babies:
            return babies[gs] + j*m
        gs = (gs*giant_step) % p


p=21847359589888208475506724917162265063571401985325370367631361781114029653025956815157605328190411141044160689815741319381196532979871500038979862309158738250945118554961626824152307536605872616502884288878062467052777605227846709781850614792748458838951342204812601838112937805371782600380106020522884406452823818824455683982042882928183431194593189171431066371138510252979648513553078762584596147427456837289623008879364829477705183636149304120998948654278133874026711188494311770883514889363351380064520413459602696141353949407971810071848354127868725934057811052285511726070951954828625761984797831079801857828431

g=21744646143243216057020228551156208752703942887207308868664445275548674736620508732925764357515199547303283870847514971207187185912917434889899462163342116463504651187567271577773370136574456671482796328194698430314464307239426297609039182878000113673163760381575629928593038563536234958563213385495445541911168414741250494418615704883548296728080545795859843320405072472266753448906714605637308642468422898558630812487636188819677130134963833040948411243908028200183454403067866539747291394732970142401544187137624428138444276721310399530477238861596789940953323090393313600101710523922727140772179016720953265564666

h=2379943664994463434447180799986543062713483099464815442605819358024518874205912039079297734838557301077499485690715187242732637166621861199722810552790750351063910501376656279916109818380142480153541630024844375987866909360327482454547879833328229210199064615160934199590056906292770813436916890557374599901608776771002737638288892742464424376302165637115904125111643815237390808049788607647462153922322177386615212924778476029834861337534317344050414511899408665633738083462745720713477559240135989896733710248600757926137849819921071458210373753356840504150106675895043640641251817448597517740418989043930823670446

a=6384201945364259416484618556230682430992417498764575739869190272523735481484018572812468821955378599176918034272111105002324791003253919162436622535453745408437647881572386470941971475251078850286304439754861599469147475492519769292883229128057869632295023589669156129147001420291798187153143127735238126939728677098865317467404967501011186234614072662215754693860629617912797573819290964731520795401609222935030001060869435851177399452933354698474411159337923418076284460501174419894324660021273635203791996633586742144073352269865971941687673123777993188268979508244658784407075950581524330447222535111673938658510

c=71778295986317464977181358951733941026818952858286003634564124680358033840379585505943440223381732309059767994475589178857749561223221520781996969649457324093122032073466344010212086647833256617483980995376446966096288489787358374855411062932987688832004337428232104632177155706591924834977564049130435850596

t=9312646501987776677123069996165334953320238908514227830892894577967066010696080028032345464092038552178334908514757885668168857837159455619655708977528533978424087822692334952394425457616804123105906796449332890016607809976150608314165053890213678247959214214602749195694451747310100020199660344584515222600627105504679940926315507796335602231758745928978650450797822806071056984134

r = baby_step_giant_step(g,a,p)

x = (t-r)%p
x *= pow(c,-1,p)

print(x)

print(long_to_bytes(x))