#!/usr/bin/env python

import os
import shutil

openbabel = {
    "name": "openbabel",
    
    "exes": [
        'babel',
        'obabel',
        'obchiral',
        'obconformer',
        'obdistgen',
        'obenergy',
        'obfit',
        'obgen',
        'obgrep',
        'obminimize',
        'obprobe',
        'obprop',
        'obrms',
        'obrotamer',
        'obrotate',
        'obspectrophore',
        'obsym',
        'obtautomer',
        'obthermo',
        'roundtrip',
    ],

    "ini_text" : """'''# OpenBabel executable options.
# These may be overridden by the plugin using Packmol,
# i.e. from_smiles_step.ini or by the general seamm.ini file.

openbabel-path = {}'''.format(directories[dindex])""",
}


lammps = {
    "name": "lammps",
    
    "exes" : [
        'mpiexec',
        'lmp_serial',
        'lmp_mpi'
    ],

    "ini_text": """'''# LAMMPS executable options.
# These may be overridden by the plugin using LAMMPS, ie.
# lammps_step.ini or by the general seamm.ini file.

lammps-use-mpi = True
lammps-mpi-np = default
lammps-mpi-max-np = default
lammps-mpiexec = {mpiexec}
lammps-serial = {lmp_serial}
lammps-mpi = {lmp_mpi}
lammps-atoms-per-core = 1000'''.format(**paths)""",
}

packmol = {
    "name": "packmol",
    
    "exes": [
        'packmol'
    ],

    "ini_text": """ '''# Packmol executable options.
# These may be overridden by the plugin using Packmol,
# i.e. packmol_step.ini or by the general seamm.ini file.

packmol-path = {}'''.format(directories[dindex])"""
}

mopac = {
    "name": "mopac",

    "exes": [
        'MOPAC2016'
    ],

    "ini_text" : """ '''# MOPAC executable options.
# These may be overridden by the plugin using MOPAC,
# i.e. mopac_step.ini or by the general seamm.ini file.

mopac-exe = {MOPAC2016}
mopac-num-threads = default
mopac-mkl-num-threads = default'''.format(**paths)""",
}

def add_program(program_config, prompt=True):
    """Find the path to the OpenBabel executables and set up the
    configuration file openbabel.ini in the appropriate location.
    """

    # Check if config file exists for program already
    filename = '~/.seamm/{}.ini'.format(program_config['name'])

    directory = os.path.dirname(os.path.expanduser(filename))
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    if os.path.exists(os.path.expanduser(filename)):
        answer = input(
            'The configuration file {} exists. Shall I overwrite it? [y]/n: '
            .format(filename)
        )
        if answer != '' and answer[0].lower() != 'y':
            return

    # Find the paths to the executables, noting ones that are missing
    paths = {}
    missing = []
    directories = []
    for exe in program_config['exes']:
        path = shutil.which(exe)
        if not path:
            path = shutil.which(exe + '.exe')
        if path:
            path = os.path.abspath(path)
        paths[exe] = path
        if path is None:
            missing.append(exe)
        else:
            directory = os.path.dirname(path)
            if directory not in directories:
                directories.append(directory)

    if len(missing) > 0:
        print("The following executables were not found:\n\t")
        print('\n\t'.join(missing))
        answer = input('Continue configuring {}? [y]/n: '.format(program_config["name"]))
        print()
        if answer != '' and answer[0].lower() != 'y':
            return
        else:
            for missing_executable in missing:
                while True:
                    executable_location = input('Please input a location for {} (ie, leave off the executable name). Leave blank to configure later: \t'.format(missing_executable))
                    if executable_location == '':
                        print('No executable location given for {}. Continuing...'.format(missing_executable))
                        break
                    else:
                        # Construct given path
                        exe_path = os.path.join(executable_location, missing_executable+'.exe')
                        # Check that executable exists at this location.
                        if os.path.exists(exe_path):
                            directories.append(executable_location)
                            paths[exe] = exe_path
                            break
                        else:
                            print('Executable for {} not found at {}. Please try again.'.format(missing_executable, executable_location))
    
    directories = list(set(directories))

    if len(directories) == 1:
        dindex = 0
    elif len(directories) > 1:
        print("More than one path was found:")
        i = 0
        for directory in directories:
            i += 1
            print('\t{}: {}'.format(i, directory))
        answer = input(
            'Which do you want to use? 1-{}, return to exit:'.format(i)
        )
        if answer == '':
            return
        try:
            answer = int(answer)
        except:
            return
        if answer < 1 or answer > i:
            print('You must enter a number between 1 and {}'.format(i))
            return
        dindex = answer - 1
    else:
        print('There were no directories in the paths!')
        return

    with open(os.path.expanduser(filename), 'w') as fd:
        write_string = eval(program_config["ini_text"])
        fd.write(write_string)

    print('Wrote {}\n'.format(filename))

print(__name__)
if __name__ == "__main__":
    print('calling packmol')
    add_program(packmol)
    add_program(openbabel)
    add_program(lammps)
    add_program(mopac)
