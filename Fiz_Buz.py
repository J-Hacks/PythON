

def fiz_buz_FizBuz(i) :
    if i%15==0 :
        print("FizBuz")
    elif i%3==0 :
        print("Fiz")
    elif i%5==0 :
        print("Buz")
    else :
        print(f"{i}")
x = int(input("enter number upto check :"))
for i in range(1, x+1) :
    fiz_buz_FizBuz(i)

        
