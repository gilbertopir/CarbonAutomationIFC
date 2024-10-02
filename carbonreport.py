import pandas as pd
import os

def factorstemplate(mat):
    factors=open("/mount/src/carbonautomation/Streamlit_Automation_Rev01/Templates/Factors.csv", "r")
    factors=factors.read().split('\n')
    factors.pop(0)
    #templevel=[]
    #mat=[]
    for data in factors:
        data=data.replace(" ", "")
        data=data.split(',')
        tempmat=data[0]
        factor=data[2]
        density=data[5]
        #mat=data[1]
        if str(tempmat) == str(mat):
            #print ('--------> found factor')
            return factor,density
            #print(mat,tempmat)
            #input()
    
    print ('!!! Material not on Factors.csv list !!!',mat)
    input()
    
def mattemplate(level):
    materials=open("/mount/src/carbonautomation/Streamlit_Automation_Rev01/Templates/MaterialsBYLevels.csv", "r")
    materials=materials.read().split('\n')
    materials.pop(0)
    #templevel=[]
    #mat=[]
    #print('>>>Addiing Materials to Levels<<<')
    for data in materials:
        data=data.replace(" ", "")
        data=data.split(',')
        #print(data)
        templevel=data[0]
        mat=data[1]
        if str(templevel) == str(level):
            #print ('level found', mat)
            return mat
        
    print ('!!! Level not on MaterialsBYLevels.csv list !!!')
    print('Level name: ', level)

def filenames():
    folder_path = "DWG_Reports"
    filenames = []
    # Loop through the files in the folder and append file names to the list
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            filenames.append(filename)
    # Print the result
    sortedlist=sorted(filenames)
    return sortedlist
    
######################
#### main routine ####
######################
def main(fileRead):
    #fileRead="DWG_Reports/"+str(fileList[0])
    print("DWG_Reports/"+fileRead)
    #input()
    f = open("DWG_Reports/"+fileRead, "r")
    file=(f.read()).split('\n')
    file.pop(0)
    
    fileWrite="Output_Reports/"+fileRead
    fileout=open(fileWrite, "w")
    fileout.write('Element,Material,Quantity,Carbon Factor (kgCO2e/kg),Carbon (kgCO2e),Density (kg/m3)\n')
    
    dataframe=[]
    for line in file:
        if line:
            line.replace(" ", "")
            line=line.split(',')
            level=line[1]
            level=level.replace(" ", "")
            volume=line[2]
            ## match level in template file ##
            mat=mattemplate(level)
            ## match material in template file ##
            factor,density=factorstemplate(mat)
            ## return ##
            ## calculate carbon ##
            try:
                mass=float(volume)*float(density)
                carbon=round(mass*float(factor),4)
                data= (level,mat,float(volume),float(factor),float(carbon),float(density))
                #print(data)
                dataframe.append(data)
            except:
                print ('!!! Error in carbon calculation !!!')
                print ('Error data:',mat,volume,density,factor)
                
            ## write to file ##
        fileout.write(str(level)+','+str(mat)+','+str(volume)+','+str(factor)+','+str(carbon)+','+str(density))
        fileout.write('\n')
    
    fileout.close()
    
    ## pandas ##
    df = pd.DataFrame(dataframe, columns=["Element", "Material", "Quantity", "Carbon Factor", "Carbon", "Density"])
    grouped_df = df.groupby("Element").agg({
        "Element": "first",
        "Material": "first",
        "Quantity": "sum",
        "Carbon Factor": "first",
        "Carbon": "sum",
        "Density": "first"
    })
    
    #print(grouped_df)
    groupedFileName="Output_Reports/"+fileRead.replace(".csv", ".xlsx")
    print (groupedFileName)
    grouped_df.to_excel(groupedFileName, index=False, columns=["Element", "Material", "Quantity", "Carbon Factor", "Carbon", "Density"])
    
    
    print('\n############################',"End file process!","############################\n")
    

####################
### Start Script ###
####################
#filenames()
#fileList=filenames()
#for fileRead in fileList:
#    fileRead=str(fileRead)
#    main(fileRead)

#print('All done!!!')
