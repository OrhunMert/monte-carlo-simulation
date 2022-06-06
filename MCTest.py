
import MCOutput1
import MCOutput2


import pandas as pd
import numpy as np
import xlsxwriter

def ReadFile(FileName,data_SheetName = "Data",distributions_SheetName = "Distributions"):
    
        """
        English:
        
        --> The ReadFile function reads the input.xlsx file which includes input variables. There are one column for average and one column for standart deviation for
        each input variable.
    
        --> For example, the format of the input.xlsx file should be as follows.
    
                1.column      2.column   3.column         4.column   5.column        . . . n.column
        1.row   Wave Lengths  Average 1  Standart Dev. 1  Average 2  Standart Dev. 2
        2.row      350          0.55      0.45*10^-5       0.7        0.1*10^-10 
          .
          .
          .
        m.row
    
   
        --> After the format is set correctly, it assigns the values of the first column of the input excel file 
        (except for the 1st row because it must be the header row) to the matrix_waveLengths variable.
        --> The size of matrix_waveLengths variable will be ==> Wave Length Number x 1. Their values will be like 350,351....
        --> The size of matrix_values variable will be ==> WaveLength Number  x DataNumber*2

        """

        # FileName can be "input_1.xlsx" or "input_2.xlsx"...
    
        # reading first column of input excel file
        df_wavelengths = pd.read_excel(FileName , sheet_name = data_SheetName , usecols = "A" , engine='openpyxl') 
 
        # From the 2nd column (except the 1st column) it reads the input excel file.
        df_values = pd.read_excel(FileName , sheet_name = data_SheetName , index_col=0 , engine='openpyxl')
    
        df_distr = pd.read_excel(FileName , sheet_name = distributions_SheetName , engine = 'openpyxl')
    
        # we need to numpy.array as type. 
        matrix_waveLengths = np.array(df_wavelengths)
        matrix_values = np.array(df_values)
        matrix_distr = np.array(df_distr)
       
   
        return matrix_waveLengths , matrix_values , matrix_distr

def getTranspose(matrix):
    
        """
         English:
        
        --> matrix must be numpy.array.
    
        --> We are getting transpose of matrix. Because we need to get the transpose of the matrix for some "for" loops.
    
        """
        return matrix.T

def findDimensions(matrix):
    
        """
        English:
    
        --> This function takes matrix as parameter. Returns the row and column numbers of the matrix.
    
        --> Returning rowNumber and colNumber, our goal is to find Wavelength number and DataNumber with this parameter. 
        
        """
    
        rowNum = len(matrix)
        colNum = len(matrix[0])
     
        return rowNum,colNum

def checkIsEqual(mean_array , std_array):
    
        checkMean = np.all(mean_array == mean_array[0])
        checkStd = np.all(std_array == std_array[0])
    
        return checkMean , checkStd

