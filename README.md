# The TemporalQA system
A KG-QA system over Wikidata for temporal or simple questions

# Install
```
pip install pycorenlp
pip install pandas
pip install numpy
pip install requests
pip install functools

```

# Usage
First make sure you download Stanford CoreNLP server.  See [the instructions here](https://stanfordnlp.github.io/CoreNLP/download.html) for how to do that.

Then navigate to the path where you unzipped the JAR files folder. Navigate inside the folder and execute the following command on the command prompt:
```
>>>java -mx6g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000
```

Finally navigate to the path of the folder of the TemporalQA system and execute the following command on the command prompt:
```
>>> python final.py 0.1 7 which position did ronaldo play in 2006
[('Manchester United F.C.', [[0.6746084314651151, 'http://www.wikidata.org/entity/Q18656']]), ('5279', [[0.4968944696804637, '5279']]), ('forward', [[0.48359925275681037, 'http://www.wikidata.org/entity/Q280658']]), ('Premier League', [[0.4734814177532328, 'http://www
.wikidata.org/entity/Q9448']]), ('Portugal', [[0.4629537816221213, 'http://www.wikidata.org/entity/Q45']]), ('24753', [[0.45915052862181704, '24753']]), ('201200', [[0.44875024645203915, '201200']])]
```


The first parameter set to 0.1 in the example above is the threshold of TAGME, which influences the result of named-entity recognition.
The second parameter set to 7 in the example above is the number of predicates of wikidata. The more the “Predicate_num” is set, the higher the recall of the problem is while the lower the precision is.
The third parameter set to which position did ronaldo play in 2006 is the question you ask.

The result of the example are Manchester United F.C., forward, Portugal, etc. Each answer has a confidence and link to Wikidata.

