import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #Getting user input for city (chicago, new york city, washington) while handling potential user error.
    city=None
    while city not in set(['chicago','washington','new york city']):
        city=input("Enter the city name: \n").lower()
        if city in set(['nyc','new york','ny']):
            city='new york city' 
        if city not in set(['chicago','washington','new york city']):
            print('Please enter a valid city name')


    #Getting user input for month (all, january, february, ... , june) and handling potential user error.
    month=None
    while month not in set(['january','february','march','april','may','june']):
        month=input("Enter the name of the month or type 'all' to apply no filter\nplease note that the selected month must be from the first half of the year: \n").lower()
        if month=='all':
            break
        if month not in set(['january','february','march','april','may','june']):
            print("Please enter a valid month name from the first half of the year")
    if month!='all':
        months=['january','february','march','april','may','june','july','august','september','october','november','december']     
        month=months.index(month)+1
    


    #Getting user input for day of week (all, monday, tuesday, ... sunday) and handling poetenital user error
    day=None
    while day not in set(['Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday']):
        day=input("Enter the name of the day or type 'all' to apply no filter: \n").title()
        if day=='All':
            day='all'
        if day=='all':
            break
        if day not in set(['Saturday','Sunday','Monnday','Tuesday','Wednesday','Thursday','Friday']):
            print('Please enter a valid day name ')


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city]) #Reading the user-selected file
    
    df['Start Time']=pd.to_datetime(df['Start Time'])
    
    df['month']=df['Start Time'].dt.month #Creating a "month" column 
    if month!='all':
        df=df[df['month']==month] #Filtering the dataframe by user-selected month
    
    df['day']=df['Start Time'].dt.day_name() #Creating a "day" column
    if day!='all': 
        df=df[df['day']==day] #Filtering by day
    prompt=input("Would you like to view the first 5 rows of the data you selected? ").lower()
    if prompt=='yes':
        print(df.head()) #Viewing a sample of the raw data upon user request
        



    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Displaying the most common month
    m=df['month'].mode()[0]
    months=['january','february','march','april','may','june']
    m=months[m-1]
    print("most common month from the filtered data is: {}".format(m))


    #Displaying the most common day of week
    print("Most common day from the filtered data is: {}".format(df['day'].mode()[0]))


    #Displaying the most common start hour
    df['hour']=df['Start Time'].dt.hour
    print("Most common hour from the filtered data is: {}(24h system)".format(df['hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Displaying most commonly used start station
    print("Most commonly used start station is: {}".format(df['Start Station'].mode()[0]))


    #Displaying most commonly used end station
    print("Most commonly used end station is: {}".format(df['End Station'].mode()[0]))


    #Displaying most frequent combination of start station and end station trip
    s=df['Start Station']+" to "+df['End Station']
    print("Most frequent combination of start station and end station trip is: {}".format(s.mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Displaying total travel time
    print("Total drive time is: {} hours".format(df['Trip Duration'].sum()/(60*60)))


    #Displaying mean travel time
    print("Average travel time is: {} minutes".format(df['Trip Duration'].mean()/(60)))

    #Display the shortest and longest amount of time it takes to complete a trip from start to end
    print("Longest trip duration is: {} hours".format(df['Trip Duration'].max()/(60*60)))
    print("Shortes trip duration is: {} minute(s)".format(df['Trip Duration'].min()/(60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Displaying counts of user types
    print("Total number of subscribers is: {} subscriber\n".format(df['User Type'].value_counts()[0]))
    print("Total number of customers is: {} customer".format(df['User Type'].value_counts()[1]))
    


    #Display counts of gender
    print('\nCalculating Gender Stats...\n')
    try:
        print("Total number of males is: {}".format(df['Gender'].value_counts()[0]))
        print("Total number of females is: {}".format(df['Gender'].value_counts()[1]))
        print("Male percentage from the total users number is: {}".format(df['Gender'].value_counts()[0]/(df['Gender'].value_counts()[0]+df['Gender'].value_counts()[1])*100))
        print("Female percentage from the total users number is: {}".format(df['Gender'].value_counts()[1]/(df['Gender'].value_counts()[0]+df['Gender'].value_counts()[1])*100))
    except:
        print('insights about year of birth and gender are only available for NYC and Chicago.')
        print('-'*40)
    #Displaying earliest, most recent, and most common year of birth
    print('\nCalculating Birth Year Stats...\n')
    try:
        print("Earliest year of birth is: {}".format(df['Birth Year'].min()))
        print("Most recent year of birth is: {}".format(df['Birth Year'].max()))
        print("Most common year of birth is {}".format(df['Birth Year'].mode()[0]))
    except:
        print('insights about year of birth and gender are only available for NYC and Chicago.')
    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
