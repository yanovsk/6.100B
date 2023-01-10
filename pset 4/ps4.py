# -*- coding: utf-8 -*-
# 6.100B Fall 2022
# Problem Set 4: Sea Level Rise
# Name:
# Collaborators:

from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import PIL, PIL.Image

import scipy.stats as st
import scipy.interpolate 


#####################
# Begin helper code #
#####################

def calculate_std(upper, mean):
    """
	Calculate standard deviation based on the upper 95th percentile

	Args:
		upper: a 1-d numpy array with length N, representing the 95th percentile
            values from N data points
		mean: a 1-d numpy array with length N, representing the mean values from
            the corresponding N data points

	Returns:
		a 1-d numpy array of length N, with the standard deviation corresponding
        to each value in upper and mean
	"""
    return (upper - mean) / st.norm.ppf(.975)


def interp(target_year, input_years, years_data):
    """
	Interpolates data for a given year, based on the data for the years around it

	Args:
		target_year: an integer representing the year which you want the predicted
            sea level rise for
		input_years: a 1-d numpy array that contains the years for which there is data
		    (can be thought of as the "x-coordinates" of data points)
        years_data: a 1-d numpy array representing the current data values
            for the points which you want to interpolate, eg. the SLR mean per year data points
            (can be thought of as the "y-coordinates" of data points)

	Returns:
		the interpolated predicted value for the target year
	"""
    return np.interp(target_year, input_years, years_data, right=-99)


def load_data():
    """
	Loads data from sea_level_change.csv and puts it into numpy arrays

	Returns:
		a length 3 tuple of 1-d numpy arrays:
		    1. an array of years as ints
		    2. an array of 2.5th percentile sea level rises (as floats) for the years from the first array
		    3. an array of 97.5th percentile of sea level rises (as floats) for the years from the first array
        eg.
            (
                [2020, 2030, ..., 2100],
                [3.9, 4.1, ..., 5.4],
                [4.4, 4.8, ..., 10]
            )
            can be interpreted as:
                for the year 2020, the 2.5th percentile SLR is 3.9ft, and the 97.5th percentile would be 4.4ft.
	"""
    df = pd.read_csv('sea_level_change.csv')
    df.columns = ['Year', 'Lower', 'Upper']
    return (df.Year.to_numpy(), df.Lower.to_numpy(), df.Upper.to_numpy())


###################
# End helper code #
###################
##########
# Part 1 #
##########

def predicted_sea_level_rise(show_plot=True):
    """
	Creates a numpy array from the data in sea_level_change.csv where each row
    contains a year, the mean sea level rise for that year, the 2.5th percentile
    sea level rise for that year, the 97.5th percentile sea level rise for that
    year, and the standard deviation of the sea level rise for that year. If
    the year is between 2020 and 2100 and not included in the data, the values
    for that year should be interpolated. If show_plot, displays a plot with
    mean and the 95%, assuming sea level rise follows a linear trend.

	Args:
		show_plot: displays desired plot if true

	Returns:
		a 2-d numpy array with each row containing a year in order from 2020-2100
        inclusive, mean, the 2.5th percentile, 97.5th percentile, and standard
        deviation of the sea level rise for the given year
	"""
    #get tuple of data from load_data(): ([years],[lower],[upper] )
    years, lower, upper  = load_data()
   #init numpy array
    arr = np.zeros((81,5)) #shape 81 rows x 5 cols

    #iterate from 2020-2100 (inclusive)
    for year in range(2020, 2101):

        if year in years:
            idx = np.where(years == year) #get index of the year in its array
            #calulate mean
            mean = (lower[idx]+upper[idx])/2
            std = calculate_std(np.array([lower[idx], upper[idx]]), mean)
            arr[year-2020][0] = year
            arr[year-2020][1] = mean
            arr[year-2020][2] = lower[idx]
            arr[year-2020][3] = upper[idx]
            arr[year-2020][4] = std[1] #assign with positive value of std, which is second elem
        #if year is not in the cvs spreadsheet
        else: 
            #interpolate lower and upper values
            lower_interp = interp(year, years, lower)
            upper_interp = interp(year, years, upper)
            #calculate mean and std from interpolated values
            mean = (lower_interp+upper_interp)/2
            std = calculate_std(np.array([lower_interp, upper_interp]), mean)

            #populate 2d numpy array
            arr[year-2020][0] = year
            arr[year-2020][1] = mean
            arr[year-2020][2] = lower_interp
            arr[year-2020][3] = upper_interp
            arr[year-2020][4] = std[1] #assign with positive value of std, which is second elem

    if show_plot:
        #plot resulting data
        x = arr[:,0] #x-axis is year
        y_mean = arr[:,1] #y-axis is Projected annual mean water level rise (ft)
        y_lower = arr[:,2]
        y_upper = arr[:,3]

        plt.plot(x,y_mean, color="green", label="Mean")
        plt.plot(x,y_upper, color="blue", label="Upper", linestyle='dashed')
        plt.plot(x,y_lower, color="red", label="Lower", linestyle='dashed')
        plt.ylabel(' Projected annual mean water level rise (ft)')
        plt.xlabel('Year')
        plt.legend(loc='best') #add labels
        plt.show()

    return arr




