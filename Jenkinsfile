
pipeline {
    agent any

    environment {
        IMAGE_NAME = "krithikan99/hello"
        DOCKER_PATH = "C:\\Users\\admin\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin"
    }

    stages {
        stage('Git Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Generate Image Tag') {
            steps {
                script {
                    env.IMAGE_TAG = new Date().format("yyyy-MM-dd-HHmmss")
                }

                echo "Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Docker Build') {
            steps {
                bat '''
                    "%DOCKER_PATH%\\docker.exe" build ^
                    -t "%IMAGE_NAME%:%IMAGE_TAG%" ^
                    -t "%IMAGE_NAME%:latest" .
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker_cred',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    powershell '''
                        $ErrorActionPreference = 'Stop'

                        $env:DOCKER_PASSWORD |
                            & "$env:DOCKER_PATH\\docker.exe" login `
                                -u $env:DOCKER_USERNAME --password-stdin

                        if ($LASTEXITCODE -ne 0) {
                            exit $LASTEXITCODE
                        }
                    '''
                }
            }
        }

        stage('Docker Push') {
            steps {
                bat '''
                    "%DOCKER_PATH%\\docker.exe" push "%IMAGE_NAME%:%IMAGE_TAG%"
                    if errorlevel 1 exit /b %ERRORLEVEL%

                    "%DOCKER_PATH%\\docker.exe" push "%IMAGE_NAME%:latest"
                    if errorlevel 1 exit /b %ERRORLEVEL%
                '''
            }
        }

        stage('Docker Logout') {
            steps {
                bat '''
                    "%DOCKER_PATH%\\docker.exe" logout
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
            echo "Pushed image: ${IMAGE_NAME}:${IMAGE_TAG}"
            echo "Latest image: ${IMAGE_NAME}:latest"
        }

        failure {
            echo "Pipeline failed. Please check the Console Output."
        }
    }
}
