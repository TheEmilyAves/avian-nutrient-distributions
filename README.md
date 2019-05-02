# Avian Nutrient Distributions

This project was initially designed to make data manipulation of quail carotenoid distributions more reproducible by using Python to do the heavy-lifting for all custom data manipulation and R for stats and figures. I plan to make the code more generalizable so that it can be used by anyone who wants to analyze multi-level nutrient data in any animal.

It takes a .csv file with bird-related experiment information (e.g. sex, treatment group, etc.) and output from HPLC (high-performance liquid chromatography) as input. Then it stores the data with embedded classes (BIRD and TISSUE) so that the data can be easily manipulated for new file generation without altering the original files. The output files are designed to be R-friendly, which is the coding environment I use primarily for statistics and figure-generation.

## Getting Started

Your input file should be a .csv file containing 8+ columns of data:
Column 0 - identification codes for individuals in your dataset
Column 1 - sex of individuals in your dataset
Column 2 - group individuals belong to (e.g. treatment group)
Column 3 - type of tissue analyzed
Column 4 - mass of the sample analyzed
Column 5 - total mass of tissue, only different from Column 4 if part of the tissue was analyzed instead of the whole
Column 6 - body mass of the individual
Column 7+ - area outputs from HPLC for each peak representing a carotenoid type, number of these columns is flexible

Sample headers and data:

id    sex     treatment   tissue_type   mass_sample    mass_total   bodymass    lutein    zeaxanthin
5517  male    control     spleen        0.024          0.024        12.3        10        9
5510  female  treatment   spleen        0.052          0.052        13          45        30
6242  female  control     spleen        0.004          0.004        11.6        22        11

Run the ANDmain.py file, and it will ask you for input:
* Name of input file - make sure to include .csv at end
* Name of output file - make sure to include .csv at end
* Exceptions? - for this, say no (this code is not easily usable by others if you say yes)

It should output a .csv file with the following columns:
Column 0 - identification codes for individuals in your dataset
Column 1 - sex of individuals in your dataset
Column 2 - group individuals belong to (e.g. treatment group)
Column 3 - type of tissue analyzed
Column 4 - total mass of tissue
Column 5 - proportion of all carotenoids in a tissue out of total carotenoids in all tissues measured
Column 6 - relative proportion of caroteonids in a tissue with respect to the tissue mass / body mass ratio
Column 7 - concentration of all carotenoids in each tissue
Column 8 - total amount of carotenoids in each tissue
Column 9 - total carotenoids in all tissues in input file (same as Column 8 if only processing one tissue type)
Column 10+ - concentration of each caroteonid peak (i.e. type) in separate columns

## Prerequisites

There are currently no prerequisites to using this code. All code was written with base packages available through installing Python (3.6 for Mac OS with Spyder, installed with Anaconda 1.6.2).

## Author

Emily Webb, Biology PhD Student at Arizona State University

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgements

* Michael Rosenberg - Principles of Programming for Biologists - for teaching me how to program
* Many classmates - Advanced Topics in Programming for Biologists - for helping me brainstorm ideas for how to store my data in Python

