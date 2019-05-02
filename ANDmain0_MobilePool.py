"""
Main file for quail carotenoid data
"""

# import modules
import ANDfunctions_StoreData as stda
import ANDfunctions_ModifyData as moda
import ANDfunctions_GetOutput as geou


# main function
def main():
    headers = "bird.id","sex","treatment","tissue.type","total.carot","total.tissue.mass"
    # get input from user
    infile_name, outfile_name, alt_calc, list_except = stda.getInput()
    print("successfully got input")
    # read data files
    columns, indexToName = stda.readData(infile_name)
    except_files = stda.readExceptions(list_except, alt_calc)
    print("successfully read data")
    # make bird objects
    nutri_list = stda.getNutrients(columns, indexToName)
    ti_list = stda.invokeTISSUE(columns, indexToName, nutri_list)
    bird = stda.invokeBIRD(columns, indexToName, ti_list)
    print("successfully made bird objects")
    # make carotenoid calculations and add to bird objects
    moda.convertCarot(bird, alt_calc, list_except, except_files)
    print("successfully converted carotenoids and added to existing objects")
    moda.calcTotalCarot(bird)
    moda.calcProp(bird)
    print("finished calculations")
    # get output data and write output file
    col0, col1, col2, col3, col4, col5 = geou.getOutput_tc(bird)
    list_rows = geou.colToRow(col0, col1, col2, col3, col4, col5)
    geou.writeOutput(outfile_name, list_rows, headers)
    print("done")


if __name__ == "__main__":
    main()

