pipeline 
{
    agent any

    stages 
    {
        stage('Get Code') 
        {
            steps 
            {
                deleteDir()
                git branch: "develop", url: "https://github.com/franbecpin/todo-list-aws.git"                
            }
        } 
        
        stage ('Static Test')
        {
            steps
            {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') 
                {
                    sh'''
                        export PYTHONPATH="$WORKSPACE/src"
                        # Formato pylint (útil si ya usas pyLint(...) en Jenkins)
                        flake8 --format=pylint --exit-zero --verbose src > flake8.out 2>&1
                    '''
                    recordIssues sourceCodeRetention: 'LAST_BUILD', tools: [flake8(pattern: 'flake8.out')]
                    

                }
            }
        }
        
        stage('Security') 
        {
            steps 
            {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') 
                {

                    sh '''#!/bin/bash
                    set -euxo pipefail
    
                    # Crear entorno virtual aislado en el workspace
                    python3 -m venv .venv
    
                    # Activar el entorno virtual
                    source .venv/bin/activate
    
                    # Actualizar pip dentro del venv (esto NO afecta al sistema)
                    pip install --upgrade pip
    
                    # Instalar Bandit dentro del venv
                    pip install bandit
    
                    # Ejecutar Bandit desde el venv
                    bandit --exit-zero -r --verbose src . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}" 
                    '''
    
                    recordIssues(sourceCodeRetention: 'LAST_BUILD',  tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')])
                }
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
                        # sam deploy --guided
                        sam deploy --config-file samconfig.toml --no-confirm-changeset --no-fail-on-empty-changeset
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
                        def BASE_URL = sh( script: "aws cloudformation describe-stacks --stack-name todo-list-aws --query 'Stacks[0].Outputs[?OutputKey==`BaseUrlApi`].OutputValue' --region us-east-1 --output text",
                            returnStdout: true)
                        echo "$BASE_URL"
                        echo 'Initiating Integration Tests'
                        
                        // Ejecutar pytest con BASE_URL exportada al entorno
                        withEnv(["BASE_URL=${BASE_URL}"]) {
                            sh "pytest test/integration/todoApiTest.py -v --junitxml=pytest.xml"
                        }

                    }
                }
            }    
        }
        
    }
}

