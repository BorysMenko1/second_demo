pipeline {
    agent {label 'jenkins-slave'}
    environment {
        GIT_COMMIT_HASH = sh (script: "git log -n 1 --pretty=format:'%H'", returnStdout: true)
    }
    stages {
        stage('Build') {
            steps {
                sh '''
                sudo docker build -t ecr-repo:latest -t ecr-repo:$GIT_COMMIT_HASH .
                sudo docker rm $(docker ps -aq) 2>/dev/null || true
                sudo docker images -f "dangling=true" -q | xargs -r docker rmi --force
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
                // docker build -t ecr-repo:latest -t ecr-repo:$GIT_COMMIT_HASH .
                // docker rm $(docker ps -aq) 2>/dev/null || true
                // docker images -f "dangling=true" -q | xargs -r docker rmi --force
                // build docker image   --multi stage build --lpain // image size should be small
                withCredentials([string(credentialsId: 'ECR_URI', variable: 'ECR_URI'), string(credentialsId: 'REGION', variable: 'REGION')]) {
                    sh 'aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECR_URI}'
                    sh 'docker tag ecr-repo:latest ${ECR_URI}/ecr-repo:latest'
                    // sh 'docker tag ecr-repo:$GIT_COMMIT_HASH ${ECR_URI}/ecr-repo:$GIT_COMMIT_HASH'
                    sh 'docker push ${ECR_URI}/ecr-repo:latest'
                    // sh 'docker push ${ECR_URI}/ecr-repo:$GIT_COMMIT_HASH'
            }
            }
        }
        // stage('publish docker'){
        //     steps{
        //         // github docker registry // run at ECS
        //     }
        // }
        // stage('deploy') {
        //     steps {
        //      script {
        //         sshPublisher(
        //         continueOnError: false, failOnError: true,
        //         publishers: [
        //             sshPublisherDesc(
        //             configName: "app_server",
        //             transfers: [    
        //             sshTransfer(
        //                 cleanRemote: true,
        //                 remoteDirectory: '/application',
        //                 sourceFiles: '**/*.zip'
        //             ),
        //             sshTransfer(
        //                 execCommand: "cd application/ && unzip app_${BUILD_NUMBER}.zip"
        //             ),
        //             sshTransfer(
        //                 execCommand: "nohup python3 -u application/main.py </dev/null &>/dev/null & disown -h %1"
        //             )
        //             ])
        //         ])
        //         }
        //         }
        //     }
        }
    }
    // data dock monitoring tool