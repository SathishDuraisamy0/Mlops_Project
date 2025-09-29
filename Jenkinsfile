pipeline{
    agent any 

    stages{
        stage("Cloning Github repo to Jenkins"){
            steps{
                script{
                    echo"cloning Github repo to Jenkins.........."
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/SathishDuraisamy0/Mlops_Project.git']])
                }
            }
        }
    }
}