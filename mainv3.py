import display
import utime
import math
#import ray

import sys
import random
b=65535
ch,cm=0,0
lcd = display.LCD_1inch28()
lcd.set_bl_pwm(b)
old=0,0
#Pinout:
#leftmost is vcc
#second leftmost is gp17
#second rightmost is gp16
#rightmost is gnd
"""z
radius=1
i=0
while radius<121:
    lcd.ellipse(120,120,radius+i*2,radius+i*2,random.randint(0,65000))
    lcd.ellipse(120,120,radius+i*4,radius+i*4,random.randint(0,65000))
    lcd.ellipse(120,120,radius,radius,0xffff,1)
    radius+=int(i/3)
    i+=1
    lcd.show()



lcd.write_text('Neil.M',120-48,120-8,2,0)
lcd.show()
utime.sleep(2)
"""
Touch=display.Touch_CST816T(mode=1,LCD=lcd)
Touch.Flgh = 0
Touch.Flag = 0
Touch.Mode = 1
Touch.Set_Mode(Touch.Mode)
Touch.tim.init(period=10, callback=Touch.Timer_callback)
def to_color(red, green, blue):
        brightness = 1.0
        
        # Convert from 8-bit colors for red, green, and blue to 5-bit for blue and red and 6-bit for green.
        b = int((blue / 255.0) * (2 ** 5 - 1) * brightness)
        r = int((red / 255.0) * (2 ** 5 - 1) * brightness)
        g = int((green / 255.0) * (2 ** 6 - 1) * brightness)
        
        # Shift the 5-bit blue and red to take the correct bit positions in the final color value
        bs = b << 8
        rs = r << 3
        
        # Shift the 6-bit green value, properly handling the 3 bits that overlflow to the beginning of the value
        g_high = g >> 3
        g_low = (g & 0b000111) << 13
        
        gs = g_high + g_low
        
        # Combine together the red, green, and blue values into a single color value
        color = bs + rs + gs
        
        return color

def rotate(radius,angle,x,y):
	x=round(x+radius*math.sin(math.radians(angle)))

	y=round(y-radius*math.cos(math.radians(angle)))
	return x,y
def lp():
    for i in range(0,10):
        t=touch()
        if t==None:
            return
        else:
            utime.sleep(.1)
    return True
pp,ppp=0,0
var1,var2=0,0
def touch():
    global pp,ppp
    x,y=pp,ppp
    if Touch.Flgh == 0 and Touch.X_point != 0:
        Touch.Flgh = 1
        x = Touch.X_point
        y = Touch.Y_point
        
    if Touch.Flag == 1:
       
        color = 0
        Touch.Flgh = 0
        Touch.Flag = 0
        Touch.Mode = 1
        Touch.Set_Mode(Touch.Mode)
        Touch.tim.init(period=10, callback=Touch.Timer_callback)
        
        pp,ppp=x,y
        if x!=0 and y!=0:
            
            return x,y,True
def touch1():
        global var1,var2,old
        x,y=var1,var2
        if Touch.Flgh == 0 and Touch.X_point != 0:
            Touch.Flgh = 1
            x = Touch.X_point
            y = Touch.Y_point
            
        if Touch.Flag == 1:
           
            color = 0
            Touch.Flgh = 0
            Touch.Flag = 0
            Touch.Mode = 1
            Touch.Set_Mode(Touch.Mode)
            Touch.tim.init(period=10, callback=Touch.Timer_callback)
            
            var1,var2=x,y
            if x!=0 and y!=0 and x!=old[0] and y!=old[1]:
                old=x,y
                return x,y,True
def gesture():
    global old
    
    points=[]
    for i in range(0,3):
        t=touch()
        
        if t==None:
            return None
        else:
            string=[t[0],t[1]]
            
            points.append(string)
        
        utime.sleep(.05)
    spx=points[1][0]
    epx=points[-1][0]
    spy=points[1][1]
    epy=points[-1][1]
    old=epx,epy
    if epx>spx+15:
        return 'RIGHT'
    if epx<spx-15:
        return 'LEFT'
    if epy>spy+15:
        return 'DOWN'
    if epy<spy-15:
        return 'UP'
   
on=True
timervar=False
current_time=0

timerlength=0
def line(x,y,x1,y1,size,color):
    size=round(size/2)
    try:
        slope=float((y1-y)/(x1-x))
    except ZeroDivisionError:
        num,num1=y,y1
        
        if y1<y:
            num1,num=y,y1
            
        lcd.fill_rect(x-size,num,size*2,num1-num,color)
    num,num1=x,x1
    num2=1
    if x1<x:
        num1,num=x,x1
        num2=-1
    for i in range(0,(num1-num)*10):
        i1=i/10*num2
        lcd.ellipse(round(i1+x),round(y+i1*slope),size,size,color,1)
    
