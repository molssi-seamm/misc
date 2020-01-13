.PHONY: $(TOPTARGETS)
.PHONY: help all uninstall clean
.PHONY: clone_core clone_plugins clone_misc clone
.PHONY: seamm_env seam-dev_env seamm-compute_env

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
	seamm_util \
	seamm \
	seamm_widgets \
	seamm_ff_util \
	reference_handler \
	misc

PLUGINDIRS := \
	cassandra_step \
	custom_step \
	forcefield_step \
	from_smiles_step \
	lammps_step \
	loop_step \
	mopac_step \
	packmol_step \
	read_structure_step \
	table_step

#	print_step \

SUBDIRS = $(COREDIRS) $(PLUGINDIRS)


help: ## Diaplay this help text
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

# all: environments core plugins ## Make the conda environments, and get the git repositories

install: core plugins

uninstall: uninstall-core uninstall-plugins ## Remove the core and plugins repositories

core: $(COREDIRS) ## Fetch the core repositories from GitHub
	$(MAKE) -C seamm_util install
	$(MAKE) -C seamm install
	$(MAKE) -C seamm_widgets install
	$(MAKE) -C seamm_ff_util install
	$(MAKE) -C reference_handler install

plugins: $(PLUGINDIRS)  ## Fetch the MolSSI plugins for GitHub
	$(MAKE) -C custom_step install
	$(MAKE) -C forcefield_step install
	$(MAKE) -C from_smiles_step install
	$(MAKE) -C lammps_step install
	$(MAKE) -C loop_step install
	$(MAKE) -C mopac_step install
	$(MAKE) -C packmol_step install
	$(MAKE) -C read_structure_step install
	$(MAKE) -C table_step install

uninstall-core: $(COREDIRS) ## Uninstall the core parts of SEAMM from the environment
	$(MAKE) -C seamm_util uninstall
	$(MAKE) -C seamm uninstall
	$(MAKE) -C seamm_widgets uninstall
	$(MAKE) -C seamm_ff_util uninstall

uninstall-plugins: $(PLUGINDIRS) ## Uninstall the plugins from the environment
	$(MAKE) -C custom_step uninstall
	$(MAKE) -C forcefield_step uninstall
	$(MAKE) -C from_smiles_step uninstall
	$(MAKE) -C lammps_step uninstall
	$(MAKE) -C loop_step uninstall
	$(MAKE) -C mopac_step uninstall
	$(MAKE) -C packmol_step uninstall
	$(MAKE) -C read_structure_step uninstall
	$(MAKE) -C table_step uninstall

status:
	@for dir in $(SUBDIRS); \
        do \
		(echo '\n'$$dir && cd $$dir && git status -s -b); \
        done

pull:
	@for dir in $(SUBDIRS); \
        do \
		(echo '\n'$$dir && cd $$dir && git pull); \
        done

checkout:
	@for dir in $(SUBDIRS); \
        do \
		(echo '\n'$$dir && cd $$dir && git checkout master); \
        done

bugfix:
	@for dir in $(SUBDIRS); \
        do \
		(echo '\n'$$dir && cd $$dir && git checkout -B bugfix && git branch --set-upstream-to=origin/bugfix); \
        done

push:
	@for dir in $(SUBDIRS); \
        do \
		(echo '\n'$$dir && cd $$dir && git push); \
        done

clone_core:
	git clone git@github.com:molssi-seamm/seamm_util.git
	git clone git@github.com:molssi-seamm/seamm.git
	git clone git@github.com:molssi-seamm/seamm_widgets.git
	git clone git@github.com:molssi-seamm/seamm_ff_util.git
	git clone git@github.com:molssi/reference_handler.git
	git clone git@github.com:molssi-seamm/misc

clone_plugins:
	git clone git@github.com:molssi-seamm/cassandra_step.git
	git clone git@github.com:molssi-seamm/custom_step.git
	git clone git@github.com:molssi-seamm/forcefield_step.git
	git clone git@github.com:molssi-seamm/from_smiles_step.git
	git clone git@github.com:molssi-seamm/lammps_step.git
	git clone git@github.com:molssi-seamm/loop_step.git
	git clone git@github.com:molssi-seamm/mopac_step.git
	git clone git@github.com:molssi-seamm/packmol_step.git
	git clone git@github.com:molssi-seamm/read_structure_step.git
	git clone git@github.com:molssi-seamm/table_step.git

$(SUBDIRS):
	@echo 'cloning '$@
	git clone git@github.com:molssi-seamm/$@.git

reference_handler:
	git clone git@github.com:molssi/reference_handler.git

clone: clone_core clone_plugins

# Conda environments
conda-update:
	conda update -y -n base -c defaults conda

seamm_env: misc/conda_environments
	conda env create --force --file misc/conda_environments/seamm.yml

seamm-dev_env: misc/conda_environments
	conda env create --force --file misc/conda_environments/seamm-dev.yml

seamm-compute_env: misc/conda_environments
	conda env create --force --file misc/conda_environments/seamm-compute.yml
	conda active seamm-compute ; misc/scripts/find_executables.py

environments: seamm_env seamm-dev_env seamm-compute_env

misc/conda_environments:
	git clone git@github.com:molssi-seamm/misc
