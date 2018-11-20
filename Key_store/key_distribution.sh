#!/usr/bin/env bash
cp ./Bank* ../Bank_server/
cp ./Client* ../Shop_client/
cp ./Shop* ../Shop_server/
rm -f ./Bank_private.pem
rm -f ./Client_private.pem
rm -f ./Shop_private.pem