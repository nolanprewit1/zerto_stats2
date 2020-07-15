# zerto_stats2
A internal status and alerting platform integrated with Zerto Analytics API.

Build Information 

    - Author = Parker Prewit
    - Author Email = nolanprewit1@gmail.com

What Is This? 


How To Use This 

    Running locally    
        1. Run `pip install -r requirements.txt` to install all dependecies
        2. Run `python app.py` to start and run the application

    Running in Docker container
        1. Run `git clone https://github.com/nolanprewit1/zerto_stats2.git` to download the source code to your desired server
        2. Run ` docker-compose up -d --force-recreate --build ` to build and run the included docker-compose file. 

    Viewing logs on docker contianers
        1. ru ` docker-compose logs zerto_stats2_poller `

Stop and remove all docker containers, images, and volumes

    docker stop $(docker ps -a -q) && \
    docker rm $(docker ps -aq) && \
    docker system prune -a -f && \
    docker image prune -a -f && \
    docker volume prune -f