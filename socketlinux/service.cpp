#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#define SERVER_PORT 6666
#define LISTEN_QUEUE 20
#define BUFFER_SIZE 1024
 
int main(int argc,char **argv)
{
      struct sockaddr_in server_addr;
        bzero(&server_addr,sizeof(server_addr));//全部置零
          //设置地址相关的属性
      server_addr.sin_family=AF_INET;
       server_addr.sin_addr.s_addr=htons(INADDR_ANY);
      server_addr.sin_port=htons(SERVER_PORT);      
       //创建套接字
      int server_socket=socket(AF_INET,SOCK_STREAM,0);
      if(server_socket<0) 
      {
          printf("socket create error\n");
          exit(1);
      }
      //绑定端口
       if(bind(server_socket,(struct sockaddr*)&server_addr,sizeof(server_addr)))
       {
           printf("bind error\n");
           exit(1);
       }
       //服务器端监听
      if(listen(server_socket,LISTEN_QUEUE))
      {
          printf("Server listen error\n");
          exit(1);
      }
      //服务器端一直运行
       while(1)
       {
           pid_t pid;
           struct sockaddr_in client_addr;
           socklen_t length=sizeof(client_addr);
          
           //accept返回一个新的套接字与客户端进行通信
            int new_server_socket=accept(server_socket,(struct sockaddr*)&client_addr,&length);
//1*begin****************************************************************************
            if(new_server_socket==-1)
            {
                printf("accept error\n");
                continue;
            }
            else
            {
                 printf("客户端%s连接成功\n",inet_ntoa(client_addr.sin_addr));
                 pid=fork();
//3*begin**运行子进程************************************************************
                                                                                                       if(pid==0)
                                                                                                       {
                                                                                                           int data_len,flag=0;
                                                                                                           char buffer[BUFFER_SIZE];
                                                                                                           // 定义文件流
                                                                                                                                                                                                        FILE *stream;
                                                                                                                                                                                                        bzero(buffer,BUFFER_SIZE);                                                                                                                                                                                                                                                               strcpy(buffer,"请输入要传输的文件的完整路径：");
                                                                                                                                                                                                        strcat(buffer,"\n");                                                                                                                                                                         send(new_server_socket,buffer,BUFFER_SIZE,0);
    bzero(buffer,BUFFER_SIZE);
//2*begin**服务器接受数据******************************************         
   if((stream=fopen("data","w"))==NULL)     
   {
       printf("file open error\n");                                                                     exit(1);    
   }
   else{
       bzero(buffer,BUFFER_SIZE);
   }                                                                                                                                                                                                // printf("正在接收来自%s的文件....\n",inet_ntoa(client_addr.sin_addr));                                                                                                                        //先将数据接受到缓冲区buffer中，再写入到新建文件中
   while(data_len=recv(new_server_socket,buffer,BUFFER_SIZE,0)) {
           flag++;
           if(flag==1)
           {
           printf("正在接收来自%s的文件....\n",inet_ntoa(client_addr.sin_addr));
           }
           if(data_len<0)
            {
            printf("接收错误\n");
            exit(1);
            }
            //向文件中写入数据
            int write_len=fwrite(buffer,sizeof(char),data_len,stream);  
            if(write_len>data_len)
            {
            printf("file write failed\n");
            exit(1);
            }
            bzero(buffer,BUFFER_SIZE);
            }
   if(flag>0)
       printf("%s的文件传送完毕\n",inet_ntoa(client_addr.sin_addr));
   if(flag==0)
       printf("%s的文件传输失败\n",inet_ntoa(client_addr.sin_addr));
   //2*end**服务器接受数据**************************************************** 
   // rename("data",inet_ntoa(client_addr.sin_addr)); 
       fclose(stream);
       rename("data",inet_ntoa(client_addr.sin_addr));
       exit(1);         
                                                                                                       }                                                                                        //3*end**运行子进程********************************************************* 
                                                                                                       else
                                                                                                       {
                                                                                                           close(new_server_socket);
                                                                                                       }
            }
//1*end**************************************************************************************
        
    close(new_server_socket);
       }
       return 0;
}
