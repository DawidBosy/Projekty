#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<string.h>
#include <arpa/inet.h>
#include <fcntl.h> // for open
#include <unistd.h> // for close
#include<pthread.h>


#define ROWS 8
#define COLS 8
 
#define EMPTY 1
#define RED 2
#define BLACK 3
#define REDKING 4
#define BLACKKING 5
 
 
#define ISRED(c)  (c == RED || c == REDKING)
#define ISBLACK(c) (c == BLACK || c == BLACKKING))
#define ISEMPTY(c) (c == 1)

char client_message[2000];
char buffer[1024];
int playerColor[2]= {RED,BLACK};
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_t thread_id;
int gamepairs[16][2];
int gameStarts[16];
int winners[16];
int gameMove[0];
	int example[8][8]={
    {0,2,0,2,0,2,0,2},
    {2,0,2,0,2,0,2,0}, 
    {0,2,0,2,0,2,0,2}, 
    {1,0,1,0,1,0,1,0}, 
    {0,1,0,1,0,1,0,1}, 
    {3,0,3,0,3,0,3,0},
    {0,3,0,3,0,3,0,3},
	{3,0,3,0,3,0,3,0}};

int d[16][8][8]={    {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //1
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //2
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //3
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //4
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //5
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //6
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //7
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0},  
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //8
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //9
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //10
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //11
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //12
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //13
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //14
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}, //15
  {{0,2,0,2,0,2,0,2},    {2,0,2,0,2,0,2,0},     {0,2,0,2,0,2,0,2},     {1,0,1,0,1,0,1,0}, 
  {0,1,0,1,0,1,0,1},     {3,0,3,0,3,0,3,0},    {0,3,0,3,0,3,0,3},	{3,0,3,0,3,0,3,0}}}; //16 

 
 
void printDisplay(int d[][COLS]);
void swapIJKL(int d[ROWS][COLS], int i, int j, int k, int l);
int Playersturn(int d[][COLS], int player,int i,int j,int k,int l);

void clearPos(int d[][8]){
  for(int x =0;x< 8;x++){
    for(int y = 0;y < 8;y++){
      d[x][y] = example[x][y];
    }
  }  
}

int IsWinner(int d[][8]){
  int redInGame = 0;
  int blackInGame = 0;
  for(int x =0;x< 8;x++){
    for(int y = 0;y < 8;y++){
      if(d[x][y] == 2){
      redInGame = 1;
      break;
      }
    }
  }
  for(int x =0;x< 8;x++){
    for(int y = 0;y < 8;y++){
      if(d[x][y] == 3){
      blackInGame = 1;
      break;
      }
    }
  }
  if(blackInGame && redInGame)
  return 0;
  if(blackInGame && !redInGame)
  return 2;
  if(!blackInGame && redInGame)
  return 1;
}

void swapIJKL(int d[ROWS][COLS], int i, int j, int k, int l)
{
    int temp;
    temp = d[i][j];
    d[i][j] = d[k][l];
    d[k][l] = temp;
}
 
int Playersturn(int d[][COLS], int player,int i,int j,int k,int l)
{
    int jmp_r;
    int jmp_c;
    
    if(player == RED){
        printf("RED move from %d,%d to %d,%d\n", i, j, k, l);
    } else {
        printf("BLACK move from %d,%d to %d,%d\n", i, j, k, l);
    }
    
    if(i < 0 && ROWS <= i){ 
        printf("i is out of bounds\n");
        return 1;
    }
    if(j < 0 && COLS <= j){
        printf("j is out of bound");
        return 2;
    }
        
    if(k < 0 && ROWS <= k){
        printf("k is out of bounds");
        return 3;
        
    }
    if(l < 0 && COLS<= l){
        printf("l is out of bounds\n");
        return 4;
    }
        
    if(player == RED){
        if(d[i][j] != RED){
            printf("move your own piece!\n");
            return 5;
        }
    } else { 
        if(d[i][j] != BLACK){
            printf("move your own piece!\n");
            return 5;
        }
    }
    
    if(d[k][l] != EMPTY){
        printf("You must move to a empty location");
        return 6;
    }
    
    
    if(player == RED){
        if(i >= k){
            printf("RED player must move down\n");
            return 7;
        }
    } else { 
        if(i <= k){
            printf("BLACK player must move up\n");   
            return 8;
        }
    }
    
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
            
            if(player==RED && d[jmp_r][jmp_c]!=BLACK)
            {
                printf("Enemy is not Black at %d%d",jmp_r, jmp_c);
                return 9;
            }
            if(player==BLACK && d[jmp_r][jmp_c] != RED){
                printf("you can only jump over an enemy player\n");
                return 10;
            }

            d[jmp_r][jmp_c] = 1;
            swapIJKL(d,i,j,k,l);
            return 0;
        }
    }
    
    printf("You can only move diagnally\n");
    return 11;
    
}

