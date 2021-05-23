import random
class Chromosome:
    def __init__(self, target):
        """Target is the what we want the string to evaluate to"""
        self.chromoLen = 5 #can make longer
        self.chromo = ""#initially it is empty
        self.score= 0   #fitness
        self.total = 0  #what the string evaluates to
        self.target = target#goal
        
        #randomly make a string that is 5 nibbles long
        #make a dictionary so this is easier
        lookUp = {
            0:"0000", 
            1:"0001", 
            2:"0010" ,
            3:"0011" ,
            4:"0100" ,
            5:"0101" ,
            6:"0110" ,
            7:"0111" ,
            8:"1000" ,
            9:"1001" ,
            10:"1010", 
            11:"1011" ,
            12:"1100" ,
            13:"1101" 
        }
        
        for i in range(self.chromoLen):
            randomNum = random.randint(0,13) #generate a random number that is a possible num or operator
            binString = lookUp.get(randomNum)#find its nibble representation
            self.chromo = self.chromo + binString#add it to the string representation
        #print(self.chromo)#error checking
        self.scoreChromo()#now score the chromosome
    

        
    def scoreChromo(self):
        """fitness function"""
        self.total = self.evaluate()#translate and evaluate
        if self.total == self.target:
            self.score = 0
        else:
            self.score = 1/(self.target - self.total)
        return self.score
        
    def getTotal(self):
        """return total of the chromosome from evaluated the equation"""
        return self.total
    
    def evaluate(self):
        """walks the chromosome and performs the calculations, left to right"""
        decodedString = self.decodeChromo()
        tot = 0
        #find first number
        ptr = 0
        while ptr < len(decodedString):
            ch = decodedString[ptr]
            if ch.isdigit():
                tot += float(ch)
                #print(f"first num at: {ptr}")
                ptr +=1
                break
            else:
                ptr+=1
        #check if no numbers were found - only operators
        if ptr == len(decodedString):
            return 0
        #loop for the remaining string
        num = False
        oper = ' '
        while ptr < len(decodedString):
            ch = decodedString[ptr]
            #make sure it is what we are expecting
            if (num and not ch.isdigit()):
                ptr+=1
                continue #got to next iteration
            if (not num and ch.isdigit()):
                ptr+=1
                continue #got to next iteration
            if(num):
                if oper == "+":
                    tot+= float(ch)
                    
                elif oper == "-":
                    tot-= float(ch)
                    
                elif oper == "*":
                    tot *= float(ch)
                    
                elif oper == "/":
                    if ch != "0":#can't divide by zero
                        tot /= float(ch)   
            else:
                oper = ch
            
            ptr+=1
            num = not num
        #print(f"total: {tot}")#error checking
        return tot  
            
    def printChromo(self):
        """Quick method to print the string"""
        print(f"chromosome: {self.chromo}")
    
    def decodeChromo(self):
        """Walks the string translating the nibble into what it is supposed to be"""
        #make a dictionary for look up
        lookUp = {
            "0000" : "0",
            "0001" : "1",
            "0010" : "2",
            "0011" : "3",
            "0100" : "4",
            "0101" : "5",
            "0110" : "6",
            "0111" : "7",
            "1000" : "8",
            "1001" : "9",
            "1010" : "+",
            "1011" : "-",
            "1100" : "*",
            "1101" : "/"
        }
        decoded = ""#empty string
        for i in range(0,len(self.chromo), 4):
            key = self.chromo[i:i+4]#walks the string in nibbles
            numKey = int(key, 2) #convert binary string key into an integer
            if numKey < len(lookUp): 
                decoded = decoded + lookUp.get(key)#concatenate to the end of the string
        #print(decoded)#for error checking
        return decoded
    
    def isValid (self):
        """
        makes sure that the chromosome encodes a valid equaltion
        looking for operand - operator - operand - operator- operand pattern
        """
        decodedString = self.decodeChromo()#get the string that is the equation
        if len(decodedString) <self.chromoLen:#if there were missing parts after decoded
            return False
        #print(decodedString)
        num = True #starts with a number
        for i in range (len(decodedString)):
            c = decodedString[i]#grab a character in the string
            negatedDig = not(c.isdigit())
            if num == negatedDig:# looking for operand - operator - operand - operator- operand pattern
                #print(f"bad form {decodedString}")#error checking
                return False
            if(i > 0 and c == "0" and decodedString[i-1] == "/"): #cannot divide by zero
                return False
            num = not num #switch for the next character because this one was okay
        # cannot end in an operator
        if not decodedString[-1].isdigit():# if it does not end in a operand then not valid
            return False
        return True
    
    def crossover (self, other, rate):
        """This  will swap tails of two chromosomes"""
        if(random.random() > rate):#you don't dp this based on probability
            return
        #randomly pick a position
        pos = random.randint(0,len(self.chromo)-1)
        
        #swap chars from that point on
        for i in range(pos, len(self.chromo)):
            self.swapFromOther(other, i)

            
    def mutate(self, mutRate):
        """ walk the chromosome and flip based on probability"""
        for i in range(len(self.chromo)):
            if(random.random()<= mutRate):
                self.swap(i)

    def swap(self, pos):
        """strings are immutable - so have to rebuild the string"""
        if self.chromo[pos] == "0":
            self.chromo = self.chromo[0:pos] + "1"+ self.chromo[pos+1:len(self.chromo)]
        elif self.chromo[pos] == "1":
            self.chromo = self.chromo[0:pos] + "0"+ self.chromo[pos+1:len(self.chromo)]
    
    def swapFromOther(self, other, pos):
        """this swap tails of Strings starting at given pos"""
        temp1 = self.chromo[pos]
        temp2 = other.chromo[pos]
        self.chromo = self.chromo[0:pos] + temp2+ self.chromo[pos+1:len(self.chromo)]
        other.chromo = other.chromo[0:pos] + temp1 + other.chromo[pos+1:len(other.chromo)]
        
       
    def getScore(self):
        """return score"""
        return self.score
    
        
    def __repr__(self):
        """string representation of chromosome"""
        return f'Chromosome: {self.chromo} Decoded: {self.decodeChromo()} score: {self.scoreChromo()}'


    def __lt__(self, other):
        return self.score < other.score


    def __gt__(self, other):
        return self.score > other.score