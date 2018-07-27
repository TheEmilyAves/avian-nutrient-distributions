# Avian Nutrient Distributions

This project was initially designed to make data manipulation of quail carotenoid distributions more reproducible by using Python to do the heavy-lifting for all custom data manipulation and R for stats and figures. I plan to make the code more generalizable so that it can be used by anyone who wants to analyze multi-level nutrient data in any animal.

It takes a .csv file with bird-related experiment information (e.g. sex, treatment group, etc.) and output from HPLC (high-performance liquid chromatography) as input. Then it stores the data with embedded classes (BIRD and TISSUE) so that the data can be easily manipulated for new file generation without altering the original files. The output files are designed to be R-friendly, which is the coding environment I use primarily for statistics and figure-generation.

## Getting Started

The first draft of this project is currently under construction, and is unusable at this point. Though anyone could take working parts of the code that I've already written and adapt it for their own use as long as license guidelines are followed. I will fill out this section more when I've completed a working draft of the project.

## Prerequisites

There are currently no prerequisites to using this code. All code was written with base packages available through installing R (3.3.2 for Mac OS) and Python (3.6 for Mac OS with Spyder, installed with Anaconda 1.6.2).

## Author

Emily Webb, Biology PhD Student at Arizona State University

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgements

* Michael Rosenberg - Principles of Programming for Biologists - for teaching me how to program
* Many classmates - Advanced Topics in Programming for Biologists - for helping me brainstorm ideas for how to store my data in Python

