#all important imports
import pyspark
import json
import sys
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml.regression import LinearRegression
from pyspark.ml.linalg import Vectors
#make a new spark context session
sc = SparkContext.getOrCreate()
spark = SparkSession(sc)

frame = spark.createDataFrame([(0.0,0.0,Vectors.dense(0,0,0))], ["label", "weight", "features"])

try:
    user = sys.argv[1]
except:
    user = input("Username: ")

path = "C:\\Users\\Aaron\\Documents\\CPSC 454\\454 project\\" #SET THIS
# Load training data
with open(path + user + ".json") as file:
    jsonData = json.load(file)

for i, key in enumerate(jsonData):
    newRow = spark.createDataFrame([(float(i),1.0,Vectors.dense(jsonData[key]['count'],jsonData[key]['retweet'],jsonData[key]['favorite'])),], ["label", "weight", "features"])
    frame = frame.union(newRow)
#addEnd = spark.createDataFrame((["label", "weight", "features"],))
#frame = frame.union(addEnd)
training = frame
    #spark.createDataFrame([
    #(1.0, 2.0, Vectors.dense(1.0, 20, 40, 50)),
   #(0.0, 2.0, Vectors.dense(1.0, 40, 50, 60))],
    #    ["label", "weight", "features"])

##should be this format, the if the data format was replies, favs, rts the vector would look like
##spark.createDataFrame([
##    (0.0, 0.0, Vectors.dense(replies, rts, favs,)),
##   (1.0, 0.0, Vectors.dense(replies, rts, favs))],
##        ["label", "weight", "features"])

#shows the data
training.show()

#make the linear regression model
lr = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

# Fit the model
lrModel = lr.fit(training)

# Print the coefficients and intercept for linear regression
print("Coefficients: %s" % str(lrModel.coefficients))
print("Intercept: %s" % str(lrModel.intercept))

# Summarize the model over the training set and print out some metrics
trainingSummary = lrModel.summary
print("numIterations: %d" % trainingSummary.totalIterations)
print("objectiveHistory: %s" % str(trainingSummary.objectiveHistory))
trainingSummary.residuals.show()
print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
print("r2: %f" % trainingSummary.r2)
