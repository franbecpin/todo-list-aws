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
        
        stage('Security'){
            steps{
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh'''
                        /snap/bin/bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}"                        
                    '''
                    

                }   
            }
        }
    }
}

