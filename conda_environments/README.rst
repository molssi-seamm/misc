# misc/conda_environments

The files in this directory specify conda environments for running
SEAMM. Currently there are three:

   seamm.yml

      Creates an environment named **seamm** by default, which can be used for
      running SEAMM or flowcharts. Currently this install both the core of SEAMM
      and the steps supported by the MolSSI:

         1. seamm
	 #. seamm-util
	 #. seamm-widgets
	 #. seamm-ff-util
	 #. cassandra_step
         #. custom_step
         #. forcefield_step
         #. from_smiles_step
         #. lammps_step
         #. loop_step
         #. mopac_step
         #. packmol_step
         #. table_step

   seamm-compute.yml

      Creates an environment named **seamm-compute** using conda-forge that
      contains LAMMPS, OpenMPI, OpenBabel and Packmol.

   seam-dev.yml

      Creates an environment named **seamm-dev** by default, with the tools
      needed for development, with the dependencies for SEAMM installed, but
      none of the plugin modules that make up SEAMM.

Use the conda command::

  conda env create -f <filename>

to create these environments. If you wish to give a different name to the
environment, add the -n option::

  conda env create -f <filename> -n <name>
