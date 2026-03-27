Note- data folder and artifact fodler can be ignored as they are used while running the codes indivisually in local.
* this project is implemented in 2 units :
  
* in first unit when user commit any changes in this repo , pipeline.py code get triggered by github Actions by reading the      workflow/main.yml.
* pipeline is containing the 5 steps, DataPreprocessing,ModelTraining,ModelEvaluation,AccuracyCheck and ModelRegistry.
* if accuracy is more than 80% then only ModelRegistry step will ecexute otherwise pipeline will stop after ModelEvaluation     step.

* after completion of the pipeline, Model get registered in sagemaker model registry with version (e.g model-name ,v1) with     "Pending Approval" step.

* in second unit i have designed the EventBridge based artichecture :
* a rule is created in EventBridge which is reading the sagemaker model approval status, if mode in approved from sagemaker     model registry section EventBridge will send a trigger to lambda function and lambda function will trigger the endpoint       deployment.

  * we can call the endpoint by simple python code or by some other mechanism and can get the prediction.


    ################### Thank You ##################
