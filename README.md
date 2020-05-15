# VocalTractCPP

## Vocal tract
This folder contains the original code, with the pre-inverted system.

## Vocal Tract solve
This folder contains the code to adapt. In this one, the linear sparse system
will be inverted using a LDL.T decomposition (Hermitian matrices). 


The developpement steps:
  1. Create the two matrices $A$ and $B$ (Q22 and Q12 in doc 28)
  2. Implement their update methods
  3. Solve {A x = -B y, find x}
  4. Update the `o` vector with the result of solver

### Properties of the matrix
A is a symmetric, positive definite matrix. It is tri-diagonal, therefore the
solver must use LDL.T decomposition. B is positive definite.

## Steps of project
First goal is to produce a code that yields the same results as the original
one, hence the saved copy in the folder `vocal_tract`.

Second goal is to generate, from a template file, the code to insert into the
simulation produced by `PyPHS`.

Third goal is to automatically generate the code for an arbitrary number of
tubes.


## Debug cpp
Simulation is diverging. We are trying to see if the system is correctly inverting (see folder `04_debug_cpp`). Hypothesis are:
  1. The system to invert is ill-conditionned at some point
  2. The discrete PHS is ill-condtionnned

