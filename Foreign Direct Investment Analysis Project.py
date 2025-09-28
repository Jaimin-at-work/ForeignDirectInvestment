


import pandas as pd
import matplotlib.pyplot as plt



FDI = pd.read_csv("FDI data (1).csv")
FDI.style.set_caption("Amount in US$ Millions)").format(precision=2)

Year = ['2000-01', '2001-02', '2002-03', '2003-04', '2004-05',
       '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11',
       '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17']
Sectors = ['Sector']

#Extracting Detailed Information
FDI.info()

#Checking the null Values
FDI.isnull().sum()

#Creating Average Exchange Rate list  :- Rbi website
Rates = [45.68,47.69,48.39,45.95,44.93,44.27,45.24,40.26,45.99,
         47.44,45.56,47.92,54.40,60.50,61.14,65.46,67.07]

#USD to INR
def multiply_columns(df, col_list, num):
    for col in col_list:
        df[col] = df[col] * Rates[col_list.index(col)]/10
    return df

FDI_InUSD=FDI.copy()
FDI_02 = multiply_columns(FDI, Year, Rates)

#FDI INFLOWS (Amount in ₹ Crores)
FDI_02.style.set_caption("FDI INFLOWS (Amount in ₹ Crores)").format(precision=2)

# Unpivoting melt Dataframe
melt = pd.melt(FDI_InUSD, id_vars = Sectors, value_vars = Year, var_name='Year',
    value_name='FDI(US$ Million)',ignore_index=True)
print(melt)


#Unpivoting melt01 Dataframe
melt01 = pd.melt(FDI_02, id_vars = Sectors, value_vars = Year, var_name='Year',
    value_name='FDI(₹ Crores)',ignore_index=True)
melt01=round(melt01,2)
print(melt01)

# Merging the FDI(US$ Million) column of melt Dataframe into melto1 Dataframe
Merged=melt01.merge(melt,how='left')
print(Merged)


#Sorting the Sectors and Year columns
Sorted = Merged.sort_values(['Sector','Year'], ignore_index=True)
print(Sorted)

print("\nStats for Sectors\n",'-'*65, sep='')
print(pd.DataFrame(Sorted.groupby('Sector').describe().loc[:,:]).transpose())


#Repalcing some Long values of Sector Column to Short form
Sorted = Sorted[['Sector','FDI(₹ Crores)', 'FDI(US$ Million)'
                 ,]].replace(["CONSTRUCTION DEVELOPMENT: Townships, housing, built-up infrastructure and construction-development projects"
                              ,"SERVICES SECTOR (Fin.,Banking,Insurance,Non Fin/Business,Outsourcing,R&D,Courier,Tech. Testing and Analysis, Other)"
                              ,'TEA AND COFFEE (PROCESSING & WAREHOUSING COFFEE & RUBBER)']
                             ,["CONSTRUCTION DEVELOPMENT","SERVICES SECTOR",'TEA AND COFFEE'])


#Grouping by Sector column to find Total FDI Inflow per Sector from FY2000-01 to FY2016-17
Sectorwise_fdi = Sorted.groupby('Sector').sum()
Sectorwise_fdi.sort_values(by='FDI(US$ Million)',ascending=False)

Sectorwise_fdi.plot(kind='bar',y='FDI(₹ Crores)',figsize = (25,7), legend= True, title='SECTOR_WISE FDI INFLOWS',ylabel='FDI(₹ Crores)')
plt.show()
Sectorwise_fdi.plot(kind='bar',y='FDI(US$ Million)',figsize = (25,7), legend= True, title='SECTOR_WISE FDI INFLOWS' ,ylabel='FDI(US$ Million)')
plt.show()

