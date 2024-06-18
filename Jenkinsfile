pipeline {
  agent {label 'Jenkins-Slave'}
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
        input(message: "Do you want to deploy the application?", ok: "Yes!")
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
        withCredentials([string(credentialsId: 'ECS_CLUSTER_NAME', variable: 'ECS_CLUSTER_NAME'), string(credentialsId: 'ECS_SERVICE_NAME', variable: 'ECS_SERVICE_NAME'), string(credentialsId: 'TASK_DEFINITION', variable: 'TASK_DEFINITION')]) {
          sh '''
            aws ecs update-service --cluster ${ECS_CLUSTER_NAME} --service ${ECS_SERVICE_NAME} --task-definition ${TASK_DEFINITION} --force-new-deployment
          '''
        }
      }
    }
  }
}
