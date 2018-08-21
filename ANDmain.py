"""
Main file for quail carotenoid data
"""

# import modules
import ANDfunctions_Main as m

# main function
def main():
    headers = ""
    bird, except_files, list_except, alt_calc, outfile_name = m.storeData()
    m.modifyData(bird, except_files, list_except, alt_calc)
    m.getOutput(bird, headers, outfile_name)

if __name__ == "__main__":
    main()


