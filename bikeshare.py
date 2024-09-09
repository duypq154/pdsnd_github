import time
import pandas as pd
import numpy as np
import os
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]

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
    while True:
        city = input('Would you like to see data for Chicago, New York or Washington? \n>')
        if city.lower() in CITIES:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month? January, February, March, April, May, or June? \n>')
        if month.lower() in MONTHS:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day? Please type your response as (Monday, Tuesday...) \n>' )
        if day.lower() in DAYS:
            break

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
    try:
        # Load data frame
        df = pd.read_csv(CITY_DATA[city.lower()])
        
        # Convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # Extract hour from the Start Time column to create an hour column
        df['hour'] = df['Start Time'].dt.hour
        
        # Extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name
       
        # Filter by month if applicable
        if month != 'all':
            # Use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month.lower()) + 1
            # Filter by month to create the new dataframe
            df = df[df['month'] == month]
            
        # Filter by day of week if applicable
        if day != 'all':
            # Filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]
        
        return df
    except FileNotFoundError as e:
        print(e)
        raise FileNotFoundError

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_popular_month =  df['month'].mode()[0]
    print("What is the most popular month for traveling?", most_popular_month)

    # display the most common day of week
    most_popular_day_of_week = df['day_of_week'].mode()[0]
    print("What is the most popular day of week for traveling?", most_popular_day_of_week)

    # display the most common start hour
    most_popular_start_hour =  df['hour'].mode()[0]
    print("What is the most popular hour for traveling?", most_popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        most_popular_start_station = df['Start Station'].mode()[0]
        print("The most commonly used start station: ", most_popular_start_station)
    except KeyError:
      print("The most commonly used start station: No data available.")

    # display most commonly used end station
    try:
        most_popular_end_station = df['End Station'].mode()[0]
        print("The most commonly used end station: ", most_popular_end_station)
    except KeyError:
      print("The most commonly used end station: No data available.")

    # display most frequent combination of start station and end station trip
    try:
        most_popular_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
        print("The most commonly used start station and end station: {}, {}".format(most_popular_start_end_station[0], most_popular_start_end_station[1]))
    except KeyError:
      print("The most commonly used start station and end station: No data available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    try:
        total_travel = df['Trip Duration'].sum()
        print("The total travel time: ", total_travel)
    except KeyError:
      print("The total travel time: No data available.")

    # display mean travel time
    try: 
        mean_travel = df['Trip Duration'].mean()
        print("The mean travel time: ", mean_travel)
    except KeyError:
      print("The mean travel time: No data available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_counts = df['User Type'].value_counts()
        print("Counts of user types: ", user_counts)
    except KeyError:
      print("Counts of user types: No data available.")

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print("Counts of gender: ",gender_counts)
    except KeyError:
      print("Counts of gender: No data available.")

    # Display earliest, most recent, and most common year of birth
    try:
        most_common_year = df['Birth Year'].mode()[0]
        print("The most common birth year: ", most_common_year)
        
        most_recent_year = df['Birth Year'].max()
        print("The most recent birth year: ", most_recent_year)
        
        earliest_year = df['Birth Year'].min()
        print("The most earliest birth year: ", earliest_year)
    except KeyError:
      print("No data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_display(df): 
    view_data  = input('\nDo you want to check the first 5 rows of the dataset related to the chosen city? Enter yes or no\n')
    start_loc = 0
    while view_data  == "yes":
      print(df.iloc[start_loc:start_loc + 5])
      start_loc += 5
      view_data  = input("Do you want to check another 5 rows of the dataset? Enter yes or no\n ").lower()
      
    while view_data == "no":
        restart = input('\nDo you want to restart the kernel? Enter yes or no.\n')
        if restart.lower() != 'no':
            os.execv(sys.executable, ['python'] + sys.argv)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

    ##update on refactoring