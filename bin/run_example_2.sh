#!/bin/bash

# ungrip
./tecan roma_g 900
# clear above any objects
./tecan roma_z 2480
#return to base
./tecan roma_x 0
./tecan roma_y 0
./tecan roma_r 0


./tecan roma_g 900
./tecan roma_r 900
./tecan roma_z 2480
./tecan roma_x 5250
./tecan roma_y 2900
./tecan roma_z 1000
./tecan roma_rz -60
./tecan roma_g 805
./tecan roma_z 2000


#./tecan roma_x 6750
./tecan roma_rx 1500

./tecan roma_z 1110

./tecan roma_g 850
./tecan roma_z 2000


./tecan roma_z 2480
./tecan roma_y 0
./tecan roma_r 0
./tecan roma_x 0
