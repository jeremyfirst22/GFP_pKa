#!/bin/bash

if [ ! -d cryst_pKas ] ; then mkdir cryst_pKas ; fi 
cd cryst_pKas

molecList="
CN145_T203C
CN145_T203D
CN145_T203F
CN145_T203H
CN145_T203N
CN145_T203S
CN145_T203W
CN145_T203Y
CN145_WT
CN165_T203C
CN165_T203D
CN165_T203F
CN165_T203H
CN165_T203N
CN165_T203S
CN165_T203W
CN165_T203Y
CN165_WT
GFP_WT_T203C
GFP_WT_T203D
GFP_WT_T203F
GFP_WT_T203H
GFP_WT_T203N
GFP_WT_T203S
GFP_WT_T203W
GFP_WT_T203Y
GFP_WT" 

check(){
    for var in $@ ; do 
        if [ ! -s $var ] ; then 
            echo "ERROR: $var does not exist!" 
            exit 
            fi 
        done 
}

logFile=Cryst.log
errFile=Cryst.err

for molec in $molecList ; do 
    printf "$molec:\t" 
    if [ ! -f ../A_State/$molec/Solvate/$molec.gro ] ; then 
        echo "Skipped!"
        continue 
        fi
    cp ../A_State/$molec/Solvate/$molec.gro  . 
    cp ../A_State/free_energy_files/AMBER* . 
    cp ../A_State/free_energy_files/20template.in . 

    printf "A State..."

    gmx editconf -f $molec.gro -o $molec.pdb >> $logFile 2>> $errFile 
    check $molec.pdb

    sed "s/CROn/CRO /" $molec.pdb > $molec+CRO.pdb 
    check $molec+CRO.pdb

    pdb2pqr --userff=AMBER.DAT --usernames=AMBER.names --assign-only $molec+CRO.pdb $molec+CRO.pqr >> $logFile 2>> $errFile 
    check $molec+CRO.pqr 

    if grep -sq WARNING $molec+CRO.pqr ; then 
        printf "\nERROR: Warning flagged in ${molec}+CRO.pqr " 
        exit 
        fi 

    grep " CRO " $molec+CRO.pqr > CRO.pqr 
    echo "TER " >> CRO.pqr
    echo "END " >> CRO.pqr

    awk '{if ($4 == "CRO") {$9 = "0.0000"} ; print }' $molec+CRO.pqr > $molec-CRO.pqr 
    check $molec+CRO.pqr CRO.pqr $molec-CRO.pqr

    sed "s/file2.pqr/$molec+CRO.pqr/" 20template.in > temp.in 
    sed "s/file.pqr/$molec+CRO.pqr/" temp.in > $molec+CRO.in 
    sed "s/file.pqr/$molec-CRO.pqr/" temp.in > $molec-CRO.in 
    sed "s/file.pqr/CRO.pqr/" temp.in > CRO.in 
    rm temp.in 

    printf "1..."
    apbs CRO.in > CRO.out 2>> $errFile
    if ! grep -q Global CRO.out ; then echo "Failed" ; exit ; fi 
    
    printf "2..."
    apbs $molec+CRO.in > $molec+CRO.out  2>> $errFile 
    if ! grep -q Global $molec+CRO.out ; then echo "Failed" ; exit ; fi 

    printf "3..."
    apbs $molec-CRO.in > $molec-CRO.out  2>> $errFile 
    if ! grep -q Global $molec-CRO.out ; then echo "Failed" ; exit ; fi 

    printf "B State..."

    ## Repeat with CRB
    sed "s/CROn/CRB /" $molec.pdb > $molec+CRB.pdb 
    check $molec+CRB.pdb 2>> $errFile 
    grep -v "HH  CRB " $molec+CRB.pdb > temp.pdb 
    mv temp.pdb $molec+CRB.pdb 

    pdb2pqr --userff=AMBER.DAT --usernames=AMBER.names --assign-only $molec+CRB.pdb $molec+CRB.pqr >> $logFile 2>> $errFile 
    check $molec+CRB.pqr 

    if grep -sq WARNING $molec+CRB.pqr ; then 
        printf "\nERROR: Warning flagged in ${molec}+CRB.pqr " 
        exit 
        fi 

    grep " CRB " $molec+CRB.pqr > CRB.pqr 
    echo "TER " >> CRB.pqr
    echo "END " >> CRB.pqr

    awk '{if ($4 == "CRB") {$9 = "0.0000"} ; print }' $molec+CRB.pqr > $molec-CRB.pqr 
    check $molec+CRB.pqr CRB.pqr $molec-CRB.pqr

    sed "s/file2.pqr/$molec+CRB.pqr/" 20template.in > temp.in 
    sed "s/file.pqr/$molec+CRB.pqr/" temp.in > $molec+CRB.in 
    sed "s/file.pqr/$molec-CRB.pqr/" temp.in > $molec-CRB.in 
    sed "s/file.pqr/CRB.pqr/" temp.in > CRB.in 
    rm temp.in 

    printf "1..."
    apbs CRB.in > CRB.out  2>> $errFile 
    if ! grep -q Global CRB.out ; then echo "Failed" ; exit ; fi 
    
    printf "2..."
    apbs $molec+CRB.in > $molec+CRB.out  2>> $errFile 
    if ! grep -q Global $molec+CRB.out ; then echo "Failed" ; exit ; fi 

    printf "3..."
    apbs $molec-CRB.in > $molec-CRB.out 2>> $errFile 
    if ! grep -q Global $molec-CRB.out ; then echo "Failed" ; exit ; fi 

    printf "Complete\n" 

    G1A=$(grep Global $molec+CRO.out | awk '{print $6}') 
    G2A=$(grep Global $molec-CRO.out | awk '{print $6}') 
    G3A=$(grep Global CRO.out | awk '{print $6}') 

    dG_xfer_CRO=$(python -c "print ($G1A - $G2A - $G3A)") 

    G1B=$(grep Global $molec+CRB.out | awk '{print $6}') 
    G2B=$(grep Global $molec-CRB.out | awk '{print $6}') 
    G3B=$(grep Global CRB.out | awk '{print $6}') 

    dG_xfer_CRB=$(python -c "print ($G1B - $G2B - $G3B)") 

    ddG=$(python -c "print ($dG_xfer_CRB - $dG_xfer_CRO)") 
    echo $ddG > $molec.ddG
    printf "\t$molec\t$ddG\n" 

done 

