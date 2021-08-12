######      SETUP PROFILE ON PAWSEY      

First you'll have to setup your profile and bashrc files for running jobs on Garrawarla. My bashrc and profile scripts are uploaded as "bashrc-pawsey" and "profile-pawsey". The key environmental variables you need to set are the variables MWA_DIR, MWA_BEAM_FILE, and MWA_ASVO_API_KEY. The rest of them you shouldn't need to add. You should also module load/use the modules listed under Garrawarla in "profile-pawsey". 

To set the MWA_BEAM_FILE you can use the same location I use ("/pawsey/mwa/mwa_full_embedded_element_pattern.h5").

For the MWA_DIR location you need to create a directory which has a subdirectory named 'data'.  For EoR jobs I use MWA_DIR=/astro/mwaeor/MWA/ and there is a directory /astro/mwaeor/MWA/data. For transients jobs I created my own "data" directory in "/astro/mwasci/clynch/". 

The MWA_ASVO_API_KEY is assigned to you when you make an account with the MWA ASVO website (https://asvo.mwatelescope.org/), you should be able to login using your uni-credentials. 

######      DOWNLOADING DATA TO Garrawarla    

To download the data you should use the package 'gator' which is already installed on Garrawarla. More info on this package can be found here:

https://gitlab.com/chjordan/gator

I use tmux to run gator since it continually checks to see if the job is done. To use tmux you must first load the module, and then issue 'tmux' command. More info about tmux can be found here:

https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/

Then module load gator in the new tmux window.  Gator is run in two steps: (1) create a sql database (2) submit the database to download from the MWA ASVO.

To create the database you'll need a text file where each line is the observation ID you want to download. I've uploaded an example of two observations that I downloaded. For a large number of observations, you can get the observation IDs from the MWA ASVO by searching for the observations. You can export the observations by selecting them and then choosing either to export a conversion job or a download job (either works, you just need the obs IDs). Then modify the csv file to create your observation list text file.

Once you have your text file you create the sql database using the command gator_add_to_database.rb. The options for this command can be seen by issuing:

gator_add_to_database.rb --h

The options you want to use are -d (download only), --db database_name.sqlite (output name of sql database), obs_list.txt (list of observations to download). So you'll issue:

gator_add_to_database.rb -d --db database_name.sqlite obs_list.txt

Next you use:

gator_daemon.rb --db database_name.sqlite

This will submit the jobs to the asvo to be downloaded and then when they are finished processing they will download to MWA_DIR/data.

Downloading the data might take a while depending on how many other people are using the ASVO. You can check the status of your download jobs on the ASVO website under the 'My Jobs' tab.

######      SETUP FILES TO RUN THE RTS AND IMAGE DATA

Once the data is downloaded it should show up in your MWA_DIR/data directory as a set of sub-directories (named using the observation IDs).

The following files must be edited: correct_file.py, unzip_flag_files.py, qsetup_nopeel.sh, run_patch.sh, cp_uvfits.py with the location of your data and the name of the file that lists the observation IDs.

You'll also have to change the #SBATCH --array=0-2 variable in 'qsetup_nopeel.sh',   'qedit_fix.sh',  'qimage_wsclean_py3.sh',  'run_fix.sh', and 'run_patch.sh' to span the number of observations you want to process (the only '.sh' file you should not change is 'qfixMS.sh'). I usually first test the calibration and imaging on a subset of the data before running the full set of data through. So usually I do three observation IDs to see if there are any additional flagging that needs to be done. I suggest you do this initially to make sure the scripts work and that the data is OK. So if you process three observations you would set #SBATCH --array=0-2

Finally you need to change the imaging parameters for wsclean to better suite the data you are imaging (cell size, imsize, iterations, etc.). 

######      RUNNING THE RTS


