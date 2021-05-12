from core.HandleOperation import sendKey
from constant.states import get_states
import time

class Fisher:
    def __init__(self,mem,hwnd):
        self.mem=mem
        self.max_gp=self.mem.get_max_gp()
        self.current_gp=self.max_gp
        self.gp_timer=0.
        self.p2_timer=0.
        self.fish_timer=0.
        self.iterval=0.5
        self.potion_timer=0.
        self.hwnd=hwnd
        self.small_big=False

    def sleep_time(self,iterval):
        time.sleep(iterval)
        self.gp_timer+=iterval
        self.p2_timer-=iterval
        self.fish_timer+=iterval
        self.potion_timer-=iterval
        
    def run(self):
        while True:
            self.fish_op=get_states(hex(self.mem.get_fish_status()))
            print(f'gp {self.current_gp}, op {self.fish_op}, gp_timer {self.gp_timer}, p2_timer {self.p2_timer}, fish_timer {self.fish_timer}, small_big {self.small_big}, potion_timer {self.potion_timer}')
            
            self.max_gp=self.mem.get_max_gp()
            if self.max_gp<900:
                sendKey(self.hwnd,'Q')
                self.max_gp=self.mem.get_max_gp()
                self.sleep_time(1)
                continue

            while self.gp_timer>=3.:
                self.current_gp=min(self.current_gp+7,self.max_gp)
                self.gp_timer-=3.
            
            

            if self.fish_timer>10. and self.fish_op==1:
                sendKey(self.hwnd,'X')

            if self.fish_op==3:
                sendKey(self.hwnd,'V')
                sendKey(self.hwnd,'V')
                self.current_gp-=50
                sendKey(self.hwnd,'X')
                self.small_big=True

            if (self.fish_op==4 or self.fish_op==5) and self.small_big:
                sendKey(self.hwnd,'C')
                sendKey(self.hwnd,'C')
                self.current_gp-=50
                sendKey(self.hwnd,'X')
                self.small_big=False
            
            if self.fish_op==2:
                self.small_big=True
            if self.fish_op==1:
                self.small_big=False

            if self.fish_op==0:
                if self.current_gp<=500 and self.potion_timer<=0.:
                    self.sleep_time(3)
                    sendKey(self.hwnd,'3')
                    sendKey(self.hwnd,'3')
                    self.current_gp+=400
                    self.potion_timer=180
                    self.sleep_time(3)
                    continue

                if self.p2_timer<=5. and self.current_gp<630 and not self.small_big:
                    self.sleep_time(3)
                    continue

                if self.p2_timer<=5. and self.current_gp>=630 and not self.small_big:
                    self.sleep_time(3)
                    sendKey(self.hwnd,'2')
                    sendKey(self.hwnd,'2')
                    self.current_gp-=560
                    self.p2_timer=145
                    self.sleep_time(3)
                    continue

                if self.current_gp<=500 and self.potion_timer<=0.:
                    self.sleep_time(3)
                    sendKey(self.hwnd,'3')
                    sendKey(self.hwnd,'3')
                    self.current_gp+=400
                    self.potion_timer=180
                    self.sleep_time(3)
                    continue
                
                if self.small_big:
                    self.sleep_time(0.8)
                    sendKey(self.hwnd,'4')
                    self.sleep_time(0.5)
                    self.fish_timer=0.
                    sendKey(self.hwnd,'Z')
                    self.sleep_time(0.5)
                    continue
                else:
                    self.sleep_time(0.8)
                    sendKey(self.hwnd,'Z')
                    self.sleep_time(0.5)
                    self.fish_timer=0.
                    continue
                
            self.sleep_time(self.iterval)

