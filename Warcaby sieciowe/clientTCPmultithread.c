#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <fcntl.h> // for open
#include <unistd.h> // for close
#include<pthread.h>


#define RED 2
#define BLACK 3
 
void swapIJKL(int d[8][8], int i, int j, int k, int l)
{
    int temp;
    temp = d[i][j];
    d[i][j] = d[k][l];
    d[k][l] = temp;
}

int Playersturn(int d[][8], int player,int i,int j,int k,int l)
{
    int jmp_r;
    int jmp_c;
    if(i - k == -1 || i - k == 1){
        if(j - l == 1 || j - l == -1){
            swapIJKL(d,i,j,k,l);
            return 0;
        }
    }  
    if(i - k == -2 || i - k == 2){
        if(j - l == -2 || j - l == 2){
            if(i < k){ 
                jmp_r = i + 1;
            } else { 
                jmp_r = i - 1;
            }
            if(j < l){ 
                jmp_c = j + 1;
            } else { 
                jmp_c = j - 1;
            }
            
            d[jmp_r][jmp_c] = 1;
            swapIJKL(d,i,j,k,l);
            return 0;
        }
    }
    
} 

char value2symbol(int i) 
{
    switch(i)
    {
  	case 0:
            return ' ';
        case 1:
            return 'E';  
        case 2:
            return '$';
        case 3:
            return '@';     
    }
    return ('?');
}

void printDisplay(int d[][8])
{
    int rr, cc, pp;
    
    printf("  +---+---+---+---+---+---+---+---+\n");
    
    for (rr=0; rr<8; ++rr)
    {
        printf("%d |", rr+1);
        for (cc=0; cc<8; ++cc)
        {
            printf(" %c |", value2symbol(d[rr][cc]) );
        }
        printf("\n");
        printf("  +---+---+---+---+---+---+---+---+\n");
    }
    
    printf("    a   b   c   d   e   f   g   h\n");
}



