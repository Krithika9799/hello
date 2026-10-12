
pipeline {
    agent any

    environment {
        IMAGE_NAME = "krithikan99/hello"
        DOCKER_PATH = "C:\\Users\\admin\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin"
    }

    stages {

        stage('git-checkout') {
            steps {
                checkout scm
            }
        }

        stage('image-build') {
            steps {
                script {
                    env.IMAGE_TAG = new Date().format("yyyy-MM-dd-HHmmss")
                }

                bat '''
                    "%DOCKER_PATH%\\docker.exe" version
                    "%DOCKER_PATH%\\docker.exe" build -t "%IMAGE_NAME%:%IMAGE_TAG%" .
                '''
            }
        }

        stage('docker login') {
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
                        echo %DOCKER_PASSWORD% | "%DOCKER_PATH%\\docker.exe" login -u "%DOCKER_USERNAME%" --password-stdin
                    '''
                }
            }
        }

        stage('docker push') {
            steps {
                bat '''
                    "%DOCKER_PATH%\\docker.exe" push "%IMAGE_NAME%:%IMAGE_TAG%"
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! Docker image built and pushed to Docker Hub.'
        }

        failure {
            echo 'Pipeline failed. Please check the Console Output for details.'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}
