import random
from threading import Thread
import time

# 角色
class role(object):
    # 爱莉
    class aili(object):
        def __init__(self):
            self.name = '爱莉'
            self.hp = 100
            self.attack = 21
            self.defense = 8
            self.speed = 20
            self.reduce_attack_round = 0
            
        def status(self):
            return
            
        def skill(self, round, oneself, enemy):
            interval = 3
            harm = 0
            if round%interval == 0:
                harm = random.randint(25, 50)
                enemy.attack -= 6
                self.reduce_attack_round = 1
                print('爱莉 对手下次行动攻击力 -6')
            elif self.reduce_attack_round == 1:
                enemy.attack += 6
                self.reduce_attack_round = 0
                print('爱莉 对手攻击力恢复 +6')
            
            return harm
            
        def passiveSkill(self, harm, oneself, enemy):
            again_attack = random.randint(1, 100)
            if again_attack <= 35:
                print('爱莉 被动追击')
                return 11
            return 0
        
        def reset(self):
            self.hp = 100
            self.attack = 21
            self.defense = 8
            self.speed = 20
            self.reduce_attack_round = 0
            
    # 梅比乌斯
    class meibiwusi(object):
        def __init__(self):
            self.name = '梅比乌斯'
            self.hp = 100
            self.attack = 21
            self.defense = 11
            self.speed = 23
            
        def status(self):
            return
            
        def skill(self, round, oneself, enemy):
            interval = 4
            harm = 0
            if round%interval == 0:
                harm = 33
            
            return harm
            
        def passiveSkill(self, harm, oneself, enemy):
            probability = random.randint(1, 100)
            if harm > 0 and probability <= 33:
                enemy.defense -= 3
                print('梅比乌斯 对 对手防御力 -3')
            return 0
        
    # 华
    class hua(object):
        def __init__(self):
            self.name = '华'
            self.hp = 100
            self.attack = 21
            self.defense = 12
            self.speed = 15
            self.charge = 0
            
        def status(self):
            return
            
        def skill(self, round, oneself, enemy):
            interval = 3
            harm = self.attack
            if round%interval == 0:
                self.defense += 3
                self.charge = 1
                harm = 0
                print('华 蓄力 防御 +3')
            elif self.charge == 1:
                self.defense -= 3
                self.charge = 0
                addharm = random.randint(10, 33)
                print('华 完成蓄力 伤害加 + %d 防御 -3' %(addharm))
                harm += addharm
            
            return harm
            
        def passiveSkill(self, harm, oneself, enemy):
            harm = harm*0.8
            # self.hp += harm
            print('华 减伤')
            return harm
        
        def reset(self):
            self.hp = 100
            self.attack = 21
            self.defense = 12
            self.speed = 15
            self.charge = 0
            
    def create_role(self, name):
        call_function = getattr(self, name)
        return call_function()
    
# 状态
class status(object):
    # 混乱
    def chaos(harm, round, target):
        return
    
    # 降攻击力
    class reduce_attack(object):
        def __init__(self, val, round, target):
            self.val = val
            self.round = round
            self.target = target
    
# 战斗
class fighting(Thread):
    def __init__(self, role1, role2):
        Thread.__init__(self)
        self.role1 = role1
        self.role2 = role2
        self.round = 0
        
    def start_fighting(self):
        count = 1
        win = 1
        if self.role1.speed > self.role2.speed:
            first_role = self.role1
            second_role = self.role2
            print('先攻 %s 后手 %s' %(first_role.name, second_role.name))
        else:
            first_role = self.role2
            second_role = self.role1 
            print('先攻 %s 后手 %s' %(first_role.name, second_role.name))
            
        for count in range(10000):
            if count == 0: continue
            if count%2 == 1 :
                self.round += 1
                print("----------第%d回合-------------" %(self.round))
            if count%2 == 1:
                harm = first_role.skill(self.round, first_role, second_role)
                is_attack = False
                if harm == 0:
                    harm = first_role.attack - second_role.defense
                    is_attack = True
                else:
                    harm = harm - second_role.defense

                harm = second_role.passiveSkill(harm, first_role, second_role)
                
                if harm < 0:
                    harm = 0
                
                second_role.hp -= harm
                print( "%s 对 %s 造成了 %d点伤害; %s剩余%dHP"  %(first_role.name, second_role.name, harm, second_role.name, second_role.hp))
                
                if is_attack:
                    passiveSkill_harm = first_role.passiveSkill(harm, first_role, second_role)
                    if passiveSkill_harm > 0:
                        second_role.hp -= passiveSkill_harm 
                        print( "%s 对 %s 被动造成了 %d点伤害; %s剩余%dHP"  %(first_role.name, second_role.name, passiveSkill_harm, second_role.name, second_role.hp))
                
                if self.is_dle(second_role.hp) :
                    print('%s 获胜' %(first_role.name))
                    win = 1
                    break
                
                
            if count%2 == 0:
                harm = second_role.skill(self.round, second_role, first_role)
                # is_attack = False
                # if harm == 1:
                #     harm = second_role.attack - first_role.defense
                #     is_attack = True
                # elif harm > 1:
                #     harm = harm - first_role.defense
                # # else:
                # #     harm = harm - first_role.defense
                
                harm = harm - first_role.defense
                
                if harm < 0:
                    harm = 0
                
                first_role.hp -= harm
                print("%s 对 %s 造成了 %d点伤害; %s剩余%dHP" %(second_role.name, first_role.name, harm, first_role.name, first_role.hp))
                
                # if is_attack:
                #     passiveSkill_harm = second_role.passiveSkill(harm, first_role, second_role)
                #     if passiveSkill_harm > 0:
                #         first_role.hp -= passiveSkill_harm
                #         print("%s 对 %s 被动造成了 %d点伤害; %s剩余%dHP" %(second_role.name, first_role.name, passiveSkill_harm, first_role.name, first_role.hp))
                
                if self.is_dle(first_role.hp) :
                    print('%s 获胜' %(second_role.name))
                    win = 2
                    break
        
        return win
                
    def is_dle(self, hp):
        if hp <= 0:
            return True
        return False
    
    def run(self):
        
        aili_win = 0
        hua_win = 0
        
        for val in range(39):
            self.role1.reset()
            self.role2.reset()
            self.round = 0
            print("-----------第%d场----------" %(val + 1))
            win = self.start_fighting()
            if win == 1:
                aili_win += 1
            else:
                hua_win += 1
            time.sleep(1)
                
        print("共40场 爱莉 胜 %d : 华 胜 %d" %(aili_win, hua_win))
            
if __name__ == '__main__':
    role = role()
    aili = role.create_role('aili')
    # meibiwusi = role.create_role('meibiwusi')
    hua = role.create_role('hua')
    fighting = fighting(aili, hua)
    fighting.start()
    