#Top 10 and bottom 10 sectors
Top_10_Sectors = Sectorwise_fdi.nlargest(10,['FDI(₹ Crores)'])
#Calculating percentage-wise FDI share among top 10 sectors and among all sectors
Total_fdi = round(melt01['FDI(₹ Crores)'].sum(),2)
Sum = Top_10_Sectors['FDI(₹ Crores)'].sum()
Top_10_Sectors['In %age'] = round(Top_10_Sectors['FDI(₹ Crores)']/Sum*100,2)
Top_10_Sectors['%age to Total Inflows'] = round((Top_10_Sectors['FDI(₹ Crores)']/Total_fdi)*100,2)
print(Top_10_Sectors)

##Creating bar chart to visualise Total FDI inflow in top 10 sectors using Matplotlib

plt.figure(figsize=(15,5))
plt.barh(Top_10_Sectors.index,Top_10_Sectors['FDI(₹ Crores)'])
plt.title('SECTORS ATTRACTING HIGHEST FDI INFLOWS')
plt.xlabel('FDI(₹ Crores)')
plt.ylabel('Top Sectors')
plt.show()

#Creating pie chart to visualise percentage share of FDI among top 10 sectors using Matplotlib

plt.figure(figsize=(20,8))
plt.pie(Top_10_Sectors['FDI(₹ Crores)'],labels=Top_10_Sectors.index,autopct='%1.1f%%',shadow=True,startangle=90)
plt.axis('equal')
plt.title('SHARE AMONG TOP 10 SECTORS ATTRACTING HIGHEST FDI INFLOWS')
plt.show()

'''
From the above Chart, we can understand that Service Sector Managed to Attract highest FDI which was ₹316347.59Cr greater than any other Sector and among top 10 Sectors it has 27.7% share and among all it has 17.65%.
'''

#Calculating share among Bottom sectors and as a whole
Bottom_5_Sectors = Sectorwise_fdi.nsmallest(5,['FDI(₹ Crores)'])
Sum = Bottom_5_Sectors['FDI(₹ Crores)'].sum()
Bottom_5_Sectors['In %age'] = round(Bottom_5_Sectors['FDI(₹ Crores)']/Sum*100,2)
Bottom_5_Sectors['%age to Total Inflows'] = round((Bottom_5_Sectors['FDI(₹ Crores)']/Total_fdi)*100,3)
print(Bottom_5_Sectors)


#Creating bar chart to visualise Total FDI inflow in Bottom 5 sectors using Matplotlib

plt.figure(figsize=(15,8))
plt.barh(Bottom_5_Sectors.index,Bottom_5_Sectors['FDI(₹ Crores)'])
plt.title('SECTORS ATTRACTING LOWEST FDI INFLOWS')
plt.xlabel('FDI(₹ Crores)')
plt.ylabel('Bottom Sectors')
plt.show()

#Creating pie chart to visualise percentage share of FDI among top 10 sectors using Matplotlib

plt.figure(figsize=(20,8))
plt.pie(Bottom_5_Sectors['FDI(₹ Crores)'],labels=Bottom_5_Sectors.index,autopct='%1.1f%%',shadow=True,startangle=90)
plt.axis('equal')
plt.title('SHARE AMONG BOTTOM 5 SECTORS ATTRACTING FDI INFLOWS')
plt.show()

'''Among Bottom 5 sectors, Coir has the lowest FDI of ₹21.64Cr having only 4.4% share among bottom 5 sectors and among all it has only 0.001208%
'''

#Creating Dataframe
melt02 = melt01[['Year', 'FDI(₹ Crores)']]
melt02=round(melt02.groupby('Year').sum(),2)
#reating new column of % growth over previous year
melt02['% growth over previous year'] = round(melt02.pct_change()*100,2)
print('\n'+"*"*8+"Details on Variation of FDI INFLOW Year-wise"+'*'*8) #Year-wise FDI Inflow
melt02.fillna('-')

#plotting to show Year by Year FDI Inflow
melt02.plot.line(y='FDI(₹ Crores)',figsize=(15,15))
plt.ylabel('FDI(₹ Crores)')
plt.title('FDI Year by Year Inflow')
plt.show()


