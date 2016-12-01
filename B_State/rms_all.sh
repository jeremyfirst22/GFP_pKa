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

if [ ! -d rms_values ] ; then mkdir rms_values ; fi 

for molec in $molecList ; do 
        printf "\n\t$molec\n" 
        if [ -f rms_values/${molec}_rms.xvg ] ; then printf "\nSkipped\n" ; continue ; fi 

        cd $molec/Production

       #if [ ! -f fixed.xtc ] ; then 
       #    echo '1 0' | gmx trjconv -s $molec.production.tpr -center -ur compact -pbc mol -f $molec.production.xtc -o fixed.xtc 
       #    fi 
       #check fixed.xtc 

       #if [ ! -f fixed.gro ] ; then 
       #    echo '1 0' | gmx trjconv -s $molec.production.tpr -center -ur compact -pbc mol -f $molec.npt_relax.gro -o fixed.gro 
       #    fi
       #check fixed.gro

        if [ ! -f crystal.ndx ] ; then 
            echo '4 && ri 3-230' > selection.dat 
            echo 'q ' >> selection.dat 

            cat selection.dat | gmx make_ndx -f $molec.production.tpr -o crystal.ndx 
            check crystal.ndx 
        fi 

        if [ ! -f ../../rms_values/${molec}_rms.xvg ] ; then 
            echo '22 22' | gmx rms -s $molec.production.tpr -f $molec.production.nopbc.xtc -o ../../rms_values/${molec}_rms.xvg -n crystal.ndx 
            fi 
        check ../../rms_values/${molec}_rms.xvg 
        cd ../../

    done 

for molec in $molecList ; do 
    printf "\n\t$molec\n" 
    if [ ! -f /Volumes/My\ Book\ Thunderbolt\ Duo/GFP_BAD_PARAMETERS/A_State/$molec/Production/$molec.production.xtc ] ; then printf "\nSkipped\n" ; continue ; fi 
    if [ -f rms_values/old_${molec}_rms.xvg ] ; then printf "\nSkipped\n" ; continue ; fi 
        
    cd rms_values 
    if [ ! -f cyrstal.ndx ] ; then 
        echo '4 && ri 3-230' > selection.dat 
        echo 'q ' >> selection.dat 

        cat selection.dat | gmx make_ndx -f /Volumes/My\ Book\ Thunderbolt\ Duo/GFP_BAD_PARAMETERS/A_State/$molec/Production/$molec.production.tpr -o crystal.ndx 
        fi 
    check crystal.ndx 

    if [ ! -f old_${molec}_rms.xvg ] ; then 
        echo '22 22' | gmx rms -s /Volumes/My\ Book\ Thunderbolt\ Duo/GFP_BAD_PARAMETERS/A_State/$molec/Production/$molec.production.tpr -f /Volumes/My\ Book\ Thunderbolt\ Duo/GFP_BAD_PARAMETERS/A_State/$molec/Production/$molec.production.nopbc.xtc -o old_${molec}_rms.xvg -n crystal.ndx 
        fi 
    check old_${molec}_rms.xvg

    rm crystal.ndx 
    rm selection.dat 

    cd ../
    done 




