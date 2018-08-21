"""
Function blocks for quail carotenoid data
"""

# import modules
import ANDfunctions_StoreData as stda
import ANDfunctions_ModifyData as moda
import ANDfunctions_GetOutput as geou


def storeData():
    infile_name, outfile_name, alt_calc, list_except = stda.getInput()
    columns, indexToName = stda.readData(infile_name)
    except_files = stda.readExceptions(list_except, alt_calc)
    nutri_list = stda.getNutrients(columns, indexToName)
    ti_list = stda.invokeTISSUE(columns, indexToName, nutri_list)
    bird = stda.invokeBIRD(columns, indexToName, ti_list)
    return bird, except_files, list_except, alt_calc, outfile_name


def modifyData(bird, except_files, list_except, alt_calc):
    moda.convertCarot(bird, alt_calc, list_except, except_files)
    moda.calcTotalCarot(bird)
    moda.calcProp(bird)
    moda.calcCarotConc(bird)
    moda.calcTissueRatio(bird)
    moda.calcRProp(bird)

def getOutput(bird, headers, outfile_name):
    col0, col1, col2, col3, col4, col5, col6, col7, col8, col9 = geou.getOutput_conc(bird)
    list_rows = geou.colToRow(col0, col1, col2, col3, col4, col5, col6, col7, col8, col9)
    geou.writeOutput(outfile_name, list_rows, headers)




