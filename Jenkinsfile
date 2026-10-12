
pipeline {
    agent any

    environment {
        IMAGE_NAME = "krithikan99/hello"
        DOCKER_PATH = "C:\\Users\\admin\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin"
    }

    stages {
        stage("git-checkout") {
            steps {
                checkout scm
            }
        }

        stage("image-build") {
            steps {
                script {
                    env.IMAGE_TAG = new Date().format("yyyy-MM-dd-HHmmss")
                    env.FULL_IMAGE = "${env.IMAGE_NAME}:${env.IMAGE_TAG}"
                }

                bat '''
                    "%DOCKER_PATH%\\docker.exe" version
                    "%DOCKER_PATH%\\docker.exe" build -t "%FULL_IMAGE%" .
                '''
            }
        }

        stage("docker login") {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker_cred',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    bat '''
                        @echo off
                        echo %DOCKER_PASSWORD% | "%DOCKER_PATH%\\docker.exe" login -u %DOCKER_USERNAME% --password-stdin
                    '''
                }
            }
        }

        stage("docker push") {
            steps {
                bat '''
                    "%DOCKER_PATH%\\docker.exe" push "%FULL_IMAGE%"
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline execution completed."
        }
    }
}