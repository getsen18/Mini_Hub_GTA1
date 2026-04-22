<<<<<<< HEAD
#!/bin/bash
=======
file="history.csv"
curr_game=$(tail -1 "$file" | cut -d "," -f4)
player_list=()
while IFS=',' read -r winner loser date game; do
    if [[ "$game" == "$curr_game" ]]; then
        player_list+=("$winner")
        player_list+=("$loser")
    fi
done < <(tail -n +2 "$file")
unique_list=()
for p in "${player_list[@]}"; do
    added=false
    for exist in "${unique_list[@]}"; do
        if [[ "$exist" == "$p" ]]; then
            added=true
            break
        fi
    done
    if [[ "$added" == false ]]; then
        unique_list+=("$p")
    fi
done
touch tempfile.txt
for pl in "${unique_list[@]}"; do
    win_count=0
    lose_count=0
    while IFS=',' read -r winner loser date game; do
        if [[ "$game" == "$curr_game" ]]; then
            if [[ "$pl" == "$winner" ]]; then
                win_count=$((win_count + 1))
            fi
            if [[ "$pl" == "$loser" ]]; then
                lose_count=$((lose_count + 1))
            fi
        fi
    done < <(tail -n +2 "$file")
    if [[ "$lose_count" -eq 0 ]]; then
        wlratio=9999
    else
        wlratio=$((win_count / lose_count))
    fi
    echo "$pl $win_count $lose_count $wlratio" >> tempfile.txt
done
SORT_BY=$1
 if [ "$SORT_BY" = "wins" ]; then
            SORT_KEY=$win_count
        elif [ "$SORT_BY" = "losses" ]; then
            SORT_KEY=$loss_count
        else
            SORT_KEY=$RATIO_NUMBER
        fi
        # Save everything to the temp file as one line
        # Format: sortkey|playername|wins|losses|ratio
        echo "$SORT_KEY|$PLAYER|$WIN_COUNT|$LOSS_COUNT|$RATIO_TEXT" >> "$TEMP_RESULTS_FILE"
    done  
 
   
    while IFS='|' read -r sort_key player_name wins losses ratio; do
        printf "  %-15s %4s  %6s  %6s\n" "$player_name" "$wins" "$losses" "$ratio"
    done < <(sort -t'|' -k1 -rn "$TEMP_RESULTS_FILE")
    rm -f "$TEMP_RESULTS_FILE"
done  
echo ""
echo "==============================="
echo ""
[23:07, 01/04/2026] Peethalu: #!/bin/bash
>>>>>>> Teenu
file = "history.csv"
curr_game=tail -1 $file | cut -d "," -f4
player_list=()
while IFS=',' read -r winner loser date game; do
<<<<<<< HEAD
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



		
	
=======
        if [[ $game==$curr_game ]];then
                player_list+=("$winner")
                player_list+=("$loser")
        fi
done << (tail -n +2 "$file")
unique_list=()
>>>>>>> Teenu
