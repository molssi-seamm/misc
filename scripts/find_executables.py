#!/usr/bin/env python

import os
import os.path
import shutil


def OpenBabel(prompt=True):
    """Find the path to the OpenBabel executables and set up the
    configuration file openbabel.ini in the appropriate location.
    """

    exes = [
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
    ]

    # Find the paths to the executables, noting ones that are missing
    paths = {}
    missing = []
    directories = []
    for exe in exes:
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
        answer = input('Do you want to continue? [y]/n: ')
        print()
        if answer != '' and answer[0].lower() != 'y':
            return

    if len(directories) == 1:
        dindex = 0
    elif len(directories) > 1:
        print("More than one path was found:")
        i = 0
        for directory in directories:
            i += 1
            print('\t{}: {}'.format(i, directory))
        answer = input(
            'Which do you want to use? 1-{}, return to exit: '.format(i)
        )
        if answer == '':
            return
        try:
            answer = int(answer)
        except:
            return
        if answer < 1 or answer > i:
            print('You must enter an number between 1 and {}'.format(i))
            return
        dindex = answer - 1
    else:
        print('There were no directories in the paths!')
        return

    filename = '~/.seamm/openbabel.ini'

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

    with open(os.path.expanduser(filename), 'w') as fd:
        fd.write(
            (
                '# OpenBabel executable options.\n'
                '# These may be overridden by the plugin using Packmol, i.e.\n'
                '# from_smiles_step.ini or by the general seamm.ini file.\n'
                '\n'
                'openbabel-path = {}'
            ).format(directories[dindex])
        )
    print('Wrote {}\n'.format(filename))


def LAMMPS(prompt=True):
    """Find the path to the LAMMPS executables and set up the
    configuration file lammps.ini in the appropriate location.
    """

    exes = [
        'mpiexec',
        'lmp_serial',
        'lmp_mpi'
    ]

    # Find the paths to the executables, noting ones that are missing
    paths = {}
    missing = []
    for exe in exes:
        path = shutil.which(exe)
        if not path:
            path = shutil.which(exe + '.exe')
        if path:
            path = os.path.abspath(path)
        paths[exe] = path
        if path is None:
            missing.append(exe)

    if len(missing) > 0:
        print("The following executables were not found:\n\t")
        print('\n\t'.join(missing))
        answer = input('Do you want to continue? [y]/n: ')
        print()
        if answer != '' and answer[0].lower() != 'y':
            return

    filename = '~/.seamm/lammps.ini'

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

    with open(os.path.expanduser(filename), 'w') as fd:
        fd.write(
            (
                '# LAMMPS executable options.\n'
                '# These may be overridden by the plugin using LAMMPS, ie.\n'
                '# lammps_step.ini or by the general seamm.ini file.\n'
                '\n'
                'lammps-use-mpi = True\n'
                'lammps-mpi-np = default\n'
                'lammps-mpi-max-np = default\n'
                'lammps-mpiexec = {mpiexec}\n'
                'lammps-serial = {lmp_serial}\n'
                'lammps-mpi = {lmp_mpi}\n'
                'lammps-atoms-per-core = 1000\n'
            ).format(**paths)
        )
    print('Wrote {}\n'.format(filename))


def Packmol(prompt=True):
    """Find the path to the Packmol executable and set up the
    configuration file packmol.ini in the appropriate location.
    """

    exes = [
        'packmol'
    ]

    # Find the paths to the executables, noting ones that are missing
    paths = {}
    missing = []
    directories = []
    for exe in exes:
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
        answer = input('Do you want to continue? [y]/n: ')
        print()
        if answer != '' and answer[0].lower() != 'y':
            return

    if len(directories) == 1:
        dindex = 0
    elif len(directories) > 1:
        print("More than one path was found:")
        i = 0
        for directory in directories:
            i += 1
            print('\t{}: {}'.format(i, directory))
        answer = input(
            'Which do you want to use? 1-{}, return to exit: '.format(i)
        )
        if answer == '':
            return
        try:
            answer = int(answer)
        except:
            return
        if answer < 1 or answer > i:
            print('You must enter an number between 1 and {}'.format(i))
            return
        dindex = answer - 1
    else:
        print('There were no directories in the paths!')
        return

    filename = '~/.seamm/packmol.ini'

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

    with open(os.path.expanduser(filename), 'w') as fd:
        fd.write(
            (
                '# Packmol executable options.\n'
                '# These may be overridden by the plugin using Packmol,\n'
                '# i.e. packmol_step.ini or by the general seamm.ini file.\n'
                '\n'
                'packmol-path = {}'
            ).format(directories[dindex])
        )
    print('Wrote {}\n'.format(filename))


def MOPAC(prompt=True):
    """Find the path to the MOPAC executables and set up the
    configuration file mopac.ini in the appropriate location.
    """

    exes = [
        'MOPAC2016'
    ]

    # Find the paths to the executables, noting ones that are missing
    paths = {}
    missing = []
    for exe in exes:
        path = shutil.which(exe)
        if not path:
            path = shutil.which(exe + '.exe')
        if path:
            path = os.path.abspath(path)
        paths[exe] = path
        if path is None:
            missing.append(exe)

    if len(missing) > 0:
        print("The following executables were not found:\n\t")
        print('\n\t'.join(missing))
        answer = input('Do you want to continue? [y]/n: ')
        print()
        if answer != '' and answer[0].lower() != 'y':
            return

    paths['MOPAC2016'] = 'MOPAC2016.exe'

    filename = '~/.seamm/mopac.ini'

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

    with open(os.path.expanduser(filename), 'w') as fd:
        fd.write(
            (
                '# MOPAC executable options.\n'
                '# These may be overridden by the plugin using MOPAC,\n'
                '# i.e. mopac_step.ini or by the general seamm.ini file.\n'
                '\n'
                'mopac-exe = {MOPAC2016}\n'
                'mopac-num-threads = default\n'
                'mopac-mkl-num-threads = default\n'
            ).format(**paths)
        )
    print('Wrote {}\n'.format(filename))


def SEAMM(prompt=True):
    """Set up the configuration file for SEAMM -- it is all commented
    but that gives the user a template.
    """

    filename = '~/.seamm/seamm.ini'

    directory = os.path.dirname(os.path.expanduser(filename))
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    if os.path.exists(os.path.expanduser(filename)):
        answer = input(
            'The configuration file {} exists. Shall I overwrite it? y/[n]: '
            .format(filename)
        )
        if answer == '' or answer[0].lower() != 'y':
            return

    with open(os.path.expanduser(filename), 'w') as fd:
        fd.write(
            (
                '# Configuration options for SEAMM.\n'
                '#\n'
                '# Options in this file override those in all other\n'
                '# configuration files, but may in turn be overridden\n'
                '# by environment variables or commandline options.\n'
                '\n'
                '# datastore = ~/SEAMM\n'
                '# project = MyProject\n'
            )
        )
    print('Wrote {}\n'.format(filename))
    print(
        '  You should look at it and uncomment and\n'
        '  set it up to meet your needs.'
    )


if __name__ == "__main__":
    Packmol()
    OpenBabel()
    LAMMPS()
    MOPAC()
    SEAMM()
