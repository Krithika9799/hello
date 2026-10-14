pipeline {
    agent any

    environment {
        IMAGE_NAME  = "krithikan99/hello"
        DOCKER_PATH = "C:\\Users\\admin\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin"

        // Per-build Docker config so the SYSTEM account doesn't depend on
        // Docker Desktop's credential helper or another user's config.
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

                    & $docker build -t $env:FULL_IMAGE .
                    if ($LASTEXITCODE -ne 0) { throw "docker build failed" }
                '''
            }
        }

        // Login and push MUST be in the same stage/block so the push is authenticated.
        stage("docker-login-push") {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'new',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    // Single-quoted ''' so Groovy never interpolates the secret.
                    powershell '''
                        $docker = "$env:DOCKER_PATH\\docker.exe"

                        $env:DOCKER_PASSWORD | & $docker login -u $env:DOCKER_USERNAME --password-stdin
                        if ($LASTEXITCODE -ne 0) { throw "Docker login failed" }

                        & $docker push $env:FULL_IMAGE
                        if ($LASTEXITCODE -ne 0) { throw "Docker push failed" }
                    '''
                }
            }
        }
    }

    post {
        always {
            powershell '''
                & "$env:DOCKER_PATH\\docker.exe" logout
                exit 0
            '''
            echo "Pipeline execution completed."
        }
    }
}