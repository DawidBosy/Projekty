# Przetwarzanie równoległe
Programy dotyczące przetwarzania równoległego
# Kompilacja
nvcc main.cu -o main -arch=sm_50 \\
g++ main.cpp -o main.exe -fopenmp
# Uruchomienie
./main
./main.exe
