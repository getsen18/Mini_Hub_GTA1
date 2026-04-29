#!/bin/bash
CRED_FILE="./users.tsv"  # tab-separated file storing username + hashed password, one per line

hash_pass() {
    echo -n "$1" | sha256sum | awk '{print $1}'  # sha256 hash of the password — never store plaintext
}

stored_hash_pass() {
    grep -P "^$1\t" "$CRED_FILE" | cut -d$'\t' -f2  # find the line starting with this username and grab column 2 (the hash)
}

user_exist() {
    grep -q -P "^$1\t" "$CRED_FILE"  # -q = quiet, just sets exit code — 0 if found, 1 if not
    }

register_player() {
    local reg_username="$1"
    local reg_password="$2"
    local hashed=$(hash_pass "$reg_password")  # hash before storing — raw password never touches the file
    if user_exist "$reg_username" ; then
        echo "Username already taken! Try a different one." >&2
        return 1
    fi

    echo -e "$reg_username\t$hashed" >> "$CRED_FILE"  # append new user — tab-separated to match grep pattern above
    echo "Registered Yayy! Welcome $reg_username" >&2
    return 0
}

login_player() {
    local username="$1"
    local password="$2"
    local entered_hash=$(hash_pass "$password")   # hash what they typed so we can compare against stored hash
    local stored=$(stored_hash_pass "$username")  # pull the hash that was saved at registration time

    if [[ "$entered_hash" == "$stored" ]]; then
        echo "Login done!Welcome back $username,lesss goo!" >&2
        return 0
    else
        echo "Damnn!wrong password,try again.:<" >&2
        return 1
    fi
}

authenticate() {
    local player_num="$1"   # 1 or 2 — just for the prompt text
    local other_player="$2" # the first player's username — prevents both players logging into the same account
    local authenticated=false
    local username
    local password

    while [[ "$authenticated" == "false" ]]; do
        echo "" >&2
        read -p "Player $player_num -Enter username :" username
        read -s -p "Player $player_num - Enter password :" password  # -s = silent, password won't show in terminal
        echo ""  >&2
        if [[ "$username" == "$other_player" ]]; then
            echo "Ahh!someone else has the same username...Try a different account." >&2
        continue  # same username as player 1 — reject and loop back
        fi

        if user_exist "$username" ; then
        if login_player "$username" "$password" ; then
        authenticated=true  # correct password — break out of the while loop
        fi
        else

            read -p "Do you want to register? (yes/no): " desire

            if [[ "$desire" == "yes" ]]; then
                if register_player "$username" "$password" ; then
                authenticated=true  # registration succeeded — they're in
            fi
            else
                echo "Patientlyy..try again." >&2

            fi
        fi
    done

    echo "$username"  # only line going to stdout — captured by $() in the caller to get the username back
}

echo "Ayy!lets get into the Game World" >&2
echo "Less goo player1" >&2
player1=$(authenticate 1 "")  # empty string for other_player — no restriction on player 1's username


echo "Less go player2" >&2
player2=$(authenticate 2 "$player1")  # pass player1's name so player2 can't reuse the same account


echo "Lets dig in playerss!!" >&2
echo "Starting game for $player1 vs $player2  Less gooo!! ENRIQUEEE!!" >&2

python3 game.py "$player1" "$player2"  # hand off to the pygame hub with both player names
