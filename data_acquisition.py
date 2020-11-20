
# coding: utf-8

# In[1]:


import openpyxl
import glob
import pandas as pd
import re

def from_sheets(file):
    '''
    File comes yearly. Excel file has 13 sheets, first is Description and other 12 sheets are for months.
    Function from_sheet concatenates monthly sheets into one dataframe.
    '''
    sheet_names = pd.ExcelFile(file).sheet_names[1:]
    
    one_from_file= pd.DataFrame(pd.read_excel(file, sheet_name=sheet_names[0], header=0, convert_float=True).drop(0,axis=0))
    one_from_file['Käyttöönottopvä'] = one_from_file['Käyttöönottopvä'].astype('datetime64[ns]')
    one_from_file['Päätöspäivä'] = one_from_file['Päätöspäivä'].astype('datetime64[ns]')
    
    
    for sheet in sheet_names[1:]:
    
        data = pd.read_excel(file, sheet_name=sheet, header=0, convert_float=True).drop(0,axis=0)
        data['Käyttöönottopvä'] = data['Käyttöönottopvä'].astype('datetime64[ns]')
        data['Päätöspäivä'] = data['Päätöspäivä'].astype('datetime64[ns]')
        one_from_file = one_from_file.append(data)
        
    return one_from_file




#for year in car_files2:
def all_data_from_files():
    '''
    Function takes year files from source folder, and concatenates into one Dataframe.
    
    
    '''
    
    car_files = []
    for file in glob.glob("*.xls"):
        car_files.append(file)
    car_files
    
    data_1st_year = from_sheets(car_files[0])
    
    for year in car_files[1:]:
        
        
        data = from_sheets(year)
        
        data_1st_year = data_1st_year.append(data)
        
        
    data_1st_year["Autovero"] = pd.to_numeric(data_1st_year["Autovero"], errors='coerce')
    data_1st_year["Ajokm/1000"] = pd.to_numeric(data_1st_year["Ajokm/1000"], errors='coerce')
    data_1st_year["Verotusarvo"] = pd.to_numeric(data_1st_year["Verotusarvo"], errors='coerce')    
    
    
    return data_1st_year
 
    
def engine_power(col):
    '''
    Extracts engine power from string
    '''
    #x = re.findall('\d+[KW]', str(col)) # Returns also 4WD
    x = re.findall(' \d+[K]', str(col)) # This works, matches numbers followed by K
    x = re.sub('[^0-9]', '', str(x))
    return(x)

def engine_size(col):
    '''
    Extracts engine size from string
    '''
    x = re.findall('\d\.\d', str(col)) # This works perfectly
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
    Column [Mallin tarkennin] has information about a car, for example power, number of doors, size of engine etc. 
    in text format. 
    
    This function extracts information from text, and creates new columns on the information.
    
    Data cleaning and renaming of columns to english is included.
    '''
    # Clean data 
    #data['Mallin tarkennin'] = data['Mallin tarkennin'].apply(lambda x: x.replace(",", "."))
    data['Mallin tarkennin'] = data['Mallin tarkennin'].str.replace(",",".")

    data['Mallin tarkennin'] = data['Mallin tarkennin'].str.upper() # All letters to capital
    data['Mallin tarkennin'] = data['Mallin tarkennin'].map(lambda x: re.sub(' KW', 'KW', str(x))) # Remove whitespace before KW
    
    # New columns
    data['diesel'] = data['Mallin tarkennin'].str.count(pat=' D ') # Look for D, if found prints 1
    data['aut'] = data['Mallin tarkennin'].str.count(pat='AUT') # Look for AUT, if found print 1
    data['neliveto'] = data['Mallin tarkennin'].str.count(pat='4WD') # Look for 4WD, if found print 1
    
    data['year_month'] = data["Päätöspäivä"].dt.strftime('%Y-%m')
    data['year'] = data['Päätöspäivä'].dt.year # Year column
    data['month'] = data['Päätöspäivä'].dt.month # Month column
    data['car_age'] = (data['Päätöspäivä']-(data['Käyttöönottopvä']))/ pd.Timedelta(365, unit='d') # Car age
    data['engine_powers'] = data['Mallin tarkennin'].apply(engine_power) # Engine power in KW:s
    data['engine_size'] = data['Mallin tarkennin'].apply(engine_size) # Engine size in cm
    data['doors'] = data['Mallin tarkennin'].apply(door_number)
    data['extract_D_one'] = data['Mallin tarkennin'].apply(extract_D_one)
    
    # Correct data types
    data['engine_powers'] = pd.to_numeric(data['engine_powers'])
    data['engine_size'] = pd.to_numeric(data['engine_size'])
    data['doors'] = pd.to_numeric(data['doors'])

    # Rename columns to english
    col_names_to_english = ["mileage","car_tax","condition_lowered_A","condition_B_N_G","registration_date", "model","model_extension", 
                            "brand","decision_date","taxation_value","diesel", "automatic", "four_wd", "year_month","year","month",
                            "car_age","power_KW","engine_size","doors","extract_D"]
    data.columns = col_names_to_english
    
    
    return(data)


if __name__ == "__main__":

    data = all_data_from_files()
    data = feature_creation(data)
    data.to_excel(r'data_with_features.xlsx', index = False)

