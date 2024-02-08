from joblib import load
import sys
import pandas as pd
import numpy as np
import math
from HousePricePredictRecommend.utils.exception import CustomException
from HousePricePredictRecommend.utils.common import load_object, output_within_range
from joblib import load
import os

import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd


class Recommender:
    def __init__(self):
        pass

    def get_similar_houses(propType, loc, furn,  city, bed, Bath, RorS, dataset, n=6):

        # converting the text data to feature vectors

        vectorize = TfidfVectorizer()

        # making input str
        input_str = propType + "   " + loc + "   " + furn + "   " + \
            city + "   " + bed + "   " + Bath + "   " + RorS + "   "

        # adding the input for tfdif
        dataset.loc[len(dataset.index)] = input_str
        # dataset.to_csv("artifacts/demo")

        # vecterization
        feature_vectors = vectorize.fit_transform(dataset["text"])

        # finding cosine similarity
        dataset['distances'] = cosine_similarity(
            feature_vectors, [feature_vectors.toarray()[-1]])

        # this contains the parent itself as the most similar entry, hence n+1 to get n children
        n_largest = dataset['distances'].nlargest(n + 2)

        # Return the top similar houses
        return dataset.loc[n_largest.index[2:]]


class PredictRecommendPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            # print(features["RentOrSale"], "hiii")
            # print(features["RentOrSale"] == "Sale", "hiii")

            if (features["RentOrSale"] == "Rent").all():
                model_path = 'artifacts/training/model.h5'
            else:
                model_path = 'artifacts/training/model_rent.h5'
            preprocessor_path = "artifacts/data_preprocessing/preprocessor.h5"
            print("Before Loading")
            model = load(model_path)
            preprocessor = load(preprocessor_path)
            print("After Loading")
            fea_df = pd.DataFrame(features, columns=['propertyType', 'locality', 'furnishing',
                                                     'city', 'bedrooms', 'bathrooms', 'RentOrSale',  'exactPrice'])
            data_scaled = preprocessor.transform(fea_df)
            preds = model.predict(data_scaled[:, :-1])
            prediction = round(preds[0])
            result = output_within_range(prediction)
            return result

        except Exception as e:
            raise CustomException(e, sys)

    def recommend(self, features):
        try:
            Data_path = "artifacts/recommend_data.csv"
            data = pd.read_csv(Data_path)

            recommend = Recommender
            similar_houses = recommend.get_similar_houses(
                features['propertyType'].loc[0], features['locality'].loc[0], features['furnishing'].loc[0],
                features['city'].loc[0], features['bedrooms'].loc[0], features['bathrooms'].loc[0], features['RentOrSale'].loc[0], dataset=data)

            return similar_houses

        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(self,
                 propertyType: str,
                 locality: str,
                 furnishing: str,
                 city: str,
                 bedrooms: str,
                 bathrooms: str,
                 RentOrSale: str,
                 exactPrice: str):

        self.propertyType = propertyType

        self.locality = locality

        self.furnishing = furnishing

        self.city = city

        self.bedrooms = bedrooms

        self.bathrooms = bathrooms

        self.RentOrSale = RentOrSale

        self.exactPrice = exactPrice

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "propertyType": [self.propertyType],
                "locality": [self.locality],
                "furnishing": [self.furnishing],
                "city": [self.city],
                "bedrooms": [self.bedrooms],
                "bathrooms": [self.bathrooms],
                "RentOrSale": [self.RentOrSale],
                "exactPrice": [self.exactPrice],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":

    # Recommendation test code

    # Getting the data for processing
    # data_transform = DataTransformationRecommend()

    # data, _ = data_transform.initiate_data_transformation_recommend()
    # Data_path = "artifacts\recommend_data.csv"
    # data = pd.read_csv(Data_path)
    # print(data)
    # Data_path = "artifacts/recommend_data.csv"
    # data = pd.read_csv(Data_path)

    # recommend = Recommender
    # similar_houses = recommend.get_similar_houses(
    #     'Multistorey Apartment',  'Narendrapur',  'Semi-Furnished', 'Kolkata',  '3', '3',   'Rent', data, n=6)

    # print(similar_houses[["city", "URLs", "RentOrSale",
    #       "furnishing", "locality", "propertyType"]])
    # print(similar_houses)

    # Prediction test code

    # Load the modelmodel = load_model(os.path.join("model", "model.h5"))

    model = load(os.path.join("artifacts", "training", "model.h5"))
    print("HI", os.path.join("artifacts", "training", "model_rent.h5"))

    print(model.get_params())
    print(model)

    pro = load("artifacts/data_preprocessing/preprocessor.h5")

    predict_pipeline = PredictRecommendPipeline()

    fea = ["Residential House", "Phase 1 Ashiana Nagar", "Semi-Furnished",
           "Patna", 3.0, 3.0, "Rent",  17000.0]
    # Convert fea to a DataFrame
    fea_df = pd.DataFrame([fea], columns=['propertyType', 'locality', 'furnishing',
                                          'city', 'bedrooms', 'bathrooms', 'RentOrSale',  'exactPrice'])

    data_preprocess = pro.transform(fea_df)
    preds = model.predict(data_preprocess[:, :-1])

    print(preds)