def simulate_year(data, year, num):
    """
	Simulates the sea level rise for a particular year based on that year's
    mean and standard deviation, assuming a normal distribution.

	Args:
		data: a 2-d numpy array with each row containing a year in order from 2020-2100
            inclusive, mean, the 2.5th percentile, 97.5th percentile, and standard
            deviation of the sea level rise for the given year
		year: the year to simulate sea level rise for
        num: the number of samples you want from this year

	Returns:
		a 1-d numpy array of length num, that contains num simulated values for
        sea level rise during the year specified
	"""
    #get info about the particular year from data 2d numpy array
    year_info = data[int(year)-2020]
    sim_value= []
    #np.random.normal(mean, std)
    for i in range(num):
        sim_value.append(np.random.normal(year_info[1], year_info[4]))

    return np.array(sim_value)

    
    
def plot_simulation(data):
    """
	Runs and plots a Monte Carlo simulation, based on the values in data and
    assuming a normal distribution. Five hundred samples should be generated
    for each year.

	Args:
		data: a 2-d numpy array with each row containing a year in order from 2020-2100
            inclusive, mean, the 2.5th percentile, 97.5th percentile, and standard
            deviation of the sea level rise for the given year
	"""
    water_level_points = []
    #run 500 simlations for 81 years
    for year in range(2020,2101):
        water_level_points.append(simulate_year(data, year, 500))

    x = data[:,0]
    y = np.array(water_level_points)

    #plot each result of simulation to the year separately (due to numpy restriction) 
    for i in range(500):
        plt.scatter(x, y[:,i], s=0.5, color="gray")
        
    y_mean = data[:,1] #y-axis is Projected annual mean water level rise (ft)
    y_lower = data[:,2]
    y_upper = data[:,3]

    plt.plot(x,y_mean, color="green", label="Mean")
    plt.plot(x,y_upper, color="blue", label="Upper", linestyle='dashed')
    plt.plot(x,y_lower, color="red", label="Lower", linestyle='dashed')
    plt.ylabel('Relative Water Level Change (ft)')
    plt.xlabel('Year')
    plt.legend(loc='best') #add labels
    plt.ylim([0,14])
    plt.show()
    

##########
# Part 2 #
##########

def simulate_water_levels(data):
    """
	Simulates the water level for all years in the range 2020 to 2100, inclusive.

	Args:
		data: a 2-d numpy array with each row containing a year in order from 2020-2100
            inclusive, mean, the 2.5th percentile, 97.5th percentile, and standard
            deviation of the sea level rise for the given year

	Returns:
		a list of simulated water levels for each year, in the order in which
        they would occur temporally
	"""
    sim_water_yearly =[]
    years = data[:,0]
    for year in years:
        level_rise = simulate_year(data, year, 1)
        sim_water_yearly.append(level_rise[0])

    return sim_water_yearly


