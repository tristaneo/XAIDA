if __name__=="__main__":

	import numpy as np
	import pandas as pd
	import matplotlib.pyplot as plt
	import itertools
	import seaborn as sns
	############### EDIT ################

	# sites: FR-Pue - med forest site, FR-Fon - paris forest

	sites = input("Which SITE do you want to analyise? (FR-Pue, FR-Fon) ")


	ecovar = input("Which VARIABLE do yuo want to use? (GPP, NEE, Reco) ")

	####################################

	start_dates = {"FR-Pue": "2000-1-1", "FR-Fon": "2005-1-1"}

	site_dates = {"FR-Pue": ["2000-1-1","2014-12-31"], "FR-Fon": ["2005-1-1","2014-12-31"]}

	path2flux = "/home/tristan/Documents/XAIDA/FLUXNET/Data"

	#####################################
	# function to read in flux data from csv format, for each site, for chosen ecovar

	def read_flux(filename, site, fluxvar):
		"""
		This function reads in fluxnet measurements from the orig dataset into a new dataframe,
		we include checking for missing data, it returns the naan values and the ecovar variable
		with the associated timesteps. 
		"""
		print("Reading in "+fluxvar+" obs")
		flux_hourly = pd.read_csv(filename)

		if fluxvar=="GPP":
			varname = "GPP_NT_VUT_REF"
		elif fluxvar=="Reco":
			varname = "Reco_NT_VUT_REF"
		elif fluxvar=="NEE":
			varname = "NEE_VUT_REF"

		flux_tmp = pd.DataFrame({fluxvar: np.array(flux_hourly[varname])}, columns=[fluxvar])

		flux_tmp[flux_tmp == '-9999'] = np.nan

		# pandas df to numpy array
		flux_tmp = flux_tmp.values
	
		# flatten -> 1D array	
		flux_tmp = np.array(list(itertools.chain(*flux_tmp)))

		# return indicies where there is nan values
		nan_inds = np.argwhere(np.isnan(flux_tmp))
		print(nan_inds, 'nans')

		flux_tmp = pd.DataFrame({fluxvar: flux_tmp}, columns=[fluxvar])


		flux_tmp["date"] = pd.date_range(start_dates[site], periods=len(flux_tmp), freq = "30min")
	
		flux_tmp = flux_tmp.set_index(["date"])
		avg_tmp = flux_tmp.resample('D').mean()
	
		print(flux_tmp)
	
		print(avg_tmp)
	
		return flux_tmp, nan_inds, avg_tmp

	flux_var, flux_var_nan_inds, avg_var = read_flux(path2flux+"/FLX_"+sites+"_FLUXNET2015_FULLSET_HH.csv", sites, ecovar)

	sns.lineplot(data = avg_var[ecovar])
	plt.show()