"""
def sc():
    
    utime.sleep(.1)
    chars=[
            '!',
            '@',
            '#',
            '$',
            '%',
            '^',
            '&',
            '*',
            '(',
            ')',
            '=',
            '+',
            'a',
            'b',
            'c',
            'd',
            '?',
            '>',
            '-',
            ':',
            ';',
            
            
            ]

    
    lcd.fill(0)
    lcd.show()
    while True:
        num=random.randint(0,30)
        color=0
        location=0
        if touch():
            return
        for o in range(0,240,10):
            location=o
            if o<num:
                    color+=1
            for i in range(0,240,10):
                if i<num:
                    color+=1
                lcd.fill_rect(i-1,location-1,10,10,0)
                lcd.text(chars[random.randint(0,len(chars)-1)],i,location,color)
                
                
            lcd.show()
sc()
"""
z,oldz=0,0
def main():
    
    global on,b,ch,cm,timervar,timerlength,current_time
    c=to_color(50,0,0)
    
    def background():
            lcd.fill(0)
            
            radius=110
            angle=0
            for i in range(0,120):
                x,y=rotate(radius,angle,120,120)
                x1,y1=rotate(radius+10,angle,120,120)
                #lcd.ellipse(x,y,3,3,0x7E0,1)
                lcd.line(x,y,x1,y1,to_color(50,50,50))
                if i%10==0:
                    line(x,y,x1,y1,3,0xffff)
                angle+=3
        
            
    
    
    while True:
        
        if on==False:
            
            try:
                if lp():
                    lcd.set_bl_pwm(b)
                    on=True
                    continue
                lcd.fill(0)
                lcd.show()
                lcd.set_bl_pwm(0)
                continue
            except KeyboardInterrupt:
                exit()
            except:
                continue
        to = touch()
        if to!=None:
            
            if to[0]>190:
                to=touch()
                utime.sleep(.1)
                app_screen()
        if on==True:
            background()
            t=utime.localtime()
            if ch==0 and cm==0:
                h,m,s=t[3],t[4],t[5]
            else:
                h,m,s=abs(t[3]+ch),t[4]+cm,t[5]
                if h==24:
                    h-=24
                if m==60:
                    m-=60
                    h+=1
            """
            if timervar==True:
                
                eh,em,es=current_time[3],current_time[4],current_time[5]
                es+=timer_length
                
                f=es%60
                em=em+(es/60-f/60)
                
                
           
                f1=em%60
                eh=eh+round(em/60-f1/60)
                em=f1
                es=f
                rh,rm,rs=int(eh-h),int(em-m),int(es-s)
                if rs<0:
                    rs+=60
                    rm-=1
                string1 = 'Timer:'+str(rh)+':'+str(rm)+':'+str(rs)
                lcd.write_text(string1,int(120-len(string1)*8),74,2,0xffff)
                
                if eh==h and em==m and es==s:
                    import Buzzer_song
                    lcd.fill(0xffff)
                    lcd.show()
                    utime.sleep(2)

                    timervar=False
                print(timer_length,eh,em,es)
            """
            angle1=s*6
            angle2=m*6
            angle3=h*30+(0.5*m)
            #sx,sy=rotate(20,angle1,120,90)
            sx,sy=rotate(110,angle1,120,120)
            mx,my=rotate(90,angle2,120,120)
            hx,hy=rotate(70,angle3,120,120)
            
            line(120,120,sx,sy,2,0x07e0)
            line(120,120,mx,my,5,0xffff)
            line(120,120,hx,hy,5,0xffff)
            lcd.ellipse(120,120,6,6,0,1)
            lcd.ellipse(120,120,6,6,0xffff)
            lcd.ellipse(120,120,3,3,0x07e0)
            string = str(h)+':'+str(m)+':'+str(s)
            lcd.write_text(string,int(120-len(string)*8),180,2,0xffff)
            lcd.text('Made by Neil.M',63,200,0xffff)
            #compass()
            lcd.show()
