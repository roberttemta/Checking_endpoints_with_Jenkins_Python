pipeline {
    agent { 
      docker { image 'python:3.8.16-bullseye' 
             args '-u root'}
    }
    stages {
       stage ("Run the script") {
            steps {
                sh "pip3 install -r requirements.txt"
                sh "python3 check_endpoint.py"
            }
        }
    }
}
