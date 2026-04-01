#!/bin/bash
file = "history.csv"
curr_game=tail -1 $file | cut -d "," -f4
player_list=()
while IFS=',' read -r winner loser date game; do
        if [[ $game==$curr_game ]];then
                player_list+=("$winner")
                player_list+=("$loser")
        fi
done << (tail -n +2 "$file")
unique_list=()
for p in "$(player_list[@])";do
added=false
for exist in "$(unique_list[@])";do
if [[ "$(exist)" == "$(p)" ]];then
 added=true
 break
fi
done
if [[ "$added" == false ]];do
unique_list+="$p"
fi
done
touch tempfile.txt
for pl in "$(unique_list[@])";do
win_count=0;
lose_count=0;
while IFS=',' read -r winner loser date game; do
if [[ "$(game)" == "$(curr_game)" ]];then
 if [[ "$pl" == "$winner" ]];then
 win_count=$((win_count+1))
 fi 
 fi
if[[ "$pl" == "$loser" ]];then                                                                                                                 
lose_count=$((lose_count+1))                                                                                                                                  
fi                                                                                                                                             
fi                                                                                                                                             
done << (tail -n +2 "$file")                                                                                                                   
if [[ "$(lose_count)" -eq 0 ]];then                                                                                                            
wlratio=9999                                                                                                                                   
else                                                                                                                                           
wlratio=$(win_count)/$(lose_count)                                                                                                             
fi                                                                                                                                             
echo "$(pl) $(win_count) $(lose_count) $(wlratio)" >> tempfile.txt                                                                             
done 



		
	
