# Complete Project 1: Divvy: Bike Sharing Company: Weekdays, Months and Stations Analysis. User vs Suscriptor

> It's a large dataset, may take minutes to load
# Scenario

You are a junior data analyst working in the marketing analyst team at Cyclistic, a bike-share company in Chicago. The director of marketing believes the company’s future success depends on maximizing the number of annual memberships. Therefore, your team wants to understand how casual riders and annual members use Cyclistic bikes differently. From these insights, your team will design a new marketing strategy to convert casual riders into annual members. But first, Cyclistic executives must approve your recommendations, so they must be backed up with compelling data insights and professional data visualizations.

# About the company

In 2016, Cyclistic launched a successful bike-share offering. Since then, the program has grown to a fleet of 5,824 bicycles that are geotracked and locked into a network of 692 stations across Chicago. The bikes can be unlocked from one station and returned to any other station in the system anytime.
Until now, Cyclistic’s marketing strategy relied on building general awareness and appealing to broad consumer segments. One approach that helped make these things possible was the flexibility of its pricing plans: single-ride passes, full-day passes, and annual memberships. Customers who purchase single-ride or full-day passes are referred to as casual riders. Customers who purchase annual memberships are Cyclistic members.
Cyclistic’s finance analysts have concluded that annual members are much more profitable than casual riders. Although the pricing flexibility helps Cyclistic attract more customers, Moreno believes that maximizing the number of annual members will be key to future growth. Rather than creating a marketing campaign that targets all-new customers, Moreno believes there is a very good chance to convert casual riders into members. She notes that casual riders are already aware of the Cyclistic program and have chosen Cyclistic for their mobility needs.
Moreno has set a clear goal: Design marketing strategies aimed at converting casual riders into annual members. In order to do that, however, the marketing analyst team needs to better understand how annual members and casual riders differ, why casual riders would buy a membership, and how digital media could affect their marketing tactics. Moreno and her team are interested in analyzing the Cyclistic historical bike trip data to identify trends.

# Main question to answer

1. How do annual members and casual riders use Cyclistic bikes differently?
2. Why would casual riders buy Cyclistic annual memberships?
3. How can Cyclistic use digital media to influence casual riders to become members?

# 1.0 Ask

For this project, I have been given a huge data set. I proceed to see the features in excel and I see that there are around 800,000 lines for each month and that they have a consistent format, so I propose to do everything in R and thus practice my skills.

Based on the data that I have available, and, in order to answer the company's questions, I am going to perform my set of questions in the database:

1. What is the average, maximum and minimum duration by type of user?
2. Trips and travel time by user and day of the week
3. Trips and travel time by user and month
4. What are the most common trips by type of user?

I think these questions can tell us the main differences between the types of user and understand how they behabe so we could offer better fits for their needs. So, let´s import the data to the enviroment:

# 2.0 Prepare

```
library(tidyverse)
library(dplyr)
library(tidyr)
library(skimr)
library(janitor)
library(ggplot2)
library(lubridate)
library(data.table)
```
```
df2108 <- read.csv('../input/cyclistic-trips-202108-to-202207/202108-divvy-tripdata.csv')
df2109 <- read.csv('../input/cyclistic-trips-202108-to-202207/202109-divvy-tripdata.csv')
df2110 <- read.csv('../input/cyclistic-trips-202108-to-202207/202110-divvy-tripdata.csv')
df2111 <- read.csv('../input/cyclistic-trips-202108-to-202207/202111-divvy-tripdata.csv')
df2112 <- read.csv('../input/cyclistic-trips-202108-to-202207/202112-divvy-tripdata.csv')
df2201 <- read.csv('../input/cyclistic-trips-202108-to-202207/202201-divvy-tripdata.csv')
df2202 <- read.csv('../input/cyclistic-trips-202108-to-202207/202202-divvy-tripdata.csv')
df2203 <- read.csv('../input/cyclistic-trips-202108-to-202207/202203-divvy-tripdata.csv')
df2204 <- read.csv('../input/cyclistic-trips-202108-to-202207/202204-divvy-tripdata.csv')
df2205 <- read.csv('../input/cyclistic-trips-202108-to-202207/202205-divvy-tripdata.csv')
df2206 <- read.csv('../input/cyclistic-trips-202108-to-202207/202206-divvy-tripdata.csv')
df2207 <- read.csv('../input/cyclistic-trips-202108-to-202207/202207-divvy-tripdata.csv')
```
Before I join all of the dfs, I should make sure if they match in size and type in the columns:
```
compare_df_cols(df2108,df2109,df2110,df2111,df2112,df2201,df2202,df2203,df2203,df2204,df2205,df2206, df2207)
```
As they all share the same structure, I combine them in a single database:
```
tripdata <- 
    rbindlist(list(df2108,df2109,df2110,df2111,df2112,df2201,df2202,df2203,df2203,df2204,df2205,df2206, df2207))
```  

