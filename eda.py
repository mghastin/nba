from player import *
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
import math

# Prints histograms for the seasons given in 'years' list and a subplot for each attribute in 'attributes'
# NUM_BINS determines the number of bars, default is set at 10
# player is a Player object

def multiyear_histogram(player, years, attributes, NUM_BINS=10):
	
	# get matrices with data for years and attributes requested
	data = {}
	for attribute in attributes:
		matrices = []
		for year in years:
			val_matrix = player.get_data(attribute, year).dropna().as_matrix()
			#val_matrix = val_matrix[np.logical_not(pd.isnull(val_matrix))]
			matrices.append(val_matrix)
		data[attribute] = matrices
	
	# Determine MIN and MAX of all year distributions for given attribute (to be plotted together)
	plt.style.use('seaborn-deep')
	f, axarr = plt.subplots(1, len(attributes))
	a = 0
	for attribute, matrices in data.iteritems():
		MIN = np.nan
		MAX = np.nan
		for matrix in matrices:
			if np.isnan(MIN) or np.min(matrix) < MIN:
				MIN = np.min(matrix)
			if np.isnan(MAX) or np.max(matrix) > MAX:
				MAX = np.max(matrix)
		COUNT_BY = math.trunc((MAX - MIN) / NUM_BINS) 
		if COUNT_BY < 1:
			COUNT_BY = 1
		i = MIN
		bins = []	
		while i <= MAX:
			bins.append(i)
			i += COUNT_BY
		axarr[a].hist(matrices, bins, label=years, normed = 1, edgecolor = 'black')
		axarr[a].set_xlabel(attribute)
		axarr[a].legend(loc='upper right')
		i = 0
		for year in years:
			y = mlab.normpdf(bins, np.mean(matrices[i]), np.std(matrices[i]))
			axarr[a].plot(bins, y, '--')
			text = year + ': $\mu$ = ' + str(round(np.mean(matrices[i]),2)) + ' , $\sigma$ = ' + str(round(np.std(matrices[i]),2))
			axarr[a].text(0, 1-i*0.05,text, horizontalalignment='left', verticalalignment='bottom', transform=axarr[a].transAxes)
			i += 1
		a += 1

	return;

#names = ['Andre Drummond', 'Reggie Jackson', 'Tobias Harris', 'Marcus Morris', \
#			'Stanley Johnson', 'Ish Smith', 'Kentavious Caldwell-Pope', 'Avery Bradley']
#players = {}
#for name in names:
#	players[name] = Player(name)
#print players['Andre Drummond'].get_attributes()
#multiyear_histogram(Player('Kentavious Caldwell-Pope'), ['2016'], ['+/-', '3P%', 'FG%'])
#multiyear_histogram(Player('Avery Bradley'), ['2017'], ['+/-', '3P%', 'FG%'])

val_matrix1 = Player('Kentavious Caldwell-Pope').get_data('FG%', '2016').dropna().as_matrix()
val_matrix2 = Player('Avery Bradley').get_data('FG%', '2017').dropna().as_matrix()

'''
data_to_get = [(('Reggie Jackson', '2017', 'PG'), ('Reggie Jackson', '2016', 'PG')), \
				(('Avery Bradley', '2017', 'SG'), ('Kentavious Caldwell-Pope', '2016', 'SG')), \
				(('Stanley Johnson', '2017', 'SF'), ('Marcus Morris', '2016', 'SF')), \
				(('Tobias Harris', '2017', 'PF'), ('Tobias Harris', '2016', 'PF')), \
				(('Andre Drummond', '2017', 'C'), ('Andre Drummond', '2016', 'C')) \
				]

attributes = ['FG%','3P%','FT%','PTS', 'AST', 'REB','+/-'] 
NUM_ROWS = 4
NUM_COLS = 2
f, axarr = plt.subplots(NUM_ROWS, NUM_COLS)
x = 0
y = 0
for attribute in attributes:
	print x, y
	matrices = []
	labels = []
	for comparison in data_to_get:
		for player_num in range(0,2):
			df = Player(comparison[player_num][0]).get_data(attribute, comparison[player_num][1])
			matrix = df.dropna().as_matrix()
			matrix = matrix.reshape(matrix.size, 1)
			matrices.append(matrix)
			label = comparison[player_num][2] + " " + comparison[player_num][1] # create label with player name + year
			labels.append(label)
	title = attribute + ' 2017 vs 2016'
	bp = axarr[y, x].boxplot(matrices, showmeans=True, labels=labels, patch_artist=True) 
	colors = ['red', 'blue', 'red', 'blue', 'red','blue', 'red', 'blue', 'red', 'blue']
	for patch, color in zip(bp['boxes'], colors):
	    patch.set_facecolor(color)
	if y == NUM_ROWS - 1:
		x += 1
		y = 0
		# Go to the next column, first row
	elif y < NUM_ROWS - 1:
		y += 1
	else:
		print "Houston we have a problem with the subplot index counters."
plt.tight_layout()
plt.show()
'''