points=[]
size=20
"""
def graphingcal():
    global points,size
    size=20
    
   
    def bg():
        lcd.fill(0xffff)
        lcd.rect(20,20,200,200,0)
        for i in range(0,200,size):
      
            lcd.text(str(int(i/size)),20+i,220,0)
            lcd.line(20+i,220,20+i,20,0)
            lcd.text(str(int((200/size)-i/size)),12,16+i,0)
            lcd.line(20,20+i,220,20+i,0)
    x_points=[]
    y_points=[]
    for i in range(0,200):
        l=[i,20+size*i]
        x_points.append(l)
    for i in range(0,200):
        l=[(200/size)-i,20+size*i]
        y_points.append(l)
    
    
    bg()
    lcd.show()
    
    while True:
        bg()
        t=touch()
        
        if t==None:
            continue
        for i in range(0,len(x_points)):
            p=x_points[i]
        
            if t[0]>=p[1]-size/2 and t[0]<=p[1]+size/2:
                for i in range(0,len(y_points)):
               
                    p1=y_points[i]
                    if t[1]>=p1[1]-size/2 and t[1]<=p1[1]+size/2:
                        #print(p[0],p1[0])
                        points.append([p[0],p1[0],p[1],p1[1]])
                        lcd.ellipse(p[1],p1[1],10,10,0,1)
                        lcd.show()
    
    while True:
        bg()
        lcd.show()
        g=gesture()
        if g=='UP':
            size+=5
            bg()
        if g=='DOWN':
            if size>5:
                size-=5
            bg()
        if g=='LEFT':
            lcd.fill(0xffff)
            lcd.rect(20,20,200,30,0)
            lcd.text('Graph with Equation',52,32,0)
        
            
         
            lcd.show()
            t=touch()
            while True:
                t=touch()
                utime.sleep(.1)
                #print(t)
                if t==None:
                    continue
                if t[0]>=20 and t[0]<=220 and t[1]>=20 and t[1]<=50:
                    colors=[0x7e0,0x001f,0xf800]
                    color=0x0000
                    buttons=['0',
                             '1',
                             '2',
                             '3',
                             '4',
                             '5',
                             '6',
                             '7',
                             '8',
                             '9',
                             '*',
                             '-',
                             '/',
                             '+',
                             'x',
                             '.',
                             'cls',
                             'GRAPH'
                             ]
                    lcd.fill(0xffff)
                    lcd.rect(50,20,137,200,color)
                    lcd.show()
                    x,y=50,55
                    b_info=[]
                    for i in range(0,len(buttons)):
                        l=[buttons[i],x,y]
                        b_info.append(l)
                        lcd.rect(x,y,46,25,color)
                        lcd.text(buttons[i],x+(23-int((len(buttons[i])*8)/2)),y+10,color)
                        lcd.show()
                        x+=46
                        if x>=188:
                            x=50
                            y+=25
                    string='y='
                    n=0
                    while True:
                        lcd.fill_rect(51,21,135,33,0xffff)
                        string=string.replace('^','**')
                        t=touch1()
                        lcd.text(string,50,22,color)
                        lcd.show()
                        if t!=None:
                            for i in range(0,len(b_info)):
                                a=b_info[i]
                                if t[0]>=a[1] and t[0]<=a[1]+46 and t[1]>=a[2] and t[1]<=a[2]+25:
                                    lcd.fill_rect(a[1],a[2],46,25,color)
                                    lcd.text(a[0],a[1]+(23-int((len(a[0])*8)/2)),a[2]+10,0xffff)
                                    lcd.show()
                                    
                                    utime.sleep(.05)
                                    lcd.fill_rect(a[1],a[2],46,25,0xffff)
                                    lcd.rect(a[1],a[2],46,25,color)
                                    lcd.text(a[0],a[1]+(23-int((len(a[0])*8)/2)),a[2]+10,color)
                                    lcd.show()
                                    n+=1
                                    if a[0]=='cls':
                                        string='y='
                                        break
                                    if a[0]=='GRAPH':
                                        bg()
                                        equation=string
                                        equation=equation.replace('y=','')
                                        old_x,old_y=0,0
                                        for i in range(0,200/size):
                                            
                                            equation1=equation.replace('x',str(i))
                                            x_p,y_p=i,eval(equation1)
                                            x_pixel,y_pixel=x_p*size+20,220-y_p*size
                                            if y_pixel<=-200:
                                                break
                                            radius=3
                                            if size<10:
                                                radius=int(size/2)
                                            lcd.ellipse(int(x_pixel),int(y_pixel),radius,radius,1,1)
                                            if i>0:
                                                lcd.line(int(old_x),int(old_y),int(x_pixel),int(y_pixel),0x000)
                                                lcd.show()
                                            old_x,old_y=x_pixel,y_pixel
                                            lcd.show()
                                            #print(x_p,y_p,x_pixel,y_pixel)
                                            utime.sleep(.1)
                                        lcd.show()
                                        utime.sleep(5)
                                        return 
                                        
                                    string+=a[0]
                                    
                                    break
                        
                        utime.sleep(.05)
                if t[0]>=20 and t[0]<=220 and t[1]>=125 and t[1]<=155:
                    
                    break
                
        utime.sleep(.1)
"""
def mindfullness():
    global b
    lcd.fill(0)
    lcd.text('Focus on your breathing',20,110,6422)
    lcd.show()
    for i in range(0,1):
        for i in range(0,65535):
            b-=1
            lcd.set_bl_pwm(b)
        for i in range(0,65535):
            b+=1
            lcd.set_bl_pwm(b)
    for o in range(0,10):
        
        r = 0
        lcd.fill(0)
        lcd.text('Breath in',80,20,0xf800)
        for i in range(0,100):
            r+=1
            lcd.ellipse(120,120,r,r,6422)
            lcd.show()
            #time.sleep(.1)
        r = 120
        
        lcd.text('Breath in',80,20,0)
        lcd.text('Breath out',70,20,0xf800)
        lcd.show()
        for i in range(0,100):
            lcd.text('Breath out',70,20,0xf800)
            r-=1
            lcd.ellipse(120,120,r,r,0)
            lcd.show()
def calculator():
    
    lcd.fill(0)
    lcd.fill_rect(6,112,32,32,0x7e0)
    lcd.rect(6,112,32,32,0xffff)
    lcd.text('X',18,124,0xffff)
    colors=[0x7e0,0x001f,0xf800]
    color=colors[random.randint(0,2)]
    
    t=touch1()
    buttons=['0',
             '1',
             '2',
             '3',
             '4',
             '5',
             '6',
             '7',
             '8',
             '9',
             '*',
             '-',
             '/',
             '+',
             'cls'
             ]
    
    lcd.rect(50,20,137,200,color)
    lcd.show()
    x,y=50,55
    b_info=[]
    for i in range(0,len(buttons)):
        l=[buttons[i],x,y]
        b_info.append(l)
        lcd.rect(x,y,46,33,color)
        lcd.text(buttons[i],x+(23-int((len(buttons[i])*8)/2)),y+16,color)
        lcd.show()
        x+=46
        if x>=188:
            x=50
            y+=33
    string='0'
    n=0
    while True:
        
        string1=string.replace('^','**')
       
      
        try:
            str2='='+str(eval(string1))
        except KeyboardInterrupt:
            exit()
        except:
            pass
        lcd.fill_rect(51,21,135,33,0)
        lcd.text(string,50,22,color)
        lcd.text(str2,70+len(string)*8,22,color)
        lcd.show()
        t=touch1()
        
        if t!=None:
            for i in range(0,len(b_info)):
                a=b_info[i]
                if t[0]>=6 and t[0]<=38 and t[1]>=112 and t[1]<=144:
                    return 
                if t[0]>=a[1] and t[0]<=a[1]+46 and t[1]>=a[2] and t[1]<=a[2]+33:
                    lcd.fill_rect(a[1],a[2],46,33,color)
                    lcd.text(a[0],a[1]+(23-int((len(a[0])*8)/2)),a[2]+16,0)
                    lcd.show()
                    
                    utime.sleep(.1)
                    lcd.fill_rect(a[1],a[2],46,33,0)
                    lcd.rect(a[1],a[2],46,33,color)
                    lcd.text(a[0],a[1]+(23-int((len(a[0])*8)/2)),a[2]+16,color)
                    lcd.show()
                    n+=1
                    if a[0]=='cls':
                        string='0'
                        break
                    string+=a[0]
                    break
                
