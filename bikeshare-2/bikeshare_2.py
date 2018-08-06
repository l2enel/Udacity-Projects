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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = ['chicago', 'new york city', 'washington']

    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july',
                    'august', 'september', 'october', 'november', 'december']

    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']



    city = input("Please type desired city for inquiry (chicago, new york city, or washington)").lower()

    while city not in valid_cities:
        city = input("Please try again and select a valid city (chicago, new york city, or washington)").lower()


    # get user input for month (all, january, february, ... , june)

    month = input("Please type desired month for inquiry (january..december), or type 'all'\n").lower()

    while month not in valid_months:
        month = input("Please try again and select valid month or all\n").lower()

    month = valid_months.index(month)

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input("Please input the desired day of the week for inquiry (monday..sunday), or type 'all'\n").lower()

    while day not in valid_days:
        day = input("Please try again and input all or select valid day\n").lower()

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
    df = pd.read_csv(CITY_DATA[city])

    ### adding new columns; month, day_of_week, start_hour
    ## first converting Start Time values to datetime values
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Now extracting new columns from the converted Start Time column
    df['month'] = df['Start Time'].dt.month

    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    #Filtering database to selected month and day
    # month will == 0 if user entered 'all'
    if month != 0:
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print("The most common month of travel is {}".format(most_common_month))

    # display the most common day of week
    most_common_day = df['day'].mode()[0]
    print("The most common day of travel is {}".format(most_common_day))

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common hour of travel is {}".format(most_common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_used_start = df['Start Station'].mode()[0]
    print("The most used start station is {}".format(most_used_start))

    # display most commonly used end station
    most_used_end = df['End Station'].mode()[0]
    print("The most used end station is {}".format(most_used_end))

    # display most frequent combination of start station and end station trip
    print("The most frequent combination of start station and end station is")

    ### Do not know how to extract the individual values and maintain the start and end station values
    print(df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).head(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time is {}".format(total_travel_time))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time is {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())


    # Display counts of gender
    ## gender column does not exist in washington.csv
    if city != 'washington':
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth

        print("Earliest birth year of a user;")
        print(df['Birth Year'].min())
        print("Most recent birthyear of a user;")
        print(df['Birth Year'].max())
        print("Average birth year of a user;")
        print(df['Birth Year'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    valid_requests = ['y', 'n']
    request = input("Would you like to view the raw data? (y/n)").lower()

    while request not in valid_requests:
        request = input("Invalid response, please enter 'y' or 'n' ").lower()

    if request == 'y':
        print(df)
    elif request == 'n':
        print('End of inquiry')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
