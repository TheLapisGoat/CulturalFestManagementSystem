Made as part of Assignment 3 for the Database Management Systems Lab Course, Spring 2023-24

## Group Members
- [Sourodeep Datta](https://github.com/TheLapisGoat)
- [Sampreeth R S](https://github.com/sampreeth-r-s)
- [Yash Kumar](https://github.com/yash23kr)
- [Yash Sirvi](https://github.com/c-12-14)
- [Ashwin Prasanth](https://github.com/ashwinpra)


## Local Setup Instructions 
- Install postgres, psql and setup user and database
- Create a file `credentials.json` in `FestivalManagementSystem/` and add the following content:
```json
{
    "USERNAME": <YOUR_POSTGRES_USERNAME>,
    "PASSWORD": <YOUR_POSTGRES_PASSWORD>
}
```
- Setup a virtual environment and activate it
- Install required packages 
- Run `python3 manage.py makemigrations webapp`
- Run `python3 manage.py migrate`
- Run `python3 manage.py runserver`