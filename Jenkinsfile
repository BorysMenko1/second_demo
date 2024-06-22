pipeline {
  agent any
  environment {
    GIT_COMMIT_HASH        = sh (script: "git log -n 1 --pretty=format:'%H'", returnStdout: true)
    DISCOR_WEBHOOK_URL     = credentials('DISCORD_WEBHOOK')
  }
  stages {
    stage('Setup Build') {
        steps {
            script {
                git_commit  = sh(script: "git rev-parse --short refs/remotes/${GIT_BRANCH}", returnStdout: true).trim()
                
                if (env.BRANCH_NAME == 'main') {
                    BUILD_PARENT = "flask-app-${git_commit}"
                } else {
                    BUILD_PARENT = "PR-${git_commit}"
                }
                currentBuild.displayName = BUILD_PARENT
            }
        }
    }
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
    stage('SonarQube Analysis') {
            steps {
                // Run SonarQube analysis for Python
                script {
                    def scannerHome = tool name: 'sq1'
                    withSonarQubeEnv('sq1') {
                        sh "echo $pwd"
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
            }
            }  
    }
    stage("Quality Gate") {
      steps {
        timeout(time: 2, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }
    // stage('manual gate') {
    //   steps {
    //     input(message: "Do you want to deploy the application?", ok: "Yes!")
    //   }
    // }
    // stage('publish docker image') {
    //   steps {
    //     withCredentials([string(credentialsId: 'ECR_URI', variable: 'ECR_URI'), string(credentialsId: 'REGION', variable: 'REGION')]) {
    //       sh '''
    //         aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECR_URI}
    //         docker tag ecr-repo:latest ${ECR_URI}/ecr-repo:latest
    //         docker tag ecr-repo:$GIT_COMMIT_HASH ${ECR_URI}/ecr-repo:$GIT_COMMIT_HASH
    //         docker push ${ECR_URI}/ecr-repo:latest
    //         docker push ${ECR_URI}/ecr-repo:$GIT_COMMIT_HASH
    //       '''
    //     }
    //   }
    // }
    // stage('restart ecs task') {
    //   steps {
    //     withCredentials([string(credentialsId: 'ECS_CLUSTER_NAME', variable: 'ECS_CLUSTER_NAME'), string(credentialsId: 'ECS_SERVICE_NAME', variable: 'ECS_SERVICE_NAME'), string(credentialsId: 'TASK_DEFINITION', variable: 'TASK_DEFINITION')]) {
    //       sh '''
    //         aws ecs update-service --cluster ${ECS_CLUSTER_NAME} --service ${ECS_SERVICE_NAME} --task-definition ${TASK_DEFINITION} --force-new-deployment
    //       '''
    //     }
    //   }
    // }
  }
  post {
    success {
        script {
            discordSend description: "Jenkins Pipeline Build", footer: "Build ${BUILD_PARENT} Passed", link: env.BUILD_URL, result: currentBuild.currentResult, title: JOB_NAME, webhookURL: "${DISCOR_WEBHOOK_URL}"
        }
    }
    failure {
        script {
            discordSend description: "Jenkins Pipeline Build", footer: "Build ${BUILD_PARENT} Failed", link: env.BUILD_URL, result: currentBuild.currentResult, title: JOB_NAME, webhookURL: "${DISCOR_WEBHOOK_URL}"
        }
        
    }
     
      
  }        
}
