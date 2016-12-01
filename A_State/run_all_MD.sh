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
CN145_T203W     GFP_WT_T203F"
#CN145_T203B     CN145_T203X     CN145_T203Z
#CN165_T203B     CN165_T203X     CN165_T203Z
#GFP_WT_T203B    GFP_WT_T203X    GFP_WT_T203Z
#"

for molec in $molecList ; do 
        printf "\n\t$molec\n" 
        if [ ! -f submit_$molec ] ; then 
            echo "#!/bin/bash" > submit_$molec
            echo >> submit_$molec
            echo "#SBATCH -J $molec " >> submit_$molec
            echo "#SBATCH -o $molec.o%j" >> submit_$molec
            echo "#SBATCH -n 16 " >> submit_$molec
            echo "#SBATCH -p normal " >> submit_$molec
            echo "#SBATCH -t 48:00:00" >> submit_$molec
            echo "#SBATCH -A Understanding-biomol" >> submit_$molec
            echo "#SBATCH --mail-user=jeremy_first@utexas.edu" >> submit_$molec
            echo "#SBATCH --mail-type=all" >> submit_$molec
                                                                                                
            echo >> submit_$molec
            echo "module load boost " >> submit_$molec
            echo "module load cxx11 " >> submit_$molec
            echo "module load gromacs " >> submit_$molec 
            
           echo >> submit_$molec
           echo "bash run_GFP.sh StartingStructures/$molec.pdb" >> submit_$molec

           fi  

    #sbatch submit_$molec
    #bash run_GFP.sh StartingStructures/$molec.pdb
    #bash dG_transfer_calc.sh $molec
    #time bash 20dG_transfer_calc.sh $molec
    #time bash dG_transfer_calc_with_nearby_wat.sh $molec
    #time bash dG_transfer_calc_with_10_nearby.sh $molec
    #bash 6dG_transfer_calc.sh $molec
    #time bash force_calc_APBS.sh $molec
    #time bash force_calc_with_nearby_APBS.sh $molec
    #time bash dG_transfer_calc_with_nearby_lowE.sh $molec
    #time bash dG_transfer_calc_with_10_lowE.sh $molec
    #bash dG_transfer_calc_6.sh $molec
    bash dG_transfer_calc_8_with_nearby_wat.sh $molec
    done 
