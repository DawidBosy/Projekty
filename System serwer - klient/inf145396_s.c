#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/shm.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include <signal.h>
#define MAIN 1001

int main(){

struct msgbuf{
    long type;
    char msg[1024];
}name,ident,types, comunicate, newtyp,wrongN,wrongI, subscript,rcvWay;



int shmIdent;
char (*idents)[1024];
shmIdent = shmget(IPC_PRIVATE,sizeof(char[16][1024]),0600|IPC_CREAT);
idents = shmat(shmIdent,NULL,0); //imiona
for(int x =0;x<16;x++){
                strcpy(idents[x]," ");
}



int shmName;
char (*names)[1024];
shmName = shmget(IPC_PRIVATE,sizeof(char[16][1024]),0600|IPC_CREAT);
names = shmat(shmName,NULL,0); //imiona
for(int x =0;x<16;x++){
                strcpy(names[x]," ");
}


int *accountsNum;


int shmmsgTypesCounter = shmget(IPC_PRIVATE,sizeof(int),0600|IPC_CREAT);
int *msgTypesCounter;
msgTypesCounter = (int*)shmat(shmmsgTypesCounter,NULL,0);
*msgTypesCounter = 0;


int existalready = 0;
int currentType = 0;

int memory = shmget(IPC_PRIVATE,sizeof(int),0600|IPC_CREAT);
accountsNum = (int*)shmat(memory,NULL,0);
*accountsNum = 0;


int *NumOfAccounts;
int shmNumOfAccounts = shmget(IPC_PRIVATE,sizeof(int),0600|IPC_CREAT);
NumOfAccounts = (int*)shmat(shmNumOfAccounts,NULL,0);
*NumOfAccounts = 0;

int shmtypeExist = shmget(IPC_PRIVATE,sizeof(int),0600|IPC_CREAT);
int *typeExist;
typeExist = (int*)shmat(shmtypeExist,NULL,0);
*typeExist = 0;




int shmBuild;
int (*msgTypesSubs)[20];
shmBuild = shmget(IPC_PRIVATE,sizeof(int[16][21]),0600|IPC_CREAT);
msgTypesSubs = shmat(shmBuild,NULL,0); //informacje o subskrybentach kanalow
for(int x =0;x<16;x++){
        for(int y = 0;y<21;y++){
                msgTypesSubs[x][y] = 0;
        }
}


int shmclientChannels = shmget(IPC_PRIVATE,sizeof(int)*16,0600|IPC_CREAT);
int *clientChannels = (int*)shmat(shmclientChannels,NULL,0); //numery kanalow


int shmrcvChannels = shmget(IPC_PRIVATE,sizeof(int)*16,0600|IPC_CREAT);
int *rcvChannels = (int*)shmat(shmrcvChannels,NULL,0);




int shmChanOpen = shmget(IPC_PRIVATE,sizeof(int)*20,0600|IPC_CREAT);
int *ChanOpen = (int*)shmat(shmChanOpen,NULL,0);
for(int x =0;x<20;x++){
        ChanOpen[x]=0;
}


int (*rcvWays)[20];
int shmRcvWays = shmget(IPC_PRIVATE,sizeof(int[16][21]),0600|IPC_CREAT);
rcvWays = shmat(shmRcvWays,NULL,0); //subskrypcja synch lub asynch kanalu x dla typu y
for(int x =0;x<16;x++){
        for(int y = 0;y<21;y++){
                rcvWays[x][y] = 0;
        }
}



int shmAddTypeOpen = shmget(IPC_PRIVATE,sizeof(int)*20,0600|IPC_CREAT);
int *AddTypeOpen = (int*)shmat(shmAddTypeOpen,NULL,0);
for(int x = 0;x<20;x++){
        AddTypeOpen[x] = 0;
}



int shmmsgTypes = shmget(IPC_PRIVATE,sizeof(int)*21,0600|IPC_CREAT);
int *msgTypes = (int*)shmat(shmmsgTypes,NULL,0); //typy wiadomosci

char typeComment[64] = "Utworzono nowy typ wiadomosci:";

int wrongname = 1;
int wrongident = 1;
int trialChannel;
int trialRcvChannel;

int proces1;
int proces2;
int proces3;

    int mid = msgget(MAIN, 0600 | IPC_CREAT);
    proces1 = fork();
    if(proces1 == 0){

        while(1){
                for(int x =0;x<16;x++){
                        if(strcmp(names[x]," ") == 0){
                                *accountsNum = x;
                                break;
                        }
                }
                msgrcv(mid, &name, 1024, 1, 0);
                while(wrongname ==1){
                        for(int i = 0;i<16;i++){
                                if (strcmp(name.msg,names[i])==0){
                                        wrongname = 1;
                                        break;
                                }
                                else{
                                        wrongname = 0;
                                }
                        }
                        if (wrongname == 1){
                                printf("Czekam na nowa nazwe...\n");
                                strcpy(wrongN.msg,"-1");
                                wrongN.type = 4;
                                msgsnd(mid,&wrongN,strlen(wrongN.msg)+1,0);
                                msgrcv(mid,&name,1024,1,0);
                        }
                        else{
                                printf("Nazwa poprawna\n");
                                strcpy(wrongN.msg,"1");
                                wrongN.type = 4;
                                msgsnd(mid,&wrongN,strlen(wrongN.msg)+1,0);
                        }
                }
                wrongname =1;
                msgrcv(mid, &ident, 1024,2,0);
                while(wrongident ==1){
                        for(int i = 0;i<16;i++){
                                trialChannel = msgget(atoi(ident.msg),0600|IPC_CREAT);
                                trialRcvChannel = msgget(atoi(ident.msg)+100,0600|IPC_CREAT);
                                if (strcmp(ident.msg,idents[i])==0 || trialChannel == -1 || trialRcvChannel == -1){
                                        wrongident = 1;
                                        break;
                                }
                                else{
                                        wrongident = 0;
                                }
                        }
                        if (wrongident == 1){
                                printf("Czekam na nowy identyfikator...\n");
                                strcpy(wrongI.msg,"-1");
                                wrongI.type = 4;
                                msgsnd(mid,&wrongI,strlen(wrongI.msg)+1,0);
                                msgrcv(mid,&ident,1024,1,0);
                        }
                        else{
                                printf("Identyfikator poprawny\n");
                                strcpy(wrongI.msg,"1");
                                wrongI.type = 4;
                                msgsnd(mid,&wrongI,strlen(wrongI.msg)+1,0);
                        }
                }
                wrongident =1;
                msgctl(trialChannel,IPC_RMID,0);

                msgrcv(mid, &types,1024,3,0);
                msgrcv(mid, &subscript, 1024,3,0);
                msgrcv(mid, &rcvWay,1024,4,0);


                strcpy(idents[*accountsNum],ident.msg); //zapisanie identyfikatora do aktualnego klienta
                clientChannels[*accountsNum] = msgget(atoi(ident.msg),0600|IPC_CREAT); //utworzenie kanalu dla klienta
                rcvChannels[*accountsNum] = msgget(atoi(ident.msg)+100,0600|IPC_CREAT);
                strcpy(names[*accountsNum],name.msg); //zapisanie nazwy klienta

                if (msgTypes[atoi(types.msg)]==1){
                        existalready = 1;  //sprawdzanie czy taki typ juz istnieje
                }
                currentType = atoi(types.msg);

                if(existalready == 0){
                        msgTypes[currentType] = 1;      //jezeli nie, to go utworz
                        msgTypesSubs[*accountsNum][currentType] = atoi(subscript.msg); //i subskrybuj kanal
                        *msgTypesCounter+=1; //dodano kolejny typ wiadomosci
                        strcpy(typeComment,"Utworzono nowy typ wiadomosci: ");
                        strcat(typeComment,types.msg);
                        strcpy(newtyp.msg, typeComment);
                        newtyp.type = 9;
                        for(int user = 0;user <= *accountsNum;user++){
                                msgsnd(clientChannels[user],&newtyp,strlen(newtyp.msg)+1,0);
                        }
                }
                else{
                        msgTypesSubs[*accountsNum][currentType] = atoi(subscript.msg); //subskrybuj wczesniej stworzony kanal
                }

                rcvWays[*accountsNum][currentType] = atoi(rcvWay.msg);

                printf("Dolaczyl uzytkownik:%s\n",names[*accountsNum]);
                printf("Jego identyfikator: %s\n",idents[*accountsNum]);
                printf("Subskrybowany kanał: %s\n",types.msg);
                printf("Typ subskrypcji: %s\n",subscript.msg);
                printf("Tryb: %s\n",rcvWay.msg);
                *NumOfAccounts+=1;
                printf("Liczba podlaczonych uzytkownikow: %d\n",*NumOfAccounts);

        }
    }
    else{
        proces2 = fork();
        if(proces2 == 0){
            int value1 = -1;
            char message[64];
            while(1){
                for(int user = 0;user <16;user++){
                    for(int channel = 1; channel < 21;channel++){
                        if(msgTypesSubs[user][channel] != 0 && strcmp(names[user]," ") != 0){ //jezeli nadawca subskrybuje, sprawdz czy nie wyslal


                                    value1 = msgrcv(rcvChannels[user],&comunicate,1024, channel,IPC_NOWAIT); //odczytaj wiadomosc

                                    if(value1 != -1){
                                        printf("%d.  %s: %s\n",comunicate.type,names[user],comunicate.msg);
                                        sprintf(message,"%ld",channel);
                                        strcat(message,". ");
                                        strcat(message,names[user]);
                                        strcat(message,": ");
                                        strcat(message,comunicate.msg);
                                        strcpy(comunicate.msg,message);
                                        for(int rcvChan = 0;rcvChan <16;rcvChan++){
                                            if(msgTypesSubs[rcvChan][channel] > 0){ //jezeli odbiorca subskrybuje, wyslij

                                                msgsnd(clientChannels[rcvChan], &comunicate,strlen(comunicate.msg)+1,0);
                                                msgTypesSubs[rcvChan][channel] -= 1;
                                            }
                                            else if(msgTypesSubs[rcvChan][channel] == -1){
                                                    msgsnd(clientChannels[rcvChan], & comunicate,strlen(comunicate.msg)+1,0);
                                            }
                                        }
                                        value1 = -1;
                                    }
                        }
                    }
                }
            }
        }
        else{
            proces3 = fork();
            if (proces3 == 0){
            char comment[64];
            int valOfMsg = -1;
            int value = -1;
            struct msgbuf typeChange, typing,typeSubs, rcvAsync, deleteAcc;
            while(1){
                    for(int user = 0;user<16;user++){
                            if(strcmp(names[user]," ") != 0){
                                            valOfMsg = msgrcv(rcvChannels[user],&deleteAcc,1024,996,IPC_NOWAIT);
                                            if(valOfMsg != -1){
                                                for(int i = 0;i <20;i++){
                                                        msgTypesSubs[user][i] = 0;
                                                }
                                                printf("Uzytkownik %s opuscil serwer\n",names[user]);
                                                strcpy(idents[user]," ");
                                                strcpy(names[user]," ");
                                                msgctl(clientChannels[user],IPC_RMID,0);
                                                msgctl(rcvChannels[user],IPC_RMID,0);
                                                NumOfAccounts -= 1;

                                            valOfMsg = -1;
                                             }


                                            value = msgrcv(rcvChannels[user],&typeChange,1024,999,IPC_NOWAIT);

                                            if(value != -1){
                                                msgrcv(rcvChannels[user],&typeSubs,1024,998,0);
                                                msgrcv(rcvChannels[user],&rcvAsync,1024,997,0);
                                                if(msgTypes[atoi(typeChange.msg)] == 1){ //jezeli typ juz istnieje
                                                    msgTypesSubs[user][atoi(typeChange.msg)] = atoi(typeSubs.msg);
                                                    rcvWays[user][atoi(typeChange.msg)] = atoi(rcvAsync.msg);
                                                }
                                                else{
                                                    msgTypes[atoi(typeChange.msg)] = 1;
                                                    msgTypesSubs[user][atoi(typeChange.msg)] = atoi(typeSubs.msg);
                                                    rcvWays[user][atoi(typeChange.msg)] = atoi(rcvAsync.msg);
                                                    printf("Ustawiono nowy typ %d dla %d\n",atoi(typeChange.msg),clientChannels[user]);

                                                    strcpy(comment,"Utworzono nowy typ wiadomosci: ");
                                                    strcat(comment,typeChange.msg);
                                                    strcpy(typing.msg, comment);
                                                    typing.type = 9;
                                                    for(int user = 0;user < 16;user++){
                                                            if(strcmp(names[user]," ")!= 0){
                                                                msgsnd(clientChannels[user],&typing,strlen(typing.msg)+1,0);
                                                            }
                                                    }

                                                }


                                                value = -1;
                                         }
                            }


                    }
            }
            }
            else{
                    char ending[64];
                    printf("Wpisz exit zeby zamknac serwer:\n");
                    scanf("%s",ending);
                    while(strcmp(ending,"exit") != 0){
                            scanf("%s",ending);
                            printf("%s",ending);
                    }
                    kill(proces1, SIGKILL);
                    kill(proces2,SIGKILL);
                    kill(proces3,SIGKILL);
                    exit(0);
            }

        }
    }


}

                             