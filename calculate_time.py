import time
def calcProd():
# Calculate the product of the first 100 numbers.
    product = 1
    for i in range(1, 100):
        product = product * i
    return product
startTime = time.datetime()
print(startTime)
prod = calcProd()
endTime = time.time()
print(prod)
print('The result is %s digits long.' % (len(str(prod))))
print('Took %s seconds to calculate.' % (endTime - startTime))