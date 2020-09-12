import time
import pandas as pd
import numpy as np


#Project bikeshare created in August 2020

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Interact with the user for the first time running the program

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    user_city_input = input("Please select a city between New York City, Washington and Chicago: ")
    user_city_input = str(user_city_input).rstrip().lower()
    if user_city_input in CITY_DATA:
        print(f"Great! We will search for {user_city_input} information")
        city = user_city_input
    else:
        while user_city_input not in CITY_DATA: #Here we handle invalid inputs from the user
            user_city_input = input("\nTry again, remember choose between New York City, Washington and Chicago: ")
            user_city_input = str(user_city_input).rstrip().lower()
            if user_city_input in CITY_DATA:
                city = user_city_input
                print("Great!")


    #Ask the user if there is a time filter needed to analyse the data
    date_filter_answer = input("\nDo you want to filter the data by \"Month\",\"day\" or not at all? Type \"None\" for no time filters: " )
    date_filter_answer = str(date_filter_answer).rstrip().title()

    while date_filter_answer not in ("Month","Day","None"):
        new_answer = input("\Please choose one of the options Month, day or None (in case you don´t want any time filters): ")
        if str(new_answer).rstrip().title() in ("Month","Day","None"):
            date_filter_answer = str(new_answer).rstrip().title()
            break

    # get user input for month (all, january, february, ... , june)
    if date_filter_answer == "Month":
        user_month_input = input("Please select a month between January and June. Type full month name: ")
        user_month_input = str(user_month_input).rstrip().title()
        months = ["January","February","March","April","May","June"]
        if user_month_input in months:
            month = user_month_input
            day = "All"
            print("Great, we can continue")
        else:
            while user_month_input not in months:
                user_month_input = input("\nTry again, remember choose between January and June. Type full month name: ")
                user_month_input = str(user_month_input).rstrip().title()
                if user_month_input in months:
                    month = user_month_input
                    day = "All"
                    print("Great, we can continue")
                    break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if date_filter_answer == "Day":
        user_day_input = input("please select a day between Monday and Sunday: ")
        user_day_input = str(user_day_input).rstrip().title()
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        if user_day_input in days:
            day = user_day_input
            month = "All"
            print("Great, we can continue")
        else:
            while user_day_input not in days:
                user_day_input = input("\nTry again, remember choose a day between Monday to Sunday, write the full day name: ")
                user_day_input = str(user_day_input).rstrip().title()
                if user_day_input in days:
                    day = user_day_input
                    month = "All"
                    print("Great, we can continue")
                    break

     # Do not filter the dataset by time

    if date_filter_answer == "None":
        print(f"\n\tNo time filters will be applied to the {user_city_input} dataset")
        day = "All"
        month = 'All'

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
    df["Start Time"] = pd.to_datetime(df["Start Time"]) #changing the data type to a datetime type for column Start Time
    df["month"] = df["Start Time"].dt.month #creating a "month" column in the data frame
    df["days"] = df["Start Time"].dt.weekday_name #creating a "days" column in the data frame
    df["start hour"] = df["Start Time"].dt.hour #creating a "hour" column in the data frame
    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ["January","February","March","April","May","June"]
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df["days"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df["month"].mode()[0]
    print(f"most common month: {most_common_month}")

    # display the most common day of week
    most_common_day_of_week = df["days"].mode()[0]
    print(f"most common day of the week: {most_common_day_of_week}")


    # display the most common start hour
    most_common_start_hour = df["start hour"].mode()[0]
    print(f"most common start hour: {most_common_start_hour}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_popular_start_station = df["Start Station"].mode()[0]
    print ("most popular start station: {}".format(most_popular_start_station))


    # display most commonly used end station
    most_popular_end_station = df["End Station"].mode()[0]
    print ("most popular end station: {}".format(most_popular_end_station))


    # display most frequent combination of start station and end station trip
    most_popular_combinations = (df["Start Station"] + " --> " + df["End Station"]).value_counts().head(1)
    print ("most frequent trip: {}".format(most_popular_combinations))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    # display total travel time
    total_trip_time = (df["End Time"]- df["Start Time"]).sum()
    print(f"total_trip_time: {total_trip_time}")


    # display mean travel time
    mean_trip_time = (df["End Time"]- df["Start Time"]).mean()
    print(f"mean_trip_time:{mean_trip_time}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df["User Type"].value_counts()
    print("\nUser type totals:")
    print(count_user_types)

    # Display counts of gender
    try:
        count_user_gender = df["Gender"].value_counts()
        print("\nTotal users by gender:")
        print(count_user_gender)
    except KeyError:
        print("\nThis dataset does not contain any Gender information about the users")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year  = df["Birth Year"].tail(1)
        most_recent_birth_year  = df["Birth Year"].head(1)
        most_common_birth_year = df["Birth Year"].mode()[0]
    except KeyError:
        print("\nThis dataset does not contain any Birth Year information about the users")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def individual_trip_data(df):
    """Displays individual trip information for the dataset selected by the user.
    It will display only the first 5 trips, sorted by the column Start Time from the
    Dataset created by the filters applied by the user in the get_filters function at
    the beginning of the program"""

    total_trips = df["Start Station"].count()
    print(f"\nYour dataset contains {total_trips} total individual trips")

    more_data_answer = input("Would you like to view details of the first 5 trips? yes or no: ")
    while str(more_data_answer).rstrip().lower() not in ("yes","no"):
            new_answer = input("Please type yes or no: ")
            if str(new_answer).rstrip().lower() in ("yes","no"):
                more_data_answer = str(new_answer).rstrip().lower()
                break

    if str(more_data_answer).rstrip().lower() == "yes":
        print('\nSearching for individual trip data...\n')
        start_time = time.time()
        df = df.sort_values(by=["Start Time"])
        for i in range(4):
            print("\n","-"*40,"\n",df.rename(columns={"Unnamed: 0": "Trip Reference"}).iloc[i])


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

        #Asking the user if more detailed information is needed
        more_info=input("\n\nWould you like to view individual trip data related to your data selection? Type yes or no: ")
        while str(more_info).lower() not in ("yes","no"):
            new_answer = input("Please type yes or no: ")
            if str(new_answer).lower() in ("yes","no"):
                more_info = str(new_answer).lower()
                break

        if str(more_info).lower() == "yes":
            individual_trip_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
