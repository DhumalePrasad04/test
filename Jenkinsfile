pipeline{
    agent any
    environment{
        dockerhubCred= credentials('docker-cred')
        dockerImage= 'dhruvrs/stock-app:latest'
    }
    stages('Git pull'){
        steps{
            git(
                url: 'https://github.com/DhumalePrasad04/test.git'  
            )
        }
        stages('Build Docker Image'){
            steps{
                script{
                    docker.build(dockerImage)
                }
            }
        }
        stages("Push to Docker Hub"){
            steps{
                script{
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-cred') {
                        docker.image(dockerImage).push('latest')
                    }
                }
            }

        }
    }
}