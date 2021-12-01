#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/shm.h>
#include <signal.h>
#define MAIN 1001

int main(int argc, char* argv[]){


struct msgbuf{
    long type;
    char msg[1024];
}name, ident, types, comunicate, newtyp,wrongI, subs, rcvWay;


    int *TypesNum;
    int shmTypesNum = shmget(IPC_PRIVATE,sizeof(int),0600|IPC_CREAT);
    TypesNum = (int *)shmat(shmTypesNum,NULL,0);
    *TypesNum = 0;

    int shmSubTypes = shmget(IPC_PRIVATE,sizeof(int)*20,0600|IPC_CREAT);
    int *subTypes = (int*)shmat(shmSubTypes,NULL,0);

    int shmRcvTypes = shmget(IPC_PRIVATE,sizeof(int)*20,0600|IPC_CREAT);
    int *rcvTypes = (int*)shmat(shmRcvTypes,NULL,0);


    int mid = msgget(MAIN, 0600 | IPC_CREAT);

    name.type =1;
    ident.type = 2;
    types.type = 3;
    subs.type = 3;

    printf("Podaj nazwe:\n");
    scanf("%s",name.msg);

    msgsnd(mid, &name, strlen(name.msg) + 1, 0);
    msgrcv(mid, &name, 1024,4,0);
    while(strcmp(name.msg,"-1")==0){
        printf("Nazwa jest juz zajeta! Podaj inna:\n");
        scanf("%s",name.msg);
        name.type = 1;
        msgsnd(mid,&name,strlen(name.msg)+1,0);
        msgrcv(mid,&name,1024,4,0);
    }


    printf("Podaj identyfikator:\n");
    scanf("%s",ident.msg);

    msgsnd(mid, &ident, strlen(ident.msg) + 1, 0);
    msgrcv(mid, &wrongI, 1024,4,0);
    while(strcmp(wrongI.msg,"-1")==0){
        printf("Identyfikator niepoprawny! Podaj inny:\n");
        scanf("%s",ident.msg);
        ident.type = 1;
        msgsnd(mid,&ident,strlen(ident.msg)+1,0);
        msgrcv(mid,&wrongI,1024,4,0);
    }
    ident.type = 2;

    int memory = shmget(IPC_PRIVATE,sizeof(int),0600|IPC_CREAT);
    int *channel;
    channel = (int*)shmat(memory,NULL,0);
    *channel = msgget(atoi(ident.msg),0600|IPC_CREAT);

    int sndMemory = shmget(IPC_PRIVATE,sizeof(int),0600|IPC_CREAT);
    int *sndChannel;
    sndChannel = (int*)shmat(sndMemory,NULL,0);
    *sndChannel = msgget(atoi(ident.msg)+100,0600|IPC_CREAT);




    printf("Podaj typ wiadomosci:\n");
    scanf("%s",types.msg);

    while(atoi(types.msg) > 20 || atoi(types.msg) < 1){
        printf("Niepoprawny typ! Wpisz liczbe 1-20\n");
        scanf("%s",types.msg);
    }

    msgsnd(mid, &types, strlen(types.msg)+1,0);


    printf("Podaj rodzaj subskrypcji: liczbe wiadomosci lub -1, jezeli ma byc ona ciagla\n");
    scanf("%s",subs.msg);
    msgsnd(mid, &subs,strlen(subs.msg)+1,0);

    subTypes[atoi(types.msg)] = atoi(subs.msg);
    *TypesNum = 1;

    printf("W jaki sposob chcesz odbierac wiadomosci? wpisz 1, jezeli asynchronicznie, lub 0, jezeli synchronicznie\n");
    scanf("%s",rcvWay.msg);
    while(strcmp(rcvWay.msg,"1") != 0 && strcmp(rcvWay.msg,"0") != 0){
            printf("Niepoprawny komunikat! Wpisz 1 lub 0:\n");
            scanf("%s",rcvWay.msg);
    }


    rcvWay.type = 4;
    msgsnd(mid,&rcvWay,strlen(rcvWay.msg)+1,0);
    rcvTypes[atoi(types.msg)] = atoi(rcvWay.msg);


    printf("Dolaczono, kanal: %d\n", *channel);


    struct msgbuf klientCom;
    int newTypeCreated,newMessageAsynch,proces;
    proces= fork();
    if(proces==0){
            while(1){
                newTypeCreated = msgrcv(*channel,&newtyp,1024,9,IPC_NOWAIT);
                if( newTypeCreated != -1){
                    printf("%s\n",newtyp.msg);
                }
                for(int x =1;x<20;x++){
                        if(rcvTypes[x] == 1){
                            newMessageAsynch = msgrcv(*channel,&klientCom,1024,x,IPC_NOWAIT);
                            if(newMessageAsynch != -1){
                                    printf("%s\n",klientCom.msg);
                                    if(subTypes[x] != -1){
                                        subTypes[x] -= 1;
                                    }

                            }
                        }
                }
            }
    }


    char polecenie[64];
    char wiadomosc[64];
    int typo = 0;
    int subbing = 0;
    int rcvAS;
    int isSubbed = 0;
    struct msgbuf typeSubs,rcvAsync;
    while(1){
            printf("Co chcesz zrobic? wpisz send, change, read lub exit:\n");
            scanf("%s",polecenie);
            if(strcmp(polecenie,"send") == 0){
                    for(int i = 0;i < 20;i++){
                            if(subTypes[i] > 0 || subTypes[i] == -1){
                                    isSubbed = 1;
                                    break;
                            }
                            else{
                                    isSubbed = 0;
                            }
                    }
                    if(isSubbed == 0){
                            printf("Nie subskrybujesz zadnego typu!\n");
                            continue;
                    }

                    printf("Podaj tresc wiadomosci:\n");
                    scanf("%s",klientCom.msg);
                    printf("Podaj typ:\n");
                    scanf("%d",&typo);
                    while(1){
                            if(typo > 20 || typo < 1){
                                printf("Niepoprawny typ! Wpisz liczbe 1-20\n");
                                scanf("%d",&typo);
                                continue;
                            }

                            if(subTypes[typo] > 0 || subTypes[typo] == -1 || typo == 512){
                                    break;
                            }
                            else{
                                    printf("Typ nie jest subskrybowany! Podaj inny typ\n");
                                    scanf("%d",&typo);
                            }
                            if(typo == 512){
                                    continue;
                            }
                    }

                    klientCom.type = typo;
                    isSubbed = 0;
                    msgsnd(*sndChannel,&klientCom,strlen(klientCom.msg)+1,0);
            }
            else if(strcmp(polecenie,"read")==0){
                    for(int i = 0;i < 20;i++){
                            if((subTypes[i] > 0 || subTypes[i] == -1)&& rcvTypes[i] == 0){
                                    isSubbed = 1;
                                    break;
                            }
                            else{
                                    isSubbed = 0;
                            }
                    }
                    if(isSubbed == 0){
                            printf("Nie subskrybujesz zadnego typu synchronicznie!\n");
                            continue;
                    }

                    printf("Z ktorego kanalu chcesz czytac?\n");
                    scanf("%d",&typo);
                    while(1){
                            if(rcvTypes[typo] == 1){
                                    printf("Typ jest odbierany asynchronicznie! Podaj inny typ\n");
                                    scanf("%d",&typo);
                                    continue;
                            }
                            if(typo > 20 || typo < 1){
                                printf("Niepoprawny typ! Wpisz liczbe 1-20\n");
                                scanf("%d",&typo);
                                continue;
                            }

                            if(subTypes[typo] > 0 || subTypes[typo] == -1){
                                    break;
                            }
                            else{
                                    printf("Typ nie jest subskrybowany! Podaj inny typ\n");
                                    scanf("%d",&typo);
                            }
                    }

                    msgrcv(*channel,&klientCom,1024,typo,0);
                    printf("%s\n",klientCom.msg);
                    if(subTypes[typo] != -1){
                        subTypes[typo] -= 1;
                    }
            }
            else if(strcmp(polecenie,"change")==0){
                    printf("Jaki typ chcesz zmienic?\n");
                    scanf("%d",&typo);

                    while(typo > 20 || typo < 1){
                            printf("Niepoprawny typ! Wpisz liczbe 1-20\n");
                            scanf("%d",&typo);
                    }

                    printf("Jaki typ subskrypcji?\n");
                    scanf("%d",&subbing);
                    subTypes[typo]= subbing;

                    printf("Tryb asynchroniczny - 1, synchroniczny - 0:\n");
                    scanf("%d",&rcvAS);
                    isSubbed = 0;
                    klientCom.type = 999;
                    typeSubs.type = 998;
                    rcvAsync.type = 997;


                    rcvTypes[typo] = rcvAS;
                    sprintf(klientCom.msg,"%ld",typo);
                    sprintf(typeSubs.msg,"%ld",subbing);
                    sprintf(rcvAsync.msg,"%ld",rcvAS);
                    msgsnd(*sndChannel,&klientCom,strlen(klientCom.msg)+1,0);
                    msgsnd(*sndChannel,&typeSubs,strlen(typeSubs.msg)+1,0);
                    msgsnd(*sndChannel,&rcvAsync,strlen(rcvAsync.msg)+1,0);

            }
            else if(strcmp(polecenie,"exit")==0){
                    printf("Zakonczenie pracy z serwerem...\n");
                    klientCom.type = 996;
                    strcpy(klientCom.msg,"exit");
                    msgsnd(*sndChannel,&klientCom,strlen(klientCom.msg)+1,0);
                    kill(proces,SIGKILL);
                    exit(0);
            }
    }

    }

