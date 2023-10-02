pipeline {
    agent {label 'jenkins-slave'}
    stages {
        stage('Build') {
            steps {
                sh 'pip3 install --no-cache-dir -r requirements.txt'
            }
        }
        stage('test') {
            steps {
                sh 'python3.8 -m pytest tests/test_project.py'
            }
        }
        // stage('manual gate') {
        //     steps {
        //         input(message: "Do you want deploy application?", ok: "Yes!")
        //     }
        // }
        // stage('artifact') {
        //     steps {
        //         // build docker image   --multi stage build --lpain // image size should be small

        //         // sh "rm -r ${WORKSPACE}/*.zip"
        //         // zip dir:"$WORKSPACE", exclude: '' , glob: '', zipFile: "${WORKSPACE}/app_${BUILD_NUMBER}.zip", overwrite: true
        //         // sh "aws s3 cp ${WORKSPACE}/app_${BUILD_NUMBER}.zip s3://myflaskappbucket1"
        //     }
        // }
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