p1=[]
def clock():
    def time_change_main():
        points=[]
        p1=[]
        def bg():
            global p1
            lcd.fill(0)
       
            radius=110
            angle=0
            for i in range(0,60):
                x,y=rotate(radius,angle,120,120)

                lcd.ellipse(x,y,3,3,0x7E0,1)
                
                if i%5==0:
                    p1.append([x,y,i])
                    lcd.ellipse(x,y,6,6,0xffff,5)
                    lcd.ellipse(x,y,4,4,0x7E0,4)
                angle+=6
                points.append([x,y,i])
        
        def bg1():
            lcd.fill(0)
       
            radius=110
            angle=0
            for i in range(0,60):
                x,y=rotate(radius,angle,120,120)

                lcd.ellipse(x,y,3,3,0x7E0,1)
                
                if i%5==0:
                    lcd.ellipse(x,y,6,6,0xffff,5)
                    lcd.ellipse(x,y,4,4,0x7E0,4)
                angle+=6
                
        def time_change():
            global p1
            global ch,cm
            bg()
            lcd.show()
            a=0
            z=True
            s=True
            z1=True
            #print(p1)
            while z:
                bg1()
                lcd.ellipse(120,120,10,10,0xffff,1)
               
                t=touch()
                
                if t!=None:
                
                    for i in range(0,60):
                        if t[0]>=points[i][0]-6 and t[0]<=points[i][0]+6 and t[1]>=points[i][1]-6 and t[1]<=points[i][1]+6:
                            lcd.line(120,120,points[i][0],points[i][1],0x07e0)
                            lcd.ellipse(120,120,10,10,0xffff,1)
                            m1=points[i][2]
                            lcd.fill_rect(60,138,116,32,0x001f)
                            lcd.write_text('Min: '+str(m1),120-56,150,2,0xffff)
                            lcd.show()
                        if t[0]>=60 and t[0]<=176 and t[1]>=138 and t[1]<=170:
                            t=utime.localtime()
                            m=t[4]+cm
                            cm=m1-m
                            z=False
                            utime.sleep(.2)
                            break
            t=touch()
            utime.sleep(.1)
            t=touch()
            #print(t)
            z=True
            h1=0
            bg1()
            lcd.show()
            w=1
            while z:
                bg1()
                lcd.ellipse(120,120,10,10,0xffff,1)
        
                t1=touch()
                
                if t1!=None:
                
                    for i in range(0,12):
                        if t1[0]>=p1[i][0]-6 and t1[0]<=p1[i][0]+6 and t1[1]>=p1[i][1]-6 and t1[1]<=p1[i][1]+6:
                            lcd.line(120,120,p1[i][0],p1[i][1],0xf800)
                            lcd.ellipse(120,120,10,10,0xffff,1)
                            h1=p1[i][2]
                            h1/=5
                            h1=int(h1)
                            lcd.fill_rect(60,70,116,32,0x001f)
                            lcd.write_text('Hour: '+str(h1),64,74,2,0xffff)
                            lcd.show()
                        if t1[0]>=60 and t1[0]<=176 and t1[1]>=74 and t1[1]<=106:
                           
                            tim=utime.localtime()
                            h=tim[3]+ch
                            
                            dif=h-h1
                            ch=-1*(abs(dif))
                            utime.sleep(.2)
                            print(ch)
                            print(h,h1)
                            z=False
                            break
                
                
            
            
                            
            utime.sleep(.1)
        time_change()
        main()
    def timer():
        global timervar, timer_length,current_time
        lcd.fill(0)
        th=tm=ts=0
        pos=[]
        while True:
      
            lcd.fill(0)
            th1,tm1,ts1=th-1,tm-1,ts-1
            if th1<0:
                th1=' '
            if tm1<0:
                tm1=' '
            if ts1<0:
                ts1=' '
            lcd.write_text(str(str(th1)+':'+str(tm1)+':'+str(ts1)),int(120-(len(str(th1))+len(str(tm1))+len(str(ts1))+2)/2*24),112-30,3,36122)
            lcd.write_text(str(str(th)+':'+str(tm)+':'+str(ts)),int(120-(len(str(th))+len(str(tm))+len(str(ts))+2)/2*24),112,3,0xffff)
            lcd.write_text(str(str(th+1)+':'+str(tm+1)+':'+str(ts+1)),int(120-(len(str(th+1))+len(str(tm+1))+len(str(ts+1))+2)/2*24),112+30,3,36122)
            
            
            
            t=touch()
            z1=True
            if t!=None:
                points=[]
                if t[0]>=120-((len(str(tm))*12+len(str(th))*24)+24) and t[0]<=(120-len(str(tm))*12)-24:
                    
                    th=round(t[1]/5)-3
                if t[0]>=120-((len(str(tm)*12))) and t[0]<=(120+len(str(tm))*12):
                    print(t)
                    tm=round(t[1]/5)-3
                if t[0]<=120+((len(str(tm))*12+len(str(th))*24)+24) and t[0]>=(120+len(str(tm))*12)-24:
                    print(t)
                    ts=round(t[1]/3.619)-4
                if t[0]>220:
                    main()
                if t[0]<20:
                    timer_length=ts+(tm*60)+(th*3600)
                    timervar=True
                    current_time=utime.localtime()
                    main()
               
                    
            lcd.show()
            
    def clock_main():
        while True:
            lcd.fill(33010)
            lcd.ellipse(120,120,110,110,0,1)
            lcd.show()
            g=gesture()
            if g=='LEFT':
                time_change_main()
            if g=='RIGHT':
                timer()
            utime.sleep(.1)
    clock_main()
    