def repair_only(water_level_list, water_level_loss_no_prevention, house_value=400000):
    """
	Simulates the water level for all years in the range 2020 to 2100, inclusive,
    and calculates damage costs in 1000s resulting from a particular water level
    for each year dependent on a repair only strategy, where you would only pay
    to repair damage that already happened.

    The specific damage cost can be calculated using the numpy array
    water_level_loss_no_prevention, where each water level corresponds to the
    percent of property that is damaged.

    The repair only strategy is as follows:
        1) If the water level is less than or equal to 5ft, the cost is 0.
        2) If the water level is between 5ft and 10ft, the cost is the
           house_value times the percentage of property damage for that water
           level. If the water level is not an integer value, the percentage
           should be interpolated.
        3) If the water level is at least 10ft, the cost is the entire value of
           the house.

	Args:
		water_level_list: list of simulated water levels for 2020-2100
        water_level_loss_no_prevention: a 2-d numpy array where the first column is
            the SLR levels and the second column is the corresponding property damage expected
            from that water level with no flood prevention (as an integer percentage)
        house_value: the value of the property we are estimating cost for

	Returns:
		an list of damage costs in 1000s, in the order in which the costs would
        be incurred temporally
	"""
    slr_levels = water_level_loss_no_prevention[:,0]
    property_damage = water_level_loss_no_prevention[:,1]

    #call scipy.interpolate with slr_levels as x and property_damage as y
    #this returns function that we can use to interpolate y data points (property damage)
    damage_interp = scipy.interpolate.interp1d(slr_levels,property_damage,fill_value="extrapolate") 

    damage_costs = []
    #iterate thru water level for each year
    for curr_water_level in water_level_list:
        #all water levels are floats, not ints, so we need to interpolated damage loss percentage
        if curr_water_level < 5:
            damage_costs.append(0)
        elif curr_water_level > 10:
            damage_costs.append(house_value/1000)
        else:
            #divide by 100 to convert percentage into decimals, multiply by house value and then divide by 1000
            #to get value in thousands, i.e. 2600 ==> 2.6
            damage_costs.append(house_value*(damage_interp(curr_water_level)/100)/1000)
    return damage_costs


