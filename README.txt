Hello,

In reference to task requirements please read this file to properly set-up the project.

-----------------------------------------------------------------------------------------
A: RUNNING SERVER

1st method: using docker-compose

- open terminal window in ..images\image_app\images (where e.g. Dockerfile is located)
- run command: docker compose up --build
- server is running

2nd method: using terminal

- open terminal window in ..images\image_app\images (where e.g. manage.py is located)
- run command: python manage.py runserver 8000
- server is running

-----------------------------------------------------------------------------------------

B: LOGIN DATA

Superuser name: ImagesAdmin
Superuser password: 123password123
Superuser has been granted Enterprise tier

Testuser1 name: Testuser456
Testuser1 password: 456password456
Testuser456 has been granted Basic tier

Testuser2 name: Testuser789
Testuser2 password: 789password789
Testuser789 has been granted Premium tier

-----------------------------------------------------------------------------------------

C: ENDPOINTS

ADMIN: http://127.0.0.1:8000/admin/     ADMIN NAME: ImagesAdmin		PASSWORD: 123password123

LOGIN: http://127.0.0.1:8000/login/
LOGOUT: http://127.0.0.1:8000/logout/

LIST AND UPLOAD IMAGES: http://127.0.0.1:8000/image_upload/
IMAGE DETAIL: http://127.0.0.1:8000/image_upload/<pk>/		e.g.	http://127.0.0.1:8000/image_upload/1/
THUMBNAILS: http://127.0.0.1:8000/image_upload/<pk>/thumbnails/		e.g. 	http://127.0.0.1:8000/image_upload/1/thumbnails/
LIST CREATE BINARY IMAGE: http://127.0.0.1:8000/image_upload/<pk>/binary/	e.g 	http://127.0.0.1:8000/image_upload/1/binary/

-----------------------------------------------------------------------------------------

D: MORE INFO

There are created 3 users like above with different types of granted tiers. Every user has already uploaded one image. 

To create new tier:
In admin panel add AccountTier, 200px is required

To create new user: 
In admin panel add user, then create a profile for that user, and You can choose account tier or create a new one.

If there occur a problem with server starting, the only thing left is to say classically: "Strange, it works for me".


-----------------------------------------------------------------------------------------

E: TIME I SPEND PERFORMING THE TASK

During given 10 days I asked for an extra week to fulfill this project. 
I have to point out, that majority of topics and technologies I had to face with, I was just learning for the first time.
I spend on average 2,5 hours every day to learn, train and try to implement new threads. 
Well then, summarizing: it could be about 50 hours. 


-----------------------------------------------------------------------------------------


Best regards
Szymon Wais












