#!/usr/bin/env bash
cp ./Key_store/Bank* ./Bank_server/
cp ./Key_store/Client* ./Shop_client/
cp ./Key_store/Shop* ./Shop_server/
rm -f ./Key_store/Bank_private.pem
rm -f ./Key_store/Client_private.pem
rm -f ./Key_store/Shop_private.pem