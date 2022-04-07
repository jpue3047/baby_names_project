# DataSet
United States Social Security Administration (SSA) has available data of frecuency of baby names from 1880 until present.
http://www.ssa.gov/oact/babynames/html

# Data Analysis
Download zip file from SSA UR, extract zip file, and saves text files in working directory.
Create DataFrame based on time frame defined by user (sty and endy).For this analysis I use data from 2010 to 2020.
Find the proportion of babies by gender.
Find top n names by gender ( n is defined by user). I use top 10 names.
Visualize top n names by gender.
Create excel file with analysis. Check folder "Output"

# Scripts
Main Script: main.py

Supportive Scripts: 
  config.py : contains path files and function to create output folder
  excel_format.py : contains functions related to excel formatting
  functions.py: contains functions related to data wrangling

Output file: Output/ Baby Names Analysis.xlsx
