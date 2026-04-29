<<<<<<< HEAD
#!/bin/bash
<<<<<<< HEAD
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
=======

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"  # absolute path to the folder this script lives in — so history.csv is always found regardless of where we're called from
file="$SCRIPT_DIR/history.csv"  # history file lives next to this script in the project root

if [[ -n "$1" ]]; then
    curr_game="$1"  # game name passed as argument from game.py — e.g. "tictactoe"
elif [[ -f "$file" ]]; then
    curr_game=$(tail -1 "$file" | cut -d',' -f4)  # no argument — fall back to whatever game was played last
else
    echo "No history found."
    exit 1
fi

if [[ ! -f "$file" ]]; then
    echo "No history file found."
    exit 1
fi

declare -A wins    # associative array — maps player name → win count
declare -A losses  # associative array — maps player name → loss count

while IFS=',' read -r winner loser date game; do
    [[ "$game" != "$curr_game" ]] && continue  # skip rows for other games — only count the current one
    wins["$winner"]=${wins["$winner"]:-0}      # init to 0 if this player hasn't been seen yet
    wins["$loser"]=${wins["$loser"]:-0}        # loser still needs a wins entry so they appear in the table
    losses["$winner"]=${losses["$winner"]:-0}  # winner still needs a losses entry
    losses["$loser"]=${losses["$loser"]:-0}
    wins["$winner"]=$(( wins["$winner"] + 1 ))    # increment winner's win count
    losses["$loser"]=$(( losses["$loser"] + 1 ))  # increment loser's loss count
done < <(tr -d '\r' < "$file")  # tr strips \r — Python on Windows writes \r\n and bash would keep the \r in the last field otherwise

if [[ ${#wins[@]} -eq 0 ]]; then
    echo "No records found for game: $curr_game"
    exit 0
fi


echo "   LEADERBOARD: $curr_game"

printf "  %-15s %5s  %6s  %5s\n" "PLAYER" "WINS" "LOSSES" "W/L"  # header row — column widths matched to data rows below


SORT_BY="${2:-wins}"  # second argument sets sort order — defaults to wins if not given
if [[ "$SORT_BY" == "losses" ]]; then
    sort_field=3  # pipe format is w|player|l|ratio — field 3 is losses
elif [[ "$SORT_BY" == "ratio" ]]; then
    sort_field=4  # field 4 is ratio
else
    sort_field=1  # default — sort by wins (field 1)
fi

tmp=$(mktemp)  # temp file to collect all rows before sorting — can't sort a while-read loop in place
for player in "${!wins[@]}"; do
    w=${wins["$player"]}
    l=${losses["$player"]}
    if [[ "$l" -eq 0 ]]; then
        ratio=9999  # sentinel for "never lost" — shown as "inf" in output
>>>>>>> 60d6bf5d94f2df3e840a2886850ffd15dbebdbd3
    else
        ratio=$(( w / l ))  # integer division — good enough for ranking
    fi
<<<<<<< HEAD
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
        if [[ $game==$curr_game ]];then
                player_list+=("$winner")
                player_list+=("$loser")
        fi
done << (tail -n +2 "$file")
unique_list=()
=======
    printf "%s|%s|%s|%s\n" "$w" "$player" "$l" "$ratio" >> "$tmp"  # pipe-delimited so sort -t'|' can split on it
done

sort -t'|' -k"$sort_field" -rn "$tmp" | while IFS='|' read -r w player l ratio; do  # sort descending numerically, then print each row
    if [[ "$ratio" -eq 9999 ]]; then
        ratio_str="inf"  # convert sentinel back to readable "inf"
    else
        ratio_str="$ratio"
    fi
    printf "  %-15s %5s  %6s  %5s\n" "$player" "$w" "$l" "$ratio_str"
done

rm -f "$tmp"  # clean up temp file
>>>>>>> 60d6bf5d94f2df3e840a2886850ffd15dbebdbd3
