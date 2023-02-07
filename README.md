# Event manager
### Test project for the junior Python position in Poly-Tech
___
## Content
 - [Technologies](#what-we-used)
 - [Desription](#what-we-do)
 - [Star Project](#how-to-start-project)
 - [Sources](#sources)

## What we used?
_Technologies used_: Djando, DRF, Django-Unittest, SQLite.

## What we do?
We have developed a management system that accepts POST requests from POST request with Json. Accordingly, 
2 Django models were developed - 'Event_type' and 'Event'.<br>
<p>Example Json:<br>
{<br>"event_type": "Sleep", <br>"info":{"all_info": "text"}, <br>"timestamp": "2023-02-09 17:45:05"<br>}</p>
The 'Event_type' model has one column with the name. Records are created automatically when a POST request is received. 
If the record is already in the database, then it does not change.<br>
The UUIDs Pseudo-PK approach was used for 'Event' model. This means that database queries use the standard primary key. 
And for work with ORM, UUID key is used.
Benefits of UUID key include:<br>
	- They obscure the identifier, making it virtually impossible for attackers to guess IDs.<br>
	- They allow Foreign Key references to be similarly obscured.<br>
	- They allow for horizontal partitioning without key collision or rekeying concerns.<br>
At the same time, database performance is maintained.
The 'Event' model has 2 foreign keys - 'user' and 'event_type'. The 'created_at' column is filled in automatically. 
We take the user ID from the session, which is created by the token key.<br>
To get a token and work with token keys, we used the library 'rest_framework.authtoken'. On the basis of this library, 
a system was created for registering new users. Added the ability to work with 'event' and 'event_type' models to the admin panel.
And we also created the ability to generate a token key for users or delete them.<br>
For testing, you can use Unitest or manually test in Postman. 
The format of requests for a manual test is described in the file 'check_api.http'.

## How to start project?
1. Run `git clone {SSH-link from GitHub}` on your PC;
2. Run `pip install -r requirements.txt`;
3. Create '.env' file and write to it the enviroment variables:
	- SECRET_KEY (Fot example: 'django-insecure-5tj_b9&8y82i5lpeh1cc_3k^rgp4=!ti1wnu7x8!nop0@!281$')
4. Run `python3 manage.py migrate`;
5. Create superuser '`python3 manage.py createsuperuser`; 

## Sources
1. [Django REST framework official](https://www.django-rest-framework.org/)
2. [How to use UUID "Pseudo" Primary Keys in Django Rest Framework in 2 easy steps!](https://www.stevenmoseley.com/blog/tech/uuid-primary-keys-django-rest-framework-2-steps)