int findGameNumber(int SocketNumber){
  for(int x = 0;x<16;x++){
    if(SocketNumber == gamepairs[x][0] || SocketNumber == gamepairs[x][1]){
      return x;
    }
    else{
      continue;
    }
  }
  return -1;
}


int findPlayerNumber(int SocketNumber){
  for(int x = 0;x<16;x++){
    if(SocketNumber == gamepairs[x][0]){
      return 0;
    }
    else if(SocketNumber == gamepairs[x][1]){
      return 1;
    }
    else{
      continue;
    }
  }
  return -1;
}

void * socketThread(void *arg)
{
  int newSocket = *((int *)arg);
  int n;
  int game = findGameNumber(newSocket);
  int i,k,moveCorrect;
  char j,l;
  char moveCorrectCH[10];
  while(1){
  n=recv(newSocket , client_message , 2000 , 0); //odbierz numer rozgrywki
    if(n > 0){
      game = atoi(client_message);
      if(gamepairs[game][0]!= 0 && gamepairs[game][1] != 0){ //jezeli rozgrywka jest zajeta
        send(newSocket,"3",sizeof("3"),0);
        continue;
      }
      else if(gamepairs[game][0] != 0 && gamepairs[game][1] == 0){ //jezeli 1 gracz juz dolaczyl
        gamepairs[game][1] = newSocket;
        printf("Uzytkownik dolaczyl do rozgrywki nr %s\n",client_message);
        printf("Game begins!\n");
        send(newSocket,"2",sizeof("2"),0);
        send(gamepairs[game][0],"2",sizeof("2"),0);
        send(newSocket,"1",sizeof("1"),0);
        send(gamepairs[game][0],"0",sizeof("0"),0);
        gameStarts[game] = 1;
        winners[game]=0;
        break;
      }
      else if(gamepairs[game][0] == 0){ //jezeli nikogo jeszcze nie ma
        clearPos(d[game]);
        gamepairs[game][0] = newSocket;
        printf("Uzytkownik dolaczyl do rozgrywki nr %s\n",client_message);
        printf("Waiting for second player to join...\n");
        send(newSocket,"1",sizeof("1"),0);
        while(gamepairs[game][1]==0){
          sleep(1);
          continue;
        }
        break;
      }
    }
  }
  while(gameStarts[game]==0){
    sleep(1);
    continue;
  }
  while(winners[game]==0){
    int player = findPlayerNumber(newSocket);
    while(player != gameMove[game]){
      sleep(1);
      continue;
    }

    while(1){
      while( n=recv(newSocket , client_message , 2000 , 0) < 0 && winners[game]==0){ //odebranie ruchu
        sleep(1);
        continue;
      } 
      if(!strcmp(client_message,"exit")){
        printf("Gracz opuścił rozgrywkę\n");
        send(gamepairs[game][abs(player-1)],"12",sizeof("12"),0); // gracz opuścił grę
        gamepairs[game][0] = 0;
        gamepairs[game][1]=0;
        winners[game] = abs(player-1)+1;
        clearPos(d[game]);
        memset(&client_message, 0, sizeof (client_message));
        printf("Exit socketThread \n");

        pthread_exit(NULL);
      }
      if(gamepairs[game][0] == 0 || gamepairs[game][1]==0){
        printf("Exit socketThread \n");

        pthread_exit(NULL);
      }

      i = client_message[0]-'0'; //ustawienie wartosci
      j = client_message[1];
      k = client_message[2]-'0';
      l = client_message[3];
      printf("%d\n",playerColor[player]);
      moveCorrect = Playersturn(d[game], playerColor[player], i-1,j - 'a',k-1,l - 'a');
      sprintf(moveCorrectCH,"%d",moveCorrect); 
      printf("Error: %s\n",moveCorrectCH);
      
      if(moveCorrect == 0){ //jezeli ruch byl poprawny
        winners[game] = IsWinner(d[game]);
        if(winners[game] != 0){
          if(winners[game] == 1){
            send(gamepairs[game][0],"14",sizeof("14"),0); //odsyłanie wiadomości
            send(gamepairs[game][1],"13",sizeof("13"),0); //odsyłanie wiadomości
          }
          else if(winners[game]==2){
            send(gamepairs[game][1],"14",sizeof("14"),0); //odsyłanie wiadomości
            send(gamepairs[game][0],"13",sizeof("13"),0); //odsyłanie wiadomości
          }
          gamepairs[game][0] = 0;
          gamepairs[game][1]=0;
          memset(&client_message, 0, sizeof (client_message));
          printf("Exit socketThread \n");

          pthread_exit(NULL);
        }
        
        char *message = malloc(sizeof(client_message)); 
        strcpy(message,client_message);

        send(gamepairs[game][abs(player-1)],message,sizeof(message),0); //odsyłanie wiadomości
        memset(&client_message, 0, sizeof (client_message));
        gameMove[game] = abs(gameMove[game]-1);
      }
      winners[game] = IsWinner(d[game]);
      if(winners[game]!= 0){
        memset(&client_message, 0, sizeof (client_message));
        printf("Exit socketThread \n");
        
        pthread_exit(NULL);        
      }
      send(gamepairs[game][player],moveCorrectCH,sizeof(moveCorrectCH),0); //odsyłanie wiadomości czy ruch był poprawny

      
    }
    printf("Exit socketThread \n");

    pthread_exit(NULL);


    }
  printf("Exit socketThread \n");

  pthread_exit(NULL);
  
}

