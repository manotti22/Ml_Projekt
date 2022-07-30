
from package.exception import PackageException
import sys
from package.logger import logging
from typing import List
from package.gebilde.ordner_gebilde import DataTransformOrdner, ModelTrainerOrdner
from package.gebilde.schmuck_gebilde import ModelTrainerSchmuck
from package.util.util import load_numpy_array_data,save_object,load_object
from package.gebilde.model_factory import MetricInfoOrdner, MetricInfoOrdner, ModelFactory,GridSearchedBestModel
from package.gebilde.model_factory import evaluate_classification_model



class PackageEstimatorModel:
    def __init__(self, preprocessing_object, trained_model_object):
        """
        TrainedModel constructor
        preprocessing_object: preprocessing_object
        trained_model_object: trained_model_object
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, X):
        """
        function accepts raw inputs and then transformed raw input using preprocessing_object
        which gurantees that the inputs are in the same format as the training data
        At last it perform prediction on transformed features
        """
        transformed_feature = self.preprocessing_object.transform(X)
        return self.trained_model_object.predict(transformed_feature)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"




class ModelTrainer:

    def __init__(self, model_trainer_ordner:ModelTrainerSchmuck, data_transformation_ordner: DataTransformOrdner):
        try:
            logging.info(f"{'>>' * 30}Model trainer log started.{'<<' * 30} ")
            self.model_trainer_ordner = model_trainer_ordner
            self.data_transformation_ordner = data_transformation_ordner
        except Exception as e:
            raise PackageException(e, sys) from e

    def initiate_model_trainer(self)->ModelTrainerOrdner:
        try:
            logging.info(f"Loading transformed training dataset")
            transformed_train_file_path = self.data_transformation_ordner.transformed_train_file_path
            #train_array = load_numpy_array_data(file_path=transformed_train_file_path)
            input_feature_train_df= load_numpy_array_data(file_path=transformed_train_file_path)

            logging.info(f"Loading transformed testing dataset")
            transformed_test_file_path = self.data_transformation_ordner.transformed_test_file_path
            #test_array = load_numpy_array_data(file_path=transformed_test_file_path)
            input_feature_test_df=load_numpy_array_data(file_path=transformed_test_file_path)

            logging.info(f"Splitting training and testing input and target feature")
            x_train,y_train,x_test,y_test = 
            

            logging.info(f"Extracting model config file path")
            model_ordner_file_path = self.model_trainer_ordner.model_ordner_file_path

            logging.info(f"Initializing model factory class using above model config file: {model_ordner_file_path}")
            model_factory = ModelFactory(model_ordner_path=model_ordner_file_path)
            
            
            base_accuracy = self.model_trainer_ordner.base_accuracy
            logging.info(f"Expected accuracy: {base_accuracy}")

            logging.info(f"Initiating operation model selecttion")
            best_model = model_factory.get_best_model(X=x_train,y=y_train,base_accuracy=base_accuracy)
            
            logging.info(f"Best model found on training dataset: {best_model}")
            
            logging.info(f"Extracting trained model list.")
            grid_searched_best_model_list:List[GridSearchedBestModel]=model_factory.grid_searched_best_model_list
            
            model_list = [model.best_model for model in grid_searched_best_model_list ]
            logging.info(f"Evaluation all trained model on training and testing dataset both")
            metric_info:MetricInfoOrdner = evaluate_classification_model(model_list=model_list,X_train=x_train,y_train=y_train,X_test=x_test,y_test=y_test,base_accuracy=base_accuracy)

            logging.info(f"Best found model on both training and testing dataset.")
            
            preprocessing_obj=  load_object(file_path=self.data_transformation_ordner.preprocessed_object_file_path)
            model_object = metric_info.model_object


            trained_model_file_path=self.model_trainer_ordner.trained_model_file_path
            Package_model = PackageEstimatorModel(preprocessing_object=preprocessing_obj,trained_model_object=model_object)
            logging.info(f"Saving model at path: {trained_model_file_path}")
            save_object(file_path=trained_model_file_path,obj=Package_model)


            model_trainer_ordner=  ModelTrainerOrdner(is_trained=True,message="Model Trained successfully",
            trained_model_file_path=trained_model_file_path,
            train_recall= metric_info.train_recall
            test_recall = metric_info.test_recall
            train_accuracy= metric_info.train_accuracy
            test_accuracy=metric_info.test_accuracy
            model_accuracy=metric_info.model_accuracy
            
            )

            logging.info(f"Model Trainer Artifact: {model_trainer_ordner}")
            return model_trainer_ordner
        except Exception as e:
            raise PackageException(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 30}Model trainer log completed.{'<<' * 30} ")



#loading transformed training and testing datset
#reading model config file 
#getting best model on training datset
#evaludation models on both training & testing datset -->model object
#loading preprocessing pbject
#custom model object by combining both preprocessing obj and model obj
#saving custom model object
#return model_trainer_artifact