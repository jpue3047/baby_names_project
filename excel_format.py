from pandas import ExcelWriter
import config


def percentage(workbook):
    """Format cell in excel shoing percentage
    Args:
        workbook (string): Workbook name

    Returns:
        Cell with percentage format
    """
    return workbook.add_format({'num_format': '0.00%'})

def header_format(workbook):
    """ Define header format
    Args:
        workbook (excel element): Workbook 

    Returns:
        Cells with defined format
    """
    return workbook.add_format({
        'bold': True,
        'fg_color': '#0081C6',
        'font_color': 'white',
        'text_wrap': True,
        'align': 'center',
        'valign': 'vcenter'    })
  

def format_birth(df, sheet_name, workbook, writer):
    """ Copy DataFrame to excel tab and format data
    Args:
        df (pd.DataFrame): DataFrame to cooy in excel tab
        sheet_name (string): Sheet name in excel file. Add string in quotes
        workbook (string): Workbook name
        writer (string):  Writer name
    """
    #change columns name
    df.rename(columns= config.col_name, inplace=True)
    
    #write dataframe to excel worksheet
    df.to_excel(writer, sheet_name = sheet_name, index=False)

    worksheet = writer.sheets[sheet_name]

    #set columns width
    worksheet.set_column('A:A', 5, None)
    worksheet.set_column('B:C', 10, percentage(workbook))
    worksheet.set_column('D:E', 60, None)


    #format headers
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format(workbook))


def format_trend(df, sheet_name, workbook, writer, chart_title):
    """Copy DataFrame to excel tab and create chart line with multiples series
    Args:
        df (pd.DataFrame): DataFrame to cooy in excel tab
        sheet_name (string): Sheet name in excel file. Add string in quotes
        workbook (string): Workbook name
        writer (string):  Writer name
        chart_title (string): Chart Title. Add string in quotes
    """
    #write dataframe to excel worksheet
    df.to_excel(writer, sheet_name = sheet_name, index=False)

    worksheet = writer.sheets[sheet_name]

    #create chart object
    chart = workbook.add_chart({'type': 'line'})

    #add multiple series to chart line
    l = len(df) + 1
    col = len(df.columns) 
      
    for i in range(col - 1):   
        chart.add_series({ 'name': [sheet_name, 0, i + 1 ],
            'categories': [sheet_name, 1, 0, l - 1, 0],
            'values': [sheet_name, 1, i + 1, l- 1, i +1 ]})

    #set chart title
    chart.set_title ({'name': chart_title})

    #set chart size
    chart.set_size({'width': 1300,'height': 800})
    
    #insert chart into the worksheet
    worksheet.insert_chart('A1', chart)