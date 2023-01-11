# -*- coding: utf-8 -*-
# Problem Set 5: Modeling Temperature Change
# Name:
# Collaborators:

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import re
from sklearn.cluster import KMeans
import math
# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAIN_INTERVAL = range(1961, 2000)
TEST_INTERVAL = range(2000, 2017)

##########################
#    Begin helper code   #
##########################

def standard_error_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by a linear
            regression model
        model: a numpy array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = np.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

# KMeans class not required until Problem 7
class KMeansClustering(KMeans):

    def __init__(self, data, k):
        super().__init__(n_clusters=k, random_state=0)
        self.fit(data)
        self.labels = self.predict(data)

    def get_centroids(self):
        'return np array of shape (n_clusters, n_features) representing the cluster centers'
        return self.cluster_centers_

    def get_labels(self):
        'Predict the closest cluster each sample in data belongs to. returns an np array of shape (samples,)'
        return self.labels

    def total_inertia(self):
        'returns the total inertia of all clusters, rounded to 4 decimal points'
        return round(self.inertia_, 4)



class Dataset(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Dataset instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_daily_temps(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d numpy array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return np.array(temperatures)

    def get_temp_on_date(self, city, month, day, year):
        """
        Get the temperature for the given city at the specified date.

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified date and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year {} is not available".format(year)
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

##########################
#    End helper code     #
##########################

    def calculate_annual_temp_averages(self, cities, years):
        """
        For each year in the given range of years, computes the average of the
        annual temperatures in the given cities.

        Args:
            cities: a list of the names of cities to include in the average
                annual temperature calculation
            years: a list of years to evaluate the average annual temperatures at

        Returns:
            a 1-d numpy array of floats with length = len(years). Each element in
            this array corresponds to the average annual temperature over the given
            cities for a given year.
        """
        #cities  = cols
        #years = rows
        temps = [] 
        for year in years:
            curr = []
            for city in cities:
                curr.append(np.mean(self.get_daily_temps(city, year)))
            temps.append(sum(curr)/len(curr))
        return np.array(temps)
        


def linear_regression(x, y):
    """
    Calculates a linear regression model for the set of data points.

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points

    Returns:
        (m, b): A tuple containing the slope and y-intercept of the regression line,
                both of which are floats.
    """

    m = ((x - np.mean(x))*(y-np.mean(y))).sum()/((x - np.mean(x))**2).sum()
    b = np.mean(y) - (m*np.mean(x))
    return (m,b)


def squared_error(x, y, m, b):
    '''
    Calculates the squared error of the linear regression model given the set
    of data points.

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        m: The slope of the regression line
        b: The y-intercept of the regression line


    Returns:
        a float for the total squared error of the regression evaluated on the
        data set
    '''
    y_est = m*x + b
    return ((y-y_est)**2).sum()




def generate_polynomial_models(x, y, degrees):
    """
    Generates a list of polynomial regression models with degrees specified by
    degrees for the given set of data points

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        degrees: a list of integers that correspond to the degree of each polynomial
            model that will be fit to the data

    Returns:
        a list of numpy arrays, where each array is a 1-d numpy array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    fits=[]
    for d in degrees:
        fits.append(np.array(np.polyfit(x,y,d)))
    return fits

def evaluate_models(x, y, models, display_graphs=False):
    """
    For each regression model, compute the R-squared value for this model and
    if display_graphs is True, plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as green dots and your best
    fit curve (i.e. the model) as an orange solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        Degree of your regression model,
        R-squared of your model evaluated on the given data points,
        and standard error/slope (if this model is linear).

    R-squared and standard error/slope should be rounded to 4 decimal places.

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial
        display_graphs: A boolean whose value specifies if the graphs should be
            displayed

    Returns:
        A list holding the R-squared value for each model
    """
    r2_list = []
    for model in models:
        #get r2 value

        est_Y = np.polyval(model, x)
        r2 = (r2_score(y, est_Y)).round(4)
        r2_list.append(r2)
        #if polynomial is 1st degree
        #plot
        if display_graphs:
            plt.ylabel('Degrees (Celcius)')    
            plt.xlabel('Years')
            degree = len(model) -1
            plt.scatter(x,y, c="green")
            plt.plot(x,est_Y, c="orange")
            plt.locator_params(integer=True)


            if len(model) == 2:
                se_ratio = (standard_error_over_slope(x,y, est_Y, model)).round(4)
                plt.title(f"R^2={r2}, Degree={degree}, ratio of standard error = {se_ratio}".format(r2,degree,se_ratio))
            else:
                plt.title(f"R^2={r2}, Degree={degree}".format(r2,degree))                
        plt.show()

    return r2_list

def get_max_trend(x, y, length, positive_slope):
    """
    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        length: the length of the interval
        positive_slope: a boolean whose value specifies whether to look for
            an interval with the most extreme positive slope (True) or the most
            extreme negative slope (False)

    Returns:
        a tuple of the form (i, j, m) such that the application of linear (deg=1)
        regression to the data in x[i:j], y[i:j] produces the most extreme
        slope m, with the sign specified by positive_slope and j-i = length.

        In the case of a tie, it returns the first interval. For example,
        if the intervals (2,5) and (8,11) both have slope 3.1, (2,5,3.1) should be returned.

        If no intervals matching the length and sign specified by positive_slope
        exist in the dataset then return None
    """
    curr = (None, None, 0.0)
    i = 0
    slopes =[]
    
    for j in range(len(x)+1):
        if j-i == length:
            m,b = linear_regression(x[i:j], y[i:j])
            slopes.append((i,j,m))

            if positive_slope:
                if m > curr[2] and (m-curr[2] > 1e-8):
                    curr = (i,j,m)
            elif positive_slope== False:
                if m < curr[2] and (curr[2]-m > 1e-8):
                    curr = (i,j,m)            
            i +=1

    if curr[0] == None:
        return None
    return curr


def get_all_max_trends(x, y):
    """
    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points

    Returns:
        a list of tuples of the form (i,j,m) such that the application of linear
        regression to the data in x[i:j], y[i:j] produces the most extreme
        positive OR negative slope m, and j-i=length.

        The returned list should have len(x) - 1 tuples, with each tuple representing the
        most extreme slope and associated interval for all interval lengths 2 through len(x).
        If there is no positive or negative slope in a given interval length L (m=0 for all
        intervals of length L), the tuple should be of the form (0,L,None).

        The returned list should be ordered by increasing interval length. For example, the first
        tuple should be for interval length 2, the second should be for interval length 3, and so on.

        If len(x) < 2, return an empty list
    """
    #[1,2,3,4,5]
    if len(x) < 2: return []
    results = []


    for interval in range(2,len(x)+1):
        curr = (0, interval, 0) #None = i:j
        i = 0

        for j in range(len(x)+1):
            if j-i == interval:
                m,b = linear_regression(x[i:j], y[i:j])
                
                if abs(m) > abs(curr[2]):
                    curr = (i,j,m)
                i +=1
        if curr[2] != 0:
            results.append(curr)
        else:
            results.append((0,interval, None))

    return results




def calculate_rmse(y, estimated):
    """
    Calculate the root mean square error term.
    Args:
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    rmse = ((y-estimated)**2).sum()/len(y)
    return math.sqrt(rmse)



def evaluate_rmse(x, y, models, display_graphs=False):
    """
    For each regression model, compute the RMSE for this model and if
    display_graphs is True, plot the test data along with the model's estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    RMSE should be rounded to 4 decimal places.

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N test data sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N test data sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.
        display_graphs: A boolean whose value specifies if the graphs should be
            displayed

    Returns:
        A list holding the RMSE value for each model
    """
    rmse_list = []
    for model in models:
        #get r2 value
        est_Y = np.polyval(model, x)
        rmse = round(calculate_rmse(y, est_Y), 4)
        rmse_list.append(rmse)
        if display_graphs:
            plt.ylabel('Degrees (Celcius)')    
            plt.xlabel('Years')
            degree = len(model) -1
            plt.scatter(x,y, c="green")
            plt.plot(x,est_Y, c="orange")

            plt.title(f"RMSE={rmse}, Degree={degree}".format(rmse,degree))                
            plt.show()

    return rmse_list

def cluster_cities(cities, years, data, n_clusters):
    '''
    Clusters cities into n_clusters clusters using their average daily temperatures
    across all years in years. Generates a line plot with the average daily temperatures
    for each city. Each cluster of cities should have a different color for its
    respective plots.

    Args:
        cities: a list of the names of cities to include in the average
                daily temperature calculations
        years: a list of years to include in the average daily
                temperature calculations
        data: a Dataset instance
        n_clusters: an int representing the number of clusters to use for k-means

    Note that this part has no test cases, but you will be expected to show and explain
    your plots during your checkoff
    '''
    raise NotImplementedError   


if __name__ == '__main__':
    ##################################################################################
    # Problem 4A: DAILY TEMPERATURE     
    ds = Dataset('data.csv')
    x, y = [], []
    for year in range(1971, 2016):
        x.append(year)
        y.append(ds.get_temp_on_date('SAN FRANCISCO', 12, 1, year))

    #generate polynomial model
    model = generate_polynomial_models(np.array(x),np.array(y),[1])
    evaluate_models(np.array(x),np.array(y), model, display_graphs=True)


    ##################################################################################
    # Problem 4B: ANNUAL TEMPERATURE
    x = range(1971, 2016)
    y = ds.calculate_annual_temp_averages(['SAN FRANCISCO'], x)
    
    model = generate_polynomial_models(np.array(x),y,[1])
    evaluate_models(np.array(x),y, model, display_graphs=True)

    ##################################################################################
    # Problem 5B: INCREASING TRENDS
    years = [i for i in range(1961,2017)]
    yearly_temps = ds.calculate_annual_temp_averages(['SEATTLE'], years)


    result_pos = get_max_trend(years, yearly_temps, 30, True)
    i = result_pos[0]
    j = result_pos[1]
    x = np.array(years[i:j])
    y = np.array(yearly_temps[i:j])
    model = np.polyfit(x, y, 1)
    evaluate_models(x,y, [model], display_graphs=True)
    # ##################################################################################
    # # Problem 5C: DECREASING TRENDS
    years = [i for i in range(1961,2017)]


    yearly_temps = ds.calculate_annual_temp_averages(['SEATTLE'], years)
    result_pos = get_max_trend(years, yearly_temps, 12, False)
    i = result_pos[0]
    j = result_pos[1]
    x = np.array(years[i:j])
    y = np.array(yearly_temps[i:j])
    model = np.polyfit(x, y, 1)
    evaluate_models(x,y, [model], display_graphs=True)

    ##################################################################################
    # Problem 5D: ALL EXTREME TRENDS
    # Your code should pass test_get_max_trend. No written answer for this part, but
    # be prepared to explain in checkoff what the max trend represents.

    ##################################################################################
    # # Problem 6B: PREDICTING
    train_set = ds.calculate_annual_temp_averages(CITIES, TRAIN_INTERVAL)
    models = generate_polynomial_models(np.array(TRAIN_INTERVAL),train_set,[2,10])
    evaluate_models(np.array(TRAIN_INTERVAL),train_set, models, display_graphs=True)


    test_set = ds.calculate_annual_temp_averages(CITIES, TEST_INTERVAL)
    evaluate_rmse(TEST_INTERVAL, test_set, models, display_graphs=True)


    ##################################################################################
    # Problem 7: KMEANS CLUSTERING (Checkoff Question Only)


    ####################################################################################
