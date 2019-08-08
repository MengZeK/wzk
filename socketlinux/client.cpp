#include <netinet/in.h>
#include <sys/types.h>    
#include <sys/socket.h>    
#include <stdio.h>        
#include <stdlib.h>       
#include <string.h>      
#include <time.h>                
#include <arpa/inet.h>
 
#define SERVER_PORT 6666
#define BUFFER_SIZE 1024
 
int main(int argc,char **argv)
{
 if(argc!=2)
  {
      printf("参数错误，清输入两个参数\n");
     exit(1);
   }
  FILE *stream;
  struct sockaddr_in server_addr;
   bzero(&server_addr,sizeof(server_addr)); //把一段内存区的内容全部设置为0
   server_addr.sin_family = AF_INET;    //internet协议族
   server_addr.sin_addr.s_addr = inet_addr(argv[1]);
   server_addr.sin_port = htons(SERVER_PORT);   
   int sfd;
   sfd=socket(AF_INET,SOCK_STREAM,0);
   if(sfd<0)
    {
      printf("socket error\n");
      exit(0);
    }
 
   if(connect(sfd,(struct sockaddr*)&server_addr,sizeof(server_addr)) < 0)
    {
        printf("Can Not Connect To %s\n",argv[1]);
        exit(1);
    }
 
    char buffer[BUFFER_SIZE];
    bzero(buffer,BUFFER_SIZE);
    int length = recv(sfd,buffer,BUFFER_SIZE,0);
    if(length < 0)
     {
       printf("Recieve Data From Server %s Failed!\n", argv[1]);
       exit(1);
     }
 
    printf("\n%s\n",buffer);
    bzero(buffer,BUFFER_SIZE);
   // fgets(buffer,1024,stdin);
   // char filename[100];
   gets(buffer); 
   //打开文件流
    if((stream=fopen(buffer,"r"))==NULL)
     {
       printf("the file was not opened\n");
       exit(1);
     }
    bzero(buffer,BUFFER_SIZE);
    printf("正在传输...\n");
    int len=0;
    //不断读取并发送数据
    while((len=fread(buffer,1,1024,stream))>0)
     {
      // printf("len=%d\n",len);
       if(send(sfd,buffer,len,0)<0)
         {
            printf("send file error\n");
            break;
          }
         bzero(buffer,BUFFER_SIZE);
     }
    if(fclose(stream))
     {
       printf("file close error\n");
       exit(1);
     }
    close(sfd);
    return 0;
}