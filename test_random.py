import random

# PC random choice
def pc_random_choice():

    w_1 = random.randint(1,100)
    w_2 = random.randint(-20, 20)
    odds = w_1 + w_2

    if odds < 1:
        odds = 1
    elif odds > 100:
        odds = 100

    if (odds >= 1) and (odds < 61):
        return 'CONFESAR'
    elif odds < 75:
        return 'CALLAR'
    else: 
        return 'MENTIR'


choices = []
for _ in range(100):
    choices.append(pc_random_choice())

print(f"CONFESAR: {choices.count('CONFESAR')}%")
print(f"MENTIR: {choices.count('MENTIR')}%")
print(f"CALLAR: {choices.count('CALLAR')}%")
