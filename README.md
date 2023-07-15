## Test case 

All business logic is placed in a separate layer from view, such as `service`

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

        $ docker-compose -f local.yml run django  python manage.py seed_employees

- If you need to delete all employees, use: 

        $ docker-compose -f local.yml run django python manage.py delete_employees

### TODO

- Add ajax drug&drop
- Add tests
- Add github ci
