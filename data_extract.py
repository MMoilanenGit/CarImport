
# coding: utf-8

# In[ ]:


import pandas as pd
from sklearn import linear_model


def edit_data(data, age):
    """
    Make corrections to Data
    
    Select only cars by age, we dont want to include old cars but are just iterested cars that are expected to
    come on regular use.
    
    
    
    Return feature and pred data sets
    """
    data.diesel = data.diesel.apply(lambda x: 1 if x > 1 else x)
    data.automatic = data.automatic.apply(lambda x: 1 if x > 1 else x)
    data.four_wd = data.four_wd.apply(lambda x: 1 if x > 1 else x) # Impute later as average 
    data.doors = data.doors.apply(lambda x: 0 if x > 9 else x)     # Impute later as average
    data.mileage = data.mileage.apply(lambda x: 0 if x > 700 else x) # Impute later as average
    data.power_KW = data.power_KW.apply(lambda x: 0 if x > 500 else x)
    
    data = data[(data["car_age"] < age)]
    
    return data


# Create here function for selecting dates based on start and end DAte
# Create that returns train and prediction col

def select_time_period(data,start_date, end_date):
    
    data = data.loc[(data['decision_date'] > start_date) & (data['decision_date'] <= end_date)]
    data['year_month'] = pd.to_datetime(data['decision_date']).dt.strftime('%Y-%m')
    data.drop(['condition_B_N_G', 'registration_date','condition_lowered_A','decision_date','model_extension',
                    'taxation_value'],axis=1, inplace=True)
    
    feature_list = data.columns.drop('car_tax')

    data_pred = data.drop(feature_list, axis=1)
    data_features = data.drop('car_tax', axis=1)
    
    
    return data_features, data_pred



if __name__ == "__main__": 
    data = pd.read_excel("data_with_features.xlsx")
    data = edit_data(data,20)
    data = select_time_period(data, '2012-01-01','2018-12-31')

