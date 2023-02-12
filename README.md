# FindmeHelpme

Find me help me
A voluntary initiative aimed at locating the missing after the earthquakes in Turkey and Syria 2023

The initiative emerged after strong earthquakes struck several areas in Turkey and Syria, which doubled the threat to the lives of people trapped under the rubble. We launched a technology platform to coordinate rescue efforts.

https://findmehelpme.com/




## Project features

 - Pin on the map to notice a missing person:
Where the relative of the missing person can put a pin on the map for the last place before the earthquake with there with name, description, and phone number.

 - Search on map 
Volunteers can browse the map and search for the injured or missing in the area where they are located.

 - Add a go-to location button, a link showing the location on google maps 
 
 - Allow adding multiple people in one pin (like family or roommates)
 
 - Automatically update an excel sheet on every new change in dB
 
 - Add new pins type (missing, in hospital, need help, found), thess pins shows with 4 differnt collers on map
 
 - Updating state is ready as backend through Gmail authentication, the person who made the report can update the status (only backend needs a frontend)
 
 - Add search-by-name bar
 
 - frontend for the update status (table page needs to login)

## Missing:
 - Enhance UI/UX 
 - add image/s to missing pin (Need legal approval)
 
### NOTE : You can create pull request to ``new_development`` branch for development.
 
## HOW TO RUN THE PROJECT (without docker)
1. clone the project
```
git clone https://github.com/abdullah-audteye/DepremKayiplari.git
```
2. change the branch for ``new_development`` branch with this command :
```
git checkout new_development
```

3. create python virtual environment and activate it from terminal (ubuntu & mac) 
```
cd DepremKayiplari
virtualenv env
```
then activate the env
```
source env/bin/activate
```
4. create .env file (ubuntu & mac) 
```
touch .env
```
5. fill the .env params
```
DEBUG=True
SECRET_KEY=< Your SECRET_KEY>
```
- **you can use sqlite for development pourpes**
 go to `appname/setting.py` Line 94 and comment out
 ```
  DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': BASE_DIR / 'db.sqlite3',
     }
 }
```
 and comment from line 101 to 110
 
6. install dependecies 
```
pip3 install -r requirements.txt
```
7. migrate the DB
```
python manage.py makemigrations
```
```
python manage.py migrate
```
8. run the app 
```
python manage.py runserver
```

 
