import MCTest
import MC_PTB

import numpy as np

#output2
def calculateMeanStdMC(matrix_Values , matrix_Distr , Data_Number , WaveLength_Number , drawNumber):
    
        """
        English:
    
        --> This function takes matrix_Values , Data_Number and WaveLength_Number as parameters.
        matrix_Values parameter is transpose of matrix of ReadFile function and given as a parameter to the this function.
        Transpose operation is required. Because the rows of our matrix should have mean and standard deviation values, and the column number should be as much as the number of wavelengths.
        For Exemple:
            matrix.Values:
                    1.column(350)       2.column(351)         3.column ...    WaveLength_Number. column
            1.row   average 1       average 1
            2.row   Standart Dev.1  Standart Dev.1
            3.row   average 2       average 2
            .
            .
            .
            Data_Number*2.row
    
        So the size of matrix_Values parameter should be ==> DataNumber*2 x WaveLength Number. It is used accordingly in our loops.
    
        --> The main purpose of this function is to prepare the output2 of the output Excel file.
        
        --> Iterations of the data are taken separately for each wavelength, and the mean and standard deviation values of the iteration matrices are calculated.
        For Example:
            
                 First Data(A1)                     Second Data(A2)   . . .DataNumber.Data(An)
                 
                 A1,350,first iteration             A2,350,first iteration
                 A1,350,second iteration            A2,350,second iteration
                 .
        350:     .
                 .
                 A1,350, drawNumber. iteration      A2,350,drawNumber. iteration
                ------------------------------      ---------------------------
                 A1,350,mean --> mean_matrix[0][0]  A2,350,mean --> mean_matrix[0][1]  
                 A1,350,std  --> std_matrix[0][0]   A2,350,std  --> std_matrix[0][1]
         
         .   
         .
         .
         
        Lastest Wave Length: . . .
    
        --> Calculated values are kept in mean_matrix and std_matrix variables.
        The dimensions of mean_matrix and std_matrix are ==> WaveLength_Number x DataNumber.
    
        -->  It is used in the drawValues and sumMC functions written by PTB in the this function.

        Changed functionality:
            For the Data A7 to A13 there is only one set of "drawNumber" results generated.
            A7 to A13 do not change over wavelength in the provided input data.
            If one measurement for each quantity A7 to A13 determines the value used for each wavelength, the expected value of the distribution is the same.
            This results in complete correlation over wavelength, meaning the generated random number has to change over each iteration, but has to stay the same for each wavelength.
            
        """
    
        result_list = [] # We use the DrawValues function to hold the returns. and we send to calculateOutputwithFormulMC function.
    
        mean_matrix     = [[0 for j in range(Data_Number)] for i in range(WaveLength_Number)]
        std_matrix      = [[0 for j in range(Data_Number)] for i in range(WaveLength_Number)]
        interval_matrix = [[[0,0] for j in range(Data_Number)] for i in range(WaveLength_Number)]
    
    
        isDefine_output = False
    
        for i in range(0,Data_Number*2,2): # matrix_Values's row number equals Data_Number*2 
        
            data_count = int(((i+1)/2)+1)
        
            check_mean , check_std = MCTest.checkIsEqual(matrix_Values[i] , matrix_Values[i+1])
            # matrix_Values[i] = average 1 , matrix_Values[i+1] = standart dev. 1.
            #is it fixed value or isn't ?
            if check_mean & check_std == False:
            
                result = MC_PTB.drawValues(matrix_Values[i] , matrix_Values[i+1] , drawNumber , DoF = 1 , Type = matrix_Distr[data_count-1])
                result_list.append(result)
                # len(result) = WaveLength_Number len(result[0]) = drawNumber
            
                for j in range(0,WaveLength_Number):
            
                
                    output = MC_PTB.sumMC(result[j] , Coverage = 0.95 , printOutput= False)
                            
                    mean_matrix[j][data_count-1] = output[0][0]
                    std_matrix[j][data_count-1] = output[0][1]
                    interval_matrix[j][data_count-1] = output[1]#output[1]=[high , low]
                
                isDefine_output = True
            
            elif check_mean & check_std == True:
           
                if isDefine_output == False:
                    output = [[matrix_Values[i,0],matrix_Values[i+1,0]],[0,0]]
           
                result = MC_PTB.drawValues(matrix_Values[i,0] , matrix_Values[i+1,0] , drawNumber, DoF = 1 , Type = matrix_Distr[data_count-1])
           
             #len(result) --> drawNumber 
            
                temp = []
            
                for k in range(WaveLength_Number):
                    temp.append(result)
                
            
                temp_np=np.array(temp)
            
                result_list.append(temp_np)
              
                # We calculated mean and standart dev. of draws(Iteration Number) for each wave length
                for j in range(0,WaveLength_Number):
            
                    mean_matrix[j][data_count-1] = np.full_like(output[0][0] , np.mean(temp_np[j]))
                    std_matrix[j][data_count-1] = np.full_like(output[0][0] , np.std(temp_np[j]))
    
        return result_list , mean_matrix , std_matrix , interval_matrix