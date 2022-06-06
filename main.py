import MCTest
import MCCorrelation


drawNumber = 1000 # Iteration Number

#input_FileName = "makaleDegerleri input.xlsx"
#input_FileName = "Tayfsal Responsivity input.xlsx" # It has to be excel file.
input_FileName = "flux input.xlsx"
#input_FileName = "flux2m input.xlsx"
#input_FileName = "Philip input.xlsx"
modelFunctionName = "flux"
data_SheetName = "Data"
distributions_SheetName = "Distributions"

"""
There are three options now. 
modelFunctionName = "flux" or 
modelFunctionName = "tayfsal" or 
modelFunctionName = "article" or 
modelFunctionName = "flux2m"
"""

# ------- running ------- 

#mean matrix's size = (Wave Lenghts Number , DataNumber)
output_matrix , mean_matrix , std_matrix , mc_matrix , matrix_WaveLengths , matrix_Values = MCTest.mainMC(drawNumber , 
input_FileName , modelFunctionName)
MCCorrelation.spectralcorrelation(mc_matrix)#mc_matrix's size = (drawValue , Wave Length Number)
MCCorrelation.resultplot(matrix_WaveLengths , output_matrix)

#-------------------------