# 3.0 Process

Since we have loaded such a large amount of data, we must see the structure of the data and proceed to clean it to obtain a database that works for us:
Let's start by removing the duplicates and NA values and then checking the database:
``` 
tripdata <- tripdata %>%
  na_if("") %>%
  na.omit
tripdata <- distinct(tripdata)

str(tripdata)
```
Let's now change types in the columns and create the ride lenght column as the difference in time betewwb ended and started trip, and, if there's one with incorrect time (less than 0 min.), we'll drop it:
```
tripdata$started_at <- 
    strptime(tripdata$started_at, "%Y-%m-%d %H:%M:%S")

tripdata$ended_at <- 
    strptime(tripdata$ended_at,"%Y-%m-%d %H:%M:%S")

tripdata <- 
    mutate(tripdata, ride_length = round(difftime(tripdata$ended_at, tripdata$started_at, units= "min"), 2))

tripdata$ride_length <- 
    as.numeric(gsub(",", "",tripdata$ride_length))

tripdata<-
    filter(tripdata,ride_length > 0)

str(tripdata)
```

# 4.0 Analysis
## 4.1 What is the average, maximum and minimum duration by type of user?
```
tripdata %>%
  group_by(member_casual) %>%
  summarise(max_ride_length=max(ride_length), min_ride_length=min(ride_length), mean_ride_length=round(mean(ride_length), 2) ,
            median_ride_length=median(ride_length),total_trips=n())
```
Oh! we can see that users and members behave very differently, the average trip is more than double! Despite of it, the median is not that different... it seems that some trips carried out by casual users raise the average a lot, as we can see in the max values.

Let's continue with the analysis to be able to see different behaviors with other variables:
## 4.2 Trips and travel time by user and day of the week
First of all, we create the day of the week column to filter what day each trip was made:
```
tripdata$week_day<- 
    weekdays(tripdata$started_at)

tripdata$week_day <- factor(tripdata$week_day, levels= c("Sunday", "Monday", 
    "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"))

str(tripdata)
```
```
#Minutes graph

tripdata %>%
    group_by(week_day, member_casual) %>%
    summarise(mean_trip_duration=round(mean(ride_length), 2), total_min=round(n()*mean(ride_length), 2)) %>%
    mutate(total_min_freq = formattable::percent (round(total_min / sum(total_min), 3))) %>%

ggplot() + 
    geom_col(aes(week_day,total_min_freq, fill=member_casual)) + 
    labs(title="Fig. 01: Week's Total Minutes By Type of User", 
         x='week day', y='%', fill='Type of user')

#Trips graph

tripdata %>%
    group_by(week_day, member_casual) %>%
    summarise(mean_trip_duration=round(mean(ride_length), 2), total_trips=n()) %>%
    mutate(total_trips_freq = formattable::percent (round(total_trips / sum(total_trips), 3))) %>%

ggplot() + 
    geom_col(aes(week_day,total_trips_freq, fill=member_casual)) + 
    labs(title="Fig. 02: Week's Total Trips By Type of User", x='week day', y='%', fill='Type of user')
```
This is so illuminating! Members use our services much more, but almost never reach 50% of the total minutes per day. This may mean that they tend to use it for defined routes and casual users use it for sightseeing or other leisure activities and spend more time on the road.

