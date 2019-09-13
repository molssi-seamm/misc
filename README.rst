# misc
Miscellaneous files and helpers for installing and running
SEAMM. There are currently three subdirectories:

   conda_environments

      Contains YAML definition files of useful cond environments.

   flowcharts

      Contains sample flowcharts for running SEAMM.

   scripts

      Contains scripts for setting up configuration files and doing
      other useful things for SEAMM.

Installing SEAMM
----------------
The graphical part of SEAMM is installed in the **seamm** conda
environment. If you do not have conda (or anaconda) installed, head
over to Miniconda_ or Anaconda_ and grab the installer, following
their directions. Miniconda_ is a small, stripped down version, which
is perfectly fine for our use. Anaconda_ comes with many packages
preinstalled and also a graphical interface, so if you plan to use it
for your own work it might be more useful. But Anaconda_ is more than
is needed for SEAMM.

Once you have conda installed, get the *seamm.yml* file from the
*conda_environments/* subfolder. You can download it from GitHub or just
clone this entire repository. Either way, once you have it run the
conda command to create the environment::
  conda env create -f seamm.yml

If you prefer a name other than the default of **seamm** for the
environment, add that name like this::
  conda env create -f seamm.yml -n <name>

Once the enironment is installed, activate it with::
  conda activate seamm

If you chose a different name, use that instead of **seamm**.

You can start the flowchart editor by typing::
  seamm

There are some sample flowcharts in *misc/flowcharts* to help you get
started.

Installing the Compute Engines
------------------------------
**N.B. Currently only Linux and MacOS versions of Packmol and LAMMPS
are supported by conda-forge. So, at the moment, these instructions
will not work under Windows.**

The plugins in SEAMM use a number of external executables to accomplish
their tasks.
   - **seamm_util** and **from_smiles_step** use parts of OpenBabel
   - **packmol_step** uses Packmol to build fluid systems
   - **lammps_step** uses LAMMPS and OpenMPI
   - **mopac_step** uses MOPAC

Installing LAMMPS, OpenBabel and Packmol
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want to run flowcharts using these plugins, you will need to
install the correct executables. All of these except MOPAC can be
installed using the conda environment specified in *seamm-compute.yml*::
  conda env create -f seamm-compute.yml
  
Of course, if you want a name other than the default **seamm-compute**
you can override the default with the -n option.

Installing MOPAC
~~~~~~~~~~~~~~~~
Head to the MOPAC_ homepage and click on one of the download links in
the section on MOPAC2016. MOPAC is free for academics, so if you are
at a university or school you can request a copy and license. Follow
the instructions included with the download for installing MOPAC and
activating MOPAC.

The path to the MOPAC executable is stored in the next step in the
file ~/.seamm/mopac.ini. If MOPAC is not in your path you can have the
script create the file, then edit ~/.seamm/mopac.ini to put in the
correct path -- usually /opt/mopac/MOPAC2016.exe on Linux or Windows.

Finishing Up
~~~~~~~~~~~~
After the installation completes, activate the environment::
  conda activate seamm-compute

There is one more step needed to let SEAMM know the location of the
executables. Execute the script *find_executables.py* in the
**seamm-compute** environment::
  ./find_executables.py

The script may ask you some questions, but normally it will just run
to completion, telling you that it created *~/.seamm/packmol.ini*,
*~/.seamm/openbabel.ini* and *~/.seamm/lammps.ini*. The hidden
directory *~/.seamm* is where SEAMM expects to find configuration
files.

Running Flowcharts
------------------
Once you have installed both the **seamm** and **seamm-compute**
environments, and run the *find_executables.py* script, you can run
flowcharts. You need to be running in the **seamm** environment and
can either run the directly from within the SEAMM flowchart editor,
using the **File/Run** command, or you can simply execute the
flowchart. For example::
  flowcharts/demos/ar_npt.flow

will run a simple example of using molecular dynamics with an NPT
ensemble to predict the density of liquid argon at 130 K and 100
atm. It will take a couple minutes to run, with output appearing in
the shell window, and also in a directory it will create with a name
like *2019-09-11_11:40:28/*. This is a timestamp that keeps different
runs in different directories. There are some options to control where
the output goes, etc.::
  flowcharts/demos/ar_npt.flow --help

  usage: run_flowchart [-h] [--seamm-configfile SEAMM_CONFIGFILE] [-v]
                     [--directory DIRECTORY] [--force] [--output {files,stdout,both}]
                     filename

   Execute a SEAMM flowchart Args that start with '--' (eg. -v) can also be set in a
   config file (/etc/seamm/seamm.ini or ~/.seamm/seamm.ini or specified via --seamm-
   configfile). Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for
   details, see syntax at https://goo.gl/R74nmi). If an arg is specified in more than one
   place, then commandline values override environment variables which override config
   file values which override defaults.

   positional arguments:
     filename              the filename of the flowchart

   optional arguments:
     -h, --help            show this help message and exit
     --seamm-configfile SEAMM_CONFIGFILE
			   a configuration file to override others
     -v, --verbose         increases log verbosity for each occurence. [env var: VERBOSE]
     --directory DIRECTORY
			   Directory to write output and other files. [env var: DIRECTORY]
     --force               [env var: FORCE]
     --output {files,stdout,both}
			   whether to put the output in files, direct to stdout, or both
			   [env var: OUTPUT]

  
.. _Miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _Anaconda: https://docs.anaconda.com/anaconda/
.. _MOPAC: http://openmopac.net/index.html
