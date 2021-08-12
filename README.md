##      Setup profile on Pawsey

First you'll have to setup your profile and bashrc files for running jobs on Garrawarla. My bashrc and profile scripts are uploaded as "bashrc-pawsey" and "profile-pawsey". The key environmental variables you need to set are the variables *MWA_DIR*, *MWA_BEAM_FILE*, and *MWA_ASVO_API_KEY*.  You should also module load/use the modules listed under Garrawarla in *profile-pawsey*. 

- To set the *MWA_BEAM_FILE* you can use the same location I use */pawsey/mwa/mwa_full_embedded_element_pattern.h5*.

- For the *MWA_DIR* location you need to create a directory which has a subdirectory named 'data'.  For EoR jobs I use *MWA_DIR=/astro/mwaeor/MWA/* and there is a directory */astro/mwaeor/MWA/data*. For transients jobs I created my own "data" directory in */astro/mwasci/clynch/*. 

- The *MWA_ASVO_API_KEY* is assigned to you when you make an account with the MWA ASVO website (https://asvo.mwatelescope.org/), you should be able to login using your uni-credentials. 

##      Downloading data to Garrawarla

To download the data you should use the package 'gator' which is already installed on Garrawarla. More info on this package can be found here:

https://gitlab.com/chjordan/gator

Gator is run in two steps: (1) create a sql database (2) submit the database to download from the MWA ASVO.

1. To create the database you'll need a text file where each line is the observation ID you want to download. I've uploaded an example of two observations that I downloaded. For a large number of observations, you can get the observation IDs from the MWA ASVO by searching for the observations. You can export the observations by selecting them and then choosing either to export a conversion job or a download job (either works, you just need the obs IDs). Then modify the csv file to create your observation list text file. 

You might need to use **correct_file.py** to fix text file (remove '\r' and add '\n') -- to use: 

```
module load python-singularity
python correct_file.py
```

2. Once you have your text file you create the sql database using *gator_add_to_database.rb*. The options for this command can be seen by issuing:

`gator_add_to_database.rb --h`

The options you want to use are *-d*(download only), *--db* database_name.sqlite (output name of sql database), *obs_list.txt* (list of observations to download). So you'll issue:

`gator_add_to_database.rb -d --db database_name.sqlite obs_list.txt`

3. Next you use:

`gator_daemon.rb --db database_name.sqlite`

This will submit the jobs to the asvo to be downloaded and then when they are finished processing they will download to *MWA_DIR/data*.

Downloading the data might take a while depending on how many other people are using the ASVO. You can check the status of your download jobs on the ASVO website under the 'My Jobs' tab.

##      Setup files to run the RTS and WSCLEAN

Once the data is downloaded it should show up in your *MWA_DIR/data* directory as a set of sub-directories (named using the observation IDs).

The following files must be edited: **correct_file.py**, **qsetup.sh**, **run_rts.sh**, **qfix_files.sh** with the location of your data and the name of the file that lists the observation IDs.

You'll also have to change the *#SBATCH --array=0-2* variable in **qsetup.sh**,   **qfix_files.sh**,  **qimage_wsclean_py3.sh**, and **run_rts.sh** to span the number of observations you want to process. I usually first test the calibration and imaging on a subset of the data before running the full set of data through. So usually I do three observation IDs to see if there are any additional flagging that needs to be done. I suggest you do this initially to make sure the scripts work and that the data is OK. So if you process three observations you would set *#SBATCH --array=0-2*.

Finally you need to change the imaging parameters for wsclean to better suite the data you are imaging (cell size, imsize, iterations, etc.); change these in **imaging_wsclean_py3.py**.

##      Running the RTS

1. Run **qsetup.sh** which is used to generate several files needed to run the RTS and format the data correctly. It does the following:
   1. Unzips the flag files for the downloaded data. 
   2. Creates the following:
      - directory within *MWA_DIR/data/OBSID/* where the RTS will be run and the calibrated data will be stored. Currently use the date as the name of the directory (you can change this in **edit_rts.py**).
      - slurm script to run the RTS within the new directory + moves it to that directory
      - sourcelist (patch and peel) for the observation
      - patch and peel RTS .in files
   3. Edits the RTS mwaf files so the RTS can read them (re-flag).

2. Once **qsetup.sh** is finished, submit **run_rts.sh** which changes directory into *MWA_DIR/data/OBSID/DATE/* and runs the RTS. 

##      Converting the RTS calibrated uvfits files to measurement-sets 
Before we can use WSCLEAN to image the calibrated visibilities we first have to convert the uvfits files to measurement sets. Additionally, two corrections are carried out: (1) the central frequency of the uvfits is corrected (RTS is wrong?); (2) the antenna table in the outputed measurement set is formatted so WSCLEAN will not complain. 

To make these corrections and do the conversion run **qfix_files.sh**. This slurm script first copies the calibrated uvfits files to a new directory in your current working directory (I run this from */astro/mwaeor/clynch/*), edits the frequency of the uvfits files, imports and converts the uvfits files using CASA, and then updates the antenna table. 

##      Imaging the calibrated visibilities

##      File summary

3C444_compact145_vis.txt > 

bashrc-pawsey > 

correct_file.py > 

correct_rtsuvfits.py > 

edit_rts.py > 

fixMS.py > 

imaging_wsclean_py3.py > 

profile-pawsey > 

qfix_files.sh > 

qimage_wsclean_py3.sh > 

qsetup.sh > 

rts_path.sh > 

rts_uv2ms.py > 

run_rts.sh > 