def brightness():
    global b
    utime.sleep(.5)
    t=touch1()
    t=touch1()
    
    while True:
        lcd.fill(0)
        lcd.fill_rect(110,0,20,240,0)
        lcd.rect(110,0,20,240,0xffff)
        t=touch()
        
        if t!=None:
            if t[0]<=20:
                return 
            
            else:
                lcd.fill_rect(90,t[1],60,20,0xffff)
                lcd.fill_rect(111,t[1]+20,18,240-t[1],0xfff)
                diff=240-t[1]
                diff*=273.0625
            
                b=int(diff)
                lcd.set_bl_pwm(b)
        
                lcd.show()
       
"""
def flappy_game():
    for i in range(0,3):
        lcd.fill(0)
        lcd.write_text(str(3-i),108,108,3,0xffff)
        lcd.show()
        utime.sleep(1)
    x,y=100,100
    score=0
    speed=3
    px,py,pl = 240,0,random.randint(0,120)
    
    
    def flappy_bird(x,y,color):
                                    
                                    
                                        
                                       
        
        lcd.fill_rect(x,y,20,20,0x0000)
        lcd.fill_rect(x+2,y+2,17,17,color)
        lcd.fill_rect(x+12,y+3,6,6,0x0000)
        lcd.fill_rect(x+13,y+4,4,4,0xffff)
        lcd.fill_rect(x+14,y+10,10,5,0x0000)
        lcd.fill_rect(x+15,y+11,8,3,252)
        lcd.fill_rect(x+14,y+4,3,3,0x0000)
        lcd.fill_rect(x-8,y+5,15,5,0x0000)
        lcd.fill_rect(x-7,y+6,13,3,0x7BEF)
        lcd.show()
    def pipes(x,y,l,speed=3):
        px=x
        py=y
        pl=l
        if x<=-35:
            px=240
            pl = random.randint(0,120)
       
        lcd.fill_rect(px,py,30,pl,0x0000)
        lcd.fill_rect(px+3,py+3,24,pl-6,0x001f)
        
        lcd.fill_rect(px,py+pl+90,40,240-pl,6422)
        lcd.fill_rect(px,py+pl+90,30,240-pl,0x0000)
        lcd.fill_rect(px+3,py+pl+90+3,24,240-pl,0x001f)
        px-=speed
        
        return px,py,pl
    while True:
        
        lcd.fill(6422)
        px,py,pl=pipes(px,py,pl,speed)
        flappy_bird(x,y,2047)
        if touch1()[2]:
            for i in range(0,5):
                y-=5
                lcd.fill(6422)
                px,py,pl=pipes(px,py,pl)
                flappy_bird(x,y,2047)
        
        elif x+20>=px and x+20<= px +2:
            score+=1
        #print(score)
        if score>0 and score%3==0:
            
            speed+=1
        if x+20>=px and x+20<=px+30 and y>=py and y<=py+pl or x+20>=px and x+20<=px+30 and y>=py+pl+90 or  x>=px and x<=px+30 and y>=py and y<=py+pl or x>=px and x<=px+30 and y>=py+pl+90 or x+20>=px and x+20<=px+30 and y+20>=py and y+20<=py+pl or x+20>=px and x+20<=px+30 and y+20>=py+pl+90 or  x>=px and x<=px+30 and y+20>=py and y+20<=py+pl or x>=px and x<=px+30 and y+20>=py+pl+90 :
                
                
                while True:
                    lcd.fill(6422)
                    pipes(px,py,pl)
                    flappy_bird(x,y,0x07E0)
                    if y>=220:
                        break
                    
                    
                    y+=2
        if y+20>=240:
            flappy_bird(x,y,0x07E0)
            
            break
        y+=3
   
    lcd.ellipse(120,120,100,100,0x7e0,1)
    lcd.ellipse(120,120,100,100,0)
    lcd.write_text('Score:'+str(score),75,112,2,0xffff)
    lcd.show()
"""
def compass():
    
    
    qmi8658=display.QMI8658()
    
    oldz=0
    while(True):
        lcd.fill(0)
        lcd.ellipse(120,120,5,5,0xffff,1)
        #read QMI8658
        xyz=qmi8658.Read_XYZ()
        """
        LCD.fill(LCD.white)
        
        LCD.fill_rect(0,0,240,40,LCD.red)
        LCD.text("Waveshare",80,25,LCD.white)
        
        LCD.fill_rect(0,40,240,40,LCD.blue)
        # LCD.text("Long Press to Quit",20,57,LCD.white)
        LCD.write_text("Long Press to Quit",50,57,1,LCD.white)
        
        LCD.fill_rect(0,80,120,120,0x1805)
        LCD.text("ACC_X={:+.2f}".format(xyz[0]),20,100-3,LCD.white)
        LCD.text("ACC_Y={:+.2f}".format(xyz[1]),20,140-3,LCD.white)
        LCD.text("ACC_Z={:+.2f}".format(xyz[2]),20,180-3,LCD.white)

        LCD.fill_rect(120,80,120,120,0xF073)
        LCD.text("GYR_X={:+3.2f}".format(xyz[3]),125,100-3,LCD.white)
        LCD.text("GYR_Y={:+3.2f}".format(xyz[4]),125,140-3,LCD.white)
        LCD.text("GYR_Z={:+3.2f}".format(xyz[5]),125,180-3,LCD.white)
        """
        
        z=str("{:+3.2f}".format(xyz[5]))
        z=float(z)
        #print(x,y,z)
        
        
        z=round(oldz+z/20)
        oldz=z
        if oldz>360:
            oldz-=360
      
        x1,y1 = rotate(110,360-z,120,120)
        lcd.line(120,120,x1,y1,0x7e0)
        lcd.show()
        #LCD.fill_rect(0,200,240,40,0x180f)
        ##reading = Vbat.read_u16()*3.3/65535*2
        #LCD.text("Vbat={:.2f}".format(reading),80,215,LCD.white)
        
        lcd.show()
        
        if touch()!=None:
            break
