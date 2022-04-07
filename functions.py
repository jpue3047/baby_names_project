import numpy as np
import pandas as pd
import requests, zipfile
from io import BytesIO
import sys
import os
import config
import excel_format

def loadData():
    """ Go to URL ssa.gov, extract zip file, and save files into folder project  """
    
    # extract zip file and save files in folder project
    url = 'https://www.ssa.gov/oact/babynames/names.zip'
    resp = requests.get(url, allow_redirects=True)

    #extract zip file
    zipfiles = zipfile.ZipFile(BytesIO(resp.content))
    zipfiles.extractall(config.input_path)


def combineFiles(sty, endy):
    """ Combine txt files based on start year and end year
    Args:
        sty (int): start year of analysis
        endy (int): end year of analysis

    Returns:
        data_df: pd.DataFrame 
                DataFrame with all text files combined
    """

    #combine files from start year  until end year
    col = ['name', 'sex', 'births']
    data_df = pd.DataFrame([])
    for year in range(sty, endy + 1):
        pathfile = f'''{config.input_path}/yob{year}.txt''' 

        #read files from path, otherwise skip
        if os.path.exists(pathfile):
            df = pd.read_csv(pathfile, names = col)
            df['year'] = year
            data_df = data_df.append(df)
        else:
            pass
            
    return data_df

def birthAnalysis(df, n):
    """ Generate dataframes showing top n names by gender and birth rate by years selected by user
    Args:
        df (pd.DataFrame): DataFrame with all years to analyze
        n (integer): top n names

    Returns:
        final_df: pd.DataFrame
                    DataFrame showing birth rate by year and top n names by gender
        names_sorted_df: pd.DataFrame
                    DataFrame showing top n names by gender 
    """
    #identify percentage birth by year
    births_df = df.pivot_table('births', index = 'year', columns = 'sex', aggfunc = sum).rename_axis(None, axis = 1).reset_index()
    births_df['per_female'] = births_df.apply(lambda x: x['F']/(x['F']+x['M']), axis = 1)
    births_df['per_male'] = births_df.apply(lambda x: x['M']/(x['F']+x['M']), axis = 1)
    
    #identify top n names by male and female
    names_df = df.groupby(['year','name','sex']).births.sum().reset_index()
    names_df['total_births'] = names_df.groupby(['year','sex'])['births'].transform('sum')
    names_df['prop'] = names_df.apply(lambda x: x['births']/x['total_births'], axis = 1)
    names_df.drop(columns={'total_births'}, inplace=True)

    #sorted top n values by year and sex
    names_sorted_df = names_df.sort_values('births', ascending = False).groupby(['year','sex']).head(n).reset_index(drop = True)
    
    #sort names by year and sex
    top_df = names_sorted_df.groupby([ 'year','sex'])['name'].agg(['unique']).reset_index()
    top_df.rename(columns={'unique':'top_names'}, inplace=True)
    top_df['top_names'] = top_df.apply(lambda x: str(x['top_names'].tolist()).replace("[","").replace("]","").replace("'",""), axis=1)

    #add top n values in list
    top_names_df = top_df.pivot( index=['year'], columns='sex', values='top_names').rename_axis(None, axis=1).reset_index()
    top_names_df.rename( columns ={'F':'top_names_female', 'M':'top_names_male'}, inplace=True)

    #merge birth year data with top n names
    final_df = pd.merge(births_df[['year','per_female', 'per_male']], top_names_df, on ='year', how='left')
    
    return final_df, names_sorted_df

def namesTrend(df):
    """ Create DataFrame for female and male with trend names
    Args:
        df (pd.DataFrame): DataFrame with top n names 

    Returns:
        female_top: pd.DataFrame
                    DataFrame showing female trend names in years selected by user
        male_top: pd.DataFrame
                    DataFrame showing male trend names in years selected by user
    """
    female_top = df[df['sex']=='F'].pivot_table('births', index = 'year', columns ='name', aggfunc = sum).rename_axis(None, axis = 1).reset_index()
    female_top.fillna(0, inplace = True)
    male_top = df[df['sex']=='M'].pivot_table('births', index = 'year', columns ='name', aggfunc = sum).rename_axis(None, axis = 1).reset_index()
    male_top.fillna(0, inplace = True)
    return female_top , male_top

def runAnalysis(sty, endy, n):
    """ Main functions to load and extract zip files, combine files based on years, analysis data, and create excel file with tables and line chart
    Args:
        sty (int): start year of analysis
        endy (int): end year of analysis
        n (integer): top n names
    """
    #load and extract zip file
    loadData()

    #combine text files
    df = combineFiles(sty,endy)

    #create Birth Analysis
    births_df, names_df = birthAnalysis(df, n)
    
    #create dataframe for top names
    female_top, male_top = namesTrend(names_df)
    
    #creaate output folder in project directory
    config.make_output_dir()

    #create excel file
    writer = pd.ExcelWriter(config.output_path +"/Baby Name Analysis.xlsx", engine = 'xlsxwriter')
    workbook = writer.book

    #copy dataframes in excel file and format files and create line charts 
    excel_format.format_birth(births_df, 'Birth_Data', workbook, writer)
    excel_format.format_trend(female_top, 'Female_Trend',  workbook, writer,'Trend Top Female Name')
    excel_format.format_trend(male_top, 'Male_Trend',  workbook, writer,'Trend Top Male Name')
    
    #save excel file and close 
    workbook.close()
    writer.save()