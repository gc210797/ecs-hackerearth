Users Table:
aws dynamodb create-table --table-name users --attribute-definitions AttributeName=user_id,AttributeType=S --key-schema AttributeName=user_id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=5 --endpoint_url http://localhost:8000
