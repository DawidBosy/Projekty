
#include <iostream>
#include <string.h>
#include <time.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include <curand_kernel.h>

__host__ __device__ bool isSubsetSum(int* set, int n, int sum)
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

__global__ void CudaRun(int iterations, int arrayLength,int* numbers,float * result){
    int x,i,n;
    curandState state;
    curand_init(1234,0,0,&state);
    
    clock_t startTime = clock();
    for(i = 0;i<iterations;i++){      
        for(x = 0;x<arrayLength;x++){
            numbers[x] = (int)(ceil((curand_uniform(&state)*(50 + 1))) - 1);
        }
        n = sizeof(numbers) / sizeof(numbers[0]);
        isSubsetSum(numbers,n,(int)(ceil((curand_uniform(&state)*(50 + 1))) - 1)+50);
    }
    
    clock_t endTime = clock();
    *result = (float)(endTime - startTime);
}

int main(){
    
    int problemNum = 6000;
    int arrayLength = 50;
    float result;
    srand(time(NULL));
    int startTime = time(NULL);

    int *numbers;
    int *d_numbers;
    float * d_result;

    // Allocate host memory
    numbers   = (int*)malloc(sizeof(int) * arrayLength);

    cudaMalloc((void**)&d_numbers, sizeof(int)*arrayLength);
    cudaMalloc((void**)&d_result,sizeof(float));



    // Transfer data from host to device memory
    cudaMemcpy(d_numbers, &numbers, sizeof(int)*arrayLength, cudaMemcpyHostToDevice);

    // Executing kernel 
    CudaRun<<<1,1>>>(problemNum,arrayLength,d_numbers,d_result);
    
    // Transfer data back to host memory
    cudaMemcpy(&result, d_result, sizeof(float), cudaMemcpyDeviceToHost);

    printf("Seconds passed in sequence run: %f \n",(double)result/(double)CLOCKS_PER_SEC);

    // Deallocate device memory
    cudaFree(d_result);
    cudaFree(d_numbers);

    // Deallocate host memory
    free(numbers); 
}
