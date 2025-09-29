pipeline{
    agent any
 
    environment {
        VENV_DIR =''
    }

    stages{
        stage("Cloning Github repo to Jenkins"){
            steps{
                script{
                    echo"cloning Github repo to Jenkins.........."
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/SathishDuraisamy0/Mlops_Project.git']])
                }
            }
        }
        stage("Cloning vs"){
            steps{
                script{
                    echo"cloning up vs.........."
                    sh '''
                    python -m venv $(VIEW_DIR)
                    .&{VEW_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e.                
                    '''
                }
    }
}