# -*- coding: utf-8 -*-
"""Team7_Data_analysis_CEC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lKmIV5SEGveA38fdKEvpbE-rWKzqYjMk

**Importing libraries**
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import missingno as msn
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

"""**Read the dataset into a pandas dataframe**"""

df = pd.read_csv('/content/drive/MyDrive/Airplane_Crashes_and_Fatalities_Since_1908.csv')

"""**Display the first 5 rows**"""

df.head()

"""**Column names and data types**"""

df.info()

"""**Number of columns and rows in the dataset**"""

df.shape

"""# Data Cleaning

**Find null values**
"""

df.isnull().sum()

"""**Visualizing missing data**"""

msn.bar(df)
plt.show()

"""**Decide which column to drop**"""

df.isnull().sum()/df.shape[0]

df.drop('Flight #', axis=1,inplace=True)

df.head(10)

"""
**Verify if i have duplicated rows and there is none**"""

df[df.duplicated(keep=False)==True]

df['Ground'].value_counts()

df.nunique()

"""**Summary statistics of the dataset**"""

df.describe().T

df['Aboard'].nunique()

df['Location'].value_counts()

"""**Time column**"""

#cleaning up
df['Time'] = df['Time'].str.replace('c: ', '')
df['Time'] = df['Time'].str.replace('c:', '')
df['Time'] = df['Time'].str.replace('c', '')
df['Time'] = df['Time'].str.replace('12\'20', '12:20')
df['Time'] = df['Time'].str.replace('18.40', '18:40')
df['Time'] = df['Time'].str.replace('0943', '09:43')
df['Time'] = df['Time'].str.replace('22\'08', '22:08')
df['Time'] = df['Time'].str.replace('114:20', '00:00')

"""**Time NaN values**"""

df['Time'] = df['Time'].fillna('00:00')

df.tail()

"""**Create the DateTime Colmun**"""

df['DateTime'] = df['Date'] + ' ' + df['Time']

df.head()

df['DateTime'] = pd.to_datetime(df['DateTime'])

df.info()

df.head()

"""**Operator Column**

Avoid duplicates like 'British Airlines' and 'BRITISH Airlines'
"""

df.Operator = df.Operator.str.upper()

df.head(2)

df['cn/In'].value_counts()

"""**Separating the location columns into two columns "City" and "Country"**"""

df[["City","Country"]]=df["Location"].str.split(',',1, expand=True)
df.head()

# Replace 'Alaska' and 'California' with 'USA'
df['Country'] = df['Country'].str.strip()
df['Country'].replace({'Alaska': 'USA', 'California': 'USA', 'New York': 'USA', 'Texas': 'USA', 'Virginia': 'USA', 'New Jersey': 'USA'}, inplace=True)

df.head(10)

"""**Calculating the count of accidents by country**"""

df['Country'].value_counts().head(10)

"""**Classificate accidents by cities**"""

df['City'].value_counts().head(10)

"""**Calculating the count of accidents by routes (ex : traject agadir-casablanca)**"""

df['Route'].value_counts().head(10)

"""**Calculating the operator that has most of accidents**"""

df['Operator'].value_counts().head(10)

"""**Type of airplan that has the most number of accidents**"""

df['Type'].value_counts().head(20)

"""**Creating a function to extract the maximum of causes of accidents from summary columns using some keywords that are repeated most**"""

def classify_summary(x):
    if pd.isna(x) or 'unknown' in x.lower() :  # Check if the value is NaN (float)
        return 'unknown'  # or any other appropriate label
    elif 'storm' in x.lower() or 'weather' in x.lower() or 'snow' in x.lower() or 'cloud' in x.lower() or 'lightning' in x.lower():
        return 'Bad weather condition'
    elif 'shot down' in x.lower() or 'bomber' in x.lower():
        return 'Shooted'
    elif 'burn' in x.lower() or 'fire' in x.lower() or 'engine' in x.lower()  or 'propellers' in x.lower() or 'exploded' in x.lower()  or 'crashed'in x.lower()  or 'wing'in x.lower():
        return 'Technical damage'
    elif 'visibility' in x.lower() or 'night' in x.lower()  :
        return 'Poor of visibility'
    elif 'tree' in x.lower() or 'hill'in x.lower() or 'montain'in x.lower() or 'sea'in x.lower() or 'river'in x.lower() :
        return 'Collision accident'
    elif 'pilot error' in x.lower() or 'destroyed' in x.lower() :
        return 'Pilot error'
    elif 'disappeared' in x.lower()  :
        return 'Disappeared'
    elif 'hijacked' in x.lower()  :
        return 'Hijacked'
    else:
        return 'Other'

df['Classification'] = df['Summary'].apply(classify_summary)
df.head()

"""**Most causes of accidents**"""

df['Classification'].value_counts()

"""**Grouping the 'Time' column  into 'day' that represent time betwen 6AM and 8PM and night that represent time betwen 8PM and 6AM**

