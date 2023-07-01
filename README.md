# 🔗 Installation Process

1.  Install [Python](https://python.org/download)
2.  Copy the repo

```plaintext
git clone https://github.com/Shoib007/BillingAppVersion1.gi
```

     3.  Go into the project Folder

```plaintext
cd BillingAppVersion1
```

     4. Install the requirement.txt files using the following command.

```plaintext
pip install -r requirement.txt
```

     5. Make migrations of the models

```plaintext
python manage.py makemigrations
```

     6. Migrate the models

```plaintext
python manage.py migrate
```

     7. Finally, run the development server

```plaintext
python manage.py runserver
```

## API URL

<table><tbody><tr><td>SN</td><td>API Functions (Request Type)</td><td>API URL</td></tr><tr><td>1</td><td>Get access/ refresh token (GET)</td><td>http://localhost:8000/token/</td></tr><tr><td>2</td><td>Register User (POST)</td><td>http://localhost:8000/register/</td></tr><tr><td>3</td><td>Posting Order (POST)</td><td>http://localhost:8000/order/</td></tr><tr><td>4</td><td>Getting specific Order (GET)</td><td>http://localhost:8000/token/{order_num}</td></tr></tbody></table>
