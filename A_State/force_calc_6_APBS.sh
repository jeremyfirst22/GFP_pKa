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

if [[ ${MOLEC:0:6} == 'GFP_WT' ]] ; then 
    echo "No nitrile on this molecuele. Nothing to do." 
    exit 
    fi 

if (( $tot % 4 )) ; then 
    echo "WARNING: $tot % 4 != 0. There may not be frames for requested time steps" 
    fi 
timeStep=$(echo "$tot / $numFrames" | bc) #ps 
if [[ $timeStep -lt 20 ]] ; then 
    echo "ERROR: Requested time step is $timeStep. Frames only printed every 20 ps." 
    exit ; fi 
logFile=$TOP/forces.log
errFile=$TOP/forces.err

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

if [ ! -d APBS_6_force_calc ] ; then mkdir APBS_6_force_calc ; fi 
cd APBS_6_force_calc
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
if [ -f rxn_field.out ] ; then rm rxn_field.out ; fi 
if [ -f coloumb_field.out ] ; then rm coloumb_field.out ; fi 
for frame in $(seq 0 $timeStep $tot) ; do 
    printf "\tReading %5i of %5i..." $frame $tot

    if [ ! -f time_${frame}.pdb ] ; then 
        echo '1' | gmx trjconv -f $XTC -s $TPR -o time_${frame}.pdb -dump $frame -tu ps >> $logFile 2>> $errFile 
        check time_${frame}.pdb 
        fi 

    ####For whatever reason, APBS only support 3-character names for residues 
    sed "s/CROn/CRO /" time_${frame}.pdb > temp.pdb 
    mv temp.pdb time_${frame}.pdb 

    if ! grep -sq CRO time_${frame}.pdb ; then 
        printf "ERROR: We left CRO behind! \n"
        exit 
        fi 

    if [ ! -f time_${frame}.pqr ] ; then 
        pdb2pqr time_${frame}.pdb time_${frame}.pqr --userff AMBER.DAT --usernames AMBER.names --assign-only >> $logFile 2>> $errFile
        check time_${frame}.pqr 
        fi 

    if [ ! -f time_${frame}+DUM.pqr ] ; then 
        python ../../free_energy_files/add_dummy_pqr.py time_${frame}.pqr 0.1 CNF CT NH > time_${frame}+DUM.pqr 
        fi 

    if [[ ! -f time_${frame}_78.txt || ! -f time_${frame}_1.txt ]] ; then 
        sed "s/SDIE/78/" ../../free_energy_files/force_6_temp.in | sed "s/FRAME/${frame}/" >> time_${frame}_78.in 
        check time_${frame}_78.in 
        apbs time_${frame}_78.in >> $logFile 2>> $errFile 
        check time_${frame}_78.txt

        sed "s/SDIE/1/" ../../free_energy_files/force_6_temp.in | sed "s/FRAME/${frame}/" >> time_${frame}_1.in 
        check time_${frame}_1.in 

        apbs time_${frame}_1.in >> $logFile 2>> $errFile 
        check time_${frame}_1.txt
        fi 

    ../../free_energy_files/read_apbs_rxn_field time_${frame}+DUM.pqr time_${frame}_78.txt time_${frame}_1.txt >> rxn_field.out 2>> /dev/null
    check rxn_field.out

    python ../../free_energy_files/analytic_coloumb.py time_${frame}.pqr CNF NH CT >> coloumb_field.out 2>> /dev/null
    printf "Complete\n" 
    
    done 

printf "\n\t *** Program Complete  *** \n\n" 




