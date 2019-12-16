# Anchor Classifier
This is anchor classifier.
Your face can be classified to each category; ```NHK``` , ```フジテレビ``` , ```朝日テレビ``` , ```TBS``` , ```日本テレビ```

## How to use
### Run on your host OS(Mac)
1. Download and Install [Docker](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
2. Setup docker-compose
```
Docker version
curl -L https://github.com/docker/compose/releases/download/1.24.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose  
chmod 0755 /usr/local/bin/docker-compose 
Docker-compose -v  
```
3. Clone and docker-compose up
```
git clone https://github.com/wandora58/Anchor_Classifier.git
cd Anchor_Classifier
docker-compose up -d --build
```
4. Access this app
```
http://localhost/anchor/
```

### Let's Start!
When you enter your face image, this app will tell you the most recommended key station(```NHK``` , ```フジテレビ``` , ```朝日テレビ``` , ```TBS``` , ```日本テレビ```) 
