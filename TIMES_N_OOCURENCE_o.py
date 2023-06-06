a = [1,1,1,2,2,2,1,3,3,3,1,3,1,2]
T = int(input("enter number of times : "))
abc = []
last_element = []
maxlist = []
for x in a :
    times = a.count(x)
    if times == T :
        abc.append(x)
if abc == []:
    print("no repeating")
else :
    # print(abc)
    dic = dict(enumerate(abc))
    sorted = dict(sorted(dic.items(), key=lambda y:y[1]))
    # print(sorted)
    list1 = list(sorted.keys())
    # print(list1)
    L = int((len(list1)+1) / T)
    for i in range(1, L+1):
        x = (i*T) - 1
        last_element.append(x)
    # print(last_element)
    for each in last_element:
        maxlist.append(list1[each])
    # print(maxlist)
    index = min(maxlist)
    print(abc[index])