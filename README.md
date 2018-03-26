# SEProject 

### 1. Installation

<!--
For Mac User:
##### 1. Install MYSQL ()
    brew install mysql-server
    brew tap homebrew/services
    brew services start mysql
    mysqladmin -u root password 'yourpassword'
-->

##### 2. Download repository and run
    git clone https://github.com/liuchengtian/SE568
    cd SE568
    pip install -r requirements.txt
    cd source
    python fetch_data.py
    python app.py
    
### 2. Resource

[Gentelella](https://github.com/puikinsh/gentelella) is a free to use Bootstrap admin template.

This project(https://github.com/afourmy/flask-gentelella) integrates Gentelella with Flask using blueprints, flask_login and flask_migrate.