def game():
    for i in range(0,3):
        lcd.fill(0)
        lcd.write_text(str(3-i),108,108,3,0xffff)
        lcd.show()
        utime.sleep(1)
    def background(cx,cy):
        lcd.fill(6422)
        lcd.fill_rect(cx,cy,50,10,0xffff)
        lcd.fill_rect(cx+15,cy-10,20,10,0xffff)
        lcd.fill_rect(cx+100,cy-10,50,15,0xffff)
        lcd.fill_rect(cx+100+20,cy-20,16,10,0xffff)
        lcd.fill_rect(cx+200,cy,50,10,0xffff)
        lcd.fill_rect(cx+15+200,cy-10,20,10,0xffff)
        lcd.fill_rect(0,162,240,100,lcd.brown)
    def avatar(x,y):
        lcd.fill_rect(x,y,20,20,0x001f)
        lcd.rect(x,y,20,20,0x00)
        lcd.fill_rect(x+3,y+3,5,5,0)
        lcd.fill_rect(x+12,y+3,5,5,0)
        lcd.fill_rect(x+8,y+8,4,4,0)
        lcd.fill_rect(x+3,y+11,14,4,0)
        lcd.fill_rect(x+3,y+15,4,3,0)
        lcd.fill_rect(x+13,y+15,4,3,0)
        lcd.fill_rect(x+5,y+20,10,29,0x001f)
        lcd.rect(x+5,y+19,10,30,0)
        lcd.fill_rect(x-6,y+48,12,15,0x001f)
        lcd.rect(x-6,y+48,12,15,0)
        lcd.fill_rect(x+14,y+48,12,15,0x001f)
        lcd.rect(x+14,y+48,12,15,0)
    def obstacles(x,y):
        
        lcd.fill_rect(x,y,25,25,0xffff)
        lcd.fill_rect(x,y,25,6,0x07e0)
        lcd.fill_rect(x,y+19,25,6,0x07e0)
        lcd.text('TNT',x+1,y+8,0x000)
        lcd.fill_rect(x+12,y-3,3,3,0)
        lcd.fill_rect(x+14,y-6,3,3,0)
    
    lcd.fill(6422)
    avatar(100,100)
    lcd.show()
    x,y=100,100
    cx,cy=240,50
    ox,oy=250,137
    speed=4
    distance=0
    playing=True
    n=11
    while playing:
        t=touch1()
        background(cx,cy)
        avatar(x,y)
        obstacles(ox,oy)
        lcd.text(str(distance),120-int(len(str(distance))/2),10,0)
        lcd.show()
        if  distance>0 and distance%200==0:
            speed+=1
        if  distance>0 and distance%400==0:
            n+=1
        if cx<=-240:
            cx=240
        if ox<=-240:
            ox=250
        if ox<=125 and ox>=75 and  oy>=y+32:
            lcd.fill_rect(ox,oy,25,25,0xffff)
            lcd.show()
            utime.sleep(.5)
            obstacles(ox,oy)
            lcd.show()
            lcd.fill_rect(ox,oy,25,25,0xffff)
            lcd.show()
            utime.sleep(1)
            obstacles(ox,oy)
            
            lcd.show()
            utime.sleep(1)
            lcd.fill_rect(ox,oy,25,25,0xffff)
            lcd.show()
            utime.sleep(.2)
        
            size=2
            colors=[0x07e0,0xffff,2047]
            for i in range(0,30):
                lcd.fill_rect(int(ox+12-size/2),oy+12-int(size/2),size,size,colors[random.randint(0,2)])
                lcd.show()
                size+=i
            playing=False
            break
        cx-=speed
        ox-=speed+1
        distance+=1
        if t!=None:
            
            spd=n
            for i in range(0,n):
                background(cx,cy)
                obstacles(ox,oy)
                avatar(x,y)
                lcd.text(str(distance),120-int(len(str(distance))*8/2),10,0)
                if ox<=125 and ox>=75 and  oy>=y+32 and oy<=y+64:
                    lcd.fill_rect(ox,oy,25,25,0xffff)
                    lcd.show()
                    utime.sleep(.5)
                    obstacles(ox,oy)
                    lcd.show()
                    lcd.fill_rect(ox,oy,25,25,0xffff)
                    lcd.show()
                    utime.sleep(1)
                    obstacles(ox,oy)
                    
                    lcd.show()
                    utime.sleep(1)
                    lcd.fill_rect(ox,oy,25,25,0xffff)
                    lcd.show()
                    utime.sleep(.2)
                
                    size=2
                    colors=[0x07e0,0xffff,2047]
                    for i in range(0,30):
                        lcd.fill_rect(int(ox+12-size/2),oy+12-int(size/2),size,size,colors[random.randint(0,2)])
                        lcd.show()
                        size+=i
                    playing=False
                    break
                y-=spd
                spd-=int(n/10)
                lcd.show()
                cx-=speed
                ox-=speed+1
                distance+=1
            for i in range(0,n):
                
                background(cx,cy)
                obstacles(ox,oy)
                avatar(x,y)
                lcd.text(str(distance),120-int(len(str(distance))/2),10,0)
                if ox<=125 and ox>=75 and  oy>=y+32 and oy<=y+64:
                    lcd.fill_rect(ox,oy,25,25,0xffff)
                    lcd.show()
                    utime.sleep(.5)
                    obstacles(ox,oy)
                    lcd.show()
                    lcd.fill_rect(ox,oy,25,25,0xffff)
                    lcd.show()
                    utime.sleep(1)
                    obstacles(ox,oy)
                    
                    lcd.show()
                    utime.sleep(1)
                    lcd.fill_rect(ox,oy,25,25,0xffff)
                    lcd.show()
                    utime.sleep(.2)
                
                    size=2
                    colors=[0x07e0,0xffff,2047]
                    for i in range(0,30):
                        lcd.fill_rect(int(ox+12-size/2),oy+12-int(size/2),size,size,colors[random.randint(0,2)])
                        lcd.show()
                        size+=i
                    playing=False
                    break
                spd+=int(n/10)
                y+=spd
                cx-=speed
                ox-=speed+1
                distance+=1
                lcd.show()
    lcd.ellipse(120,120,100,100,0x7e0,1)
    lcd.ellipse(120,120,100,100,0)
    lcd.write_text('Score:'+str(distance),75,112,2,0xffff)
    lcd.show()
    utime.sleep(3)
   
        
