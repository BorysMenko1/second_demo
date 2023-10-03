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
        sh 'docker run --entrypoint /usr/local/bin/python --rm ecr-repo:latest -m pytest tests/test_project.py'
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
          sh '''
            aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECR_URI}
            docker tag ecr-repo:latest ${ECR_URI}/ecr-repo:latest
            docker tag ecr-repo:$GIT_COMMIT_HASH ${ECR_URI}/ecr-repo:$GIT_COMMIT_HASH
            docker push ${ECR_URI}/ecr-repo:latest
            docker push ${ECR_URI}/ecr-repo:$GIT_COMMIT_HASH
          '''
        }
      }
    }
    stage('restart ecs task') {
      steps {
        withCredentials([string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'), string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')]) {
          sh '''
            export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
            export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
            aws ecs update-service --cluster demo-app-cluster --service cc-demo-app-service --task-definition demo-app-task --force-new-deployment
          '''
                }
      }
    }
  }
}
    // data dock monitoring tool