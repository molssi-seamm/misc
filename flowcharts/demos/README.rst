# misc/flowcharts/demos
This directory contains sample flowcharts that demo various parts of the SEAMM
environment. Currently there are the following:

   ar_npt.flow

      This is a simple demonstration flowchart that creates a fluid box containing
      1000 atoms of Argon. This is equilibrated using a LAMMPS NVT stage and then a
      production run of NPT dynamics is used to predict the density.

      The state point is:
          T = 130 K
	  P = 100 atm
	  rho = 1.15 g/ml
   
   ethane_npt.flow

      This is a simple demonstration flowchart that creates a fluid box containing
      ethane molecules with a total of about 1000 atoms. This is equilibrated using
      a LAMMPS NVT stage and then a production run of NPT dynamics is used to
      predict the density. The temperature is defined in a custom Python stage using
      the variable 'T', which is then used in LAMMPS to define the state.

      The state point is:
          T = 120 K
	  P = 1 atm
	  rho = 0.61935 g/ml

   hc_mopac.flow

      This flowchart illustrates looping over a table and adding calculated results
      to the table. The initial table is created using a custom Python stage in
      order to make this flowchart self-contained. Normally one would input the
      table. The table has columns for the name of the molecule, its SMILES
      representation, and the experimental heat of formation from the NIST Webbook.

      The loop creates each structure from the SMILES string, then runs a MOPAC
      optimization. Various results such as the heat of formation and ionization
      potential are added to the table, and each row is printed as the iterations
      progress. Finally at the end the table is saved and printed in full.

   mopac.flow

      This is a very simple flowchart illustrating MOPAC. Benzene is created from a
      SMILES string, and then run with MOPAC. The structure is optimized and then a
      standard thermodynamics calculation is performed. Some of the calculated
      properties are placed into the table 'results', which is then printed.
