nohup tbot start database-tunnel --listen=tcp://localhost:5432 --service=dev-psql-rds --username=teleport-db-admin --database=transactionsDb --join-method=iam --token=mcp-db-tunnel-bot-token --proxy-server=nebula-dash.teleport.sh:443 --storage=/tmp/tbot >> /dev/null &

cd ~/code/apex_auto_app

docker compose up