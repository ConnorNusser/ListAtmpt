import random
import time
import copy
import csv 
ipSet = set()
ipArr = []
start_time = time.time()
for i in range(2 * 10 ** 5):
  ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0,255),4))
  request_HandlerString = 'request_handle("%s")' % ip
  if request_HandlerString in ipSet:
    continue
  ipSet.add(request_HandlerString)
  ipArr.append(request_HandlerString)
  
endArr = []
for i in range(10 ** 6):
    random_element = random.randrange(0, len(ipArr))
    top100_flag = random.randrange(0, 100)
    if top100_flag == 99:
        endArr.append("top100()")
    endArr.append(ipArr[random_element])

knownipOne = 'request_handle("10.20.40.60")'
knownipTwo = 'request_handle("5.10.15.20")'

knownipThree = 'request_handle("fuck.10weqewweq.15.20")'


for i in range(10000):
    endArr.append(knownipOne)
for i in range(20000):
    endArr.append(knownipTwo)    
for i in range(46):
    endArr.append(knownipThree)
random.shuffle(endArr)

for i in range(52):
    endArr.insert(0, 'request_handle("done")')
    
    
with open("txtFile.csv", mode="w") as file:

    # create a CSV writer object
    writer = csv.writer(file)

    # write each item in the list as a new row in the CSV file
    for item in endArr:
        writer.writerow([item])
 
print("--- %s seconds ---" % (time.time() - start_time))
    

    

