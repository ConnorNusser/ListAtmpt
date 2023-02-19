from enum import Enum
import csv
import sys
class IpBucket:
    def __init__(self, currVal = 1, assumedIndex = 0):
        #current Value for this bucket of values
        self.currVal = currVal
        # The set of different Ip Addresses
        self.IpBucketSet = set()

        # because the array itself will shrink and 
        # expand the index object itself won't neccesarily be valid
        self.assumedIndex = assumedIndex

        # two pointers to point to the next and previous linked list points
        self.next = None
        self.prev = None
class IpMetadata(Enum):
    VALUE = 0
    INDEXPOSITION = 1

class Solution:
    def __init__(self):
        self.ipDictionary =  {}
        self.indexOffSet = 0

        self.IpArray = [IpBucket()]




    def moveNextAppend(self, localBucket: IpBucket, currIndex, ipName):
        # localBucket is our previous array Item
        # currIndex is our index without offset
        # ipName is the name of the ip
        self.IpArray.append(IpBucket(self.ipDictionary[ipName][IpMetadata.VALUE.value], localBucket.assumedIndex + 1))
        self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] + 1
        self.IpArray[-1].IpBucketSet.add(ipName)

        actualIndex = currIndex +  self.indexOffSet

        # If our previous bucket is now empty jump to the prev one
        if len(localBucket.IpBucketSet) == 0:
            tmp = self.IpArray[actualIndex].prev
            self.IpArray[-1].prev = tmp
            tmp.next = self.IpArray[-1]
            self.IpArray[actualIndex].prev = None
            self.IpArray[actualIndex].next = None
        else:
            self.IpArray[actualIndex].next = self.IpArray[-1]
            self.IpArray[-1].prev = self.IpArray[actualIndex]

    def moveNextSquare(self, currIndex, ipName):
        #Goals move to the next element
        #Steps to move next...
        #First check if current element is empty
        oldIndex = currIndex + self.indexOffSet
        newIndex = oldIndex + 1
        # add Element to new Index
        self.IpArray[newIndex].IpBucketSet.add(ipName)
        # change Index position of ipDictionary Element
        self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = self.IpArray[newIndex].assumedIndex
        
        if len(self.IpArray[oldIndex].IpBucketSet) == 0:
            prev = self.IpArray[oldIndex].prev
            next = self.IpArray[oldIndex].next
            # remove pointers from old Index
            self.IpArray[oldIndex].next = None
            self.IpArray[oldIndex].prev = None
            # add pointers to new Index
            self.IpArray[newIndex].prev = prev
            self.IpArray[newIndex].next = next
            # change outlying pointers
            prev.next = self.IpArray[newIndex]
            next.prev = self.IpArray[newIndex]
        else:
            # alternatively we just need to add in our element to the index
            next = self.IpArray[oldIndex].next
            # remove next pointer from oldIndex and reassign
            self.IpArray[oldIndex].next = self.IpArray[newIndex]
            # add pointers to new Index
            self.IpArray[newIndex].prev = self.IpArray[oldIndex]
            self.IpArray[newIndex].next = next
            # next pointer needs to jump up to newIndex
            next.prev = self.IpArray[newIndex]

    def moveNextArrow(self,currIndex, ipName):
        #actual Index in case values were popped
        oldIndex = currIndex + self.indexOffSet
        newIndex = oldIndex + 1
        # add Element to new Index
        self.IpArray[newIndex].IpBucketSet.add(ipName)
        # change Index position of ipDictionary Element
        self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = self.IpArray[newIndex].assumedIndex
        
        if len(self.IpArray[oldIndex].IpBucketSet) == 0:
            prev = self.IpArray[oldIndex].prev
            # remove nodes from oldIndex
            self.IpArray[oldIndex].next = None
            self.IpArray[oldIndex].prev = None
            # add new prev position
            self.IpArray[newIndex].prev = prev
            prev.next = self.IpArray[newIndex]

            
        
        
    def handle_initial_requests(self, ipName):
        currentIpVal = self.ipDictionary[ipName][IpMetadata.VALUE.value]
        #scenarios are: if IpBucket is empty 
        if len(self.IpArray[0].IpBucketSet) == 0:
            self.IpArray[0].IpBucketSet.add(ipName)
            self.IpArray[0].currVal = 1

            #add Index to None
            self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = 0
            return
        
        if self.IpArray[0].currVal > currentIpVal:
            #if IpBucket first value is bigger than our IP but you still need to add in the value
            self.indexOffSet += 1
            currIndex = self.IpArray[0].assumedIndex
            self.IpArray.insert(0, IpBucket(currentIpVal,self.currIndex))
            self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = 0 - self.indexOffSet
            self.IpArray[0].next = self.IpArray[1]
            self.IpArray[1].prev = self.IpArray[0]
            self.IpArray[0].add(ipName)
            return
        if self.IpArray[0].currVal == currentIpVal:
            self.IpArray[0].IpBucketSet.add(ipName)
            self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = 0 + self.indexOffSet
            return
        else:
            # grab Index
            currIndex = self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value]
            localBucket = self.IpArray[currIndex +  self.indexOffSet]
            self.IpArray[currIndex +  self.indexOffSet].IpBucketSet.remove(ipName)
            if localBucket.next == None:
                self.moveNextAppend(localBucket, currIndex, ipName)
                return

            if self.IpArray[currIndex + self.indexOffSet].next.currVal > self.ipDictionary[ipName][IpMetadata.VALUE.value]:
                self.moveNextSquare(currIndex, ipName)   
                return  
            else:
                self.moveNextArrow(currIndex, ipName)
                return
                    
    def popbottomElement(self):
        removed_val = self.IpArray[0].IpBucketSet.pop()
        self.ipDictionary[removed_val][IpMetadata.INDEXPOSITION.value] = None

    def handle_stream_requests(self, ipName):
        #Find Index of ipName
        #O(1) Lookup
        localIndex = self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value]
        localValue = self.ipDictionary[ipName][IpMetadata.VALUE.value]
        self.checkOffSet()
        
        if(localValue <= self.IpArray[0].currVal):
            return
        # Value must be greater and if its not already in our system it should be in the next.index
        if(localIndex == None):
            # Edge Case essentially where the ipDictionary hit were only active once
            if len(self.IpArray) == 1:
                # add new element
                prevIndex = self.IpArray[0].assumedIndex
                self.IpArray.append(IpBucket(localValue, prevIndex + 1 + self.indexOffSet))
                self.IpArray[1].IpBucketSet.add(ipName)
                #Update Index for our Dictionary Object
                self.ipDictionary[ipName][1] = prevIndex + 1 + self.indexOffSet
                #Remove element from bottom
                self.popbottomElement()
                #add pointers
                self.IpArray[0].next = self.IpArray[1]
                self.IpArray[1].prev = self.IpArray[0]
                return
            # if the second bucket is empty we'll need to add pointers back to this node
            elif len(self.IpArray[1].IpBucketSet) == 0:
                #store .next Pointer
                tmp = self.IpArray[0].next
                self.IpArray[0].next.prev = self.IpArray[1]
                self.IpArray[1].next = tmp
                self.IpArray[1].prev = self.IpArray[0]
                self.IpArray[0].next = self.IpArray[1]
                # add our value into the set
                self.IpArray[1].IpBucketSet.add(ipName)
                self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = self.IpArray[1].assumedIndex
                #Remove element from bottom
                self.popbottomElement()
                return
            else:
                #simple case add element to bucket pop bottom
                # add our value into the set
                self.IpArray[1].IpBucketSet.add(ipName)
                self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = self.IpArray[1].assumedIndex
                self.popbottomElement()
                return
        else:
            #This is an existing value already in our top ip system so we'll update its location and the pointers
            #but no removal will be neccesary
            # localIndex in this case is when it was passed in 
            actualIndex = localIndex + self.indexOffSet
            #remove curr set position
            self.IpArray[actualIndex].IpBucketSet.discard(ipName)
            # front of array
            if self.IpArray[actualIndex].next == None:
                self.moveNextAppend(self.IpArray[actualIndex], localIndex , ipName)
                return
            elif self.IpArray[actualIndex].next.currVal > localValue:
                self.moveNextSquare(localIndex, ipName)
            else:
                self.moveNextArrow(localIndex, ipName)

    
    def checkOffSet(self):
        if(len(self.IpArray[0].IpBucketSet) == 0):
            self.IpArray.pop(0)
            self.indexOffSet -= 1
        
    def request_handle(self, ip_address):
        if ip_address not in self.ipDictionary:
            self.ipDictionary[ip_address] = [1, None]
        else:
            self.ipDictionary[ip_address][IpMetadata.VALUE.value] = self.ipDictionary[ip_address][IpMetadata.VALUE.value] + 1
        
        if len(self.ipDictionary) <= 100:
            # go crazy fill the array as much as you can
            self.handle_initial_requests(ip_address)
            return
        self.handle_stream_requests(ip_address)
    def clear(self):
        self.ipDictionary =  {}
        self.indexOffSet = 0
        self.IpArray = [IpBucket()]
    def top100(self):
        print("-----")
        tmp = self.IpArray[0]
        print("This is the length of the array: " + str(len(self.IpArray)))
        while(tmp):
            s = tmp.IpBucketSet
            print("Curr Value in this set: %s " % tmp.currVal)
            for i in s:
                print(i)
            tmp = tmp.next
        print("xxxxxxxx")

def main(argv):
    sol = Solution()
    def request_handle(ip_address):
        sol.request_handle(ip_address)
    def top100():
        sol.top100()
    def clear():
        sol.clear()
    with open("./txtFile.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            exec(row[0])

if __name__ == "__main__":
   main(sys.argv[1:])

