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
                    bat'''
                     #  bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}"                        
                    '''
                    #recordIssues aggregatingResults: true, enabledForFailure: true, qualityGates: [[integerThreshold: 2, threshold: 2.0, type: 'TOTAL'], [criticality: 'ERROR', integerThreshold: 4, threshold: 4.0, type: 'TOTAL']], sourceCodeRetention: 'LAST_BUILD', tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')]

                }   
            }
        }
    }
}

