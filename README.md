# agile-forecasting
Forecasting and Probability tools

## Monte Carlo Simulations

### multiple-items-date-forecast.py

Generates probable date forecasts for completing multiple items.

* **throughputs** - Add historical thorughput values
* **num_items** - Number of items planned to complete
* **num_completed** - If any of the planned items have been completed to date, account for them here
* **timeframe_weeks** - Timeframe represented in weeks for which both throughput has been completed, as well as num_items to be completed
* **start_date** - Format: 'YYYY-MM-DD' or leave as "" to use today's date
  
throughputs, num_items, num_completed all need to be of the same value type. That is, if throughput is in user stories, then num_completed should be the planned user stories and num_completed are the user stories completed to date.

Note that standard deviation of historical thorughput values can be represented in the following line of code:

> completed += random.normalvariate(throughput / timeframe_weeks, 10) # Assuming 10 as variability

### multiple-items-date-forecast-cli:

Same script as above, except that the script uses historical throughput values from a comma-delimited (CSV) file via a command line argument.

The command line prompt will look like this:

> python multiple-items-date-forecast.py data.csv

Where:

* the CSV can be specified in an absolute path, i.e., c:\data\data.csv
* the CSV can be in a subdirectory to the directory in which the script is run, i.e., data/data.csv
* the CSV can be in the same directory in which the script is run, i.e., data.csv
* if there is no argument specified, the script will assume "throughput_data.csv" in the directory the script is run as the input file

The input file can be represented in columns, i.e.:

>55
>
>86
>
>132
>
>152
>
>132

or rows, i.e.:

>55,86,132,152,132

an example CSV file "throughput_data.csv" has been uploaded to the repo as an example. 

### multiple-items-probability-forecast.py:

Throughput values can be of any type for use in planning (i.e., features, work items)

* **historical_throughput** - Add historical throughput values

Note that standard deviation of historical thorughput values can be represented in the following line of code:

> simulated_value = random.normalvariate(historical_value, 5)  # Using standard deviation of 5

### multiple-items-date-forecast-wip.py:

Same variables and output as multiple-items-date-forecast.py, with the addition of using Little's Law to compute the effect of WIP on probable date. WIP can be adjusted via the following line of code:

> max_wip = 100  # Maximum allowable work-in-progress

### SLEs

Below are some scripts to use to calculate Service Level Expectations (SLEs) for your teams. There are two versions - a simple and an advanced SLE - which are explained below.

### simple-sle.py:

* Update **historical_data** with the states and average cycle times per state you wish to use in your calculations
* Set the **timebox_duration** to the timebox you wish to use for your SLE (in this case, default to 14 days/2 weeks)

SLE will be generated based on the length of the timebox. If the historical data used is longer than the specified timebox_duration, then the SLE for each state in the workflow will be adjusted accordingly to fit within the timebox. This will give you an idea of historically how long each work item spends in each state, relative to the timebox specified. You can use this information to rightsize your work accordingly.

### advance-sle.py

This version reads a comma_delimited source file with historical cycle data for each state in the workflow. This will allow you to input more specific historical data derived from our source data, so that percentiles for each state can be generated.

The input file formation should be as follows:
```
Input file format:

state, time_spent
To Do,5
In Progress,17
Review,4
To Do,8
In Progress,12
Review,6
```

The SLE is generated with percentiles of each state at 50%, 85% and 95% probability.