"""

data = df.copy()
data.dropna(subset=['Time'], inplace=True)
data['Time'] = data['Time'].str.replace('c: ', '')
data['Time'] = data['Time'].str.replace('c:', '')
data['Time'] = data['Time'].str.replace('c', '')
data['Time'] = data['Time'].str.replace('12\'20', '12:20')
data['Time'] = data['Time'].str.replace('18.40', '18:40')
data['Time'] = data['Time'].str.replace('0943', '09:43')
data['Time'] = data['Time'].str.replace('22\'08', '22:08')
data['Time'] = data['Time'].str.replace('114:20', 'NaN')
data['Time'] = data['Time'].str.replace('1:00', 'NaN')
data['Time'] = data['Time'].str.replace('1NaN:00' , 'NaN')
data['Time'] = data['Time'].str.replace('0NaN' , 'NaN')
data['Time'] = data['Time'].str.replace('2NaN' , 'NaN')
data['Time'] = data['Time'].str.replace('1NaN' , 'NaN')
data = data[data['Time'] != 'NaN']
data.head()

#the condition we used is to divide 'Time' column into two conditions 'day' and 'night' using this function
def categorize_time(time):
    if pd.isnull(time) or pd.isna(time) :
        return 'other'
    hour = pd.to_datetime(time).hour
    if 6 <= hour < 20:
        return 'day'
    else:
        return 'night'

# Create a new column 'Time_Category' based on the conditions
data['Time_Category'] = data['Time'].apply(categorize_time)
data.head()

data['Time_Category'].value_counts()

"""**Dropping unnecessary columns**"""

df.drop(['Time', 'Date', 'cn/In'], axis=1, inplace=True)

df.head()

"""# Data Visualization"""

y = np.array([2156,873])
mylabels = ["Day", "Night"]
mycolors = ["#01d6ff", "#020083"]

plt.pie(y, labels=mylabels, colors=mycolors, autopct='%1.1f%%', startangle=90)
plt.title('Distribution of accidents according to Day and Night')
plt.legend()
plt.show()

"""**Total number of accidents by Type of flight**"""

Temp = df.copy()
Temp['isMilitary'] = Temp.Operator.str.contains('MILITARY')
Temp = Temp.groupby('isMilitary')[['isMilitary']].count()
Temp.index = ['Passenger','Military']

Temp2 = df.copy()
Temp2['Military'] = Temp2.Operator.str.contains('MILITARY')
Temp2['Passenger'] = Temp2.Military == False
Temp2 = Temp2.loc[:, ['DateTime', 'Military', 'Passenger']]
Temp2 = Temp2.groupby(Temp2.DateTime.dt.year)[['Military', 'Passenger']].aggregate(np.count_nonzero)

colors = ['#E3CF57', '#556B2F']
plt.figure(figsize=(15,6))
plt.subplot(1, 2, 1)
patches, texts = plt.pie(Temp.isMilitary, colors=colors, labels=Temp.isMilitary, startangle=90)
plt.legend(patches, Temp.index, loc="best", fontsize=10)
plt.axis('equal')
plt.title('Total number of accidents by Type of flight', loc='Center', fontsize=14)

