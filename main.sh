#!/bin/bash

register_player(){
local reg_username="$1"
local reg_password="$2"
hash_reg_password=$(hash_pass "$reg_password")
echo -E "$reg_username'\t'$hash_reg_password">>"$USER_FILE"
echo "Signed Up!Lesss gooo!"
}

login_player(){
local username ="$1"
local password ="$2"
if [[ $existuser ]];then 
hash_password=$(hash_pass "$password")
stored_password=$(stored_hash_pass "$username")

if [[ $hash_password==$stored_password ]];then 
echo "Login Successful"
authenticated=1
fi
else echo "Wrong Password!Try again"
fi
else 
read -p  "username incorrect ? or register ? type "yes" to register and "no" to retry login :" desire
if [[ $desire=="yes" ]];then
read -p "username" : username1
read -s -p "password" : password1
register_player "$username1" "$password1"
else 
read -p "username" : username1
read -s -p "password" : password1
login_player "$username1" "$password1"
