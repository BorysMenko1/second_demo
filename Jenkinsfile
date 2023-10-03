pipeline {
  agent {label 'jenkins-slave'}
  environment {
    GIT_COMMIT_HASH = sh (script: "git log -n 1 --pretty=format:'%H'", returnStdout: true)
  }
  stages {
    stage('Build') {
      steps {
        sh '''
        docker rm $(docker ps -aq) 2>/dev/null || true
        docker images -f "dangling=true" -q | xargs -r docker rmi --force
        docker build -t ecr-repo:latest -t ecr-repo:$GIT_COMMIT_HASH .
        '''
    }
    }
    stage('test') {
      steps {
          sh 'python3.8 -m pytest tests/test_project.py'
      }
    }
    stage('manual gate') {
      steps {
        input(message: "Do you want deploy application?", ok: "Yes!")
      }
    }
    stage('publish docker image') {
      steps {
        withCredentials([string(credentialsId: 'ECR_URI', variable: 'ECR_URI'), string(credentialsId: 'REGION', variable: 'REGION')]) {
          sh 'aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECR_URI}'
          sh 'docker tag ecr-repo:latest ${ECR_URI}/ecr-repo:latest'
          sh 'docker tag ecr-repo:$GIT_COMMIT_HASH ${ECR_URI}/ecr-repo:$GIT_COMMIT_HASH'
          sh 'docker push ${ECR_URI}/ecr-repo:latest'
          sh 'docker push ${ECR_URI}/ecr-repo:$GIT_COMMIT_HASH'
        }
      }
    }
  }
}
    // data dock monitoring tool