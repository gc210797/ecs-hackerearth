This project was created for the challenge on hackerearth for ECS. This is the first time I am ever dealing with dynamoDB, using boto3 and using flask to implement this. This was supposed to be completed in 6 hours. I wasn't able to complete this in the given time due to lack of hands on, on these technologies but taking extra 2 hours I completed the requirements. It being quite hectic and pulling this much off in about 8 hrs without any hands on using these technologies, it seemed like quite an achievement for me.

# Requirements:
- Using dynamodb create provided methods. These methods should be exposed using flask as an API.
- Methods:
  - get_books(filter, page_number, page_size): This should list out all the books, for which data is provided in the zip. 
    - **filter** will provide attribute to filter it by, eg. title=Harry Potter. I have not been able to yet figure how to make it generic and use the one passed by the caller. Will look into this in future so for now only 'equals' operation is supported for filtering
    - **page_number** will provide the page we want to get to for the results.
    - **page_size** will provide the number of elements in each page of results.
  - get_book(id): This will provide a single result for an provided book id
  - add_book(params): This will add book to the **data** table created using the provided zip file
  - update_book(id, params): This will update the book with provided attribute in params for the book with provided book id
  - get_favourite(user_id): This will provide all the favourite books of a user with provided user_id
  - add_favourite(user_id, book_id): This will add favourite book with provided book_id and to the user with provided user_id
  - remove_favourite(user_id, book_id): This will remove provided book_id from favourites of user with provided user_id

# Desireable requirements
  - Add token based authentication - Implemented
  - Provide a better single table schema - I will implement in future if I find some time and add it to the repo. This will require more reading of dynamoDB and thinking.
  - Create frontend for API - I will implement in future if I find some time.

# Users Table:
``aws dynamodb create-table --table-name users --attribute-definitions AttributeName=user_id,AttributeType=S --key-schema AttributeName=user_id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=5 --endpoint_url http://localhost:8000``

# Test
``pytest -v -s``

# Run
``python main.py``

This has a lot of space for improvement. Off the bat I would want to make the API more RESTful, currently the endpoints are quite verbose and the operations should have been based on methods only. In some future, I would definitly improve the API. Also the response from API doesn't remove the dynamoDB elements of the type, which I would also change.
