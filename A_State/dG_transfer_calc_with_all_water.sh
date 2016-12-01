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

if [ ! -d ALL_WAT_ENERGIES ] ; then mkdir ALL_WAT_ENERGIES ; fi 
cd ALL_WAT_ENERGIES
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
    printf "Complete\n" 
else 
    printf "Skipped\n" 
    fi 

XTC=compress.xtc

printf "\n\t*** pdb2pqr and APBS    ***\n\n" 
index=0
echo "group Protein || group Water " > selection.dat
cat selection.dat | gmx select -s $TPR -f $XTC -on index.ndx >> $logFile 2>> $errFile 

for frame in $(seq 0 $timeStep $tot) ; do 
    printf "\tReading %5i of %5i..." $frame $tot
    
    if ! grep -sq Global time_${frame}_Protein-CRO.out ; then     

        echo $index | gmx trjconv -n index.ndx -f $XTC -s $TPR -o time_${frame}.pdb -dump $frame -tu ps >> $logFile 2>> $errFile 
        check time_${frame}.pdb 
        ((index++)) 

        ####For whatever reason, APBS only support 3-character names for residues 
        sed "s/CROn/CRO /" time_${frame}.pdb > temp.pdb 
        mv temp.pdb time_${frame}.pdb 

        if ! grep -sq CRO time_${frame}.pdb ; then 
            printf "ERROR: We left CRO behind! \n"
            exit 
            fi 

        pdb2pqr time_${frame}.pdb time_${frame}_Protein+CRO.pqr --userff AMBER.DAT --usernames AMBER.names --assign-only >> $logFile 2>> $errFile
        check time_${frame}_Protein+CRO.pqr 
             
        if grep -sq WARNING time_${frame}_Protein+CRO.pqr ; then 
            printf "\nERROR: Warning flagged in time_${time}_Protein+CRO.pqr file\n"
            exit 
            fi 

        #printf "\n\nDude this isn't going to work yet. Fix it\n\n"
        #exit     

        grep " CRO " time_${frame}_Protein+CRO.pqr > time_${frame}_cro.pqr 
        echo "TER " >> time_${frame}_cro.pqr 
        echo "END " >> time_${frame}_cro.pqr 
            
        awk '{if ($4 == "CRO") {$9 = "0.0000"} ; print }' time_${frame}_Protein+CRO.pqr > time_${frame}_Protein-CRO.pqr 
        check time_${frame}_Protein+CRO.pqr time_${frame}_Protein-CRO.pqr time_${frame}_cro.pqr

        sed "s/file2.pqr/time_${frame}_Protein+CRO.pqr/" ../../free_energy_files/20template.in > temp.in
        sed "s/file.pqr/time_${frame}_Protein+CRO.pqr/" temp.in > time_${frame}_Protein+CRO.in 
        sed "s/file.pqr/time_${frame}_Protein-CRO.pqr/" temp.in > time_${frame}_Protein-CRO.in 
        sed "s/file.pqr/time_${frame}_CRO.pqr/" temp.in > time_${frame}_CRO.in 
        rm temp.in

#APBS is called three times for each frame. The first call takes ~5 sec (smaller system), the second two take 10-15 each. 
        printf "1..." 
        apbs time_${frame}_cro.in > time_${frame}_cro.out 2>> time_${frame}.err 
        if ! grep -q Global time_${frame}_cro.out ; then echo "Failed" ; exit ; fi 

        printf "2..." 
        apbs time_${frame}_Protein+CRO.in > time_${frame}_Protein+CRO.out 2>> time_${frame}.err
        if ! grep -q Global time_${frame}_Protein+CRO.out ; then echo "Failed" ; exit ; fi 
   
        printf "3..." 
        apbs time_${frame}_Protein-CRO.in > time_${frame}_Protein-CRO.out 2>> time_${frame}.err 
        if ! grep -q Global time_${frame}_Protein-CRO.out ; then echo "Failed" ; exit ; fi 

        printf "Complete\n" 
    else  
        printf "............Skipped\n" 
        fi 
    
    done 

printf "\n\t *** Compiling Results *** \n\n" 
if [ -f dG_xter_CRO.dat ] ; then rm dG_xter_CRO.dat ; fi 
for frame in $(seq 0 $timeStep $tot) ; do 
    printf "\tFrame   %5i of %5i....." $frame $tot
    if ! grep -sq Global time_${frame}_Protein+CRO.out ; then 
        printf "\nERROR: Delete time_${frame}_Protein-CRO.out and repeat\n" 
        fi 
    if ! grep -sq Global time_${frame}_cro.out ; then 
        printf "\nERROR: Delete time_${frame}_Protein-CRO.out and repeat\n" 
        fi 
    if ! grep -sq Global time_${frame}_Protein-CRO.out ; then 
        printf "\nERROR: How did you get here? I have a logical fallacy\n" 
        fi 

    G1=$(grep Global time_${frame}_Protein+CRO.out | awk '{print $6}') 
    G2=$(grep Global time_${frame}_Protein-CRO.out | awk '{print $6}') 
    G3=$(grep Global time_${frame}_cro.out | awk '{print $6}') 

    dG_xfer_CRO=$(python -c "print ($G1 - $G2 - $G3)") 
    printf "$frame \t $dG_xfer_CRO \n" >> dG_xter_CRO.dat 
    if ! grep -q $frame dG_xter_CRO.dat ; then echo "Failed" ; exit ; fi 
    echo $dG_xfer_CRO  

    done 

printf "\n\t *** Program Complete  *** \n\n" 




