pipeline {
    agent any
    
    parameters {
        string(name: 'BRANCH', defaultValue: 'development',
               description: 'Branch to build from')
    }
    
    environment {
        DOCKER_IMAGE = "book-service:${BUILD_NUMBER}"
        FYRE_VM_USER = credentials('fyre-vm-ssh-key')
        FYRE_VM_HOST = 'your-fyre-vm-hostname'
        APP_PORT = 8080
        GITHUB_CREDENTIALS = credentials('github-credentials')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: "${params.BRANCH}",
                    credentialsId: "${GITHUB_CREDENTIALS}",
                    url: 'https://github.com/your-org/book-service.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${DOCKER_IMAGE} .
                    docker tag ${DOCKER_IMAGE} ${DOCKER_IMAGE}:latest
                """
            }
        }
        
        stage('Run Tests') {
            steps {
                sh """
                    docker run --rm ${DOCKER_IMAGE} \\
                        pip install pytest \\
                        && pytest tests/
                """
            }
        }
        
        stage('Deploy') {
            steps {
                sshagent(['fyre-vm-ssh-key']) {
                    sh """
                        ssh ${FYRE_VM_USER}@${FYRE_VM_HOST} \\
                            'docker stop \$(docker ps -aq -f name=book-service) || true'
                        ssh ${FYRE_VM_USER}@${FYRE_VM_HOST} \\
                            'docker rm \$(docker ps -aq -f name=book-service) || true'
                        docker tag ${DOCKER_IMAGE} ${FYRE_VM_USER}@${FYRE_VM_HOST:${APP_PORT}/book-service
                        docker push ${FYRE_VM_USER}@${FYRE_VM_HOST:${APP_PORT}/book-service
                        ssh ${FYRE_VM_USER}@${FYRE_VM_HOST} \\
                            'docker run -d --name book-service -p ${APP_PORT}:${APP_PORT} ${DOCKER_IMAGE}'
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo "Book Service deployed successfully at http://${FYRE_VM_HOST}:8080/book-service"
        }
        failure {
            echo "Deployment failed!"
        }
    }
}