int main(){
  int serverSocket, newSocket;
  struct sockaddr_in serverAddr;
  struct sockaddr_storage serverStorage;
  socklen_t addr_size;
  int r,c;
	int pr, pb;
	int i, k;
	char j, l;
  for(int x =0;x<16;x++){
    gameStarts[x] = 0;
    winners[x]=-1;
    gameMove[x] = 0;
  }


  
  //Create the socket. 
  serverSocket = socket(PF_INET, SOCK_STREAM, 0);

  // Configure settings of the server address struct
  // Address family = Internet 
  serverAddr.sin_family = AF_INET;

  //Set port number, using htons function to use proper byte order 
  serverAddr.sin_port = htons(1100);

  //Set IP address to localhost 
  serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);


  //Set all bits of the padding field to 0 
  memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);

  //Bind the address struct to the socket 
  bind(serverSocket, (struct sockaddr *) &serverAddr, sizeof(serverAddr));

  //Listen on the socket
  if(listen(serverSocket,50)==0)
    printf("Listening\n");
  else
    printf("Error\n");
    pthread_t thread_id;

    while(1)
    {
        //Accept call creates a new socket for the incoming connection
        addr_size = sizeof serverStorage;
        newSocket = accept(serverSocket, (struct sockaddr *) &serverStorage, &addr_size);

        if( pthread_create(&thread_id, NULL, socketThread, &newSocket) != 0 )
           printf("Failed to create thread\n");

        printf("Thread id:%ld\n",thread_id);
        pthread_detach(thread_id);
        //pthread_join(thread_id,NULL);
    }
  return 0;
}