def app_screen():
    global on
    x,y=0,0
    def icons(icon,x,y):
        if icon=='Calculator':
            lcd.rect(x-8,y-8,46,56,0xffff)
            lcd.fill_rect(x-5,y-5,40,50,0xffff)
            lcd.fill_rect(x,y,30,40,801)
            lcd.rect(x,y,30,40,0)
            lcd.fill_rect(x+3,y+3,24,5,64006)
            lcd.fill_rect(x+3,y+10,5,4,1033)
            lcd.fill_rect(x+11,y+10,5,4,1033)
            for i in range(0,24,6):
                
                    
                    lcd.fill_rect(x+3+i,y+10,5,5,to_color(100,100,100))
            for i in range(0,24,6):
                
                    
                    lcd.fill_rect(x+3+i,y+18,5,5,to_color(100,100,100))
            for i in range(0,24,6):
                
                    
                    lcd.fill_rect(x+3+i,y+26,5,5,to_color(100,100,100))
        elif icon=='Clock':
            lcd.rect(x-8,y-8,46,56,0xffff)
            lcd.fill_rect(x-5,y-5,40, 50,0xf800)
            lcd.ellipse(x+15,y+20,15,15,0x000,3)
            lcd.ellipse(x+15,y+20,13,13,0xffff,3)
            lcd.line(x+15,y+20,x+22,y+13,0x000)
            lcd.line(x+15,y+20,x+15,y+10,0x000)
            
        
            
           
        elif icon=='Flappy Bird':
            lcd.rect(x-8,y-8,46,56,0xffff)
            lcd.fill_rect(x-5,y-5,40, 50,6422)
            #lcd.fill_rect(x-15,y-10,40,45,6422)
            lcd.fill_rect(x+5,y,20,20,0x0000)
            lcd.fill_rect(x+7,y+2,17,17,2047)
            lcd.fill_rect(x+17,y+3,6,6,0x0000)
            lcd.fill_rect(x+18,y+4,4,4,0xffff)
            lcd.fill_rect(x+19,y+10,10,5,0x0000)
            lcd.fill_rect(x+20,y+11,8,3,252)
            lcd.fill_rect(x+19,y+4,3,3,0x0000)
            lcd.fill_rect(x-3,y+5,15,5,0x0000)
            lcd.fill_rect(x-2,y+6,13,3,0x7BEF)
        elif icon=='Exit':
            lcd.rect(x-8,y-8,46,56,0xffff)
            lcd.fill_rect(x-5,y-5,40, 50,0x001f)
            lcd.text('Exit',x,y+30,0x000)
            lcd.line(x+5,y+15,x+25,y+15,0x0000)
            lcd.line(x+5,y+15,x+10,y+10,0x0000)
            lcd.line(x+5,y+15,x+10,y+20,0x0000)
        elif icon=='Power Off':
            lcd.rect(x-8,y-8,46,56,0xffff)
            lcd.fill_rect(x-5,y-5,40, 50,0x07e0)
 #           lcd.text('PowerOff',x,y+30,0x000)
            lcd.ellipse(x+15,y+20,15,15,0x000,3)
            lcd.ellipse(x+15,y+20,13,13,0x07e0,3)
            lcd.fill_rect(x+7,y+4,16,10,0x7e0)
            lcd.fill_rect(x+13,y,2,15,0)
        elif icon=='Graphingcal':
            lcd.rect(x-8,y-8,46,56,0xffff)
            lcd.fill_rect(x-5,y-5,40, 50,0xffff)
            lcd.line(x+15,y,x+15,y+40,0)
            lcd.line(x+2,y+20,x+30,y+20,0)
            lcd.line(x+2,y+40,x+30,y+5,0)
        elif icon == 'Mindfullness':
            lcd.rect(x-8,y-8,46,56,0xffff)
            lcd.fill_rect(x-5,y-5,40, 50,0xffff)
            lcd.ellipse(x+15,y+20,15,15,0xff,3)
           
            lcd.fill_rect(x+22,y+15,4,4,0)
            lcd.fill_rect(x+8,y+15,4,4,0)
            lcd.text('\_/',x+3,y+22,0)
        elif icon=='Creeper Game':
            lcd.rect(x-8,y-8,46,56,0xffff)
            lcd.fill_rect(x-5,y-5,40, 50,6422)
            lcd.fill_rect(x+3,y+5,25,25,0xffff)
            lcd.fill_rect(x+3,y+5,25,6,0x07e0)
            lcd.fill_rect(x+3,y+5+19,25,6,0x07e0)
            lcd.text('TNT',x+3+1,y+8+5,0x000)
            lcd.fill_rect(x+12+3,y-3+5,3,3,0)
            lcd.fill_rect(x+14+3,y-6+5,3,3,0)
        elif icon=='Direction Tracking':
            lcd.rect(x-8,y-8,46,56,0xffff)
            lcd.rect(x-5,y-5,40, 50,0xffff)
            lcd.ellipse(x+15,y+20,15,15,to_color(100,100,100),3)
            lcd.ellipse(x+15,y+20,10,10,0xffff,3)
            
            lcd.line(x+15,y+20,x+15,y+10,0x07e0)
        else:
            lcd.rect(x-8,y-8,46,56,0xffff)
            lcd.fill_rect(x-5,y-5,40, 50,0xffff)
            lcd.text(icon,x-5,y+15)
            
    j = True
    apps=['Clock','Calculator','Power Off','Light','Creeper Game','Direction Tracking','Mindfullness']
    app_locations=None
    def swipe(x):
        j = True
        jj=True
        y=0
       
        while True:
            lcd.fill(to_color(50,50,50))
            app_locations=[]
            lcd.fill_rect(x,y,240,240,0)
            
            lcd.fill_rect(x+10,y+80,9,80,0xffff)
            lcd.ellipse(x+14,y+80,4,4,0xffff,1)
            lcd.ellipse(x+14,y+160,4,4,0xffff,1)
            if j ==True and jj==True:
                t=touch()
                if t!=None:
                    x,y=t[0],0
                else:
                    if x>80:
                        x = 240
                        jj=False
                        continue
                    if x<80:
                        x = 0
                        j = False
                        continue
            x1,y1=x+50,y+30
            for i in range(0,len(apps)):
                
                icons(apps[i],x1,y1)
                app_locations.append([apps[i],x1,y1])
                y1+=70
                if y1>=180:
                    y1=y+30
                    x1+=60
                
                
            lcd.show()
            if jj==False:
                return None
            if j == False:
                return app_locations
            
    app_locations = swipe(240)
    print(app_locations)
    if app_locations==None:
        
        main()
    def g():
        for i in range(0,260,30):
            app_locations=[]
            x=240-i
            lcd.fill_rect(x,y,240,240,0)
            x1,y1=x+50,y+30
            for i in range(0,len(apps)):
                
                icons(apps[i],x1,y1)
                app_locations.append([apps[i],x1,y1])
                y1+=70
                if y1>=180:
                    y1=y+30
                    x1+=60
            lcd.show()
        return app_locations
    
    utime.sleep(.5)
    lcd.show()
    t = touch1()
    t = touch1()
    
    while True:
        lcd.show()
        t=touch1()
        
        if t!=None:
            if t[0]<30:
                
                if swipe(5)==None:
        
                    main()
            for i in range(0,len(app_locations)):
                c=app_locations[i]
              
                if t[0]>=c[1]-8 and t[0]<=c[1]-8+45 and t[1]>=c[2]-8 and t[1]<=c[2]-8+55:
                    choice=c[0]
                    #print(choice)
                    if choice=='Flappy Bird':
                        flappy_game()
                        utime.sleep(2)
                        app_screen()
                    if choice=='Clock':
                        clock()
                    if choice=='Exit':
                        main()
                    if choice=='Power Off':
                        on=False
                        lcd.set_bl_pwm(0)
                        main()
                    if choice=='Calculator':
                        calculator()
                    if choice=='Graphingcal':
                        graphingcal()
                        
                    if choice=='Light':
                        brightness()
                    if choice=='Creeper Game':
                        game()
                    if choice=='Direction Tracking':
                        compass()
                    if choice=='Mindfullness':
                        mindfullness()
                    app_locations = g()
                
        #print(t)
        utime.sleep(.05)

while True:
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as err:
       
            
        lcd.fill(0xffff)
        lcd.ellipse(120,120,100,100,0xf800 ,1)
        lcd.text('An error occured',53,50,0xffff)       
        lcd.show()
        print(err)
        utime.sleep(.5)
        
        continue
