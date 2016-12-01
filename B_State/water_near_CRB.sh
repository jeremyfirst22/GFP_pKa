#!/bin/bash

##T203R mutants removed since R doesn't form the chromophore.
molecList="
CN145_T203C     CN145_T203Y     CN165_T203S     GFP_WT_T203H
CN145_T203D     CN145_WT        CN165_T203W     GFP_WT_T203N
CN145_T203F     CN165_T203C     CN165_T203Y     
CN145_T203H     CN165_T203D     CN165_WT        GFP_WT_T203S
CN145_T203N     CN165_T203F     GFP_WT          GFP_WT_T203W
CN165_T203H     GFP_WT_T203C    GFP_WT_T203Y
CN145_T203S     CN165_T203N     GFP_WT_T203D    
CN145_T203W     GFP_WT_T203F
"

check(){
    for arg in $@ ; do 
        if [ ! -s $arg ] ; then 
            echo "ERROR: $arg not found " 
            exit 
            fi 
        done 
}

if [ ! -d wat_near_CRB ] ; then mkdir wat_near_CRB ; fi 

for molec in $molecList ; do 
        printf "\n\t$molec\n" 
        if [ -f wat_near_CRB/${molec}.wat_near_CRB.xvg ] ; then printf "\nSkipped\n" ; continue ; fi 
        if [ ! -f ${molec}/Production/${molec}.production.nopbc.xtc ] ; then printf "\nTrajectory not found\n" ; continue ; fi 

        cd $molec/Production
        
        gmx select -f $molec.production.nopbc.xtc -s $molec.production.tpr -os ../../wat_near_CRB/${molec}.wat_near_CRB.xvg -olt ../../wat_near_CRB/${molec}.lifetime.xvg -select 'group Water and same residue as within 0.5 of resname CROa'


        check ../../wat_near_CRB/${molec}.wat_near_CRB.xvg 
        cd ../../

    done 



