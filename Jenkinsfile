pipeline {
    agent any

    environment {
        IMAGE_NAME  = "krithikan99/hello"
        DOCKER_PATH = "C:\\Users\\admin\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin"

        // Isolates Docker's config/credentials per build. Avoids credential-helper
        // problems when Jenkins runs as a different Windows user than "admin".
        DOCKER_CONFIG = "${env.WORKSPACE}\\.docker"
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
                    env.IMAGE_TAG  = new Date().format("yyyy-MM-dd-HHmmss")
                    env.FULL_IMAGE = "${env.IMAGE_NAME}:${env.IMAGE_TAG}"
                }

                powershell '''
                    $docker = "$env:DOCKER_PATH\\docker.exe"

                    & $docker version
                    if ($LASTEXITCODE -ne 0) { throw "docker version failed" }

                    & $docker build -t $env:FULL_IMAGE .
                    if ($LASTEXITCODE -ne 0) { throw "docker build failed" }
                '''
            }
        }

        // TEMPORARY: remove once login works. Prints lengths only, never the secret.
        stage("debug-creds") {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'krithikan99',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    powershell '''
                        Write-Host "whoami: $(whoami)"
                        Write-Host "User length: $($env:DOCKER_USERNAME.Length)"
                        Write-Host "Pass length: $($env:DOCKER_PASSWORD.Length)"
                    '''
                }
            }
        }

        stage("docker-login-push") {
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
        always {
            // Always log out so credentials don't linger in the workspace config.
            powershell '''
                & "$env:DOCKER_PATH\\docker.exe" logout
                exit 0
            '''
            echo "Pipeline execution completed."
        }
    }
}