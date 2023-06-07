def sumof():
    for x in a:
        element.append(x)
        if sum(element) == s:
            print(f'{element[0]}  {element[-1]}')
    return -1

a = [2,3,4,5,6,7,8,9,10]
s = 15
element = []
for y in range(0, (len(a)-1)):
    if sumof() == -1:
        a.pop(0)
        element = []
        sumof()