plt.subplot(1, 2, 2)
plt.plot(Temp2.index, 'Military', data=Temp2, color='#556B2F', marker = ".", linewidth=1)
plt.plot(Temp2.index, 'Passenger', data=Temp2, color='#CDAA7D', marker = ".", linewidth=1)
plt.legend(fontsize=10)
plt.xlabel('Year', fontsize=10)
plt.ylabel('Number of accidents', fontsize=10)
plt.title('Number of accidents by Year', loc='Center', fontsize=14)
plt.tight_layout()
plt.show()

"""**Number of accidents by year**"""

nb_year= df.groupby(df.DateTime.dt.year)[['DateTime']].count()
plt.figure(figsize= (18, 8))
plt.plot(nb_year.index, nb_year['DateTime'], marker= '*')
plt.xlabel('Years')
plt.ylabel('Total Accidents')
plt.show()

"""**Number of accidents by month**"""

nb_month = df.groupby(df.DateTime.dt.month)[['DateTime']].count()

plt.figure(figsize= (16, 8))
plt.plot(range(len(nb_month)), nb_month['DateTime'], marker= '*', color= 'red')
plt.xticks(range(len(nb_month)), ['Jan', 'Feb', 'March', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.xlabel('Month')
plt.ylabel('Number of Accidents')
plt.show()

"""
**Number of accidents by week**"""

df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')
# Extraire le mois et le jour de la semaine à partir de la colonne 'Date'
df['Week'] = df['DateTime'].dt.week  # Utiliser dt.week pour obtenir le numéro de la semaine

# Grouper les données par semaine
weekly_accidents = df.groupby('Week').size()

# Noms des jours de la semaine
week_names = [f'Week {i}' for i in range(1, max(weekly_accidents.index)+1)]

# Créer le graphique pour les semaines
plt.figure(figsize=(16, 8))

sns.barplot(x=weekly_accidents.index, y=weekly_accidents.values, color='#FF7256')
plt.title('Average number of accidents per week')
plt.xlabel('Week of the year')
plt.ylabel('Number of accidents')
plt.xticks(ticks=range(1, len(week_names) + 1), labels=week_names, rotation=45, ha="right")

plt.tight_layout()
plt.show()

"""**Number of accidents by day**"""

nb_day = df.groupby(df.DateTime.dt.day)[['DateTime']].count()
plt.figure(figsize= (16, 8))
sns.barplot(x=nb_day.index, y=nb_day['DateTime'], color ='#B23AEE')
plt.xlabel('Day')
plt.ylabel('Total Accidents');

"""**Average number of accidents per month and per week:**"""

# Extraire le mois et le jour de la semaine à partir de la colonne 'Date'
df['Month'] = df['DateTime'].dt.month
df['Day_of_Week'] = df['DateTime'].dt.dayofweek  # 0 = lundi, 1 = mardi, ..., 6 = dimanche

# Grouper les données par mois
monthly_accidents = df.groupby('Month').size()

# Grouper les données par jour de la semaine
day_of_week_accidents = df.groupby('Day_of_Week').size()

# Noms des mois et des jours de la semaine
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Créer des graphiques pour les mois et les jours de la semaine
plt.figure(figsize=(15, 5))



plt.subplot(1, 2, 2)
sns.barplot(x=day_of_week_accidents.index, y=day_of_week_accidents.values, color='green')
plt.title('Average number of accidents per month and per week')
plt.xlabel('Day of the week')
plt.ylabel('Number of accidents')
plt.xticks(ticks=range(7), labels=day_names)

plt.tight_layout()
plt.show()

"""**The operators most frequently involved in accidents**"""

# Grouper les données par opérateur et compter le nombre d'accidents
operator_accidents = df['Operator'].value_counts()

# Sélectionner les 10 opérateurs les plus fréquemment impliqués
top_operators = operator_accidents.head(10)

# Créer un graphique des opérateurs les plus fréquemment impliqués
plt.figure(figsize=(15, 6))
top_operators.plot(kind='bar', color='red')
plt.title('The top 10 operators most frequently involved in accidents')
plt.xlabel('Operator')
plt.ylabel('Number of accidents')
plt.show()

"""**The operators least frequently involved in accidents**


"""

# Grouper les données par opérateur et compter le nombre d'accidents
operator_accidents = df['Operator'].value_counts()

# Sélectionner les 10 opérateurs les plus fréquemment impliqués
top_operators = operator_accidents.tail(10)

# Créer un graphique des opérateurs les plus fréquemment impliqués
plt.figure(figsize=(15, 6))
top_operators.plot(kind='bar', color='green')
plt.title('The operators least frequently involved in accidents')
plt.xlabel('Operator')
plt.ylabel('Number of accidents')
plt.show()

"""**Aircraft types tend to be involved in the greatest number of accidents**"""

# Grouper les données par type d'avion et compter le nombre d'accidents
aircraft_type_accidents = df['Type'].value_counts()

# Sélectionner les 10 types d'avions les plus fréquemment impliqués
top_aircraft_types = aircraft_type_accidents.head(10)

# Créer un graphique des types d'avions les plus fréquemment impliqués
plt.figure(figsize=(15, 6))
top_aircraft_types.plot(kind='bar', color='lightcoral')
plt.title('Aircraft types tend to be involved in the greatest number of accidents')
plt.xlabel('Type of Aircraft')
plt.ylabel('Number of accidents')
plt.show()

"""**The most dangerous places in terms of plane crashes**"""

# Fréquence des accidents par ville
accidents_par_ville = df['City'].value_counts().nlargest(10)

# Fréquence des accidents par pays
accidents_par_pays = df['Country'].value_counts().nlargest(10)

# Plot des accidents par ville
plt.figure(figsize=(12, 6))
accidents_par_ville.plot(kind='bar', color='skyblue')
plt.title('Top 10 cities with the most plane accidents')
plt.xlabel('City')
plt.ylabel('Nombre d\'accidents')
plt.xticks(rotation=45)
plt.show()

# Plot des accidents par pays
plt.figure(figsize=(12, 6))
accidents_par_pays.plot(kind='bar', color='salmon')
plt.title('Top 10 countries with the most plane accidents')
plt.xlabel('Country')
plt.ylabel('Number of accidents')
plt.xticks(rotation=45)
plt.show()

"""**Location**"""

import plotly.express as px
from geopy.geocoders import Nominatim



# Grouper les données par itinéraire et compter le nombre d'accidents
route_accidents = df['City'].value_counts()

# Sélectionner les 10 itinéraires les plus touchés
top_routes = route_accidents.head(10).index

# Filtrer les données pour inclure uniquement les itinéraires sélectionnés
filtered_data = df[df['City'].isin(top_routes)]

# Utiliser le service de géocodage Nominatim avec un délai de lecture plus long
geolocator = Nominatim(user_agent="my_geocoder", timeout=10)  # ajuster le timeout à 10 secondes

# Géocoder les lieux et ajouter les coordonnées à la dataframe
filtered_data['City'] = filtered_data['City'].apply(geolocator.geocode)
filtered_data['lat'] = filtered_data['City'].apply(lambda x: x.latitude if x else None)
filtered_data['lon'] = filtered_data['City'].apply(lambda x: x.longitude if x else None)

# Créer la carte interactive avec Plotly Express
fig = px.scatter_geo(filtered_data,
                     lat='lat',
                     lon='lon',
                     color='Location',
                     hover_name='Location',
                     title='Cities most affected by plane crashes',
                     projection='natural earth')

# Afficher la carte interactive
fig.show()

"""**Routes of Accidents**"""

# Grouper les données par itinéraire et compter le nombre d'accidents
route_accidents = df['Route'].value_counts()

# Sélectionner les 10 itinéraires les plus touchés
top_routes = route_accidents.head(10)

# Créer un graphique des itinéraires les plus touchés
plt.figure(figsize=(15, 6))
top_routes.plot(kind='bar', color='purple')
plt.title('The 10 most affected routes in terms of plane accidents')
plt.xlabel('Itinerary')
plt.ylabel('Number of accidents')
plt.show()

"""**The distribution of the main causes of accidents**"""

# Assuming 'Classification' is the correct column name
classification_distribution = df['Classification'].value_counts()

# Plotting a pie chart
plt.figure(figsize=(8, 8))
colors = plt.cm.Paired.colors
plt.pie(classification_distribution, labels=None, startangle=90, colors=colors)

# Adding legend to the right with percentages
legend_labels = [f'{label} ({percentage:.1f}%)' for label, percentage in zip(classification_distribution.index, classification_distribution / classification_distribution.sum() * 100)]
plt.legend(legend_labels, title='Classification', bbox_to_anchor=(1, 0.5), loc="center left", borderaxespad=0.)

# Adjusting layout for better visibility of labels
plt.tight_layout()

plt.title('The distribution of the main causes of accidents ')
plt.show()

"""**Top operators who suffer accidents due to technical damage (filtration according to the classification column**"""

subset_df = df[df['Classification'] == 'Technical damage']

most_frequent_operators = subset_df['Operator'].value_counts().nlargest(10)


plt.figure(figsize=(12, 6))
most_frequent_operators.plot(kind='bar', color='red')
plt.title('Top operators who suffer accidents due to technical damage ')
plt.xlabel('Operator')
plt.ylabel('Number of Occurrences')
plt.xticks(rotation=45)
plt.show()

"""**Operators who suffer the fewest accidents due to technical damage**"""

subset_df = df[df['Classification'] == 'Technical dammage']

moins_frequents_operateurs = subset_df['Operator'].value_counts().nsmallest(10)

plt.figure(figsize=(12, 6))
moins_frequents_operateurs.plot(kind='bar', color='green')
plt.title('Operators who suffer the fewest accidents due to technical damage')
plt.xlabel('Operator')
plt.ylabel('Numbre of occurrences')
plt.xticks(rotation=45)
plt.show()

"""# STATISTICS"""

# Create a scatter plot to visualize the correlation
plt.figure(figsize=(12, 8))

# Scatter plot for Aboard vs Fatalities
plt.subplot(2, 2, 1)
sns.scatterplot(x='Aboard', y='Fatalities', data=df)
plt.title('Aboard vs Fatalities')

# Scatter plot for Aboard vs Ground
plt.subplot(2, 2, 2)
sns.scatterplot(x='Aboard', y='Ground', data=df)
plt.title('Aboard vs Ground')

# Scatter plot for Fatalities vs Ground
plt.subplot(2, 2, 3)
sns.scatterplot(x='Fatalities', y='Ground', data=df)
plt.title('Fatalities vs Ground')

# Correlation heatmap
plt.subplot(2, 2, 4)
correlation_matrix = df[['Aboard', 'Fatalities', 'Ground']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')

plt.tight_layout()
plt.show()

"""**Average number of people on board during accidents over time**"""

# Group by 'Date' and calculate the average number of people aboard
average_aboard_by_date = df.groupby('DateTime')['Aboard'].mean()

# Plot the graph
plt.figure(figsize=(12, 6))
average_aboard_by_date.plot()
plt.title('Average number of people on board during accidents over time')
plt.xlabel('Date')
plt.ylabel('Average Aboard')
plt.show()

"""**Average number of victims (on board and on the ground) per accident over time**"""

# Create a new column 'Total Victims' representing the sum of 'Fatalities' and 'Ground'
df['Total Victims'] = df['Fatalities'] + df['Ground']

# Group by 'Date' and calculate the average number of victims per accident
average_victims_by_date = df.groupby('DateTime')['Total Victims'].mean()

# Plot the graph
plt.figure(figsize=(12, 6))
average_victims_by_date.plot()
plt.title('Average number of victims (on board and on the ground) per accident over time')
plt.xlabel('Date')
plt.ylabel('Average Number of Victims')
plt.show()

"""***CONCLUSIONS***

We conclude that PACIFIALASKA AIRLINES , HORIZON PROPERTIES , LINEA AREA NACIONAL... are the most safest operator however AEROFLOT has the most number of accidents because it might have the largest amount of flights.​

The USA is The country that have the most number of accidents .​

The technical damage is the main cause of accidents (53.3%).​

While the number of accidents and fatalities is rising, so is the number of flight.
"""