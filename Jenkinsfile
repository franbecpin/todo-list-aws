pipeline 
{
    agent any
    
    options { skipDefaultCheckout() }

    stages 
    {
        stage('Get Code') 
        {
            steps 
            {
                deleteDir()
                git branch: "main", url: "https://github.com/franbecpin/todo-list-aws.git"                
            }
        } 
        
       
        stage('Deploy')
        {
            steps
            {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE')
                {
                    sh '''
                        sam build
                        sam validate --region us-east-1 
                        # desplegando segun la configuracion para production de samconfig.toml
                        sam deploy --config-file samconfig.toml --config-env production --resolve-s3 --no-confirm-changeset --no-fail-on-empty-changeset
                        
                        '''
                }
            }
        }
        
        stage('Rest Test'){
         steps
            {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE')
                {
                    script {
                        def BASE_URL = sh( script: "aws cloudformation describe-stacks --stack-name todo-list-aws-production --query 'Stacks[0].Outputs[?OutputKey==`BaseUrlApi`].OutputValue' --region us-east-1 --output text",
                            returnStdout: true)
                        echo "$BASE_URL"
                        echo 'Initiating Rest Tests'
                        
                        // Ejecutar pytest con BASE_URL exportada al entorno
                        withEnv(["BASE_URL=${BASE_URL}"]) {
                            sh '''
                                set -x
                                export PYTHONPATH="$WORKSPACE"
                                # pytest test/integration/todoApiTest.py -v --junitxml=pytest.xml
                                # pytest test/integration/todoApiTest.py -v --junitxml=pytest.xml -m 'not destructive'
                                # pytest test/integration/todoApiTest.py --co -q --junitxml=pytest.xml -m
                                pytest test/integration/todoApiTest.py -v --junitxml=pytest.xml -k "not addtodo and not updatetodo and not deletetodo and not listtodos"
                                
                            '''
                        }

                    }
                    
                }
            }    
        }
        
            
        
    }
}

