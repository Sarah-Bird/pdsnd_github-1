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
    city = input('Which city would you like to look at? Chicago, New York City or Washington? \n').lower()
    while city not in CITY_DATA:
        print('That\'s not a valid input. Please try again.')
        city = input('Which city would you like to look at? Chicago, New York City or Washington? \n').lower()
    else:
        print('Thanks for that.')


    # get user input for month (all, january, february, ... , june)
    month = input('Which month would you like to look at? Choose a month from January to June or choose all \n').lower()
    while month not in ['january', 'february', 'march', 'april','may', 'june', 'all']:
        print('That\'s not a valid input. Please try again.')
        month = input('Which month would you like to look at? Choose a month from January to June or choose all \n')
    else:
        print('Thanks for that.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day of the week would you like to look at? Choose a day from Monday to Sunday or choose all \n').lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print('That\'s not a valid input. Please try again.')
        day = input('Which day of the week would you like to look at? Choose a day from Monday to Sunday or choose all \n')
    else:
        print('Thanks for that.')
    print('-'*40)
    print('\n \n')
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df
def show_data(df,data_request):
    """Displays resulting data 5 rows at a time until the user requests otherwise."""
    print('There are {} results'.format(df.shape[0]))
    #Calls on data_request in main.
    if data_request.lower() == 'yes':
        #Shows first 5 results
        for i in range(0,5):
            print('Journey result',i+1,
            '\n Start time: ', df['Start Time'].iloc[i],
            '\n End time: ', df['End Time'].iloc[i],
            '\n Trip Duration: ', df['Trip Duration'].iloc[i],
            '\n Start station: ', df['Start Station'].iloc[i],
            '\n End Station: ', df['End Station'].iloc[i],
            '\n User Type: ', df['User Type'].iloc[i],
            #Gender and birth year not always supplied and not available for certain states so a related string is printed in these cases.
            '\n Gender: ', (df['Gender'].iloc[i] if type(df['Gender'].iloc[i]) is str else 'not given') if 'Gender' in df else 'No information available',
            '\n Birth year: ', (int(df['Birth Year'].iloc[i]) if df['Birth Year'].iloc[i] > 1900 else 'not given') if 'Birth Year' in df else 'No information available')
        #Starts from sixth result
        i = 5
        while i < df.shape[0] and input('Would you like to see more? Please type yes or no: ') == 'yes':
            for i in range(i, i+5):
                try:
                    print('Journey result',i+1,
                    '\n Start time: ', df['Start Time'].iloc[i],
                    '\n End time: ', df['End Time'].iloc[i],
                    '\n Trip Duration: ', df['Trip Duration'].iloc[i],
                    '\n Start station: ', df['Start Station'].iloc[i],
                    '\n End Station: ', df['End Station'].iloc[i],
                    '\n User Type: ', df['User Type'].iloc[i],
                    '\n Gender: ', (df['Gender'].iloc[i] if type(df['Gender'].iloc[i]) is str else 'not given') if 'Gender' in df else 'No information available',
                    '\n Birth year: ', (int(df['Birth Year'].iloc[i]) if df['Birth Year'].iloc[i] > 1900 else 'not given') if 'Birth Year' in df else 'No information available')
                    i += 1
                #Error will be raised if last 5 does not contain 5 entries.
                #Except shows remainder of entries.
                except:
                    for i in range(df.shape[0]-(df.shape[0]%5),df.shape[0]):
                        print('Journey result',i+1,
                        '\n Start time: ', df['Start Time'].iloc[i],
                        '\n End time: ', df['End Time'].iloc[i],
                        '\n Trip Duration: ', df['Trip Duration'].iloc[i],
                        '\n Start station: ', df['Start Station'].iloc[i],
                        '\n End Station: ', df['End Station'].iloc[i],
                        '\n User Type: ', df['User Type'].iloc[i],
                        '\n Gender: ', (df['Gender'].iloc[i] if type(df['Gender'].iloc[i]) is str else 'not given') if 'Gender' in df else 'No information available',
                        '\n Birth year: ', (int(df['Birth Year'].iloc[i]) if df['Birth Year'].iloc[i] > 1900 else 'not given') if 'Birth Year' in df else 'No information available')
    elif data_request.lower() == 'no':
        print('User selected to skip viewing data')
    else:
        print('Unknown input!')
        data_request = input('Please try again and respond yes or no:  ')
        show_data(df,data_request)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month if 'all' selected.
    #If month specified, popular month will be the chosen month

    df['month'] = df['Start Time'].dt.month_name()
    popular_month = df['month'].mode()[0]
    # if 'all' was selected, there will be more than 1 unique month in the dataframe
    if len(df['month'].unique()) > 1:
        print('The most common month for hires is', popular_month,'.')
    else:
        print('Your chosen month is', popular_month)

    # display the most common day of week
    # if day specified,popular_day will be the chosen day
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_day = df['day_of_week'].mode()[0]
    if len(df['day_of_week'].unique()) > 1:
        print('The most common day for hires is', popular_day,'.')
    else:
        print('Your chosen month is', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour for hires is', popular_hour,'.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_depart = df['Start Station'].mode()[0]
    print('Customers most commonly leave from', popular_depart,'.')

    # display most commonly used end station
    popular_destination = df['End Station'].mode()[0]
    print('Customers most commonly ride to', popular_destination,'.')

    # display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ' to ' + df['End Station']
    popular_route = df['route'].mode()[0]
    print('The most popular combination of start and end stations is', popular_route)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['trip duration'] = df['End Time'] - df['Start Time']
    # display total travel time
    total_time = df['trip duration'].sum()
    print('The total travel time is',total_time)

    # display mean travel time
    mean_time = df['trip duration'].mean()
    print('The mean travel time is', mean_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('These are the total number of customers in each user group.\n')
    user_type_totals = df.groupby(['User Type'])['User Type'].count()
    print(user_type_totals,'\n')

    # Display counts of gender
    print('These are the total number of customers in each gender category where that information has been given.\n')
    while True:
        #If lack of gender data causes an error, user informed information not available
        try:
            gender_totals = df.groupby(['Gender'])['Gender'].count()
            print(gender_totals)
            break
        except:
            print('Gender information not available for this State or time period')
            break

    # Display earliest, most recent, and most common year of birth
    print('\n')
    print('These are the Birth Year statistics available:\n')
    while True:
        #If lack of birth year data causes an error, user informed information not available
        try:
            earliest_by = int(df['Birth Year'].min())
            latest_by = int(df['Birth Year'].max())
            common_by = int(df['Birth Year'].mode()[0])
            print('The earliest year of birth is', earliest_by)
            print('The most recent year of birth is', latest_by)
            print('The most common year of birth is', common_by)
            break
        except:
            print('Birth Year information not available for this State or time period')
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #show_data function used twice so input message depends on when function carried out.
        #initial show_data to view data stats based upon.
        show_data(df, input('Would you like to view your search results before viewing statistics? Please type yes or no: '))
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #second show_data to review data once stats have been viewed.
        show_data(df, input('Would you like to review your search results? Please type yes or no: '))

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
