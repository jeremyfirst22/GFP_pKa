#!/bin/bash
if [ -z $1 ] ; then 
    echo "Usage: $0 <Calculation directory to analyze> " 
    exit 
    fi 

if [ ! -d $1 ] ; then 
    echo "ERROR: $1 directory does not exist. Have you run this MD yet?" 
    exit 
    fi 

printf "\n\t*** Program Beginning ***\n\n" 

MOLEC=$1
TOP=$(PWD)
XTC=$TOP/$MOLEC/Production/$MOLEC.production.nopbc.xtc 
TPR=$TOP/$MOLEC/Production/$MOLEC.production.tpr
tot=50000 #ps
numFrames=100
if (( $tot % 4 )) ; then 
    echo "WARNING: $tot % 4 != 0. There may not be frames for requested time steps" 
    fi 
timeStep=$(echo "$tot / $numFrames" | bc) #ps 
if [[ $timeStep -lt 20 ]] ; then 
    echo "ERROR: Requested time step is $timeStep. Frames only printed every 20 ps." 
    exit ; fi 
logFile=$TOP/energies.log
errFile=$TOP/energies.err

if [ ! -f $XTC ] ; then 
    echo "ERROR: $XTC not found. Did the calculation finish?" 
    exit 
    fi 

if [ ! -f $TPR ] ; then 
    echo "ERROR: $TPR not found " 
    exit 
    fi 

cd $MOLEC

check(){
    for arg in $@ ; do 
        if [ ! -s $arg ] ; then 
            echo ; echo "ERROR: $arg does not exist" 
            exit 
            fi 
        done 
}

if [ ! -d FREE_ENERGIES ] ; then mkdir FREE_ENERGIES ; fi 
cd FREE_ENERGIES
cp ../../free_energy_files/AMBER.DAT . 
cp ../../free_energy_files/AMBER.names . 
cp ../../GMXFF/*.dat . 
cp -r ../../GMXFF/amber03.ff . 

check AMBER.DAT AMBER.names

printf "\n\t*** Pre-Compress      ***\n\n" 
printf "\tExtracting relevant frames.............." 
if [ ! -f compress.xtc ] ; then 
    echo '0' | gmx trjconv -f $XTC -s $TPR -o compress.xtc -b 0 -e $tot -dt $timeStep -tu ps >> $logFile 2>> $errFile 
    check compress.xtc
else 
    printf "Skipped\n" 
    fi 
printf "Complete\n" 

XTC=compress.xtc

printf "\n\t*** pdb2pqr and APBS    ***\n\n" 
for frame in $(seq 0 $timeStep $tot) ; do 
    printf "\tReading %5i of %5i..." $frame $tot
    
    if ! grep -sq Global time_${frame}_Protein-CRB.out ; then     

        echo '1' | gmx trjconv -f $XTC -s $TPR -o time_${frame}.pdb -dump $frame -tu ps >> $logFile 2>> $errFile 
        check time_${frame}.pdb 


        ####For whatever reason, APBS only support 3-character names for residues 
        sed "s/CROa/CRB /" time_${frame}.pdb > temp.pdb 
        mv temp.pdb time_${frame}.pdb 



        if ! grep -sq CRB time_${frame}.pdb ; then 
            printf "ERROR: We left CRB behind! \n"
            exit 
            fi 

        pdb2pqr time_${frame}.pdb time_${frame}_Protein+CRB.pqr --userff AMBER.DAT --usernames AMBER.names --assign-only >> $logFile 2>> $errFile
        check time_${frame}_Protein+CRB.pqr 
             
        if grep -sq WARNING time_${frame}_Protein+CRB.pqr ; then 
            printf "\nERROR: Warning flagged in time_${time}_Protein+CRB.pqr file\n"
            exit 
            fi 

        #printf "\n\nDude this isn't going to work yet. Fix it\n\n"
        #exit     

        grep " CRB " time_${frame}_Protein+CRB.pqr > time_${frame}_crb.pqr 
        echo "TER " >> time_${frame}_crb.pqr 
        echo "END " >> time_${frame}_crb.pqr 
            
        awk '{if ($4 == "CRB") {$9 = "0.0000"} ; print }' time_${frame}_Protein+CRB.pqr > time_${frame}_Protein-CRB.pqr 
        check time_${frame}_Protein+CRB.pqr time_${frame}_Protein-CRB.pqr time_${frame}_crb.pqr

        sed "s/file2.pqr/time_${frame}_Protein+CRB.pqr/" ../../free_energy_files/template.in > temp.in
        sed "s/file.pqr/time_${frame}_Protein+CRB.pqr/" temp.in > time_${frame}_Protein+CRB.in 
        sed "s/file.pqr/time_${frame}_Protein-CRB.pqr/" temp.in > time_${frame}_Protein-CRB.in 
        sed "s/file.pqr/time_${frame}_CRB.pqr/" temp.in > time_${frame}_CRB.in 
        rm temp.in

#APBS is called three times for each frame. The first call takes ~5 sec (smaller system), the second two take 10-15 each. 
        printf "1..." 
        apbs time_${frame}_crb.in > time_${frame}_crb.out 2>> time_${frame}.err 
        if ! grep -q Global time_${frame}_crb.out ; then echo "Failed" ; exit ; fi 

        printf "2..." 
        apbs time_${frame}_Protein+CRB.in > time_${frame}_Protein+CRB.out 2>> time_${frame}.err
        if ! grep -q Global time_${frame}_Protein+CRB.out ; then echo "Failed" ; exit ; fi 
   
        printf "3..." 
        apbs time_${frame}_Protein-CRB.in > time_${frame}_Protein-CRB.out 2>> time_${frame}.err 
        if ! grep -q Global time_${frame}_Protein-CRB.out ; then echo "Failed" ; exit ; fi 

        printf "Complete\n" 
    else  
        printf "............Skipped\n" 
        fi 
    
    done 

printf "\n\t *** Compiling Results *** \n\n" 
if [ -f dG_xter_CRB.dat ] ; then rm dG_xter_CRB.dat ; fi 
for frame in $(seq 0 $timeStep $tot) ; do 
    printf "\tFrame   %5i of %5i....." $frame $tot
    if ! grep -sq Global time_${frame}_Protein+CRB.out ; then 
        printf "\nERROR: Delete time_${frame}_Protein-CRB.out and repeat\n" 
        fi 
    if ! grep -sq Global time_${frame}_crb.out ; then 
        printf "\nERROR: Delete time_${frame}_Protein-CRB.out and repeat\n" 
        fi 
    if ! grep -sq Global time_${frame}_Protein-CRB.out ; then 
        printf "\nERROR: How did you get here? I have a logical fallacy\n" 
        fi 

    G1=$(grep Global time_${frame}_Protein+CRB.out | awk '{print $6}') 
    G2=$(grep Global time_${frame}_Protein-CRB.out | awk '{print $6}') 
    G3=$(grep Global time_${frame}_crb.out | awk '{print $6}') 

    dG_xfer_CRB=$(python -c "print ($G1 - $G2 - $G3)") 
    printf "$frame \t $dG_xfer_CRB \n" >> dG_xter_CRB.dat 
    if ! grep -q $frame dG_xter_CRB.dat ; then echo "Failed" ; exit ; fi 
    echo $dG_xfer_CRB  

    done 

printf "\n\t *** Program Complete  *** \n\n" 




