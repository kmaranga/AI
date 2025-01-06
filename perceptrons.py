
############################################################
# Section 1: Perceptrons
############################################################

class BinaryPerceptron(object):

    def vectorMath(self , vector1 , vector2, operation):
      # print("in vectorMath")
    #get all possible keys 
      
      AllKeys = list(set(set(vector1.keys()).union(set(vector2.keys()))))

      #make the evantual resultant Vector and initalize all keys to be 0 
      resultVector = dict()
      dotProductSum = 0
      for key in AllKeys:
          if key not in vector1:
              vector1[key] = 0
          if key not in vector2:
              vector2[key] = 0
          
          if operation == '*':
              resultVector[key] = vector1[key] * vector2[key]
              dotProductSum += resultVector[key]
          if operation == '+':
              resultVector[key] = vector1[key] + vector2[key]
          if operation == '-':
              resultVector[key] = vector1[key] - vector2[key]
          
      if operation == '*':
          # print("did *")
          return dotProductSum
      else : 
        # print("did + or -")
        return resultVector
    
    def __init__(self, examples, iterations):
        #train the weight vector w⃗  on the input data using iterations passes over the data set, then store w⃗  as an internal variable for future use. 
        self.weightedVector = dict()

        for i in range(iterations):
            for example in examples:
                xi = example[0] #
                yi = example[1] 
                yiHat = self.predict(xi)
                if yi != yiHat:
                    if yi:     
                        self.weightedVector = self.vectorMath(self.weightedVector,xi,'+')
                    else :
                        self.weightedVector = self.vectorMath(self.weightedVector,xi,'-')

    def predict(self, x):
        #take as input an unlabeled example x⃗  and compute the predicted label as sign(w⃗ ⋅x⃗ ), returning True if w⃗ ⋅x⃗ >0 or False if w⃗ ⋅x⃗ ≤0.
        predicted_label = self.vectorMath(self.weightedVector,x,'*')
        if predicted_label > 0 :
            return True 
        else : 
            return False 

class MulticlassPerceptron(object):

    def vectorMath(self , vector1 , vector2, operation):
      # print("in vectorMath")
    #get all possible keys 
      AllKeys = list(set(set(vector1.keys()).union(set(vector2.keys()))))

      #make the evantual resultant Vector and initalize all keys to be 0 
      resultVector = dict()
      dotProductSum = 0
      for key in AllKeys:
          if key not in vector1:
              vector1[key] = 0
          if key not in vector2:
              vector2[key] = 0
          
          if operation == '*':
              resultVector[key] = vector1[key] * vector2[key]
              dotProductSum += resultVector[key]
          if operation == '+':
              resultVector[key] = vector1[key] + vector2[key]
          if operation == '-':
              resultVector[key] = vector1[key] - vector2[key]
          
      if operation == '*':
          # print("did *")
          return dotProductSum
      else : 
        # print("did + or -")
        return resultVector
    
    def __init__(self, examples, iterations):
        #you should train the weight vector w⃗  on the input data using iterations passes over the data set, then store w⃗  as an internal variable for future use.

        #determine number of labels 
        setOfLabels = set()
        for example in examples:
            setOfLabels.add(example[1])
        

        #weightedVector is a dictorary of dictonaries with the key being labels
        self.listOfLabels = list(setOfLabels)

        self.weightedVector = dict()
        for label in self.listOfLabels:
           self.weightedVector[label] = dict()
 

        for i in range(iterations):
            for example in examples:
                xi = example[0] #x1
                yi = example[1]

                maxDotProdResult = -1000000
                yiHat = 0
                #run through all labels and determine which label has the max yiHat val
                for label in self.listOfLabels:
                  dotProdResult = self.vectorMath(self.weightedVector[label],xi,'*')
                  if dotProdResult > maxDotProdResult:
                    maxDotProdResult = dotProdResult
                    yiHat = label
                  
                if yi != yiHat:    
                        self.weightedVector[yi] = self.vectorMath(self.weightedVector[yi],xi,'+')
                        self.weightedVector[yiHat] = self.vectorMath(self.weightedVector[yiHat],xi,'-')

    def predict(self, x):
        #take as input an unlabeled example x⃗  and compute the predicted label as sign(w⃗ ⋅x⃗ ), returning True if w⃗ ⋅x⃗ >0 or False if w⃗ ⋅x⃗ ≤0.
        maxDotProdResult = -1000000
        yiHat = 0

        for label in self.listOfLabels:
            dotProdResult = self.vectorMath(self.weightedVector[label],x,'*')
            if dotProdResult > maxDotProdResult:
              maxDotProdResult = dotProdResult
              yiHat = label
        
        return yiHat

