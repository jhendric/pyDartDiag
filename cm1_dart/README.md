# cm1_dart
A collection of Python scripts for running CM1 with the DART data assimilation system

REQUIREMENTS
This requires at least version 18.3 of the CM1 model code, available at:
http://www2.mmm.ucar.edu/people/bryan/cm1/

And a developmental branch of the DART code (by request only):
https://www.image.ucar.edu/DAReS/DART/

On the Python end, the only requirement outside of the Python Standard Library is the netcdf4-python library:
https://github.com/Unidata/netcdf4-python

EXAMPLE EXPERIMENT SEQUENCE

1) Extract the repository into a working directory

2) Edit the file <b>ens\_dart\_param.py</b>.  Most important changes are to change the "exp\_name" variable to match the name of your current working directory, and the "dir" variable to match the path to where everything is located.  If you plan to follow a different directory structure, edit all of the "dir\_*" variables to point to relevant locations.  
--If using a queueing system for your experiment, edit the section of ens\_dart\_param.py that deals with the queue names, number of processors, etc.  The scripts by default will decide whether you are running on Yellowstone or a local cluster using PBS and submit scripts accordingly.  
--Edit the section having do with experiment parameters (dt, grid\_resolutions) to match what you have in your CM1 namelist.input file.  Also set "Ne" to be the number of ensemble members to use.  Make sure that "cycle\_len" is set to the number of seconds in each assimilation cycle and "fcst\_len" is set to be any additional forecast time you want CM1 to run beyond the cycling length (or 0 will just cycle the enemble without producing additional forecasts).
--Parameters relating to localization are at the end of the file

3) Run the script <b>set\_all\_scripts.py</b>.  This will update the source paths in each script to point to your main working directory.

4) Copy in all needed auxilliary files for running CM1 and DART into your working directory.  This is usually a CM1 namelist.input file, a template DART input.nml file, and an input_sounding file for CM1 (optional, only if initializing with a real sounding.

5) Run the script <b>make\_ensemble.py</b>.  This will go to the directory specified by "dir\_mems" in ens\_dart\_param.py and make a separate directory for each ensemble member.  This directory will be populated with the required cm1 files.

ENSEMBLE CYCLING LOOP
6) Run the <b>submit\_all.py</b> script while specifying the starting time of this cycle in seconds.  For instance, at the initial time, you would run:
<b>./submit\_all.py -d 0</b>

7) Wait for all members to finish.  You can check on their status by running the script <b>check\_ensemble\_status.py</b> and specifying <i>the time the ensemble is building towards</i>.  For instance, if my current ensemble cycle is integrating from time=0 seconds to time=3600 seconds, to check on the status I would run:
<b>./check\_ensemble\_status.py -d 3600</b>
This will return information about which ensemble members are running, which have finished, which are waiting in the queue, and which may have exited in error.  If all ensemble members are completed, the script will check to be sure that they all have produced restart files valid at the specified time.

8) When all ensemble members are done, run DART by using <b>submit\_filter.py</b>.  Here, we give the script the time (in seconds) that the ensemble is currently at, e.g.:
<b>./submit\_filter.py -d 3600</b>
This will run the DART sequence in the "assimilation" subdirectory.  Here we assume that you already have generated observation sequence files (separate for each assimilation cycle) in the "obs" subdirectory, and that these files are named "NNNNNN\_obs\_seq.prior", where NNNNNN is the integer time in seconds of the simulation when the observations are valid.  There is an example script mentioned below that helps generate those observations.  The settings DART will use are specified in the master input.nml file located in your working directory, including the variable types to assimilate and the components of the state vector.  Output diagnostics from the assimilation will be saved to the "longsave" subdirectory.  Because we are using direct NETCDF IO, there is no need to move any "new" initial condition files for each member; their restart files will be updated in place.

9) Go back to step 6 and re-submit the ensemble, specifying the new start time (in seconds).  Repeat steps 6-9 for the duration of the experiment.

EXTRA SCRIPTS

--To run an entire experiment automatically, use the <b>autorun\_ensemble.py</b> script.  You are required to manually proceed through at least step 6 above.  However, once all the ensemble members have been submitted, you may run the autorun script, specifying the <i>starting time of the current integration cycle</i>, e.g.:
<b>./autorun\_ensemble.py -d 0</b>.
This script uses the exp\_length and cycle\_length parameters from ens\_dart\_param.py to cycle the ensemble until exp_length has been reached.  This script assumes that observation sequence files for all cycle times exist in the "obs" subdirectory before beginning.

--To generate OSSE/ideal observations, the script <b>make\_osse\_obs.py</b> provides a template for doing so.  This script basically automates the perfect\_model\_obs sequence from DART.  It is presently set up to make a grid of observations of arbitrary densities and types, but could be adapted for other networks.





