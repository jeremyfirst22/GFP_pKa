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

if [ ! -d rms_203_values ] ; then mkdir rms_203_values ; fi 

for molec in $molecList ; do 
        printf "\n\t$molec\n" 
        if [ -f rms_203_values/${molec}_rms_203.xvg ] ; then printf "\nSkipped\n" ; continue ; fi 
        if [ ! -f ${molec}/Production/${molec}.production.nopbc.xtc ] ; then printf "\nTrajectory not found\n" ; continue ; fi 

        cd $molec/Production

        if [ ! -f ri203.ndx ] ; then 
            echo 'ri 202' > selection.dat 
            echo 'q ' >> selection.dat 

            cat selection.dat | gmx make_ndx -f $molec.production.tpr -o ri203.ndx 
            check ri203.ndx 
        fi 

        if [ ! -f ../../rms_203_values/${molec}_rms_203.xvg ] ; then 
            echo '4 22' | gmx rms -s $molec.production.tpr -f $molec.production.nopbc.xtc -o ../../rms_203_values/${molec}_rms_203.xvg -n ri203.ndx 
            fi 
        check ../../rms_203_values/${molec}_rms_203.xvg 
        cd ../../

    done 



