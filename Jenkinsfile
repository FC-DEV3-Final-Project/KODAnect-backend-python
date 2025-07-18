pipeline {
    agent any

    environment {
        DOCKER_USER = credentials('docker-user')
        DOCKER_PASS = credentials('docker-pass')
        SERVER_HOST = credentials('server-host')
        SLACK_TOKEN = credentials('slack-token')
        IMAGE_NAME = 'kodanect'

        CI_FAILED = 'false'
        CD_FAILED = 'false'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    githubNotify context: 'checkout', status: 'PENDING', description: '코드 체크아웃 중...'
                    catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                        checkout scm
                    }
                    if (currentBuild.currentResult == 'FAILURE') {
                        githubNotify context: 'checkout', status: 'FAILURE', description: '체크아웃 실패'
                        env.CI_FAILED = 'true'
                        error('Checkout 실패')
                    } else {
                        githubNotify context: 'checkout', status: 'SUCCESS', description: '체크아웃 완료'
                    }
                }
            }
        }

        stage('Docker Build & Push') {
            when {
                branch 'main'
            }
            steps {
                script {
                    imageTag = "build-python-${new Date().format('yyyyMMdd-HHmm')}"
                    fullImage = "docker.io/${DOCKER_USER}/${IMAGE_NAME}:${imageTag}"

                    githubNotify context: 'docker', status: 'PENDING', description: "도커 이미지 빌드 중... [${imageTag}]"

                    catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                        sh "docker build -t ${fullImage} ."
                        sh """
                            echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
                            docker push ${fullImage}
                        """
                    }

                    if (currentBuild.currentResult == 'FAILURE') {
                        githubNotify context: 'docker', status: 'FAILURE', description: '도커 푸시 실패'
                        env.CD_FAILED = 'true'
                        error('Docker Build & Push 실패')
                    } else {
                        githubNotify context: 'docker', status: 'SUCCESS', description: "도커 이미지 푸시 완료 [${imageTag}]"
                    }
                }
            }
        }

        stage('Deploy to Server') {
            when {
                branch 'main'
            }
            steps {
                script {
                    githubNotify context: 'deploy', status: 'PENDING', description: '서버에 배포 중...'

                    withCredentials([
                        string(credentialsId: 'upstage-api-key', variable: 'UPSTAGE_API_KEY'),
                        string(credentialsId: 'db-host', variable: 'DB_HOST'),
                        string(credentialsId: 'db-port', variable: 'DB_PORT'),
                        string(credentialsId: 'db-name', variable: 'DB_NAME'),
                        string(credentialsId: 'db-username', variable: 'DB_USERNAME'),
                        string(credentialsId: 'db-password', variable: 'DB_PASSWORD'),
                        string(credentialsId: 'github-token-string', variable: 'GITHUB_TOKEN'),
                        usernamePassword(credentialsId: 'server-ssh-login', usernameVariable: 'SSH_USER', passwordVariable: 'SSH_PASS')
                    ]) {
                        sh """
                            cat > .env <<EOF
UPSTAGE_API_KEY=${UPSTAGE_API_KEY}
DB_HOST=${DB_HOST}
DB_PORT=${DB_PORT}
DB_NAME=${DB_NAME}
DB_USERNAME=${DB_USERNAME}
DB_PASSWORD=${DB_PASSWORD}
DOCKER_USER=${DOCKER_USER}
DOCKER_PASS=${DOCKER_PASS}
IMAGE_TAG=${imageTag}
EOF

                            sshpass -p "\$SSH_PASS" ssh -o StrictHostKeyChecking=no \$SSH_USER@${SERVER_HOST} '
                                set -e
                                
                                mkdir -p /root/docker-compose-python-prod

                                if [ ! -d /root/docker-compose-python-prod/.git ]; then
                                    rm -rf /root/docker-compose-python-prod
                                    git clone https://github.com/FC-DEV3-Final-Project/KODAnect-backend-python.git /root/docker-compose-python-prod
                                else
                                    cd /root/docker-compose-python-prod && git pull --no-rebase
                                fi
                            '

                            sshpass -p "\$SSH_PASS" scp -o StrictHostKeyChecking=no .env \$SSH_USER@${SERVER_HOST}:/root/docker-compose-python-prod/.env

                            sshpass -p "\$SSH_PASS" ssh -o StrictHostKeyChecking=no \$SSH_USER@${SERVER_HOST} '
                                set -e
                                cd /root/docker-compose-python-prod
                                set -a && . .env && set +a

                                echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
                                docker-compose -f docker-compose.prod.yml pull
                                docker-compose -f docker-compose.prod.yml up -d
                                rm -f .env
                            '

                            rm -f .env
                        """

                        githubNotify context: 'deploy', status: 'SUCCESS', description: "배포 완료 [${imageTag}]"

                        sh """
                            export GITHUB_TOKEN=${GITHUB_TOKEN}
                            gh release create ${imageTag} \\
                              --repo FC-DEV3-Final-Project/KODAnect-backend-python \\
                              --title "Release ${imageTag}" \\
                              --notes "이미지: ${fullImage}"
                        """
                    }

                    if (currentBuild.currentResult == 'FAILURE') {
                        githubNotify context: 'deploy', status: 'FAILURE', description: '배포 실패'
                        env.CD_FAILED = 'true'
                        error('배포 실패')
                    }
                }
            }
        }

//         stage('Health Check') {
//             when {
//                 branch 'main'
//             }
//             steps {
//                 script {
//                     githubNotify context: 'healthcheck', status: 'PENDING', description: '헬스체크 중...'
//
//                     def healthCheckUrl = "http://${SERVER_HOST}:8000/health"
//                     def retries = 3
//                     def success = false
//
//                     for (int i = 0; i < retries; i++) {
//                         def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' ${healthCheckUrl}", returnStdout: true).trim()
//                         if (response == '200') {
//                             success = true
//                             break
//                         }
//                         sleep(5)
//                     }
//
//                     if (success) {
//                         githubNotify context: 'healthcheck', status: 'SUCCESS', description: '헬스체크 성공'
//                     } else {
//                         githubNotify context: 'healthcheck', status: 'FAILURE', description: '헬스체크 실패'
//                         env.CD_FAILED = 'true'
//                         error('Health check failed')
//                     }
//                 }
//             }
//         }
    }

    post {
        success {
            script {
                if (env.CHANGE_ID != null || env.BRANCH_NAME?.trim() == 'main') {
                    slackSend(
                        channel: '4_파이널프로젝트_1조_jenkins',
                        color: 'good',
                        token: SLACK_TOKEN,
                        message: "빌드 성공: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|바로가기>)"
                    )
                    if (env.BRANCH_NAME == 'main') {
                        slackSend(
                            channel: '4_파이널프로젝트_1조_jenkins',
                            color: 'good',
                            token: SLACK_TOKEN,
                            message: "배포 성공: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|바로가기>)"
                        )
                    }
                }
            }
        }

        failure {
            script {
                if (env.CHANGE_ID != null || env.BRANCH_NAME?.trim() == 'main') {
                    slackSend(
                        channel: '4_파이널프로젝트_1조_jenkins',
                        color: 'danger',
                        token: SLACK_TOKEN,
                        message: "빌드 실패: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|바로가기>)"
                    )
                    if (env.BRANCH_NAME == 'main') {
                        slackSend(
                            channel: '4_파이널프로젝트_1조_jenkins',
                            color: 'danger',
                            token: SLACK_TOKEN,
                            message: "배포 실패: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|바로가기>)"
                        )
                    }
                }
            }
        }
    }
}
