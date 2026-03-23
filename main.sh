authentication(){
work=0
existuser=0
authenticated=0
 username=$1
 password=$2
user_exist "$username"
login_player "$username" "$password"
}
hash_pass(){ 
    echo -n $1 | sha256sum | awk '{print $1}'
    }
stored_hash_pass(){
    grep -name "$1" users.tsv | cut -d$'\t' -f2
}
user_exist(){
    file='users.tsv'
    while read -r line; do
    if [[ cut -d$'|t' -f1 $(line) == $1 ]]; then
    existuser=1;
    fi
    done < "$file" 
}

check_info(){
    file='users.tsv'
    while read -r line; do
if [[ existuser ]]; then
    if [[ cut -d$'\t' -f2 $(line) == $(hash_pass "$2") ]]; then
    work=1
    else
    echo "Incorrect password.Try again!"
    fi
    done < "$file"
}
read -p "Player 1 username: " username1
read -s -p "Player 1 password: " password1
read -p "Player 2 username: " username2
read -s -p "Player 2 password: " password2
authentication "$(username1)" "$(password1)"
authentication "$(username2)" "$(password2)"
