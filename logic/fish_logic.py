from core.HandleOperation import sendKey
from constant.states import get_states
import time
import random
class Fisher:
    def __init__(self,mem,hwnd):
        self.mem=mem
        self.max_gp=self.mem.get_max_gp()
        self.current_gp=self.max_gp
        self.gp_timer=0.
        self.p2_timer=0.
        self.p2_state=False
        self.fish_timer=0.
        self.iterval=0.5
        self.potion_timer=0.
        self.hwnd=hwnd
        self.small_big=False
        self.idle_count=0
        self.food_timer=0
        

    def sleep_time(self,iterval, add_random=True):
        if add_random:
            iterval+=random.gauss(0,0.1)
        time.sleep(iterval)
        self.gp_timer+=iterval
        self.p2_timer-=iterval
        self.fish_timer+=iterval
        self.potion_timer-=iterval
        self.food_timer-=iterval
        
    def run(self):
        while True:
            self.fish_op=get_states(hex(self.mem.get_fish_status()))
            print(f'gp {self.current_gp}, op {self.fish_op}, gp_timer {self.gp_timer}, p2_timer {self.p2_timer}, fish_timer {self.fish_timer}, small_big {self.small_big}, potion_timer {self.potion_timer}, idle_count {self.idle_count}')
            
            # 空闲时连续操作不超过5个
            if self.fish_op!=0:
                self.idle_count=0

            # 修正GP
            self.max_gp=self.mem.get_max_gp()
            self.current_gp=min(self.current_gp,self.max_gp)
            while self.gp_timer>=3.:
                self.current_gp=min(self.current_gp+7,self.max_gp)
                self.gp_timer-=3.
            
            # 修正小大状态
            if self.fish_op==2:
                self.small_big=True
            if self.fish_op==1:
                self.small_big=False
            
            # 超时提竿
            if self.fish_timer>10. and self.fish_op==1:
                self.sleep_time(0.5)
                sendKey(self.hwnd,'X')

            # 轻杆全提
            if self.fish_op==3:
                self.sleep_time(0.7)
                sendKey(self.hwnd,'V')
                sendKey(self.hwnd,'V')
                self.sleep_time(0.7)
                self.current_gp-=50
                sendKey(self.hwnd,'X')
                self.small_big=True

            # 小大中重杆提
            if (self.fish_op==4 or self.fish_op==5) and self.small_big:
                self.sleep_time(0.7)
                sendKey(self.hwnd,'C')
                sendKey(self.hwnd,'C')
                self.sleep_time(0.7)
                if self.p2_state:
                    self.current_gp-=50
                sendKey(self.hwnd,'X')
                self.small_big=False    

            # 空闲状态
            if self.fish_op==0:

                # 最大GP小于940吃蟹饼
                if self.max_gp<940 and self.idle_count<5:
                    self.sleep_time(3)
                    sendKey(self.hwnd,'Q')
                    old_gp=self.max_gp
                    self.max_gp=self.mem.get_max_gp()
                    if self.max_gp>old_gp:
                        self.food_timer=1800
                    self.current_gp=min(self.current_gp,self.max_gp)
                    self.sleep_time(1.5)
                    self.idle_count+=1
                    continue
                
                # 还小于940 说明装备坏了，不钓
                if self.max_gp<940 and self.food_timer>1:
                    break
                    
                # gp<540 吃强心剂
                if self.current_gp<=540 and self.potion_timer<=0. and self.idle_count<5:
                    self.sleep_time(3)
                    sendKey(self.hwnd,'3')
                    sendKey(self.hwnd,'3')
                    self.current_gp+=400
                    self.potion_timer=180
                    self.sleep_time(2)
                    self.idle_count+=1
                    continue
                
                # gp不够，休息
                if self.p2_timer<=5. and self.current_gp<630 and not self.small_big:
                    self.sleep_time(3)
                    continue
                
                # 开耐2
                if self.p2_timer<=5. and self.current_gp>=630 and not self.small_big and self.idle_count<5:
                    self.sleep_time(3)
                    sendKey(self.hwnd,'2')
                    sendKey(self.hwnd,'2')
                    self.p2_state=True
                    self.current_gp-=560
                    self.p2_timer=145
                    self.sleep_time(1.5)
                    self.idle_count+=1
                    continue
                
                # gp<540 吃强心剂
                if self.current_gp<=500 and self.potion_timer<=0. and self.idle_count<5:
                    self.sleep_time(3)
                    sendKey(self.hwnd,'3')
                    sendKey(self.hwnd,'3')
                    self.current_gp+=400
                    self.potion_timer=180
                    self.sleep_time(2)
                    self.idle_count+=1
                    continue
                
                # 小大
                if self.small_big:
                    self.sleep_time(0.7)
                    if self.p2_timer<-1:
                        self.p2_state=False
                    sendKey(self.hwnd,'4')
                    self.sleep_time(0.3)
                    self.fish_timer=0.
                    sendKey(self.hwnd,'Z')
                    self.sleep_time(0.5)
                    continue
                # 普通抛竿
                else:
                    
                    self.sleep_time(0.7)
                    if self.p2_timer<-1:
                        self.p2_state=False
                    sendKey(self.hwnd,'Z')
                    self.fish_timer=0.
                    self.sleep_time(0.3)
                    
                    continue
                
            self.sleep_time(self.iterval)