############################################################
# Section 2: Applications
############################################################

class IrisClassifier(object):

    def __init__(self, data):
        #(6.0, 2.2, 4.0, 1.0), "iris-versicolor")
        newData = []
        valuesNames = ["lengthSeptals" , "widthSeptals" , "lengthPetals" , "widthPetals"]
        for example in data:
          values = example[0]
          label = example[1]
          dictValues = dict()
          for loc in range(4):
            dictValues[valuesNames[loc]] = values[loc]
          newData.append((dictValues,label))
          
        self.multiclassPerceptron = MulticlassPerceptron(newData , 1 )

    def classify(self, instance):
        valueNames = ["lengthSeptals" , "widthSeptals" , "lengthPetals" , "widthPetals"]
        dictValues = dict()
        for loc in range(4):
          dictValues[valueNames[loc]] = instance[loc]
        
        return self.multiclassPerceptron.predict(dictValues) 

class DigitClassifier(object):

    def __init__(self, data):
        # Example data will be provided as a list of 2-tuples (x⃗ ,y), where 
        #x⃗  is a 64-tuple of pixel counts between 0 and 16 and y is the digit represented by the image
        valuesNames = range(0, 63)
        newData = []

        for example in data:
          values = example[0]
          label = example[1]
          dictValues = dict()
          for loc in range(63):
            dictValues[valuesNames[loc]] = values[loc]
          newData.append((dictValues,label))
          
        self.multiclassPerceptron = MulticlassPerceptron(newData , 10 )


    def classify(self, instance):
        valuesNames = range(0, 63)
        dictValues = dict()

        for loc in range(63):
          dictValues[valuesNames[loc]] = instance[loc]
        
        return self.multiclassPerceptron.predict(dictValues) 

class BiasClassifier(object):

    def __init__(self, data):
      #({'bias': xx?, 'value': 0.969158}, False)
        newData = []

        for example in data:
          #(0.969158, False)
          value = example[0] # 0.969158
          label = example[1] # False 
          valueDict = dict() # {}

          valueDict["value"] = value
          valueDict["bias"] = 1
          # if value > 1 : 
          #   valueDict["bias"] = 1
          # else : 
          #   valueDict["bias"] = 0

          newData.append((valueDict , label))

        print(newData)
        self.bP = BinaryPerceptron(newData , 10 )

    def classify(self, instance):
        valueDict = dict()

        valueDict["value"] = instance
        valueDict["bias"] = 1
        
        return self.bP.predict(valueDict)

class MysteryClassifier1(object):

    def __init__(self, data):

        newData = []

        for example in data:
          #example = ((-1.121368,  0.901347), False),
          values = example[0] # (-1.121368,  0.901347)
          label = example[1] # False
          dictValues = dict()
        

          dictValues["squVal"] = (values[1]**2 + values[0]**2)**.5
          # dictValues["val1"] = values[0]
          # dictValues["val2"] = values[1]
          dictValues["bias"] = 1 

          newData.append((dictValues,label))
          
        # print(newData)
        self.BinaryPerceptron = BinaryPerceptron(newData , 1 )

    def classify(self, instance):
        valuesNames = ["squVal","bias"]
        dictValues = dict()
        

        dictValues["squVal"] = (instance[1]**2 + instance[0]**2)**.5
        # dictValues["val1"] = instance[0]
        # dictValues["val2"] = instance[1]
        dictValues["bias"] = 1
        
        return self.BinaryPerceptron.predict(dictValues) 

class MysteryClassifier2(object):

    def __init__(self, data):

        newData = []

        for example in data:
          values = example[0] # 
          label = example[1] # False
          dictValues = dict()

          dictValues["squVal"] = values[2] * values[1] * values[0] 
          dictValues["bias"] = 1 

          newData.append((dictValues,label))
          
        # print(newData)
        self.BinaryPerceptron = BinaryPerceptron(newData , 1 )

    def classify(self, instance):
        valuesNames = ["squVal","bias"]
        dictValues = dict()
        

        dictValues["squVal"] = instance[2] * instance[1] * instance[0]
        dictValues["bias"] = 1
        
        return self.BinaryPerceptron.predict(dictValues) 


