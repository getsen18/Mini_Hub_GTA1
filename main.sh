#!/bin/bash
CRED_FILE="./users.tsv"

hash_pass() {
    echo -n "$1" | sha256sum | awk '{print $1}'
}

stored_hash_pass() {
    grep -P "^$1\t" "$CRED_FILE" | cut -d$'\t' -f2
}

user_exist() {
    grep -q -P "^$1\t" "$CRED_FILE"
    }

register_player() {
    local reg_username="$1"
    local reg_password="$2"
    local hashed=$(hash_pass "$reg_password")
    if user_exist "$reg_username" ; then
        echo "Username already taken! Try a different one."
        return 1
    fi

    echo -e "$reg_username\t$hashed" >> "$CRED_FILE"
    echo "Registered Yayy! Welcome $reg_username"
    return 0
}
login_player() {
    local username="$1"
    local password="$2"
    local entered_hash=$(hash_pass "$password")
    local stored=$(stored_hash_pass "$username")

    if [[ "$entered_hash" == "$stored" ]]; then
        echo "Login done!Welcome back $username,lesss goo!"
        return 0
    else
        echo "Damnn!wrong password,try again.:<"
        return 1
    fi
}
authenticate() {
    local player_num="$1"
    local other_player="$2"
    local authenticated=false
    local username
    local password

    while [[ "$authenticated" == "false" ]]; do
        echo ""
        read -p "Player $player_num -Enter username :" username
        read -s -p "Player $player_num - Enter password :" password
        echo ""  
        if [[ "$username" == "$other_player" ]]; then
            echo "Ahh!someone else has the same username...Try a different account."
        continue
        fi

        if user_exist "$username" ; then
        if login_player "$username" "$password" ; then
        authenticated=true                      
        fi
        else
 echo "Oh damn!The username don't exist!?"
            read -p "Do you want to register? (yes/no): " desire

            if [[ "$desire" == "yes" ]]; then
                if register_player "$username" "$password" ; then
                authenticated=true   
            fi
            else
                echo "Patientlyy..try again."
        
            fi
        fi
    done

    echo "$username"  
}

echo "Ayy!lets get into the Game World"
echo "Less goo player1"
player1=$(authenticate 1 "")


echo "Less go player2"
player2=$(authenticate 2 "$player1")


echo "Lets dig in playerss!!"
echo "Starting game for $player1 vs $player2  Less gooo!! ENRIQUEEE!!"


<<<<<<< HEAD
python3 game.py "$player1" "$player2"
=======
python3 game.py "$player1" "$player2"
>>>>>>> Teenu
