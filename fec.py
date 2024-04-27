# import the necessary libraries
from pyforest import *
import numpy_financial as npf
from dateutil.relativedelta import relativedelta
from datetime import date
import pandas as pd 

# get data from excel function
def get_data_from_excel(sheet, excelFileName):
    path_excel = excelFileName 
    df = pd.read_excel(
        io = path_excel,
        engine = 'openpyxl',
        sheet_name = sheet)
    return df

# function for process
def process(excel_name, fec='FEC', Param='Param'): 
    # read in excel
    param = get_data_from_excel(Param, excel_name)

    # assign variables to the parameters
    date = param['Date'][0]
    company = param['Entreprise'][0]
    montantcash = param['Cash'][0]

    # read in FEC or read in as csv 
    df = get_data_from_excel(fec, excel_name)
        
    # sort df by date
    df.sort_values(by = 'EcritureDate', inplace = True, ascending = True)
    # get 10 largest txs
    df['Montant'] = df['Montant'].str.replace(',', '.').astype(float)
    big10 = df.nlargest(n=10, columns=['Montant'])
    # get cash acct convert to str  Commence par 531 pas contains
    df['CompteNum'] = df['CompteNum'].astype(str)
    cash = df[df['CompteNum'].str.contains('531')]
    # calculate progressive cash account
    # if cash n+1 > n-1 flag those 2 txs
    # add if for dates if they are all the same
    if (cash.EcritureDate.eq(cash.EcritureDate.iloc[0]).all()) == True: 
        cash['AcctEspeces'] = 0
    else:
        cash['AcctEspeces'] = cash['Montant'].shift(-1)>cash['Montant']
    # get cash tx larger than 5K
    hcash = cash.loc[(df['Montant'] > montantcash)]
    # get total cash txs
    cash['Total Toutes Especes'] = cash['Montant'].sum()
    # get TVA FR and MC and compare tva amount with purchase amount
    tvafr = df[df['CompteNum'].str.contains('445662')]
    tvafr = tvafr.loc[tvafr['Montant'] > tvafr['Montant'][-1]]

    tvamc = df[df['CompteNum'].str.contains('445661')]
    tvamc = tvamc.loc[tvamc['Montant'] > tvamc['Montant'][-1]]

    # move the different dfs to different excel sheets
    writer = pd.ExcelWriter(f'FEC_{company}_{date}.xlsx', engine='xlsxwriter')
    tvafr.to_excel(writer, sheet_name = 'TVA FR')
    tvamc.to_excel(writer, sheet_name = 'TVA MC')
    big10.to_excel(writer, sheet_name = '10+ Operations')
    hcash.to_excel(writer, sheet_name = f'Especes {montantcash}+')
    cash.to_excel(writer, sheet_name = 'Compte Cash')
    
    writer.save()

en = 'fec.param.xlsx'

process(en)
