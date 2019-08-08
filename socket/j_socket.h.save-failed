//j_socket.h
#ifndef J_SOCKET_H_INCLUDED
#define J_SOCKET_H_INCLUDED
#include <stdio.h>
#include <errno.h>
#include <winsock2.h>
#include <pthread.h>

#define INIT_ERROR 1
#define BIND_ERROR 2
#define LISTEN_ERROR 3
struct rec_args{
int * l;
SOCKET* s;
};
void* receive( void* args)
{
    char recvBuf[512];
    rec_args *a=(rec_args*)args;
    while(true)
    {
        recv(*(a->s),recvBuf,512,0);
        printf("receive message: %s\n",recvBuf);
        printf("111111\n");
        if(strcmp(recvBuf,"end")==0){break;}

    }
    closesocket(*(a->s));
    (*(a->l))--;
    printf("22222\n");
    return NULL;
}
class j_server
{
private:
    SOCKET Server_Sock;
    SOCKADDR_IN server_addr;
    SOCKADDR_IN client_addr;

    int max_num;
    int link_num=0;
    int error_num;

public:
    j_server(int port)
    {
        WSADATA wsa;
        /*初始化socket资源*/
        if (WSAStartup(MAKEWORD(1,1),&wsa) != 0)
        {
            error_num=INIT_ERROR;
            return;
        }

        if((Server_Sock = socket(AF_INET, SOCK_STREAM, 0))==-1)
        {
            error_num=INIT_ERROR;
            return;
        }
        ZeroMemory((char *)&server_addr,sizeof(server_addr));
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(port);           /*本地监听端口*/
        server_addr.sin_addr.s_addr = htonl(INADDR_ANY); /*有IP*/

        if(bind(Server_Sock,(struct sockaddr *)&server_addr,sizeof(server_addr))==-1)
        {
            error_num=BIND_ERROR;
            return;
        }
        if(listen(Server_Sock,5)==-1) //其中第二个参数代表能够接收的最多的连接数
        {
            error_num=LISTEN_ERROR;
            return;
        }
        max_num=20;

    }
    int j_listen()
    {
        int len=sizeof(SOCKADDR);
        while(true)
        {
            if(link_num>max_num)
            {
                Sleep(100);
                continue;
            }
            SOCKET Command_Sock  = accept(Server_Sock, (SOCKADDR*)&client_addr,&len);
            if(Command_Sock == INVALID_SOCKET)
            {
                printf("accept error !");
                closesocket(Command_Sock);
            }
            link_num++;
            pthread_t listen_p;
            int ret;
            rec_args a;
            a.l=&link_num;
            a.s=&Command_Sock;
            ret= pthread_create( &listen_p,  NULL, receive,(void *)&a  ); //参数：创建的线程id，线程参数，线程运行函数的起始地址，运行函数的参数
        }
        return 0;
    }

};
class j_client
{
private:
    SOCKET Client_Sock;
    SOCKADDR_IN server_addr;
    char sendBuf[512];
    int error_num;
public:

    j_client(char * server_addr_str,int port)
    {
        WSADATA wsa;
        /*初始化socket资源*/
        if (WSAStartup(MAKEWORD(1,1),&wsa) != 0)
        {
            error_num=INIT_ERROR;
            return;   //代表失败
        }
        if((Client_Sock = socket(AF_INET, SOCK_STREAM, 0))==-1)
        {
            error_num=INIT_ERROR;
            return;   //代表失败
        }
        server_addr.sin_addr.S_un.S_addr=inet_addr(server_addr_str);
        server_addr.sin_family=AF_INET;
        server_addr.sin_port=htons(port);
        if(connect(Client_Sock,(SOCKADDR*)&server_addr,sizeof(SOCKADDR)) ==-1)
        {
            printf("connect error !");
            //printf( "%d ", WSAGetLastError());
        }
    }
    int j_send()
    {
        while(true)
        {
            printf("input message:  ");
            scanf("%s",sendBuf);
            if(send(Client_Sock,sendBuf,strlen(sendBuf)+1,0)!=(strlen(sendBuf)+1))
            {
                printf("send error !");
                //printf( "%d ", WSAGetLastError());
            }
        }
        return 0;
    }
    int j_close()
    {
        closesocket(Client_Sock);
        WSACleanup();
    }
};



#endif // J_SOCKET_H_INCLUDED
