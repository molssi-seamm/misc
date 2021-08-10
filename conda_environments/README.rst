# misc/conda_environments

The files in this directory specify conda environments for developing
SEAMM.

   seam-dev.yml

      Creates an environment named **seamm-dev** by default, with the tools
      needed for development, with the dependencies for SEAMM installed, but
      none of the plugin modules that make up SEAMM.

Use the conda command::

  conda env create -f <filename>

to create these environments. If you wish to give a different name to the
environment, add the -n option::

  conda env create -f <filename> -n <name>
