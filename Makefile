SHELL = /bin/bash
.PHONY: $(TOPTARGETS)
.PHONY: help all uninstall clean
.PHONY: clone_core clone_plugins clone_misc clone
.PHONY: seamm_env seam-dev_env seamm-compute_env dashboard_env

.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

COREDIRS := \
	molsystem \
	seamm_util \
	seamm \
	seamm_widgets \
	seamm_ff_util \
	seamm_jobserver \
	reference_handler

PLUGINDIRS := \
	control_parameters_step \
	crystal_builder_step \
	custom_step \
	dftbplus_step \
	forcefield_step \
	from_smiles_step \
	lammps_step \
	loop_step \
	mopac_step \
	packmol_step \
	psi4_step \
	read_structure_step \
	set_cell_step \
	solvate_step \
	supercell_step \
	system_step \
	table_step

DASHBOARD = seamm_dashboard

WEBSITE = molssi-seamm.github.io

SUBDIRS = $(COREDIRS) $(PLUGINDIRS) $(DASHBOARD) $(WEBSITE)


help: ## Display this help text
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

# all: environments core plugins ## Make the conda environments, and get the git repositories

install: core plugins ## Install all modules

uninstall: uninstall-core uninstall-plugins ## Remove the core and plugins repositories

core: $(COREDIRS) ## Install the core modules
	@for dir in $(COREDIRS); \
        do \
	   if [ -d $$dir ] ;\
	   then \
		$(MAKE) -C $$dir install ;\
	   fi; \
        done

plugins: $(PLUGINDIRS)  ## Install the plug-ins
	@for dir in $(PLUGINDIRS); \
        do \
	   if [ -d $$dir ] ;\
	   then \
		$(MAKE) -C $$dir install ;\
	   fi; \
        done

uninstall-core: $(COREDIRS) ## Uninstall the core parts of SEAMM from the environment
	@for dir in $(COREDIRS); \
        do \
	   if [ -d $$dir ] ;\
	   then \
		$(MAKE) -C $$dir uninstall ;\
	   fi; \
        done

uninstall-plugins: $(PLUGINDIRS) ## Uninstall the plugins from the environment
	@for dir in $(PLUGINDIRS); \
        do \
	   if [ -d $$dir ] ;\
	   then \
		$(MAKE) -C $$dir uninstall ;\
	   fi; \
        done

status: ## Get the status for the modules
	@for dir in $(SUBDIRS); \
        do \
	   if [ -d $$dir ] ;\
	   then \
		(echo '' && echo $$dir && cd $$dir && git status -s -b); \
	   fi; \
        done

pull: ## Pull (update) the local repositories
	@for dir in $(SUBDIRS); \
        do \
	   if [ -d $$dir ] ;\
	   then \
		(echo '' && echo $$dir && cd $$dir && git pull); \
	   fi; \
        done

checkout: ## Checkout the master branch of all the repositories
	@for dir in $(SUBDIRS); \
        do \
	   if [ -d $$dir ] ;\
	   then \
		(echo '' && echo $$dir && cd $$dir && git checkout master); \
	   fi; \
        done

bugfix:  ## Create a bugfix branch for all the repositories
	@for dir in $(SUBDIRS); \
        do \
	   if [ -d $$dir ] ;\
	   then \
		(echo '' && echo $$dir && cd $$dir && git checkout -B bugfix && git branch --set-upstream-to=origin/bugfix); \
	   fi; \
        done

push:  ## Push all the repositories
	@for dir in $(SUBDIRS); \
        do \
	   if [ -d $$dir ] ;\
	   then \
		(echo '' && echo $$dir && cd $$dir && git push); \
	   fi; \
        done

clone_core: $(COREDIRS)  ## Clone the core repositories

clone_plugins: $(PLUGINDIRS)  ## Clone the plugin repositories

clone_website: $(WEBSITE)  ## Clone the molssi-seamm.github.io site

$(SUBDIRS):  ## Clone any of the repositories
	@echo 'cloning '$@
	@if [ $@ = 'reference_handler' ] ;\
	then \
		git clone git@github.com:MolSSI/$@.git ;\
	else \
		git clone git@github.com:molssi-seamm/$@.git ;\
	fi

## clone: clone_core clone_plugins  ## Clone all the repositories
clone: $(SUBDIRS)  ## Clone all the repositories

# Conda environments
conda-update:  ## Update conda
	conda update -y -n base -c defaults conda

test_env: misc/  ## Create a test SEAMM Conda environment
	conda env create --force --name test --file misc/conda_environments/seamm.yml

seamm_env: misc/  ## Create the SEAMM Conda environment
	conda env create --force --file misc/conda_environments/seamm.yml

seamm-dev_env: misc/  ## Create the SEAMM development Conda environment
	conda env create --force --file misc/conda_environments/seamm-dev.yml

seamm-compute_env: misc/  ## Create the SEAMM Conda environment with the executables
	conda env create --force --file misc/conda_environments/seamm-compute.yml
	@echo ""
	@echo ""
	@echo "Please activate the seamm-compute environment"
	@echo "    conda activate seamm-compute"
	@echo "and then run the script to find the executbales:"
	@echo "    ./misc/scripts/find_executables.py"

dashboard_env: seamm_dashboard/  ## Create the environment for running the dashboard
	@$(MAKE) -C seamm_dashboard environment

finish_dashboard: seamm_dashboard/  ## Finish creating the environment for running the dashboard
	@$(MAKE) -C seamm_dashboard finish_dashboard

environments: seamm_env seamm-dev_env seamm-compute_env  dashboard_env ## Create all the Conda environments

try: ## create the environment for running the dashboard
	@echo 'Installing the Javascript, which will also take a couple minutes!'
	@echo ''
	cd seamm_dashboard/app/static ;\
	$$CONDA_PREFIX_1/envs/seamm-dashboard/bin/npm install
	@echo ''