int main(int argc,char*argv[]){
  const char* errorMsgs[12] = {"Move is correct!","i is out of bounds",
  "j is out of bound","k is out of bounds",
  "l is out of bounds","move your own piece!",
  "You must move to a empty location","RED player must move down",
  "BLACK player must move up","Enemy is not Black",
  "you can only jump over an enemy player","You can only move diagnally"};
  char gameNum[1000];
  char gameStarting[1000];
  char moveFrom[1000];
  char moveTo[1000];
  char moveRcv[1024];
  char errorNum[1024];
  char* IP=argv[1];
  int clientSocket;
  int playerNum;
  int errorNumI;
  int i,k;
  char j,l;
  int order;
  struct sockaddr_in serverAddr;
  socklen_t addr_size;
	int d[8][8]={
    {0,2,0,2,0,2,0,2},
    {2,0,2,0,2,0,2,0}, 
    {0,2,0,2,0,2,0,2}, 
    {1,0,1,0,1,0,1,0}, 
    {0,1,0,1,0,1,0,1}, 
    {3,0,3,0,3,0,3,0},
    {0,3,0,3,0,3,0,3},
	{3,0,3,0,3,0,3,0}};
  // Create the socket. 
  clientSocket = socket(PF_INET, SOCK_STREAM, 0);

  //Configure settings of the server address
 // Address family is Internet 
  serverAddr.sin_family = AF_INET;

  //Set port number, using htons function 
  serverAddr.sin_port = htons(1100);

 //Set IP address
  serverAddr.sin_addr.s_addr = inet_addr("172.17.142.214");
  memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);

  //Connect the socket to the server using the address
  addr_size = sizeof serverAddr;
  connect(clientSocket, (struct sockaddr *) &serverAddr, addr_size);

  printf("Choose number of game from 1-15\n");
  scanf("%s",gameNum);
  if( send(clientSocket , gameNum , strlen(gameNum) , 0) < 0)
  {
          printf("Send failed\n");
  }

  while(1)
  {
    if(recv(clientSocket, gameStarting, 1024, 0) < 0){
      sleep(1);
      continue;
    }
    else{
      if(!strcmp(gameStarting,"2")){
        printf("Game begins!\n");
        playerNum = 2; 
        break;
      }
      else if(!strcmp(gameStarting,"1")) {
        printf("Waiting for second player to join...\n");
        playerNum = 3;
      }
      else if(!strcmp(gameStarting,"3")){
        printf("Game is already playing!");
        printf("Choose another number of game from 1-15\n");
        scanf("%s",gameNum);
        if( send(clientSocket , gameNum , strlen(gameNum) , 0) < 0)
        {
                printf("Send failed\n");
        }
      }
    }
  }
  while(recv(clientSocket, gameStarting, 1024, 0) < 0){
    sleep(1);
    continue;
  }
  
  printDisplay(d);
  order = atoi(gameStarting);


  if(order == 1){ //second player starts
    while(1){
      while(recv(clientSocket, moveRcv, 1024, 0) < 0){
        sleep(1);
        continue;
      }
      if(atoi(moveRcv)==12){
        printf("Second player surrendered. You won!\n");
        exit(0);
      }
      if(atoi(moveRcv)==13){
        printf("Second player won. You lost!\n");
        exit(0);
      }
      if(atoi(moveRcv)==14){
        printf("Second player lost. You won!\n");
        exit(0);
      }
      i = moveRcv[0]-'0'; //ustawienie wartosci
      j = moveRcv[1];
      k = moveRcv[2]-'0';
      l = moveRcv[3];
      Playersturn(d, playerNum, i-1,j - 'a',k-1,l - 'a');
      printDisplay(d);
      printf("Move: %s ",moveRcv);


      while(1){
        printf("Give next move:");
        scanf("%s",moveFrom);
        if(!strcmp(moveFrom,"exit")){
          printf("You surrendered. The game ended.\n");
          send(clientSocket , moveFrom , strlen(moveFrom) , 0);
          exit(0);
        }
        printf("to: \n"); 
        scanf("%s",moveTo); 
        i = moveFrom[0]-'0'; //ustawienie wartosci
        j = moveFrom[1];
        k = moveTo[0]-'0';
        l = moveTo[1];          
        if( send(clientSocket , strcat(moveFrom,moveTo) , strlen(strcat(moveFrom,moveTo)) , 0) < 0)
        {
                printf("Send failed\n");
        }
        while(recv(clientSocket, errorNum, 1024, 0) < 0){
          sleep(1);
          continue;
        }
        if(atoi(errorNum) == 0){ //jeżeli ruch jest poprawny przejdź dalej
          printf("%s\n",errorMsgs[atoi(errorNum)]);
          Playersturn(d, playerNum, i-1,j - 'a',k-1,l - 'a');
          printDisplay(d);
          break;
        }
        if(atoi(errorNum)==13){
          printf("Second player won. You lost!\n");
          exit(0);
        }
        if(atoi(errorNum)==14){
          printf("Second player lost. You won!\n");
          exit(0);
        }
        printf("%s\n",errorMsgs[atoi(errorNum)]);
      }
    }
  } ///////////////// you start
  else if(order == 0){
    while(1){
      while(1){
        printf("Give next move:");
        scanf("%s",moveFrom);
        if(!strcmp(moveFrom,"exit")){
          printf("You surrendered. The game ended.\n");
          send(clientSocket , moveFrom , strlen(moveFrom) , 0);
          exit(0);
        }
        printf("to: \n"); 
        scanf("%s",moveTo); 
        i = moveFrom[0]-'0'; //ustawienie wartosci
        j = moveFrom[1];
        k = moveTo[0]-'0';
        l = moveTo[1];          
        if( send(clientSocket , strcat(moveFrom,moveTo) , strlen(strcat(moveFrom,moveTo)) , 0) < 0)
        {
                printf("Send failed\n");
        }
        while(recv(clientSocket, errorNum, 1024, 0) < 0){
          sleep(1);
          continue;
        }
        if(atoi(errorNum) == 0){ //jeżeli ruch jest poprawny przejdź dalej
          printf("%s\n",errorMsgs[atoi(errorNum)]);
          Playersturn(d, playerNum, i-1,j - 'a',k-1,l - 'a');
          printDisplay(d);
          break;
        }
        if(atoi(errorNum)==13){
          printf("Second player won. You lost!\n");
          exit(0);
        }
        if(atoi(errorNum)==14){
          printf("Second player lost. You won!\n");
          exit(0);
        }
        printf("%s\n",errorMsgs[atoi(errorNum)]);
      }

      while(recv(clientSocket, moveRcv, 1024, 0) < 0){
        sleep(1);
        continue;
      }
      if(atoi(moveRcv)==12){
        printf("Second player surrendered. You won!\n");
        exit(0);
      }
      if(atoi(moveRcv)==13){
        printf("Second player won. You lost!\n");
        exit(0);
      }
      if(atoi(moveRcv)==14){
        printf("Second player lost. You won!\n");
        exit(0);
      }
      i = moveRcv[0]-'0'; //ustawienie wartosci
      j = moveRcv[1];
      k = moveRcv[2]-'0';
      l = moveRcv[3];
      Playersturn(d, playerNum, i-1,j - 'a',k-1,l - 'a');
      printDisplay(d);
      printf("Move: %s ",moveRcv);

    }
  }
  

  close(clientSocket);
    
  return 0;
}
