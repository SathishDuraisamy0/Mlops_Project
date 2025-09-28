import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.common_function import read_yaml,load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:

    def __init__(self,train_path,test_path,processed_dir,config_path):
        self.train_path =train_path
        self.test_path =test_path
        self.processed_dir=processed_dir

        self.config=read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self,df):
        try:
            logger.info("Start point for data process")
            logger.info("Dropping the columns")
            df.drop(columns=['Unnamed: 0','Booking_ID'],inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols=self.config["data_processing"]["categorical_columns"]
            num_cols=self.config["data_processing"]["numerical_columns"]

            logger.info("Applying label encode")
            Label_encoder= LabelEncoder()
            mapping={}

            for col in cat_cols:
                df[col]=Label_encoder.fit_transform(df[col])
                mapping[col]={label:code for label,code in zip(Label_encoder.classes_,Label_encoder.transform(Label_encoder.classes_))}
            
            logger.info ("Label Mapping: ")
            for col,mapping in mapping.items():
                logger.info(f"{col}:{mapping}")
            
            logger.info("Skewness Handling")

            skew_threshold=self.config["data_processing"]["skewness_threshold"]
            skewness=df[num_cols].apply(lambda x:x.skew())

            for column in skewness[skewness > skew_threshold].index:
                df[column]=np.log1p(df[column])
                return df
            

        except Exception as e:
            logger.error(f"Erro during preprocessing step {e}")
            raise CustomException ("Error while preprocess data",e)
        
    def balance_data(self,df):
        try:
            logger.info("Handling imbalance data")
            x=df.drop(columns='booking_status')
            y=df['booking_status']

            smote=SMOTE(random_state=42)

            x_res,y_res=smote.fit_resample(x,y)

            balanced_df=pd.DataFrame(x_res,columns=x.columns)
            balanced_df["booking_status"] =y_res

            logger.info("Data balance sucessfully")

            return balanced_df
        
        except Exception as e:
            logger.error(f"Erro during balancing step {e}")
            raise CustomException ("Error while balancing data",e)
    
    def feature_selection(self,df):
        try:
            logger.info("Starting our feature selection")

            X=df.drop(columns='booking_status')
            y=df['booking_status']

            model =RandomForestClassifier(random_state=42)

            model.fit(X,y)

            Feature_importance=model.feature_importances_
            feature_importance= pd.DataFrame({
                                'feature':X.columns,
                                'importance': Feature_importance})
            
            top_importance_feature=feature_importance.sort_values(by="importance",ascending=False)
            num_features_to_select =self.config["data_processing"] ["no_of_features"]

            top_10_features=top_importance_feature["feature"].head(num_features_to_select).values

            logger.info(f"Top 10 features are selected: {top_10_features}")

            top_10_df = df[top_10_features.tolist() + ["booking_status"]]

            logger.info("Feature slection completed sucesfully")

            return top_10_df

        except Exception as e:
                logger.error(f"Error during feature selection step {e}")
                raise CustomException("Error while feature selection", e)

    def save_data(self,df,file_path):
        try:
            logger.info("saving final data")

            df.to_csv(file_path,index=False)

            logger.info(f"data saved succesfully to {file_path}")

        except Exception as e:
                logger.error(f"Error data saved step {e}")
                raise CustomException("Error data saved", e)

    def process(self):
        try:
            logger.info("Loading data from RAW directory")

            train_df= load_data(self.train_path)
            test_df= load_data(self.test_path)

            train_df=self.preprocess_data(train_df)
            test_df=self.preprocess_data(test_df)

            train_df=self.balance_data(train_df)
            test_df=self.balance_data(test_df)

            train_df=self.feature_selection(train_df)
            test_df=test_df[train_df.columns]

            self.save_data(train_df,PROCEESSED_TRAIN_DATA_PATH)
            self.save_data(test_df,PROCEESSED_TEST_DATA_PATH)

            logger.info("Data processing is done")

        except Exception as e:
                logger.error(f"Error preproceeing pipeline {e}")
                raise CustomException("Error preproceeing pipeline", e)

if __name__=="__main__":
     processer=DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCEESSED_DIR,CONFIG_PATH)
     processer.process()


            