Let's continue with our analysis regarding, this time, the months of the year. This way we can see if these trends are more visible depending on the month of the trip.
## 4.3 Trips and travel time by user and month
```
#Minutes graph

tripdata %>%
    mutate(month = format(started_at, "%m")) %>% 
    group_by(month, member_casual) %>%
    summarise(mean_trip_duration=round(mean(ride_length), 2), total_min=round(n()*mean(ride_length), 2)) %>%
    mutate(total_min_freq = formattable::percent (round(total_min / sum(total_min), 3))) %>%

ggplot() + 
    geom_col(aes(month, total_min_freq, fill=member_casual)) +
    labs(title="Fig. 03: Month Total Minutes By Type of User", x='month', y='%', fill='Type of user')

#Trips graph

tripdata %>%
    mutate(month = format(started_at, "%m")) %>% 
    group_by(month, member_casual) %>%
    summarise(mean_trip_duration=round(mean(ride_length), 2), total_trips=n()) %>%
    mutate(total_trips_freq = formattable::percent (round(total_trips / sum(total_trips), 3))) %>%

ggplot() + 
    geom_col(aes(month,total_trips_freq, fill=member_casual)) + 
    labs(title="Fig.04: Month Total Trips By Type of User", x='month', y='%', fill='Type of user')
```
With this analysis we get the same as results as the previous one, the typical working months (mid-September to May), the majority of trips are subscriber trips and in the summer months it drops to a great extent.

The total minutes of the summer months in the casual members are very high, again, to leisure trips and tourists who come to the city, the graphs seem to tell us.
## 4.4 What are the most common trips by type of user?
Now that we know how each type of user differs, let's see what trips each one makes to find out where they are most likely to get new subscribers:
```
tripdata %>%
    group_by(start_station_name, end_station_name, member_casual) %>%
    summarise(mean_trip_duration=round(mean(ride_length), 2), total_trips=n()) %>%
    filter(total_trips>100) %>%

ggplot() + 
    geom_density(aes(mean_trip_duration, fill=member_casual), alpha=0.3) +
    labs(title="Fig.05: Trips density By Users", y='Density of Trips', x='Mean Trip duration (min)', fill='Type of user')
```
We can see the different behavior of the data sets. Our focus should be mainly on the overlapping data, since they are short trips that tend to be more of subscribers.

We can also see a small 'hill' in the member data, these can be typical tourist or leisure trips. We should be able to understand this section and to be able to take out a product accordingly, as there is a market that uses it and has no solution. But, in spite of this, we should focus the business on subscribing members who can offer us a base for our business.

To do this we should focus on marketing to users who use the following sections:
```
head(
tripdata %>%
    group_by(start_station_name, end_station_name, member_casual) %>%
    summarise(total_trips=n(), mean_trip_duration=round(mean(ride_length), 2)) %>%
    filter(total_trips>100) %>%
    filter(mean_trip_duration < 12.5) %>%
    filter(member_casual=='casual') %>%
    arrange(desc(mean_trip_duration)))
```
# 5.0 Conclusions
To begin with, we are going to answer the questions in the questionnaire.

1. How do annual members and casual riders use Cyclistic bikes differently?

  Members use it more on working days (Fig. 2) and by the months, also on working ones (Fig. 4). Casual users, on the other hand, use it longer than subscribers and mainly on weekends (Fig.1). As for the months, they use it more in the spring and summer months, both in terms of time and number of trips (Fig.3).

2. Why would casual riders buy Cyclistic annual memberships?

  According to my analysis (Fig.5), they subscribe for 'small to medium' time trips and for repetitive activities that will use a lot of time (such as work)

3. How can Cyclistic use digital media to influence casual riders to become members?

  We've to look over the stations that are most likely to be used by members to engage with them and, among those used by casual members, we should focus on the ones shown in the last table, as they have the optimal conditions to become subscribing members.
