data_to_get = [(('Reggie Jackson', '2017', 'PG'), ('Reggie Jackson', '2016', 'PG')), \
				(('Avery Bradley', '2017', 'SG'), ('Kentavious Caldwell-Pope', '2016', 'SG')), \
				(('Stanley Johnson', '2017', 'SF'), ('Marcus Morris', '2016', 'SF')), \
				(('Tobias Harris', '2017', 'PF'), ('Tobias Harris', '2016', 'PF')), \
				(('Andre Drummond', '2017', 'C'), ('Andre Drummond', '2016', 'C')) \
				]

'''data_to_get = [(('Ish Smith', '2017', 'PG'), ('Ish Smith', '2016', 'PG')), \
				(('Luke Kennard', '2017', 'SG'), ('Reggie Bullock', '2016', 'SG')), \
				(('Reggie Bullock', '2017', 'SF'), ('Stanley Johnson', '2016', 'SF')), \
				(('Anthony Tolliver', '2017', 'PF'), ('Jon Leuer', '2016', 'PF')), \
				(('Eric Moreland', '2017', 'C'), ('Aron Baynes', '2016', 'C')) \
				]
'''				
	

attributes = ['FG%','3P%','FT%','PTS', 'AST', 'REB','+/-'] 
NUM_ROWS = 1
NUM_COLS = 1
#x = 0
#y = 0
for attribute in attributes:
	f, axarr = plt.subplots(NUM_ROWS, NUM_COLS)
	#print x, y
	matrices = []
	labels = []
	for comparison in data_to_get:
		for player_num in range(0,2):
			df = Player(comparison[player_num][0]).get_data(attribute, comparison[player_num][1])
			matrix = df.dropna().as_matrix()
			matrix = matrix.reshape(matrix.size, 1)
			matrices.append(matrix)
			label = comparison[player_num][2] + " " + comparison[player_num][1] # create label with player pos + year
			labels.append(label)
	title = attribute + ' 2017 vs 2016'
	axarr.set_title(title)
	bp = axarr.boxplot(matrices, showmeans=True, labels=labels, patch_artist=True) 
	colors = ['red', 'blue', 'red', 'blue', 'red','blue', 'red', 'blue', 'red', 'blue']
	for patch, color in zip(bp['boxes'], colors):
	    patch.set_facecolor(color)
	'''if y == NUM_ROWS - 1:
		x += 1
		y = 0
		# Go to the next column, first row
	elif y < NUM_ROWS - 1:
		y += 1
	else:
		print "Houston we have a problem with the subplot index counters."
		'''
plt.tight_layout()
plt.show()






#f, axarr = plt.subplots(1, 2)
#print val_matrix1
#print val_matrix1.shape
#rint val_matrix1.reshape(1,81)
#print val_matrix1.reshape(1,81).shape
#axarr[0].boxplot(val_matrix1.reshape(1,81))
#matrices = [val_matrix1.reshape(val_matrix1.size,1), val_matrix2.reshape(val_matrix2.size,1)]
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.set_title(title)
#bp = ax.boxplot(matrices, showmeans=True, labels=labels, patch_artist=True) #,boxprops=dict(facecolor="red"))

#colors = ['red', 'red', 'blue', 'blue', 'red','red', 'blue', 'blue', 'red', 'red']
#colors = ['red', 'blue', 'red', 'blue', 'red','blue', 'red', 'blue', 'red', 'blue']
#for patch, color in zip(bp['boxes'], colors):
#    patch.set_facecolor(color)
#for patch in bp['boxes']:
#        patch.setp(facecolor='blue')
#ax.tick_params('x', rotation=90)




#print array
#plt.boxplot(array)
#axarr[1].boxplot(val_matrix2)

#multiyear_histogram(players['Andre Drummond'], ['2016','2017'], ['REB', '+/-', 'PTS'])
#multiyear_histogram(players['Andre Drummond'], ['2016', '2017'], ['AST', 'BLK', 'STL'])
#multiyear_histogram(players['Andre Drummond'], ['2016', '2017'],  ['FT%', 'FG%']) 
