#!/bin/bash

token='h6EIh3PMyMh5h93nLUW9jpuZj9Ix1EJq'
secret='epeWOYJ04LI1hOgwtpcSpiILXKNkSQYq'
date=`date -u +'%Y-%m-%dT%H:%M:%SZ'`
signature=`echo -n "date: $date" | openssl dgst -sha256 -binary -hmac "$secret" | base64`

curl -H "Authorization: Bearer $token" -H "Date: $date" -H "Signature: keyId=\"$token\",algorithm=\"hmac-sha256\",headers=\"date\",signature=\"$signature\"" 'https://api.demo.narmitech.com/v1/account_balances/'
 
