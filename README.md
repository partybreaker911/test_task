## Test case 
### How to run project

-   For local build, use command like:

        $ docker-compose -f local.yml build --no-cache

-   For starting project localy, use: 

        $ docker-compose -f local.yml up

-   For generate admin user, use command:

        $ docker-compose -f local.yml run django python manage.py initadmin
    
this command generate superuser with  this credentials:

            email: admin@example
            username: admin
            password: admin

-   For seed database employees, use command:

        $ docker-compose -f local.yml run django  python manage.py seed_employees <count_of_records> <count_of_hierarchy>

- If you need to delete all employees, use: 

        $ docker-compose -f local.yml run django python manage.py delete_employees

-   For cathing all email's for user auth and registration used `mailhog` you can access it from web browser using this ip address in your local deployment 0.0.0.0:8025