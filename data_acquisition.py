
# coding: utf-8

# In[3]:


import openpyxl
import glob
import pandas as pd
import re

def from_sheets(file):
    '''
    Source data includes one full year in one file. 
    
    Yearly Excel file has 13 sheets, first is Description and other 12 sheets are for months.
    Function from_sheet concatenates monthly sheets into one dataframe, and thus returns Dataframe of one full year.
    
    
    '''
    #Skip Description sheet
    sheet_names = pd.ExcelFile(file).sheet_names[1:]
    
    year_file = pd.DataFrame()
    
    for sheet in sheet_names:
        
        # Use converter for Dates columns into strings, because as in few sheets were saved as numbers, and gave date 1970-01-01
        data = pd.read_excel(file, sheet_name=sheet, header=0, converters={'Käyttöönottopvä':str,'Päätöspäivä':str}).drop(0,axis=0)
        year_file = year_file.append(data)
        
    return year_file


def all_data_from_files():
    '''
    Merge all yearly Excel files from working directory into one Dataframe.
    
    '''
    
    car_files = []
    for file in glob.glob("*.xls"):
        car_files.append(file)
    car_files
    
    #data_1st_year = from_sheets(car_files[0])
    data_years = pd.DataFrame()
    
    for year in car_files:
        
        data = from_sheets(year)
        data_years = data_years.append(data)
    
    return data_years
 
    
def engine_power(col):
    '''
    Extracts engine power from string
    '''
    #x = re.findall('\d+[KW]', str(col)) 
    x = re.findall(' \d+[K]', str(col)) 
    x = re.sub('[^0-9]', '', str(x))
    return(x)

def engine_size(col):
    '''
    Extracts engine size from string
    '''
    x = re.findall('\d\.\d', str(col)) 
    x = re.sub('[^0-9.]','', str(x))
    return(x)

def door_number(col):
    '''
    Extracts number of doors from string
    '''
    x = re.findall(' \d+[D]', str(col))
    x = re.sub('[^0-9.]','', str(x))
    return(x)

def extract_D_one(col):
    '''
    Format for D tag, is sometimes attached to engine size, "1.9D". This function transforms as
    "1.9 D", so diesel tag in function feature_creation works in all cases.
    '''
    x = re.findall('\d\.\d[A-Z]+', str(col))
    x = re.sub('[0-9.]',"", str(x)).strip("[']")
    
    
    return(x)

def feature_creation(data):
    '''
    This function extracts information from text in column model_extension, and creates new columns on the information.
    
    For Example in column model_extension:
    "2.0 D 5D MA 4WD AUT 150KW", we extract information to new columns
    engine_size = 2.0
    diesel = 1
    automatic = 1
    four_wd = 1
    doors = 5
    power_KW = 150
    

    Columns are renamed and data types are changed
    '''
    english_col_names = ["brand","model", "model_extension","condition_B_N_G","decision_date","registration_date","mileage","taxation_value","car_tax","condition_lowered_A"]
    
    data.columns = english_col_names
    
    data["car_tax"] = pd.to_numeric(data["car_tax"], errors='coerce')
    data["mileage"] = pd.to_numeric(data["mileage"], errors='coerce')
    data["taxation_value"] = pd.to_numeric(data["taxation_value"], errors='coerce') 
    
    data['registration_date'] = data['registration_date'].astype('datetime64[ns]')
    data['decision_date'] = data['decision_date'].astype('datetime64[ns]')
    
    
    # Clean data 
    data['model_extension'] = data['model_extension'].str.replace(",",".")
    data['model_extension'] = data['model_extension'].str.upper() # All letters to capital
    data['model_extension'] = data['model_extension'].map(lambda x: re.sub(' KW', 'KW', str(x))) # Remove whitespace before KW
    
    # New columns
    data['diesel'] = data['model_extension'].str.count(pat=' D ') # Look for D, if found prints 1
    data['automatic'] = data['model_extension'].str.count(pat='AUT') # Look for AUT, if found print 1
    data['four_wd'] = data['model_extension'].str.count(pat='4WD') # Look for 4WD, if found print 1
    data['car_age'] = (data['decision_date']-(data['registration_date']))/ pd.Timedelta(365, unit='d') # Car age
    data['power_KW'] = data['model_extension'].apply(engine_power) # Engine power in KW:s
    data['engine_size'] = data['model_extension'].apply(engine_size) # Engine size in cm
    data['doors'] = data['model_extension'].apply(door_number) # Number of doors
    
    data['extract_D_one'] = data['model_extension'].apply(extract_D_one).str.count(pat='D') #Extract from col model_extension, add 1 if D found
    data["diesel"] = data["diesel"].add(data["extract_D_one"]) # Add 1 to diesel column
    data = data.drop(["extract_D_one"], axis=1)
    
    
    
    # Correct data types
    data['power_KW'] = pd.to_numeric(data['power_KW'])
    data['engine_size'] = pd.to_numeric(data['engine_size'])
    data['doors'] = pd.to_numeric(data['doors'])
    
    return(data)   



if __name__ == "__main__":

    data = all_data_from_files()
    data = feature_creation(data)
    data.to_excel(r'data_with_features.xlsx', index = False)