def wait_a_bit(water_level_list, water_level_loss_no_prevention, water_level_loss_with_prevention, house_value=400000,
               cost_threshold=100000):
    """
	Simulates the water level for all years in the range 2020 to 2100, inclusive,
    and calculates damage costs in 1000s resulting from a particular water level
    for each year dependent on a wait a bit to repair strategy, where you start
    flood prevention measures after having a year with an excessive amount of
    damage cost.

    The specific damage cost can be calculated using the numpy array
    water_level_loss_no_prevention and water_level_loss_with_prevention, where
    each water level corresponds to the percent of property that is damaged.
    You should be using water_level_loss_no_prevention when no flood prevention
    measures are in place, and water_level_loss_with_prevention when there are
    flood prevention measures in place.

    Flood prevention measures are put into place if you have any year with a
    damage cost above the cost_threshold.

    The wait a bit to repair only strategy is as follows:
        1) If the water level is less than or equal to 5ft, the cost is 0.
        2) If the water level is between 5ft and 10ft, the cost is the
           house_value times the percentage of property damage for that water
           level, which is affected by the implementation of flood prevention
           measures. If the water level is not an integer value, the percentage
           should be interpolated.
        3) If the water level is at least 10ft, the cost is the entire value of
           the house.

	Args:
		water_level_list: list of simulated water levels for 2020-2100
        water_level_loss_no_prevention: a 2-d numpy array where the columns are
            water levels and the corresponding percent of property damage expected
            from that water level with no flood prevention
        water_level_loss_with_prevention: a 2-d numpy array where the columns are
            water levels and the corresponding percent of property damage expected
            from that water level with flood prevention
        house_value: the value of the property we are estimating cost for
        cost_threshold: the amount of cost incurred before flood prevention
            measures are put into place

	Returns:
		an list of damage costs in 1000s, in the order in which the costs would
        be incurred temporally
	"""

    slr_no_prevention = water_level_loss_no_prevention[:,0]
    damage_no_prevention = water_level_loss_no_prevention[:,1]

    slr_w_prevention = water_level_loss_with_prevention[:,0]
    damage_w_prevention = water_level_loss_with_prevention[:,1]
    

    #call scipy.interpolate with slr_levels as x and property_damage as y
    #this returns function that we can use to interpolate y data points (property damage)
    damage_interp_no_prev = scipy.interpolate.interp1d(slr_no_prevention,damage_no_prevention,fill_value="extrapolate") 
    damage_inrerp_w_prev = scipy.interpolate.interp1d(slr_w_prevention,damage_w_prevention,fill_value="extrapolate") 

    damage_costs_list = []
    #variable to get damage cost with each level rise and compare with threshold value
    damage_cost = 0
    #iterate thru water level for each year
    for i in range(len(water_level_list)):

        if damage_cost < cost_threshold: 
            #all water levels are floats, not ints, so we need to interpolated damage loss percentage
            if water_level_list[i] < 5:
                damage_cost = 0
                damage_costs_list.append(damage_cost)
            elif water_level_list[i] > 10:
                damage_cost = house_value
                damage_costs_list.append(damage_cost/1000)
            else:
                #divide by 100 to convert percentage into decimals, multiply by house value and then divide by 1000
                #to get value in thousands, i.e. 2600 ==> 2.6
                damage_cost = house_value*(damage_interp_no_prev(water_level_list[i])/100)
                damage_costs_list.append(damage_cost/1000)
        else:
            break
    #if threshold value is exceeded we terminate first loop and continue calculations with values if we use preventions measures
    for j in range(i, len(water_level_list)):
        if water_level_list[j] < 5:
            damage_cost = 0
            damage_costs_list.append(damage_cost)
        elif water_level_list[j] > 10:
            damage_cost = house_value
            damage_costs_list.append(damage_cost/1000)
        else:
            #divide by 100 to convert percentage into decimals, multiply by house value and then divide by 1000
            #to get value in thousands, i.e. 2600 ==> 2.6
            damage_cost = house_value*(damage_inrerp_w_prev(water_level_list[j])/100)
            damage_costs_list.append(damage_cost/1000)

    return damage_costs_list





def prepare_immediately(water_level_list, water_level_loss_with_prevention, house_value=400000):
    """
	Simulates the water level for all years in the range 2020 to 2100, inclusive,
    and calculates damage costs in 1000s resulting from a particular water level
    for each year dependent on a prepare immediately strategy, where you start
    flood prevention measures immediately.

    The specific damage cost can be calculated using the numpy array
    water_level_loss_with_prevention, where each water level corresponds to the
    percent of property that is damaged.

    The prepare immediately strategy is as follows:
        1) If the water level is less than or equal to 5ft, the cost is 0.
        2) If the water level is between 5ft and 10ft, the cost is the
           house_value times the percentage of property damage for that water
           level, which is affected by the implementation of flood prevention
           measures. If the water level is not an integer value, the percentage
           should be interpolated.
        3) If the water level is at least 10ft, the cost is the entire value of
           the house.

	Args:
		water_level_list: list of simulated water levels for 2020-2100
        water_level_loss_with_prevention: a 2-d numpy array where the columns are
            water levels and the corresponding percent of property damage expected
            from that water level with flood prevention
        house_value: the value of the property we are estimating cost for

	Returns:
		an list of damage costs in 1000s, in the order in which the costs would
        be incurred temporally
	"""
    slr_w_prevention = water_level_loss_with_prevention[:,0]
    damage_w_prevention = water_level_loss_with_prevention[:,1]
    damage_inrerp_w_prev = scipy.interpolate.interp1d(slr_w_prevention,damage_w_prevention,fill_value="extrapolate") 
    damage_costs_list = []

    for j in range(len(water_level_list)):
        if water_level_list[j] < 5:
            damage_cost = 0
            damage_costs_list.append(damage_cost)
        elif water_level_list[j] > 10:
            damage_cost = house_value
            damage_costs_list.append(damage_cost/1000)
        else:
            #divide by 100 to convert percentage into decimals, multiply by house value and then divide by 1000
            #to get value in thousands, i.e. 2600 ==> 2.6
            damage_cost = house_value*(damage_inrerp_w_prev(water_level_list[j])/100)
            damage_costs_list.append(damage_cost/1000)

    return damage_costs_list

    

