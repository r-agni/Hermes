-- THIS CODE WAS RUN ON MindsDB'S DEMO CLOUD

/*
Welcome! This is the MindsDB Cloud SQL Editor.
To get started, check out one of the tutorials in Learning Hub.
Happy Machine Learning!
*/ 

CREATE DATABASE cockroachdb
WITH ENGINE = 'cockroachdb',
PARAMETERS = {
  "host": "marble-caracal-13324.5xj.cockroachlabs.cloud",
  "database": "defaultdb",
  "user": "aditya",
  "password": "XB1A07FP5Gr0jESIsz6tXg",
  "port": "26257"
  };

CREATE ML_ENGINE mindsdb.openai_engine
FROM openai
USING
  api_key = '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';

CREATE MODEL gpt_model
PREDICT answer
USING
    engine = 'openai_engine',
    model_name = 'gpt-4',
    api_key = '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',
    question_column = 'question';

SELECT * FROM cockroachdb.data;

SELECT question, answer
FROM gpt_model
WHERE question = 'What can I do to improve my blood test results?'