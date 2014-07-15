#####DEE: Environment Environment (self-hosted coding environment)

In my daily work I always meet situations when you can't reproduce project's 
environment on the local machine in reasonable timeframes. In most cases 
I used nano/vim directly on server, but sometimes you need something more 
comfortable. That's when DEE comes in. It can be easily installed on server 
and then used as server-hosted IDE.


#####Installation

1. sudo apt-get install python-virtualenv python-pip
2. git clone https://github.com/ogurtsov/dee.git
3. cd dee
4. virtualenv venv
5. source venv/bin/activate
6. pip install -r requirements.txt
7. ./manage.py syncdb (create a user with a strong password there)
8. ./manage.py 0.0.0.0:8000 (or use your IP instead of 0.0.0.0 to make it more secure)
9. access the DEE on http://example.com:8000/
