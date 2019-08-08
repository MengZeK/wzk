//main.cpp
#include "j_socket.h"
#include <stdio.h>
#include <pthread.h>
static int port=21;
j_server* ser;
void* main_listen( void* args)
{
    ser=new j_server(port);
    ser->j_listen();
}
int main()
{
    static pthread_t listen_p;
    int ret;
    ret= pthread_create( &listen_p, NULL, main_listen, NULL ); //参数：创建的线程id，线程参数，线程运行函数的起始地址，运行函数的参数
    if( ret != 0 ) //创建线程成功返回0
    {
        printf("pthread_create error:error_code=%d\n",ret );
    }
    static j_client* cli;
    cli =new j_client("127.0.0.1",port);
    cli->j_send();
    return 0;
}
