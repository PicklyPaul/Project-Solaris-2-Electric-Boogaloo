# Project-Solaris-2-Electric-Boogaloo
  This is a long-term prediction weather app originally built for the 2025 NASA Space Apps competition. This weather app uses over 20 years of satelite data to predict the following years weather. The weather is measured on a monthly basis on a 1 degree grid(70mi*70mi), with it being able to generate temperature results within the real daily fluctuations of our location. Additionally due to limitations with dataset, it is limited to on land and excludes Antartica.

Required libraries:

pywebview

h5py

pandas

earthaccess(extra info below)

Extra Information on Earthaccces:

  Earthaccess is nasa's library to extract information from their opendas repository. We use it to download the GLDAS dataset. For the moment, the data will need to be downloaded, and so an earthaccess login is required every time the app is run, or can be hard coded in the compute file. In the future, we will still require earthacces login, but that will be provided with another file, so no extra steps will need to be done on the user end.
