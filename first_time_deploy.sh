#! /bin/bash

echo '======== Installing NGINX ================'

sudo apt update
sudo apt install nginx

echo ''
echo '*******************************************'


echo '======== Enabling NGINX on Firewall =============='

sudo ufw allow 'Nginx HTTPS'
sudo ufw status

echo ''
echo '******************************************'
echo ''

systemctl status nginx

echo ''
echo '******************************************'

echo '======== Start NGINX ====================='

sudo systemctl start nginx

echo ''
echo '******************************************'


echo '========= Create folder within NGINX =========='
sudo mkdir -p /var/www/sairamsubramaniam.in/html
sudo chown -R $USER:$USER /var/www/sairamsubramaniam.in/html
sudo chmod -R 755 /var/www/sairamsubramaniam.in

echo '**********************************************'

echo '============= END ==================='

echo '**********************************************'