def writeExcel(output_matrix,mean_matrix,std_matrix,
                   interval_matrix,Data_Number,WaveLength_Number,
                   matrix_WaveLengths,modelFunctionName,drawNumber):

        """
    
        English:
        
        --> The function takes output_matrix , mean_matrix , std_matrix , Data_Number , WaveLength_Number and matrix_WaveLengths as parameters.
    
        output_matrix:calculateOutputwithFormulaMC corresponds to the returned matrix of the function and expects it.
    
        mean_matrix , std_matrix: corresponds to the returned mean_matrix and std_matrix matrices of the calculateMeanStdMC function and expects them.
    
        WaveLength_Number: It corresponds to 1 minus the number of lines of the Excel file. Or it is equal to the returned Column Number of the findDimensions function and is expected.
    
        matrix_WaveLengths: Corresponds to the matrix_WaveLengths returned from the ReadFile function.
    
        --> The results produced as a result of Monte Carlo are written to Excel output_drawNumber.xlsx file.
    
        """
    
        workbook = xlsxwriter.Workbook(modelFunctionName+"output_"+str(drawNumber)+".xlsx") 
        worksheet_formul_output = workbook.add_worksheet("output1")
        worksheet_mean_std_output = workbook.add_worksheet("output2")
        worksheet_interval_output = workbook.add_worksheet("intervals")
    
        worksheet_mean_std_output.write(0,0,"Wave Lengths") 
        worksheet_formul_output.write(0,0,"Iteration Number")
        worksheet_formul_output.write(0,1,""+str(drawNumber))
        worksheet_formul_output.write(1,0,"Wave Lengths")
        worksheet_formul_output.write(1,1,"Mean")
        worksheet_formul_output.write(1,2,"Standart Dev")
    
        worksheet_interval_output.write(0,0,"Wave Lengths")
    
        for i in range(1,WaveLength_Number+1):
            worksheet_mean_std_output.write(i,0,matrix_WaveLengths[i-1])
            worksheet_formul_output.write(i+1,0,matrix_WaveLengths[i-1])
            worksheet_interval_output.write(i,0,matrix_WaveLengths[i-1])
        
        for i in range(1,WaveLength_Number+1):
        
            for j in range(0,Data_Number):
            
                # we are controling;is it first row or not ? true : false
                if i - 1 == 0:
    
                    # j == 0 --> column: 1 , 2 j==1 --> column: 3 ,4  j==2 --> column: 5 , 6 
                    worksheet_mean_std_output.write(i-1,2*j+1,"mean"+str(j+1))
                    worksheet_mean_std_output.write(i-1,2*j+2,"std"+str(j+1))
                    worksheet_interval_output.write(i-1,2*j+1,"Low"+str(j+1))
                    worksheet_interval_output.write(i-1,2*j+2,"High"+str(j+1))
                
                worksheet_mean_std_output.write(i,2*j+1,mean_matrix[i-1][j])
                worksheet_mean_std_output.write(i,2*j+2,std_matrix[i-1][j])
            
                worksheet_interval_output.write(i,2*j+1,interval_matrix[i-1][j][0])
                worksheet_interval_output.write(i,2*j+2,interval_matrix[i-1][j][1])
            
            worksheet_formul_output.write(i+1 , 1 , output_matrix[i-1][0]) # row --> 0 2 4
            worksheet_formul_output.write(i+1 , 2 , output_matrix[i-1][1]) # row --> 1 3 5
    
        print("\nWriting is finished")
    
        workbook.close()

def mainMC(drawNum , FileName , modelFunctionName):
    
        """
        English:
        
        --> The function takes 2 parameters as drawNum and FileName as parameters. "DrawNum" corresponds to the number of iterations, 
        while "FileName" corresponds to the name of the "input" excel file.
        These two parameters must be defined as global variables at the top of the Python code and given as parameters when calling this function.
    
        --> "mainMC" function is the function that calls the functions that read  "input" excel file, apply the MonteCarlo method and write results to "output" Excel file.
    
        Changed functionality:
            Added "mc_matrix" to be included. 
            Added "version" to enable easy comparison between the old version of generating values and the changed version
        
        """
    
        print("\nMonte Carlo is started\n")
    
        matrix_WaveLengths , matrix_Values , matrix_Distr = ReadFile(FileName)
        matrix_Values = getTranspose(matrix_Values) # matrix_Values's size = (Data Number*2 , Wave Length Number)
        matrix_Distr  = getTranspose(matrix_Distr)

        row_Number , Column_Number = findDimensions(matrix_Values)
    
        # Normally, the WaveLength_Number variable will be equal to the Row Number. However, since we transpose it, it equals the number of columns. The reason for doing this is to use it more comfortably in our loops.
        WaveLength_Number = Column_Number
 
        # This condition is only for checking whether the format of the input excel file prepared for Monte Carlo calculation is correct.
        if row_Number % 2 == 0 :
            Data_Number = int(row_Number/2)
    
        else :
            print("row Number has to be even !!!")
    
        #output2
        result_list , mean_matrix , std_matrix , interval_matrix = MCOutput2.calculateMeanStdMC(matrix_Values , matrix_Distr 
        , Data_Number, WaveLength_Number , drawNum)
    
        #output1
        output_matrix, mc_matrix = MCOutput1.calculateOutputwithFormulaMC(result_list , Data_Number,
         WaveLength_Number , modelFunctionName , drawNum)
    
        print("\nMonte Carlo is finished\n")
    
        writeExcel(output_matrix , mean_matrix, std_matrix , 
        interval_matrix , Data_Number , WaveLength_Number, 
        matrix_WaveLengths , modelFunctionName , drawNum) 
     
        return output_matrix , mean_matrix , std_matrix, mc_matrix, matrix_WaveLengths ,   matrix_Values