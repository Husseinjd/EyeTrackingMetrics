import numpy as np
import pandas as pd
import glob
import os
from eyesmetriccalculator import EyesMetricCalculator
from transition_matrix import *
import csv

def getGazeTrails(file):
	df = pd.read_csv(file,sep='\t')
	df=df[["Event","Gaze point X", "Gaze point Y","Gaze event duration","Fixation point X","Fixation point Y"]]  # select columns

	normal_start_idx=df[df['Event'] == 'Normal Trial Start'].index.to_numpy() 
	normal_stop_idx=df[df['Event'] == 'Normal Trail End'].index.to_numpy() 
	attack_start_idx=df[df['Event'] == 'Attack Trial Start'].index.to_numpy() 
	attack_stop_idx=df[df['Event'] == 'Attack Trial End'].index.to_numpy() 

	# print(normal_start_idx)
	# print(normal_stop_idx)
	# print(attack_start_idx)
	# print(attack_stop_idx)

	start_idx=np.hstack((normal_start_idx,attack_start_idx))
	stop_idx=np.hstack((normal_stop_idx,attack_stop_idx))

	# print(start_idx)
	# print(stop_idx)

	df=df[["Gaze point X", "Gaze point Y","Gaze event duration","Fixation point X","Fixation point Y"]]  # select columns

	alltrials=[]
	for i in range(stop_idx.shape[0]):
		alltrials.append(df.loc[start_idx[i]:stop_idx[i]].dropna().to_numpy())
	return(alltrials)

def getAOI(nx, ny, screen_dimension):
	#Setting important variables
	TEST_VERTICES_1 = [[ 20,20] , [400,250], [40,400]]
	TEST_VERTICES_2 = [[800,800], [1000,800], [700,650]]

	x = np.linspace(0, screen_dimension[0], nx)
	y = np.linspace(0, screen_dimension[1], ny)

	xv, yv = np.meshgrid(x, y)
	# print(x)
	# print(y)
	# print(xv.shape)
	# print(yv.shape)

	aoiDict = {}
	vertices=np.zeros((4,2))
	for i in range(xv.shape[0]-1):
		for j in range(xv.shape[1]-1):
			aoiName='aoi_'+str(i)+'_'+str(j)
			vertices[0,:]=np.array([xv[i,j],yv[i,i]])
			vertices[1,:]=np.array([xv[i,j+1],yv[i,j+1]])
			vertices[2,:]=np.array([xv[i+1,j+1],yv[i+1,j]])
			vertices[3,:]=np.array([xv[i+1,j],yv[i+1,j+1]])
			# print(vertices)
			aoiDict[aoiName]=PolyAOI(screen_dimension,vertices)

	# print(len(aoiDict))

	return(aoiDict)

def getSGE_GTE(trials):
	"""
	input: gaze and fixation data for one participant (i.e. 20 trials. 10 normal, 10 attack)
	output: list of 40 elements (10 normal SGE, 10 attack SGE, 10 normal GTE, 10 attack GTE)
	"""

	SGEdata=[]
	GTEdata=[]
	# print("trialshape",len(trials))
	for trial in trials:
		gaze=np.zeros((trial.shape[0],3))
		gaze[:,:2]=trial[:,:2]
		fixation=trial[:,2:]
		fixation=fixation[:,[1,2,0]]	
		ec = EyesMetricCalculator(fixation,gaze,TEST_SCREENDIM)
		# print('ConvexHullArea: ' ,ec.convexHull('area').compute() )
		# print('SpatialDensity: ' , ec.spatialDensity(30,40).compute())
		# print('NNI Metric: ' , ec.NNI().compute())
		SGE=ec.GEntropy(TEST_AOI_DICT,'stationary').compute()
		GTE=ec.GEntropy(TEST_AOI_DICT,'transition').compute()
		# gz = GazeTransitions(TEST_SCREENDIM, TEST_AOI_DICT, gaze)
		# gz.plot_all(annotate_points=True)

		# print(trial)
		# print(gaze)
		# print(fixation)
		# print(SGE,GTE)
		SGEdata.append(SGE)
		GTEdata.append(GTE)
	return(SGEdata+GTEdata)


if __name__ == '__main__':
	TEST_SCREENDIM = [1920,1080]
	TEST_AOI_DICT=getAOI(11,11,TEST_SCREENDIM)
	folder_name = 'data'
	allgazedata=[]
	for f in sorted(glob.glob(folder_name + "/*.tsv")):
		print("Processing file: ",f)
		trials=getGazeTrails(f) #"Gaze point X", "Gaze point Y","Gaze event duration","Fixation point X","Fixation point Y"
		if len(trials)<20:
			print("Incomplete data for this file {}".format(f))
		else:
			gazedata=getSGE_GTE(trials) 
			allgazedata.append(gazedata)

	with open("gazedata.csv", 'w') as csvfile: 
	    # creating a csv writer object 
	    csvwriter = csv.writer(csvfile) 
	    # writing the fields 
	    csvwriter.writerow(["SGE normal"]*10 + ["SGE attack"]*10 + ["GTE normal"]*10 + ["GTE attack"]*10) 
	    # writing the data rows 
	    csvwriter.writerows(allgazedata)

	# np.save('gazedata', np.array(allgazedata))