def plot_strategies(data, water_level_loss_no_prevention, water_level_loss_with_prevention, house_value=400000,
                    cost_threshold=100000):
    """
	Runs and plots a Monte Carlo simulation of all of the different preparation
    strategies, based on the values in data and assuming a normal distribution.
    Five hundred samples should be generated for each year.

	Args:
		data: a 2-d numpy array with each row containing a year in order from 2020-2100
            inclusive, the 5th percentile, 95th percentile, mean, and standard
            deviation of the sea level rise for the given year
        water_level_loss_no_prevention: a 2-d numpy array where the columns are
            water levels and the corresponding percent of property damage expected
            from that water level with no flood prevention
        water_level_loss_with_prevention: a 2-d numpy array where the columns are
            water levels and the corresponding percent of property damage expected
            from that water level with flood prevention
        house_value: the value of the property we are estimating cost for
        cost_threshold: the amount of cost incurred before flood prevention
            measures are put into place
	"""
    x_vals = data[:,0] #x-axis is year
    #get water level list
    repair, wait, prepare = [],[],[]
    for i in range(500):
        #call 3 functions for 500 times, each time with diferent water levels returned from simulation function
        y_repairs = repair_only(simulate_water_levels(data), water_level_loss_no_prevention, house_value)
        repair.append(y_repairs)
        plt.scatter(x_vals, y_repairs, s=.5, color="gray")


        y_wait = wait_a_bit(simulate_water_levels(data), water_level_loss_no_prevention, water_level_loss_with_prevention, house_value, cost_threshold)
        wait.append(y_wait)
        plt.scatter(x_vals, y_wait,  s=.5, color="teal")

        y_prep = prepare_immediately(simulate_water_levels(data), water_level_loss_with_prevention, house_value)
        prepare.append(y_prep)
        plt.scatter(x_vals, y_prep, s=.5, color="slategrey")
    
    #we have 3 arrays with 81 columns (damage costs per year) and 500 rows (because 500 times simulation) 
    #we need to find mean for each year
    #np.meas(some_array, axis=0) takes mean of each column of the array

    plt.plot(x_vals,np.mean(repair, axis=0), color="green", label="Repair-Only Scenario")
    plt.plot(x_vals,np.mean(wait, axis=0), color="blue", label="Wait-a-Bit Scenario")
    plt.plot(x_vals,np.mean(prepare, axis=0), color="red", label="Prepare-Immediately Scenario")

    plt.ylabel('Estimated Damage Cost($k)')
    plt.xlabel('Year')
    plt.legend(loc='best') #add labels

    plt.show()

if __name__ == '__main__':
    pass
    # Comment out the 'pass' statement below to run the lines below it

    # # Uncomment the following lines to plot generate plots
    data = predicted_sea_level_rise()
    # water_level_list=simulate_water_levels(data)
    # water_level_loss_no_prevention = np.array([[5, 6, 7, 8, 9, 10], [0, 10, 25, 45, 75, 100]]).T
    # water_level_loss_with_prevention = np.array([[5, 6, 7, 8, 9, 10], [0, 5, 15, 30, 70, 100]]).T

    plot_simulation(data)
    # plot_strategies(data, water_level_loss_no_prevention, water_level_loss_with_prevention)
