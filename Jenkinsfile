pipeline{
    agent any
    environment{
        dockerhubCred= credentials('docker-cred')
        dockerImage= 'dhruvrs/stock-app:latest'
    }
    stages{
        stage('Git Checkout'){
            steps{
                git(
                    url: 'https://github.com/DhumalePrasad04/test.git',
                    branch: 'main'  
                )
            }
        }
            
        stage('Build Docker Image'){
            steps{
                script{
                    docker.build(dockerImage)
                }
            }
        }
        stage("Push to Docker Hub"){
            steps{
                script{
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-cred') {
                        docker.image(dockerImage).push('latest')
                    }
                }
            }
        }
        stage('Deploy to k8s'){
            steps{
                script{
                    sh 'kubectl apply -f k8s/deployment.yaml'
                    sh 'kubectl apply -f k8s/service.yaml'
                }
            }
        }
    }
}