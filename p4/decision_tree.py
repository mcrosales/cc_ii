import sys

from pyspark import SparkContext, SparkConf, SQLContext

from pyspark.ml import Pipeline
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.feature import IndexToString,StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler

from pyspark.ml.evaluation import BinaryClassificationEvaluator

if __name__ == '__main__':

    #Creacion del contexto de Spark
    conf = SparkConf().setAppName('Mario Cesar Rosales Castro -> Practica 4 - Decision Tree')  
    sc = SparkContext(conf=conf)

    #Creacion del contexto SQL
    sqlc = SQLContext(sc)
   
    bigFile = sqlc.read.csv("/user/ccsaK047942/ECBDL14_IR2.data",sep=",", inferSchema = True)
    #Columnas correctas
    filteredC_small_training = bigFile.select('_c613','_c258','_c267','_c272','_c410','_c520','_c631')

    #Conversion del conjunto de datos a formato legible
    assembler = VectorAssembler(inputCols=['_c613', '_c258', '_c267', '_c272', '_c410', '_c520'], outputCol='features')
    dataset = assembler.transform(filteredC_small_training)
    dataset = dataset.selectExpr('features as features', '_c631  as label')
    dataset = dataset.select('features', 'label')


    # Index labels, adding metadata to the label column.
    # Fit on whole dataset to include all labels in index.
    labelIndexer = StringIndexer(inputCol='label', outputCol='indexedLabel').fit(dataset)
    # Automatically identify categorical features, and index them.
    # We specify maxCategories so features with > 4 distinct values are treated as continuous.
    featureIndexer = VectorIndexer(inputCol='features', outputCol='indexedFeatures', maxCategories=2).fit(dataset)

    # Split the data into training and test sets (30% held out for testing)
    (trainingData, testData) = dataset.randomSplit([0.7, 0.3])

    # Train a DecisionTree model.
    dt = DecisionTreeClassifier(labelCol='indexedLabel', featuresCol='indexedFeatures')

    # Chain indexers and tree in a Pipeline
    pipeline = Pipeline(stages=[labelIndexer, featureIndexer, dt])

    # Train model.  This also runs the indexers.
    model = pipeline.fit(trainingData)

    # Make predictions.
    predictions = model.transform(testData)

    # Select example rows to display.
    predictions.select('prediction', 'indexedLabel', 'features').show(10)

    # Select (prediction, true label) and compute test error
    evaluator = MulticlassClassificationEvaluator(labelCol='indexedLabel', predictionCol='prediction', metricName='accuracy')
    accuracy = evaluator.evaluate(predictions)
    print('Test Error = %g ' % (1.0 - accuracy))
    
    sc.stop()