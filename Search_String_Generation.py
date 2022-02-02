#!/usr/bin/env python

__author__ = 'Matiss Ozols'
__date__ = '2020-11-19'
__version__ = '0.0.1'

import pandas as pd
import itertools

Parameters1 = [".*protease",
                ".*proteinase",
                ".*peptidase",
                "inhibit*"]
Parameters2 = ["human", "homo sapien*", "patient*", "subject*", "individual*", "participant*", "donor*"]
Parameters3=["skin","derm*","Epiderm*","Cutaneou*"]
Parameter4=["NOT 'Epidermal growth factor'"]

def main():
    print('ļets do some PCA')
    Dataset = pd.read_csv("Recourses/MEROPS_FINAL.csv",header=None)
    Uniprot_Dataset = pd.read_csv("Recourses/All_Uniprot_IDs.csv",header=None)
    Uniprot_Names = pd.read_csv("Recourses/Protein_Names.csv",header=None)
    print('Search Strings Generated')
    Dataset_UID=Dataset.loc[:,3]
    Search_UIDs = []
    Merops_Names = {}
    for UID in Dataset_UID:
       print(UID) 
       Merops_Entry = Dataset[Dataset.loc[:,3]==UID]
       #UID='A2MG_HUMAN'
       Locate_UAC = Uniprot_Dataset[Uniprot_Dataset.loc[:,1]==UID]
       if Locate_UAC.shape[0]==0:
        # Here it means that this is not Uniprot UAC
        
        # Check if it is in the UID collum.
        Locate_UID = Uniprot_Dataset[Uniprot_Dataset.loc[:,2]==UID]
        if Locate_UID.shape[0]==0:
            UID = Dataset[Dataset.loc[:,3]==UID].loc[:,14].reset_index(drop=True)[0]
            Locate_UID = Uniprot_Dataset[Uniprot_Dataset.loc[:,2]==UID]
        #Make sure that UID is not UAC
        if Locate_UID.shape[0]!=0:
            # If it is present then use it for search
            Search_UIDs.append(UID)
            Merops_Name = Merops_Entry[2].reset_index(drop=True)[0]
            Uniprot_Names_Protein = list(Uniprot_Names[Uniprot_Names.loc[:,2]==UID].loc[:,1])
            Uniprot_Names_Protein.append(Merops_Name)
            Unique_Uniprot_Names_Protein = list(set(Uniprot_Names_Protein))
            
            Unique_Uniprot_Names_Protein = ['"' + sub for sub in Unique_Uniprot_Names_Protein]
            Unique_Uniprot_Names_Protein = [sub + '"' for sub in Unique_Uniprot_Names_Protein]
            dataset = [ Parameters1 , Parameters2 ,Parameters3,  Unique_Uniprot_Names_Protein ]
            List = list ( itertools.product ( *dataset ) )
            Array_of_all = pd.DataFrame()
            for i2, item in enumerate(List):
                    Array_of_all = Array_of_all.append({"Search_Strings": " AND ".join(item)}, ignore_index=True)
            
            #This Search String is used in Web of Science Topic Section
            string_search = " OR ".join("(" + Array_of_all.Search_Strings.astype(str) + ")")
            f = open(f"All_Search_Strings/{UID}.txt", "w")
            f.write(string_search)
            f.close()
    
    
if __name__ == '__main__':
    main()
    
