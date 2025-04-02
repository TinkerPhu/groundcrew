import mlflow

mlflow.set_tracking_uri("http://htkasrv120:5000")
mlflow.set_experiment("PHU_demo")

mlflow.start_run()
mlflow.log_metric("m1", 1.2)

mlflow.end_run()