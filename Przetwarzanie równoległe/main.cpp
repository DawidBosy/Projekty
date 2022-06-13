
#include <iostream>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>
#include <vector>
using namespace std;
 
bool isSubsetSum(vector<int> set, int n, int sum)
{
    if (sum == 0)
        return true;
    if (n == 0)
        return false;
 
    if (set[n - 1] > sum)
        return isSubsetSum(set, n - 1, sum);
 
    return isSubsetSum(set, n - 1, sum)
           || isSubsetSum(set, n - 1, sum - set[n - 1]);
}

int SequenceRun(int iterations, int arrayLength,vector<int> numbers){
    int x,i,n;
    
    
    int startTime = time(NULL);
    for(i = 0;i<iterations;i++){      
        for(x = 0;x<arrayLength;x++){
            numbers.push_back(rand()%50);
        }
        n = sizeof(numbers) / sizeof(numbers[0]);
        isSubsetSum(numbers,n,rand()%50+50);
    }
    
    int endTime = time(NULL);
    return endTime - startTime;
}


int ParallelRun(int iterations, int arrayLength,vector<int> numbers,int threads){
    int x,i,n;
    omp_set_num_threads(threads);

    int startTime = time(NULL);
    #pragma omp parallel for shared(iterations,arrayLength) private(i,x,numbers)
    for(i = 0;i<iterations;i++){      
        for(x = 0;x<arrayLength;x++){
            numbers.push_back(rand()%50);
        }
        n = sizeof(numbers) / sizeof(numbers[0]);
        isSubsetSum(numbers,n,rand()%50+50);
    }
    int endTime = time(NULL);
    return endTime - startTime;
}
 
// Driver Code
int main()
{
    vector<int> numbers = {};
    
    int problemNum = 5000;
    int arrayLength = 50;
    srand(time(NULL));

    cout << "Seconds passed in sequence run: " << SequenceRun(problemNum,arrayLength,numbers) << "\n";

    cout << "Seconds passed in parallel run with 2 threads: " << ParallelRun(problemNum,arrayLength,numbers,2) << "\n";

    cout << "Seconds passed in parallel run with 4 threads: " << ParallelRun(problemNum,arrayLength,numbers,4) << "\n";

    cout << "Seconds passed in parallel run with 8 threads: " << ParallelRun(problemNum,arrayLength,numbers,8) << "\n";
    
    cout << "Seconds passed in parallel run with 16 threads: " << ParallelRun(problemNum,arrayLength,numbers,16) << "\n";

 
    return 0;
}